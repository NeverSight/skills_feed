---
name: olakai-add-monitoring
description: >
  Add Olakai monitoring to an existing AI agent or LLM integration.

  AUTO-INVOKE when user wants to: add monitoring to existing code, integrate
  observability into a working agent, instrument an existing AI system,
  add tracking to LLM calls, wrap OpenAI/Anthropic clients, add analytics
  to working AI code, or retrofit monitoring to production AI.

  TRIGGER KEYWORDS: olakai, add monitoring, integrate monitoring, instrument,
  wrap client, observability, SDK integration, @olakai/sdk, olakai-sdk,
  existing agent, existing code, add tracking, analytics, telemetry,
  retrofit monitoring, existing LLM, existing OpenAI, existing Anthropic.

  DO NOT load for: creating new agents from scratch (use olakai-create-agent),
  troubleshooting issues (use olakai-troubleshoot), or generating reports
  (use generate-analytics-reports).
license: MIT
metadata:
  author: olakai
  version: "1.8.0"
---

# Add Olakai Monitoring to Existing Agent

This skill guides you through adding Olakai monitoring to an existing AI agent or LLM-powered application with minimal code changes.

For full SDK documentation, see: https://app.olakai.ai/llms.txt

## Prerequisites

- Existing working AI agent/application using OpenAI, Anthropic, or other LLM
- Olakai CLI installed and authenticated (`npm install -g olakai-cli && olakai login`)
- Olakai API key for your agent (get via CLI: `olakai agents get AGENT_ID --json | jq '.apiKey'`)
- Node.js 18+ (for TypeScript) or Python 3.7+ (for Python)

> **Note:** Each agent can have its own API key. Create one with `olakai agents create --name "Name" --with-api-key`

## Why Custom KPIs Are Essential

Adding monitoring is only the first step. **The real value of Olakai comes from tracking custom KPIs specific to your agent's business purpose.**

**Without KPIs configured:**
- ❌ Only basic token counts and request logs
- ❌ No aggregated business metrics on dashboard
- ❌ No alerting capabilities
- ❌ No ROI tracking

**With KPIs configured:**
- ✅ Custom metrics (items processed, success rates, quality scores)
- ✅ Trend analysis and performance dashboards
- ✅ Threshold-based alerting
- ✅ Business value calculations

> ⚠️ **Plan to configure at least 2-4 KPIs** that answer: "How do I know this agent is performing well?"

> ⚠️ **KPIs are unique per agent.** If adding monitoring to an agent that needs the same KPIs as another already-configured agent, you must still create new KPI definitions for this agent. KPIs cannot be shared or reused across agents.

## Understanding the customData → KPI Pipeline

Before adding monitoring, understand how custom data flows through Olakai:

```
SDK customData → CustomDataConfig (Schema) → Context Variable → KPI Formula → kpiData
```

### Critical Rules

| Rule | Consequence |
|------|-------------|
| Only CustomDataConfig fields become variables | Unregistered customData fields are NOT usable in KPIs |
| Formula evaluation is case-insensitive | `stepCount`, `STEPCOUNT`, `StepCount` all work in formulas |
| NUMBER configs need numeric values | Don't send `"5"` (string), send `5` (number) |

> ⚠️ **IMPORTANT**: The SDK accepts any JSON in `customData`, but **only fields registered as CustomDataConfigs are processed**. Unregistered fields are stored but cannot be used in KPIs.

## Quick Start (5-Minute Integration)

### For TypeScript/JavaScript

**1. Install the SDK:**
```bash
npm install @olakai/sdk
```

**2. Wrap your existing client:**

Before:
```typescript
import OpenAI from "openai";
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
```

After:
```typescript
import OpenAI from "openai";
import { OlakaiSDK } from "@olakai/sdk";

const olakai = new OlakaiSDK({ apiKey: process.env.OLAKAI_API_KEY! });
await olakai.init();

const openai = olakai.wrap(
  new OpenAI({ apiKey: process.env.OPENAI_API_KEY }),
  { provider: "openai" }
);
```

**That's it!** All calls through `openai` are now automatically tracked.

### For Python

**1. Install the SDK:**
```bash
pip install olakai-sdk
```

**2. Add instrumentation:**

Before:
```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

After:
```python
from openai import OpenAI
from olakaisdk import olakai_config, instrument_openai

olakai_config(os.getenv("OLAKAI_API_KEY"))
instrument_openai()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

