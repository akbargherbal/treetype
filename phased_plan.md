## 🎯 Phased Implementation Plan: Tree-Sitter Typing Game

### Philosophy (Borrowed from Speedtyper Success)

- **Baseline first**: Prove each layer works before adding complexity
- **Incremental validation**: Each phase has clear success criteria
- **Low-risk assumptions**: Test what we think we know
- **Rollback-friendly**: Each phase is independently functional
- **Documentation-driven**: Context docs prevent re-explaining decisions

---

## Phase 1: Static Rendering Foundation (Days 1-2)

### Goal
**Prove we can render parsed code as styled HTML with proper indentation—no typing logic yet.**

### What We're Testing
- Tree-sitter parsing works for Python/JS/TS/TSX
- We can convert tokens to display-ready JSON
- Frontend can render tokens with Tailwind indentation
- Syntax highlighting maps token types to colors

### Tasks

**1.1: Finalize Parsing Pipeline** (2 hours)
- Use your existing sanity check code (already works ✅)
- Add token classification: `is_non_typeable()`
- Add indentation calculation: `start_col // 4`
- Output: JSON per line with display tokens

```python
# Expected output structure
{
    "line_number": 4,
    "indent_level": 0,
    "tokens": [
        {"text": "def", "type": "def", "typeable": true},
        {"text": " ", "type": "whitespace", "typeable": false},
        {"text": "calculate", "type": "identifier", "typeable": true},
        # ... etc
    ]
}
```

**1.2: Create Sample JSON Files** (1 hour)
- Export 3 sample files:
  - `python_sample.json` (Fibonacci function)
  - `javascript_sample.json` (React component stub)
  - `typescript_sample.json` (API client)

**1.3: Build Static HTML Renderer** (3 hours)
- Create simple HTML page (no React, just vanilla JS for speed)
- Read JSON via `fetch()`
- Render each line as `<div>` with tokens as `<span>`
- Apply Tailwind padding: `pl-${indent_level * 4}`

```html
<!-- Example output -->
<div class="line">
  <span class="pl-0">
    <span class="keyword">def</span>
    <span class="identifier">calculate</span>
    <span class="punctuation">(</span>
    <!-- ... -->
  </span>
</div>
```

**1.4: Add Syntax Highlighting** (2 hours)
- Map token types to Tailwind colors
  - `def`, `function`, `class` → `text-purple-500`
  - `identifier` → `text-blue-400`
  - `string_content` → `text-green-400`
  - `number` → `text-orange-400`
  - `comment` → `text-gray-500`
- Test with all 3 sample files

**1.5: Test Multi-line Tokens** (1 hour)
- Add docstring example to Python sample
- Verify: Does it render correctly?
- Decision point: Single block or split by line?

