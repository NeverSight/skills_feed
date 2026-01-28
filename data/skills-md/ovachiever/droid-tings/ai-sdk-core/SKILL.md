---
name: ai-sdk-core
description: |
  Build backend AI with Vercel AI SDK v5/v6. Covers v6 beta (Agent abstraction, tool approval, reranking),
  v4→v5 migration (breaking changes), latest models (GPT-5/5.1, Claude 4.x, Gemini 2.5), Workers startup
  fix, and 12 error solutions (AI_APICallError, AI_NoObjectGeneratedError, streamText silent errors).

  Use when: implementing AI SDK v5/v6, migrating v4→v5, troubleshooting errors, fixing Workers startup
  issues, or updating to latest models.
license: MIT
metadata:
  version: 1.2.0
  last_verified: 2025-11-22
  ai_sdk_version: 5.0.98 stable / 6.0.0-beta.107
  breaking_changes: true (v4→v5 migration guide included)
  production_tested: true
  keywords:
    - ai sdk core
    - vercel ai sdk
    - ai sdk v5
    - ai sdk v6 beta
    - ai sdk 6
    - agent abstraction
    - tool approval
    - reranking support
    - human in the loop
    - generateText
    - streamText
    - generateObject
    - streamObject
    - ai sdk node
    - ai sdk server
    - zod ai schema
    - ai schema validation
    - ai tool calling
    - ai agent class
    - openai sdk
    - anthropic sdk
    - google gemini sdk
    - cloudflare workers ai
    - workers-ai-provider
    - gpt-5
    - gpt-5.1
    - claude 4
    - claude sonnet 4.5
    - claude opus 4.1
    - gemini 2.5
    - ai streaming backend
    - multi-provider ai
    - ai provider abstraction
    - AI_APICallError
    - AI_NoObjectGeneratedError
    - ai sdk errors
    - structured ai output
    - backend llm integration
    - server-side ai generation
---

# AI SDK Core

Backend AI with Vercel AI SDK v5 and v6 Beta.

**Installation:**
```bash
npm install ai @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google zod
# Beta: npm install ai@beta @ai-sdk/openai@beta
```

---

## AI SDK 6 Beta (November 2025)

**Status:** Beta (stable release planned end of 2025)
**Latest:** ai@6.0.0-beta.107 (Nov 22, 2025)

### New Features

**1. Agent Abstraction**
Unified interface for building agents with `ToolLoopAgent` class:
- Full control over execution flow, tool loops, and state management
- Replaces manual tool calling orchestration

**2. Tool Execution Approval (Human-in-the-Loop)**
Request user confirmation before executing tools:
- Static approval: Always ask for specific tools
- Dynamic approval: Conditional based on tool inputs
- Native human-in-the-loop pattern

**3. Reranking Support**
Improve search relevance by reordering documents:
- Supported providers: Cohere, Amazon Bedrock, Together.ai
- Specialized reranking models for RAG workflows

**4. Structured Output (Stable)**
Combine multi-step tool calling with structured data generation:
- Multiple output strategies: objects, arrays, choices, text formats
- Now stable and production-ready in v6

**5. Call Options**
Dynamic runtime configuration:
- Type-safe parameter passing
- RAG integration, model selection, tool customization
- Provider-specific settings adjustments

**6. Image Editing (Coming Soon)**
Native support for image transformation workflows.

### Migration from v5

**Unlike v4→v5, v6 has minimal breaking changes:**
- Powered by v3 Language Model Specification
- Most users require no code changes
- Agent abstraction is additive (opt-in)

**Install Beta:**
```bash
npm install ai@beta @ai-sdk/openai@beta @ai-sdk/react@beta
```

**Official Docs:** https://ai-sdk.dev/docs/announcing-ai-sdk-6-beta

---

## Latest AI Models (2025)

### OpenAI

**GPT-5** (Aug 7, 2025):
- 45% less hallucination than GPT-4o
- State-of-the-art in math, coding, visual perception, health
- Available in ChatGPT, API, GitHub Models, Microsoft Copilot

**GPT-5.1** (Nov 13, 2025):
- Improved speed and efficiency over GPT-5
- Available in API platform

```typescript
import { openai } from '@ai-sdk/openai';
const gpt5 = openai('gpt-5');
const gpt51 = openai('gpt-5.1');
```

### Anthropic

