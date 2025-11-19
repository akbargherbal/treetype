import { TestState, SnippetInfo } from "./types/state";
import { SnippetData } from "./types/snippet";
import { CodeRenderer } from "./ui/renderer";
import { KeyboardHandler } from "./ui/keyboard";
import {
  PRESETS,
  applyExclusionConfig,
  loadConfig,
  saveConfig,
} from "./core/config";
import {
  getElapsedTime,
  calculateWPM,
  calculateAccuracy,
  formatTime,
} from "./core/timer";
import {
  loadSnippetStats,
  saveSnippetStats,
  enableFirebaseSync,
  disableFirebaseSync,
} from "./core/storage";
import { AuthManager } from "./core/auth";
import { User } from "firebase/auth";

/**
 * Helper to generate initials from email
 * e.g. march.ghurbal.2025@gmail.com -> MG
 * e.g. admin@test.com -> AD
 */
function getInitials(email: string | null): string {
  if (!email) return "??";
  const parts = email.split("@")[0].split(".");
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return email.substring(0, 2).toUpperCase();
}

/**
 * Main application class for TreeType
 */
export class TreeTypeApp {
  private state: TestState;
  private data: SnippetData | null = null;
  private rawData: SnippetData | null = null;
  private snippetInfo: SnippetInfo;
  private renderer: CodeRenderer;
  private keyboardHandler: KeyboardHandler | null = null;
  private authManager: AuthManager;

  constructor() {
    this.state = this.initializeState();
    this.snippetInfo = { path: null, id: null, language: null };
    this.renderer = new CodeRenderer("codeLines");

    // Initialize AuthManager with callback
    this.authManager = new AuthManager((user) => this.handleAuthChange(user));

    this.setupEventListeners();
    this.loadInitialSnippet();
  }

  /**
   * Initialize test state
   */
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

  /**
   * Handle authentication state changes
   */
  private handleAuthChange(user: User | null): void {
    // Handle Sync State
    if (user) {
      enableFirebaseSync(user.uid).catch((err) =>
        console.error("Sync failed:", err)
      );
    } else {
      disableFirebaseSync();
    }

    // Handle UI
    const authContainer = document.getElementById("authContainer");
    if (!authContainer) return;

    if (user) {
      // Logged in state - Avatar Menu (Standard 1)
      const initials = getInitials(user.email);

      authContainer.innerHTML = `
        <div class="relative group z-50">
            <button class="flex items-center gap-2 pl-1 pr-2 py-1 rounded-full hover:bg-gray-800 transition border border-transparent hover:border-gray-700">
                <!-- Avatar -->
                <div class="h-9 w-9 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-bold text-white shadow-sm select-none">
                    ${initials}
                </div>
                <!-- Chevron -->
                <svg class="text-gray-400" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            
            <!-- Dropdown Wrapper: Uses pt-2 instead of mt-2 to create a hover bridge -->
            <div class="absolute right-0 top-full pt-2 w-64 hidden group-hover:block">
                <!-- Visual Dropdown Box -->
                <div class="bg-gray-800 rounded-md shadow-xl border border-gray-700 py-1">
                    <div class="px-4 py-3 text-xs text-gray-400 border-b border-gray-700">
                        <div class="font-medium text-gray-200 mb-1">Signed in as</div>
                        <div class="truncate" title="${user.email}">${user.email}</div>
                    </div>
                    <button id="authSignOutBtn" class="w-full text-left block px-4 py-2 text-sm text-red-400 hover:bg-gray-700 transition flex items-center gap-2 rounded-b-md">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                        Sign Out
                    </button>
                </div>
            </div>
        </div>
      `;

      // Wire up Sign Out
      document
        .getElementById("authSignOutBtn")
        ?.addEventListener("click", () => {
          this.authManager.logout();
        });
    } else {
      // Logged out state
      authContainer.innerHTML = `
        <button id="authSignInBtn" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-full text-sm font-semibold transition shadow-lg flex items-center gap-2">
          <span>G</span> <span class="hidden sm:inline">Sign In</span>
        </button>
      `;

      // Wire up Sign In
      document
        .getElementById("authSignInBtn")
        ?.addEventListener("click", () => {
          this.authManager.signInWithGoogle().catch((error) => {
            alert("Sign in failed: " + error.message);
          });
        });
    }
  }

