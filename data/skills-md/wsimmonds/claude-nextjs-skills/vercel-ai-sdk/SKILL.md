---
name: vercel-ai-sdk
description: Guide for Vercel AI SDK v5 implementation patterns including generateText, streamText, useChat hook, tool calling, embeddings, and MCP integration. Use when implementing AI chat interfaces, streaming responses, tool/function calling, text embeddings, or working with convertToModelMessages and toUIMessageStreamResponse. Activates for AI SDK integration, useChat hook usage, message streaming, or tool calling tasks.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebFetch
---

# Vercel AI SDK v5 Implementation Guide

## When to Use This Skill

Use this skill when:
- Implementing AI chat interfaces with `useChat` hook
- Creating API routes that generate or stream AI responses
- Adding tool calling / function calling capabilities
- Generating text embeddings for semantic search or RAG
- Migrating from AI SDK v4 to v5
- Integrating Model Context Protocol (MCP) servers
- Working with streaming responses or message persistence

## Structured Implementation Workflow

<workflow>
  <step id="1" name="verify-requirements">
    <description>Understand the task requirements</description>
    <actions>
      - Identify what AI functionality is needed (chat, generation, tools, embeddings)
      - Determine if client-side (useChat) or server-side (API route) implementation
      - Check if streaming or non-streaming response is required
      - Verify model provider (OpenAI, Anthropic, etc.)
    </actions>
  </step>

  <step id="2" name="check-documentation">
    <description>Verify current API patterns if uncertain</description>
    <actions>
      - Use WebFetch to check https://ai-sdk.dev/docs/ if API patterns are unclear
      - Confirm model specification format for the provider
      - Verify function signatures for complex features
    </actions>
  </step>

  <step id="3" name="implement">
    <description>Implement using correct v5 patterns</description>
    <actions>
      - Use string-based model specification ('provider/model-id')
      - For chat: use sendMessage (not append), parts-based messages
      - For tools: MUST import and use tool() helper from 'ai', MUST use inputSchema (NOT parameters), MUST use zod
      - For streaming: use toUIMessageStreamResponse() or toTextStreamResponse()
      - For embeddings: use provider.textEmbeddingModel()
    </actions>
  </step>

  <step id="4" name="verify-types">
    <description>Ensure TypeScript types are correct</description>
    <actions>
      - Check for proper imports from 'ai' package
      - Verify message types (UIMessage for useChat)
      - Ensure tool parameter types are inferred correctly
      - Add explicit types for async functions
    </actions>
  </step>

  <step id="5" name="install-dependencies">
    <description>Install any missing dependencies with the CORRECT package manager</description>
    <actions>
      - **CRITICAL: Detect which package manager the project uses FIRST**
        * Check for lockfiles: pnpm-lock.yaml → use pnpm, package-lock.json → use npm, yarn.lock → use yarn, bun.lockb → use bun
        * If pnpm-lock.yaml exists, you MUST use pnpm (NOT npm!)
      - Check if all imported packages are installed
      - If build fails with "Module not found", identify the package name from the error
      - Add the package to package.json dependencies
      - Install using the CORRECT package manager:
        * If pnpm-lock.yaml exists: `pnpm install [package]` or `pnpm add [package]`
        * If package-lock.json exists: `npm install [package]`
        * If yarn.lock exists: `yarn add [package]`
        * If bun.lockb exists: `bun install [package]` or `bun add [package]`
      - Re-run build to verify installation succeeded
    </actions>
    <critical>
      **NEVER use the wrong package manager!**
      - Using npm when the project uses pnpm creates package-lock.json alongside pnpm-lock.yaml
      - This causes dependency version mismatches and breaks the build
      - ALWAYS check for existing lockfiles and use the matching package manager

      NEVER accept "Module not found" errors as environment issues
      YOU must install the required packages with the CORRECT package manager

      Common packages needed:
      - ai (core AI SDK)
      - @ai-sdk/openai (OpenAI provider)
      - @ai-sdk/anthropic (Anthropic provider)
      - @modelcontextprotocol/sdk (MCP integration)
      - zod (for tool schemas)
    </critical>
  </step>

  <step id="6" name="verify-build">
    <description>Run build and fix ALL errors until it passes</description>
    <actions>
      - Run: npm run build (or bun run build)
      - If build fails, read the FULL error message carefully
      - Common fixes:
        * "Module not found" → Install the package (go back to step 5)
        * Type errors → Fix TypeScript types
        * Config errors → Check next.config.js/ts
        * Framework errors → Research the error, try different approaches
      - Apply fix and re-run build
      - REPEAT until build passes
    </actions>
    <critical>
      NEVER stop at "build fails but code is correct"
      NEVER blame "environment" or "framework bugs" without debugging
      KEEP ITERATING until the build PASSES
      If you encounter a framework error, research it, try workarounds, debug it
      DO NOT give up until you have a passing build
    </critical>
  </step>

  <step id="7" name="verify-tests">
    <description>Run tests and debug ALL failures until they pass</description>
    <actions>
      - Run: npm run test (or bun run test)
      - If tests fail, read the FULL error message carefully
      - Debug the failure:
        * Check what the test expects vs what you're providing
        * Look at test assertions
        * Verify your implementation matches the requirements
        * Check for type mismatches or missing properties
      - Fix the implementation
      - Re-run tests
      - REPEAT until all tests pass
    </actions>
    <critical>
      NEVER accept test failures without debugging
      NEVER dismiss failures as "test framework bugs" without investigation
      Each test failure is telling you something - LISTEN to it
      KEEP DEBUGGING until all tests pass
      Test failures are NOT acceptable - they mean your implementation is incomplete
    </critical>
  </step>

  <step id="8" name="final-verification">
    <description>Verify EVERYTHING passes</description>
    <actions>
      - Run: npm run build && npm run lint && npm run test
      - All three must pass: ✅ Build, ✅ Lint, ✅ Tests
      - If any fail, go back and fix them
      - Do not consider the task complete until ALL checks pass
    </actions>
    <critical>
      The task is NOT complete until:
      - ✅ Build passes
      - ✅ Lint passes
      - ✅ Tests pass

      "Code is correct" is NOT enough
      You must achieve FULL PASSING status
      This is what it means to be an autonomous agent
    </critical>
  </step>
