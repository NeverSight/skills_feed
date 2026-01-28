---
name: chatkit-python
description: Build custom chat API backends for OpenAI ChatKit frontend using FastAPI. Covers chat endpoint implementation, SSE streaming, conversation persistence, and integration with OpenAI Agents SDK + Gemini via LiteLLM.
---

# ChatKit Python Backend Skill

Build custom chat API backends that work with OpenAI ChatKit frontend.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Frontend (ChatKit-JS)                               │
│                  useChatKit({ api: { url, domainKey } })               │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ HTTP POST /api/chat
                                  │ (SSE streaming response)
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                   /api/chat Endpoint                             │   │
│  │  • Parse ChatKit request                                         │   │
│  │  • Run Agent with MCP tools                                      │   │
│  │  • Stream response via SSE                                       │   │
│  │  • Persist conversation to DB                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐    │
│  │  OpenAI Agents  │  │   MCP Server    │  │   Neon Database     │    │
│  │  SDK + Gemini   │  │   (Todo Tools)  │  │   (Conversations)   │    │
│  └─────────────────┘  └─────────────────┘  └─────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
pip install fastapi uvicorn sse-starlette "openai-agents[litellm]"

# Or with uv
uv add fastapi uvicorn sse-starlette "openai-agents[litellm]"
```

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@host/database

# Gemini API
GOOGLE_API_KEY=your-gemini-api-key

# CORS (frontend URL)
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

## Reference

| Pattern | Guide |
|---------|-------|
| **Chat Endpoint** | [reference/chat-endpoint.md](reference/chat-endpoint.md) |
| **SSE Streaming** | [reference/sse-streaming.md](reference/sse-streaming.md) |
| **Conversation Persistence** | [reference/conversation-persistence.md](reference/conversation-persistence.md) |

## Examples

| Example | Description |
|---------|-------------|
| [examples/chat-server.md](examples/chat-server.md) | Complete chat server implementation |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/chat_router.py](templates/chat_router.py) | FastAPI chat endpoint router |
| [templates/models.py](templates/models.py) | Database models for conversations |

## Basic Chat Endpoint

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from typing import Optional, List, AsyncGenerator
import json

app = FastAPI()

# CORS for ChatKit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    thread_id: Optional[str] = None
    user_id: Optional[str] = None

async def generate_response(messages: List[ChatMessage]) -> AsyncGenerator[str, None]:
    """Generate streaming response from agent."""
    # Your agent logic here
    response = "Hello! How can I help you?"

    # Stream response word by word
    for word in response.split():
        yield f"data: {json.dumps({'content': word + ' '})}\n\n"

    yield f"data: {json.dumps({'done': True})}\n\n"

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint with SSE streaming."""
    return EventSourceResponse(
        generate_response(request.messages),
        media_type="text/event-stream",
    )
```

## Chat Endpoint with Agent

```python
import os
from fastapi import FastAPI, Request, HTTPException
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from typing import Optional, List, AsyncGenerator
import json

from agents import Agent, Runner, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp
from agents.extensions.models.litellm_model import LitellmModel

set_tracing_disabled(disabled=True)

app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    thread_id: Optional[str] = None
    user_id: str

# Global MCP server connection (managed via lifespan)
mcp_server = None

@app.on_event("startup")
async def startup():
    global mcp_server
    mcp_server = MCPServerStreamableHttp(
        name="Todo MCP",
        params={"url": "http://localhost:8000/api/mcp", "timeout": 30},
        cache_tools_list=True,
    )
    await mcp_server.__aenter__()

@app.on_event("shutdown")
async def shutdown():
    global mcp_server
    if mcp_server:
        await mcp_server.__aexit__(None, None, None)

def create_agent(user_id: str):
    """Create agent with user context."""
    return Agent(
        name="Todo Assistant",
        instructions=f"""You are a task management assistant for user {user_id}.
Use the MCP tools to help manage tasks:
- add_task: Create new tasks
- list_tasks: View tasks
- complete_task: Mark done
- delete_task: Remove tasks
Always pass user_id="{user_id}" to tools.""",
        model=LitellmModel(
            model="gemini/gemini-2.0-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
        ),
        mcp_servers=[mcp_server] if mcp_server else [],
    )

async def stream_agent_response(
    agent: Agent,
    user_message: str,
) -> AsyncGenerator[str, None]:
    """Stream agent response as SSE events."""
    try:
        result = Runner.run_streamed(agent, user_message)

        async for event in result.stream_events():
            if hasattr(event, 'item') and event.item:
                yield f"data: {json.dumps({'content': str(event.item)})}\n\n"

        # Final response
        final = result.final_output
        yield f"data: {json.dumps({'content': final, 'done': True})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with streaming response."""
    if not request.messages:
        raise HTTPException(400, "No messages provided")

    # Get last user message
    user_message = request.messages[-1].content

    # Create agent for this user
    agent = create_agent(request.user_id)

    return EventSourceResponse(
        stream_agent_response(agent, user_message),
        media_type="text/event-stream",
    )
```

## SSE Event Format

ChatKit expects Server-Sent Events in this format:

```python
# Content chunk
yield f"data: {json.dumps({'content': 'partial response'})}\n\n"

# Done signal
yield f"data: {json.dumps({'done': True})}\n\n"

# Error
yield f"data: {json.dumps({'error': 'error message'})}\n\n"

# Tool call (optional)
yield f"data: {json.dumps({'tool_call': {'name': 'add_task', 'result': {...}}})}\n\n"
```

## Conversation Persistence

```python
from sqlmodel import SQLModel, Field, Session
from datetime import datetime
from typing import Optional

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: str = Field(index=True, unique=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: str = Field(index=True)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

async def save_message(thread_id: str, role: str, content: str):
    """Save message to database."""
    with Session(engine) as session:
        message = Message(thread_id=thread_id, role=role, content=content)
        session.add(message)
        session.commit()

async def load_conversation(thread_id: str) -> List[dict]:
    """Load conversation history."""
    with Session(engine) as session:
        messages = session.exec(
            select(Message)
            .where(Message.thread_id == thread_id)
            .order_by(Message.created_at)
        ).all()
        return [{"role": m.role, "content": m.content} for m in messages]
```

## Authentication Integration

```python
from fastapi import Depends, HTTPException, Header

async def get_current_user(authorization: str = Header(...)) -> dict:
    """Verify JWT and extract user."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")

    token = authorization[7:]
    user = await verify_jwt_token(token)  # Your JWT verification

    if not user:
        raise HTTPException(401, "Invalid token")

    return user

@app.post("/api/chat")
async def chat(
    request: ChatRequest,
    user: dict = Depends(get_current_user),
):
    """Authenticated chat endpoint."""
    # Use user["id"] as user_id
    agent = create_agent(user["id"])
    # ...
```

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

# Get from environment
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)},
    )

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # ... chat logic
        pass
    except ConnectionError:
        raise HTTPException(503, "MCP server unavailable")
    except TimeoutError:
        raise HTTPException(504, "Request timed out")
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
```

## Testing

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/chat",
            json={
                "messages": [{"role": "user", "content": "Hello"}],
                "user_id": "test-user",
            },
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
```

## Best Practices

1. **Stream responses** - Better UX with SSE streaming
2. **Persist conversations** - Enable conversation continuity
3. **Authenticate requests** - Verify user before processing
4. **Handle errors gracefully** - Return structured error responses
5. **Configure CORS** - Allow frontend domain
6. **Use connection pooling** - For database and MCP connections
7. **Log conversations** - For debugging and analytics
