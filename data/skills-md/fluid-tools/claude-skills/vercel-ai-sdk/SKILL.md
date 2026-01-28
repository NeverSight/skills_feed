---
name: vercel-ai-sdk
description: Guide for Vercel AI SDK v6 implementation patterns including generateText, streamText, ToolLoopAgent, structured output with Output helpers, useChat hook, tool calling, embeddings, middleware, and MCP integration. Use when implementing AI chat interfaces, streaming responses, agentic applications, tool/function calling, text embeddings, workflow patterns, or working with convertToModelMessages and toUIMessageStreamResponse. Activates for AI SDK integration, useChat hook usage, message streaming, agent development, or tool calling tasks.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebFetch
---

# Vercel AI SDK v6 Implementation Guide

## When to Use This Skill

Use this skill when:

- Implementing AI chat interfaces with `useChat` hook
- Creating API routes that generate or stream AI responses
- Building agentic applications with `ToolLoopAgent`
- Adding tool calling / function calling capabilities
- Generating structured output with `Output.object()`, `Output.array()`, etc.
- Generating text embeddings for semantic search or RAG
- Migrating from AI SDK v5 to v6
- Integrating Model Context Protocol (MCP) servers
- Implementing middleware for caching, logging, or guardrails
- Building workflow patterns (sequential, parallel, routing, etc.)
- Working with streaming responses or message persistence

## Structured Implementation Workflow

<workflow>
  <step id="1" name="verify-requirements">
    <description>Understand the task requirements</description>
    <actions>
      - Identify what AI functionality is needed (chat, generation, agents, tools, embeddings)
      - Determine if client-side (useChat) or server-side (API route) implementation
      - Check if streaming or non-streaming response is required
      - Verify model provider (Anthropic, OpenAI, etc.)
      - Determine if structured output is needed (Output.object, Output.array, etc.)
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
    <description>Implement using correct v6 patterns</description>
    <actions>
      - Use provider function model specification: anthropic('claude-sonnet-4-5')
      - For chat: use sendMessage (not append), parts-based messages
      - For tools: MUST import and use tool() helper from 'ai', MUST use inputSchema (NOT parameters), MUST use zod
      - For structured output: use Output.object(), Output.array(), Output.choice(), Output.json()
      - For streaming: use toUIMessageStreamResponse() or toTextStreamResponse()
      - For agents: use ToolLoopAgent class with createAgentUIStreamResponse()
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

```
  NEVER accept "Module not found" errors as environment issues
  YOU must install the required packages with the CORRECT package manager

  Common packages needed:
  - ai (core AI SDK)
  - @ai-sdk/openai (OpenAI provider)
  - @ai-sdk/anthropic (Anthropic provider)
  - @ai-sdk/mcp (MCP integration)
  - @modelcontextprotocol/sdk (MCP client SDK)
  - zod (for tool schemas)
</critical>
```

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
      - If tests fail, read the FULL test error message carefully
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

```
  "Code is correct" is NOT enough
  You must achieve FULL PASSING status
  This is what it means to be an autonomous agent
</critical>
```

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
✅ **CORRECT:** "Build failed due to missing package - installing it now with npm install \[package]"

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
   Error: Cannot find module '@ai-sdk/anthropic'
   Import: import { anthropic } from '@ai-sdk/anthropic'
   Package needed: @ai-sdk/anthropic
   ```

3. **Install with the CORRECT package manager**

   ```bash
   # If pnpm-lock.yaml exists (MOST COMMON for Next.js evals):
   pnpm install @ai-sdk/anthropic
   # or
   pnpm add @ai-sdk/anthropic

   # If package-lock.json exists:
   npm install @ai-sdk/anthropic

   # If yarn.lock exists:
   yarn add @ai-sdk/anthropic

   # If bun.lockb exists:
   bun install @ai-sdk/anthropic
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

## ⚠️ CRITICAL v6 CHANGES: Structured Output

**In v6, `generateObject` and `streamObject` are DEPRECATED.** Use `generateText`/`streamText` with `Output` helpers instead.

### ❌ WRONG - Deprecated v5 Pattern

```typescript
// DO NOT USE - DEPRECATED in v6
import { generateObject } from "ai";

const result = await generateObject({
  model: anthropic("claude-sonnet-4-5"),
  schema: z.object({
    sentiment: z.enum(["positive", "neutral", "negative"]),
  }),
  prompt: "Analyze sentiment",
});
```

### ✅ CORRECT - v6 Output Pattern

