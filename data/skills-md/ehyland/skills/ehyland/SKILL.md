---
name: ehyland
description: Eamon Hyland's opinionated tooling and conventions for TypeScript projects. Use when setting up new projects, configuring a linter, monorepos, library publishing, or when the user mentions Eamon's preferences.
metadata:
  author: Eamon Hyland
  version: "2026.2.08"
---

# Eamon Hyland's Preferences

| Category | Preference |
|----------|------------|
| Package Manager | Bun for apps, pnpm for libraries |
| Language | TypeScript (strict mode, ESM only) |
| Linting & Formatting | Oxlint and Oxfmt |
| Testing | Bun for apps, Vitest for libraries |
| Git Hooks | simple-git-hooks + lint-staged |
| Bundler | Bun for apps, tsdown for libraries |

---

## Core Conventions

### Server environment configuration

- Server configuration should be loaded from environment variables and validated with zod
- Default values should be set for dev environment
- Test defaults can be set in the test runner (e.g. bun test or vitest setup script)

Configuration should be defined in `src/config.ts` or `src/server/config.ts` (for fullstack apps)


```ts
// src/config.ts
import { z } from "zod";

const configSchema = z.object({
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  DATABASE_URL: z.string().default("sqlite.db"),
});

const parsed = configSchema.safeParse(process.env);

if (!parsed.success) {
  console.error("❌ Invalid environment variables:", parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const config = parsed.data
```

```ts
// src/config.ts
import { z } from "zod";

const configSchema = z.object({
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  DATABASE_URL: z.string().default("sqlite.db"),
});

const parsed = configSchema.safeParse(process.env);

if (!parsed.success) {
  console.error("❌ Invalid environment variables:", parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const config = parsed.data
```

```ts
// src/test/setup.ts
process.env.DATABASE_URL = ":memory:";
```

### client -> server communication

- Prefer trpc with react query for fullstack projects (when the server and client are in the same package). See [bun-trpc-setup](./references/bun-trpc-setup.md).
- Otherwise prefer graphql. See [bun-graphql-setup](./references/bun-graphql-setup.md).

### TypeScript

- Never use `@ts-ignore`
- Never use `as any` casting or `as unknown as <some-other-type>`

Preferred `tsconfig.json` config

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noUncheckedIndexedAccess": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  }
}
```

### Package.json scripts

The following are my preferred set of package.json scripts. 
Not all scripts are relevant to all projects e.g. library packages will not have db scripts

```jsonc
{
  "scripts": {
    "dev": "bun run --watch src/index.ts",
    
    "db:generate": "drizzle-kit generate",
    "db:studio": "drizzle-kit studio",
    
    "typecheck": "tsc --noEmit",
    
    "format": "oxfmt src",
    "format:check": "oxfmt src --check",

    "lint": "oxlint --type-aware",
    "lint:fix": "oxlint --type-aware --fix --fix-suggestions --fix-dangerously",

    "fix": "bun format && bun lint:fix",

    "check": "concurrently 'bun:format' 'bun:lint:fix' 'bun:typecheck' 'bun:test' 'bun:test:e2e'",
    
    "test": "bun test",
    "test:e2e": "playwright test"
  }
}
```

### Linting Setup

Use Oxlint and Oxfmt from [OXC](https://oxc.rs)

```json
// .oxlintrc.json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["typescript"],
  "rules": {
    "typescript/no-floating-promises": "error",
    "typescript/no-unsafe-assignment": "warn"
  }
}
```

```json
// .oxfmtrc.json
{
  "$schema": "./node_modules/oxfmt/configuration_schema.json",
  "trailingComma": "all",
  "printWidth": 80,
  "ignorePatterns": []
}
```

Fix linting errors & formatting errors with fix script, e.g. `bun run fix` or `pnpm run fix`.

### Git Hooks

Use npm dependencies `simple-git-hooks` & `lint-staged`

```json
{
  "simple-git-hooks": {
    "pre-commit": "pnpm i --frozen-lockfile --ignore-scripts --offline && pnpm lint-staged"
  },
  "lint-staged": { "*": "pnpm fix" },
  "scripts": { "prepare": "pnpm simple-git-hooks" }
}
```

### Test Conventions

- Test files: `foo.ts` → `foo.test.ts` (same directory)
- Use `describe`/`it` API (not `test`)

---

## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Bun and tRPC Setup | Configuration for Bun.serve with native routes and tRPC fetch adapter | [bun-trpc-setup](./references/bun-trpc-setup.md) |
| Bun and GraphQL Setup | Configuration for Bun.serve with Yoga GraphQL | [bun-graphql-setup](./references/bun-graphql-setup.md) |
| SQLite with Drizzle | SQLite setup with Drizzle ORM in Bun runtime, schema, migrations, testing | [sqlite-drizzle](./references/sqlite-drizzle.md) |
| Deployment and CI/CD Setup | Buildkite pipelines, docker configuration | [deployment](./references/deployment.md) |
