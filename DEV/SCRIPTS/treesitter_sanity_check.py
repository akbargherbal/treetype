# ============================================================================
# MULTI-LANGUAGE TREE-SITTER SANITY CHECK
# Tests Python, JavaScript, TypeScript, and TSX parsing with reconstruction
# ============================================================================

import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
from tree_sitter_typescript import language_typescript, language_tsx
from tree_sitter import Language, Parser
import pandas as pd
from pathlib import Path

# ----------------------------------------------------------------------------
# SETUP PARSERS
# ----------------------------------------------------------------------------

PY_LANGUAGE = Language(tspython.language())
JS_LANGUAGE = Language(tsjavascript.language())
TS_LANGUAGE = Language(language_typescript())
TSX_LANGUAGE = Language(language_tsx())

py_parser = Parser(PY_LANGUAGE)
js_parser = Parser(JS_LANGUAGE)
ts_parser = Parser(TS_LANGUAGE)
tsx_parser = Parser(TSX_LANGUAGE)

# ----------------------------------------------------------------------------
# LEAF EXTRACTION FUNCTION
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
# RECONSTRUCTION FUNCTION
# ----------------------------------------------------------------------------

def reconstruct_code_from_leaves(node_data, placeholder='#7/7#'):
    """Reconstruct line from leaf nodes with proper indentation"""
    shell = [placeholder for i in range(node_data[-1][3])]
    
    for i in node_data:
        shell[i[1]: i[3]] = i[4]
    
    shell = [" " if (i == placeholder) else i for i in shell]
    shell = ''.join(shell)
    return shell

# ----------------------------------------------------------------------------
# COMPARISON FUNCTION
# ----------------------------------------------------------------------------

def compare_lines(actual, reconstructed):
    """Compare actual and reconstructed lines character by character"""
    if len(actual) != len(reconstructed):
        length_identical = False
    else:
        length_identical = True
    
    char_identity = [
        (idx, i) for (idx, i) in enumerate(list(zip(actual, reconstructed))) 
        if i[0] != i[1]
    ]
    
    if len(actual) == 0:
        percent_identical = 1.0
    else:
        percent_identical = (len(actual) - len(char_identity)) / len(actual)
        percent_identical = round(percent_identical, 2)
    
    return {
        'length_identical': length_identical,
        'char_identity': char_identity,
        'percent_identical': percent_identical
    }

# ----------------------------------------------------------------------------
# MAIN ANALYSIS FUNCTION
# ----------------------------------------------------------------------------

