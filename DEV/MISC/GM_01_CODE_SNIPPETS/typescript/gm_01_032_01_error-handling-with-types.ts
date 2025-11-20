// PATTERN: Error Handling with Types

function processUserInput(input: string): string {
  try {
    if (input.length === 0) {
      throw new Error("Input cannot be empty.");
    }
    if (input === "invalid") {
      throw new TypeError("Invalid input format.");
    }
    return `Processed: ${input.toUpperCase()}`;
  } catch (error: unknown) {
    if (error instanceof TypeError) {
      console.error("Format error:", error.message);
      return "Error: Please check input format.";
    } else if (error instanceof Error) {
      console.error("General error:", error.message);
      return "Error: Processing failed.";
    } else {
      console.error("An unexpected error occurred.");
      return "Error: Unknown failure.";
    }
  }
}

// PATTERN: Error Handling with Types

class NetworkError extends Error {
  constructor(message: string, public statusCode: number) {
    super(message);
    this.name = 'NetworkError';
    Object.setPrototypeOf(this, NetworkError.prototype);
  }
}

function fetchData(url: string): string {
  if (url === "http://bad.com") {
    throw new NetworkError("Failed to connect to host.", 500);
  }
  if (url === "http://unauthorized.com") {
    throw new NetworkError("Authentication required.", 401);
  }
  return `Data from ${url}`;
}

try {
  console.log(fetchData("http://good.com"));
  console.log(fetchData("http://bad.com"));
} catch (error: unknown) {
  if (error instanceof NetworkError) {
    console.error(`Network Error (${error.statusCode}): ${error.message}`);
  } else if (error instanceof Error) {
    console.error(`Generic Error: ${error.message}`);
  }
}

// PATTERN: Error Handling with Types

type Result<T, E> = { success: true; value: T } | { success: false; error: E };

function Ok<T>(value: T): Result<T, never> {
  return { success: true, value };
}

function Err<E>(error: E): Result<never, E> {
  return { success: false, error };
}

function parseNumber(input: string): Result<number, string> {
  const num = parseInt(input, 10);
  if (isNaN(num)) {
    return Err("Invalid number format.");
  }
  return Ok(num);
}

const parsed1 = parseNumber("123");
if (parsed1.success) {
  console.log("Parsed number:", parsed1.value);
} else {
  console.error("Parsing failed:", parsed1.error);
}

const parsed2 = parseNumber("abc");
if (parsed2.success) {
  console.log("Parsed number:", parsed2.value);
} else {
  console.error("Parsing failed:", parsed2.error);
}

// PATTERN: Error Handling with Types

function executeTask(shouldFail: boolean): string {
  try {
    if (shouldFail) {
      // Simulate different types of errors, including non-Error objects
      if (Math.random() > 0.5) {
        throw new Error("A critical task error occurred.");
      } else {
        throw "Task failed due to an unexpected condition."; // A string error
      }
    }
    return "Task completed successfully.";
  } catch (error: unknown) {
    if (error instanceof Error) {
      console.error("Caught an Error object:", error.message);
      return `Task failed: ${error.message}`;
    } else if (typeof error === 'string') {
      console.error("Caught a string error:", error);
      return `Task failed: ${error}`;
    } else {
      console.error("Caught an unknown type of error:", error);
      return "Task failed: An unexpected error type occurred.";
    }
  }
}