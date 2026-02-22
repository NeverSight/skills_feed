---
name: glove
description: Expert guide for building AI-powered applications with the Glove framework. Use when working with glove-core, glove-react, glove-next, tools, display stack, model adapters, stores, or any Glove example project.
---

# Glove Framework — Development Guide

You are an expert on the Glove framework. Use this knowledge when writing, debugging, or reviewing Glove code.

## What Glove Is

Glove is an open-source TypeScript framework for building AI-powered applications. Users describe what they want in conversation, and an AI decides which capabilities (tools) to invoke. Developers define tools and renderers; Glove handles the agent loop.

**Repository**: https://github.com/porkytheblack/glove
**Docs site**: https://glove.dterminal.net
**License**: MIT (dterminal)

## Package Overview

| Package | Purpose | Install |
|---------|---------|---------|
| `glove-core` | Runtime engine: agent loop, tool execution, display manager, model adapters, stores | `pnpm add glove-core` |
| `glove-react` | React hooks (`useGlove`), `GloveClient`, `GloveProvider`, `defineTool`, `<Render>`, `MemoryStore`, `ToolConfig` with colocated renderers | `pnpm add glove-react` |
| `glove-next` | One-line Next.js API route handler (`createChatHandler`) for streaming SSE | `pnpm add glove-next` |

**Most projects need just `glove-react` + `glove-next`.** `glove-core` is included as a dependency of `glove-react`.

## Architecture at a Glance

```
User message → Agent Loop → Model decides tool calls → Execute tools → Feed results back → Loop until done
                                                          ↓
                                                   Display Stack (pushAndWait / pushAndForget)
                                                          ↓
                                                   React renders UI slots
```

### Core Concepts

- **Agent** — AI coordinator that replaces router/navigation logic. Reads tools, decides which to call.
- **Tool** — A capability: name, description, inputSchema (Zod), `do` function, optional `render` + `renderResult`.
- **Display Stack** — Stack of UI slots tools push onto. `pushAndWait` blocks tool; `pushAndForget` doesn't.
- **Display Strategy** — Controls slot visibility lifecycle: `"stay"`, `"hide-on-complete"`, `"hide-on-new"`.
- **renderData** — Client-only data returned from `do()` that is NOT sent to the AI model. Used by `renderResult` for history rendering.
- **Adapter** — Pluggable interfaces for Model, Store, DisplayManager, and Subscriber. Swap providers without changing app code.
- **Context Compaction** — Auto-summarizes long conversations to stay within context window limits. The store preserves full message history (so frontends can display the entire chat), while `Context.getMessages()` splits at the last compaction summary so the model only sees post-compaction context. Summary messages are marked with `is_compaction: true`.

## Quick Start (Next.js)

### 1. Install

```bash
pnpm add glove-core glove-react glove-next zod
```

### 2. Server route

```typescript
// app/api/chat/route.ts
import { createChatHandler } from "glove-next";

export const POST = createChatHandler({
  provider: "anthropic",     // or "openai", "openrouter", "gemini", etc.
  model: "claude-sonnet-4-20250514",
});
```

Set `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`, etc.) in `.env.local`.

### 3. Define tools with `defineTool`

```tsx
// lib/glove.tsx
import { GloveClient, defineTool } from "glove-react";
import type { ToolConfig } from "glove-react";
import { z } from "zod";

const inputSchema = z.object({
  question: z.string().describe("The question to display"),
  options: z.array(z.object({
    label: z.string().describe("Display text"),
    value: z.string().describe("Value returned when selected"),
  })),
});

const askPreferenceTool = defineTool({
  name: "ask_preference",
  description: "Present options for the user to choose from.",
  inputSchema,
  displayPropsSchema: inputSchema,       // Zod schema for display props
  resolveSchema: z.string(),             // Zod schema for resolve value
  displayStrategy: "hide-on-complete",   // Hide slot after user responds
  async do(input, display) {
    const selected = await display.pushAndWait(input);  // typed!
    return {
      status: "success" as const,
      data: `User selected: ${selected}`,         // sent to AI
      renderData: { question: input.question, selected },  // client-only
    };
  },
  render({ props, resolve }) {           // typed props, typed resolve
    return (
      <div>
        <p>{props.question}</p>
        {props.options.map(opt => (
          <button key={opt.value} onClick={() => resolve(opt.value)}>
            {opt.label}
          </button>
        ))}
      </div>
    );
  },
  renderResult({ data }) {               // renders from history
    const { question, selected } = data as { question: string; selected: string };
    return <div><p>{question}</p><span>Selected: {selected}</span></div>;
  },
});

// Tools without display stay as raw ToolConfig
const getDateTool: ToolConfig = {
  name: "get_date",
  description: "Get today's date",
  inputSchema: z.object({}),
  async do() { return { status: "success", data: new Date().toLocaleDateString() }; },
};

export const gloveClient = new GloveClient({
  endpoint: "/api/chat",
  systemPrompt: "You are a helpful assistant.",
  tools: [askPreferenceTool, getDateTool],
});
```

