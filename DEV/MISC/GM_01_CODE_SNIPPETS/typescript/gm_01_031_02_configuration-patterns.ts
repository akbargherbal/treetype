// PATTERN: Configuration Patterns

{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}

// PATTERN: Configuration Patterns

{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}

// PATTERN: Configuration Patterns

// src/types/my-library.d.ts
declare module 'my-custom-library' {
  interface LibraryConfig {
    apiKey: string;
    timeout?: number;
  }

  function initialize(config: LibraryConfig): void;
  function fetchData<T>(url: string): Promise<T>;
}

// PATTERN: Configuration Patterns

// src/global.d.ts
declare const MY_GLOBAL_APP_NAME: string;

declare function trackAnalyticsEvent(eventName: string, data?: Record<string, any>): void;

interface Window {
  myCustomGlobalFunction: (message: string) => void;
}

// PATTERN: Configuration Patterns

// src/app.ts
/// <reference types="node" />
/// <reference path="./utils.d.ts" />

import { EventEmitter } from 'events';
import { formatMessage } from './utils';

const emitter = new EventEmitter();
console.log(formatMessage('Hello', 'TypeScript'));