</workflow>

## ⚠️ AUTONOMOUS AGENT MINDSET

**You are not just writing code - you are COMPLETING TASKS AUTONOMOUSLY.**

This means:
1. ✅ Write correct implementation
2. ✅ **Install any required dependencies**
3. ✅ **Run build and fix ALL errors**
4. ✅ **Run tests and debug ALL failures**
5. ✅ **Iterate until EVERYTHING passes**
6. ✅ **Never make excuses or give up**

### Common Failure Patterns to AVOID

❌ **WRONG:** "The code is correct, but the package isn't installed - that's an environment issue"
✅ **CORRECT:** "Build failed due to missing package - installing it now with npm install [package]"

❌ **WRONG:** "Tests pass but build fails - not my problem"
✅ **CORRECT:** "Build is failing - debugging the error and fixing it now"

❌ **WRONG:** "There's a framework bug, can't fix it"
✅ **CORRECT:** "Framework error detected - researching the issue, trying workarounds, debugging until I find a solution"

❌ **WRONG:** "The implementation is complete" (with failing tests)
✅ **CORRECT:** "Tests are failing - debugging and fixing until they all pass"

### Dependency Installation Workflow

When you encounter "Module not found" errors:

1. **Detect the package manager FIRST** - Check for lockfiles:
   ```bash
   ls -la | grep -E "lock"
   # Look for: pnpm-lock.yaml, package-lock.json, yarn.lock, bun.lockb
   ```

2. **Identify the package** from the import statement
   ```
   Error: Cannot find module '@ai-sdk/openai'
   Import: import { openai } from '@ai-sdk/openai'
   Package needed: @ai-sdk/openai
   ```

