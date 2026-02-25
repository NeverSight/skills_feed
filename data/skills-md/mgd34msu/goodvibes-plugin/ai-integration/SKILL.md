---
name: ai-integration
description: "Load PROACTIVELY when task involves AI, LLM, or machine learning features. Use when user says \"add AI chat\", \"implement streaming responses\", \"build a RAG pipeline\", \"add embeddings\", or \"integrate OpenAI\". Covers chat interfaces, streaming with Vercel AI SDK, retrieval-augmented generation, vector search, embeddings pipelines, tool/function calling, and provider abstraction for OpenAI, Anthropic, and local models."
metadata:
  version: 1.0.0
  category: outcome
  tags: [ai, llm, chat, streaming, rag, embeddings, vector-search, function-calling]
---

## Resources
```
scripts/
  validate-ai-integration.sh
references/
  ai-patterns.md
```

# AI Integration Implementation

This skill guides you through integrating AI and LLM capabilities into applications, from basic chat interfaces to complex RAG pipelines and function calling. It leverages GoodVibes precision tools and project analysis for production-ready AI implementations.

## When to Use This Skill

Use this skill when you need to:

- Implement chat interfaces with LLM providers
- Add streaming response capabilities
- Build RAG (Retrieval Augmented Generation) pipelines
- Integrate embeddings and vector search
- Implement tool/function calling patterns
- Connect to OpenAI, Anthropic, or local models
- Handle AI API rate limiting and error recovery

## Workflow

Follow this sequence for AI integration:

### 1. Discover Existing AI Infrastructure

Before implementing AI features, understand the current state:

```yaml
detect_stack:
  project_root: "."
  categories: ["ai", "llm"]
```

This identifies:
- AI SDK in use (Vercel AI SDK, LangChain, LlamaIndex)
- LLM providers (OpenAI, Anthropic, Cohere)
- Vector databases (Pinecone, pgvector, Weaviate)
- Existing chat or completion endpoints
- Embedding generation patterns

**Check project memory for AI decisions:**

```yaml
precision_read:
  files:
    - path: ".goodvibes/memory/decisions.json"
    - path: ".goodvibes/memory/patterns.json"
  verbosity: minimal
```

Look for:
- Provider choices ("Use OpenAI GPT-4 for quality")
- Cost optimization patterns ("Cache embeddings for 24h")
- Streaming preferences ("Always stream for chat UIs")
- Known issues ("Anthropic rate limits on Claude Opus")

**Search for existing AI patterns:**

```yaml
precision_grep:
  queries:
    - id: openai-usage
      pattern: "import.*openai|from 'openai'"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: streaming-endpoints
      pattern: "stream|StreamingTextResponse|toDataStreamResponse"
      glob: "**/*.{ts,tsx}"
    - id: embeddings
      pattern: "embed|embedding|vector"
      glob: "**/*.{ts,tsx}"
  output:
    format: files_only
```

### 2. Provider Selection

Choose the appropriate AI provider and SDK based on requirements.

See: **[references/ai-patterns.md](references/ai-patterns.md)** for provider comparison.

**Key decision factors:**

| Need | Recommendation |
|------|----------------|
| Best model quality | OpenAI GPT-4 or Anthropic Claude Opus |
| Fastest responses | OpenAI GPT-4o or Anthropic Claude Haiku |
| Cost-effective | Anthropic Claude Haiku or GPT-4o-mini |
| Local/privacy | Ollama with Llama 3 or Mistral |
| Function calling | OpenAI (best support) or Anthropic |
| Long context | Anthropic Claude (200K tokens) |
| React integration | Vercel AI SDK |
| Complex workflows | LangChain or LlamaIndex |

**Install dependencies:**

```yaml
precision_exec:
  commands:
    - cmd: "npm install ai @ai-sdk/openai @ai-sdk/anthropic zod"
      expect:
        exit_code: 0
  verbosity: minimal
```

### 3. Configure API Keys

Securely manage API keys in environment variables.

**Check .env.example for documentation:**

```yaml
precision_read:
  files:
    - path: ".env.example"
  verbosity: minimal
```

**Add required environment variables:**

```yaml
precision_edit:
  operations:
    - file: ".env.example"
      edits:
        - action: append
          content: |
            # AI Provider API Keys
            OPENAI_API_KEY=your_openai_api_key_here
            ANTHROPIC_API_KEY=sk-ant-...
            
            # Optional: Model configuration
            AI_MODEL=gpt-4o  # or gpt-4o-mini, claude-3-5-sonnet-20241022, etc.
            AI_TEMPERATURE=0.7
            AI_MAX_TOKENS=4096
  verbosity: minimal
```

