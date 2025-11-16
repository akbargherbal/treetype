import { SnippetData, Line, Token } from "../types/snippet";
import { TestState } from "../types/state";

/**
 * Handles rendering of code display
 */
export class CodeRenderer {
  private container: HTMLElement;

  constructor(containerId: string) {
    const element = document.getElementById(containerId);
    if (!element) {
      throw new Error(`Element with id "${containerId}" not found`);
    }
    this.container = element;
  }

  /**
   * Render entire code snippet
   */
  renderCode(data: SnippetData, state: TestState): void {
    this.container.innerHTML = "";

    data.lines.forEach((lineData, lineIndex) => {
      const lineDiv = this.createLineElement(lineData, lineIndex, state);
      this.container.appendChild(lineDiv);
    });
  }

  /**
   * Update only the current line (for performance)
   */
  updateCurrentLine(
    lineData: Line,
    lineIndex: number,
    state: TestState
  ): void {
    const contentDiv = document.getElementById(`line-content-${lineIndex}`);
    if (contentDiv && lineData) {
      contentDiv.innerHTML = "";
      this.renderLineTokens(contentDiv, lineData, lineIndex, state);
    }

    // Update active line indicator
    document.querySelectorAll(".line").forEach((line, idx) => {
      if (idx === lineIndex) {
        line.classList.add("test-active-line");
      } else {
        line.classList.remove("test-active-line");
      }
    });
  }

  /**
   * Create a line element with line number and content
   */
  private createLineElement(
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

  /**
   * Render tokens for a single line with progressive reveal
   */
  private renderLineTokens(
    container: HTMLElement,
    lineData: Line,
    lineIndex: number,
    state: TestState
  ): void {
    let currentCol = 0;
    let typedCharCount = 0;

    const isCurrentLine = lineIndex === state.currentLineIndex;
    const isCompletedLine = state.completedLines.has(lineIndex);
    const isFutureLine = lineIndex > state.currentLineIndex;

    lineData.display_tokens.forEach((token) => {
      // Add spacing before token if needed
      if (token.start_col > currentCol) {
        const spaces = " ".repeat(token.start_col - currentCol);
        container.appendChild(document.createTextNode(spaces));
      }

      const baseCssClass = this.getCssClass(token.type, token.text);

      if (token.typeable) {
        // Render each character of typeable token individually
        for (let i = 0; i < token.text.length; i++) {
          const charSpan = document.createElement("span");
          charSpan.textContent = token.text[i];
          charSpan.className = baseCssClass;

          if (isCompletedLine) {
            // Already typed - show with syntax highlighting
          } else if (isFutureLine) {
            // Not yet reached - show as gray
            charSpan.classList.add("char-untyped");
          } else if (isCurrentLine) {
            if (typedCharCount < state.currentCharIndex) {
              // Already typed on current line - show with syntax highlighting
            } else if (typedCharCount === state.currentCharIndex) {
              // Current character to type
              if (state.errorOnCurrentChar) {
                charSpan.classList.add("char-error");
              } else {
                charSpan.classList.add("char-current");
              }
              charSpan.classList.add("char-untyped");
              charSpan.id = "current-char";
            } else {
              // Future character on current line
              charSpan.classList.add("char-untyped");
            }
          }

          container.appendChild(charSpan);
          typedCharCount++;
        }
      } else {
        // Non-typeable token - render as single span
        const tokenSpan = document.createElement("span");
        tokenSpan.textContent = token.text;
        tokenSpan.className = baseCssClass;

        if (isCompletedLine) {
          // Already typed - show with syntax highlighting
        } else if (isFutureLine) {
          // Not yet reached - show as gray
          tokenSpan.classList.add("char-untyped");
        } else if (isCurrentLine) {
          const currentCharInfo =
            lineData.char_map[String(state.currentCharIndex)];
          const currentDisplayCol = currentCharInfo?.display_col || 0;

          const tokenStartsAfterCursor = token.start_col > currentDisplayCol;

          if (tokenStartsAfterCursor) {
            tokenSpan.classList.add("char-untyped");
          }
        }

        container.appendChild(tokenSpan);
      }

      currentCol = token.end_col;
    });
  }

  /**
   * Get CSS class for token type
   */
  private getCssClass(type: string, text: string): string {
    if (["(", ")", "[", "]", "{", "}", "<", ">"].includes(type)) {
      return "bracket";
    }

    const keywords = [
      "def",
      "function",
      "class",
      "return",
      "if",
      "elif",
      "else",
      "for",
      "while",
      "import",
      "from",
      "as",
      "const",
      "let",
      "var",
      "async",
      "await",
      "interface",
      "type",
      "export",
      "default",
    ];

    if (keywords.includes(type)) return type;
    if (type.includes("comment")) return "comment";
    if (type.includes("string")) return type.replace(/_/g, "_");
    if (type === "integer" || type === "number" || type === "float") {
      return "number";
    }
    if (type.includes("identifier")) return type;
    if (["->", "=>", "=", "+", "-", "*", "/", "%", "++", "--"].includes(type)) {
      return "operator";
    }
    if ([":", ";", ",", "."].includes(type)) return "punctuation";

    return type.replace(/[^a-zA-Z0-9_]/g, "_");
  }
}