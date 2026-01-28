---
name: streaming
description: Server-Sent Events (SSE) streaming for Claude API with support for text, tool use, and extended thinking. Activate for real-time responses, stream handling, and progressive output.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
triggers:
  - streaming
  - stream
  - sse
  - server-sent events
  - real-time
  - progressive
  - delta
  - event
dependencies:
  - llm-integration
related-skills:
  - tool-use
  - extended-thinking
---

# Streaming Skill

Implement real-time streaming responses from Claude API using Server-Sent Events (SSE).

## When to Use This Skill

- Real-time user interfaces
- Long-running generations
- Progressive output display
- Tool use with streaming
- Extended thinking visualization

## SSE Event Flow

```
message_start
    → content_block_start
        → content_block_delta (repeated)
    → content_block_stop
    → (more blocks...)
→ message_delta
→ message_stop
```

## Core Implementation

### Basic Text Streaming (Python)

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short story."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Event-Based Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="")
            elif event.delta.type == "input_json_delta":
                # Tool input (accumulate, don't parse yet!)
                tool_input_buffer += event.delta.partial_json
        elif event.type == "content_block_stop":
            # Now safe to parse tool input
            if tool_input_buffer:
                tool_input = json.loads(tool_input_buffer)
```

### TypeScript Streaming

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const stream = client.messages.stream({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{ role: 'user', content: 'Write a story.' }]
});

for await (const event of stream) {
    if (event.type === 'content_block_delta' &&
        event.delta.type === 'text_delta') {
        process.stdout.write(event.delta.text);
    }
}

const finalMessage = await stream.finalMessage();
```

## Event Types Reference

| Event | When | Data |
|-------|------|------|
| `message_start` | Beginning | Message metadata |
| `content_block_start` | Block begins | Block type, index |
| `content_block_delta` | Content chunk | Delta content |
| `content_block_stop` | Block ends | - |
| `message_delta` | Message update | Stop reason, usage |
| `message_stop` | Complete | - |

## Delta Types

| Delta Type | Content | When |
|-----------|---------|------|
| `text_delta` | `.text` | Text content |
| `input_json_delta` | `.partial_json` | Tool input |
| `thinking_delta` | `.thinking` | Extended thinking |
| `signature_delta` | `.signature` | Thinking signature |

## Tool Use Streaming

### Critical Rule: Never Parse JSON Mid-Stream!

```python
# WRONG - Will fail on partial JSON!
for event in stream:
    if event.delta.type == "input_json_delta":
        tool_input = json.loads(event.delta.partial_json)  # FAILS!

# CORRECT - Accumulate then parse
tool_json_buffer = ""
for event in stream:
    if event.delta.type == "input_json_delta":
        tool_json_buffer += event.delta.partial_json
    elif event.type == "content_block_stop":
        if tool_json_buffer:
            tool_input = json.loads(tool_json_buffer)  # Safe now!
            tool_json_buffer = ""
```

### Complete Tool Streaming Pattern

```python
def stream_with_tools(client, messages, tools):
    current_block = None
    tool_input_buffer = ""

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=messages,
        tools=tools
    ) as stream:
        for event in stream:
            if event.type == "content_block_start":
                current_block = event.content_block
                tool_input_buffer = ""

            elif event.type == "content_block_delta":
                if event.delta.type == "text_delta":
                    yield {"type": "text", "content": event.delta.text}
                elif event.delta.type == "input_json_delta":
                    tool_input_buffer += event.delta.partial_json

            elif event.type == "content_block_stop":
                if current_block.type == "tool_use":
                    yield {
                        "type": "tool_call",
                        "id": current_block.id,
                        "name": current_block.name,
                        "input": json.loads(tool_input_buffer)
                    }
```

## Extended Thinking Streaming

```python
thinking_content = ""
signature = ""

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "Solve this complex problem..."}]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                thinking_content += event.delta.thinking
                # Optionally display thinking in UI
            elif event.delta.type == "signature_delta":
                signature = event.delta.signature
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="")
```

## Error Handling

### Retriable Errors

```python
import time

RETRIABLE_ERRORS = [529, 429, 500, 502, 503]

def stream_with_retry(client, **kwargs):
    max_retries = 3
    base_delay = 1

    for attempt in range(max_retries):
        try:
            with client.messages.stream(**kwargs) as stream:
                for event in stream:
                    yield event
            return
        except anthropic.APIStatusError as e:
            if e.status_code in RETRIABLE_ERRORS and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
            else:
                raise
```

### Silent Overloaded Errors

```python
# CRITICAL: Check for error events even at HTTP 200!
for event in stream:
    if event.type == "error":
        if event.error.type == "overloaded_error":
            # Retry with backoff
            pass
```

## Connection Management

### Keep-Alive Configuration

```python
import httpx

# Proper timeout configuration
http_client = httpx.Client(
    timeout=httpx.Timeout(
        connect=10.0,    # Connection timeout
        read=120.0,      # Read timeout (long for streaming!)
        write=30.0,      # Write timeout
        pool=30.0        # Pool timeout
    )
)

client = anthropic.Anthropic(http_client=http_client)
```

### Connection Pooling

```python
http_client = httpx.Client(
    limits=httpx.Limits(
        max_keepalive_connections=20,
        max_connections=100,
        keepalive_expiry=30.0
    )
)
```

## Best Practices

### DO:
- Set read timeout >= 60 seconds
- Accumulate tool JSON, parse after block_stop
- Handle error events even at HTTP 200
- Use exponential backoff for retries

### DON'T:
- Parse partial JSON during streaming
- Use short timeouts
- Ignore overloaded_error events
- Leave connections idle >5 minutes

## UI Integration Pattern

```python
async def stream_to_ui(websocket, prompt):
    """Stream Claude response to WebSocket client"""
    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for text in stream.text_stream:
            await websocket.send_json({
                "type": "chunk",
                "content": text
            })

        await websocket.send_json({
            "type": "complete",
            "usage": stream.get_final_message().usage
        })
```

## See Also

- [[llm-integration]] - API basics
- [[tool-use]] - Tool calling
- [[extended-thinking]] - Deep reasoning
