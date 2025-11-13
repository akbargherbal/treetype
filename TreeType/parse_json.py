# ============================================================================
# TREE-SITTER PARSER TO JSON EXPORT
# Phase 1.1: Enhanced parsing with token classification and JSON output
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
    'python': (Language(tspython.language()), Parser(Language(tspython.language()))),
    'javascript': (Language(tsjavascript.language()), Parser(Language(tsjavascript.language()))),
    'typescript': (Language(language_typescript()), Parser(Language(language_typescript()))),
    'tsx': (Language(language_tsx()), Parser(Language(language_tsx())))
}

# ----------------------------------------------------------------------------
# TOKEN CLASSIFICATION
# ----------------------------------------------------------------------------

def is_non_typeable(token_type, token_text):
    """
    Define what users should NOT type.
    Default: unknown tokens are typeable (safer for exploration).
    """
    
    # Punctuation
    punctuation = {':', ';', ',', '.'}
    
    # Brackets
    brackets = {'(', ')', '[', ']', '{', '}', '<', '>'}
    
    # Operators
    operators = {'=', '+', '-', '*', '/', '%', '!', '&', '|', '^', '~', '->', '=>', '++', '--', '+=', '-=', '*=', '/=', '?'}
    
    # JSX/TSX specific
    jsx_syntax = {'</', '/>'}
    
    # String delimiters
    string_delimiters = {'string_start', 'string_end', '"', "'", '`'}
    
    # Comments (visible but not typeable)
    comments = {'comment', 'line_comment', 'block_comment'}
    
    # Combine all non-typeable categories
    non_typeable_types = punctuation | brackets | operators | string_delimiters | comments | jsx_syntax
    
    # Check if token type or text matches
    if token_type in non_typeable_types:
        return True
    if token_text in non_typeable_types:
        return True
    
    return False

# ----------------------------------------------------------------------------
# LEAF EXTRACTION (from sanity check)
# ----------------------------------------------------------------------------