3. **Install with the CORRECT package manager**
   ```bash
   # If pnpm-lock.yaml exists (MOST COMMON for Next.js evals):
   pnpm install @ai-sdk/openai
   # or
   pnpm add @ai-sdk/openai

   # If package-lock.json exists:
   npm install @ai-sdk/openai

   # If yarn.lock exists:
   yarn add @ai-sdk/openai

   # If bun.lockb exists:
   bun install @ai-sdk/openai
   ```

4. **Re-run build** to verify
   ```bash
   npm run build
   # or pnpm run build, yarn build, bun run build
   ```

5. **Fix any new errors** that appear

**⚠️ CRITICAL WARNING:**
Using the WRONG package manager (e.g., npm when the project uses pnpm) will:
- Create a second conflicting lockfile
- Install different versions of dependencies
- Cause dependency version mismatches
- Break the build with cryptic errors like "Cannot read properties of null"

### Build Error Debugging Workflow

When build fails:

1. **Read the FULL error message** - don't skim it
2. **Identify the root cause**:
   - Module not found → Install package
   - Type error → Fix types
   - Config error → Check config files
   - Next.js error → Research, try different approaches
3. **Apply the fix**
4. **Re-run build**
5. **Repeat until build passes**

### Test Failure Debugging Workflow

When tests fail:

1. **Read the FULL test error** - understand what's expected
2. **Compare** expected vs actual behavior
3. **Check your implementation** against test assertions
4. **Fix the issue** in your code
5. **Re-run tests**
6. **Repeat until all tests pass**

### Success Criteria

Task is ONLY complete when:
- ✅ Build passes (`npm run build` succeeds)
- ✅ Lint passes (`npm run lint` succeeds)
- ✅ Tests pass (`npm run test` succeeds)

**NEVER stop at "code is correct" - achieve FULL PASSING status!**

## ⚠️ CRITICAL: Tool Calling API - MUST USE tool() Helper

**When implementing tool calling, you MUST use the `tool()` helper function from the 'ai' package.**

### ❌ WRONG - Plain Object (WILL CAUSE BUILD ERROR)

```typescript
// DO NOT DO THIS - This pattern is INCORRECT
import { z } from 'zod';

tools: {
  myTool: {
    description: 'My tool',
    parameters: z.object({...}),  // ❌ WRONG - "parameters" doesn't exist in v5
    execute: async ({...}) => {...},
  }
}
```

**This will fail with:** `Type '{ description: string; parameters: ... }' is not assignable to type '{ inputSchema: FlexibleSchema<any>; ... }'`

### ✅ CORRECT - Use tool() Helper (REQUIRED)

```typescript
// ALWAYS DO THIS - This is the ONLY correct pattern
import { tool } from 'ai';  // ⚠️ MUST import tool
import { z } from 'zod';

tools: {
  myTool: tool({  // ⚠️ MUST wrap with tool()
    description: 'My tool',
    inputSchema: z.object({...}),  // ⚠️ MUST use "inputSchema" (not "parameters")
    execute: async ({...}) => {...},
  }),
}
```

### Tool Calling Checklist

Before implementing any tool, verify:
- [ ] Imported `tool` from 'ai' package: `import { tool } from 'ai';`
- [ ] Wrapped tool definition with `tool({ ... })`
- [ ] Used `inputSchema` property (NOT `parameters`)
- [ ] Used zod schema: `z.object({ ... })`
- [ ] Defined `execute` function with async callback
- [ ] Added `description` string for the tool

## ⚠️ CRITICAL: Common v4 to v5 Breaking Changes

### 1. useChat Hook Changes

**❌ WRONG (v4 pattern):**
```typescript
const { messages, input, setInput, append } = useChat();

// Sending message
append({ content: text, role: 'user' });
```

