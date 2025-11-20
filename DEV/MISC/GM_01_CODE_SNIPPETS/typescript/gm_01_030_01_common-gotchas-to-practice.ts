// PATTERN: Common Gotchas to Practice

type UserInfoTuple = [number, string, boolean];
type UserInfoArray = (number | string | boolean)[];

const userProfile: UserInfoTuple = [101, "Alice Smith", true];
// const invalidProfile: UserInfoTuple = ["Bob", 202, false]; // Error: Type 'string' is not assignable to type 'number'

const mixedDataList: UserInfoArray = [1, "Item A", true, 2, "Item B"];
const anotherMixedList: UserInfoArray = ["Charlie", 3];

function displayUser(user: UserInfoTuple) {
  console.log(`ID: ${user[0]}, Name: ${user[1]}, Active: ${user[2]}`);
}

displayUser(userProfile);

// PATTERN: Common Gotchas to Practice

interface Product {
  id: string;
  name: string;
  description?: string; // Can be undefined
  lastReviewed: Date | null; // Can be null
}

function getProductDescription(product: Product): string {
  // Using nullish coalescing operator (??) for undefined
  return product.description ?? "No description available.";
}

function getLastReviewDate(product: Product): string {
  // Using optional chaining (?.) and null check for null
  return product.lastReviewed?.toLocaleDateString() ?? "Never reviewed.";
}

const productA: Product = { id: "P001", name: "Laptop", lastReviewed: new Date() };
const productB: Product = { id: "P002", name: "Mouse", description: "Wireless mouse", lastReviewed: null };

console.log(getProductDescription(productA));
console.log(getLastReviewDate(productB));

// PATTERN: Common Gotchas to Practice

let userStatus = "active"; // Type is 'string', not '"active"'
userStatus = "inactive"; // OK

let productTags = ["electronics", "gadget"]; // Type is 'string[]', not '["electronics", "gadget"]'
productTags.push("sale"); // OK

// Preventing widening with 'as const'
const fixedStatus = "pending" as const; // Type is '"pending"'
// fixedStatus = "completed"; // Error: Type '"completed"' is not assignable to type '"pending"'

const fixedTags = ["new", "featured"] as const; // Type is 'readonly ["new", "featured"]'
// fixedTags.push("hot"); // Error: Property 'push' does not exist on type 'readonly ["new", "featured"]'

console.log(typeof userStatus);
console.log(typeof fixedStatus);

// PATTERN: Common Gotchas to Practice

type Notification = { type: "email"; recipient: string } | { type: "sms"; phoneNumber: string };

function sendNotification(notification: Notification) {
  if (notification.type === "email") {
    // 'notification' is narrowed to { type: "email"; recipient: string }
    console.log(`Sending email to: ${notification.recipient}`);
  } else {
    // 'notification' is narrowed to { type: "sms"; phoneNumber: string }
    console.log(`Sending SMS to: ${notification.phoneNumber}`);
  }
}

type LogEntry = string | number | boolean;

function processLog(entry: LogEntry) {
  if (typeof entry === "string") {
    console.log(`String log: ${entry.toUpperCase()}`);
  } else if (typeof entry === "number") {
    console.log(`Number log: ${entry.toFixed(2)}`);
  } else {
    console.log(`Boolean log: ${entry ? "True" : "False"}`);
  }
}

sendNotification({ type: "email", recipient: "user@example.com" });
processLog(123.456);

// PATTERN: Common Gotchas to Practice

type ThemeColors = {
  primary: string;
  secondary: string;
  background: string;
  text?: string;
};

const myTheme = {
  primary: "#1a73e8",
  secondary: "#fbbc05",
  background: "#ffffff",
  headerHeight: 64, // This property is allowed
} satisfies ThemeColors;

// Without 'satisfies', 'primary' would be widened to 'string'
// With 'satisfies', 'primary' retains its literal type '#1a73e8'
type PrimaryColorLiteral = typeof myTheme.primary; // Type is '#1a73e8'

function applyTheme(colors: ThemeColors) {
  console.log(`Applying primary color: ${colors.primary}`);
}

applyTheme(myTheme);
// const invalidTheme = { primary: 123 } satisfies ThemeColors; // Error: Type 'number' is not assignable to type 'string'