**Claude 4 Family** (May-Oct 2025):
- **Opus 4** (May 22): Best for complex reasoning, $15/$75 per million tokens
- **Sonnet 4** (May 22): Balanced performance, $3/$15 per million tokens
- **Opus 4.1** (Aug 5): Enhanced agentic tasks, real-world coding
- **Sonnet 4.5** (Sept 29): Most capable for coding, agents, computer use
- **Haiku 4.5** (Oct 15): Small, fast, low-latency model

```typescript
import { anthropic } from '@ai-sdk/anthropic';
const sonnet45 = anthropic('claude-sonnet-4-5-20250929');  // Latest
const opus41 = anthropic('claude-opus-4-1-20250805');
const haiku45 = anthropic('claude-haiku-4-5-20251015');
```

### Google

**Gemini 2.5 Family** (Mar-Sept 2025):
- **Pro** (March 2025): Most intelligent, #1 on LMArena at launch
- **Pro Deep Think** (May 2025): Enhanced reasoning mode
- **Flash** (May 2025): Fast, cost-effective
- **Flash-Lite** (Sept 2025): Updated efficiency

```typescript
import { google } from '@ai-sdk/google';
const pro = google('gemini-2.5-pro');
const flash = google('gemini-2.5-flash');
const lite = google('gemini-2.5-flash-lite');
```

---

## v5 Core Functions (Basics)

**generateText()** - Text completion with tools
**streamText()** - Real-time streaming
**generateObject()** - Structured output (Zod schemas)
**streamObject()** - Streaming structured data

See official docs for usage: https://ai-sdk.dev/docs/ai-sdk-core

---

## Cloudflare Workers Startup Fix

**Problem:** AI SDK v5 + Zod causes >270ms startup time (exceeds Workers 400ms limit).

**Solution:**
```typescript
// ❌ BAD: Top-level imports cause startup overhead
import { createWorkersAI } from 'workers-ai-provider';
const workersai = createWorkersAI({ binding: env.AI });

// ✅ GOOD: Lazy initialization inside handler
app.post('/chat', async (c) => {
  const { createWorkersAI } = await import('workers-ai-provider');
  const workersai = createWorkersAI({ binding: c.env.AI });
  // ...
});
```

**Additional:**
- Minimize top-level Zod schemas
- Move complex schemas into route handlers
- Monitor startup time with Wrangler

---

## v5 Tool Calling Changes

**Breaking Changes:**
- `parameters` → `inputSchema` (Zod schema)
- Tool properties: `args` → `input`, `result` → `output`
- `ToolExecutionError` removed (now `tool-error` content parts)
- `maxSteps` parameter removed → Use `stopWhen(stepCountIs(n))`

**New in v5:**
- Dynamic tools (add tools at runtime based on context)
- Agent class (multi-step execution with tools)

---

## Critical v4→v5 Migration

AI SDK v5 introduced extensive breaking changes. If migrating from v4, follow this guide.

### Breaking Changes Overview

1. **Parameter Renames**
   - `maxTokens` → `maxOutputTokens`
   - `providerMetadata` → `providerOptions`

2. **Tool Definitions**
   - `parameters` → `inputSchema`
   - Tool properties: `args` → `input`, `result` → `output`

3. **Message Types**
   - `CoreMessage` → `ModelMessage`
   - `Message` → `UIMessage`
   - `convertToCoreMessages` → `convertToModelMessages`

4. **Tool Error Handling**
   - `ToolExecutionError` class removed
   - Now `tool-error` content parts
   - Enables automated retry

5. **Multi-Step Execution**
   - `maxSteps` → `stopWhen`
   - Use `stepCountIs()` or `hasToolCall()`

6. **Message Structure**
   - Simple `content` string → `parts` array
   - Parts: text, file, reasoning, tool-call, tool-result

7. **Streaming Architecture**
   - Single chunk → start/delta/end lifecycle
   - Unique IDs for concurrent streams

8. **Tool Streaming**
   - Enabled by default
   - `toolCallStreaming` option removed

9. **Package Reorganization**
   - `ai/rsc` → `@ai-sdk/rsc`
   - `ai/react` → `@ai-sdk/react`
   - `LangChainAdapter` → `@ai-sdk/langchain`

### Migration Examples

**Before (v4):**
```typescript
import { generateText } from 'ai';

const result = await generateText({
  model: openai.chat('gpt-4'),
  maxTokens: 500,
  providerMetadata: { openai: { user: 'user-123' } },
  tools: {
    weather: {
      description: 'Get weather',
      parameters: z.object({ location: z.string() }),
      execute: async (args) => { /* args.location */ },
    },
  },
  maxSteps: 5,
});
```