**✅ CORRECT (v5 pattern):**
```typescript
const { messages, sendMessage } = useChat();
const [input, setInput] = useState('');

// Sending message
sendMessage({ text: input });
```

### 2. Message Structure

**❌ WRONG (v4 simple content):**
```typescript
<div>{message.content}</div>
```

**✅ CORRECT (v5 parts-based):**
```typescript
<div>
  {message.parts.map((part, index) =>
    part.type === 'text' ? <span key={index}>{part.text}</span> : null
  )}
</div>
```

### 3. Model Specification

**✅ PREFER: String-based (v5 recommended):**
```typescript
import { generateText } from 'ai';

const result = await generateText({
  model: 'openai/gpt-4o',  // String format
  prompt: 'Hello',
});
```

**✅ ALSO WORKS: Function-based (legacy support):**
```typescript
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

const result = await generateText({
  model: openai('gpt-4o'),  // Function format
  prompt: 'Hello',
});
```

## Core API Reference

### 1. generateText - Non-Streaming Text Generation

**Purpose:** Generate text for non-interactive use cases (email drafts, summaries, agents with tools).

**Signature:**
```typescript
import { generateText } from 'ai';

const result = await generateText({
  model: 'openai/gpt-4o',           // String format: 'provider/model-id'
  prompt: 'Your prompt here',        // User input
  system: 'Optional system message', // Optional system instructions
  tools?: { ... },                   // Optional tool calling
  maxSteps?: 5,                      // For multi-step tool calling
});
```

**Return Value:**
```typescript
{
  text: string;              // Generated text output
  toolCalls: ToolCall[];     // Tool invocations made
  finishReason: string;      // Why generation stopped
  usage: TokenUsage;         // Token consumption
  response: RawResponse;     // Raw provider response
  warnings: Warning[];       // Provider-specific alerts
}
```

**Example:**
```typescript
// app/api/generate/route.ts
import { generateText } from 'ai';

export async function GET() {
  const result = await generateText({
    model: 'anthropic/claude-4-sonnet',
    prompt: 'Why is the sky blue?',
  });

  return Response.json({ text: result.text });
}
```

### 2. streamText - Streaming Text Generation

**Purpose:** Stream responses for interactive chat applications.

**Signature:**
```typescript
import { streamText } from 'ai';

const result = streamText({
  model: 'openai/gpt-4o',
  prompt: 'Your prompt here',
  system: 'Optional system message',
  messages?: ModelMessage[],  // For chat history
  tools?: { ... },
  onFinish?: async (result) => { ... },
  onError?: async (error) => { ... },
});
```

**Return Methods:**
```typescript
// For chat applications with useChat hook
result.toUIMessageStreamResponse();

// For simple text streaming
result.toTextStreamResponse();
```

**Example - Chat API Route:**
```typescript
// app/api/chat/route.ts
import { streamText, convertToModelMessages } from 'ai';
import type { UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: 'openai/gpt-4o',
    system: 'You are a helpful assistant.',
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

### 3. useChat Hook - Client-Side Chat Interface

**Purpose:** Build interactive chat UIs with streaming support.

**Signature:**
```typescript
import { useChat } from 'ai/react';

const {
  messages,        // Array of UIMessage with parts-based structure
  sendMessage,     // Function to send messages (replaces append)
  status,          // 'submitted' | 'streaming' | 'ready' | 'error'
  stop,            // Abort current streaming
  regenerate,      // Reprocess last message
  setMessages,     // Manually modify history
  error,           // Error object if request fails
  reload,          // Retry after error
} = useChat({
  api: '/api/chat',  // API endpoint
  onFinish?: (message) => { ... },
  onError?: (error) => { ... },
});
```

**Complete Example:**
```typescript
'use client';

import { useChat } from 'ai/react';
import { useState } from 'react';