### 4. Provider + Render

```tsx
// app/providers.tsx
"use client";
import { GloveProvider } from "glove-react";
import { gloveClient } from "@/lib/glove";

export function Providers({ children }: { children: React.ReactNode }) {
  return <GloveProvider client={gloveClient}>{children}</GloveProvider>;
}
```

```tsx
// app/page.tsx — using <Render> component
"use client";
import { useGlove, Render } from "glove-react";

export default function Chat() {
  const glove = useGlove();

  return (
    <Render
      glove={glove}
      strategy="interleaved"
      renderMessage={({ entry }) => (
        <div><strong>{entry.kind === "user" ? "You" : "AI"}:</strong> {entry.text}</div>
      )}
      renderStreaming={({ text }) => <div style={{ opacity: 0.7 }}>{text}</div>}
    />
  );
}
```

Or use `useGlove()` directly for full manual control:

```tsx
// app/page.tsx — manual rendering
"use client";
import { useState } from "react";
import { useGlove } from "glove-react";

export default function Chat() {
  const { timeline, streamingText, busy, slots, sendMessage, renderSlot, renderToolResult } = useGlove();
  const [input, setInput] = useState("");

  return (
    <div>
      {timeline.map((entry, i) => (
        <div key={i}>
          {entry.kind === "user" && <p><strong>You:</strong> {entry.text}</p>}
          {entry.kind === "agent_text" && <p><strong>AI:</strong> {entry.text}</p>}
          {entry.kind === "tool" && (
            <>
              <p>Tool: {entry.name} — {entry.status}</p>
              {entry.renderData !== undefined && renderToolResult(entry)}
            </>
          )}
        </div>
      ))}
      {streamingText && <p style={{ opacity: 0.7 }}>{streamingText}</p>}
      {slots.map(renderSlot)}
      <form onSubmit={(e) => { e.preventDefault(); sendMessage(input.trim()); setInput(""); }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} disabled={busy} />
        <button type="submit" disabled={busy}>Send</button>
      </form>
    </div>
  );
}
```

## Display Stack Patterns

### pushAndForget — Show results (non-blocking)

```tsx
async do(input, display) {
  const data = await fetchData(input);
  await display.pushAndForget({ input: data }); // Shows UI, tool continues
  return { status: "success", data: "Displayed results", renderData: data };
},
render({ data }) {
  return <Card>{data.title}</Card>;
},
renderResult({ data }) {
  return <Card>{(data as any).title}</Card>;  // Same card from history
},
```

### pushAndWait — Collect user input (blocking)

```tsx
async do(input, display) {
  const confirmed = await display.pushAndWait({ input }); // Pauses until user responds
  return {
    status: "success",
    data: confirmed ? "Confirmed" : "Cancelled",
    renderData: { confirmed },
  };
},
render({ data, resolve }) {
  return (
    <div>
      <p>{data.message}</p>
      <button onClick={() => resolve(true)}>Yes</button>
      <button onClick={() => resolve(false)}>No</button>
    </div>
  );
},
renderResult({ data }) {
  const { confirmed } = data as { confirmed: boolean };
  return <div>{confirmed ? "Confirmed" : "Cancelled"}</div>;
},
```

### Display Strategies

| Strategy | Behavior | Use for |
|----------|----------|---------|
| `"stay"` (default) | Slot always visible | Info cards, results |
| `"hide-on-complete"` | Hidden when slot is resolved | Forms, confirmations, pickers |
| `"hide-on-new"` | Hidden when newer slot from same tool appears | Cart summaries, status panels |

### SlotRenderProps

| Prop | Type | Description |
|------|------|-------------|
| `data` | `T` | Input passed to pushAndWait/pushAndForget |
| `resolve` | `(value: unknown) => void` | Resolves the slot. For pushAndWait, the value returns to `do`. For pushAndForget, use `resolve()` or `removeSlot(id)` to dismiss. |
| `reject` | `(reason?: string) => void` | Rejects the slot. For pushAndWait, this causes the promise to reject. Use for cancellation flows. |

