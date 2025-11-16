# TreeType - Build Programming Muscle Memory

A typing game for developers that helps you build muscle memory for programming constructs using real code snippets.

**Live Demo**: [Coming in Session 21 - GitHub Pages]

---

## 🎯 What is TreeType?

TreeType is a specialized typing trainer that uses **parsed code snippets** to help developers improve their typing speed and accuracy on real programming syntax. Unlike traditional typing games that use natural language, TreeType focuses on the unique challenges of coding:

- Brackets, operators, and punctuation
- Multi-line structures
- Indentation patterns
- Language-specific syntax

### ✨ Key Features

- **Progressive Reveal**: Type to "paint" code syntax highlighting into existence
- **3 Difficulty Modes**: Minimal, Standard, and Full typing
- **4 Languages**: Python, JavaScript, TypeScript, TSX/React
- **Real-Time Metrics**: WPM, accuracy, completion time
- **Custom Snippets**: Practice your own code (Phase 6)
- **Zero Setup**: Runs entirely in the browser

---

## 🚀 Quick Start

### Play Online

Visit [GitHub Pages URL] and start typing immediately. No installation required.

### Run Locally

```bash
# Clone repository
git clone https://github.com/yourusername/TreeType.git
cd TreeType

# Start local server
python -m http.server 8000

# Visit http://localhost:8000
```

---

## 📚 Custom Snippets (Phase 6)

### Adding Your Own Code

```bash
# 1. Add source file to sources/
cp ~/my-project/utils.py sources/python/

# 2. Run the helper script
./build/add_snippet.sh sources/python/utils.py

# 3. Commit and push
git commit -m "Add utils snippet"
git push

# 4. Snippet appears in library within 1 minute
```

### Supported File Types

- `.py` → Python
- `.js`, `.jsx` → JavaScript
- `.ts` → TypeScript
- `.tsx` → TSX/React

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

## 🎮 How to Play

### Controls

- **Any key**: Start test
- **Esc**: Reset test at any time
- **Type**: Character by character (only typeable characters)

### Visual Feedback

- **Gray text**: Not yet typed
- **Yellow highlight**: Current character to type
- **Colored text**: Already typed (syntax revealed)
- **Red highlight**: Wrong key (persists until corrected)

### Typing Modes

#### Minimal Mode ⚡

Type only keywords and identifiers. Skip all punctuation and brackets.

**Best for**: Speed practice, learning new syntax patterns

#### Standard Mode ⭐ (Recommended)

Type keywords, identifiers, operators, and essential punctuation (`:` `;`). Skip heavy pinky work (brackets).

**Best for**: Balanced practice, real-world coding simulation

#### Full Mode 🎯

Type everything except whitespace and comments. Maximum challenge.

**Best for**: Comprehensive practice, perfectionism

---

## 🏗️ Architecture

TreeType uses a **static-first architecture** with zero backend:

```
Your Machine          GitHub Repository          GitHub Pages
─────────────         ─────────────────         ─────────────
sources/              snippets/                 Live Website
  └── your-code.py      ├── metadata.json         ├── index.html
                        └── python/               └── library.html
                            └── your-code.json
         │                      │                      │
         └──[parse]──────────>  └──[deploy]──────────>
```

**Key insight**: No server needed. Parser runs offline, snippets are static files, GitHub Pages hosts everything for free.

---

## 🛠️ Development

### Prerequisites

```bash
pip install pandas tree-sitter tree-sitter-python tree-sitter-javascript tree-sitter-typescript
```

### Project Structure

```
TreeType/
├── build/                      # Build tools
│   ├── parse_json.py          # CLI parser
│   ├── build_metadata.py      # Metadata generator
│   └── add_snippet.sh         # Workflow automation
├── snippets/                   # Static library (committed)
│   ├── metadata.json          # Master index
│   └── <language>/            # Language-organized snippets
├── sources/                    # Personal code (gitignored)
│   └── <language>/            # Your source files
├── index.html                  # Main typing game
└── library.html                # Snippet browser (Session 21)
```

