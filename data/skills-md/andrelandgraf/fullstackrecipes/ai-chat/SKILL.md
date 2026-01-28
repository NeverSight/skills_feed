---
name: ai-chat
description: Build a complete AI chat application with database persistence, chat list management, and automatic title generation.
---

# AI Chat

Build a complete AI chat application with database persistence, chat list management, and automatic title generation.

## Prerequisites

Complete these recipes first (in order):

### Type-Safe Environment Configuration

Type-safe environment variable validation using Zod with a Drizzle-like schema API. Supports server/public fields, feature flags, either-or constraints, and client-side protection.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/config-schema-setup
```

### Neon + Drizzle Setup

Connect a Next.js app to Neon Postgres using Drizzle ORM with optimized connection pooling for Vercel serverless functions.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/neon-drizzle-setup
```

### Next.js on Vercel

Create a Next.js app running on Bun, configure the development environment, and deploy to Vercel with automatic deployments on push.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/nextjs-on-vercel
```

### Shadcn UI & Theming

Add Shadcn UI components with dark mode support using next-themes. Includes theme provider and CSS variables configuration.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/shadcn-ui-setup
```

### Authentication

Complete authentication system with Better Auth, email verification, password reset, protected routes, and account management.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/authentication
```

### URL State with nuqs

Sync React state to URL query parameters for shareable filters, search queries, and deep links to modal dialogs. Preserves UI state on browser back/forward navigation.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/nuqs-setup
```

### Pino Logging Setup

Configure structured logging with Pino. Outputs human-readable colorized logs in development and structured JSON in production for log aggregation services.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/pino-logging-setup
```

### Workflow Development Kit Setup

Install and configure the Workflow Development Kit for resumable, durable AI agent workflows with step-level persistence, stream resumption, and agent orchestration.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/workflow-setup
```

## Cookbook - Complete These Recipes in Order

### AI Chat Persistence with Neon

Persist AI chat conversations to Neon Postgres with full support for AI SDK message parts including tools, reasoning, and streaming. Uses UUID v7 for chronologically-sortable IDs.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/ai-chat-persistence
```

### Chat List & Management

Build a chat list page with search, rename, and delete functionality. Uses nuqs for URL-synced filters and deep-linkable modal dialogs.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/chat-list
```

### Automatic Chat Naming

Generate descriptive chat titles from the first message using a fast LLM. Runs as a background workflow step after the main response to avoid delaying the experience.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/chat-naming
```
