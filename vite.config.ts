import { defineConfig } from "vitest/config";
import { resolve } from "path";

export default defineConfig({
  base: "/treetype/", // ← CRITICAL: Base path for GitHub Pages!

  // App serving configuration
  root: ".",
  build: {
    outDir: "dist",
    // Production optimizations
    minify: "terser", // Best compression
    sourcemap: true, // For debugging production issues
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        library: resolve(__dirname, "library.html"),
      },
      output: {
        // Manual chunking for better caching
        manualChunks: {
          timer: ["./src/core/timer.ts"],
          config: ["./src/core/config.ts"],
          storage: ["./src/core/storage.ts"],
        },
      },
    },
    // Terser options for production
    terserOptions: {
      compress: {
        drop_console: false, // Keep console.log (personal use)
        drop_debugger: true, // Remove debugger statements
      },
    },
    // Report compressed size
    reportCompressedSize: true,
    // Chunk size warning limit (500 kB)
    chunkSizeWarningLimit: 500,
  },
  server: {
    port: 3000,
    open: true,
  },

  // Test configuration
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    include: ["tests/**/*.test.ts"],
    coverage: {
      provider: "v8",
      include: ["src/**/*.ts"], // Measure coverage for source files only
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "tests/",
        "**/*.test.ts",
        "dist/",
        "build/",
        "**/*.config.*",
      ],
      // Report coverage even if tests fail
      reportOnFailure: true,
      // Include all source files, even untested ones
      all: true,
      // Optional: Set coverage thresholds (remove if too strict)
      // thresholds: {
      //   lines: 80,
      //   functions: 80,
      //   branches: 75,
      //   statements: 80,
      // },
    },
  },
});