export default function ChatPage() {
  const { messages, sendMessage, status } = useChat();
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    sendMessage({ text: input });
    setInput('');
  };

  return (
    <div>
      <div>
        {messages.map((message) => (
          <div key={message.id}>
            <strong>{message.role}:</strong>
            {message.parts.map((part, index) =>
              part.type === 'text' ? (
                <span key={index}>{part.text}</span>
              ) : null
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={status === 'streaming'}
        />
        <button type="submit" disabled={status === 'streaming'}>
          Send
        </button>
      </form>
    </div>
  );
}
```

### 4. Tool Calling / Function Calling

**Purpose:** Enable AI models to call functions with structured parameters.

**Defining Tools:**
```typescript
import { tool } from 'ai';
import { z } from 'zod';

const weatherTool = tool({
  description: 'Get the weather in a location',
  inputSchema: z.object({
    location: z.string().describe('The location to get the weather for'),
    unit: z.enum(['C', 'F']).describe('Temperature unit'),
  }),
  execute: async ({ location, unit }) => {
    // Fetch or mock weather data
    return {
      location,
      temperature: 24,
      unit,
      condition: 'Sunny',
    };
  },
});
```

**Using Tools with generateText/streamText:**
```typescript
// app/api/chat/route.ts
import { streamText, convertToModelMessages, tool } from 'ai';
import { z } from 'zod';
import type { UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: 'openai/gpt-4o',
    messages: convertToModelMessages(messages),
    tools: {
      getWeather: tool({
        description: 'Get the weather for a location',
        inputSchema: z.object({
          city: z.string().describe('The city to get the weather for'),
          unit: z.enum(['C', 'F']).describe('The unit to display the temperature in'),
        }),
        execute: async ({ city, unit }) => {
          // Mock response
          return `It is currently 24°${unit} and Sunny in ${city}!`;
        },
      }),
    },
  });

  return result.toUIMessageStreamResponse();
}
```

**Multi-Step Tool Calling:**
```typescript
const result = await generateText({
  model: 'openai/gpt-4o',
  tools: {
    weather: weatherTool,
    search: searchTool,
  },
  prompt: 'What is the weather in San Francisco and find hotels there?',
  maxSteps: 5,  // Allow up to 5 tool call steps
});
```

### 5. Text Embeddings

**Purpose:** Convert text into numerical vectors for semantic search, RAG, or similarity.

**Signature:**
```typescript
import { embed } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await embed({
  model: openai.textEmbeddingModel('text-embedding-3-small'),
  value: 'Text to embed',
});
```

**Return Value:**
```typescript
{
  embedding: number[];  // Numerical array representing the text
  usage: { tokens: number };  // Token consumption
  response: RawResponse;  // Raw provider response
}
```

**Example - Embedding API Route:**
```typescript
// app/api/embed/route.ts
import { embed } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function GET() {
  const { embedding, usage } = await embed({
    model: openai.textEmbeddingModel('text-embedding-3-small'),
    value: 'sunny day at the beach',
  });

  return Response.json({ embedding, usage });
}
```

**Batch Embeddings:**
```typescript
import { embedMany } from 'ai';

const { embeddings, usage } = await embedMany({
  model: openai.textEmbeddingModel('text-embedding-3-small'),
  values: [
    'sunny day at the beach',
    'rainy afternoon in the city',
    'snowy mountain landscape',
  ],
});
```

### 6. Message Utilities

**convertToModelMessages:**
Converts UI messages from `useChat` into `ModelMessage` objects for AI functions.

```typescript
import { convertToModelMessages } from 'ai';
import type { UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: 'openai/gpt-4o',
    messages: convertToModelMessages(messages),  // Convert for model
  });

  return result.toUIMessageStreamResponse();
}
```

### 7. Model Context Protocol (MCP) Integration

**Purpose:** Connect to external MCP servers for dynamic tool access.

**Example:**
```typescript
// app/api/chat/route.ts
import { experimental_createMCPClient, streamText } from 'ai';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';

