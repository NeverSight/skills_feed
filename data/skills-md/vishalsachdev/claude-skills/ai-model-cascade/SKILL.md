---
name: ai-model-cascade
description: A production-ready pattern for integrating AI models (specifically Google Gemini) with automatic fallback, retry logic, structured output via Zod schemas, and comprehensive error handling. Use when integrating AI/LLM APIs, need automatic fallback when models are overloaded, want type-safe structured responses, or building features requiring reliable AI generation.
---

# AI Model Cascade with Structured Output

A production-ready pattern for integrating AI models (specifically Google Gemini) with automatic fallback, retry logic, structured output via Zod schemas, and comprehensive error handling.

## When to use this skill

- Integrating AI/LLM APIs into your application
- Need automatic fallback when models are overloaded or rate-limited
- Want type-safe, structured responses from AI models
- Building features that require reliable AI generation
- Converting Zod schemas to LLM-compatible formats
- Implementing smart/fast generation modes with different model tiers

## Core Features

1. **Model Cascade** - Auto-fallback: lite → flash → pro
2. **Structured Output** - Zod schema → Gemini format conversion
3. **Retry Logic** - Automatic retry on 503/429 errors
4. **Token Tracking** - Log usage metrics for monitoring
5. **Timeout Support** - Prevent hanging requests
6. **Error Classification** - Distinguish retryable from fatal errors

## Implementation

### Step 1: Create Gemini Client

Create `lib/gemini-client.ts`:

