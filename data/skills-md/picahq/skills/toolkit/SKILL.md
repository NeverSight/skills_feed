---
name: toolkit
description: Build AI agents with access to 200+ integrations using Pica ToolKit (Vercel AI SDK, LangChain, OpenAI Agents, MCP)
---

# Pica ToolKit

Build AI agents that can interact with 200+ third-party integrations. ToolKit provides a unified interface across Vercel AI SDK, LangChain, OpenAI Agents, and MCP.

## Overview

ToolKit gives your AI agents access to:
- 25,000+ actions across 200+ platforms (Gmail, Slack, HubSpot, Stripe, etc.)
- Built-in authentication and token management
- Rate limiting, retries, and error handling
- Schema validation via Pica's knowledge base

## Prerequisites

- Pica API key from https://app.picaos.com/settings/api-keys
- At least one connected integration in the Pica dashboard
- LLM provider API key (OpenAI, Anthropic, Google, etc.)

---

## Framework Selection

Choose your framework:

| Framework | Package | Best For |
|-----------|---------|----------|
| Vercel AI SDK | `@picahq/toolkit` | Next.js apps, streaming UIs |
| LangChain | `pica-langchain` | Python agents, chains |
| OpenAI Agents | `@picahq/mcp` | OpenAI's Agents SDK |
| MCP Server | `@picahq/mcp` | Claude Desktop, any MCP client |

---

## Vercel AI SDK

### Installation

```bash
npm install @picahq/toolkit ai @ai-sdk/openai
```

### Environment

```bash
PICA_SECRET_KEY=your_pica_secret_key
OPENAI_API_KEY=your_openai_key
```

### Basic Usage

```typescript
import { Pica } from "@picahq/toolkit";
import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";

// Initialize Pica
const pica = new Pica(process.env.PICA_SECRET_KEY!, {
  connectors: ["*"],  // All connections, or specific keys
  actions: ["*"],     // All actions, or specific IDs
});

// Create streaming response
const result = streamText({
  model: openai("gpt-4o"),
  messages: [{ role: "user", content: "Send an email to team@example.com" }],
  tools: pica.tools(),
  system: pica.systemPrompt,
});
```

### Configuration Options

```typescript
const pica = new Pica(process.env.PICA_SECRET_KEY!, {
  // Connection filtering
  connectors: ["*"],                    // All, or ["live::gmail::default::abc123"]
  actions: ["*"],                       // All, or ["gmail-send-email"]

  // Permissions
  permissions: "admin",                 // "read" | "write" | "admin"

  // Multi-tenant
  identity: userId,                     // Filter by user/team/org
  identityType: "user",                 // "user" | "team" | "organization" | "project"

  // AuthKit (prompt users to connect)
  authkit: true,

  // Advanced
  serverUrl: "https://api.picaos.com",  // Custom server
  headers: {},                          // Additional headers
});
```

### Permission Levels

| Level | HTTP Methods | Use Case |
|-------|--------------|----------|
| `read` | GET only | Customer-facing read access |
| `write` | GET, POST, PUT, PATCH | Standard operations |
| `admin` | All including DELETE | Full automation |

### Available Tools

When you call `pica.tools()`, these tools are available to the agent:

- `listPicaConnections` - List user's connected integrations
- `searchPlatformActions` - Find actions for a platform
- `getActionsKnowledge` - Get schema and parameters for an action
- `execute` - Execute an action on a connected platform
- `promptToConnectIntegration` - Prompt user to connect (with AuthKit)

### Full API Route Example

```typescript
import { Pica } from "@picahq/toolkit";
import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";

export async function POST(req: Request) {
  const { messages } = await req.json();
  const userId = req.headers.get("x-user-id");

  if (!userId) {
    return new Response("Unauthorized", { status: 401 });
  }

  const pica = new Pica(process.env.PICA_SECRET_KEY!, {
    connectors: ["*"],
    actions: ["*"],
    permissions: "admin",
    identity: userId,
    identityType: "user",
    authkit: true,
  });

  const customPrompt = "You help users automate tasks across their connected tools.";

  const result = streamText({
    model: openai("gpt-4o"),
    messages,
    tools: pica.tools(),
    system: pica.generateSystemPrompt(customPrompt),
    maxSteps: 25,  // Prevent infinite loops
  });

  return result.toDataStreamResponse();
}
```

