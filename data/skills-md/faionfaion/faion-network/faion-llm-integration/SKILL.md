---
name: faion-llm-integration
description: "LLM APIs: OpenAI, Claude, Gemini, local LLMs, prompt engineering, function calling."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# LLM Integration Skill

**Communication: User's language. Code: English.**

## Purpose

Handles direct integration with LLM APIs. Covers OpenAI, Claude, Gemini, local models, prompt engineering, and output structuring.

## Scope

| Area | Coverage |
|------|----------|
| **LLM APIs** | OpenAI (GPT-4o, o1), Claude (Opus 4.5, Sonnet 4), Gemini (Pro, Flash) |
| **Prompt Engineering** | Few-shot, CoT, chain-of-thought techniques |
| **Structured Output** | JSON mode, function calling, tool use |
| **Guardrails** | Content safety, validation, error handling |
| **Local LLMs** | Ollama integration, privacy-focused deployments |

## Quick Start

| Task | Files |
|------|-------|
| OpenAI integration | openai-api-integration.md → openai-chat-completions.md |
| Claude integration | claude-api-basics.md → claude-messages-api.md |
| Gemini integration | gemini-basics.md → gemini-multimodal.md |
| Local LLM | local-llm-ollama.md |
| Prompts | prompt-basics.md → prompt-techniques.md |
| Function calling | function-calling-patterns.md + tool-use-basics.md |

## Methodologies (26)

**OpenAI (5):**
- openai-api-integration: API setup, authentication, models
- openai-chat-completions: Chat API, streaming, parameters
- openai-function-calling: Tool definitions, execution
- openai-embeddings: Text embeddings (moved to rag-engineer)
- openai-assistants: Assistant API, threads, tools

**Claude (6):**
- claude-api-basics: Anthropic API setup
- claude-messages-api: Messages API, streaming
- claude-tool-use: Tool definitions, structured output
- claude-advanced-features: Extended thinking, prompt caching
- claude-best-practices: Safety, context management
- claude-api-integration: SDK integration patterns

**Gemini (4):**
- gemini-basics: Google AI setup, models
- gemini-multimodal: Vision, audio, video inputs
- gemini-function-calling: Function declarations
- gemini-api-integration: SDK patterns

**Prompt Engineering (6):**
- prompt-basics: Structure, few-shot, roles
- prompt-techniques: Advanced patterns, templates
- cot-basics: Chain-of-thought fundamentals
- cot-techniques: Zero-shot CoT, reasoning chains
- structured-output-basics: JSON mode, schemas
- structured-output-patterns: Advanced structuring

**Safety & Tools (4):**
- guardrails-basics: Content safety, PII detection
- guardrails-implementation: Implementation patterns
- function-calling-patterns: Tool design, error handling
- tool-use-basics: Tool fundamentals

**Local (1):**
- local-llm-ollama: Ollama setup, model management

## Code Examples

### OpenAI Chat Completion

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing"}
    ]
)
print(response.choices[0].message.content)
```

### Claude Messages

```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain RAG systems"}]
)
print(message.content[0].text)
```

### Function Calling

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in SF?"}],
    tools=tools
)
```

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-rag-engineer | Uses embeddings APIs |
| faion-ai-agents | Uses tool calling |
| faion-ml-ops | Uses for evaluation |

---

*LLM Integration v1.0 | 26 methodologies*
