---
name: coverage-analysis
description: Analyze test coverage, generate reports, and identify untested code. Use when improving test coverage, ensuring code quality, or preparing for production.
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# Coverage Analysis Skill

This skill helps you analyze and improve test coverage across the monorepo using Vitest's V8 coverage provider.

## When to Use This Skill

- Analyzing test coverage across packages
- Identifying untested code paths
- Setting coverage thresholds
- Generating coverage reports
- Improving test quality
- Pre-deployment coverage checks
- Code review coverage validation

## Coverage Overview

The project uses **Vitest with V8 coverage provider** for:
- **Line coverage**: Percentage of lines executed
- **Branch coverage**: Percentage of conditional branches tested
- **Function coverage**: Percentage of functions called
- **Statement coverage**: Percentage of statements executed

## Configuration

### Vitest Coverage Config

```typescript
// vitest.config.ts (root or package-level)
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node", // or "jsdom" for frontend
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html", "lcov"],
      reportsDirectory: "./coverage",
      exclude: [
        "node_modules/",
        "__tests__/",
        "**/*.test.ts",
        "**/*.spec.ts",
        "dist/",
        "build/",
        "*.config.ts",
        "*.config.js",
        ".next/",
        ".turbo/",
      ],
      include: ["src/**/*.ts", "src/**/*.tsx"],
      all: true,
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
});
```

### Package-Specific Configs

**API Package:**
```typescript
// apps/api/vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      thresholds: {
        lines: 85,      // Higher threshold for backend
        functions: 85,
        branches: 80,
        statements: 85,
      },
      exclude: [
        "__tests__/",
        "src/index.ts",  // Exclude entry point
        "src/config/**", // Exclude config files
      ],
    },
  },
});
```

**Web Package:**
```typescript
// apps/web/vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      thresholds: {
        lines: 75,      // Frontend may have lower threshold
        functions: 75,
        branches: 70,
        statements: 75,
      },
      exclude: [
        "__tests__/",
        "src/app/**",    // Exclude Next.js app directory
        "**/*.config.*",
      ],
    },
  },
});
```

**Database Package:**
```typescript
// packages/database/vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      thresholds: {
        lines: 90,      // Very high threshold for critical package
        functions: 90,
        branches: 85,
        statements: 90,
      },
      include: ["src/**/*.ts"],
      exclude: [
        "__tests__/",
        "migrations/**",  // Exclude migrations
      ],
    },
  },
});
```

## Running Coverage

### Common Commands

```bash
# Generate coverage for all packages
pnpm test:coverage

# Generate coverage for specific package
pnpm -F @sgcarstrends/api test:coverage
pnpm -F @sgcarstrends/web test:coverage
pnpm -F @sgcarstrends/database test:coverage

# Generate coverage with specific reporters
pnpm test:coverage -- --coverage.reporter=html
pnpm test:coverage -- --coverage.reporter=lcov

# Run tests and generate coverage in watch mode
pnpm test:watch -- --coverage

# Generate coverage for changed files only
pnpm test:coverage -- --changed
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:coverage:ui": "vitest --ui --coverage"
  }
}
```

## Coverage Reports

### Text Report

```bash
# Terminal output
pnpm test:coverage

# Example output:
# ----------|---------|----------|---------|---------|-------------------
# File      | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
# ----------|---------|----------|---------|---------|-------------------
# All files |   87.5  |   83.33  |   85.71 |   87.5  |
#  cars.ts  |   90    |   85     |   100   |   90    | 45-47
#  coe.ts   |   85    |   80     |   75    |   85    | 23, 56-58
# ----------|---------|----------|---------|---------|-------------------
```

### HTML Report

```bash
# Generate HTML report
pnpm test:coverage

# Open in browser
open coverage/index.html  # macOS
xdg-open coverage/index.html  # Linux
start coverage/index.html  # Windows

# HTML report features:
# - Interactive file browser
# - Line-by-line coverage visualization
# - Color-coded coverage (green = covered, red = uncovered)
# - Branch coverage details
```

### JSON Report

```bash
# Generate JSON report
pnpm test:coverage -- --coverage.reporter=json

# Output: coverage/coverage-final.json
{
  "path/to/file.ts": {
    "lines": { "1": 1, "2": 1, "3": 0 },
    "functions": { "functionName": 1 },
    "branches": { "0": [1, 0] },
    "statements": { "1": 1, "2": 1 }
  }
}
```

### LCOV Report

```bash
# Generate LCOV format (for CI tools like Codecov, Coveralls)
pnpm test:coverage -- --coverage.reporter=lcov

# Output: coverage/lcov.info
```

