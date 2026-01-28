---
name: linter-formatter-init
description: Set up Biome (default) or ESLint + Prettier, Vitest testing, and pre-commit hooks for any JavaScript/TypeScript project. Uses Bun as the package manager. Use this skill when initializing code quality tooling for a new project or adding linting to an existing one.
---

# Linter Formatter Init

Set up comprehensive linting, formatting, and testing for JavaScript/TypeScript projects using **Biome 2.3+** (default), **Vitest**, and **Bun**.

**IMPORTANT**: Always uses Biome 2.3+ (latest) - never older versions.

## Purpose

This skill automates the setup of:

- **Biome** for linting + formatting (default, recommended)
- **Vitest** for testing with coverage (use `--vitest` flag)
- ESLint + Prettier (legacy, use `--eslint` flag)
- Husky + lint-staged for pre-commit hooks
- VS Code/Cursor settings for auto-format on save
- bun scripts for manual linting, formatting, and testing

## When to Use

Use this skill when:

- Starting a new JS/TS project
- Adding linting to an existing project without tooling
- Standardizing code quality across a team
- Setting up pre-commit hooks to enforce quality

## Quick Start

```bash
# Default setup (Biome) - RECOMMENDED
python3 ~/.claude/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project

# Use ESLint + Prettier instead (legacy)
python3 ~/.claude/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --eslint

# ESLint + Prettier with TypeScript
python3 ~/.claude/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --eslint \
  --typescript

# Skip pre-commit hooks
python3 ~/.claude/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --no-hooks

# Add Vitest testing with 80% coverage threshold
python3 ~/.claude/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --vitest

# Full setup: Biome + Vitest + Husky
python3 ~/.claude/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --vitest \
  --coverage 80
```

## What Gets Installed

### Dependencies

**Biome 2.3+ (default):**

- @biomejs/biome@latest (always latest, minimum 2.3+)

**Vitest (with --vitest):**

- vitest
- @vitest/coverage-v8

**ESLint + Prettier (legacy, with --eslint):**

- eslint
- prettier
- eslint-config-prettier
- eslint-plugin-prettier
- @typescript-eslint/parser (if --typescript)
- @typescript-eslint/eslint-plugin (if --typescript)

**Pre-commit hooks:**

- husky
- lint-staged

### Configuration Files (Biome - Default)

```
project/
├── biome.json              # Biome config (lint + format)
├── .vscode/
│   └── settings.json       # Auto-format on save
├── .husky/
│   └── pre-commit          # Pre-commit hook
└── package.json            # Updated with scripts + lint-staged
```

### Configuration Files (ESLint + Prettier - Legacy)

```
project/
├── .eslintrc.json          # ESLint config
├── .prettierrc             # Prettier config
├── .prettierignore         # Prettier ignore patterns
├── .eslintignore           # ESLint ignore patterns
├── .vscode/
│   └── settings.json       # Auto-format on save
├── .husky/
│   └── pre-commit          # Pre-commit hook
└── package.json            # Updated with scripts + lint-staged
```

### Bun Scripts Added (Biome)

```json
{
  "scripts": {
    "lint": "biome lint .",
    "lint:fix": "biome lint --write .",
    "format": "biome format --write .",
    "format:check": "biome format .",
    "check": "biome check .",
    "check:fix": "biome check --write ."
  }
}
```

### Bun Scripts Added (Vitest)

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

### Bun Scripts Added (ESLint + Prettier)

```json
{
  "scripts": {
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

## Biome Configuration (Default)

Biome is a fast, all-in-one linter and formatter. The default config includes:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.3.12/schema.json",
  "assist": {
    "actions": {
      "source": { "organizeImports": "on" }
    }
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": { "noForEach": "off" },
      "style": { "noNonNullAssertion": "off" },
      "suspicious": { "noArrayIndexKey": "off", "noExplicitAny": "warn" }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "es5",
      "semicolons": "always"
    }
  }
}
```

### Customization

After setup, customize `biome.json` to adjust:

- Linting rules
- Formatting preferences
- File ignore patterns

## Vitest Configuration (with --vitest)

When you use the `--vitest` flag, this skill creates a `vitest.config.ts`:

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node", // or "jsdom" for frontend
    include: ["src/**/*.{test,spec}.{ts,tsx}", "**/*.{test,spec}.{ts,tsx}"],
    exclude: ["node_modules", "dist", ".next", "build"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html", "lcov"],
      include: ["src/**/*.ts", "src/**/*.tsx"],
      exclude: ["src/**/*.test.ts", "src/**/*.spec.ts", "src/**/*.d.ts"],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
    },
    mockReset: true,
    restoreMocks: true,
  },
});
```

### Coverage Thresholds

Default threshold is 80%. Customize with:

```bash
python3 ~/.claude/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --vitest \
  --coverage 90  # Set to 90%
```

### Test Setup File

Creates `src/test/setup.ts` for global test configuration:

```typescript
import { expect, afterEach } from "vitest";
import { cleanup } from "@testing-library/react"; // For React projects

// Cleanup after each test
afterEach(() => {
  cleanup();
});
```

## Pre-commit Hooks

When enabled (default), lint-staged runs on every commit:

**Biome (default):**

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,json,css}": ["bunx biome check --write"]
  }
}
```

**ESLint + Prettier (legacy):**

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml,yaml}": ["prettier --write"]
  }
}
```

This ensures:

- All committed code passes linting
- All committed code is formatted
- No broken code enters the repo

## VS Code / Cursor Integration

The skill creates `.vscode/settings.json`:

**Biome (default):**

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "biomejs.biome",
  "editor.codeActionsOnSave": {
    "source.organizeImports.biome": "explicit",
    "quickfix.biome": "explicit"
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  }
}
```

**ESLint + Prettier (legacy):**

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

## Why Biome Over ESLint + Prettier?

- **Faster**: Written in Rust, 10-100x faster than ESLint + Prettier
- **Simpler**: One tool instead of two, one config file
- **No conflicts**: No need for eslint-config-prettier or similar workarounds
- **Better defaults**: Sensible rules out of the box

## Monorepo Support

For monorepos, run from the root:

```bash
python3 ~/.claude/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/monorepo \
  --monorepo
```

This adds root-level config that applies to all packages.

## Troubleshooting

### Pre-commit hooks not running

```bash
# Reinstall husky
bunx husky
chmod +x .husky/pre-commit
```

### Format on save not working (Biome)

1. Install the Biome extension in VS Code/Cursor
2. Set Biome as default formatter
3. Enable "Format on Save" in settings

### Format on save not working (ESLint + Prettier)

1. Install the Prettier extension in VS Code/Cursor
2. Set Prettier as default formatter
3. Enable "Format on Save" in settings

## Framework-Specific Configs (ESLint mode only)

When using `--eslint`, the skill detects common frameworks and adjusts config:

- **Next.js**: Adds `next/core-web-vitals` to ESLint
- **React**: Adds `eslint-plugin-react` and `eslint-plugin-react-hooks`
- **NestJS**: Adds rules for decorators and DI patterns

## Manual Setup (Alternative)

If you prefer manual setup over the script:

**Biome:**

```bash
bun add -D @biomejs/biome husky lint-staged
bunx biome init
bunx husky
```

**ESLint + Prettier:**

```bash
bun add -D eslint prettier eslint-config-prettier eslint-plugin-prettier husky lint-staged
bun add -D @typescript-eslint/parser @typescript-eslint/eslint-plugin
bunx eslint --init
bunx husky
```

Then copy configs from `~/.claude/skills/linter-formatter-init/assets/configs/`
