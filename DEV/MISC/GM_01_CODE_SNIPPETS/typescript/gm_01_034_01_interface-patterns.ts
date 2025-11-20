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

interface ProductConfig {
  id: string;
  name: string;
  description?: string;
  price?: number;
}

const productA: ProductConfig = {
  id: "P001",
  name: "Laptop",
};

const productB: ProductConfig = {
  id: "P002",
  name: "Mouse",
  price: 25.99,
};

console.log(productA.description);

// PATTERN: Interface Patterns

interface ImmutablePoint {
  readonly x: number;
  readonly y: number;
}

const origin: ImmutablePoint = { x: 0, y: 0 };

// origin.x = 1; // Error: Cannot assign to 'x' because it is a read-only property.

const newPoint: ImmutablePoint = { x: 10, y: 20 };
console.log(newPoint.x, newPoint.y);

// PATTERN: Interface Patterns

interface Shape {
  color: string;
}

interface Circle extends Shape {
  radius: number;
}

const myCircle: Circle = {
  color: "blue",
  radius: 10,
};

console.log(`My circle is ${myCircle.color} with radius ${myCircle.radius}`);

// PATTERN: Interface Patterns

interface StringDictionary {
  [key: string]: string;
}

const userSettings: StringDictionary = {
  theme: "dark",
  language: "en-US",
  fontSize: "medium",
};

console.log(userSettings["theme"]);
userSettings["lastLogin"] = new Date().toISOString();
console.log(userSettings["lastLogin"]);

// PATTERN: Interface Patterns

interface Calculator {
  add(a: number, b: number): number;
  subtract: (a: number, b: number) => number;
}

const myCalculator: Calculator = {
  add: (x, y) => x + y,
  subtract: (x, y) => x - y,
};

console.log(myCalculator.add(5, 3));
console.log(myCalculator.subtract(10, 4));

// PATTERN: Interface Patterns

interface Counter {
  (start: number): string;
  interval: number;
  reset(): void;
}

const createCounter = (): Counter => {
  let count = 0;
  const counter = ((start: number) => {
    count = start;
    return `Count set to ${start}`;
  }) as Counter;

  counter.interval = 1;
  counter.reset = () => { count = 0; };
  return counter;
};

const myCounter = createCounter();
console.log(myCounter(5));
myCounter.reset();
console.log(myCounter.interval);