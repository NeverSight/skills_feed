---
name: vueuse-math-skilld
description: "ALWAYS use when writing code importing \"@vueuse/math\". Consult for debugging, best practices, or modifying @vueuse/math, vueuse/math, vueuse math, vueuse."
metadata:
  version: 14.2.1
  generated_by: Gemini CLI · Gemini 3 Flash
---

# vueuse/vueuse `@vueuse/math`

**Version:** 14.2.1 (Feb 2026)
**Deps:** @vueuse/shared@14.2.1
**Tags:** alpha: 14.0.0-alpha.3 (Sep 2025), beta: 14.0.0-beta.1 (Sep 2025), latest: 14.2.1 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- DEPRECATED: `and`, `or`, `not` — v14 deprecated in favor of original names `logicAnd`, `logicOr`, `logicNot` [source](./references/releases/v14.0.0.md)

- BREAKING: Requires Vue 3.5+ — v14 moved to Vue 3.5 as minimum version, enabling native `useTemplateRef` and `MaybeRefOrGetter` [source](./references/releases/v14.0.0.md)

- BREAKING: ESM-only — v13 dropped CommonJS (CJS) support entirely [source](./references/releases/v13.0.0.md)

- NEW: `useAverage` — reactively calculate average from an array or variadic arguments

- NEW: `useSum` — reactively calculate sum from an array or variadic arguments

- NEW: `createProjection` — create a reusable numeric projector between two numeric domains

- NEW: `createGenericProjection` — create a projector with a custom mapping function for arbitrary types

- NEW: `usePrecision` — options now include `math` property for rounding strategy (`floor`, `ceil`, `round`)

- NEW: `useClamp` — returns `ComputedRef` instead of `Ref` when input is a getter or readonly ref

- NEW: `useMath` — provides reactive access to any standard `Math` method via key name

- NEW: `logicAnd`, `logicOr`, `logicNot` — variadic reactive boolean logic supporting multiple refs

- NEW: `useMax`, `useMin` — support both array and variadic arguments for reactive comparison

- NEW: `useAbs`, `useCeil`, `useFloor`, `useRound`, `useTrunc` — dedicated reactive wrappers for common Math methods

- NEW: `useProjection` — reactive numeric projection from one domain to another

**Also changed:** `tsdown` build system v14 · `WatchSource<T>` types v14 · `MaybeRefOrGetter` native v12.8

## Best Practices

- Use `useClamp` with a mutable `ref` to create a self-validating state. When a mutable ref is passed, it returns a writable computed that automatically clamps any value assigned to it [source](./references/docs/useClamp/index.md)

```ts
// Preferred: prevents invalid state assignment
const value = useClamp(shallowRef(0), 0, 10)
value.value = 15 // state remains 10
```

- Pass reactive arrays for domains in `useProjection` to handle dynamic scaling. This is preferred for UI elements like zoomable charts or responsive sliders where the input/output boundaries change over time [source](./references/docs/useProjection/index.md)

- Define reusable mappers with `createProjection` outside component logic. This ensures consistent scaling across different parts of the application and reduces the overhead of redefining domains [source](./references/docs/createProjection/index.md)

- Leverage rest arguments in aggregation composables for ad-hoc calculations. `useSum`, `useAverage`, `useMax`, and `useMin` accept multiple refs directly, avoiding the need to create intermediate array refs

```ts
// Preferred: cleaner syntax for fixed sets of refs
const total = useSum(refA, refB, refC)
```

- Prefer `usePrecision` over `toFixed` for numeric operations. `usePrecision` returns a `number`, which prevents type-coercion bugs and allows further mathematical operations without re-parsing strings [source](./references/docs/usePrecision/index.md)

- Use explicit rounding modes in `usePrecision` for specific UI requirements. Pass the `math` option ('floor' | 'ceil' | 'round') to control how fractional values are handled in paginators or progress bars [source](./references/docs/usePrecision/index.md)

- Combine `logicAnd` or `logicOr` with `@vueuse/core`'s `whenever` for cleaner side effects. This pattern is more readable than complex manual `computed` properties when triggering actions based on multiple reactive flags [source](./references/docs/logicAnd/index.md)

- Employ `createGenericProjection` for non-linear domain mapping. Provide a custom projector function to handle logarithmic scales or custom eased transitions between numeric domains [source](./references/docs/createGenericProjection/index.md)

- Use `useMath` to reactively derive values from standard `Math` methods. It automatically wraps multiple arguments and ensures the result updates whenever any input dependency changes [source](./references/docs/useMath/index.md)

- Use `logicNot` for reactive boolean inversion in templates. It expresses intent more clearly than `!ref.value` or manual `computed` wrappers when defining visibility or disabled states
