---
name: react-code-review-patterns
description: "Review checklists and patterns for React/TypeScript frontend code reviews. Use when: (1) reviewing React components, (2) checking TypeScript type safety, (3) validating hooks usage, (4) checking accessibility compliance."
layer: 2
tech_stack: [react, typescript, javascript]
topics: [code-review, react-patterns, typescript, hooks, accessibility, performance]
depends_on: [react-development-patterns, typescript-advanced-types]
complements: [code-review-excellence, javascript-testing-patterns]
keywords: [React, TypeScript, Hooks, useEffect, useCallback, useMemo, a11y, ARIA, React Query]
---

# React Code Review Patterns

Checklists and patterns for reviewing React/TypeScript frontend code.

## Quick Reference

| Priority | Category | Key Checks |
|----------|----------|------------|
| 1 | Security | No secrets, XSS prevention, safe innerHTML |
| 2 | Type Safety | No `any`, explicit types, proper generics |
| 3 | React Patterns | Hooks rules, component structure, keys |
| 4 | Performance | Memoization, bundle size, re-renders |
| 5 | Accessibility | ARIA, keyboard nav, semantic HTML |

## TypeScript Checklist

| Check | Required Pattern | Anti-Pattern |
|-------|------------------|--------------|
| Type annotations | Explicit types | `any`, implicit any |
| Generics | Proper constraints | `<any>` |
| Null handling | Strict null checks | `!` assertions |
| Type guards | Proper narrowing | Type casting |
| API types | Generated from schema | Manual types |
| Enums | String enums or const objects | Numeric enums |

## React Components Checklist

| Check | Required Pattern | Anti-Pattern |
|-------|------------------|--------------|
| Component type | Functional components | Class components |
| Props typing | Interface/type for props | Inline types, `any` |
| Default props | Default parameters | defaultProps |
| Children | Explicit `children` prop | Implicit |
| Fragments | `<>` or `Fragment` | Unnecessary divs |
| Keys | Stable, unique keys | Index as key |

## Hooks Checklist

| Check | Required Pattern | Anti-Pattern |
|-------|------------------|--------------|
| Hook rules | Top level only | Conditional hooks |
| Dependencies | Complete deps array | Missing deps, `// eslint-disable` |
| useEffect cleanup | Return cleanup function | Missing cleanup |
| Custom hooks | `use` prefix | Non-hook abstractions |
| useMemo/useCallback | For expensive ops | Premature optimization |

## State Management Checklist

| Check | Required Pattern | Anti-Pattern |
|-------|------------------|--------------|
| Server state | React Query | useState for API data |
| Client state | Context or useState | Redux for simple state |
| Form state | React Hook Form | Manual form handling |
| Loading states | `isLoading`, `isError` | Boolean flags |
| Optimistic updates | React Query mutations | Manual state sync |

## API Integration Checklist

| Check | Required Pattern | Anti-Pattern |
|-------|------------------|--------------|
| Data fetching | `useQuery` | `useEffect` + `fetch` |
| Mutations | `useMutation` | Direct API calls |
| Error handling | Error boundaries + query errors | Try-catch everywhere |
| Caching | React Query cache | Manual caching |

## Performance Checklist

| Check | Required Pattern | Anti-Pattern |
|-------|------------------|--------------|
| Re-renders | Memoized callbacks | Inline functions in JSX |
| Lists | Virtualization for long lists | Render all items |
| Lazy loading | `React.lazy` + Suspense | All code in bundle |
| Images | Lazy loading, proper sizes | Unoptimized images |

## Accessibility Checklist

| Check | Required Pattern | Anti-Pattern |
|-------|------------------|--------------|
| Semantic HTML | `<button>`, `<nav>`, `<main>` | `<div onClick>` |
| ARIA labels | `aria-label`, `aria-describedby` | Missing labels |
| Keyboard nav | `tabIndex`, focus management | Mouse-only interactions |
| Color contrast | WCAG AA compliant | Low contrast |
| Form labels | `<label htmlFor>` | Placeholder only |

## Testing Checklist

| Check | Required Pattern | Anti-Pattern |
|-------|------------------|--------------|
| Test coverage | Tests for components | No tests |
| Test type | Behavior tests | Implementation tests |
| Queries | `getByRole`, `getByLabelText` | `getByTestId` |
| Async | `waitFor`, `findBy` | Manual timeouts |
| Mocking | MSW for API | Mock fetch directly |

## General Checklist

| Check | Required Pattern | Anti-Pattern |
|-------|------------------|--------------|
| Console | No console.log | Debug statements |
| Comments | Explain "why" | Explain "what" |
| File size | <300 lines per component | Monolithic components |
| Imports | Absolute paths | Relative hell `../../../` |

## Common Anti-Patterns

| Anti-Pattern | Issue | Correct Pattern |
|--------------|-------|-----------------|
| `any` type | Loses type safety | Explicit types |
| Index as key | Causes re-render bugs | Stable unique ID |
| Inline functions | Re-creates on render | `useCallback` |
| `useEffect` for derived state | Unnecessary effect | Compute in render |
| `// eslint-disable` | Hiding real issues | Fix the issue |
| Direct DOM manipulation | Bypasses React | Refs or state |
| `dangerouslySetInnerHTML` | XSS risk | Sanitize or avoid |
| Missing error boundaries | Crashes whole app | Error boundary wrapper |

## References

- [references/examples.md](references/examples.md) - Code examples for patterns