**That's it!** All calls through `client` are now automatically tracked.

---

## Detailed Integration Guide

### Step 1: Identify Your Integration Pattern

**Pattern A: Single LLM Client**
You have one OpenAI/Anthropic client used throughout your app.
→ Use the wrapped client approach (shown above)

**Pattern B: Multiple LLM Calls per Request**
Your agent makes several LLM calls to complete one task.
→ Use manual event tracking to aggregate calls

**Pattern C: Streaming Responses**
You stream LLM responses to users.
→ SDK handles this automatically; events sent after stream completes

**Pattern D: Third-Party LLM (not OpenAI/Anthropic)**
You use Perplexity, Groq, local models, etc.
→ Use manual event tracking via REST API or `olakai.event()`

### Step 2: Install and Configure

#### TypeScript Setup

```typescript
// lib/olakai.ts - Create a singleton
import { OlakaiSDK } from "@olakai/sdk";
import OpenAI from "openai";

let olakaiInstance: OlakaiSDK | null = null;
let wrappedOpenAI: OpenAI | null = null;

export async function getOlakaiClient(): Promise<OlakaiSDK> {
  if (!olakaiInstance) {
    olakaiInstance = new OlakaiSDK({
      apiKey: process.env.OLAKAI_API_KEY!,
      debug: process.env.NODE_ENV === "development",
      retries: 3,
      timeout: 30000,
    });
    await olakaiInstance.init();
  }
  return olakaiInstance;
}

export async function getOpenAI(): Promise<OpenAI> {
  if (!wrappedOpenAI) {
    const olakai = await getOlakaiClient();
    wrappedOpenAI = olakai.wrap(
      new OpenAI({ apiKey: process.env.OPENAI_API_KEY }),
      {
        provider: "openai",
        defaultContext: {
          task: "Software Development", // Default task category
        },
      }
    );
  }
  return wrappedOpenAI;
}
```

#### Python Setup

```python
# lib/olakai.py - Create initialization module
import os
from olakaisdk import olakai_config, instrument_openai

_initialized = False

def init_olakai():
    global _initialized
    if not _initialized:
        olakai_config(
            api_key=os.getenv("OLAKAI_API_KEY"),
            debug=os.getenv("DEBUG") == "true"
        )
        instrument_openai()
        _initialized = True

# Call at app startup
init_olakai()
```

### Step 3: Add Context to Calls

#### Adding User Information

TypeScript:
```typescript
const response = await openai.chat.completions.create(
  {
    model: "gpt-4o",
    messages: [{ role: "user", content: userMessage }],
  },
  {
    userEmail: user.email,        // Track by user
    task: "Customer Experience",  // Categorize
  }
);
// Session grouping is automatic
```

Python:
```python
from olakaisdk import olakai_context

with olakai_context(
    userEmail=user.email,
    userId=user.id,  # Optional: explicit user tracking
    task="Customer Experience"
):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
# Note: Session grouping is automatic via internal sessionId
```

#### Adding Custom Data

> ⚠️ **IMPORTANT**: Only send fields you've registered as CustomDataConfigs (Step 5.3). Unregistered fields are stored but **cannot be used in KPIs**.

> ⚠️ **Only send data you'll use in KPIs or for filtering.** Don't duplicate fields already tracked by the platform:
> - Session ID, Agent ID (automatic)
> - User email (use `userEmail` parameter)
> - Timestamps, token count, model, provider (automatic)

TypeScript:
```typescript
const response = await openai.chat.completions.create(
  { model: "gpt-4o", messages },
  {
    userEmail: user.email,
    customData: {
      // Only include fields registered as CustomDataConfigs
      Department: user.department,
      ProjectId: currentProject.id,
      Priority: ticket.priority,
      // ❌ Don't add unregistered fields - they can't be used in KPIs
    },
  }
);
```

Python:
```python
with olakai_context(
    userEmail=user.email,
    customData={
        # Only include fields registered as CustomDataConfigs
        "Department": user.department,
        "ProjectId": project.id,
        "Priority": ticket.priority
    }
):
    response = client.chat.completions.create(...)
```

### Step 4: Handle Agentic Workflows

If your agent makes multiple LLM calls per task, aggregate them into a single event:

```typescript
async function processDocument(doc: Document): Promise<ProcessingResult> {
  const olakai = await getOlakaiClient();
  const openai = await getOpenAI();

  const startTime = Date.now();
  let totalTokens = 0;

  // Step 1: Extract
  const extraction = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: `Extract from: ${doc.content}` }],
  });
  totalTokens += extraction.usage?.total_tokens ?? 0;

  // Step 2: Analyze
  const analysis = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: `Analyze: ${extraction.choices[0].message.content}` }],
  });
  totalTokens += analysis.usage?.total_tokens ?? 0;

  // Step 3: Summarize
  const summary = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: `Summarize: ${analysis.choices[0].message.content}` }],
  });
  totalTokens += summary.usage?.total_tokens ?? 0;

  const result = summary.choices[0].message.content ?? "";

  // Track the complete workflow as ONE event
  // ⚠️ Only send fields registered as CustomDataConfigs
  olakai.event({
    prompt: `Process document: ${doc.title}`,
    response: result,
    tokens: totalTokens,
    requestTime: Date.now() - startTime,
    task: "Data Processing & Analysis",
    customData: {
      // Only registered fields - see Step 5.3
      DocumentId: doc.id,
      DocumentType: doc.type,
      StepCount: 3,
      Success: 1,  // Use 1/0 for boolean in NUMBER fields
    },
  });

  return { summary: result, tokens: totalTokens };
}
```

### Step 5: Configure Custom Metrics (Essential for Value)

> ⚠️ **This step is required to get real value from Olakai.** Without KPIs, you're only logging events - not gaining actionable insights.

| Without KPIs | With KPIs |
|--------------|-----------|
| Raw event logs only | Aggregated business metrics |
| No dashboard insights | Visual performance trends |
| No alerting | Threshold-based alerts |
| No ROI tracking | Calculated business value |

#### 5.1 Install CLI (if not already)
```bash
npm install -g olakai-cli
olakai login
```

#### 5.2 Register Your Agent
```bash
# Create agent entry (associate with a workflow)
olakai agents create --name "Document Processor" --description "Processes and summarizes documents" --workflow WORKFLOW_ID --with-api-key

# Note the agent ID returned
```

#### 5.2.1 Ensure Agent Has a Workflow

> ⚠️ **Every agent MUST belong to a workflow**, even if it's the only agent.

```bash
# Check if agent has a workflow
olakai agents get YOUR_AGENT_ID --json | jq '.workflowId'

# If null, create a workflow and associate:
olakai workflows create --name "Your Workflow Name" --json
olakai agents update YOUR_AGENT_ID --workflow WORKFLOW_ID
```

**Why workflows matter:**
- Enable future multi-agent expansion
- Provide workflow-level KPI aggregation
- Establish proper organizational hierarchy

#### 5.3 Create Custom Data Configs FIRST

> ⚠️ **IMPORTANT**: Create configs for ALL fields you send in `customData`. Only registered fields can be used in KPIs.

```bash
# For each field in your customData, create a config
olakai custom-data create --name "DocumentId" --type STRING
olakai custom-data create --name "DocumentType" --type STRING
olakai custom-data create --name "StepCount" --type NUMBER
olakai custom-data create --name "Success" --type NUMBER  # Use 1/0 for boolean

# Verify all configs exist
olakai custom-data list
```

**What this enables:**
- ✅ These field names become **context variables** in KPI formulas
- ✅ Values sent in SDK `customData` with these names are processed
- ❌ Any `customData` field NOT listed here is ignored for KPI purposes

#### 5.4 Create KPIs

> ⚠️ **Create KPIs for THIS agent specifically.** KPIs are bound to a single agent and are not shared like CustomDataConfigs. Even if another agent has identical KPIs, you must create them again here with this agent's ID.

```bash
olakai kpis create \
  --name "Documents Processed" \
  --agent-id YOUR_AGENT_ID \
  --calculator-id formula \
  --formula "IF(Success = 1, 1, 0)" \
  --aggregation SUM

olakai kpis create \
  --name "Avg Steps per Document" \
  --agent-id YOUR_AGENT_ID \
  --calculator-id formula \
  --formula "StepCount" \
  --aggregation AVERAGE
```

#### 5.5 Update SDK Code to Match

After creating configs, ensure your SDK code sends **exactly those field names**:

```typescript
customData: {
  DocumentId: doc.id,       // Matches CustomDataConfig "DocumentId"
  DocumentType: doc.type,   // Matches CustomDataConfig "DocumentType"
  StepCount: 3,             // Matches CustomDataConfig "StepCount"
  Success: true ? 1 : 0,    // Matches CustomDataConfig "Success"
  // ❌ Don't add fields without configs - they won't be usable in KPIs
}
```

