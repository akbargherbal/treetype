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