### Success Criteria
- ✅ Can visually inspect rendered code
- ✅ Indentation looks correct (matches source)
- ✅ Syntax colors match expectations
- ✅ Multi-line strings display (even if imperfect)
- ✅ No typing functionality yet (that's Phase 2)

### Deliverables
- `render_code.html` - Static renderer
- `sample_*.json` - Test data
- Screenshot comparison: rendered vs source

### Risk Assessment
- **Low risk**: No backend, no complex state
- **If it fails**: Parsing assumptions are wrong—fix before continuing

---

## Phase 2: Typing Sequence Logic (Days 3-4)

### Goal
**Prove we can create a typeable character sequence and track cursor position—no auto-jump yet.**

### What We're Testing
- Can filter typeable vs non-typeable tokens
- Can flatten tokens into character sequence
- Can map typed characters to display positions
- Can highlight current typing position

### Tasks

**2.1: Add Typeable Filter to Parser** (1 hour)
- Modify Phase 1 JSON output to include `typeable` flag
- Generate second field: `typing_sequence` (flattened string)

```python
# Enhanced output
{
    "line_number": 4,
    "indent_level": 0,
    "display_tokens": [...],  # All tokens
    "typing_sequence": "defcalculatefibonaccinintListint",  # Only typeable
    "char_map": {
        0: {"token_idx": 0, "display_col": 0},  # 'd' at col 0
        3: {"token_idx": 1, "display_col": 4},  # 'c' at col 4 (after space)
        # ...
    }
}
```

**2.2: Build Typing Input Handler** (3 hours)
- Add `<input>` field to HTML renderer
- Listen to `keypress` events
- Compare input to `typing_sequence`
- Track: current character index

**2.3: Add Visual Feedback** (2 hours)
- Highlight current character/token being typed
- Show: characters typed correctly (green)
- Show: characters not yet typed (gray)
- Show: current cursor position (blinking underline)

**2.4: Test Manual Typing** (1 hour)
- Type through a full line manually
- Verify: highlight moves correctly
- Verify: wrong keys don't advance cursor
- Verify: correct keys advance to next typeable char

**2.5: Handle Spaces Manually** (1 hour)
- User types: `d` `e` `f` `[SPACE]` `c` `a` `l` ...
- Verify: Space advances to next token
- Note: This is NOT auto-jump—testing baseline behavior

### Success Criteria
- ✅ Can type through entire snippet character-by-character
- ✅ Visual feedback shows progress
- ✅ Wrong keys don't advance
- ✅ Typing sequence matches expectations
- ✅ Manual space bar advances cursor

### Deliverables
- Enhanced JSON with `typing_sequence` + `char_map`
- Updated `render_code.html` with typing input
- Video/GIF demonstrating manual typing

### Risk Assessment
- **Medium risk**: Character mapping could be complex
- **If it fails**: Simplify—test with single line first

---

## Phase 3: Auto-Jump Experimentation (Days 5-6)

### Goal
**Test if auto-jump feels natural—skip space bar, cursor jumps automatically.**

### What We're Testing
- User experience of auto-jump
- Does it feel faster or jarring?
- Do users understand what's happening?
- Edge cases: punctuation clusters, operators

### Tasks

**3.1: Implement Auto-Jump Logic** (2 hours)
- After correct character typed: check if next char is non-typeable
- If yes: skip to next typeable character
- Update visual cursor position

**3.2: Add Configuration Toggle** (1 hour)
- Checkbox: "Enable auto-jump"
- Allow switching between manual space and auto-jump
- Persist preference in localStorage

**3.3: Conduct User Testing** (3 hours)
- Test yourself: Type 5 snippets with auto-jump ON
- Test yourself: Type 5 snippets with auto-jump OFF
- Record: WPM, error rate, subjective feel
- Ask: Does auto-jump feel natural or disorienting?

**3.4: Test Edge Cases** (2 hours)
- Dense punctuation: `func(x, y, z)`
- Operators: `x += 5`
- Strings with spaces: `"hello world"`
- Comments: `# this is a comment`

**3.5: Iterate on Feedback** (2 hours)
- If jarring: Add smooth animation for cursor jump
- If confusing: Add visual cue (e.g., fade effect)
- If natural: Keep it, move to Phase 4

### Success Criteria
- ✅ Auto-jump implemented and configurable
- ✅ Subjective assessment: "This feels good/bad"
- ✅ Edge cases documented
- ✅ Decision made: Keep or remove auto-jump

### Deliverables
- Updated renderer with auto-jump toggle
- Testing notes document
- Decision: Keep, modify, or remove feature

### Risk Assessment
- **High risk**: UX might not match expectations
- **If it fails**: Revert to manual spaces—no harm done

---

## Phase 4: Multi-Line & Navigation (Day 7)

### Goal
**Handle multi-line typing, line completion, snippet completion.**

### What We're Testing
- Advancing from line to line
- Handling empty lines
- Snippet completion detection
- Result display (WPM, accuracy)

### Tasks

**4.1: Add Line Advancement** (2 hours)
- When line typing sequence complete: move to next line
- Reset cursor to start of new line
- Highlight next line

**4.2: Handle Edge Cases** (2 hours)
- Empty lines (blank lines in code)
- Lines with only comments (if excluded from typing)
- Last line completion (trigger results)

**4.3: Add Metrics Calculation** (2 hours)
- Track: start time, end time
- Calculate: WPM (standard formula)
- Calculate: accuracy (correct chars / total chars)
- Display: results screen

**4.4: Test Full Snippets** (2 hours)
- Type through entire Python function
- Type through JavaScript class
- Verify: metrics accurate
- Verify: smooth line transitions

### Success Criteria
- ✅ Can complete full multi-line snippets
- ✅ Line transitions smooth
- ✅ Metrics calculate correctly
- ✅ Results display properly

### Deliverables
- Full typing game prototype
- Metrics display screen
- Video of complete typing session

---

## Phase 5: Language Support & Configuration (Day 8-9)

### Goal
**Test all 4 languages, add configuration UI.**

### What We're Testing
- Python, JS, TS, TSX parsing all work
- Syntax highlighting correct for each
- User can select language
- User can configure exclusion rules

### Tasks

**5.1: Test All Languages** (3 hours)
- Parse samples for each language
- Render side-by-side comparison
- Verify: token types consistent
- Fix: any language-specific issues

**5.2: Add Language Selector** (1 hour)
- Dropdown: Python | JavaScript | TypeScript | TSX
- Load appropriate sample JSON
- Update syntax highlighting scheme

**5.3: Add Configuration Panel** (3 hours)
- Checkboxes for exclusion rules:
  - ☐ Exclude comments
  - ☐ Exclude punctuation (`:`, `;`, `,`)
  - ☐ Exclude brackets (`()`, `[]`, `{}`)
  - ☐ Exclude operators (`=`, `+`, `-`)
  - ☐ Exclude string delimiters
- Regenerate typing sequence on change

**5.4: Test Configurations** (2 hours)
- Minimal: All exclusions ON
- Moderate: Comments + delimiters excluded
- Full: Only comments excluded
- Document: Which feels best?

### Success Criteria
- ✅ All 4 languages supported
- ✅ Configuration UI functional
- ✅ Can test different exclusion sets
- ✅ Preference saved

---

## Phase 6: File Upload & Snippet Management (Days 10-11)

### Goal
**Allow users to practice their own code.**

### What We're Testing
- File upload flow
- Parsing user-uploaded files
- Snippet validation (too long/short?)
- Error handling for bad syntax

### Tasks

**6.1: Add File Upload UI** (2 hours)
- Drag-and-drop zone
- File type validation (.py, .js, .ts, .tsx)
- Read file content with FileReader API

**6.2: Client-Side Parsing** (3 hours)
- Load tree-sitter WASM in browser
- Parse uploaded file
- Generate JSON (same structure as Phase 1)
- Display result

**6.3: Add Validation** (2 hours)
- Check: snippet length (100-500 chars ideal)
- Check: line count (5-15 lines ideal)
- Warn: if snippet too long/short
- Option: auto-split long files

**6.4: Snippet Library** (2 hours)
- Store snippets in localStorage
- List view: uploaded snippets
- Select snippet to practice
- Delete option

### Success Criteria
- ✅ Can upload own code
- ✅ Parses correctly
- ✅ Can practice uploaded code
- ✅ Snippets persist across sessions

---

## Phase 7: Polish & Edge Cases (Days 12-14)

### Goal
**Refine UX, handle remaining edge cases, prepare for deployment.**

### Tasks
- Add loading states
- Improve error messages
- Add keyboard shortcuts
- Test on different screen sizes
- Performance optimization (if needed)
- Final documentation
- Create demo video

---

## 🚨 Phase Gates (Decision Points)

After each phase, evaluate:

1. **Does this work as expected?** → Continue
2. **Does this feel good?** → Continue
3. **Is this worse than expected?** → Pivot or simplify

### Example Decision Points:

**Phase 2 Gate:** If typing sequence mapping is too complex:
- **Option A**: Simplify to word-level (not char-level)
- **Option B**: Skip auto-jump (stay with spaces)

**Phase 3 Gate:** If auto-jump feels bad:
- **Option A**: Remove feature, document decision
- **Option B**: Modify (add animations, visual cues)

**Phase 6 Gate:** If client-side tree-sitter WASM doesn't work:
- **Option A**: Pre-parse files, upload JSON
- **Option B**: Build simple backend API

---

## 📋 Session Handoff Template

When starting next session:

```markdown
## Current Status
- **Phase:** [1-7]
- **Task:** [Specific task from plan]
- **Blockers:** [Any issues]
- **Files modified:** [List paths]

## Context Documents
- [x] CONTEXT.md (this tree-sitter project)
- [x] TREE_SITTERS_PYTHON_EXAMPLE_12.md (sanity check)
- [x] speedtyper_context.md (reference project)
- [x] speedtyper_plan.md (reference methodology)

## Next Steps
[What you want to work on this session]
```

---

## 🎯 Success Definition

**Minimum Viable Product (End of Phase 4):**
- ✅ Can render code with proper indentation/highlighting
- ✅ Can type through multi-line snippets
- ✅ Auto-jump tested (keep or remove decision made)
- ✅ Basic metrics displayed

**Full Product (End of Phase 7):**
- ✅ All 4 languages supported
- ✅ Users can upload own code
- ✅ Configurable exclusion rules
- ✅ Polished UX
- ✅ Ready for personal use

---