  /**
   * Set up event listeners
   */
  private setupEventListeners(): void {
    // Global keydown handler
    document.addEventListener("keydown", (e) => {
      this.keyboardHandler?.handleKeyPress(e);
    });

    // Language selector
    const languageSelect = document.getElementById(
      "languageSelect"
    ) as HTMLSelectElement;
    languageSelect.addEventListener("change", (e) => {
      this.loadLanguage((e.target as HTMLSelectElement).value);
      this.saveCurrentConfig();
    });

    // Typing mode radios
    document.querySelectorAll('input[name="typingMode"]').forEach((radio) => {
      radio.addEventListener("change", () => {
        this.reapplyTypingMode();
        this.saveCurrentConfig();
      });
    });

    // Reset button
    document.getElementById("resetBtn")?.addEventListener("click", () => {
      this.resetTest();
    });

    // Pause button
    document.getElementById("pauseBtn")?.addEventListener("click", () => {
      this.togglePause();
    });

    // Code display focus
    const codeDisplay = document.getElementById("codeDisplay");
    codeDisplay?.addEventListener("click", () => {
      codeDisplay.classList.add("focused");
    });
    codeDisplay?.addEventListener("blur", () => {
      codeDisplay.classList.remove("focused");
    });
  }

  /**
   * Load initial snippet based on saved config
   */
  private async loadInitialSnippet(): Promise<void> {
    const config = loadConfig();

    // Set UI to match config
    const presetRadio = document.querySelector(
      `input[name="typingMode"][value="${config.preset}"]`
    ) as HTMLInputElement;
    if (presetRadio) {
      presetRadio.checked = true;
    }

    const languageSelect = document.getElementById(
      "languageSelect"
    ) as HTMLSelectElement;
    languageSelect.value = config.language;

    await this.loadLanguage(config.language);

    setTimeout(() => {
      document.getElementById("codeDisplay")?.focus();
    }, 100);
  }

  /**
   * Load language snippet
   */
  async loadLanguage(language: string): Promise<void> {
    const urlParams = new URLSearchParams(window.location.search);
    const snippetPath = urlParams.get("snippet");

    let fetchPath: string;
    if (snippetPath) {
      fetchPath = snippetPath;
    } else {
      const defaultSnippets: Record<string, string> = {
        python:
          "snippets/python/gm_01_001_02_03_core-python-patterns-quick-refresh.json",
        javascript: "snippets/javascript/gm_01_001_01_array-methods.json",
        typescript: "snippets/typescript/gm_01_026_01_apidata-patterns.json",
        tsx: "snippets/tsx/gm_01_014_01_async-patterns.json",
      };
      fetchPath = defaultSnippets[language];
    }

    try {
      const response = await fetch(fetchPath);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      this.rawData = await response.json();

      this.snippetInfo.path = fetchPath;
      this.snippetInfo.language = this.rawData!.language;

      const pathParts = fetchPath.split("/");
      const filename = pathParts[pathParts.length - 1].replace(".json", "");
      const lang = pathParts[pathParts.length - 2];
      this.snippetInfo.id = `${lang}-${filename}`;

      console.log("Loaded snippet:", this.snippetInfo);

      this.reapplyTypingMode();
      this.resetTest();
    } catch (error) {
      console.error("Error loading file:", error);
      const codelinesEl = document.getElementById("codeLines");
      if (codelinesEl) {
        codelinesEl.innerHTML = `
          <div class="text-red-400">
            Error loading snippet<br>
            Make sure you're running this from the project root directory.<br>
            Error: ${
              error instanceof Error ? error.message : String(error)
            }<br><br>
            <a href="library.html" class="text-blue-400 underline">Go to Library to select a snippet</a>
          </div>
        `;
      }
    }
  }

  /**
   * Reapply typing mode to current data
   */
  private reapplyTypingMode(): void {
    if (!this.rawData) return;

    const preset = (
      document.querySelector(
        'input[name="typingMode"]:checked'
      ) as HTMLInputElement
    )?.value as "minimal" | "standard" | "full";

    this.data = {
      ...this.rawData,
      lines: this.rawData.lines.map((line) =>
        applyExclusionConfig(line, preset)
      ),
    };

    // Update keyboard handler with new data
    if (this.keyboardHandler && this.data) {
      this.keyboardHandler.updateReferences(this.state, this.data);
    }
  }

