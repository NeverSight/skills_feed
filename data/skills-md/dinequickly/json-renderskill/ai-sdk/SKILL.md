---
name: ai-sdk
description: Build or refactor apps using the Vercel AI SDK (core or RSC). Use when implementing tool calling, returning JSON for UI rendering, mapping tool outputs to React components, or streaming UI with @ai-sdk/rsc in Next.js App Router.
---

# AI SDK UI Rendering

## Overview
Use this skill to turn AI SDK tool calls into UI components, either by rendering on the client from tool outputs or streaming UI from the server with RSC.

## Quick Decision
- Use client-side rendering when you already receive message parts on the client and want a simple mapping from tool outputs to components.
- Use server-side streaming (RSC) when you want the server to render components during tool execution and stream them to the client.

## Task: Return JSON from tools for UI
1. Define a tool with a clear input schema and return a JSON object that matches the UI props.
2. Keep outputs serializable (no functions, Dates, or class instances).
3. If multiple tools share a UI pattern, normalize output shape or add a `kind` field.

Example:
```tsx
const result = await generateText({
  model,
  prompt,
  tools: {
    getWeather: {
      description: 'Get the weather for a location',
      inputSchema: z.object({
        city: z.string(),
        unit: z.enum(['C', 'F']),
      }),
      execute: async ({ city, unit }) => {
        const weather = getWeather({ city, unit });
        return {
          temperature: weather.temperature,
          unit,
          description: weather.description,
          forecast: weather.forecast,
        };
      },
    },
  },
});
```

## Task: Client-side mapping from tool outputs to components
1. Iterate message parts.
2. Guard on `part.state === 'output-available'`.
3. Map `part.type` (tool name) to the right component.

Example:
```tsx
const renderers: Record<string, (output: any) => JSX.Element> = {
  'tool-getWeather': output => (
    <WeatherCard weather={output} />
  ),
  'tool-searchCourses': output => (
    <Courses courses={output} />
  ),
};

return messages.map(message => (
  <div key={message.id}>
    {message.parts.map(part => {
      if (part.state !== 'output-available') return null;
      if (part.type === 'text') return <div>{part.text}</div>;
      const render = renderers[part.type];
      return render ? render(part.output) : null;
    })}
  </div>
));
```

## Task: Server-side UI streaming with RSC
1. Create a UI stream with `createStreamableUI`.
2. In a tool `execute`, render a component and call `uiStream.done(...)`.
3. Return `uiStream.value` from the server action and render it directly on the client.

Example:
```tsx
import { createStreamableUI } from '@ai-sdk/rsc';

const uiStream = createStreamableUI();

await generateText({
  model,
  prompt,
  tools: {
    getWeather: {
      description: 'Get the weather for a location',
      inputSchema: z.object({
        city: z.string(),
        unit: z.enum(['C', 'F']),
      }),
      execute: async ({ city, unit }) => {
        const weather = getWeather({ city, unit });
        uiStream.done(<WeatherCard weather={weather} />);
      },
    },
  },
});

return { display: uiStream.value };
```

Client render:
```tsx
return (
  <div>
    {messages.map(message => (
      <div key={message.id}>{message.display}</div>
    ))}
  </div>
);
```

## Multi-tool UI scaling
- Prefer a registry map over large switch statements.
- Normalize tool outputs or include a `kind` field for shared components.
- For multi-step tool chains, keep the UI stream open until the final result is ready.

## References
- See `references/ui-rendering.md` for patterns, edge cases, and suggested message-part helpers.

## Resources
### references/
- `references/ui-rendering.md`: patterns for tool output shapes, part rendering helpers, and streaming guidance.