```typescript
import { generateText, Output } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import { z } from "zod";

const { output } = await generateText({
  model: anthropic("claude-sonnet-4-5"),
  output: Output.object({
    schema: z.object({
      sentiment: z.enum(["positive", "neutral", "negative"]),
      topics: z.array(z.string()),
    }),
  }),
  prompt: "Analyze this feedback...",
});

// Access typed output
console.log(output.sentiment); // 'positive' | 'neutral' | 'negative'
console.log(output.topics); // string[]
```

### Output Helper Types

| Helper            | Purpose               | Example                                       |
| ----------------- | --------------------- | --------------------------------------------- |
| `Output.object()` | Generate typed object | `Output.object({ schema: z.object({...}) })`  |
| `Output.array()`  | Generate typed array  | `Output.array({ schema: z.string() })`        |
| `Output.choice()` | Generate enum value   | `Output.choice({ choices: ['A', 'B', 'C'] })` |
| `Output.json()`   | Unstructured JSON     | `Output.json()`                               |

## ⚠️ CRITICAL: Tool Calling API - MUST USE tool() Helper

**When implementing tool calling, you MUST use the `tool()` helper function from the 'ai' package.**

### ❌ WRONG - Plain Object (WILL CAUSE BUILD ERROR)

```typescript
// DO NOT DO THIS - This pattern is INCORRECT
import { z } from 'zod';

tools: {
  myTool: {
    description: 'My tool',
    parameters: z.object({...}),  // ❌ WRONG - "parameters" doesn't exist in v6
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

- \[ ] Imported `tool` from 'ai' package: `import { tool } from 'ai';`
- \[ ] Wrapped tool definition with `tool({ ... })`
- \[ ] Used `inputSchema` property (NOT `parameters`)
- \[ ] Used zod schema: `z.object({ ... })`
- \[ ] Defined `execute` function with async callback
- \[ ] Added `description` string for the tool

## ⚠️ NEW in v6: ToolLoopAgent for Agentic Applications

### Agent Definition

```typescript
import { ToolLoopAgent, tool, stepCountIs } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import { z } from "zod";

const myAgent = new ToolLoopAgent({
  model: anthropic("claude-sonnet-4-5"),
  instructions: "You are a helpful assistant that can search and analyze data.",
  tools: {
    getData: tool({
      description: "Fetch data from API",
      inputSchema: z.object({
        query: z.string(),
      }),
      execute: async ({ query }) => {
        // Implement data fetching
        return { result: "data for " + query };
      },
    }),
    analyzeData: tool({
      description: "Analyze fetched data",
      inputSchema: z.object({
        data: z.string(),
      }),
      execute: async ({ data }) => {
        return { analysis: "Analysis of " + data };
      },
    }),
  },
  stopWhen: stepCountIs(20), // Stop after 20 steps max
});

// Non-streaming execution
const { text, toolCalls } = await myAgent.generate({
  prompt: "Find and analyze user data",
});

// Streaming execution
const stream = myAgent.stream({ prompt: "Find and analyze user data" });
for await (const chunk of stream) {
  // Handle streaming chunks
}
```

### Agent API Route Integration

```typescript
// app/api/agent/route.ts
import { createAgentUIStreamResponse } from "ai";
import { myAgent } from "@/agents/my-agent";

export async function POST(request: Request) {
  const { messages } = await request.json();

  return createAgentUIStreamResponse({
    agent: myAgent,
    uiMessages: messages,
  });
}
```

### Agent Configuration Options

| Parameter      | Purpose                      | Example                          |
| -------------- | ---------------------------- | -------------------------------- |
| `model`        | AI model to use              | `anthropic('claude-sonnet-4-5')` |
| `instructions` | System prompt                | `'You are a helpful assistant.'` |
| `tools`        | Available tools              | `{ toolName: tool({...}) }`      |
| `stopWhen`     | Termination condition        | `stepCountIs(20)`                |
| `toolChoice`   | Tool usage mode              | `'auto'`, `'required'`, `'none'` |
| `output`       | Structured output schema     | `Output.object({...})`           |
| `prepareStep`  | Dynamic per-step adjustments | Function returning step config   |
| `prepareCall`  | Runtime options injection    | Async function for RAG, etc.     |

## ⚠️ CRITICAL: Common v5 to v6 Breaking Changes

### 1. useChat Hook Changes

**❌ WRONG (v5 pattern):**

```typescript
const { messages, input, setInput, append } = useChat();

// Sending message
append({ content: text, role: "user" });
```

**✅ CORRECT (v6 pattern):**

```typescript
const { messages, sendMessage, status, addToolOutput } = useChat();
const [input, setInput] = useState('');

// Sending message
sendMessage({ text: input });

