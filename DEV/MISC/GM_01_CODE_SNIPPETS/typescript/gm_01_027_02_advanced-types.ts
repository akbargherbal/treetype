// PATTERN: Advanced Types

function identity<T>(arg: T): T {
  return arg;
}

let output1 = identity<string>("myString");
let output2 = identity<number>(123);

console.log(output1, output2);

// PATTERN: Advanced Types

interface Box<T> {
  value: T;
}

let stringBox: Box<string> = { value: "Hello" };
let numberBox: Box<number> = { value: 42 };

console.log(stringBox.value, numberBox.value);

// PATTERN: Advanced Types

interface Lengthwise {
  length: number;
}

function logLength<T extends Lengthwise>(arg: T): T {
  console.log(arg.length);
  return arg;
}

logLength("TypeScript");
logLength([1, 2, 3]);
// logLength(10); // Error: Argument of type 'number' is not assignable to parameter of type 'Lengthwise'.

// PATTERN: Advanced Types

interface UserProfile {
  name: string;
  age: number;
  email?: string;
}

type UserProfileKeys = keyof UserProfile; // "name" | "age" | "email"

function getPropertyValue<T, K extends keyof T>(obj: T, key: K) {
  return obj[key];
}

const user: UserProfile = { name: "Alice", age: 30 };
const userName = getPropertyValue(user, "name");
console.log(userName);

// PATTERN: Advanced Types

const userSettings = {
  theme: "dark",
  fontSize: 16,
};

type UserSettingsType = typeof userSettings;

function applySettings(settings: UserSettingsType) {
  console.log(`Applying theme: ${settings.theme}, font size: ${settings.fontSize}`);
}

applySettings({ theme: "light", fontSize: 14 });

// PATTERN: Advanced Types

interface Product {
  id: number;
  name: string;
  price: number;
  details: {
    weight: number;
    color: string;
  };
}

type ProductName = Product["name"]; // string
type ProductDetails = Product["details"]; // { weight: number; color: string; }
type ProductDetailColor = Product["details"]["color"]; // string

const productName: ProductName = "Laptop";
const productDetailColor: ProductDetailColor = "Silver";
console.log(productName, productDetailColor);

// PATTERN: Advanced Types

type IsString<T> = T extends string ? "Yes" : "No";

type Result1 = IsString<string>; // "Yes"
type Result2 = IsString<number>; // "No"

function checkType<T>(value: T): IsString<T> {
  return (typeof value === 'string' ? "Yes" : "No") as IsString<T>;
}

console.log(checkType("hello"));
console.log(checkType(123));

// PATTERN: Advanced Types

interface UserPermissions {
  canView: boolean;
  canEdit: boolean;
  canDelete: boolean;
}

type ReadonlyPermissions<T> = {
  readonly [P in keyof T]: T[P];
};

type UserReadonlyPermissions = ReadonlyPermissions<UserPermissions>;

const userPerms: UserReadonlyPermissions = {
  canView: true,
  canEdit: false,
  canDelete: false,
};
// userPerms.canView = false; // Error: Cannot assign to 'canView' because it is a read-only property.
console.log(userPerms);

// PATTERN: Advanced Types

interface UserSettings {
  theme: string;
  notificationsEnabled: boolean;
  language: string;
}

function updateSettings(settings: UserSettings, updates: Partial<UserSettings>) {
  return { ...settings, ...updates };
}

const defaultSettings: UserSettings = { theme: "dark", notificationsEnabled: true, language: "en" };
const newSettings = updateSettings(defaultSettings, { theme: "light", language: "fr" });

console.log(newSettings);

// PATTERN: Advanced Types

interface ProductInfo {
  id: number;
  name?: string;
  description?: string;
}

type CompleteProductInfo = Required<ProductInfo>;

const product: CompleteProductInfo = {
  id: 101,
  name: "Widget",
  description: "A useful widget.",
};

// const incompleteProduct: CompleteProductInfo = { id: 102 }; // Error: Property 'name' is missing
console.log(product);

// PATTERN: Advanced Types

interface Configuration {
  apiUrl: string;
  timeout: number;
}

type ImmutableConfig = Readonly<Configuration>;

const appConfig: ImmutableConfig = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
};

// appConfig.timeout = 10000; // Error: Cannot assign to 'timeout' because it is a read-only property.
console.log(appConfig.apiUrl);

// PATTERN: Advanced Types

interface Employee {
  id: number;
  name: string;
  email: string;
  department: string;
}

type EmployeeSummary = Pick<Employee, "id" | "name">;

const employee: Employee = {
  id: 1,
  name: "John Doe",
  email: "john.doe@example.com",
  department: "Engineering",
};

const summary: EmployeeSummary = {
  id: employee.id,
  name: employee.name,
};
console.log(summary);

// PATTERN: Advanced Types

interface Task {
  id: string;
  title: string;
  description: string;
  dueDate: Date;
  completed: boolean;
}

type TaskCreationPayload = Omit<Task, "id" | "completed">;

const newTask: TaskCreationPayload = {
  title: "Implement feature X",
  description: "Details about feature X implementation.",
  dueDate: new Date(),
};
console.log(newTask);

// PATTERN: Advanced Types

type UserRole = "admin" | "editor" | "viewer";

interface UserDetails {
  id: number;
  name: string;
}

type RoleAssignments = Record<UserRole, UserDetails[]>;

const assignments: RoleAssignments = {
  admin: [{ id: 1, name: "Alice" }],
  editor: [{ id: 2, name: "Bob" }, { id: 3, name: "Charlie" }],
  viewer: [],
};
console.log(assignments.admin[0].name);

// PATTERN: Advanced Types

type AllColors = "red" | "green" | "blue" | "yellow" | "purple";
type PrimaryColors = "red" | "green" | "blue";

type NonPrimaryColors = Exclude<AllColors, PrimaryColors>; // "yellow" | "purple"

const myColor: NonPrimaryColors = "yellow";
// const invalidColor: NonPrimaryColors = "red"; // Error: Type '"red"' is not assignable to type '"yellow" | "purple"'.
console.log(myColor);

// PATTERN: Advanced Types

type EventType = "click" | "submit" | "change" | "focus" | "blur";
type InteractiveEvents = "click" | "submit" | "change";

type UIInteractionEvents = Extract<EventType, InteractiveEvents>; // "click" | "submit" | "change"

const event1: UIInteractionEvents = "click";
// const event2: UIInteractionEvents = "focus"; // Error: Type '"focus"' is not assignable to type '"click" | "submit" | "change"'.
console.log(event1);

// PATTERN: Advanced Types

function getUserData(userId: number) {
  return { id: userId, name: "Jane Doe", email: "jane@example.com" };
}

type UserData = ReturnType<typeof getUserData>;

const data: UserData = getUserData(123);
console.log(data.name);

type AsyncFunction = () => Promise<string>;
type AsyncReturnType = ReturnType<AsyncFunction>; // Promise<string>