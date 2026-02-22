---
name: convex-agents
description: Building AI agents and assistants with Convex. Use when implementing chat interfaces, AI assistants, tool-calling agents, RAG (retrieval-augmented generation), conversation threads, or integrating LLMs like OpenAI/Anthropic.
---

# Convex AI Agents

## Basic Chat Schema

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  threads: defineTable({
    userId: v.string(),
    title: v.optional(v.string()),
    createdAt: v.number(),
    updatedAt: v.number(),
  }).index("by_user", ["userId"]),

  messages: defineTable({
    threadId: v.id("threads"),
    role: v.union(v.literal("user"), v.literal("assistant"), v.literal("system")),
    content: v.string(),
    createdAt: v.number(),
  }).index("by_thread", ["threadId"]),
});
```

## Thread Management

```typescript
// convex/threads.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { ConvexError } from "convex/values";

export const create = mutation({
  args: {},
  returns: v.id("threads"),
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) {
      throw new ConvexError({ code: "UNAUTHENTICATED", message: "Not logged in" });
    }

    return await ctx.db.insert("threads", {
      userId: identity.subject,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    });
  },
});

export const list = query({
  args: {},
  returns: v.array(v.object({
    _id: v.id("threads"),
    title: v.optional(v.string()),
    updatedAt: v.number(),
  })),
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) return [];

    return await ctx.db
      .query("threads")
      .withIndex("by_user", (q) => q.eq("userId", identity.subject))
      .order("desc")
      .collect();
  },
});

export const getMessages = query({
  args: { threadId: v.id("threads") },
  returns: v.array(v.object({
    _id: v.id("messages"),
    role: v.union(v.literal("user"), v.literal("assistant"), v.literal("system")),
    content: v.string(),
    createdAt: v.number(),
  })),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_thread", (q) => q.eq("threadId", args.threadId))
      .order("asc")
      .collect();
  },
});
```

## AI Integration with Actions

```typescript
// convex/ai.ts
"use node";

import { internalAction, internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";
import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export const chat = internalAction({
  args: {
    threadId: v.id("threads"),
    userMessage: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Save user message
    await ctx.runMutation(internal.ai.saveMessage, {
      threadId: args.threadId,
      role: "user",
      content: args.userMessage,
    });

    // Get conversation history
    const messages = await ctx.runQuery(internal.ai.getHistory, {
      threadId: args.threadId,
    });

    // Call OpenAI
    const response = await openai.chat.completions.create({
      model: "gpt-4",
      messages: messages.map((m) => ({
        role: m.role,
        content: m.content,
      })),
    });

    const assistantMessage = response.choices[0]?.message?.content ?? "";

    // Save assistant response
    await ctx.runMutation(internal.ai.saveMessage, {
      threadId: args.threadId,
      role: "assistant",
      content: assistantMessage,
    });

    return null;
  },
});

export const saveMessage = internalMutation({
  args: {
    threadId: v.id("threads"),
    role: v.union(v.literal("user"), v.literal("assistant"), v.literal("system")),
    content: v.string(),
  },
  returns: v.id("messages"),
  handler: async (ctx, args) => {
    // Update thread timestamp
    await ctx.db.patch(args.threadId, { updatedAt: Date.now() });

    return await ctx.db.insert("messages", {
      threadId: args.threadId,
      role: args.role,
      content: args.content,
      createdAt: Date.now(),
    });
  },
});

export const getHistory = internalQuery({
  args: { threadId: v.id("threads") },
  returns: v.array(v.object({
    role: v.union(v.literal("user"), v.literal("assistant"), v.literal("system")),
    content: v.string(),
  })),
  handler: async (ctx, args) => {
    const messages = await ctx.db
      .query("messages")
      .withIndex("by_thread", (q) => q.eq("threadId", args.threadId))
      .order("asc")
      .collect();

    return messages.map((m) => ({ role: m.role, content: m.content }));
  },
});
```

## Streaming Responses

```typescript
// convex/ai.ts
"use node";

export const streamChat = internalAction({
  args: {
    threadId: v.id("threads"),
    userMessage: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Save user message
    await ctx.runMutation(internal.ai.saveMessage, {
      threadId: args.threadId,
      role: "user",
      content: args.userMessage,
    });

    // Create placeholder for assistant message
    const messageId = await ctx.runMutation(internal.ai.saveMessage, {
      threadId: args.threadId,
      role: "assistant",
      content: "",
    });

    // Get history
    const messages = await ctx.runQuery(internal.ai.getHistory, {
      threadId: args.threadId,
    });

    // Stream from OpenAI
    const stream = await openai.chat.completions.create({
      model: "gpt-4",
      messages: messages.slice(0, -1).map((m) => ({
        role: m.role,
        content: m.content,
      })),
      stream: true,
    });

    let fullContent = "";
    let lastUpdate = Date.now();

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content ?? "";
      fullContent += content;

      // Update every 500ms to avoid too many mutations
      if (Date.now() - lastUpdate > 500) {
        await ctx.runMutation(internal.ai.updateMessage, {
          messageId,
          content: fullContent,
        });
        lastUpdate = Date.now();
      }
    }

    // Final update
    await ctx.runMutation(internal.ai.updateMessage, {
      messageId,
      content: fullContent,
    });

    return null;
  },
});

export const updateMessage = internalMutation({
  args: { messageId: v.id("messages"), content: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(args.messageId, { content: args.content });
    return null;
  },
});
```

## Tool Calling / Function Calling

```typescript
// convex/ai.ts
"use node";

