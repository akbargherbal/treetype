## 🎯 Testing Priority (5 Sessions)

| Session | File                          | Coverage Target | Why This Order                                                                                                               |
| ------- | ----------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **1**   | `src/ui/renderer.ts`          | 70-80%          | The JSX bug took 5 sessions. Token filtering is complex, mode-dependent, and executes on every character. Highest risk area. |
| **2**   | `src/ui/keyboard.ts`          | 70%+            | Every keystroke goes through here. Input bugs = terrible UX. User-facing and hard to debug in production.                    |
| **3**   | `src/core/storage.ts`         | 60%+            | Data persistence bugs lose user progress. You're in dual-write phase - need to prove safety net works.                       |
| **4**   | `src/core/firestoreSync.ts`   | 50%+            | Validates your dual-write safety net before cutting over to Firestore-only. Critical for migration confidence.               |
| **5**   | `tests/integration/` (expand) | N/A             | Integration tests catch regressions across the whole system. Proves complete user journeys work end-to-end.                  |

---
