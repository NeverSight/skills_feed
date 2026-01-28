---
name: mcp-server
description: Build MCP (Model Context Protocol) servers using the official Python SDK. Covers FastMCP high-level API with @mcp.tool(), @mcp.resource(), @mcp.prompt() decorators, FastAPI/Starlette integration, transports (stdio, SSE, streamable-http), and database integration.
---

# MCP Server Skill

Build MCP (Model Context Protocol) servers using the official Python SDK with FastMCP high-level API.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MCP Server (FastMCP)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │   @tool()   │  │ @resource() │  │  @prompt()  │                     │
│  │  add_task   │  │ tasks://    │  │ task_prompt │                     │
│  │ list_tasks  │  │ user://     │  │ help_prompt │                     │
│  │complete_task│  │             │  │             │                     │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘                     │
│         │                │                                              │
│         ▼                ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Database Layer (SQLModel)                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              │ Transports: stdio | SSE | streamable-http
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         MCP Client (Agent)                              │
│              OpenAI Agents SDK / Claude / Other Clients                 │
└─────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
# pip
pip install mcp

# poetry
poetry add mcp

# uv
uv add mcp
```

### Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

## Core Concepts

| Concept | Decorator | Purpose |
|---------|-----------|---------|
| **Tools** | `@mcp.tool()` | Perform actions, computations, side effects |
| **Resources** | `@mcp.resource()` | Expose data for reading (URI-based) |
| **Prompts** | `@mcp.prompt()` | Reusable prompt templates |

## Basic MCP Server

```python
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP("Todo Server", json_response=True)

# Define a tool
@mcp.tool()
def add_task(title: str, description: str = None) -> dict:
    """Add a new task to the todo list."""
    # Implementation here
    return {"task_id": 1, "status": "created"}

# Define a resource
@mcp.resource("tasks://{user_id}")
def get_user_tasks(user_id: str) -> str:
    """Get all tasks for a user."""
    return "task data as string"

# Define a prompt
@mcp.prompt()
def task_assistant(task_type: str = "general") -> str:
    """Generate a task management prompt."""
    return f"You are a helpful {task_type} task assistant."

# Run the server
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

## Reference

| Pattern | Guide |
|---------|-------|
| **Tools** | [reference/tools.md](reference/tools.md) |
| **Resources** | [reference/resources.md](reference/resources.md) |
| **Prompts** | [reference/prompts.md](reference/prompts.md) |
| **Transports** | [reference/transports.md](reference/transports.md) |
| **FastAPI Integration** | [reference/fastapi-integration.md](reference/fastapi-integration.md) |

## Examples

| Example | Description |
|---------|-------------|
| [examples/todo-server.md](examples/todo-server.md) | Complete todo MCP server with CRUD tools |
| [examples/database-integration.md](examples/database-integration.md) | MCP server with SQLModel database |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/mcp_server.py](templates/mcp_server.py) | Basic MCP server template |
| [templates/mcp_tools.py](templates/mcp_tools.py) | Tool definitions template |
| [templates/mcp_fastapi.py](templates/mcp_fastapi.py) | FastAPI + MCP integration template |

## FastAPI/Starlette Integration

```python
import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Todo Server", stateless_http=True, json_response=True)

@mcp.tool()
def add_task(title: str) -> dict:
    """Add a task."""
    return {"status": "created"}

# Lifespan manager for session handling
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield

# Create Starlette app with MCP mounted
app = Starlette(
    routes=[
        Mount("/mcp", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

# Add CORS for browser clients
app = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"],
    expose_headers=["Mcp-Session-Id"],
)

# Run with: uvicorn server:app --reload
# MCP endpoint: http://localhost:8000/mcp/mcp
```

## Tool with Context (Progress, Logging)

```python
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("Progress Server")

@mcp.tool()
async def long_task(steps: int, ctx: Context) -> str:
    """Execute a task with progress updates."""
    await ctx.info("Starting task...")

    for i in range(steps):
        progress = (i + 1) / steps
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Step {i + 1}/{steps}",
        )
        await ctx.debug(f"Completed step {i + 1}")

    return f"Task completed in {steps} steps"
```

## Database Integration with Lifespan

```python
from contextlib import asynccontextmanager
from dataclasses import dataclass
from mcp.server.fastmcp import Context, FastMCP

@dataclass
class AppContext:
    db: Database

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        await db.disconnect()

mcp = FastMCP("DB Server", lifespan=app_lifespan)

@mcp.tool()
def query_tasks(user_id: str, ctx: Context) -> list:
    """Query tasks from database."""
    app_ctx = ctx.request_context.lifespan_context
    return app_ctx.db.query(f"SELECT * FROM tasks WHERE user_id = '{user_id}'")
```

## Transport Options

| Transport | Use Case | Command |
|-----------|----------|---------|
| **stdio** | CLI tools, local agents | `mcp.run()` or `mcp.run(transport="stdio")` |
| **SSE** | Web clients, real-time | `mcp.run(transport="sse", port=8000)` |
| **streamable-http** | Production APIs | `mcp.run(transport="streamable-http")` |

## Stateless vs Stateful

```python
# Stateless (recommended for production)
mcp = FastMCP("Server", stateless_http=True, json_response=True)

# Stateful (maintains session state)
mcp = FastMCP("Server")
```

## Security Considerations

1. **Validate all inputs** - Never trust user-provided data
2. **Use parameterized queries** - Prevent SQL injection
3. **Authenticate requests** - Verify user identity before operations
4. **Limit resource access** - Only expose necessary data
5. **Log tool invocations** - Audit trail for debugging

## Troubleshooting

### Server won't start
- Check port availability
- Verify dependencies installed
- Check for syntax errors in tool definitions

### Client can't connect
- Verify transport matches (stdio/SSE/HTTP)
- Check CORS configuration for web clients
- Ensure MCP endpoint URL is correct

### Tools not appearing
- Verify `@mcp.tool()` decorator is applied
- Check function has docstring (used as description)
- Restart server after adding new tools
