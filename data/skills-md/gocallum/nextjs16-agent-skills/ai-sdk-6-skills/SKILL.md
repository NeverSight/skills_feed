---
name: ai-sdk-6-skills
description: AI SDK 6 Beta overview, agents, tool approval, Groq (Llama), and Vercel AI Gateway. Key breaking changes from v5 and new patterns.
---

## Links

- AI SDK 6 Beta Docs: https://v6.ai-sdk.dev/docs/announcing-ai-sdk-6-beta
- Groq Provider: https://v6.ai-sdk.dev/providers/ai-sdk-providers/groq
- Vercel AI Gateway: https://v6.ai-sdk.dev/providers/ai-sdk-providers/ai-gateway
- AI SDK GitHub: https://github.com/vercel/ai
- Groq Console Models: https://console.groq.com/docs/models

## Installation

```sh
pnpm add ai@beta @ai-sdk/openai@beta @ai-sdk/react@beta @ai-sdk/groq@beta
```

**Note**: Pin versions during beta as breaking changes may occur in patch releases.

## What's New in AI SDK 6?

### 1. **Agent Abstraction** (New)

Unified interface for building agents with full control over execution flow, tool loops, and state management.

```typescript
import { ToolLoopAgent } from 'ai';
import { tool } from 'ai';
import { z } from 'zod';

const weatherTool = tool({
  description: 'Get weather for a location',
  inputSchema: z.object({ city: z.string() }),
  execute: async ({ city }) => ({ temperature: 72, condition: 'sunny' }),
});

const agent = new ToolLoopAgent({
  model: 'groq/llama-3.3-70b-versatile', // or any model
  instructions: 'You are a helpful weather assistant.',
  tools: { weather: weatherTool },
});

// Use the agent
const result = await agent.generate({
  prompt: 'What is the weather in San Francisco?',
});

console.log(result.output);
```

### 2. **Tool Execution Approval** (New)

Request user confirmation before executing sensitive tools.

```typescript
import { tool } from 'ai';
import { z } from 'zod';

const paymentTool = tool({
  description: 'Process a payment',
  inputSchema: z.object({
    amount: z.number(),
    recipient: z.string(),
  }),
  needsApproval: true, // Require approval
  execute: async ({ amount, recipient }) => {
    return { success: true, id: 'txn-123' };
  },
});
```

Client-side approval UI:

```typescript
export function PaymentToolView({ invocation, addToolApprovalResponse }) {
  if (invocation.state === 'approval-requested') {
    return (
      <div>
        <p>Process payment of ${invocation.input.amount} to {invocation.input.recipient}?</p>
        <button
          onClick={() =>
            addToolApprovalResponse({
              id: invocation.approval.id,
              approved: true,
            })
          }
        >
          Approve
        </button>
        <button
          onClick={() =>
            addToolApprovalResponse({
              id: invocation.approval.id,
              approved: false,
            })
          }
        >
          Deny
        </button>
      </div>
    );
  }
  return null;
}
```

### 3. **Structured Output + Tool Calling** (Stable)

Combine tool calling with structured output generation:

```typescript
import { ToolLoopAgent, Output } from 'ai';
import { z } from 'zod';

const agent = new ToolLoopAgent({
  model: 'groq/llama-3.3-70b-versatile',
  tools: { /* ... */ },
  output: Output.object({
    schema: z.object({
      summary: z.string(),
      temperature: z.number(),
      recommendation: z.string(),
    }),
  }),
});

const { output } = await agent.generate({
  prompt: 'What is the weather in San Francisco and what should I wear?',
});

console.log(output);
// { summary: '...', temperature: 72, recommendation: '...' }
```

### 4. **Reranking Support** (New)

Improve search relevance by reordering documents:

```typescript
import { rerank } from 'ai';
import { cohere } from '@ai-sdk/cohere';

const { ranking } = await rerank({
  model: cohere.reranking('rerank-v3.5'),
  documents: [
    'sunny day at the beach',
    'rainy afternoon in the city',
    'snowy night in the mountains',
  ],
  query: 'talk about rain',
  topN: 2,
});

console.log(ranking);
// [
//   { originalIndex: 1, score: 0.9, document: 'rainy afternoon...' },
//   { originalIndex: 0, score: 0.3, document: 'sunny day...' }
// ]
```

## Migration from AI SDK 5

**Minimal breaking changes expected**. Most AI SDK 5 code will work with little modification.

Key differences:

- Agent abstraction replaces ad-hoc patterns; consider migrating to `ToolLoopAgent`.
- Structured output now works with `generateText` / `streamText` (requires `stopWhen`).
- `@ai-sdk/*` packages may have minor API adjustments during beta.

## Groq Provider (Open Weight Models)

### Setup

```sh
pnpm add @ai-sdk/groq
```

Environment:

```env
GROQ_API_KEY=your_groq_api_key
```

### Open Weight Models Available

Popular Groq models for AI SDK 6:

- `llama-3.3-70b-versatile` (Llama 3.3, 70B, balanced)
- `llama-3.1-8b-instant` (Llama 3.1, 8B, fast)
- `mixtral-8x7b-32768` (Mixture of Experts)
- `gemma2-9b-it` (Google Gemma 2)
- `qwen/qwen3-32b` (Qwen 3)

See [Groq console](https://console.groq.com/docs/models) for full list.

### Basic Llama Example

```typescript
import { groq } from '@ai-sdk/groq';
import { generateText } from 'ai';

const { text } = await generateText({
  model: groq('llama-3.3-70b-versatile'),
  prompt: 'Write a TypeScript function to compute Fibonacci.',
});

console.log(text);
```

### Structured Output with Llama (Groq)

```typescript
import { groq } from '@ai-sdk/groq';
import { generateObject } from 'ai';
import { z } from 'zod';

const result = await generateObject({
  model: groq('llama-3.3-70b-versatile'),
  schema: z.object({
    recipe: z.object({
      name: z.string(),
      ingredients: z.array(z.string()),
      instructions: z.array(z.string()),
    }),
  }),
  prompt: 'Generate a simple pasta recipe.',
  providerOptions: {
    groq: {
      structuredOutputs: true, // Enable for supported models
    },
  },
});

console.log(JSON.stringify(result.object, null, 2));
```

### Tool Use with Llama (Groq)

```typescript
import { groq } from '@ai-sdk/groq';
import { generateText, tool } from 'ai';
import { z } from 'zod';

const weatherTool = tool({
  description: 'Get weather for a city',
  inputSchema: z.object({ city: z.string() }),
  execute: async ({ city }) => ({ temp: 72, condition: 'sunny' }),
});

const { text } = await generateText({
  model: groq('llama-3.3-70b-versatile'),
  prompt: 'What is the weather in NYC and LA?',
  tools: { weather: weatherTool },
});

console.log(text);
```

### Reasoning Models (Groq)

Groq offers reasoning models like `qwen/qwen3-32b` and `deepseek-r1-distill-llama-70b`:

```typescript
import { groq } from '@ai-sdk/groq';
import { generateText } from 'ai';

const { text } = await generateText({
  model: groq('qwen/qwen3-32b'),
  providerOptions: {
    groq: {
      reasoningFormat: 'parsed', // 'parsed', 'hidden', or 'raw'
      reasoningEffort: 'default', // low, medium, high
    },
  },
  prompt: 'How many "r"s are in the word "strawberry"?',
});

console.log(text);
```

### Image Input with Llama (Groq Multi-Modal)

```typescript
import { groq } from '@ai-sdk/groq';
import { generateText } from 'ai';

const { text } = await generateText({
  model: groq('meta-llama/llama-4-scout-17b-16e-instruct'), // Multi-modal model
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'What is in this image?' },
        { type: 'image', image: 'https://example.com/image.jpg' },
      ],
    },
  ],
});

console.log(text);
```

## Vercel AI Gateway

### What It Is

A unified interface to access models from 20+ providers (OpenAI, Anthropic, Google, Groq, xAI, Mistral, etc.) through a single API. Requires **Vercel account and credit card**.

### Setup

```env
AI_GATEWAY_API_KEY=your_gateway_api_key
```

Get your key from Vercel Dashboard > AI Gateway.

**⚠️ Note**: Credit card required for Gateway usage. You will be billed for model calls routed through the gateway.

### Authentication

#### API Key Authentication

Set via environment variable or directly in code:

```typescript
import { createGateway } from 'ai';

const gateway = createGateway({
  apiKey: process.env.AI_GATEWAY_API_KEY,
});
```

#### OIDC Authentication (Vercel Deployments)

When deployed to Vercel, use OIDC tokens for automatic authentication (no API key needed):

**Production/Preview**: Automatic OIDC handling, no setup required.

**Local Development**:

1. Install & authenticate Vercel CLI: `vercel login`
2. Pull OIDC token: `vercel env pull`
3. Use `vercel dev` to start dev server (handles token refresh automatically)

Note: OIDC tokens expire after 12 hours; use `vercel dev` for automatic refresh, or run `vercel env pull` again manually.

```bash
# Start dev with automatic token management
vercel dev
```

### Basic Usage

```typescript
import { generateText } from 'ai';

// Plain model string format: creator/model-name
const { text } = await generateText({
  model: 'openai/gpt-5',
  prompt: 'Explain quantum computing.',
});

console.log(text);
```

### Gateway Instance

```typescript
import { createGateway } from 'ai';

const gateway = createGateway({
  apiKey: process.env.AI_GATEWAY_API_KEY,
});

const { text } = await generateText({
  model: gateway('anthropic/claude-sonnet-4'),
  prompt: 'Write a haiku about AI.',
});

console.log(text);
```

### Model Discovery (Dynamic)

```typescript
import { gateway } from 'ai';

const availableModels = await gateway.getAvailableModels();

availableModels.models.forEach((model) => {
  console.log(`${model.id}: ${model.name}`);
  if (model.pricing) {
    console.log(`  Input: $${model.pricing.input}/token`);
    console.log(`  Output: $${model.pricing.output}/token`);
  }
});

// Use first model
const { text } = await generateText({
  model: availableModels.models[0].id,
  prompt: 'Hello world',
});
```

### Check Credit Usage

```typescript
import { gateway } from 'ai';

const credits = await gateway.getCredits();
console.log(`Balance: ${credits.balance} credits`);
console.log(`Total used: ${credits.total_used} credits`);
```

### Streaming with Gateway

```typescript
import { streamText } from 'ai';

const { textStream } = await streamText({
  model: 'openai/gpt-5',
  prompt: 'Explain serverless architecture.',
});

for await (const chunk of textStream) {
  process.stdout.write(chunk);
}
```

### Tool Use with Gateway

```typescript
import { generateText, tool } from 'ai';
import { z } from 'zod';

const weatherTool = tool({
  description: 'Get weather',
  inputSchema: z.object({ location: z.string() }),
  execute: async ({ location }) => `Sunny in ${location}`,
});

const { text } = await generateText({
  model: 'xai/grok-4', // Via Gateway
  prompt: 'What is the weather in SF?',
  tools: { getWeather: weatherTool },
});

console.log(text);
```

### Bring Your Own Key (BYOK)

Connect your own provider credentials to Gateway for private resource access:

```typescript
import { generateText } from 'ai';
import type { GatewayProviderOptions } from '@ai-sdk/gateway';

const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4',
  prompt: 'Use my Anthropic account',
  providerOptions: {
    gateway: {
      byok: {
        anthropic: [{ apiKey: 'sk-ant-...' }],
      },
    } satisfies GatewayProviderOptions,
  },
});
```

Set up BYOK credentials in Vercel team's AI Gateway settings; no code changes needed after configuration.

### Provider-Executed Tools

Some providers offer tools executed server-side (e.g., OpenAI web search). Use through Gateway by importing the provider:

```typescript
import { generateText, stepCountIs } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateText({
  model: 'openai/gpt-5-mini',
  prompt: 'What is the Vercel AI Gateway?',
  stopWhen: stepCountIs(10),
  tools: {
    web_search: openai.tools.webSearch({}),
  },
});

console.log(result.text);
```

**Note**: Tools requiring account-specific configuration (e.g., Claude Agent Skills) may need direct provider access via BYOK.

### Provider Routing & Fallback

**Core Routing Options**:

- `order`: Try providers in sequence (fallback priority)
- `only`: Restrict to specific providers only
- `models`: Fallback to alternative models if primary fails
- `user`: Track usage per end-user
- `tags`: Categorize requests for analytics
- `zeroDataRetention`: Only use providers with zero data retention
- `byok`: Request-scoped BYOK credentials

#### Example: Provider & Model Fallback

```typescript
import { generateText } from 'ai';
import type { GatewayProviderOptions } from '@ai-sdk/gateway';

const { text } = await generateText({
  model: 'openai/gpt-4o', // Primary model
  prompt: 'Write a TypeScript haiku',
  providerOptions: {
    gateway: {
      order: ['vertex', 'anthropic'], // Try Vertex AI first, then Anthropic
      only: ['vertex', 'anthropic'], // Only allow these providers
      models: ['openai/gpt-5-nano', 'gemini-2.0-flash'], // Fallback models
      user: 'user-123',
      tags: ['code-gen', 'v2'],
    } satisfies GatewayProviderOptions,
  },
});

// Fallback sequence:
// 1. Try vertex with openai/gpt-4o
// 2. Try anthropic with openai/gpt-4o
// 3. Try vertex with openai/gpt-5-nano
// 4. Try anthropic with openai/gpt-5-nano
// etc.
```

#### Example: Usage Tracking

```typescript
import { generateText } from 'ai';
import type { GatewayProviderOptions } from '@ai-sdk/gateway';

const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4',
  prompt: 'Summarize this document...',
  providerOptions: {
    gateway: {
      user: 'user-abc-123', // Track per end-user
      tags: ['document-summary', 'premium-feature'],
    } satisfies GatewayProviderOptions,
  },
});

// View analytics by user and feature in Vercel Dashboard
```

### Zero Data Retention

Route requests only to providers with zero data retention policies for sensitive data:

```typescript
import { generateText } from 'ai';
import type { GatewayProviderOptions } from '@ai-sdk/gateway';

const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4',
  prompt: 'Process sensitive document...',
  providerOptions: {
    gateway: {
      zeroDataRetention: true, // Enforce zero data retention
    } satisfies GatewayProviderOptions,
  },
});
```

When `zeroDataRetention: true`, Gateway only routes to providers that don't retain your data. No enforcement applied if omitted or `false`.

## Key Concepts

### Call Options for Agents

Dynamically configure agents at runtime:

```typescript
import { ToolLoopAgent } from 'ai';
import { z } from 'zod';

const supportAgent = new ToolLoopAgent({
  model: 'groq/llama-3.3-70b-versatile',
  callOptionsSchema: z.object({
    userId: z.string(),
    accountType: z.enum(['free', 'pro', 'enterprise']),
  }),
  instructions: 'You are a support agent.',
  prepareCall: ({ options, ...settings }) => ({
    ...settings,
    instructions:
      settings.instructions +
      `\nUser: ${options.userId}, Account: ${options.accountType}`,
  }),
});

const result = await supportAgent.generate({
  prompt: 'How do I upgrade?',
  options: {
    userId: 'user-456',
    accountType: 'free',
  },
});
```

### UI Integration with React

```typescript
import { createAgentUIStreamResponse } from 'ai';
import { useChat } from '@ai-sdk/react';
import { InferAgentUIMessage } from 'ai';

// Server-side
export async function POST(request: Request) {
  const { messages } = await request.json();
  return createAgentUIStreamResponse({
    agent: weatherAgent,
    messages,
  });
}

// Client-side
type AgentMessage = InferAgentUIMessage<typeof weatherAgent>;
const { messages, sendMessage } = useChat<AgentMessage>();
```

## Best Practices

### Groq

- Use `llama-3.3-70b-versatile` for balanced performance and cost.
- Use `llama-3.1-8b-instant` for low-latency, lightweight tasks.
- Enable `parallelToolCalls: true` (default) for faster multi-tool execution.
- Use `serviceTier: 'flex'` for 10x rate limits if you can tolerate occasional failures.

### Vercel AI Gateway

- **Always add credit card**; gateway is pay-per-token.
- Use `only` / `order` to control routing and costs.
- Use `user` and `tags` for spend tracking and debugging.
- Enable `zeroDataRetention` for sensitive data.
- Check `gateway.getCredits()` regularly to monitor usage.

### Agents

- Use `ToolLoopAgent` as a starting point; extend only if needed.
- Combine structured output with tool calling for rich responses.
- Use tool approval for payment/deletion operations.
- Set `stopWhen` to control loop iterations (default: `stepCountIs(20)`).

## Common Patterns

### RAG Agent

```typescript
const ragAgent = new ToolLoopAgent({
  model: 'groq/llama-3.3-70b-versatile',
  tools: {
    searchDocs: tool({
      description: 'Search documentation',
      inputSchema: z.object({ query: z.string() }),
      execute: async ({ query }) => {
        // Call vector DB (Upstash, Pinecone, etc.)
        return { docs: [/* ... */] };
      },
    }),
  },
  instructions: 'Answer questions by searching docs.',
});
```

### Multi-Provider with Fallback

```typescript
const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4',
  prompt: 'Complex task requiring reasoning',
  providerOptions: {
    gateway: {
      models: ['openai/gpt-5', 'gemini-2.0-flash'],
    },
  },
});
```

### Cost-Optimized Selection

```typescript
const isSensitive = userQuery.includes('payment');
const model = isSensitive 
  ? 'anthropic/claude-sonnet-4' 
  : 'openai/gpt-5-nano';

const { text } = await generateText({
  model,
  prompt: userQuery,
});
```

## Timeline

- **AI SDK 6 Beta**: Available now (pin versions)
- **Stable Release**: End of 2025
