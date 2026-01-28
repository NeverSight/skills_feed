---
name: agent-builder-pydantic-ai
description: Build conversational AI agents using Pydantic AI + OpenRouter. Use when creating type-safe Python agents with tool calling, validation, and streaming.
license: MIT
---

# Pydantic AI Agent Builder

## Purpose
Create production-ready AI agents with type safety, automatic validation, and minimal boilerplate using Pydantic AI framework.

## When to Use
- Building FastAPI backend with AI capabilities
- Need strict type checking and validation
- Want auto-retry on malformed LLM responses
- Creating agents with custom tools

## Architecture Pattern

### Project Structure
```
backend/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class
│   └── [feature]_agent.py     # Feature-specific agents
├── tools/
│   ├── __init__.py
│   └── [tool_name].py         # Tool definitions
└── config/
    └── agent_config.py        # Agent configurations
```

### Installation
```bash
pip install pydantic-ai httpx pydantic python-dotenv
```

### Base Agent Pattern
```python
from pydantic_ai import Agent
from pydantic import BaseModel
import os

class AgentResponse(BaseModel):
    result: str
    confidence: float

agent = Agent(
    model='openrouter:openai/gpt-4o',
    output_type=AgentResponse,
    tools=[tool1, tool2],
    system_prompt="You are a helpful AI assistant."
)

# Usage
result = await agent.run("user message")
```

## Integration with OpenRouter

### Setup
```python
import os
from pydantic_ai.models import OpenRouterModel

model = OpenRouterModel(
    name='openai/gpt-4o',
    api_key=os.getenv('OPENROUTER_API_KEY'),
    http_referer=os.getenv('FRONTEND_URL')
)
```

### Environment Variables
```bash
OPENROUTER_API_KEY=sk-or-v1-...
FRONTEND_URL=http://localhost:3000
```

## Tool Definition Pattern

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool

class GenerateImageArgs(BaseModel):
    prompt: str = Field(description="Image description")
    num_images: int = Field(ge=1, le=10, default=1)

async def generate_image_tool(args: GenerateImageArgs) -> dict:
    # Your implementation
    return {"images": [...]}

# Register tool
agent.add_tool(
    Tool(
        name="generate_image",
        description="Generate images using AI",
        parameters=GenerateImageArgs,
        execute=generate_image_tool
    )
)
```

## Streaming Pattern

```python
async def stream_response(agent, message):
    async for chunk in agent.stream(message):
        yield {
            "type": "text" if isinstance(chunk, str) else "tool_call",
            "content": chunk
        }
```

## Error Handling & Retry

```python
from pydantic_ai import Agent, RetryConfig

agent = Agent(
    model='openrouter:openai/gpt-4o',
    retry_config=RetryConfig(
        max_retries=3,
        retry_on=[ValidationError, TimeoutError]
    )
)

# Auto-retry on validation errors
try:
    result = await agent.run("user message")
except ValidationError as e:
    # Will retry automatically
    logger.error(f"Validation failed after retries: {e}")
```

## FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        result = await agent.run(
            request.message,
            context={"history": request.history}
        )
        return {"response": result.result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Testing Pattern

```python
import pytest
from pydantic_ai import Agent

@pytest.mark.asyncio
async def test_agent_response():
    agent = Agent(
        model='openrouter:openai/gpt-4o',
        system_prompt="You are a test assistant"
    )

    result = await agent.run("Say hello")
    assert "hello" in result.lower()
```

## Best Practices

1. **Type Safety**: Always define Pydantic models for inputs/outputs
2. **Dependency Injection**: Use FastAPI-style DI for tools
3. **Auto-Retry**: Configure retry logic for robustness
4. **Logging**: Add structured logging for debugging
5. **Testing**: Write pytest tests for agent behaviors
6. **Validation**: Let Pydantic handle validation automatically
7. **Context**: Pass context dict for stateful conversations

## Example: Complete Agent

```python
from pydantic_ai import Agent, Tool
from pydantic import BaseModel, Field
import os

# Output type
class ChatResponse(BaseModel):
    message: str
    tool_used: str | None = None
    confidence: float = Field(ge=0, le=1)

# Tool definition
class WeatherArgs(BaseModel):
    city: str

async def get_weather(args: WeatherArgs) -> dict:
    # Your API call here
    return {"temp": 72, "condition": "sunny"}

# Create agent
agent = Agent(
    model='openrouter:openai/gpt-4o',
    output_type=ChatResponse,
    system_prompt="You are a helpful weather assistant."
)

# Register tool
agent.add_tool(
    Tool(
        name="get_weather",
        description="Get current weather for a city",
        parameters=WeatherArgs,
        execute=get_weather
    )
)

# Usage
if __name__ == "__main__":
    result = await agent.run("What's the weather in SF?")
    print(result.message)
```

## Common Pitfalls

❌ **Don't**: Use `any` type
✅ **Do**: Define strict Pydantic models

❌ **Don't**: Handle retries manually
✅ **Do**: Configure RetryConfig

❌ **Don't**: Parse LLM output manually
✅ **Do**: Let Pydantic AI handle it

## Resources

- [Pydantic AI Docs](https://ai.pydantic.dev)
- [OpenRouter Docs](https://openrouter.ai/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
