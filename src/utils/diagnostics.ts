import { Token, Line, SnippetData } from "../types/snippet.js";
import { TypingMode } from "../types/config.js";

/**
 * Diagnostic information for a token
 */
export interface TokenDiagnostic {
  index: number;
  text: string;
  displayText: string; // Visual representation
  type: string;
  categories: string[];
  typeable: boolean;
  base_typeable: boolean;
  start_col: number;
  end_col: number;
}

/**
 * Diagnostic report for a line
 */
export interface LineDiagnostic {
  lineNumber: number;
  originalSequence: string;
  typeableTokens: TokenDiagnostic[];
  nonTypeableTokens: TokenDiagnostic[];
  whitespaceSummary: {
    total: number;
    typeable: number;
    nonTypeable: number;
  };
}

/**
 * Comparison report between languages
 */
export interface ComparisonReport {
  language: string;
  totalTokens: number;
  typeableTokens: number;
  whitespaceTokens: number;
  typeableWhitespace: number;
  sampleTokens: TokenDiagnostic[];
}

/**
 * Log detailed token diagnostics for a line
 */
export function logTokenDiagnostics(
  line: Line,
  language: string,
  mode: TypingMode
): LineDiagnostic {
  console.group(`🔍 Token Diagnostics: Line ${line.line_number} (${language}, ${mode} mode)`);

  const typeableTokens: TokenDiagnostic[] = [];
  const nonTypeableTokens: TokenDiagnostic[] = [];
  let whitespaceCount = { total: 0, typeable: 0, nonTypeable: 0 };

  line.display_tokens.forEach((token, idx) => {
    const diagnostic: TokenDiagnostic = {
      index: idx,
      text: token.text,
      displayText: visualizeWhitespace(token.text),
      type: token.type,
      categories: token.categories || [],
      typeable: token.typeable,
      base_typeable: token.base_typeable,
      start_col: token.start_col,
      end_col: token.end_col,
    };

    if (token.typeable) {
      typeableTokens.push(diagnostic);
    } else {
      nonTypeableTokens.push(diagnostic);
    }

    // Track whitespace
    if (isWhitespace(token.text)) {
      whitespaceCount.total++;
      if (token.typeable) {
        whitespaceCount.typeable++;
        console.warn(`⚠️  WHITESPACE IS TYPEABLE!`, diagnostic);
      } else {
        whitespaceCount.nonTypeable++;
      }
    }
  });

  console.log(`📊 Summary:`);
  console.log(`  Total tokens: ${line.display_tokens.length}`);
  console.log(`  Typeable: ${typeableTokens.length}`);
  console.log(`  Non-typeable: ${nonTypeableTokens.length}`);
  console.log(`  Whitespace: ${whitespaceCount.total} (${whitespaceCount.typeable} typeable, ${whitespaceCount.nonTypeable} non-typeable)`);
  console.log(`  Typing sequence: "${line.typing_sequence}"`);

  if (typeableTokens.length > 0) {
    console.log(`\n✅ Typeable tokens:`);
    console.table(typeableTokens);
  }

  if (nonTypeableTokens.length > 0) {
    console.log(`\n❌ Non-typeable tokens:`);
    console.table(nonTypeableTokens);
  }

  console.groupEnd();

  return {
    lineNumber: line.line_number,
    originalSequence: line.typing_sequence,
    typeableTokens,
    nonTypeableTokens,
    whitespaceSummary: whitespaceCount,
  };
}

/**
 * Compare token categorization between languages
 */
