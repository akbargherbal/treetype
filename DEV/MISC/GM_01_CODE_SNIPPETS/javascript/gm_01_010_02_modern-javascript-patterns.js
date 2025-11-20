// PATTERN: Modern JavaScript Patterns

// userModule.js (conceptual file)
// export const userName = "Alice";
// export function greetUser(name) { return `Hello, ${name}!`; }

import { userName, greetUser } from './userModule.js';

console.log(userName);
console.log(greetUser("Bob"));

// PATTERN: Modern JavaScript Patterns

// userModule.js (conceptual file)
// const defaultUser = { name: "Alice", age: 30 };
// export default defaultUser;

import currentUser from './userModule.js';

console.log(currentUser.name);
console.log(currentUser.age);

// PATTERN: Modern JavaScript Patterns

// mathModule.js (conceptual file)
// export const PI = 3.14159;
// export function add(a, b) { return a + b; }

import * as math from './mathModule.js';

console.log(math.PI);
console.log(math.add(5, 3));

// PATTERN: Modern JavaScript Patterns

// dataService.js
export const API_KEY = "your_api_key_here";

export function fetchData(endpoint) {
  console.log(`Fetching data from ${endpoint} with key: ${API_KEY}`);
  return { id: 1, data: "example" };
}

// Usage in another file: import { API_KEY, fetchData } from './dataService.js';

// PATTERN: Modern JavaScript Patterns

// userService.js
class User {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Greetings, ${this.name}!`;
  }
}
export default User;

// Usage in another file: import User from './userService.js';
// const newUser = new User("John");
// console.log(newUser.greet());

// PATTERN: Modern JavaScript Patterns

// mathOperations.js (conceptual file)
// export function calculateSum(a, b) { return a + b; }

async function loadAndUseMath() {
  try {
    const { calculateSum } = await import('./mathOperations.js');
    const result = calculateSum(10, 20);
    console.log(`Calculated sum: ${result}`);
  } catch (error) {
    console.error("Error loading math module:", error);
  }
}
loadAndUseMath();

// PATTERN: Modern JavaScript Patterns

const productNames = ["Laptop", "Keyboard", "Mouse", "Monitor"];

for (const product of productNames) {
  console.log(`Processing product: ${product}`);
}

const uniqueIds = new Set([101, 102, 103]);
for (const id of uniqueIds) {
  console.log(`Unique ID: ${id}`);
}

// PATTERN: Modern JavaScript Patterns

const userProfile = {
  firstName: "Alice",
  lastName: "Smith",
  age: 30,
  email: "alice@example.com"
};

for (const key in userProfile) {
  if (Object.prototype.hasOwnProperty.call(userProfile, key)) {
    console.log(`${key}: ${userProfile[key]}`);
  }
}

// PATTERN: Modern JavaScript Patterns

const userName = "Bob";
const userAge = 25;
const propertyPrefix = "user";

const user = {
  userName, // Shorthand property name
  userAge,  // Shorthand property name
  greet() { // Shorthand method name
    return `Hello, ${this.userName}!`;
  },
  [propertyPrefix + 'Id']: 123 // Computed property name
};

console.log(user.greet());
console.log(user.userId);

// PATTERN: Modern JavaScript Patterns

function* idGenerator() {
  let id = 1;
  while (true) {
    yield id++;
  }
}

const generateId = idGenerator();

console.log(generateId.next().value); // 1
console.log(generateId.next().value); // 2
console.log(generateId.next().value); // 3

// PATTERN: Modern JavaScript Patterns

const uniqueActionId = Symbol('actionIdentifier');
const anotherUniqueId = Symbol('actionIdentifier');

const event = {
  name: "UserLogin",
  timestamp: Date.now(),
  [uniqueActionId]: "LOGIN_SUCCESS" // Using Symbol as a unique object key
};

console.log(event[uniqueActionId]);
console.log(uniqueActionId === anotherUniqueId); // Symbols are unique