### Adding New Snippets

```bash
# Manual workflow
python build/parse_json.py sources/python/myfile.py
python build/build_metadata.py
git add snippets/ && git commit && git push

# Automated workflow (recommended)
./build/add_snippet.sh sources/python/myfile.py
git commit -m "Add myfile snippet"
git push
```

### Testing Locally

```bash
# Start local server
python -m http.server 8000

# Visit http://localhost:8000

# Test snippet workflow
echo 'def test(): pass' > sources/python/test.py
./build/add_snippet.sh sources/python/test.py
```

---

## 📊 Technical Details

### Parser (Tree-Sitter)

TreeType uses [Tree-Sitter](https://tree-sitter.github.io/) to parse source code into an abstract syntax tree (AST), then converts it to a token-based JSON format optimized for progressive reveal typing.

**Token Categories**:

- `keyword`, `identifier`, `type_identifier`
- `comment`, `string_content`, `string_delimiter`
- `operator`, `punctuation`
- `parenthesis`, `curly_brace`, `square_bracket`, `angle_bracket`

Each token includes:

- Text content
- Syntax type
- Categories (for filtering)
- Position metadata
- Typeability flag

### Typing Modes (Config System)

Each mode defines which token categories to exclude:

```javascript
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
      "string_delimiter",
      "comment",
    ],
    includeSpecific: [":", ";", ".", ",", "(", ")"],
  },
  full: {
    exclude: ["comment", "string_content"],
  },
};
```

The frontend dynamically regenerates the typing sequence based on the selected preset.

### Progressive Reveal System

As you type, characters transition through states:

1. **Untyped** (gray): Not yet reached
2. **Current** (yellow highlight): Next character to type
3. **Typed** (syntax-colored): Already typed correctly
4. **Error** (red highlight): Wrong key pressed

Non-typeable tokens (excluded by preset) automatically transition from gray to colored as the cursor passes them.

---

## 🎯 Phase Roadmap

### Phase 1-5 ✅ Complete

- Static rendering and syntax highlighting
- Typing sequence logic
- Progressive reveal UX
- Configuration UI with 3 presets
- Enhanced keyboard controls

### Phase 6 ⏳ In Progress (Session 20/21/22)

- **Session 20** ✅: Repository restructure, metadata builder
- **Session 21** 🔜: GitHub Pages, library browser UI
- **Session 22** ⏳: Stats tracking, export/import

### Phase 7 📋 Future

- Performance optimization
- Accessibility improvements
- Additional keyboard shortcuts
- Help/onboarding
- Analytics

---

## 🤝 Contributing

Contributions welcome! This project is currently in active development (Phase 6).

### Ways to Contribute

- **Add snippets**: Share useful code snippets via PR
- **Report bugs**: Open issues for bugs or UX problems
- **Suggest features**: Ideas for improvements
- **Test languages**: Help test with different codebases

### Development Guidelines

- Follow existing code style
- Test locally before submitting PR
- Add snippets to appropriate `snippets/<language>/` directory
- Update metadata with `python build/build_metadata.py`

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- [Tree-Sitter](https://tree-sitter.github.io/) - Parsing library
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [VS Code Dark+ Theme](https://code.visualstudio.com/) - Color scheme inspiration
- Inspired by [MonkeyType](https://monkeytype.com/) and similar typing trainers

---

## 📧 Contact

- **GitHub**: [yourusername/TreeType]
- **Issues**: [Report bugs or request features]

---

## 🎉 Fun Stats

- **Languages supported**: 4 (Python, JS, TS, TSX)
- **Typing modes**: 3 (Minimal, Standard, Full)
- **Sample snippets**: 4 (more coming in Session 21)
- **Lines of code**: ~1,500 (HTML + JS)
- **Backend code**: 0 (static-first architecture)
- **Hosting cost**: $0/month (GitHub Pages)

---

**Built with ❤️ for developers who want to type code faster**

---

_Last updated: Session 20 - Phase 6 in progress_
