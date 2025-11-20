// PATTERN: Function Patterns

type MathOperation = (a: number, b: number) => number;

const add: MathOperation = (x, y) => x + y;
const subtract: MathOperation = (x, y) => x - y;

console.log(add(5, 3));
console.log(subtract(10, 4));

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

logMessage("User logged in.");
logMessage("Failed to connect to database.", "error");
logMessage("Invalid input received.", "warn");

// PATTERN: Function Patterns

function sumAllNumbers(...numbers: number[]): number {
  return numbers.reduce((total, num) => total + num, 0);
}

console.log(sumAllNumbers(1, 2, 3));
console.log(sumAllNumbers(10, 20, 30, 40, 50));

// PATTERN: Function Patterns

function formatValue(value: string): string;
function formatValue(value: number, currency?: string): string;
function formatValue(value: string | number, currency?: string): string {
  if (typeof value === 'string') {
    return value.toUpperCase();
  } else {
    return `${currency || '$'}${value.toFixed(2)}`;
  }
}

console.log(formatValue("hello world"));
console.log(formatValue(123.456, "€"));
console.log(formatValue(99.99));

// PATTERN: Function Patterns

const calculateArea = (width: number, height: number): number => {
  return width * height;
};

const greet = (name: string): string => `Hello, ${name}!`;

console.log(calculateArea(10, 5));
console.log(greet("TypeScript"));

// PATTERN: Function Patterns

type DataProcessor = (data: string) => void;

function fetchData(url: string, callback: DataProcessor): void {
  // Simulate fetching data
  setTimeout(() => {
    const fetchedData = `Data from ${url}`;
    callback(fetchedData);
  }, 1000);
}

const processResult: DataProcessor = (result) => {
  console.log("Processing:", result);
};

fetchData("https://api.example.com/data", processResult);

// PATTERN: Function Patterns

function simulateApiCall(id: number): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve(`Data for item ${id}`);
      } else {
        reject(new Error("Invalid ID provided."));
      }
    }, 500);
  });
}

simulateApiCall(123)
  .then(data => console.log(data))
  .catch(error => console.error(error.message));

// PATTERN: Function Patterns

async function fetchUserData(userId: number): Promise<{ id: number; name: string }> {
  // Simulate network request delay
  await new Promise(resolve => setTimeout(resolve, 700));
  
  if (userId <= 0) {
    throw new Error("Invalid user ID.");
  }
  
  return { id: userId, name: `User ${userId}` };
}

async function displayUser(id: number) {
  try {
    const user = await fetchUserData(id);
    console.log(`User found: ${user.name} (ID: ${user.id})`);
  } catch (error: any) {
    console.error("Error fetching user:", error.message);
  }
}

displayUser(42);
displayUser(-1);