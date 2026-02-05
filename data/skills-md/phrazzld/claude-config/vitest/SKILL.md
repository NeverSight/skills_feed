---
name: vitest
description: |
  Vitest configuration best practices for pools, performance, coverage, and mocking.
  Use when: auditing vitest.config.ts, optimizing CI, debugging test failures,
  configuring coverage, troubleshooting mocking, upgrading to Node 22+.
user-invocable: true
---

# Vitest Best Practices

For test philosophy (behavior vs implementation, TDD workflow, when to mock), see `/testing-philosophy`.

## Critical Rules

1. **Node 22+**: Use `pool: 'forks'` - threads have known issues
2. **CI optimization**: Single worker, disable watch, enable `isolate: false` if safe
3. **Coverage**: Always define `coverage.include` - defaults exclude too much
4. **Mocking**: Prefer `vi.spyOn` over `vi.mock` - avoids hoisting footguns
5. **RTL cleanup**: Requires `globals: true` in config

## Quick Reference

### Pool Selection (Node 22+)

| Pool | Use When | Avoid When |
|------|----------|------------|
| `forks` | Node 22+, default choice | - |
| `threads` | Node <22, CPU-bound tests | Node 22+ (native fetch issues) |
| `vmThreads` | Need isolation + speed | Memory-constrained CI |

### CI Configuration

```typescript
export default defineConfig({
  test: {
    pool: 'forks',
    poolOptions: {
      forks: {
        singleFork: true,  // CI: predictable, less overhead
      },
    },
    isolate: false,        // Faster if tests don't leak state
    reporters: ['verbose'],
    coverage: {
      reportOnFailure: true,
    },
  },
})
```

### Coverage Quick Reference

```typescript
coverage: {
  provider: 'v8',          // Accurate in Vitest 3.2+
  include: ['src/**'],     // ALWAYS define - defaults miss files
  reporter: ['text', 'lcov'],
  reportOnFailure: true,   // Get coverage even on test failure
}
```

### Mocking Quick Reference

```typescript
// PREFER: vi.spyOn - explicit, no hoisting issues
const spy = vi.spyOn(service, 'method').mockReturnValue('mocked')

// AVOID unless necessary: vi.mock - hoisted, can't use imports
vi.mock('./module', () => ({ fn: vi.fn() }))
```

## Reference Files

- [Pool Configuration](./references/pool-configuration.md) - threads vs forks vs vmThreads
- [Performance Patterns](./references/performance-patterns.md) - CI optimization, sharding
- [Coverage Strategy](./references/coverage-strategy.md) - v8 vs Istanbul, thresholds
- [Mocking Pitfalls](./references/mocking-pitfalls.md) - vi.mock hoisting, cleanup
