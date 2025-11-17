# TreeType - Essential Documentation

**A specialized typing trainer for developers that uses progressive reveal to practice real code patterns**

---

## What is TreeType?

TreeType helps developers build muscle memory for typing code. Instead of typing boring text, you practice real Python, JavaScript, TypeScript, and TSX code with intelligent filtering that adapts to your skill level.

### Core Concept: Progressive Reveal

Code starts completely gray. As you type, it "paints" itself into existence with syntax highlighting. You're not just matching characters—you're revealing the code token by token.

**Visual States:**

- **Gray** - Not yet typed
- **Yellow highlight** - Current character (type this)
- **Syntax colored** - Already typed correctly
- **Red** - Error (persists until you type the correct key)

### What Makes It Different

- **Real code patterns** - Practice the punctuation, brackets, and operators you actually use
- **Smart filtering** - Three modes from minimal (keywords only) to full (everything)
- **No setup** - Runs entirely in browser, works offline
- **Zero backend** - Static files only, perfect for GitHub Pages

---

## Quick Start

### Try It Now

Visit [your-deployed-url] and press any key to start typing.

### Run Locally

```bash
git clone https://github.com/yourusername/treetype.git
cd treetype
pnpm install
pnpm dev
```

### Controls

- **Any key** - Start typing
- **Tab** - Pause/resume
- **Esc** - Reset test
- **Type the yellow character** - Progress through code

---

## Typing Modes

### ⚡ Minimal Mode

**Practice**: Keywords and identifiers only  
**Skip**: All brackets, operators, punctuation, strings, comments

```python
def calculate(n: int) -> list:
```

You type: `defcalculatenintlist`

**Best for**: Speed building, learning syntax vocabulary

---

### ⭐ Standard Mode (Recommended)

**Practice**: Keywords, identifiers, operators, `()`, and `:.,`  
**Skip**: `{}`, `[]`, `<>`, strings, comments

```javascript
setIsActive(!isActive);
```

You type: `setIsActive(!isActive)` (semicolon auto-reveals)

**Best for**: Realistic practice without pinky strain. Includes function call patterns but excludes heavy bracket combinations.

**Why this works**: You practice 80% of typing patterns (function calls, operators) while avoiding 20% of ergonomic pain (Shift+bracket combinations).

---

### 🎯 Full Mode

**Practice**: Everything except whitespace, comments, and string content  
**Skip**: Only structural elements

```python
def calculate(n: int) -> list:
```

You type: `defcalculate(n:int)->list:`

**Best for**: Maximum muscle memory building

---

## Architecture Overview

TreeType uses a **two-stage design** that separates parsing (offline) from interaction (runtime):

```
Source Code (.py/.js/.ts/.tsx)
         ↓
Parser (Python + Tree-Sitter) ← Runs on your machine
         ↓
JSON Snippets (static files) ← Committed to repo
         ↓
Frontend (TypeScript + Vite) ← Runs in browser
```

### Why This Architecture?

✅ **No server needed** - Everything is pre-computed  
✅ **Instant loading** - JSON files are immediately parseable  
✅ **Mode switching** - Re-filter client-side, no network requests  
✅ **Free hosting** - Static files work on GitHub Pages  
✅ **Offline capable** - Works without internet

---

## How It Works: Technical Deep Dive

### 1. Parsing Stage (Offline)

**File**: `build/parse_json.py`

Tree-sitter analyzes source code and extracts tokens with metadata:

```python
# Each token gets categorized
categories = []
if "comment" in type: categories.append("comment")
if token_text in {"(", ")"}: categories.append("parenthesis")
if token_type == "jsx_text": categories.append("string_content")  # Critical!
```

**Output**: JSON files in `snippets/<language>/` with:

- All tokens with positions, types, and categories
- Pre-computed typing sequence (baseline)
- Character map (for cursor positioning)

### 2. Token Categories

Every token is assigned to 0+ categories for filtering:

| Category         | Examples                | Purpose                         |
| ---------------- | ----------------------- | ------------------------------- |
| `keyword`        | `def`, `const`, `async` | Language keywords               |
| `identifier`     | Variable/function names | User-defined names              |
| `string_content` | `"Hello"`, JSX text     | Content that shouldn't be typed |
| `punctuation`    | `:`, `;`, `,`, `.`      | Structural punctuation          |
| `parenthesis`    | `(`, `)`                | Function calls, grouping        |
| `curly_brace`    | `{`, `}`                | Blocks, objects                 |
| `square_bracket` | `[`, `]`                | Arrays, indexing                |
| `angle_bracket`  | `<`, `>`                | JSX/TSX tags                    |
| `operator`       | `=`, `+`, `=>`          | Operators                       |
| `comment`        | `#`, `//`               | Comments                        |

### 3. Frontend Filtering (Runtime)

**File**: `src/core/config.ts`

Each mode defines categories to exclude:

```typescript
PRESETS = {
  minimal: {
    exclude: ["parenthesis", "curly_brace", "operator", "punctuation",
              "string_content", "comment", ...all brackets]
  },
  standard: {
    exclude: ["curly_brace", "square_bracket", "angle_bracket",
              "string_content", "comment"],
    includeSpecific: [":", ".", ",", "(", ")"]  // Override exclusions
  },
  full: {
    exclude: ["comment", "string_content"]
  }
}
```

