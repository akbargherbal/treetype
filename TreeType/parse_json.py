# ============================================================================
# TREE-SITTER PARSER TO JSON EXPORT
# Phase 5.3: Split bracket categories for granular control
# NEW: Separate parenthesis, curly_brace, square_bracket, angle_bracket
# ============================================================================

import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
from tree_sitter_typescript import language_typescript, language_tsx
from tree_sitter import Language, Parser
import pandas as pd
import json
from pathlib import Path

# ----------------------------------------------------------------------------
# SETUP PARSERS
# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------
# TOKEN CATEGORIZATION (PHASE 5.3: SPLIT BRACKETS)
# ----------------------------------------------------------------------------


def categorize_token(token_type, token_text):
    """
    Classify tokens into categories for frontend filtering.

    PHASE 5.3 CHANGE: Split 'bracket' into 4 subcategories:
        - parenthesis: ( )
        - curly_brace: { }
        - square_bracket: [ ]
        - angle_bracket: < > </ />

    This allows Standard mode to include parentheses while excluding
    curly braces and square brackets (ergonomic optimization).

    Returns:
        list: Categories this token belongs to (can be multiple)

    Categories:
        - comment: Single-line and multi-line comments
        - string_content: Content inside string literals
        - string_delimiter: Quote characters (", ', `)
        - punctuation: : ; , .
        - parenthesis: ( )
        - curly_brace: { }
        - square_bracket: [ ]
        - angle_bracket: < > </ /> (JSX/TSX)
        - operator: = + - * / % ! & | ^ ~ -> => ++ -- += -= *= /= ?
    """
    categories = []

    # Check token type first (case-insensitive)
    type_lower = token_type.lower()

    # Comments (any type containing 'comment')
    if "comment" in type_lower:
        categories.append("comment")

    # String content (content inside strings, NOT the delimiters)
    if "string" in type_lower and ("content" in type_lower or "fragment" in type_lower):
        categories.append("string_content")

    # String delimiters (the quotes themselves)
    if token_text in {'"', "'", "`"}:
        categories.append("string_delimiter")

    # Also check for string_start/string_end types
    if "string_start" in type_lower or "string_end" in type_lower:
        categories.append("string_delimiter")

    # Punctuation
    if token_text in {":", ";", ",", "."}:
        categories.append("punctuation")

    # PHASE 5.3: Split brackets into 4 categories
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


# ----------------------------------------------------------------------------
# TOKEN CLASSIFICATION (REFACTORED FOR PHASE 5.1)
# ----------------------------------------------------------------------------


def is_non_typeable(token_type, token_text):
    """
    Define what is STRUCTURALLY non-typeable (only whitespace).

    Returns:
        bool: True if token should NEVER be typeable (structural only)
    """

    # Only structural whitespace is truly non-typeable
    if token_type == "whitespace" and token_text.strip() == "":
        return True

    return False


# ----------------------------------------------------------------------------
# LEAF EXTRACTION
# ----------------------------------------------------------------------------


def get_leaves(node, nodes=None):
    """Get leaf nodes, treating string_content and comment as atomic."""
    if nodes is None:
        nodes = []

    # Atomic types: treat these as single units even if they span multiple lines
    atomic_types = {"string_content", "comment", "string_fragment"}

    for child in node.children:
        if child.type in atomic_types:
            nodes.append(child)
        elif child.children:
            nodes.extend(get_leaves(child))
        else:
            nodes.append(child)

    return nodes


# ----------------------------------------------------------------------------
# ENHANCED PARSING FUNCTION
# ----------------------------------------------------------------------------


