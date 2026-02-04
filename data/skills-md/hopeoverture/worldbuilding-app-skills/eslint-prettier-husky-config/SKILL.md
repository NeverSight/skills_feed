---
name: eslint-prettier-husky-config
description: This skill should be used when setting up code quality tooling with ESLint v9 flat config, Prettier formatting, Husky git hooks, lint-staged pre-commit checks, and GitHub Actions CI lint workflow. Apply when initializing linting, adding code formatting, configuring pre-commit hooks, setting up quality gates, or establishing lint CI checks for Next.js or React projects.
---

# ESLint, Prettier, Husky Configuration

## Overview

Configure comprehensive code quality tooling for Next.js/React projects using ESLint v9 (flat config), Prettier, Husky git hooks, lint-staged, and CI lint checks.

## Installation and Configuration Steps

### 1. Install Dependencies

Install required packages for ESLint v9, Prettier, and git hooks:

```bash
npm install -D eslint@^9 @eslint/js eslint-config-prettier eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y prettier husky lint-staged
```

For TypeScript projects, add:

```bash
npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin typescript-eslint
```

### 2. Create ESLint Flat Config

Create `eslint.config.mjs` in project root using the provided template from `assets/eslint.config.mjs`. This flat config format:

- Uses modern ESLint v9 configuration
- Includes React, React Hooks, and JSX accessibility rules
- Supports TypeScript with type-aware linting
- Ignores Next.js build directories and configuration files

Customize the configuration based on project needs:
- Adjust `languageOptions.parserOptions` for different ECMAScript versions
- Modify `rules` to match team preferences
- Add additional plugins as needed

### 3. Create Prettier Configuration

Create `.prettierrc` in project root using the template from `assets/.prettierrc`. This configuration:

- Sets 2-space indentation
- Uses single quotes for strings
- Removes trailing commas
- Sets 100-character line width
- Uses Unix line endings

Adjust formatting rules to match team style guide.

Create `.prettierignore` using `assets/.prettierignore` to exclude:
- Build directories (.next, dist, out)
- Dependencies (node_modules, package-lock.json)
- Generated files
- Public assets

### 4. Set Up Husky and Lint-Staged

Initialize Husky for git hooks:

```bash
npx husky init
```

This creates `.husky/` directory with a `pre-commit` hook.

Replace the pre-commit hook content with:

```bash
npx lint-staged
```

Add lint-staged configuration to `package.json` using the example from `references/package-json-config.md`:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ]
  }
}
```

This runs ESLint and Prettier on staged files before each commit.

### 5. Add Package Scripts

Add the following scripts to `package.json` (see `references/package-json-config.md` for complete example):

```json
{
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "prepare": "husky"
  }
}
```

These scripts enable:
- `npm run lint` - Check for linting errors (fails on warnings)
- `npm run lint:fix` - Auto-fix linting issues
- `npm run format` - Format all files with Prettier
- `npm run format:check` - Check formatting without modifying files
- `prepare` - Automatically set up Husky when installing dependencies

### 6. Create GitHub Actions Lint Workflow

Create `.github/workflows/lint.yml` using the template from `assets/github-workflows-lint.yml`. This workflow:

- Runs on pull requests and pushes to main/master
- Checks out code and sets up Node.js
- Installs dependencies
- Runs both linting and format checks
- Fails CI if any issues are found

Customize the workflow:
- Adjust Node.js version as needed
- Modify branch names to match repository
- Add caching for faster CI runs

### 7. Verify Setup

Test the complete setup:

1. **Lint check**: Run `npm run lint` to verify ESLint configuration
2. **Format check**: Run `npm run format:check` to verify Prettier configuration
3. **Pre-commit hook**: Make a change and commit to test Husky and lint-staged
4. **CI workflow**: Push to a branch and open a PR to verify GitHub Actions

Fix any configuration issues:
- Review ESLint errors and adjust rules if needed
- Format all files: `npm run format`
- Commit the configuration changes

### 8. Team Documentation

Document the setup for team members (see `references/team-documentation.md` for template):

- Explain the purpose of each tool
- Provide setup instructions for new developers
- Document how to temporarily bypass hooks (for emergencies only)
- Include troubleshooting steps for common issues

## Configuration Customization

### ESLint Rules

Adjust rule severity in `eslint.config.mjs`:
- `"off"` - Disable rule
- `"warn"` - Warning (doesn't fail CI)
- `"error"` - Error (fails CI)

Common customizations:
- Disable specific rules: `'react/prop-types': 'off'`
- Adjust rule options: `'max-len': ['error', { code: 120 }]`
- Add project-specific rules

### Prettier Options

Modify formatting in `.prettierrc`:
- `printWidth` - Line length limit
- `tabWidth` - Spaces per indentation level
- `semi` - Semicolon preference
- `singleQuote` - Quote style
- `trailingComma` - Trailing comma rules

### Lint-Staged Configuration

Customize pre-commit checks in `package.json`:
- Add file type patterns
- Include additional commands (tests, type checking)
- Adjust which files trigger which linters

Example with type checking:
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "tsc-files --noEmit"
    ]
  }
}
```

## Troubleshooting

**ESLint errors on existing code**: Run `npm run lint:fix` then `npm run format` to auto-fix most issues.

**Husky hooks not running**: Ensure `npm install` was run after Husky initialization. Check `.husky/pre-commit` is executable.

**CI failing but local passes**: Verify Node.js version matches between local and CI. Check that all dependencies are in `package.json`.

**Conflicts between ESLint and Prettier**: Ensure `eslint-config-prettier` is last in extends array to disable conflicting ESLint formatting rules.

## Resources

### scripts/

No executable scripts needed for this skill.

### references/

- `package-json-config.md` - Complete package.json example with all scripts and lint-staged configuration
- `team-documentation.md` - Template for documenting the setup for team members

### assets/

- `eslint.config.mjs` - ESLint v9 flat config template with React, TypeScript, and Next.js support
- `.prettierrc` - Prettier configuration with recommended settings
- `.prettierignore` - Files and directories to exclude from formatting
- `github-workflows-lint.yml` - GitHub Actions workflow for automated lint checks
