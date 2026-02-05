---
name: dead-code-detector
description: |
  Find and remove dead code in TypeScript/JavaScript projects. Detects unused exports (functions, types, constants never imported elsewhere), unused npm dependencies (packages in package.json never imported), and unreachable code patterns (code after returns, always-false conditions, stale TODOs). Use when: "find dead code", "check for unused exports", "clean up unused code", "find unused dependencies", "audit codebase for dead code", "what code can I delete", or before major refactors.
---

# Dead Code Detector

Detect and eliminate dead code in TypeScript/JavaScript codebases.

## Quick Start

Run the automated scanner:
```bash
node ~/.claude/skills/dead-code-detector/scripts/find-dead-code.js .
```

Output: Console report + `dead-code-report.json` with all findings.

## What Gets Detected

### 1. Unused Exports
Exported symbols never imported elsewhere in the codebase.

```typescript
// src/utils/helpers.ts
export function formatDate() { ... }  // Used
export function oldFormatter() { ... }  // DEAD - never imported
```

**False positive handling:** Automatically skips:
- Entry points (`index.ts`, `page.tsx`, `convex/` functions)
- Common type suffixes (`Props`, `Config`, `Schema`)
- Default exports (may be dynamically imported)

### 2. Unused Dependencies
Packages in `package.json` never imported anywhere.

```json
{
  "dependencies": {
    "lodash": "^4.17.21",  // DEAD - replaced by native methods
    "react": "^18.0.0"     // Used
  }
}
```

**False positive handling:** Automatically skips:
- Dev tools: typescript, eslint, prettier, vitest, jest
- Type packages: @types/*
- Build tools: webpack, vite, rollup, postcss, tailwindcss

### 3. Unreachable Code Patterns
```typescript
// Code after return
function foo() {
  return 1;
  console.log("dead");  // FLAGGED
}

// Always-false conditions
if (false) { ... }  // FLAGGED

// Stale TODOs
// TODO (2021): Fix this  // FLAGGED as stale
```

## Manual Investigation Workflow

For findings that need verification:

### Check if export is truly unused
```bash
rg "symbolName" --type ts
rg "from.*filename" --type ts  # Check imports of file
```

### Check for dynamic imports
```bash
rg "import\(['\"].*moduleName" --type ts
rg "require\(['\"].*moduleName" --type js
```

### Check if dependency is used in config
```bash
rg "packageName" *.config.* package.json
```

## Framework Considerations

Framework-specific exports that look unused but aren't:

| Framework | Safe to Keep |
|-----------|--------------|
| Next.js | `generateStaticParams`, `generateMetadata`, exports from `page.tsx`/`layout.tsx` |
| Remotion | Compositions in `Root.tsx`, `calculateMetadata` |
| Convex | All `convex/` function exports (deployed via API) |
| Express | Route handlers, middleware (registered, not imported) |

## Cleanup Workflow

1. **Run scanner** on project root
2. **Review findings** - verify each is truly dead
3. **Remove code** - delete unused exports and functions
4. **Remove dependencies** - `npm uninstall <package>`
5. **Run tests** - ensure nothing broke
6. **Commit** - "chore: remove dead code"

## Reference

For detailed patterns and edge cases, see [references/patterns.md](references/patterns.md).
