// PATTERN: Function Patterns

type MathOperation = (a: number, b: number) => number;

const add: MathOperation = (x, y) => x + y;
const subtract: MathOperation = (x, y) => x - y;

console.log(add(10, 5));
console.log(subtract(10, 5));

// PATTERN: Function Patterns

function greetUser(name: string, greeting?: string): string {
  if (greeting) {
    return `${greeting}, ${name}!`;
  }
  return `Hello, ${name}!`;
}

console.log(greetUser("Alice"));
console.log(greetUser("Bob", "Good morning"));

// PATTERN: Function Patterns

function logMessage(message: string, level: "info" | "warn" | "error" = "info"): void {
  console.log(`[${level.toUpperCase()}] ${message}`);
}

logMessage("User logged in");
logMessage("Failed to connect to database", "error");
logMessage("Configuration missing", "warn");

// PATTERN: Function Patterns

function sumNumbers(...numbers: number[]): number {
  return numbers.reduce((total, num) => total + num, 0);
}

console.log(sumNumbers(1, 2, 3));
console.log(sumNumbers(10, 20, 30, 40, 50));
console.log(sumNumbers());

// PATTERN: Function Patterns

function formatValue(value: string): string;
function formatValue(value: number, currency?: string): string;
function formatValue(value: string | number, currency?: string): string {
  if (typeof value === 'string') {
    return value.toUpperCase();
  }
  return currency ? `${currency} ${value.toFixed(2)}` : value.toString();
}

console.log(formatValue("hello world"));
console.log(formatValue(123.456));
console.log(formatValue(99.99, "$"));

// PATTERN: Function Patterns

type User = { id: number; name: string };

const createUser = (id: number, name: string): User => {
  return { id, name };
};

const displayUser = (user: User): void => {
  console.log(`User ID: ${user.id}, Name: ${user.name}`);
};

const newUser = createUser(1, "Jane Doe");
displayUser(newUser);

// PATTERN: Function Patterns

type DataProcessor = (data: string) => string;

function processData(input: string, processor: DataProcessor): string {
  console.log("Processing data...");
  return processor(input);
}

const toUpperCaseProcessor: DataProcessor = (text) => text.toUpperCase();
const addPrefixProcessor: DataProcessor = (text) => `Processed: ${text}`;

console.log(processData("hello", toUpperCaseProcessor));
console.log(processData("world", addPrefixProcessor));

// PATTERN: Function Patterns

function fetchData(url: string): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (url.startsWith("http")) {
        resolve(`Data from ${url}`);
      } else {
        reject(new Error("Invalid URL"));
      }
    }, 1000);
  });
}

fetchData("http://api.example.com/data")
  .then(data => console.log(data))
  .catch(error => console.error(error.message));

// PATTERN: Function Patterns

async function fetchUserData(userId: number): Promise<{ id: number; name: string }> {
  const response = await new Promise<{ id: number; name: string }>(resolve => {
    setTimeout(() => resolve({ id: userId, name: `User ${userId}` }), 500);
  });
  return response;
}

async function displayUserDetail(id: number) {
  try {
    const user = await fetchUserData(id);
    console.log(`Fetched user: ${user.name}`);
  } catch (error) {
    console.error("Error fetching user:", error);
  }
}

displayUserDetail(123);