---
name: deno-scripting
description: Guidelines for developing standalone Deno CLI scripts using TypeScript for troubleshooting, diagnostics, batch processing, and automation. Use when creating CLI tools, data processing scripts, reports, migration utilities, or any standalone TypeScript script running on Deno.
---

# Deno CLI Scripting

You are an expert in Deno and TypeScript development with deep knowledge of
building standalone CLI scripts, batch processing tools, and diagnostic
utilities using Deno's native TypeScript support and built-in tooling.

## TypeScript General Guidelines

### Basic Principles

- Use English for all code and documentation
- Always declare types for variables and functions (parameters and return
  values)
- Avoid using `any` type - create necessary types instead
- Use JSDoc to document public classes and methods
- Write concise, maintainable, and technically accurate code
- Use functional and declarative programming patterns
- No configuration needed - Deno runs TypeScript natively

### Nomenclature

- Use PascalCase for types and interfaces
- Use camelCase for variables, functions, and methods
- Use kebab-case for file and directory names
- Use UPPERCASE for environment variables
- Use descriptive variable names with auxiliary verbs: `isLoading`, `hasError`,
  `canDelete`
- Start each function with a verb

### Functions

- Write short functions with a single purpose
- Use arrow functions for simple operations and consistency
- Use async/await for asynchronous operations
- Prefer the RO-RO pattern (Receive Object, Return Object) for multiple
  parameters

### Types and Interfaces

- Prefer `type` over `interface` for object shapes in scripts
- Avoid enums; use const objects with `as const`
- Use Zod for runtime validation when needed
- Use `readonly` for immutable properties

### Type Organization

**Guide**: For projects with multiple scripts sharing types, organize types in a
dedicated directory.

#### When to Use Separate Type Files

| Project Size                  | Recommendation                      |
| ----------------------------- | ----------------------------------- |
| Single script                 | Keep types inline in the script     |
| 2-3 scripts with shared types | Create `types/index.ts`             |
| Larger projects               | Create `types/` with multiple files |

#### Directory Structure

```
project/
├── main.ts              # Config, utilities, re-exports types
├── types/
│   └── index.ts         # All shared type definitions
└── scripts/
    ├── script-a.ts      # Imports types from main.ts or types/
    └── script-b.ts
```

#### Type File Pattern

```typescript
// types/index.ts
/**
 * Shared Type Definitions
 *
 * Domain types used across multiple scripts.
 */

// =============================================================================
// Domain Types
// =============================================================================

/** User record from database */
export type User = {
  readonly id: string;
  readonly name: string;
  readonly email: string;
};

/** User with computed fields */
export type UserWithBalance = User & {
  readonly balance: string;
};

// =============================================================================
// API Response Types
// =============================================================================

export type ApiResponse<T> = {
  readonly success: boolean;
  readonly data?: T;
  readonly error?: string;
};

// =============================================================================
// Script-Specific Types (export for reuse)
// =============================================================================

/** Result of a batch operation */
export type BatchResult<T> =
  | { success: true; data: T }
  | { success: false; error: string };
```

#### Re-exporting from main.ts

```typescript
// main.ts
import "@std/dotenv/load";

// Re-export all types for convenient imports
export type {
  ApiResponse,
  BatchResult,
  User,
  UserWithBalance,
} from "./types/index.ts";

// ... rest of main.ts (config, utilities)
```

#### Importing in Scripts

```typescript
// scripts/process-users.ts
import {
  type BatchResult,
  config,
  type User,
  type UserWithBalance,
} from "../main.ts";

// Script-specific types can stay inline if not shared
type ProcessingStats = {
  total: number;
  processed: number;
  failed: number;
};
```

#### Type Naming Conventions

| Type Category   | Naming Pattern    | Example                       |
| --------------- | ----------------- | ----------------------------- |
| Domain entities | PascalCase noun   | `User`, `Transaction`         |
| With additions  | `EntityWithX`     | `UserWithBalance`             |
| API responses   | `EntityResponse`  | `TransactionResponse`         |
| State objects   | `EntityState`     | `AirdropState`                |
| Results         | `OperationResult` | `SubmitResult`, `FetchResult` |
| Status enums    | `EntityStatus`    | `TransactionStatus`           |

---

## Questions to Ask First

Before implementing, clarify these with the user to determine which patterns to
apply:

1. **Input format**: "What is the input format - JSON file, CSV file, or text
   file with one item per line?"