def analyze_language(source_code, parser, language_name, file_extension):
    """Complete analysis pipeline for any language"""
    
    print(f"\n{'='*70}")
    print(f"ANALYZING: {language_name}")
    print(f"{'='*70}\n")
    
    # Parse
    src_code_bytes = source_code.encode('utf-8')
    root_node = parser.parse(src_code_bytes).root_node
    leaves = get_leaves(root_node)
    
    print(f"Total leaf nodes extracted: {len(leaves)}")
    
    # Build DataFrame
    df = pd.DataFrame(leaves).rename(columns={0: 'NODE'})
    df['START_ROW'] = df['NODE'].apply(lambda x: x.range.start_point[0])
    df['START_COL'] = df['NODE'].apply(lambda x: x.range.start_point[1])
    df['END_ROW'] = df['NODE'].apply(lambda x: x.range.end_point[0])
    df['END_COL'] = df['NODE'].apply(lambda x: x.range.end_point[1])
    df['TEXT'] = df['NODE'].apply(lambda x: x.text.decode('utf-8'))
    df['TYPE'] = df['NODE'].apply(lambda x: x.type)
    
    # Check for multi-line tokens
    multi_line_count = len(df[df['START_ROW'] != df['END_ROW']])
    print(f"Multi-line tokens found: {multi_line_count}")
    
    if multi_line_count > 0:
        print("\nMulti-line tokens:")
        multi_line_tokens = df[df['START_ROW'] != df['END_ROW']][['START_ROW', 'END_ROW', 'TYPE', 'TEXT']]
        for idx, row in multi_line_tokens.iterrows():
            print(f"  Lines {row['START_ROW']}-{row['END_ROW']} | Type: {row['TYPE']}")
            print(f"    Preview: {row['TEXT'][:50]}..." if len(row['TEXT']) > 50 else f"    Text: {row['TEXT']}")
    
    # Create node data tuples
    df['NODE_DATA'] = df.apply(lambda x: (
        x['START_ROW'], x['START_COL'], x['END_ROW'], x['END_COL'], x['TEXT'], x['TYPE']
    ), axis=1)
    
    # Group by line
    df_grouped = df.groupby(['START_ROW'], as_index=False).agg({
        'NODE_DATA': lambda x: sorted(list(x), key=lambda y: (y[0], y[1], y[2], y[3]))
    }).reset_index(drop=True)
    df_grouped = df_grouped.sort_values(['START_ROW']).reset_index(drop=True)
    
    print(f"Total lines grouped: {len(df_grouped)}")
    
    # Reconstruct
    df_grouped['RECONSTRUCT'] = df_grouped['NODE_DATA'].apply(
        lambda x: reconstruct_code_from_leaves(x)
    )
    
    # Get actual lines
    src_code_lines = source_code.split('\n')
    dict_line_idx = {i: line for i, line in enumerate(src_code_lines)}
    
    df_grouped['ACTUAL_LINE'] = df_grouped['START_ROW'].apply(
        lambda x: dict_line_idx[x]
    )
    
    # Compare
    df_grouped['ANALYSIS'] = df_grouped.apply(
        lambda x: compare_lines(x['ACTUAL_LINE'], x['RECONSTRUCT']), 
        axis=1
    )
    
    # Filter discrepancies
    df_different = df_grouped[
        df_grouped['ANALYSIS'].apply(lambda x: x['percent_identical'] < 0.98)
    ].copy()
    
    print(f"\nLines with <98% match: {len(df_different)}")
    
    if len(df_different) > 0:
        # Check for missing newlines
        df_different['MISSING_NEWLINE'] = df_different.apply(
            lambda x: x['ACTUAL_LINE'].endswith('\n') and not x['RECONSTRUCT'].endswith('\n'),
            axis=1
        )
        
        newline_issues = df_different['MISSING_NEWLINE'].sum()
        print(f"  - Missing newline issues: {newline_issues}")
        
        # Show non-newline discrepancies
        real_discrepancies = df_different[~df_different['MISSING_NEWLINE']]
        print(f"  - Real discrepancies (excluding newlines): {len(real_discrepancies)}")
        
        if len(real_discrepancies) > 0:
            print("\n⚠️  REAL DISCREPANCIES FOUND:")
            for idx, row in real_discrepancies.iterrows():
                print(f"\n  Line {row['START_ROW']}:")
                print(f"    Actual:       '{row['ACTUAL_LINE'][:60]}...'")
                print(f"    Reconstructed: '{row['RECONSTRUCT'][:60]}...'")
                print(f"    Match: {row['ANALYSIS']['percent_identical']*100}%")
    else:
        print("✅ All lines match perfectly!")
    
    # Token type distribution
    print(f"\n{'-'*70}")
    print("TOKEN TYPE DISTRIBUTION:")
    print(f"{'-'*70}")
    token_types = df['TYPE'].value_counts()
    for token_type, count in token_types.head(15).items():
        print(f"  {token_type:30} {count:5}")
    
    if len(token_types) > 15:
        print(f"  ... and {len(token_types) - 15} more types")
    
    return df_grouped, df_different

# ============================================================================
# SAMPLE CODE FOR EACH LANGUAGE
# ============================================================================

# ----------------------------------------------------------------------------
# PYTHON SAMPLE
# ----------------------------------------------------------------------------
python_code = '''import sys
from typing import List, Dict, Optional

def calculate_fibonacci(n: int) -> List[int]:
    """
    Calculate Fibonacci sequence up to n terms.
    Multi-line docstring for testing.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib

class DataProcessor:
    def __init__(self, data: Dict[str, any]):
        self.data = data
        self.processed = False
    
    def process(self) -> Optional[Dict]:
        # Process the data
        result = {k: v * 2 for k, v in self.data.items()}
        self.processed = True
        return result

if __name__ == "__main__":
    processor = DataProcessor({"a": 1, "b": 2})
    print(processor.process())
'''

# ----------------------------------------------------------------------------
# JAVASCRIPT SAMPLE
# ----------------------------------------------------------------------------
javascript_code = '''const express = require('express');
const path = require('path');

// Multi-line comment
// for testing purposes
function calculateSum(arr) {
    return arr.reduce((acc, val) => acc + val, 0);
}

class UserManager {
    constructor(users = []) {
        this.users = users;
        this.activeCount = 0;
    }
    
    addUser(user) {
        this.users.push(user);
        this.activeCount++;
        return true;
    }
    
    getActiveUsers() {
        return this.users.filter(u => u.active);
    }
}

const app = express();

app.get('/api/users/:id', async (req, res) => {
    try {
        const userId = req.params.id;
        const user = await database.findUser(userId);
        
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        
        res.json(user);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = { UserManager, calculateSum };
'''

