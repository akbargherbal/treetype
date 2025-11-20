// PATTERN: ES6+ Class Syntax

class User {
  // Class body
}

const newUser = new User();
console.log(newUser instanceof User); // true

// PATTERN: ES6+ Class Syntax

class Product {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
}

const laptop = new Product("Laptop", 1200);
console.log(laptop.name); // Laptop
console.log(laptop.price); // 1200

// PATTERN: ES6+ Class Syntax

class Order {
  constructor(orderId, items) {
    this.orderId = orderId;
    this.items = items;
  }

  getTotalPrice() {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}

const myOrder = new Order("A123", [{ name: "Book", price: 25 }, { name: "Pen", price: 5 }]);
console.log(myOrder.getTotalPrice()); // 30

// PATTERN: ES6+ Class Syntax

class TemperatureConverter {
  static celsiusToFahrenheit(celsius) {
    return (celsius * 9/5) + 32;
  }

  static fahrenheitToCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5/9;
  }
}

const tempF = TemperatureConverter.celsiusToFahrenheit(25);
const tempC = TemperatureConverter.fahrenheitToCelsius(77);
console.log(`25°C is ${tempF}°F`); // 25°C is 77°F
console.log(`77°F is ${tempC}°C`); // 77°F is 25°C

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
  bark() {
    return `${this.name} barks!`;
  }
}

const myDog = new Dog("Buddy", "Golden Retriever");
console.log(myDog.speak()); // Buddy makes a sound.
console.log(myDog.bark()); // Buddy barks!

// PATTERN: ES6+ Class Syntax

class Shape {
  constructor(color) {
    this.color = color;
  }
}

class Circle extends Shape {
  constructor(color, radius) {
    super(color); // Calls the constructor of the parent class (Shape)
    this.radius = radius;
  }

  getArea() {
    return Math.PI * this.radius * this.radius;
  }
}

const myCircle = new Circle("blue", 10);
console.log(myCircle.color); // blue
console.log(myCircle.getArea().toFixed(2)); // 314.16