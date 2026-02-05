---
name: nextfriday-best-practices
description: Next Friday coding standards - naming conventions, code style, imports, types, React/JSX patterns, Next.js rules. Use when writing or reviewing TypeScript/React/Next.js code.
user-invocable: false
---

# Next Friday Best Practices

Essential coding standards for Next Friday projects. This skill covers 41 rules across 7 topics.

## Topics

| Topic | Rules | Reference |
| ----- | ----- | --------- |
| Variable Naming | 5 | [variable-naming.md](variable-naming.md) |
| File Naming | 4 | [file-naming.md](file-naming.md) |
| Code Style | 13 | [code-style.md](code-style.md) |
| Imports | 3 | [imports.md](imports.md) |
| Types | 6 | [types.md](types.md) |
| React/JSX | 8 | [react-jsx.md](react-jsx.md) |
| Next.js | 2 | [nextjs.md](nextjs.md) |

## Quick Reference

When writing or reviewing code, ensure:

**Naming**
- Boolean variables use prefixes: `is`, `has`, `should`, `can`, `did`, `will`
- Constants use SCREAMING_SNAKE_CASE
- Files use kebab-case (.ts/.js), PascalCase (.tsx/.jsx), SNAKE_CASE (.md)

**Code Style**
- Use guard clauses with early returns
- Use async/await over .then() chains
- Use function declarations over arrow functions in .ts files
- Add blank lines after multi-line blocks and before return statements

**Imports**
- Use absolute imports, not relative with `../`
- Use `import type` for type-only imports

**Types**
- Props interfaces end with `Props` suffix
- Wrap component props with `Readonly<>`
- Always specify explicit return types

**React/JSX**
- Wrap lazy components in Suspense
- Extract inline objects in JSX to const variables
- Destructure props inside component body, not in parameters

**Next.js**
- Use `NEXT_PUBLIC_` prefix for client-side env vars
- No fallback values for env vars