2. **Output format**: "Should the output be JSON, CSV, or both? Do you need a
   human-readable summary?"
3. **Environment**: "Will this run against staging/testnet or
   production/mainnet? Do you need environment switching?"
4. **Batch processing**: "How many items should be processed in parallel per
   batch? (default: 50)"
5. **Resumability**: "Should the script be resumable if interrupted? (saves
   state after each operation)"
6. **Dry run**: "Do you want a --dry-run flag to preview without making
   changes?"

---

## Guides

The following sections are **templates and patterns** to apply based on the
user's answers above. Adapt them to the specific use case.

---

## Project Structure

```
project/
├── deno.json                 # Configuration, tasks, and imports
├── .env                      # Environment variables (gitignored)
├── .env.example              # Environment variables template
├── main.ts                   # Shared configuration and utilities
└── scripts/
    ├── <script-name>.ts      # Script files
    └── ...
```

## deno.json Configuration

```json
{
  "tasks": {
    "check": "deno fmt --check && deno check scripts/*.ts",
    "<task-name>": "deno run --allow-net --allow-read --allow-write --allow-env scripts/<script-name>.ts"
  },
  "imports": {
    "@std/cli": "jsr:@std/cli@1",
    "@std/dotenv": "jsr:@std/dotenv@0.225"
  }
}
```

**Add imports based on needs:**

```bash
# Always needed
deno add jsr:@std/dotenv

# If using CLI arguments
deno add jsr:@std/cli

# If reading/writing CSV
deno add jsr:@std/csv
```

## Quality Checks

Always run before committing:

```bash
deno fmt
deno check scripts/*.ts

# Or use task
deno task check
```

## Environment Configuration

**Guide**: Always use `@std/dotenv` for environment variables. Never hardcode
secrets.

```typescript
// main.ts
import "@std/dotenv/load";

// Environment selection (if user needs staging/production switching)
export const ENV = Deno.env.get("ENV") || "production";
export const isStaging = ENV === "staging";

// Validation helper
const assertEnv = (name: string): string => {
  const value = Deno.env.get(name);
  if (!value) {
    console.error(`Error: ${name} environment variable is required`);
    Deno.exit(1);
  }
  return value;
};

// Load required env vars
export const API_KEY = assertEnv("API_KEY");

// Environment-aware URLs (if needed)
export const API_BASE = isStaging
  ? "https://staging.api.example.com"
  : "https://api.example.com";

// Environment-aware file naming (if user needs environment switching)
export const getInputFile = (baseName: string): string =>
  isStaging ? `./${baseName}.staging.json` : `./${baseName}.production.json`;

export const getOutputFile = (baseName: string): string =>
  isStaging ? `./${baseName}.staging.json` : `./${baseName}.production.json`;
```

**.env.example:**

```
ENV="production"
API_KEY="your_api_key_here"
```

## Script Structure

**Guide**: Use arrow functions throughout. Organize with clear sections.

```typescript
import "@std/dotenv/load";
import { parseArgs } from "@std/cli/parse-args";

// ============================================================
// CLI Arguments (if user wants CLI flags)
// ============================================================
const args = parseArgs(Deno.args, {
  string: ["file", "output"],
  boolean: ["dry-run"],
  default: {
    file: "input.json",
    output: "./output",
    "dry-run": false,
  },
});

// ============================================================
// Configuration
// ============================================================
const API_KEY = Deno.env.get("API_KEY");
if (!API_KEY) {
  console.error("Error: API_KEY required");
  Deno.exit(1);
}

// ============================================================
// Types
// ============================================================
type InputRecord = {
  id: string;
  // ... fields based on user's data
};

type OutputRecord = {
  id: string;
  status: "success" | "failed" | "skipped";
  // ... fields based on user's needs
};

// ============================================================
// Utilities
// ============================================================
const sleep = (ms: number): Promise<void> =>
  new Promise((resolve) => setTimeout(resolve, ms));

// ============================================================
// Core Logic
// ============================================================
const processRecord = async (record: InputRecord): Promise<OutputRecord> => {
  // Implementation based on user's requirements
};

// ============================================================
// Main
// ============================================================
const main = async (): Promise<void> => {
  // Implementation
};

main();
```

## Batch Processing

**Guide**: Apply if user needs to process many items with controlled
concurrency.

