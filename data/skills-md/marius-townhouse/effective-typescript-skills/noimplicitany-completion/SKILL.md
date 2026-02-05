---
name: noimplicitany-completion
description: Use when finishing TypeScript migration. Use when enabling strict mode. Use when finalizing tsconfig. Use when ensuring type safety. Use when completing adoption.
---

# Don't Consider Migration Complete Until You Enable noImplicitAny

## Overview

`noImplicitAny` is the cornerstone of TypeScript's type safety. When disabled, TypeScript silently gives variables the `any` type when it can't infer a type. This defeats the purpose of TypeScript. Don't consider your migration complete until you've enabled `noImplicitAny` and eliminated all implicit anys.

## When to Use This Skill

- Finishing TypeScript migration
- Enabling strict mode
- Finalizing tsconfig configuration
- Ensuring type safety
- Completing TypeScript adoption

## The Iron Rule

**Enable `noImplicitAny` to complete your TypeScript migration. Eliminate all implicit anys for full type safety.**

## Example

```typescript
// With noImplicitAny: false (default during migration)
function parse(data) {
  // data is implicitly any - no error!
  return data.json();
}

// With noImplicitAny: true
function parse(data) {
  // Error: Parameter 'data' implicitly has an 'any' type
  return data.json();
}

// Fixed with explicit type
function parse(data: string): unknown {
  return JSON.parse(data);
}
```

## Enabling Strict Mode

```json
{
  "compilerOptions": {
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 83: Don't Consider Migration Complete Until You Enable noImplicitAny