## Framework-Specific Integrations

### Next.js API Routes

```typescript
// app/api/chat/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getOpenAI } from "@/lib/olakai";
import { auth } from "@/auth";

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { message, conversationId } = await req.json();
  const openai = await getOpenAI();

  const response = await openai.chat.completions.create(
    {
      model: "gpt-4o",
      messages: [{ role: "user", content: message }],
    },
    {
      userEmail: session.user.email!,
      task: "Customer Experience",
    }
  );
  // Session grouping is automatic

  return NextResponse.json({
    reply: response.choices[0].message.content,
  });
}
```

### Express.js

```typescript
// middleware/olakai.ts
import { getOlakaiClient, getOpenAI } from "../lib/olakai";

export async function initOlakai() {
  await getOlakaiClient();
  console.log("Olakai initialized");
}

// routes/chat.ts
import express from "express";
import { getOpenAI } from "../lib/olakai";

const router = express.Router();

router.post("/", async (req, res) => {
  const openai = await getOpenAI();
  const { message } = req.body;

  const response = await openai.chat.completions.create(
    { model: "gpt-4o", messages: [{ role: "user", content: message }] },
    { userEmail: req.user.email }
  );
  // Session grouping is automatic

  res.json({ reply: response.choices[0].message.content });
});
```

### FastAPI (Python)

```python
# main.py
from fastapi import FastAPI, Depends
from openai import OpenAI
from olakaisdk import olakai_config, instrument_openai, olakai_context

app = FastAPI()

@app.on_event("startup")
async def startup():
    olakai_config(os.getenv("OLAKAI_API_KEY"))
    instrument_openai()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/chat")
async def chat(message: str, user: User = Depends(get_current_user)):
    with olakai_context(userEmail=user.email, task="Customer Support"):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}]
        )
    return {"reply": response.choices[0].message.content}
```

## Handling Edge Cases

### Streaming Responses

The SDK automatically handles streaming. Events are sent after the stream completes:

```typescript
const stream = await openai.chat.completions.create(
  {
    model: "gpt-4o",
    messages: [{ role: "user", content: userMessage }],
    stream: true,
  },
  { userEmail: user.email }
);

for await (const chunk of stream) {
  // Stream to client
  res.write(chunk.choices[0]?.delta?.content ?? "");
}
// Event automatically sent here with full response
```

### Error Handling

Wrap calls to ensure errors are tracked:

```typescript
try {
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages,
  });
  return response.choices[0].message.content;
} catch (error) {
  // SDK still tracks the failed attempt
  // Optionally send explicit error event
  olakai.event({
    prompt: messages[messages.length - 1].content,
    response: `Error: ${error instanceof Error ? error.message : "Unknown"}`,
    task: "Software Development",
    customData: { error: true, errorType: error.name },
  });
  throw error;
}
```

### Non-OpenAI Providers

For Anthropic, Perplexity, or other providers, use manual tracking:

```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

async function callClaude(prompt: string): Promise<string> {
  const startTime = Date.now();

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
  });

  const content = response.content[0].type === "text" ? response.content[0].text : "";

  // Manual tracking for non-wrapped clients
  olakai.event({
    prompt,
    response: content,
    tokens: response.usage.input_tokens + response.usage.output_tokens,
    requestTime: Date.now() - startTime,
    task: "Content Development",
    customData: {
      provider: "anthropic",
      model: "claude-sonnet-4-20250514",
    },
  });

  return content;
}
```

## Test-Validate-Iterate Cycle

**CRITICAL:** Never assume your integration is working. Always validate by generating a test event and inspecting the actual data.

### Step 1: Generate a Test Event

Run your application to trigger at least one LLM call:

```bash
# For a web app, make a test request
curl -X POST http://localhost:3000/api/chat -d '{"message": "test"}'

# For a script, run it
node my-agent.js "test input"
python my_agent.py "test input"
```

### Step 2: Fetch and Inspect the Event

```bash
# Get the most recent event
olakai activity list --limit 1 --json

# Get full details (note the event ID from above)
olakai activity get EVENT_ID --json
```

### Step 3: Validate Each Component

**Check the event was received:**
```bash
olakai activity list --limit 1 --json | jq '.prompts[0] | {id, createdAt, app}'
```

If no event: Check API key, SDK initialization, and debug mode.

**Check customData is present:**
```bash
olakai activity get EVENT_ID --json | jq '.customData'
```

