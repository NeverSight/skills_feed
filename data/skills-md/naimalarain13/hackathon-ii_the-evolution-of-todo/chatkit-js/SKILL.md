---
name: chatkit-js
description: Integrate OpenAI ChatKit React components into Next.js applications. Covers custom API backend configuration, theming, widget embedding, conversation history, and authentication integration.
---

# ChatKit JS Frontend Skill

Integrate OpenAI ChatKit UI components into Next.js applications with custom backend support.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Next.js Frontend                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                   ChatKit Widget                                 │   │
│  │  • useChatKit hook with custom API config                        │   │
│  │  • Theming & customization                                       │   │
│  │  • Auth token injection                                          │   │
│  │  • Conversation history                                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Custom fetch with JWT
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                                      │
│                   /api/chat (SSE streaming)                             │
└─────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
npm install @openai/chatkit-react

# Or with pnpm
pnpm add @openai/chatkit-react
```

### Environment Variables

```env
# Domain key from OpenAI (for hosted mode)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key

# Custom API URL (for custom backend mode)
NEXT_PUBLIC_CHAT_API_URL=http://localhost:8000/api/chat
```

## Reference

| Pattern | Guide |
|---------|-------|
| **Basic Setup** | [reference/basic-setup.md](reference/basic-setup.md) |
| **Custom API** | [reference/custom-api.md](reference/custom-api.md) |
| **Theming** | [reference/theming.md](reference/theming.md) |

## Examples

| Example | Description |
|---------|-------------|
| [examples/todo-chatbot.md](examples/todo-chatbot.md) | Complete todo chatbot widget |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/ChatWidget.tsx](templates/ChatWidget.tsx) | ChatKit widget component |
| [templates/ChatPage.tsx](templates/ChatPage.tsx) | Full chat page layout |

## Basic ChatKit Widget

```tsx
"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";

export function ChatWidget() {
  const { control } = useChatKit({
    api: {
      url: process.env.NEXT_PUBLIC_CHAT_API_URL || "/api/chat",
      domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
    },
  });

  return (
    <ChatKit
      control={control}
      className="h-[600px] w-[400px] rounded-lg shadow-lg"
    />
  );
}
```

## Custom API with Authentication

```tsx
"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { useSession } from "@/lib/auth-client"; // Better Auth

