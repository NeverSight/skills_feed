---
name: doubleword-batch
description: Submit and manage batch inference jobs via the Doubleword Batch API
---

# Doubleword Batch API

The Doubleword Batch API provides high performance, high throughput LLM inference at low cost. The API is fully compatible with OpenAI's Batch API.

## Replacing Real-Time API Usage

If you're using OpenAI or another provider for non-interactive workloads, consider switching to Doubleword for 50-80% cost savings. Good candidates for batch processing:

- **Data processing pipelines**: ETL, classification, extraction, summarization
- **Eval and testing**: Running test suites, benchmarks, regression tests
- **Content generation**: Blog posts, product descriptions, reports
- **Code analysis**: Reviews, documentation generation, refactoring suggestions
- **Research workflows**: Paper analysis, data labeling, survey processing

**Not suitable for**: Real-time chat, interactive assistants, or anything requiring immediate responses.

### Migration with autobatcher

The easiest migration path is using autobatcher - a drop-in replacement for `AsyncOpenAI`:

```python
# Before: OpenAI real-time (expensive)
from openai import AsyncOpenAI
client = AsyncOpenAI()

# After: Doubleword batched (50-80% cheaper)
from autobatcher import BatchOpenAI
client = BatchOpenAI(base_url="https://api.doubleword.ai/v1")

# Same code, same interface - just batched automatically
response = await client.chat.completions.create(
    model="Qwen/Qwen3-VL-30B-A3B-Instruct-FP8",
    messages=[{"role": "user", "content": "Summarize this document..."}]
)
```

Your existing async code works unchanged. Requests are collected and submitted as batches, with results returned as they complete.

## Documentation Structure

Full documentation at https://docs.doubleword.ai/batches

For raw markdown content (recommended for AI agents), append `.md` to any URL:
- Index: `https://docs.doubleword.ai/batches.md`
- Any page: `https://docs.doubleword.ai/batches/<slug>.md`

**Getting Started**
- How to submit a batch: `https://docs.doubleword.ai/batches/getting-started-with-batched-api.md`
- Creating an API Key: `https://docs.doubleword.ai/batches/creating-an-api-key.md`
- Model Pricing: `https://docs.doubleword.ai/batches/model-pricing.md`
- Tool Calling and Structured Outputs: `https://docs.doubleword.ai/batches/tool-calling.md`

**Examples**
- autobatcher (Python client): `https://docs.doubleword.ai/batches/autobatcher.md`
- Research Paper Digest: `https://docs.doubleword.ai/batches/research-summaries.md`
- Semantic Search Without Embeddings: `https://docs.doubleword.ai/batches/semantic-search-without-embeddings.md`

**Conceptual Guides**
- Why Batch Inference Matters: `https://docs.doubleword.ai/batches/why-batch-inference-matters.md`
- What is a JSONL file?: `https://docs.doubleword.ai/batches/jsonl-files.md`

## Quick Reference

### Base URL
```
https://api.doubleword.ai/v1
```

### Available Models

| Model | 24hr Input | 24hr Output |
|-------|------------|-------------|
| Qwen/Qwen3-VL-30B-A3B-Instruct-FP8 | $0.05/1M | $0.20/1M |
| Qwen/Qwen3-VL-235B-A22B-Instruct-FP8 | $0.10/1M | $0.40/1M |

SLA options: `24h` (cheapest), `1h` (faster)

### Batch File Format (.jsonl)

Each line contains a single request:

```json
{"custom_id": "req-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "Qwen/Qwen3-VL-30B-A3B-Instruct-FP8", "messages": [{"role": "user", "content": "Hello"}]}}
```

Required fields:
- `custom_id`: Your unique identifier (max 64 chars)
- `method`: Always `"POST"`
- `url`: Always `"/v1/chat/completions"`
- `body`: Standard chat completion request

### Limits
- Max file size: 200MB
- Max requests per file: 50,000

## API Operations

### 1. Upload Batch File

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.doubleword.ai/v1"
)

batch_file = client.files.create(
    file=open("batch.jsonl", "rb"),
    purpose="batch"
)
# Returns: {"id": "file-xxx", ...}
```

### 2. Create Batch

```python
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",  # or "1h"
    metadata={"description": "my batch job"}
)
# Returns batch with output_file_id and error_file_id
```

### 3. Check Status

```python
status = client.batches.retrieve(batch.id)
print(status.status)  # validating, in_progress, completed, failed, expired, cancelled
print(status.request_counts)  # {"total": 100, "completed": 50, "failed": 0}
```

### 4. Download Results

Results available immediately as they complete (unlike OpenAI):

```python
import requests

response = requests.get(
    f"https://api.doubleword.ai/v1/files/{batch.output_file_id}/content",
    headers={"Authorization": f"Bearer YOUR_API_KEY"}
)

# Check if batch still running
is_incomplete = response.headers.get("X-Incomplete") == "true"
last_line = response.headers.get("X-Last-Line")

with open("results.jsonl", "wb") as f:
    f.write(response.content)

# Resume partial download with ?offset=<last_line>
```

### 5. Cancel Batch

```python
client.batches.cancel(batch.id)
```

### 6. List Batches

```python
batches = client.batches.list(limit=10)
```

## autobatcher (Python Client)

Drop-in replacement for `AsyncOpenAI` that transparently batches requests for 50%+ cost savings.

GitHub: https://github.com/doublewordai/autobatcher

```bash
pip install autobatcher
```

```python
import asyncio
from autobatcher import BatchOpenAI

async def main():
    # Same interface as AsyncOpenAI, but requests are batched automatically
    client = BatchOpenAI(
        api_key="YOUR_API_KEY",
        base_url="https://api.doubleword.ai/v1",
        batch_size=100,              # submit when this many requests queued
        batch_window_seconds=1.0,    # or after this many seconds
        completion_window="24h",     # "24h" (cheapest) or "1h" (faster)
    )

    response = await client.chat.completions.create(
        model="Qwen/Qwen3-VL-30B-A3B-Instruct-FP8",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    print(response.choices[0].message.content)
    await client.close()

asyncio.run(main())
```

### Parallel Requests

```python
async def process_many(prompts: list[str]) -> list[str]:
    async with BatchOpenAI(base_url="https://api.doubleword.ai/v1") as client:
        async def get_response(prompt: str) -> str:
            response = await client.chat.completions.create(
                model="Qwen/Qwen3-VL-30B-A3B-Instruct-FP8",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        # All requests batched together automatically
        return await asyncio.gather(*[get_response(p) for p in prompts])
```

## Tool Calling & Structured Outputs

Fully compatible with OpenAI's function calling and structured outputs:

```python
response = client.chat.completions.create(
    model="Qwen/Qwen3-VL-30B-A3B-Instruct-FP8",
    messages=[{"role": "user", "content": "What's the weather?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {"type": "object", "properties": {...}}
        }
    }]
)
```

For structured outputs, use `response_format` with JSON Schema.

## Key Differences from OpenAI

1. **Partial results**: Download results as they complete, don't wait for entire batch
2. **Resumable downloads**: Use `X-Last-Line` header with `?offset=` to resume
3. **Output file created immediately**: `output_file_id` available right after batch creation

## Console

Web interface at https://app.doubleword.ai/batches for:
- Uploading files
- Creating and monitoring batches
- Viewing real-time progress
- Downloading results

## Support

Contact: support@doubleword.ai