# ----------------------------------------------------------------------------
# TYPESCRIPT SAMPLE
# ----------------------------------------------------------------------------
typescript_code = '''interface User {
    id: number;
    name: string;
    email: string;
    role?: 'admin' | 'user';
}

type ResponseData<T> = {
    data: T;
    status: number;
    message?: string;
}

class ApiClient<T> {
    private baseUrl: string;
    private headers: Record<string, string>;
    
    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Content-Type': 'application/json'
        };
    }
    
    async fetch(endpoint: string): Promise<ResponseData<T>> {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            headers: this.headers
        });
        
        const data = await response.json();
        
        return {
            data: data as T,
            status: response.status,
            message: response.ok ? 'Success' : 'Error'
        };
    }
    
    setAuthToken(token: string): void {
        this.headers['Authorization'] = `Bearer ${token}`;
    }
}

function processUsers(users: User[]): User[] {
    return users
        .filter(u => u.role === 'admin')
        .map(u => ({ ...u, email: u.email.toLowerCase() }));
}

export { ApiClient, User, ResponseData };
'''

# ----------------------------------------------------------------------------
# TSX SAMPLE
# ----------------------------------------------------------------------------
tsx_code = '''import React, { useState, useEffect } from 'react';
import { Button, Card } from './components';

interface TodoItem {
    id: number;
    text: string;
    completed: boolean;
}

interface TodoListProps {
    initialTodos?: TodoItem[];
    onUpdate?: (todos: TodoItem[]) => void;
}

const TodoList: React.FC<TodoListProps> = ({ initialTodos = [], onUpdate }) => {
    const [todos, setTodos] = useState<TodoItem[]>(initialTodos);
    const [inputValue, setInputValue] = useState('');
    
    useEffect(() => {
        if (onUpdate) {
            onUpdate(todos);
        }
    }, [todos, onUpdate]);
    
    const addTodo = () => {
        if (inputValue.trim()) {
            const newTodo: TodoItem = {
                id: Date.now(),
                text: inputValue,
                completed: false
            };
            setTodos([...todos, newTodo]);
            setInputValue('');
        }
    };
    
    const toggleTodo = (id: number) => {
        setTodos(todos.map(todo =>
            todo.id === id ? { ...todo, completed: !todo.completed } : todo
        ));
    };
    
    return (
        <Card className="p-4">
            <h2 className="text-xl font-bold mb-4">My Todo List</h2>
            
            <div className="flex gap-2 mb-4">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addTodo()}
                    placeholder="Add a new todo..."
                    className="flex-1 px-3 py-2 border rounded"
                />
                <Button onClick={addTodo}>Add</Button>
            </div>
            
            <ul className="space-y-2">
                {todos.map(todo => (
                    <li
                        key={todo.id}
                        onClick={() => toggleTodo(todo.id)}
                        className={`cursor-pointer p-2 rounded ${
                            todo.completed ? 'line-through text-gray-500' : ''
                        }`}
                    >
                        {todo.text}
                    </li>
                ))}
            </ul>
        </Card>
    );
};

export default TodoList;
'''

# ============================================================================
# RUN ALL ANALYSES
# ============================================================================

print("\n" + "="*70)
print("TREE-SITTER MULTI-LANGUAGE SANITY CHECK")
print("="*70)

# Python
py_df, py_diff = analyze_language(python_code, py_parser, "PYTHON", ".py")

# JavaScript
js_df, js_diff = analyze_language(javascript_code, js_parser, "JAVASCRIPT", ".js")

# TypeScript
ts_df, ts_diff = analyze_language(typescript_code, ts_parser, "TYPESCRIPT", ".ts")

# TSX
tsx_df, tsx_diff = analyze_language(tsx_code, tsx_parser, "TSX/REACT", ".tsx")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("FINAL SUMMARY")
print("="*70)

summary_data = {
    'Language': ['Python', 'JavaScript', 'TypeScript', 'TSX'],
    'Total Lines': [len(py_df), len(js_df), len(ts_df), len(tsx_df)],
    'Discrepancies': [len(py_diff), len(js_diff), len(ts_diff), len(tsx_diff)]
}

summary_df = pd.DataFrame(summary_data)
print("\n", summary_df.to_string(index=False))

print("\n✅ Sanity check complete!")
print("\nNext steps:")
print("  1. Examine any discrepancies found")
print("  2. Test with your actual source files")
print("  3. Design frontend data structure based on findings")