**After (v5):**
```typescript
import { generateText, tool, stopWhen, stepCountIs } from 'ai';

const result = await generateText({
  model: openai('gpt-4'),
  maxOutputTokens: 500,
  providerOptions: { openai: { user: 'user-123' } },
  tools: {
    weather: tool({
      description: 'Get weather',
      inputSchema: z.object({ location: z.string() }),
      execute: async ({ location }) => { /* input.location */ },
    }),
  },
  stopWhen: stepCountIs(5),
});
```

### Migration Checklist

- [ ] Update all `maxTokens` to `maxOutputTokens`
- [ ] Update `providerMetadata` to `providerOptions`
- [ ] Convert tool `parameters` to `inputSchema`
- [ ] Update tool execute functions: `args` → `input`
- [ ] Replace `maxSteps` with `stopWhen(stepCountIs(n))`
- [ ] Update message types: `CoreMessage` → `ModelMessage`
- [ ] Remove `ToolExecutionError` handling
- [ ] Update package imports (`ai/rsc` → `@ai-sdk/rsc`)
- [ ] Test streaming behavior (architecture changed)
- [ ] Update TypeScript types

### Automated Migration

AI SDK provides a migration tool:

```bash
npx ai migrate
```

This will update most breaking changes automatically. Review changes carefully.

**Official Migration Guide:**
https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0

---

## Top 12 Errors & Solutions

### 1. AI_APICallError

**Cause:** API request failed (network, auth, rate limit).

**Solution:**
```typescript
import { AI_APICallError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4'),
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof AI_APICallError) {
    console.error('API call failed:', error.message);
    console.error('Status code:', error.statusCode);
    console.error('Response:', error.responseBody);

    // Check common causes
    if (error.statusCode === 401) {
      // Invalid API key
    } else if (error.statusCode === 429) {
      // Rate limit - implement backoff
    } else if (error.statusCode >= 500) {
      // Provider issue - retry
    }
  }
}
```

**Prevention:**
- Validate API keys at startup
- Implement retry logic with exponential backoff
- Monitor rate limits
- Handle network errors gracefully

---

### 2. AI_NoObjectGeneratedError

**Cause:** Model didn't generate valid object matching schema.

**Solution:**
```typescript
import { AI_NoObjectGeneratedError } from 'ai';

try {
  const result = await generateObject({
    model: openai('gpt-4'),
    schema: z.object({ /* complex schema */ }),
    prompt: 'Generate data',
  });
} catch (error) {
  if (error instanceof AI_NoObjectGeneratedError) {
    console.error('No valid object generated');

    // Solutions:
    // 1. Simplify schema
    // 2. Add more context to prompt
    // 3. Provide examples in prompt
    // 4. Try different model (gpt-4 better than gpt-3.5 for complex objects)
  }
}
```

**Prevention:**
- Start with simple schemas, add complexity incrementally
- Include examples in prompt: "Generate a person like: { name: 'Alice', age: 30 }"
- Use GPT-4 for complex structured output
- Test schemas with sample data first

---

### 3. Worker Startup Limit (270ms+)

**Cause:** AI SDK v5 + Zod initialization overhead in Cloudflare Workers exceeds startup limits.

**Solution:**
```typescript
// BAD: Top-level imports cause startup overhead
import { createWorkersAI } from 'workers-ai-provider';
import { complexSchema } from './schemas';

const workersai = createWorkersAI({ binding: env.AI });

// GOOD: Lazy initialization inside handler
export default {
  async fetch(request, env) {
    const { createWorkersAI } = await import('workers-ai-provider');
    const workersai = createWorkersAI({ binding: env.AI });

    // Use workersai here
  }
}
```

**Prevention:**
- Move AI SDK imports inside route handlers
- Minimize top-level Zod schemas
- Monitor Worker startup time (must be <400ms)
- Use Wrangler's startup time reporting

**GitHub Issue:** Search for "Workers startup limit" in Vercel AI SDK issues

---

### 4. streamText Fails Silently

**Cause:** Stream errors can be swallowed by `createDataStreamResponse`.

**Status:** ✅ **RESOLVED** - Fixed in ai@4.1.22 (February 2025)

**Solution (Recommended):**
```typescript
// Use the onError callback (added in v4.1.22)
const stream = streamText({
  model: openai('gpt-4'),
  prompt: 'Hello',
  onError({ error }) {
    console.error('Stream error:', error);
    // Custom error logging and handling
  },
});

// Stream safely
for await (const chunk of stream.textStream) {
  process.stdout.write(chunk);
}
```