export function compareLanguages(
  snippets: { language: string; data: SnippetData }[]
): ComparisonReport[] {
  console.group(`🔬 Language Comparison Analysis`);

  const reports = snippets.map(({ language, data }) => {
    const allTokens = data.lines.flatMap((line) => line.display_tokens);
    const typeableTokens = allTokens.filter((t) => t.typeable);
    const whitespaceTokens = allTokens.filter((t) => isWhitespace(t.text));
    const typeableWhitespace = whitespaceTokens.filter((t) => t.typeable);

    // Get sample typeable tokens for inspection
    const sampleTokens: TokenDiagnostic[] = typeableTokens
      .slice(0, 10)
      .map((token, idx) => ({
        index: idx,
        text: token.text,
        displayText: visualizeWhitespace(token.text),
        type: token.type,
        categories: token.categories || [],
        typeable: token.typeable,
        base_typeable: token.base_typeable,
        start_col: token.start_col,
        end_col: token.end_col,
      }));

    return {
      language,
      totalTokens: allTokens.length,
      typeableTokens: typeableTokens.length,
      whitespaceTokens: whitespaceTokens.length,
      typeableWhitespace: typeableWhitespace.length,
      sampleTokens,
    };
  });

  console.log(`📊 Summary by Language:`);
  console.table(
    reports.map((r) => ({
      Language: r.language,
      "Total Tokens": r.totalTokens,
      "Typeable Tokens": r.typeableTokens,
      "Whitespace Tokens": r.whitespaceTokens,
      "⚠️ Typeable Whitespace": r.typeableWhitespace,
    }))
  );

  // Flag inconsistencies
  const typeableWhitespaceCounts = reports.map((r) => r.typeableWhitespace);
  const hasInconsistency = new Set(typeableWhitespaceCounts).size > 1;

  if (hasInconsistency) {
    console.warn(`\n⚠️  INCONSISTENCY DETECTED!`);
    console.warn(`Different languages have different counts of typeable whitespace:`);
    reports.forEach((r) => {
      if (r.typeableWhitespace > 0) {
        console.warn(
          `  ${r.language}: ${r.typeableWhitespace} typeable whitespace tokens`
        );
      }
    });
  } else {
    console.log(`\n✅ All languages consistent: ${typeableWhitespaceCounts[0]} typeable whitespace tokens`);
  }

  console.groupEnd();

  return reports;
}

/**
 * Find specific problem tokens across a snippet
 */
export function findProblemTokens(data: SnippetData): {
  typeableWhitespace: { line: number; token: Token; index: number }[];
  ambiguousCategories: { line: number; token: Token; index: number }[];
} {
  const typeableWhitespace: { line: number; token: Token; index: number }[] = [];
  const ambiguousCategories: { line: number; token: Token; index: number }[] = [];

  data.lines.forEach((line) => {
    line.display_tokens.forEach((token, idx) => {
      // Check for typeable whitespace (BUG!)
      if (isWhitespace(token.text) && token.typeable) {
        typeableWhitespace.push({
          line: line.line_number,
          token,
          index: idx,
        });
      }

      // Check for tokens with no categories (might be problem)
      if (
        token.typeable &&
        (!token.categories || token.categories.length === 0)
      ) {
        ambiguousCategories.push({
          line: line.line_number,
          token,
          index: idx,
        });
      }
    });
  });

  console.group(`🐛 Problem Token Report: ${data.language}`);

  if (typeableWhitespace.length > 0) {
    console.error(`❌ Found ${typeableWhitespace.length} TYPEABLE WHITESPACE tokens (BUG!):`);
    console.table(
      typeableWhitespace.map((item) => ({
        Line: item.line,
        Index: item.index,
        Text: visualizeWhitespace(item.token.text),
        Type: item.token.type,
        Categories: item.token.categories?.join(", ") || "none",
      }))
    );
  } else {
    console.log(`✅ No typeable whitespace found`);
  }

  if (ambiguousCategories.length > 0) {
    console.warn(`⚠️  Found ${ambiguousCategories.length} tokens with no categories:`);
    console.table(
      ambiguousCategories.slice(0, 20).map((item) => ({
        Line: item.line,
        Index: item.index,
        Text: visualizeWhitespace(item.token.text),
        Type: item.token.type,
      }))
    );
  }

  console.groupEnd();

  return { typeableWhitespace, ambiguousCategories };
}

/**
 * Check if text is whitespace
 */
function isWhitespace(text: string): boolean {
  return text.trim() === "";
}

/**
 * Visualize whitespace characters for debugging
 */
function visualizeWhitespace(text: string): string {
  return text
    .replace(/ /g, "·") // Space -> middle dot
    .replace(/\t/g, "→") // Tab -> arrow
    .replace(/\n/g, "↵"); // Newline -> return symbol
}

/**
 * Export diagnostic data as JSON for analysis
 */
export function exportDiagnostics(
  snippets: { language: string; data: SnippetData }[]
): string {
  const diagnostics = snippets.map(({ language, data }) => {
    const problems = findProblemTokens(data);
    return {
      language,
      totalLines: data.total_lines,
      typeableWhitespaceCount: problems.typeableWhitespace.length,
      typeableWhitespaceLocations: problems.typeableWhitespace.map((p) => ({
        line: p.line,
        token: {
          text: p.token.text,
          type: p.token.type,
          categories: p.token.categories,
        },
      })),
    };
  });

  return JSON.stringify(diagnostics, null, 2);
}