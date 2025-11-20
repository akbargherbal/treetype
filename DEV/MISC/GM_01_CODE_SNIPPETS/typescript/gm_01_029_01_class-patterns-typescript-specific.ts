// PATTERN: Class Patterns (TypeScript-Specific)

class Book {
  title: string;
  author: string;
  pages: number;

  constructor(title: string, author: string, pages: number) {
    this.title = title;
    this.author = author;
    this.pages = pages;
  }

  getSummary(): string {
    return `${this.title} by ${this.author}, ${this.pages} pages.`;
  }
}

// PATTERN: Class Patterns (TypeScript-Specific)

class Product {
  constructor(
    public id: number,
    public name: string,
    private _price: number
  ) {}

  getPrice(): number {
    return this._price;
  }

  setPrice(newPrice: number): void {
    if (newPrice >= 0) {
      this._price = newPrice;
    }
  }
}

// PATTERN: Class Patterns (TypeScript-Specific)

class Vehicle {
  public make: string;
  protected year: number;
  private vin: string;

  constructor(make: string, year: number, vin: string) {
    this.make = make;
    this.year = year;
    this.vin = vin;
  }

  public getMake(): string {
    return this.make;
  }

  protected getYear(): number {
    return this.year;
  }
}

class Car extends Vehicle {
  constructor(make: string, year: number, vin: string) {
    super(make, year, vin);
  }

  getCarInfo(): string {
    return `Car: ${this.make}, Year: ${this.year}`; // 'year' is protected, accessible in subclass
  }
}

// PATTERN: Class Patterns (TypeScript-Specific)

class Configuration {
  readonly apiUrl: string;
  readonly maxConnections: number;

  constructor(url: string, connections: number) {
    this.apiUrl = url;
    this.maxConnections = connections;
  }

  // Attempting to modify apiUrl here would result in a compile-time error:
  // setApiUrl(newUrl: string) {
  //   this.apiUrl = newUrl;
  // }
}

// PATTERN: Class Patterns (TypeScript-Specific)

abstract class Shape {
  constructor(public name: string) {}

  abstract getArea(): number; // Abstract method

  displayInfo(): string {
    return `This is a ${this.name}.`;
  }
}

class Circle extends Shape {
  constructor(name: string, public radius: number) {
    super(name);
  }

  getArea(): number {
    return Math.PI * this.radius * this.radius;
  }
}

// PATTERN: Class Patterns (TypeScript-Specific)

interface Loggable {
  log(message: string): void;
  getTimestamp(): Date;
}

class ConsoleLogger implements Loggable {
  log(message: string): void {
    console.log(`[${this.getTimestamp().toISOString()}] ${message}`);
  }

  getTimestamp(): Date {
    return new Date();
  }
}

// PATTERN: Class Patterns (TypeScript-Specific)

class MathUtils {
  static readonly PI: number = 3.14159;
  static version: string = "1.0.0";

  private constructor() {} // Prevent instantiation

  static add(a: number, b: number): number {
    return a + b;
  }

  static multiply(a: number, b: number): number {
    return a * b;
  }
}

// PATTERN: Class Patterns (TypeScript-Specific)

class Temperature {
  private _celsius: number;

  constructor(celsius: number) {
    this._celsius = celsius;
  }

  get celsius(): number {
    return this._celsius;
  }

  set celsius(value: number) {
    if (value < -273.15) { // Absolute zero
      throw new Error("Temperature cannot be below absolute zero.");
    }
    this._celsius = value;
  }

  get fahrenheit(): number {
    return (this._celsius * 9 / 5) + 32;
  }

  set fahrenheit(value: number) {
    this._celsius = (value - 32) * 5 / 9;
  }
}