  /**
   * Save current configuration
   */

  private saveCurrentConfig(): void {
    const preset = (
      document.querySelector(
        'input[name="typingMode"]:checked'
      ) as HTMLInputElement
    )?.value as "minimal" | "standard" | "full";
    const language = (
      document.getElementById("languageSelect") as HTMLSelectElement
    )?.value as "python" | "javascript" | "typescript" | "tsx";

    saveConfig({ preset, language });
  }

  /**
   * Reset test to initial state
   */
  resetTest(): void {
    this.state = this.initializeState();

    if (this.data) {
      // Skip to first typeable line
      while (
        this.state.currentLineIndex < this.data.total_lines &&
        (!this.data.lines[this.state.currentLineIndex] ||
          this.data.lines[this.state.currentLineIndex].typing_sequence
            .length === 0)
      ) {
        this.state.currentLineIndex++;
      }
    }

    document.body.classList.remove("test-active");
    this.hidePauseOverlay();

    if (this.data) {
      this.renderer.renderCode(this.data, this.state);

      // Create keyboard handler with callbacks
      this.keyboardHandler = new KeyboardHandler(
        this.state,
        this.data,
        this.snippetInfo,
        {
          onTestStart: () => this.startTest(),
          onCharacterTyped: () => this.updateDisplay(),
          onLineComplete: () => this.moveToNextLine(),
          onTestComplete: () => this.completeTest(),
          onPauseToggle: () => this.togglePause(),
          onReset: () => {
            this.closeModal();
            this.resetTest();
          },
        }
      );
    }

    this.updateStats();
    this.updatePauseButton();
    this.updateStatus("Press any key to start...");

    // Scroll to first line
    requestAnimationFrame(() => {
      const firstLine = document.getElementById(
        `line-${this.state.currentLineIndex}`
      );
      if (firstLine) {
        const targetY =
          firstLine.offsetTop -
          window.innerHeight / 4 +
          firstLine.offsetHeight / 4;
        window.scrollTo({
          top: targetY,
          behavior: "auto",
        });
      }
    });
  }

  /**
   * Start the typing test
   */
  private startTest(): void {
    this.state.active = true;
    this.state.startTime = Date.now();
    this.updateStatus("Typing...", "success");
    document.body.classList.add("test-active");
    this.updatePauseButton();
  }

  /**
   * Toggle pause state
   */
  private togglePause(): void {
    if (!this.state.active) {
      console.log("Cannot pause: test not active");
      return;
    }

    if (this.state.paused) {
      // Resume
      console.log("Resuming test");

      const pauseDuration = Date.now() - (this.state.pauseStartTime || 0);
      this.state.totalPausedTime += pauseDuration;

      this.state.paused = false;
      this.state.pauseStartTime = null;

      this.hidePauseOverlay();
      this.updatePauseButton();
      this.updateStatus("Typing...", "success");

      document.getElementById("codeDisplay")?.focus();
    } else {
      // Pause
      console.log("Pausing test");

      this.state.paused = true;
      this.state.pauseStartTime = Date.now();

      this.showPauseOverlay();
      this.updatePauseButton();
      this.updateStatus("Paused (Tab to resume)", "warning");
    }

    this.updateStats();
  }

