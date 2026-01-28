---
name: pydantic-ai-agent
description: Build production-grade Pydantic AI agents with layered architecture. Use when creating AI agents with tool systems, dependency injection, streaming responses, multi-provider support, or conversation state management. Includes scaffolding scripts for rapid project setup and comprehensive architectural patterns for FastAPI web services and CLI applications.
---

# Pydantic AI Agent Builder

Build production-grade AI agents using Pydantic AI with a layered architectural pattern.

## When to Use This Skill

Use this skill when building:
- AI agents with tool/function calling capabilities
- Conversational agents with state management
- Streaming chat applications (SSE, real-time responses)
- Multi-provider LLM applications (OpenAI, Anthropic, Google, Ollama)
- FastAPI web services with AI agents
- CLI applications with AI agents
- Agents requiring dependency injection for tools

## Quick Start

### 1. Scaffold a New Project

```bash
python scripts/scaffold_agent.py my_agent
cd my_agent
pip install -r requirements.txt
```

**Options**:
- `--minimal` - Core files only
- `--web` - Include FastAPI example
- `--cli` - Include CLI example

### 2. Configure Provider

```bash
# .env file
LLM_PROVIDER=anthropic
LLM_MODEL_NAME=claude-3-5-sonnet-20241022
LLM_API_KEY=sk-ant-...
```

### 3. Run Examples

```bash
# CLI
python example_cli.py

# Web service
python example_fastapi.py
# Visit http://localhost:8000/docs
```

## Architecture Overview

This pattern uses a layered architecture:

```
Router/CLI → Service → AgentFactory → Agent
                ↓           ↓
            Tools ← ToolRegistry
                ↓
            StateStore
```

**Key Components**:
- **AgentFactory** - Creates configured agents (Factory pattern)
- **AgentService** - Orchestrates agent lifecycle
- **ToolRegistry** - Centralized tool registration
- **ToolCollection** - Dependency injection for tools
- **AgentState** - Conversation history management
- **StateStore** - State persistence
- **ModelProvider** - Multi-provider abstraction

## Core Patterns

### 1. Agent Factory Pattern

Create agents with different configurations:

```python
from agent_factory import agent_factory, AgentType

# Use default configuration
agent = agent_factory.create_agent(
    agent_type=AgentType.GENERAL,
    model=model,
    tools=tools,
    state=state
)

# Register custom configuration
agent_factory.register_config(AgentConfig(
    agent_type=AgentType.SPECIALIZED,
    system_prompt="You are a specialized assistant...",
    tool_names=["tool1", "tool2"],  # Filter tools
    model_settings={"temperature": 0.0}
))
```

### 2. Tool Registration

Register tools with metadata:

```python
from tool_registry import tool_registry, ToolCategory

@tool_registry.register(
    name="search_database",
    category=ToolCategory.DATA,
    description="Search the database for records",
    requires_approval=False,
    tags={"database", "search"}
)
async def search_database(query: str) -> str:
    """Search database with query"""
    return f"Results for: {query}"
```

### 3. Dependency Injection

Tools with service dependencies:

```python
# Define tool with service parameter
@tool_registry.register(...)
async def query_db(db_service: DatabaseService, query: str) -> str:
    """Query database (db_service injected automatically)"""
    return await db_service.execute(query)

# ToolCollection binds the service
@dataclass
class ToolCollection:
    database_service: DatabaseService

    def get_all_tools(self):
        # Automatically binds db_service to tools
        # LLM only sees: query_db(query: str)
        return self._create_bound_tools()
```

**See [references/dependency-injection.md](references/dependency-injection.md) for complete guide**

### 4. Streaming Responses

Stream text with tool call tracking:

```python
async def stream_chat(self, prompt: str) -> AsyncIterable[str]:
    """Stream agent responses"""
    agent = self._create_agent()

    async with agent.run_stream(prompt) as result:
        async for chunk in result.stream_text(delta=True):
            if chunk:
                yield chunk
                await asyncio.sleep(0)  # Force flush
```

**See [references/streaming.md](references/streaming.md) for SSE implementation**

### 5. Multi-Provider Support

Switch between LLM providers:

```python
from model_provider import ModelProvider

# Anthropic
model = ModelProvider.ANTHROPIC.create(
    model_name="claude-3-5-sonnet-20241022",
    api_key="sk-ant-..."
)

# OpenAI
model = ModelProvider.OPENAI.create(
    model_name="gpt-4",
    api_key="sk-..."
)

# Ollama (local)
model = ModelProvider.OLLAMA.create(
    model_name="llama3.2",
    base_url="http://localhost:11434/v1"
)
```

**See [references/providers.md](references/providers.md) for all providers**

## Common Workflows

### Building a Web Service

1. Scaffold project with web example:
```bash
python scripts/scaffold_agent.py my_service --web
```

2. Customize `service.py` with your business logic

3. Add tools in `tools.py`:
```python
@tool_registry.register(...)
async def my_tool(param: str) -> str:
    return f"Processed: {param}"
```

4. Update `example_fastapi.py` with your endpoints

5. Run:
```bash
uvicorn example_fastapi:app --reload
```

### Building a CLI Application

1. Scaffold project with CLI example:
```bash
python scripts/scaffold_agent.py my_cli --cli
```

2. Customize agent configuration in `agent_factory.py`

3. Add tools for your domain

