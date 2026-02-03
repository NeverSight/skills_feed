---
name: opper-node-sdk
description: >
  Use the Opper Node/TypeScript SDK (opperai) for AI task completion, structured output with JSON Schema or Zod, knowledge base semantic search, streaming responses, and tracing. Activate when building TypeScript or JavaScript applications that need LLM-powered task completion, RAG pipelines, or AI function orchestration with the Opper platform.
---

# Opper Node SDK

Build AI-powered applications in TypeScript with declarative task completion, structured outputs, knowledge bases, streaming, and full observability.

## Installation

```bash
npm add opperai
# or: pnpm add opperai / yarn add opperai / bun add opperai
```

Set your API key:

```bash
export OPPER_HTTP_BEARER="your-api-key"
```

Get your API key from [platform.opper.ai](https://platform.opper.ai).

## Core Pattern: Task Completion

The `opper.call()` method is the primary interface. Describe a task and get structured results:

```typescript
import { Opper } from "opperai";

const opper = new Opper({
  httpBearer: process.env["OPPER_HTTP_BEARER"] ?? "",
});

// Simple call with structured output
const result = await opper.call({
  name: "extractRoom",
  instructions: "Extract details about the room from the provided text",
  input: "The Grand Hotel offers a luxurious suite with 3 rooms and an ocean view.",
  outputSchema: {
    type: "object",
    properties: {
      room_count: { type: "number" },
      view: { type: "string" },
      hotel_name: { type: "string" },
    },
    required: ["room_count", "view", "hotel_name"],
  },
});

console.log(result.jsonPayload);
// { room_count: 3, view: "ocean", hotel_name: "The Grand Hotel" }
```

## Structured Output with JSON Schema

Define input and output schemas for type-safe interactions:

```typescript
const result = await opper.call({
  name: "analyze_sentiment",
  instructions: "Analyze the sentiment of the given text",
  inputSchema: {
    type: "object",
    properties: {
      text: { type: "string", description: "Text to analyze" },
    },
    required: ["text"],
  },
  outputSchema: {
    type: "object",
    properties: {
      label: { type: "string", enum: ["positive", "negative", "neutral"] },
      confidence: { type: "number", description: "0.0 to 1.0" },
      reasoning: { type: "string" },
    },
    required: ["label", "confidence"],
  },
  input: { text: "I love this product!" },
});

console.log(result.jsonPayload);
// { label: "positive", confidence: 0.95, reasoning: "..." }
```

## Model Selection

Control which LLM to use with the `model` parameter:

```typescript
const result = await opper.call({
  name: "generate",
  instructions: "Write a haiku about the given topic",
  input: "autumn leaves",
  model: "anthropic/claude-4-sonnet",
});
```

Available models include providers like `openai/`, `anthropic/`, `google/`, and more.

## Few-Shot Examples

Guide model behavior with input/output examples:

```typescript
const result = await opper.call({
  name: "classify_ticket",
  instructions: "Classify the support ticket category",
  input: { text: "My payment was declined" },
  examples: [
    { input: { text: "I can't log in" }, output: "authentication" },
    { input: { text: "Charged twice" }, output: "billing" },
    { input: { text: "App crashes" }, output: "bug", comment: "Technical issues" },
  ],
});
```

## Streaming

Stream responses token-by-token using `opper.stream()`:

```typescript
const outer = await opper.stream({
  name: "write_story",
  instructions: "Write a short story about the given topic",
  input: "a robot learning to paint",
  outputSchema: {
    type: "object",
    properties: {
      title: { type: "string" },
      story: { type: "string" },
    },
    required: ["title", "story"],
  },
});

// Access the result stream directly
const stream = outer.result;

for await (const event of stream) {
  const delta = event.data?.delta;
  if (delta) {
    process.stdout.write(delta);
  }
}
```

## Tracing with Spans

Track operations by passing `parentSpanId`:

```typescript
// Create a span for grouping related calls
const result = await opper.call({
  name: "step_one",
  instructions: "First step of the pipeline",
  input: "data",
  parentSpanId: "123e4567-e89b-12d3-a456-426614174000",
  tags: {
    project: "my_project",
    user: "user_123",
  },
});
```

## Tags and Metadata

Add metadata for filtering and cost attribution:

```typescript
const result = await opper.call({
  name: "translate",
  instructions: "Translate to French",
  input: "Hello world",
  tags: {
    project: "website",
    environment: "production",
    user_id: "usr_123",
  },
});
```

## Error Handling

```typescript
import { Opper } from "opperai";
import * as errors from "opperai/models/errors";

try {
  const result = await opper.call({ name: "task", instructions: "...", input: "..." });
} catch (error) {
  if (error instanceof errors.OpperError) {
    console.error(`Status ${error.statusCode}: ${error.message}`);
    if (error instanceof errors.BadRequestError) {
      console.error("Details:", error.data$.detail);
    }
  }
}
```

## Common Mistakes

- **Missing `httpBearer`**: The SDK won't authenticate without it. Use environment variable `OPPER_HTTP_BEARER`.
- **Forgetting `required` in schemas**: JSON Schema fields are optional by default. Always specify `required`.
- **Not awaiting calls**: All SDK methods are async. Always `await` them.
- **Using Zod v4**: The SDK currently supports Zod v3.x only (`zod@^3.23.8`).

## Additional Resources

- For function CRUD operations and versioning, see [references/FUNCTIONS.md](references/FUNCTIONS.md)
- For knowledge base operations and RAG, see [references/KNOWLEDGE.md](references/KNOWLEDGE.md)
- For tracing and span operations, see [references/TRACING.md](references/TRACING.md)
- For advanced streaming patterns, see [references/STREAMING.md](references/STREAMING.md)

## Related Skills

- **opper-node-agents**: Use when you need autonomous agents with tool use, reasoning loops, and multi-step execution rather than single-shot task completion.
- **opper-python-sdk**: Use when building with Python instead of TypeScript.

## Upstream Sources

If this skill's content is outdated, check the canonical sources:

- **Source code**: https://github.com/opper-ai/opper-node
- **Documentation**: https://docs.opper.ai
