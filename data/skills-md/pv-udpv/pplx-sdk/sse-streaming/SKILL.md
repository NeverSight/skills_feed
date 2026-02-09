---
name: sse-streaming
description: Implement and debug SSE (Server-Sent Events) streaming for the Perplexity AI API, including parsing, reconnection, and retry logic.
context: fork
agent: sse-expert
---

# sse-streaming

Handle SSE streaming implementation, debugging, and reconnection for pplx-sdk.

## When to use

Use this skill when implementing, debugging, or extending SSE streaming functionality for the Perplexity API.

## Instructions

### SSE Protocol Format

The Perplexity API uses standard SSE format:

```
event: query_progress
data: {"status": "searching", "progress": 0.5}

event: answer_chunk
data: {"text": "partial token", "backend_uuid": "uuid-here"}

event: final_response
data: {"text": "complete answer", "cursor": "cursor-value", "backend_uuid": "uuid-here"}

: [end]
```

### Parsing Rules

1. Read line-by-line from streaming response
2. Skip lines starting with `:` (comments) — except check for `[end]` marker
3. Parse `event: <type>` lines → set current event type
4. Parse `data: <json>` lines → `json.loads()` into payload
5. Empty line → emit event (type + accumulated data), reset buffers
6. Stop on `[end]` marker

### Event Types

| Event | Purpose | Key Fields |
|-------|---------|-----------|
| `query_progress` | Search progress | `status`, `progress` |
| `search_results` | Source citations | `sources[]` |
| `answer_chunk` | Partial token | `text` |
| `final_response` | Complete answer | `text`, `cursor`, `backend_uuid` |
| `related_questions` | Follow-up suggestions | `questions[]` |
| `error` | Server error | `message`, `code` |

### Stream Lifecycle

```python
for chunk in transport.stream(query="...", context_uuid="..."):
    if chunk.type == "answer_chunk":
        print(chunk.text, end="", flush=True)  # Incremental display
    elif chunk.type == "final_response":
        entry = Entry(...)  # Build complete entry
        break
```

### Reconnection with Cursor

When a stream disconnects, resume using the cursor from the last `final_response`:

```python
cursor = last_chunk.data.get("cursor")
backend_uuid = last_chunk.backend_uuid

payload["cursor"] = cursor
payload["resume_entry_uuids"] = [backend_uuid]
```

### Retry with Exponential Backoff

```python
from pplx_sdk.shared.retry import RetryConfig

config = RetryConfig(
    max_retries=3,
    initial_backoff_ms=1000,   # 1s, 2s, 4s
    max_backoff_ms=30000,
    backoff_multiplier=2.0,
    jitter=True,               # ±25% randomization
)
```

### Common Pitfalls

- **Don't parse non-JSON data lines**: Wrap `json.loads()` in try/except
- **Handle empty streams**: Raise `StreamingError` if no events received
- **Buffer multi-line data**: Some `data:` fields span multiple lines; accumulate until empty line
- **Respect `[end]` marker**: Always check for `[end]` in comment lines to stop iteration
