#!/usr/bin/env python3
"""
treetype Metadata Builder
Scans snippets/ directory and generates metadata.json index
"""

import json
from pathlib import Path
from datetime import datetime
import hashlib


def generate_snippet_id(filepath):
    """Generate stable ID from filepath"""
    # Use relative path from snippets/ as base
    rel_path = filepath.relative_to(Path("snippets"))
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

        return {
            "id": snippet_id,
            "name": get_snippet_name(filepath),
            "language": data.get("language", "unknown"),
            "path": str(filepath),
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
    """Scan snippets/ directory and generate metadata.json"""

    snippets_dir = Path("snippets")

    if not snippets_dir.exists():
        print(f"❌ Error: {snippets_dir} directory not found!")
        print("   Make sure you're running this from the project root.")
        return False

    print(f"\n{'='*70}")
    print("BUILDING METADATA INDEX")
    print(f"{'='*70}\n")

    # Find all JSON files (excluding metadata.json itself)
    json_files = [f for f in snippets_dir.rglob("*.json") if f.name != "metadata.json"]

    if not json_files:
        print("⚠️  No snippet JSON files found in snippets/")
        print("   Add some snippets first using: ./build/add_snippet.sh")
        return False

    print(f"Found {len(json_files)} snippet file(s):\n")

    # Process each snippet
    snippets = []
    for filepath in sorted(json_files):
        print(f"  Processing: {filepath.relative_to(snippets_dir)}")
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

    # Write metadata.json
    output_path = snippets_dir / "metadata.json"
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
    print(f"  2. Test with local server: python -m http.server 8000")
    print(f"  3. Commit and push to deploy")

    return True


if __name__ == "__main__":
    import sys

    success = build_metadata()
    sys.exit(0 if success else 1)
