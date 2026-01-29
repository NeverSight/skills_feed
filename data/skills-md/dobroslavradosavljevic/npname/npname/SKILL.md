---
name: npname
description: Validate npm package names and check availability on the registry. Use when creating new npm packages, suggesting package names, or validating package naming conventions.
license: MIT
metadata:
  author: dobroslavradosavljevic
  version: "1.0.4"
---

# npm Package Name Validation

Use this skill when helping users create new npm packages, validate package names, or check name availability on the npm registry.

## CLI Usage

Check package name availability:

```bash
npx npname <name> [names...]
```

### Options

| Option           | Description                      |
| ---------------- | -------------------------------- |
| `--validate, -v` | Validate only (no network check) |
| `--check, -c`    | Full check with detailed output  |
| `--registry, -r` | Custom registry URL              |
| `--json, -j`     | Output as JSON for scripting     |
| `--quiet, -q`    | Minimal output (exit codes only) |

### Examples

```bash
# Check single package availability
npx npname my-awesome-package

# Check multiple packages
npx npname react vue angular

# Validate without network check
npx npname "My Package" --validate

# JSON output for scripting
npx npname foo bar --json
```

## Programmatic Usage

```typescript
import npname from "npname";

// Check availability
const isAvailable = await npname("my-package");

// Validate only (no network)
const validation = npname.validate("my-package");

// Full check: validate + availability
const result = await npname.check("my-package");

// Batch check multiple names
const results = await npname.many(["name1", "name2", "name3"]);
```

## npm Naming Rules

### Errors (Invalid for all packages)

- Must be a string
- Cannot be empty
- No leading/trailing spaces
- Cannot start with `.`, `_`, or `-`
- Must be URL-safe (no special characters like `:`, `?`, etc.)
- Cannot be blacklisted names (`node_modules`, `favicon.ico`)

### Warnings (Invalid for new packages)

- Max 214 characters
- No uppercase letters
- No special characters (`~'!()*`)
- Cannot be Node.js core module names (`fs`, `http`, `path`, etc.)

### Scoped Packages

Within a scope (`@scope/name`), the name portion can:

- Start with `-` or `_`
- Use core module names
- Use reserved names

## Best Practices

When suggesting package names:

1. Use lowercase letters, numbers, and hyphens only
2. Keep names short but descriptive
3. Check availability before recommending
4. For scoped packages, use `@org/package-name` format
5. Avoid generic names that are likely taken
