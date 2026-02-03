---
name: opper-api
description: >
  Use the Opper REST API directly via HTTP for AI task completion, structured output with JSON Schema, streaming via SSE, knowledge base semantic search, function management, and tracing. Activate when calling the Opper API with curl, fetch, or any HTTP client without using the Python or Node SDKs.
---

# Opper REST API

Call the Opper platform directly via HTTP for task completion, knowledge bases, streaming, and observability.

## Authentication

All requests require a Bearer token:

```bash
Authorization: Bearer $OPPER_API_KEY
```

Get your API key from [platform.opper.ai](https://platform.opper.ai).

## Base URL

```
https://api.opper.ai
```

## Core Endpoint: Task Completion

**POST /v2/call** — The primary endpoint. Describe a task and get structured results.

```bash
curl -X POST https://api.opper.ai/v2/call \
  -H "Authorization: Bearer $OPPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "extract_entities",
    "instructions": "Extract named entities from the text",
    "input": "Tim Cook announced Apple'\''s new office in Austin, Texas.",
    "output_schema": {
      "type": "object",
      "properties": {
        "people": {"type": "array", "items": {"type": "string"}},
        "locations": {"type": "array", "items": {"type": "string"}},
        "organizations": {"type": "array", "items": {"type": "string"}}
      },
      "required": ["people", "locations", "organizations"]
    }
  }'
```

**Response:**

```json
{
  "span_id": "550e8400-e29b-41d4-a716-446655440000",
  "json_payload": {
    "people": ["Tim Cook"],
    "locations": ["Austin", "Texas"],
    "organizations": ["Apple"]
  },
  "cached": false,
  "usage": {
    "input_tokens": 45,
    "output_tokens": 28,
    "total_tokens": 73
  },
  "cost": {
    "total": 0.00012,
    "generation": 0.0001,
    "platform": 0.00002
  }
}
```

## Request Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique task identifier (used for tracking and auto-creating functions) |
| `instructions` | No | What the model should do |
| `input` | No | The input data (string, object, or any JSON) |
| `input_schema` | No | JSON Schema validating the input |
| `output_schema` | No | JSON Schema for structured output |
| `model` | No | Model name or array of fallbacks (e.g., `"anthropic/claude-4-sonnet"`) |
| `examples` | No | Few-shot examples: `[{"input": ..., "output": ..., "comment": ...}]` |
| `parent_span_id` | No | UUID to link this call to a parent trace span |
| `tags` | No | Key-value metadata for filtering and cost attribution |

## Streaming

**POST /v2/call/stream** — Server-Sent Events for real-time token output.

```bash
curl -X POST https://api.opper.ai/v2/call/stream \
  -H "Authorization: Bearer $OPPER_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "name": "write_story",
    "instructions": "Write a short story",
    "input": "a robot learning to paint"
  }'
```

**SSE Response:**

```
data: {"delta": "Once", "chunk_type": "text"}

data: {"delta": " upon", "chunk_type": "text"}

data: {"delta": " a time", "chunk_type": "text"}

data: {"delta": "", "span_id": "...", "chunk_type": "text"}
```

## Model Selection

Specify any supported model:

```json
{
  "name": "task",
  "instructions": "...",
  "input": "...",
  "model": "anthropic/claude-4-sonnet"
}
```

With fallback chain:

```json
{
  "model": ["anthropic/claude-4-sonnet", "openai/gpt-4o"]
}
```

Common models: `openai/gpt-4o`, `openai/gpt-4o-mini`, `anthropic/claude-4-sonnet`, `anthropic/claude-4-opus`, `google/gemini-2.5-pro`.

## Few-Shot Examples

Guide model behavior with examples:

```json
{
  "name": "classify",
  "instructions": "Classify the support ticket",
  "input": "My payment failed",
  "examples": [
    {"input": "Can't log in", "output": "auth", "comment": "Login issues"},
    {"input": "Wrong charge", "output": "billing"}
  ]
}
```

## Structured Output with JSON Schema

The `output_schema` field accepts standard JSON Schema:

```json
{
  "output_schema": {
    "type": "object",
    "properties": {
      "sentiment": {
        "type": "string",
        "enum": ["positive", "negative", "neutral"]
      },
      "confidence": {
        "type": "number",
        "minimum": 0,
        "maximum": 1
      },
      "keywords": {
        "type": "array",
        "items": {"type": "string"},
        "maxItems": 5
      }
    },
    "required": ["sentiment", "confidence"]
  }
}
```

When `output_schema` is provided, the response uses `json_payload`. Without it, the response uses `message` (plain string).

## Tracing

Create spans to group related operations:

```bash
# Create a parent span
curl -X POST https://api.opper.ai/v2/spans \
  -H "Authorization: Bearer $OPPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "my_pipeline"}'

# Use the span_id as parent for subsequent calls
curl -X POST https://api.opper.ai/v2/call \
  -H "Authorization: Bearer $OPPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "step_one",
    "instructions": "...",
    "input": "...",
    "parent_span_id": "SPAN_ID_FROM_ABOVE"
  }'
```

## Knowledge Bases

Create and query semantic search indexes:

```bash
# Create a knowledge base
curl -X POST https://api.opper.ai/v2/knowledge \
  -H "Authorization: Bearer $OPPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "support_docs"}'

# Add a document
curl -X POST https://api.opper.ai/v2/knowledge/{id}/add \
  -H "Authorization: Bearer $OPPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "doc1",
    "content": "To reset your password, click Forgot Password.",
    "metadata": {"category": "auth"}
  }'

# Query
curl -X POST https://api.opper.ai/v2/knowledge/{id}/query \
  -H "Authorization: Bearer $OPPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "How to reset password?", "top_k": 3}'
```

## Error Handling

All errors return JSON with `detail` and appropriate HTTP status:

| Status | Meaning |
|--------|---------|
| 400 | Bad request / invalid input |
| 401 | Missing or invalid API key |
| 404 | Resource not found |
| 422 | Validation error |
| 502 | Upstream LLM provider error |

```json
{"detail": "Invalid output_schema: ..."}
```

## Common Mistakes

- **Missing `name` field**: Every call requires a unique `name` for tracking.
- **Wrong auth header**: Use `Authorization: Bearer <key>`, not `X-API-Key` or similar.
- **No `output_schema` but expecting JSON**: Without a schema, you get a plain string in `message`.
- **Forgetting `required` in schemas**: JSON Schema fields are optional by default.
- **Not checking `json_payload` vs `message`**: Structured calls use `json_payload`; unstructured use `message`.

## Additional Resources

- For the complete endpoint catalog, see [references/ENDPOINTS.md](references/ENDPOINTS.md)
- For knowledge base operations, see [references/KNOWLEDGE.md](references/KNOWLEDGE.md)
- For tracing and spans, see [references/TRACING.md](references/TRACING.md)

## Related Skills

- **opper-python-sdk**: Use when building in Python — provides a higher-level client wrapping this API.
- **opper-node-sdk**: Use when building in TypeScript — provides a typed client wrapping this API.
- **opper-python-agents**: Use when you need autonomous agents, not just single API calls.
- **opper-node-agents**: Use when you need autonomous agents in TypeScript.
- **opper-cli**: Use when calling Opper functions from the terminal.

## Upstream Sources

If this skill's content is outdated, check the canonical sources:

- **Documentation**: https://docs.opper.ai
- **API spec**: https://api.opper.ai/openapi.json
