---
name: weave-integration
description: Add W&B Weave observability and LLM tracing to any project. Use when instrumenting LLM calls for token visibility, latency tracking, cost analysis, or debugging. Supports TypeScript/Node.js and Python projects. Weave provides automatic tracing for OpenAI, Anthropic, and 20+ LLM providers with minimal code changes.
---

# Weave Integration

Add [W&B Weave](https://docs.wandb.ai/weave/) observability to any LLM project. Weave traces all LLM calls, captures tokens/latency/costs, and provides a UI for debugging and evaluation.

## Quick Start

### 1. Install

```bash
# TypeScript/Node.js
npm install weave

# Python
pip install weave
```

### 2. Get API Key

Set `WANDB_API_KEY` environment variable. Get key from [wandb.ai/settings](https://wandb.ai/settings).

```bash
export WANDB_API_KEY="your-key-here"
```

### 3. Initialize

```typescript
// TypeScript
import * as weave from 'weave';
await weave.init('your-team/project-name');
```

```python
# Python
import weave
weave.init('your-team/project-name')
```

### 4. Trace LLM Calls

**Auto-patching** (supported providers traced automatically):

```typescript
// TypeScript - CommonJS: works out of the box
import OpenAI from 'openai';
import * as weave from 'weave';

await weave.init('my-project');
const client = new OpenAI();
// All calls now traced automatically
```

**Manual wrapping** (for custom functions or unsupported libs):

```typescript
// TypeScript
const myFunction = weave.op(async (input: string) => {
  // your code here
  return result;
});
```

```python
# Python
@weave.op()
def my_function(input: str):
    return result
```

## TypeScript Setup Details

See [references/typescript.md](references/typescript.md) for:
- ESM configuration (`--import=weave/instrument`)
- Bundler compatibility (Next.js, Vite)
- Manual patching fallback

## Supported Providers (Auto-traced)

OpenAI, Anthropic, Cohere, Mistral, Google, Groq, Together AI, LiteLLM, Azure, Bedrock, Cerebras, HuggingFace, OpenRouter, NVIDIA NIM, and more.

Full list: https://docs.wandb.ai/weave/guides/integrations

## Integration Workflow

When adding Weave to a project:

1. **Find LLM call sites** — search for OpenAI/Anthropic client usage
2. **Add weave.init()** — early in app startup, before any LLM calls
3. **Verify auto-patching** — check traces appear in W&B UI
4. **Wrap custom functions** — use `weave.op()` for additional visibility
5. **Add cost tracking** — Weave tracks tokens automatically for supported providers

## Viewing Traces

After running your app:
- Open [wandb.ai](https://wandb.ai) → Your project → Weave tab
- See all traces with inputs, outputs, latency, token usage, costs
- Filter, search, and export call data

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `WANDB_API_KEY` | Authentication (required) |
| `WEAVE_IMPLICITLY_PATCH_INTEGRATIONS` | Set `false` to disable auto-patching |

## Common Patterns

### Wrap Existing Client

```typescript
import { wrapOpenAI } from 'weave';
import OpenAI from 'openai';

const client = wrapOpenAI(new OpenAI());
```

### Trace Class Methods

```typescript
class MyAgent {
  @weave.op
  async predict(prompt: string) {
    return "response";
  }
}
```

### Add Display Names

```typescript
const myOp = weave.op(myFunction, {
  callDisplayName: (input) => `Custom Name: ${input}`
});
```

## Clawdbot-Specific Integration

For Clawdbot/similar Node.js agents:
1. Locate the LLM client initialization (usually Anthropic/OpenAI SDK)
2. Add `weave.init()` in the main entry point
3. For ESM, add `--import=weave/instrument` to node invocation
4. All provider calls will be traced to W&B

## Troubleshooting

- **No traces appearing**: Check `WANDB_API_KEY` is set
- **ESM not patching**: Use `--import=weave/instrument` flag
- **Bundler issues**: Mark LLM libs as external in config
- **Manual fallback**: Use `wrapOpenAI()` or explicit `weave.op()` wrappers
