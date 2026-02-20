---
name: tanstack-ai-vue-skilld
description: "ALWAYS use when writing code importing \"@tanstack/ai-vue\". Consult for debugging, best practices, or modifying @tanstack/ai-vue, tanstack/ai-vue, tanstack ai-vue, tanstack ai vue, ai."
metadata:
  version: 0.5.4
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# TanStack/ai `@tanstack/ai-vue`

**Version:** 0.5.4 (Feb 2026)
**Deps:** @tanstack/ai-client@0.4.5
**Tags:** latest: 0.5.4 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: Adapter functions split — v0.1.0 split monolithic adapters into activity-specific functions (e.g., `openaiText('gpt-4o')`, `openaiImage()`) to enable optimal tree-shaking [source](./references/docs/guides/migration.md)

- BREAKING: Options flattened — common parameters like `temperature`, `maxTokens`, and `topP` moved from nested `options` object to top-level configuration since v0.1.0 [source](./references/docs/guides/migration.md)

- BREAKING: `modelOptions` — `providerOptions` renamed to `modelOptions` in v0.1.0 for clarity; contains model-specific configurations and is fully type-safe [source](./references/docs/guides/migration.md)

- BREAKING: `toServerSentEventsStream` — `toResponseStream` renamed in v0.1.0; now returns a `ReadableStream` instead of a `Response`, requiring manual response creation [source](./references/docs/guides/migration.md)

- BREAKING: Embeddings removed — the `embedding()` function and associated adapters were removed in v0.1.0 to focus on chat and agentic workflows [source](./references/docs/guides/migration.md)

- NEW: `status` property — `useChat` added a `status` ref in v0.4.0 to track the generation lifecycle: `ready`, `submitted`, `streaming`, or `error` [source](./references/releases/@tanstack/ai-vue@0.4.0.md)

- NEW: Multimodal support — v0.5.0 introduced support for multiple modalities (images, audio, video, documents) via the `MultimodalContent` type in `sendMessage` [source](./references/releases/@tanstack/ai-vue@0.5.0.md)

- NEW: `agentLoopStrategy` — replaced `maxIterations` with a strategy pattern in v0.1.0, using helpers like `maxIterations(n)`, `untilFinishReason()`, or `combineStrategies()` [source](./references/releases/CHANGELOG.md)

- NEW: `chatCompletion()` — added in v0.1.0 for promise-based results without the automatic tool execution loop used by `chat()` [source](./references/releases/CHANGELOG.md)

- NEW: Tool Handling — `useChat` exposed `addToolResult` and `addToolApprovalResponse` for manual management of tool outputs and user approvals

- NEW: `toHttpStream` — introduced in v0.1.0 to support newline-delimited JSON (NDJSON) streaming as an alternative to Server-Sent Events [source](./references/docs/guides/migration.md)

- NEW: `fetchHttpStream` — connection adapter added to `@tanstack/ai-client` for consuming NDJSON streams in `useChat` [source](./references/releases/CHANGELOG.md)

- NEW: `geminiSpeech` (experimental) — experimental text-to-speech support for Google Gemini models added in v0.5.0 [source](./references/docs/guides/migration.md)

- NEW: Video generation (experimental) — experimental support for video generation via `openaiVideo` and `fal` adapters introduced in v0.1.0 [source](./references/docs/guides/video-generation.md)

**Also changed:** `standard-schema` support v0.2.0 · `useId` integration (Vue 3.5+) · `initialMessages` option · `ToolCallManager` class · `fetchServerSentEvents` adapter

## Best Practices

- Import specific activity and adapter functions instead of entire namespaces to ensure optimal tree-shaking and minimize bundle size [source](./references/docs/guides/tree-shaking.md)

```ts
// Preferred
import { chat } from '@tanstack/ai'
import { openaiText } from '@tanstack/ai-openai'

// Avoid - pulls in all activities and adapters
import * as ai from '@tanstack/ai'
```

- Use `toServerSentEventsResponse` on the server to automatically handle SSE headers, protocol framing, and the "[DONE]" termination chunk [source](./references/docs/guides/streaming.md)

```ts
export async function POST(req: Request) {
  const stream = chat({ adapter: openaiText('gpt-5.2'), messages })
  return toServerSentEventsResponse(stream)
}
```

- Prefer `fetchServerSentEvents` or `fetchHttpStream` connection adapters in `useChat` for built-in protocol parsing and state synchronization [source](./references/docs/guides/streaming.md)

- Define tools using `toolDefinition` with Zod schemas to enable full end-to-end TypeScript inference and runtime validation [source](./references/docs/guides/tools.md)

```ts
const getWeather = toolDefinition({
  name: 'get_weather',
  inputSchema: z.object({ city: z.string() }),
  outputSchema: z.object({ temp: z.number() })
})
```

- Use `.client()` implementations for browser-only operations and pass the base `toolDefinition` to the server `chat()` call to trigger automatic execution [source](./references/docs/guides/client-tools.md)

- Group client tools with `clientTools()` and `createChatClientOptions()` to enable precise type narrowing for tool names and schemas in `messages` [source](./references/docs/api/ai-client.md)

```ts
const tools = clientTools(uiTool.client(fn), storageTool.client(fn))
const options = createChatClientOptions({ connection, tools })
const { messages } = useChat(options) // messages parts are now narrowed!
```

- Pass the model name directly to the adapter factory to enable model-specific type safety and autocomplete for `modelOptions` [source](./references/docs/guides/per-model-type-safety.md)

```ts
// TypeScript enforces options supported only by gpt-5
const stream = chat({
  adapter: openaiText('gpt-5'),
  modelOptions: { text: { type: 'json_schema', ... } }
})
```

- Subscribe to `aiEventClient` with `{ withEventTarget: true }` in production to capture internal events for observability and timeline reconstruction [source](./references/docs/guides/observability.md)

- Pass all related tools to a single `chat()` call to allow the model to autonomously manage multi-step reasoning cycles (Agentic Cycle) [source](./references/docs/guides/agentic-cycle.md)

- Leverage Vue's reactivity by passing a reactive object to the `body` property of `useChat` to update request parameters without recreating the client

```ts
const model = ref('gpt-5.2')
const { sendMessage } = useChat({
  connection,
  body: computed(() => ({ model: model.value }))
})
```
