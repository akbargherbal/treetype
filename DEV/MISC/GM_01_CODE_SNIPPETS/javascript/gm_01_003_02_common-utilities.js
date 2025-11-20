// PATTERN: Common Utilities

const showGreeting = () => {
  console.log("Hello after 2 seconds!");
};

setTimeout(showGreeting, 2000);

// With arguments
const greetUser = (name) => {
  console.log(`Hello, ${name}!`);
};
setTimeout(greetUser, 3000, "Alice");

// PATTERN: Common Utilities

let counter = 0;
const displayCount = () => {
  console.log(`Interval count: ${counter++}`);
};

const intervalId = setInterval(displayCount, 1000);

// To stop it later, you would use clearInterval(intervalId)
// For demonstration, we'll let it run for a few seconds then stop.
setTimeout(() => {
  clearInterval(intervalId);
  console.log("Interval stopped.");
}, 5500);

// PATTERN: Common Utilities

const delayedMessage = () => {
  console.log("This message will not appear.");
};

const timeoutId = setTimeout(delayedMessage, 5000);
clearTimeout(timeoutId);
console.log("Timeout cleared.");

let intervalCount = 0;
const intervalAction = () => {
  console.log(`Interval running: ${intervalCount++}`);
  if (intervalCount >= 3) {
    clearInterval(intervalId);
    console.log("Interval cleared after 3 runs.");
  }
};

const intervalId = setInterval(intervalAction, 1000);

// PATTERN: Common Utilities

// Current date and time
const now = new Date();
console.log("Current date:", now.toString());

// Date from a date string
const specificDate = new Date("2023-10-27T10:00:00Z");
console.log("Specific date:", specificDate.toString());

// Date from year, month (0-11), day, hour, minute, second, millisecond
const customDate = new Date(2024, 0, 1, 12, 30, 0, 0); // Jan 1, 2024, 12:30:00
console.log("Custom date:", customDate.toString());

// Date from milliseconds since epoch
const epochDate = new Date(1678886400000); // March 15, 2023 00:00:00 GMT
console.log("Epoch date:", epochDate.toString());

// PATTERN: Common Utilities

const today = new Date();

// Using toLocaleDateString and toLocaleTimeString
const formattedDate = today.toLocaleDateString("en-US", {
  year: "numeric",
  month: "long",
  day: "numeric",
});
const formattedTime = today.toLocaleTimeString("en-US", {
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
});
console.log(`Date: ${formattedDate}, Time: ${formattedTime}`);

// Using toISOString for a standard format
const isoString = today.toISOString();
console.log("ISO String:", isoString);

// Custom formatting using Intl.DateTimeFormat
const formatter = new Intl.DateTimeFormat("en-GB", {
  weekday: "short",
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
});
console.log("Custom format:", formatter.format(today));

// PATTERN: Common Utilities

// Generate a random float between 0 (inclusive) and 1 (exclusive)
const randomFloat = Math.random();
console.log("Random float (0-1):", randomFloat);

// Generate a random integer between 1 and 10 (inclusive)
const min = 1;
const max = 10;
const randomInt = Math.floor(Math.random() * (max - min + 1)) + min;
console.log(`Random integer (${min}-${max}):`, randomInt);

// Generate a random boolean
const randomBoolean = Math.random() < 0.5;
console.log("Random boolean:", randomBoolean);

// PATTERN: Common Utilities

const number = 4.7;
const negativeNumber = -3.2;

// Math.floor: rounds down to the nearest integer
console.log(`Math.floor(${number}):`, Math.floor(number)); // Output: 4
console.log(`Math.floor(${negativeNumber}):`, Math.floor(negativeNumber)); // Output: -4

// Math.ceil: rounds up to the nearest integer
console.log(`Math.ceil(${number}):`, Math.ceil(number)); // Output: 5
console.log(`Math.ceil(${negativeNumber}):`, Math.ceil(negativeNumber)); // Output: -3

