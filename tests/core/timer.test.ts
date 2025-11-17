import { describe, test, expect, vi } from "vitest";
import {
  getElapsedTime,
  calculateWPM,
  calculateAccuracy,
  formatTime,
} from "../../src/core/timer";
import { TestState } from "../../src/types/state";

// Helper to create a default test state
const createDefaultState = (): TestState => ({
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
});

describe("Timer Functions", () => {
  describe("getElapsedTime", () => {
    test("returns 0 when test not active", () => {
      const state = createDefaultState();
      expect(getElapsedTime(state)).toBe(0);
    });

    test("calculates elapsed time correctly", () => {
      const state = { ...createDefaultState(), active: true, startTime: Date.now() - 60000 }; // 60s ago
      const elapsed = getElapsedTime(state);
      expect(elapsed).toBeCloseTo(60, 0);
    });

    test("excludes pause time from elapsed time", () => {
      const state = { ...createDefaultState(), active: true, startTime: Date.now() - 90000, totalPausedTime: 30000 };
      const elapsed = getElapsedTime(state);
      expect(elapsed).toBeCloseTo(60, 0); // 90s total - 30s paused = 60s
    });

    test("excludes current pause duration when paused", () => {
        const now = Date.now();
        vi.spyOn(Date, 'now').mockReturnValue(now); // Freeze time
        const state = { ...createDefaultState(), active: true, paused: true, startTime: now - 90000, pauseStartTime: now - 10000, totalPausedTime: 30000 };
        const elapsed = getElapsedTime(state);
        expect(elapsed).toBeCloseTo(50, 0); // 90 - 30 (previous) - 10 (current) = 50
        vi.spyOn(Date, 'now').mockRestore(); // Unfreeze time
    });
  });

  describe("calculateWPM", () => {
    test("calculates WPM correctly", () => {
      expect(calculateWPM(300, 60)).toBe(60); // 300 chars / 5 / 1 min
    });

    test("returns 0 for zero or negative elapsed time", () => {
      expect(calculateWPM(100, 0)).toBe(0);
      expect(calculateWPM(100, -10)).toBe(0);
    });
  });

  describe("calculateAccuracy", () => {
    test("calculates accuracy correctly", () => {
      expect(calculateAccuracy(100, 5)).toBe(95);
      expect(calculateAccuracy(100, 0)).toBe(100);
    });

    test("returns 100% for zero total chars", () => {
      expect(calculateAccuracy(0, 5)).toBe(100);
    });
  });

  describe("formatTime", () => {
    test("formats time correctly", () => {
      expect(formatTime(0)).toBe("0:00");
      expect(formatTime(5)).toBe("0:05");
      expect(formatTime(65)).toBe("1:05");
      expect(formatTime(125)).toBe("2:05");
    });
  });
});