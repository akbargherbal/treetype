// PATTERN: String Methods

const rawInput = "   Hello World!   ";
const trimmedInput = rawInput.trim();

console.log(`Original: '${rawInput}'`);
console.log(`Trimmed: '${trimmedInput}'`);

// PATTERN: String Methods

const sentence = "Learn JavaScript patterns easily";
const words = sentence.split(" ");

console.log("Original string:", sentence);
console.log("Array of words:", words);

const csvData = "apple,banana,orange";
const fruits = csvData.split(",");
console.log("Array of fruits:", fruits);

// PATTERN: String Methods

const tags = ["javascript", "patterns", "coding"];
const tagString = tags.join(", ");

console.log("Original array:", tags);
console.log("Joined string:", tagString);

const pathSegments = ["home", "user", "documents"];
const fullPath = pathSegments.join("/");
console.log("Joined path:", fullPath);

// PATTERN: String Methods

const articleContent = "This article discusses modern JavaScript patterns.";
const keyword = "JavaScript";
const hasKeyword = articleContent.includes(keyword);

console.log(`Content: "${articleContent}"`);
console.log(`Includes "${keyword}"? ${hasKeyword}`);

const searchItem = "patterns";
if (articleContent.includes(searchItem)) {
  console.log(`Found "${searchItem}" in the content.`);
}

// PATTERN: String Methods

const fileName = "report.2023.pdf";
const url = "https://www.example.com/data";

const isPdf = fileName.endsWith(".pdf");
const isSecure = url.startsWith("https://");

console.log(`File "${fileName}" ends with ".pdf"? ${isPdf}`);
console.log(`URL "${url}" starts with "https://"? ${isSecure}`);

const isReport = fileName.startsWith("report");
console.log(`File "${fileName}" starts with "report"? ${isReport}`);

// PATTERN: String Methods

const originalText = "The quick brown fox jumps over the lazy fox.";

// Replace only the first occurrence
const firstReplaced = originalText.replace("fox", "dog");
console.log("First replaced:", firstReplaced);

// Replace all occurrences
const allReplaced = originalText.replaceAll("fox", "dog");
console.log("All replaced:", allReplaced);

// Using regex for global replacement (alternative to replaceAll)
const regexReplaced = originalText.replace(/fox/g, "cat");
console.log("Regex replaced (all):", regexReplaced);

// PATTERN: String Methods

const productName = "JavaScript Framework";
const userInput = "react";

const lowerCaseName = productName.toLowerCase();
const upperCaseName = productName.toUpperCase();

console.log(`Original: "${productName}"`);
console.log(`Lowercase: "${lowerCaseName}"`);
console.log(`Uppercase: "${upperCaseName}"`);

// Useful for case-insensitive comparisons
if (userInput.toLowerCase() === "react") {
  console.log("User input matches 'react' (case-insensitive).");
}

// PATTERN: String Methods

const invoiceNumber = "123";
const totalLength = 6;

const paddedStart = invoiceNumber.padStart(totalLength, "0");
console.log(`Padded start: ${paddedStart}`); // "000123"

const productCode = "ABC";
const paddedEnd = productCode.padEnd(5, "-");
console.log(`Padded end: ${paddedEnd}`); // "ABC--"

const shortName = "JS";
const paddedName = shortName.padEnd(10, ".");
console.log(`Padded name: ${paddedName}`);

// PATTERN: String Methods

const userName = "Alice";
const userAge = 30;
const userCity = "New York";

const greeting = `Hello, my name is ${userName} and I am ${userAge} years old.`;
console.log(greeting);

const userInfo = `User: ${userName}
Age: ${userAge}
City: ${userCity}`;
console.log(userInfo);

const price = 19.99;
const taxRate = 0.05;
const total = `Total: $${(price * (1 + taxRate)).toFixed(2)}`;
console.log(total);