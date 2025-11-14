## 🎯 Phased Implementation Plan: Tree-Sitter Typing Game
## **UPDATED VERSION - Post Phase 3.5 Completion**

### Philosophy (Borrowed from Speedtyper Success)

- **Baseline first**: Prove each layer works before adding complexity
- **Incremental validation**: Each phase has clear success criteria
- **Low-risk assumptions**: Test what we think we know
- **Rollback-friendly**: Each phase is independently functional
- **Documentation-driven**: Context docs prevent re-explaining decisions
- **UX-driven iteration**: Respond to user feedback and discoveries

---

## ✅ Phase 1: Static Rendering Foundation (COMPLETE)

### Goal
**Prove we can render parsed code as styled HTML with proper indentation—no typing logic yet.**

### What We Tested
- Tree-sitter parsing works for Python/JS/TS/TSX
- We can convert tokens to display-ready JSON
- Frontend can render tokens with Tailwind indentation
- Syntax highlighting maps token types to colors

### Deliverables
- ✅ `parse_json.py` - Parser with token classification
- ✅ `render_code.html` - Static renderer
- ✅ JSON samples for all 4 languages
- ✅ Syntax highlighting system (VS Code Dark+ theme)

### Success Criteria Met
- ✅ Can visually inspect rendered code
- ✅ Indentation looks correct (matches source)
- ✅ Syntax colors match expectations
- ✅ Multi-line strings display correctly
- ✅ Comments render as atomic blocks

---

## ✅ Phase 2: Typing Sequence Logic (COMPLETE)

### Goal
**Prove we can create a typeable character sequence and track cursor position—no auto-jump yet.**

### What We Tested
- Can filter typeable vs non-typeable tokens
- Can flatten tokens into character sequence
- Can map typed characters to display positions
- Can highlight current typing position

### Deliverables
- ✅ Enhanced JSON with `typing_sequence` + `char_map`
- ✅ Typing input handler with keypress validation
- ✅ Visual feedback system (green/gray/cursor highlighting)
- ✅ Character-by-character advancement logic

### Success Criteria Met
- ✅ Can type through entire snippet character-by-character
- ✅ Visual feedback shows progress
- ✅ Wrong keys don't advance cursor
- ✅ Typing sequence matches expectations

---

## ✅ Phase 3: Auto-Jump Experimentation (COMPLETE)

### Goal
**Test if auto-jump feels natural—skip space bar, cursor jumps automatically.**

### What We Tested
- User experience of auto-jump
- Does it feel faster or jarring?
- Do users understand what's happening?
- Edge cases: punctuation clusters, operators

### Outcome
**DECISION: Auto-jump removed from final design.**

After testing, we determined that:
- Punctuation and brackets are better handled as **non-typeable elements**
- Users should only type **meaningful code characters** (keywords, identifiers, values)
- Non-typeable elements transition from gray → colored automatically as cursor passes
- This creates a cleaner, more intuitive typing experience

### Key Learning
The typing experience should feel like **"revealing" or "painting"** the code into existence, not mechanically matching every character. This insight led directly to Phase 3.5.

---

## ✅ Phase 3.5: Progressive Reveal & Enhanced UX (COMPLETE) ⭐

### Goal
**Transform the typing experience from validation to creation—make it feel like the user is bringing code to life.**

This phase emerged from Phase 3 learnings and represents a fundamental UX enhancement that became the core of the application's value proposition.

### Key Features Implemented

#### 1. **Progressive Color Reveal System**
- **Gray text** = Not yet typed (neutral canvas)
- **Syntax-colored text** = Already typed (code revealed)
- **Yellow highlight** = Current character to type
- **Red highlight** = Error state (persistent until corrected)

**Design Philosophy**: Users "paint" the code into existence. Every keystroke reveals the underlying structure through syntax highlighting.

#### 2. **Persistent Error Feedback**
- Wrong keystrokes turn the current character **red**
- Error persists until user types the correct character
- Prevents advancement until error is resolved
- Clear, actionable feedback without breaking flow