export async function POST(req: Request) {
  const { prompt }: { prompt: string } = await req.json();

  try {
    // Connect to MCP server
    const httpTransport = new StreamableHTTPClientTransport(
      new URL('http://localhost:3000/mcp')
    );

    const httpClient = await experimental_createMCPClient({
      transport: httpTransport,
    });

    // Fetch tools from MCP server
    const tools = await httpClient.tools();

    const response = streamText({
      model: 'openai/gpt-4o',
      tools,
      prompt,
      onFinish: async () => {
        await httpClient.close();  // Clean up
      },
      onError: async () => {
        await httpClient.close();  // Clean up on error
      },
    });

    return response.toTextStreamResponse();
  } catch (error) {
    return new Response('Internal Server Error', { status: 500 });
  }
}
```

**Key Points:**
- Use `experimental_createMCPClient` (note: experimental API)
- Always close the client in `onFinish` and `onError`
- Tools are fetched dynamically with `httpClient.tools()`
- Requires `@modelcontextprotocol/sdk` package

## Model Specification Patterns

### String-Based (Recommended for v5)

```typescript
// Format: 'provider/model-id'
model: 'openai/gpt-4o'
model: 'anthropic/claude-4-sonnet'
model: 'google/gemini-2.0-flash'
```

### Function-Based (Legacy Support)

```typescript
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';

model: openai('gpt-4o')
model: anthropic('claude-4-sonnet')
```

### Embedding Models

```typescript
import { openai } from '@ai-sdk/openai';

// Text embeddings use a different method
openai.textEmbeddingModel('text-embedding-3-small')
openai.textEmbeddingModel('text-embedding-3-large')
```

## TypeScript Best Practices

### Type Imports

```typescript
import type {
  UIMessage,           // Message type from useChat
  ModelMessage,        // Message type for model functions
  ToolCall,            // Tool call information
  TokenUsage,          // Token consumption data
} from 'ai';
```

### Strongly Typed Tools

```typescript
import { tool } from 'ai';
import { z } from 'zod';

// Tool helper infers execute parameter types
const myTool = tool({
  description: 'My tool',
  inputSchema: z.object({
    param1: z.string(),
    param2: z.number(),
  }),
  execute: async ({ param1, param2 }) => {
    // param1 is inferred as string
    // param2 is inferred as number
    return { result: 'success' };
  },
});
```

### API Route Types

```typescript
// app/api/chat/route.ts
import type { UIMessage } from 'ai';

export async function POST(req: Request): Promise<Response> {
  const { messages }: { messages: UIMessage[] } = await req.json();

  // ... implementation
}
```

## Common Patterns

### Pattern 1: Simple Chat Application

**Client (`app/page.tsx`):**
```typescript
'use client';

import { useChat } from 'ai/react';
import { useState } from 'react';

