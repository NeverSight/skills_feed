---
name: thesys-c1-genui
description: Provides comprehensive guidance for building AI-powered Generative UI applications with the Thesys C1 API and GenUI SDK. Use it when developing interactive UI components, chat interfaces, dashboards, or any application that benefits from dynamically generated React interfaces from natural language prompts.
---

**Note: Refer to this SKILL.md file whenever there is any requirement for adding/editing functionality for C1.**

# Thesys C1 Generative UI Development

This skill provides comprehensive guidance for developing applications with the Thesys C1 API and GenUI SDK, enabling AI-powered Generative UI applications.

## What is Thesys C1?

Thesys C1 is a Generative UI API that dynamically generates interactive UI components from natural language prompts. Unlike traditional AI that returns text/markdown, C1 generates live, interactive interfaces rendered through React components.

### Key Features

- **Interactive Components**: Forms, charts, tables, buttons that users can interact with
- **Themeable**: Consistent brand styling via `<ThemeProvider>`
- **Real-time UI Streaming**: Progressive rendering as responses generate
- **OpenAI-Compatible API**: Drop-in replacement for OpenAI SDKs
- **Robust Error Handling**: Graceful degradation with `onError` prop

### What Can You Build?

- Analytics dashboards with dynamic charts
- Conversational AI agents with rich UI
- Internal tools and admin panels
- E-commerce flows with forms and product displays
- AI assistants like ChatGPT with Generative UI

---

## Quickstart

### Prerequisites

- Node.js 18+ or Python 3.8+
- Thesys API key from [console.thesys.dev](https://console.thesys.dev)
- Install the required packages:

```bash
npm install @thesysai/genui-sdk@latest @crayonai/react-ui@latest @crayonai/react-core@latest @crayonai/stream@latest openai@latest next@latest react@^19.0.0 react-dom@^19.0.0
```

### Next.js Setup

```bash
npx create-c1-app my-app
cd my-app
npm run dev
```

### Python (FastAPI) Setup

```bash
git clone https://github.com/thesysdev/template-c1-fastapi.git
cd template-c1-fastapi
pip install -r requirements.txt
uvicorn main:app --reload
# In another terminal for frontend:
npm install && npm run dev
```

Set your API key:
```bash
export THESYS_API_KEY=<your-api-key>
```

---

## Core Components

### `<C1Component>` - Render C1 Responses

The fundamental component that renders C1 DSL into a functional micro-frontend:

```tsx
import { C1Component, ThemeProvider } from "@thesysai/genui-sdk";
import "@crayonai/react-ui/styles/index.css";

<ThemeProvider>
  <C1Component
    c1Response={response}
    isStreaming={isLoading}
    onAction={({ llmFriendlyMessage, humanFriendlyMessage }) => {
      // Handle button clicks, form submissions
    }}
    updateMessage={(updatedResponse) => {
      // Persist state changes to database
    }}
  />
</ThemeProvider>
```

### `<C1Chat>` - Full Conversational UI

A batteries-included chat component with thread management:

```tsx
import { C1Chat } from "@thesysai/genui-sdk";
import "@crayonai/react-ui/styles/index.css";

<C1Chat
  apiUrl="/api/chat"
  agentName="My Assistant"
  logoUrl="/logo.png"
  formFactor="full-page"  // or "side-panel"
/>
```

### Key Differences

| Feature | `<C1Component>` | `<C1Chat>` |
|---------|-----------------|------------|
| Render C1 DSL | ✅ | ✅ |
| Streaming | ✅ | ✅ |
| Forms & Actions | ✅ | ✅ |
| Message History | DIY | ✅ Built-in |
| Thread Management | DIY | ✅ Built-in |
| Chat UI | ❌ | ✅ |

---

## How C1 Works

### The Flow

1. **User sends prompt** → Frontend
2. **Frontend calls backend** → Your API
3. **Backend calls C1 API** → `https://api.thesys.dev/v1/embed`
4. **C1 returns DSL** → Backend
5. **Backend streams to frontend** → Response
6. **`<C1Component>` renders UI** → User sees interactive UI

### Backend API Call

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://api.thesys.dev/v1/embed",
  apiKey: process.env.THESYS_API_KEY,
});

const response = await client.chat.completions.create({
  model: "c1/anthropic/claude-sonnet-4/v-20251230",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Show me a chart of sales data" }
  ],
  stream: true,
});
```

### C1 Response Structure

C1 responses use an XML-like structure:

```xml
<thinking>Analyzing request...</thinking>
<content>
  <!-- Interactive UI components -->
</content>
<artifact id="report-1">
  <!-- Document content like slides/reports -->