const tools = [
  {
    type: "function" as const,
    function: {
      name: "search_documents",
      description: "Search the knowledge base for relevant documents",
      parameters: {
        type: "object",
        properties: {
          query: { type: "string", description: "Search query" },
        },
        required: ["query"],
      },
    },
  },
  {
    type: "function" as const,
    function: {
      name: "create_task",
      description: "Create a new task for the user",
      parameters: {
        type: "object",
        properties: {
          title: { type: "string", description: "Task title" },
          dueDate: { type: "string", description: "Due date in ISO format" },
        },
        required: ["title"],
      },
    },
  },
];

export const chatWithTools = internalAction({
  args: { threadId: v.id("threads"), userMessage: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Save user message and get history...

    const response = await openai.chat.completions.create({
      model: "gpt-4",
      messages,
      tools,
    });

    const choice = response.choices[0];

    // Handle tool calls
    if (choice?.finish_reason === "tool_calls") {
      const toolCalls = choice.message.tool_calls ?? [];

      for (const toolCall of toolCalls) {
        const { name, arguments: argsJson } = toolCall.function;
        const toolArgs = JSON.parse(argsJson);

        let result: string;

        switch (name) {
          case "search_documents":
            result = await ctx.runAction(internal.search.query, {
              query: toolArgs.query,
            });
            break;
          case "create_task":
            await ctx.runMutation(internal.tasks.create, {
              title: toolArgs.title,
              dueDate: toolArgs.dueDate,
            });
            result = `Task "${toolArgs.title}" created.`;
            break;
          default:
            result = "Unknown tool";
        }

        // Continue conversation with tool result
        // ... (recursive call or message append)
      }
    }

    return null;
  },
});
```

## RAG (Retrieval-Augmented Generation)

### Vector Search Schema

```typescript
// convex/schema.ts
documents: defineTable({
  content: v.string(),
  embedding: v.array(v.float64()),
  metadata: v.object({
    source: v.string(),
    title: v.optional(v.string()),
  }),
}).vectorIndex("by_embedding", {
  vectorField: "embedding",
  dimensions: 1536,  // OpenAI ada-002
}),
```

### Embedding and Search

```typescript
// convex/search.ts
"use node";

import { internalAction, internalMutation, internalQuery } from "./_generated/server";
import { v } from "convex/values";
import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export const embed = internalAction({
  args: { text: v.string() },
  returns: v.array(v.float64()),
  handler: async (ctx, args) => {
    const response = await openai.embeddings.create({
      model: "text-embedding-ada-002",
      input: args.text,
    });
    return response.data[0].embedding;
  },
});

export const indexDocument = internalAction({
  args: { content: v.string(), source: v.string(), title: v.optional(v.string()) },
  returns: v.id("documents"),
  handler: async (ctx, args) => {
    const embedding = await ctx.runAction(internal.search.embed, {
      text: args.content,
    });

    return await ctx.runMutation(internal.search.saveDocument, {
      content: args.content,
      embedding,
      metadata: { source: args.source, title: args.title },
    });
  },
});

export const saveDocument = internalMutation({
  args: {
    content: v.string(),
    embedding: v.array(v.float64()),
    metadata: v.object({ source: v.string(), title: v.optional(v.string()) }),
  },
  returns: v.id("documents"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("documents", args);
  },
});

export const search = internalAction({
  args: { query: v.string(), limit: v.optional(v.number()) },
  returns: v.array(v.object({
    content: v.string(),
    score: v.number(),
  })),
  handler: async (ctx, args) => {
    const queryEmbedding = await ctx.runAction(internal.search.embed, {
      text: args.query,
    });

    const results = await ctx.runQuery(internal.search.vectorSearch, {
      embedding: queryEmbedding,
      limit: args.limit ?? 5,
    });

    return results;
  },
});

export const vectorSearch = internalQuery({
  args: { embedding: v.array(v.float64()), limit: v.number() },
  returns: v.array(v.object({ content: v.string(), score: v.number() })),
  handler: async (ctx, args) => {
    const results = await ctx.db
      .query("documents")
      .withSearchIndex("by_embedding", (q) =>
        q.vector(args.embedding).limit(args.limit)
      );

    return results.map((r) => ({
      content: r.content,
      score: r._score,
    }));
  },
});
```

### RAG Chat

```typescript
export const ragChat = internalAction({
  args: { threadId: v.id("threads"), userMessage: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Search for relevant documents
    const relevantDocs = await ctx.runAction(internal.search.search, {
      query: args.userMessage,
      limit: 3,
    });

    const context = relevantDocs.map((d) => d.content).join("\n\n");

    // Build system prompt with context
    const systemMessage = `You are a helpful assistant. Use the following context to answer questions:

${context}

If the context doesn't contain relevant information, say so.`;

    // Continue with chat completion...
  },
});
```

## Common Pitfalls

- **API keys in client** - Always use actions with `"use node"` for API calls
- **Long conversations** - Implement context windowing or summarization
- **Missing error handling** - Handle API rate limits and failures
- **No streaming fallback** - Have non-streaming backup for reliability
- **Unbounded context** - Limit message history sent to LLM

## References

- Actions: https://docs.convex.dev/functions/actions
- Vector Search: https://docs.convex.dev/search/vector-search
- Environment Variables: https://docs.convex.dev/production/environment-variables