**Alternative (Manual try-catch):**
```typescript
// Fallback if not using onError callback
try {
  const stream = streamText({
    model: openai('gpt-4'),
    prompt: 'Hello',
  });

  for await (const chunk of stream.textStream) {
    process.stdout.write(chunk);
  }
} catch (error) {
  console.error('Stream error:', error);
}
```

**Prevention:**
- **Use `onError` callback** for proper error capture (recommended)
- Implement server-side error monitoring
- Test stream error handling explicitly
- Always log on server side in production

**GitHub Issue:** #4726 (RESOLVED)

---

### 5. AI_LoadAPIKeyError

**Cause:** Missing or invalid API key.

**Solution:**
```typescript
import { AI_LoadAPIKeyError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4'),
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof AI_LoadAPIKeyError) {
    console.error('API key error:', error.message);

    // Check:
    // 1. .env file exists and loaded
    // 2. Correct env variable name (OPENAI_API_KEY)
    // 3. Key format is valid (starts with sk-)
  }
}
```

**Prevention:**
- Validate API keys at application startup
- Use environment variable validation (e.g., zod)
- Provide clear error messages in development
- Document required environment variables

---

### 6. AI_InvalidArgumentError

**Cause:** Invalid parameters passed to function.

**Solution:**
```typescript
import { AI_InvalidArgumentError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4'),
    maxOutputTokens: -1,  // Invalid!
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof AI_InvalidArgumentError) {
    console.error('Invalid argument:', error.message);
    // Check parameter types and values
  }
}
```

**Prevention:**
- Use TypeScript for type checking
- Validate inputs before calling AI SDK functions
- Read function signatures carefully
- Check official docs for parameter constraints

---

### 7. AI_NoContentGeneratedError

**Cause:** Model generated no content (safety filters, etc.).

**Solution:**
```typescript
import { AI_NoContentGeneratedError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4'),
    prompt: 'Some prompt',
  });
} catch (error) {
  if (error instanceof AI_NoContentGeneratedError) {
    console.error('No content generated');

    // Possible causes:
    // 1. Safety filters blocked output
    // 2. Prompt triggered content policy
    // 3. Model configuration issue

    // Handle gracefully:
    return { text: 'Unable to generate response. Please try different input.' };
  }
}
```

**Prevention:**
- Sanitize user inputs
- Avoid prompts that may trigger safety filters
- Have fallback messaging
- Log occurrences for analysis

---

### 8. AI_TypeValidationError

**Cause:** Zod schema validation failed on generated output.

**Solution:**
```typescript
import { AI_TypeValidationError } from 'ai';

try {
  const result = await generateObject({
    model: openai('gpt-4'),
    schema: z.object({
      age: z.number().min(0).max(120),  // Strict validation
    }),
    prompt: 'Generate person',
  });
} catch (error) {
  if (error instanceof AI_TypeValidationError) {
    console.error('Validation failed:', error.message);

    // Solutions:
    // 1. Relax schema constraints
    // 2. Add more guidance in prompt
    // 3. Use .optional() for unreliable fields
  }
}
```

**Prevention:**
- Start with lenient schemas, tighten gradually
- Use `.optional()` for fields that may not always be present
- Add validation hints in field descriptions
- Test with various prompts

---

### 9. AI_RetryError

**Cause:** All retry attempts failed.

**Solution:**
```typescript
import { AI_RetryError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4'),
    prompt: 'Hello',
    maxRetries: 3,  // Default is 2
  });
} catch (error) {
  if (error instanceof AI_RetryError) {
    console.error('All retries failed');
    console.error('Last error:', error.lastError);

    // Check root cause:
    // - Persistent network issue
    // - Provider outage
    // - Invalid configuration
  }
}
```

**Prevention:**
- Investigate root cause of failures
- Adjust retry configuration if needed
- Implement circuit breaker pattern for provider outages
- Have fallback providers

---

### 10. Rate Limiting Errors

**Cause:** Exceeded provider rate limits (RPM/TPM).

**Solution:**
```typescript
// Implement exponential backoff
async function generateWithBackoff(prompt: string, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await generateText({
        model: openai('gpt-4'),
        prompt,
      });
    } catch (error) {
      if (error instanceof AI_APICallError && error.statusCode === 429) {
        const delay = Math.pow(2, i) * 1000;  // Exponential backoff
        console.log(`Rate limited, waiting ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Rate limit retries exhausted');
}
```

**Prevention:**
- Monitor rate limit headers
- Queue requests to stay under limits
- Upgrade provider tier if needed
- Implement request throttling

---

### 11. TypeScript Performance with Zod

**Cause:** Complex Zod schemas slow down TypeScript type checking.

**Solution:**
```typescript
// Instead of deeply nested schemas at top level:
// const complexSchema = z.object({ /* 100+ fields */ });

