---
name: agentmail-toolkit
description: Add email capabilities to AI agents using popular frameworks. Provides pre-built tools for TypeScript and Python frameworks including Vercel AI SDK, LangChain, Clawdbot, OpenAI Agents SDK, and LiveKit Agents. Use when integrating AgentMail with agent frameworks that need email send/receive tools.
---

# AgentMail Toolkit

Pre-built email tools for popular agent frameworks. Instantly add inbox management, sending, receiving, and email automation to your agents.

## Installation

```bash
# TypeScript/Node
npm install agentmail-toolkit

# Python
pip install agentmail-toolkit
```

## Configuration

Set your API key as an environment variable:

```bash
export AGENTMAIL_API_KEY=your-api-key
```

Get your API key from [console.agentmail.to](https://console.agentmail.to).

---

## TypeScript Frameworks

### Vercel AI SDK

```typescript
import { AgentMailToolkit } from "agentmail-toolkit/ai-sdk";
import { streamText } from "ai";
import { openai } from "@ai-sdk/openai";

const toolkit = new AgentMailToolkit();

const result = await streamText({
  model: openai("gpt-4o"),
  messages,
  system: "You are an email agent that can send and receive emails.",
  tools: toolkit.getTools(),
});
```

### LangChain

```typescript
import { createAgent, HumanMessage, AIMessage } from "langchain";
import { AgentMailToolkit } from "agentmail-toolkit/langchain";

const agent = createAgent({
  model: "openai:gpt-4o",
  tools: new AgentMailToolkit().getTools(),
  systemPrompt: "You are an email agent that can send and receive emails.",
});

const result = await agent.stream({ messages }, { streamMode: "messages" });
```

### Clawdbot (Pi Agent)

For Clawdbot/Pi Agent integration.

```typescript
import { AgentMailToolkit } from "agentmail-toolkit/clawdbot";

const toolkit = new AgentMailToolkit();
const tools = toolkit.getTools();

// Each tool has: name, label, description, parameters, execute
for (const tool of tools) {
  agent.registerTool(tool);
}
```

---

## Python Frameworks

### OpenAI Agents SDK

```python
from agentmail_toolkit.openai import AgentMailToolkit
from agents import Agent

agent = Agent(
    name="Email Agent",
    instructions="You can send, receive, and manage emails.",
    tools=AgentMailToolkit().get_tools(),
)
```

### LangChain

```python
from langchain.agents import create_agent
from agentmail_toolkit.langchain import AgentMailToolkit

agent = create_agent(
    model="gpt-4o",
    system_prompt="You are an email agent that can send and receive emails.",
    tools=AgentMailToolkit().get_tools(),
)

result = agent.stream({"messages": messages}, stream_mode="messages")
```

### LiveKit Agents

For voice AI agents with email capabilities.

```python
from livekit.agents import Agent
from agentmail_toolkit.livekit import AgentMailToolkit

agent = Agent(
    name="Voice Email Agent",
    tools=AgentMailToolkit().get_tools(),
)
```

---

## Available Tools

All frameworks get access to these tools:

| Tool               | Description              |
| ------------------ | ------------------------ |
| `create_inbox`     | Create a new email inbox |
| `list_inboxes`     | List all inboxes         |
| `get_inbox`        | Get inbox details        |
| `delete_inbox`     | Delete an inbox          |
| `send_message`     | Send an email            |
| `reply_to_message` | Reply to an email        |
| `list_threads`     | List email threads       |
| `get_thread`       | Get thread details       |
| `get_attachment`   | Download an attachment   |
| `update_message`   | Update message labels    |

---

## Custom Configuration

### Custom API Key

```typescript
// TypeScript
const toolkit = new AgentMailToolkit({ apiKey: "your-api-key" });
```

```python
# Python
toolkit = AgentMailToolkit(api_key="your-api-key")
```

### Custom Client

```python
# Python - use existing AgentMail client
from agentmail import AgentMail
from agentmail_toolkit.openai import AgentMailToolkit

client = AgentMail(api_key="your-api-key")
toolkit = AgentMailToolkit(client=client)
```

---

## Framework Summary

| Framework         | TypeScript Import                    | Python Import                                              |
| ----------------- | ------------------------------------ | ---------------------------------------------------------- |
| Vercel AI SDK     | `from 'agentmail-toolkit/ai-sdk'`    | -                                                          |
| LangChain         | `from 'agentmail-toolkit/langchain'` | `from agentmail_toolkit.langchain import AgentMailToolkit` |
| Clawdbot          | `from 'agentmail-toolkit/clawdbot'`  | -                                                          |
| OpenAI Agents SDK | -                                    | `from agentmail_toolkit.openai import AgentMailToolkit`    |
| LiveKit Agents    | -                                    | `from agentmail_toolkit.livekit import AgentMailToolkit`   |
