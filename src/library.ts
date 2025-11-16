import { SnippetMetadata } from "./types/snippet.js";
import { SnippetStats } from "./types/state.js";
import { loadSnippetStats } from "./core/storage.js";

/**
 * Library page for browsing and selecting code snippets
 */
export class LibraryPage {
  private allSnippets: SnippetMetadata[] = [];
  private userStats: Record<string, SnippetStats> = {};
  private currentFilter: string = "all";
  private currentSearch: string = "";
  private currentSort: string = "name";

  constructor() {
    this.initialize();
  }

  /**
   * Initialize the library page
   */
  private async initialize(): Promise<void> {
    this.setupEventListeners();
    await this.loadMetadata();
  }

  /**
   * Load snippet metadata from JSON file
   */
  private async loadMetadata(): Promise<void> {
    try {
      const response = await fetch("snippets/metadata.json");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      this.allSnippets = data.snippets;

      // Load user statistics
      this.userStats = loadSnippetStats();

      // Render everything
      this.renderSummaryStats();
      this.renderSnippets();

      // Hide loading, show grid
      document.getElementById("loadingState")?.classList.add("hidden");
      document.getElementById("snippetGrid")?.classList.remove("hidden");
    } catch (error) {
      console.error("Error loading metadata:", error);
      const loadingEl = document.getElementById("loadingState");
      if (loadingEl) {
        loadingEl.innerHTML = `
          <div class="text-center text-red-400">
            <div class="text-4xl mb-4">⚠️</div>
            <h3 class="text-xl font-bold mb-2">Failed to load snippets</h3>
            <p>Error: ${error instanceof Error ? error.message : String(error)}</p>
            <p class="mt-2 text-sm">Make sure you're running from the project root directory</p>
          </div>
        `;
      }
    }
  }

  /**
   * Calculate and render summary statistics
   */
  private renderSummaryStats(): void {
    const statsEntries = Object.values(this.userStats);

    // Total snippets
    const totalEl = document.getElementById("totalSnippets");
    if (totalEl) totalEl.textContent = String(this.allSnippets.length);

    // Practiced count
    const practicedEl = document.getElementById("practicedCount");
    if (practicedEl) practicedEl.textContent = String(statsEntries.length);

    // Average and best WPM
    if (statsEntries.length > 0) {
      const avgWPM =
        statsEntries.reduce((sum, s) => sum + (s.bestWPM || 0), 0) /
        statsEntries.length;
      const maxWPM = Math.max(...statsEntries.map((s) => s.bestWPM || 0));

      const avgEl = document.getElementById("averageWPM");
      if (avgEl) avgEl.textContent = String(Math.round(avgWPM));

      const bestEl = document.getElementById("bestWPM");
      if (bestEl) bestEl.textContent = String(maxWPM);
    } else {
      const avgEl = document.getElementById("averageWPM");
      if (avgEl) avgEl.textContent = "0";

      const bestEl = document.getElementById("bestWPM");
      if (bestEl) bestEl.textContent = "0";
    }
  }

  /**
   * Filter and sort snippets based on current settings
   */
  private filterAndSortSnippets(): SnippetMetadata[] {
    let filtered = [...this.allSnippets];

    // Language filter
    if (this.currentFilter !== "all") {
      filtered = filtered.filter((s) => s.language === this.currentFilter);
    }

    // Search filter
    if (this.currentSearch) {
      const searchLower = this.currentSearch.toLowerCase();
      filtered = filtered.filter((s) =>
        s.name.toLowerCase().includes(searchLower)
      );
    }

    // Sort
    filtered.sort((a, b) => {
      switch (this.currentSort) {
        case "name":
          return a.name.localeCompare(b.name);
        case "wpm": {
          const aStats = this.userStats[a.id] || {};
          const bStats = this.userStats[b.id] || {};
          return (bStats.bestWPM || 0) - (aStats.bestWPM || 0);
        }
        case "practiced": {
          const aStats = this.userStats[a.id] || {};
          const bStats = this.userStats[b.id] || {};
          return (bStats.practiceCount || 0) - (aStats.practiceCount || 0);
        }
        case "lines":
          return a.lines - b.lines;
        default:
          return 0;
      }
    });

    return filtered;
  }

