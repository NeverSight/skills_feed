---
name: google-adk-typescript
description: >
  Build production-ready AI agents in TypeScript using Google Agent Development Kit (ADK).
  Use when creating agentic TypeScript/JavaScript applications with LlmAgent, workflow agents
  (SequentialAgent, ParallelAgent, LoopAgent), custom agents (BaseAgent with runAsyncImpl),
  FunctionTool with Zod schemas, MCP and OpenAPI tools, multi-agent orchestration,
  session and state management (outputKey, app/user/temp prefixes, CallbackContext),
  callbacks and guardrails, testing and evaluation, backend frameworks (Express, Hono),
  or deploying to Cloud Run or containers.
  Triggers on "build an agent TypeScript", "ADK TypeScript", "ADK TS", "@google/adk",
  "multi-agent system TypeScript", "agentic application TypeScript", "Gemini agent TypeScript".
---

# Google Agent Development Kit (ADK) - TypeScript

ADK is Google's open-source, code-first TypeScript framework for building, evaluating, and deploying AI agents. Optimized for Gemini but model-agnostic. Requires Node.js 20.12.7+.

## Quick Start

```bash
mkdir my-agent && cd my-agent
npm init -y
npm install @google/adk
npm install @google/adk-devtools
npm install -D typescript
npm install zod
npx tsc --init
```

**Project structure:**
```
my-agent/
├── agent.ts
├── package.json
├── tsconfig.json
└── .env
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "verbatimModuleSyntax": false
  }
}
```

**.env:**
```bash
GOOGLE_GENAI_API_KEY=your_api_key
# Or use GEMINI_API_KEY=your_api_key (also supported)
# Or for Vertex AI:
# GOOGLE_GENAI_USE_VERTEXAI=TRUE
# GOOGLE_CLOUD_PROJECT=your_project
# GOOGLE_CLOUD_LOCATION=us-central1
```

**Minimal agent (agent.ts):**
```typescript
import { LlmAgent } from '@google/adk';

export const rootAgent = new LlmAgent({
  name: 'assistant',
  model: 'gemini-2.5-flash',
  instruction: 'You are a helpful assistant.',
  description: 'A general-purpose assistant.',
});
```

**Run:**
```bash
npx @google/adk-devtools run agent.ts    # CLI
npx @google/adk-devtools web             # Dev UI at localhost:8000
```

## Agent Types

| Type | Import | Use When |
|------|--------|----------|
| `LlmAgent` | `@google/adk` | Flexible reasoning, tool selection |
| `SequentialAgent` | `@google/adk` | Ordered multi-step pipelines |
| `ParallelAgent` | `@google/adk` | Concurrent independent tasks |
| `LoopAgent` | `@google/adk` | Iterative refinement |
| `BaseAgent` | `@google/adk` | Custom orchestration logic |

See [references/agents.md](references/agents.md) for detailed patterns and code examples.

## Tools

Define tools with `FunctionTool` and Zod schemas:

```typescript
import { FunctionTool, LlmAgent } from '@google/adk';
import { z } from 'zod';

const getWeather = new FunctionTool({
  name: 'get_weather',
  description: 'Get weather for a city.',
  parameters: z.object({
    city: z.string().describe('City name'),
  }),
  execute: async ({ city }) => {
    return { city, temp: '72F', condition: 'sunny' };
  },
});

export const rootAgent = new LlmAgent({
  name: 'weather_agent',
  model: 'gemini-2.5-flash',
  instruction: 'Help users check weather.',
  tools: [getWeather],
});
```

See [references/tools.md](references/tools.md) for MCP, OpenAPI, LongRunningFunctionTool, and built-in tools.

## Multi-Agent Orchestration

**Six core patterns:**

1. **Coordinator/Dispatcher** - Central LlmAgent routes to specialist sub-agents
2. **Sequential Pipeline** - SequentialAgent chains agents with `outputKey` state passing
3. **Parallel Fan-Out** - ParallelAgent for concurrent work, then aggregate
4. **Hierarchical Decomposition** - Tree of delegating agents
5. **Generator-Critic** - Create then review with SequentialAgent
6. **Iterative Refinement** - LoopAgent until quality threshold or `maxIterations`

See [references/multi-agent.md](references/multi-agent.md) for implementation details.

## State Management

```typescript
// 1. outputKey - auto-save agent response to state
const writer = new LlmAgent({
  name: 'writer',
  outputKey: 'draft',  // state['draft'] = agent response
  // ...
});

// 2. Instruction templating - read from state
const editor = new LlmAgent({
  instruction: 'Edit this draft: {draft}',
  // ...
});

// 3. CallbackContext - manual read/write
function myCallback(context: CallbackContext) {
  const count = context.state.get('counter', 0);
  context.state.set('counter', count + 1);
  context.state.set('temp:scratch', 'temporary');
}
```

**State prefixes:** unprefixed (session), `user:` (cross-session per user), `app:` (global), `temp:` (discarded after invocation).