## Coverage Thresholds

### Setting Thresholds

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      thresholds: {
        // Global thresholds
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,

        // Per-file thresholds
        perFile: true,

        // Fail build if below thresholds
        100: false, // Don't require 100% coverage
      },
    },
  },
});
```

### Enforcing Thresholds in CI

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install
      - run: pnpm test:coverage

      # Fail if coverage below threshold
      - name: Check coverage
        run: |
          if [ $(jq '.total.lines.pct' coverage/coverage-summary.json | cut -d. -f1) -lt 80 ]; then
            echo "Coverage below 80%"
            exit 1
          fi
```

## Analyzing Coverage

### Identify Untested Files

```bash
# Generate coverage for all files (including untested)
pnpm test:coverage -- --coverage.all=true

# Find files with 0% coverage
grep -r '"pct": 0' coverage/coverage-final.json
```

### Find Uncovered Lines

```bash
# Generate HTML report and inspect
pnpm test:coverage
open coverage/index.html

# Look for red-highlighted lines in HTML report
# These are uncovered lines that need tests
```

### Check Branch Coverage

```typescript
// Example: Find uncovered branches
function processData(data: any) {
  // Branch 1: if condition
  if (data.value > 10) {
    return "high";
  }

  // Branch 2: else condition (uncovered)
  return "low";
}

// Test both branches
describe("processData", () => {
  it("should return high for values > 10", () => {
    expect(processData({ value: 15 })).toBe("high");
  });

  it("should return low for values <= 10", () => {
    expect(processData({ value: 5 })).toBe("low");
  });
});
```

## Improving Coverage

### Strategy 1: Test Untested Functions

```typescript
// Find untested function
export function calculateCOEPrice(quota: number, bids: number): number {
  // Untested
  return quota > 0 ? bids / quota : 0;
}

// Add test
describe("calculateCOEPrice", () => {
  it("should calculate price when quota is positive", () => {
    expect(calculateCOEPrice(100, 50000)).toBe(500);
  });

  it("should return 0 when quota is 0", () => {
    expect(calculateCOEPrice(0, 50000)).toBe(0);
  });
});
```

### Strategy 2: Test Error Paths

```typescript
// Original: Only happy path tested
export async function fetchCarData(month: string) {
  const res = await fetch(`/api/cars?month=${month}`);
  return res.json(); // What if fetch fails?
}

// Improved: Test error path
describe("fetchCarData", () => {
  it("should fetch data successfully", async () => {
    // Happy path test
  });

  it("should handle network errors", async () => {
    vi.spyOn(global, "fetch").mockRejectedValue(new Error("Network error"));

    await expect(fetchCarData("2024-01")).rejects.toThrow("Network error");
  });

  it("should handle non-200 responses", async () => {
    vi.spyOn(global, "fetch").mockResolvedValue({
      ok: false,
      status: 500,
    } as Response);

    await expect(fetchCarData("2024-01")).rejects.toThrow();
  });
});
```

### Strategy 3: Test Edge Cases

```typescript
// Original: Basic test
export function formatMonth(date: Date): string {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;
}

// Improved: Test edge cases
describe("formatMonth", () => {
  it("should format single-digit months", () => {
    expect(formatMonth(new Date("2024-01-01"))).toBe("2024-01");
  });

  it("should format double-digit months", () => {
    expect(formatMonth(new Date("2024-12-01"))).toBe("2024-12");
  });

  it("should handle leap years", () => {
    expect(formatMonth(new Date("2024-02-29"))).toBe("2024-02");
  });
});
```

### Strategy 4: Test Conditional Branches

```typescript
// Function with multiple branches
export function getVehicleCategory(type: string): string {
  if (type === "car") return "Category A";
  if (type === "motorcycle") return "Category B";
  if (type === "taxi") return "Category C";
  return "Unknown"; // Often forgotten!
}

// Test all branches
describe("getVehicleCategory", () => {
  it.each([
    ["car", "Category A"],
    ["motorcycle", "Category B"],
    ["taxi", "Category C"],
    ["bus", "Unknown"],
  ])("should return %s for %s", (type, expected) => {
    expect(getVehicleCategory(type)).toBe(expected);
  });
});
```

## Coverage in CI/CD

### GitHub Actions Integration

```yaml
# .github/workflows/coverage.yml
name: Coverage

on: [push, pull_request]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install
      - run: pnpm test:coverage

      # Upload coverage to Codecov
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          flags: unittests
          name: codecov-umbrella

      # Upload coverage as artifact
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
```

### Coverage Badges

