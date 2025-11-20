// PATTERN: String Methods

const rawInput = "   Hello World!   ";
const trimmedInput = rawInput.trim();

console.log(`Original: '${rawInput}'`);
console.log(`Trimmed: '${trimmedInput}'`);

// PATTERN: String Methods

const csvString = "apple,banana,orange,grape";
const fruitsArray = csvString.split(',');

console.log("CSV String:", csvString);
console.log("Fruits Array:", fruitsArray);

// PATTERN: String Methods

const words = ["Hello", "beautiful", "world"];
const sentence = words.join(' ');

console.log("Words Array:", words);
console.log("Joined Sentence:", sentence);

// PATTERN: String Methods

const message = "The quick brown fox jumps over the lazy dog.";
const hasFox = message.includes("fox");
const hasCat = message.includes("cat");

console.log(`Message: "${message}"`);
console.log(`Includes "fox"? ${hasFox}`);
console.log(`Includes "cat"? ${hasCat}`);

// PATTERN: String Methods

const fileName = "document.pdf";
const isPdf = fileName.endsWith(".pdf");
const startsWithDoc = fileName.startsWith("doc");

console.log(`File Name: "${fileName}"`);
console.log(`Is PDF? ${isPdf}`);
console.log(`Starts with "doc"? ${startsWithDoc}`);

// PATTERN: String Methods

const text = "The dog is a loyal animal. A dog is a good friend.";
const firstReplace = text.replace("dog", "cat");
const allReplace = text.replaceAll("dog", "cat");

console.log(`Original: "${text}"`);
console.log(`First replace: "${firstReplace}"`);
console.log(`All replace: "${allReplace}"`);

// PATTERN: String Methods

const mixedCase = "JavaScript Programming";
const lowerCase = mixedCase.toLowerCase();
const upperCase = mixedCase.toUpperCase();

console.log(`Original: "${mixedCase}"`);
console.log(`Lowercase: "${lowerCase}"`);
console.log(`Uppercase: "${upperCase}"`);

// PATTERN: String Methods

const userId = "42";
const paddedIdStart = userId.padStart(5, '0');
const paddedIdEnd = userId.padEnd(5, 'X');

console.log(`Original ID: "${userId}"`);
console.log(`Padded Start: "${paddedIdStart}"`);
console.log(`Padded End: "${paddedIdEnd}"`);

// PATTERN: String Methods

const userName = "Alice";
const userAge = 30;
const greeting = `Hello, ${userName}! You are ${userAge} years old.`;

console.log(greeting);