## Callbacks & Guardrails

```typescript
const agent = new LlmAgent({
  name: 'safe_agent',
  beforeAgentCallback: checkIfAgentShouldRun,
  afterAgentCallback: modifyOutputAfterAgent,
  beforeModelCallback: simpleBeforeModelModifier,
  // Also: afterModelCallback, beforeToolCallback, afterToolCallback
});
```

Return `undefined` to proceed, return a Content/LlmResponse object to override. See [references/callbacks.md](references/callbacks.md).

## Session & Runner

```typescript
import { InMemoryRunner } from '@google/adk';
import { createUserContent } from '@google/genai';

const runner = new InMemoryRunner({ agent: rootAgent });
const session = await runner.sessionService.createSession({
  appName: runner.appName,
  userId: 'user-1',
  state: { initial_key: 'value' },
});

for await (const event of runner.runAsync({
  userId: session.userId,
  sessionId: session.id,
  newMessage: createUserContent('Hello'),
})) {
  console.log(event);
}
```

**Note:** `createUserContent` and the `Content` type come from `@google/genai` (transitive dependency of `@google/adk`), not from `@google/adk` directly.

## Testing & Evaluation

ADK provides trajectory-based evaluation comparing actual agent behavior against expected tool call sequences and reference responses. A recommended best practice is to follow a **task-first approach**:

1. **Identify tasks/intents** - Map every user intent the agent handles, with tools involved
2. **Map trajectories** - For each task, define happy paths and failure trajectories (not found, not eligible, tool errors, ambiguous input)
3. **Select evals** - Use all 9 built-in metrics as baseline, then construct custom rubrics per task category
4. **Test in layers** - Unit tests (mocked tools/sub-agents) → integration tests (real LLM) → simulated scenario tests (multi-turn personas)

**Built-in metrics:** `tool_trajectory_avg_score`, `response_match_score`, `final_response_match_v2`, `rubric_based_final_response_quality_v1`, `rubric_based_tool_use_quality_v1`, `hallucinations_v1`, `safety_v1`

**Run:** `npx adk eval <agent_folder> <test_file.test.json>`

See [references/testing.md](references/testing.md) for task-first strategy, rubric construction, mocked unit tests, integration tests, and simulated scenario tests.

## Backend Integrations

### Express

```typescript
import express from 'express';
import { InMemoryRunner, isFinalResponse, stringifyContent } from '@google/adk';
import { createUserContent } from '@google/genai';

const app = express();
app.use(express.json());
const runner = new InMemoryRunner({ agent: rootAgent });

app.post('/chat', async (req, res) => {
  const { message, sessionId, userId } = req.body;
  // Get or create session
  let session = await runner.sessionService.getSession({
    appName: runner.appName, userId, sessionId,
  });
  if (!session) {
    session = await runner.sessionService.createSession({
      appName: runner.appName, userId,
    });
  }
  const events = [];
  for await (const event of runner.runAsync({
    userId, sessionId: session.id,
    newMessage: createUserContent(message),
  })) {
    if (isFinalResponse(event)) {
      events.push({ type: 'response', content: stringifyContent(event) });
    }
  }
  res.json({ events });
});

app.listen(8080);
```

See [references/deployment.md](references/deployment.md) for Hono, Cloud Run, and container patterns.

## Best Practices

1. **Use Zod schemas** - Type-safe tool parameters with `.describe()` for LLM hints
2. **Use `outputKey`** - Auto-store agent output in state for downstream agents
3. **Unique state keys in ParallelAgent** - Prevent race conditions
4. **Descriptive `description` fields** - Guides LLM routing to sub-agents
5. **`async*` generators** - Use `runAsyncImpl` for custom agent flow control
6. **Dev UI for debugging** - `npx @google/adk-devtools web` to inspect events/state

## Common Pitfalls

- **Forgetting `verbatimModuleSyntax: false`** in tsconfig - causes import errors
- **Mutating session directly** - Always use `CallbackContext.state` or `outputKey`
- **Missing Zod `.describe()`** - LLM gets no hint about parameter purpose
- **Single sub-agent instance reuse** - An agent can only be sub-agent once
- **Blocking in async generators** - Use `for await` with `runAsync`

## Resources

- [references/agents.md](references/agents.md) - Agent types and custom agents
- [references/tools.md](references/tools.md) - FunctionTool, MCP, OpenAPI
- [references/multi-agent.md](references/multi-agent.md) - Orchestration patterns
- [references/callbacks.md](references/callbacks.md) - Callbacks and state
- [references/testing.md](references/testing.md) - Evaluation framework
- [references/deployment.md](references/deployment.md) - Express, Hono, Cloud Run

## External Links

- [Official Docs](https://google.github.io/adk-docs/)
- [GitHub (google/adk-js)](https://github.com/google/adk-js)
- [TypeScript Quickstart](https://google.github.io/adk-docs/get-started/typescript/)
