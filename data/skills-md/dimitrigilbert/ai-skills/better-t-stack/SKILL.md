---
name: better-t-stack
description: Expert guidance for using the Better-T-Stack CLI to scaffold type-safe TypeScript projects. Use when creating new projects, adding features to existing projects, or troubleshooting compatibility issues.
---

# Better-T-Stack

Better-T-Stack is a modern CLI tool for scaffolding end-to-end type-safe TypeScript projects with customizable configurations. This skill provides expert guidance for using it effectively.

## When to Use This Skill

Use this skill when:
- Creating a new TypeScript project with frontend, backend, database, ORM, auth, or addons
- Adding features (addons, deployment config) to an existing Better-T-Stack project
- Troubleshooting compatibility issues between stack components
- Deciding on the right stack combination for a project's needs
- Understanding CLI options and their interactions

## Quick Start

### Interactive Mode
```bash
npx create-better-t-stack@latest
```
Follow the prompts to choose your stack interactively.

### Non-Interactive (Recommended for Agents)
```bash
npx create-better-t-stack@latest my-project \
  --frontend tanstack-router \
  --backend hono \
  --database sqlite \
  --orm drizzle \
  --auth better-auth \
  --addons turborepo \
  --yes
```

### Add to Existing Project
```bash
cd my-existing-project
npx create-better-t-stack@latest add --addons pwa biome --install
```

## Key Commands

### `create` - Create new project
```bash
create-better-t-stack [project-directory] [options]
```
Core flags:
- `--template [template]`: Use predefined stack (choices: "mern", "pern", "t3", "uniwind", "none")
- `--frontend <type>`: tanstack-router, next, react-router, nuxt, svelte, solid, astro, native-uniwind, native-nativewind, none
- `--backend <type>`: hono, express, fastify, elysia, convex, self, none
- `--database <type>`: sqlite, postgres, mysql, mongodb, none
- `--orm <type>`: drizzle, prisma, mongoose, none
- `--auth <provider>`: better-auth, clerk, none
- `--api <type>`: trpc, orpc, none
- `--addons <types...>`: pwa, tauri, biome, turborepo, starlight, fumadocs, etc.
- `--yes`: Use defaults, skip prompts (RECOMMENDED for automation)
- `--yolo`: Bypass all validations (use with caution)

### `add` - Add to existing project
```bash
create-better-t-stack add [options]
```
Used in project directory with `bts.jsonc`. Supports adding addons and deployment configs.

## Critical Compatibility Rules

### Must-Have Pairings
- **Database + ORM**: Always required together (both must be non-`none`)
- **MongoDB**: Requires `prisma` or `mongoose` (not `drizzle`)
- **Workers runtime**: Requires `hono` backend, `drizzle` or `prisma` ORM, SQLite database

### Single-Selection Constraints
- **Web frameworks**: Only one allowed (tanstack-router, next, etc.)
- **Native frameworks**: Only one allowed (native-uniwind or native-nativewind)
- **Backend**: Only one allowed
- **Database**: Only one allowed
- **ORM**: Only one allowed

### API Compatibility
- **tRPC**: Not supported with nuxt, svelte, solid, or astro frontends (use oRPC instead)
- **oRPC**: Works with all frontends

### Frontend + Backend Rules
- **Web + Native**: Can combine one web + one native
- **Self backend** (fullstack): Only supports next, tanstack-start, nuxt, and astro
- **Convex backend**: Not compatible with solid or astro frontends

### Cloudflare Workers Constraints
```
--runtime workers REQUIRES:
  backend: hono (only)
  orm: drizzle or prisma (no mongoose)
  database: sqlite only (no postgres, mysql, mongodb)
  db-setup: d1 only (no docker)
```

### Addon Compatibility
Some addons require specific frontends:
- **PWA**: Requires tanstack-router, react-router, solid, or next
- **Tauri**: Requires tanstack-router, react-router, nuxt, svelte, solid, or next
- **Others**: No frontend restrictions

## Common Stack Patterns

