# 🔄 TypeScript Migration Plan: Phased Approach

## Philosophy (Mirrors Original TreeType Development)

- **Baseline first**: Set up TypeScript without breaking existing functionality
- **Incremental validation**: Each phase produces a working application
- **Low-risk assumptions**: Test TypeScript benefits before full commitment
- **Rollback-friendly**: Can stop at any phase and still have a functional app
- **Documentation-driven**: Type definitions serve as living documentation
- **Learn-as-you-go**: Build TypeScript knowledge through practical application

---

## 📊 Current State Assessment

### What We Have

- ✅ **index.html**: 500+ lines of inline JavaScript (game logic)
- ✅ **library.html**: 300+ lines of inline JavaScript (library browser)
- ✅ **snippets/**: 98 pre-parsed JSON files
- ✅ **build/parse_json.py**: Python parser for generating JSON

### Known Issues to Address

- ❌ **Auto-jump inconsistency**: Spacebar behavior differs between TSX and other languages
- ❌ **No type safety**: Easy to introduce bugs when modifying data structures
- ❌ **Monolithic structure**: Hard to test individual functions
- ❌ **No compile-time checks**: Bugs only discovered at runtime

### Success Metrics

- ✅ Type system catches the auto-jump bug's root cause
- ✅ IDE provides autocomplete for all data structures
- ✅ Can refactor with confidence (rename, restructure)
- ✅ Code is modular and testable
- ✅ Build process is fast (<5 seconds)

---

## 🎯 Phase 1: Foundation Setup (Session 29)

### Goal

**Set up TypeScript tooling and define core type system—no code migration yet.**

### What We'll Test

- TypeScript compiler works correctly
- Build process is simple and fast
- Type definitions accurately represent our data structures
- Can check types without changing JavaScript code

### Tasks

#### 1.1: Initialize TypeScript Project (15 mins)

```bash
# Initialize npm project
npm init -y

# Install dependencies
npm install --save-dev typescript vite @types/node

# Initialize TypeScript config
npx tsc --init
```

#### 1.2: Configure Build System (15 mins)

**Create `tsconfig.json`:**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowJs": true,
    "checkJs": false
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Create `vite.config.js`:**

```javascript
import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  root: ".",
  build: {
    outDir: "dist",
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        library: resolve(__dirname, "library.html"),
      },
    },
  },
  server: {
    port: 3000,
    open: true,
  },
});
```

**Update `package.json` scripts:**

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "type-check": "tsc --noEmit"
  }
}
```

#### 1.3: Create Type Definitions (45 mins)

**File: `src/types/snippet.ts`**

```typescript
/**
 * Token categories used for filtering in typing modes
 */
export type TokenCategory =
  | "parenthesis"
  | "curly_brace"
  | "square_bracket"
  | "angle_bracket"
  | "operator"
  | "punctuation"
  | "string_content"
  | "string_delimiter"
  | "comment"
  | "keyword"
  | "identifier";

/**
 * Individual token in parsed code
 */
export interface Token {
  text: string;
  type: string;
  typeable: boolean;
  base_typeable: boolean;
  start_col: number;
  end_col: number;
  categories: TokenCategory[];
}

/**
 * Single line of code with typing metadata
 */
export interface Line {
  line_number: number;
  indent_level: number;
  display_tokens: Token[];
  typing_sequence: string;
  char_map: {
    [charIndex: string]: {
      token_idx: number;
      display_col: number;
    };
  };
}

/**
 * Complete parsed snippet data
 */
export interface SnippetData {
  language: "python" | "javascript" | "typescript" | "tsx";
  total_lines: number;
  lines: Line[];
}

/**
 * Snippet metadata from library
 */
export interface SnippetMetadata {
  id: string;
  name: string;
  language: string;
  path: string;
  lines: number;
  typeable_chars: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  tags: string[];
  dateAdded: string;
}
```

**File: `src/types/state.ts`**

```typescript
/**
 * Test state during typing session
 */
export interface TestState {
  active: boolean;
  paused: boolean;
  startTime: number | null;
  endTime: number | null;
  pauseStartTime: number | null;
  totalPausedTime: number;
  currentLineIndex: number;
  currentCharIndex: number;
  totalCharsTyped: number;
  totalErrors: number;
  completedLines: Set<number>;
  errorOnCurrentChar: boolean;
}

/**
 * Snippet info for tracking
 */
export interface SnippetInfo {
  path: string | null;
  id: string | null;
  language: string | null;
}

/**
 * User statistics for a snippet
 */
export interface SnippetStats {
  bestWPM: number;
  bestAccuracy: number;
  practiceCount: number;
  lastPracticed: string;
}
```

**File: `src/types/config.ts`**

```typescript
import { TokenCategory } from "./snippet";

/**
 * Typing mode preset configuration
 */
export interface PresetConfig {
  name: string;
  description: string;
  exclude: TokenCategory[];
  includeSpecific?: string[];
}

/**
 * Available typing modes
 */
export type TypingMode = "minimal" | "standard" | "full";

/**
 * Preset configurations map
 */
export type PresetsConfig = {
  [K in TypingMode]: PresetConfig;
};

/**
 * User configuration
 */
export interface UserConfig {
  preset: TypingMode;
  language: "python" | "javascript" | "typescript" | "tsx";
}
```

#### 1.4: Create Directory Structure (5 mins)

```bash
mkdir -p src/{types,core,ui,utils}
touch src/types/{snippet.ts,state.ts,config.ts}
```

### Deliverables

- ✅ TypeScript compiler installed and configured
- ✅ Vite build system working
- ✅ Complete type definitions for all data structures
- ✅ Can run `npm run type-check` successfully
- ✅ Project structure ready for migration

### Success Criteria

- ✅ `npm run dev` starts development server
- ✅ `npm run build` compiles without errors
- ✅ Type definitions match existing JSON/JavaScript structures
- ✅ No breaking changes to existing functionality

### Time Estimate: 2 hours

---

## 🎯 Phase 2: Extract Pure Functions (Session 30)

### Goal

**Migrate utility functions to TypeScript modules while keeping app functional.**

### What We'll Test

- Can import TypeScript modules into HTML
- Type checking catches potential bugs
- Functions work identically after migration
- Build process integrates smoothly

### Tasks

#### 2.1: Extract Timer Logic (30 mins)

**File: `src/core/timer.ts`**

```typescript
import { TestState } from "../types/state";

/**
 * Calculate elapsed time excluding pauses
 */
export function getElapsedTime(state: TestState): number {
  if (!state.active || !state.startTime) return 0;

  const now = Date.now();
  let elapsedMs = now - state.startTime - state.totalPausedTime;

  if (state.paused && state.pauseStartTime) {
    const currentPauseDuration = now - state.pauseStartTime;
    elapsedMs -= currentPauseDuration;
  }

  return elapsedMs / 1000;
}

/**
 * Calculate words per minute
 * Standard: 5 characters = 1 word
 */
export function calculateWPM(
  charsTyped: number,
  elapsedSeconds: number
): number {
  if (elapsedSeconds <= 0) return 0;
  const elapsedMinutes = elapsedSeconds / 60;
  return Math.round(charsTyped / 5 / elapsedMinutes);
}

/**
 * Calculate typing accuracy percentage
 */
export function calculateAccuracy(totalChars: number, errors: number): number {
  if (totalChars === 0) return 100;
  return Math.round(((totalChars - errors) / totalChars) * 100);
}

/**
 * Format elapsed time as MM:SS
 */