export default function Chat() {
  const { messages, sendMessage, status } = useChat();
  const [input, setInput] = useState('');

  return (
    <div>
      {messages.map((m) => (
        <div key={m.id}>
          <strong>{m.role}:</strong>
          {m.parts.map((part, i) =>
            part.type === 'text' ? <span key={i}>{part.text}</span> : null
          )}
        </div>
      ))}
      <form onSubmit={(e) => {
        e.preventDefault();
        sendMessage({ text: input });
        setInput('');
      }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} />
        <button disabled={status === 'streaming'}>Send</button>
      </form>
    </div>
  );
}
```

**Server (`app/api/chat/route.ts`):**
```typescript
import { streamText, convertToModelMessages } from 'ai';
import type { UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: 'openai/gpt-4o',
    system: 'You are a helpful assistant.',
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

### Pattern 2: Chat with Tools

**Server with tool calling:**
```typescript
import { streamText, convertToModelMessages, tool } from 'ai';
import { z } from 'zod';
import type { UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: 'openai/gpt-4o',
    messages: convertToModelMessages(messages),
    tools: {
      getWeather: tool({
        description: 'Get weather for a city',
        inputSchema: z.object({
          city: z.string(),
        }),
        execute: async ({ city }) => {
          // API call or mock data
          return { city, temp: 72, condition: 'Sunny' };
        },
      }),
      searchWeb: tool({
        description: 'Search the web',
        inputSchema: z.object({
          query: z.string(),
        }),
        execute: async ({ query }) => {
          // Search implementation
          return { results: ['...'] };
        },
      }),
    },
  });

  return result.toUIMessageStreamResponse();
}
```

### Pattern 3: Non-Interactive Generation

```typescript
// app/api/summarize/route.ts
import { generateText } from 'ai';

export async function POST(req: Request) {
  const { text } = await req.json();

  const result = await generateText({
    model: 'anthropic/claude-4-sonnet',
    system: 'You are a summarization expert.',
    prompt: `Summarize this text:\n\n${text}`,
  });

  return Response.json({ summary: result.text });
}
```

### Pattern 4: Semantic Search with Embeddings

```typescript
// app/api/search/route.ts
import { embed } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  const { query } = await req.json();

  // Generate embedding for search query
  const { embedding } = await embed({
    model: openai.textEmbeddingModel('text-embedding-3-small'),
    value: query,
  });

  // Use embedding for similarity search in vector database
  // const results = await vectorDB.search(embedding);

  return Response.json({ embedding, results: [] });
}
```

## Common Pitfalls and Solutions

### Pitfall 1: NOT Using tool() Helper for Tools - ⚠️ CRITICAL

**This is the most common and critical mistake. Always use `tool()` helper!**

```typescript
// ❌ WRONG - Plain object (WILL CAUSE BUILD FAILURE)
import { z } from 'zod';

tools: {
  myTool: {
    description: 'My tool',
    parameters: z.object({      // ❌ Wrong property name
      city: z.string(),
    }),
    execute: async ({ city }) => { ... },
  },
}
// Build error: Type '{ description: string; parameters: ... }' is not assignable

// ✅ CORRECT - Use tool() helper (REQUIRED)
import { tool } from 'ai';      // ⚠️ MUST import tool
import { z } from 'zod';

tools: {
  myTool: tool({                // ⚠️ MUST use tool() wrapper
    description: 'My tool',
    inputSchema: z.object({     // ⚠️ Use inputSchema (not parameters)
      city: z.string(),
    }),
    execute: async ({ city }) => { ... },
  }),
}
```

### Pitfall 2: Using v4 useChat API in v5

```typescript
// ❌ WRONG - v4 pattern
const { input, setInput, append } = useChat();
append({ content: 'Hello', role: 'user' });

// ✅ CORRECT - v5 pattern
const { sendMessage } = useChat();
const [input, setInput] = useState('');
sendMessage({ text: 'Hello' });
```

### Pitfall 3: Accessing message.content instead of message.parts

```typescript
// ❌ WRONG - v4 pattern
<div>{message.content}</div>

// ✅ CORRECT - v5 parts-based
<div>
  {message.parts.map((part, i) =>
    part.type === 'text' ? <span key={i}>{part.text}</span> : null
  )}
</div>
```

### Pitfall 4: Not Converting UIMessages for Model

```typescript
// ❌ WRONG - passing UIMessages directly
const result = streamText({
  model: 'openai/gpt-4o',
  messages: messages,  // UIMessage[] - type error
});

// ✅ CORRECT - convert to ModelMessage[]
const result = streamText({
  model: 'openai/gpt-4o',
  messages: convertToModelMessages(messages),
});
```

### Pitfall 5: Forgetting MCP Client Cleanup

```typescript
// ❌ WRONG - no cleanup
const httpClient = await experimental_createMCPClient({
  transport: httpTransport,
});
const tools = await httpClient.tools();
const response = streamText({ model, tools, prompt });
return response.toTextStreamResponse();

// ✅ CORRECT - cleanup in callbacks
const response = streamText({
  model,
  tools,
  prompt,
  onFinish: async () => {
    await httpClient.close();
  },
  onError: async () => {
    await httpClient.close();
  },
});
```

### Pitfall 6: Using Wrong Response Method

```typescript
// ❌ WRONG - using text stream for useChat
return result.toTextStreamResponse();  // Won't work with useChat hook

// ✅ CORRECT - use UI message stream for useChat
return result.toUIMessageStreamResponse();

// ✅ ALSO CORRECT - text stream for non-chat scenarios
// For simple text streaming (not using useChat hook)
return result.toTextStreamResponse();
```

### Pitfall 7: Wrong Embedding Model Method

```typescript
// ❌ WRONG - using regular model method
const { embedding } = await embed({
  model: openai('text-embedding-3-small'),  // Wrong method
  value: 'text',
});

// ✅ CORRECT - use textEmbeddingModel
const { embedding } = await embed({
  model: openai.textEmbeddingModel('text-embedding-3-small'),
  value: 'text',
});
```

## Migration Checklist (v4 → v5)

When migrating from v4 to v5, update:

- [ ] Replace `append` with `sendMessage` in useChat
- [ ] Remove `input`, `setInput`, `handleInputChange` from useChat destructuring
- [ ] Add local state management for input: `const [input, setInput] = useState('')`
- [ ] Update message rendering from `message.content` to `message.parts.map(...)`
- [ ] Update sendMessage calls to use `{ text: input }` structure
- [ ] Verify `convertToModelMessages` is used in API routes
- [ ] Check that `toUIMessageStreamResponse()` is used (not v4 streaming methods)
- [ ] Update tool definitions to use `tool()` helper with `inputSchema`
- [ ] Consider using string-based model specification (`'provider/model-id'`)
- [ ] Update TypeScript types (`UIMessage`, `ModelMessage`)

## Decision Guide

When implementing AI SDK features, ask:

1. **Is this client-side or server-side?**
   - Client: Use `useChat` hook
   - Server: Use `generateText` or `streamText`

2. **Do I need streaming or non-streaming?**
   - Streaming chat: `streamText` + `toUIMessageStreamResponse()`
   - Non-streaming: `generateText`
   - Simple text stream: `streamText` + `toTextStreamResponse()`

3. **Do I need tool calling?**
   - Yes: Define tools with `tool()` helper and `inputSchema` (zod)
   - Pass tools object to `generateText` or `streamText`

4. **Am I using the correct message format?**
   - Client (useChat): Returns `UIMessage[]` with `parts` property
   - Server: Convert with `convertToModelMessages()` to `ModelMessage[]`
   - Render messages using `message.parts.map(...)`

5. **Is my model specification correct?**
   - Prefer string format: `'openai/gpt-4o'`
   - Function format also works: `openai('gpt-4o')`
   - Embeddings: `openai.textEmbeddingModel('text-embedding-3-small')`

6. **Do I need embeddings?**
   - Use `embed` for single values
   - Use `embedMany` for batches
   - Use `textEmbeddingModel()` method

## Quick Reference

| Task | Function | Key Parameters |
|------|----------|----------------|
| Generate text | `generateText()` | `model`, `prompt`, `system`, `tools` |
| Stream text | `streamText()` | `model`, `messages`, `tools`, `onFinish` |
| Chat UI | `useChat()` | `api`, `onFinish`, `onError` |
| Tool calling | `tool()` | `description`, `inputSchema`, `execute` |
| Text embedding | `embed()` | `model`, `value` |
| Batch embedding | `embedMany()` | `model`, `values` |
| Message conversion | `convertToModelMessages()` | `messages` (UIMessage[]) |
| MCP integration | `experimental_createMCPClient()` | `transport` |

## Additional Resources

When in doubt, check the official documentation:
- Main docs: https://ai-sdk.dev/docs
- API reference: https://ai-sdk.dev/docs/reference
- Examples: https://ai-sdk.dev/examples

**Remember:** AI SDK v5 uses string-based model specification, parts-based messages, `sendMessage` instead of `append`, and requires `convertToModelMessages` in API routes.
