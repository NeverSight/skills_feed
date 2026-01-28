---
name: langfuse-observability
description: |
  Query Langfuse traces, prompts, and LLM metrics. Use when:
  - Analyzing LLM generation traces (errors, latency, tokens)
  - Reviewing prompt performance and versions
  - Debugging failed generations
  - Comparing model outputs across runs
  Keywords: langfuse, traces, observability, LLM metrics, prompt management, generations
---

# Langfuse Observability

Query traces, prompts, and metrics from Langfuse. Requires env vars:
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_HOST` (e.g., `https://us.cloud.langfuse.com`)

## Quick Start

All commands run from the skill directory:
```bash
cd ~/.claude/skills/langfuse-observability
```

### List Recent Traces
```bash
# Last 10 traces
npx tsx scripts/fetch-traces.ts --limit 10

# Filter by name pattern
npx tsx scripts/fetch-traces.ts --name "quiz-generation" --limit 5

# Filter by user
npx tsx scripts/fetch-traces.ts --user-id "user_abc123" --limit 10
```

### Get Single Trace Details
```bash
# Full trace with spans and generations
npx tsx scripts/fetch-trace.ts <trace-id>
```

### Get Prompt
```bash
# Fetch specific prompt
npx tsx scripts/list-prompts.ts --name scry-intent-extraction

# With label
npx tsx scripts/list-prompts.ts --name scry-intent-extraction --label production
```

### Get Metrics Summary
```bash
# Summary for recent traces
npx tsx scripts/get-metrics.ts --limit 50

# Filter by trace name
npx tsx scripts/get-metrics.ts --name "quiz-generation" --limit 100
```

## Output Formats

All scripts output JSON to stdout for easy parsing.

### Trace List Output
```json
[
  {
    "id": "trace-abc123",
    "name": "quiz-generation",
    "userId": "user_xyz",
    "input": {"prompt": "..."},
    "output": {"concepts": [...]},
    "latencyMs": 3200,
    "createdAt": "2025-12-09T..."
  }
]
```

### Single Trace Output
Includes full nested structure: trace → observations (spans + generations) with token usage.

### Metrics Output
```json
{
  "totalTraces": 50,
  "successCount": 48,
  "errorCount": 2,
  "avgLatencyMs": 2850,
  "totalTokens": 125000,
  "byName": {"quiz-generation": 30, "phrasing-generation": 20}
}
```

## Common Workflows

### Debug Failed Generation
```bash
cd ~/.claude/skills/langfuse-observability

# 1. Find recent traces
npx tsx scripts/fetch-traces.ts --limit 10

# 2. Get details of specific trace
npx tsx scripts/fetch-trace.ts <trace-id>
```

### Monitor Token Usage
```bash
# Get metrics for cost analysis
npx tsx scripts/get-metrics.ts --limit 100
```

### Check Prompt Configuration
```bash
npx tsx scripts/list-prompts.ts --name scry-concept-synthesis --label production
```

## Cost Tracking

### Calculate Costs

```typescript
// Get metrics with cost calculation
const metrics = await langfuse.getMetrics({ limit: 100 });

// Pricing per 1M tokens (update as needed)
const pricing = {
  "claude-3-5-sonnet": { input: 3.0, output: 15.0 },
  "gpt-4o": { input: 2.5, output: 10.0 },
  "gpt-4o-mini": { input: 0.15, output: 0.6 },
};

function calculateCost(model: string, inputTokens: number, outputTokens: number) {
  const p = pricing[model] || { input: 1, output: 1 };
  return (inputTokens * p.input + outputTokens * p.output) / 1_000_000;
}
```

### Daily/Monthly Spend

```bash
# Get traces for date range
npx tsx scripts/fetch-traces.ts --from "2025-12-01" --to "2025-12-07" --limit 1000

# Calculate spend (parse output and sum costs)
```

### Cost Alerts

**Set up alerts in Langfuse dashboard:**
1. Go to Dashboard → Alerts
2. Create alert for: `daily_cost > X` or `cost_per_trace > Y`
3. Configure notification (email, Slack webhook)

