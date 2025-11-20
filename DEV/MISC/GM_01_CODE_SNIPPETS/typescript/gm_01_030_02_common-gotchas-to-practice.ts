// PATTERN: Common Gotchas to Practice

type UserInfoTuple = [number, string, boolean]; // Fixed length, fixed types
type UserNamesArray = string[]; // Variable length, all strings

function processUserInfo(user: UserInfoTuple): string {
  const [id, name, isActive] = user;
  return `User ID: ${id}, Name: ${name}, Active: ${isActive}`;
}

const user1: UserInfoTuple = [101, "Alice", true];
const userNames: UserNamesArray = ["Bob", "Charlie"];

console.log(processUserInfo(user1));
// console.log(userNames[0].toUpperCase()); // Example usage

// PATTERN: Common Gotchas to Practice

interface UserProfile {
  name: string;
  email?: string; // Optional property, can be undefined
  lastLogin: Date | null; // Can be null
}

function getUserEmail(profile: UserProfile): string {
  // Use nullish coalescing (??) for default value
  const email = profile.email ?? "No email provided";

  // Check for null explicitly
  if (profile.lastLogin === null) {
    return `${profile.name} (${email}) - Never logged in.`;
  }
  return `${profile.name} (${email}) - Last login: ${profile.lastLogin.toLocaleDateString()}.`;
}

const userA: UserProfile = { name: "Alice", lastLogin: new Date() };
const userB: UserProfile = { name: "Bob", email: "bob@example.com", lastLogin: null };

console.log(getUserEmail(userA));
console.log(getUserEmail(userB));

// PATTERN: Common Gotchas to Practice

let statusCode = 200; // Type is widened to 'number'
statusCode = 404; // OK

const defaultTheme = "dark"; // Type is inferred as literal '"dark"'
// defaultTheme = "light"; // Error: Type '"light"' is not assignable to type '"dark"'.

const userSettings = {
  theme: "light", // 'theme' property type is widened to 'string'
  fontSize: 16, // 'fontSize' property type is widened to 'number'
};

userSettings.theme = "dark"; // OK
userSettings.fontSize = 18; // OK

// To prevent widening for object literals, use 'as const':
const strictSettings = {
  theme: "light",
  fontSize: 16,
} as const;

// strictSettings.theme = "dark"; // Error: Cannot assign to 'theme' because it is a read-only property.

// PATTERN: Common Gotchas to Practice

type Id = number | string;

function processId(id: Id): string {
  if (typeof id === "string") {
    // 'id' is narrowed to 'string' here
    return `String ID: ${id.toUpperCase()}`;
  }
  // 'id' is narrowed to 'number' here
  return `Number ID: ${id.toFixed(2)}`;
}

class Dog { bark() { return "Woof!"; } }
class Cat { meow() { return "Meow!"; } }

type Pet = Dog | Cat;

function makeSound(pet: Pet): string {
  if (pet instanceof Dog) {
    // 'pet' is narrowed to 'Dog'
    return pet.bark();
  }
  // 'pet' is narrowed to 'Cat'
  return pet.meow();
}

console.log(processId(123.456));
console.log(processId("abc-789"));
console.log(makeSound(new Dog()));
console.log(makeSound(new Cat()));

// PATTERN: Common Gotchas to Practice

type ColorPalette = {
  primary: string;
  secondary: string;
  accent: string;
};

// Without 'satisfies', 'themeColors.primary' would be inferred as 'string'
const themeColors = {
  primary: "#FF0000",
  secondary: "#00FF00",
  accent: "#0000FF",
} satisfies ColorPalette;

// With 'satisfies', 'themeColors.primary' retains its literal type '#FF0000'
type PrimaryColor = typeof themeColors.primary; // Type is '#FF0000'

function applyColor(color: PrimaryColor) {
  console.log(`Applying primary color: ${color}`);
}

applyColor(themeColors.primary);
// applyColor("#CCCCCC"); // Error: Argument of type '"#CCCCCC"' is not assignable to parameter of type '"#FF0000"'.