---
name: isentinel
description: |
    Opinionated preferences for roblox-ts development. Use when setting up new
    roblox-ts projects or when coding style/tooling decisions arise.
metadata:
    author: Christopher Buss
    version: "2026.1.29"
---

# isentinel Preferences

Opinionated tooling and patterns for roblox-ts development.

## Quick Summary

| Category          | Preference                             |
| ----------------- | -------------------------------------- |
| Package Manager   | pnpm (bun as optional runtime)         |
| Language          | TypeScript (strict + extra checks)     |
| TypeScript Config | @isentinel/tsconfig                    |
| Linting           | @isentinel/eslint-config (no Prettier) |
| Testing           | Jest-roblox, TDD approach              |
| Git Hooks         | husky + lint-staged                    |
| Commits           | Conventional Commits                   |

---

## Package Manager (pnpm)

Use pnpm as the package manager. Can use bun as runtime for scripts.

### @antfu/ni

Use `@antfu/ni` for unified package manager commands (It auto-detects the
package manager (pnpm/npm/yarn/bun) based on lockfile):

| Command       | Description          |
| ------------- | -------------------- |
| `ni`          | Install dependencies |
| `ni <pkg>`    | Add dependency       |
| `ni -D <pkg>` | Add dev dependency   |
| `nr <script>` | Run script           |
| `nu`          | Upgrade dependencies |
| `nun <pkg>`   | Uninstall dependency |
| `nci`         | Clean install        |
| `nlx <pkg>`   | Execute package      |

---

## TypeScript

Use `@isentinel/tsconfig` with the roblox preset. Strict mode plus additional
checks:

- `exactOptionalPropertyTypes`
- `noUncheckedIndexedAccess`
- `noPropertyAccessFromIndexSignature`
- `noImplicitOverride`
- `noImplicitReturns`
- `noFallthroughCasesInSwitch`

```json
{
	"extends": "@isentinel/tsconfig/roblox"
}
```

---

## Linting

Use `@isentinel/eslint-config`. No Prettier - ESLint handles formatting.

```ts
// eslint.config.ts
import { isentinel } from "@isentinel/eslint-config";

export default isentinel();
```

Fix errors with `nr lint --fix`.

---

## Error Handling

Prefer assertions over silent failing. Fail fast, fail loud.

See [error-handling.md](references/error-handling.md) for patterns.

---

## Test-Driven Development

Red → Green → Refactor:

1. Write a failing test
2. Write minimal code to pass
3. Refactor with test protection

### Simplicity Rules (in order)

1. Passes all tests
2. Expresses intent clearly
3. Contains no duplication
4. Has minimum elements

Three similar lines of code is better than a premature abstraction.

See [testing.md](references/testing.md) for Jest-roblox setup.

---

## References

| Topic             | Reference                                         |
| ----------------- | ------------------------------------------------- |
| Tooling details   | [tooling.md](references/tooling.md)               |
| TypeScript config | [typescript.md](references/typescript.md)         |
| Linting rules     | [linting.md](references/linting.md)               |
| Testing (TDD)     | [testing.md](references/testing.md)               |
| Error handling    | [error-handling.md](references/error-handling.md) |
