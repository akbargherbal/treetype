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