### Custom System Prompt

```typescript
// Combine your prompt with Pica's
const systemPrompt = pica.generateSystemPrompt(
  "You are a sales automation assistant.",
  "\n\n"  // Separator
);

// Or access Pica's prompt directly
console.log(pica.systemPrompt);
```

---

## LangChain (Python)

### Installation

```bash
pip install pica-langchain langchain-openai
```

### Environment

```bash
export PICA_SECRET=your_pica_secret_key
export OPENAI_API_KEY=your_openai_key
```

### Basic Usage

```python
import os
from pica_langchain import PicaClient, create_pica_agent
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType

# Initialize client
pica_client = PicaClient(secret=os.environ["PICA_SECRET"])
pica_client.initialize()

# Create agent
agent = create_pica_agent(
    client=pica_client,
    llm=ChatOpenAI(temperature=0, model="gpt-4o"),
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

# Run
response = agent.invoke({"input": "List my Gmail labels"})
print(response["output"])
```

### Configuration Options

```python
from pica_langchain import PicaClient, PicaClientOptions

options = PicaClientOptions(
    connectors=["*"],           # All or specific connection keys
    permissions="admin",        # "read" | "write" | "admin"
    identity=user_id,           # Multi-tenant filtering
    identity_type="user",       # "user" | "team" | "organization" | "project"
    authkit=True,               # Enable connection prompts
    server_url=None,            # Custom server URL
)

pica_client = PicaClient(
    secret=os.environ["PICA_SECRET"],
    options=options,
)
pica_client.initialize()
```

### Streaming

```python
from langchain.callbacks import StreamingStdOutCallbackHandler

agent = create_pica_agent(
    client=pica_client,
    llm=ChatOpenAI(
        temperature=0,
        model="gpt-4o",
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    ),
    agent_type=AgentType.OPENAI_FUNCTIONS,
)
```

### Adding Custom Tools

```python
from langchain.tools import Tool

custom_tool = Tool(
    name="calculator",
    func=lambda x: eval(x),
    description="Evaluate math expressions",
)

agent = create_pica_agent(
    client=pica_client,
    llm=llm,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    extra_tools=[custom_tool],
)
```

---

## OpenAI Agents SDK

### Installation

```bash
pip install openai-agents
npm install -g @picahq/mcp
```

### Environment

```bash
export PICA_SECRET=your_pica_secret_key
export OPENAI_API_KEY=your_openai_key
```

### Basic Usage

```python
from agents import Agent, Runner
from agents.extensions.mcp import MCPServerManager
import os

# Initialize MCP server
mcp = MCPServerManager()
mcp.add_server(
    name="pica",
    command="npx",
    args=["@picahq/mcp"],
    env={"PICA_SECRET": os.getenv("PICA_SECRET")},
)

# Create agent with Pica tools
async with mcp:
    tools = await mcp.list_tools()

    agent = Agent(
        name="Assistant",
        instructions="""You help users with their connected integrations.

        Workflow:
        1. Use list_pica_integrations to see connections
        2. Use get_pica_platform_actions to find actions
        3. Use get_pica_action_knowledge for parameters
        4. Use execute_pica_action to run actions
        """,
        tools=tools,
    )

    result = await Runner.run(agent, "Send a Slack message to #general")
    print(result.final_output)
```

### Available MCP Tools

- `list_pica_integrations` - View connected platforms
- `get_pica_platform_actions` - Discover available actions
- `get_pica_action_knowledge` - Get parameter schemas
- `execute_pica_action` - Execute an action

### Agent Handoffs

```python
# Specialist agent for integrations
integration_agent = Agent(
    name="Integration Specialist",
    instructions="Handle all third-party integration tasks.",
    tools=pica_tools,
)

# Main agent that can hand off
main_agent = Agent(
    name="Assistant",
    instructions="Route integration tasks to the specialist.",
    handoffs=[integration_agent],
)
```