```typescript
import { GoogleGenerativeAI, GenerationConfig, SchemaType } from '@google/generative-ai';
import { z } from 'zod';

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

const MODEL_CASCADE = [
  'gemini-2.5-flash-lite',
  'gemini-2.5-flash',
  'gemini-2.5-pro'
] as const;

type ValidModel = typeof MODEL_CASCADE[number];

interface GeminiModelConfig {
  generationConfig?: GenerationConfig;
  preferredModel?: string;
  timeoutMs?: number;
  zodSchema?: z.ZodType<any>;
}

function isValidModel(model: string): model is ValidModel {
  return MODEL_CASCADE.includes(model as ValidModel);
}

function isRetryableError(error: any): boolean {
  return error?.status === 503 ||
         error?.status === 429 ||
         error?.message?.includes('503') ||
         error?.message?.includes('429') ||
         error?.message?.includes('overload') ||
         error?.message?.includes('rate limit');
}

function getErrorType(error: any): string {
  if (error?.status === 503 || error?.message?.includes('503') || error?.message?.includes('overload')) {
    return 'overloaded';
  }
  if (error?.status === 429 || error?.message?.includes('429') || error?.message?.includes('rate limit')) {
    return 'rate limited';
  }
  if (error?.status === 401 || error?.message?.includes('401') || error?.message?.includes('unauthorized')) {
    return 'authentication failed';
  }
  if (error?.status === 400 || error?.message?.includes('400')) {
    return 'invalid request';
  }
  return 'unknown error';
}

function convertToGeminiSchema(jsonSchema: any): any {
  if (jsonSchema.anyOf || jsonSchema.oneOf) {
    const schemas = jsonSchema.anyOf || jsonSchema.oneOf;
    const nonNullSchemas = schemas.filter((s: any) => s.type !== 'null');

    if (nonNullSchemas.length === 1) {
      const converted = convertToGeminiSchema(nonNullSchemas[0]);
      converted.nullable = true;
      return converted;
    }

    if (nonNullSchemas.length > 0) {
      return convertToGeminiSchema(nonNullSchemas[0]);
    }
  }

  if (jsonSchema.type === 'object') {
    const properties: Record<string, any> = {};
    const required: string[] = jsonSchema.required || [];

    for (const [key, value] of Object.entries(jsonSchema.properties || {})) {
      properties[key] = convertToGeminiSchema(value);
    }

    return {
      type: SchemaType.OBJECT,
      properties,
      required
    };
  }

  if (jsonSchema.type === 'array') {
    const arraySchema: Record<string, any> = {
      type: SchemaType.ARRAY,
      items: jsonSchema.items ? convertToGeminiSchema(jsonSchema.items) : { type: SchemaType.STRING }
    };

    if (typeof jsonSchema.minItems === 'number') {
      arraySchema.minItems = jsonSchema.minItems;
    }
    if (typeof jsonSchema.maxItems === 'number') {
      arraySchema.maxItems = jsonSchema.maxItems;
    }

    return arraySchema;
  }

  if (jsonSchema.type === 'string') {
    const stringSchema: Record<string, any> = { type: SchemaType.STRING };
    if (typeof jsonSchema.pattern === 'string') {
      stringSchema.pattern = jsonSchema.pattern;
    }
    return stringSchema;
  }

  if (jsonSchema.type === 'number' || jsonSchema.type === 'integer') {
    return { type: SchemaType.NUMBER };
  }

  if (jsonSchema.type === 'boolean') {
    return { type: SchemaType.BOOLEAN };
  }

  return { type: SchemaType.STRING };
}

export async function generateWithFallback(
  prompt: string,
  config: GeminiModelConfig = {}
): Promise<string> {
  if (config.preferredModel && !isValidModel(config.preferredModel)) {
    console.warn(`Invalid preferredModel "${config.preferredModel}", using default cascade`);
  }

  const models = config.preferredModel && isValidModel(config.preferredModel)
    ? [config.preferredModel, ...MODEL_CASCADE.filter(m => m !== config.preferredModel)]
    : [...MODEL_CASCADE];

  let lastError: any;
  const attemptedModels: string[] = [];

  for (const modelName of models) {
    attemptedModels.push(modelName);

    try {
      let generationConfig = config.generationConfig;

      if (config.zodSchema) {
        try {
          const jsonSchema = z.toJSONSchema(config.zodSchema);
          const geminiSchema = convertToGeminiSchema(jsonSchema);
          generationConfig = {
            ...generationConfig,
            responseMimeType: "application/json",
            responseSchema: geminiSchema
          };
          console.log(`Using structured output with schema for ${modelName}`);
        } catch (schemaError) {
          console.error(`Failed to convert Zod schema to Gemini schema:`, schemaError);
          throw new Error(`Schema conversion failed: ${schemaError instanceof Error ? schemaError.message : 'Unknown error'}`);
        }
      }

      const model = genAI.getGenerativeModel({
        model: modelName,
        generationConfig
      });

      const requestStart = Date.now();
      const generatePromise = model.generateContent(prompt);

      const result = config.timeoutMs
        ? await Promise.race([
            generatePromise,
            new Promise((_, reject) =>
              setTimeout(() => reject(new Error('Request timeout')), config.timeoutMs)
            )
          ])
        : await generatePromise;

      const latencyMs = Date.now() - requestStart;
      const geminiResponse = (result as any).response;
      const response = geminiResponse.text();

      if (response) {
        const usage = geminiResponse?.usageMetadata || {};
        const promptTokens = usage.promptTokenCount ?? 'n/a';
        const candidateTokens = usage.candidatesTokenCount ?? usage.outputTokenCount ?? 'n/a';
        const totalTokens = usage.totalTokenCount ?? 'n/a';
        console.log(
          `[Gemini][${modelName}] latency=${latencyMs}ms promptChars=${prompt.length} ` +
          `promptTokens=${promptTokens} responseTokens=${candidateTokens} totalTokens=${totalTokens}`
        );
        console.log(`Content generated using ${modelName}`);
        return response;
      }

      console.warn(`Model ${modelName} returned empty response, trying next...`);
    } catch (error) {
      lastError = error;
      const errorType = getErrorType(error);

      if (!isRetryableError(error)) {
        console.error(`Model ${modelName} failed with non-retryable error (${errorType}):`, error);
        throw new Error(`Gemini API error (${errorType}): ${error instanceof Error ? error.message : 'Unknown error'}`);
      }

      console.log(`Model ${modelName} ${errorType}, trying next...`);
    }
  }

  const errorType = getErrorType(lastError);
  throw new Error(
    `All Gemini models failed after trying: ${attemptedModels.join(', ')}. ` +
    `Last error type: ${errorType}. ` +
    `${lastError instanceof Error ? lastError.message : 'Unknown error'}`
  );
}
```