## Tool Definition

### `defineTool` (recommended for tools with UI)

```typescript
import { defineTool } from "glove-react";

const tool = defineTool({
  name: string,
  description: string,
  inputSchema: z.ZodType,              // Zod schema for tool input
  displayPropsSchema?: z.ZodType,      // Zod schema for display props (recommended for tools with UI)
  resolveSchema?: z.ZodType,           // Zod schema for resolve value (omit for pushAndForget-only)
  displayStrategy?: SlotDisplayStrategy,
  requiresPermission?: boolean,
  unAbortable?: boolean,                 // Tool runs to completion even if abort signal fires (e.g. voice barge-in)
  do(input, display): Promise<ToolResultData>,  // display is TypedDisplay<D, R>
  render?({ props, resolve, reject }): ReactNode,
  renderResult?({ data, output, status }): ReactNode,
});
```

**Key points:**
- `do()` should return `{ status, data, renderData }` — `data` goes to model, `renderData` stays client-only
- `render()` gets typed `props` (matching displayPropsSchema) and typed `resolve` (matching resolveSchema)
- `renderResult()` receives `renderData` for showing read-only views from history
- `displayPropsSchema` is optional but recommended — tools without display should use raw `ToolConfig`

### `ToolConfig` (for tools without UI or manual control)

```typescript
interface ToolConfig<I = any> {
  name: string;
  description: string;
  inputSchema: z.ZodType<I>;
  do: (input: I, display: ToolDisplay) => Promise<ToolResultData>;
  render?: (props: SlotRenderProps) => ReactNode;
  renderResult?: (props: ToolResultRenderProps) => ReactNode;
  displayStrategy?: SlotDisplayStrategy;
  requiresPermission?: boolean;
  unAbortable?: boolean;
}
```

### ToolResultData

```typescript
interface ToolResultData {
  status: "success" | "error";
  data: unknown;          // Sent to the AI model
  message?: string;       // Error message (for status: "error")
  renderData?: unknown;   // Client-only — NOT sent to model, used by renderResult
}
```

**Important:** Model adapters explicitly strip `renderData` before sending to the AI. This makes it safe to store sensitive client-only data (e.g., email addresses, UI state) in `renderData`.

## `<Render>` Component

Headless render component that replaces manual timeline rendering:

```tsx
import { Render } from "glove-react";

<Render
  glove={gloveHandle}           // return value of useGlove()
  strategy="interleaved"        // "interleaved" | "slots-before" | "slots-after" | "slots-only"
  renderMessage={({ entry, index, isLast }) => ...}
  renderToolStatus={({ entry, index, hasSlot }) => ...}
  renderStreaming={({ text }) => ...}
  renderInput={({ send, busy, abort }) => ...}
  renderSlotContainer={({ slots, renderSlot }) => ...}
  as="div"                      // wrapper element
  className="chat"
/>
```

**Features:**
- Automatic slot visibility based on `displayStrategy`
- Automatic `renderResult` rendering for completed tools with `renderData`
- Interleaving: slots appear inline next to their tool call
- Sensible defaults for all render props

## `GloveHandle` Interface

The interface consumed by `<Render>`, returned by `useGlove()`:

```typescript
interface GloveHandle {
  timeline: TimelineEntry[];
  streamingText: string;
  busy: boolean;
  slots: EnhancedSlot[];
  sendMessage: (text: string, images?: { data: string; media_type: string }[]) => void;
  abort: () => void;
  renderSlot: (slot: EnhancedSlot) => ReactNode;
  renderToolResult: (entry: ToolEntry) => ReactNode;
  resolveSlot: (slotId: string, value: unknown) => void;
  rejectSlot: (slotId: string, reason?: string) => void;
}
```

## useGlove Hook Return

| Property | Type | Description |
|----------|------|-------------|
| `timeline` | `TimelineEntry[]` | Messages + tool calls |
| `streamingText` | `string` | Current streaming buffer |
| `busy` | `boolean` | Agent is processing |
| `slots` | `EnhancedSlot[]` | Active display stack with metadata |
| `tasks` | `Task[]` | Agent task list |
| `stats` | `GloveStats` | `{ turns, tokens_in, tokens_out }` |
| `sendMessage(text, images?)` | `void` | Send user message |
| `abort()` | `void` | Cancel current request |
| `renderSlot(slot)` | `ReactNode` | Render a display slot |
| `renderToolResult(entry)` | `ReactNode` | Render a tool result from history |
| `resolveSlot(id, value)` | `void` | Resolve a pushAndWait slot |
| `rejectSlot(id, reason?)` | `void` | Reject a pushAndWait slot |

