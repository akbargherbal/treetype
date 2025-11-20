// PATTERN: Object Manipulation

const userProfile = {
  firstName: "Jane",
  lastName: "Doe",
  age: 28,
  email: "jane.doe@example.com"
};

const keys = Object.keys(userProfile);
console.log(keys);
// Expected: ["firstName", "lastName", "age", "email"]

// PATTERN: Object Manipulation

const productDetails = {
  name: "Wireless Mouse",
  brand: "Logitech",
  price: 49.99,
  inStock: true
};

const values = Object.values(productDetails);
console.log(values);
// Expected: ["Wireless Mouse", "Logitech", 49.99, true]

// PATTERN: Object Manipulation

const studentGrades = {
  math: 90,
  science: 85,
  history: 92
};

const entries = Object.entries(studentGrades);
console.log(entries);
// Expected: [["math", 90], ["science", 85], ["history", 92]]

// PATTERN: Object Manipulation

const defaultSettings = {
  theme: "dark",
  notifications: true
};

const userPreferences = {
  theme: "light",
  language: "en-US"
};

const mergedSettings = Object.assign({}, defaultSettings, userPreferences);
console.log(mergedSettings);
// Expected: { theme: "light", notifications: true, language: "en-US" }

// PATTERN: Object Manipulation

const queryParams = [
  ["userId", "123"],
  ["status", "active"],
  ["page", "2"]
];

const queryConfig = Object.fromEntries(queryParams);
console.log(queryConfig);
// Expected: { userId: "123", status: "active", page: "2" }

// PATTERN: Object Manipulation

const itemType = "productCode";
const itemId = "SKU12345";

const inventoryItem = {
  name: "Laptop",
  price: 1200,
  [itemType]: itemId,
  ["stock" + "Count"]: 50
};

console.log(inventoryItem);
// Expected: { name: "Laptop", price: 1200, productCode: "SKU12345", stockCount: 50 }

// PATTERN: Object Manipulation

const userName = "Alice";
const userAge = 30;
const isActive = true;

const userDetails = {
  userName,
  userAge,
  isActive
};

console.log(userDetails);
// Expected: { userName: "Alice", userAge: 30, isActive: true }

// PATTERN: Object Manipulation

const calculator = {
  value: 0,
  add(a, b) {
    return a + b;
  },
  subtract(a, b) {
    return a - b;
  },
  multiply: function(a, b) { // Traditional syntax for comparison
    return a * b;
  }
};

console.log(calculator.add(5, 3));
// Expected: 8