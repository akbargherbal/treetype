// PATTERN: Interface Patterns

interface UserProfile {
  id: number;
  name: string;
  email: string;
}

const user: UserProfile = {
  id: 1,
  name: "Alice Smith",
  email: "alice@example.com",
};

console.log(user.name);

// PATTERN: Interface Patterns

interface Product {
  id: string;
  name: string;
  description?: string; // Optional property
  price: number;
}

const laptop: Product = {
  id: "LPT101",
  name: "Gaming Laptop",
  price: 1200,
};

const keyboard: Product = {
  id: "KBD202",
  name: "Mechanical Keyboard",
  description: "RGB backlit, tactile switches",
  price: 150,
};

console.log(laptop.description); // undefined

// PATTERN: Interface Patterns

interface Configuration {
  readonly apiKey: string;
  readonly baseUrl: string;
  timeout: number;
}

const appConfig: Configuration = {
  apiKey: "abc-123",
  baseUrl: "https://api.example.com",
  timeout: 5000,
};

// appConfig.apiKey = "new-key"; // Error: Cannot assign to 'apiKey' because it is a read-only property.
appConfig.timeout = 10000; // OK

console.log(appConfig.apiKey);

// PATTERN: Interface Patterns

interface Shape {
  color: string;
}

interface Circle extends Shape {
  radius: number;
}

interface Rectangle extends Shape {
  width: number;
  height: number;
}

const myCircle: Circle = {
  color: "blue",
  radius: 10,
};

const myRectangle: Rectangle = {
  color: "red",
  width: 20,
  height: 30,
};

console.log(myCircle.color, myRectangle.width);

// PATTERN: Interface Patterns

interface StringDictionary {
  [key: string]: string;
}

interface NumberDictionary {
  [index: number]: string;
}

const userSettings: StringDictionary = {
  theme: "dark",
  language: "en-US",
  fontSize: "16px",
};

const errorCodes: NumberDictionary = {
  404: "Not Found",
  500: "Internal Server Error",
};

console.log(userSettings["theme"]);
console.log(errorCodes[404]);

// PATTERN: Interface Patterns

interface MathOperation {
  (x: number, y: number): number;
}

const add: MathOperation = (a, b) => a + b;
const subtract: MathOperation = (a, b) => a - b;

console.log(add(5, 3));
console.log(subtract(10, 4));

// You can also define methods within an interface
interface Calculator {
  add(x: number, y: number): number;
  subtract(x: number, y: number): number;
}

const basicCalc: Calculator = {
  add: (x, y) => x + y,
  subtract: (x, y) => x - y,
};

console.log(basicCalc.add(2, 2));

// PATTERN: Interface Patterns

interface Counter {
  (start: number): string; // Callable signature
  interval: number;
  reset(): void;
}

function createCounter(): Counter {
  let count = 0;

  const counter = ((start: number) => {
    count = start;
    return `Counter started at ${start}`;
  }) as Counter;

  counter.interval = 1;
  counter.reset = () => {
    count = 0;
    console.log("Counter reset!");
  };

  return counter;
}

const myCounter = createCounter();
console.log(myCounter(10));
myCounter.reset();
console.log(myCounter.interval);