#### 3. **Non-Typeable Element Handling**
- Punctuation, brackets, operators, string delimiters marked as non-typeable
- These elements automatically transition from gray → colored as cursor passes
- Users focus only on meaningful code characters
- Creates smooth, uninterrupted typing rhythm

#### 4. **Ergonomic Scroll System**
- **Manual smart scroll**: Calculates exact target position for line centering
- **Always-down rule**: Prevents disorienting upward scrolling
- **Zen mode spacers**: Invisible top/bottom spacers (40vh) push controls out of view
- **Distraction-free typing**: Controls fade during active typing (hover to restore)
- **Smooth transitions**: CSS `scroll-behavior: smooth` on `<html>` element

#### 5. **Multi-Line Navigation** (Absorbed Phase 4 goals)
- Automatic line advancement when typing sequence complete
- Skip empty lines or lines with no typeable content
- Active line indicator (green border)
- Smooth transitions between lines

#### 6. **Completion Modal & Metrics**
- Beautiful completion modal with celebration UI
- Real-time WPM calculation (5-char word standard)
- Accuracy tracking (correct chars / total chars)
- Time display (MM:SS format)
- Retry and language-switch options

#### 7. **Keyboard Controls**
- **Esc**: Reset test at any time
- **Any key**: Start test from ready state
- **Continuous typing**: No special keys needed, pure flow

### Technical Implementation

#### JSON Schema (from parser):
```json
{
  "lines": [
    {
      "line_number": 0,
      "indent_level": 0,
      "display_tokens": [
        {"text": "def", "type": "keyword", "typeable": true, "start_col": 0},
        {"text": " ", "type": "whitespace", "typeable": false, "start_col": 3},
        {"text": "calculate", "type": "identifier", "typeable": true, "start_col": 4}
      ],
      "typing_sequence": "defcalculate",
      "char_map": {
        "0": {"token_idx": 0, "display_col": 0},
        "3": {"token_idx": 2, "display_col": 4}
      }
    }
  ]
}
```

#### Core Functions:
- `renderLineTokens()`: Applies progressive reveal states to each character
- `handleKeyPress()`: Validates input, updates state, manages error persistence
- `moveToNextLine()`: Advances to next typeable line, triggers scroll
- `manualSmartScroll()`: Ergonomic centering with down-only constraint
- `completeTest()`: Calculates metrics, displays completion modal

### Deliverables
- ✅ `render_code.html` - Full application with all UX enhancements
- ✅ Progressive reveal CSS system
- ✅ Ergonomic scroll implementation
- ✅ Completion modal with metrics
- ✅ Distraction-free mode
- ✅ Full keyboard control system

### Success Criteria Met
- ✅ Typing feels creative and engaging (not mechanical)
- ✅ Errors are clear, persistent, and actionable
- ✅ Scroll behavior is smooth, predictable, ergonomic
- ✅ Non-typeable elements transition seamlessly
- ✅ Metrics accurately reflect performance
- ✅ Controls fade elegantly during typing
- ✅ All 4 languages work identically
- ✅ Reset/retry functionality flawless

### Key Learnings from Phase 3.5

1. **UX Discovery**: The "progressive reveal" concept wasn't in the original plan but emerged as the natural evolution of the typing experience
2. **Scroll Complexity**: Getting scroll behavior right required multiple iterations and diagnostic-driven debugging
3. **State Management**: Persistent error state is crucial for learning-focused typing (vs. speed-focused)
4. **Zen Mode**: Removing distractions during typing significantly improves focus and enjoyment

---

## 🔜 Phase 5: Configuration UI & Dynamic Token Filtering (NEXT)

### Goal
**Allow users to customize what they type via configuration panel.**

### Current Limitation
The parser currently **hardcodes** non-typeable rules:
- Comments: always non-typeable
- String content: always non-typeable
- Punctuation/brackets/operators: always non-typeable

