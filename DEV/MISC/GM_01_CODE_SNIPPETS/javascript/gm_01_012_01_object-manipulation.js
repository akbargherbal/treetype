// PATTERN: Object Manipulation

const productDetails = {
  id: 'P101',
  name: 'Wireless Mouse',
  price: 25.99,
  inStock: true
};

const keys = Object.keys(productDetails);
console.log(keys);
// Expected: ["id", "name", "price", "inStock"]

// PATTERN: Object Manipulation

const productDetails = {
  id: 'P101',
  name: 'Wireless Mouse',
  price: 25.99,
  inStock: true
};

const values = Object.values(productDetails);
console.log(values);
// Expected: ["P101", "Wireless Mouse", 25.99, true]

// PATTERN: Object Manipulation

const productDetails = {
  id: 'P101',
  name: 'Wireless Mouse',
  price: 25.99,
  inStock: true
};

const entries = Object.entries(productDetails);
console.log(entries);
/* Expected:
[
  ["id", "P101"],
  ["name", "Wireless Mouse"],
  ["price", 25.99],
  ["inStock", true]
]
*/

// PATTERN: Object Manipulation

const defaultSettings = { theme: 'dark', notifications: true, language: 'en' };
const userPreferences = { theme: 'light', language: 'es' };

const mergedSettings = Object.assign({}, defaultSettings, userPreferences);
console.log(mergedSettings);
/* Expected:
{
  theme: 'light',
  notifications: true,
  language: 'es'
}
*/

// PATTERN: Object Manipulation

const userProfileArray = [
  ['firstName', 'Jane'],
  ['lastName', 'Doe'],
  ['age', 28],
  ['isActive', true]
];

const userProfileObject = Object.fromEntries(userProfileArray);
console.log(userProfileObject);
/* Expected:
{
  firstName: 'Jane',
  lastName: 'Doe',
  age: 28,
  isActive: true
}
*/

// PATTERN: Object Manipulation

const itemType = 'productCode';
const itemValue = 'XYZ789';
const quantityKey = 'stockQuantity';
const quantityValue = 150;

const inventoryItem = {
  [itemType]: itemValue,
  [quantityKey]: quantityValue,
  description: 'High-quality widget'
};

console.log(inventoryItem);
/* Expected:
{
  productCode: 'XYZ789',
  stockQuantity: 150,
  description: 'High-quality widget'
}
*/

// PATTERN: Object Manipulation

const userName = 'Alice';
const userAge = 30;
const userEmail = 'alice@example.com';

const user = {
  userName,
  userAge,
  userEmail,
  isAdmin: false
};

console.log(user);
/* Expected:
{
  userName: 'Alice',
  userAge: 30,
  userEmail: 'alice@example.com',
  isAdmin: false
}
*/

// PATTERN: Object Manipulation

const calculator = {
  value: 0,
  add(a, b) {
    return a + b;
  },
  subtract(a, b) {
    return a - b;
  },
  multiply(a, b) {
    this.value = a * b;
    return this.value;
  }
};

console.log(calculator.add(5, 3));
console.log(calculator.multiply(4, 2));
console.log(calculator.value);
// Expected: 8, 8, 8