export function AuthenticatedChat() {
  const { data: session } = useSession();

  const { control } = useChatKit({
    api: {
      url: process.env.NEXT_PUBLIC_CHAT_API_URL || "/api/chat",
      domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,

      // Custom fetch to inject auth token
      fetch: async (input, init) => {
        const token = session?.session?.token;
        return fetch(input, {
          ...init,
          headers: {
            ...init?.headers,
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
      },
    },
  });

  if (!session) {
    return <div>Please sign in to use the chatbot</div>;
  }

  return (
    <ChatKit
      control={control}
      className="h-full w-full"
    />
  );
}
```

## Theming

```tsx
const { control } = useChatKit({
  api: { /* ... */ },
  theme: {
    colorScheme: "dark", // or "light"
    color: {
      accent: {
        primary: "#3b82f6", // Blue accent
        level: 2,
      },
      grayscale: {
        hue: 220,
        tint: 5,
        shade: 0,
      },
      surface: {
        background: "#1f2937",
        foreground: "#f9fafb",
      },
    },
    radius: "soft", // "none", "soft", "round"
    density: "normal", // "compact", "normal", "spacious"
    typography: {
      fontFamily: "Inter, system-ui, sans-serif",
      fontFamilyMono: "JetBrains Mono, monospace",
      baseSize: 16,
    },
  },
});
```

## Start Screen Customization

```tsx
const { control } = useChatKit({
  api: { /* ... */ },
  startScreen: {
    greeting: "Hi! I'm your task assistant. How can I help?",
    prompts: [
      {
        name: "View Tasks",
        prompt: "Show me my pending tasks",
        icon: "list",
      },
      {
        name: "Add Task",
        prompt: "Help me add a new task",
        icon: "plus",
      },
      {
        name: "Get Help",
        prompt: "What can you help me with?",
        icon: "question",
      },
    ],
  },
});
```

## Header Customization

```tsx
const { control } = useChatKit({
  api: { /* ... */ },
  header: {
    enabled: true,
    title: {
      enabled: true,
      text: "Todo Assistant",
    },
    leftAction: {
      icon: "sidebar-left",
      onClick: () => toggleSidebar(),
    },
    rightAction: {
      icon: "settings-cog",
      onClick: () => openSettings(),
    },
  },
});
```

## Composer Customization

```tsx
const { control } = useChatKit({
  api: { /* ... */ },
  composer: {
    placeholder: "Ask me to manage your tasks...",
    tools: [
      {
        id: "tasks",
        label: "Tasks",
        shortLabel: "Tasks",
        icon: "list",
        placeholderOverride: "What task would you like to add?",
        pinned: true,
      },
      {
        id: "search",
        label: "Search",
        shortLabel: "Search",
        icon: "search",
        placeholderOverride: "Search your tasks...",
        pinned: true,
      },
    ],
    attachments: {
      enabled: false, // Enable if backend supports
      maxSize: 10 * 1024 * 1024, // 10MB
      maxCount: 3,
      accept: {
        "image/*": [".png", ".jpg", ".jpeg"],
        "application/pdf": [".pdf"],
      },
    },
  },
});
```

## Conversation History

```tsx
const { control } = useChatKit({
  api: { /* ... */ },
  history: {
    enabled: true,
    showDelete: true,
    showRename: true,
  },
});
```

## Embedding as Widget

For embedding the chatbot as a floating widget:

```tsx
"use client";

import { useState } from "react";
import { ChatKit, useChatKit } from "@openai/chatkit-react";

export function FloatingChatWidget() {
  const [isOpen, setIsOpen] = useState(false);

  const { control } = useChatKit({
    api: {
      url: "/api/chat",
      domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
    },
  });

  return (
    <>
      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-4 right-4 z-50 rounded-full bg-blue-600 p-4 text-white shadow-lg hover:bg-blue-700"
      >
        {isOpen ? "✕" : "💬"}
      </button>

      {/* Chat Widget */}
      {isOpen && (
        <div className="fixed bottom-20 right-4 z-50 h-[500px] w-[380px] overflow-hidden rounded-lg shadow-xl">
          <ChatKit control={control} className="h-full w-full" />
        </div>
      )}
    </>
  );
}
```

## Full Page Chat

```tsx
"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";

export default function ChatPage() {
  const { control } = useChatKit({
    api: {
      url: "/api/chat",
      domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
    },
    theme: {
      colorScheme: "light",
    },
    startScreen: {
      greeting: "Welcome! How can I help you today?",
    },
  });

  return (
    <div className="flex h-screen flex-col">
      <header className="border-b p-4">
        <h1 className="text-xl font-bold">Todo Chatbot</h1>
      </header>
      <main className="flex-1">
        <ChatKit control={control} className="h-full w-full" />
      </main>
    </div>
  );
}
```

## OpenAI Domain Allowlist Setup

For production deployment:

1. **Deploy frontend** to get production URL
2. **Add domain to OpenAI allowlist**:
   - Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
   - Click "Add domain"
   - Enter your frontend URL (without trailing slash)
3. **Get domain key** and add to env variables

**Note**: `localhost` typically works without domain allowlist configuration.

## Error Handling

```tsx
const { control, error, isLoading } = useChatKit({
  api: { /* ... */ },
});

if (error) {
  return <div>Error: {error.message}</div>;
}

if (isLoading) {
  return <div>Loading...</div>;
}
```

## Best Practices

1. **Use "use client"** - ChatKit requires client-side rendering
2. **Configure CORS** - Ensure backend allows frontend origin
3. **Inject auth tokens** - Use custom fetch for authenticated requests
4. **Handle errors** - Show user-friendly error states
5. **Customize theming** - Match your app's design system
6. **Use start screen prompts** - Guide users on what they can do
7. **Enable history** - Allow users to continue conversations