def parse_code_to_dataframe(source_code, parser, language_name):
    """Parse code and return enhanced DataFrame with classification"""

    src_code_bytes = source_code.encode("utf-8")
    root_node = parser.parse(src_code_bytes).root_node
    leaves = get_leaves(root_node)

    # Build DataFrame
    df = pd.DataFrame(leaves).rename(columns={0: "NODE"})
    df["START_ROW"] = df["NODE"].apply(lambda x: x.range.start_point[0])
    df["START_COL"] = df["NODE"].apply(lambda x: x.range.start_point[1])
    df["END_ROW"] = df["NODE"].apply(lambda x: x.range.end_point[0])
    df["END_COL"] = df["NODE"].apply(lambda x: x.range.end_point[1])
    df["TEXT"] = df["NODE"].apply(lambda x: x.text.decode("utf-8"))
    df["TYPE"] = df["NODE"].apply(lambda x: x.type)

    # Add base_typeable (structural constraint only)
    df["BASE_TYPEABLE"] = df.apply(
        lambda x: not is_non_typeable(x["TYPE"], x["TEXT"]), axis=1
    )

    # PHASE 5.3: Add split bracket categories
    df["CATEGORIES"] = df.apply(
        lambda x: categorize_token(x["TYPE"], x["TEXT"]), axis=1
    )

    # Calculate indentation level (assuming 4-space indents)
    df["INDENT_LEVEL"] = df["START_COL"].apply(lambda x: x // 4)

    return df


# ----------------------------------------------------------------------------
# JSON EXPORT FUNCTION
# ----------------------------------------------------------------------------


def dataframe_to_json(df, source_code, language_name):
    """Convert DataFrame to frontend-ready JSON structure."""

    lines_data = []
    src_lines = source_code.split("\n")

    # Group by line
    for line_num, line_df in df.groupby("START_ROW"):
        line_df = line_df.sort_values(["START_COL"]).reset_index(drop=True)

        # Get indentation level (from first token on line)
        indent_level = line_df.iloc[0]["INDENT_LEVEL"] if len(line_df) > 0 else 0

        # Build display tokens (all tokens with enhanced metadata)
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

        # Build typing sequence (default: only base_typeable tokens)
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


# ----------------------------------------------------------------------------
# MAIN EXPORT FUNCTION
# ----------------------------------------------------------------------------


def export_code_to_json(source_code, language_name, output_path):
    """Main pipeline: Parse -> DataFrame -> JSON -> File"""

    if language_name not in PARSERS:
        raise ValueError(f"Unsupported language: {language_name}")

    lang, parser = PARSERS[language_name]

    print(f"\n{'='*70}")
    print(f"PARSING: {language_name.upper()}")
    print(f"{'='*70}\n")

    # Parse to DataFrame
    df = parse_code_to_dataframe(source_code, parser, language_name)

    print(f"Total tokens extracted: {len(df)}")
    print(f"Base typeable tokens: {df['BASE_TYPEABLE'].sum()}")
    print(f"Structural non-typeable tokens: {(~df['BASE_TYPEABLE']).sum()}")

    # Show category distribution
    print(f"\n{'-'*70}")
    print("CATEGORY DISTRIBUTION:")
    print(f"{'-'*70}")

    category_counts = {}
    for categories in df["CATEGORIES"]:
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1

    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:20s}: {count:3d} tokens")

    # Show token type breakdown
    print(f"\n{'-'*70}")
    print("TOKEN TYPE BREAKDOWN (Top 10):")
    print(f"{'-'*70}")
    type_summary = (
        df.groupby("TYPE").agg({"BASE_TYPEABLE": ["count", "sum"]}).reset_index()
    )
    type_summary.columns = ["Type", "Total", "Base_Typeable"]
    type_summary["Non-Typeable"] = type_summary["Total"] - type_summary["Base_Typeable"]
    type_summary = type_summary.sort_values("Total", ascending=False).head(10)
    print(type_summary.to_string(index=False))

    # Convert to JSON
    json_data = dataframe_to_json(df, source_code, language_name)

    # Write to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ JSON exported to: {output_file}")
    print(f"   Total lines: {json_data['total_lines']}")

    return json_data


# ============================================================================
# SAMPLE CODE (WITH MULTI-LINE CONTENT)
# ============================================================================

# Python sample: Fibonacci function WITH DOCSTRING
python_sample = '''def calculate_fibonacci(n: int) -> list:
    """
    Calculate Fibonacci sequence up to n terms.
    
    Args:
        n: Number of terms to generate
    
    Returns:
        List of Fibonacci numbers
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib

result = calculate_fibonacci(10)
print(result)
'''

# JavaScript sample: React component WITH TEMPLATE LITERAL
javascript_sample = """function UserProfile({ user }) {
    const [isActive, setIsActive] = useState(false);
    
    const handleClick = () => {
        setIsActive(!isActive);
    };
    
    // Multi-line template literal
    const description = `
        User: ${user.name}
        Status: ${isActive ? 'Active' : 'Inactive'}
        Email: ${user.email}
    `;
    
    return (
        <div className="profile">
            <h2>{user.name}</h2>
            <button onClick={handleClick}>
                {isActive ? 'Active' : 'Inactive'}
            </button>
        </div>
    );
}
"""

# TypeScript sample: API client WITH JSDOC COMMENT
typescript_sample = """interface User {
    id: number;
    name: string;
    email: string;
}

/**
 * Fetch user data from API
 * @param id - User ID to fetch
 * @returns Promise resolving to User object
 */
async function fetchUser(id: number): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();
    return data as User;
}
"""

# TSX sample: Todo component
tsx_sample = """import React, { useState } from 'react';

const TodoList: React.FC = () => {
    const [todos, setTodos] = useState<string[]>([]);
    const [input, setInput] = useState('');
    
    const addTodo = () => {
        if (input.trim()) {
            setTodos([...todos, input]);
            setInput('');
        }
    };
    
    return (
        <div>
            <input 
                value={input}
                onChange={(e) => setInput(e.target.value)}
            />
            <button onClick={addTodo}>Add</button>
            <ul>
                {todos.map((todo, idx) => (
                    <li key={idx}>{todo}</li>
                ))}
            </ul>
        </div>
    );
};
"""

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import sys

    # Create output directory
    output_dir = Path("output/json_samples")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print("TREE-SITTER PARSER TO JSON - PHASE 5.3")
    print(
        "Split bracket categories: parenthesis, curly_brace, square_bracket, angle_bracket"
    )
    print("=" * 70)

    # Export all sample files
    samples = {
        "python": python_sample,
        "javascript": javascript_sample,
        "typescript": typescript_sample,
        "tsx": tsx_sample,
    }

    for lang, code in samples.items():
        output_path = output_dir / f"{lang}_sample.json"
        export_code_to_json(code, lang, output_path)

    print("\n" + "=" * 70)
    print("✅ ALL SAMPLES EXPORTED")
    print("=" * 70)
    print(f"\nOutput directory: {output_dir.absolute()}")
    print("\nNext steps:")
    print("  1. Review JSON structure - check for new bracket categories")
    print("  2. Update render_code.html preset definitions")
    print("  3. Test Standard mode with parentheses included")
