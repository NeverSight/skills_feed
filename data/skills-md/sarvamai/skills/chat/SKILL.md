---
name: chat
description: Generate chat completions using Sarvam AI's Sarvam-M model. Use when the user needs AI chat, text generation, question answering, or reasoning in Indian languages. Sarvam-M is a 24B parameter model with hybrid thinking, superior Indic language understanding, and OpenAI-compatible API. Free to use.
license: Apache-2.0
metadata:
  author: sarvam-ai
  version: "1.0"
  model: sarvam-m
---

# Chat with Sarvam-M

Sarvam-M is Sarvam AI's flagship language model optimized for Indian languages with hybrid thinking capabilities for complex reasoning.

## Key Features

- **24B parameters** optimized for Indic languages
- **Hybrid thinking mode** for complex reasoning
- **Free to use** (no cost)
- **OpenAI-compatible API**
- **Multilingual** chat in English + 10 Indian languages

## Installation

```bash
pip install sarvamai
# or
pip install openai  # OpenAI-compatible
```

## Quick Start

### Sarvam SDK

```python
from sarvamai import SarvamAI

client = SarvamAI()

response = client.chat.completions.create(
    model="sarvam-m",
    messages=[
    {
        "role": "user",
        "content": "भारत की राजधानी क्या है?"
    }
]
)

print(response.choices[
    0
].message.content)
```

### OpenAI-Compatible

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ[
    "SARVAM_API_KEY"
],
    base_url="https://api.sarvam.ai/v1"
)

response = client.chat.completions.create(
    model="sarvam-m",
    messages=[
    {
        "role": "user",
        "content": "What is the capital of India?"
    }
]
)

print(response.choices[
    0
].message.content)
```

## Hybrid Thinking Mode

Enable step-by-step reasoning for complex problems:

```python
response = client.chat.completions.create(
    model="sarvam-m",
    messages=[
    {
        "role": "user",
        "content": "Solve: If a train travels 120km in 2 hours, what is its average speed?"
    }
],
    thinking=True  # Enable reasoning
)

# Access thinking process
print("Thinking:", response.choices[
    0
].message.thinking)
print("Answer:", response.choices[
    0
].message.content)
```

## System Prompts

Guide the model's behavior:

```python
response = client.chat.completions.create(
    model="sarvam-m",
    messages=[
    {
        "role": "system",
        "content": "You are a helpful Hindi tutor. Always respond in Hindi with English transliteration in parentheses."
    },
    {
        "role": "user",
        "content": "How do I say 'Good morning'?"
    }
]
)
```

## Multi-turn Conversations

Maintain context across turns:

```python
messages = [
    {
        "role": "system",
        "content": "You are a knowledgeable assistant."
    },
    {
        "role": "user",
        "content": "Tell me about the Taj Mahal"
    },
    {
        "role": "assistant",
        "content": "The Taj Mahal is a white marble mausoleum..."
    },
    {
        "role": "user",
        "content": "Who built it and when?"
    }
]

response = client.chat.completions.create(
    model="sarvam-m",
    messages=messages
)
```

## Streaming

Stream responses token by token:

```python
stream = client.chat.completions.create(
    model="sarvam-m",
    messages=[
    {
        "role": "user",
        "content": "Write a short poem about India"
    }
],
    stream=True
)

for chunk in stream:
    if chunk.choices[
    0
].delta.content:
        print(chunk.choices[
    0
].delta.content, end="", flush=True)
```

## Temperature Control

Control randomness:

```python
# Creative (higher temperature)
response = client.chat.completions.create(
    model="sarvam-m",
    messages=[
    {
        "role": "user",
        "content": "Write a creative story"
    }
],
    temperature=0.9
)

# Factual (lower temperature)
response = client.chat.completions.create(
    model="sarvam-m",
    messages=[
    {
        "role": "user",
        "content": "What is 2+2?"
    }
],
    temperature=0.1
)
```

## JavaScript

```javascript
import { SarvamAI
} from "sarvamai";

const client = new SarvamAI();

const response = await client.chat.completions.create({
  model: "sarvam-m",
  messages: [
        { role: "user", content: "भारत की राजधानी क्या है?"
        }
    ]
});

console.log(response.choices[
    0
].message.content);
```

### OpenAI SDK

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.SARVAM_API_KEY,
  baseURL: "https://api.sarvam.ai/v1"
});

const response = await client.chat.completions.create({
  model: "sarvam-m",
  messages: [
        { role: "user", content: "Hello!"
        }
    ]
});
```

## cURL

```bash
curl -X POST "https://api.sarvam.ai/v1/chat/completions" \
  -H "api-subscription-key: $SARVAM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sarvam-m",
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of India?"
        }
    ]
}'
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | `sarvam-m` |
| `messages` | array | Yes | Conversation history |
| `temperature` | float | No | 0.0-2.0 (default: 1.0) |
| `max_tokens` | int | No | Max response length |
| `stream` | bool | No | Enable streaming |
| `thinking` | bool | No | Enable hybrid thinking |
| `top_p` | float | No | Nucleus sampling (0.0-1.0) |

## Response

```json
{
    "id": "chatcmpl-abc123",
    "object": "chat.completion",
    "model": "sarvam-m",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "भारत की राजधानी नई दिल्ली है।"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 12,
        "total_tokens": 27
    }
}
```

See [references/prompting.md
](references/prompting.md) for advanced prompting techniques.

