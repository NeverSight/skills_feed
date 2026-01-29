---
name: t3-dot-env-zod
description: T3 Env setup with Zod for Next.js 16+ and Vite. Use for implementing or debugging `@t3-oss/env-nextjs` or `@t3-oss/env-core` schemas, `experimental__runtimeEnv`, client/server separation, build-time validation, presets, and Zod env-safe coercions.
license: MIT
---

# T3 Env with Zod

Use T3 Env to validate and type your environment variables with Zod, with correct client/server separation and framework-aware runtime env handling.

## Workflow

1. Identify the target framework.
2. Choose the correct `createEnv` variant and runtime strategy.
3. Apply Zod patterns that are safe for env strings.
4. Add build-time validation where possible.
5. Use presets instead of hand-maintaining platform vars.

## Decision Tree

```
Is this Next.js (16+)?
  |-- Yes → use @t3-oss/env-nextjs
  |     |-- Use experimental__runtimeEnv (usually client vars only)
  |     '-- Validate on build → import env in next.config.ts
  |
  '-- Is this Vite?
        '-- Yes → use @t3-oss/env-core
              |-- clientPrefix: "VITE_"
              '-- runtimeEnv: import.meta.env
```

## References

- `references/nextjs.md`
- `references/core.md`
- `references/zod.md`
- `references/presets.md`
- `references/pitfalls.md`

## Examples

Copy/paste examples live under `examples/`:

- `examples/nextjs/nextjs-16-plus/`
- `examples/core/vite-import-meta-env/`
