import { PresetsConfig, UserConfig, TypingMode } from "../types/config";
import { Line, Token } from "../types/snippet";

/**
 * Preset configurations for typing modes
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
 * Helper function to detect if a token is a JSX tag name
 * Handles both simple tags (<div>) and tags with attributes (<button onClick={...}>)
 */
function isJSXTagName(
  token: Token,
  idx: number,
  tokens: Token[]
): boolean {
  // Must be an identifier-like token
  if (token.type !== "identifier" && token.type !== "type_identifier") {
    return false;
  }

  const prevToken = idx > 0 ? tokens[idx - 1] : null;

  // Must follow < or </
  if (!prevToken || (prevToken.text !== "<" && prevToken.text !== "</")) {
    return false;
  }

  // Look ahead to find the closing > or />
  // Skip over attributes, whitespace, etc.
  for (let i = idx + 1; i < tokens.length; i++) {
    const nextToken = tokens[i];
    
    // Found the closing bracket - this is a JSX tag name
    if (nextToken.text === ">" || nextToken.text === "/>") {
      return true;
    }

    // If we hit another opening bracket or a different structural element,
    // this is probably not a JSX tag
    if (nextToken.text === "<" || nextToken.text === "{") {
      return false;
    }
  }

  return false;
}

/**
 * Apply exclusion config to line data
 *
 * CRITICAL FIXES INCLUDED:
 * 1. Whitespace is NEVER typeable
 * 2. JSX tag names follow angle_bracket exclusion rules (handles attributes)
 * 3. includeSpecific has highest priority
 */
export function applyExclusionConfig(lineData: Line, preset: TypingMode): Line {
  const config = PRESETS[preset];

  const filteredTokens: Token[] = lineData.display_tokens.map((token, idx) => {
    let typeable = token.base_typeable;

    // CRITICAL FIX #1: Whitespace is NEVER typeable
    if (token.text.trim() === "") {
      return { ...token, typeable: false };
    }

    // If token is not base_typeable, keep it that way
    if (!typeable) {
      return { ...token, typeable };
    }

    // CRITICAL FIX #2: JSX tag names follow angle_bracket exclusion rules
    if (isJSXTagName(token, idx, lineData.display_tokens)) {
      // This is a JSX tag name - apply angle_bracket exclusion rules
      if (config.exclude.includes("angle_bracket")) {
        return { ...token, typeable: false };
      }
    }

    // CRITICAL FIX #3: Check includeSpecific FIRST (highest priority)
    if (config.includeSpecific?.includes(token.text)) {
      return { ...token, typeable: true };
    }

    // If no categories, default to typeable (keywords, identifiers)
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