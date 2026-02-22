---
name: portkey-python-sdk
description: Complete reference for the Portkey AI Gateway Python SDK with unified API access to 200+ LLMs, automatic fallbacks, caching, and full observability. Use when building Python applications that need LLM integration with production-grade reliability.
license: Apache-2.0
compatibility: Requires Python 3.8+. Works with pip, poetry, or uv.
metadata:
  author: portkey-ai
  version: "1.0.0"
  sdk-version: "2.1.0"
  sdk-repo: https://github.com/portkey-ai/portkey-python-sdk
  docs: https://docs.portkey.ai
---

# Portkey Python SDK

The Portkey Python SDK provides a unified interface to 200+ LLMs through the Portkey AI Gateway. Built on top of the OpenAI SDK for seamless compatibility, it adds production-grade features: automatic fallbacks, retries, load balancing, semantic caching, guardrails, and comprehensive observability.

**Additional References:**
- [API Reference](references/API_REFERENCE.md) - Response structures, error handling
- [Advanced Features](references/ADVANCED_FEATURES.md) - Tool calling, embeddings, audio, images
- [Framework Integrations](references/INTEGRATIONS.md) - LangChain, LlamaIndex, Strands, Google ADK
- [Provider Configuration](references/PROVIDERS.md) - Azure, AWS Bedrock, Vertex AI setup

---

## Installation

```bash
pip install portkey-ai

# Or with poetry/uv
poetry add portkey-ai
uv add portkey-ai
```

---

## Quick Start

```python
import os
from portkey_ai import Portkey

client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    virtual_key="your-openai-virtual-key"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

---

## Authentication

### API Key + Virtual Key (Recommended)

Virtual keys securely store provider API keys in Portkey's vault:

```python
import os
from portkey_ai import Portkey

client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],  # From app.portkey.ai
    virtual_key="openai-virtual-key-xxx"     # From app.portkey.ai/virtual-keys
)
```

### Using Config IDs

Pre-configure routing, fallbacks, and caching in the dashboard:

```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    config="pc-config-xxx"  # Config ID from dashboard
)
```

---

## Chat Completions

### Basic Request

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing briefly."}
    ]
)

print(response.choices[0].message.content)
print(f"Tokens used: {response.usage.total_tokens}")
```

### Streaming

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a short story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Async Support

```python
import asyncio
from portkey_ai import AsyncPortkey

async def main():
    client = AsyncPortkey(
        api_key=os.environ["PORTKEY_API_KEY"],
        virtual_key="openai-key"
    )
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

### Async Streaming

```python
async def stream_response():
    client = AsyncPortkey(
        api_key=os.environ["PORTKEY_API_KEY"],
        virtual_key="openai-key"
    )
    
    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Write a poem"}],
        stream=True
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## Gateway Features

### Fallbacks

Automatic failover when a provider fails:

```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    config={
        "strategy": {"mode": "fallback"},
        "targets": [
            {
                "virtual_key": "openai-key",
                "override_params": {"model": "gpt-4o"}
            },
            {
                "virtual_key": "anthropic-key",
                "override_params": {"model": "claude-3-5-sonnet-20241022"}
            }
        ]
    }
)

# If OpenAI fails, automatically tries Anthropic
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Load Balancing

Distribute traffic across providers:

```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    config={
        "strategy": {"mode": "loadbalance"},
        "targets": [
            {"virtual_key": "openai-key-1", "weight": 0.7},
            {"virtual_key": "openai-key-2", "weight": 0.3}
        ]
    }
)
```

### Automatic Retries

```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    config={
        "retry": {
            "attempts": 3,
            "on_status_codes": [429, 500, 502, 503, 504]
        },
        "virtual_key": "openai-key"
    }
)
```

### Semantic Caching

Reduce costs and latency with intelligent caching:

```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    config={
        "cache": {
            "mode": "semantic",  # or "simple" for exact match
            "max_age": 3600      # TTL in seconds
        },
        "virtual_key": "openai-key"
    }
)

# Similar queries return cached responses
response1 = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the capital of France?"}]
)

response2 = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me France's capital"}]
)  # Returns cached response
```

### Request Timeout

```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    virtual_key="openai-key",
    request_timeout=30  # 30 seconds
)
```

---

## Observability

### Trace IDs

Link related requests for debugging:

```python
import uuid

client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    virtual_key="openai-key",
    trace_id=str(uuid.uuid4())
)
```

### Custom Metadata

Add searchable metadata to requests:

```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    virtual_key="openai-key",
    metadata={
        "user_id": "user-123",
        "session_id": "session-456",
        "environment": "production"
    }
)
```

### Per-Request Options

```python
response = client.with_options(
    trace_id="unique-trace-id",
    metadata={"request_type": "summarization"}
).chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Summarize this..."}]
)
```

---

## Common Patterns

### Multi-turn Conversation

```python
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a high-level programming language..."},
    {"role": "user", "content": "Show me a hello world example."}
]

response = client.chat.completions.create(model="gpt-4o", messages=messages)
```

### JSON Output

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Extract as JSON with name and age fields."},
        {"role": "user", "content": "John is 30 years old."}
    ],
    response_format={"type": "json_object"}
)
# Returns: {"name": "John", "age": 30}
```

### Production Setup with Fallbacks + Caching

```python
def create_production_client():
    return Portkey(
        api_key=os.environ["PORTKEY_API_KEY"],
        config={
            "strategy": {"mode": "fallback"},
            "targets": [
                {
                    "virtual_key": os.environ["OPENAI_VIRTUAL_KEY"],
                    "override_params": {"model": "gpt-4o"},
                    "retry": {"attempts": 2, "on_status_codes": [429, 500]}
                },
                {
                    "virtual_key": os.environ["ANTHROPIC_VIRTUAL_KEY"],
                    "override_params": {"model": "claude-3-5-sonnet-20241022"}
                }
            ],
            "cache": {"mode": "semantic", "max_age": 3600}
        },
        trace_id="production-session",
        metadata={"environment": "production"}
    )
```

---

## Best Practices

1. **Use environment variables** - Never hardcode API keys
2. **Implement fallbacks** - Always have backup providers for production
3. **Use streaming** - Better UX for long responses
4. **Add tracing** - Enable observability with trace IDs and metadata
5. **Enable caching** - Reduce costs with semantic caching
6. **Handle errors** - Implement retry logic with exponential backoff

---

## Resources

- **Dashboard**: [app.portkey.ai](https://app.portkey.ai)
- **Documentation**: [docs.portkey.ai](https://docs.portkey.ai)
- **GitHub**: [github.com/portkey-ai/portkey-python-sdk](https://github.com/portkey-ai/portkey-python-sdk)
- **Discord**: [portkey.ai/discord](https://portkey.ai/discord)
