# Document 1: Targeted Test Suite for Session 6 Fixes

## 🎯 **Session 6 Testing Protocol - Multi-line Token Handling**

**Focus Area:** Verifying that docstrings, comments, and template literals are properly skipped, and that visual artifacts (multiple cursors) are eliminated.

**Assumption:** Basic features from Session 5 are working (cursor movement, reset, stats, error handling).

---

## Test Suite A: Python Multi-line Docstring Handling

### Test A.1: Docstring Auto-Skip

**Steps:**
1. Open render_code.html (Python sample)
2. Type through line 0: `defcalculate_fibonaccinintlist`
3. After typing final `t` in `list`

**Expected:**
- Cursor immediately jumps from line 0 to line 10 (skipping lines 1-9)
- Line 10 has green left border (active indicator)
- Yellow highlight appears on `i` in `if`
- Stats show: Line Progress "11/13" (not "2/13")

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

### Test A.2: No Ghost Cursors After Line Skip

**Steps:**
1. Complete line 0 (as in Test A.1)
2. Visually inspect lines 1-9 (the skipped docstring lines)

**Expected:**
- NO yellow highlights on any character in lines 1-9
- NO blinking underlines on lines 1-9
- Docstring text appears dimmed/grayed out
- Only ONE yellow highlight exists (on line 10)

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

### Test A.3: Typing Continues Normally After Skip

**Steps:**
1. After landing on line 10, type: `ifn`
2. Continue through line 10: `ifn0`

**Expected:**
- Each character turns green as typed
- Yellow highlight moves forward normally
- No visual artifacts from previous lines
- Line 10 completes and advances to line 11

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

### Test A.4: Character Count Excludes Docstring

**Steps:**
1. Complete line 0
2. Check "Char Progress" stat when cursor lands on line 10

**Expected:**
- Should show "0/X" (where X is the typeable chars in line 10)
- Should NOT show "159/X" (docstring content length)
- Total typeable chars for entire file should be ~40 (not ~200)

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Char Progress shown:** ___________

---

## Test Suite B: JavaScript Template Literal Handling

### Test B.1: Switch to JavaScript Sample

**Steps:**
1. From Python sample, select "JavaScript" from dropdown
2. Reset (Esc)
3. Type through lines 0-1 normally

**Expected:**
- JavaScript sample loads
- Can type through function declaration and const line
- No errors in console

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

### Test B.2: Template Literal Auto-Skip

**Context:** JavaScript sample has multi-line template literal at lines 8-12

**Steps:**
1. Type through lines until you reach line 7 (the line before template literal)
2. Complete line 7
3. Observe what happens

**Expected:**
- Cursor skips from line 7 to line 13 (after template literal)
- Lines 8-12 are NOT typeable
- Template literal content appears dimmed
- No cursor on template literal lines

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Actual behavior:**

---

### Test B.3: No Multi-Cursor Bug in JavaScript

**Steps:**
1. As you type through JavaScript sample, watch last character of each completed line

**Expected:**
- Last character of completed line turns green (correct state)
- NO yellow highlight remains on completed lines
- NO blinking underline on completed lines
- Only ONE yellow highlight exists at any time

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**If failed, which lines show ghost cursors:** ___________

---

## Test Suite C: TypeScript JSDoc Comment Handling

### Test C.1: Switch to TypeScript Sample

**Steps:**
1. Select "TypeScript" from dropdown
2. Reset (Esc)
3. Type through lines 0-5 (interface and blank line)

**Expected:**
- TypeScript sample loads
- Can type through interface definition
- No issues with type annotations (`:`, `number`, `string`)

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

### Test C.2: JSDoc Comment Auto-Skip

**Context:** TypeScript sample has JSDoc comment at lines 6-10

**Steps:**
1. Complete line 5 (line after interface)
2. Observe cursor behavior

**Expected:**
- Cursor jumps from line 5 to line 11 (skipping lines 6-10)
- JSDoc comment lines (/** ... */) are dimmed
- Stats show line 12/17 (not 7/17)
- Can continue typing line 11 (`async function...`)

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Actual behavior:**

---

### Test C.3: Comment Content Not in Typing Sequence

**Steps:**
1. After skipping JSDoc comment, press Ctrl+Shift+I (open Dev Tools)
2. In Console tab, run:
   ```javascript
   currentData.lines[6].typing_sequence
   ```

**Expected:**
- Should return: `""` (empty string)
- Lines 6-10 should all have empty typing sequences

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Console output:**

---

## Test Suite D: TSX/React Sample

### Test D.1: Switch to TSX Sample

**Steps:**
1. Select "TSX/React" from dropdown
2. Reset (Esc)
3. Type through first few lines

**Expected:**
- TSX sample loads
- Can type through import statement and component declaration
- JSX syntax (`<`, `>`, `{`, `}`) is dimmed/skipped

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