### What Needs to Change

#### 5.1: Refactor Parser to Be Permissive (2-3 hours)
**Objective**: Export all tokens with full metadata, let frontend decide what's typeable.

**Changes to `parse_json.py`**:
```python
def is_non_typeable(token_type, token_text, exclusion_config=None):
    """
    Make this function accept a configuration dict.
    Default behavior: only structural whitespace is non-typeable.
    Everything else is marked as 'potentially_typeable' with metadata.
    """
    # Only structural whitespace is truly non-typeable
    if token_type == 'whitespace' and token_text.strip() == '':
        return True
    
    return False

# Add token category metadata
def categorize_token(token_type, token_text):
    """Classify tokens into categories for frontend filtering"""
    categories = []
    
    if 'comment' in token_type.lower():
        categories.append('comment')
    if 'string' in token_type.lower():
        categories.append('string')
    if token_text in {':', ';', ',', '.'}:
        categories.append('punctuation')
    if token_text in {'(', ')', '[', ']', '{', '}', '<', '>'}:
        categories.append('bracket')
    if token_text in {'=', '+', '-', '*', '/', '%', '!', '&', '|', '^'}:
        categories.append('operator')
    
    return categories
```

**Enhanced JSON output**:
```json
{
  "display_tokens": [
    {
      "text": "#",
      "type": "comment",
      "categories": ["comment"],
      "base_typeable": true,
      "start_col": 0
    }
  ]
}
```

#### 5.2: Build Configuration Panel (3 hours)
**Objective**: Add UI for exclusion preferences.

**UI Design**:
```html
<div class="config-panel">
  <h3>Typing Configuration</h3>
  <div class="config-group">
    <h4>Exclude from typing:</h4>
    <label><input type="checkbox" id="exclude-comments"> Comments</label>
    <label><input type="checkbox" id="exclude-strings"> String Content</label>
    <label><input type="checkbox" id="exclude-punctuation"> Punctuation (:;,.)</label>
    <label><input type="checkbox" id="exclude-brackets"> Brackets (()[]{}<>)</label>
    <label><input type="checkbox" id="exclude-operators"> Operators (=+-*/%)</label>
  </div>
  <div class="config-group">
    <h4>Difficulty Presets:</h4>
    <button onclick="applyPreset('minimal')">Minimal (Code Flow Only)</button>
    <button onclick="applyPreset('moderate')">Moderate (No Comments/Strings)</button>
    <button onclick="applyPreset('full')">Full (Type Everything)</button>
  </div>
</div>
```

#### 5.3: Implement Client-Side Filtering (2 hours)
**Objective**: Regenerate typing sequence based on config.

**Core function**:
```javascript
function applyExclusionConfig(lineData, config) {
  // Filter tokens based on user preferences
  const filteredTokens = lineData.display_tokens.map(token => {
    let typeable = token.base_typeable;
    
    if (config.excludeComments && token.categories.includes('comment')) {
      typeable = false;
    }
    if (config.excludeStrings && token.categories.includes('string')) {
      typeable = false;
    }
    // ... etc for other categories
    
    return { ...token, typeable };
  });
  
  // Regenerate typing_sequence
  const typingSequence = filteredTokens
    .filter(t => t.typeable)
    .map(t => t.text)
    .join('');
  
  // Regenerate char_map
  const charMap = buildCharMap(filteredTokens);
  
  return { ...lineData, display_tokens: filteredTokens, typing_sequence: typingSequence, char_map: charMap };
}
```

#### 5.4: Persist User Preferences (1 hour)
**Objective**: Save config to localStorage.

```javascript
function saveConfig(config) {
  localStorage.setItem('treetype_config', JSON.stringify(config));
}

function loadConfig() {
  const saved = localStorage.getItem('treetype_config');
  return saved ? JSON.parse(saved) : DEFAULT_CONFIG;
}
```

#### 5.5: Test All Configurations (2 hours)
**Objective**: Validate that progressive reveal works with all exclusion combinations.