**Validate no hardcoded keys exist:**

```yaml
precision_grep:
  queries:
    - id: hardcoded-keys
      pattern: "sk-[a-zA-Z0-9]{20,}"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: count_only
```

Expect count: 0. If found, move keys to environment variables immediately.

### 4. Implement Chat Interface

Create a chat endpoint and UI using the Vercel AI SDK pattern.

**Create API route:**

```yaml
precision_write:
  files:
    - path: "src/app/api/chat/route.ts"
      mode: fail_if_exists
      content: |
        import { openai } from '@ai-sdk/openai';
        import { streamText } from 'ai';
        
        export const runtime = 'edge'; // Optional: Edge runtime for low-latency responses. Remove if using Node-only modules (ws, fs, etc.)
        
        // Note: Import zod at the top of the file
        // import { z } from 'zod';
        
        export async function POST(req: Request) {
          // Validate input with Zod (shown here, omitted in later examples for brevity)
          const RequestSchema = z.object({
            messages: z.array(z.object({
              role: z.enum(['user', 'assistant', 'system']),
              content: z.string().max(10000),
            })),
          });
          const body = RequestSchema.safeParse(await req.json());
          if (!body.success) {
            return new Response('Invalid request', { status: 400 });
          }
          const { messages } = body.data;
        
          const result = streamText({
            model: openai('gpt-4o'),
            messages,
            temperature: 0.7,
            maxTokens: 4096,
          });
        
          return result.toDataStreamResponse();
        }
  verbosity: minimal
```

**Create chat UI component:**

```yaml
precision_write:
  files:
    - path: "src/components/chat.tsx"
      mode: fail_if_exists
      content: |
        'use client';
        
        import { useChat } from 'ai/react';
        
        export function Chat() {
          const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat();
        
          return (
            <div className="flex flex-col h-screen">
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((m) => (
                  <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-md px-4 py-2 rounded-lg ${
                      m.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'
                    }`}>
                      {m.content}
                    </div>
                  </div>
                ))}
                {isLoading && <div className="text-gray-500">Thinking...</div>}
              </div>
              <form onSubmit={handleSubmit} className="border-t p-4">
                <input
                  value={input}
                  onChange={handleInputChange}
                  placeholder="Type a message..."
                  className="w-full px-4 py-2 border rounded-lg"
                  disabled={isLoading}
                />
              </form>
            </div>
          );
        }
  verbosity: minimal
```

**Validate implementation:**

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
  verbosity: minimal
```

### 5. Implement Streaming Responses

Optimize chat UX with token-by-token streaming.

**Streaming is built into Vercel AI SDK** via `streamText()` and `useChat()`. The pattern above already streams.

**For custom streaming implementations:**

```yaml
precision_write:
  files:
    - path: "src/lib/streaming.ts"
      mode: fail_if_exists
      content: |
        import OpenAI from 'openai';
        
        const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
        
        export async function streamCompletion(prompt: string) {
          const stream = await openai.chat.completions.create({
            model: 'gpt-4o',
            messages: [{ role: 'user', content: prompt }],
            stream: true,
          });
        
          const encoder = new TextEncoder();
        
          return new ReadableStream({
            async start(controller) {
              for await (const chunk of stream) {
                const content = chunk.choices[0]?.delta?.content || '';
                if (content) {
                  controller.enqueue(encoder.encode(content));
                }
              }
              controller.close();
            },
          });
        }
  verbosity: minimal
```

**Server-Sent Events (SSE) alternative:**

```yaml
precision_write:
  files:
    - path: "src/app/api/stream/route.ts"
      mode: fail_if_exists
      content: |
        import OpenAI from 'openai';
        
        export const runtime = 'edge'; // Optional: Edge runtime for low-latency responses. Remove if using Node-only modules (ws, fs, etc.)
        
        export async function POST(req: Request) {
          // Add Zod validation as shown in first API route example
          const { prompt } = await req.json();
          const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
        
          const stream = await openai.chat.completions.create({
            model: 'gpt-4o',
            messages: [{ role: 'user', content: prompt }],
            stream: true,
          });
        
          const encoder = new TextEncoder();
        
          return new Response(
            new ReadableStream({
              async start(controller) {
                for await (const chunk of stream) {
                  const content = chunk.choices[0]?.delta?.content || '';
                  if (content) {
                    controller.enqueue(encoder.encode(`data: ${JSON.stringify({ content })}\n\n`));
                  }
                }
                controller.enqueue(encoder.encode('data: [DONE]\n\n'));
                controller.close();
              },
            }),
            {
              headers: {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
              },
            }
          );
        }
  verbosity: minimal
```

