---
name: letta-api-client
description: Build applications with the Letta API — a model-agnostic, stateful API for building persistent agents with memory and long-term learning. Covers SDK patterns for Python and TypeScript. Includes 24 working code examples.
license: MIT
---

# Letta API Client Skill

Build applications on top of the **Letta API** — a model-agnostic, stateful API for building persistent agents with memory and long-term learning. The Letta API powers [Letta Code](https://github.com/letta-ai/letta-code) and the [Learning SDK](https://github.com/letta-ai/learning-sdk). This skill covers the core patterns for creating agents, managing memory, building custom tools, and handling multi-user scenarios.

## When to Use This Skill

- Building applications that need persistent, stateful AI agents
- Creating chatbots, assistants, or autonomous agents with memory
- Integrating Letta into existing web/mobile applications
- Building multi-user applications where each user has their own agent
- Understanding the API layer that Letta Code and Learning SDK are built on

## Quick Start

See [getting-started.md](./getting-started.md) for first-time setup and common onboarding issues.

## SDK Versions Tested

Examples last tested with:
- **Python SDK**: `letta-client==1.7.1`
- **TypeScript SDK**: `@letta-ai/letta-client@1.7.1`

## Core Concepts

### 1. Client Setup
See [client-setup.md](./client-setup.md) for initialization patterns:
- Letta Cloud vs self-hosted connections
- Environment variable management
- Singleton patterns for web frameworks

### 2. Memory Architecture  
See [memory-architecture.md](./memory-architecture.md) for memory patterns:
- **Core Memory Blocks**: Always in-context (persona, human, custom blocks)
- **Archival Memory**: Large corpus with semantic search
- **Conversation History**: Searchable message history
- **Shared Blocks**: Multi-agent coordination

### 3. Custom Tools
See [custom-tools.md](./custom-tools.md) for tool creation:
- Simple function tools with auto-generated schemas
- Tools with environment variable secrets
- BaseTool class for complex schemas
- Sandboxed execution requirements

### 4. Client-Side Tools
See [client-side-tools.md](./client-side-tools.md) for local tool execution:
- Execute tools on your machine while agent runs on Letta API
- How [Letta Code](https://github.com/letta-ai/letta-code) runs Bash/Read/Write locally
- Approval-based flow with `type: "tool"` responses
- Access local files, databases, and private APIs

### 5. Client Injection & Secrets
See [client-injection.md](./client-injection.md) for server-side tool patterns:
- Pre-injected `client` variable on Letta Cloud
- Building custom memory tools that modify agent state
- Agent secrets via `os.getenv()`
- `LETTA_AGENT_ID` for self-referential tools

### 6. Multi-User Patterns
See [multi-user.md](./multi-user.md) for scaling:
- One agent per user (personalization)
- Shared agent with Conversations API
- Identity system for user context

### 7. Streaming
See [streaming.md](./streaming.md) for real-time responses:
- Basic SSE streaming
- Long-running operations with `include_pings`
- Background execution and resumable streams

### 8. Conversations
Conversations enable parallel sessions with shared memory:
- Thread-safe concurrent messaging (agents.messages.create is NOT thread-safe)
- Shared memory blocks across all conversations
- Separate context windows per conversation
- Use for: same user with multiple parallel tasks, multi-threaded applications

### 9. Sleeptime Agents
See [sleeptime.md](./sleeptime.md) for background memory processing:
- Enable with `enable_sleeptime=True`
- Background agent refines memory between conversations
- Good for agents that learn over time

### 10. Agent Files & Folders
See [agent-files.md](./agent-files.md) for portability and file access:
- Export/import agents with `.af` files
- Attach folders to give agents document access
- Migration checklist for moving agents

### 11. Tool Rules
See [tool-rules.md](./tool-rules.md) for constraining tool execution:
- `InitToolRule` - Force a tool to run first
- `ChildToolRule` - Control which tools can follow
- `TerminalToolRule` - End agent turn after tool
- Sequential pipelines and approval workflows

## Quick Reference

### Python SDK
```bash
pip install letta-client
```

```python
from letta_client import Letta

# Cloud
client = Letta(api_key="LETTA_API_KEY")

# Self-hosted
client = Letta(base_url="http://localhost:8283")
```

### TypeScript SDK
```bash
npm install @letta-ai/letta-client
```

```typescript
import { Letta } from "@letta-ai/letta-client";

// Cloud
const client = new Letta({ apiKey: process.env.LETTA_API_KEY });

// Self-hosted
const client = new Letta({ baseUrl: "http://localhost:8283" });
```

## Examples

See the `examples/` directory for runnable code:

**Python:**
- `01_basic_client.py` - Client initialization
- `02_create_agent.py` - Agent creation with memory blocks
- `03_custom_tool_simple.py` - Basic custom tool
- `04_custom_tool_secrets.py` - Tool with environment variables
- `05_send_message.py` - Basic messaging
- `06_send_message_stream.py` - Streaming responses
- `07_multi_user.py` - Multi-user patterns
- `08_archival_memory.py` - Archival memory operations
- `09_shared_blocks.py` - Multi-agent shared memory
- `10_conversations.py` - Parallel sessions with conversations
- `11_client_injection.py` - Custom memory tools with injected client
- `12_tool_rules.py` - Constraining tool execution order
- `13_client_side_tools.py` - Execute tools locally (like Letta Code)

**TypeScript:**
- `01_basic_client.ts` - Client initialization
- `02_create_agent.ts` - Agent creation
- `03_send_message.ts` - Basic messaging
- `04_send_message_stream.ts` - Streaming
- `05_nextjs_singleton.ts` - Next.js pattern
- `06_multi_user.ts` - Multi-user patterns
- `07_conversations.ts` - Parallel sessions
- `08_custom_tool.ts` - Custom tools with secrets
- `09_archival_memory.ts` - Long-term storage
- `10_shared_blocks.ts` - Multi-agent shared memory
- `11_client_injection.ts` - Custom memory tools
- `12_tool_rules.ts` - Tool execution order
- `13_client_side_tools.ts` - Execute tools locally (like Letta Code)

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Check `LETTA_API_KEY` env var |
| 422 Validation Error | Missing required field | Add `model`, `embedding`, or `memory_blocks` |
| Tool not found | Tool not attached to agent | `client.agents.tools.attach(agent_id, tool_id)` |
| `os.getenv()` returns None | Secret not configured | Add to agent via `secrets` parameter |
| 524 Timeout | Long operation without pings | Add `include_pings=True` to streaming |
| Agent not responding | Model issue or empty response | Check for `assistant_message` type in response |
| Memory block not updating | Looking at wrong agent | Verify `agent_id` matches |
| Import error in tool | Top-level import | Move imports inside function body |

## Key Gotchas

1. **Imports in tools must be inside the function** - Tools run in a sandbox without access to top-level imports
2. **Use `os.getenv()` for secrets** - Don't pass sensitive data as function arguments
3. **On Cloud, use injected `client`** - Don't instantiate `Letta()` inside tools, use the pre-injected client
4. **Memory blocks are character-limited** - Use archival memory for large data
5. **Streaming requires `include_pings=True` for long operations** - Prevents timeout on Cloud
6. **SDK 1.0 uses `.update()` not `.modify()`** - Method was renamed
7. **`LETTA_AGENT_ID` is always available** - Use it in tools to reference the current agent
8. **Archival tools need `include_base_tools=True`** - Not attached by default
9. **Use `memory_insert` for shared blocks** - Safest for concurrent writes (append-only)
10. **Tool docstrings require Args section** - Parameters need descriptions or schema generation fails

## TypeScript SDK Notes

```typescript
// Client initialization uses baseURL (not baseUrl)
const client = new Letta({ apiKey: "...", baseURL: "http://localhost:8283" });

// Block API: positional args changed
client.agents.blocks.attach(blockId, { agent_id });      // blockId is first
client.agents.blocks.retrieve(blockLabel, { agent_id }); // label is first

// Passages.create returns array
const passages = await client.agents.passages.create(agentId, { text: "..." });
const passage = passages[0];

// Content can be string | array - use type guard
const content = typeof msg.content === "string" ? msg.content : JSON.stringify(msg.content);

// Conversations API returns streams by default
const stream = await client.conversations.messages.create(convId, { messages: [...] });
for await (const chunk of stream) { ... }

// Tool rule types
{ type: "run_first", tool_name: "..." }           // InitToolRule
{ type: "constrain_child_tools", tool_name: "...", children: [...] } // ChildToolRule  
{ type: "exit_loop", tool_name: "..." }           // TerminalToolRule
```

## Quick Reference

```python
# Client
client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# Create agent
agent = client.agents.create(
    model="anthropic/claude-sonnet-4-5-20250929",
    embedding="openai/text-embedding-3-small",
    memory_blocks=[{"label": "persona", "value": "..."}],
    include_base_tools=True,  # archival memory tools
    enable_sleeptime=True,    # background memory processing
)

# Send message
response = client.agents.messages.create(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "Hello"}]
)

# Stream response
stream = client.agents.messages.stream(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "Hello"}],
    stream_tokens=True,
    include_pings=True,  # prevent timeout
)

# Create tool
tool = client.tools.create(source_code="def my_tool(x: str) -> str: ...")
client.agents.tools.attach(agent_id=agent.id, tool_id=tool.id)

# Memory blocks
client.agents.blocks.retrieve(agent_id=agent.id, block_label="persona")
client.agents.blocks.update(agent_id=agent.id, block_label="persona", value="...")

# Folders
folder = client.folders.create(name="docs")
client.folders.files.upload(file=f, folder_id=folder.id)
client.agents.folders.attach(agent_id=agent.id, folder_id=folder.id)

# Conversations (parallel sessions)
conv = client.conversations.create(agent_id=agent.id)
stream = client.conversations.messages.create(conv.id, messages=[...])

# Agent secrets (for tools)
client.agents.update(agent_id=agent.id, secrets={"API_KEY": "..."})
```

## Resources

**Platform:**
- [Letta Cloud (ADE)](https://app.letta.com) - Agent Development Environment
- [API Keys](https://app.letta.com/api-keys) - Get your API key

**Documentation:**
- [Letta Docs](https://docs.letta.com) - Full documentation
- [Agents Guide](https://docs.letta.com/guides/agents/overview) - Agent concepts
- [Memory Blocks](https://docs.letta.com/guides/agents/memory-blocks) - Memory architecture
- [Custom Tools](https://docs.letta.com/guides/agents/custom-tools) - Tool creation
- [Streaming](https://docs.letta.com/guides/agents/streaming) - Real-time responses
- [Multi-User](https://docs.letta.com/guides/agents/multi-user) - Scaling patterns

**SDKs:**
- [Python SDK](https://github.com/letta-ai/letta-python) - `pip install letta-client`
- [TypeScript SDK](https://github.com/letta-ai/letta-node) - `npm install @letta-ai/letta-client`

**Examples:**
- [Chatbot Example](https://github.com/letta-ai/letta-chatbot-example) - Full app example
