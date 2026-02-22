---
name: typescript-patterns
description: 'Advanced TypeScript patterns for strict mode development. Covers type utilities (Pick, Omit, Partial, Record, Awaited), generics with constraints and inference, type guards and narrowing, discriminated unions, conditional and mapped types, template literal types, const assertions, satisfies operator, module patterns, and modern JavaScript idioms (eslint-plugin-unicorn). Use when building type-safe APIs, preventing runtime errors through types, working with strict TypeScript configuration, debugging complex type errors, or enforcing modern JS idioms. Use for generics, type guards, utility types, strict mode, type inference, narrowing, type safety, const assertions, satisfies, module augmentation, unicorn, for-of, modern-js.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://www.typescriptlang.org/docs/'
---

# TypeScript Patterns

## Overview

Advanced TypeScript patterns that leverage the type system to prevent runtime errors. Focuses on strict mode TypeScript with patterns for type inference, narrowing, and compile-time validation. **Not** a beginner tutorial.

**When to use:** Building type-safe APIs, complex data transformations, library authoring, preventing runtime errors through types, working with strict mode flags.

**When NOT to use:** Learning TypeScript basics (primitives, interfaces, classes), JavaScript-to-TypeScript migration guidance, tooling setup, or build configuration.

## Quick Reference

| Pattern               | API                                  | Key Points                           |
| --------------------- | ------------------------------------ | ------------------------------------ |
| Utility types         | `Pick<T, K>`, `Omit<T, K>`           | Extract or exclude properties        |
| Partial/Required      | `Partial<T>`, `Required<T>`          | Make properties optional or required |
| Record type           | `Record<K, V>`                       | Object with known keys               |
| Awaited type          | `Awaited<T>`                         | Unwrap Promise return types          |
| ReturnType/Parameters | `ReturnType<F>`, `Parameters<F>`     | Extract function types               |
| Generic constraints   | `<T extends Type>`                   | Constrain generic parameters         |
| Type inference        | `type Inferred = typeof value`       | Let TypeScript infer from values     |
| Type guards           | `typeof`, `instanceof`, `in`         | Narrow types at runtime              |
| Custom type guards    | `(x): x is Type`                     | User-defined narrowing functions     |
| Inferred predicates   | `(x) => x !== null`                  | Auto-inferred type predicate filters |
| Discriminated unions  | Union with literal `type` property   | Exhaustive pattern matching          |
| Conditional types     | `T extends U ? X : Y`                | Type-level conditionals              |
| Mapped types          | `{ [K in keyof T]: T[K] }`           | Transform all properties             |
| Template literals     | `` `${A}-${B}` ``                    | String literal type manipulation     |
| Const assertions      | `as const`                           | Narrowest possible literal types     |
| Satisfies operator    | `value satisfies Type`               | Type check without widening          |
| NoInfer utility       | `NoInfer<T>`                         | Prevent inference from a position    |
| Const type params     | `<const T extends Type>`             | Narrow inference without `as const`  |
| Inline type imports   | `import { type User }`               | Import types explicitly              |
| Module augmentation   | `declare module 'lib' { ... }`       | Extend third-party types             |
| Assertion functions   | `function assert(x): asserts x is T` | Throw if type guard fails            |

## Common Mistakes

| Mistake                              | Correct Pattern                                |
| ------------------------------------ | ---------------------------------------------- |
| Using `any` without justification    | Use `unknown` and narrow with type guards      |
| Manual type assertions everywhere    | Let inference work, type function returns      |
| Destructuring before type narrowing  | Keep object intact for discriminated unions    |
| Index access without undefined check | Enable `noUncheckedIndexedAccess`              |
| `as Type` casting unsafe values      | Use `satisfies Type` to preserve narrow types  |
| Inline objects in generics           | Extract to `const` or type alias               |
| Omitting `extends` in constraints    | Always constrain generics when possible        |
| Using `Parameters<typeof fn>[0]`     | Type the parameter directly in function        |
| Not handling union exhaustiveness    | Use `never` checks in switch/if-else           |
| `value as const satisfies Type`      | Use `satisfies Type` then `as const` if needed |

## Delegation

- **Pattern discovery**: Use `Explore` agent to find existing patterns in codebase
- **Type error debugging**: Use `Task` agent for multi-step type resolution
- **Code review**: Delegate to `code-reviewer` skill for type safety audit

## References

- [Type utilities (Pick, Omit, Partial, Required, Record, Extract, Exclude, ReturnType, Parameters, Awaited)](references/type-utilities.md)
- [Generics (constraints, inference, default parameters, variance)](references/generics.md)
- [Type guards and narrowing (typeof, instanceof, in, custom guards, assertion functions)](references/type-guards.md)
- [Discriminated unions (exhaustive checking, never type, tagged unions)](references/discriminated-unions.md)
- [Conditional types (distributive conditionals, infer keyword, type-level logic)](references/conditional-types.md)
- [Mapped types (key remapping, template literals, modifiers)](references/mapped-types.md)
- [Strict mode patterns (noUncheckedIndexedAccess, exactOptionalPropertyTypes, const assertions, satisfies)](references/strict-mode.md)
- [Module patterns (inline type imports, declaration files, module augmentation, ambient types)](references/module-patterns.md)
- [Modern idioms (eslint-plugin-unicorn patterns, modern array/string/DOM APIs, ES modules)](references/modern-idioms.md)
