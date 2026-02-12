---
name: subconscious-dev
description: "Build AI agents with Subconscious platform. Use when user wants to: build an agent, create an AI agent, use Subconscious, build with TIM, create agent with tools, research agent, search agent, tool-calling agent, subconscious.dev, TIMRUN, tim-gpt, tim-edge, tim-gpt-heavy. Do NOT use for generic OpenAI/Anthropic/LLM tasks without Subconscious."
---

# Building with Subconscious Platform

Subconscious is a platform for running AI agents with external tool use and long-horizon reasoning. **Key differentiator**: You kick off an agent with a single API call—define goals and tools, Subconscious handles orchestration, context management, and multi-hop reasoning automatically. No multi-agent frameworks needed.

## Quick Start

**Use the native Subconscious SDK** (recommended approach):

### Python

```python
from subconscious import Subconscious

client = Subconscious(api_key="your-api-key")  # Get from https://subconscious.dev/platform

run = client.run(
    engine="tim-gpt",
    input={
        "instructions": "Research quantum computing breakthroughs in 2025",
        "tools": []  # Optional: see Tools section below
    },
    options={"await_completion": True}
)

# Extract the answer for display
answer = run.result.answer  # Clean text response
print(answer)
```

### Node.js/TypeScript

```typescript
import { Subconscious } from "subconscious";

const client = new Subconscious({
  apiKey: process.env.SUBCONSCIOUS_API_KEY!,
});

const run = await client.run({
  engine: "tim-gpt",
  input: {
    instructions: "Research quantum computing breakthroughs in 2025",
    tools: [],  // Optional: see Tools section below
  },
  options: { awaitCompletion: true },
});

// Extract the answer for display
const answer = run.result?.answer;  // Clean text response
console.log(answer);
```

## Response Structure

**Critical**: The Subconscious SDK returns a different structure than OpenAI:

```typescript
{
  runId: "run_abc123...",
  status: "succeeded",
  result: {
    answer: "The clean text response for display",  // ← Use this for chat UIs
    reasoning: [  // Optional: step-by-step reasoning
      {
        title: "Step 1",
        thought: "I need to search for...",
        conclusion: "Found relevant information"
      }
    ]
  },
  usage: {
    inputTokens: 1234,
    outputTokens: 567,
    durationMs: 45000
  }
}
```

**For chat UIs, always use `run.result?.answer`** - this is the clean text response. The `reasoning` field contains internal reasoning steps (useful for debugging but not for display).

## Simple Chat Example (No Tools)

For conversational chat without tools:

### Python

```python
from subconscious import Subconscious

client = Subconscious(api_key="your-api-key")

# Convert message history to instructions format
messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there! How can I help?"},
    {"role": "user", "content": "Tell me about quantum computing"}
]

# Convert to instructions string
instructions = "\n\n".join([
    f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
    for m in messages
]) + "\n\nRespond to the user's latest message."

run = client.run(
    engine="tim-gpt",
    input={"instructions": instructions, "tools": []},
    options={"await_completion": True}
)

print(run.result.answer)  # Clean text response
```

### Node.js/TypeScript

```typescript
import { Subconscious } from "subconscious";

const client = new Subconscious({
  apiKey: process.env.SUBCONSCIOUS_API_KEY!,
});

const messages = [
  { role: "user", content: "Hello!" },
  { role: "assistant", content: "Hi there! How can I help?" },
  { role: "user", content: "Tell me about quantum computing" }
];

// Convert to instructions string
const instructions = messages
  .map(m => `${m.role === "user" ? "User" : "Assistant"}: ${m.content}`)
  .join("\n\n") + "\n\nRespond to the user's latest message.";

const run = await client.run({
  engine: "tim-gpt",
  input: { instructions, tools: [] },
  options: { awaitCompletion: true },
});

console.log(run.result?.answer);  // Clean text response
```

## Instructions Format vs Messages

**Important**: Subconscious uses `instructions` (single string), not `messages` array like OpenAI.

- **OpenAI format**: `messages: [{role: "user", content: "..."}]`
- **Subconscious format**: `input: {instructions: "..."}` (single string)

### Converting Messages to Instructions

```typescript
function buildInstructions(
  systemPrompt: string,
  messages: Array<{role: string; content: string}>
): string {
  const conversation = messages
    .map(m => `${m.role === "user" ? "User" : "Assistant"}: ${m.content}`)
    .join("\n\n");

  return `${systemPrompt}

## Conversation History

${conversation}

## Instructions

