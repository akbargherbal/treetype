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
 * FIXED: Now properly handles whitespace in all contexts
 */
export function applyExclusionConfig(lineData: Line, preset: TypingMode): Line {
  const config = PRESETS[preset];

  const filteredTokens: Token[] = lineData.display_tokens.map((token) => {
    let typeable = token.base_typeable;

    // CRITICAL FIX #1: Whitespace is NEVER typeable, regardless of context
    if (token.text.trim() === "") {
      return { ...token, typeable: false };
    }

    // If token is not base_typeable, keep it that way
    if (!typeable) {
      return { ...token, typeable };
    }

    // CRITICAL FIX #2: Check includeSpecific FIRST (highest priority)
    if (config.includeSpecific?.includes(token.text)) {
      return { ...token, typeable: true };
    }

    // If no categories, default to typeable (unless excluded above)
    if (!token.categories || token.categories.length === 0) {
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

  // Regenerate typing sequence from typeable tokens only
  const typingSequence = filteredTokens
    .filter((t) => t.typeable)
    .map((t) => t.text)
    .join("");

  // Regenerate char_map
  const charMap: Line["char_map"] = {};
  let charIdx = 0;

  filteredTokens.forEach((token, tokenIdx) => {
    if (token.typeable) {
      for (let i = 0; i < token.text.length; i++) {
        charMap[String(charIdx)] = {
          token_idx: tokenIdx,
          display_col: token.start_col,
        };
        charIdx++;
      }
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