### Step 2: Define Zod Schemas

Create `lib/schemas.ts`:

```typescript
import { z } from 'zod';

const timestampPattern = /^(?:\d{1,2}:)?\d{1,2}:\d{1,2}$/;

export const topicQuoteSchema = z.object({
  timestamp: z.string(),
  text: z.string()
});

export const topicGenerationSchema = z.array(
  z.object({
    title: z.string(),
    quote: topicQuoteSchema.optional()
  })
);

export const suggestedQuestionsSchema = z.array(z.string());

export const chatResponseSchema = z.object({
  answer: z.string(),
  timestamps: z.array(z.string().regex(timestampPattern)).max(5).optional()
});

export const summaryTakeawaySchema = z.object({
  label: z.string().min(1),
  insight: z.string().min(1),
  timestamps: z.array(z.string().regex(timestampPattern)).min(1).max(2)
});

export const summaryTakeawaysSchema = z.array(summaryTakeawaySchema).min(4).max(6);
```

## Usage Examples

### Example 1: Generate Structured Topics

```typescript
import { generateWithFallback } from '@/lib/gemini-client';
import { topicGenerationSchema } from '@/lib/schemas';

async function generateTopics(transcript: string) {
  const prompt = `
    Analyze this video transcript and identify 5 key topics.
    For each topic, provide a title and an interesting quote with timestamp.

    Transcript:
    ${transcript}
  `;

  try {
    const response = await generateWithFallback(prompt, {
      zodSchema: topicGenerationSchema,
      preferredModel: 'gemini-2.5-flash-lite', // Start with fastest
      timeoutMs: 60000 // 60 second timeout
    });

    // Response is guaranteed to match schema
    const topics = JSON.parse(response);
    return topics; // Type-safe!
  } catch (error) {
    console.error('Failed to generate topics:', error);
    throw error;
  }
}
```

**Benefits**:
- ✅ Automatic fallback if lite model is overloaded
- ✅ Type-safe response matching Zod schema
- ✅ Timeout protection
- ✅ Structured JSON output guaranteed

---

### Example 2: AI Chat with Citations

```typescript
import { generateWithFallback } from '@/lib/gemini-client';
import { chatResponseSchema } from '@/lib/schemas';

async function askQuestion(question: string, transcript: string, history: ChatMessage[]) {
  const conversationContext = history
    .map(msg => `${msg.role}: ${msg.content}`)
    .join('\n');

  const prompt = `
    Context: ${transcript}

    Previous conversation:
    ${conversationContext}

    User question: ${question}

    Provide a helpful answer with up to 5 relevant timestamps from the transcript.
  `;

  const response = await generateWithFallback(prompt, {
    zodSchema: chatResponseSchema,
    preferredModel: 'gemini-2.5-flash',
    timeoutMs: 30000
  });

  const parsed = JSON.parse(response);

  return {
    answer: parsed.answer,
    timestamps: parsed.timestamps || []
  };
}
```

---

### Example 3: Smart vs Fast Mode

```typescript
type GenerationMode = 'smart' | 'fast';

async function generateContent(text: string, mode: GenerationMode) {
  const modelPreference = mode === 'fast'
    ? 'gemini-2.5-flash-lite'  // Fastest, lower quality
    : 'gemini-2.5-flash';       // Balanced

  const prompt = mode === 'fast'
    ? `Quickly summarize: ${text}`
    : `Provide detailed analysis with examples: ${text}`;

  return await generateWithFallback(prompt, {
    preferredModel: modelPreference,
    timeoutMs: mode === 'fast' ? 15000 : 60000
  });
}
```