### 6. Build RAG Pipeline

Implement document ingestion, chunking, embedding, and retrieval.

**Step 6.1: Document Ingestion**

```yaml
precision_write:
  files:
    - path: "src/lib/rag/ingestion.ts"
      mode: fail_if_exists
      content: |
        import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
        
        export async function chunkDocument(text: string, metadata: Record<string, unknown> = {}) {
          const splitter = new RecursiveCharacterTextSplitter({
            chunkSize: 1000,
            chunkOverlap: 200,
            separators: ['\n\n', '\n', ' ', ''],
          });
        
          const chunks = await splitter.createDocuments([text], [metadata]);
          return chunks.map((chunk, index) => ({
            content: chunk.pageContent,
            metadata: { ...chunk.metadata, chunk_index: index },
          }));
        }
  verbosity: minimal
```

**Step 6.2: Generate Embeddings**

```yaml
precision_write:
  files:
    - path: "src/lib/rag/embeddings.ts"
      mode: fail_if_exists
      content: |
        import { embed } from 'ai';
        import { openai } from '@ai-sdk/openai';
        
        export async function generateEmbedding(text: string): Promise<number[]> {
          const { embedding } = await embed({
            model: openai.embedding('text-embedding-3-small'),
            value: text,
          });
          return embedding;
        }
        
        export async function generateEmbeddings(texts: string[]): Promise<number[][]> {
          return Promise.all(texts.map(generateEmbedding));
        }
  verbosity: minimal
```

**Step 6.3: Vector Storage (Pinecone example)**

```yaml
precision_write:
  files:
    - path: "src/lib/rag/vector-store.ts"
      mode: fail_if_exists
      content: |
        import { Pinecone } from '@pinecone-database/pinecone';
        import { generateEmbedding } from './embeddings';
        
        // Validate env vars at startup (example shown here, subsequent ! usage for brevity)
        const apiKey = process.env.PINECONE_API_KEY;
        if (!apiKey) throw new Error('PINECONE_API_KEY is required');
        const pinecone = new Pinecone({ apiKey });
        const index = pinecone.index('documents');
        
        export async function storeDocument(id: string, text: string, metadata: Record<string, unknown>) {
          const embedding = await generateEmbedding(text);
          await index.upsert([{
            id,
            values: embedding,
            metadata: { text, ...metadata },
          }]);
        }
        
        export async function searchSimilar(query: string, topK: number = 5) {
          const queryEmbedding = await generateEmbedding(query);
          const results = await index.query({
            vector: queryEmbedding,
            topK,
            includeMetadata: true,
          });
          return results.matches || [];
        }
  verbosity: minimal
```

**Step 6.4: RAG Completion Endpoint**

```yaml
precision_write:
  files:
    - path: "src/app/api/rag/route.ts"
      mode: fail_if_exists
      content: |
        import { openai } from '@ai-sdk/openai';
        import { streamText } from 'ai';
        import { searchSimilar } from '@/lib/rag/vector-store';
        
        export const runtime = 'edge'; // Optional: Edge runtime for low-latency responses. Remove if using Node-only modules (ws, fs, etc.)
        
        export async function POST(req: Request) {
          // Add Zod validation as shown in first API route example
          const { messages } = await req.json();
          const lastMessage = messages[messages.length - 1];
        
          // Retrieve relevant context
          const context = await searchSimilar(lastMessage.content, 3);
          const contextText = context
            .map((match) => match.metadata?.text || '')
            .join('\n\n');
        
          // Augment prompt with context
          const augmentedMessages = [
            {
              role: 'system',
              content: `You are a helpful assistant. Use the following context to answer the user's question:\n\n${contextText}`,
            },
            ...messages,
          ];
        
          const result = streamText({
            model: openai('gpt-4o'),
            messages: augmentedMessages,
          });
        
          return result.toDataStreamResponse();
        }
  verbosity: minimal
```

### 7. Implement Vector Search

Configure vector database for semantic search.

**Provider comparison:**

See: **[references/ai-patterns.md](references/ai-patterns.md)** for vector database comparison.

**Pinecone (managed):**

```yaml
precision_exec:
  commands:
    - cmd: "npm install @pinecone-database/pinecone"
      expect:
        exit_code: 0
  verbosity: minimal