```typescript
const BATCH_SIZE = 50; // Adjust based on user's answer
const INTER_BATCH_DELAY_MS = 500;

const processBatch = async <T, R>(
  items: T[],
  processor: (item: T, index: number, total: number) => Promise<R>,
  startIndex: number,
  totalItems: number,
): Promise<R[]> => {
  const promises = items.map((item, i) =>
    processor(item, startIndex + i, totalItems)
  );
  return Promise.all(promises);
};

const processAllInBatches = async <T, R>(
  items: T[],
  processor: (item: T, index: number, total: number) => Promise<R>,
): Promise<R[]> => {
  const results: R[] = [];
  const totalBatches = Math.ceil(items.length / BATCH_SIZE);

  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE);
    const batchNum = Math.floor(i / BATCH_SIZE) + 1;

    console.log(`\n--- Batch ${batchNum}/${totalBatches} ---`);

    const batchResults = await processBatch(batch, processor, i, items.length);
    results.push(...batchResults);

    if (i + BATCH_SIZE < items.length) {
      await sleep(INTER_BATCH_DELAY_MS);
    }
  }

  return results;
};
```

## Retry with Exponential Backoff

**Guide**: Apply for any HTTP requests or external API calls.

```typescript
const MAX_RETRIES = 5;
const INITIAL_BACKOFF_MS = 1000;

const withRetry = async <T>(
  fn: () => Promise<T>,
  label: string,
): Promise<T> => {
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      if (attempt < MAX_RETRIES) {
        const backoffMs = INITIAL_BACKOFF_MS * 2 ** (attempt - 1);
        console.warn(
          `  [Retry ${attempt}/${MAX_RETRIES}] ${label} failed. Waiting ${backoffMs}ms...`,
        );
        await sleep(backoffMs);
      }
    }
  }

  throw lastError;
};
```

## Resumability Pattern

**Guide**: Apply if user wants the script to be resumable after interruption.

```typescript
type ScriptState = {
  lastUpdated: string;
  environment: string;
  summary: { total: number; success: number; failed: number; skipped: number };
  results: OutputRecord[];
};

const STATE_FILE = "./output/state.json";

const loadState = async (): Promise<ScriptState | null> => {
  try {
    const data = await Deno.readTextFile(STATE_FILE);
    return JSON.parse(data);
  } catch {
    return null;
  }
};

const saveState = async (state: ScriptState): Promise<void> => {
  await Deno.writeTextFile(STATE_FILE, JSON.stringify(state, null, 2));
};

// In main loop:
const main = async (): Promise<void> => {
  const previousState = await loadState();
  const alreadyProcessed = new Set(
    previousState?.results
      .filter((r) => r.status === "success")
      .map((r) => r.id) || [],
  );

  const results: OutputRecord[] = previousState?.results || [];

  for (const [i, record] of inputData.entries()) {
    const progress = `[${i + 1}/${inputData.length}]`;

    if (alreadyProcessed.has(record.id)) {
      console.log(`${progress} ${record.id} - SKIPPED (already done)`);
      continue;
    }

    // Process and save state after EACH operation
    // ...
    await saveState(currentState);
  }
};
```

## Reading Input Files

**Guide**: Apply based on user's input format answer.

### JSON Input

```typescript
const loadJsonInput = async <T>(filePath: string): Promise<T[]> => {
  const content = await Deno.readTextFile(filePath);
  return JSON.parse(content);
};
```

### CSV Input

```typescript
import { parse } from "@std/csv/parse";

const loadCsvInput = async <T>(
  filePath: string,
  columns: string[],
): Promise<T[]> => {
  const content = await Deno.readTextFile(filePath);
  return parse(content, { skipFirstRow: true, columns }) as T[];
};
```

### Text Input (one item per line)

```typescript
const loadTextInput = async (filePath: string): Promise<string[]> => {
  const content = await Deno.readTextFile(filePath);
  return content.split("\n").map((line) => line.trim()).filter((line) => line);
};
```

## Writing Output Files

**Guide**: Apply based on user's output format answer.

### JSON Output

```typescript
const writeJsonOutput = async <T>(filePath: string, data: T): Promise<void> => {
  await Deno.writeTextFile(filePath, JSON.stringify(data, null, 2));
  console.log(`Wrote JSON to ${filePath}`);
};
```

### CSV Output

```typescript
import { stringify } from "@std/csv/stringify";

const writeCsvOutput = async (
  filePath: string,
  columns: string[],
  rows: Record<string, unknown>[],
): Promise<void> => {
  const csv = stringify(rows, { columns });
  await Deno.writeTextFile(filePath, csv);
  console.log(`Wrote ${rows.length} rows to ${filePath}`);
};
```

