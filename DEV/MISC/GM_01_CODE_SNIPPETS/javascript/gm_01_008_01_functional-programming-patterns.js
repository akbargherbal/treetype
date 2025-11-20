// PATTERN: Functional Programming Patterns

const calculateTotalPrice = (items, taxRate) => {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const taxAmount = subtotal * taxRate;
  return subtotal + taxAmount;
};

const products = [{ price: 10, quantity: 2 }, { price: 5, quantity: 3 }];
const total = calculateTotalPrice(products, 0.08);
// console.log(total);

// PATTERN: Functional Programming Patterns

const addTodo = (todos, newTodoText) => {
  return [...todos, { id: todos.length + 1, text: newTodoText, completed: false }];
};

const toggleTodoCompletion = (todos, todoId) => {
  return todos.map(todo =>
    todo.id === todoId ? { ...todo, completed: !todo.completed } : todo
  );
};

const initialTodos = [{ id: 1, text: 'Learn JS', completed: false }];
const updatedTodos = addTodo(initialTodos, 'Build App');
const finalTodos = toggleTodoCompletion(updatedTodos, 1);
// console.log(finalTodos);

// PATTERN: Functional Programming Patterns

const toUpperCase = str => str.toUpperCase();
const addExclamation = str => `${str}!`;
const reverseString = str => str.split('').reverse().join('');

const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);

const transformMessage = compose(addExclamation, toUpperCase, reverseString);

const result = transformMessage("hello");
// console.log(result);

// PATTERN: Functional Programming Patterns

const curriedMultiply = a => b => c => a * b * c;

const multiplyByTwo = curriedMultiply(2);
const multiplyByTwoAndThree = multiplyByTwo(3);
const finalResult = multiplyByTwoAndThree(4);

// console.log(finalResult);

// PATTERN: Functional Programming Patterns

const createLogger = (prefix) => (message) => {
  console.log(`${prefix}: ${message}`);
};

const logInfo = createLogger("INFO");
const logError = createLogger("ERROR");

logInfo("Application started.");
logError("Failed to connect to database.");

const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(num => num * 2);
// console.log(doubled);

// PATTERN: Functional Programming Patterns

const fetchData = (url, callback) => {
  setTimeout(() => {
    const data = `Data from ${url}`;
    callback(data);
  }, 100);
};

const processData = (data) => {
  console.log(`Processing: ${data}`);
};

fetchData("https://api.example.com/users", processData);

// PATTERN: Functional Programming Patterns

(function() {
  const privateMessage = "This is a private message.";
  console.log(privateMessage);
})();

const result = (() => {
  const x = 10;
  const y = 20;
  return x + y;
})();
// console.log(result);