```

**pgvector (PostgreSQL extension):**

```yaml
precision_write:
  files:
    - path: "src/lib/vector/pgvector.ts"
      mode: fail_if_exists
      content: |
        import { sql } from 'drizzle-orm';
        import { db } from '@/lib/db';
        
        export async function enablePgvector() {
          await db.execute(sql`CREATE EXTENSION IF NOT EXISTS vector`);
        }
        
        export async function searchSimilar(embedding: number[], limit: number = 5) {
          return db.execute(sql`
            SELECT id, content, metadata, 1 - (embedding <=> ${embedding}::vector) AS similarity
            FROM documents
            ORDER BY embedding <=> ${embedding}::vector
            LIMIT ${limit}
          `);
        }
  verbosity: minimal
```

**Weaviate (hybrid search):**

```yaml
precision_write:
  files:
    - path: "src/lib/vector/weaviate.ts"
      mode: fail_if_exists
      content: |
        import weaviate, { WeaviateClient } from 'weaviate-ts-client';
        
        const client: WeaviateClient = weaviate.client({
          scheme: 'https',
          host: process.env.WEAVIATE_HOST!,
          apiKey: { apiKey: process.env.WEAVIATE_API_KEY! },
        });
        
        export async function hybridSearch(query: string, limit: number = 5) {
          return client.graphql
            .get()
            .withClassName('Document')
            .withHybrid({ query, alpha: 0.5 })
            .withFields('content metadata _additional { score }')
            .withLimit(limit)
            .do();
        }
  verbosity: minimal
```

### 8. Implement Tool/Function Calling

Enable LLMs to call external functions and tools.

**Define tools with Zod schemas:**

```yaml
precision_write:
  files:
    - path: "src/lib/ai/tools.ts"
      mode: fail_if_exists
      content: |
        import { z } from 'zod';
        import { tool } from 'ai';
        
        export const weatherTool = tool({
          description: 'Get the current weather for a location',
          parameters: z.object({
            location: z.string().describe('City name or zip code'),
            unit: z.enum(['celsius', 'fahrenheit']).default('celsius'),
          }),
          execute: async ({ location, unit }) => {
            // Call weather API using URL constructor for safe param encoding
            const url = new URL('https://api.weather.com/v1/current');
            url.searchParams.set('location', location);
            url.searchParams.set('unit', unit);
            const response = await fetch(url);
            return response.json();
          },
        });
        
        export const calculatorTool = tool({
          description: 'Perform mathematical calculations',
          parameters: z.object({
            expression: z.string().describe('Mathematical expression to evaluate'),
          }),
          execute: async ({ expression }) => {
            // Safe eval using mathjs
            try {
              const { evaluate } = await import('mathjs');
              const result = evaluate(expression);
              return { result };
            } catch (error) {
              return { error: 'Invalid expression' };
            }
          },
        });
  verbosity: minimal
```

**Use tools in completions:**

```yaml
precision_write:
  files:
    - path: "src/app/api/chat-tools/route.ts"
      mode: fail_if_exists
      content: |
        import { openai } from '@ai-sdk/openai';
        import { streamText } from 'ai';
        import { weatherTool, calculatorTool } from '@/lib/ai/tools';
        
        export const runtime = 'edge'; // Optional: Edge runtime for low-latency responses. Remove if using Node-only modules (ws, fs, etc.)
        
        export async function POST(req: Request) {
          // Add Zod validation as shown in first API route example
          const { messages } = await req.json();
        
          const result = streamText({
            model: openai('gpt-4o'),
            messages,
            tools: {
              weather: weatherTool,
              calculator: calculatorTool,
            },
            maxSteps: 5, // Allow multi-step tool use
          });
        
          return result.toDataStreamResponse();
        }
  verbosity: minimal
```

**Handle tool results in UI:**

```yaml
precision_edit:
  operations:
    - file: "src/components/chat.tsx"
      edits:
        - action: replace
          old_text: "export function Chat() {"
          new_text: |
            export function Chat() {
              const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
                onToolCall: ({ toolCall }) => {
                  // Use proper logger in production: logger.info('Tool called:', toolCall.toolName, toolCall.args);
                  console.log('Tool called:', toolCall.toolName, toolCall.args);
                },
              });
  verbosity: minimal
