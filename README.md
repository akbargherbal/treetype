# TreeType

**Build muscle memory for programming constructs**

TreeType is a typing trainer that helps developers practice typing actual code syntax, not just words. Using tree-sitter parsing, it intelligently extracts the meaningful parts of code and creates a focused, distraction-free typing experience.

---

## What is TreeType?

Traditional typing games make you type random words or prose. TreeType makes you type **real code** with proper syntax highlighting, indentation, and structure.

As you type, the code progressively reveals itself through color—you're not just matching characters, you're **painting the code into existence**. It feels less like a test and more like creating something.

### What TreeType is NOT

- **Not a code editor** - It's a focused practice tool, not a replacement for your IDE
- **Not a comprehensive typing tutor** - It assumes you already know how to type; it builds speed and accuracy on code-specific patterns
- **Not a memorization tool** - You see the code you're typing; this is about muscle memory, not recall

---

## Features

### Core Experience
- **Progressive reveal system** - Code starts gray and reveals its syntax colors as you type
- **4 language support** - Python, JavaScript, TypeScript, and TSX/React
- **3 typing modes** - Customize difficulty from minimal (keywords only) to full (everything)
- **Real-time metrics** - Track WPM, accuracy, and time as you type
- **Distraction-free mode** - Controls fade during typing, reveal on hover
- **Persistent configuration** - Your language and mode preferences are saved

### UX Features
- **Smart scrolling** - Code stays centered as you progress, no jarring jumps
- **Persistent error feedback** - Wrong keys turn red until corrected
- **Automatic line advancement** - Seamlessly flows from line to line
- **Completion celebration** - Beautiful modal with your final stats
- **Keyboard-first design** - Esc to reset, any key to start, pure flow

---

## Quick Start

### Prerequisites
- Python 3.x (for local file server)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. Clone or download this repository:
```bash
git clone https://github.com/yourusername/TreeType.git
cd TreeType
```

2. Start a local web server:
```bash
python -m http.server 8000
```

3. Open your browser and navigate to:
```
http://localhost:8000/render_code.html
```

4. Select a language, choose a typing mode, and press any key to start!

### First Use

1. **Choose your language** - Start with Python if unsure (most readable)
2. **Select Standard mode** - It's the recommended balance of challenge and speed
3. **Click into the code area** - Or it will auto-focus when you press a key
4. **Start typing** - Only type the highlighted yellow character
5. **Press Esc anytime** - Reset and try again

---

## Typing Modes Explained

TreeType offers three preset modes that control what you actually type:

### Minimal Mode
**Type**: Keywords and identifiers only  
**Skip**: Brackets, operators, punctuation, quotes, string content, comments

**Use case**: Fastest typing, pure vocabulary focus. Great for warming up or learning new language syntax quickly.

**Example**:
```python
def calculate(n: int) -> list:
```
You type: `defcalculatenintlist`

---

### Standard Mode ⭐ (Recommended)
**Type**: Keywords, identifiers, operators, and structural punctuation (`:`, `;`)  
**Skip**: Brackets, quotes, string content, comments, commas, periods

**Use case**: Balanced practice with realistic code structure. You're typing the "meaningful" parts while the visual noise auto-reveals.

**Example**:
```python
def calculate(n: int) -> list:
```
You type: `defcalculaten:int->list:`

---

### Full Mode
**Type**: Everything except whitespace and comments/string content  
**Skip**: Only whitespace, comments, and string content

**Use case**: Maximum muscle memory building. Every bracket, every operator, every character. Closest to real coding.

**Example**:
```python
def calculate(n: int) -> list:
```
You type: `defcalculate(n:int)->list:`

---

## How It Works

### Architecture Overview

TreeType uses a two-stage architecture:

1. **Parser (Python)** - Analyzes code using tree-sitter and exports structured JSON
2. **Renderer (JavaScript)** - Consumes JSON and creates the interactive typing experience

### Tree-Sitter Parsing

Tree-sitter is a parsing library that understands code syntax at a deep level. TreeType uses it to:

- Extract all tokens (keywords, identifiers, operators, etc.)
- Classify tokens into 6 categories (comments, strings, brackets, operators, punctuation, identifiers)
- Preserve exact positioning and indentation
- Handle multi-line constructs correctly (docstrings, template literals, JSX)

### Token Categorization

Every token in the parsed code gets assigned to one or more categories:

| Category | Examples | Use |
|----------|----------|-----|
| `comment` | `#`, `//`, `/* */` | Comments and docstrings |
| `string_content` | Text inside `"..."` or `` `...` `` | String literal content |
| `string_delimiter` | `"`, `'`, `` ` `` | Quote characters |
| `punctuation` | `:`, `;`, `,`, `.` | Structural punctuation |
| `bracket` | `()`, `[]`, `{}`, `<>` | Brackets and JSX syntax |
| `operator` | `=`, `+`, `->`, `=>` | Operators |

These categories power the preset filtering system. Each mode excludes different categories to create the desired typing experience.

### Progressive Reveal System

The magic of TreeType is how code "appears" as you type:

1. **Gray text** = Not yet typed (neutral canvas)
2. **Yellow highlight** = Current character to type
3. **Syntax colors** = Already typed (code revealed)
4. **Red highlight** = Error (stays until corrected)

Non-typeable tokens (like brackets in Standard mode) automatically transition from gray → colored as your cursor passes them, creating a smooth "painting" effect.

### Client-Side Filtering

When you switch typing modes, TreeType doesn't reload the file—it regenerates the typing sequence on the fly:

1. Filter `display_tokens` based on preset's exclusion rules
2. Rebuild `typing_sequence` from remaining typeable tokens
3. Regenerate `char_map` (character index → display position mapping)
4. Reset test and re-render

This happens instantly and allows mid-test preset switching.

---

## Controls & Keyboard Shortcuts

### During Typing
- **Any key** - Start test from ready state
- **Character keys** - Type the highlighted character
- **Esc** - Reset test immediately, return to ready state

### Anytime
- **Hover over controls** - Reveal faded controls during active typing
- **Click Reset button** - Same as Esc key
- **Change language** - Dropdown in header (resets test)
- **Change typing mode** - Radio buttons (resets test)

### Completion Modal
- **Retry Test** - Reset with same language/mode
- **Change Language** - Close modal, modify settings
- **Esc or click outside** - Close modal

---

## Technical Details (For Developers)

### File Structure
```
TreeType/
├── parse_json.py              # Python parser (tree-sitter → JSON)
├── render_code.html           # Frontend application (single file)
├── output/
│   └── json_samples/          # Pre-generated code samples
│       ├── python_sample.json
│       ├── javascript_sample.json
│       ├── typescript_sample.json
│       └── tsx_sample.json
└── README.md                  # This file
```

### Parser Architecture (`parse_json.py`)

**Key functions**:
- `categorize_token()` - Assigns category labels to tokens
- `is_non_typeable()` - Marks structural whitespace as non-typeable
- `parse_code_to_dataframe()` - Tree-sitter → Pandas DataFrame
- `dataframe_to_json()` - DataFrame → Frontend-ready JSON

**JSON output structure**:
```json
{
  "language": "python",
  "total_lines": 10,
  "lines": [
    {
      "line_number": 0,
      "indent_level": 0,
      "actual_line": "def calculate(n: int):",
      "display_tokens": [
        {
          "text": "def",
          "type": "keyword",
          "categories": [],
          "base_typeable": true,
          "start_col": 0,
          "end_col": 3
        },
        ...
      ],
      "typing_sequence": "defcalculatenint",
      "char_map": {
        "0": {"token_idx": 0, "display_col": 0},
        ...
      }
    }
  ]
}
```

### Frontend Implementation (`render_code.html`)

**Core functions**:
- `applyExclusionConfig()` - Client-side filtering based on preset
- `renderLineTokens()` - Applies progressive reveal states to each character
- `handleKeyPress()` - Validates input, manages error persistence
- `moveToNextLine()` - Advances to next typeable line, triggers scroll
- `manualSmartScroll()` - Ergonomic centering with down-only constraint
- `completeTest()` - Calculates metrics, displays modal

**State management**:
```javascript
testState = {
  active: false,              // Is test running?
  startTime: null,            // Timestamp of first keystroke
  currentLineIndex: 0,        // Which line is active
  currentCharIndex: 0,        // Position in typing_sequence
  totalCharsTyped: 0,         // Correct chars (for WPM)
  totalErrors: 0,             // Wrong keystrokes
  completedLines: Set,        // Lines fully typed
  errorOnCurrentChar: false   // Is current char in error state?
}
```

**Preset filtering logic**:

Each preset defines:
- `exclude` - Array of categories to skip
- `includeSpecific` - Array of specific characters to include (overrides category exclusion)

Example (Standard mode):
```javascript
{
  exclude: ["bracket", "string_content", "string_delimiter", "comment"],
  includeSpecific: [":", ";"]  // Include these despite being in "punctuation"
}
```

### Configuration Persistence

User preferences are saved to `localStorage`:
```javascript
{
  "preset": "standard",    // Last selected typing mode
  "language": "python"     // Last selected language
}
```

Loaded on page load, saved on every change.

---

## Development Philosophy

TreeType was built using a phased, validation-driven approach:

### Principles
1. **Baseline first** - Prove each layer works before adding complexity
2. **Incremental validation** - Each phase has clear success criteria
3. **Low-risk assumptions** - Test what we think we know
4. **Rollback-friendly** - Each phase is independently functional
5. **UX-driven iteration** - Respond to user feedback and discoveries

### Why This Matters

Traditional typing games feel mechanical—you're matching characters, not creating. TreeType's progressive reveal system transforms typing from validation into creation. Every keystroke reveals structure and meaning.

This UX breakthrough emerged from testing, not planning. Phase 3's "auto-jump" experiment failed, leading to the insight that non-typeable elements should auto-reveal rather than require explicit skipping. That insight became the core of the experience.

**Good software emerges from iteration, not specification.**

---

## Roadmap

### ✅ Completed Phases

- **Phase 1** - Static rendering (tree-sitter parsing, syntax highlighting)
- **Phase 2** - Typing sequence logic (cursor tracking, character validation)
- **Phase 3** - Auto-jump experimentation (tested and rejected in favor of progressive reveal)
- **Phase 3.5** - Progressive reveal UX (the core experience, emerged from Phase 3 learnings)
- **Phase 5** - Configuration UI (3 presets, client-side filtering, persistence)

### 📜 Planned Phases

#### Phase 6: File Upload & Snippet Management
- Upload your own code files
- Practice your actual codebase
- Build a personal snippet library
- Tag and organize practice materials

#### Phase 7: Polish & Public Release
- Performance optimization
- Accessibility improvements
- Additional keyboard shortcuts
- Analytics and progress tracking
- Help system and onboarding
- Theme customization
- Public deployment

---

## Project History

TreeType emerged from a simple question: "Why do typing games make you type prose when developers type code?"

The project evolved through **14 development sessions** over several weeks, with each phase validating assumptions and iterating on UX. Key milestones:

- **Session 1-4** - Proved tree-sitter parsing works, built static renderer
- **Session 5-6** - Added typing logic, character-by-character advancement
- **Session 7** - Experimented with auto-jump (ultimately rejected)
- **Session 8-11** - Built progressive reveal system (the breakthrough moment)
- **Session 12** - Fixed critical scroll bug via systematic debugging
- **Session 13** - Implemented full configuration system
- **Session 14** - Systematic testing, fixed hover and reveal bugs, Phase 5 sign-off

For detailed development history, see:
- `phased_plan.md` - Overall vision and roadmap
- `session_*.md` - Individual session notes and decisions
- Git commit history - Code evolution

---

## Contributing

TreeType is currently in active development. The codebase is stable and the core experience is polished, but the project is pre-Phase 6.

### Feedback Welcome

If you use TreeType and have thoughts on:
- UX friction points
- Typing mode balance (too easy/hard?)
- Language support priorities
- Feature suggestions
- Bugs or issues

Please open an issue! Real-world usage insights are invaluable.

### Code Contributions

Not accepting pull requests yet—the architecture may change significantly in Phase 6/7. Check back after public release.

---

## License

MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Acknowledgments

- **Tree-sitter** - The parsing library that makes intelligent code analysis possible
- **Tailwind CSS** - Rapid UI development with utility classes
- **VS Code Dark+** - Syntax highlighting theme inspiration

---

## Questions?

### Why not use existing typing trainers?

Traditional typing trainers focus on prose or random words. Code has unique patterns:
- Frequent use of brackets, operators, punctuation
- Significant indentation and structure
- Language-specific syntax
- Less common character combinations

TreeType is purpose-built for these patterns.

### Why only 4 languages?

Tree-sitter supports 40+ languages, but these 4 cover the most common web/data development scenarios. Adding languages is straightforward—each requires a parser import and sample file. Phase 6 will let users upload their own code in any supported language.

### Can I use this offline?

Yes! Once you've cloned the repo and generated the JSON samples, everything runs locally. No internet required after initial setup.

### Why is the full app in a single HTML file?

Simplicity. For a project this size, bundling tools add complexity without benefit. Everything is readable and hackable in one place. May split into modules in Phase 7 if complexity demands it.

### What's the WPM calculation?

Standard typing metric: (characters typed / 5) / (time in minutes). The "5" is the industry standard for average word length. So 300 characters in 1 minute = 60 WPM.

---

**Ready to build muscle memory for code? Clone, run, and start typing!** 🚀