Test matrix:
- Minimal config (only keywords/identifiers)
- Moderate config (no comments/strings)
- Full config (type everything)
- Custom combinations

### Success Criteria
- ✅ Parser exports all tokens with category metadata
- ✅ Configuration panel functional and intuitive
- ✅ Typing sequence regenerates correctly based on config
- ✅ Progressive reveal works with any configuration
- ✅ Preferences persist across sessions
- ✅ Presets provide quick configuration options

### Estimated Time: 10-12 hours

### Risk Assessment
- **Medium risk**: Regenerating typing sequences client-side could introduce bugs
- **Mitigation**: Extensive testing with all 4 languages and all config combinations
- **Rollback**: Can revert to hardcoded exclusions if client-side filtering proves unstable

---

## 🔜 Phase 6: File Upload & Snippet Management (FUTURE)

### Goal
**Allow users to practice their own code.**

### Prerequisites
- Phase 5 complete (configuration system must work with uploaded files)

### Tasks

#### 6.1: Add File Upload UI (2 hours)
- Drag-and-drop zone
- File type validation (.py, .js, .ts, .tsx)
- Read file content with FileReader API

#### 6.2: Client-Side Parsing (4 hours)
**Option A: WASM Tree-Sitter**
- Load tree-sitter WASM in browser
- Parse uploaded file client-side
- Generate JSON (same structure as backend parser)

**Option B: Backend API**
- Build simple Flask/FastAPI endpoint
- Upload file, receive JSON
- Simpler but requires server

**Recommendation**: Start with Option B for reliability, migrate to WASM if needed.

#### 6.3: Add Validation & Feedback (2 hours)
- Check: snippet length (100-500 chars ideal)
- Check: line count (5-15 lines ideal)
- Warn: if snippet too long/short
- Option: auto-split long files into chunks

#### 6.4: Snippet Library (3 hours)
- Store snippets in localStorage (or backend DB if using Option B)
- List view: uploaded snippets
- Select snippet to practice
- Delete/edit options
- Tag system for organization

#### 6.5: Integration with Config System (1 hour)
- Uploaded files must respect user's exclusion config
- Apply same filtering logic as built-in samples

### Success Criteria
- ✅ Can upload own code files
- ✅ Parses correctly with user's config applied
- ✅ Can practice uploaded code
- ✅ Snippets persist across sessions
- ✅ Library management is intuitive

### Estimated Time: 12-15 hours

### Risk Assessment
- **High risk if WASM**: Browser compatibility, bundle size
- **Low risk if backend**: Simple API, proven approach
- **Mitigation**: Start with backend, WASM is optional optimization

---

## 🔜 Phase 7: Polish & Edge Cases (FUTURE)

### Goal
**Refine UX, handle remaining edge cases, prepare for deployment.**

### Tasks

#### 7.1: Performance Optimization (2 hours)
- Profile rendering performance with large snippets
- Optimize token rendering if needed
- Lazy load language parsers if using WASM

#### 7.2: Accessibility (2 hours)
- Keyboard navigation audit
- Screen reader support (ARIA labels)
- High contrast mode
- Font size controls

#### 7.3: Additional Keyboard Shortcuts (1 hour)
- `Ctrl+R`: Retry current snippet
- `Ctrl+L`: Change language
- `Ctrl+,`: Open config panel
- `?`: Show help overlay

#### 7.4: Error Handling & Edge Cases (2 hours)
- Handle network errors (if using backend)
- Handle parsing failures gracefully
- Empty file uploads
- Corrupted JSON recovery
- Browser compatibility testing

#### 7.5: Help & Onboarding (2 hours)
- First-time user tutorial overlay
- Tooltips for config options
- Example videos/GIFs
- FAQ section

#### 7.6: Analytics & Feedback (2 hours)
- Track: average WPM over time
- Track: most practiced languages
- Track: error patterns (which chars cause most mistakes)
- Export: practice history as CSV

