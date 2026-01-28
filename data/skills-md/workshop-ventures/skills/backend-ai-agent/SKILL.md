---
name: backend-ai-agent
description: Create AI agents using Vercel AI SDK with tool use, tracing, and failover. Use when asked to "create an AI agent", "add AI", "create LLM integration", or "build an assistant".
---

# Backend AI Agent Creation

Create AI agents using the Vercel AI SDK with proper patterns for tool use, tracing, and error handling.

## Overview

The AI SDK supports:
- **One-off calls**: `generateText` and `generateObject` for single-purpose operations
- **Agentic workflows**: Multi-turn conversations with tool use

## Installation

```bash
npm install ai @ai-sdk/anthropic @ai-sdk/google @ai-sdk/openai zod
```

## Setup

### 1. Model Providers (`lib/ai/models.ts`)

```typescript
import { createAnthropic } from '@ai-sdk/anthropic';
import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { createOpenAI } from '@ai-sdk/openai';
import config from '../../config';

export const gemini = createGoogleGenerativeAI({ apiKey: config.gemini.apiKey });
export const claude = createAnthropic({ apiKey: config.anthropic.apiKey });
export const openai = createOpenAI({ apiKey: config.openai.apiKey });
```

### 2. Model Constants (in `@{project}/types`)

```typescript
export const LATEST_PRO_CLAUDE_MODEL = 'claude-sonnet-4-20250514';
export const LATEST_PRO_OPENAI_MODEL = 'gpt-4o-2025-04-15';
export const LATEST_PRO_GEMINI_MODEL = 'gemini-2.0-flash-exp';
export const CLAUDE_HAIKU_MODEL = 'claude-haiku-4.5-20250103';
export const GEMINI_FLASH_MODEL = 'gemini-2.0-flash-exp';

export type ModelProvider = 'openai' | 'claude' | 'gemini';
```

### 3. Config

Add to `apps/backend/src/config/index.ts`:

```typescript
anthropic: { apiKey: process.env.ANTHROPIC_API_KEY || '' },
openai: { apiKey: process.env.OPENAI_API_KEY || '' },
gemini: { apiKey: process.env.GEMINI_API_KEY || '' },
```

## One-Off LLM Calls

### Text Generation

```typescript
import { generateText } from 'ai';
import { gemini } from '../lib/ai/models';
import { GEMINI_FLASH_MODEL } from '@{project}/types';

export async function generateSummary(content: string): Promise<string | null> {
  try {
    const result = await generateText({
      model: gemini(GEMINI_FLASH_MODEL),
      prompt: `Summarize the following content:\n\n${content}`,
    });
    return result.text;
  } catch (err) {
    log.error({ err }, 'Error generating summary');
    return null;
  }
}
```

### Structured Output

```typescript
import { generateObject } from 'ai';
import { z } from 'zod/v4';

const TimeEstimateSchema = z.object({
  hours: z.number().int().min(0).describe('Estimated hours'),
  minutes: z.number().int().min(0).max(59).describe('Additional minutes'),
  reasoning: z.string().describe('Explanation'),
});

const result = await generateObject({
  model: gemini(GEMINI_FLASH_MODEL),
  schema: TimeEstimateSchema,
  prompt: `Estimate how long this task will take: ${task}`,
});
```

## Agentic Workflows

See [references/agent-patterns.md](references/agent-patterns.md) for complete examples including:
- Basic agent structure with conversation loop
- Tool creation patterns
- Model failover implementation

## Model Selection Guide

| Use Case | Recommended Model |
|----------|-------------------|
| Simple categorization | Gemini Flash, Claude Haiku |
| Short summaries | Gemini Flash |
| Complex reasoning | Claude Sonnet, GPT-4o |
| Agentic workflows | Claude Sonnet, GPT-4o |
| Maximum quality | Claude Opus |

## Best Practices

### Prompt Structure

```typescript
const prompt = `
  You are an expert at [specific task].

  <context>
  ${relevantContext}
  </context>

  <instructions>
  1. [First instruction]
  2. [Second instruction]
  </instructions>
`;
```

### Schema Design

Make schemas descriptive:

```typescript
const schema = z.object({
  category: z.enum(['urgent', 'normal', 'low'])
    .describe('Priority level based on deadline and impact'),
  confidence: z.number().min(0).max(1)
    .describe('Confidence score from 0 to 1'),
});
```

### Error Handling

Always handle errors gracefully with safe defaults:

```typescript
try {
  const result = await generateObject({ model, schema, prompt });
  return result.object;
} catch (error) {
  log.error({ error }, 'AI call failed');
  return { category: 'normal', confidence: 0, reasoning: 'Error occurred' };
}
```

### Token Limits

- One-off calls: `maxOutputTokens: 2048`
- Agentic workflows: `maxOutputTokens: 8192`
- Complex structured output: `maxOutputTokens: 16384`

## File Structure

```
apps/backend/src/lib/ai/
├── models.ts           # Model provider instances
├── failover.ts         # Failover utilities
├── agents/
│   └── MyAgent.ts      # Agent implementations
└── tools/
    └── myTools.ts      # Tool definitions
```

## Checklist

1. **Install dependencies**: `npm install ai @ai-sdk/anthropic @ai-sdk/google @ai-sdk/openai`
2. **Create** `lib/ai/models.ts` with provider instances
3. **Add** model constants to `@{project}/types`
4. **Add** API keys to config
5. **Create** agent class with conversation loop
6. **Create** tools with Zod parameters
7. **Implement** failover for critical operations
8. **Test** with realistic inputs
