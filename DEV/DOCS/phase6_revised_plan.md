# Phase 6 Implementation Plan (Revised - Post Session 24)
## TreeType: Custom Snippet Library

**Status**: Session 24 Complete - Metadata Generated ✅  
**Next**: Session 25 - Library UI  
**Estimated remaining effort**: 8-10 hours (2-3 sessions)

---

## 🎯 Goals

Allow users to practice their own code snippets with minimal backend complexity.

**What we're building**:
1. ✅ Offline snippet generation workflow (Python script) - **COMPLETE**
2. ✅ Static snippet hosting (GitHub Pages) - **COMPLETE**
3. 🔄 Snippet library browser UI - **IN PROGRESS**
4. 🔄 User stats tracking (localStorage) - **NEXT**
5. ❌ Export/Import (deferred to Phase 7)

**What we're NOT building** (future phases):
- ❌ Backend API for parsing
- ❌ Database (Cloud SQL, Firestore)
- ❌ User accounts/authentication
- ❌ Real-time features
- ❌ Community snippet sharing
- ❌ Complex historical stats tracking

---

## 🗂️ File Structure (Current)

```
treetype/
├── index.html                      # Main typing game
├── library.html                    # Snippet browser (TO BUILD)
│
├── snippets/                       # Static snippet library (committed to Git)
│   ├── metadata.json               # Master index (98 snippets) ✅
│   ├── javascript/                 # 24 snippets
│   ├── tsx/                        # 24 snippets (React)
│   ├── typescript/                 # 17 snippets
│   └── python/                     # 33 snippets
│
├── sources/                        # Source code files (gitignored)
│   ├── javascript/
│   ├── tsx/
│   ├── typescript/
│   └── python/
│
└── build/                          # Build scripts
    ├── parse_json.py               # Refactored parser ✅
    ├── build_metadata.py           # Generates metadata.json ✅
    └── process_all_snippets.py     # Batch processor ✅
```

---

## 📊 Metadata Workflow (Session 23-24)

### ✅ Completed: Metadata Generation

**Workflow:**
1. **Jupyter Notebook** exports snippet metadata (`snippets_metadata.json`)
   - Contains: prompt_id, category, display_name, language, source_file
   - Generated from DataFrame with all snippet info
2. **Parser** (`parse_json.py`) processes source files → JSON
   - Extracts tokens, typing sequences, character maps
3. **Metadata Builder** (`build_metadata.py`) merges:
   - Notebook metadata (categories, display names)
   - Parsed data (line counts, difficulty, paths)
   - Output: Final `metadata.json` for library UI

**Key Decision:** Keep original filenames (`gm_01_001_01_array-methods.js`)
- Preserves batch tracking (`gm_01` = Gemini Model batch 01)
- No file renaming needed
- Metadata maps to clean display names in UI

---

## 💾 localStorage Schema (Simplified for MVP)

```javascript
// Key: treetype_snippet_stats
{
  "javascript-array-methods-001-01": {
    "bestWPM": 62,
    "bestAccuracy": 96,
    "practiceCount": 5,
    "lastPracticed": "2025-11-16T14:30:00Z"
  },
  "python-flask-patterns-004-02-03": {
    "bestWPM": 48,
    "bestAccuracy": 91,
    "practiceCount": 2,
    "lastPracticed": "2025-11-15T10:20:00Z"
  }
}

// Key: treetype_preferences (already exists in index.html)
{
  "preset": "standard",
  "language": "python",
  "lastSnippet": "javascript-array-methods-001-01"
}

// Key: treetype_schema_version
"1.0"
```

**What we track (per snippet):**
- Best WPM achieved
- Best accuracy %
- Total practice count
- Last practiced date

**What we DON'T track:**
- ❌ Session history (localStorage is fragile)
- ❌ Per-session metrics
- ❌ Time-series data
- ❌ Cross-device sync

**Rationale:** Keep it simple. Users clear localStorage frequently. Don't build complex features on fragile storage.

---

## 📋 Implementation Progress

### ✅ Session 19-20: Repository Setup & GitHub Pages (COMPLETE)

**Accomplished:**
- ✅ Restructured repository for GitHub Pages
- ✅ Deployed to `https://akbargherbal.github.io/treetype/`
- ✅ Created `snippets/` and `sources/` folder structure
- ✅ Set up `.gitignore` (sources/ ignored, snippets/ committed)

