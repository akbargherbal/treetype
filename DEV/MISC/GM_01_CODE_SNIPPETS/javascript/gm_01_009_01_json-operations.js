// PATTERN: JSON Operations

const jsonString = '{"productName": "Laptop", "price": 1200, "inStock": true}';
const product = JSON.parse(jsonString);

console.log(product.productName);
console.log(product.price);

// PATTERN: JSON Operations

const userData = {
  id: "user123",
  name: "Jane Doe",
  email: "jane.doe@example.com"
};

const jsonUserData = JSON.stringify(userData);

console.log(jsonUserData);

// PATTERN: JSON Operations

const config = {
  appName: "MyWebApp",
  version: "1.0.0",
  settings: {
    theme: "dark",
    notifications: true
  }
};

const prettyJsonConfig = JSON.stringify(config, null, 2);

console.log(prettyJsonConfig);

// PATTERN: JSON Operations

const potentiallyInvalidJson = '{"item": "Keyboard", "price": 75.00, "available": true'; // Missing closing brace
let parsedObject = null;

try {
  parsedObject = JSON.parse(potentiallyInvalidJson);
  console.log("Parsed object:", parsedObject);
} catch (error) {
  console.error("Failed to parse JSON:", error.message);
  // Fallback or error recovery logic here
}