4. Run:
```bash
python example_cli.py
```

### Adding Service Dependencies

1. Define your service:
```python
@dataclass
class MyService:
    config: dict

    async def process(self, data: str) -> str:
        return f"Processed: {data}"
```

2. Add tools using the service:
```python
@tool_registry.register(...)
async def process_data(service: MyService, data: str) -> str:
    return await service.process(data)
```

3. Update `ToolCollection`:
```python
@dataclass
class ToolCollection:
    my_service: MyService

    def get_all_tools(self):
        # Automatically binds my_service
        return self._create_bound_tools()
```

4. Initialize in service layer:
```python
def _create_tools(self):
    my_service = MyService(config={...})
    return ToolCollection(my_service=my_service)
```

### Implementing Streaming with SSE

1. Define SSE message types in `schema.py`:
```python
class SSEChunkMessage(BaseModel):
    type: Literal["chunk"] = "chunk"
    content: str
```

2. Update `service.py` to yield SSE messages:
```python
async def stream_chat(self, prompt: str):
    async with agent.run_stream(prompt) as result:
        async for chunk in result.stream_text(delta=True):
            yield SSEChunkMessage(content=chunk).model_dump_json()
            await asyncio.sleep(0)
```

3. Add SSE wrapper in `utils.py`:
```python
async def wrap_sse_stream(source):
    async for chunk in source:
        yield f"data: {chunk}\n\n"
        await asyncio.sleep(0)
```

4. Use in FastAPI:
```python
@app.post("/chat")
async def chat(prompt: str):
    text_stream = service.stream_chat(prompt)
    sse_stream = wrap_sse_stream(text_stream)
    return StreamingResponse(
        sse_stream,
        media_type="text/event-stream"
    )
```

## Reference Documentation

For detailed implementation guides:

- **[architecture.md](references/architecture.md)** - Complete architectural patterns, component responsibilities, data flow, and extension points
- **[dependency-injection.md](references/dependency-injection.md)** - Deep dive into DI pattern with signature manipulation, multiple services, and testing
- **[streaming.md](references/streaming.md)** - Streaming implementation, SSE formatting, tool call tracking, and client integration
- **[providers.md](references/providers.md)** - Multi-provider support, configuration, model selection, and cost optimization

## Customization Guide

### Adding New Agent Types

1. Define enum value in `agent_factory.py`:
```python
class AgentType(str, Enum):
    GENERAL = "general"
    SPECIALIZED = "specialized"
```

2. Register configuration:
```python
agent_factory.register_config(AgentConfig(
    agent_type=AgentType.SPECIALIZED,
    system_prompt="Custom prompt...",
    tool_names=["specific_tool"],
    model_settings={"temperature": 0.0}
))
```

### Adding New Tool Categories

1. Extend `ToolCategory` in `tool_registry.py`:
```python
class ToolCategory(str, Enum):
    UTILITY = "utility"
    DATA = "data"
    CUSTOM = "custom"  # New category
```

2. Register tools with new category:
```python
@tool_registry.register(
    name="custom_tool",
    category=ToolCategory.CUSTOM,
    description="Custom functionality"
)
async def custom_tool() -> str:
    return "Custom result"
```

### Implementing Custom State Storage

Replace in-memory storage with Redis/DB:

```python
class RedisStateStore(StateStore):
    def __init__(self, redis_client):
        self.redis = redis_client

    async def save(self, state: AgentState):
        await self.redis.set(
            state.conversation_id,
            state.to_json(),
            ex=86400
        )

    async def load(self, conversation_id: str):
        data = await self.redis.get(conversation_id)
        return AgentState.from_json(data) if data else None
```

## Best Practices

1. **Use environment variables** for configuration (API keys, model names)
2. **Implement proper error handling** in tools and service layer
3. **Set usage limits** to prevent infinite tool loops (`UsageLimits(request_limit=10)`)
4. **Force flush when streaming** with `await asyncio.sleep(0)`
5. **Track tool execution** by monitoring `result.all_messages()`
6. **Test with multiple providers** to ensure compatibility
7. **Use type hints** throughout for better IDE support
8. **Log important events** for debugging and monitoring
9. **Validate tool inputs** with Pydantic models
10. **Handle state persistence** properly for conversation continuity

## Troubleshooting

**Tools not being called**:
- Check tool descriptions are clear
- Verify tool signatures are correct
- Ensure tools are registered before agent creation
- Check provider supports function calling

**Streaming not real-time**:
- Add `await asyncio.sleep(0)` after each yield
- Check SSE headers (disable buffering)
- Verify client is consuming stream properly

**Service dependencies not working**:
- Verify first parameter type annotation matches service type
- Check `_bind_service` is called for the tool
- Ensure signature is updated after binding

**State not persisting**:
- Verify `state_store.save()` is called after response
- Check state store implementation
- Ensure conversation_id is passed correctly

## Resources

### scripts/

**scaffold_agent.py** - Generates complete agent project structure with all core modules, examples, and configuration files. Run with `--minimal`, `--web`, or `--cli` flags to customize output.

### references/

Detailed implementation guides:
- **architecture.md** - Layered architecture, component responsibilities, design patterns
- **dependency-injection.md** - Service injection pattern with signature manipulation
- **streaming.md** - Real-time streaming, SSE, tool call tracking
- **providers.md** - Multi-provider configuration and usage