### Text Summary

```typescript
const writeSummary = async (
  filePath: string,
  stats: Record<string, unknown>,
): Promise<void> => {
  const summary = `
================================================================================
SUMMARY
================================================================================
Timestamp: ${new Date().toISOString()}

${Object.entries(stats).map(([k, v]) => `${k}: ${v}`).join("\n")}
================================================================================
`.trim();

  await Deno.writeTextFile(filePath, summary);
  console.log(summary);
};
```

## Logging Format

**Guide**: Use consistent logging throughout.

```typescript
// Progress: [current/total]
const progress = `[${i + 1}/${items.length}]`;

// Status markers
console.log(`${progress} ${id} - SUCCESS`);
console.log(`${progress} ${id} - FAILED: ${error}`);
console.log(`${progress} ${id} - SKIPPED (reason)`);

// Section dividers
console.log(
  "================================================================================",
);
console.log("SECTION TITLE");
console.log(
  "================================================================================",
);

// Batch progress
console.log(`\n--- Batch ${batchNum}/${totalBatches} ---`);
```

## HTTP Requests

**Guide**: Always wrap in retry logic. Never hardcode API keys.

```typescript
const fetchData = async (url: string): Promise<unknown> => {
  return withRetry(async () => {
    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${API_KEY}` },
    });

    if (response.status === 429) {
      throw new Error("Rate limited");
    }

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
  }, `Fetching ${url}`);
};
```

## BigInt for Token Amounts

**Guide**: Apply for financial calculations to avoid floating-point errors.

```typescript
const formatUnits = (raw: bigint, decimals: number): string => {
  const divisor = BigInt(10 ** decimals);
  const whole = raw / divisor;
  const fraction = (raw % divisor).toString().padStart(decimals, "0");
  return `${whole}.${fraction}`;
};

const parseUnits = (formatted: string, decimals: number): bigint => {
  const [whole, fraction = ""] = formatted.split(".");
  const paddedFraction = fraction.padEnd(decimals, "0").slice(0, decimals);
  return BigInt(whole + paddedFraction);
};
```

## Security Model

Deno is secure by default. Request only necessary permissions:

```bash
# Run with specific permissions
deno run --allow-net --allow-read=./data --allow-env scripts/process.ts

# Permission flags
--allow-net=example.com    # Network access to specific domains
--allow-read=./path        # File read access
--allow-write=./path       # File write access
--allow-env=API_KEY        # Environment variable access
--allow-run=cmd            # Subprocess execution
```

## Built-in Tooling

```bash
# Formatting (uses Deno defaults)
deno fmt

# Linting
deno lint

# Type checking
deno check scripts/*.ts

# Dependency inspection
deno info scripts/main.ts

# Compile to standalone executable
deno compile --allow-net --allow-read --allow-env scripts/main.ts
```

## Testing with Built-in Test Runner

**Guide**: Apply when user needs automated tests for script utilities.

```typescript
// scripts/utils_test.ts
import { assertEquals, assertRejects } from "@std/assert";
import { describe, it } from "@std/testing/bdd";
import { processRecord, validateInput } from "./utils.ts";

describe("processRecord", () => {
  it("should process valid record", async () => {
    const result = await processRecord({ id: "1", name: "test" });
    assertEquals(result.status, "success");
  });

  it("should throw for invalid input", async () => {
    await assertRejects(
      () => processRecord({ id: "", name: "" }),
      Error,
      "Invalid input",
    );
  });
});
```

```bash
# Run tests
deno test --allow-net --allow-read
```

## Web Standards

Deno embraces web standards. Use these APIs:

- `fetch()` for HTTP requests
- `URL` and `URLSearchParams` for URL manipulation
- `TextEncoder` / `TextDecoder` for encoding
- `crypto.subtle` for cryptography
- `AbortController` for request cancellation

## Performance Tips

- Use web streams for large file processing
- Process items in batches to avoid memory issues
- Use `Deno.Command` for subprocess execution
- Compile to standalone executable for distribution

## Run Commands

```bash
# Format and check
deno task check

# Run with task
deno task <task-name>

# Run directly
deno run --allow-net --allow-read --allow-write --allow-env scripts/<script>.ts

# Switch environment
ENV=staging deno task <task-name>

# With CLI arguments
deno task <task-name> --file input.json --dry-run
```