---

### ✅ Session 21-22: Repository Rename (COMPLETE)

**Accomplished:**
- ✅ Renamed repo: TreeType → treetype (lowercase)
- ✅ Updated all URLs and references
- ✅ Verified GitHub Pages deployment

---

### ✅ Session 23: Planning & Architecture (COMPLETE)

**Accomplished:**
- ✅ Defined MVP scope (no complex stats)
- ✅ Validated user flow (library → practice → modal → library)
- ✅ Made 5 key architecture decisions:
  1. Filename strategy: Keep original names
  2. Metadata generation: Hybrid (notebook + script)
  3. Multi-part display: Separate cards
  4. Stats display: Best WPM + Practice Count
  5. Category grouping: Flat list + filters

---

### ✅ Session 24: Metadata Generation & Snippet Processing (COMPLETE)

**Accomplished:**
- ✅ Created metadata export cell in Jupyter notebook
- ✅ Generated `snippets_metadata.json` (98 snippets)
- ✅ Enhanced `build_metadata.py` to merge metadata sources
- ✅ Created `process_all_snippets.py` batch processor
- ✅ Parsed all 98 source files to JSON
- ✅ Generated final `metadata.json` with complete data

**Deliverables:**
- ✅ `snippets/metadata.json` (master index)
- ✅ 98 parsed JSON files in `snippets/` folders
- ✅ All source files in `sources/` (gitignored)
- ✅ Build scripts tested and working

---

### 🔄 Session 25: Library UI (NEXT - 3-4 hours)

**Goals:**
Build the snippet library browser interface.

**Tasks:**

#### Task 25.1: Library Page Structure (1 hour)
- [ ] Create `library.html` with basic layout
- [ ] Header: "TreeType Snippet Library"
- [ ] Filter controls:
  - Language dropdown (All, JavaScript, TypeScript, TSX, Python)
  - Search box (filter by category name)
- [ ] Snippet grid: Cards with metadata
- [ ] Link to typing game (index.html)

#### Task 25.2: Snippet Loading & Display (1 hour)
- [ ] Fetch `snippets/metadata.json` on page load
- [ ] Parse and display snippet cards
- [ ] Show on each card:
  - Category name (display_name)
  - Language badge
  - Line count
  - Best WPM (from localStorage, if exists)
  - Practice count (from localStorage, if exists)
  - "Practice" button
- [ ] Implement filtering by language
- [ ] Implement search by category name

#### Task 25.3: localStorage Stats Integration (1 hour)
- [ ] Read `treetype_snippet_stats` on page load
- [ ] Display stats on snippet cards:
  - "Best: 62 WPM" (if practiced before)
  - "Practiced 5 times"
  - "Never practiced" (if no stats)
- [ ] Sort options:
  - Default: By category name
  - By most practiced
  - By best WPM

#### Task 25.4: UI Polish (30 min)
- [ ] Loading spinner while fetching metadata
- [ ] Empty state (no snippets found after filtering)
- [ ] Error handling (network failures)
- [ ] Responsive design (mobile-friendly grid)
- [ ] Hover effects on cards

**Deliverables:**
- ✅ Functional `library.html`
- ✅ Basic filtering/search working
- ✅ Stats display integrated
- ✅ Clean, responsive design

---

### 🔄 Session 26: Dynamic Loading & Stats Persistence (2-3 hours)

**Goals:**
Connect library to typing game, track stats.

**Tasks:**

#### Task 26.1: URL Parameter Support (1 hour)
- [ ] Update `index.html` to accept `?snippet=<id>` parameter
- [ ] Load snippet JSON dynamically based on ID
- [ ] Example: `index.html?snippet=javascript-array-methods-001-01`
- [ ] Fetch from `snippets/javascript/gm_01_001_01_array-methods.json`
- [ ] Display error if snippet not found

#### Task 26.2: Stats Persistence (1 hour)
- [ ] Update completion handler in `index.html`
- [ ] After snippet completion, save stats to localStorage:
  - Update bestWPM if current > previous
  - Update bestAccuracy if current > previous
  - Increment practiceCount
  - Set lastPracticed timestamp
- [ ] Test with multiple snippets

#### Task 26.3: Completion Modal Updates (30 min)
- [ ] Add "Back to Library" button to modal
- [ ] Add "Try Another" button → random snippet
- [ ] Update "Retry" button to reload same snippet
- [ ] All buttons work correctly with URL parameters