## TimelineEntry

```typescript
type TimelineEntry =
  | { kind: "user"; text: string; images?: string[] }
  | { kind: "agent_text"; text: string }
  | { kind: "tool"; id: string; name: string; input: unknown; status: "running" | "success" | "error"; output?: string; renderData?: unknown };

type ToolEntry = Extract<TimelineEntry, { kind: "tool" }>;
```

## Supported Providers

| Provider | Env Variable | Default Model | SDK Format |
|----------|-------------|---------------|------------|
| `openai` | `OPENAI_API_KEY` | `gpt-4.1` | openai |
| `anthropic` | `ANTHROPIC_API_KEY` | `claude-sonnet-4-20250514` | anthropic |
| `openrouter` | `OPENROUTER_API_KEY` | `anthropic/claude-sonnet-4` | openai |
| `gemini` | `GEMINI_API_KEY` | `gemini-2.5-flash` | openai |
| `minimax` | `MINIMAX_API_KEY` | `MiniMax-M2.5` | openai |
| `kimi` | `MOONSHOT_API_KEY` | `kimi-k2.5` | openai |
| `glm` | `ZHIPUAI_API_KEY` | `glm-4-plus` | openai |

## Pre-built Tool Registry

Available at https://glove.dterminal.net/tools — copy-paste into your project:

- `confirm_action` — Yes/No confirmation dialog
- `collect_form` — Multi-field form
- `ask_preference` — Single-select preference picker
- `text_input` — Free-text input
- `show_info_card` — Info/success/warning card (pushAndForget)
- `suggest_options` — Multiple-choice suggestions
- `approve_plan` — Step-by-step plan approval

## Voice Integration (`glove-voice`)

### Package Overview

| Package | Purpose | Install |
|---------|---------|---------|
| `glove-voice` | Voice pipeline: `GloveVoice`, adapters (STT/TTS/VAD), `AudioCapture`, `AudioPlayer` | `pnpm add glove-voice` |
| `glove-react/voice` | React hook: `useGloveVoice` | Included in `glove-react` |
| `glove-next` | Token handlers: `createVoiceTokenHandler` (already in `glove-next`, no separate import) | Included in `glove-next` |

### Architecture

```
Mic → VAD → STTAdapter → glove.processRequest() → TTSAdapter → Speaker
```

`GloveVoice` wraps a Glove instance with a full-duplex voice pipeline. Glove remains the intelligence layer — all tools, display stack, and context management work normally. STT and TTS are swappable adapters. Text tokens stream through a `SentenceBuffer` into TTS in real-time.

### Quick Start (Next.js + ElevenLabs)

**Step 1: Token routes** — server-side handlers that exchange your API key for short-lived tokens

```typescript
// app/api/voice/stt-token/route.ts
import { createVoiceTokenHandler } from "glove-next";
export const GET = createVoiceTokenHandler({ provider: "elevenlabs", type: "stt" });
```

```typescript
// app/api/voice/tts-token/route.ts
import { createVoiceTokenHandler } from "glove-next";
export const GET = createVoiceTokenHandler({ provider: "elevenlabs", type: "tts" });
```

Set `ELEVENLABS_API_KEY` in `.env.local`.

**Step 2: Client voice config**

```typescript
// app/lib/voice.ts
import { createElevenLabsAdapters } from "glove-voice";

async function fetchToken(path: string): Promise<string> {
  const res = await fetch(path);
  const data = await res.json();
  return data.token;
}

export const { stt, createTTS } = createElevenLabsAdapters({
  getSTTToken: () => fetchToken("/api/voice/stt-token"),
  getTTSToken: () => fetchToken("/api/voice/tts-token"),
  voiceId: "JBFqnCBsd6RMkjVDRZzb",
});
```

**Step 3: SileroVAD** — dynamic import for SSR safety

```typescript
export async function createSileroVAD() {
  const { SileroVADAdapter } = await import("glove-voice/silero-vad");
  const vad = new SileroVADAdapter({
    positiveSpeechThreshold: 0.5,
    negativeSpeechThreshold: 0.35,
    wasm: { type: "cdn" },
  });
  await vad.init();
  return vad;
}
```

**Step 4: React hook**

