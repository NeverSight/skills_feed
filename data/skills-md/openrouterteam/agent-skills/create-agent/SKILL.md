---
name: create-agent
description: Bootstrap a modular AI agent with OpenRouter SDK, extensible hooks, and optional Ink TUI
metadata:
  version: 0.0.0
  homepage: https://openrouter.ai
---

# Build a Modular AI Agent with OpenRouter

This skill helps you create a **modular AI agent** with:

- **Standalone Agent Core** - Runs independently, extensible via hooks
- **OpenRouter SDK** - Unified access to 300+ language models
- **Optional Ink TUI** - Beautiful terminal UI (separate from agent logic)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Your Application                 │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Ink TUI   │  │  HTTP API   │  │   Discord   │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
│         │                │                │         │
│         └────────────────┼────────────────┘         │
│                          ▼                          │
│              ┌───────────────────────┐              │
│              │      Agent Core       │              │
│              │  (hooks & lifecycle)  │              │
│              └───────────┬───────────┘              │
│                          ▼                          │
│              ┌───────────────────────┐              │
│              │    OpenRouter SDK     │              │
│              └───────────────────────┘              │
└─────────────────────────────────────────────────────┘
```

## Prerequisites

Get an OpenRouter API key at: https://openrouter.ai/settings/keys

⚠️ **Security:** Never commit API keys. Use environment variables.

## Project Setup

### Step 1: Initialize Project

```bash
mkdir my-agent && cd my-agent
npm init -y
npm pkg set type="module"
```

### Step 2: Install Dependencies

```bash
npm install @openrouter/sdk zod eventemitter3
npm install ink react  # Optional: only for TUI
npm install -D typescript @types/react tsx
```

### Step 3: Create tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
```

### Step 4: Add Scripts to package.json

```json
{
  "scripts": {
    "start": "tsx src/cli.tsx",
    "start:headless": "tsx src/headless.ts",
    "dev": "tsx watch src/cli.tsx"
  }
}
```

## File Structure

```bash
src/
├── agent.ts        # Standalone agent core with hooks
├── tools.ts        # Tool definitions
├── cli.tsx         # Ink TUI (optional interface)
└── headless.ts     # Headless usage example
```

## Step 1: Agent Core with Hooks

Create `src/agent.ts` - the standalone agent that can run anywhere:

```typescript
import { OpenRouter, tool, stepCountIs } from '@openrouter/sdk';
import type { Tool, StopCondition, StreamableOutputItem } from '@openrouter/sdk';
import { EventEmitter } from 'eventemitter3';
import { z } from 'zod';

// Message types
export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

// Agent events for hooks (items-based streaming model)
export interface AgentEvents {
  'message:user': (message: Message) => void;
  'message:assistant': (message: Message) => void;
  'item:update': (item: StreamableOutputItem) => void;  // Items emitted with same ID, replace by ID
  'stream:start': () => void;
  'stream:delta': (delta: string, accumulated: string) => void;
  'stream:end': (fullText: string) => void;
  'tool:call': (name: string, args: unknown) => void;
  'tool:result': (name: string, result: unknown) => void;
  'reasoning:update': (text: string) => void;  // Extended thinking content
  'error': (error: Error) => void;
  'thinking:start': () => void;
  'thinking:end': () => void;
}


// Agent configuration
export interface AgentConfig {
  apiKey: string;
  model?: string;
  instructions?: string;
  tools?: Tool<z.ZodTypeAny, z.ZodTypeAny>[];
  maxSteps?: number;
}

// The Agent class - runs independently of any UI
export class Agent extends EventEmitter<AgentEvents> {
  private client: OpenRouter;
  private messages: Message[] = [];
  private config: Required<Omit<AgentConfig, 'apiKey'>> & { apiKey: string };

  constructor(config: AgentConfig) {
    super();
    this.client = new OpenRouter({ apiKey: config.apiKey });
    this.config = {
      apiKey: config.apiKey,
      model: config.model ?? 'openrouter/auto',
      instructions: config.instructions ?? 'You are a helpful assistant.',
      tools: config.tools ?? [],
      maxSteps: config.maxSteps ?? 5,
    };
  }

  // Get conversation history
  getMessages(): Message[] {
    return [...this.messages];
  }

  // Clear conversation
  clearHistory(): void {
    this.messages = [];
  }

  // Add a system message
  setInstructions(instructions: string): void {
    this.config.instructions = instructions;
  }

  // Register additional tools at runtime
  addTool(newTool: Tool<z.ZodTypeAny, z.ZodTypeAny>): void {
    this.config.tools.push(newTool);
  }

  // Send a message and get streaming response using items-based model
  // Items are emitted multiple times with the same ID but progressively updated content
  // Replace items by their ID rather than accumulating chunks
  async send(content: string): Promise<string> {
    const userMessage: Message = { role: 'user', content };
    this.messages.push(userMessage);
    this.emit('message:user', userMessage);
    this.emit('thinking:start');

    try {
      const result = this.client.callModel({
        model: this.config.model,
        instructions: this.config.instructions,
        input: this.messages.map((m) => ({ role: m.role, content: m.content })),
        tools: this.config.tools.length > 0 ? this.config.tools : undefined,
        stopWhen: [stepCountIs(this.config.maxSteps)],
      });

      this.emit('stream:start');
      let fullText = '';

      // Use getItemsStream() for items-based streaming (recommended)
      // Each item emission is complete - replace by ID, don't accumulate
      for await (const item of result.getItemsStream()) {
        // Emit the item for UI state management (use Map keyed by item.id)
        this.emit('item:update', item);

        switch (item.type) {
          case 'message':
            // Message items contain progressively updated content
            const textContent = item.content?.find((c: { type: string }) => c.type === 'output_text');
            if (textContent && 'text' in textContent) {
              const newText = textContent.text;
              if (newText !== fullText) {
                const delta = newText.slice(fullText.length);
                fullText = newText;
                this.emit('stream:delta', delta, fullText);
              }
            }
            break;
          case 'function_call':
            // Function call arguments stream progressively
            if (item.status === 'completed') {
              this.emit('tool:call', item.name, JSON.parse(item.arguments || '{}'));
            }
            break;
          case 'function_call_output':
            this.emit('tool:result', item.callId, item.output);
            break;
          case 'reasoning':
            // Extended thinking/reasoning content
            const reasoningText = item.content?.find((c: { type: string }) => c.type === 'reasoning_text');
            if (reasoningText && 'text' in reasoningText) {
              this.emit('reasoning:update', reasoningText.text);
            }
            break;
          // Additional item types: web_search_call, file_search_call, image_generation_call
        }
      }

      // Get final text if streaming didn't capture it
      if (!fullText) {
        fullText = await result.getText();
      }

      this.emit('stream:end', fullText);

      const assistantMessage: Message = { role: 'assistant', content: fullText };
      this.messages.push(assistantMessage);
      this.emit('message:assistant', assistantMessage);

      return fullText;
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      this.emit('error', error);
      throw error;
    } finally {
      this.emit('thinking:end');
    }
  }

  // Send without streaming (simpler for programmatic use)
  async sendSync(content: string): Promise<string> {
    const userMessage: Message = { role: 'user', content };
    this.messages.push(userMessage);
    this.emit('message:user', userMessage);

    try {
      const result = this.client.callModel({
        model: this.config.model,
        instructions: this.config.instructions,
        input: this.messages.map((m) => ({ role: m.role, content: m.content })),
        tools: this.config.tools.length > 0 ? this.config.tools : undefined,
        stopWhen: [stepCountIs(this.config.maxSteps)],
      });

      const fullText = await result.getText();
      const assistantMessage: Message = { role: 'assistant', content: fullText };
      this.messages.push(assistantMessage);
      this.emit('message:assistant', assistantMessage);

      return fullText;
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      this.emit('error', error);
      throw error;
    }
  }
}

// Factory function for easy creation
export function createAgent(config: AgentConfig): Agent {
  return new Agent(config);
}
```

