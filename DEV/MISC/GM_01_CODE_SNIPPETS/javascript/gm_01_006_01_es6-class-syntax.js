// PATTERN: ES6+ Class Syntax

class User {
  // Class body can be empty or contain methods/properties
}
const admin = new User();
console.log(admin instanceof User);

// PATTERN: ES6+ Class Syntax

class Product {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
}
const laptop = new Product("Laptop", 1200);
console.log(`${laptop.name}: $${laptop.price}`);

// PATTERN: ES6+ Class Syntax

class Product {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }

  getDetails() {
    return `${this.name} costs $${this.price}.`;
  }
}
const smartphone = new Product("Smartphone", 800);
console.log(smartphone.getDetails());

// PATTERN: ES6+ Class Syntax

class Calculator {
  static add(a, b) {
    return a + b;
  }

  static multiply(a, b) {
    return a * b;
  }
}
const sum = Calculator.add(10, 5);
const product = Calculator.multiply(4, 3);
console.log(`Sum: ${sum}, Product: ${product}`);

// PATTERN: ES6+ Class Syntax

class Vehicle {
  constructor(make) {
    this.make = make;
  }
  getMake() {
    return this.make;
  }
}

class Car extends Vehicle {
  constructor(make, model) {
    super(make);
    this.model = model;
  }
  getModel() {
    return `${this.make} ${this.model}`;
  }
}
const myCar = new Car("Toyota", "Camry");
console.log(myCar.getModel());

// PATTERN: ES6+ Class Syntax

class Animal {
  constructor(name) {
    this.name = name;
  }
  speak() {
    return `${this.name} makes a sound.`;
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name); // Calls the parent constructor
    this.breed = breed;
  }
  speak() {
    return `${super.speak()} Woof!`; // Calls parent method
  }
}
const myDog = new Dog("Buddy", "Golden Retriever");
console.log(myDog.speak());