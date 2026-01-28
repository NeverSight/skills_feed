---
name: workflow-devkit
description: Build durable, resumable TypeScript workflows with Vercel Workflow DevKit. Use when creating long-running processes, AI agents, background jobs, multi-step pipelines, webhooks, or event-driven systems. Triggers on "workflow", "durable", "resumable", "use workflow", "use step".
---

# Workflow DevKit

Build reliable, long-running processes with automatic retries, state persistence, and observability.

## Quick Reference

| Pattern | Use Case | Key API |
|---------|----------|---------|
| **Workflows** | Orchestrate durable operations | `"use workflow"` directive |
| **Steps** | Atomic, retriable units | `"use step"` directive |
| **Webhooks** | Human-in-the-loop, callbacks | `createWebhook()` |
| **Actors** | Event-driven state machines | `defineHook()` + `for await` |
| **Streaming** | Real-time frontend updates | `getWritable()` / `run.readable` |
| **AI Agents** | Durable LLM workflows | `DurableAgent` + `globalThis.fetch = fetch` |
| **AI Gateway** | Multi-provider model switching | `"provider/model"` strings, `@ai-sdk/gateway` |

## Prerequisites

```bash
pnpm add workflow @workflow/ai ai @ai-sdk/gateway zod
```

## Core Concepts

### Workflows (`"use workflow"`)

```typescript
import { sleep } from "workflow";

export async function myWorkflow(input: string) {
  "use workflow";
  const result = await step1(input);
  await sleep("5s");
  return result;
}
```

### Steps (`"use step"`) - MUST be in SAME FILE as workflow

```typescript
async function step1(input: string) {
  "use step";
  return await fetch(`/api/data?q=${input}`).then(r => r.json());
}
```

### Error Types

```typescript
import { FatalError, RetryableError } from "workflow";

// Auto-retried
throw new Error("Transient failure");

// No retry - stops workflow
throw new FatalError("Invalid credentials");

// Custom retry timing
throw new RetryableError("Rate limited", { retryAfter: "60s" });
```

## Detailed Documentation

- [patterns.md](patterns.md) - Workflow patterns (sequential, parallel, routing, actors)
- [api-reference.md](api-reference.md) - Complete API reference
- [ai-integration.md](ai-integration.md) - AI SDK and DurableAgent patterns

## Imports Cheat Sheet

```typescript
// Core workflow
import {
  sleep, fetch, FatalError, RetryableError,
  createWebhook, createHook, defineHook,
  getWritable, getWorkflowMetadata, getStepMetadata,
} from "workflow";

// API routes
import { start, getRun } from "workflow/api";

// AI integration
import { DurableAgent } from "@workflow/ai/agent";
import { generateText, generateObject } from "ai";
import { createUIMessageStreamResponse } from "ai";
```

## Examples Directory

Reference implementations: `~/dev/workflow-examples/`

| Example | Pattern |
|---------|---------|
| `nextjs/` | Basic user signup workflow |
| `kitchen-sink/` | All patterns reference |
| `actors/` | Event-driven actor pattern |
| `ai-sdk-workflow-patterns/` | AI agent patterns |
| `flight-booking-app/` | DurableAgent with tools |
| `rag-agent/` | RAG with PostgreSQL + embeddings |
| `birthday-card-generator/` | Webhooks + scheduling |
