---
name: bun-validator
description: Validate Bun workspace configuration and detect common monorepo issues. Ensures proper workspace setup, dependency catalogs, isolated installs, and Bun 1.3+ best practices.
version: 1.0.0
tags:
  - bun
  - monorepo
  - workspace
  - validation
  - package-manager
---

# Bun Validator

Validates Bun workspace configuration and prevents common monorepo issues. Ensures Bun 1.3+ patterns and proper workspace isolation.

## When This Activates

- Setting up a new Bun monorepo
- Before adding dependencies to workspaces
- Auditing existing Bun workspaces
- After AI generates package.json files
- CI/CD pipeline validation

## Quick Start

```bash
python3 ~/.claude/skills/bun-validator/scripts/validate.py --root .
python3 ~/.claude/skills/bun-validator/scripts/validate.py --root . --strict
```

## What Gets Checked

### 1. Bun Version

```bash
# GOOD: v1.3+
bun --version  # 1.3.0 or higher

# BAD: v1.2 or earlier
bun --version  # 1.2.x
```

### 2. Root package.json

**GOOD - Monorepo root:**

```json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["apps/*", "packages/*"]
}
```

**BAD - Dependencies in root:**

```json
{
  "workspaces": ["apps/*"],
  "dependencies": {
    "react": "^19.0.0"  // BAD: Don't put deps in root
  }
}
```

### 3. Workspace Structure

**GOOD:**

```
my-monorepo/
├── package.json          # Root with workspaces, private: true
├── bun.lockb             # Single lockfile at root
├── apps/
│   ├── web/
│   │   └── package.json  # Own dependencies
│   └── api/
│       └── package.json  # Own dependencies
└── packages/
    ├── ui/
    │   └── package.json  # Shared package
    └── config/
        └── package.json  # Shared config
```

**BAD:**

```
my-monorepo/
├── package.json
├── apps/
│   └── web/
│       ├── package.json
│       └── bun.lockb     # BAD: Lockfile in workspace
```

### 4. Workspace Dependencies

**GOOD - Using workspace protocol:**

```json
{
  "dependencies": {
    "@myorg/ui": "workspace:*",
    "@myorg/config": "workspace:^1.0.0"
  }
}
```

**BAD - Hardcoded versions:**

```json
{
  "dependencies": {
    "@myorg/ui": "1.0.0"  // BAD: Use workspace:*
  }
}
```

### 5. Dependency Catalogs (Bun 1.3+)

**GOOD - Centralized versions:**

```json
// Root package.json
{
  "catalog": {
    "react": "^19.0.0",
    "typescript": "^5.7.0",
    "@types/node": "^22.0.0"
  }
}
```

```json
// apps/web/package.json
{
  "dependencies": {
    "react": "catalog:"  // Uses version from catalog
  }
}
```

### 6. Isolated Installs

**GOOD - Default in Bun 1.3:**
Packages can only access dependencies they explicitly declare.

**BAD - Hoisted dependencies:**

```json
// Don't disable isolation
{
  "workspaces": {
    "packages": ["apps/*"],
    "nohoist": ["**"]  // Don't do this
  }
}
```

## Bun 1.3+ Features

### Dependency Catalogs

Centralize version management:

```json
// Root package.json
{
  "catalog": {
    "react": "^19.0.0",
    "next": "^16.0.0",
    "typescript": "^5.7.0"
  }
}
```

### Interactive Updates

```bash
bun update --interactive  # Selectively update deps
```

### Dependency Chains

```bash
bun why react  # Explain why a package is installed
```

### Workspace Commands

```bash
# Install in specific workspace
bun add express --cwd apps/api

# Run script in workspace
bun run --cwd apps/web dev

# Run in all workspaces
bun run --filter '*' build
```

## Common Issues

### Issue: "Cannot find module"

**Cause:** Dependency not declared in workspace package.json

**Fix:**

```bash
bun add <package> --cwd <workspace>
```

### Issue: Multiple lockfiles

**Cause:** Running `bun install` in workspace directory

**Fix:**

```bash
rm apps/*/bun.lockb packages/*/bun.lockb
bun install  # From root only
```

### Issue: Version conflicts

**Cause:** Same package with different versions across workspaces

**Fix:** Use dependency catalogs:

```json
{
  "catalog": {
    "problematic-package": "^1.0.0"
  }
}
```

## Validation Output

```
=== Bun Workspace Validation Report ===

Bun Version: 1.3.2 ✓

Root package.json:
  ✓ private: true
  ✓ workspaces defined
  ✗ Found dependencies in root (should be empty)

Workspace Structure:
  ✓ apps/web - valid workspace
  ✓ apps/api - valid workspace
  ✓ packages/ui - valid workspace
  ✗ apps/web/bun.lockb - lockfile should only be at root

Dependencies:
  ✓ Using workspace:* protocol
  ✗ @myorg/ui uses hardcoded version "1.0.0"

Catalogs:
  ✗ No dependency catalog found (recommended for Bun 1.3+)

Summary: 3 issues found
```

## Best Practices

### 1. Always use workspace protocol

```json
"@myorg/shared": "workspace:*"
```

### 2. Use --cwd for workspace operations

```bash
bun add lodash --cwd apps/web  # NOT: cd apps/web && bun add
```

### 3. Single lockfile at root

```bash
# Only run bun install from root
bun install
```

### 4. Use catalogs for shared dependencies

```json
{
  "catalog": {
    "typescript": "^5.7.0",
    "vitest": "^3.0.0"
  }
}
```

### 5. Declare all dependencies explicitly

Each workspace should list all its dependencies - don't rely on hoisting.

## CI/CD Integration

```yaml
# .github/workflows/validate.yml
- name: Validate Bun Workspace
  run: |
    python3 ~/.claude/skills/bun-validator/scripts/validate.py \
      --root . \
      --strict \
      --ci
```

## Integration

- `linter-formatter-init` - Sets up Biome with Bun
- `project-scaffold` - Creates workspace structure
- `nextjs-validator` - Validates Next.js in workspace