#### 7.7: Visual Polish (2 hours)
- Loading states and spinners
- Better animations (token reveal, line transitions)
- Theme customization (dark/light mode variants)
- Custom font options

#### 7.8: Documentation (2 hours)
- User guide
- Developer documentation
- API documentation (if backend)
- Contribution guidelines

### Success Criteria
- ✅ Performance smooth even with large files
- ✅ Accessible to all users
- ✅ Professional, polished feel
- ✅ Comprehensive error handling
- ✅ Clear documentation
- ✅ Ready for public release

### Estimated Time: 15-20 hours

---

## 📊 Progress Summary

| Phase | Status | Completion | Time Spent |
|-------|--------|-----------|------------|
| **Phase 1** | ✅ Complete | 100% | ~8 hours |
| **Phase 2** | ✅ Complete | 100% | ~6 hours |
| **Phase 3** | ✅ Complete | 100% | ~4 hours |
| **Phase 3.5** | ✅ Complete | 100% | ~12 hours |
| **Phase 4** | ✅ Absorbed by 3.5 | 100% | (included above) |
| **Phase 5** | 🔜 Next | 0% | Est. 10-12 hours |
| **Phase 6** | 🔜 Future | 0% | Est. 12-15 hours |
| **Phase 7** | 🔜 Future | 0% | Est. 15-20 hours |

**Total Completed**: ~30 hours  
**Remaining Estimated**: ~40-50 hours  
**Total Project**: ~70-80 hours

---

## 🎯 Current Product Status

### ✅ **Minimum Viable Product: ACHIEVED**

The application currently has:
- ✅ Beautiful, engaging typing experience
- ✅ 4 language support (Python, JS, TS, TSX)
- ✅ Progressive reveal system
- ✅ Real-time metrics (WPM, accuracy)
- ✅ Completion tracking
- ✅ Ergonomic scroll system
- ✅ Distraction-free mode
- ✅ Professional visual design

### 🎯 **Value Proposition**

**TreeType is already usable and valuable** for:
- Developers learning to type code faster
- Anyone wanting to practice syntax muscle memory
- People who find traditional typing games boring
- Developers who want to improve flow state while coding

### 🚀 **Next Value Unlocks**

**Phase 5** unlocks:
- Customizable difficulty levels
- Practice specific syntax patterns (e.g., only brackets, only keywords)
- Tailored learning paths

**Phase 6** unlocks:
- Practice your own codebase
- Learn new frameworks by typing their examples
- Muscle memory for your team's coding style

**Phase 7** unlocks:
- Public release readiness
- Community features
- Long-term engagement tracking

---

## 📝 Session Handoff Template

When starting next session:

```markdown
## Current Status
- **Phase**: 5 (Configuration UI)
- **Last Completed**: Phase 3.5 - Progressive Reveal System
- **Next Task**: Refactor parser to export token categories
- **Blockers**: None
- **Files to modify**: `parse_json.py`, `render_code.html`

## Context Documents
- [x] phased_plan.md (this file - UPDATED)
- [x] 3.5.md (Phase 3.5 goals document)
- [x] session_10.md (ergonomic scroll breakthrough)
- [x] session_11.md (spacer fix, Phase 3.5 sign-off)

## Next Steps
1. Review Phase 5 requirements
2. Refactor `is_non_typeable()` to be config-aware
3. Add token categorization function
4. Export enhanced JSON with category metadata
5. Build configuration panel UI
```

---

## 🎉 Celebration Points

Take a moment to appreciate what's been built:

1. **Session 10**: Solved a complex UX problem (scroll behavior) through systematic debugging
2. **Session 11**: Identified and fixed language-switching bug with spacer solution
3. **Phase 3.5**: Created a genuinely delightful typing experience that transforms code practice from a chore into creative flow

**The foundation is rock solid. The UX is polished. The path forward is clear.**

Ready for Phase 5 when you are! 🚀
