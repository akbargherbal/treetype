#!/usr/bin/env python3
"""
treetype Parser - Refactored for Phase 6
Converts source code files to treetype JSON format
Supports: Python, JavaScript, TypeScript, TSX
"""

import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
from tree_sitter_typescript import language_typescript, language_tsx
from tree_sitter import Language, Parser
import pandas as pd
import json
from pathlib import Path
import argparse
import sys

# ============================================================================
# PARSER SETUP
# ============================================================================

PARSERS = {
    "python": (Language(tspython.language()), Parser(Language(tspython.language()))),
    "javascript": (
        Language(tsjavascript.language()),
        Parser(Language(tsjavascript.language())),
    ),
    "typescript": (
        Language(language_typescript()),
        Parser(Language(language_typescript())),
    ),
    "tsx": (Language(language_tsx()), Parser(Language(language_tsx()))),
}

LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
}

# ============================================================================
# TOKEN CATEGORIZATION
# ============================================================================


def categorize_token(token_type, token_text):
    """Classify tokens into categories for frontend filtering"""
    categories = []
    type_lower = token_type.lower()

    # Comments
    if "comment" in type_lower:
        categories.append("comment")

    # String content
    if "string" in type_lower and ("content" in type_lower or "fragment" in type_lower):
        categories.append("string_content")

    # JSX text content (treat like string content)
    if token_type == "jsx_text":
        categories.append("string_content")

    # String delimiters
    if token_text in {'"', "'", "`"}:
        categories.append("string_delimiter")
    if "string_start" in type_lower or "string_end" in type_lower:
        categories.append("string_delimiter")

    # Punctuation
    if token_text in {":", ";", ",", "."}:
        categories.append("punctuation")

    # Split brackets
    if token_text in {"(", ")"}:
        categories.append("parenthesis")
    if token_text in {"{", "}"}:
        categories.append("curly_brace")
    if token_text in {"[", "]"}:
        categories.append("square_bracket")
    if token_text in {"<", ">", "</", "/>"}:
        categories.append("angle_bracket")

    # Operators
    operators = {
        "=",
        "+",
        "-",
        "*",
        "/",
        "%",
        "!",
        "&",
        "|",
        "^",
        "~",
        "->",
        "=>",
        "++",
        "--",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "==",
        "!=",
        "===",
        "!==",
        "<=",
        ">=",
        "&&",
        "||",
        "<<",
        ">>",
        "**",
        "//",
        "?",
        ":",
        "??",
        "?.",
        "...",
    }
    if token_text in operators:
        categories.append("operator")

    return categories


def is_non_typeable(token_type, token_text):
    """Only structural whitespace is non-typeable"""
    if token_type == "whitespace" and token_text.strip() == "":
        return True
    return False


# ============================================================================
# JSX TEXT HANDLING (BUG FIX)
# ============================================================================


def split_jsx_text_token(row):
    """
    Split jsx_text tokens to separate content from whitespace.
    Returns a list of row dictionaries (compatible with pandas).

    Example: "Debounced: " -> [
        {"TEXT": "Debounced:", "BASE_TYPEABLE": True, ...},
        {"TEXT": " ", "BASE_TYPEABLE": False, ...}
    ]
    """
    text = row["TEXT"]
    token_type = row["TYPE"]

    # Only process jsx_text tokens
    if token_type != "jsx_text":
        return [row.to_dict() if hasattr(row, "to_dict") else row]

    # If no leading/trailing whitespace, return as-is
    if text == text.strip():
        return [row.to_dict() if hasattr(row, "to_dict") else row]

    tokens = []
    start_col = row["START_COL"]
    start_row = row["START_ROW"]
    end_row = row["END_ROW"]
    indent_level = row["INDENT_LEVEL"]
    current_col = start_col

    # Handle leading whitespace
    leading_ws = len(text) - len(text.lstrip())
    if leading_ws > 0:
        tokens.append(
            {
                "START_ROW": start_row,
                "START_COL": current_col,
                "END_ROW": end_row,
                "END_COL": current_col + leading_ws,
                "TEXT": text[:leading_ws],
                "TYPE": "jsx_text_whitespace",
                "BASE_TYPEABLE": False,
                "CATEGORIES": [],
                "INDENT_LEVEL": indent_level,
            }
        )
        current_col += leading_ws

    # Handle middle content (actual text)
    content = text.strip()
    if content:
        categories = row["CATEGORIES"] if isinstance(row["CATEGORIES"], list) else []
        tokens.append(
            {
                "START_ROW": start_row,
                "START_COL": current_col,
                "END_ROW": end_row,
                "END_COL": current_col + len(content),
                "TEXT": content,
                "TYPE": "jsx_text",
                "BASE_TYPEABLE": True,
                "CATEGORIES": categories,
                "INDENT_LEVEL": indent_level,
            }
        )
        current_col += len(content)

    # Handle trailing whitespace
    trailing_ws = len(text) - len(text.rstrip())
    if trailing_ws > 0:
        tokens.append(
            {
                "START_ROW": start_row,
                "START_COL": current_col,
                "END_ROW": end_row,
                "END_COL": current_col + trailing_ws,
                "TEXT": text[-trailing_ws:],
                "TYPE": "jsx_text_whitespace",
                "BASE_TYPEABLE": False,
                "CATEGORIES": [],
                "INDENT_LEVEL": indent_level,
            }
        )

    return tokens


