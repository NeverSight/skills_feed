---
name: olakai-create-agent
description: >
  Create a new AI agent with Olakai monitoring from scratch.

  AUTO-INVOKE when user wants to: build a new AI agent, create an AI workflow,
  set up a new chatbot or copilot, implement an autonomous agent, design an
  AI-powered feature, start a new project with AI observability, or add
  KPI tracking and governance to a new AI system.

  TRIGGER KEYWORDS: olakai, create agent, new agent, build agent, AI agent,
  AI workflow, chatbot, copilot, autonomous agent, agent architecture,
  agentic AI, assistive AI, observability setup, KPI tracking, governance,
  new AI project, AI monitoring setup, agent from scratch.

  DO NOT load for: adding monitoring to existing code (use olakai-add-monitoring),
  troubleshooting existing agents (use olakai-troubleshoot), or generating reports
  (use generate-analytics-reports).
license: MIT
metadata:
  author: olakai
  version: "1.8.0"
---

# Create AI Agent with Olakai Monitoring

This skill guides you through creating a new AI agent that is fully integrated with Olakai for monitoring, analytics, and governance.

## Prerequisites

Before starting, ensure:
1. Olakai CLI installed: `npm install -g olakai-cli`
2. CLI authenticated: `olakai login`
3. API key for SDK (generated per-agent via CLI - see Step 2.1)

## Why Custom KPIs Are Essential

Olakai's core value is **tracking business-specific KPIs for your AI agents**. Without KPIs, you're just logging events - not gaining actionable insights.

**What you can measure with KPIs:**
- Business outcomes (items processed, success rates, revenue impact)
- Operational metrics (step counts, retry rates, execution time)
- Quality indicators (error rates, user satisfaction signals)

**Without KPIs configured:**
- ❌ No dashboard metrics beyond basic token counts
- ❌ No aggregated performance views
- ❌ No alerting thresholds
- ❌ No ROI calculations

> ⚠️ **Every agent should have 2-4 KPIs that answer: "How do I know this agent is performing well?"**

> ⚠️ **KPIs created here belong to this specific agent only.** If you later create additional agents, each one needs its own KPI definitions — KPIs cannot be shared or reused across agents.

## Understanding the customData → KPI Pipeline

Before diving into implementation, understand how data flows through Olakai:

```
SDK customData → CustomDataConfig (Schema) → Context Variable → KPI Formula → kpiData
```

### How It Works

1. **customData** (SDK): Raw JSON you send with each event
2. **CustomDataConfig** (Platform): Schema defining which fields are processed
3. **Context Variables**: CustomDataConfig fields become available for formulas
4. **KPI Formula**: Expression that computes a metric (e.g., `SuccessRate * 100`)
5. **kpiData** (Response): Computed KPI values returned with each event

### Critical Rules

| Rule | Consequence |
|------|-------------|
| Only CustomDataConfig fields become variables | Unregistered customData fields are NOT usable in KPIs |
| Formula evaluation is case-insensitive | `stepCount`, `STEPCOUNT`, `StepCount` all work in formulas |
| NUMBER configs need numeric values | Don't send `"5"` (string), send `5` (number) |
| KPIs are unique per agent | Each KPI belongs to exactly one agent — create separately for each, even with identical formulas |

### Built-in Context Variables (Always Available)

| Variable | Type | Description |
|----------|------|-------------|
| `Prompt` | string | The prompt text sent to the LLM |
| `Response` | string | The LLM response text |
| `Documents count` | number | Number of attached documents |
| `PII detected` | boolean | Whether PII was detected |
| `PHI detected` | boolean | Whether PHI was detected |
| `CODE detected` | boolean | Whether code was detected |
| `SECRET detected` | boolean | Whether secrets were detected |

## Step 1: Design the Agent Architecture

### 1.1 Determine Agent Type

**Agentic AI** (Multi-step autonomous workflows):
- Research agents, document processors, data pipelines
- Track as SINGLE events aggregating all internal LLM calls
- Focus on workflow-level metrics (total tokens, total time, success/failure)

