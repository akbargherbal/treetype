# TreeType - Build Programming Muscle Memory

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A typing trainer that helps developers practice typing real code with progressive reveal.**

TreeType uses tree-sitter parsing to intelligently extract code tokens and create a focused, distraction-free typing experience. As you type, code progressively reveals itself through syntax coloring—you're not just matching characters, you're **painting code into existence**.

---

## 🎯 What is TreeType?

TreeType is specialized typing practice for developers that focuses on:

- **Real code patterns** - Brackets, operators, punctuation, indentation
- **Progressive reveal** - Code starts gray and reveals syntax colors as you type
- **Configurable difficulty** - Three modes from minimal (keywords only) to full (everything)
- **Four languages** - Python, JavaScript, TypeScript, TSX/React
- **Zero setup** - Runs entirely in the browser

### What TreeType is NOT

- **Not a code editor** - It's a focused practice tool
- **Not a memorization tool** - You see the code as you type
- **Not a comprehensive typing tutor** - Assumes you can type; builds code-specific speed

---

## 🚀 Quick Start

### Play Online

Visit the live demo at [your-github-pages-url] and start typing immediately.

### Run Locally

```bash
# Clone repository
git clone https://github.com/yourusername/treetype.git
cd treetype

# Install dependencies
pnpm install

# Start development server
pnpm dev

# Visit http://localhost:5173
```

### First Use

1. **Choose your language** - Start with Python if unsure (most readable)
2. **Select Standard mode** ⭐ - Recommended balance of challenge and speed
3. **Press any key to start** - Type only the highlighted yellow characters
4. **Press Tab to pause** - Resume with Tab again
5. **Press Esc anytime** - Reset and try again

---

## 🎮 How to Play

### Controls

| Key                | Action                         |
| ------------------ | ------------------------------ |
| **Any key**        | Start test                     |
| **Character keys** | Type the highlighted character |
| **Tab**            | Pause/resume test              |
| **Esc**            | Reset test immediately         |

### Visual Feedback

- **Gray text** - Not yet typed (neutral canvas)
- **Yellow highlight** - Current character to type
- **Syntax colors** - Already typed (code revealed)
- **Red highlight** - Wrong key (persists until corrected)

### Typing Modes

#### Minimal Mode ⚡

**Type**: Keywords and identifiers only  
**Skip**: All brackets, operators, punctuation, string content, comments

**Best for**: Speed practice, learning new syntax patterns quickly

**Example**:

```python
def calculate(n: int) -> list:
```

You type: `defcalculatenintlist`

---

#### Standard Mode ⭐ (Recommended)

**Type**: Keywords, identifiers, operators, parentheses `()`, and essential punctuation (`:`, `.`, `,`)  
**Skip**: Curly braces `{}`, square brackets `[]`, angle brackets `<>`, string content, comments

**Best for**: Balanced practice with realistic code structure

**Example**:

```javascript
setIsActive(!isActive);
```

You type: `setIsActive(!isActive)`

**Why this mode?**

- ✅ Practices function call patterns `()`
- ✅ Includes operators and essential punctuation
- ✅ Reduces pinky strain (no Shift+bracket combinations)
- ✅ TSX/JSX friendly (angle brackets auto-reveal)

---

#### Full Mode 🎯

**Type**: Everything except whitespace, comments, and string content  
**Skip**: Only structural whitespace, comments, string literal content

**Best for**: Maximum muscle memory building

**Example**:

```python
def calculate(n: int) -> list:
```

You type: `defcalculate(n:int)->list:`

---

## 📚 Library System

### Browsing Snippets

Click **"📚 Browse Library"** to view all available code snippets:

- Filter by language
- Search by name or tags
- Sort by various criteria
- View snippet stats (best WPM, accuracy, practice count)

### Adding Your Own Code

```bash
# 1. Add source file to sources/<language>/
cp ~/my-project/utils.py sources/python/

# 2. Parse the file
python build/parse_json.py sources/python/utils.py

# 3. Update metadata
python build/build_metadata.py

# 4. Verify it appears
pnpm dev
# Visit library and search for your snippet
```

### Snippet Guidelines

**Ideal snippets**:

- 5-50 lines (sweet spot: 10-20 lines)
- Self-contained functions or components
- Real production code (not tutorials)
- Clear, idiomatic syntax

**Avoid**:

- Very long files (200+ lines)
- Code with excessive comments
- Minified or obfuscated code

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────┐
│  Source Code (.py, .js, .ts, .tsx)                 │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Parser (Python + Tree-Sitter)                      │
│  • Tokenizes code into AST                          │
│  • Categorizes tokens (9 categories)                │
│  • Marks typeability (base_typeable flag)           │
│  • Splits JSX text from whitespace                  │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  JSON Snippets (snippets/<language>/*.json)         │
│  • Static files committed to repo                   │
│  • Contains: tokens, categories, positions          │
│  • Pre-computed for instant loading                 │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Frontend (TypeScript + Vite)                       │
│  • Loads JSON snippets                              │
│  • Applies mode-based filtering (config.ts)         │
│  • Renders progressive reveal UI                    │
│  • Handles keyboard input and state                 │
└─────────────────────────────────────────────────────┘
```

### Two-Stage Architecture

**Stage 1: Parser (Offline)**

- Runs on developer machine
- Analyzes code using tree-sitter
- Generates static JSON files
- Categorizes every token for filtering

**Stage 2: Frontend (Runtime)**

- Loads pre-parsed JSON
- Applies typing mode filters dynamically
- Renders progressive reveal experience
- Tracks metrics and state

**Key Insight**: No server needed. Parser runs offline, snippets are static files, everything is pre-computed.

---

## 🔧 Technical Details

### Token Categorization

Every token gets assigned to one or more of **9 categories**:

| Category           | Examples                       | Purpose                  |
| ------------------ | ------------------------------ | ------------------------ |
| `keyword`          | `def`, `if`, `const`           | Language keywords        |
| `identifier`       | Variable names, function names | User-defined names       |
| `comment`          | `#`, `//`, `/* */`             | Comments and docstrings  |
| `string_content`   | Text inside `"..."`            | String literal content   |
| `string_delimiter` | `"`, `'`, `` ` ``              | Quote characters         |
| `punctuation`      | `:`, `;`, `,`, `.`             | Structural punctuation   |
| `parenthesis`      | `(`, `)`                       | Function calls, grouping |
| `curly_brace`      | `{`, `}`                       | Blocks, objects          |
| `square_bracket`   | `[`, `]`                       | Arrays, indexing         |
| `angle_bracket`    | `<`, `>`, `</`, `/>`           | JSX/TSX tags             |
| `operator`         | `=`, `+`, `->`, `=>`           | Operators                |

**Critical Implementation Detail**: `jsx_text` tokens (JSX text content like `<p>Hello</p>`) are assigned the `string_content` category because they represent displayable content that shouldn't be typed, just like string literals.

### Typing Mode Filtering

Each mode defines categories to **exclude**:

```typescript
// From src/core/config.ts
PRESETS = {
  minimal: {
    exclude: [
      "parenthesis",
      "curly_brace",
      "square_bracket",
      "angle_bracket",
      "operator",
      "punctuation",
      "string_content",
      "string_delimiter",
      "comment",
    ],
  },
  standard: {
    exclude: [
      "curly_brace",
      "square_bracket",
      "angle_bracket",
      "string_content",
      "punctuation",
      "string_delimiter",
      "comment",
    ],
    includeSpecific: [":", ".", ",", "(", ")"], // Override exclusions
  },
  full: {
    exclude: ["comment", "string_content"],
  },
};
```

**Three Critical Filtering Rules** (applied in `applyExclusionConfig()`):

1. **Whitespace is NEVER typeable** - Structural whitespace (spaces, tabs, newlines) is always skipped
2. **JSX tag names follow angle bracket rules** - If `<` and `>` are excluded, tag names between them are also excluded
3. **includeSpecific has highest priority** - Characters in this list are always typeable, overriding category exclusions

### JSX Text Handling (Bug Fix from Session 37)

**Problem**: JSX text content like `<p>Loading item...</p>` was incorrectly appearing in Minimal/Standard modes.

**Root Cause**: `jsx_text` tokens had empty `categories: []`, so they weren't excluded by any preset.

**Solution** (2 lines in `build/parse_json.py`):

```python
# JSX text content (treat like string content)
if token_type == "jsx_text":
    categories.append("string_content")
```

**Why this is correct**:

- JSX text content IS displayable content (like strings)
- Shouldn't be typed (just like string literals)
- Follows same exclusion rules as `string_content`
- Semantically accurate categorization

### Progressive Reveal System

Characters transition through states as you type:

1. **Untyped** (gray, class: `char-untyped`)
2. **Current** (yellow highlight, class: `char-current`)
3. **Typed** (syntax-colored, no special class)
4. **Error** (red highlight, class: `char-error`, persists until corrected)

Non-typeable tokens automatically transition from gray → colored as the cursor passes them, creating a smooth "painting" effect.

---

## 🛠️ Development

### Prerequisites

```bash
# Python (for parser)
pip install pandas tree-sitter tree-sitter-python tree-sitter-javascript tree-sitter-typescript

# Node.js (for frontend)
pnpm install
```

### Project Structure

```
treetype/
├── build/                      # Build tools
│   ├── parse_json.py          # Parser (Python + tree-sitter)
│   ├── build_metadata.py      # Metadata generator
│   └── add_snippet.sh         # Workflow automation
├── snippets/                   # Pre-parsed JSON (committed)
│   ├── metadata.json          # Master library index
│   ├── python/*.json
│   ├── javascript/*.json
│   ├── typescript/*.json
│   └── tsx/*.json
├── sources/                    # Your source files (gitignored)
│   ├── python/
│   ├── javascript/
│   ├── typescript/
│   └── tsx/
├── src/                        # Frontend TypeScript
│   ├── app.ts                 # Main application
│   ├── core/                  # Core logic
│   │   ├── config.ts          # Mode filtering
│   │   ├── timer.ts           # Metrics calculation
│   │   └── storage.ts         # localStorage wrapper
│   ├── ui/                    # UI components
│   │   ├── renderer.ts        # Progressive reveal rendering
│   │   └── keyboard.ts        # Input handling
│   ├── types/                 # TypeScript definitions
│   │   ├── snippet.ts         # Token/Line/Snippet types
│   │   ├── state.ts           # Test state types
│   │   └── config.ts          # Configuration types
│   └── utils/
├── tests/                      # Vitest test suite
├── index.html                  # Main typing game
├── library.html                # Snippet browser
├── vite.config.ts              # Vite configuration
└── tsconfig.json               # TypeScript configuration
```

### Adding New Snippets

```bash
# Quick workflow
./build/add_snippet.sh sources/python/myfile.py

# Manual workflow
python build/parse_json.py sources/python/myfile.py
python build/build_metadata.py

# Verify
pnpm dev
# Check library for new snippet
```

### Running Tests

```bash
pnpm test           # Run tests once
pnpm test:watch     # Watch mode
pnpm test:ui        # Visual test UI
```

### Building for Production

```bash
pnpm build          # TypeScript compile + Vite build
pnpm preview        # Preview production build locally
```

---

## 📊 Progress & Roadmap

### ✅ Completed Phases

- **Phase 1-2** - Tree-sitter parsing, static rendering, typing sequence logic
- **Phase 3-3.5** - Progressive reveal UX (the breakthrough moment)
- **Phase 4** - Multi-language support (Python, JS, TS, TSX)
- **Phase 5** - Configuration system (3 presets, persistence)
- **Phase 6** - TypeScript migration, modular architecture
- **Phase 5 (Bug Fix)** - JSX text categorization (Sessions 33-37, 5 sessions, 8 hours)

### 🔄 Current Status

- **Core experience**: Production-ready ✅
- **Library system**: Fully functional ✅
- **Testing infrastructure**: Vitest setup complete ✅
- **Documentation**: Comprehensive (you are here!) ✅

### 🎯 Future Enhancements

- **Phase 7** - Expanded test coverage
- **Phase 8** - Performance optimization
- **Phase 9** - Analytics and progress tracking
- **Phase 10** - Public deployment and marketing

---

## 🤝 Contributing

TreeType is in active development. Contributions welcome!

### Ways to Contribute

- **Add snippets** - Share useful code snippets via PR
- **Report bugs** - Open issues for bugs or UX problems
- **Suggest features** - Ideas for improvements
- **Test languages** - Help test with different codebases

### Development Guidelines

- Follow existing TypeScript style
- Test locally before submitting PR
- Add snippets to `sources/<language>/` directory
- Run parser and metadata builder before committing
- Update documentation if changing behavior

---

## 📖 Documentation

- **README.md** (this file) - Overview and user guide
- **ARCHITECTURE.md** - Technical design and implementation details
- **REQUIREMENTS.md** - Formal requirements specification
- **ts_migration_plan.md** - TypeScript migration roadmap
- **session\_\*.md** - Development session notes

---

## 🙏 Acknowledgments

- [Tree-Sitter](https://tree-sitter.github.io/) - The parsing library that makes intelligent code analysis possible
- [Vite](https://vitejs.dev/) - Lightning-fast build tool
- [TypeScript](https://www.typescriptlang.org/) - Type safety and developer experience
- [Tailwind CSS](https://tailwindcss.com/) - Rapid UI development
- [VS Code Dark+](https://code.visualstudio.com/) - Syntax highlighting theme inspiration

---

## ❓ FAQ

### Why only 4 languages?

These cover the most common web/data development scenarios. Tree-sitter supports 40+ languages—adding more is straightforward. Focus is on quality over quantity.

### Can I use this offline?

Yes! Once cloned and built, everything runs locally. No internet required.

### What's the WPM calculation?

Standard typing metric: `(characters_typed / 5) / (time_in_minutes)`. The "5" is industry standard for average word length. So 300 characters in 1 minute = 60 WPM.

### Why TypeScript?

Type safety prevents bugs (like the jsx_text categorization bug we spent 5 sessions fixing). TypeScript caught similar issues during migration.

### Can I customize the color scheme?

Not yet, but it's planned for Phase 10. Currently uses VS Code Dark+ theme.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

**Ready to build muscle memory for code? Clone, run, and start typing!** 🚀

_Built with ❤️ by developers, for developers_

_Last updated: Session 38 - Post-Phase 6, comprehensive documentation_