Respond to the user's latest message.`;
}

// Usage
const instructions = buildInstructions(
  "You are a helpful coding assistant. Be concise and use code examples.",
  messages
);
```

### System Prompts

Subconscious doesn't have a separate `system` field. Prepend your system prompt to the instructions:

```typescript
const systemPrompt = "You are a helpful assistant. Always be concise.";
const userMessage = "Explain quantum computing";

const instructions = `${systemPrompt}

User: ${userMessage}

Respond to the user's message.`;
```

## Choosing an Engine

| Engine | API Name | Type | Best For |
|--------|----------|------|----------|
| TIM-Edge | `tim-edge` | Unified (custom model + runtime) | Speed, efficiency, search-heavy tasks |
| TIM-GPT | `tim-gpt` | Compound (GPT-4.1 backed) | Most use cases, good balance of cost/performance |
| TIM-GPT-Heavy | `tim-gpt-heavy` | Compound (GPT-5.2 backed) | Maximum capability, complex reasoning |

**Recommendation**: Start with `tim-gpt` for most applications.

## Tools: The Key Differentiator

Subconscious tools are **remote HTTP endpoints**. When the agent needs to use a tool, Subconscious makes an HTTP POST to the URL you specify. This is fundamentally different from OpenAI function calling where YOU handle tool execution in a loop.

### Tool Definition Format

```python
tools = [
    {
        "type": "function",
        "name": "SearchTool",
        "description": "a general search engine returns title, url, and description of 10 webpages",
        "url": "https://your-server.com/search",  # YOUR hosted endpoint
        "method": "POST",
        "timeout": 10,  # seconds
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A natural language query for the search engine."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
]
```

**Key fields unique to Subconscious:**
- `url`: The HTTP endpoint Subconscious will call when the agent uses this tool
- `method`: HTTP method (typically POST)
- `timeout`: How long to wait for tool response (seconds)

The agent decides when and how to call tools. You don't manage a tool-call loop. Subconscious handles multi-hop reasoning internally via TIMRUN.

### Building a Tool Server

Your tool endpoint receives POST requests with parameters as JSON and returns JSON results.

**FastAPI (Python):**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search(req: SearchRequest):
    # Your search logic here
    return {
        "results": [
            {"title": "Result 1", "url": "https://example.com/1", "description": "..."}
        ]
    }

# Run with: uvicorn server:app --host 0.0.0.0 --port 8000
```

**Express.js (Node.js):**
```typescript
import express from "express";

const app = express();
app.use(express.json());

app.post("/search", (req, res) => {
  const { query } = req.body;
  // Your search logic here
  res.json({
    results: [
      { title: "Result 1", url: "https://example.com/1", description: "..." }
    ]
  });
});

app.listen(8000, () => console.log("Tool server running on :8000"));
```

**Important**: Your endpoint must be publicly accessible. For local development, use [ngrok](https://ngrok.com) or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/).

## Structured Output

Structured output allows you to define the exact shape of the agent's response using JSON Schema. This ensures you receive data in a predictable, parseable format.

### When to Use Structured Output

Use structured output when you need:
- Responses that integrate with other systems
- Consistent data formats for downstream processing
- Type-safe responses in your application

### Using answerFormat

The `answerFormat` field accepts a JSON Schema that defines the structure of the agent's answer:

**Python:**
```python
from subconscious import Subconscious

client = Subconscious(api_key="your-api-key")

run = client.run(
    engine="tim-gpt",
    input={
        "instructions": "Analyze the sentiment of this review: 'Great product, fast shipping!'",
        "tools": [],
        "answerFormat": {
            "type": "object",
            "title": "SentimentAnalysis",
            "properties": {
                "sentiment": {
                    "type": "string",
                    "enum": ["positive", "negative", "neutral"],
                    "description": "The overall sentiment"
                },
                "confidence": {
                    "type": "number",
                    "description": "Confidence score from 0 to 1"
                },
                "keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key phrases that influenced the sentiment"
                }
            },
            "required": ["sentiment", "confidence", "keywords"]
        }
    },
    options={"await_completion": True},
)

# Response is already a dict matching your schema - no parsing needed
result = run.result.answer
print(result["sentiment"])   # "positive"
print(result["confidence"])  # 0.95
print(result["keywords"])     # ["Great product", "fast shipping"]
```

**Node.js/TypeScript:**
```typescript
import { Subconscious } from "subconscious";

const client = new Subconscious({
  apiKey: process.env.SUBCONSCIOUS_API_KEY!,
});

const run = await client.run({
  engine: "tim-gpt",
  input: {
    instructions: "Analyze the sentiment of this review: 'Great product, fast shipping!'",
    tools: [],
    answerFormat: {
      type: "object",
      title: "SentimentAnalysis",
      properties: {
        sentiment: {
          type: "string",
          enum: ["positive", "negative", "neutral"],
          description: "The overall sentiment"
        },
        confidence: {
          type: "number",
          description: "Confidence score from 0 to 1"
        },
        keywords: {
          type: "array",
          items: { type: "string" },
          description: "Key phrases that influenced the sentiment"
        }
      },
      required: ["sentiment", "confidence", "keywords"]
    }
  },
  options: { awaitCompletion: true },
});

// Response is already an object matching your schema - no parsing needed
const result = run.result?.answer;
console.log(result.sentiment);   // "positive"
console.log(result.confidence);  // 0.95
console.log(result.keywords);     // ["Great product", "fast shipping"]
```

**Important**: When using `answerFormat`, `run.result.answer` returns a **parsed object** (dict in Python, object in JavaScript), not a JSON string. You can access fields directly without parsing.

### Using Pydantic Models (Python)

The Python SDK automatically converts Pydantic models to JSON Schema:

```python
from subconscious import Subconscious
from pydantic import BaseModel

class SentimentAnalysis(BaseModel):
    sentiment: str
    confidence: float
    keywords: list[str]

client = Subconscious(api_key="your-api-key")

run = client.run(
    engine="tim-gpt",
    input={
        "instructions": "Analyze the sentiment of: 'Great product!'",
        "answerFormat": SentimentAnalysis,  # Pass the class directly
    },
    options={"await_completion": True},
)

print(run.result.answer["sentiment"])
```

### Using Zod (Node.js/TypeScript)

For TypeScript, we recommend using [Zod](https://zod.dev) to define your schema:

```typescript
import { z } from 'zod';
import { Subconscious, zodToJsonSchema } from 'subconscious';

const AnalysisSchema = z.object({
  summary: z.string().describe('A brief summary of the findings'),
  keyPoints: z.array(z.string()).describe('Main takeaways'),
  sentiment: z.enum(['positive', 'neutral', 'negative']),
  confidence: z.number().describe('Confidence score from 0 to 1'),
});

const client = new Subconscious({
  apiKey: process.env.SUBCONSCIOUS_API_KEY!,
});

const run = await client.run({
  engine: 'tim-gpt',
  input: {
    instructions: 'Analyze the latest news about electric vehicles',
    tools: [{ type: 'platform', id: 'parallel_search' }],
    answerFormat: zodToJsonSchema(AnalysisSchema, 'Analysis'),
  },
  options: { awaitCompletion: true },
});

// Result is typed according to your schema
const result = run.result?.answer as z.infer<typeof AnalysisSchema>;
console.log(result.summary);
console.log(result.keyPoints);
```

### Structured Reasoning (Optional)

You can also structure the reasoning output using `reasoningFormat`:

```typescript
const ReasoningSchema = z.object({
  steps: z.array(z.object({
    thought: z.string(),
    action: z.string(),
  })),
  conclusion: z.string(),
});

const run = await client.run({
  engine: 'tim-gpt',
  input: {
    instructions: 'Research and analyze a topic',
    tools: [],
    reasoningFormat: zodToJsonSchema(ReasoningSchema, 'Reasoning'),
  },
  options: { awaitCompletion: true },
});

const reasoning = run.result?.reasoning;  // Structured reasoning
```

### Schema Requirements

- Must be valid JSON Schema
- Use `type: "object"` for structured responses
- Include `title` field for better results
- Define `properties` for each field
- Use `required` array for mandatory fields
- Set `additionalProperties: false` to prevent extra fields

See `references/api-reference.md` for more details on structured output.

## run() vs stream() - Critical Difference

### Use `run()` for Chat UIs (Recommended)

**Method**: `run({ options: { awaitCompletion: true } })`  
**Behavior**: Waits for completion, returns clean answer  
**What you get**: `run.result?.answer` = clean text for display  
**Best for**: Chat UIs, simple responses, production apps

```typescript
const run = await client.run({
  engine: "tim-gpt",
  input: { instructions: "Your prompt", tools: [] },
  options: { awaitCompletion: true }
});

const answer = run.result?.answer;  // Clean text - use this for display
const reasoning = run.result?.reasoning;  // Optional: step-by-step reasoning
```

### Use `stream()` for Real-time Reasoning Display

**Method**: `stream()`  
**Behavior**: Streams JSON incrementally as it's built  
**What you get**: Raw JSON chunks building toward: `{"reasoning": [...], "answer": "..."}`

**WARNING**: The stream content is raw JSON characters, not clean text. You must parse it.

#### What the stream looks like:

```
delta: {"rea
delta: soning": [{"th
delta: ought": "Analyzing
...
delta: "}], "answer": "Here's the answer"}
done: {runId: "run_xxx"}
```

#### When to use stream():

| Use Case | Method | Why |
|----------|--------|-----|
| Show thinking in real-time | `stream()` | Users see reasoning as it happens (like ChatGPT) |
| Simple chat, fast response | `run()` | Easier, returns clean `answer` directly |
| Background processing | `run()` without `awaitCompletion` | Poll for status |

#### How to use stream() for reasoning UI:

**See `references/streaming-and-reasoning.md` for complete implementation** including:
- How to extract thoughts from the JSON stream
- Next.js API route example
- React component for displaying reasoning
- CSS styling

**Quick example:**
```typescript
const stream = client.stream({
  engine: "tim-gpt",
  input: { instructions: "Your prompt", tools: [] }
});

let fullContent = "";
for await (const event of stream) {
  if (event.type === "delta") {
    fullContent += event.content;
    // Extract thoughts using regex (see streaming-and-reasoning.md)
    const thoughts = extractThoughts(fullContent);
    // Send to UI
  } else if (event.type === "done") {
    const final = JSON.parse(fullContent);
    const answer = final.answer;  // Extract final answer
  }
}
```

**For most chat UIs, use `run()` instead** - it's simpler and returns clean text directly.

## API Modes

### Sync Mode (Recommended for Chat)

```python
run = client.run(
    engine="tim-gpt",
    input={"instructions": "Your task", "tools": tools},
    options={"await_completion": True}
)
answer = run.result.answer  # Clean text
```

### Async Mode

For long-running jobs, don't set `await_completion`:

```python
run = client.run(
    engine="tim-gpt",
    input={"instructions": "Long task", "tools": tools}
    # No await_completion - returns immediately
)

run_id = run.run_id

# Poll for status
status = client.get(run_id)
while status.status not in ["succeeded", "failed"]:
    time.sleep(2)
    status = client.get(run_id)

answer = status.result.answer
```

### Streaming (Advanced)

See `references/examples.md` for streaming examples. **Note**: Streaming returns raw JSON, not clean text.

## SDK Methods Reference

| Method | Description | When to Use |
|--------|-------------|-------------|
| `client.run()` | Create a run (sync or async) | Most common - create agent runs |
| `client.stream()` | Stream run events in real-time | Chat UIs, live demos |
| `client.get(runId)` | Get current status of a run | Check async run status |
| `client.wait(runId)` | Poll until run completes | Background jobs, dashboards |
| `client.cancel(runId)` | Cancel a running/queued run | User cancellation, timeouts |

### client.get()

Get the current status of a run:

```python
status = client.get(run.run_id)
print(status.status)  # 'queued' | 'running' | 'succeeded' | 'failed'
if status.status == "succeeded":
    print(status.result.answer)
```

```typescript
const status = await client.get(run.runId);
console.log(status.status);
if (status.status === "succeeded") {
  console.log(status.result?.answer);
}
```

### client.wait()

Automatically poll until a run completes:

```python
result = client.wait(
    run.run_id,
    options={
        "interval_ms": 2000,  # Poll every 2 seconds (default)
        "max_attempts": 60,   # Max attempts before giving up (default: 60)
    },
)
```

```typescript
const result = await client.wait(run.runId, {
  intervalMs: 2000,  // Poll every 2 seconds
  maxAttempts: 60,   // Max attempts before giving up
});
```

### client.cancel()

Cancel a run that's still in progress:

```python
client.cancel(run.run_id)
```

```typescript
await client.cancel(run.runId);
```

## Common Patterns

### Research Agent

```python
tools = [
    {
        "type": "function",
        "name": "web_search",
        "description": "Search the web for current information",
        "url": "https://your-server.com/search",
        "method": "POST",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
]

run = client.run(
    engine="tim-gpt",
    input={
        "instructions": "Research the latest AI breakthroughs",
        "tools": tools
    },
    options={"await_completion": True}
)

print(run.result.answer)
```

### Multi-Tool Agent

Define multiple tools. The agent will chain them as needed:

```python
tools = [
    {
        "type": "function",
        "name": "search",
        "description": "Search the web",
        "url": "https://your-server.com/search",
        "method": "POST",
        "parameters": {...}
    },
    {
        "type": "function",
        "name": "save_to_db",
        "description": "Save results to database",
        "url": "https://your-server.com/save",
        "method": "POST",
        "parameters": {...}
    }
]
```

## TypeScript Types

### SDK Exports

```typescript
import {
  Subconscious,
  type RunResponse,
  type StreamEvent,
  type ReasoningStep,
  type Tool,
  type SubconsciousError
} from "subconscious";
```

### Response Types

```typescript
interface RunResponse {
  runId: string;
  status: "queued" | "running" | "succeeded" | "failed" | "canceled" | "timed_out";
  result?: {
    answer: string;  // Clean text response
    reasoning?: ReasoningStep[];  // Optional: step-by-step reasoning
  };
  usage?: {
    inputTokens: number;
    outputTokens: number;
    durationMs: number;
    toolCalls?: { [toolName: string]: number };
  };
  error?: {
    code: string;
    message: string;
  };
}

interface ReasoningStep {
  title?: string;
  thought?: string;
  conclusion?: string;
  tooluse?: {
    tool_name: string;
    parameters: Record<string, unknown>;
    tool_result: unknown;
  };
  subtasks?: ReasoningStep[];
}

interface StreamEvent {
  type: "delta" | "done" | "error";
  content?: string;  // Raw JSON chunk for delta events
  runId?: string;   // Present on done
  message?: string;  // Present on error
}
```

## Error Handling

### SDK Errors

```typescript
import { SubconsciousError } from "subconscious";

try {
  const run = await client.run({
    engine: "tim-gpt",
    input: { instructions: "...", tools: [] },
    options: { awaitCompletion: true }
  });
} catch (error) {
  if (error instanceof SubconsciousError) {
    switch (error.code) {
      case "invalid_api_key":
        // Redirect to settings
        console.error("Invalid API key");
        break;
      case "rate_limited":
        // Show retry message
        console.error("Rate limited, retry later");
        break;
      case "insufficient_credits":
        // Prompt to add credits
        console.error("Insufficient credits");
        break;
      case "invalid_request":
        // Log for debugging
        console.error("Invalid request:", error.message);
        break;
      case "timeout":
        // Offer to retry with longer timeout
        console.error("Request timed out");
        break;
      default:
        console.error("Error:", error.message);
    }
  } else {
    // Network or other errors
    console.error("Unexpected error:", error);
  }
}
```

### HTTP Status Codes

| Status | Code | Meaning | Action |
|--------|------|---------|--------|
| 400 | `invalid_request` | Bad request parameters | Fix request |
| 401 | `invalid_api_key` | Invalid or missing API key | Check API key |
| 402 | `insufficient_credits` | Account needs credits | Add credits |
| 429 | `rate_limited` | Too many requests | Retry after delay |
| 500 | `server_error` | Server error | Retry with backoff |
| 503 | `service_unavailable` | Service down | Retry later |

### Run-Level Errors

Runs can fail after being accepted. Always check status:

```typescript
const run = await client.run({...});

if (run.status === "succeeded") {
  console.log(run.result?.answer);
} else if (run.status === "failed") {
  console.error("Run failed:", run.error?.message);
} else if (run.status === "timed_out") {
  console.error("Run timed out");
}
```

## Request Cancellation

### Using AbortController

```typescript
const controller = new AbortController();

// Start the request
const runPromise = client.run({
  engine: "tim-gpt",
  input: { instructions: "...", tools: [] },
  options: { awaitCompletion: true }
});

// Cancel after 10 seconds
setTimeout(() => controller.abort(), 10000);

// Or cancel on user action
cancelButton.onclick = () => controller.abort();

try {
  const run = await runPromise;
} catch (error) {
  if (error.name === "AbortError") {
    console.log("Request cancelled by user");
  }
}
```

### Cancelling Async Runs

```typescript
// Start async run
const run = await client.run({
  engine: "tim-gpt",
  input: { instructions: "...", tools: [] }
  // No awaitCompletion
});

// Cancel it
await client.cancel(run.runId);
```

## Common Gotchas

### CRITICAL: Streaming Returns Raw JSON, Not Text

**The #1 mistake**: Displaying `event.content` from `stream()` directly in the UI shows ugly raw JSON like `{"reasoning":[{"thought":"I need to...`.

**The fix**: Extract thoughts and answer from the JSON:

```typescript
// BAD - shows raw JSON in UI
for await (const event of stream) {
  if (event.type === "delta") {
    displayToUser(event.content);  // Shows: {"rea... (ugly!)
  }
}

// GOOD - extract thoughts and show clean text
let fullContent = "";
let sentThoughts: string[] = [];

for await (const event of stream) {
  if (event.type === "delta") {
    fullContent += event.content;

    // Extract thoughts using regex
    const thoughtPattern = /"thought"\s*:\s*"((?:[^"\\]|\\.)*)"/g;
    let match;
    while ((match = thoughtPattern.exec(fullContent)) !== null) {
      const thought = match[1].replace(/\\n/g, " ").replace(/\\"/g, '"');
      if (!sentThoughts.includes(thought)) {
        displayThinking(thought);  // Shows: "I need to search for movies..."
        sentThoughts.push(thought);
      }
    }
  } else if (event.type === "done") {
    const parsed = JSON.parse(fullContent);
    displayAnswer(parsed.answer);  // Shows clean final answer
  }
}
```

See `references/streaming-and-reasoning.md` for complete implementation.

---

1. **Use `run.result?.answer` for display** - Not `choices[0].message.content` (that's OpenAI format)
2. **`stream()` returns raw JSON** - Use `run()` for clean text answers in chat UIs. See `references/streaming-and-reasoning.md` for parsing.
3. **No `/chat/completions` endpoint** - Use the native SDK, not OpenAI SDK
4. **Instructions format, not messages** - Convert message history to single string
5. **Tools must be publicly accessible** - Use ngrok for local development
6. **Response has `result.answer`** - The clean text is in `result.answer`, not `result.content`
7. **Reasoning field is optional** - Contains internal steps, useful for debugging
8. **Engine names**: Use `tim-edge`, `tim-gpt`, `tim-gpt-heavy` (not `tim-small`/`tim-large`)
9. **Streaming shows raw JSON** - You must parse `{"reasoning": [...], "answer": "..."}` yourself. For simple chat, use `run()` instead.
10. **`tools: []` is required** - Even if you have no tools, pass an empty array.
11. **No system message field** - Prepend system prompt to your instructions string.
12. **Always check `run.status`** - Don't access `run.result` without checking status first.

## Next.js/Vercel Example

See `references/examples.md` for complete Next.js API route example with Server-Sent Events.

## Production Checklist

### Security
- [ ] API key in environment variables, never client-side
- [ ] Rate limiting on your API routes
- [ ] Input validation (max message length, sanitization)
- [ ] CORS configuration for production domains

### Reliability
- [ ] Retry logic with exponential backoff for 5xx errors
- [ ] Timeout configuration (default may be too short for complex tasks)
- [ ] Graceful error messages for users
- [ ] Health check endpoint

### Monitoring
- [ ] Log `run.usage` for cost tracking
- [ ] Track `run.usage.durationMs` for latency monitoring
- [ ] Alert on error rate spikes
- [ ] Monitor `run.usage.toolCalls` for tool usage patterns

### UX
- [ ] Loading states while waiting for response
- [ ] Ability to cancel long-running requests
- [ ] Show reasoning/thinking indicators (if using stream())
- [ ] Error recovery (retry buttons)
- [ ] Clear error messages

### Cost Control
- [ ] Use `tim-edge` for simple tasks, `tim-gpt-heavy` only when needed
- [ ] Implement usage quotas per user if needed
- [ ] Monitor token usage in production

## Reference Files

For detailed information, see:
- `references/api-reference.md` - Complete API documentation with correct response formats
- `references/streaming-and-reasoning.md` - **CRITICAL**: How to stream and display reasoning steps (solves the raw JSON problem)
- `references/typescript-types.md` - Complete TypeScript type definitions
- `references/error-handling.md` - Error handling patterns and best practices
- `references/tools-guide.md` - Deep dive on tool system
- `references/examples.md` - Complete working examples including Next.js and reasoning display

## Resources

- **Docs**: https://docs.subconscious.dev
- **Platform**: https://subconscious.dev/platform
- **Playground**: https://subconscious.dev/playground
- **Python SDK**: https://github.com/subconscious-systems/subconscious-python
- **Node SDK**: https://github.com/subconscious-systems/subconscious-node
- **Examples**: https://github.com/subconscious-systems/subconscious/tree/main/examples

When in doubt, check the official docs at docs.subconscious.dev for the latest information.