**Assistive AI** (Interactive chatbots/copilots):
- Customer support bots, coding assistants, Q&A systems
- Track EACH interaction as separate events
- Focus on conversation-level metrics (per-message tokens, response quality)

### 1.2 Design Your Metrics Schema (CRITICAL)

**Design your metrics BEFORE writing any SDK code.** This ensures only meaningful data is sent and tracked.

#### Step A: Identify Business Questions

What do stakeholders need to know about this agent?
- "How many items does it process per run?"
- "What's the success/failure rate?"
- "How efficient is each execution?"

#### Step B: Map Questions to Metrics

| Business Question | Field Name | Type | KPI Formula | Aggregation |
|-------------------|------------|------|-------------|-------------|
| Throughput | ItemsProcessed | NUMBER | `ItemsProcessed` | SUM |
| Reliability | SuccessRate | NUMBER | `SuccessRate * 100` | AVERAGE |
| Error count | SuccessRate | NUMBER | `IF(SuccessRate < 1, 1, 0)` | SUM |
| Workflow ID | ExecutionId | STRING | (for filtering only) | - |

#### Step C: Plan Your customData Structure

```typescript
// ONLY include fields you'll register as CustomDataConfigs
customData: {
  // Business metrics (will become KPIs)
  ItemsProcessed: number,  // Count of items handled
  SuccessRate: number,     // 0-1 success ratio

  // Performance metrics (will become KPIs)
  StepCount: number,       // Number of workflow steps

  // Identification (for filtering, not KPIs)
  ExecutionId: string,     // Correlation ID
}
```

> ⚠️ **IMPORTANT**: Only include fields you will register as CustomDataConfigs.
> Unregistered fields are stored but **cannot be used in KPIs** - they're effectively wasted data.

### What NOT to Include in customData

The Olakai platform automatically tracks these fields - do NOT duplicate them in customData:

| Already Tracked | Where | Don't Send As customData |
|-----------------|-------|--------------------------|
| Session ID | Main payload | ❌ `sessionId` |
| Agent ID | API key association | ❌ `agentId` |
| User email | `userEmail` parameter | ❌ `email`, `userEmail` |
| Timestamp | Event metadata | ❌ `timestamp`, `createdAt` |
| Request time | `requestTime` parameter | ❌ `duration`, `latency` |
| Token count | `tokens` parameter | ❌ `tokenCount`, `totalTokens` |
| Model | Auto-detected | ❌ `model`, `modelName` |
| Provider | Wrapped client config | ❌ `provider` |

**customData is ONLY for:**
1. **KPI variables** - Fields you'll use in formula calculations (e.g., `ItemsProcessed`, `SuccessRate`)
2. **Tagging/filtering** - Fields you'll filter by in queries (e.g., `Department`, `ProjectId`)

**❌ BAD: Sending redundant data**
```typescript
customData: {
  sessionId: session.id,       // ❌ Already tracked
  agentId: agentConfig.id,     // ❌ Already tracked
  userEmail: user.email,       // ❌ Pass via userEmail param instead
  timestamp: Date.now(),       // ❌ Already tracked
  ItemsProcessed: 10,          // ✅ Needed for KPI
}
```

**✅ GOOD: Only KPI-relevant data**
```typescript
customData: {
  ItemsProcessed: 10,          // ✅ Used in KPI formula
  SuccessRate: 1.0,            // ✅ Used in KPI formula
  ExecutionId: uuid,           // ✅ For correlation/filtering
}
```

## Step 2: Configure Olakai Platform

### 2.1 Create a Workflow (Required)

> ⚠️ **Every agent MUST belong to a workflow**, even if it's the only agent in that workflow.

**Why workflows are required:**
- Enable future multi-agent expansion without restructuring
- Provide workflow-level aggregation for KPIs
- Establish proper organizational hierarchy
- Support workflow-level governance policies

```bash
# Create the workflow first
olakai workflows create --name "Your Workflow Name" --json

# Save the workflow ID for agent association
# Output: { "id": "wfl_xxx...", "name": "Your Workflow Name" }
```

