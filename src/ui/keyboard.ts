import { TestState, SnippetInfo } from "../types/state";
import { SnippetData } from "../types/snippet";

/**
 * Callback types for keyboard events
 */
export interface KeyboardCallbacks {
  onTestStart: () => void;
  onCharacterTyped: (correct: boolean) => void;
  onLineComplete: () => void;
  onTestComplete: () => void;
  onPauseToggle: () => void;
  onReset: () => void;
}

/**
 * Handles keyboard input during typing test
 */
export class KeyboardHandler {
  private state: TestState;
  private data: SnippetData;
  private snippetInfo: SnippetInfo;
  private callbacks: KeyboardCallbacks;

  constructor(
    state: TestState,
    data: SnippetData,
    snippetInfo: SnippetInfo,
    callbacks: KeyboardCallbacks
  ) {
    this.state = state;
    this.data = data;
    this.snippetInfo = snippetInfo;
    this.callbacks = callbacks;
  }

  /**
   * Update state and data references
   */
  updateReferences(state: TestState, data: SnippetData): void {
    this.state = state;
    this.data = data;
  }

  /**
   * Handle keyboard events
   */
  handleKeyPress(event: KeyboardEvent): void {
    // Tab key for pause/resume
    if (event.key === "Tab" && this.state.active) {
      event.preventDefault();
      this.callbacks.onPauseToggle();
      return;
    }

    // Block input during pause (except Esc)
    if (this.state.paused) {
      if (event.key === "Escape") {
        event.preventDefault();
        this.callbacks.onReset();
      }
      return;
    }

    // Ignore modifier key combinations
    if (event.ctrlKey || event.metaKey || event.altKey) return;

    // Escape key to reset
    if (event.key === "Escape") {
      event.preventDefault();
      this.callbacks.onReset();
      return;
    }

    // Ignore special keys (except Enter and Space)
    if (event.key.length > 1 && event.key !== "Enter" && event.key !== " ") {
      return;
    }

    event.preventDefault();

    if (!this.data) return;

    // Start test on first keypress
    if (!this.state.active) {
      this.callbacks.onTestStart();
    }

    const currentLine = this.data.lines[this.state.currentLineIndex];
    if (!currentLine) return;

    const expectedChar =
      currentLine.typing_sequence[this.state.currentCharIndex];
    const typedKey = event.key;

    if (typedKey === expectedChar) {
      // Correct character
      this.state.currentCharIndex++;
      this.state.totalCharsTyped++;
      this.state.errorOnCurrentChar = false;

      this.callbacks.onCharacterTyped(true);

      // Check if line is complete
      if (
        this.state.currentCharIndex >= currentLine.typing_sequence.length
      ) {
        setTimeout(() => {
          this.callbacks.onLineComplete();
        }, 50);
      }
    } else {
      // Incorrect character
      this.state.totalErrors++;
      this.state.errorOnCurrentChar = true;

      this.callbacks.onCharacterTyped(false);
    }
  }

  /**
   * Move to next typeable line
   * @returns true if moved to next line, false if test complete
   */
  moveToNextLine(): boolean {
    this.state.completedLines.add(this.state.currentLineIndex);
    this.state.currentLineIndex++;
    this.state.currentCharIndex = 0;
    this.state.errorOnCurrentChar = false;

    // Skip empty lines
    while (this.state.currentLineIndex < this.data.total_lines) {
      const nextLine = this.data.lines[this.state.currentLineIndex];
      if (
        nextLine &&
        nextLine.typing_sequence &&
        nextLine.typing_sequence.length > 0
      ) {
        break;
      }
      this.state.completedLines.add(this.state.currentLineIndex);
      this.state.currentLineIndex++;
    }

    // Check if test is complete
    if (this.state.currentLineIndex >= this.data.total_lines) {
      this.callbacks.onTestComplete();
      return false;
    }

    return true;
  }
}