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

# Visit http://localhost:3000
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

---

## 📚 Library System

### Browsing Snippets

Click **"📚 Browse Library"** to view all available code snippets:

- Filter by language
- Search by name or tags
- Sort by various criteria
- View snippet stats (best WPM, accuracy, practice count)

### Adding Your Own Code (Quick Workflow)

Adding custom code files to practice is fully automated. Simply follow these steps:

```bash
# 1. (Optional) Put your source file inside sources/
mkdir -p sources/python/
cp ~/my-project/utils.py sources/python/

# 2. Run the automated parsing and indexing workflow
./build/add_snippet.sh sources/python/utils.py

# 3. Start development server and test it!
pnpm dev
# Visit your local browser library and search for your snippet
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
│  Source Code (.py, .js, .ts, .tsx)                  │
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
│  JSON Snippets (public/<language>/*.json)           │
│  • Static files served directly by Vite             │
│  • Contains: tokens, categories, positions          │
│  • Pre-computed for instant loading                 │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Frontend (TypeScript + Vite)                       │
│  • Loads JSON snippets from public directory        │
│  • Applies mode-based filtering (config.ts)         │
│  • Renders progressive reveal UI                    │
│  • Handles keyboard input and state                 │
└─────────────────────────────────────────────────────┘
```

### Two-Stage Architecture

**Stage 1: Parser (Offline)**

- Runs on developer machine
- Analyzes code using tree-sitter
- Generates static JSON files straight into the `public/` directory
- Categorizes every token for filtering

**Stage 2: Frontend (Runtime)**

- Loads pre-parsed JSON served at `/`
- Applies typing mode filters dynamically
- Renders progressive reveal experience
- Tracks metrics and state

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
├── sources/                    # Your raw source files (gitignored)
│   ├── python/
│   ├── javascript/
│   ├── typescript/
│   └── tsx/
├── public/                     # Static assets served by Vite (committed)
│   ├── metadata.json          # Master library index (generated)
│   ├── python/*.json          # Pre-parsed JSON files
│   ├── javascript/*.json
│   ├── typescript/*.json
│   └── tsx/*.json
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

### Adding New Snippets (Quick Workflow)

To process and add any new snippet, use the shell command:

```bash
# Quick workflow
./build/add_snippet.sh sources/python/myfile.py

# Verify locally
pnpm dev

# Sync/deploy live on Firebase
pnpm run deploy
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

## 🤝 Contributing

TreeType is in active development. Contributions welcome!

### Ways to Contribute

- **Add snippets** - Share useful code snippets via PR
- **Report bugs** - Open issues for bugs or UX problems
- **Suggest features** - Ideas for improvements
- **Test languages** - Help test with different codebases

---

## ❓ FAQ

### Why only 4 languages?

These cover the most common web/data development scenarios. Tree-sitter supports 40+ languages—adding more is straightforward. Focus is on quality over quantity.

### Can I use this offline?

Yes! Once cloned and built, everything runs locally. No internet required.

### What's the WPM calculation?

Standard typing metric: `(characters_typed / 5) / (time_in_minutes)`. The "5" is industry standard for average word length. So 300 characters in 1 minute = 60 WPM.

### Can I customize the color scheme?

Not yet, but it's planned for Phase 10. Currently uses VS Code Dark+ theme.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

**Ready to build muscle memory for code? Clone, run, and start typing!** 🚀

_Built with ❤️ by developers, for developers_

_Last updated: Post-Consolidated Public Assets Migration_