  /**
   * Show pause overlay
   */
  private showPauseOverlay(): void {
    this.hidePauseOverlay();

    const overlay = document.createElement("div");
    overlay.id = "pauseOverlay";
    overlay.className = "pause-overlay";
    overlay.innerHTML = `
      <div class="pause-content">
        <div class="pause-icon">⸸</div>
        <h2 class="text-3xl font-bold mb-4">Paused</h2>
        <p class="text-lg mb-2">Press <kbd class="pause-kbd">Tab</kbd> to resume</p>
        <p class="text-sm text-gray-400 mt-4">or <kbd class="pause-kbd">Esc</kbd> to reset test</p>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.addEventListener("click", () => this.togglePause());
  }

  /**
   * Hide pause overlay
   */
  private hidePauseOverlay(): void {
    const overlay = document.getElementById("pauseOverlay");
    if (overlay) {
      overlay.remove();
    }
  }

  /**
   * Update pause button state
   */
  private updatePauseButton(): void {
    const btn = document.getElementById("pauseBtn");
    if (!btn) return;

    if (this.state.paused) {
      btn.textContent = "▶️ Resume";
      btn.classList.add("paused-state");
    } else {
      btn.textContent = "⸸ Pause";
      btn.classList.remove("paused-state");
    }

    if (!this.state.active) {
      btn.setAttribute("disabled", "true");
      btn.classList.add("opacity-50", "cursor-not-allowed");
    } else {
      btn.removeAttribute("disabled");
      btn.classList.remove("opacity-50", "cursor-not-allowed");
    }
  }

  /**
   * Update display after character typed
   */
  private updateDisplay(): void {
    if (!this.data) return;

    const currentLine = this.data.lines[this.state.currentLineIndex];
    this.renderer.updateCurrentLine(
      currentLine,
      this.state.currentLineIndex,
      this.state
    );
    this.updateStats();
  }

  /**
   * Move to next line
   */
  private moveToNextLine(): void {
    if (!this.keyboardHandler) return;

    const moved = this.keyboardHandler.moveToNextLine();

    if (moved && this.data) {
      this.renderer.renderCode(this.data, this.state);
      this.updateStats();
      setTimeout(() => this.smartScroll(), 0);
    }
  }

  /**
   * Smart scroll to keep current line visible
   */
  private smartScroll(): void {
    const nextLineEl = document.getElementById(
      `line-${this.state.currentLineIndex}`
    );
    if (!nextLineEl) return;

    const currentScrollY = window.scrollY;
    const viewportHeight = window.innerHeight;

    const targetY =
      nextLineEl.offsetTop - viewportHeight / 4 + nextLineEl.offsetHeight / 4;

    if (targetY > currentScrollY) {
      window.scrollTo({
        top: targetY,
      });
    }
  }

  /**
   * Complete the test
   */
  private completeTest(): void {
    this.state.endTime = Date.now();

    // Calculate stats BEFORE setting active = false
    const elapsed = getElapsedTime(this.state);
    const wpm = calculateWPM(this.state.totalCharsTyped, elapsed);
    const accuracy = calculateAccuracy(
      this.state.totalCharsTyped,
      this.state.totalErrors
    );

    // NOW set inactive
    this.state.active = false;
    document.body.classList.remove("test-active");

    const timeStr = formatTime(elapsed);

    // Save stats
    if (this.snippetInfo.id) {
      saveSnippetStats(this.snippetInfo.id, wpm, accuracy).catch((err) =>
        console.error("Failed to save stats:", err)
      );
    }

    this.updatePauseButton();
    this.showCompletionModal(wpm, accuracy, timeStr);
    this.updateStats();
  }

  /**
   * Show completion modal
   */
  private showCompletionModal(
    wpm: number,
    accuracy: number,
    timeStr: string
  ): void {
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";
    overlay.id = "completionModal";
    overlay.innerHTML = `
      <div class="modal-content p-8 gap-5" style="max-width: 525px">
        <!-- Header -->
        <div>
          <h2 class="text-4xl font-bold">🎉 Test Complete!</h2>
          <p class="text-lg text-gray-400 mt-2">Great job on completing the test</p>
        </div>

        <!-- Stats (Integrated Grid) -->
        <div class="grid grid-cols-3 gap-4 py-3 text-center">
          <div>
            <p class="text-base text-gray-400 uppercase tracking-wider">WPM</p>
            <p class="text-5xl font-bold text-green-400">${wpm}</p>
          </div>
          <div>
            <p class="text-base text-gray-400 uppercase tracking-wider">Accuracy</p>
            <p class="text-5xl font-bold text-green-400">${accuracy}%</p>
          </div>
          <div>
            <p class="text-base text-gray-400 uppercase tracking-wider">Time</p>
            <p class="text-5xl font-bold text-green-400">${timeStr}</p>
          </div>
        </div>

        <!-- Divider -->
        <hr class="border-gray-600" />

        <!-- Buttons (2x2 Grid for equal sizing) -->
        <div class="grid grid-cols-2 gap-4">
          <button id="retryBtn" class="modal-button modal-button-primary text-lg py-4 px-5">
            <span>🔄</span> Retry
          </button>
          <button id="randomBtn" class="modal-button modal-button-primary text-lg py-4 px-5">
            <span>🎲</span> Random
          </button>
          <button id="libraryBtn" class="modal-button modal-button-secondary text-lg py-4 px-5">
            <span>📚</span> Library
          </button>
          <button id="settingsBtn" class="modal-button modal-button-secondary text-lg py-4 px-5">
            <span>⚙️</span> Settings
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    // Add event listeners to modal buttons
    document.getElementById("retryBtn")?.addEventListener("click", () => {
      this.closeModal();
      this.resetTest();
    });

    document.getElementById("randomBtn")?.addEventListener("click", () => {
      this.loadRandomSnippet();
    });

    document.getElementById("libraryBtn")?.addEventListener("click", () => {
      window.location.href = "library.html";
    });

    document.getElementById("settingsBtn")?.addEventListener("click", () => {
      this.closeModal();
    });

    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) this.closeModal();
    });
  }

  /**
   * Close modal
   */
  private closeModal(): void {
    const modal = document.getElementById("completionModal");
    if (modal) modal.remove();
  }

  /**
   * Load random snippet
   */
  private async loadRandomSnippet(): Promise<void> {
    try {
      const response = await fetch("snippets/metadata.json");
      if (!response.ok) throw new Error("Cannot fetch metadata");

      const metadata = await response.json();
      const snippets = metadata.snippets;

      const randomSnippet =
        snippets[Math.floor(Math.random() * snippets.length)];

      window.location.href = `index.html?snippet=${encodeURIComponent(
        randomSnippet.path
      )}`;
    } catch (error) {
      console.error("Error loading random snippet:", error);
      alert("Could not load random snippet. Please try again.");
    }
  }

  /**
   * Update stats display
   */
  private updateStats(): void {
    if (!this.data) return;

    const currentLine = this.data.lines[this.state.currentLineIndex];
    const progress = currentLine
      ? `${this.state.currentCharIndex}/${currentLine.typing_sequence.length}`
      : "0/0";

    let wpm = 0;
    let accuracy = 100;

    // Calculate WPM if test has started (regardless of pause state)
    if (this.state.active && this.state.startTime) {
      const elapsedSeconds = getElapsedTime(this.state);
      wpm = calculateWPM(this.state.totalCharsTyped, elapsedSeconds);
    }

    if (this.state.totalCharsTyped > 0) {
      accuracy = calculateAccuracy(
        this.state.totalCharsTyped,
        this.state.totalErrors
      );
    }

    const preset = (
      document.querySelector(
        'input[name="typingMode"]:checked'
      ) as HTMLInputElement
    )?.value;
    const presetName = PRESETS[preset as keyof typeof PRESETS]?.name || preset;

    const statsEl = document.getElementById("stats");
    if (statsEl) {
      statsEl.innerHTML = `
      <div class="grid grid-cols-6 gap-4 text-sm">
        <div><div class="text-gray-400">Language</div><div class="font-bold">${
          this.data.language
        }</div></div>
        <div><div class="text-gray-400">Mode</div><div class="font-bold">${presetName}</div></div>
        <div><div class="text-gray-400">Line Progress</div><div class="font-bold">${
          this.state.currentLineIndex + 1
        }/${this.data.total_lines}</div></div>
        <div><div class="text-gray-400">Char Progress</div><div class="font-bold">${progress}</div></div>
        <div><div class="text-gray-400">WPM</div><div class="font-bold">${wpm}</div></div>
        <div><div class="text-gray-400">Accuracy</div><div class="font-bold ${
          accuracy < 95 ? "text-yellow-400" : "text-green-400"
        }">${accuracy}%</div></div>
      </div>
    `;
    }
  }

  /**
   * Update status message
   */
  private updateStatus(message: string, type: string = "info"): void {
    const statusEl = document.getElementById("testStatus");
    const colors: Record<string, string> = {
      info: "text-gray-400",
      success: "text-green-400",
      error: "text-red-400",
      warning: "text-yellow-400",
    };
    if (statusEl) {
      statusEl.innerHTML = `<span class="${colors[type]}">${message}</span>`;
    }
  }
}
