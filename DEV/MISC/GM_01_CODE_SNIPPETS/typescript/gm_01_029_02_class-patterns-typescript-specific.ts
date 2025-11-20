// PATTERN: Class Patterns (TypeScript-Specific)

class User {
  id: number;
  name: string;
  isActive: boolean;

  constructor(id: number, name: string, isActive: boolean) {
    this.id = id;
    this.name = name;
    this.isActive = isActive;
  }
}

const user1 = new User(1, "Alice Smith", true);
// console.log(user1.name);

// PATTERN: Class Patterns (TypeScript-Specific)

class Product {
  constructor(
    public id: number,
    private _name: string,
    public price: number
  ) {}

  get name(): string {
    return this._name;
  }

  displayProduct(): string {
    return `${this.id}: ${this._name} - $${this.price}`;
  }
}

const product1 = new Product(101, "Laptop", 1200);
// console.log(product1.displayProduct());

// PATTERN: Class Patterns (TypeScript-Specific)

class Vehicle {
  public make: string;
  private _vin: string;
  protected year: number;

  constructor(make: string, vin: string, year: number) {
    this.make = make;
    this._vin = vin;
    this.year = year;
  }

  getVin(): string {
    return this._vin; // Accessible within the class
  }
}

class Car extends Vehicle {
  constructor(make: string, vin: string, year: number, public model: string) {
    super(make, vin, year);
  }

  getDetails(): string {
    return `${this.make} ${this.model} (${this.year})`; // 'year' is protected, accessible in subclass
  }
}

const myCar = new Car("Toyota", "VIN12345", 2022, "Camry");
// console.log(myCar.make); // Public
// console.log(myCar.getDetails());

// PATTERN: Class Patterns (TypeScript-Specific)

class Configuration {
  readonly apiUrl: string;
  readonly timeout: number = 5000;

  constructor(url: string) {
    this.apiUrl = url;
  }

  // apiUrl = "newUrl"; // Error: Cannot assign to 'apiUrl' because it is a read-only property.
}

const config = new Configuration("https://api.example.com");
// console.log(config.apiUrl);
// console.log(config.timeout);

// PATTERN: Class Patterns (TypeScript-Specific)

abstract class Shape {
  constructor(public color: string) {}

  abstract getArea(): number;

  displayColor(): string {
    return `This shape is ${this.color}.`;
  }
}

class Circle extends Shape {
  constructor(color: string, public radius: number) {
    super(color);
  }

  getArea(): number {
    return Math.PI * this.radius * this.radius;
  }
}

const myCircle = new Circle("blue", 10);
// console.log(myCircle.displayColor());
// console.log(`Area: ${myCircle.getArea()}`);

// PATTERN: Class Patterns (TypeScript-Specific)

interface Logger {
  log(message: string): void;
  error(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string): void {
    console.log(`[INFO] ${message}`);
  }

  error(message: string): void {
    console.error(`[ERROR] ${message}`);
  }
}

const appLogger: Logger = new ConsoleLogger();
// appLogger.log("Application started.");
// appLogger.error("Failed to load data.");

// PATTERN: Class Patterns (TypeScript-Specific)

class MathUtils {
  static readonly PI: number = 3.14159;
  static readonly E: number = 2.71828;

  static add(a: number, b: number): number {
    return a + b;
  }

  static multiply(a: number, b: number): number {
    return a * b;
  }
}

// console.log(MathUtils.PI);
// console.log(MathUtils.add(5, 3));
// console.log(MathUtils.multiply(4, 2));

// PATTERN: Class Patterns (TypeScript-Specific)

class Person {
  private _age: number;

  constructor(initialAge: number) {
    this._age = initialAge;
  }

  get age(): number {
    return this._age;
  }

  set age(newAge: number) {
    if (newAge >= 0 && newAge <= 120) {
      this._age = newAge;
    } else {
      console.error("Invalid age provided.");
    }
  }
}

const person1 = new Person(30);
// console.log(person1.age); // Uses getter
person1.age = 31; // Uses setter
// console.log(person1.age);
person1.age = 150; // Will log an error