export function formatTime(seconds: number): string {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${minutes}:${secs.toString().padStart(2, "0")}`;
}
```

#### 2.2: Extract Configuration Logic (30 mins)

**File: `src/core/config.ts`**

```typescript
import { PresetsConfig, UserConfig, TypingMode } from "../types/config";
import { Line, Token } from "../types/snippet";

/**
 * Preset configurations
 */
export const PRESETS: PresetsConfig = {
  minimal: {
    name: "Minimal",
    description: "Type only keywords and identifiers",
    exclude: [
      "parenthesis",
      "curly_brace",
      "square_bracket",
      "angle_bracket",
      "operator",
      "punctuation",
      "string_content",
      "string_delimiter",
      "comment",
    ],
  },
  standard: {
    name: "Standard",
    description: "Balanced practice without pinky strain (recommended)",
    exclude: [
      "curly_brace",
      "square_bracket",
      "angle_bracket",
      "string_content",
      "punctuation",
      "string_delimiter",
      "comment",
    ],
    includeSpecific: [":", ".", ",", "(", ")"],
  },
  full: {
    name: "Full",
    description: "Type everything except whitespace and comments",
    exclude: ["comment", "string_content"],
  },
};

/**
 * Default user configuration
 */
export const DEFAULT_CONFIG: UserConfig = {
  preset: "standard",
  language: "python",
};

/**
 * Apply exclusion config to line data
 */
export function applyExclusionConfig(lineData: Line, preset: TypingMode): Line {
  const config = PRESETS[preset];

  const filteredTokens: Token[] = lineData.display_tokens.map((token) => {
    let typeable = token.base_typeable;

    if (!typeable) {
      return { ...token, typeable };
    }

    if (!token.categories || token.categories.length === 0) {
      return { ...token, typeable: true };
    }

    // Check includeSpecific first
    if (config.includeSpecific?.includes(token.text)) {
      return { ...token, typeable: true };
    }

    // Check if any category is excluded
    for (const category of token.categories) {
      if (config.exclude.includes(category)) {
        typeable = false;
        break;
      }
    }

    return { ...token, typeable };
  });

  // Regenerate typing sequence
  const typingSequence = filteredTokens
    .filter((t) => t.typeable)
    .map((t) => t.text)
    .join("");

  // Regenerate char_map
  const charMap: Line["char_map"] = {};
  let charIdx = 0;
  const typeableTokens = filteredTokens.filter((t) => t.typeable);

  typeableTokens.forEach((token, tokenIdx) => {
    for (let i = 0; i < token.text.length; i++) {
      charMap[String(charIdx)] = {
        token_idx: tokenIdx,
        display_col: token.start_col,
      };
      charIdx++;
    }
  });

  return {
    ...lineData,
    display_tokens: filteredTokens,
    typing_sequence: typingSequence,
    char_map: charMap,
  };
}

/**
 * Save user configuration to localStorage
 */
export function saveConfig(config: UserConfig): void {
  localStorage.setItem("treetype_config", JSON.stringify(config));
}

/**
 * Load user configuration from localStorage
 */
export function loadConfig(): UserConfig {
  const saved = localStorage.getItem("treetype_config");
  return saved ? JSON.parse(saved) : DEFAULT_CONFIG;
}
```

#### 2.3: Extract Storage/Stats Logic (30 mins)

**File: `src/core/storage.ts`**

```typescript
import { SnippetStats } from "../types/state";

/**
 * Load all snippet statistics
 */
export function loadSnippetStats(): Record<string, SnippetStats> {
  const saved = localStorage.getItem("treetype_snippet_stats");
  return saved ? JSON.parse(saved) : {};
}

/**
 * Save snippet statistics
 */
export function saveSnippetStats(
  snippetId: string,
  wpm: number,
  accuracy: number
): void {
  const stats = loadSnippetStats();

  if (!stats[snippetId]) {
    stats[snippetId] = {
      bestWPM: wpm,
      bestAccuracy: accuracy,
      practiceCount: 1,
      lastPracticed: new Date().toISOString(),
    };
  } else {
    stats[snippetId].bestWPM = Math.max(stats[snippetId].bestWPM || 0, wpm);
    stats[snippetId].bestAccuracy = Math.max(
      stats[snippetId].bestAccuracy || 0,
      accuracy
    );
    stats[snippetId].practiceCount = (stats[snippetId].practiceCount || 0) + 1;
    stats[snippetId].lastPracticed = new Date().toISOString();
  }

  localStorage.setItem("treetype_snippet_stats", JSON.stringify(stats));
}
```

#### 2.4: Update HTML to Import Modules (30 mins)

**Modify `index.html`:**

```html
<!-- Before </head> -->
<script type="module">
  import {
    getElapsedTime,
    calculateWPM,
    calculateAccuracy,
  } from "/src/core/timer.js";
  import {
    PRESETS,
    applyExclusionConfig,
    loadConfig,
    saveConfig,
  } from "/src/core/config.js";
  import { loadSnippetStats, saveSnippetStats } from "/src/core/storage.js";

  // Rest of inline JavaScript can now use these imports
  // ...existing code...
</script>
```

### Deliverables

- ✅ `src/core/timer.ts` with all timer functions
- ✅ `src/core/config.ts` with configuration logic
- ✅ `src/core/storage.ts` with localStorage functions
- ✅ HTML files import and use TypeScript modules
- ✅ All functionality still works identically

### Success Criteria

- ✅ App runs without errors in browser
- ✅ TypeScript compiler catches type mismatches
- ✅ Can modify functions with confidence (types guide you)
- ✅ Build process completes successfully

### Time Estimate: 2 hours

---

## 🎯 Phase 3: Main App Migration (Session 31)

### Goal

**Migrate index.html game logic to TypeScript while maintaining functionality.**

### What We'll Test

- Full game loop works in TypeScript
- Keyboard handling preserved
- State management type-safe
- All 4 languages work correctly

### Tasks

#### 3.1: Extract Rendering Logic (45 mins)

**File: `src/ui/renderer.ts`**

```typescript
import { Line, SnippetData } from "../types/snippet";
import { TestState } from "../types/state";

export class CodeRenderer {
  private container: HTMLElement;

  constructor(containerId: string) {
    const element = document.getElementById(containerId);
    if (!element) throw new Error(`Element ${containerId} not found`);
    this.container = element;
  }

  renderCode(data: SnippetData, state: TestState): void {
    this.container.innerHTML = "";

    data.lines.forEach((lineData, lineIndex) => {
      const lineDiv = this.createLine(lineData, lineIndex, state);
      this.container.appendChild(lineDiv);
    });
  }

  private createLine(
    lineData: Line,
    lineIndex: number,
    state: TestState
  ): HTMLElement {
    const lineDiv = document.createElement("div");
    lineDiv.className = "line flex";
    lineDiv.id = `line-${lineIndex}`;

    if (lineIndex === state.currentLineIndex) {
      lineDiv.classList.add("test-active-line");
    }

    // Line number
    const lineNum = document.createElement("span");
    lineNum.className = "line-number";
    lineNum.textContent = String(lineData.line_number + 1);
    lineDiv.appendChild(lineNum);

    // Content
    const contentDiv = document.createElement("div");
    contentDiv.className = "flex-1";
    contentDiv.style.paddingLeft = `${lineData.indent_level * 16}px`;
    contentDiv.id = `line-content-${lineIndex}`;

    this.renderLineTokens(contentDiv, lineData, lineIndex, state);

    lineDiv.appendChild(contentDiv);
    return lineDiv;
  }

  private renderLineTokens(
    container: HTMLElement,
    lineData: Line,
    lineIndex: number,
    state: TestState
  ): void {
    // ... token rendering logic ...
    // (This will be the existing renderLineTokens function)
  }
}
```

#### 3.2: Extract Keyboard Handler (45 mins)

**File: `src/ui/keyboard.ts`**

```typescript
import { TestState, SnippetInfo } from "../types/state";
import { SnippetData } from "../types/snippet";

export class KeyboardHandler {
  private state: TestState;
  private data: SnippetData;
  private snippetInfo: SnippetInfo;

  constructor(state: TestState, data: SnippetData, snippetInfo: SnippetInfo) {
    this.state = state;
    this.data = data;
    this.snippetInfo = snippetInfo;
  }

  handleKeyPress(event: KeyboardEvent): void {
    // Tab key for pause/resume
    if (event.key === "Tab" && this.state.active) {
      event.preventDefault();
      this.togglePause();
      return;
    }

    // Block input during pause
    if (this.state.paused) {
      if (event.key === "Escape") {
        event.preventDefault();
        this.resetTest();
      }
      return;
    }

    // ... rest of keyboard handling logic ...
  }

  private togglePause(): void {
    // ... existing pause logic ...
  }

  private resetTest(): void {
    // ... existing reset logic ...
  }
}
```

#### 3.3: Create Main App Class (60 mins)

**File: `src/app.ts`**

```typescript
import { TestState, SnippetInfo } from "./types/state";
import { SnippetData } from "./types/snippet";
import { CodeRenderer } from "./ui/renderer";
import { KeyboardHandler } from "./ui/keyboard";
import { loadConfig, applyExclusionConfig } from "./core/config";
import { getElapsedTime, calculateWPM, calculateAccuracy } from "./core/timer";

export class TreeTypeApp {
  private state: TestState;
  private data: SnippetData | null = null;
  private rawData: SnippetData | null = null;
  private snippetInfo: SnippetInfo;
  private renderer: CodeRenderer;
  private keyboardHandler: KeyboardHandler | null = null;

  constructor() {
    this.state = this.initializeState();
    this.snippetInfo = { path: null, id: null, language: null };
    this.renderer = new CodeRenderer("codeLines");

    this.setupEventListeners();
    this.loadInitialSnippet();
  }

  private initializeState(): TestState {
    return {
      active: false,
      paused: false,
      startTime: null,
      endTime: null,
      pauseStartTime: null,
      totalPausedTime: 0,
      currentLineIndex: 0,
      currentCharIndex: 0,
      totalCharsTyped: 0,
      totalErrors: 0,
      completedLines: new Set(),
      errorOnCurrentChar: false,
    };
  }

  private setupEventListeners(): void {
    document.addEventListener("keydown", (e) => {
      this.keyboardHandler?.handleKeyPress(e);
    });

    // ... other event listeners ...
  }

  private async loadInitialSnippet(): Promise<void> {
    const config = loadConfig();
    await this.loadLanguage(config.language);
  }

  async loadLanguage(language: string): Promise<void> {
    // ... existing loadLanguage logic ...
  }
}

// Initialize app when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  new TreeTypeApp();
});
```

#### 3.4: Update index.html (15 mins)

**New minimal `index.html`:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>TreeType - Code Typing Practice</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="/src/styles/main.css" />
  </head>
  <body class="p-8">
    <div class="max-w-6xl mx-auto">
      <!-- HTML structure stays the same -->
      <!-- ... existing markup ... -->
    </div>

    <!-- Load app bundle -->
    <script type="module" src="/src/app.ts"></script>
  </body>
</html>
```

### Deliverables

- ✅ `src/app.ts` - Main application class
- ✅ `src/ui/renderer.ts` - Rendering logic
- ✅ `src/ui/keyboard.ts` - Keyboard handling
- ✅ Minimal index.html that loads TypeScript modules
- ✅ CSS extracted to separate file

### Success Criteria

- ✅ Full typing test works end-to-end
- ✅ All keyboard shortcuts functional
- ✅ Pause/resume works correctly
- ✅ Stats save properly
- ✅ All 4 languages load and work

### Time Estimate: 3 hours

---

## 🎯 Phase 4: Library Page Migration (Session 32)

### Goal

**Migrate library.html to TypeScript, sharing types with main app.**

### Tasks

#### 4.1: Extract Library Logic (60 mins)

**File: `src/library.ts`**

```typescript
import { SnippetMetadata } from "./types/snippet";
import { SnippetStats } from "./types/state";
import { loadSnippetStats } from "./core/storage";

export class LibraryPage {
  private allSnippets: SnippetMetadata[] = [];
  private userStats: Record<string, SnippetStats> = {};
  private currentFilter: string = "all";
  private currentSearch: string = "";
  private currentSort: string = "name";

  constructor() {
    this.initialize();
  }

  private async initialize(): Promise<void> {
    await this.loadMetadata();
    this.setupEventListeners();
  }

  private async loadMetadata(): Promise<void> {
    const response = await fetch("snippets/metadata.json");
    const data = await response.json();
    this.allSnippets = data.snippets;

    this.userStats = loadSnippetStats();
    this.renderSummaryStats();
    this.renderSnippets();
  }

  // ... rest of library logic ...
}

// Initialize when DOM ready
document.addEventListener("DOMContentLoaded", () => {
  new LibraryPage();
});
```

#### 4.2: Update library.html (15 mins)

**New minimal `library.html`:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>TreeType Snippet Library</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="/src/styles/library.css" />
  </head>
  <body class="p-8">
    <div class="max-w-7xl mx-auto">
      <!-- HTML structure stays the same -->
    </div>

    <script type="module" src="/src/library.ts"></script>
  </body>
</html>
```

### Deliverables

- ✅ `src/library.ts` - Library page logic
- ✅ Shared types between app and library
- ✅ Minimal library.html

### Success Criteria

- ✅ Library page loads correctly
- ✅ Filtering and sorting work
- ✅ Can navigate to snippets
- ✅ Stats display correctly

### Time Estimate: 1.5 hours

---

## 🎯 Phase 5: Bug Investigation & Fix (Session 33)

### Goal

**Use TypeScript's type system to investigate and fix the auto-jump whitespace bug.**

### Tasks

#### 5.1: Add Diagnostic Logging (30 mins)

**Create `src/utils/diagnostics.ts`:**

```typescript
import { Token } from "../types/snippet";

export interface TokenDiagnostic {
  text: string;
  type: string;
  categories: string[];
  typeable: boolean;
  base_typeable: boolean;
  language: string;
}

export function logTokenDiagnostics(
  tokens: Token[],
  language: string,
  mode: string
): void {
  console.group(`Token Diagnostics: ${language} (${mode} mode)`);

  tokens.forEach((token, idx) => {
    if (token.text.trim() === "" || token.text === " ") {
      console.log(`Token ${idx}:`, {
        text: `"${token.text}"`,
        type: token.type,
        categories: token.categories,
        typeable: token.typeable,
        base_typeable: token.base_typeable,
      });
    }
  });

  console.groupEnd();
}

export function compareTokensBetweenLanguages(
  pythonTokens: Token[],
  tsxTokens: Token[]
): void {
  console.group("Token Comparison: Python vs TSX");

  const pythonSpaces = pythonTokens.filter((t) => t.text === " ");
  const tsxSpaces = tsxTokens.filter((t) => t.text === " ");

  console.log("Python spaces:", pythonSpaces);
  console.log("TSX spaces:", tsxSpaces);

  console.log("Differences:");
  if (pythonSpaces.length !== tsxSpaces.length) {
    console.warn("Different number of space tokens");
  }

  // Compare categories
  const pythonCategories = new Set(pythonSpaces.flatMap((t) => t.categories));
  const tsxCategories = new Set(tsxSpaces.flatMap((t) => t.categories));

  console.log("Python space categories:", Array.from(pythonCategories));
  console.log("TSX space categories:", Array.from(tsxCategories));

  console.groupEnd();
}
```

#### 5.2: Test Across All Languages (60 mins)

1. Load identical code patterns in all 4 languages
2. Enable diagnostic logging
3. Compare token categorization
4. Identify root cause of inconsistency

#### 5.3: Implement Fix (30 mins)

Based on findings, update `applyExclusionConfig()` or parser logic.

**Hypothesis fix in `src/core/config.ts`:**

```typescript
export function applyExclusionConfig(lineData: Line, preset: TypingMode): Line {
  const config = PRESETS[preset];

  const filteredTokens: Token[] = lineData.display_tokens.map((token) => {
    let typeable = token.base_typeable;

    // CRITICAL FIX: Handle whitespace explicitly
    if (token.text.trim() === "") {
      return { ...token, typeable: false }; // Never type whitespace
    }

    if (!typeable) {
      return { ...token, typeable };
    }

    // ... rest of logic ...
  });

  // ... rest of function ...
}
```

### Deliverables

- ✅ Diagnostic utility functions
- ✅ Root cause identified
- ✅ Fix implemented and tested
- ✅ All 4 languages behave consistently

### Success Criteria

- ✅ Auto-jump works identically across all languages
- ✅ Spacebar never required (except in TSX strings if desired)
- ✅ Token categorization is consistent

### Time Estimate: 2 hours

---

# Session 32 Summary: Phase 5 - Bug Fix Attempt & Testing Pivot

**Date**: Monday, November 18, 2025  
**Duration**: ~2 hours  
**Status**: 🔄 Phase 5 In Progress - Pivoting to Testing Strategy  
**Focus**: Attempted to fix the TSX auto-jump bug in the Python parser, discovered deeper issue requiring proper testing framework.

---

## 🎯 Session Goals

1. ✅ **Phase 5 Part 1:** Implement fix for JSX text whitespace bug in Python parser
2. ✅ **Phase 5 Part 1:** Regenerate TSX snippets with fixed parser
3. ⚠️ **Phase 5 Part 1:** Verify bug is resolved across all modes
4. 🔄 **Discovery:** Identified need for comprehensive testing strategy before continuing

---

## 🔧 Phase 5 Part 1: Python Parser Fix

### The Original Bug

From Session 31, we identified that the Python parser (`build/parse_json.py`) was creating `jsx_text` tokens with trailing whitespace marked as `base_typeable: true`, causing spaces to be included in the typing sequence when they shouldn't be.

**Example from `gm_01_015_01_common-ui-patterns.tsx` line 78:**

```json
{
  "text": "Debounced: ", // ← Space included in token
  "type": "jsx_text",
  "base_typeable": true // ← WRONG! Should be split
}
```

### The Fix Implemented

**File: `build/parse_json.py`**

Added a new function `split_jsx_text_token()` that:

1. Detects `jsx_text` tokens with leading/trailing whitespace
2. Splits them into separate tokens:
   - Leading whitespace → `jsx_text_whitespace` with `BASE_TYPEABLE: False`
   - Content → `jsx_text` with `BASE_TYPEABLE: True`
   - Trailing whitespace → `jsx_text_whitespace` with `BASE_TYPEABLE: False`
3. Preserves accurate column positions for each split token

**Integration Point:**

```python
# In parse_code_to_dataframe(), after initial DataFrame creation
if language_name in ["tsx", "javascript"]:  # JSX can appear in both
    expanded_rows = []
    for idx, row in df.iterrows():
        split_tokens = split_jsx_text_token(row)
        expanded_rows.extend(split_tokens)

    if expanded_rows:
        df = pd.DataFrame(expanded_rows)
```

### Verification Results

**Test Case 1: "Debounced:" - ✅ SUCCESS**

Re-parsed `gm_01_015_01_common-ui-patterns.tsx`:

```json
{
  "text": "Debounced:",
  "type": "jsx_text",
  "base_typeable": true
},
{
  "text": " ",
  "type": "jsx_text_whitespace",
  "base_typeable": false  // ✅ Fixed!
}
```

The parser successfully split the trailing space, and the typing sequence correctly excludes it: `"<p>Debounced:{debouncedValue}</p>"`

**Test Case 2: "Loading item..." - ⚠️ UNEXPECTED ISSUE**

Testing `gm_01_014_01_async-patterns.tsx` revealed a **different problem**:

- Token structure is correct: `"Loading item..."` is a single token with `base_typeable: true`
- The issue is NOT with whitespace inside the token (the space between "Loading" and "item" is correct content)
- The ACTUAL problem: **JSX tag names (`<p>`, `</p>`) are being included in minimal mode**

---

## 🐛 The Real Bug Discovery

### Investigation Process

Using debug logging in `config.ts`, we discovered:

```javascript
// Line 18: if (loading) return <p>Loading item...</p>;
// Filtered tokens in MINIMAL mode:
{
  text: '<',
  categories: ['angle_bracket'],
  typeable: false  // ✅ Correctly excluded
},
{
  text: 'p',
  categories: [],  // ← NO CATEGORY!
  typeable: true   // ❌ WRONG! Should be false
},
{
  text: '>',
  categories: ['angle_bracket'],
  typeable: false  // ✅ Correctly excluded
}
```

**Typing sequence in minimal mode:** `"ifloadingreturnpLoading item...p"`  
**Expected sequence:** `"ifloadingreturnLoading item..."`

### Root Cause

**JSX tag names are categorized as generic `identifier` tokens** with no special categorization. While angle brackets (`<`, `>`) are correctly excluded in minimal mode, the tag names between them (`p`, `div`, `span`, etc.) are treated as regular identifiers and included.

This is technically "correct" from a token perspective (tag names ARE identifiers), but it violates the UX expectation: **when you exclude angle brackets, you don't want to type the tag names either**.

---

## 🔄 The Pivot: Testing Strategy Required

### Why We Need Tests

After multiple iterations of changing `config.ts` without success:

1. **No fast feedback loop** - Every change required rebuild + manual testing
2. **No regression detection** - Could break other modes while fixing one
3. **No clear success criteria** - Hard to know if a fix actually works
4. **No documentation** - Expected behavior only in our heads

### The Decision

**Stop fixing blindly. Build tests first.**

This aligns with the original migration plan Phase 6, but we're pulling it forward because we need it NOW.

---

## 📋 Key Learnings

### 1. Parser vs. Config Separation of Concerns

- **Parser responsibility**: Accurately tokenize source code
- **Config responsibility**: Filter tokens based on typing mode

The parser fix for whitespace splitting was correct and necessary. The JSX tag name issue is a config/filtering problem, not a parser problem.

### 2. The Danger of Iterative Debugging Without Tests

Quote from user:

> "Going around changing `src/core/config.ts` for the nth time, typing 18 lines of code only to discover the same problem persists, is not a strategy."

This was the wake-up call. Manual testing is:

- Slow
- Error-prone
- Unsustainable
- Frustrating

### 3. First Time with TypeScript/Vitest

User context:

- First TypeScript project
- Unfamiliar with JS ecosystem testing
- Coming from Python/pytest background
- Needs clear guidance on async testing patterns

This makes proper testing setup even MORE important - it will be a learning experience that pays dividends for future projects.

---

## 📊 Progress Update

### Migration Status

- ✅ **Phase 1:** Foundation Setup
- ✅ **Phase 2:** Extract Pure Functions
- ✅ **Phase 3:** Main App Migration
- ✅ **Phase 4:** Library Page Migration
- 🔄 **Phase 5 Part 1:** Parser Fix (Complete)
- 🔄 **Phase 5 Part 2:** Config Fix (Blocked - needs tests)
- ⏳ **Phase 5.5:** Testing Setup (Next session)
- ⬜ **Phase 6:** Additional Testing & Coverage
- ⬜ **Phase 7:** Build Optimization & Deployment

**Progress:** 4.5/7 phases complete (~64%)

---

## 🔧 Files Modified This Session

### Parser Fix

- **`build/parse_json.py`**
  - Added `split_jsx_text_token()` function
  - Modified `parse_code_to_dataframe()` to apply splitting for TSX/JSX
  - Successfully handles trailing/leading whitespace in jsx_text

### Config Debug Attempts (Multiple Iterations)

- **`src/core/config.ts`**
  - Added debug logging
  - Attempted JSX tag name detection (incomplete)
  - Needs proper solution guided by tests

### Regenerated Snippets

- **`snippets/tsx/gm_01_015_01_common-ui-patterns.json`** - ✅ Fixed
- **All other TSX snippets** - Regenerated with parser fix

---

## 📝 Next Session Preparation (Session 33)

### Phase 5.5: Testing Setup

**Goal:** Implement comprehensive testing framework BEFORE attempting more fixes.

**What We'll Do:**

1. Install Vitest and testing dependencies
2. Configure Vitest for TypeScript + jsdom environment
3. Create `tests/core/config.test.ts` with comprehensive test cases
4. Write tests that DEFINE expected behavior for all three modes
5. Run tests (they will FAIL - that's expected!)
6. Use failing tests as a specification for the fix
7. Implement config.ts changes guided by tests
8. Iterate until all tests PASS
9. Add tests for edge cases
10. Document testing patterns for future development

### Testing Framework: Vitest

**Why Vitest:**

- Modern, fast (uses Vite's build system)
- Jest-compatible API (easy to learn)
- Built-in TypeScript support
- Watch mode for rapid development
- UI mode for visual debugging

**Comparison to pytest:**

```python
# pytest (Python)
def test_addition():
    assert add(2, 3) == 5
```

```typescript
// Vitest (TypeScript)
test("addition", () => {
  expect(add(2, 3)).toBe(5);
});
```

Very similar syntax!

### Key Test Cases to Implement

1. **Minimal Mode Tests**

   - ✅ Excludes angle brackets
   - ✅ Excludes parentheses
   - ✅ Includes keywords and identifiers
   - ❌ **Excludes JSX tag names** ← Currently failing
   - ✅ Includes JSX text content

2. **Standard Mode Tests**

   - ✅ Includes parentheses (via includeSpecific)
   - ✅ Excludes angle brackets
   - ❌ **Excludes JSX tag names** ← Currently failing
   - ✅ Includes JSX text content

3. **Full Mode Tests**

   - ✅ Includes everything except comments
   - ✅ Includes JSX tag names
   - ✅ Includes angle brackets

4. **Whitespace Tests**
   - ✅ Never makes pure whitespace typeable
   - ✅ Includes spaces within text content
   - ✅ Excludes structural whitespace

### Preparation Checklist

- [ ] Review Vitest documentation: https://vitest.dev/
- [ ] Understand test file structure
- [ ] Have `build/parse_json.py` available (may need reference)
- [ ] Have all TSX test snippets ready for validation
- [ ] Be prepared to run: `pnpm add -D vitest @vitest/ui jsdom`

---

## 💾 Commit Summary

```bash
# Parser Fix Commit
git add build/parse_json.py
git commit -m "fix: Phase 5 - Split jsx_text tokens to handle whitespace correctly

✅ Added split_jsx_text_token() to separate content from leading/trailing whitespace
✅ jsx_text_whitespace tokens are marked as base_typeable: false
✅ Fixes trailing space bug in snippets like 'Debounced: '
✅ Preserves accurate column positions for each split token
⚠️  Note: Discovered separate issue with JSX tag names requiring testing framework"

# Regenerate TSX snippets
git add snippets/tsx/*.json
git commit -m "chore: Regenerate all TSX snippets with whitespace fix"

# Config attempts (optional - can be reverted)
git add src/core/config.ts
git commit -m "wip: Phase 5 - Debug logging for JSX tag name issue

🔄 Added debug logging to investigate minimal mode behavior
🔄 Multiple attempts to handle JSX tag names
⚠️  Not yet functional - needs proper testing strategy
📋 Next: Implement Vitest testing framework before continuing"
```

---

## 🎓 What We Learned About Testing

### Testing in TypeScript/JavaScript Ecosystem

1. **Vitest = Modern Jest** (user was correct!)

   - Same API, faster execution
   - Better TypeScript integration
   - Built by Vite team for seamless integration

2. **Async Testing**

   - Less of a concern for our use case
   - Most of our logic is synchronous (token filtering, config)
   - Async only relevant for file loading (already handled by app)

3. **Test Structure**

   ```typescript
   describe("feature", () => {
     // Group related tests
     it("does something", () => {
       // Individual test
       expect(result).toBe(expected); // Assertion
     });
   });
   ```

4. **Fast Feedback Loop**
   - Watch mode re-runs tests on file changes
   - No rebuild needed (Vitest is smart)
   - See results in <100ms

### Why This Matters

For someone new to TypeScript, proper testing is **MORE important**, not less:

- **Learning tool**: Tests document how things work
- **Safety net**: Can experiment without fear
- **Refactoring confidence**: Change code, tests catch mistakes
- **Future-proofing**: As project grows, tests prevent regressions

---

## 🎯 Success Criteria for Next Session

By end of Session 33, we should have:

1. ✅ Vitest installed and configured
2. ✅ Comprehensive test suite for `config.ts`
3. ✅ Tests clearly showing expected vs. actual behavior
4. ✅ Config fix implemented and all tests passing
5. ✅ Verified fix works in browser
6. ✅ Documentation of testing patterns for future use

**Then Phase 5 will be truly complete, and we can move forward with confidence.**

---

## 🤔 Philosophical Note: When to Stop and Test

This session perfectly illustrated the principle:

> **"If you find yourself debugging the same thing three times, stop and write tests."**

We tried:

1. Parser fix (worked for one case)
2. Config fix attempt #1 (didn't work)
3. Config fix attempt #2 (didn't work)
4. Config fix attempt #3 (didn't work)

At this point, the right move is to **step back and build infrastructure** rather than keep guessing.

This is the essence of good engineering: recognizing when tactical fixes are failing and switching to a strategic approach.

---

**Looking forward to Session 33 where we build the testing foundation that will make future development faster, safer, and more enjoyable!** 🚀

---

## 📚 Additional Resources for Next Session

- [Vitest Getting Started](https://vitest.dev/guide/)
- [Vitest API Reference](https://vitest.dev/api/)
- [Testing Best Practices](https://vitest.dev/guide/best-practices.html)
- [Jest to Vitest Migration](https://vitest.dev/guide/migration.html) (for reference)

## 🎯 Phase 6: Testing & Validation (Session 34)

### Goal

**Add proper unit tests now that code is modular.**

### Tasks

#### 6.1: Install Testing Framework (15 mins)

```bash
npm install --save-dev vitest @vitest/ui
```

**Update `package.json`:**

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

**Create `vitest.config.ts`:**

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/setup.ts"],
  },
});
```

#### 6.2: Write Timer Tests (45 mins)

**File: `tests/core/timer.test.ts`**

```typescript
import { describe, test, expect, beforeEach } from "vitest";
import {
  getElapsedTime,
  calculateWPM,
  calculateAccuracy,
  formatTime,
} from "../../src/core/timer";
import { TestState } from "../../src/types/state";

describe("Timer Functions", () => {
  describe("getElapsedTime", () => {
    test("returns 0 when test not active", () => {
      const state: TestState = {
        active: false,
        paused: false,
        startTime: null,
        endTime: null,
        pauseStartTime: null,
        totalPausedTime: 0,
        currentLineIndex: 0,
        currentCharIndex: 0,
        totalCharsTyped: 0,
        totalErrors: 0,
        completedLines: new Set(),
        errorOnCurrentChar: false,
      };

      expect(getElapsedTime(state)).toBe(0);
    });

    test("calculates elapsed time correctly", () => {
      const state: TestState = {
        active: true,
        paused: false,
        startTime: Date.now() - 60000, // 60 seconds ago
        endTime: null,
        pauseStartTime: null,
        totalPausedTime: 0,
        currentLineIndex: 0,
        currentCharIndex: 0,
        totalCharsTyped: 100,
        totalErrors: 5,
        completedLines: new Set(),
        errorOnCurrentChar: false,
      };

      const elapsed = getElapsedTime(state);
      expect(elapsed).toBeCloseTo(60, 0); // Within 1 second tolerance
    });

    test("excludes pause time from elapsed time", () => {
      const state: TestState = {
        active: true,
        paused: false,
        startTime: Date.now() - 90000, // 90 seconds ago
        endTime: null,
        pauseStartTime: null,
        totalPausedTime: 30000, // 30 seconds paused
        currentLineIndex: 0,
        currentCharIndex: 0,
        totalCharsTyped: 100,
        totalErrors: 5,
        completedLines: new Set(),
        errorOnCurrentChar: false,
      };

      const elapsed = getElapsedTime(state);
      expect(elapsed).toBeCloseTo(60, 0); // Should be 60, not 90
    });

    test("excludes current pause duration when paused", () => {
      const state: TestState = {
        active: true,
        paused: true,
        startTime: Date.now() - 90000, // 90 seconds ago
        endTime: null,
        pauseStartTime: Date.now() - 10000, // Paused 10 seconds ago
        totalPausedTime: 30000, // Previous pauses: 30 seconds
        currentLineIndex: 0,
        currentCharIndex: 0,
        totalCharsTyped: 100,
        totalErrors: 5,
        completedLines: new Set(),
        errorOnCurrentChar: false,
      };

      const elapsed = getElapsedTime(state);
      expect(elapsed).toBeCloseTo(50, 0); // 90 - 30 - 10 = 50
    });
  });

  describe("calculateWPM", () => {
    test("calculates WPM correctly", () => {
      expect(calculateWPM(300, 60)).toBe(60); // 300 chars in 60s = 60 WPM
      expect(calculateWPM(150, 30)).toBe(60); // 150 chars in 30s = 60 WPM
      expect(calculateWPM(500, 120)).toBe(50); // 500 chars in 120s = 50 WPM
    });

    test("returns 0 for zero elapsed time", () => {
      expect(calculateWPM(100, 0)).toBe(0);
    });

    test("returns 0 for negative elapsed time", () => {
      expect(calculateWPM(100, -10)).toBe(0);
    });

    test("rounds to nearest integer", () => {
      expect(calculateWPM(303, 60)).toBe(61); // 60.6 -> 61
      expect(calculateWPM(297, 60)).toBe(59); // 59.4 -> 59
    });
  });

  describe("calculateAccuracy", () => {
    test("calculates accuracy correctly", () => {
      expect(calculateAccuracy(100, 5)).toBe(95);
      expect(calculateAccuracy(100, 0)).toBe(100);
      expect(calculateAccuracy(100, 10)).toBe(90);
    });

    test("returns 100% for zero total chars", () => {
      expect(calculateAccuracy(0, 0)).toBe(100);
    });

    test("handles edge case of more errors than chars", () => {
      expect(calculateAccuracy(50, 60)).toBe(-20);
    });

    test("rounds to nearest integer", () => {
      expect(calculateAccuracy(100, 3)).toBe(97); // 97% exactly
      expect(calculateAccuracy(100, 7)).toBe(93); // 93% exactly
    });
  });

  describe("formatTime", () => {
    test("formats time correctly", () => {
      expect(formatTime(0)).toBe("0:00");
      expect(formatTime(30)).toBe("0:30");
      expect(formatTime(60)).toBe("1:00");
      expect(formatTime(90)).toBe("1:30");
      expect(formatTime(125)).toBe("2:05");
      expect(formatTime(3661)).toBe("61:01");
    });

    test("pads seconds with leading zero", () => {
      expect(formatTime(5)).toBe("0:05");
      expect(formatTime(65)).toBe("1:05");
    });
  });
});
```

#### 6.3: Write Config Tests (45 mins)

**File: `tests/core/config.test.ts`**

```typescript
import { describe, test, expect, beforeEach, vi } from "vitest";
import {
  applyExclusionConfig,
  PRESETS,
  saveConfig,
  loadConfig,
} from "../../src/core/config";
import { Line, Token } from "../../src/types/snippet";

describe("Configuration Functions", () => {
  describe("applyExclusionConfig", () => {
    const mockLine: Line = {
      line_number: 0,
      indent_level: 0,
      display_tokens: [
        {
          text: "def",
          type: "keyword",
          typeable: true,
          base_typeable: true,
          start_col: 0,
          end_col: 3,
          categories: ["keyword"],
        },
        {
          text: " ",
          type: "whitespace",
          typeable: false,
          base_typeable: false,
          start_col: 3,
          end_col: 4,
          categories: [],
        },
        {
          text: "hello",
          type: "identifier",
          typeable: true,
          base_typeable: true,
          start_col: 4,
          end_col: 9,
          categories: ["identifier"],
        },
        {
          text: "(",
          type: "parenthesis",
          typeable: true,
          base_typeable: true,
          start_col: 9,
          end_col: 10,
          categories: ["parenthesis"],
        },
        {
          text: ")",
          type: "parenthesis",
          typeable: true,
          base_typeable: true,
          start_col: 10,
          end_col: 11,
          categories: ["parenthesis"],
        },
        {
          text: ":",
          type: "punctuation",
          typeable: true,
          base_typeable: true,
          start_col: 11,
          end_col: 12,
          categories: ["punctuation"],
        },
      ],
      typing_sequence: "",
      char_map: {},
    };

    test("minimal mode excludes parentheses and punctuation", () => {
      const result = applyExclusionConfig(mockLine, "minimal");

      expect(result.typing_sequence).toBe("defhello");
      expect(result.display_tokens[0].typeable).toBe(true); // def
      expect(result.display_tokens[2].typeable).toBe(true); // hello
      expect(result.display_tokens[3].typeable).toBe(false); // (
      expect(result.display_tokens[4].typeable).toBe(false); // )
      expect(result.display_tokens[5].typeable).toBe(false); // :
    });

    test("standard mode includes specific punctuation", () => {
      const result = applyExclusionConfig(mockLine, "standard");

      expect(result.typing_sequence).toBe("defhello():");
      expect(result.display_tokens[3].typeable).toBe(true); // ( included
      expect(result.display_tokens[4].typeable).toBe(true); // ) included
      expect(result.display_tokens[5].typeable).toBe(true); // : included
    });

    test("full mode includes everything except comments", () => {
      const result = applyExclusionConfig(mockLine, "full");

      expect(result.typing_sequence).toBe("defhello():");
      expect(result.display_tokens.filter((t) => t.typeable).length).toBe(5);
    });

    test("regenerates char_map correctly", () => {
      const result = applyExclusionConfig(mockLine, "minimal");

      expect(result.char_map["0"]).toEqual({ token_idx: 0, display_col: 0 });
      expect(result.char_map["3"]).toEqual({ token_idx: 1, display_col: 4 });
    });

    test("whitespace is never typeable", () => {
      const result = applyExclusionConfig(mockLine, "full");

      expect(result.display_tokens[1].typeable).toBe(false); // space
    });
  });

  describe("localStorage integration", () => {
    beforeEach(() => {
      // Mock localStorage
      const store: Record<string, string> = {};

      vi.spyOn(Storage.prototype, "getItem").mockImplementation(
        (key) => store[key] || null
      );
      vi.spyOn(Storage.prototype, "setItem").mockImplementation(
        (key, value) => {
          store[key] = value;
        }
      );
    });

    test("saveConfig stores configuration", () => {
      const config = {
        preset: "minimal" as const,
        language: "python" as const,
      };

      saveConfig(config);

      expect(localStorage.setItem).toHaveBeenCalledWith(
        "treetype_config",
        JSON.stringify(config)
      );
    });

    test("loadConfig retrieves saved configuration", () => {
      const config = {
        preset: "standard" as const,
        language: "typescript" as const,
      };
      localStorage.setItem("treetype_config", JSON.stringify(config));

      const loaded = loadConfig();

      expect(loaded).toEqual(config);
    });

    test("loadConfig returns default when nothing saved", () => {
      const loaded = loadConfig();

      expect(loaded).toEqual({ preset: "standard", language: "python" });
    });
  });
});
```

#### 6.4: Write Integration Tests (60 mins)

**File: `tests/integration/typing-flow.test.ts`**

```typescript
import { describe, test, expect, beforeEach } from "vitest";
import { TestState } from "../../src/types/state";
import { SnippetData } from "../../src/types/snippet";
import { applyExclusionConfig } from "../../src/core/config";
import { getElapsedTime, calculateWPM } from "../../src/core/timer";

describe("Complete Typing Flow Integration", () => {
  let mockSnippet: SnippetData;
  let state: TestState;

  beforeEach(() => {
    mockSnippet = {
      language: "python",
      total_lines: 2,
      lines: [
        {
          line_number: 0,
          indent_level: 0,
          display_tokens: [
            {
              text: "def",
              type: "keyword",
              typeable: true,
              base_typeable: true,
              start_col: 0,
              end_col: 3,
              categories: ["keyword"],
            },
            {
              text: " ",
              type: "whitespace",
              typeable: false,
              base_typeable: false,
              start_col: 3,
              end_col: 4,
              categories: [],
            },
            {
              text: "test",
              type: "identifier",
              typeable: true,
              base_typeable: true,
              start_col: 4,
              end_col: 8,
              categories: ["identifier"],
            },
          ],
          typing_sequence: "deftest",
          char_map: {
            "0": { token_idx: 0, display_col: 0 },
            "3": { token_idx: 2, display_col: 4 },
          },
        },
        {
          line_number: 1,
          indent_level: 1,
          display_tokens: [
            {
              text: "return",
              type: "keyword",
              typeable: true,
              base_typeable: true,
              start_col: 4,
              end_col: 10,
              categories: ["keyword"],
            },
          ],
          typing_sequence: "return",
          char_map: {
            "0": { token_idx: 0, display_col: 4 },
          },
        },
      ],
    };

    state = {
      active: false,
      paused: false,
      startTime: null,
      endTime: null,
      pauseStartTime: null,
      totalPausedTime: 0,
      currentLineIndex: 0,
      currentCharIndex: 0,
      totalCharsTyped: 0,
      totalErrors: 0,
      completedLines: new Set(),
      errorOnCurrentChar: false,
    };
  });

  test("complete typing test without errors", () => {
    // Start test
    state.active = true;
    state.startTime = Date.now();

    // Type first line: "deftest"
    "deftest".split("").forEach((char) => {
      state.currentCharIndex++;
      state.totalCharsTyped++;
    });

    // Move to second line
    state.completedLines.add(0);
    state.currentLineIndex = 1;
    state.currentCharIndex = 0;

    // Type second line: "return"
    "return".split("").forEach((char) => {
      state.currentCharIndex++;
      state.totalCharsTyped++;
    });

    // Complete test
    state.active = false;
    state.endTime = Date.now();

    expect(state.totalCharsTyped).toBe(13);
    expect(state.totalErrors).toBe(0);
    expect(state.completedLines.size).toBe(1);
  });

  test("typing test with pause preserves accuracy", () => {
    // Start test
    state.active = true;
    state.startTime = Date.now() - 60000; // Started 60 seconds ago

    // Type some characters
    state.totalCharsTyped = 300;

    // Pause for 30 seconds
    state.paused = true;
    state.pauseStartTime = Date.now() - 30000;
    state.totalPausedTime = 30000;

    // Resume
    state.paused = false;

    // Calculate WPM
    const elapsed = getElapsedTime(state);
    const wpm = calculateWPM(state.totalCharsTyped, elapsed);

    // Should be based on 30 seconds of typing, not 60
    expect(elapsed).toBeCloseTo(30, 0);
    expect(wpm).toBeCloseTo(120, 0); // 300 chars / 5 / 0.5 min = 120 WPM
  });

  test("mode switching regenerates typing sequence correctly", () => {
    const line = mockSnippet.lines[0];

    // Apply minimal mode
    const minimal = applyExclusionConfig(line, "minimal");
    expect(minimal.typing_sequence).toBe("deftest");

    // Apply standard mode (includes parentheses if present)
    const standard = applyExclusionConfig(line, "standard");
    expect(standard.typing_sequence).toBe("deftest");

    // Sequences should be consistent
    expect(minimal.display_tokens.length).toBe(standard.display_tokens.length);
  });
});
```

### Deliverables

- ✅ Vitest configured
- ✅ 30+ unit tests for core functions
- ✅ Integration tests for typing flows
- ✅ All tests passing

### Success Criteria

- ✅ `npm test` runs all tests
- ✅ 80%+ code coverage on core logic
- ✅ Tests document expected behavior
- ✅ Can run tests in CI/CD

### Time Estimate: 2.5 hours

---

## 🎯 Phase 7: Build Optimization & Deployment (Session 35)

### Goal

**Optimize build process, add production build, prepare for deployment.**

### Tasks

#### 7.1: Optimize Bundle Size (30 mins)

**Update `vite.config.js`:**

```javascript
import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  root: ".",
  build: {
    outDir: "dist",
    minify: "terser",
    sourcemap: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        library: resolve(__dirname, "library.html"),
      },
      output: {
        manualChunks: {
          vendor: ["lodash"], // If using any third-party libs
        },
      },
    },
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.logs in production
      },
    },
  },
  server: {
    port: 3000,
    open: true,
  },
});
```

#### 7.2: Add Production Build Script (15 mins)

**Update `package.json`:**

```json
{
  "scripts": {
    "dev": "vite",
    "build": "npm run type-check && vite build",
    "build:prod": "npm run test && npm run build",
    "preview": "vite preview",
    "type-check": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

#### 7.3: Setup GitHub Actions CI/CD (30 mins)

**File: `.github/workflows/ci.yml`**

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Type check
        run: npm run type-check

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

#### 7.4: Add Environment-Specific Config (15 mins)

**File: `.env.development`:**

```
VITE_APP_ENV=development
VITE_ENABLE_LOGGING=true
```

**File: `.env.production`:**

```
VITE_APP_ENV=production
VITE_ENABLE_LOGGING=false
```

**Use in code:**

```typescript
const isDev = import.meta.env.VITE_APP_ENV === "development";

if (isDev) {
  console.log("Debug info:", data);
}
```

### Deliverables

- ✅ Optimized production build
- ✅ GitHub Actions CI/CD pipeline
- ✅ Environment-specific configurations
- ✅ Automated deployment to GitHub Pages

### Success Criteria

- ✅ Build size < 500KB (compressed)
- ✅ CI/CD runs on every push
- ✅ Auto-deploys on main branch
- ✅ Tests must pass before deploy

### Time Estimate: 1.5 hours

---

## 📊 Migration Summary

### Total Timeline

| Phase       | Focus          | Time           | Sessions       |
| ----------- | -------------- | -------------- | -------------- |
| **Phase 1** | Setup & Types  | 2 hours        | Session 29     |
| **Phase 2** | Pure Functions | 2 hours        | Session 30     |
| **Phase 3** | Main App       | 3 hours        | Session 31     |
| **Phase 4** | Library Page   | 1.5 hours      | Session 32     |
| **Phase 5** | Bug Fix        | 2 hours        | Session 33     |
| **Phase 6** | Testing        | 2.5 hours      | Session 34     |
| **Phase 7** | Deployment     | 1.5 hours      | Session 35     |
| **Total**   |                | **14.5 hours** | **7 sessions** |

---

## ✅ Phase Completion Checklist

### Before Starting Each Phase

- [ ] Review previous phase deliverables
- [ ] Ensure all tests passing
- [ ] Commit current working state
- [ ] Read phase objectives carefully

### After Completing Each Phase

- [ ] All deliverables completed
- [ ] Success criteria met
- [ ] Tests passing (if applicable)
- [ ] Code committed with descriptive message
- [ ] Documentation updated
- [ ] Ready to demo functionality

---

## 🎯 Benefits Gained at Each Phase

### After Phase 1

- ✅ Type definitions document entire codebase
- ✅ IDE autocomplete for all data structures
- ✅ Can catch type errors before running code

### After Phase 2

- ✅ Core logic is testable
- ✅ Functions have clear input/output contracts
- ✅ Refactoring is safer

### After Phase 3

- ✅ Main app is fully type-safe
- ✅ No more "undefined is not a function" errors
- ✅ Can confidently add new features

### After Phase 4

- ✅ Entire codebase is TypeScript
- ✅ Shared types between pages
- ✅ Consistent data structures

### After Phase 5

- ✅ Auto-jump bug fixed forever
- ✅ Type system prevents similar bugs
- ✅ All languages work consistently

### After Phase 6

- ✅ Automated testing catches regressions
- ✅ Refactoring with confidence
- ✅ Documentation via tests

### After Phase 7

- ✅ Professional deployment pipeline
- ✅ Automatic quality checks
- ✅ Production-ready builds

---

## 🚨 Risk Management

### Low Risk Phases

- Phase 1 (just setup)
- Phase 2 (pure functions, easily testable)
- Phase 7 (deployment, doesn't affect code)

### Medium Risk Phases

- Phase 4 (library page less critical)
- Phase 6 (testing, additive only)

### Higher Risk Phases

- Phase 3 (main app migration)
- Phase 5 (bug fix could introduce regressions)

**Mitigation Strategy:**

- Always commit working state before risky changes
- Write tests before refactoring
- Keep phases small and reversible
- Test manually after each phase

---

## 🔄 Rollback Strategy

If anything goes wrong at any phase:

1. **Immediate rollback:**

   ```bash
   git reset --hard HEAD~1
   ```

2. **Gradual rollback:**

   - Revert specific files
   - Keep type definitions
   - Return to previous phase

3. **Forward fix:**
   - Identify specific issue
   - Fix in isolation
   - Add test to prevent recurrence

---

## 📚 Learning Resources

### TypeScript Basics (Recommended Before Phase 1)

- Official TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/intro.html
- Focus on:
  - Basic types
  - Interfaces
  - Type aliases
  - Generics (briefly)

### Vite (Glance Before Phase 1)

- Getting started: https://vitejs.dev/guide/
- Just understand: it bundles files fast

### Vitest (Before Phase 6)

- Getting started: https://vitest.dev/guide/
- Similar to Jest, easier setup

---

## 💡 Session-by-Session Focus

### Session 29: Foundation (Phase 1)

**Mindset:** "Set up the runway"

- Don't write code yet, just infrastructure
- Type definitions are documentation
- Slow and steady, ensure everything works

### Session 30: Pure Functions (Phase 2)

**Mindset:** "Extract the easy stuff first"

- Start with timer.ts (simplest)
- Test each function as you extract
- Small wins build confidence

### Session 31: Main Migration (Phase 3)

**Mindset:** "This is the big one"

- Expect 3+ hours
- Take breaks between subsections
- Test frequently in browser

### Session 32: Library Page (Phase 4)

**Mindset:** "Easier than Phase 3"

- Follow same pattern as main app
- Share types and utilities
- Should feel familiar now

### Session 33: Bug Hunt (Phase 5)

**Mindset:** "Detective mode"

- Use TypeScript to guide investigation
- Add logging, compare outputs
- Fix root cause, not symptoms

### Session 34: Testing (Phase 6)

**Mindset:** "Safety net time"

- Write tests you wish you had before
- Test complex functions first
- Integration tests last

### Session 35: Deploy (Phase 7)

**Mindset:** "Ship it"

- Optimize for production
- Automate everything
- Celebrate! 🎉

---

## 🎉 Completion Celebration Checklist

When all phases complete:

- [ ] Run full test suite: `npm test`
- [ ] Build production: `npm run build:prod`
- [ ] Check bundle size
- [ ] Test on real devices/browsers
- [ ] Update README with new structure
- [ ] Create release tag
- [ ] Deploy to production
- [ ] Share with community!

---

## 📝 Next Steps After Migration

With TypeScript foundation in place:

1. **Add more typing modes** (easier now with types)
2. **Build snippet editor** (types prevent bugs)
3. **Add leaderboards** (shared types for client/server)
4. **Mobile app** (reuse types in React Native)
5. **VS Code extension** (TypeScript is native)

**The possibilities are endless with a type-safe foundation!**

---

## 🤝 Getting Help

If stuck during any phase:

1. **Check type errors carefully** - They're helpful!
2. **Use `npm run type-check`** - Catch issues early
3. **Console.log strategically** - Debug data flow
4. **Test in isolation** - Break down problems
5. **Ask Claude** - Bring error messages + context

---

**Ready to start Phase 1 in Session 29?** 🚀

Let's build a rock-solid, type-safe TreeType!