# ============================================================================
# TREE-SITTER PARSING
# ============================================================================


def get_leaves(node, nodes=None):
    """Get leaf nodes, treating string_content and comment as atomic"""
    if nodes is None:
        nodes = []

    atomic_types = {"string_content", "comment", "string_fragment"}

    for child in node.children:
        if child.type in atomic_types:
            nodes.append(child)
        elif child.children:
            nodes.extend(get_leaves(child))
        else:
            nodes.append(child)

    return nodes


def parse_code_to_dataframe(source_code, parser, language_name):
    """Parse code and return enhanced DataFrame"""
    src_code_bytes = source_code.encode("utf-8")
    root_node = parser.parse(src_code_bytes).root_node
    leaves = get_leaves(root_node)

    df = pd.DataFrame(leaves).rename(columns={0: "NODE"})
    df["START_ROW"] = df["NODE"].apply(lambda x: x.range.start_point[0])
    df["START_COL"] = df["NODE"].apply(lambda x: x.range.start_point[1])
    df["END_ROW"] = df["NODE"].apply(lambda x: x.range.end_point[0])
    df["END_COL"] = df["NODE"].apply(lambda x: x.range.end_point[1])
    df["TEXT"] = df["NODE"].apply(lambda x: x.text.decode("utf-8"))
    df["TYPE"] = df["NODE"].apply(lambda x: x.type)

    df["BASE_TYPEABLE"] = df.apply(
        lambda x: not is_non_typeable(x["TYPE"], x["TEXT"]), axis=1
    )
    df["CATEGORIES"] = df.apply(
        lambda x: categorize_token(x["TYPE"], x["TEXT"]), axis=1
    )
    df["INDENT_LEVEL"] = df["START_COL"].apply(lambda x: x // 4)

    # CRITICAL FIX: Split jsx_text tokens to separate whitespace
    if language_name in ["tsx", "javascript"]:  # JSX can appear in both
        expanded_rows = []
        for idx, row in df.iterrows():
            split_tokens = split_jsx_text_token(row)
            expanded_rows.extend(split_tokens)

        # Rebuild dataframe with split tokens
        if expanded_rows:
            df = pd.DataFrame(expanded_rows)

    return df


# ============================================================================
# JSON EXPORT
# ============================================================================


def dataframe_to_json(df, source_code, language_name):
    """Convert DataFrame to frontend-ready JSON"""
    lines_data = []
    src_lines = source_code.split("\n")

    for line_num, line_df in df.groupby("START_ROW"):
        line_df = line_df.sort_values(["START_COL"]).reset_index(drop=True)
        indent_level = line_df.iloc[0]["INDENT_LEVEL"] if len(line_df) > 0 else 0

        # Build display tokens
        display_tokens = []
        for idx, row in line_df.iterrows():
            display_tokens.append(
                {
                    "text": row["TEXT"],
                    "type": row["TYPE"],
                    "categories": row["CATEGORIES"],
                    "base_typeable": bool(row["BASE_TYPEABLE"]),
                    "start_col": int(row["START_COL"]),
                    "end_col": int(row["END_COL"]),
                }
            )

        # Build typing sequence
        typing_tokens = [t for t in display_tokens if t["base_typeable"]]
        typing_sequence = "".join([t["text"] for t in typing_tokens])

        # Build character map
        char_map = {}
        char_idx = 0
        for token_idx, token in enumerate(typing_tokens):
            for char in token["text"]:
                char_map[str(char_idx)] = {
                    "token_idx": int(token_idx),
                    "display_col": int(token["start_col"]),
                }
                char_idx += 1

        lines_data.append(
            {
                "line_number": int(line_num),
                "indent_level": int(indent_level),
                "actual_line": src_lines[line_num] if line_num < len(src_lines) else "",
                "display_tokens": display_tokens,
                "typing_sequence": typing_sequence,
                "char_map": char_map,
            }
        )

    return {
        "language": language_name,
        "total_lines": len(lines_data),
        "lines": lines_data,
    }


# ============================================================================
# FILE PROCESSING
# ============================================================================


def validate_file(filepath):
    """Validate source file"""
    path = Path(filepath)

    if not path.exists():
        return False, f"File not found: {filepath}"

    if not path.is_file():
        return False, f"Not a file: {filepath}"

    if path.suffix not in LANGUAGE_EXTENSIONS:
        return (
            False,
            f"Unsupported file type: {path.suffix}. Supported: {', '.join(LANGUAGE_EXTENSIONS.keys())}",
        )

    # Check file size (warn if > 1000 lines)
    with open(path, "r", encoding="utf-8") as f:
        line_count = sum(1 for _ in f)

    if line_count < 5:
        return False, f"File too short ({line_count} lines). Minimum: 5 lines"

    if line_count > 200:
        print(f"⚠️  Warning: File has {line_count} lines (recommended: 5-50 lines)")
        print("   Long snippets may be harder to practice. Consider splitting.")

    return True, None


def process_file(input_path, output_path=None, quiet=False):
    """Process a single source file"""
    # Validate
    valid, error = validate_file(input_path)
    if not valid:
        print(f"❌ Error: {error}")
        return False

    input_file = Path(input_path)
    language = LANGUAGE_EXTENSIONS[input_file.suffix]

    # Determine output path
    if output_path is None:
        output_path = Path("snippets") / language / f"{input_file.stem}.json"
    else:
        output_path = Path(output_path)

    # Read source
    with open(input_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Parse
    if not quiet:
        print(f"\n{'='*70}")
        print(f"PARSING: {input_file.name} ({language})")
        print(f"{'='*70}\n")

    lang, parser = PARSERS[language]
    df = parse_code_to_dataframe(source_code, parser, language)

    if not quiet:
        print(f"Total tokens: {len(df)}")
        print(f"Base typeable: {df['BASE_TYPEABLE'].sum()}")
        print(f"Lines: {df['START_ROW'].nunique()}")

    # Convert to JSON
    json_data = dataframe_to_json(df, source_code, language)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    if not quiet:
        print(f"\n✅ Snippet generated: {output_path}")
        print(f"   Lines: {json_data['total_lines']}")
        typeable_chars = sum(
            len(line.get("typing_sequence", "")) for line in json_data["lines"]
        )
        print(f"   Typeable characters: {typeable_chars}")

    return True


# ============================================================================
# CLI
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="treetype Parser - Convert source code to typing snippets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse single file (auto-detect language and output path)
  python build/parse_json.py sources/python/views.py
  
  # Parse with custom output path
  python build/parse_json.py sources/python/views.py -o snippets/python/django_views.json
  
  # Parse multiple files
  python build/parse_json.py sources/python/*.py
  
  # Batch process directory
  python build/parse_json.py sources/python/
  
  # Quiet mode (no output except errors)
  python build/parse_json.py sources/python/views.py -q

Supported languages:
  .py   -> Python
  .js   -> JavaScript
  .jsx  -> JavaScript
  .ts   -> TypeScript
  .tsx  -> TSX/React
        """,
    )

    parser.add_argument("input", nargs="+", help="Source file(s) or directory to parse")
    parser.add_argument(
        "-o",
        "--output",
        help="Output path (default: snippets/<language>/<filename>.json)",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Quiet mode (minimal output)"
    )

    args = parser.parse_args()

    # Collect all files to process
    files_to_process = []
    for input_item in args.input:
        path = Path(input_item)
        if path.is_dir():
            # Recursively find supported files
            for ext in LANGUAGE_EXTENSIONS.keys():
                files_to_process.extend(path.rglob(f"*{ext}"))
        elif path.is_file():
            files_to_process.append(path)
        else:
            # Might be a glob pattern
            files_to_process.extend(Path(".").glob(input_item))

    if not files_to_process:
        print("❌ Error: No valid source files found")
        return 1

    # Process files
    success_count = 0
    for filepath in files_to_process:
        # Can only specify output for single file
        output = args.output if len(files_to_process) == 1 else None

        if process_file(filepath, output, args.quiet):
            success_count += 1

    # Summary
    if not args.quiet and len(files_to_process) > 1:
        print(f"\n{'='*70}")
        print(f"✅ Processed {success_count}/{len(files_to_process)} file(s)")
        print(f"{'='*70}")
        print("\nNext steps:")
        print("  1. Run: python build/build_metadata.py")
        print("  2. Test locally: python -m http.server 8000")
        print("  3. Commit and push to deploy")

    return 0 if success_count == len(files_to_process) else 1


if __name__ == "__main__":
    sys.exit(main())