### Guardrails

```python
from agents import GuardrailFunctionOutput, input_guardrail

@input_guardrail
async def block_sensitive_emails(ctx, agent, input_data):
    if "ceo@" in input_data.lower():
        return GuardrailFunctionOutput(
            output_info={"blocked": True},
            tripwire_triggered=True,
        )
    return GuardrailFunctionOutput(output_info={"blocked": False})

agent = Agent(
    name="Assistant",
    input_guardrails=[block_sensitive_emails],
    tools=tools,
)
```

---

## MCP Server (Claude Desktop)

### Installation

```bash
npm install -g @picahq/mcp
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pica": {
      "command": "npx",
      "args": ["@picahq/mcp"],
      "env": {
        "PICA_SECRET": "your_pica_secret_key"
      }
    }
  }
}
```

### Available Tools in Claude

Once configured, Claude Desktop has access to:

- **list_pica_integrations** - "What integrations do I have connected?"
- **get_pica_platform_actions** - "What can I do with Gmail?"
- **get_pica_action_knowledge** - "How do I send an email?"
- **execute_pica_action** - "Send an email to john@example.com"

---

## Best Practices

### 1. Specify Connections in Production

```typescript
// Development - convenient
connectors: ["*"]

// Production - faster, more secure
connectors: ["live::gmail::default::abc123", "live::slack::default::xyz789"]
```

### 2. Use Appropriate Permissions

```typescript
// Customer-facing: read-only
permissions: "read"

// Standard operations
permissions: "write"

// Internal automation only
permissions: "admin"
```

### 3. Always Filter by Identity in Multi-Tenant Apps

```typescript
const pica = new Pica(secretKey, {
  identity: userId,
  identityType: "user",
});
```

### 4. Set Step Limits

```typescript
// Vercel AI SDK
streamText({
  maxSteps: 25,  // Prevent infinite loops
});
```

### 5. Handle Errors Gracefully

```typescript
try {
  const result = await streamText({ ... });
} catch (error) {
  if (error.message.includes("rate limit")) {
    // Retry with backoff
  }
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No connections available | Missing connections or wrong filter | Check dashboard, verify `connectors` config |
| Actions won't execute | Permission denied or bad params | Check `permissions` level, verify action schema |
| System prompt too long | Too many connections/actions | Specify exact connections, use smaller action set |
| Authentication errors | Invalid or expired credentials | Verify API key, reconnect integration in dashboard |
| MCP server won't start | Node.js issue or missing env | Verify `npx` works, check `PICA_SECRET` is set |
| Rate limit errors | Too many requests | Implement backoff, reduce request frequency |

---

## API Reference

### Pica Constructor

```typescript
new Pica(secretKey: string, options?: PicaOptions)
```

### PicaOptions

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `connectors` | `string[]` | `["*"]` | Connection keys to enable |
| `actions` | `string[]` | `["*"]` | Action IDs to enable |
| `permissions` | `string` | `"admin"` | `"read"` / `"write"` / `"admin"` |
| `identity` | `string` | - | User/team/org ID for filtering |
| `identityType` | `string` | - | `"user"` / `"team"` / `"organization"` / `"project"` |
| `authkit` | `boolean` | `false` | Enable connection prompts |
| `serverUrl` | `string` | `https://api.picaos.com` | Custom API server |
| `headers` | `Record<string, string>` | `{}` | Additional HTTP headers |

### Pica Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `tools()` | `ToolSet` | Tools for Vercel AI SDK |
| `systemPrompt` | `string` | Generated system prompt |
| `generateSystemPrompt(custom?, separator?)` | `string` | Combined prompt |
| `getConnectedIntegrations()` | `Promise<Connection[]>` | User's connections |
| `getAvailableConnectors()` | `Promise<Connector[]>` | All 200+ platforms |
| `getAvailableActions(platform)` | `Promise<Action[]>` | Platform actions |

### Links

- Demo: https://github.com/picahq/toolkit-demo
- Actions Browser: https://app.picaos.com/tools
- Documentation: https://docs.picaos.com
- AuthKit: See `authkit` skill for OAuth widget setup
