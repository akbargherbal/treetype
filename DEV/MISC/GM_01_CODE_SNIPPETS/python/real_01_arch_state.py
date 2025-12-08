#!/usr/bin/env python3
import argparse
import json
import os
import sys
import shutil
import datetime
import fnmatch
import re
import copy
from collections import defaultdict

# --- CONFIGURATION ---
STATE_FILE = "architecture.json"
BACKUP_FILE = "architecture.json.backup"
SESSION_FILE = ".session_start"  # [FIX] Added for CLI persistence
# Base ignores - will be augmented by .gitignore
IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', '.env', 'dist', 'build', '.idea', '.vscode', 'target', 'bin', 'obj'}
IGNORE_EXTS = {'.pyc', '.o', '.exe', '.so', '.dll', '.class', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot'}
SIGNIFICANT_SIZE_KB = 1

# --- COLORS ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- DEFAULT SCHEMA ---
DEFAULT_STATE = {
    "schema_version": "2.2",
    "metadata": {
        "project_name": "",
        "project_type": "Unknown",
        "last_updated": "",
        "phase": "survey",
        "total_sessions": 0,
        "scan_stats": {
            "total_files_scanned": 0,
            "significant_files_total": 0,
            "mapped_files_count": 0,
            "coverage_percentage": 0.0,
            "coverage_quality": 0.0
        },
        "session_history": []
    },
    "systems": {},
    "progress": {
        "systems_identified": 0,
        "systems_complete": 0,
        "estimated_overall_completeness": 0
    }
}

class StateManager:
    def __init__(self):
        self.data = self.load_state()
        self.ignore_patterns = self.load_gitignore()
        self.session_start_state = None

    def load_state(self):
        if not os.path.exists(STATE_FILE): return None
        try:
            with open(STATE_FILE, 'r') as f: return json.load(f)
        except json.JSONDecodeError:
            print(f"{Colors.FAIL}❌ Error: {STATE_FILE} is corrupted.{Colors.ENDC}")
            if os.path.exists(BACKUP_FILE):
                print(f"{Colors.WARNING}⚠️  Restoring from backup...{Colors.ENDC}")
                with open(BACKUP_FILE, 'r') as f: return json.load(f)
            sys.exit(1)

    def save_state(self):
        if not self.data: return
        self.data["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
        
        # Atomic Write Pattern
        if os.path.exists(STATE_FILE): shutil.copy(STATE_FILE, BACKUP_FILE)
        temp = STATE_FILE + ".tmp"
        with open(temp, 'w') as f: json.dump(self.data, f, indent=2)
        os.replace(temp, STATE_FILE)
        print(f"{Colors.GREEN}💾 State saved.{Colors.ENDC}")

    def init_project(self, name):
        if os.path.exists(STATE_FILE):
            if input(f"Overwrite {STATE_FILE}? (y/N): ").lower() != 'y': return
        
        self.data = copy.deepcopy(DEFAULT_STATE)
        
        self.data["metadata"]["project_name"] = name
        self.data["metadata"]["project_type"] = self.detect_project_type()
        self.save_state()
        print(f"{Colors.BLUE}🚀 Initialized project: {name}{Colors.ENDC}")
        print(f"{Colors.BLUE}   Detected type: {self.data['metadata']['project_type']}{Colors.ENDC}")

    def detect_project_type(self):
        """Infer project type from file signatures"""
        if os.path.exists("manage.py") or os.path.exists("wsgi.py"):
            return "Django Web Application"
        if os.path.exists("app.py") and os.path.exists("requirements.txt"):
            return "Flask Web Application"
        if os.path.exists("package.json"):
            with open("package.json") as f:
                try:
                    pkg = json.load(f)
                    if "express" in pkg.get("dependencies", {}):
                        return "Node.js/Express Application"
                except: pass
            return "Node.js Application"
        if os.path.exists("Cargo.toml"):
            return "Rust Project"
        if os.path.exists("go.mod"):
            return "Go Project"
        if os.path.exists("setup.py") or os.path.exists("pyproject.toml"):
            return "Python Package/Library"
        if os.path.exists("Dockerfile"):
            return "Containerized Application"
        return "Unknown"

    # --- METRICS & SCANNING ---
    def load_gitignore(self):
        """Parses .gitignore to augment IGNORE_DIRS"""
        patterns = set()
        if os.path.exists(".gitignore"):
            try:
                with open(".gitignore", "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            if line.endswith("/"):
                                IGNORE_DIRS.add(line.rstrip("/"))
                            patterns.add(line)
            except Exception:
                pass
        return patterns

    def is_ignored(self, path, name):
        if name in IGNORE_DIRS: return True
        if os.path.splitext(name)[1] in IGNORE_EXTS: return True
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(name, pattern): return True
        return False

    def scan_files(self):
        total, sig_total, sig_paths = 0, 0, set()
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if not self.is_ignored(os.path.join(root, d), d)]
            
            for file in files:
                if self.is_ignored(os.path.join(root, file), file): continue
                
                path = os.path.join(root, file)
                rel = os.path.relpath(path, ".").replace("\\", "/")
                if rel.startswith("./"): rel = rel[2:]
                
                total += 1
                try:
                    if os.path.getsize(path) / 1024 >= SIGNIFICANT_SIZE_KB:
                        sig_total += 1
                        sig_paths.add(rel)
                except OSError: pass
        return total, sig_total, sig_paths

    def calculate_coverage_quality(self, sig_paths, mapped):
        """Penalize test/doc files to get real architectural coverage"""
        core_mapped = [f for f in mapped if not any(x in f.lower() for x in ['test', 'doc', 'example', 'spec', '__pycache__'])]
        core_sig = [f for f in sig_paths if not any(x in f.lower() for x in ['test', 'doc', 'example', 'spec', '__pycache__'])]
        
        if not core_sig: return 0.0
        return round(len(core_mapped) / len(core_sig) * 100, 1)

    def update_stats(self):
        if not self.data: return
        total, sig_total, sig_paths = self.scan_files()
        
        mapped = set()
        systems = self.data.get("systems", {})
        for s in systems.values(): mapped.update(s.get("key_files", []))
        
        mapped_sig = len(sig_paths.intersection(mapped))
        cov = (mapped_sig / sig_total * 100) if sig_total > 0 else 0.0
        quality = self.calculate_coverage_quality(sig_paths, mapped)
        
        stats = self.data["metadata"]["scan_stats"]
        stats.update({
            "total_files_scanned": total,
            "significant_files_total": sig_total,
            "mapped_files_count": mapped_sig,
            "coverage_percentage": round(cov, 1),
            "coverage_quality": quality
        })
        
        prog = self.data["progress"]
        prog["systems_identified"] = len(systems)
        prog["systems_complete"] = len([s for s in systems.values() if s.get("completeness", 0) >= 85])
        if systems:
            prog["estimated_overall_completeness"] = round(sum(s.get("completeness", 0) for s in systems.values()) / len(systems), 1)
        self.save_state()

    # --- SESSION TRACKING ---
    def start_session(self):
        """Mark the beginning of a new session"""
        if not self.data: return
        
        # [FIX] Save baseline to file for CLI persistence
        with open(SESSION_FILE, 'w') as f:
            json.dump(self.data, f)
            
        self.session_start_state = copy.deepcopy(self.data)
        self.data["metadata"]["total_sessions"] += 1
        self.save_state() # [FIX] Persist the counter increment
        print(f"{Colors.BLUE}📍 Session {self.data['metadata']['total_sessions']} started{Colors.ENDC}")

    def end_session(self):
        """Record what happened in this session"""
        if not self.data: return
        
        # [FIX] Try to load from file if not in memory (CLI usage)
        if self.session_start_state is None and os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r') as f:
                    self.session_start_state = json.load(f)
            except json.JSONDecodeError:
                pass
        
        if not self.session_start_state:
            print(f"{Colors.WARNING}⚠️  No active session found (run session-start first).{Colors.ENDC}")
            return
        
        old_systems = set(self.session_start_state.get("systems", {}).keys())
        new_systems = set(self.data["systems"].keys())
        systems_added = len(new_systems - old_systems)
        
        old_files = set()
        for s in self.session_start_state.get("systems", {}).values():
            old_files.update(s.get("key_files", []))
        
        new_files = set()
        for s in self.data["systems"].values():
            new_files.update(s.get("key_files", []))
        
        files_mapped = len(new_files - old_files)
        
        old_insights = sum(len(s.get("insights", [])) for s in self.session_start_state.get("systems", {}).values())
        new_insights = sum(len(s.get("insights", [])) for s in self.data["systems"].values())
        insights_added = new_insights - old_insights
        
        session_id = self.data["metadata"]["total_sessions"]
        self.data["metadata"]["session_history"].append({
            "session_id": session_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "new_systems_found": systems_added,
            "new_files_mapped": files_mapped,
            "insights_added": insights_added
        })
        
        self.save_state()
        
        # [FIX] Cleanup session file
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
            
        print(f"{Colors.GREEN}✅ Session {session_id} recorded:{Colors.ENDC}")
        print(f"   Systems added: {systems_added}")
        print(f"   Files mapped: {files_mapped}")
        print(f"   Insights added: {insights_added}")

    # --- MODIFICATION COMMANDS ---
    def add_system(self, name):
        if not self.data: return
        if name in self.data["systems"]:
            print(f"{Colors.WARNING}⚠️  System '{name}' already exists.{Colors.ENDC}")
            return
        self.data["systems"][name] = {
            "description": "TODO",
            "completeness": 0,
            "clarity": "low",
            "key_files": [],
            "dependencies": [],
            "insights": [],
            "complexities": []
        }
        print(f"{Colors.GREEN}✅ Added system: {name}{Colors.ENDC}")
        self.save_state()

    def update_system(self, name, desc=None, comp=None, clarity=None):
        if name not in self.data["systems"]:
            print(f"{Colors.FAIL}❌ System '{name}' not found.{Colors.ENDC}")
            return
        
        sys = self.data["systems"][name]
        
        if desc:
            # Prevent newlines in descriptions (shell safety)
            if "\n" in desc:
                print(f"{Colors.FAIL}❌ Description cannot contain newlines. Use single-line descriptions.{Colors.ENDC}")
                return
            sys["description"] = desc
            
        if comp is not None: sys["completeness"] = int(comp)
        if clarity: sys["clarity"] = clarity
        print(f"{Colors.GREEN}✅ Updated metadata for: {name}{Colors.ENDC}")
        self.save_state()

    def map_files(self, name, files):
        if name not in self.data["systems"]:
            print(f"{Colors.FAIL}❌ System '{name}' not found.{Colors.ENDC}")
            return
        
        self.data["systems"][name]["key_files"].extend(files)
        self.data["systems"][name]["key_files"] = list(set(self.data["systems"][name]["key_files"]))
        print(f"{Colors.GREEN}✅ Mapped {len(files)} files to: {name}{Colors.ENDC}")
        self.update_stats()

    def similar_text(self, a, b, threshold=0.8):
        """Simple word overlap check for duplicate detection"""
        words_a = set(a.lower().split())
        words_b = set(b.lower().split())
        if not words_a or not words_b: return False
        overlap = len(words_a & words_b) / max(len(words_a), len(words_b))
        return overlap > threshold

    def add_insight(self, name, text):
        if name not in self.data["systems"]: return
        
        # Check for duplicates
        existing = self.data["systems"][name]["insights"]
        if any(self.similar_text(text, e) for e in existing):
            print(f"{Colors.WARNING}⚠️  Similar insight already exists. Skipping.{Colors.ENDC}")
            return
        
        existing.append(text)
        print(f"{Colors.GREEN}✅ Added insight to: {name}{Colors.ENDC}")
        self.save_state()

    def add_dependency(self, name, target, reason):
        if name not in self.data["systems"]:
            print(f"{Colors.FAIL}❌ System '{name}' not found.{Colors.ENDC}")
            return
        
        # Check if target exists
        if target not in self.data["systems"]:
            print(f"{Colors.WARNING}⚠️  Target system '{target}' doesn't exist yet.{Colors.ENDC}")
            if input("Create it now? (y/N): ").lower() == 'y':
                self.add_system(target)
            else:
                return
        
        self.data["systems"][name]["dependencies"].append(
            {"system": target, "reason": reason}
        )
        print(f"{Colors.GREEN}✅ Linked {name} -> {target}{Colors.ENDC}")
        self.save_state()

    # --- VALIDATION ---
    def validate_schema(self):
        """Check for data quality issues"""
        if not self.data: return []
        
        errors = []
        systems = self.data.get("systems", {})
        
        # 1. Check required fields
        for name, sys in systems.items():
            if not sys.get("description") or sys["description"] == "TODO":
                errors.append(f"{name}: Missing or placeholder description")
            if not sys.get("key_files"):
                errors.append(f"{name}: No key_files listed")
            if not sys.get("insights"):
                errors.append(f"{name}: No insights recorded")
        
        # 2. Check dependency references
        for name, sys in systems.items():
            for dep in sys.get("dependencies", []):
                if dep["system"] not in systems:
                    errors.append(f"{name}: References non-existent system '{dep['system']}'")
        
        # 3. Check for orphaned significant files
        total, sig_total, sig_paths = self.scan_files()
        mapped = set()
        for sys in systems.values():
            mapped.update(sys["key_files"])
        
        orphans = sig_paths - mapped
        # Filter out test/doc files from orphan warnings
        core_orphans = [f for f in orphans if not any(x in f.lower() for x in ['test', 'doc', 'example', 'spec'])]
        
        if core_orphans and len(core_orphans) > 5:
            errors.append(f"Found {len(core_orphans)} unmapped significant files (sample: {list(core_orphans)[:5]})")
        
        return errors

    # --- REPORTING ---
    def print_status(self):
        self.update_stats()
        meta = self.data["metadata"]
        stats = meta["scan_stats"]
        cov_color = Colors.GREEN if stats['coverage_percentage'] >= 90 else Colors.WARNING
        
        print(f"\n{Colors.HEADER}=== 🏛️  PROJECT STATE ==={Colors.ENDC}")
        print(f"Project:  {Colors.BOLD}{meta.get('project_name')}{Colors.ENDC} ({meta.get('project_type', 'Unknown')})")
        print(f"Phase:    {meta.get('phase', 'survey')}")
        print(f"Sessions: {meta.get('total_sessions', 0)}")
        print(f"Coverage: {cov_color}{stats['coverage_percentage']}%{Colors.ENDC} ({stats['mapped_files_count']}/{stats['significant_files_total']} significant files)")
        print(f"Quality:  {stats['coverage_quality']}% (excluding tests/docs)")
        print(f"Systems:  {self.data['progress']['systems_identified']} identified, {self.data['progress']['systems_complete']} complete")
        
        # Check stopping criteria
        if stats['coverage_percentage'] >= 90:
            print(f"\n{Colors.GREEN}🎯 Gate A: Coverage threshold met (90%+){Colors.ENDC}")
        
        if len(meta.get('session_history', [])) >= 3:
            last_3 = meta['session_history'][-3:]
            if all(s['new_systems_found'] == 0 and s['new_files_mapped'] < 3 for s in last_3):
                print(f"\n{Colors.GREEN}🎯 Gate B: Diminishing returns detected (3 low-yield sessions){Colors.ENDC}")

    def list_systems(self):
        print(f"\n{Colors.HEADER}=== 🗺️  SYSTEMS ==={Colors.ENDC}")
        for name, s in sorted(self.data["systems"].items(), key=lambda x: x[1]['completeness'], reverse=True):
            print(f"{name:<30} | {s['completeness']:>3}% | {len(s['key_files']):>2} files | {len(s['insights']):>2} insights")

    def show_system(self, name, summary=False):
        if name not in self.data["systems"]:
            print(f"{Colors.FAIL}System not found.{Colors.ENDC}")
            return
        
        sys = self.data["systems"][name]
        
        if summary:
            # Condensed view for Phase 2
            output = {
                "description": sys["description"],
                "completeness": sys["completeness"],
                "dependencies": [d["system"] for d in sys.get("dependencies", [])],
                "top_insights": sys.get("insights", [])[:3]
            }
            print(json.dumps(output, indent=2))
        else:
            print(json.dumps(sys, indent=2))

    def sanitize_for_mermaid(self, name):
        """Remove all non-alphanumeric except underscores"""
        return re.sub(r'[^\w]', '_', name)

    def export_graph(self):
        """Generates Mermaid.js graph syntax"""
        print(f"\n{Colors.HEADER}=== 🕸️  DEPENDENCY GRAPH (Mermaid) ==={Colors.ENDC}")
        print("```mermaid")
        print("graph TD")
        
        # Nodes
        for name in self.data["systems"].keys():
            safe_name = self.sanitize_for_mermaid(name)
            print(f"  {safe_name}[\"{name}\"]")
        
        # Edges
        for name, s in self.data["systems"].items():
            source = self.sanitize_for_mermaid(name)
            for dep in s.get("dependencies", []):
                target = self.sanitize_for_mermaid(dep["system"])
                reason = (dep['reason'][:30] + '..') if len(dep['reason']) > 30 else dep['reason']
                print(f"  {source} -->|{reason}| {target}")
        print("```")

    def print_coverage_detail(self):
        """Show coverage by directory"""
        if not self.data: return
        
        total, sig_total, sig_paths = self.scan_files()
        mapped = set()
        for s in self.data["systems"].values():
            mapped.update(s["key_files"])
        
        # Group by directory
        dir_stats = defaultdict(lambda: {"total": 0, "mapped": 0, "files": []})
        
        for path in sig_paths:
            dir_name = os.path.dirname(path) or "."
            dir_stats[dir_name]["total"] += 1
            if path in mapped:
                dir_stats[dir_name]["mapped"] += 1
            else:
                dir_stats[dir_name]["files"].append(path)
        
        print(f"\n{Colors.HEADER}=== 📊 COVERAGE BY DIRECTORY ==={Colors.ENDC}")
        for dir_name in sorted(dir_stats.keys()):
            stat = dir_stats[dir_name]
            pct = (stat["mapped"] / stat["total"] * 100) if stat["total"] > 0 else 0
            bar_filled = int(pct / 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            
            if pct >= 90:
                icon = "✅"
            elif pct >= 60:
                icon = "⚠️ "
            else:
                icon = "❌"
            
            print(f"{icon} {dir_name:<30} [{bar}] {pct:>3.0f}% ({stat['mapped']}/{stat['total']})")
        
        # Show top unmapped files
        all_unmapped = []
        for stat in dir_stats.values():
            all_unmapped.extend(stat["files"])
        
        if all_unmapped:
            print(f"\n{Colors.HEADER}=== 📄 TOP UNMAPPED FILES ==={Colors.ENDC}")
            # Sort by line count (approximate by file size)
            unmapped_with_size = []
            for f in all_unmapped[:20]:  # Limit to 20
                try:
                    size = os.path.getsize(f)
                    unmapped_with_size.append((f, size))
                except OSError:
                    pass
            
            unmapped_with_size.sort(key=lambda x: x[1], reverse=True)
            for i, (f, size) in enumerate(unmapped_with_size[:10], 1):
                kb = size / 1024
                print(f"  {i}. {f:<50} ({kb:.1f} KB)")

# --- CLI ---
def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init").add_argument("name")
    sub.add_parser("status")
    sub.add_parser("list")
    sub.add_parser("graph")
    sub.add_parser("validate")
    sub.add_parser("coverage")
    
    sub.add_parser("session-start")
    sub.add_parser("session-end")
    
    show = sub.add_parser("show")
    show.add_argument("name")
    show.add_argument("--summary", action="store_true")
    
    sub.add_parser("add").add_argument("name")
    
    upd = sub.add_parser("update")
    upd.add_argument("name")
    upd.add_argument("--desc")
    upd.add_argument("--comp", type=int)
    upd.add_argument("--clarity")

    map_cmd = sub.add_parser("map")
    map_cmd.add_argument("name")
    map_cmd.add_argument("files", nargs="+")

    ins = sub.add_parser("insight")
    ins.add_argument("name")
    ins.add_argument("text")

    dep = sub.add_parser("dep")
    dep.add_argument("name")
    dep.add_argument("target")
    dep.add_argument("reason")

    args = parser.parse_args()
    mgr = StateManager()

    if args.cmd == "init":
        mgr.init_project(args.name)
    elif args.cmd == "status":
        mgr.print_status()
    elif args.cmd == "list":
        mgr.list_systems()
    elif args.cmd == "graph":
        mgr.export_graph()
    elif args.cmd == "validate":
        errors = mgr.validate_schema()
        if errors:
            print(f"\n{Colors.FAIL}❌ Validation Errors:{Colors.ENDC}")
            for e in errors:
                print(f"  • {e}")
        else:
            print(f"\n{Colors.GREEN}✅ Validation passed. Ready for Phase 2.{Colors.ENDC}")
    elif args.cmd == "coverage":
        mgr.print_coverage_detail()
    elif args.cmd == "session-start":
        mgr.start_session()
    elif args.cmd == "session-end":
        mgr.end_session()
    elif args.cmd == "show":
        mgr.show_system(args.name, args.summary)
    elif args.cmd == "add":
        mgr.add_system(args.name)
    elif args.cmd == "update":
        mgr.update_system(args.name, args.desc, args.comp, args.clarity)
    elif args.cmd == "map":
        mgr.map_files(args.name, args.files)
    elif args.cmd == "insight":
        mgr.add_insight(args.name, args.text)
    elif args.cmd == "dep":
        mgr.add_dependency(args.name, args.target, args.reason)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()