## Step 2: Define Tools

Create `src/tools.ts`:

```typescript
import { tool } from '@openrouter/sdk';
import { z } from 'zod';

export const timeTool = tool({
  name: 'get_current_time',
  description: 'Get the current date and time',
  inputSchema: z.object({
    timezone: z.string().optional().describe('Timezone (e.g., "UTC", "America/New_York")'),
  }),
  execute: async ({ timezone }) => {
    return {
      time: new Date().toLocaleString('en-US', { timeZone: timezone || 'UTC' }),
      timezone: timezone || 'UTC',
    };
  },
});

export const calculatorTool = tool({
  name: 'calculate',
  description: 'Perform mathematical calculations',
  inputSchema: z.object({
    expression: z.string().describe('Math expression (e.g., "2 + 2", "sqrt(16)")'),
  }),
  execute: async ({ expression }) => {
    // Simple safe eval for basic math
    const sanitized = expression.replace(/[^0-9+\-*/().\s]/g, '');
    const result = Function(`"use strict"; return (${sanitized})`)();
    return { expression, result };
  },
});

export const defaultTools = [timeTool, calculatorTool];
```

## Step 3: Headless Usage (No UI)

Create `src/headless.ts` - use the agent programmatically:

```typescript
import { createAgent } from './agent.js';
import { defaultTools } from './tools.js';

async function main() {
  const agent = createAgent({
    apiKey: process.env.OPENROUTER_API_KEY!,
    model: 'openrouter/auto',
    instructions: 'You are a helpful assistant with access to tools.',
    tools: defaultTools,
  });

  // Hook into events
  agent.on('thinking:start', () => console.log('\n🤔 Thinking...'));
  agent.on('tool:call', (name, args) => console.log(`🔧 Using ${name}:`, args));
  agent.on('stream:delta', (delta) => process.stdout.write(delta));
  agent.on('stream:end', () => console.log('\n'));
  agent.on('error', (err) => console.error('❌ Error:', err.message));

  // Interactive loop
  const readline = await import('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  console.log('Agent ready. Type your message (Ctrl+C to exit):\n');

  const prompt = () => {
    rl.question('You: ', async (input) => {
      if (!input.trim()) {
        prompt();
        return;
      }
      await agent.send(input);
      prompt();
    });
  };

  prompt();
}

main().catch(console.error);
```

Run headless: `OPENROUTER_API_KEY=sk-or-... npm run start:headless`

## Step 4: Ink TUI (Optional Interface)

Create `src/cli.tsx` - a beautiful terminal UI that uses the agent with items-based streaming:

```tsx
import React, { useState, useEffect, useCallback } from 'react';
import { render, Box, Text, useInput, useApp } from 'ink';
import type { StreamableOutputItem } from '@openrouter/sdk';
import { createAgent, type Agent, type Message } from './agent.js';
import { defaultTools } from './tools.js';

// Initialize agent (runs independently of UI)
const agent = createAgent({
  apiKey: process.env.OPENROUTER_API_KEY!,
  model: 'openrouter/auto',
  instructions: 'You are a helpful assistant. Be concise.',
  tools: defaultTools,
});

function ChatMessage({ message }: { message: Message }) {
  const isUser = message.role === 'user';
  return (
    <Box flexDirection="column" marginBottom={1}>
      <Text bold color={isUser ? 'cyan' : 'green'}>
        {isUser ? '▶ You' : '◀ Assistant'}
      </Text>
      <Text wrap="wrap">{message.content}</Text>
    </Box>
  );
}

// Render streaming items by type using the items-based pattern
function ItemRenderer({ item }: { item: StreamableOutputItem }) {
  switch (item.type) {
    case 'message': {
      const textContent = item.content?.find((c: { type: string }) => c.type === 'output_text');
      const text = textContent && 'text' in textContent ? textContent.text : '';
      return (
        <Box flexDirection="column" marginBottom={1}>
          <Text bold color="green">◀ Assistant</Text>
          <Text wrap="wrap">{text}</Text>
          {item.status !== 'completed' && <Text color="gray">▌</Text>}
        </Box>
      );
    }
    case 'function_call':
      return (
        <Text color="yellow">
          {item.status === 'completed' ? '  ✓' : '  🔧'} {item.name}
          {item.status === 'in_progress' && '...'}
        </Text>
      );
    case 'reasoning': {
      const reasoningText = item.content?.find((c: { type: string }) => c.type === 'reasoning_text');
      const text = reasoningText && 'text' in reasoningText ? reasoningText.text : '';
      return (
        <Box flexDirection="column" marginBottom={1}>
          <Text bold color="magenta">💭 Thinking</Text>
          <Text wrap="wrap" color="gray">{text}</Text>
        </Box>
      );
    }
    default:
      return null;
  }
}

function InputField({
  value,
  onChange,
  onSubmit,
  disabled,
}: {
  value: string;
  onChange: (v: string) => void;
  onSubmit: () => void;
  disabled: boolean;
}) {
  useInput((input, key) => {
    if (disabled) return;
    if (key.return) onSubmit();
    else if (key.backspace || key.delete) onChange(value.slice(0, -1));
    else if (input && !key.ctrl && !key.meta) onChange(value + input);
  });

  return (
    <Box>
      <Text color="yellow">{'> '}</Text>
      <Text>{value}</Text>
      <Text color="gray">{disabled ? ' ···' : '█'}</Text>
    </Box>
  );
}

function App() {
  const { exit } = useApp();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  // Use Map keyed by item ID for efficient React state updates (items-based pattern)
  const [items, setItems] = useState<Map<string, StreamableOutputItem>>(new Map());

  useInput((_, key) => {
    if (key.escape) exit();
  });

  // Subscribe to agent events using items-based streaming
  useEffect(() => {
    const onThinkingStart = () => {
      setIsLoading(true);
      setItems(new Map()); // Clear items for new response
    };

    // Items-based streaming: replace items by ID, don't accumulate
    const onItemUpdate = (item: StreamableOutputItem) => {
      setItems((prev) => new Map(prev).set(item.id, item));
    };

    const onMessageAssistant = () => {
      setMessages(agent.getMessages());
      setItems(new Map()); // Clear streaming items
      setIsLoading(false);
    };

    const onError = (err: Error) => {
      setIsLoading(false);
    };

    agent.on('thinking:start', onThinkingStart);
    agent.on('item:update', onItemUpdate);
    agent.on('message:assistant', onMessageAssistant);
    agent.on('error', onError);

    return () => {
      agent.off('thinking:start', onThinkingStart);
      agent.off('item:update', onItemUpdate);
      agent.off('message:assistant', onMessageAssistant);
      agent.off('error', onError);
    };
  }, []);

  const sendMessage = useCallback(async () => {
    if (!input.trim() || isLoading) return;
    const text = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    await agent.send(text);
  }, [input, isLoading]);

  return (
    <Box flexDirection="column" padding={1}>
      <Box marginBottom={1}>
        <Text bold color="magenta">🤖 OpenRouter Agent</Text>
        <Text color="gray"> (Esc to exit)</Text>
      </Box>

      <Box flexDirection="column" marginBottom={1}>
        {/* Render completed messages */}
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}

        {/* Render streaming items by type (items-based pattern) */}
        {Array.from(items.values()).map((item) => (
          <ItemRenderer key={item.id} item={item} />
        ))}
      </Box>

      <Box borderStyle="single" borderColor="gray" paddingX={1}>
        <InputField
          value={input}
          onChange={setInput}
          onSubmit={sendMessage}
          disabled={isLoading}
        />
      </Box>
    </Box>
  );
}

render(<App />);
```

Run TUI: `OPENROUTER_API_KEY=sk-or-... npm start`

## Understanding Items-Based Streaming