### 2.2 Create the Agent in Olakai

```bash
# Create the agent associated with the workflow
olakai agents create \
  --name "Your Agent Name" \
  --description "What this agent does" \
  --workflow WORKFLOW_ID \
  --with-api-key \
  --json

# Returns agent details including apiKey for SDK use:
# {
#   "id": "cmkbteqn501kyjy4yu6p6xrrx",
#   "name": "Your Agent Name",
#   "workflowId": "wfl_xxx...",
#   "apiKey": "sk_agent_xxxxx..."   <-- Use this in your SDK
# }

# To retrieve an existing agent's API key:
olakai agents get AGENT_ID --json | jq '.apiKey'
```

**Workflow → Agent Hierarchy:**
```
Workflow: "Customer Support Pipeline"
├── Agent: "Ticket Classifier"
├── Agent: "Response Generator"
└── Agent: "Quality Checker"

Workflow: "Document Processing"
└── Agent: "Document Summarizer"  ← Even single agents need a workflow
```

### 2.3 Create Custom Data Configurations (BEFORE Writing SDK Code)

> ⚠️ **This step MUST be completed before Step 3 (SDK Integration).**
> Only fields registered here can be used in KPI formulas. Design the schema first, then code to it.

> ⚠️ **ONLY create configs for data you'll use in KPIs or for filtering.**
> Don't create configs for data already tracked (sessionId, timestamps, tokens) or "nice to have" fields.
> Each config should answer: "Will I use this in a KPI formula?" or "Will I filter/group by this?"

For each custom metric from Step 1.2, create a CustomDataConfig:

```bash
# For numeric metrics (can be used in KPI calculations)
olakai custom-data create --name "ItemsProcessed" --type NUMBER --description "Count of items processed per run"
olakai custom-data create --name "SuccessRate" --type NUMBER --description "Success ratio 0-1"
olakai custom-data create --name "StepCount" --type NUMBER --description "Number of workflow steps executed"

# For string metrics (for filtering/grouping, not calculations)
olakai custom-data create --name "ExecutionId" --type STRING --description "Correlation ID for the execution"

# Verify all configs are created
olakai custom-data list
```

**What this enables:**
- ✅ These field names become **context variables** in KPI formulas
- ✅ Values sent in SDK `customData` with these names are processed
- ❌ Any `customData` field NOT listed here is ignored for KPI purposes

### 2.4 Create KPI Definitions

> ⚠️ **KPIs are created for THIS agent only.** Unlike CustomDataConfigs (account-level, shared across all agents), each KPI is bound to one agent. Do NOT reuse KPI IDs from another agent — if multiple agents need the same metric, create the KPI separately for each.

Define KPIs that use your custom data:

```bash
# Simple variable KPIs
olakai kpis create \
  --name "Items Processed" \
  --agent-id YOUR_AGENT_ID \
  --calculator-id formula \
  --formula "ItemsProcessed" \
  --unit "items" \
  --aggregation SUM

# Calculated KPIs
olakai kpis create \
  --name "Success Rate" \
  --agent-id YOUR_AGENT_ID \
  --calculator-id formula \
  --formula "SuccessRate * 100" \
  --unit "%" \
  --aggregation AVERAGE

# Conditional KPIs
olakai kpis create \
  --name "Error Count" \
  --agent-id YOUR_AGENT_ID \
  --calculator-id formula \
  --formula "IF(SuccessRate < 1, 1, 0)" \
  --unit "errors" \
  --aggregation SUM

# Validate formulas before creating
olakai kpis validate --formula "ItemsProcessed" --agent-id YOUR_AGENT_ID
```

## Step 3: Implement SDK Integration

### 3.1 TypeScript Implementation (Recommended)

**Install dependencies:**
```bash
npm install @olakai/sdk openai
```