**Or implement in code:**
```typescript
async function checkCostBudget() {
  const dailyMetrics = await langfuse.getMetrics({ since: "24h" });
  const dailyCost = calculateTotalCost(dailyMetrics);

  if (dailyCost > DAILY_BUDGET) {
    await notifySlack(`⚠️ LLM daily spend ($${dailyCost}) exceeded budget ($${DAILY_BUDGET})`);
  }
}
```

## Production Best Practices

### 1. Trace Everything

```typescript
import { Langfuse } from "langfuse";

const langfuse = new Langfuse({
  publicKey: process.env.LANGFUSE_PUBLIC_KEY,
  secretKey: process.env.LANGFUSE_SECRET_KEY,
});

// Wrap every LLM call
async function tracedLLMCall(name: string, messages: Message[]) {
  const trace = langfuse.trace({
    name,
    userId: currentUser.id,
    metadata: { environment: process.env.NODE_ENV },
  });

  const generation = trace.generation({
    name: "chat",
    model: selectedModel,
    input: messages,
  });

  try {
    const response = await llm.chat({ model: selectedModel, messages });

    generation.end({
      output: response.choices[0].message,
      usage: {
        promptTokens: response.usage.prompt_tokens,
        completionTokens: response.usage.completion_tokens,
      },
    });

    return response;
  } catch (error) {
    generation.end({ level: "ERROR", statusMessage: error.message });
    throw error;
  }
}
```

### 2. Add Context

```typescript
// Include useful metadata for debugging
const trace = langfuse.trace({
  name: "user-query",
  userId: user.id,
  sessionId: session.id,  // Group related traces
  metadata: {
    userPlan: user.plan,
    feature: "chat",
    version: "v2.1",
  },
  tags: ["production", "chat-feature"],
});
```

### 3. Score Outputs

```typescript
// Track quality metrics
generation.score({
  name: "user-feedback",
  value: userRating, // 1-5
});

// Or automated scoring
generation.score({
  name: "response-length",
  value: response.content.length < 500 ? 1 : 0,
});
```

### 4. Flush Before Exit

```typescript
// Important for serverless environments
await langfuse.flushAsync();
```

## Promptfoo Integration

### Trace → Eval Case Workflow

1. **Find interesting traces in Langfuse** (failures, edge cases)
2. **Export as test cases** for Promptfoo
3. **Add to regression suite** to prevent future issues

```typescript
// Export failed traces as test cases
const failedTraces = await langfuse.getTraces({ level: "ERROR", limit: 50 });

const testCases = failedTraces.map(trace => ({
  vars: trace.input,
  assert: [
    { type: "not-contains", value: "error" },
    { type: "llm-rubric", value: "Response should address the user's question" },
  ],
}));

// Add to promptfooconfig.yaml
```

### Langfuse Callback in Promptfoo

```yaml
# promptfooconfig.yaml
defaultTest:
  options:
    callback: langfuse
    callbackConfig:
      publicKey: ${LANGFUSE_PUBLIC_KEY}
      secretKey: ${LANGFUSE_SECRET_KEY}
```

## Alternatives Comparison

| Feature | Langfuse | Helicone | LangSmith |
|---------|----------|----------|-----------|
| Open Source | ✅ | ✅ | ❌ |
| Self-Host | ✅ | ✅ | ❌ |
| Free Tier | ✅ Generous | ✅ 10K/mo | ⚠️ Limited |
| Prompt Mgmt | ✅ | ❌ | ✅ |
| Tracing | ✅ | ✅ | ✅ |
| Cost Track | ✅ | ✅ | ✅ |
| A/B Testing | ⚠️ | ❌ | ✅ |

**Choose Langfuse when**: Self-hosting needed, cost-conscious, want prompt management.

**Choose Helicone when**: Proxy-based setup preferred, simple integration.

**Choose LangSmith when**: LangChain ecosystem, enterprise support needed.

## Related Skills

- `llm-evaluation` - Promptfoo for testing, pairs well with Langfuse for observability
- `llm-gateway-routing` - OpenRouter/LiteLLM for model routing
- `ai-llm-development` - Overall LLM development patterns

## Related Commands

- `/llm-gates` - Audit LLM infrastructure including observability gaps
- `/observe` - General observability audit
