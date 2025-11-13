# Context Document: Tree-Sitter Exploratory Analysis Project

## Project Intent

This is an **exploratory, learning-focused project** using tree-sitter to analyze code structure. The end goal is building an **interactive typing/educational app** (e.g., typing practice, fill-in-the-blank quizzes) where code is rendered as manipulable HTML elements with Tailwind styling—not as `<pre>/<code>` blocks.

**Critical: This is NOT a code reconstruction project.** Code reconstruction is used purely as a **validation mechanism** and **sanity check** to verify that tree-sitter parsing captured what we expected.

## Methodological Philosophy

### Core Values

- **First-principles approach**: Dictionary lookups, basic Pandas operations, transparent logic
- **Conceptual clarity over optimization**: Understanding the "why" matters more than elegant solutions
- **Simplicity over sophistication**: Avoid abstractions that obscure reasoning or introduce unnecessary dependencies
- **Reproducible analysis**: Each step should be traceable and verifiable

### What This Project Is NOT

- ❌ Building production-grade code reconstruction tools
- ❌ Optimizing for performance or elegance
- ❌ Creating reusable libraries or frameworks
- ❌ Achieving byte-perfect source fidelity

### What This Project IS

- ✅ Testing assumptions about tree-sitter parsing behavior
- ✅ Validating analytical reasoning through reconstruction checks
- ✅ Exploring token-level code representation for frontend rendering
- ✅ Building mental models of AST structure and leaf node extraction
- ✅ Learning through structured experimentation

## Technical Approach

### Data Flow

1. **Parse source code** → tree-sitter AST
2. **Extract leaf nodes** → terminal tokens with position metadata
3. **Convert to DataFrame** → structured analysis with Pandas
4. **Group by line** → line-based token sequences
5. **Reconstruct lines** → validation check (NOT the goal itself)
6. **Compare with source** → identify parsing gaps or logic errors

### Key Design Decisions

**Line-based grouping**: Chosen deliberately because the frontend app will render code line-by-line with artificial indentation via Tailwind classes (not preserved whitespace).

**Reconstruction logic**: Used as a diagnostic tool to verify:

- Are all tokens captured?
- Is token ordering correct?
- Is positional metadata accurate?

**Simple data structures**: Tuples and lists in DataFrames rather than complex node objects—easier to inspect, debug, and understand.

## Current State (Breakthrough Achieved)

### Major Bug Fixed

Original reconstruction function started shell from first token position, **losing leading indentation**:

```python
# WRONG (lost 400 lines to indentation loss):
shell = [placeholder for i in range(node_data[0][1], node_data[-1][3])]

# CORRECT (only 35 discrepancies, all expected):
shell = [placeholder for i in range(node_data[-1][3])]
```

### Remaining Discrepancies (35 → 1 lines)

- **34 lines**: Missing `\n` characters (irrelevant for frontend rendering)
- **5 lines**: Multi-line tokens (docstrings, multi-line strings) requiring special handling
- **After cleanup**: Only 1 true discrepancy remaining

### Validation Status

✅ **99.5%+ reconstruction accuracy** confirms parsing logic is sound  
✅ Token sequences are correctly captured and ordered  
✅ Position metadata is reliable for indentation calculation  
✅ Ready to move toward frontend data preparation

## Frontend Application Goals

### User Experience Design

- **Auto-jump typing**: User types tokens, spaces/indentation handled automatically
- **No whitespace typing**: System manages all spacing visually
- **Token-by-token progression**: Advance on correct token completion
- **Visual indentation**: Rendered via Tailwind padding classes, not typed spaces

### Data Requirements for Frontend

- Token text and type (for syntax highlighting)
- Indentation level (for left-padding calculation)
- Token sequence per line (for typing progression)
- Multi-line token handling strategy (TBD: single block vs. split display)

### What Users Will NOT Type

- Spaces between tokens
- Newlines
- Indentation spaces/tabs
- Possibly comments (design decision TBD)

## Communication Guidelines for Future Sessions

### DO Assume

- We understand reconstruction isn't the goal
- We prefer simple, transparent solutions
- We want to validate assumptions through testing
- We're comfortable with Pandas/dict-based approaches
- We're building toward a typing game/educational app

### DON'T Assume

- We need elegant/optimized code reconstruction
- We care about byte-perfect source fidelity
- We want sophisticated abstractions or libraries
- We're confused about project direction
- Performance is a concern

### Helpful Context to Provide

- Alternative approaches to validation (if simpler)
- Frontend data structure suggestions
- Multi-line token handling strategies
- Edge cases in tree-sitter parsing behavior
- Typing game UX considerations

### Less Helpful

- Lecture on "proper" reconstruction techniques
- Suggestions to use complex AST libraries
- Performance optimization advice
- Critiques of "inefficient" approaches

## Key Learnings So Far

1. **Tree-sitter leaf nodes capture all visible tokens** when traversed correctly
2. **Position metadata (start_point, end_point) is reliable** for column/row calculation
3. **Multi-line tokens exist** (5 found) and need special frontend handling
4. **Reconstruction serves as validation**, not as the product
5. **Line-based grouping works** for frontend rendering despite not being "standard"
6. **Simple tuple-based data structures** are sufficient and easier to debug than node objects

## Next Steps (When Ready)

1. Finalize multi-line token handling strategy
2. Generate frontend-ready JSON with token metadata
3. Build HTML preview to visualize typing game layout
4. Design token progression logic (auto-jump behavior)
5. Handle edge cases: empty lines, comments, operators
6. Explore syntax highlighting mappings (token type → CSS class)

---

**Meta-note**: This document should prevent future sessions from derailing into "here's how to properly reconstruct code" discussions. The reconstruction works, it validates our parsing, and that's sufficient. We're building a typing game, not a formatter.