**Basic wrapped client setup:**
```typescript
import { OlakaiSDK } from "@olakai/sdk";
import OpenAI from "openai";

// Initialize Olakai
const olakai = new OlakaiSDK({
  apiKey: process.env.OLAKAI_API_KEY!,
  debug: process.env.NODE_ENV === "development",
});
await olakai.init();

// Wrap your LLM client
const openai = olakai.wrap(
  new OpenAI({ apiKey: process.env.OPENAI_API_KEY }),
  {
    provider: "openai",
    defaultContext: {
      task: "Your Task Category", // e.g., "Data Processing & Analysis"
    },
  }
);

// Use wrapped client - monitoring happens automatically
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: userPrompt }],
});
```

**Agentic workflow with manual event tracking:**
```typescript
async function runAgent(input: string): Promise<string> {
  const startTime = Date.now();
  const executionId = crypto.randomUUID();
  let totalTokens = 0;
  let stepCount = 0;
  let itemsProcessed = 0;

  try {
    // Step 1: Planning
    stepCount++;
    const plan = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [{ role: "user", content: `Plan: ${input}` }],
    });
    totalTokens += plan.usage?.total_tokens ?? 0;

    // Step 2: Execution (example: process multiple items)
    const items = parseItems(plan.choices[0].message.content);
    for (const item of items) {
      stepCount++;
      const result = await openai.chat.completions.create({
        model: "gpt-4o",
        messages: [{ role: "user", content: `Process: ${item}` }],
      });
      totalTokens += result.usage?.total_tokens ?? 0;
      itemsProcessed++;
    }

    // Step 3: Summarize
    stepCount++;
    const summary = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [{ role: "user", content: "Summarize results" }],
    });
    totalTokens += summary.usage?.total_tokens ?? 0;

    const finalResponse = summary.choices[0].message.content ?? "";

    // Track the complete workflow as a single event
    // ⚠️ IMPORTANT: Only send fields that have CustomDataConfigs (from Step 2.2)
    olakai.event({
      prompt: input,
      response: finalResponse,
      tokens: totalTokens,
      requestTime: Date.now() - startTime,
      task: "Data Processing & Analysis",
      customData: {
        // Only include fields registered in Step 2.2
        ExecutionId: executionId,
        StepCount: stepCount,
        ItemsProcessed: itemsProcessed,
        SuccessRate: 1.0,
        // ❌ DON'T add unregistered fields - they can't be used in KPIs
      },
    });

    return finalResponse;
  } catch (error) {
    // Track failed execution - same fields, different values
    olakai.event({
      prompt: input,
      response: `Error: ${error instanceof Error ? error.message : "Unknown"}`,
      tokens: totalTokens,
      requestTime: Date.now() - startTime,
      task: "Data Processing & Analysis",
      customData: {
        ExecutionId: executionId,
        StepCount: stepCount,
        ItemsProcessed: itemsProcessed,
        SuccessRate: 0,  // 0 indicates failure
      },
    });
    throw error;
  }
}
```

### 3.2 Python Implementation

**Install dependencies:**
```bash
pip install olakai-sdk openai
```

**Auto-instrumentation setup:**
```python
import os
from olakaisdk import olakai_config, instrument_openai, olakai_context, olakai_event, OlakaiEventParams
from openai import OpenAI

# Initialize Olakai
olakai_config(os.getenv("OLAKAI_API_KEY"))
instrument_openai()

# Create OpenAI client (automatically instrumented)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# For assistive AI - use context manager
with olakai_context(userEmail="user@example.com", task="Customer Support"):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
```

