---
name: opper-node-agents
description: >
  Use the Opper TypeScript Agent SDK (@opperai/agents) to build AI agents with think-act reasoning loops, tool use via createFunctionTool or @tool decorator, Zod schema validation, multi-agent composition, MCP integration, streaming, and hooks for observability. Activate when building TypeScript AI agents, autonomous systems, or tool-using reasoning loops with the Opper platform.
---

# Opper Node Agents

Build type-safe AI agents in TypeScript with think-act reasoning loops, Zod-validated tools, multi-agent composition, streaming, and full observability.

## Installation

```bash
npm install @opperai/agents
# or: pnpm add @opperai/agents / yarn add @opperai/agents
```

**Prerequisites:** Node.js 20+

Set your API key:

```bash
export OPPER_API_KEY="your-api-key"
```

Get your API key from [platform.opper.ai](https://platform.opper.ai).

## Core Pattern: Agent with Tools

Define tools with `createFunctionTool`, create an agent, and run it:

```typescript
import { Agent, createFunctionTool } from "@opperai/agents";
import { z } from "zod";

const getWeather = createFunctionTool(
  (input: { city: string }) => `The weather in ${input.city} is 22°C and sunny`,
  { name: "get_weather", schema: z.object({ city: z.string() }) },
);

const getPopulation = createFunctionTool(
  (input: { city: string }) => {
    const pops: Record<string, number> = { Paris: 2_161_000, London: 8_982_000 };
    return pops[input.city] ?? 0;
  },
  { name: "get_population", schema: z.object({ city: z.string() }) },
);

const agent = new Agent<string, { answer: string }>({
  name: "CityBot",
  instructions: "Help users with city information using available tools.",
  tools: [getWeather, getPopulation],
  outputSchema: z.object({ answer: z.string() }),
});

const { result, usage } = await agent.run("What's the weather and population of Paris?");
console.log(result.answer);
console.log(usage); // { requests, inputTokens, outputTokens, totalTokens }
```

## How the Agent Loop Works

The agent follows a Think-Act-Observe loop:

1. **Think**: The LLM analyzes the goal and available tools
2. **Act**: It selects and executes a tool with validated input
3. **Observe**: Results are added to the execution history
4. **Loop/Return**: Repeat until the goal is met, then return validated output

The loop runs up to `maxIterations` times (default: 25).

## Structured Output with Zod

Use Zod schemas for compile-time and runtime type safety:

```typescript
import { z } from "zod";

const CityReport = z.object({
  city: z.string(),
  temperature_c: z.number(),
  population: z.number(),
  summary: z.string().describe("One-sentence summary"),
});

type CityReportType = z.infer<typeof CityReport>;

const agent = new Agent<string, CityReportType>({
  name: "CityReporter",
  instructions: "Generate a city report using available tools.",
  tools: [getWeather, getPopulation],
  outputSchema: CityReport,
});

const { result } = await agent.run("Report on London");
// result is fully typed as CityReportType
console.log(result.city);          // "London"
console.log(result.temperature_c); // 18.0
```

## Model Selection

Specify which LLM the agent uses for reasoning:

```typescript
const agent = new Agent({
  name: "SmartAgent",
  instructions: "You are a helpful assistant.",
  tools: [myTool],
  model: "anthropic/claude-4-sonnet",
});

// With fallback chain
const agent = new Agent({
  name: "ResilientAgent",
  instructions: "You are a helpful assistant.",
  tools: [myTool],
  model: ["anthropic/claude-4-sonnet", "openai/gpt-4o"],
});
```

## Decorator-Based Tools

Use the class-based `@tool` decorator pattern:

```typescript
import { tool, extractTools } from "@opperai/agents";
import { z } from "zod";

class MathTools {
  @tool({ schema: z.object({ a: z.number(), b: z.number() }) })
  add({ a, b }: { a: number; b: number }) {
    return a + b;
  }

  @tool({ schema: z.object({ a: z.number(), b: z.number() }) })
  multiply({ a, b }: { a: number; b: number }) {
    return a * b;
  }
}

const tools = extractTools(new MathTools());
const agent = new Agent({
  name: "Calculator",
  instructions: "Use math tools to compute.",
  tools,
  outputSchema: z.object({ answer: z.number() }),
});
```

## Multi-Agent Composition

Use agents as tools within other agents:

```typescript
const mathAgent = new Agent<string, { answer: number }>({
  name: "MathAgent",
  instructions: "Solve math problems step by step.",
  tools: [add, multiply],
  outputSchema: z.object({ answer: z.number() }),
});

const researchAgent = new Agent<string, { answer: string }>({
  name: "ResearchAgent",
  instructions: "Answer factual questions.",
  tools: [searchWeb],
  outputSchema: z.object({ answer: z.string() }),
});

const coordinator = new Agent<string, string>({
  name: "Coordinator",
  instructions: "Delegate tasks to specialist agents.",
  tools: [mathAgent.asTool("math"), researchAgent.asTool("research")],
});

const { result, usage } = await coordinator.run("What is 15 * 23?");
// usage includes aggregated stats from child agents
```

## Streaming

Enable real-time token streaming:

```typescript
const agent = new Agent({
  name: "StreamingAgent",
  instructions: "Answer questions.",
  enableStreaming: true,
  outputSchema: z.object({ answer: z.string() }),
  onStreamStart: ({ callType }) => console.log(`[start] ${callType}`),
  onStreamChunk: ({ callType, accumulated }) => {
    if (callType === "final_result") {
      process.stdout.write(accumulated);
    }
  },
});

const { result } = await agent.run("Explain quantum computing");
```

## MCP Integration

Connect to MCP servers for external tools:

```typescript
import { mcp, MCPconfig, Agent } from "@opperai/agents";

const fsServer = MCPconfig({
  name: "filesystem",
  transport: "stdio",
  command: "npx",
  args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
});

const agent = new Agent<string, string>({
  name: "FileAgent",
  instructions: "Use filesystem tools to manage files.",
  tools: [mcp(fsServer)],
});
```

## Hooks

Monitor agent lifecycle events:

```typescript
import { HookEvents } from "@opperai/agents";

agent.registerHook(HookEvents.AgentStart, ({ context }) => {
  console.log(`Starting with goal: ${context.goal}`);
});

agent.registerHook(HookEvents.BeforeTool, ({ tool, input, toolCallId }) => {
  console.log(`[${toolCallId}] Calling ${tool.name}`);
});

agent.registerHook(HookEvents.AfterTool, ({ tool, result, record }) => {
  console.log(`[${record.id}] ${tool.name} returned: ${result.success}`);
});

agent.registerHook(HookEvents.AgentEnd, ({ context }) => {
  console.log(`Done. Tokens used: ${context.usage.totalTokens}`);
});
```

Tool hooks include a `toolCallId` to correlate `tool:before` with `tool:after`/`tool:error` events. See [references/HOOKS.md](references/HOOKS.md) for all events and payloads.

## Common Mistakes

- **Forgetting `await`**: `agent.run()` and `agent.process()` are async. Always use `await`.
- **Missing tool descriptions**: Tools need clear names and Zod schemas so the LLM knows when/how to use them.
- **Zod v4 incompatibility**: Use `zod@^3.23.8`. The SDK does not support Zod v4 yet.
- **No `outputSchema`**: Without it, the agent returns unstructured strings. Use Zod schemas for reliable typed output.
- **Too many tools**: Keep tools focused (5-10 per agent). Use composition for more capabilities.

## Additional Resources

- For hook events and payloads, see [references/HOOKS.md](references/HOOKS.md)
- For advanced tool patterns, see [references/TOOLS.md](references/TOOLS.md)
- For MCP server configuration, see [references/MCP.md](references/MCP.md)
- For multi-agent composition patterns, see [references/COMPOSITION.md](references/COMPOSITION.md)
- For streaming events and patterns, see [references/STREAMING.md](references/STREAMING.md)

## Related Skills

- **opper-node-sdk**: Use for single-shot task completion without agent loops — simpler when you don't need multi-step reasoning.
- **opper-python-agents**: Use when building agents in Python instead of TypeScript.

## Upstream Sources

If this skill's content is outdated, check the canonical sources:

- **Source code**: https://github.com/opper-ai/opperai-agent-sdk-node
- **Documentation**: https://docs.opper.ai
