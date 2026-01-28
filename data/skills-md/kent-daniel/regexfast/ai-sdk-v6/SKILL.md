---
name: ai-sdk-v6
description: Guide for building AI-powered applications using the Vercel AI SDK v6. Use when developing with generateText, streamText, useChat, tool calling, agents, structured output generation, MCP integration, or any LLM-powered features in TypeScript/JavaScript applications. Covers React, Next.js, Vue, Svelte, and Node.js implementations.
---

# AI SDK v6

## Overview

The AI SDK is the TypeScript toolkit for building AI-powered applications with React, Next.js, Vue, Svelte, Node.js, and more. It provides a unified API across multiple model providers (OpenAI, Anthropic, Google, etc.) and consists of:

- **AI SDK Core**: Unified API for text generation, structured data, tool calling, and agents
- **AI SDK UI**: Framework-agnostic hooks (`useChat`, `useCompletion`, `useObject`) for chat interfaces

## Quick Start

### Installation

```bash
npm install ai @ai-sdk/openai  # or @ai-sdk/anthropic, @ai-sdk/google, etc.
```

### Basic Text Generation

```typescript
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4.5', // or use provider-specific: anthropic('claude-sonnet-4.5')
  prompt: 'Write a haiku about programming.',
});
```

### Streaming Text

```typescript
import { streamText } from 'ai';

const result = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Explain quantum computing.',
});

for await (const text of result.textStream) {
  process.stdout.write(text);
}
```

## Provider Configuration

### Using Provider Functions

```typescript
import { anthropic } from '@ai-sdk/anthropic';
import { openai } from '@ai-sdk/openai';
import { google } from '@ai-sdk/google';

// Provider-specific model initialization
const result = await generateText({
  model: anthropic('claude-sonnet-4.5'),
  prompt: 'Hello!',
});
```

### Using Gateway Strings

```typescript
// Simpler string-based model references
const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Hello!',
});
```

## Tool Calling

Define tools with schemas and execute functions:

```typescript
import { generateText, tool, stepCountIs } from 'ai';
import { z } from 'zod';

const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  tools: {
    weather: tool({
      description: 'Get the weather in a location',
      inputSchema: z.object({
        location: z.string().describe('City name'),
      }),
      execute: async ({ location }) => ({
        location,
        temperature: 72,
        condition: 'sunny',
      }),
    }),
  },
  stopWhen: stepCountIs(5), // Enable multi-step tool execution
  prompt: 'What is the weather in San Francisco?',
});
```

### Tool Execution Approval (Human-in-the-Loop)

```typescript
const runCommand = tool({
  description: 'Run a shell command',
  inputSchema: z.object({
    command: z.string(),
  }),
  needsApproval: true, // Require user approval before execution
  execute: async ({ command }) => {
    // execution logic
  },
});
```

## Agents (New in v6)

### ToolLoopAgent

Production-ready agent abstraction that handles the complete tool execution loop:

```typescript
import { ToolLoopAgent } from 'ai';

const weatherAgent = new ToolLoopAgent({
  model: 'anthropic/claude-sonnet-4.5',
  instructions: 'You are a helpful weather assistant.',
  tools: {
    weather: weatherTool,
  },
});

const result = await weatherAgent.generate({
  prompt: 'What is the weather in San Francisco?',
});
```

### Agent with Structured Output

```typescript
import { ToolLoopAgent, Output } from 'ai';

const agent = new ToolLoopAgent({
  model: 'anthropic/claude-sonnet-4.5',
  tools: { weather: weatherTool },
  output: Output.object({
    schema: z.object({
      summary: z.string(),
      temperature: z.number(),
    }),
  }),
});
```

## Structured Data Generation

```typescript
import { generateObject, Output } from 'ai';
import { z } from 'zod';

const { object } = await generateObject({
  model: 'anthropic/claude-sonnet-4.5',
  schema: z.object({
    recipe: z.object({
      name: z.string(),
      ingredients: z.array(z.object({
        name: z.string(),
        amount: z.string(),
      })),
      steps: z.array(z.string()),
    }),
  }),
  prompt: 'Generate a lasagna recipe.',
});
```

## UI Integration (React/Next.js)

### useChat Hook

```typescript
'use client';

import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';

export default function Chat() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({
      api: '/api/chat',
    }),
  });

  return (
    <div>
      {messages.map(message => (
        <div key={message.id}>
          {message.role}: {message.parts.map((part, i) => 
            part.type === 'text' ? <span key={i}>{part.text}</span> : null
          )}
        </div>
      ))}
      <form onSubmit={e => {
        e.preventDefault();
        sendMessage({ text: input });
      }}>
        <input value={input} onChange={e => setInput(e.target.value)} />
        <button type="submit" disabled={status !== 'ready'}>Send</button>
      </form>
    </div>
  );
}
```

### API Route (Next.js App Router)

```typescript
// app/api/chat/route.ts
import { convertToModelMessages, streamText, UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: 'anthropic/claude-sonnet-4.5',
    system: 'You are a helpful assistant.',
    messages: await convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

## MCP (Model Context Protocol) Integration

```typescript
import { createMCPClient } from '@ai-sdk/mcp';

const mcpClient = await createMCPClient({
  transport: {
    type: 'http',
    url: 'https://your-server.com/mcp',
    headers: { Authorization: 'Bearer my-api-key' },
  },
});

const tools = await mcpClient.tools();

// Use MCP tools with generateText/streamText
const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  tools,
  prompt: 'Use the available tools to help me.',
});
```

## DevTools

Debug AI applications with full visibility into LLM calls:

```typescript
import { wrapLanguageModel, gateway } from 'ai';
import { devToolsMiddleware } from '@ai-sdk/devtools';

const model = wrapLanguageModel({
  model: gateway('anthropic/claude-sonnet-4.5'),
  middleware: devToolsMiddleware(),
});

// Launch viewer: npx @ai-sdk/devtools
// Open http://localhost:4983
```

## Resources

For detailed API documentation, see:

- [references/core-api.md](references/core-api.md) - Complete AI SDK Core API (generateText, streamText, generateObject, tool definitions)
- [references/ui-hooks.md](references/ui-hooks.md) - AI SDK UI hooks (useChat, useCompletion, useObject) and transport configuration
- [references/agents.md](references/agents.md) - Agent abstractions (ToolLoopAgent), workflow patterns, and loop control
