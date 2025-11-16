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
