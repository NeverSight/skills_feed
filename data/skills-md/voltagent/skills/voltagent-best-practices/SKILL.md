---
name: voltagent-best-practices
# prettier-ignore
description: VoltAgent architectural patterns and conventions. Covers agents vs workflows, project layout, memory, servers, and observability.
license: MIT
metadata:
  author: VoltAgent
  version: "1.0.0"
  repository: https://github.com/VoltAgent/skills
---

# VoltAgent Best Practices

Quick reference for VoltAgent conventions and patterns.

---

## Choosing Agent or Workflow

| Use | When |
| --- | --- |
| Agent | Open-ended tasks that require tool selection and adaptive reasoning |
| Workflow | Multi-step pipelines with explicit control flow and suspend/resume |

---

## Layout

```
src/
|-- index.ts
|-- agents/
|-- tools/
`-- workflows/
```

---

## Quick Snippets

### Basic Agent

```typescript
import { Agent } from "@voltagent/core";

const agent = new Agent({
  name: "assistant",
  instructions: "You are helpful.",
  model: "openai/gpt-4o-mini",
});
```

Model format is `provider/model` (for example `openai/gpt-4o-mini` or `anthropic/claude-3-5-sonnet`).

### Basic Workflow

```typescript
import { createWorkflowChain } from "@voltagent/core";
import { z } from "zod";

const workflow = createWorkflowChain({
  id: "example",
  input: z.object({ text: z.string() }),
  result: z.object({ summary: z.string() }),
}).andThen({
  id: "summarize",
  execute: async ({ data }) => ({ summary: data.text }),
});
```

### VoltAgent Bootstrap

```typescript
import { VoltAgent } from "@voltagent/core";
import { honoServer } from "@voltagent/server-hono";

new VoltAgent({
  agents: { agent },
  workflows: { workflow },
  server: honoServer(),
});
```

---

## Memory Defaults

- Use `memory` for a shared default across agents and workflows.
- Use `agentMemory` or `workflowMemory` when defaults need to differ.

---

## Server Options

- Use `@voltagent/server-hono` for Node HTTP servers.
- Use `@voltagent/server-elysia` as an alternative Node server provider.
- Use `serverless` provider for fetch runtimes (Cloudflare, Netlify).

---

## Observability Notes

- Use `VoltOpsClient` or `createVoltAgentObservability` for tracing.
- VoltAgent will auto-configure VoltOps if `VOLTAGENT_PUBLIC_KEY` and `VOLTAGENT_SECRET_KEY` are set.

---

## Recipes

Short best-practice recipes live in the embedded docs:

- `packages/core/docs/recipes/`
- Search: `rg -n "keyword" packages/core/docs/recipes -g"*.md"`
- Read: `cat packages/core/docs/recipes/<file>.md`

---

## Footguns

- Do not use `JSON.stringify` inside VoltAgent packages. Use `safeStringify` from `@voltagent/internal`.

---

## Resources

- https://voltagent.dev/docs
- https://github.com/voltagent/voltagent
- https://github.com/voltagent/voltagent/tree/main/examples
