---
name: biome-validator
description: Validate Biome 2.3+ configuration and detect outdated patterns. Ensures proper schema version, domains, assists, and recommended rules. Use before any linting work or when auditing existing projects.
version: 1.0.0
tags:
  - biome
  - linter
  - formatter
  - validation
  - code-quality
---

# Biome Validator

Validates Biome 2.3+ configuration and prevents outdated patterns. Ensures type-aware linting, domains, and modern Biome features are properly configured.

## When This Activates

- Setting up linting for a new project
- Before any code quality work
- Auditing existing Biome configurations
- After AI generates biome.json
- CI/CD pipeline validation

## Quick Start

```bash
python3 ~/.claude/skills/biome-validator/scripts/validate.py --root .
python3 ~/.claude/skills/biome-validator/scripts/validate.py --root . --strict
```

## What Gets Checked

### 1. Biome Version & Schema

**GOOD - Biome 2.3+:**

```json
{
  "$schema": "https://biomejs.dev/schemas/2.3.12/schema.json"
}
```

**BAD - Old schema:**

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json"
}
```

### 2. Package Version

```json
// GOOD: v2.3+
"@biomejs/biome": "^2.3.0"

// BAD: v1.x or v2.0-2.2
"@biomejs/biome": "^1.9.0"
```

### 3. Linter Configuration

**GOOD - Biome 2.x:**

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "warn"
      }
    }
  }
}
```

### 4. Biome Assist (2.0+)

**GOOD - Using assist:**

```json
{
  "assist": {
    "actions": {
      "source": {
        "organizeImports": "on"
      }
    }
  }
}
```

**BAD - Old organizeImports location:**

```json
{
  "organizeImports": {
    "enabled": true
  }
}
```

### 5. Domains (2.0+)

**GOOD - Using domains for framework-specific rules:**

```json
{
  "linter": {
    "domains": {
      "react": "on",
      "next": "on"
    }
  }
}
```

### 6. Suppression Comments

**GOOD - Biome 2.0+ comments:**

```typescript
// biome-ignore lint/suspicious/noExplicitAny: legacy code
// biome-ignore-all lint/style/useConst
// biome-ignore-start lint/complexity
// biome-ignore-end
```

**BAD - Wrong format:**

```typescript
// @ts-ignore  // Not Biome
// eslint-disable  // Wrong tool
```

## Biome 2.3+ Features

### Type-Aware Linting

Biome 2.0+ includes type inference without requiring TypeScript compiler:

```json
{
  "linter": {
    "rules": {
      "correctness": {
        "noUndeclaredVariables": "error",
        "useAwaitThenable": "error"
      }
    }
  }
}
```

### Assist Actions

```json
{
  "assist": {
    "actions": {
      "source": {
        "organizeImports": "on",
        "useSortedKeys": "on"
      }
    }
  }
}
```

### Multi-file Analysis

Lint rules can query information from other files for more powerful analysis.

### Framework Domains

```json
{
  "linter": {
    "domains": {
      "react": "on",       // React-specific rules
      "next": "on",        // Next.js rules
      "test": "on"         // Testing framework rules
    }
  }
}
```

## Recommended Configuration

```json
{
  "$schema": "https://biomejs.dev/schemas/2.3.12/schema.json",
  "assist": {
    "actions": {
      "source": {
        "organizeImports": "on"
      }
    }
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noForEach": "off"
      },
      "style": {
        "noNonNullAssertion": "off"
      },
      "suspicious": {
        "noArrayIndexKey": "off",
        "noExplicitAny": "warn"
      },
      "correctness": {
        "useAwaitThenable": "error",
        "noLeakedRender": "error"
      }
    },
    "domains": {
      "react": "on",
      "next": "on"
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
  },
  "files": {
    "ignore": [
      "node_modules",
      "dist",
      "build",
      ".next",
      "out",
      ".cache",
      ".turbo",
      "coverage"
    ]
  }
}
```

## Deprecated Patterns

| Deprecated | Replacement (2.3+) |
|------------|-------------------|
| `organizeImports.enabled` | `assist.actions.source.organizeImports` |
| Schema < 2.0 | Schema 2.3.11+ |
| `@biomejs/biome` < 2.3 | `@biomejs/biome@latest` |
| No domains config | Use `linter.domains` for frameworks |

## Validation Output

```
=== Biome 2.3+ Validation Report ===

Package Version: @biomejs/biome@2.3.11 ✓

Configuration:
  ✓ Schema version: 2.3.11
  ✓ Linter enabled with recommended rules
  ✓ Using assist.actions for imports
  ✗ No domains configured (consider enabling react, next)
  ✓ Formatter configured

Rules:
  ✓ noExplicitAny: warn
  ✓ useAwaitThenable: error
  ✗ noLeakedRender not enabled (recommended)

Summary: 2 issues found
```

## Migration from ESLint

### Step 1: Install Biome

```bash
bun remove eslint prettier eslint-config-* eslint-plugin-*
bun add -D @biomejs/biome@latest
```

### Step 2: Create biome.json

```bash
bunx biome init
```

### Step 3: Migrate rules

```bash
bunx biome migrate eslint --write
```

### Step 4: Update scripts

```json
{
  "scripts": {
    "lint": "biome lint .",
    "lint:fix": "biome lint --write .",
    "format": "biome format --write .",
    "check": "biome check .",
    "check:fix": "biome check --write ."
  }
}
```

### Step 5: Remove old configs

```bash
rm .eslintrc* .prettierrc* .eslintignore .prettierignore
```

## VS Code Integration

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "biomejs.biome",
  "editor.codeActionsOnSave": {
    "source.organizeImports.biome": "explicit",
    "quickfix.biome": "explicit"
  }
}
```

## CI/CD Integration

```yaml
# .github/workflows/lint.yml
- name: Validate Biome Config
  run: |
    python3 ~/.claude/skills/biome-validator/scripts/validate.py \
      --root . \
      --strict \
      --ci

- name: Lint
  run: bunx biome check --error-on-warnings .
```

## Integration

- `linter-formatter-init` - Sets up Biome from scratch
- `nextjs-validator` - Validates Next.js (enable next domain)
- `bun-validator` - Validates Bun workspace