```tsx
const { runnable } = useGlove({ tools, sessionId });
const voice = useGloveVoice({ runnable, voice: { stt, createTTS, vad } });
// voice.mode: "idle" | "listening" | "thinking" | "speaking"
// voice.start(), voice.stop(), voice.interrupt(), voice.commitTurn()
```

### Turn Modes

| Mode | Behavior | Use for |
|------|----------|---------|
| `"vad"` (default) | Auto speech detection + barge-in | Hands-free, voice-first apps |
| `"manual"` | Push-to-talk, explicit `commitTurn()` | Noisy environments, precise control |

### Voice-First Tool Design

- **Use `pushAndForget` instead of `pushAndWait`** — blocking tools that wait for clicks are unusable in voice mode
- **Return descriptive text in `data`** — the LLM reads it to formulate spoken responses
- **Add a voice-specific system prompt** — instruct the agent to narrate results concisely

### Supported Voice Providers

| Provider | Token Handler Config | Env Variable |
|----------|---------------------|--------------|
| ElevenLabs | `{ provider: "elevenlabs", type: "stt" \| "tts" }` | `ELEVENLABS_API_KEY` |
| Deepgram | `{ provider: "deepgram" }` | `DEEPGRAM_API_KEY` |
| Cartesia | `{ provider: "cartesia" }` | `CARTESIA_API_KEY` |

## Supporting Files

For detailed API reference, see [api-reference.md](api-reference.md).
For example patterns from real implementations, see [examples.md](examples.md).

## Common Gotchas

1. **model_response_complete vs model_response**: Streaming adapters emit `model_response_complete`, not `model_response`. Subscribers must handle both.
2. **Closure capture in React hooks**: When re-keying sessions, use mutable `let currentKey = key` to avoid stale closures.
3. **React useEffect timing**: State updates don't take effect in the same render cycle — guard with early returns.
4. **Browser-safe imports**: `glove-core` barrel exports include native deps (better-sqlite3). For browser code, import from subpaths: `glove-core/core`, `glove-core/glove`, `glove-core/display-manager`, `glove-core/tools/task-tool`.
5. **`Displaymanager` casing**: The concrete class is `Displaymanager` (lowercase 'm'), not `DisplayManager`. Import it as: `import { Displaymanager } from "glove-core/display-manager"`.
6. **`createAdapter` stream default**: `stream` defaults to `true`, not `false`. Pass `stream: false` explicitly if you want synchronous responses.
7. **Tool return values**: The `do` function should return `ToolResultData` with `{ status, data, renderData? }`. `data` goes to the AI; `renderData` stays client-only.
8. **Zod .describe()**: Always add `.describe()` to schema fields — the AI reads these descriptions to understand what to provide.
9. **displayPropsSchema is optional but recommended**: `defineTool`'s `displayPropsSchema` is optional, but recommended for tools with display UI — tools without display should use raw `ToolConfig` instead.
10. **renderData is stripped by model adapters**: Model adapters explicitly exclude `renderData` when formatting tool results for the AI, so it's safe for client-only data.
11. **SileroVAD must use dynamic import**: Never import `glove-voice/silero-vad` at module level in Next.js/SSR. Use `await import("glove-voice/silero-vad")` to avoid pulling WASM into the server bundle.
12. **Next.js transpilePackages**: Add `"glove-voice"` to `transpilePackages` in `next.config.ts` so Next.js processes the ES module.
13. **createTTS must be a factory**: `GloveVoice` calls it once per turn to get a fresh TTS adapter. Pass `() => new ElevenLabsTTSAdapter(...)`, not a single instance.
14. **Barge-in protection requires `unAbortable`**: A `pushAndWait` resolver suppresses voice barge-in at the trigger level (GloveVoice skips `interrupt()` when `resolverStore.size > 0`). But that alone doesn't protect the tool — if `interrupt()` is called by other means, only `unAbortable: true` on the tool guarantees it runs to completion despite the abort signal. Use both together for mutation-critical tools like checkout. Use `pushAndForget` for voice-first tools.
15. **Empty committed transcripts**: ElevenLabs Scribe may return empty committed transcripts for short utterances. The adapter auto-falls back to the last partial transcript.
16. **TTS idle timeout**: ElevenLabs TTS WebSocket disconnects after ~20s idle. GloveVoice handles this by closing TTS after each model_response_complete and opening a fresh session on next text_delta.
17. **onnxruntime-web build warnings**: `Critical dependency: require function is used in a way...` warnings from onnxruntime-web are expected and harmless.
18. **Audio sample rate**: All adapters must agree on 16kHz mono PCM (the default). Don't change unless your provider explicitly requires something different.
