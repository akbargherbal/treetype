#!/usr/bin/env python3
"""
treetype Metadata Builder
Scans public/ directory and generates metadata.json index
"""

import json
from pathlib import Path
from datetime import datetime


def generate_snippet_id(filepath):
    """Generate stable ID from filepath"""
    # Use relative path from public/ as base
    rel_path = filepath.relative_to(Path("public"))
    # Remove .json extension and replace / with -
    id_str = str(rel_path.with_suffix("")).replace("/", "-")
    return id_str


def estimate_difficulty(line_count, typeable_chars):
    """Estimate difficulty based on snippet characteristics"""
    if line_count <= 5 or typeable_chars <= 50:
        return "beginner"
    elif line_count <= 15 or typeable_chars <= 200:
        return "intermediate"
    else:
        return "advanced"


def extract_tags(filepath, snippet_data):
    """Extract tags from filename and content"""
    tags = []

    # Add language as tag
    language = snippet_data.get("language", "")
    if language:
        tags.append(language)

    # Extract from filename (e.g., "django_views.json" -> ["django", "views"])
    stem = filepath.stem
    words = stem.replace("_", "-").split("-")
    tags.extend([w.lower() for w in words if len(w) > 2])

    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)

    return unique_tags[:5]  # Limit to 5 tags


def get_snippet_name(filepath):
    """Generate human-readable name from filename"""
    stem = filepath.stem
    # Convert snake_case to Title Case
    words = stem.replace("_", " ").split()
    return " ".join(word.capitalize() for word in words)


def analyze_snippet(filepath):
    """Load and analyze a snippet JSON file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Calculate stats
        line_count = len(data.get("lines", []))
        total_typeable_chars = sum(
            len(line.get("typing_sequence", "")) for line in data.get("lines", [])
        )

        # Get file modification time
        mtime = filepath.stat().st_mtime
        date_added = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

        # Generate metadata
        snippet_id = generate_snippet_id(filepath)

        # Compute relative path and prepend "snippets/" for backward compatibility with frontend routing
        rel_path = filepath.relative_to(Path("public"))
        legacy_path = f"snippets/{rel_path}"

        return {
            "id": snippet_id,
            "name": get_snippet_name(filepath),
            "language": data.get("language", "unknown"),
            "path": legacy_path,
            "lines": line_count,
            "typeable_chars": total_typeable_chars,
            "difficulty": estimate_difficulty(line_count, total_typeable_chars),
            "tags": extract_tags(filepath, data),
            "dateAdded": date_added,
        }
    except Exception as e:
        print(f"⚠️  Warning: Could not process {filepath}: {e}")
        return None


def build_metadata():
    """Scan public/ directory and generate metadata.json"""

    public_dir = Path("public")

    if not public_dir.exists():
        print(f"❌ Error: {public_dir} directory not found!")
        print("   Make sure you're running this from the project root.")
        return False

    print(f"\n{'='*70}")
    print("BUILDING METADATA INDEX FROM ACTIVE PUBLIC DIRECTORY")
    print(f"{'='*70}\n")

    # Only scan active language subdirectories within public/
    languages = ["python", "javascript", "typescript", "tsx"]
    json_files = []
    for lang in languages:
        lang_dir = public_dir / lang
        if lang_dir.exists():
            json_files.extend(list(lang_dir.rglob("*.json")))

    if not json_files:
        print("⚠️  No snippet JSON files found in public/")
        print("   Add some snippets first using: ./build/add_snippet.sh")
        return False

    print(f"Found {len(json_files)} snippet file(s):\n")

    # Process each snippet
    snippets = []
    for filepath in sorted(json_files):
        print(f"  Processing: {filepath.relative_to(public_dir)}")
        metadata = analyze_snippet(filepath)
        if metadata:
            snippets.append(metadata)
            print(
                f"    ✅ {metadata['name']} ({metadata['language']}, {metadata['lines']} lines)"
            )

    if not snippets:
        print("\n❌ No valid snippets found!")
        return False

    # Build metadata structure
    metadata = {
        "version": "1.0",
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "totalSnippets": len(snippets),
        "languages": sorted(list(set(s["language"] for s in snippets))),
        "snippets": snippets,
    }

    # Write metadata.json directly into public/
    output_path = public_dir / "metadata.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*70}")
    print("✅ METADATA GENERATED SUCCESSFULLY")
    print(f"{'='*70}\n")
    print(f"Output: {output_path}")
    print(f"Total snippets: {len(snippets)}")
    print(f"Languages: {', '.join(metadata['languages'])}")
    print(f"\nNext steps:")
    print(f"  1. Review {output_path}")
    print(f"  2. Run development server: pnpm dev")
    print(f"  3. Commit and push to deploy")

    return True


if __name__ == "__main__":
    import sys

    success = build_metadata()
    sys.exit(0 if success else 1)
