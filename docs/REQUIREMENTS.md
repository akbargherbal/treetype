# TreeType Requirements Specification

**Formal requirements that match current implementation**

Version: 1.0 (Post-Phase 6)  
Last Updated: Session 38  
Status: Living Document

---

## Table of Contents

1. [Functional Requirements](#functional-requirements)
2. [Token Categorization Requirements](#token-categorization-requirements)
3. [Typing Mode Requirements](#typing-mode-requirements)
4. [User Interface Requirements](#user-interface-requirements)
5. [Performance Requirements](#performance-requirements)
6. [Data Format Requirements](#data-format-requirements)
7. [Testing Requirements](#testing-requirements)

---

## Functional Requirements

### FR-1: Language Support

**Requirement**: The system SHALL support parsing and typing practice for four programming languages.

**Languages**:
- Python (`.py`)
- JavaScript (`.js`, `.jsx`)
- TypeScript (`.ts`)
- TSX/React (`.tsx`)

**Acceptance Criteria**:
- ✅ Each language uses appropriate tree-sitter grammar
- ✅ Language is auto-detected from file extension
- ✅ All languages share same JSON output format
- ✅ Syntax highlighting is language-specific

---

### FR-2: Progressive Reveal System

**Requirement**: The system SHALL implement a progressive reveal typing experience where code starts gray and reveals syntax colors as the user types.

**States**:
1. **Untyped** - Gray text, character not yet reached
2. **Current** - Yellow highlight, next character to type
3. **Typed** - Syntax-colored, character already typed correctly
4. **Error** - Red highlight, wrong key pressed

**Acceptance Criteria**:
- ✅ Characters transition states based on user input
- ✅ Syntax colors match VS Code Dark+ theme
- ✅ Non-typeable tokens auto-reveal as cursor passes
- ✅ Error state persists until correct key typed

**Rationale**: Progressive reveal creates a "painting code" experience that is more engaging than traditional character-matching.

---

### FR-3: Typing Modes

**Requirement**: The system SHALL provide three typing difficulty modes with configurable token filtering.

**Modes**:

#### FR-3.1: Minimal Mode

**Purpose**: Speed practice, vocabulary focus

**Includes**: Keywords, identifiers only

**Excludes**: 
- All brackets (parentheses, curly, square, angle)
- All operators
- All punctuation
- String content and delimiters
- Comments

**Example**:
```python
def calculate(n: int) -> list:
```
User types: `defcalculatenintlist`

**Acceptance Criteria**:
- ✅ Only keywords and identifiers are typeable
- ✅ All excluded tokens auto-reveal
- ✅ JSX text content is excluded
- ✅ JSX tag names are excluded

---

#### FR-3.2: Standard Mode (Recommended)

**Purpose**: Balanced practice, realistic code patterns

**Includes**: 
- Keywords, identifiers
- Operators
- Parentheses `(` `)`
- Essential punctuation: `:` `;` `,` `.`

**Excludes**:
- Curly braces `{` `}`
- Square brackets `[` `]`
- Angle brackets `<` `>`
- String content and delimiters
- Comments

**Example**:
```javascript
setIsActive(!isActive);
```
User types: `setIsActive(!isActive)` (semicolon auto-reveals)

**Acceptance Criteria**:
- ✅ Parentheses are typeable (function calls)
- ✅ Essential punctuation is typeable (`:`, `.`, `,`)
- ✅ Heavy brackets excluded (reduces pinky strain)
- ✅ JSX angle brackets excluded (including tag names)
- ✅ String content excluded

**Rationale**: Standard mode practices the most common typing patterns (function calls, operators) while reducing ergonomic strain from bracket combinations.

---

#### FR-3.3: Full Mode

**Purpose**: Maximum practice, comprehensive typing

**Includes**: Everything except:
- Whitespace (structural)
- Comments
- String content

**Excludes**:
- Comments
- String content (literal text inside quotes)

**Example**:
```python
def calculate(n: int) -> list:
```
User types: `defcalculate(n:int)->list:`

**Acceptance Criteria**:
- ✅ All brackets are typeable
- ✅ All operators are typeable
- ✅ All punctuation is typeable
- ✅ Comments auto-reveal
- ✅ String content auto-reveals
- ✅ JSX tag names are typeable

---

### FR-4: Keyboard Controls

**Requirement**: The system SHALL provide keyboard-first interaction with no mouse required during typing.

**Controls**:

| Key | Action | Behavior |
|-----|--------|----------|
| Any character key | Start test (if not active) | Begin timing and typing |
| Character keys | Type character | Validate against expected character |
| Tab | Pause/Resume | Toggle pause state, maintain elapsed time |
| Esc | Reset test | Return to ready state, clear progress |

**Acceptance Criteria**:
- ✅ Any key starts test from ready state
- ✅ Only valid characters are accepted
- ✅ Tab pauses without ending test
- ✅ Esc resets immediately
- ✅ No mouse required during typing

**Error Handling**:
- ✅ Wrong key displays error state (red)
- ✅ Error persists until correct key typed
- ✅ Error count increments on wrong key
- ✅ No backspace or correction allowed

---

### FR-5: Metrics Tracking

**Requirement**: The system SHALL track and display real-time typing metrics.

**Metrics**:
1. **WPM (Words Per Minute)** - `(characters_typed / 5) / (elapsed_minutes)`
2. **Accuracy** - `((total_chars - errors) / total_chars) * 100`
3. **Elapsed Time** - Total time minus paused time (MM:SS format)
4. **Completion** - Percentage of snippet typed

**Acceptance Criteria**:
- ✅ WPM updates in real-time during typing
- ✅ Accuracy calculated excluding paused time
- ✅ Time display shows MM:SS format
- ✅ Paused time excluded from calculations
- ✅ Final metrics displayed in completion modal

---

### FR-6: Snippet Library

**Requirement**: The system SHALL provide a browsable library of code snippets with metadata.

**Features**:
- Browse all snippets
- Filter by language
- Search by name or tags
- Sort by various criteria
- View snippet statistics

**Metadata Fields**:
```json
{
  "id": "unique_identifier",
  "name": "Snippet Name",
  "language": "python",
  "path": "snippets/python/filename.json",
  "lines": 25,
  "typeable_chars": 450,
  "difficulty": "intermediate",
  "tags": ["web", "api", "async"],
  "dateAdded": "2025-01-15"
}
```

**Acceptance Criteria**:
- ✅ All snippets appear in library
- ✅ Filtering works for all languages
- ✅ Search matches name and tags
- ✅ User can navigate to any snippet
- ✅ Snippet stats persist across sessions

---

## Token Categorization Requirements

### CR-1: Category System

**Requirement**: The parser SHALL assign each token to zero or more of nine categories for filtering.

**Categories**:
1. `keyword` - Language keywords
2. `identifier` - User-defined names
3. `comment` - Comments and docstrings
4. `string_content` - String literal content (including JSX text)
5. `string_delimiter` - Quote characters
6. `punctuation` - `:`, `;`, `,`, `.`
7. `parenthesis` - `(`, `)`
8. `curly_brace` - `{`, `}`
9. `square_bracket` - `[`, `]`
10. `angle_bracket` - `<`, `>`, `</`, `/>`
11. `operator` - `=`, `+`, `->`, `=>`, etc.

**Acceptance Criteria**:
- ✅ Every token has `categories` array (may be empty)
- ✅ Categories are assigned consistently across languages
- ✅ Multiple categories allowed (e.g., `:` can be both punctuation and operator)

---

### CR-2: JSX Text Content Categorization

**Requirement**: JSX text content SHALL be categorized as `string_content` for consistent filtering across modes.

**Examples**:
```tsx
<p>Hello World</p>
```

The text "Hello World" is `jsx_text` token with category `["string_content"]`.

**Rationale**: JSX text is displayable content (like string literals) and should be excluded from Minimal and Standard modes.

**Acceptance Criteria**:
- ✅ All `jsx_text` tokens have `string_content` category
- ✅ JSX text excluded in Minimal mode
- ✅ JSX text excluded in Standard mode
- ✅ JSX text included in Full mode (for typing practice)

**Reference**: Bug fix from Session 37. Previously, `jsx_text` had empty categories, causing incorrect inclusion in Minimal/Standard modes.

---

### CR-3: Whitespace Handling

**Requirement**: Structural whitespace (spaces, tabs, newlines) SHALL be marked as non-typeable.

**Definition**: Structural whitespace is:
- Indentation (leading spaces/tabs)
- Spacing between tokens
- Newlines

**NOT structural whitespace**:
- Spaces within string content ("Hello World")
- Spaces within JSX text content

**Acceptance Criteria**:
- ✅ All whitespace tokens have `base_typeable: false`
- ✅ Frontend ensures `typeable: false` even if base_typeable is true
- ✅ User never required to press spacebar

**Implementation**:
```python
# Parser (build/parse_json.py)
def is_non_typeable(token_type, token_text):
    if token_type == "whitespace" and token_text.strip() == "":
        return True
    return False
```

```typescript
// Frontend (src/core/config.ts)
if (token.text.trim() === "") {
  return { ...token, typeable: false };
}
```

---

### CR-4: JSX Text Whitespace Splitting

**Requirement**: The parser SHALL split `jsx_text` tokens to separate content from trailing/leading whitespace.

**Example**:
```tsx
<p>Debounced: </p>
```

Tree-sitter parses "Debounced: " as single token. Parser splits to:
1. "Debounced:" - `jsx_text`, `base_typeable: true`, `categories: ["string_content"]`
2. " " - `jsx_text_whitespace`, `base_typeable: false`, `categories: []`

**Acceptance Criteria**:
- ✅ Leading whitespace → separate token, non-typeable
- ✅ Content → separate token, typeable
- ✅ Trailing whitespace → separate token, non-typeable
- ✅ Column positions accurate for each split token

**Rationale**: Prevents spaces from being included in typing sequence when they're structural, not content.

---

## Typing Mode Requirements

### MR-1: Mode Configuration

**Requirement**: Each typing mode SHALL be defined by an exclusion list and optional inclusion list.

**Configuration Structure**:
```typescript
interface PresetConfig {
  name: string;
  description: string;
  exclude: TokenCategory[];
  includeSpecific?: string[];  // Optional override list
}
```

**Acceptance Criteria**:
- ✅ Each mode has clear name and description
- ✅ Exclusion list defines which categories to skip
- ✅ includeSpecific overrides category exclusions
- ✅ Configuration is type-safe (TypeScript)

---

### MR-2: Filter Application Priority

**Requirement**: Token filtering SHALL follow a strict priority order.

**Priority Order** (highest to lowest):
1. **Whitespace check** - If whitespace, NEVER typeable
2. **JSX tag name check** - If between angle brackets, follow angle bracket rules
3. **includeSpecific check** - If in includeSpecific list, ALWAYS typeable
4. **Empty categories check** - If no categories, default typeable (keywords, identifiers)
5. **Category exclusion check** - If any category excluded, not typeable

**Acceptance Criteria**:
- ✅ Whitespace always non-typeable (even in Full mode)
- ✅ JSX tag names follow angle bracket exclusion
- ✅ includeSpecific overrides category exclusion
- ✅ Keywords/identifiers typeable by default
- ✅ Multi-category tokens excluded if ANY category excluded

**Example**:
```typescript
// Token: "(" with categories: ["parenthesis"]
// Mode: Standard with includeSpecific: ["("]
// Result: TYPEABLE (includeSpecific wins)

// Token: "div" with categories: [] (identifier)
// Previous: "<", Next: ">"
// Mode: Minimal (excludes angle_bracket)
// Result: NOT TYPEABLE (JSX tag name detection)
```

---

### MR-3: Dynamic Re-filtering

**Requirement**: The system SHALL support mode switching without reloading snippet data.

**Process**:
1. User changes mode
2. `applyExclusionConfig()` re-filters all tokens
3. Regenerate `typing_sequence` from typeable tokens
4. Regenerate `char_map` (character index → token mapping)
5. Reset test state
6. Re-render with new filtering

**Acceptance Criteria**:
- ✅ Mode switch is instant (<50ms)
- ✅ No network request required
- ✅ Test state resets (prevents partial progress confusion)
- ✅ All three modes work correctly on same snippet

---

## User Interface Requirements

### UI-1: Visual Feedback

**Requirement**: The system SHALL provide clear visual feedback for all typing states.

**State Indicators**:
| State | Visual | CSS Class |
|-------|--------|-----------|
| Untyped | Gray text (`#858585`) | `.char-untyped` |
| Current | Yellow highlight + border | `.char-current` |
| Typed | Syntax color (varies by token type) | (none) |
| Error | Red text + red background | `.char-error` |

**Acceptance Criteria**:
- ✅ Current character has pulsing border animation
- ✅ Error state is immediately visible (red)
- ✅ Syntax colors follow VS Code Dark+ theme
- ✅ Transitions are smooth (CSS transitions)

---

### UI-2: Active Line Highlighting

**Requirement**: The current active line SHALL be visually distinguished.

**Implementation**:
- Green left border (4px, `#10b981`)
- Subtle background highlight on hover (when test inactive)

**Acceptance Criteria**:
- ✅ Only current line has green border
- ✅ Border updates as user progresses
- ✅ Hover effects disabled during active typing

---

### UI-3: Distraction-Free Mode

**Requirement**: Controls SHALL fade during active typing to minimize distraction.

**Behavior**:
- When test active, controls opacity: 0.1
- On hover, controls opacity: 1.0
- Smooth transition (0.3s)

**Acceptance Criteria**:
- ✅ Header fades when typing starts
- ✅ Stats display fades when typing starts
- ✅ Instructions panel fades when typing starts
- ✅ Hovering reveals faded elements
- ✅ Code display always visible

---

### UI-4: Completion Modal

**Requirement**: The system SHALL display a completion modal with final metrics when user finishes typing.

**Modal Contents**:
- Celebration title ("Test Complete!")
- Subtitle with snippet name
- Final WPM (large, prominent)
- Final accuracy percentage
- Total time elapsed
- Action buttons (Retry, Change Language)

**Acceptance Criteria**:
- ✅ Modal appears immediately on completion
- ✅ Modal blocks interaction until closed
- ✅ Metrics are accurate (match real-time display)
- ✅ Esc key closes modal
- ✅ Click outside closes modal
- ✅ Retry button resets same snippet
- ✅ Change Language closes modal

---

### UI-5: Pause Overlay

**Requirement**: The system SHALL display a full-screen pause overlay when test is paused.

**Overlay Contents**:
- Pause icon (large, pulsing)
- "Test Paused" text
- Instructions ("Press Tab to resume")
- Semi-transparent dark background

**Acceptance Criteria**:
- ✅ Overlay covers entire screen
- ✅ Blocks all input except Tab and Esc
- ✅ Blur effect on background
- ✅ Pause button shows active state
- ✅ Timer stops during pause
- ✅ Tab resumes test

---

## Performance Requirements

### PF-1: Load Time

**Requirement**: The system SHALL load snippets with minimal delay.

**Targets**:
- Initial page load: < 1 second
- Snippet load: < 100ms
- Mode switch: < 50ms

**Acceptance Criteria**:
- ✅ JSON files are pre-parsed (no runtime parsing)
- ✅ Syntax highlighting CSS is static
- ✅ No network requests for mode switching
- ✅ Rendering is optimized (minimal DOM updates)

---

### PF-2: Render Performance

**Requirement**: The system SHALL maintain smooth rendering during typing.

**Targets**:
- Keypress to render: < 16ms (60fps)
- Line scroll: smooth (CSS scroll-behavior)
- Stats update: < 5ms

**Acceptance Criteria**:
- ✅ No frame drops during typing
- ✅ Character state updates are instant
- ✅ Scrolling is smooth (no jarring jumps)
- ✅ WPM updates don't cause lag

---

### PF-3: Memory Usage

**Requirement**: The system SHALL efficiently manage memory for large snippets.

**Constraints**:
- Support snippets up to 200 lines
- Support libraries with 100+ snippets
- No memory leaks during long sessions

**Acceptance Criteria**:
- ✅ Snippet data garbage collected when unloaded
- ✅ Event listeners properly cleaned up
- ✅ No retained references to old state
- ✅ Browser memory usage stable over time

---

## Data Format Requirements

### DF-1: JSON Snippet Format

**Requirement**: Parser output SHALL conform to a strict JSON schema.

**Schema**:
```typescript
interface SnippetData {
  language: "python" | "javascript" | "typescript" | "tsx";
  total_lines: number;
  lines: Line[];
}

interface Line {
  line_number: number;
  indent_level: number;
  actual_line: string;
  display_tokens: Token[];
  typing_sequence: string;
  char_map: { [charIndex: string]: { token_idx: number; display_col: number } };
}

interface Token {
  text: string;
  type: string;
  categories: TokenCategory[];
  base_typeable: boolean;
  start_col: number;
  end_col: number;
}
```

**Acceptance Criteria**:
- ✅ All fields are present and correctly typed
- ✅ JSON is valid and parseable
- ✅ No undefined or null values in required fields
- ✅ Array indices are sequential (0, 1, 2, ...)

---

### DF-2: Metadata Format

**Requirement**: Snippet library metadata SHALL conform to a strict JSON schema.

**Schema**:
```typescript
interface LibraryMetadata {
  lastUpdated: string;  // ISO 8601 timestamp
  totalSnippets: number;
  snippets: SnippetMetadata[];
}

interface SnippetMetadata {
  id: string;
  name: string;
  language: "python" | "javascript" | "typescript" | "tsx";
  path: string;
  lines: number;
  typeable_chars: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  tags: string[];
  dateAdded: string;  // ISO 8601 timestamp
}
```

**Acceptance Criteria**:
- ✅ All snippets have unique IDs
- ✅ Paths are correct and files exist
- ✅ Typeable chars match snippet content
- ✅ Difficulty is one of three valid values
- ✅ Tags are lowercase and descriptive

---

## Testing Requirements

### TR-1: Unit Test Coverage

**Requirement**: Core functions SHALL have comprehensive unit test coverage.

**Target Coverage**:
- `src/core/config.ts` - 90%+
- `src/core/timer.ts` - 90%+
- `src/core/storage.ts` - 80%+

**Test Categories**:
- Token filtering logic
- Timer calculations (WPM, accuracy)
- Mode switching
- Edge cases (empty snippets, single-line)

**Acceptance Criteria**:
- ✅ All exported functions tested
- ✅ Edge cases covered
- ✅ Error handling tested
- ✅ Tests run in < 1 second

---

### TR-2: Integration Tests

**Requirement**: Complete user flows SHALL be tested end-to-end.

**Test Scenarios**:
1. Load snippet → Type complete → View results
2. Load snippet → Pause → Resume → Complete
3. Load snippet → Switch mode → Type in new mode
4. Load snippet → Make errors → Correct → Complete

**Acceptance Criteria**:
- ✅ All scenarios pass
- ✅ State transitions are correct
- ✅ Metrics are accurate
- ✅ No race conditions or timing issues

---

### TR-3: Cross-Language Consistency

**Requirement**: All four languages SHALL behave identically given equivalent code.

**Test Cases**:
- Same construct in different languages (e.g., `if` statement)
- Verify same tokens are typeable/non-typeable
- Verify consistent category assignment

**Acceptance Criteria**:
- ✅ Keywords treated consistently
- ✅ Brackets treated consistently
- ✅ String content excluded consistently
- ✅ Comments excluded consistently

---

## Validation & Acceptance

### VA-1: Bug Fix Verification

**Requirement**: The JSX text categorization bug (Session 37) SHALL remain fixed.

**Test Cases**:
1. Load TSX snippet with JSX text content
2. Switch to Minimal mode
3. Verify JSX text is not in typing sequence
4. Switch to Standard mode
5. Verify JSX text is not in typing sequence
6. Switch to Full mode
7. Verify JSX text IS in typing sequence (for practice)

**Acceptance Criteria**:
- ✅ Minimal mode: JSX text excluded
- ✅ Standard mode: JSX text excluded
- ✅ Full mode: JSX text included
- ✅ Behavior consistent across all TSX snippets

---

### VA-2: JSX Tag Name Verification

**Requirement**: JSX tag names SHALL follow angle bracket exclusion rules.

**Test Cases**:
```tsx
<div>Content</div>
```

1. Minimal mode (excludes angle_bracket)
   - `<` not typeable ✅
   - `div` not typeable ✅
   - `>` not typeable ✅
   - `Content` typeable ✅ (it's string_content, but should be excluded)
   - Actually, `Content` should NOT be typeable (it's JSX text with string_content category)

2. Full mode (includes angle_bracket)
   - `<` typeable ✅
   - `div` typeable ✅
   - `>` typeable ✅
   - `Content` not typeable ✅ (still excluded as string_content)

**Acceptance Criteria**:
- ✅ Tag names follow bracket rules in all modes
- ✅ Detection works for self-closing tags (`<input />`)
- ✅ Detection works for closing tags (`</div>`)

---

## Requirements Traceability

### Critical Bug Fixes

| Bug | Session | Requirement | Status |
|-----|---------|-------------|--------|
| JSX text in Minimal mode | 33-37 | CR-2 | ✅ Fixed |
| JSX text whitespace splitting | 32 | CR-4 | ✅ Fixed |
| Whitespace typeability | 31 | CR-3 | ✅ Fixed |

### Feature Evolution

| Feature | Original Session | Current Requirement | Status |
|---------|-----------------|---------------------|--------|
| Progressive reveal | 3.5 | FR-2 | ✅ Stable |
| Typing modes | 5 | FR-3 | ✅ Stable |
| Pause/resume | 27 | FR-4 | ✅ Stable |
| TypeScript migration | 29-31 | N/A | ✅ Complete |
| Library system | 20-21 | FR-6 | ✅ Stable |

---

## Document Maintenance

**Update Triggers**:
- Any change to token categorization logic
- Addition/modification of typing modes
- Changes to user interface behavior
- Bug fixes that affect requirements

**Review Schedule**:
- After each major phase
- Before public release
- Quarterly for active development

**Version History**:
- 1.0 (Session 38) - Initial comprehensive specification
- Future versions will be tracked here

---

## Appendices

### Appendix A: Token Category Examples

**Python**:
```python
def calculate(n: int) -> list:
    return [n * 2]
```

Tokens:
- `def` - keyword, categories: []
- `calculate` - identifier, categories: []
- `(` - parenthesis, categories: ["parenthesis"]
- `n` - identifier, categories: []
- `:` - punctuation, categories: ["punctuation"]
- `int` - type_identifier, categories: []
- `)` - parenthesis, categories: ["parenthesis"]
- `->` - operator, categories: ["operator"]
- `list` - type_identifier, categories: []
- `:` - punctuation, categories: ["punctuation"]
- `return` - keyword, categories: []
- `[` - square_bracket, categories: ["square_bracket"]
- `n` - identifier, categories: []
- `*` - operator, categories: ["operator"]
- `2` - number, categories: []
- `]` - square_bracket, categories: ["square_bracket"]

**TSX**:
```tsx
<p>Loading item...</p>
```

Tokens:
- `<` - angle_bracket, categories: ["angle_bracket"]
- `p` - identifier, categories: []
- `>` - angle_bracket, categories: ["angle_bracket"]
- `Loading item...` - jsx_text, categories: ["string_content"]
- `</` - angle_bracket, categories: ["angle_bracket"]
- `p` - identifier, categories: []
- `>` - angle_bracket, categories: ["angle_bracket"]

---

### Appendix B: Glossary

**Terms**:
- **Token** - Smallest unit of code (keyword, identifier, bracket, etc.)
- **Category** - Semantic grouping of tokens for filtering
- **Typeable** - Whether user must type this token
- **base_typeable** - Parser's initial typeability decision
- **typeable** - Frontend's final typeability decision (after filtering)
- **Progressive reveal** - Code starts gray and reveals syntax colors as typed
- **Preset** - Pre-configured typing mode (Minimal, Standard, Full)
- **Snippet** - A single code sample for typing practice

---

_This requirements document reflects the actual implementation as of Session 38._  
_For architectural details, see ARCHITECTURE.md_  
_For user documentation, see README.md_
