// PATTERN: Configuration Patterns

{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}

// PATTERN: Configuration Patterns

{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  },
  "include": ["src/**/*.ts"]
}

// PATTERN: Configuration Patterns

// src/types/my-library.d.ts
declare module "my-awesome-library" {
  export interface LibraryConfig {
    apiKey: string;
    debugMode?: boolean;
  }

  export function initialize(config: LibraryConfig): void;
  export function fetchData<T>(endpoint: string): Promise<T>;
}

// PATTERN: Configuration Patterns

// src/global.d.ts
declare const APP_VERSION: string;
declare const IS_PRODUCTION: boolean;

interface Window {
  myGlobalFunction: (message: string) => void;
}

declare namespace MyGlobalUtils {
  function formatCurrency(amount: number): string;
}

// PATTERN: Configuration Patterns

// src/app.ts or src/types/references.d.ts
/// <reference path="./utils.d.ts" />
/// <reference types="node" />
/// <reference lib="dom" />

// Example usage (assuming utils.d.ts declares 'formatDate')
declare function formatDate(date: Date): string; // Placeholder for utils.d.ts content
const today = new Date();
console.log(formatDate(today));