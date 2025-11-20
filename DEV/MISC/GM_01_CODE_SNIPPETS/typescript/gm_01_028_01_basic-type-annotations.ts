// PATTERN: Basic Type Annotations

let userName: string = "Alice";
let userAge: number = 30;
let isActiveUser: boolean = true;

console.log(`User: ${userName}, Age: ${userAge}, Active: ${isActiveUser}`);

// PATTERN: Basic Type Annotations

let productIds: number[] = [101, 102, 103, 104];

console.log(`First product ID: ${productIds[0]}`);
productIds.push(105);
console.log(`All product IDs: ${productIds.join(", ")}`);

// PATTERN: Basic Type Annotations

let productNames: Array<string> = ["Laptop", "Mouse", "Keyboard"];

console.log(`First product name: ${productNames[0]}`);
productNames.push("Monitor");
console.log(`All product names: ${productNames.join(", ")}`);

// PATTERN: Basic Type Annotations

let userProfile: { name: string; email: string; isActive: boolean } = {
  name: "Bob",
  email: "bob@example.com",
  isActive: false
};

console.log(`User Name: ${userProfile.name}, Email: ${userProfile.email}`);
userProfile.isActive = true;
console.log(`Is user active? ${userProfile.isActive}`);

// PATTERN: Basic Type Annotations

function greetUser(name: string, age: number): string {
  return `Hello, ${name}! You are ${age} years old.`;
}

let greetingMessage = greetUser("Charlie", 25);
console.log(greetingMessage);

// PATTERN: Basic Type Annotations

function calculateArea(width: number, height: number): number {
  return width * height;
}

let roomWidth = 10;
let roomHeight = 5;
let area = calculateArea(roomWidth, roomHeight);
console.log(`The area of the room is: ${area} square units.`);

// PATTERN: Basic Type Annotations

function logMessage(message: string): void {
  console.log(`LOG: ${message}`);
}

logMessage("Operation completed successfully.");
// The function does not return a value that can be used.
let result = logMessage("Another message."); // result will be 'void' (undefined)
console.log(result);

// PATTERN: Basic Type Annotations

let data: any = "hello world";
console.log(data.toUpperCase());

data = 123;
console.log(data * 2);

data = { name: "Any Object" };
console.log(data.name);

// PATTERN: Basic Type Annotations

let unknownValue: unknown = "this is a string";

if (typeof unknownValue === 'string') {
  console.log(unknownValue.toUpperCase());
}

unknownValue = 42;
if (typeof unknownValue === 'number') {
  console.log(unknownValue * 2);
}

// PATTERN: Basic Type Annotations

function throwFatalError(message: string): never {
  throw new Error(message);
}

function infiniteLoop(): never {
  while (true) {
    // This function never returns
  }
}

try {
  throwFatalError("Application crashed unexpectedly!");
} catch (e: any) {
  console.error(`Caught error: ${e.message}`);
}