  /**
   * Render snippet cards in the grid
   */
  private renderSnippets(): void {
    const filtered = this.filterAndSortSnippets();
    const grid = document.getElementById("snippetGrid");
    const emptyState = document.getElementById("emptyState");

    if (!grid || !emptyState) return;

    if (filtered.length === 0) {
      grid.classList.add("hidden");
      emptyState.classList.remove("hidden");
      return;
    }

    grid.classList.remove("hidden");
    emptyState.classList.add("hidden");

    grid.innerHTML = filtered
      .map((snippet) => this.createSnippetCard(snippet))
      .join("");
  }

  /**
   * Create HTML for a single snippet card
   */
  private createSnippetCard(snippet: SnippetMetadata): string {
    const stats = this.userStats[snippet.id] || {};
    const practiced = (stats.practiceCount || 0) > 0;

    const statsHtml = practiced
      ? `
          <div class="stats-display">
            <div class="flex justify-between text-xs mb-1">
              <span class="text-gray-400">Best WPM:</span>
              <span class="font-bold text-green-400">${stats.bestWPM || 0}</span>
            </div>
            <div class="flex justify-between text-xs">
              <span class="text-gray-400">Practiced:</span>
              <span class="font-bold">${stats.practiceCount}x</span>
            </div>
          </div>
        `
      : `
          <div class="stats-display">
            <div class="text-xs text-gray-500 text-center">Not practiced yet</div>
          </div>
        `;

    const cleanedName = this.cleanName(snippet.name);
    const escapedPath = this.escapeHtml(snippet.path);

    return `
          <div class="snippet-card" onclick="window.libraryPage.practiceSnippet('${escapedPath}')">
            <div class="flex items-start justify-between gap-2">
              <h3 class="font-bold text-lg flex-1 leading-tight">${cleanedName}</h3>
              <span class="language-badge lang-${snippet.language}">${snippet.language}</span>
            </div>
            
            <div class="flex gap-2 items-center text-sm text-gray-400">
              <span>📄 ${snippet.lines} lines</span>
              <span>•</span>
              <span>⌨️ ${snippet.typeable_chars} chars</span>
            </div>

            ${statsHtml}

            <button class="practice-button mt-auto" onclick="window.libraryPage.practiceSnippet('${escapedPath}'); event.stopPropagation();">
              ${practiced ? "Practice Again" : "Start Practice"}
            </button>
          </div>
        `;
  }

  /**
   * Clean snippet name for display
   */
  private cleanName(name: string): string {
    // Remove "Gm 01 ###_## " prefix and replace hyphens with spaces
    return name.replace(/^Gm \d+ \d+_\d+ /, "").replace(/-/g, " ");
  }

  /**
   * Escape HTML special characters
   */
  private escapeHtml(text: string): string {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Navigate to practice page with selected snippet
   */
  public practiceSnippet(path: string): void {
    window.location.href = `index.html?snippet=${encodeURIComponent(path)}`;
  }

  /**
   * Setup event listeners for filters, search, and sort
   */
  private setupEventListeners(): void {
    // Language filter buttons
    document
      .querySelectorAll<HTMLButtonElement>(".filter-button[data-language]")
      .forEach((btn) => {
        btn.addEventListener("click", () => {
          // Remove active class from all
          document
            .querySelectorAll(".filter-button[data-language]")
            .forEach((b) => b.classList.remove("active"));

          // Add active to clicked button
          btn.classList.add("active");

          // Update filter and re-render
          this.currentFilter = btn.dataset.language || "all";
          this.renderSnippets();
        });
      });

    // Search input
    const searchInput = document.getElementById(
      "searchInput"
    ) as HTMLInputElement;
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        this.currentSearch = (e.target as HTMLInputElement).value;
        this.renderSnippets();
      });
    }

    // Sort dropdown
    const sortSelect = document.getElementById(
      "sortSelect"
    ) as HTMLSelectElement;
    if (sortSelect) {
      sortSelect.addEventListener("change", (e) => {
        this.currentSort = (e.target as HTMLSelectElement).value;
        this.renderSnippets();
      });
    }
  }
}

// Declare global type for window.libraryPage
declare global {
  interface Window {
    libraryPage: LibraryPage;
  }
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  window.libraryPage = new LibraryPage();
});