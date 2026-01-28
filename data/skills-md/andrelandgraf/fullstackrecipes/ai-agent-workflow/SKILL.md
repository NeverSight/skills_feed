---
name: ai-agent-workflow
description: Build resumable multi-agent workflows with durable execution, tool loops, and automatic stream recovery on client reconnection.
---

# Multi-Agent Workflows

Build resumable multi-agent workflows with durable execution, tool loops, and automatic stream recovery on client reconnection.

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

### Better Auth Setup

Add user authentication using Better Auth with Drizzle ORM and Neon Postgres. Base setup with email/password authentication.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/better-auth-setup
```

### AI Chat Persistence with Neon

Persist AI chat conversations to Neon Postgres with full support for AI SDK message parts including tools, reasoning, and streaming. Uses UUID v7 for chronologically-sortable IDs.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/ai-chat-persistence
```

### Pino Logging Setup

Configure structured logging with Pino. Outputs human-readable colorized logs in development and structured JSON in production for log aggregation services.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/pino-logging-setup
```

## Cookbook - Complete These Recipes in Order

### Workflow Development Kit Setup

Install and configure the Workflow Development Kit for resumable, durable AI agent workflows with step-level persistence, stream resumption, and agent orchestration.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/workflow-setup
```

### Resumable AI Response Streams

Add automatic stream recovery to AI chat with WorkflowChatTransport, start/resume API endpoints, and the useResumableChat hook.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/resumable-ai-streams
```

### Custom Durable Agent

Build a custom durable AI agent with full control over streamText options, provider configs, and tool loops. Compatible with the Workflow Development Kit.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/custom-durable-agent
```

### Working with Workflows

Create and run durable workflows with steps, streaming, and agent execution. Covers starting, resuming, and persisting workflow results.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/using-workflows
```
