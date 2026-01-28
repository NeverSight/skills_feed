---
name: base-app-setup
description: Complete setup guide for a Next.js app with Shadcn UI, Neon Postgres, Drizzle ORM, and AI SDK.
---

# Base App Setup

Complete setup guide for a Next.js app with Shadcn UI, Neon Postgres, Drizzle ORM, and AI SDK.

## Cookbook - Complete These Recipes in Order

### Next.js on Vercel

Create a Next.js app running on Bun, configure the development environment, and deploy to Vercel with automatic deployments on push.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/nextjs-on-vercel
```

### Editor and Linting Setup

Configure Prettier for code formatting and TypeScript for typechecking. Includes VSCode settings and EditorConfig for consistent code style. Skips ESLint/Biome to avoid config complexity.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/code-style-setup
```

### AI Coding Agent Configuration

Configure AI coding agents like Cursor, GitHub Copilot, or Claude Code with project-specific patterns, coding guidelines, and MCP servers for consistent AI-assisted development.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/agent-setup
```

### Shadcn UI & Theming

Add Shadcn UI components with dark mode support using next-themes. Includes theme provider and CSS variables configuration.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/shadcn-ui-setup
```

### Assertion Helper

TypeScript assertion function for runtime type narrowing with descriptive error messages. Based on tiny-invariant.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/assert
```

### Type-Safe Environment Configuration

Type-safe environment variable validation using Zod with a Drizzle-like schema API. Supports server/public fields, feature flags, either-or constraints, and client-side protection.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/config-schema-setup
```

### Build-Time Environment Variable Validation

Validate environment variables on server start and before builds. Catch missing or invalid variables early with clear error messages.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/env-validation
```

### Neon + Drizzle Setup

Connect a Next.js app to Neon Postgres using Drizzle ORM with optimized connection pooling for Vercel serverless functions.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/neon-drizzle-setup
```

### AI SDK & Simple Chat

Install the Vercel AI SDK with AI Elements components. Build a streaming chat interface with the useChat hook.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/ai-sdk-setup
```

### Working with Drizzle

Write type-safe database queries with Drizzle ORM. Covers select, insert, update, delete, relational queries, and adding new tables.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/using-drizzle-queries
```