**Manual event tracking for agentic workflows:**
```python
import time
import uuid

def run_agent(input_text: str) -> str:
    start_time = time.time()
    execution_id = str(uuid.uuid4())
    total_tokens = 0
    step_count = 0
    items_processed = 0

    try:
        # Your workflow steps here...
        step_count += 1
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": input_text}]
        )
        total_tokens += response.usage.total_tokens

        final_response = response.choices[0].message.content

        # Track successful execution
        # ⚠️ Only send fields registered as CustomDataConfigs
        olakai_event(OlakaiEventParams(
            prompt=input_text,
            response=final_response,
            tokens=total_tokens,
            requestTime=int((time.time() - start_time) * 1000),
            task="Data Processing & Analysis",
            customData={
                "ExecutionId": execution_id,
                "StepCount": step_count,
                "ItemsProcessed": items_processed,
                "SuccessRate": 1.0,
            }
        ))

        return final_response

    except Exception as e:
        # Track failed execution - same fields, different values
        olakai_event(OlakaiEventParams(
            prompt=input_text,
            response=f"Error: {str(e)}",
            tokens=total_tokens,
            requestTime=int((time.time() - start_time) * 1000),
            task="Data Processing & Analysis",
            customData={
                "ExecutionId": execution_id,
                "StepCount": step_count,
                "ItemsProcessed": items_processed,
                "SuccessRate": 0,  # 0 indicates failure
            }
        ))
        raise
```

### 3.3 REST API Direct Integration

For other languages or custom integrations:

```bash
# ⚠️ customData fields must match registered CustomDataConfigs exactly
curl -X POST "https://app.olakai.ai/api/monitoring/prompt" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "prompt": "User input here",
    "response": "Agent response here",
    "app": "your-agent-name",
    "task": "Data Processing & Analysis",
    "tokens": 1500,
    "requestTime": 5000,
    "customData": {
      "ExecutionId": "abc-123",
      "StepCount": 5,
      "ItemsProcessed": 10,
      "SuccessRate": 1.0
    }
  }'
```

## Step 4: Test-Validate-Iterate Cycle

**CRITICAL:** Always validate your implementation by running a test and inspecting the actual event data. Do not assume configuration is correct - verify it.

### 4.1 Run Your Agent (Generate Test Event)

Execute your agent with test data to generate at least one monitoring event:

```typescript
// Run your agent
const result = await runAgent("Test input for validation");
console.log("Agent completed, checking Olakai...");
```

### 4.2 Fetch and Inspect the Event

```bash
# List recent activity for your agent
olakai activity list --agent-id YOUR_AGENT_ID --limit 1 --json

# Get the full event details including customData and kpiData
olakai activity get EVENT_ID --json
```

### 4.3 Validate Each Component

**Check customData is present and correct:**
```bash
olakai activity get EVENT_ID --json | jq '.customData'
```

Expected output:
```json
{
  "ExecutionId": "abc-123",
  "StepCount": 5,
  "ItemsProcessed": 10,
  "SuccessRate": 1.0
}
```

If fields are missing: SDK isn't sending them. Check your `customData` object in the event call.

**Check KPIs are numeric (not strings):**
```bash
olakai activity get EVENT_ID --json | jq '.kpiData'
```

**CORRECT** - numeric values:
```json
{
  "Items Processed": 10,
  "Success Rate": 100
}
```

**WRONG** - string values (indicates broken formula):
```json
{
  "Items Processed": "itemsProcessed",
  "Success Rate": "SuccessRate"
}
```

If KPIs show strings: The formula is stored incorrectly. Fix with:
```bash
olakai kpis update KPI_ID --formula "YourVariable"
```

**Check KPIs show values (not null):**

If KPIs show `null`:
1. Verify customData contains the field: `jq '.customData.YourField'`
2. Verify CustomDataConfig exists: `olakai custom-data list`
3. Verify field name case matches exactly (case-sensitive!)

### 4.4 Iterate Until Correct

Repeat the cycle until all validations pass:

```
┌─────────────────────────────────────────────────────────┐
│  1. Run agent (generate event)                          │
│                    ↓                                    │
│  2. Fetch event: olakai activity get ID --json          │
│                    ↓                                    │
│  3. Check customData present?                           │
│     NO → Fix SDK code, goto 1                           │
│                    ↓                                    │
│  4. Check kpiData numeric (not strings)?                │
│     NO → Fix formula: olakai kpis update ID --formula   │
│          goto 1                                         │
│                    ↓                                    │
│  5. Check kpiData not null?                             │
│     NO → Create CustomDataConfig or fix field name      │
│          goto 1                                         │
│                    ↓                                    │
│  ✅ All validations pass - implementation complete      │
└─────────────────────────────────────────────────────────┘
```