```

### 9. Add Security and Rate Limiting

Protect against abuse and manage costs.

**Rate limiting middleware:**

```yaml
precision_write:
  files:
    - path: "src/middleware/rate-limit.ts"
      mode: fail_if_exists
      content: |
        import { Ratelimit } from '@upstash/ratelimit';
        import { Redis } from '@upstash/redis';
        
        const redis = new Redis({
          url: process.env.UPSTASH_REDIS_REST_URL!,
          token: process.env.UPSTASH_REDIS_REST_TOKEN!,
        });
        
        export const ratelimit = new Ratelimit({
          redis,
          limiter: Ratelimit.slidingWindow(10, '60 s'), // 10 requests per minute
          analytics: true,
        });
        
        export async function checkRateLimit(identifier: string) {
          const { success, limit, remaining, reset } = await ratelimit.limit(identifier);
          
          if (!success) {
            throw new Error(`Rate limit exceeded. Try again in ${Math.ceil((reset - Date.now()) / 1000)}s`);
          }
          
          return { limit, remaining, reset };
        }
  verbosity: minimal
```

**Apply rate limiting to routes:**

```yaml
precision_edit:
  operations:
    - file: "src/app/api/chat/route.ts"
      edits:
        - action: replace
          old_text: "export async function POST(req: Request) {"
          new_text: |
            import { checkRateLimit } from '@/middleware/rate-limit';
            
            export async function POST(req: Request) {
              const ip = req.headers.get('x-forwarded-for') || 'anonymous';
              
              try {
                await checkRateLimit(ip);
              } catch (error) {
                const message = error instanceof Error ? error.message : 'Rate limit exceeded';
                return new Response(message, { status: 429 });
              }
  verbosity: minimal
```

**Prompt injection prevention:**

```yaml
precision_write:
  files:
    - path: "src/lib/ai/safety.ts"
      mode: fail_if_exists
      content: |
        // Detect prompt injection attempts
        export function detectInjection(input: string): boolean {
          const injectionPatterns = [
            /ignore (previous|above|all) (instructions|prompts)/i,
            /you are now/i,
            /new instructions:/i,
            /system: /i,
            /<\w+>/, // HTML-like tags
          ];
          
          return injectionPatterns.some((pattern) => pattern.test(input));
        }
        
        // Sanitize user input
        export function sanitizeInput(input: string): string {
          // Remove potential injection markers
          return input
            .replace(/[<>]/g, '')
            .replace(/system:/gi, '')
            .trim()
            .slice(0, 10000); // Limit length
        }
  verbosity: minimal
```

**Content filtering:**

```yaml
precision_write:
  files:
    - path: "src/lib/ai/moderation.ts"
      mode: fail_if_exists
      content: |
        import OpenAI from 'openai';
        
        const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
        
        export async function moderateContent(text: string) {
          const moderation = await openai.moderations.create({ input: text });
          const result = moderation.results[0];
          
          if (result.flagged) {
            const categories = Object.entries(result.categories)
              .filter(([_, flagged]) => flagged)
              .map(([category]) => category);
            
            throw new Error(`Content flagged for: ${categories.join(', ')}`);
          }
          
          return result;
        }
  verbosity: minimal
```

### 10. Testing AI Integration

Implement deterministic testing strategies.

**Mock LLM responses:**

```yaml
precision_write:
  files:
    - path: "src/lib/ai/__tests__/chat.test.ts"
      mode: fail_if_exists
      content: |
        import { describe, it, expect, vi } from 'vitest';
        import { streamText } from 'ai';
        
        vi.mock('ai', () => ({
          streamText: vi.fn(),
        }));
        
        describe('Chat API', () => {
          it('should return streamed response', async () => {
            const mockStream = {
              toDataStreamResponse: () => new Response('mocked response'),
            };
            
            vi.mocked(streamText).mockResolvedValue(mockStream);
            
            import { POST } from '@/app/api/chat/route';
            
            const req = new Request('http://localhost/api/chat', {
              method: 'POST',
              body: JSON.stringify({ messages: [{ role: 'user', content: 'Hello' }] }),
            });
            const response = await POST(req);
            
            expect(response.ok).toBe(true);
          });
        });
  verbosity: minimal
```

**Test with deterministic seed:**

```yaml
precision_write:
  files:
    - path: "src/lib/ai/__tests__/embeddings.test.ts"
      mode: fail_if_exists
      content: |
        import { describe, it, expect } from 'vitest';
        import { generateEmbedding } from '../embeddings';
        
        describe('Embeddings', () => {
          // Mock AI SDK to prevent real API calls in tests
          vi.mock('ai', () => ({
            embed: vi.fn().mockResolvedValue({ embedding: new Array(1536).fill(0.1) })
          }));
          
          it('should generate consistent embeddings', async () => {
            const text = 'Hello world';
            const embedding1 = await generateEmbedding(text);
            const embedding2 = await generateEmbedding(text);
            
            // Embeddings should be very similar (cosine similarity)
            const similarity = cosineSimilarity(embedding1, embedding2);
            expect(similarity).toBeGreaterThan(0.99);
          });
        });
        
        function cosineSimilarity(a: number[], b: number[]): number {
          const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
          const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
          const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
          return dotProduct / (magnitudeA * magnitudeB);
        }
  verbosity: minimal
```

**Cost tracking:**

```yaml
precision_write:
  files:
    - path: "src/lib/ai/cost-tracker.ts"
      mode: fail_if_exists
      content: |
        import { Redis } from '@upstash/redis';
        
        const redis = new Redis({
          url: process.env.UPSTASH_REDIS_REST_URL!,
          token: process.env.UPSTASH_REDIS_REST_TOKEN!,
        });
        
        const MODEL_COSTS = {
          // Prices as of early 2026 -- verify current rates at provider sites
          'gpt-4o': { input: 0.0025, output: 0.01 }, // per 1K tokens
          'gpt-4o-mini': { input: 0.00015, output: 0.0006 },
          'claude-opus-4': { input: 0.015, output: 0.075 },
          'claude-sonnet-4-5': { input: 0.003, output: 0.015 },
          'claude-haiku-4-5': { input: 0.0008, output: 0.004 },
        };
        
        export async function trackUsage(
          model: keyof typeof MODEL_COSTS,
          inputTokens: number,
          outputTokens: number
        ) {
          const costs = MODEL_COSTS[model];
          const cost = (inputTokens / 1000) * costs.input + (outputTokens / 1000) * costs.output;
          
          const today = new Date().toISOString().split('T')[0];
          const key = `ai:cost:${today}`;
          
          await redis.incrbyfloat(key, cost);
          await redis.expire(key, 86400 * 90); // 90 days retention
          
          return cost;
        }
        
        export async function getTodayCost(): Promise<number> {
          const today = new Date().toISOString().split('T')[0];
          const cost = await redis.get<number>(`ai:cost:${today}`);
          return cost || 0;
        }
  verbosity: minimal
```

### 11. Validation

Run the validation script to ensure all AI integration requirements are met:

```yaml
precision_exec:
  commands:
    - cmd: "bash plugins/goodvibes/skills/outcome/ai-integration/scripts/validate-ai-integration.sh ."
      expect:
        exit_code: 0
  verbosity: standard
```

The validation script checks:

1. AI SDK or LLM library installed
2. API keys documented in .env.example
3. Streaming endpoints exist
4. No hardcoded API keys in source
5. Rate limiting configured
6. Error handling around AI calls
7. Token/cost tracking patterns

**Fix any violations before deploying.**

## Best Practices

### Error Handling

- Always wrap AI calls in try/catch blocks
- Handle rate limits with exponential backoff
- Implement circuit breakers for external APIs
- Log errors without exposing API keys

### Performance

- Cache embeddings for frequently accessed content
- Use streaming for long completions
- Batch embedding generation when possible
- Implement request deduplication

### Cost Management

- Set maximum token limits per request
- Track daily/monthly spending
- Use cheaper models for simple tasks
- Cache completions when appropriate

### Security

- Never commit API keys to source control
- Implement rate limiting per user/IP
- Sanitize user input before sending to LLMs
- Use content moderation for user-generated prompts
- Validate tool execution results

### Monitoring

- Track token usage and costs
- Monitor response latency
- Log successful and failed requests
- Alert on unusual spending patterns

## Common Pitfalls

1. **Forgetting to stream**: Always stream for chat interfaces to improve UX
2. **Ignoring rate limits**: Implement backoff and retry logic
3. **Hardcoding prompts**: Use template systems for maintainability
4. **Not chunking documents**: Large documents need chunking for RAG
5. **Skipping cost tracking**: AI costs can escalate quickly
6. **Trusting user input**: Always sanitize and validate
7. **No error boundaries**: Failures should degrade gracefully
8. **Oversized context**: Limit context to stay within token budgets

## Additional Resources

- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [LangChain Documentation](https://js.langchain.com/docs/)
- [Pinecone Documentation](https://docs.pinecone.io/)

See **[references/ai-patterns.md](references/ai-patterns.md)** for detailed provider comparisons and architecture patterns.
