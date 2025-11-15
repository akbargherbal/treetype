# Fix #3: ESC Key Closes Modal

## Goal:
When user presses ESC after completing a test, close the modal AND reset the test (currently only resets test).

---

## Search For (CTRL+F):
```javascript
      function handleKeyPress(event) {
        if (event.ctrlKey || event.metaKey || event.altKey) return;
        if (event.key === "Escape") {
          event.preventDefault();
          resetTest();
          return;
        }
```

## Replace With:
```javascript
      function handleKeyPress(event) {
        if (event.ctrlKey || event.metaKey || event.altKey) return;
        if (event.key === "Escape") {
          event.preventDefault();
          closeModal(); // Close modal if open
          resetTest();
          return;
        }
```

---

## Explanation:
Added `closeModal()` call before `resetTest()`. The `closeModal()` function already has a safety check (`if (modal)`) so it's safe to call even when modal isn't open.

---

## Verification:
1. Complete a test → modal appears
2. Press ESC
3. Modal should close AND test should reset
4. You should see "Press any key to start..." message
5. Pressing ESC during typing (no modal) should still work normally

---

**Estimated time**: 30 seconds  
**Risk**: Very low (adds one line)  
**Impact**: ESC key works consistently 🐛✅