If missing or incomplete: Verify your SDK code passes `customData` correctly.

**Check KPIs are numeric (if configured):**
```bash
olakai activity get EVENT_ID --json | jq '.kpiData'
```

**CORRECT:**
```json
{ "My KPI": 42 }
```

**WRONG (formula stored as string):**
```json
{ "My KPI": "MyVariable" }
```

Fix with: `olakai kpis update KPI_ID --formula "MyVariable"`

**WRONG (null value):**
```json
{ "My KPI": null }
```

Fix by ensuring:
1. CustomDataConfig exists: `olakai custom-data create --name "MyVariable" --type NUMBER`
2. Field name case matches exactly (case-sensitive)
3. SDK actually sends the field in customData

### Step 4: Iterate Until Correct

```
┌────────────────────────────────────────────────────┐
│  1. Trigger LLM call (generate event)              │
│                    ↓                               │
│  2. Fetch: olakai activity get ID --json           │
│                    ↓                               │
│  3. Event exists?                                  │
│     NO → Check API key, SDK init, debug mode       │
│                    ↓                               │
│  4. customData correct?                            │
│     NO → Fix SDK customData parameter              │
│                    ↓                               │
│  5. kpiData numeric?                               │
│     NO → olakai kpis update ID --formula "X"       │
│                    ↓                               │
│  6. kpiData not null?                              │
│     NO → Create CustomDataConfig, check case       │
│                    ↓                               │
│  ✅ Integration validated                          │
└────────────────────────────────────────────────────┘
```

### Example Validation Session

```bash
# 1. Trigger a test call
$ curl -X POST localhost:3000/api/chat -d '{"message":"hello"}'
{"reply":"Hi there!"}

# 2. Fetch the event
$ olakai activity list --limit 1 --json | jq '.prompts[0].id'
"cmkeabc123"

# 3. Inspect it
$ olakai activity get cmkeabc123 --json | jq '{customData, kpiData}'
{
  "customData": {
    "userId": "user-123",
    "department": "Engineering"
  },
  "kpiData": {
    "Response Quality": 8.5
  }
}

# ✅ All values present and numeric - integration working!
```

## Common Integration Points

| Application Type | Integration Point | Recommended Approach |
|-----------------|-------------------|---------------------|
| API endpoint | Request handler | Wrap client, add user context |
| Background job | Job execution | Manual event at job completion |
| CLI tool | Command handler | Wrap client |
| Slack/Discord bot | Message handler | Wrap client with user context |
| Scheduled task | Cron function | Manual event with workflow aggregation |

## KPI Formula Reference

### Supported Operators

| Category | Operators |
|----------|-----------|
| Arithmetic | `+`, `-`, `*`, `/` |
| Comparison | `<`, `<=`, `=`, `<>`, `>=`, `>` |
| Logical | `AND`, `OR`, `NOT` |
| Conditional | `IF(condition, true_val, false_val)` |
| Null handling | `ISNA(value)`, `ISDEFINED(value)` |

### Common Formula Patterns

```bash
# Simple passthrough
--formula "StepCount"

# Percentage conversion
--formula "SuccessRate * 100"

# Conditional counting
--formula "IF(Success = 1, 1, 0)"

# Boolean detection to number
--formula "IF(PII detected, 1, 0)"
```

### Aggregation Types

| Aggregation | Use For |
|-------------|---------|
| `SUM` | Totals, counts |
| `AVERAGE` | Rates, percentages |

## Quick Reference

```typescript
// Wrap client (automatic tracking)
const openai = olakai.wrap(new OpenAI({ apiKey }), { provider: "openai" });

// Add context to calls (session grouping is automatic)
await openai.chat.completions.create(params, {
  userEmail: "user@example.com",
  task: "Customer Experience",
  customData: { key: "value" }
});

// Manual event (for aggregation or non-OpenAI)
olakai.event({
  prompt: "input",
  response: "output",
  tokens: 1500,
  requestTime: 5000,
  task: "Data Processing & Analysis",
  customData: { workflowId: "abc" }
});
```

```python
# Auto-instrumentation
olakai_config(api_key)
instrument_openai()

# Context for calls
with olakai_context(userEmail="user@example.com", task="Support"):
    response = client.chat.completions.create(...)

# Manual event
olakai_event(OlakaiEventParams(
    prompt="input",
    response="output",
    tokens=1500,
    customData={"key": "value"}
))
```