// Math.round: rounds to the nearest integer (0.5 rounds up)
console.log(`Math.round(${number}):`, Math.round(number)); // Output: 5
console.log(`Math.round(4.3):`, Math.round(4.3)); // Output: 4
console.log(`Math.round(4.5):`, Math.round(4.5)); // Output: 5
console.log(`Math.round(${negativeNumber}):`, Math.round(negativeNumber)); // Output: -3

// PATTERN: Common Utilities

const intString = "123";
const floatString = "123.45";
const mixedString = "42px";
const invalidString = "hello";

// parseInt: parses a string argument and returns an integer
console.log(`parseInt("${intString}"):`, parseInt(intString)); // Output: 123
console.log(`parseInt("${floatString}"):`, parseInt(floatString)); // Output: 123
console.log(`parseInt("${mixedString}"):`, parseInt(mixedString)); // Output: 42
console.log(`parseInt("${invalidString}"):`, parseInt(invalidString)); // Output: NaN

// parseFloat: parses a string argument and returns a floating-point number
console.log(`parseFloat("${intString}"):`, parseFloat(intString)); // Output: 123
console.log(`parseFloat("${floatString}"):`, parseFloat(floatString)); // Output: 123.45
console.log(`parseFloat("${mixedString}"):`, parseFloat(mixedString)); // Output: 42
console.log(`parseFloat("${invalidString}"):`, parseFloat(invalidString)); // Output: NaN

// PATTERN: Common Utilities

// Global isNaN()
console.log("isNaN(NaN):", isNaN(NaN)); // true
console.log("isNaN(123):", isNaN(123)); // false
console.log("isNaN('hello'):", isNaN("hello")); // true (coerces 'hello' to NaN)
console.log("isNaN('123'):", isNaN("123")); // false (coerces '123' to 123)
console.log("isNaN(undefined):", isNaN(undefined)); // true (coerces undefined to NaN)
console.log("isNaN(null):", isNaN(null)); // false (coerces null to 0)

// Number.isNaN() - more robust, no type coercion
console.log("\nNumber.isNaN(NaN):", Number.isNaN(NaN)); // true
console.log("Number.isNaN(123):", Number.isNaN(123)); // false
console.log("Number.isNaN('hello'):", Number.isNaN("hello")); // false (does not coerce)
console.log("Number.isNaN('123'):", Number.isNaN("123")); // false
console.log("Number.isNaN(undefined):", Number.isNaN(undefined)); // false
console.log("Number.isNaN(null):", Number.isNaN(null)); // false

// PATTERN: Common Utilities

const myString = "Hello";
const myNumber = 123;
const myBoolean = true;
const myObject = { key: "value" };
const myArray = [1, 2, 3];
const myFunction = () => {};
const myUndefined = undefined;
const myNull = null; // typeof null is "object" - a historical bug

console.log(`Type of "${myString}":`, typeof myString); // "string"
console.log(`Type of ${myNumber}:`, typeof myNumber); // "number"
console.log(`Type of ${myBoolean}:`, typeof myBoolean); // "boolean"
console.log(`Type of myObject:`, typeof myObject); // "object"
console.log(`Type of myArray:`, typeof myArray); // "object" (use Array.isArray for arrays)
console.log(`Type of myFunction:`, typeof myFunction); // "function"
console.log(`Type of myUndefined:`, typeof myUndefined); // "undefined"
console.log(`Type of myNull:`, typeof myNull); // "object"

// PATTERN: Common Utilities

const dataArray = [1, 2, 3];
const dataObject = { a: 1, b: 2 };
const dataString = "hello";
const dataNull = null;
const dataUndefined = undefined;

console.log("Is dataArray an array?", Array.isArray(dataArray)); // true
console.log("Is dataObject an array?", Array.isArray(dataObject)); // false
console.log("Is dataString an array?", Array.isArray(dataString)); // false
console.log("Is dataNull an array?", Array.isArray(dataNull)); // false
console.log("Is dataUndefined an array?", Array.isArray(dataUndefined)); // false

// A common use case in conditional logic
if (Array.isArray(dataArray)) {
  console.log("dataArray is indeed an array with length:", dataArray.length);
}