// Define inside functions or use type assertions:
function generateData() {
  const schema = z.object({ /* complex schema */ });
  return generateObject({ model: openai('gpt-4'), schema, prompt: '...' });
}

// Or use z.lazy() for recursive schemas:
type Category = { name: string; subcategories?: Category[] };
const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    subcategories: z.array(CategorySchema).optional(),
  })
);
```

**Prevention:**
- Avoid top-level complex schemas
- Use `z.lazy()` for recursive types
- Split large schemas into smaller ones
- Use type assertions where appropriate

**Official Docs:**
https://ai-sdk.dev/docs/troubleshooting/common-issues/slow-type-checking

---

### 12. Invalid JSON Response (Provider-Specific)

**Cause:** Some models occasionally return invalid JSON.

**Solution:**
```typescript
// Use built-in retry and mode selection
const result = await generateObject({
  model: openai('gpt-4'),
  schema: mySchema,
  prompt: 'Generate data',
  mode: 'json',  // Force JSON mode (supported by GPT-4)
  maxRetries: 3,  // Retry on invalid JSON
});

// Or catch and retry manually:
try {
  const result = await generateObject({
    model: openai('gpt-4'),
    schema: mySchema,
    prompt: 'Generate data',
  });
} catch (error) {
  // Retry with different model
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: mySchema,
    prompt: 'Generate data',
  });
}
```

**Prevention:**
- Use `mode: 'json'` when available
- Prefer GPT-4 for structured output
- Implement retry logic
- Validate responses

**GitHub Issue:** #4302 (Imagen 3.0 Invalid JSON)

---

**More Errors:** https://ai-sdk.dev/docs/reference/ai-sdk-errors (28 total)

---

## When to Use This Skill

### Use ai-sdk-core when:

- Building backend AI features (server-side text generation)
- Implementing server-side text generation (Node.js, Workers, Next.js)
- Creating structured AI outputs (JSON, forms, data extraction)
- Building AI agents with tools (multi-step workflows)
- Integrating multiple AI providers (OpenAI, Anthropic, Google, Cloudflare)
- Migrating from AI SDK v4 to v5
- Encountering AI SDK errors (AI_APICallError, AI_NoObjectGeneratedError, etc.)
- Using AI in Cloudflare Workers (with workers-ai-provider)
- Using AI in Next.js Server Components/Actions
- Need consistent API across different LLM providers

### Don't use this skill when:

- Building React chat UIs (use **ai-sdk-ui** skill instead)
- Need frontend hooks like useChat (use **ai-sdk-ui** skill instead)
- Need advanced topics like embeddings or image generation (check official docs)
- Building native Cloudflare Workers AI apps without multi-provider (use **cloudflare-workers-ai** skill instead)
- Need Generative UI / RSC (see https://ai-sdk.dev/docs/ai-sdk-rsc)

---

## Versions

**AI SDK:**
- Stable: ai@5.0.98 (Nov 20, 2025)
- Beta: ai@6.0.0-beta.107 (Nov 22, 2025)
- Zod 3.x/4.x both supported (3.23.8 recommended)

**Latest Models (2025):**
- OpenAI: GPT-5.1, GPT-5, o3
- Anthropic: Claude Sonnet 4.5, Opus 4.1, Haiku 4.5
- Google: Gemini 2.5 Pro/Flash/Lite

**Check Latest:**
```bash
npm view ai version
npm view ai dist-tags  # See beta versions
```

---

## Official Docs

**Core:**
- AI SDK 6 Beta: https://ai-sdk.dev/docs/announcing-ai-sdk-6-beta
- AI SDK Core: https://ai-sdk.dev/docs/ai-sdk-core/overview
- v4→v5 Migration: https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0
- All Errors (28): https://ai-sdk.dev/docs/reference/ai-sdk-errors
- Providers (25+): https://ai-sdk.dev/providers/overview

**GitHub:**
- Repository: https://github.com/vercel/ai
- Issues: https://github.com/vercel/ai/issues

---

**Last Updated:** 2025-11-22
**Skill Version:** 1.2.0
**AI SDK:** 5.0.98 stable / 6.0.0-beta.107
