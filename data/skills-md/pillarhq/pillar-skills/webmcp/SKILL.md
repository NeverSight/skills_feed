---
name: webmcp
description: Implement WebMCP tools that expose web app functionality to AI agents via the W3C navigator.modelContext API. Use when adding WebMCP tools, registering browser-callable tools, exposing page functionality to AI agents, or building agentic web features.
---

# WebMCP Tools

Implement tools using the W3C WebMCP API (`navigator.modelContext`) so AI agents, browser assistants, and assistive technologies can call structured JavaScript functions on your page.

## When to Apply

Reference these guidelines when:

- Adding tools to a web page for browser AI agents
- Registering callable functions via `navigator.modelContext`
- Exposing existing page functionality to agents
- Building cooperative human-in-the-loop agent workflows

## Essential Rules

| Priority | Rule | Description |
|----------|------|-------------|
| CRITICAL | `tool-definition` | Every tool needs name, description, inputSchema, and execute |
| CRITICAL | `security` | Validate params, confirm destructive actions, don't leak sensitive data |
| HIGH | `descriptions` | Write specific descriptions — this is what the LLM reads to pick the tool |
| HIGH | `dynamic-registration` | Register/unregister tools as SPA state changes |
| MEDIUM | `user-interaction` | Use `agent.requestUserInteraction()` for purchases, deletions, and sends |

## Quick Reference

### 1. Register a Tool (CRITICAL)

```js
navigator.modelContext.registerTool({
  name: "add-to-cart",
  description: "Add a product to the shopping cart by ID",
  inputSchema: {
    type: "object",
    properties: {
      productId: { type: "string", description: "Product ID" },
      quantity: { type: "number", description: "How many to add (1-100)" }
    },
    required: ["productId"]
  },
  execute: async ({ productId, quantity }) => {
    await cartApi.add(productId, quantity ?? 1);
    return { content: [{ type: "text", text: `Added ${quantity ?? 1} to cart` }] };
  }
});
```

### 2. Feature Detection (CRITICAL)

```js
if ("modelContext" in navigator) {
  navigator.modelContext.registerTool({...});
}
```

### 3. Tool Descriptions (HIGH)

```js
// Good — specific, includes what it returns
description: "Search available flights. Returns {id, airline, price, departure, arrival}. Does not book — use book-flight to complete."

// Bad — vague
description: "Search flights"
```

### 4. User Confirmation (MEDIUM)

```js
execute: async ({ productId }, agent) => {
  const ok = await agent.requestUserInteraction(() =>
    confirm(`Buy product ${productId}?`)
  );
  if (!ok) throw new Error("Cancelled");
  await purchase(productId);
  return { content: [{ type: "text", text: "Purchased" }] };
}
```

### 5. Dynamic Registration for SPAs (HIGH)

```js
// React — register on mount, unregister on unmount
useEffect(() => {
  if (!("modelContext" in navigator)) return;
  navigator.modelContext.registerTool({ name: "edit-doc", ... });
  return () => navigator.modelContext.unregisterTool("edit-doc");
}, [doc.id]);
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/tool-definition.md
rules/descriptions.md
rules/security.md
rules/dynamic-registration.md
rules/user-interaction.md
```

For the complete guide with all patterns expanded: `AGENTS.md`
