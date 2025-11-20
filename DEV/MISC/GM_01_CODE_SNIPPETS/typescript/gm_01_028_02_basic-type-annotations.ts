// PATTERN: Basic Type Annotations

let userName: string = "Alice";
let userAge: number = 30;
let isActiveUser: boolean = true;

console.log(`User: ${userName}, Age: ${userAge}, Active: ${isActiveUser}`);

// PATTERN: Basic Type Annotations

let productIds: number[] = [101, 102, 103];
productIds.push(104);

console.log("Product IDs:", productIds);

// PATTERN: Basic Type Annotations

let productNames: Array<string> = ["Laptop", "Mouse", "Keyboard"];
productNames.push("Monitor");

console.log("Product Names:", productNames);

// PATTERN: Basic Type Annotations

let userProfile: { name: string; age: number; email?: string } = {
  name: "Bob",
  age: 25,
  email: "bob@example.com"
};

console.log(`User: ${userProfile.name}, Age: ${userProfile.age}`);

// PATTERN: Basic Type Annotations

function greetUser(name: string, greeting: string): void {
  console.log(`${greeting}, ${name}!`);
}

greetUser("Charlie", "Hello");

// PATTERN: Basic Type Annotations

function calculateArea(width: number, height: number): number {
  return width * height;
}

let area = calculateArea(10, 5);
console.log(`Calculated Area: ${area}`);

// PATTERN: Basic Type Annotations

function logMessage(message: string): void {
  console.log(`LOG: ${message}`);
}

logMessage("Application started successfully.");

// PATTERN: Basic Type Annotations

let dynamicData: any = "This is a string";
console.log(dynamicData.length);

dynamicData = 123;
console.log(dynamicData.toFixed(2)); // No compile-time error

// PATTERN: Basic Type Annotations

let unknownValue: unknown = "hello world";

if (typeof unknownValue === "string") {
  console.log(unknownValue.toUpperCase());
} else if (typeof unknownValue === "number") {
  console.log(unknownValue.toFixed(2));
}

// PATTERN: Basic Type Annotations

function throwError(message: string): never {
  throw new Error(message);
}

try {
  throwError("Critical failure occurred!");
} catch (e: any) {
  console.error(`Caught error: ${e.message}`);
}