### Using Predefined Templates
```bash
npx create-better-t-stack my-app --template t3
```
Available templates:
- **t3**: Modern full-stack TypeScript stack
- **mern**: MongoDB, Express, React, Node
- **pern**: PostgreSQL, Express, React, Node
- **uniwind**: React Native with NativeWind styling
- **none**: No predefined template (configure manually)

Templates set multiple options at once. You can override specific flags:
```bash
npx create-better-t-stack my-app --template t3 --database postgres
```

### Full-Stack Web App (Default)
```bash
npx create-better-t-stack my-webapp \
  --frontend tanstack-router \
  --backend hono \
  --database sqlite \
  --orm drizzle \
  --auth better-auth \
  --addons turborepo \
  --yes
```

### Backend-Only API Server
```bash
npx create-better-t-stack my-api \
  --frontend none \
  --backend fastify \
  --runtime node \
  --database postgres \
  --orm prisma \
  --api trpc \
  --yes
```

### Frontend-Only SPA
```bash
npx create-better-t-stack my-frontend \
  --frontend next \
  --backend none \
  --api none \
  --yes
```

### Web + Native App
```bash
npx create-better-t-stack my-app \
  --frontend next native-uniwind \
  --backend hono \
  --database sqlite \
  --orm drizzle \
  --auth better-auth \
  --yes
```

### Cloudflare Workers App
```bash
npx create-better-t-stack my-workers \
  --runtime workers \
  --backend hono \
  --database sqlite \
  --orm drizzle \
  --db-setup d1 \
  --yes
```

## Important Notes

### Mobile Development
When using native frontends with local backend development:
```bash
# Use machine IP, not localhost
EXPO_PUBLIC_SERVER_URL=http://192.168.1.X:3000
```

### bts.jsonc File
- Created automatically during project initialization
- Stores stack configuration for `add` command
- **Safe to delete** if you don't use `add` command
- Must exist for `add` command to work

### Programmatic API
For automation and CI/CD:
```typescript
import { init } from "create-better-t-stack";

const result = await init("my-project", {
  frontend: ["tanstack-router"],
  backend: "hono",
  database: "sqlite",
  orm: "drizzle",
  auth: "better-auth",
  yes: true
});

if (!result.success) {
  console.error(result.error);
}
```

## Best Practices

1. **Always use `--yes` flag** for agent-driven tasks to avoid interactive prompts
2. **Start with recommended defaults**, then customize as needed
3. **Validate compatibility** before generating commands - check critical rules above
4. **Use `--yolo` only when you're certain** about compatibility and want to skip validation
5. **Keep bts.jsonc** if you plan to use `add` command later
6. **Match database type to production needs** (sqlite for dev, postgres/mysql/mongodb for prod)
7. **Choose ORM based on database**: Drizzle for SQL, Mongoose for MongoDB

## Reference Documentation

For complete details on:
- All compatibility rules and validation logic: [references/COMPATIBILITY.md](references/COMPATIBILITY.md)
- Complete CLI options and flags: [references/OPTIONS.md](references/OPTIONS.md)
- Best practices and patterns: [references/BEST-PRACTICES.md](references/BEST-PRACTICES.md)
- Example setups for different use cases: [examples/SETUPS.md](examples/SETUPS.md)

## Troubleshooting

### Common Issues

**"Incompatible addon/frontend combination"**
- Check [COMPATIBILITY.md](references/COMPATIBILITY.md) for addon requirements
- Some addons (PWA, Tauri) require specific frontends

**"Cannot select multiple web frameworks"**
- Use only one web framework at a time
- Can combine one web + one native (e.g., `--frontend next native-uniwind`)

**"MongoDB database is not compatible with Cloudflare Workers runtime"**
- Workers runtime only supports SQLite with Drizzle/Prisma
- Use a different runtime or database

**"Database requires an ORM"**
- Must select both database and ORM (both non-`none`)
- MongoDB requires Mongoose or Prisma (not Drizzle)

**"Backend 'self' only supports Next.js and TanStack Start"**
- Use a different backend (hono, express, etc.) for other frontends
- Or switch frontend to next or tanstack-start
