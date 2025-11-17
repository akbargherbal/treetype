# TreeType Architecture

**Technical design and implementation details**

Version: Post-Phase 6 (TypeScript Migration Complete)  
Last Updated: Session 38

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Parser Architecture](#parser-architecture)
3. [Token Categorization](#token-categorization)
4. [Frontend Architecture](#frontend-architecture)
5. [Data Flow](#data-flow)
6. [Critical Implementation Details](#critical-implementation-details)
7. [Performance Considerations](#performance-considerations)
8. [Testing Strategy](#testing-strategy)

---

## System Overview

TreeType uses a **two-stage architecture** that separates parsing (offline) from rendering (runtime).

### Design Principles

1. **Static-first** - Pre-compute everything possible
2. **Zero backend** - No server required, runs entirely client-side
3. **Fast loading** - JSON files are instantly parseable
4. **Modular** - TypeScript modules enable testing and reusability
5. **Type-safe** - TypeScript prevents entire classes of bugs

### High-Level Flow

```
┌─────────────────┐
│  Source Code    │  .py, .js, .ts, .tsx files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  parse_json.py  │  Tree-sitter → JSON (offline, developer machine)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JSON Snippets  │  Static files (committed to repo)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Frontend App   │  TypeScript + Vite (runtime, user browser)
└─────────────────┘
```

**Why this architecture?**
- **No build step for users** - JSON is already parsed
- **Fast loading** - No server round-trip, instant snippet selection
- **Free hosting** - GitHub Pages serves static files
- **Offline-capable** - Everything runs client-side
- **Version control friendly** - JSON diffs show exactly what changed

---

## Parser Architecture

**File**: `build/parse_json.py`  
**Language**: Python 3.x  
**Dependencies**: tree-sitter, pandas

### Core Components

#### 1. Language Parsers

```python
PARSERS = {
    "python": (Language(tspython.language()), Parser(...)),
    "javascript": (Language(tsjavascript.language()), Parser(...)),
    "typescript": (Language(language_typescript()), Parser(...)),
    "tsx": (Language(language_tsx()), Parser(...))
}
```

Each language has a dedicated tree-sitter grammar. TSX and JavaScript share the same grammar but use different entry points.

#### 2. Token Extraction (`get_leaves()`)

```python
def get_leaves(node, nodes=None):
    """Get leaf nodes, treating string_content and comment as atomic"""
    atomic_types = {"string_content", "comment", "string_fragment"}
    
    for child in node.children:
        if child.type in atomic_types:
            nodes.append(child)  # Don't descend into strings/comments
        elif child.children:
            nodes.extend(get_leaves(child))
        else:
            nodes.append(child)
    
    return nodes
```

**Key insight**: String content and comments are treated as atomic units. We don't want to break "Hello World" into individual characters—the entire phrase is one token.

#### 3. Token Categorization (`categorize_token()`)

```python
def categorize_token(token_type, token_text):
    """Classify tokens into categories for frontend filtering"""
    categories = []
    
    # Comments
    if "comment" in type_lower:
        categories.append("comment")
    
    # String content
    if "string" in type_lower and ("content" in type_lower or "fragment" in type_lower):
        categories.append("string_content")
    
    # CRITICAL: JSX text content (treat like string content)
    if token_type == "jsx_text":
        categories.append("string_content")
    
    # String delimiters
    if token_text in {'"', "'", "`"}:
        categories.append("string_delimiter")
    
    # Punctuation
    if token_text in {":", ";", ",", "."}:
        categories.append("punctuation")
    
    # Split brackets (essential for ergonomic filtering)
    if token_text in {"(", ")"}:
        categories.append("parenthesis")
    if token_text in {"{", "}"}:
        categories.append("curly_brace")
    if token_text in {"[", "]"}:
        categories.append("square_bracket")
    if token_text in {"<", ">", "</", "/>"}:
        categories.append("angle_bracket")
    
    # Operators
    if token_text in {large_operator_set}:
        categories.append("operator")
    
    return categories
```

**Critical Decision**: `jsx_text` tokens are categorized as `string_content` because:
1. They represent displayable content (like string literals)
2. Shouldn't be typed (just like string content)
3. Follow same exclusion rules across all modes
4. Semantically accurate (it IS content, not structure)

This decision prevents bugs like the one fixed in Session 37 where JSX text appeared in Minimal mode.

#### 4. JSX Text Whitespace Splitting (`split_jsx_text_token()`)

```python
def split_jsx_text_token(row):
    """
    Split jsx_text tokens to separate content from whitespace.
    Example: "Debounced: " → [
        {"TEXT": "Debounced:", "BASE_TYPEABLE": True},
        {"TEXT": " ", "BASE_TYPEABLE": False}
    ]
    """
    text = row["TEXT"]
    
    if token_type != "jsx_text" or text == text.strip():
        return [row]  # No splitting needed
    
    tokens = []
    
    # Leading whitespace → jsx_text_whitespace (non-typeable)
    leading_ws = len(text) - len(text.lstrip())
    if leading_ws > 0:
        tokens.append(create_whitespace_token(text[:leading_ws]))
    
    # Content → jsx_text (typeable)
    content = text.strip()
    if content:
        tokens.append(create_content_token(content))
    
    # Trailing whitespace → jsx_text_whitespace (non-typeable)
    trailing_ws = len(text) - len(text.rstrip())
    if trailing_ws > 0:
        tokens.append(create_whitespace_token(text[-trailing_ws:]))
    
    return tokens
```

**Why split?** Tree-sitter parses `"Debounced: "` as a single `jsx_text` token, but we want:
- The text "Debounced:" to be typeable
- The trailing space to be non-typeable (structural whitespace)

This splitting happens **only for TSX/JSX files** during parsing.

### JSON Output Format

```json
{
  "language": "tsx",
  "total_lines": 20,
  "lines": [
    {
      "line_number": 0,
      "indent_level": 0,
      "actual_line": "export const MyComponent = () => {",
      "display_tokens": [
        {
          "text": "export",
          "type": "keyword",
          "categories": [],
          "base_typeable": true,
          "start_col": 0,
          "end_col": 6
        },
        {
          "text": " ",
          "type": "whitespace",
          "categories": [],
          "base_typeable": false,
          "start_col": 6,
          "end_col": 7
        }
      ],
      "typing_sequence": "exportconstMyComponent",
      "char_map": {
        "0": {"token_idx": 0, "display_col": 0},
        "6": {"token_idx": 1, "display_col": 7}
      }
    }
  ]
}
```

**Key fields**:
- `display_tokens` - All tokens with full metadata
- `typing_sequence` - Pre-computed from `base_typeable` tokens (used as baseline)
- `char_map` - Maps character index → token index and display position
- `categories` - Array of category strings for filtering

---

## Token Categorization

### Category System

TreeType uses **9 token categories** for granular filtering:

| Category | Description | Example Tokens |
|----------|-------------|----------------|
| `keyword` | Language keywords | `def`, `if`, `const`, `async` |
| `identifier` | User-defined names | Variable, function names |
| `comment` | Comments/docstrings | `#`, `//`, `/* */` |
| `string_content` | String literal content + JSX text | `"Hello"`, `<p>Text</p>` |
| `string_delimiter` | Quote characters | `"`, `'`, `` ` `` |
| `punctuation` | Structural punctuation | `:`, `;`, `,`, `.` |
| `parenthesis` | Round brackets | `(`, `)` |
| `curly_brace` | Curly brackets | `{`, `}` |
| `square_bracket` | Square brackets | `[`, `]` |
| `angle_bracket` | Angle brackets (JSX) | `<`, `>`, `</`, `/>` |
| `operator` | Operators | `=`, `+`, `->`, `=>` |

### Category Assignment Rules

**Type-based categories**:
- Keywords, identifiers → Assigned by tree-sitter type
- Comments → Any token with "comment" in type name
- String content → Tokens with "string" + "content" in type name, OR `jsx_text`
- String delimiters → Explicit text matching `"`, `'`, `` ` ``

**Text-based categories**:
- Punctuation → Text in `{:;,.}`
- Brackets → Text-based matching (allows split categorization)
- Operators → Text in large operator set

**Critical Design Decision**: Brackets are categorized by **text**, not type. This allows:
```python
# Tree-sitter might return type="(" 
# We categorize by text: "(" → "parenthesis"
```

This enables precise filtering: "exclude square brackets but keep parentheses."

### Special Cases

#### JSX Text Content

```tsx
<p>Loading item...</p>
```

Tree-sitter tokenizes as:
- `<` - type: `<`, categories: `["angle_bracket"]`
- `p` - type: `identifier`, categories: `[]`
- `>` - type: `>`, categories: `["angle_bracket"]`
- `Loading item...` - type: `jsx_text`, categories: `["string_content"]` ⭐
- `</` - type: `</`, categories: `["angle_bracket"]`
- `p` - type: `identifier`, categories: `[]`
- `>` - type: `>`, categories: `["angle_bracket"]`

**Why `jsx_text` gets `string_content`**:
- It's displayable text (like string literals)
- Shouldn't be typed (matches string behavior)
- Excluded in Minimal and Standard modes (like strings)

#### Whitespace

```python
def test():
    pass
#   ^^^^ - These 4 spaces are structural whitespace
```

- Type: `whitespace`
- Categories: `[]` (no categories)
- `base_typeable`: `false`

**Rule**: Structural whitespace (indentation, spacing) is NEVER typeable.

---

## Frontend Architecture

**Language**: TypeScript  
**Build Tool**: Vite  
**Testing**: Vitest

### Module Structure

```
src/
├── app.ts                 # Main application orchestration
├── core/                  # Core business logic
│   ├── config.ts          # Mode filtering, preset definitions
│   ├── timer.ts           # WPM, accuracy, time calculations
│   └── storage.ts         # localStorage wrapper
├── ui/                    # User interface components
│   ├── renderer.ts        # Progressive reveal rendering
│   └── keyboard.ts        # Input handling, validation
├── types/                 # TypeScript type definitions
│   ├── snippet.ts         # Token, Line, SnippetData types
│   ├── state.ts           # TestState, SnippetInfo types
│   └── config.ts          # PresetConfig, UserConfig types
└── utils/
    └── diagnostics.ts     # Debugging utilities
```

### Core Module: `config.ts`

**Responsibility**: Apply typing mode filters to snippet data

#### Preset Definitions

```typescript
export const PRESETS: PresetsConfig = {
  minimal: {
    name: "Minimal",
    description: "Type only keywords and identifiers",
    exclude: [
      "parenthesis", "curly_brace", "square_bracket", "angle_bracket",
      "operator", "punctuation", "string_content", "string_delimiter", "comment"
    ]
  },
  standard: {
    name: "Standard",
    description: "Balanced practice without pinky strain (recommended)",
    exclude: [
      "curly_brace", "square_bracket", "angle_bracket",
      "string_content", "punctuation", "string_delimiter", "comment"
    ],
    includeSpecific: [":", ".", ",", "(", ")"]  // High priority overrides
  },
  full: {
    name: "Full",
    description: "Type everything except whitespace and comments",
    exclude: ["comment", "string_content"]
  }
};
```

#### Filter Application (`applyExclusionConfig()`)

**Three critical rules** applied in order:

```typescript
export function applyExclusionConfig(lineData: Line, preset: TypingMode): Line {
  const config = PRESETS[preset];
  
  const filteredTokens = lineData.display_tokens.map((token, idx) => {
    let typeable = token.base_typeable;
    
    // RULE 1: Whitespace is NEVER typeable
    if (token.text.trim() === "") {
      return { ...token, typeable: false };
    }
    
    // RULE 2: JSX tag names follow angle_bracket exclusion rules
    if (token.type === "identifier" || token.type === "type_identifier") {
      const prevToken = lineData.display_tokens[idx - 1];
      const nextToken = lineData.display_tokens[idx + 1];
      
      // Detect: < tagname > or </ tagname >
      if ((prevToken?.text === "<" || prevToken?.text === "</") &&
          (nextToken?.text === ">" || nextToken?.text === "/>")) {
        
        // Apply same exclusion as angle brackets
        if (config.exclude.includes("angle_bracket")) {
          return { ...token, typeable: false };
        }
      }
    }
    
    // RULE 3: includeSpecific has highest priority
    if (config.includeSpecific?.includes(token.text)) {
      return { ...token, typeable: true };
    }
    
    // If no categories, default to typeable (keywords, identifiers)
    if (!token.categories || token.categories.length === 0) {
      return { ...token, typeable: true };
    }
    
    // Check if any category is excluded
    for (const category of token.categories) {
      if (config.exclude.includes(category)) {
        typeable = false;
        break;
      }
    }
    
    return { ...token, typeable };
  });
  
  // Regenerate typing_sequence and char_map
  // ...
}
```

**Why these rules?**

1. **Whitespace rule**: Prevents accidental spacebar typing, ensures smooth flow
2. **JSX tag name rule**: Semantic consistency—if `<` and `>` aren't typed, neither should `p` in `<p>`
3. **includeSpecific rule**: Allows Standard mode to include `()` despite excluding `parenthesis` category

### Core Module: `renderer.ts`

**Responsibility**: Render tokens with progressive reveal states

#### Token State Classes

```typescript
.char-untyped     // Gray, not yet reached
.char-current     // Yellow highlight, next to type
.char-error       // Red, wrong key pressed
// No class       // Syntax-colored, already typed
```

#### Rendering Logic

```typescript
export class CodeRenderer {
  renderLineTokens(container: HTMLElement, lineData: Line, lineIndex: number, state: TestState) {
    lineData.display_tokens.forEach((token, tokenIdx) => {
      const span = document.createElement("span");
      span.className = token.type;  // Syntax highlighting class
      
      // Split token text into individual characters for state tracking
      token.text.split("").forEach((char, charIdx) => {
        const charSpan = document.createElement("span");
        charSpan.textContent = char;
        
        // Determine state class
        if (lineIndex < state.currentLineIndex) {
          // Already completed line - all chars typed
          charSpan.className = "";  // Syntax color only
        } else if (lineIndex === state.currentLineIndex) {
          // Current active line
          const globalCharIndex = computeCharIndex(token, charIdx);
          
          if (globalCharIndex < state.currentCharIndex) {
            // Already typed
            charSpan.className = "";
          } else if (globalCharIndex === state.currentCharIndex) {
            // Current character
            charSpan.className = state.errorOnCurrentChar ? "char-error" : "char-current";
          } else {
            // Not yet typed
            charSpan.className = "char-untyped";
          }
        } else {
          // Future line - all untyped
          charSpan.className = "char-untyped";
        }
        
        span.appendChild(charSpan);
      });
      
      container.appendChild(span);
    });
  }
}
```

**Key insight**: Each character is wrapped in a `<span>` for individual state tracking. Token-level span provides syntax coloring, character-level span provides state class.

### Core Module: `keyboard.ts`

**Responsibility**: Handle input, validate characters, update state

```typescript
export class KeyboardHandler {
  handleKeyPress(event: KeyboardEvent) {
    // Special keys
    if (event.key === "Tab") {
      event.preventDefault();
      this.togglePause();
      return;
    }
    
    if (event.key === "Escape") {
      this.resetTest();
      return;
    }
    
    // Block input during pause
    if (this.state.paused) return;
    
    // Get expected character
    const expectedChar = this.getCurrentExpectedChar();
    
    // Validate input
    if (event.key === expectedChar) {
      this.handleCorrectKey();
    } else {
      this.handleIncorrectKey();
    }
  }
  
  handleCorrectKey() {
    // Clear error state
    this.state.errorOnCurrentChar = false;
    
    // Advance cursor
    this.state.currentCharIndex++;
    this.state.totalCharsTyped++;
    
    // Check if line complete
    if (this.isLineComplete()) {
      this.advanceToNextLine();
    }
    
    this.render();
  }
  
  handleIncorrectKey() {
    // Set error state (persists until correct key)
    this.state.errorOnCurrentChar = true;
    this.state.totalErrors++;
    
    this.render();
  }
}
```

**Key behavior**: Error state persists until user types the correct character. No backspace, no skipping—must fix errors to proceed.

---

## Data Flow

### Loading a Snippet

```
User selects language → 
  Fetch snippets/metadata.json → 
    User selects snippet → 
      Fetch snippets/<language>/<id>.json → 
        Parse JSON → 
          Apply preset filter (config.ts) → 
            Render initial state (renderer.ts)
```

### Typing Flow

```
User presses key → 
  keyboard.ts validates → 
    Update state (currentCharIndex, errors, etc.) → 
      renderer.ts re-renders current line → 
        Update stats display (timer.ts) → 
          If line complete, advance to next line
```

### Mode Switching

```
User changes preset → 
  applyExclusionConfig() re-filters tokens → 
    Regenerate typing_sequence → 
    Regenerate char_map → 
      Reset test state → 
        Re-render with new filtered tokens
```

**Key insight**: Mode switching is instant because JSON contains all tokens. We just re-filter client-side.

---

## Critical Implementation Details

### Bug Fix: JSX Text Categorization (Session 37)

**Problem**: JSX text content appeared in Minimal/Standard modes  
**Root Cause**: `jsx_text` tokens had `categories: []`  
**Solution**: Assign `string_content` category to `jsx_text`

**Before**:
```json
{
  "text": "Loading item...",
  "type": "jsx_text",
  "categories": []  // ❌ No category = included in all modes
}
```

**After**:
```json
{
  "text": "Loading item...",
  "type": "jsx_text",
  "categories": ["string_content"]  // ✅ Excluded in Minimal/Standard
}
```

**Why this works**:
- Minimal mode excludes `string_content` → excludes JSX text ✅
- Standard mode excludes `string_content` → excludes JSX text ✅
- Full mode includes `string_content` → includes JSX text (for typing) ✅

### JSX Tag Name Detection

**Problem**: When `<` and `>` are excluded, tag names should also be excluded

**Detection logic**:
```typescript
const prevToken = lineData.display_tokens[idx - 1];
const nextToken = lineData.display_tokens[idx + 1];

if ((prevToken?.text === "<" || prevToken?.text === "</") &&
    (nextToken?.text === ">" || nextToken?.text === "/>")) {
  // This is a JSX tag name
  if (config.exclude.includes("angle_bracket")) {
    typeable = false;
  }
}
```

**Why pattern matching?** JSX tag names are just `identifier` tokens. We need contextual detection to distinguish:
- `<div>` - tag name (should follow angle bracket rules)
- `myVar` - regular identifier (should always be typeable)

### Whitespace Handling

**Rule**: Whitespace is NEVER typeable, even in Full mode

**Implementation**:
```typescript
if (token.text.trim() === "") {
  return { ...token, typeable: false };
}
```

**Why?** 
- Structural whitespace (indentation, line breaks) isn't meaningful to type
- Users advance by typing content, not spaces
- Prevents accidental spacebar presses

**Exception**: Spaces **within** string content or JSX text are part of the token text:
```python
"Hello World"  # Space is part of string_content token
```

But string_content is excluded in Minimal/Standard modes anyway.

---

## Performance Considerations

### Parser Performance

- **Parsing time**: ~50-200ms per file (depending on size)
- **JSON size**: ~2-10KB per snippet (highly compressible)
- **Batch processing**: Can parse 100 files in ~10 seconds

### Frontend Performance

- **JSON loading**: <10ms per snippet
- **Filter application**: <1ms per line
- **Render time**: <5ms for 50-line snippet
- **Re-render on keypress**: <1ms (only affected lines)

### Optimization Strategies

1. **Pre-computed typing_sequence** - Baseline computed once during parsing
2. **Lazy rendering** - Only render visible lines (future enhancement)
3. **Event delegation** - Single keypress handler, not per-character
4. **Debounced stats updates** - Update WPM every 100ms, not every keystroke

---

## Testing Strategy

### Parser Tests

```python
# Test token categorization
def test_jsx_text_gets_string_content_category():
    token_type = "jsx_text"
    categories = categorize_token(token_type, "Hello")
    assert "string_content" in categories

# Test whitespace splitting
def test_jsx_text_whitespace_split():
    row = {"TEXT": "Hello ", "TYPE": "jsx_text"}
    tokens = split_jsx_text_token(row)
    assert len(tokens) == 2
    assert tokens[0]["TEXT"] == "Hello"
    assert tokens[1]["TEXT"] == " "
    assert tokens[1]["BASE_TYPEABLE"] == False
```

### Frontend Tests (Vitest)

```typescript
// Test mode filtering
describe("applyExclusionConfig", () => {
  it("excludes jsx_text in minimal mode", () => {
    const line = createMockLine([
      { text: "Hello", type: "jsx_text", categories: ["string_content"] }
    ]);
    
    const filtered = applyExclusionConfig(line, "minimal");
    
    expect(filtered.display_tokens[0].typeable).toBe(false);
    expect(filtered.typing_sequence).toBe("");
  });
});

// Test JSX tag name detection
describe("JSX tag name filtering", () => {
  it("excludes tag names when angle brackets excluded", () => {
    const line = createMockLine([
      { text: "<", type: "<", categories: ["angle_bracket"] },
      { text: "div", type: "identifier", categories: [] },
      { text: ">", type: ">", categories: ["angle_bracket"] }
    ]);
    
    const filtered = applyExclusionConfig(line, "minimal");
    
    expect(filtered.display_tokens[1].typeable).toBe(false);
  });
});
```

### Integration Tests

```typescript
describe("Complete typing flow", () => {
  it("handles full typing sequence with mode switches", async () => {
    // Load snippet
    const app = new TreeTypeApp();
    await app.loadSnippet("python", "sample");
    
    // Type in Standard mode
    typeSequence("defcalculate");
    expect(app.state.currentCharIndex).toBe(13);
    
    // Switch to Full mode
    app.changeMode("full");
    expect(app.state.currentCharIndex).toBe(0);  // Reset on mode change
    
    // Type in Full mode
    typeSequence("defcalculate(");
    expect(app.state.currentCharIndex).toBe(14);
  });
});
```

---

## Design Decisions & Rationale

### Why TypeScript?

**Benefits realized**:
- ✅ Caught the `jsx_text` categorization bug during type checking
- ✅ IDE autocomplete for all data structures
- ✅ Refactoring safety (rename, restructure)
- ✅ Self-documenting code (types are documentation)

**Cost**:
- Build step required (Vite)
- Learning curve for TypeScript newcomers
- More verbose than plain JavaScript

**Verdict**: Worth it. Type safety prevented bugs and enabled confident refactoring.

### Why Static JSON Files?

**Alternative considered**: Parse on-demand in browser using tree-sitter WASM

**Why rejected**:
- Slower initial load (WASM + parsing)
- Larger bundle size (~500KB for WASM)
- More complex error handling
- No benefit for pre-curated snippets

**Static JSON wins**:
- Instant loading
- Smaller payloads
- Parse errors caught during build
- Can pre-compute metadata (line count, difficulty)

### Why Category-Based Filtering?

**Alternative considered**: Type-based filtering (e.g., "exclude all operators")

**Why rejected**:
- Types are too granular (tree-sitter has 100+ types)
- Can't express "exclude `{` but include `(`"
- Hard to create balanced presets

**Category system wins**:
- Semantic grouping (punctuation, brackets, operators)
- Split brackets enable ergonomic presets
- Easy to understand ("exclude angle brackets")

---

## Future Architecture Considerations

### Phase 7: Expanded Test Coverage

- Add integration tests for all 4 languages
- Test edge cases (nested JSX, template literals)
- Performance benchmarks

### Phase 8: Performance Optimization

- Lazy rendering for long snippets
- Virtual scrolling for large libraries
- Web Worker for heavy computations

### Phase 9: Advanced Features

- User snippet uploads (client-side parsing with WASM)
- Custom preset creation
- Analytics and progress tracking

### Phase 10: Scalability

- Snippet CDN for faster loading
- Server-side snippet search
- Real-time leaderboards

---

## Conclusion

TreeType's architecture prioritizes:
1. **Simplicity** - Two-stage design, static files, zero backend
2. **Performance** - Pre-computed data, instant loading
3. **Correctness** - TypeScript types, semantic categorization
4. **Maintainability** - Modular code, comprehensive tests

The jsx_text categorization bug (5 sessions to fix) highlighted the importance of accurate documentation and semantic consistency. This architecture document serves as ground truth to prevent future mismatches between implementation and assumptions.

---

_For user-facing documentation, see README.md_  
_For formal requirements, see REQUIREMENTS.md_  
_For development history, see session_*.md files_
