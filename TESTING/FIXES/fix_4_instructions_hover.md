# Fix #4: Instructions Panel Auto-Hover Bug

## Goal:
Prevent instructions panel from appearing when auto-scroll brings it under a static cursor. Instructions should only show on intentional mouse movement.

---

## Problem:
When typing near bottom of page, auto-scroll moves the instructions panel under the cursor. Browser thinks this is a "hover" event and shows the instructions (distracting during typing).

## Solution:
Disable pointer events on instructions panel during active typing (consistent with distraction-free zen mode).

---

## Search For (CTRL+F):
```css
      body.test-active .controls-area {
        opacity: 0.1;
      }

      body.test-active .controls-area:hover {
        opacity: 1;
      }
```

## Replace With:
```css
      body.test-active .controls-area {
        opacity: 0.1;
      }

      body.test-active .controls-area:hover {
        opacity: 1;
      }

      /* Prevent instructions panel from triggering hover during auto-scroll */
      body.test-active .instructions-panel {
        pointer-events: none;
        opacity: 0.1;
      }
```

---

## Add New Class to Instructions HTML:

### Search For (CTRL+F):
```html
      <!-- Instructions: Also fade during typing -->
      <div class="mt-6 p-4 bg-gray-800 rounded controls-area">
```

### Replace With:
```html
      <!-- Instructions: Also fade during typing -->
      <div class="mt-6 p-4 bg-gray-800 rounded controls-area instructions-panel">
```

---

## Explanation:
- Added `instructions-panel` class to the instructions div
- Created CSS rule that disables pointer events during active test
- Instructions fade to 0.1 opacity like other controls
- User can still access instructions by pressing ESC (exits test mode)

---

## Verification:
1. Start typing a test
2. Place cursor at bottom of screen (don't move mouse)
3. Type until auto-scroll brings instructions panel into view
4. Instructions should stay faded (not appear)
5. Press ESC to reset
6. Instructions should now be hoverable again (test inactive)

---

**Estimated time**: 1 minute  
**Risk**: Low (CSS + one class addition)  
**Impact**: Distraction-free typing maintained 🧘✨
