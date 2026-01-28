---
name: eslint
description: Comprehensive ESLint agent for JavaScript/TypeScript code quality. Use when setting up ESLint, configuring linting rules, analyzing code for issues, fixing violations, or integrating ESLint into development workflows. Triggers on requests involving code quality, linting, static analysis, or ESLint configuration for JavaScript, TypeScript, React, or Node.js projects.
---

# ESLint Agent

## Overview

ESLint is a pluggable and configurable linter tool for identifying and reporting on patterns in JavaScript and TypeScript code. This skill enables Claude to help you set up, configure, and effectively use ESLint to maintain code quality across your projects.

## Quick Start

### Prerequisites

- Node.js (^18.18.0, ^20.9.0, or >=21.1.0) with SSL support
- Existing `package.json` file (run `npm init` if needed)

### Installation & Setup

**Automated Setup (Recommended):**

```bash
npm init @eslint/config@latest
```

This interactive setup will ask about your project and create an `eslint.config.js` file.

**Manual Setup:**

```bash
# Install ESLint packages
npm install --save-dev eslint@latest @eslint/js@latest

# Create configuration file
touch eslint.config.js
```

### Basic Configuration

The new flat config format (ESLint 9.0+) uses `eslint.config.js`:

```javascript
import { defineConfig } from "eslint/config";
import js from "@eslint/js";

export default defineConfig([
  {
    files: ["**/*.js"],
    plugins: { js },
    extends: ["js/recommended"],
    rules: {
      "no-unused-vars": "warn",
      "no-undef": "warn"
    }
  }
]);
```

### Running ESLint

```bash
# Lint a single file
npx eslint yourfile.js

# Lint a directory
npx eslint src/

# Lint with auto-fix
npx eslint src/ --fix
```

## Core ESLint Tasks

### 1. Setting Up ESLint

#### For JavaScript Projects

```bash
npm init @eslint/config@latest
```

Select options:

- How would you like to use ESLint? → **To check syntax, find problems, and enforce code style**
- What type of modules? → **JavaScript modules (import/export)**
- Which framework? → **None/React/Vue** (as applicable)
- Does your project use TypeScript? → **No**
- Where does your code run? → **Browser** and/or **Node**
- Config file format → **JavaScript/JSON/YAML** (JavaScript recommended)

#### For TypeScript Projects

```bash
npm install --save-dev eslint@latest @typescript-eslint/parser @typescript-eslint/eslint-plugin typescript-eslint
```

Configuration for TypeScript:

```javascript
import { defineConfig } from 'eslint/config';
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';

export default defineConfig(
  eslint.configs.recommended,
  ...tseslint.configs.recommended
);
```

#### For React + TypeScript

```bash
npm install --save-dev \
  eslint \
  @typescript-eslint/parser \
  @typescript-eslint/eslint-plugin \
  eslint-plugin-react \
  eslint-plugin-react-hooks \
  eslint-plugin-jsx-a11y \
  typescript-eslint
```

### 2. Configuring Rules

#### Rule Severity Levels