def get_leaves(node, nodes=None):
    """Get leaf nodes, but treat string_content and comment as atomic"""
    if nodes is None:
        nodes = []
    
    atomic_types = {'string_content', 'comment'}
    
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
    
    src_code_bytes = source_code.encode('utf-8')
    root_node = parser.parse(src_code_bytes).root_node
    leaves = get_leaves(root_node)
    
    # Build DataFrame
    df = pd.DataFrame(leaves).rename(columns={0: 'NODE'})
    df['START_ROW'] = df['NODE'].apply(lambda x: x.range.start_point[0])
    df['START_COL'] = df['NODE'].apply(lambda x: x.range.start_point[1])
    df['END_ROW'] = df['NODE'].apply(lambda x: x.range.end_point[0])
    df['END_COL'] = df['NODE'].apply(lambda x: x.range.end_point[1])
    df['TEXT'] = df['NODE'].apply(lambda x: x.text.decode('utf-8'))
    df['TYPE'] = df['NODE'].apply(lambda x: x.type)
    
    # NEW: Add token classification
    df['TYPEABLE'] = df.apply(
        lambda x: not is_non_typeable(x['TYPE'], x['TEXT']), 
        axis=1
    )
    
    # NEW: Calculate indentation level (assuming 4-space indents)
    df['INDENT_LEVEL'] = df['START_COL'].apply(lambda x: x // 4)
    
    # Add sequence number within line
    df['SEQ_IN_LINE'] = df.groupby('START_ROW').cumcount()
    
    return df

# ----------------------------------------------------------------------------
# JSON EXPORT FUNCTION
# ----------------------------------------------------------------------------

def dataframe_to_json(df, source_code, language_name):
    """
    Convert DataFrame to frontend-ready JSON structure.
    
    Output format per line:
    {
        "line_number": 4,
        "indent_level": 0,
        "display_tokens": [...],      # All tokens for rendering
        "typing_tokens": [...],       # Only typeable tokens
        "typing_sequence": "def...",  # Flattened typeable string
    }
    """
    
    lines_data = []
    src_lines = source_code.split('\n')
    
    # Group by line
    for line_num, line_df in df.groupby('START_ROW'):
        line_df = line_df.sort_values(['START_COL']).reset_index(drop=True)
        
        # Get indentation level (from first token on line)
        indent_level = line_df.iloc[0]['INDENT_LEVEL'] if len(line_df) > 0 else 0
        
        # Build display tokens (all tokens)
        display_tokens = []
        for idx, row in line_df.iterrows():
            display_tokens.append({
                'text': row['TEXT'],
                'type': row['TYPE'],
                'typeable': bool(row['TYPEABLE']),
                'start_col': int(row['START_COL']),
                'end_col': int(row['END_COL']),
                'seq_in_line': int(row['SEQ_IN_LINE'])
            })
        
        # Build typing tokens (only typeable)
        typing_tokens = [t for t in display_tokens if t['typeable']]
        
        # Build typing sequence (flattened string)
        typing_sequence = ''.join([t['text'] for t in typing_tokens])
        
        # Build character map (char index -> display position)
        char_map = {}
        char_idx = 0
        for token_idx, token in enumerate(typing_tokens):
            for char in token['text']:
                char_map[str(char_idx)] = {  # Convert to string for JSON
                    'token_idx': int(token_idx),
                    'display_col': int(token['start_col'])
                }
                char_idx += 1
        
        lines_data.append({
            'line_number': int(line_num),
            'indent_level': int(indent_level),
            'actual_line': src_lines[line_num] if line_num < len(src_lines) else '',
            'display_tokens': display_tokens,
            'typing_tokens': typing_tokens,
            'typing_sequence': typing_sequence,
            'char_map': char_map
        })
    
    return {
        'language': language_name,
        'total_lines': len(lines_data),
        'lines': lines_data
    }

# ----------------------------------------------------------------------------
# MAIN EXPORT FUNCTION
# ----------------------------------------------------------------------------

def export_code_to_json(source_code, language_name, output_path):
    """
    Main pipeline: Parse -> DataFrame -> JSON -> File
    """
    
    if language_name not in PARSERS:
        raise ValueError(f"Unsupported language: {language_name}")
    
    lang, parser = PARSERS[language_name]
    
    print(f"\n{'='*70}")
    print(f"PARSING: {language_name.upper()}")
    print(f"{'='*70}\n")
    
    # Parse to DataFrame
    df = parse_code_to_dataframe(source_code, parser, language_name)
    
    print(f"Total tokens extracted: {len(df)}")
    print(f"Typeable tokens: {df['TYPEABLE'].sum()}")
    print(f"Non-typeable tokens: {(~df['TYPEABLE']).sum()}")
    
    # Show typeable ratio by type
    print(f"\n{'-'*70}")
    print("TOKEN TYPE BREAKDOWN (Top 10):")
    print(f"{'-'*70}")
    type_summary = df.groupby('TYPE').agg({
        'TYPEABLE': ['count', 'sum']
    }).reset_index()
    type_summary.columns = ['Type', 'Total', 'Typeable']
    type_summary['Non-Typeable'] = type_summary['Total'] - type_summary['Typeable']
    type_summary = type_summary.sort_values('Total', ascending=False).head(10)
    print(type_summary.to_string(index=False))
    
    # Convert to JSON
    json_data = dataframe_to_json(df, source_code, language_name)
    
    # Write to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nâœ… JSON exported to: {output_file}")
    print(f"   Total lines: {json_data['total_lines']}")
    
    return json_data

# ============================================================================
# SAMPLE CODE FOR TESTING
# ============================================================================

# Python sample: Fibonacci function
python_sample = '''def calculate_fibonacci(n: int) -> list:
    """Calculate Fibonacci sequence up to n terms."""
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

# JavaScript sample: React component stub
javascript_sample = '''function UserProfile({ user }) {
    const [isActive, setIsActive] = useState(false);
    
    const handleClick = () => {
        setIsActive(!isActive);
    };
    
    return (
        <div className="profile">
            <h2>{user.name}</h2>
            <button onClick={handleClick}>
                {isActive ? 'Active' : 'Inactive'}
            </button>
        </div>
    );
}
'''

# TypeScript sample: API client
typescript_sample = '''interface User {
    id: number;
    name: string;
    email: string;
}

async function fetchUser(id: number): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();
    return data as User;
}
'''

# TSX sample: Todo component
tsx_sample = '''import React, { useState } from 'react';

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
        </div>
    );
};
'''

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Create output directory
    output_dir = Path("output/json_samples")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("TREE-SITTER PARSER TO JSON - PHASE 1.1")
    print("="*70)
    
    # Export all sample files
    samples = {
        'python': python_sample,
        'javascript': javascript_sample,
        'typescript': typescript_sample,
        'tsx': tsx_sample
    }
    
    for lang, code in samples.items():
        output_path = output_dir / f"{lang}_sample.json"
        export_code_to_json(code, lang, output_path)
    
    print("\n" + "="*70)
    print("âœ… ALL SAMPLES EXPORTED")
    print("="*70)
    print(f"\nOutput directory: {output_dir.absolute()}")
    print("\nNext steps:")
    print("  1. Review JSON structure in output files")
    print("  2. Test with your own code files")
    print("  3. Proceed to Phase 1.2 (HTML renderer)")