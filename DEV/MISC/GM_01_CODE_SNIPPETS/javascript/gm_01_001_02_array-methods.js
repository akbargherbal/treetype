// PATTERN: Array Methods

const products = [
  { id: 1, name: "Laptop", price: 1200 },
  { id: 2, name: "Mouse", price: 25 },
  { id: 3, name: "Keyboard", price: 75 }
];

const productNames = products.map(product => product.name.toUpperCase());

// console.log(productNames); // ["LAPTOP", "MOUSE", "KEYBOARD"]

// PATTERN: Array Methods

const transactions = [150, -30, 200, -10, 500, -75];

const deposits = transactions.filter(amount => amount > 0);

// console.log(deposits); // [150, 200, 500]

// PATTERN: Array Methods

const users = [
  { id: 101, name: "Alice" },
  { id: 102, name: "Bob" },
  { id: 103, name: "Charlie" }
];

const userBob = users.find(user => user.name === "Bob");

// console.log(userBob); // { id: 102, name: "Bob" }

// PATTERN: Array Methods

const inventory = [
  { item: "Apples", quantity: 50 },
  { item: "Bananas", quantity: 0 },
  { item: "Oranges", quantity: 30 }
];

const outOfStockIndex = inventory.findIndex(product => product.quantity === 0);

// console.log(outOfStockIndex); // 1

// PATTERN: Array Methods

const tasks = [
  { id: 1, completed: false },
  { id: 2, completed: true },
  { id: 3, completed: false }
];

const hasIncompleteTasks = tasks.some(task => !task.completed);

// console.log(hasIncompleteTasks); // true

// PATTERN: Array Methods

const sensorReadings = [
  { temp: 22, humidity: 60 },
  { temp: 23, humidity: 62 },
  { temp: 21, humidity: 59 }
];

const allTempsAbove20 = sensorReadings.every(reading => reading.temp > 20);

// console.log(allTempsAbove20); // true

// PATTERN: Array Methods

const cartItems = [
  { name: "Shirt", price: 25, quantity: 2 },
  { name: "Pants", price: 40, quantity: 1 },
  { name: "Socks", price: 10, quantity: 3 }
];

const totalCost = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

// console.log(totalCost); // 120

// PATTERN: Array Methods

const movies = [
  { title: "Inception", year: 2010 },
  { title: "Avatar", year: 2009 },
  { title: "Dune", year: 2021 }
];

movies.sort((a, b) => a.year - b.year);

// console.log(movies);
// [
//   { title: "Avatar", year: 2009 },
//   { title: "Inception", year: 2010 },
//   { title: "Dune", year: 2021 }
// ]

// PATTERN: Array Methods

const colors = ["red", "green", "blue", "yellow", "purple"];

const primaryColors = colors.slice(0, 3);
const lastTwoColors = colors.slice(-2);

// console.log(primaryColors); // ["red", "green", "blue"]
// console.log(lastTwoColors); // ["yellow", "purple"]

// PATTERN: Array Methods

const fruits = ["apple", "banana"];
const vegetables = ["carrot", "spinach"];

const produce = fruits.concat(vegetables);
const moreProduce = [...fruits, ...vegetables, "potato"]; // Modern alternative

// console.log(produce); // ["apple", "banana", "carrot", "spinach"]
// console.log(moreProduce); // ["apple", "banana", "carrot", "spinach", "potato"]

// PATTERN: Array Methods

const nestedNumbers = [1, [2, 3], [4, [5, 6]]];

const flatOnce = nestedNumbers.flat();
const flatAll = nestedNumbers.flat(Infinity);

// console.log(flatOnce); // [1, 2, 3, 4, [5, 6]]
// console.log(flatAll); // [1, 2, 3, 4, 5, 6]

// PATTERN: Array Methods

const sentences = ["Hello world", "JavaScript is fun"];

const words = sentences.flatMap(sentence => sentence.split(" "));

// console.log(words); // ["Hello", "world", "JavaScript", "is", "fun"]

// PATTERN: Array Methods

const str = "hello";
const charArray = Array.from(str);

const numbers = Array.from({ length: 5 }, (_, i) => i + 1);

// console.log(charArray); // ["h", "e", "l", "l", "o"]
// console.log(numbers); // [1, 2, 3, 4, 5]

// PATTERN: Array Methods

const allowedRoles = ["admin", "editor", "viewer"];

const userRole = "editor";
const hasAccess = allowedRoles.includes(userRole);

const invalidRole = "guest";
const hasInvalidAccess = allowedRoles.includes(invalidRole);

// console.log(hasAccess); // true
// console.log(hasInvalidAccess); // false

// PATTERN: Array Methods

const playlist = ["Song A", "Song B", "Song C", "Song B"];

const firstIndexOfSongB = playlist.indexOf("Song B");
const indexOfSongD = playlist.indexOf("Song D");

// console.log(firstIndexOfSongB); // 1
// console.log(indexOfSongD); // -1 (not found)