#### Task 26.4: Navigation Flow (30 min)
- [ ] Library → Practice (URL param passed)
- [ ] Practice → Complete → Modal → Library (clean flow)
- [ ] Test with all 4 languages
- [ ] Verify stats update correctly

**Deliverables:**
- ✅ Complete navigation flow working
- ✅ Stats persist across sessions
- ✅ URL parameters functional
- ✅ All 98 snippets testable

---

## 🎯 Success Criteria (MVP)

### Must Have (Session 26 Completion)
- ✅ Can browse all 98 snippets in library
- ✅ Can filter by language
- ✅ Can search by category name
- ✅ Can click "Practice" → loads snippet in typing game
- ✅ Stats persist (best WPM, practice count)
- ✅ Can return to library after completion
- ✅ Works on GitHub Pages (live deployment)
- ✅ All 4 languages work identically

### Nice to Have (If Time Permits)
- ⭐ Sort by most practiced / best WPM
- ⭐ "Random snippet" button
- ⭐ Keyboard shortcuts (Esc to return to library)
- ⭐ Progress indicator (X/98 practiced)

---

## 📊 Current Dataset

**98 Total Snippets:**
- JavaScript: 24 snippets (12 categories × 2 variations)
- TSX (React): 24 snippets (12 categories × 2 variations)
- TypeScript: 17 snippets (9 categories, 1 has single variation)
- Python: 33 snippets (33 categories × 1 variation)

**Snippet Structure:**
```json
{
  "id": "javascript-array-methods-001-01",
  "prompt_id": "001_01",
  "display_name": "Array Methods",
  "category": "Array Methods",
  "language": "javascript",
  "source_file": "gm_01_001_01_array-methods.js",
  "path": "snippets/javascript/gm_01_001_01_array-methods.json",
  "lines": 15,
  "typeable_chars": 123,
  "difficulty": "beginner",
  "tags": ["array methods", "javascript"],
  "dateAdded": "2025-11-16"
}
```

---

## 💰 Cost & Hosting

| Component | Solution | Cost |
|-----------|----------|------|
| **Frontend Hosting** | GitHub Pages | $0/month |
| **Snippet Storage** | Git repository | $0/month |
| **User Data** | localStorage | $0/month |
| **Parsing** | Offline (local machine) | $0/month |
| **Total** | | **$0/month** ✅ |

---

## 🚀 Future Enhancements (Phase 7+)

**Deferred to Later:**
- Export/Import stats (safety net for localStorage)
- Historical session tracking
- Analytics dashboard
- Cross-device sync (Firebase)
- User accounts
- Public snippet sharing
- Advanced difficulty estimation
- Custom snippet upload (browser-based)

**Philosophy:** Build the simplest thing that works. Add complexity only when proven necessary.

---

## 📅 Timeline Summary

| Session | Focus | Status | Hours |
|---------|-------|--------|-------|
| **19-20** | Repo setup + GitHub Pages | ✅ Complete | 3-4h |
| **21-22** | Repo rename | ✅ Complete | 1h |
| **23** | Planning & architecture | ✅ Complete | 1h |
| **24** | Metadata generation | ✅ Complete | 2h |
| **25** | Library UI | 🔄 Next | 3-4h |
| **26** | Dynamic loading + stats | 🔄 Pending | 2-3h |

**Total Phase 6**: ~12-15 hours (6 sessions)

---

## ✅ Session 24 Summary

**What We Built:**
1. ✅ Jupyter notebook cell for metadata export
2. ✅ Generated `snippets_metadata.json` (98 snippets)
3. ✅ Enhanced `build_metadata.py` script
4. ✅ Created `process_all_snippets.py` batch processor
5. ✅ Parsed all 98 source files to JSON
6. ✅ Generated final `metadata.json`

**Ready for Session 25:**
- All snippets parsed and indexed
- Metadata complete and validated
- Build scripts tested and working
- Ready to build library UI

---

**Phase 6 Progress**: 4/6 sessions complete (67%) 🎯  
**Next Session**: Build library.html with filtering and search  
**Estimated remaining time**: 5-7 hours

---

_Session 24 was all about automation. We transformed 98 source files into a fully-indexed snippet library without manual work. The metadata workflow is now repeatable for future batches._ ✨