```markdown
<!-- README.md -->
[![Coverage](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)
```

## Coverage Exclusions

### Exclude Specific Code

```typescript
// Exclude line
/* v8 ignore next */
console.log("Debug statement");

// Exclude block
/* v8 ignore start */
if (process.env.NODE_ENV === "development") {
  console.log("Development only");
}
/* v8 ignore stop */

// Exclude function
/* v8 ignore next 5 */
function debugHelper() {
  // This entire function is excluded
  console.log("Debug");
}
```

### Exclude Files/Directories

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      exclude: [
        // Test files
        "**/__tests__/**",
        "**/*.test.ts",
        "**/*.spec.ts",

        // Config files
        "**/*.config.ts",
        "**/*.config.js",

        // Build output
        "dist/**",
        "build/**",
        ".next/**",

        // Specific files
        "src/index.ts",
        "src/generated/**",

        // External dependencies
        "node_modules/**",
      ],
    },
  },
});
```

## Monorepo Coverage

### Aggregate Coverage

```bash
# Generate coverage for all packages
pnpm -r test:coverage

# Merge coverage reports (requires custom script)
node scripts/merge-coverage.js
```

### Custom Merge Script

```typescript
// scripts/merge-coverage.ts
import { readFileSync, writeFileSync } from "fs";
import { glob } from "glob";

const coverageFiles = glob.sync("**/coverage/coverage-final.json", {
  ignore: ["node_modules/**"],
});

const merged: any = {};

for (const file of coverageFiles) {
  const coverage = JSON.parse(readFileSync(file, "utf-8"));
  Object.assign(merged, coverage);
}

writeFileSync("coverage-merged.json", JSON.stringify(merged, null, 2));
console.log("Coverage merged successfully");
```

## Best Practices

### 1. Set Realistic Thresholds

```typescript
// ❌ Too strict (100% is often impractical)
thresholds: {
  lines: 100,
  functions: 100,
  branches: 100,
  statements: 100,
}

// ✅ Realistic and achievable
thresholds: {
  lines: 80,
  functions: 80,
  branches: 75,
  statements: 80,
}
```

### 2. Exclude Generated Code

```typescript
// vitest.config.ts
coverage: {
  exclude: [
    "src/generated/**",
    "*.config.*",
    "__tests__/**",
  ],
}
```

### 3. Focus on Critical Paths

```typescript
// Prioritize testing:
// 1. Business logic
// 2. Data transformations
// 3. API endpoints
// 4. Error handling

// Less critical:
// - UI components (test functionality, not styling)
// - Configuration files
// - Type definitions
```

### 4. Track Coverage Over Time

```bash
# Store coverage in git (add to .gitignore exceptions)
!coverage/coverage-summary.json

# Track changes
git diff coverage/coverage-summary.json
```

## Troubleshooting

### Coverage Not Generated

```bash
# Issue: No coverage directory created
# Solution: Ensure tests are running

pnpm test # First run tests
pnpm test:coverage # Then generate coverage
```

### Low Coverage Despite Tests

```bash
# Issue: Coverage config excludes tested files
# Solution: Check exclude patterns

# vitest.config.ts
coverage: {
  exclude: [
    // Remove overly broad patterns
    // "src/**", // ❌ This excludes everything!
  ],
}
```

### Coverage Report Empty

```bash
# Issue: Tests passing but coverage 0%
# Solution: Ensure coverage.all is true

coverage: {
  all: true, // Include all source files
  include: ["src/**/*.ts"],
}
```

### Threshold Failures

```bash
# Issue: Coverage below threshold
# Solution: Add missing tests or adjust thresholds

# Lower threshold temporarily
thresholds: {
  lines: 70, // Reduced from 80
}

# Or add tests to increase coverage
```

## References

- Vitest Coverage: https://vitest.dev/guide/coverage
- V8 Coverage: https://v8.dev/blog/javascript-code-coverage
- Istanbul (alternative): https://istanbul.js.org
- Related files:
  - `vitest.config.ts` - Coverage configuration
  - Root CLAUDE.md - Testing guidelines

## Best Practices Summary

1. **Set Realistic Thresholds**: 80% is good, 100% is often impractical
2. **Exclude Non-Critical Code**: Config files, generated code, tests
3. **Focus on Critical Paths**: Business logic, APIs, error handling
4. **Test All Branches**: Ensure conditional logic is tested
5. **Track Over Time**: Monitor coverage trends
6. **Use HTML Reports**: Visualize uncovered lines
7. **Integrate with CI**: Enforce thresholds in pipelines
8. **Don't Game Coverage**: Write meaningful tests, not just for coverage