</artifact>
```

### Supported Models

**Stable Models:**
- `c1/anthropic/claude-sonnet-4/v-20251230`
- `c1/openai/gpt-5/v-20251230`

**Experimental Models:**
- `c1-exp/anthropic/claude-sonnet-4.5/v-20251230`
- `c1-exp/anthropic/claude-haiku-4.5/v-20251230`

**Artifact Model:**
- `c1/artifact/v-20251230`

---

## Backend API Setup

### Install Dependencies

```bash
npm install openai @crayonai/stream
```

### Create Message Store

```typescript
// app/api/chat/messageStore.ts
import OpenAI from "openai";

export type DBMessage = OpenAI.Chat.ChatCompletionMessageParam & { id?: string };

const messagesStore: { [threadId: string]: DBMessage[] } = {};

export const getMessageStore = (threadId: string) => {
  if (!messagesStore[threadId]) {
    messagesStore[threadId] = [];
  }
  return {
    addMessage: (message: DBMessage) => {
      messagesStore[threadId].push(message);
    },
    getOpenAICompatibleMessageList: () => {
      return messagesStore[threadId].map((m) => {
        const { id, ...rest } = m;
        return rest;
      });
    },
  };
};
```

### Create Chat Endpoint

```typescript
// app/api/chat/route.ts
import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
import { transformStream } from "@crayonai/stream";
import { DBMessage, getMessageStore } from "./messageStore";

export async function POST(req: NextRequest) {
  const { prompt, threadId, responseId } = await req.json() as {
    prompt: DBMessage;
    threadId: string;
    responseId: string;
  };

  const client = new OpenAI({
    baseURL: "https://api.thesys.dev/v1/embed",
    apiKey: process.env.THESYS_API_KEY,
  });

  const messageStore = getMessageStore(threadId);
  messageStore.addMessage(prompt);

  const llmStream = await client.chat.completions.create({
    model: "c1/anthropic/claude-sonnet-4/v-20251230",
    messages: messageStore.getOpenAICompatibleMessageList(),
    stream: true,
  });

  const responseStream = transformStream(
    llmStream,
    (chunk) => chunk.choices[0].delta.content,
    {
      onEnd: ({ accumulated }) => {
        const message = accumulated.filter(Boolean).join("");
        messageStore.addMessage({
          role: "assistant",
          content: message,
          id: responseId,
        });
      },
    }
  ) as ReadableStream;

  return new NextResponse(responseStream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  });
}
```

---

## Integration Patterns

### C1 as Gateway LLM (Recommended)

Replace your existing LLM endpoint with C1:

```typescript
const client = new OpenAI({
  baseURL: "https://api.thesys.dev/v1/embed",  // Change from OpenAI
  apiKey: process.env.THESYS_API_KEY,
});

// Use existing tools and system prompts
const response = await client.beta.chat.completions.runTools({
  model: "c1/anthropic/claude-sonnet-4/v-20251230",
  messages: [...],
  tools: existingTools,
  stream: true,
});
```

### C1 as Presentation Layer

Generate text with your LLM, then visualize with C1:

```typescript
// 1. Get text from your LLM
const textResponse = await yourLLM.generate(prompt);

// 2. Visualize with C1
const uiResponse = await c1Client.chat.completions.create({
  model: "c1/anthropic/claude-sonnet-4/v-20251230",
  messages: [{ role: "user", content: textResponse }],
});
```

### C1 as a Tool

Expose C1 as a tool your agent can invoke:

```typescript
const tools = [{
  type: "function",
  function: {
    name: "generate_ui",
    description: "Generate interactive UI for user",
    parameters: {
      type: "object",
      properties: {
        content: { type: "string", description: "Content to visualize" }
      }
    }
  }
}];
```

---

If the user wants to visualize their own data, refer to [visualize-api-endpoint.md](./visualize-api-endpoint.md).

---

## Additional References

For detailed information on specific topics, see:

- **[Conversational UI & Persistence](./conversational-ui-and-persistence.md)**: State management, `useThreadManager`, `useThreadListManager`, database persistence
- **[Custom Actions, Components & Thinking States](./custom-actions-components-thinking-states.md)**: `c1_custom_actions`, `onAction`, custom components, `useC1State`, thinking states
- **[Artifacts](./artifacts.md)**: Generating, rendering, editing, and exporting reports/presentations
- **[Customizations & Styling](./customizations-and-styling.md)**: `<ThemeProvider>`, chart palettes, CSS overrides
- **[Migration Guide](./migration.md)**: Step-by-step migration from text-based LLM to Generative UI

---

## Resources

- **Documentation**: https://docs.thesys.dev
- **API Reference**: https://docs.thesys.dev/api-reference/getting-started
- **Examples**: https://github.com/thesysdev/examples
- **Discord Community**: https://discord.gg/Pbv5PsqUSv