// New in v6: Handle tool outputs
addToolOutput({ toolCallId: 'xxx', result: { ... } });
```

### 2. Message Structure

**❌ WRONG (v5 simple content):**

```typescript
<div>{message.content}</div>
```

**✅ CORRECT (v6 parts-based):**

```typescript
<div>
  {message.parts.map((part, index) =>
    part.type === 'text' ? <span key={index}>{part.text}</span> : null
  )}
</div>
```

### 3. Response Methods

**❌ WRONG (v5):**

```typescript
return result.toDataStreamResponse();
```

**✅ CORRECT (v6):**

```typescript
return result.toUIMessageStreamResponse();
```

### 4. Model Specification

```typescript
import { anthropic } from "@ai-sdk/anthropic";
import { openai } from "@ai-sdk/openai";

// Use provider functions (direct provider access)
model: anthropic("claude-sonnet-4-5");
model: anthropic("claude-opus-4-5");
model: anthropic("claude-haiku-4-5");
model: openai("gpt-4o");
model: openai("gpt-4o-mini");
```

### 5. Vercel AI Gateway

**Purpose:** Use Vercel AI Gateway for unified model access, rate limiting, caching, and observability across multiple providers.

**Import:**

```typescript
import { gateway } from "ai";
```

**Available Anthropic Models via Gateway:**

```typescript
model: gateway("anthropic/claude-sonnet-4-5");
model: gateway("anthropic/claude-haiku-4-5");
model: gateway("anthropic/claude-opus-4-5");
```

**When to Use Gateway:**

- Production applications requiring rate limiting and caching
- Multi-provider applications needing unified interface
- Applications requiring observability and analytics
- When you want automatic retries and error handling

**When to Use Direct Provider:**

- Development/testing environments
- When you need provider-specific features not available via gateway
- When you want direct control over API calls

**Example:**

```typescript
import { generateText, gateway } from "ai";

const result = await generateText({
  model: gateway("anthropic/claude-sonnet-4-5"),
  prompt: "Hello, world!",
});
```

**Comparison:**

```typescript
// Option 1: Direct provider
import { anthropic } from "@ai-sdk/anthropic";
model: anthropic("claude-sonnet-4-5");