### 4.5 Example Validation Session

```bash
# 1. Run your agent (generates event)
$ node my-agent.js "Test task"
Agent completed successfully

# 2. Get the latest event
$ olakai activity list --agent-id cmkxxx --limit 1 --json | jq '.prompts[0].id'
"cmkeyyy"

# 3. Inspect the event
$ olakai activity get cmkeyyy --json | jq '{customData, kpiData}'
{
  "customData": {
    "StepCount": 3,
    "ItemsProcessed": 5,
    "SuccessRate": 1
  },
  "kpiData": {
    "Steps Executed": 3,        # ✅ Numeric
    "Items Processed": 5,       # ✅ Numeric
    "Success Rate": 100         # ✅ Numeric (formula: SuccessRate * 100)
  }
}

# ✅ All good! Implementation is correct.
```

## Step 5: Production Checklist

Before deploying to production:

- [ ] API key stored securely in environment variables
- [ ] Error handling wraps all LLM calls
- [ ] Failed executions still report events (with successRate: 0)
- [ ] All custom data fields have corresponding CustomDataConfig entries
- [ ] KPI formulas validated and showing numeric values (not strings)
- [ ] SDK configured with appropriate retries and timeouts
- [ ] Sensitive data redaction enabled if needed

## KPI Formula Reference

### Supported Operators

| Category | Operators |
|----------|-----------|
| Arithmetic | `+`, `-`, `*`, `/` |
| Comparison | `<`, `<=`, `=`, `<>`, `>=`, `>` |
| Logical | `AND`, `OR`, `NOT` |
| Conditional | `IF(condition, true_val, false_val)`, `MAP(value, match1, out1, default)` |
| Math | `ABS`, `MAX`, `MIN`, `AVERAGE`, `TRUNC` |
| Null handling | `ISNA(value)`, `ISDEFINED(value)`, `NA()` |

### Common Formula Patterns

```bash
# Simple variable passthrough
--formula "ItemsProcessed"

# Percentage conversion (0-1 to 0-100)
--formula "SuccessRate * 100"

# Conditional counting (count failures)
--formula "IF(SuccessRate < 1, 1, 0)"

# Boolean to number conversion
--formula "IF(PII detected, 1, 0)"

# Null-safe with default value
--formula "IF(ISDEFINED(MyField), MyField, 0)"

# Compound conditions
--formula "IF(AND(StepCount > 5, SuccessRate < 0.9), 1, 0)"
```

### Aggregation Types

| Aggregation | Use For | Example |
|-------------|---------|---------|
| `SUM` | Totals, counts | Total items processed across all runs |
| `AVERAGE` | Rates, percentages | Average success rate |

## Task Categories Reference

Use these predefined task categories for the `task` field:

| Category | Example Subtasks |
|----------|------------------|
| Research & Intelligence | competitive intelligence, market research, legal research |
| Data Processing & Analysis | data extraction, statistical analysis, trend identification |
| Content Development | blog writing, technical documentation, proposal writing |
| Content Refinement | editing, proofreading, grammar correction |
| Customer Experience | complaint resolution, ticket triage, FAQ development |
| Software Development | code generation, code review, debugging |
| Strategic Planning | roadmap development, scenario planning |

## Quick Reference

```bash
# CLI Commands
olakai login                           # Authenticate
olakai agents create --name "Name"     # Create agent
olakai custom-data create --name X --type NUMBER  # Create custom field
olakai kpis create --formula "X" --agent-id ID    # Create KPI
olakai activity list --agent-id ID     # View events

# SDK Initialization (TypeScript)
const olakai = new OlakaiSDK({ apiKey: process.env.OLAKAI_API_KEY });
await olakai.init();
const openai = olakai.wrap(new OpenAI({ apiKey }), { provider: "openai" });

# SDK Initialization (Python)
olakai_config(os.getenv("OLAKAI_API_KEY"))
instrument_openai()
```