The OpenRouter SDK uses an **items-based streaming model** - a key paradigm where items are emitted multiple times with the same ID but progressively updated content. Instead of accumulating chunks, you **replace items by their ID**.

### How It Works

Each iteration of `getItemsStream()` yields a complete item with updated content:

```typescript
// Iteration 1: Partial message
{ id: "msg_123", type: "message", content: [{ type: "output_text", text: "Hello" }] }

// Iteration 2: Updated message (replace, don't append)
{ id: "msg_123", type: "message", content: [{ type: "output_text", text: "Hello world" }] }
```

For function calls, arguments stream progressively:

```typescript
// Iteration 1: Partial arguments
{ id: "call_456", type: "function_call", name: "get_weather", arguments: "{\"q" }

// Iteration 2: Complete arguments
{ id: "call_456", type: "function_call", name: "get_weather", arguments: "{\"query\": \"Paris\"}", status: "completed" }
```

### Why Items Are Better

**Traditional (accumulation required):**
```typescript
let text = '';
for await (const chunk of result.getTextStream()) {
  text += chunk;  // Manual accumulation
  updateUI(text);
}
```

**Items (complete replacement):**
```typescript
const items = new Map<string, StreamableOutputItem>();
for await (const item of result.getItemsStream()) {
  items.set(item.id, item);  // Replace by ID
  updateUI(items);
}
```

Benefits:
- **No manual chunk management** - each item is complete
- **Handles concurrent outputs** - function calls and messages can stream in parallel
- **Full TypeScript inference** for all item types
- **Natural Map-based state** works perfectly with React/UI frameworks

## Extending the Agent

### Add Custom Hooks

```typescript
const agent = createAgent({ apiKey: '...' });

// Log all events
agent.on('message:user', (msg) => {
  saveToDatabase('user', msg.content);
});

agent.on('message:assistant', (msg) => {
  saveToDatabase('assistant', msg.content);
  sendWebhook('new_message', msg);
});

agent.on('tool:call', (name, args) => {
  analytics.track('tool_used', { name, args });
});

agent.on('error', (err) => {
  errorReporting.capture(err);
});
```

### Use with HTTP Server

```typescript
import express from 'express';
import { createAgent } from './agent.js';

const app = express();
app.use(express.json());

// One agent per session (store in memory or Redis)
const sessions = new Map<string, Agent>();

app.post('/chat', async (req, res) => {
  const { sessionId, message } = req.body;

  let agent = sessions.get(sessionId);
  if (!agent) {
    agent = createAgent({ apiKey: process.env.OPENROUTER_API_KEY! });
    sessions.set(sessionId, agent);
  }

  const response = await agent.sendSync(message);
  res.json({ response, history: agent.getMessages() });
});

app.listen(3000);
```

### Use with Discord

```typescript
import { Client, GatewayIntentBits } from 'discord.js';
import { createAgent } from './agent.js';

const discord = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages],
});

const agents = new Map<string, Agent>();

discord.on('messageCreate', async (msg) => {
  if (msg.author.bot) return;

  let agent = agents.get(msg.channelId);
  if (!agent) {
    agent = createAgent({ apiKey: process.env.OPENROUTER_API_KEY! });
    agents.set(msg.channelId, agent);
  }

  const response = await agent.sendSync(msg.content);
  await msg.reply(response);
});

discord.login(process.env.DISCORD_TOKEN);
```

## Agent API Reference

### Constructor Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| apiKey | string | required | OpenRouter API key |
| model | string | 'openrouter/auto' | Model to use |
| instructions | string | 'You are a helpful assistant.' | System prompt |
| tools | Tool[] | [] | Available tools |
| maxSteps | number | 5 | Max agentic loop iterations |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `send(content)` | Promise<string> | Send message with streaming |
| `sendSync(content)` | Promise<string> | Send message without streaming |
| `getMessages()` | Message[] | Get conversation history |
| `clearHistory()` | void | Clear conversation |
| `setInstructions(text)` | void | Update system prompt |
| `addTool(tool)` | void | Add tool at runtime |

