// PATTERN: Error Handling

function processUserData(data) {
  if (!data || typeof data.id !== 'number') {
    throw new Error("Invalid user data provided.");
  }
  return `User ${data.id} processed successfully.`;
}

try {
  const result = processUserData({ id: 123, name: "Alice" });
  console.log(result);
  processUserData(null); // This will throw
} catch (error) {
  console.error("Caught an error:", error.message);
}

// PATTERN: Error Handling

function validateEmail(email) {
  if (!email || !email.includes('@') || !email.includes('.')) {
    throw new Error("Invalid email format.");
  }
  return true;
}

try {
  validateEmail("test@example.com");
  console.log("Email is valid.");
  validateEmail("invalid-email"); // This will throw
} catch (error) {
  console.error("Validation error:", error.message);
}

// PATTERN: Error Handling

class NetworkError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.name = "NetworkError";
    this.statusCode = statusCode;
  }
}

function fetchData(url) {
  if (url.startsWith("http://bad-server.com")) {
    throw new NetworkError("Failed to connect to server.", 500);
  }
  return "Data fetched successfully.";
}

try {
  console.log(fetchData("http://good-server.com/api/data"));
  fetchData("http://bad-server.com/api/data");
} catch (error) {
  if (error instanceof NetworkError) {
    console.error(`Custom Error: ${error.name} - ${error.message} (Status: ${error.statusCode})`);
  } else {
    console.error("An unexpected error occurred:", error.message);
  }
}

// PATTERN: Error Handling

function performCalculation(a, b) {
  if (b === 0) {
    throw new Error("Cannot divide by zero.");
  }
  return a / b;
}

function executeOperation(x, y) {
  return performCalculation(x, y);
}

try {
  executeOperation(10, 0); // This will throw
} catch (error) {
  console.error("Error caught:", error.message);
  console.error("Stack trace:", error.stack);
}