- `"off"` or `0` - Disable the rule
- `"warn"` or `1` - Warning (doesn't affect exit code)
- `"error"` or `2` - Error (exit code will be 1)

#### Common Rule Configurations

**Basic Rules:**

```javascript
export default defineConfig([
  {
    rules: {
      // Enforce semicolons
      "semi": ["error", "always"],

      // Enforce const where possible
      "prefer-const": "error",

      // Warn on unused variables
      "no-unused-vars": "warn",

      // No console.log in production
      "no-console": ["error", { allow: ["warn", "error"] }],

      // Enforce consistent quotes
      "quotes": ["error", "single"],

      // Require === instead of ==
      "eqeqeq": ["error", "always"]
    }
  }
]);
```

**TypeScript-Specific Rules:**

```javascript
export default defineConfig([
  {
    files: ["**/*.ts", "**/*.tsx"],
    rules: {
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/explicit-function-return-type": ["error", {
        allowExpressions: true
      }],
      "@typescript-eslint/naming-convention": ["error", {
        selector: "interface",
        format: ["PascalCase"],
        custom: {
          regex: "^I[A-Z]",
          match: false
        }
      }]
    }
  }
]);
```

#### Configuration Comments

Disable rules inline:

```javascript
/* eslint-disable no-console */
console.log('This is allowed');
/* eslint-enable no-console */

// Disable for single line
console.log('Debug'); // eslint-disable-line no-console

// Disable next line
// eslint-disable-next-line no-console
console.log('Debug');

// Disable specific rules
alert('foo'); // eslint-disable-line no-alert, no-undef
```

**Best Practices for Inline Disables:**

1. Use sparingly with clear justification
2. Document the reason:

   ```javascript
   // eslint-disable-next-line no-console -- Debugging production issue #1234
   console.log('User data:', userData);
   ```

3. Prefer configuration file changes over inline disables
4. Create follow-up tasks for temporary disables

### 3. File Patterns and Ignores

#### Specifying Files to Lint

```javascript
export default defineConfig([
  {
    // Only lint TypeScript files in src/
    files: ["src/**/*.ts", "src/**/*.tsx"],

    // Ignore test files for certain rules
    ignores: ["**/*.test.ts", "**/*.spec.ts"]
  }
]);
```

#### Global Ignores

```javascript
export default defineConfig([
  {
    ignores: [
      "**/node_modules/**",
      "**/dist/**",
      "**/build/**",
      "**/.next/**",
      "**/coverage/**"
    ]
  },
  // ... rest of config
]);
```

### 4. Using Shared Configurations

ESLint supports extending from popular configurations:

```javascript
import { defineConfig } from "eslint/config";
import js from "@eslint/js";
import globals from "globals";

export default defineConfig([
  js.configs.recommended, // ESLint recommended rules
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node
      }
    }
  }
]);
```

**Popular Shared Configs:**

- `eslint:recommended` - ESLint's recommended rules
- `@typescript-eslint/recommended` - TypeScript recommended
- `@typescript-eslint/strict` - Stricter TypeScript rules
- `plugin:react/recommended` - React best practices
- `plugin:react-hooks/recommended` - React Hooks rules

### 5. Auto-Fixing Issues

ESLint can automatically fix many issues:

```bash
# Fix all auto-fixable issues
npx eslint src/ --fix

# Show what would be fixed (dry run)
npx eslint src/ --fix-dry-run
```

**Auto-fixable rules include:**

- Formatting issues (spacing, semicolons, quotes)
- Simple code transformations (prefer-const, arrow functions)
- Import sorting

**Non-fixable issues** require manual intervention:

- Logic errors (no-unused-vars with actual usage)
- Complex refactoring needs

## Common Project Scenarios

### React + TypeScript Project

**Complete Configuration:**

```javascript
import { defineConfig } from 'eslint/config';
import js from '@eslint/js';
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import tseslint from 'typescript-eslint';

export default defineConfig([
  { ignores: ['dist'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        project: './tsconfig.json'
      }
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true }
      ],
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_'
      }]
    }
  }
]);
```

### Node.js + TypeScript Project

```javascript
import { defineConfig } from 'eslint/config';
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import globals from 'globals';

export default defineConfig([
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.ts'],
    languageOptions: {
      globals: globals.node
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      'no-console': 'off' // Console is fine in Node.js
    }
  }
]);
```

### Monorepo Configuration

```javascript
export default defineConfig([
  // Global ignores
  { ignores: ['**/dist/**', '**/build/**'] },

  // Frontend package
  {
    files: ['packages/frontend/**/*.{ts,tsx}'],
    languageOptions: {
      globals: globals.browser
    },
    // Frontend-specific rules
  },

  // Backend package
  {
    files: ['packages/backend/**/*.ts'],
    languageOptions: {
      globals: globals.node
    },
    // Backend-specific rules
  }
]);
```

## Integration with Development Tools

### VS Code Integration

**Install Extension:**

- ESLint extension by Microsoft (dbaeumer.vscode-eslint)

**Workspace Settings (`.vscode/settings.json`):**

```json
{
  "editor.defaultFormatter": "dbaeumer.vscode-eslint",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ]
}
```

### CI/CD Integration

**GitHub Actions:**

```yaml
name: ESLint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npx eslint .
```

**Pre-commit Hook (with Husky):**

```bash
npm install --save-dev husky lint-staged

# Add to package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "git add"]
  }
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "lint:staged": "lint-staged"
  }
}
```

## Troubleshooting

### Common Issues

**"Cannot find module 'eslint/config'"**

- Update to ESLint 9.0+: `npm install eslint@latest`

**"Parsing error: Cannot find module '@typescript-eslint/parser'"**

- Install parser: `npm install --save-dev @typescript-eslint/parser`

**Rules not being applied**

- Check file patterns match your source files
- Verify config file is named correctly (`eslint.config.js`)
- Ensure config is in project root

**Slow linting in large projects**

- Add appropriate ignores for node_modules, dist, build folders
- Use `--cache` flag: `npx eslint --cache .`
- Consider using `--max-warnings 0` to fail on warnings in CI

## Advanced Topics

### Creating Custom Rules

For project-specific patterns, see `references/custom_rules.md`.

### TypeScript Type-Aware Linting

For advanced TypeScript checks requiring type information, see `references/type_aware_linting.md`.

### Migration from ESLint 8.x

For projects using the legacy `.eslintrc.*` format, see `references/migration_guide.md`.

## Resources

### references/

- `custom_rules.md` - Guide to creating custom ESLint rules
- `type_aware_linting.md` - TypeScript type-aware linting configuration
- `migration_guide.md` - Migrating from ESLint 8.x to 9.x flat config
- `rule_reference.md` - Comprehensive rule reference with examples

### assets/

- `eslint.config.js` - Complete example configuration for various project types
- `.eslintignore` - Example ignore file patterns