---

### Example 4: API Route Integration

```typescript
// app/api/generate-topics/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { generateWithFallback } from '@/lib/gemini-client';
import { topicGenerationSchema } from '@/lib/schemas';
import { z } from 'zod';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { transcript, mode } = body;

    const model = mode === 'fast' ? 'gemini-2.5-flash-lite' : 'gemini-2.5-flash';

    const response = await generateWithFallback(
      buildPrompt(transcript),
      {
        zodSchema: topicGenerationSchema,
        preferredModel: model,
        timeoutMs: 60000
      }
    );

    const topics = JSON.parse(response);

    return NextResponse.json({ topics });
  } catch (error) {
    console.error('Error generating topics:', error);

    // User-friendly error messages
    if (error.message.includes('timeout')) {
      return NextResponse.json(
        { error: 'Request took too long. Please try again.' },
        { status: 504 }
      );
    }

    return NextResponse.json(
      { error: 'Failed to generate topics' },
      { status: 500 }
    );
  }
}
```

---

### Example 5: Validation After Generation

```typescript
import { generateWithFallback } from '@/lib/gemini-client';
import { summaryTakeawaysSchema } from '@/lib/schemas';

async function generateSummary(transcript: string) {
  const response = await generateWithFallback(
    `Summarize this video with 4-6 key takeaways: ${transcript}`,
    {
      zodSchema: summaryTakeawaysSchema,
      timeoutMs: 60000
    }
  );

  const parsed = JSON.parse(response);

  // Zod validation ensures:
  // - Array has 4-6 items
  // - Each has label, insight, timestamps (1-2 items)
  // - Timestamps match HH:MM:SS or MM:SS pattern

  const validated = summaryTakeawaysSchema.parse(parsed);

  return validated; // Type-safe and validated!
}
```

---

## Advanced Patterns

### Pattern 1: Streaming Support (Future Enhancement)

```typescript
async function* generateStreaming(prompt: string, config: GeminiModelConfig) {
  const model = genAI.getGenerativeModel({
    model: config.preferredModel || 'gemini-2.5-flash'
  });

  const result = await model.generateContentStream(prompt);

  for await (const chunk of result.stream) {
    yield chunk.text();
  }
}

// Usage in API route
export async function POST(request: NextRequest) {
  const stream = generateStreaming(prompt, config);

  return new Response(
    new ReadableStream({
      async start(controller) {
        for await (const chunk of stream) {
          controller.enqueue(new TextEncoder().encode(chunk));
        }
        controller.close();
      }
    })
  );
}
```

---

### Pattern 2: Custom Error Recovery

```typescript
async function generateWithRetry(prompt: string, maxRetries = 2) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await generateWithFallback(prompt, {
        preferredModel: 'gemini-2.5-flash-lite'
      });
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;

      console.log(`Attempt ${attempt + 1} failed, retrying...`);
      await new Promise(resolve => setTimeout(resolve, 2000 * (attempt + 1)));
    }
  }
}
```

---

### Pattern 3: Prompt Templates

```typescript
const PROMPTS = {
  topics: (transcript: string) => `
    Analyze this video transcript and identify 5 key topics.
    Focus on unique insights and actionable information.

    Transcript:
    ${transcript}
  `,

  summary: (transcript: string) => `
    Create a concise summary with 5 key takeaways.
    Include relevant timestamps for each takeaway.

    Transcript:
    ${transcript}
  `,

  questions: (transcript: string, topics: string[]) => `
    Based on these topics: ${topics.join(', ')}
    Generate 5 thought-provoking questions about the video content.

    Transcript:
    ${transcript}
  `
};

// Usage
const topics = await generateWithFallback(
  PROMPTS.topics(transcript),
  { zodSchema: topicGenerationSchema }
);
```

