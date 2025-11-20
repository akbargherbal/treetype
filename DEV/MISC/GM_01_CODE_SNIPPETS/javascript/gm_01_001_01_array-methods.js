// PATTERN: Array Methods

const products = [
  { id: 1, name: 'Laptop', price: 1200 },
  { id: 2, name: 'Mouse', price: 25 },
  { id: 3, name: 'Keyboard', price: 75 }
];

const productNames = products.map(product => product.name);

// productNames will be ['Laptop', 'Mouse', 'Keyboard']

// PATTERN: Array Methods

const users = [
  { id: 1, name: 'Alice', isActive: true },
  { id: 2, name: 'Bob', isActive: false },
  { id: 3, name: 'Charlie', isActive: true }
];

const activeUsers = users.filter(user => user.isActive);

// activeUsers will be [{ id: 1, name: 'Alice', isActive: true }, { id: 3, name: 'Charlie', isActive: true }]

// PATTERN: Array Methods

const employees = [
  { id: 101, name: 'John Doe', department: 'HR' },
  { id: 102, name: 'Jane Smith', department: 'IT' },
  { id: 103, name: 'Peter Jones', department: 'HR' }
];

const itEmployee = employees.find(employee => employee.department === 'IT');

// itEmployee will be { id: 102, name: 'Jane Smith', department: 'IT' }

// PATTERN: Array Methods

const tasks = [
  { id: 'a1', description: 'Review code', completed: false },
  { id: 'b2', description: 'Write tests', completed: true },
  { id: 'c3', description: 'Deploy app', completed: false }
];

const deployTaskIndex = tasks.findIndex(task => task.id === 'c3');

// deployTaskIndex will be 2

// PATTERN: Array Methods

const orders = [
  { id: 1, status: 'pending' },
  { id: 2, status: 'shipped' },
  { id: 3, status: 'delivered' }
];

const hasPendingOrders = orders.some(order => order.status === 'pending');

// hasPendingOrders will be true

// PATTERN: Array Methods

const sensorReadings = [
  { id: 1, value: 22, unit: 'C' },
  { id: 2, value: 23, unit: 'C' },
  { id: 3, value: 21, unit: 'C' }
];

const allCelsius = sensorReadings.every(reading => reading.unit === 'C');

// allCelsius will be true

// PATTERN: Array Methods

const expenses = [
  { item: 'Groceries', amount: 50 },
  { item: 'Transport', amount: 20 },
  { item: 'Dinner', amount: 30 }
];

const totalExpenses = expenses.reduce((sum, expense) => sum + expense.amount, 0);

// totalExpenses will be 100

// PATTERN: Array Methods

const books = [
  { title: 'Book C', year: 2005 },
  { title: 'Book A', year: 2010 },
  { title: 'Book B', year: 2008 }
];

// Sort by year ascending
books.sort((a, b) => a.year - b.year);

// books will be sorted by year: [{ title: 'Book C', year: 2005 }, { title: 'Book B', year: 2008 }, { title: 'Book A', year: 2010 }]

// PATTERN: Array Methods

const originalNumbers = [10, 20, 30, 40, 50, 60];

const middleNumbers = originalNumbers.slice(2, 5); // from index 2 up to (but not including) index 5
const allNumbersCopy = originalNumbers.slice(); // creates a shallow copy of the entire array

// middleNumbers will be [30, 40, 50]
// allNumbersCopy will be [10, 20, 30, 40, 50, 60]

// PATTERN: Array Methods

const array1 = [1, 2, 3];
const array2 = [4, 5];
const array3 = [6, 7];

const mergedArray = array1.concat(array2, array3);

// mergedArray will be [1, 2, 3, 4, 5, 6, 7]

// PATTERN: Array Methods

const nestedArray = [1, [2, 3], [4, [5, 6]]];

const flattenedOnce = nestedArray.flat(); // default depth is 1
const fullyFlattened = nestedArray.flat(2); // flatten up to depth 2

// flattenedOnce will be [1, 2, 3, 4, [5, 6]]
// fullyFlattened will be [1, 2, 3, 4, 5, 6]

// PATTERN: Array Methods

const sentences = ["Hello world", "JavaScript is fun"];

const words = sentences.flatMap(sentence => sentence.split(' '));

// words will be ["Hello", "world", "JavaScript", "is", "fun"]

// PATTERN: Array Methods

const mySet = new Set(['apple', 'banana', 'orange']);
const myString = "hello";

const arrayFromSet = Array.from(mySet);
const arrayFromString = Array.from(myString);

// arrayFromSet will be ['apple', 'banana', 'orange']
// arrayFromString will be ['h', 'e', 'l', 'l', 'o']

// PATTERN: Array Methods

const availableColors = ['red', 'green', 'blue'];

const hasGreen = availableColors.includes('green');
const hasYellow = availableColors.includes('yellow');

// hasGreen will be true
// hasYellow will be false

// PATTERN: Array Methods

const fruitBasket = ['apple', 'banana', 'orange', 'apple'];

const firstAppleIndex = fruitBasket.indexOf('apple');
const orangeIndex = fruitBasket.indexOf('orange');
const grapeIndex = fruitBasket.indexOf('grape'); // Not found

// firstAppleIndex will be 0
// orangeIndex will be 2
// grapeIndex will be -1