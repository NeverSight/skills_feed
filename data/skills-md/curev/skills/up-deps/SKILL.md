---
name: up-deps
description: Update project dependencies using taze, a modern CLI tool that keeps deps fresh. Supports monorepos, version range updates, and automatic installation. Use when updating dependencies, upgrading packages, or keeping packages up-to-date.
---

# Update Dependencies Workflow

Complete workflow for updating project dependencies using [taze](https://github.com/antfu-collective/taze), a modern CLI tool that keeps your dependencies fresh.

## Quick Start

By default, `taze` safely updates versions within the ranges specified in `package.json` (same behavior as `npm install`).

```bash
npx taze
```

For monorepos, use recursive mode:

```bash
npx taze -r
```

## Update Levels

### Safe Updates (Default)

Only bump versions within allowed ranges:

```bash
npx taze
```

### Major Updates

Check and bump to latest stable versions including major (breaking) changes:

```bash
npx taze major
```

### Minor Updates

Bump to latest minor versions within the same major version:

```bash
npx taze minor
```

### Patch Updates

Bump to latest patch versions within the same minor version:

```bash
npx taze patch
```

## Workflow Steps

### 1. Check Current Dependencies

```bash
# Check package.json location
ls package.json

# For monorepos, identify all package.json files
find . -name "package.json" -not -path "*/node_modules/*"
```

### 2. Run Taze

**Basic usage:**
```bash
npx taze
```

**With options:**
```bash
# Monorepo support
npx taze -r

# Write changes to package.json
npx taze --write

# Auto-install after updating
npx taze --write --install

# Include peer dependencies
npx taze --peer

# Include locked versions (fixed versions without ^ or ~)
npx taze --include-locked
# or short form
npx taze -l

# Force fetch latest info (no cache)
npx taze --force
```

### 3. Review Changes

After running taze, review the proposed changes by checking the output. If `--write` was used, review the updated `package.json` files:

```bash
# View package.json to see updated versions
cat package.json
# or for monorepos, check each package.json
find . -name "package.json" -not -path "*/node_modules/*" -exec cat {} \;
```

**Check for:**
- Breaking changes in major updates
- Compatibility issues

### 4. Install Updated Dependencies

If `--install` wasn't used, install manually using `@antfu/ni` which automatically detects the package manager:

```bash
npx @antfu/ni
```

`@antfu/ni` automatically detects the package manager from `package.json` `packageManager` field or lock files (`pnpm-lock.yaml`, `yarn.lock`, etc.) and uses the appropriate command.

## Advanced Configuration

### Filter Packages

Include or exclude specific packages:

```bash
# Include specific packages
npx taze --include lodash,webpack

# Exclude packages
npx taze --exclude react-dom

# Use regex patterns
npx taze --include /react/ --exclude react-dom
```

### Config File (Reference Only)

**Note:** Do not create `taze.config.ts` or `taze.config.js` automatically. Only use if the project already has one.

If a `taze.config.ts` or `taze.config.js` file exists in the project, it will be used for configuration.

For a complete example configuration, see [references/taze.config.ts](references/taze.config.ts).

**Important:** Use command-line options instead of creating config files. Only reference existing config files if they are already present in the project.

## Monorepo Support

Taze has first-class monorepo support:

```bash
# Recursive mode scans all subdirectories with package.json
npx taze -r

# Automatically handles local private packages
```

**Monorepo workflow:**
1. Run `npx taze -r` to scan all packages
2. Review taze output to see proposed changes
3. Install dependencies at root level (or in each workspace)

## Complete Example

**Scenario:** Updating dependencies in a monorepo with safe updates

```bash
# 1. Check package.json locations
find . -name "package.json" -not -path "*/node_modules/*"

# 2. Run taze in recursive mode to preview changes
npx taze -r

# 3. Review taze output for proposed changes

# 4. Write changes and install
npx taze -r --write --install
```

**Scenario:** Major version updates for specific packages

```bash
# Preview updates for TypeScript
npx taze major --include typescript

# Update only TypeScript to latest major
npx taze major --include typescript --write

# Review package.json for breaking changes
cat package.json | grep typescript

# Install dependencies
npx @antfu/ni
```

## Important Notes

- **Safe by default**: Taze only updates within version ranges unless explicitly told otherwise
- **Locked versions**: Fixed versions (without `^` or `~`) are skipped by default
- **Peer dependencies**: Not included by default, use `--peer` flag
- **Monorepos**: Use `-r` flag for recursive scanning
- **No installation required**: Use `npx taze` without installing globally
- **Breaking changes**: Always review major updates carefully

## Error Handling

**If taze fails:**
1. Check network connectivity
2. Verify package.json syntax
3. Try with `--force` to bypass cache
4. Check for conflicting version ranges

**If installation fails:**
1. Clear lock file and node_modules
2. Try with different package manager
3. Check for peer dependency conflicts
4. Review package.json for syntax errors
