---
name: opper-python-sdk
description: >
  Use the Opper Python SDK (opperai) for AI task completion, structured output with JSON Schema, knowledge base semantic search, and tracing/observability. Activate when building Python applications that need LLM-powered task completion, RAG pipelines, document indexing, or AI function orchestration with the Opper platform.
---

# Opper Python SDK

Build AI-powered applications with declarative task completion, structured outputs, knowledge bases, and full observability.

## Installation

```bash
pip install opperai
```

Set your API key:

```bash
export OPPER_HTTP_BEARER="your-api-key"
```

Get your API key from [platform.opper.ai](https://platform.opper.ai).

## Core Pattern: Task Completion

The `opper.call()` method is the primary interface. Describe a task declaratively and get results.

**Important**: The response field to read depends on whether you use `output_schema`:
- **No `output_schema`** → read `response.message` (returns `str`)
- **With `output_schema`** → read `response.json_payload` (returns `dict` or `list`)

```python
import os
from opperai import Opper

opper = Opper(http_bearer=os.environ["OPPER_HTTP_BEARER"])

# WITHOUT output_schema → use response.message (str)
response = opper.call(
    name="summarize",
    instructions="Summarize the text in one sentence",
    input="Opper is a platform for building reliable AI integrations...",
)
print(response.message)  # "Opper enables reliable AI integrations with structured outputs."

# WITH output_schema → use response.json_payload (dict)
response = opper.call(
    name="analyze_sentiment",
    instructions="Analyze the sentiment of the text",
    input="I love this product!",
    output_schema={
        "type": "object",
        "properties": {
            "label": {"type": "string"},
            "confidence": {"type": "number"},
        },
        "required": ["label", "confidence"],
    },
)
print(response.json_payload["label"])       # "positive"
print(response.json_payload["confidence"])  # 0.95
```

## Structured Output with Schema

Define output schemas using JSON Schema dictionaries:

```python
response = opper.call(
    name="extract_entities",
    instructions="Extract all named entities from the text",
    input="Tim Cook announced Apple's new office in Austin, Texas.",
    output_schema={
        "type": "object",
        "properties": {
            "people": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Names of people mentioned",
            },
            "locations": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Geographic locations",
            },
            "organizations": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Company or org names",
            },
        },
        "required": ["people", "locations", "organizations"],
    },
)
# response.json_payload["people"] => ["Tim Cook"]
# response.json_payload["locations"] => ["Austin", "Texas"]
# response.json_payload["organizations"] => ["Apple"]
```

## Model Selection

Specify which LLM to use via the `model` parameter:

```python
# Use a specific model
response = opper.call(
    name="generate",
    instructions="Write a haiku",
    input="autumn",
    model="anthropic/claude-4-sonnet",
)

# Use multiple models (fallback chain)
response = opper.call(
    name="generate",
    instructions="Write a haiku",
    input="autumn",
    model=["anthropic/claude-4-sonnet", "openai/gpt-4o"],
)
```

Available models include providers like `openai/`, `anthropic/`, `google/`, and more. Check the Opper dashboard for the full list.

## Few-Shot Examples

Provide examples to guide the model's behavior:

```python
response = opper.call(
    name="classify_ticket",
    instructions="Classify the support ticket",
    input="My payment was declined",
    examples=[
        {"input": "I can't log in", "output": "authentication"},
        {"input": "Charge me twice", "output": "billing"},
        {"input": "App crashes on start", "output": "bug"},
    ],
)
```

## Tracing and Observability

Track AI operations with spans and metrics:

```python
import os
from opperai import Opper

opper = Opper(http_bearer=os.environ["OPPER_HTTP_BEARER"])

# Create a span to group operations
span = opper.spans.create(name="qa_pipeline")

# Call with parent span for hierarchy
response = opper.call(
    name="answer",
    instructions="Answer the question accurately",
    input="What is Opper?",
    parent_span_id=span.id,
)

# Save a metric on the span
opper.span_metrics.create_metric(
    span_id=response.span_id,
    dimension="quality_score",
    value=4.5,
)

# List traces
traces = opper.traces.list()
```

## Knowledge Bases

Create and query semantic search indexes:

```python
import os
from opperai import Opper

opper = Opper(http_bearer=os.environ["OPPER_HTTP_BEARER"])

# Create a knowledge base
kb = opper.knowledge.create(name="support_docs")

# Add a document
opper.knowledge.add(
    knowledge_base_id=kb.id,
    content="To reset your password, click Forgot Password on the login page.",
    metadata={"category": "auth"},
)

# Query with semantic search
results = opper.knowledge.query(
    knowledge_base_id=kb.id,
    query="How do I change my password?",
    top_k=3,
)
for result in results:
    print(result.content, result.score)
```

## Tags and Metadata

Add metadata to calls for filtering and cost tracking:

```python
response = opper.call(
    name="translate",
    instructions="Translate to French",
    input="Hello world",
    tags={"project": "website", "user_id": "usr_123"},
)
```

## Authentication Note

The `OPPER_HTTP_BEARER` environment variable is your Opper API key. You can get it from [platform.opper.ai](https://platform.opper.ai) under your project settings. The SDK requires it to be passed explicitly:

```python
opper = Opper(http_bearer=os.environ["OPPER_HTTP_BEARER"])
```

## Common Mistakes

- **Missing `output_schema`**: Without it, the result is in `response.message` (string). Use schema dicts for structured data in `response.json_payload`.
- **Not using `name`**: Every call needs a unique name for tracking in the dashboard.
- **Not accessing response fields correctly**: Use `response.message` for string output, `response.json_payload` for structured output, and `response.span_id` for tracing.
- **Large inputs without chunking**: For large documents, split into chunks and use knowledge bases instead.

## Response Object Fields

The `opper.call()` method returns a response object with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `span_id` | str | The ID of the span for tracing |
| `message` | str \| None | Result when no `output_schema` is used |
| `json_payload` | dict/list \| None | Result when `output_schema` is used |
| `cached` | bool \| None | True if result was from cache |
| `usage` | dict \| None | Token usage (input/output/total) |
| `cost` | dict \| None | Cost in USD (total/generation/platform) |

### Accessing Results: `message` vs `json_payload`

**Use `response.message`** when calling WITHOUT `output_schema`:
```python
response = opper.call(
    name="summarize",
    instructions="Summarize in one sentence",
    input="...",
)
text = response.message  # Returns str: "Summary of the text."
```

**Use `response.json_payload`** when calling WITH `output_schema`:
```python
response = opper.call(
    name="extract",
    instructions="Extract entities",
    input="...",
    output_schema={"type": "object", "properties": {...}},
)
data = response.json_payload  # Returns dict: {"entities": [...]}
```

**Key rule**: If you pass `output_schema`, read from `json_payload`. If you don't, read from `message`.

## Additional Resources

- For function CRUD operations and versioning, see [references/FUNCTIONS.md](references/FUNCTIONS.md)
- For knowledge base operations and RAG patterns, see [references/KNOWLEDGE.md](references/KNOWLEDGE.md)
- For tracing, spans, and metrics, see [references/TRACING.md](references/TRACING.md)
- For streaming responses, see [references/STREAMING.md](references/STREAMING.md)

## Related Skills

- **opper-python-agents**: Use when you need autonomous agents with tool use, reasoning loops, and multi-step task execution rather than single-shot task completion.
- **opper-node-sdk**: Use when building with TypeScript/Node.js instead of Python.

## Upstream Sources

If this skill's content is outdated, check the canonical sources:

- **Source code**: https://github.com/opper-ai/opper-python
- **Documentation**: https://docs.opper.ai
