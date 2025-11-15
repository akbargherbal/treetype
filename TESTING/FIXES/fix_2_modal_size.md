# Fix #2: Completion Modal Size Reduction

## Goal:
Reduce modal height from ~full viewport to ~50% viewport height using tighter spacing.

---

## Search For (CTRL+F):
```css
      .modal-content {
        background: #2a2a2a;
        border-radius: 12px;
        padding: 32px;
        max-width: 400px;
        width: 90%;
        text-align: center;
        animation: slideUp 0.3s;
        border: 2px solid #4ade80;
      }
```

## Replace With:
```css
      .modal-content {
        background: #2a2a2a;
        border-radius: 12px;
        padding: 24px;
        max-width: 400px;
        width: 90%;
        text-align: center;
        animation: slideUp 0.3s;
        border: 2px solid #4ade80;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
```

---

## Search For (CTRL+F):
```css
      .modal-title {
        font-size: 2em;
        margin-bottom: 8px;
      }
```

## Replace With:
```css
      .modal-title {
        font-size: 2em;
        margin: 0;
      }
```

---

## Search For (CTRL+F):
```css
      .modal-subtitle {
        color: #9ca3af;
        margin-bottom: 24px;
      }
```

## Replace With:
```css
      .modal-subtitle {
        color: #9ca3af;
        margin: 0;
        font-size: 0.95em;
      }
```

---

## Search For (CTRL+F):
```css
      .modal-stats {
        background: #1e1e1e;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 24px;
      }
```

## Replace With:
```css
      .modal-stats {
        background: #1e1e1e;
        border-radius: 8px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 8px;
      }
```

---

## Search For (CTRL+F):
```css
      .modal-stat {
        margin: 12px 0;
      }
```

## Replace With:
```css
      .modal-stat {
        margin: 0;
      }
```

---

## Search For (CTRL+F):
```css
      .modal-buttons {
        display: flex;
        gap: 12px;
        justify-content: center;
      }
```

## Replace With:
```css
      .modal-buttons {
        display: flex;
        gap: 12px;
        justify-content: center;
        margin: 0;
      }
```

---

## Verification:
- Complete a test and check modal height
- Should occupy roughly 50% of viewport height
- All content should still be readable
- Font sizes unchanged (only spacing reduced)
- Modal should feel more compact but not cramped

---

**Estimated time**: 2-3 minutes (6 replacements)  
**Risk**: Low (CSS only, easy to revert)  
**Impact**: More elegant completion modal 🎨