### Test D.2: JSX Auto-Skip

**Steps:**
1. Type through TSX sample, paying attention to JSX elements
2. Example: Line with `<div>` or `<button>`

**Expected:**
- You type only: identifiers, strings, variable names
- You do NOT type: `<`, `>`, `{`, `}`, `=`, `/`
- Cursor jumps over JSX syntax automatically

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

## Test Suite E: Edge Cases & Visual Consistency

### Test E.1: Rapid Line Completion

**Steps:**
1. Python sample, line 0
2. Type as fast as possible: `defcalculate_fibonaccinintlist`
3. Don't pause between characters

**Expected:**
- All characters register
- Cursor keeps up with typing speed
- Line skip happens immediately
- No visual lag or cursor duplication

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

### Test E.2: Completed Line Visual State

**Steps:**
1. After completing several lines, scroll up to view completed lines

**Expected:**
- All completed lines show ALL characters in green
- NO yellow highlights on completed lines
- NO blinking cursors on completed lines
- Green left border only on current active line

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

### Test E.3: Reset After Multi-Line Skip

**Steps:**
1. Complete line 0 (triggers docstring skip)
2. Press Esc
3. Observe state

**Expected:**
- Cursor returns to line 0, first character
- All green highlighting removed
- Stats reset to 0
- Can restart typing normally

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

### Test E.4: Language Switch After Partial Progress

**Steps:**
1. Type halfway through Python sample (e.g., complete lines 0-11)
2. Switch to JavaScript from dropdown (without resetting)

**Expected:**
- JavaScript sample loads
- Test resets automatically
- No Python state carries over
- Can start typing JavaScript from beginning

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Notes:**

---

## Test Suite F: Console Error Monitoring

### Test F.1: No JavaScript Errors During Normal Use

**Steps:**
1. Open Chrome Dev Tools (F12) → Console tab
2. Clear console
3. Type through 3-4 lines in any language
4. Check console

**Expected:**
- NO red error messages
- NO warnings about missing elements
- NO "Cannot read property" errors
- Only our debug logs (if any)

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Errors found:**

---

### Test F.2: No Errors During Line Skip

**Steps:**
1. With console open, complete line 0 (Python)
2. Watch console as docstring skip happens

**Expected:**
- NO errors during skip
- `updateDisplay()` completes successfully
- New line renders without errors

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Errors found:**

---

## Test Suite G: Stats Accuracy After Multi-Line Skips

### Test G.1: Line Progress Accuracy

**Steps:**
1. Python sample
2. Complete line 0 → cursor jumps to line 10
3. Check "Line Progress" stat

**Expected:**
- Should show: "11/13" (on line 11 of 13 total)
- NOT: "2/13" (which would be wrong)

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Shown:** ___________

---

### Test G.2: WPM Calculation Not Affected

**Steps:**
1. Type through Python sample at normal speed
2. Complete at least 5 lines (including skipped docstring)
3. Check WPM stat

**Expected:**
- WPM calculated based on TYPED characters only
- Skipped content does NOT count toward WPM
- WPM should be realistic (20-80 range for normal typing)

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**WPM shown:** ___________

---

### Test G.3: Accuracy Not Affected by Skips

**Steps:**
1. Type 10 correct characters
2. Complete line (triggering skip)
3. Type 5 more correct characters
4. Check Accuracy stat

**Expected:**
- Accuracy based only on typed characters
- Should be 100% if no errors made
- Skipped content does NOT affect accuracy

**Result:** ☐ ✅ / ☐ ❌ / ☐ ⚠️  
**Accuracy shown:** ___________

---

## 📋 Summary Checklist

After completing all tests, check overall status:

### Critical Success Criteria

- [ ] ✅ Docstrings are skipped (Python)
- [ ] ✅ Template literals are skipped (JavaScript)
- [ ] ✅ JSDoc comments are skipped (TypeScript)
- [ ] ✅ NO ghost cursors on completed lines
- [ ] ✅ Only ONE yellow highlight exists at any time
- [ ] ✅ Line skips happen immediately (no stuck cursor)
- [ ] ✅ Stats are accurate (line count, WPM, accuracy)
- [ ] ✅ No console errors during typing or line skips

### Issues Found

List any issues discovered:

1. 
2. 
3. 

### Test Coverage Summary

- **Tests Passed:** _____ / 23
- **Tests Failed:** _____
- **Tests Partially Working:** _____
- **Tests Not Completed:** _____

---

## 🎯 Priority Issues for Next Session

Based on test results, rank issues by priority:

**P0 (Blockers):**
- 

**P1 (Major Issues):**
- 

**P2 (Minor Issues):**
- 

**P3 (Nice to Have):**
- 

---

**End of Test Suite Document**

---