### Events

| Event | Payload | Description |
|-------|---------|-------------|
| `message:user` | Message | User message added |
| `message:assistant` | Message | Assistant response complete |
| `item:update` | StreamableOutputItem | Item emitted (replace by ID, don't accumulate) |
| `stream:start` | - | Streaming started |
| `stream:delta` | (delta, accumulated) | New text chunk |
| `stream:end` | fullText | Streaming complete |
| `tool:call` | (name, args) | Tool being called |
| `tool:result` | (name, result) | Tool returned result |
| `reasoning:update` | text | Extended thinking content |
| `thinking:start` | - | Agent processing |
| `thinking:end` | - | Agent done processing |
| `error` | Error | Error occurred |

### Item Types (from getItemsStream)

The SDK uses an items-based streaming model where items are emitted multiple times with the same ID but progressively updated content. Replace items by their ID rather than accumulating chunks.

| Type | Purpose |
|------|---------|
| `message` | Assistant text responses |
| `function_call` | Tool invocations with streaming arguments |
| `function_call_output` | Results from executed tools |
| `reasoning` | Extended thinking content |
| `web_search_call` | Web search operations |
| `file_search_call` | File search operations |
| `image_generation_call` | Image generation operations |

## Discovering Models

**Do not hardcode model IDs** - they change frequently. Use the models API:

### Fetch Available Models

```typescript
interface OpenRouterModel {
  id: string;
  name: string;
  description?: string;
  context_length: number;
  pricing: { prompt: string; completion: string };
  top_provider?: { is_moderated: boolean };
}

async function fetchModels(): Promise<OpenRouterModel[]> {
  const res = await fetch('https://openrouter.ai/api/v1/models');
  const data = await res.json();
  return data.data;
}

// Find models by criteria
async function findModels(filter: {
  author?: string;      // e.g., 'anthropic', 'openai', 'google'
  minContext?: number;  // e.g., 100000 for 100k context
  maxPromptPrice?: number; // e.g., 0.001 for cheap models
}): Promise<OpenRouterModel[]> {
  const models = await fetchModels();

  return models.filter((m) => {
    if (filter.author && !m.id.startsWith(filter.author + '/')) return false;
    if (filter.minContext && m.context_length < filter.minContext) return false;
    if (filter.maxPromptPrice) {
      const price = parseFloat(m.pricing.prompt);
      if (price > filter.maxPromptPrice) return false;
    }
    return true;
  });
}

// Example: Get latest Claude models
const claudeModels = await findModels({ author: 'anthropic' });
console.log(claudeModels.map((m) => m.id));

// Example: Get models with 100k+ context
const longContextModels = await findModels({ minContext: 100000 });

// Example: Get cheap models
const cheapModels = await findModels({ maxPromptPrice: 0.0005 });
```

### Dynamic Model Selection in Agent

```typescript
// Create agent with dynamic model selection
const models = await fetchModels();
const bestModel = models.find((m) => m.id.includes('claude')) || models[0];

const agent = createAgent({
  apiKey: process.env.OPENROUTER_API_KEY!,
  model: bestModel.id,  // Use discovered model
  instructions: 'You are a helpful assistant.',
});
```

### Using openrouter/auto

For simplicity, use `openrouter/auto` which automatically selects the best
available model for your request:

```typescript
const agent = createAgent({
  apiKey: process.env.OPENROUTER_API_KEY!,
  model: 'openrouter/auto',  // Auto-selects best model
});
```

### Models API Reference

- **Endpoint**: `GET https://openrouter.ai/api/v1/models`
- **Response**: `{ data: OpenRouterModel[] }`
- **Browse models**: https://openrouter.ai/models

## Resources

- OpenRouter Docs: https://openrouter.ai/docs
- Models API: https://openrouter.ai/api/v1/models
- Ink Docs: https://github.com/vadimdemedes/ink
- Get API Key: https://openrouter.ai/settings/keys