**Three Critical Rules** (in priority order):

1. **Whitespace is NEVER typeable** - Even in Full mode
2. **JSX tag names follow angle bracket rules** - If `<>` excluded, tag names also excluded
3. **includeSpecific has highest priority** - Always typeable, overrides category exclusions

---

## Critical Implementation Details

### JSX Text Content (Bug Fix)

**Problem**: JSX text like `<p>Loading...</p>` appeared in Minimal/Standard modes

**Root Cause**: `jsx_text` tokens had empty categories `[]`

**Solution**: Assign `string_content` category to `jsx_text`

```python
# In parse_json.py
if token_type == "jsx_text":
    categories.append("string_content")
```

**Why this is correct**:

- JSX text IS displayable content (like strings)
- Should be excluded in Minimal/Standard (like strings)
- Semantically accurate categorization

This fix prevents typing `<p>Loading item...</p>` as `Loadingitem` in modes where you shouldn't type content.

### JSX Tag Name Detection

When angle brackets are excluded, tag names should also be excluded:

```typescript
// Detect: <div> or </div>
if (prevToken.text === "<" && nextToken.text === ">") {
  if (config.exclude.includes("angle_bracket")) {
    typeable = false; // Exclude the 'div' identifier
  }
}
```

This ensures semantic consistency: if you're not typing `<>`, you shouldn't type the tag name either.

---

## Adding Your Own Snippets

```bash
# 1. Add source file
cp ~/my-code/utils.py sources/python/

# 2. Parse it
python build/parse_json.py sources/python/utils.py

# 3. Update metadata
python build/build_metadata.py

# 4. Verify
pnpm dev
# Check library for your new snippet
```

**Good snippets**: 5-50 lines, self-contained functions, real production code, clear syntax

**Avoid**: Very long files, excessive comments, minified code

---

## Project Structure

```
treetype/
├── build/                   # Python parsing tools
│   ├── parse_json.py       # Tree-sitter → JSON
│   └── build_metadata.py   # Library index generator
├── snippets/                # Pre-parsed JSON (committed)
│   ├── metadata.json       # Library index
│   ├── python/*.json
│   ├── javascript/*.json
│   ├── typescript/*.json
│   └── tsx/*.json
├── sources/                 # Your source files (gitignored)
├── src/                     # TypeScript frontend
│   ├── app.ts              # Main orchestration
│   ├── core/               # Business logic
│   │   ├── config.ts       # Mode filtering ⭐
│   │   ├── timer.ts        # Metrics calculation
│   │   └── storage.ts      # localStorage wrapper
│   ├── ui/                 # Components
│   │   ├── renderer.ts     # Progressive reveal ⭐
│   │   └── keyboard.ts     # Input handling
│   └── types/              # TypeScript definitions
├── tests/                   # Vitest test suite
└── index.html              # Main app
```

---

## Development

### Prerequisites

```bash
# Python (parser)
pip install tree-sitter tree-sitter-python tree-sitter-javascript tree-sitter-typescript

# Node.js (frontend)
pnpm install
```

### Testing

```bash
pnpm test          # Run once
pnpm test:watch    # Watch mode
pnpm test:ui       # Visual UI
```

### Building

```bash
pnpm build         # Production build
pnpm preview       # Preview locally
```

---

## Metrics & Stats

**Tracked metrics**:

- **WPM** - `(characters_typed / 5) / elapsed_minutes`
- **Accuracy** - `((total_chars - errors) / total_chars) × 100`
- **Time** - Total elapsed (excluding pauses)
- **Errors** - Wrong keys pressed

All metrics update in real-time and display in completion modal.

---

## Key Design Decisions

### Why TypeScript?

✅ Caught the jsx_text bug during migration  
✅ Self-documenting types  
✅ Refactoring confidence  
✅ IDE autocomplete everywhere

### Why Static JSON?

✅ Instant loading (no parsing)  
✅ Smaller payloads than WASM  
✅ Parse errors caught at build time  
✅ Perfect for static hosting

### Why Category-Based Filtering?

✅ Semantic grouping (not type-specific)  
✅ Split brackets enable ergonomic modes  
✅ Easy to understand and extend

---

## Common Issues & Solutions

**Q: JSX text appearing in Minimal mode?**  
A: This was fixed in Session 37. Ensure `jsx_text` tokens have `"string_content"` category.

**Q: Whitespace is typeable?**  
A: Frontend should check `token.text.trim() === ""` and force `typeable: false`.

**Q: Tag names typeable when `<>` excluded?**  
A: Frontend should detect tag name pattern and apply angle bracket exclusion rules.

---

## What's Next

✅ **Phase 1-6 Complete**: Core experience, TypeScript migration, comprehensive docs  
🎯 **Phase 7**: Expanded test coverage  
🎯 **Phase 8**: Performance optimization  
🎯 **Phase 9**: Analytics and progress tracking  
🎯 **Phase 10**: Public deployment

---

## Contributing

Ways to help:

- Add useful code snippets
- Report bugs or UX issues
- Test with different codebases
- Suggest new features

---

## License

MIT License - See LICENSE file

---

**For complete technical details**, refer to:

- **ARCHITECTURE.md** - Implementation deep dive, data flow, performance
- **REQUIREMENTS.md** - Formal spec, all requirements, test cases

Built with ❤️ for developers who want to type code faster.