---

## Environment Setup

```bash
# .env.local
GEMINI_API_KEY=your-api-key-here
```

Get your API key: https://makersuite.google.com/app/apikey

---

## Best Practices

1. **Always use Zod schemas** for structured output - guarantees type safety
2. **Set timeouts** - Prevent hanging requests (15-60s depending on complexity)
3. **Start with lite model** - Falls back to more powerful models if needed
4. **Log token usage** - Monitor costs and optimize prompts
5. **Handle errors gracefully** - Distinguish timeout vs auth vs overload errors
6. **Use mode selection** - Let users choose fast vs quality
7. **Validate responses** - Even with schemas, validate critical fields

---

## Common Pitfalls

1. **Not handling JSON parse errors** - Even with schemas, parsing can fail
2. **Too aggressive timeouts** - Complex prompts need 30-60s
3. **Forgetting API key** - Check env vars are loaded
4. **Not testing cascade** - Simulate overload to test fallback
5. **Overly complex schemas** - Simpler schemas = more reliable results
6. **Missing error logs** - Log failures for debugging
7. **Not setting preferredModel** - Always specify based on use case

---

## Monitoring & Debugging

```typescript
// Add logging middleware
function withLogging(fn: typeof generateWithFallback) {
  return async (prompt: string, config: GeminiModelConfig) => {
    const start = Date.now();

    try {
      const result = await fn(prompt, config);
      const duration = Date.now() - start;

      console.log(`[AI] Success in ${duration}ms`);
      return result;
    } catch (error) {
      const duration = Date.now() - start;

      console.error(`[AI] Failed after ${duration}ms:`, error);
      throw error;
    }
  };
}

const generate = withLogging(generateWithFallback);
```

---

## Cost Optimization

```typescript
// Track token usage
class TokenTracker {
  private usage: Record<string, { calls: number; tokens: number }> = {};

  track(model: string, tokens: number) {
    if (!this.usage[model]) {
      this.usage[model] = { calls: 0, tokens: 0 };
    }
    this.usage[model].calls++;
    this.usage[model].tokens += tokens;
  }

  report() {
    console.table(this.usage);
  }
}

const tracker = new TokenTracker();

// In generateWithFallback, after success:
tracker.track(modelName, totalTokens);
```

---

## Testing

```typescript
// Mock for tests
jest.mock('@/lib/gemini-client', () => ({
  generateWithFallback: jest.fn(async (prompt, config) => {
    if (config.zodSchema) {
      return JSON.stringify({ title: 'Test Topic' });
    }
    return 'Test response';
  })
}));

// Test schema validation
test('validates response against schema', async () => {
  const response = await generateWithFallback(prompt, {
    zodSchema: topicGenerationSchema
  });

  const parsed = JSON.parse(response);
  expect(() => topicGenerationSchema.parse(parsed)).not.toThrow();
});
```

---

## Migration Guide

**From OpenAI to Gemini:**

```typescript
// Before (OpenAI)
const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: prompt }],
  response_format: { type: 'json_object' }
});

// After (Gemini with this skill)
const response = await generateWithFallback(prompt, {
  zodSchema: mySchema,
  preferredModel: 'gemini-2.5-flash'
});
```

---

## Next Steps

After implementing this skill:

1. Define Zod schemas for all AI outputs
2. Replace direct API calls with generateWithFallback
3. Add token usage monitoring
4. Implement smart/fast mode selection
5. Set up error alerts for cascade failures
6. Optimize prompts based on token usage

## Related Skills

- **Resilient Async Operations** - Combine with AbortManager for timeouts
- **Type-Safe Form Validation** - Zod patterns apply to both
- **Secure Next.js API Routes** - Protect AI endpoints with rate limiting

---

Built from production AI integration in [TLDW](https://github.com/vishalsachdev/tldw)