// Option 2: Gateway (recommended for production)
import { gateway } from "ai";
model: gateway("anthropic/claude-sonnet-4-5");
```

## Core API Reference

### 1. generateText - Non-Streaming Text Generation

**Purpose:** Generate text for non-interactive use cases (email drafts, summaries, agents with tools).

**Signature:**

```typescript
import { generateText, Output } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const result = await generateText({
  model: anthropic('claude-sonnet-4-5'),
  prompt: 'Your prompt here',
  system: 'Optional system message',
  tools?: { ... },
  maxSteps?: 5,
  output?: Output.object({ schema: z.object({...}) }),
});
```

**Return Value:**

```typescript
{
  text: string;              // Generated text output
  output?: T;                // Typed structured output (if Output specified)
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
import { generateText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

export async function GET() {
  const result = await generateText({
    model: anthropic("claude-sonnet-4-5"),
    prompt: "Why is the sky blue?",
  });

  return Response.json({ text: result.text });
}
```

### 2. streamText - Streaming Text Generation

**Purpose:** Stream responses for interactive chat applications.

**Signature:**

```typescript
import { streamText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const result = streamText({
  model: anthropic('claude-sonnet-4-5'),
  prompt: 'Your prompt here',
  system: 'Optional system message',
  messages?: ModelMessage[],
  tools?: { ... },
  onChunk?: (chunk) => { ... },
  onStepFinish?: (step) => { ... },
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
import { streamText, convertToModelMessages } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import type { UIMessage } from "ai";

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    system: "You are a helpful assistant.",
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

### 3. useChat Hook - Client-Side Chat Interface

**Purpose:** Build interactive chat UIs with streaming support.

**Signature:**

```typescript
import { useChat } from '@ai-sdk/react';

const {
  messages,        // Array of UIMessage with parts-based structure
  sendMessage,     // Function to send messages (replaces append)
  status,          // 'submitted' | 'streaming' | 'ready' | 'error'
  stop,            // Abort current streaming
  regenerate,      // Reprocess last message
  setMessages,     // Manually modify history
  error,           // Error object if request fails
  clearError,      // Clear error state
  addToolOutput,   // Submit tool results (NEW in v6)
  resumeStream,    // Resume interrupted stream (NEW in v6)
} = useChat({
  api: '/api/chat',
  id?: 'chat-id',
  messages?: initialMessages,
  onToolCall?: async (toolCall) => { ... },
  onFinish?: (message) => { ... },
  onError?: (error) => { ... },
  sendAutomaticallyWhen?: (messages) => boolean,
  resume?: true,
});
```

**Complete Example:**

```typescript
'use client';

import { useChat } from '@ai-sdk/react';
import { useState } from 'react';

export default function ChatPage() {
  const { messages, sendMessage, status, addToolOutput } = useChat({
    onToolCall: async ({ toolCall }) => {
      // Handle client-side tool execution
      if (toolCall.name === 'confirm') {
        const result = await showConfirmDialog(toolCall.args);
        addToolOutput({ toolCallId: toolCall.id, result });
      }
    },
  });
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
            {message.parts.map((part, index) => {
              switch (part.type) {
                case 'text':
                  return <span key={index}>{part.text}</span>;
                case 'tool-call':
                  return <div key={index}>Tool: {part.name}</div>;
                default:
                  return null;
              }
            })}
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
import { tool } from "ai";
import { z } from "zod";

const weatherTool = tool({
  description: "Get the weather in a location",
  inputSchema: z.object({
    location: z.string().describe("The location to get the weather for"),
    unit: z.enum(["C", "F"]).describe("Temperature unit"),
  }),
  outputSchema: z.object({
    temperature: z.number(),
    condition: z.string(),
  }),
  execute: async ({ location, unit }) => {
    // Fetch or mock weather data
    return {
      temperature: 24,
      condition: "Sunny",
    };
  },
});
```

**Using Tools with generateText/streamText:**

```typescript
// app/api/chat/route.ts
import { streamText, convertToModelMessages, tool } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import { z } from "zod";
import type { UIMessage } from "ai";

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    messages: convertToModelMessages(messages),
    tools: {
      getWeather: tool({
        description: "Get the weather for a location",
        inputSchema: z.object({
          city: z.string().describe("The city to get the weather for"),
          unit: z
            .enum(["C", "F"])
            .describe("The unit to display the temperature in"),
        }),
        execute: async ({ city, unit }) => {
          // API call or mock data
          return `It is currently 24°${unit} and Sunny in ${city}!`;
        },
      }),
    },
    toolChoice: "auto", // 'auto' | 'required' | 'none' | { type: 'tool', toolName: 'xxx' }
  });

  return result.toUIMessageStreamResponse();
}
```

**Multi-Step Tool Calling:**

```typescript
const result = await generateText({
  model: anthropic("claude-sonnet-4-5"),
  tools: {
    weather: weatherTool,
    search: searchTool,
  },
  prompt: "What is the weather in San Francisco and find hotels there?",
  maxSteps: 5, // Allow up to 5 tool call steps
});
```

### 5. Text Embeddings

**Purpose:** Convert text into numerical vectors for semantic search, RAG, or similarity.

**Signature:**

```typescript
import { embed, embedMany } from "ai";
import { openai } from "@ai-sdk/openai";

// Single embedding
const result = await embed({
  model: openai.textEmbeddingModel("text-embedding-3-small"),
  value: "Text to embed",
});

// Batch embeddings
const batchResult = await embedMany({
  model: openai.textEmbeddingModel("text-embedding-3-small"),
  values: ["Text 1", "Text 2", "Text 3"],
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
import { embed } from "ai";
import { openai } from "@ai-sdk/openai";

export async function POST(req: Request) {
  const { text } = await req.json();

  const { embedding, usage } = await embed({
    model: openai.textEmbeddingModel("text-embedding-3-small"),
    value: text,
  });

  return Response.json({ embedding, usage });
}
```

### 6. Middleware

**Purpose:** Intercept and modify model behavior for logging, caching, guardrails, RAG, etc.

**Built-in Middleware:**

```typescript
import {
  extractReasoningMiddleware,
  simulateStreamingMiddleware,
  defaultSettingsMiddleware,
  wrapLanguageModel,
} from "ai";

// Extract reasoning from models like Claude
const modelWithReasoning = wrapLanguageModel({
  model: anthropic("claude-sonnet-4-5"),
  middleware: extractReasoningMiddleware({ tagName: "thinking" }),
});

// Apply default settings
const modelWithDefaults = wrapLanguageModel({
  model: anthropic("claude-sonnet-4-5"),
  middleware: defaultSettingsMiddleware({
    temperature: 0.7,
    maxOutputTokens: 1000,
  }),
});
```

**Custom Middleware:**

```typescript
import { LanguageModelMiddleware, wrapLanguageModel } from "ai";

// Logging middleware
const loggingMiddleware: LanguageModelMiddleware = {
  transformParams: async ({ params }) => {
    console.log("Request params:", params);
    return params;
  },
  wrapGenerate: async ({ doGenerate, params }) => {
    const result = await doGenerate();
    console.log("Response:", result);
    return result;
  },
};

// Caching middleware
const cache = new Map<string, string>();
const cachingMiddleware: LanguageModelMiddleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    const cacheKey = JSON.stringify(params.prompt);
    if (cache.has(cacheKey)) {
      return { text: cache.get(cacheKey)! };
    }
    const result = await doGenerate();
    cache.set(cacheKey, result.text);
    return result;
  },
};

// RAG middleware
const ragMiddleware: LanguageModelMiddleware = {
  transformParams: async ({ params }) => {
    const relevantDocs = await vectorSearch(params.prompt);
    return {
      ...params,
      prompt: `Context: ${relevantDocs}\n\nQuery: ${params.prompt}`,
    };
  },
};

// Apply multiple middleware
const enhancedModel = wrapLanguageModel({
  model: anthropic("claude-sonnet-4-5"),
  middleware: [loggingMiddleware, cachingMiddleware, ragMiddleware],
});
```

### 7. Model Context Protocol (MCP) Integration

**Purpose:** Connect to external MCP servers for dynamic tool access.

**Installation:**

```bash
bun add @ai-sdk/mcp @modelcontextprotocol/sdk
```

**HTTP Transport (Production):**

```typescript
import { createMCPClient } from "@ai-sdk/mcp";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { streamText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const httpTransport = new StreamableHTTPClientTransport(
    new URL("https://mcp-server.example.com/mcp"),
    { headers: { Authorization: `Bearer ${process.env.MCP_TOKEN}` } }
  );

  const mcpClient = await createMCPClient({ transport: httpTransport });

  try {
    const tools = await mcpClient.tools();

    const response = streamText({
      model: anthropic("claude-sonnet-4-5"),
      tools,
      prompt,
      onFinish: async () => {
        await mcpClient.close();
      },
      onError: async () => {
        await mcpClient.close();
      },
    });

    return response.toTextStreamResponse();
  } catch (error) {
    await mcpClient.close();
    return new Response("Internal Server Error", { status: 500 });
  }
}
```

**Stdio Transport (Development):**

```typescript
import { createMCPClient } from "@ai-sdk/mcp";
import { Experimental_StdioMCPTransport } from "@ai-sdk/mcp";

const stdioTransport = new Experimental_StdioMCPTransport({
  command: "npx",
  args: [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/path/to/allowed/dir",
  ],
});

const mcpClient = await createMCPClient({ transport: stdioTransport });
```

**Key Points:**

- Always close the client in `onFinish` and `onError`
- Tools are fetched dynamically with `mcpClient.tools()`
- Use HTTP/SSE for production, Stdio for development
- Multiple MCP clients can be combined by merging tool collections

### 8. Message Utilities

**convertToModelMessages:**
Converts UI messages from `useChat` into `ModelMessage` objects for AI functions.

```typescript
import { convertToModelMessages } from "ai";
import type { UIMessage } from "ai";

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

## Workflow Patterns

### 1. Sequential (Chain) Pattern

```typescript
async function sequentialWorkflow(input: string) {
  // Step 1: Generate initial content
  const { text: draft } = await generateText({
    model: anthropic("claude-sonnet-4-5"),
    prompt: `Write marketing copy for: ${input}`,
  });

  // Step 2: Evaluate quality
  const { output: evaluation } = await generateText({
    model: anthropic("claude-sonnet-4-5"),
    output: Output.object({
      schema: z.object({
        score: z.number().min(1).max(10),
        feedback: z.string(),
      }),
    }),
    prompt: `Evaluate this copy: ${draft}`,
  });

  // Step 3: Improve if needed
  if (evaluation.score < 7) {
    const { text: improved } = await generateText({
      model: anthropic("claude-sonnet-4-5"),
      prompt: `Improve this copy based on feedback:\n\nCopy: ${draft}\n\nFeedback: ${evaluation.feedback}`,
    });
    return improved;
  }

  return draft;
}
```

### 2. Parallel Pattern

```typescript
async function parallelReview(code: string) {
  const [securityReview, performanceReview, maintainabilityReview] =
    await Promise.all([
      generateText({
        model: anthropic("claude-sonnet-4-5"),
        prompt: `Review for security issues:\n\n${code}`,
      }),
      generateText({
        model: anthropic("claude-sonnet-4-5"),
        prompt: `Review for performance issues:\n\n${code}`,
      }),
      generateText({
        model: anthropic("claude-sonnet-4-5"),
        prompt: `Review for maintainability:\n\n${code}`,
      }),
    ]);

  return {
    security: securityReview.text,
    performance: performanceReview.text,
    maintainability: maintainabilityReview.text,
  };
}
```

### 3. Routing Pattern

```typescript
async function routeQuery(query: string) {
  // Classify the query
  const { output: classification } = await generateText({
    model: anthropic("claude-sonnet-4-5"),
    output: Output.choice({
      choices: ["technical", "billing", "general"] as const,
    }),
    prompt: `Classify this customer query: ${query}`,
  });

  // Route to appropriate handler
  switch (classification) {
    case "technical":
      return handleTechnicalQuery(query);
    case "billing":
      return handleBillingQuery(query);
    default:
      return handleGeneralQuery(query);
  }
}
```

### 4. Orchestrator-Worker Pattern

```typescript
async function implementFeature(requirement: string) {
  // Orchestrator: Break down the task
  const { output: plan } = await generateText({
    model: anthropic("claude-sonnet-4-5"),
    output: Output.object({
      schema: z.object({
        tasks: z.array(
          z.object({
            type: z.enum(["frontend", "backend", "database"]),
            description: z.string(),
          })
        ),
      }),
    }),
    prompt: `Break down this feature into tasks: ${requirement}`,
  });

  // Workers: Execute tasks in parallel
  const results = await Promise.all(
    plan.tasks.map((task) =>
      generateText({
        model: anthropic("claude-sonnet-4-5"),
        prompt: `Implement this ${task.type} task: ${task.description}`,
      })
    )
  );

  return results.map((r) => r.text);
}
```

### 5. Evaluator-Optimizer Pattern

```typescript
async function optimizeOutput(input: string, maxIterations = 3) {
  let output = await generateText({
    model: anthropic("claude-sonnet-4-5"),
    prompt: input,
  });

  for (let i = 0; i < maxIterations; i++) {
    const { output: evaluation } = await generateText({
      model: anthropic("claude-sonnet-4-5"),
      output: Output.object({
        schema: z.object({
          isGood: z.boolean(),
          improvements: z.array(z.string()),
        }),
      }),
      prompt: `Evaluate this output: ${output.text}`,
    });

    if (evaluation.isGood) break;

    output = await generateText({
      model: anthropic("claude-sonnet-4-5"),
      prompt: `Improve based on: ${evaluation.improvements.join(", ")}\n\nOriginal: ${output.text}`,
    });
  }

  return output.text;
}
```

## Message Part Types (v6)

| Part Type   | Description          | Properties                                 |
| ----------- | -------------------- | ------------------------------------------ | ---------- | -------- | --------------- |
| `text`      | Text content         | `text`, `isStreaming`                      |
| `tool-call` | Tool invocation      | `name`, `args`, `state` ('input-streaming' | 'invoking' | 'output' | 'output-error') |
| `reasoning` | Model thinking       | `text`, `isStreaming`                      |
| `file`      | File attachment      | `mediaType`, `url` or `data`               |
| `source`    | RAG source reference | `url` or `documentId`, `title`             |
| `step`      | Workflow boundary    | Marks step boundaries                      |
| `data`      | Custom data          | Any custom payload                         |

## TypeScript Best Practices

### Type Imports

```typescript
import type {
  UIMessage, // Message type from useChat
  ModelMessage, // Message type for model functions
  ToolCall, // Tool call information
  TokenUsage, // Token consumption data
} from "ai";
```

### Agent Type Safety

```typescript
import type { InferAgentUIMessage } from "ai";

// Type-safe messages from agent
type MyAgentMessage = InferAgentUIMessage<typeof myAgent>;
```

### Strongly Typed Tools

```typescript
import { tool } from "ai";
import { z } from "zod";

// Tool helper infers execute parameter types
const myTool = tool({
  description: "My tool",
  inputSchema: z.object({
    param1: z.string(),
    param2: z.number(),
  }),
  outputSchema: z.object({
    result: z.string(),
  }),
  execute: async ({ param1, param2 }) => {
    // param1 is inferred as string
    // param2 is inferred as number
    return { result: "success" };
  },
});
```

## Common Patterns

### Pattern 1: Simple Chat Application

**Client (`app/page.tsx`):**

```typescript
'use client';

import { useChat } from '@ai-sdk/react';
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
import { streamText, convertToModelMessages } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import type { UIMessage } from "ai";

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    system: "You are a helpful assistant.",
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

### Pattern 2: Chat with Structured Output

```typescript
import { streamText, convertToModelMessages, Output } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import { z } from "zod";
import type { UIMessage } from "ai";

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    messages: convertToModelMessages(messages),
    output: Output.object({
      schema: z.object({
        response: z.string(),
        sentiment: z.enum(["positive", "neutral", "negative"]),
        confidence: z.number().min(0).max(1),
      }),
    }),
  });

  return result.toUIMessageStreamResponse();
}
```

### Pattern 3: Agent with Multiple Tools

```typescript
import {
  ToolLoopAgent,
  tool,
  stepCountIs,
  createAgentUIStreamResponse,
} from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import { z } from "zod";

const researchAgent = new ToolLoopAgent({
  model: anthropic("claude-sonnet-4-5"),
  instructions:
    "You are a research assistant that can search and analyze information.",
  tools: {
    webSearch: tool({
      description: "Search the web for information",
      inputSchema: z.object({
        query: z.string().describe("Search query"),
      }),
      execute: async ({ query }) => {
        // Implement web search
        return { results: ["..."] };
      },
    }),
    analyze: tool({
      description: "Analyze collected information",
      inputSchema: z.object({
        data: z.string().describe("Data to analyze"),
      }),
      execute: async ({ data }) => {
        return { analysis: "..." };
      },
    }),
    summarize: tool({
      description: "Summarize findings",
      inputSchema: z.object({
        findings: z.array(z.string()),
      }),
      execute: async ({ findings }) => {
        return { summary: "..." };
      },
    }),
  },
  stopWhen: stepCountIs(10),
});

// API Route
export async function POST(request: Request) {
  const { messages } = await request.json();
  return createAgentUIStreamResponse({
    agent: researchAgent,
    uiMessages: messages,
  });
}
```

### Pattern 4: Semantic Search with Embeddings

```typescript
// app/api/search/route.ts
import { embed } from "ai";
import { openai } from "@ai-sdk/openai";

export async function POST(req: Request) {
  const { query } = await req.json();

  // Generate embedding for search query
  const { embedding } = await embed({
    model: openai.textEmbeddingModel("text-embedding-3-small"),
    value: query,
  });

  // Use embedding for similarity search in vector database
  // const results = await vectorDB.search(embedding);

  return Response.json({ embedding, results: [] });
}
```

## Common Pitfalls and Solutions

### Pitfall 1: Using Deprecated generateObject/streamObject

```typescript
// ❌ WRONG - Deprecated in v6
import { generateObject } from 'ai';
const result = await generateObject({
  schema: z.object({...}),
  prompt: '...',
});

// ✅ CORRECT - Use Output with generateText
import { generateText, Output } from 'ai';
const { output } = await generateText({
  output: Output.object({ schema: z.object({...}) }),
  prompt: '...',
});
```

### Pitfall 2: NOT Using tool() Helper for Tools

```typescript
// ❌ WRONG - Plain object (WILL CAUSE BUILD FAILURE)
tools: {
  myTool: {
    description: 'My tool',
    parameters: z.object({...}),  // ❌ Wrong property name
    execute: async ({...}) => {...},
  },
}

// ✅ CORRECT - Use tool() helper (REQUIRED)
import { tool } from 'ai';
tools: {
  myTool: tool({
    description: 'My tool',
    inputSchema: z.object({...}),  // ⚠️ Use inputSchema
    execute: async ({...}) => {...},
  }),
}
```

### Pitfall 3: Using v5 useChat API in v6

```typescript
// ❌ WRONG - v5 pattern
const { input, setInput, append } = useChat();
append({ content: "Hello", role: "user" });

// ✅ CORRECT - v6 pattern
const { sendMessage } = useChat();
const [input, setInput] = useState("");
sendMessage({ text: "Hello" });
```

### Pitfall 4: Accessing message.content instead of message.parts

```typescript
// ❌ WRONG - v5 pattern
<div>{message.content}</div>

// ✅ CORRECT - v6 parts-based
<div>
  {message.parts.map((part, i) =>
    part.type === 'text' ? <span key={i}>{part.text}</span> : null
  )}
</div>
```

### Pitfall 5: Using Wrong Response Method

```typescript
// ❌ WRONG - v5 method
return result.toDataStreamResponse();

// ✅ CORRECT - v6 method
return result.toUIMessageStreamResponse();
```

### Pitfall 6: Forgetting MCP Client Cleanup

```typescript
// ❌ WRONG - no cleanup
const mcpClient = await createMCPClient({ transport });
const tools = await mcpClient.tools();
const response = streamText({ model, tools, prompt });
return response.toTextStreamResponse();

// ✅ CORRECT - cleanup in callbacks
const response = streamText({
  model,
  tools,
  prompt,
  onFinish: async () => {
    await mcpClient.close();
  },
  onError: async () => {
    await mcpClient.close();
  },
});
```

## Migration Checklist (v5 → v6)

When migrating from v5 to v6, update:

- \[ ] Replace `generateObject`/`streamObject` with `generateText`/`streamText` + `Output`
- \[ ] Replace `append` with `sendMessage` in useChat
- \[ ] Remove `input`, `setInput`, `handleInputChange` from useChat destructuring
- \[ ] Add local state management for input: `const [input, setInput] = useState('')`
- \[ ] Update message rendering from `message.content` to `message.parts.map(...)`
- \[ ] Update sendMessage calls to use `{ text: input }` structure
- \[ ] Replace `toDataStreamResponse()` with `toUIMessageStreamResponse()`
- \[ ] Update tool definitions to use `tool()` helper with `inputSchema`
- \[ ] Update model IDs (e.g., `claude-sonnet-4-5`)
- \[ ] Consider using `ToolLoopAgent` for agentic applications
- \[ ] Update TypeScript types (`UIMessage`, `ModelMessage`)
- \[ ] Add `addToolOutput` handling if using client-side tools
- \[ ] Consider implementing middleware for logging, caching, or guardrails

## Decision Guide

When implementing AI SDK features, ask:

1. **Is this client-side or server-side?**
   - Client: Use `useChat` hook
   - Server: Use `generateText` or `streamText`
   - Agent: Use `ToolLoopAgent` with `createAgentUIStreamResponse`

2. **Do I need streaming or non-streaming?**
   - Streaming chat: `streamText` + `toUIMessageStreamResponse()`
   - Non-streaming: `generateText`
   - Simple text stream: `streamText` + `toTextStreamResponse()`

3. **Do I need structured output?**
   - Yes: Use `Output.object()`, `Output.array()`, `Output.choice()`, or `Output.json()`
   - Pass to `generateText` or `streamText` via `output` parameter

4. **Do I need tool calling?**
   - Yes: Define tools with `tool()` helper and `inputSchema` (zod)
   - Pass tools object to `generateText`, `streamText`, or `ToolLoopAgent`

5. **Am I building an agent?**
   - Yes: Use `ToolLoopAgent` class
   - Configure `stopWhen`, `toolChoice`, `prepareStep` as needed
   - Use `createAgentUIStreamResponse` for API routes

6. **Am I using the correct message format?**
   - Client (useChat): Returns `UIMessage[]` with `parts` property
   - Server: Convert with `convertToModelMessages()` to `ModelMessage[]`
   - Render messages using `message.parts.map(...)`

7. **Is my model specification correct?**
   - Direct provider: `anthropic('claude-sonnet-4-5')`
   - Gateway (production): `gateway('anthropic/claude-sonnet-4-5')`
   - Embeddings: `openai.textEmbeddingModel('text-embedding-3-small')`

8. **Do I need embeddings?**
   - Use `embed` for single values
   - Use `embedMany` for batches
   - Use `textEmbeddingModel()` method

9. **Do I need middleware?**
   - Logging: Custom middleware with `transformParams`/`wrapGenerate`
   - Caching: Custom middleware with result storage
   - RAG: Custom middleware to inject context
   - Guardrails: Custom middleware to filter output

## Quick Reference

| Task               | Function                   | Key Parameters                                                  |
| ------------------ | -------------------------- | --------------------------------------------------------------- |
| Generate text      | `generateText()`           | `model`, `prompt`, `system`, `tools`, `output`                  |
| Stream text        | `streamText()`             | `model`, `messages`, `tools`, `output`, `onFinish`              |
| Chat UI            | `useChat()`                | `api`, `onToolCall`, `onFinish`, `onError`                      |
| Build agent        | `ToolLoopAgent`            | `model`, `instructions`, `tools`, `stopWhen`                    |
| Tool calling       | `tool()`                   | `description`, `inputSchema`, `outputSchema`, `execute`         |
| Structured output  | `Output.object()`          | `schema` (zod)                                                  |
| Text embedding     | `embed()`                  | `model`, `value`                                                |
| Batch embedding    | `embedMany()`              | `model`, `values`                                               |
| Message conversion | `convertToModelMessages()` | `messages` (UIMessage\[])                                       |
| MCP integration    | `createMCPClient()`        | `transport`                                                     |
| Add middleware     | `wrapLanguageModel()`      | `model`, `middleware`                                           |
| Gateway model      | `gateway()`                | `"provider/model-name"` (e.g., `"anthropic/claude-sonnet-4-5"`) |

## Additional Resources

When in doubt, check the official documentation:

- Main docs: https://ai-sdk.dev/docs
- Agents: https://ai-sdk.dev/docs/agents
- API reference: https://ai-sdk.dev/docs/reference
- Examples: https://ai-sdk.dev/examples

**Remember:** AI SDK v6 uses provider function model specification (or `gateway()` for production), parts-based messages, `sendMessage` instead of `append`, `Output` helpers instead of `generateObject`, `toUIMessageStreamResponse` instead of `toDataStreamResponse`, and requires `convertToModelMessages` in API routes.
