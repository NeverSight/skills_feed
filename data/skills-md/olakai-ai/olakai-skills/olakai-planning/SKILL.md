---
name: olakai-planning
description: >
  Structure Olakai implementation plans to survive context clearing.

  AUTO-INVOKE when: Creating a plan for Olakai monitoring, writing implementation
  steps for AI observability, planning agent creation or SDK integration, entering
  plan mode for Olakai work, designing monitoring architecture.

  TRIGGER KEYWORDS: plan, implementation plan, steps, roadmap, architecture,
  design, olakai plan, monitoring plan, agent plan, planning, plan mode.

  DO NOT load for: Executing implementation (use olakai-create-agent or
  olakai-add-monitoring), troubleshooting (use olakai-troubleshoot), generating
  reports (use generate-analytics-reports).
license: MIT
metadata:
  author: olakai
  version: "1.8.0"
---

# Olakai Implementation Planning Guide

You are creating a plan for Olakai AI monitoring that will be executed by an agent **WITHOUT your current context**. After plan approval, context may be cleared. The executing agent will NOT have access to:

- Your conversation history
- The olakai-expert agent knowledge
- Implicit understanding of Olakai patterns
- Skills loaded in this session

**Your plan must be completely self-contained.**

---

## Plan Format Template

Every Olakai implementation plan MUST follow this structure:

```markdown
# Implementation Plan: [Task Name]

## Skill Reference
| Task | Invoke Skill | Description |
|------|--------------|-------------|
| [task] | `/skill-name` | [what it does] |

## Prerequisites (Verify First)
- [ ] CLI installed: `which olakai` returns a path
- [ ] Authenticated: `olakai whoami` shows user info
- [ ] (If applicable): Agent exists: `olakai agents list --json`

---

## Step N: [Step Title]

**Invoke skill**: `/olakai-create-agent` (or appropriate skill)
**Why this skill**: [Brief explanation of what guidance this skill provides]

### What to do:
[Detailed instructions that make sense without prior context]

### Commands:
```bash
[Exact commands with explanations]
```

### Validation:
```bash
[Commands to verify this step worked]
```

### If this fails:
Invoke `/olakai-troubleshoot` with symptoms: [describe what might go wrong]

---

## Final Validation (Golden Rule)

```bash
# 1. Trigger a test event
[How to run the agent once]

# 2. Fetch the event
olakai activity list --agent-id AGENT_ID --limit 1 --json
olakai activity get EVENT_ID --json | jq '{customData, kpiData}'

# 3. Verify:
# - customData contains expected fields
# - kpiData shows NUMBERS (not strings like "MyVariable")
# - kpiData shows VALUES (not null)
```

**If validation fails**: Invoke `/olakai-troubleshoot`
```

---

## Skill Reference Cheatsheet

**CRITICAL**: Include this table in your plan so the executing agent knows which skill to use for each task.

| Task | Invoke Skill | What It Provides |
|------|--------------|------------------|
| Not authenticated / CLI missing | `/olakai-get-started` | Install CLI, login, create first agent with API key |
| Build new agent from scratch | `/olakai-create-agent` | Full agent setup with KPIs, CustomDataConfigs, SDK code |
| Add monitoring to existing code | `/olakai-add-monitoring` | Wrap existing LLM calls, add customData, minimal changes |
| Something not working | `/olakai-troubleshoot` | Diagnose missing events, wrong KPIs, SDK errors |
| Generate usage reports | `/generate-analytics-reports` | Terminal-based analytics without web UI |
| Create implementation plan | `/olakai-planning` | This skill - structure plans for context clearing |

**Every step involving Olakai work MUST specify which skill to invoke.**

---

## Context Injection Snippets

Include these in your plan steps. They will NOT be available after context clears.

### Workflow Hierarchy (Required)

**Include this in any step involving agent creation:**

```
IMPORTANT: Every agent MUST belong to a workflow

1. Create workflow FIRST: olakai workflows create --name "Name"
2. Create agent with workflow: olakai agents create --workflow WORKFLOW_ID ...

Even single agents need a parent workflow for:
- Future multi-agent expansion
- Workflow-level KPI aggregation
- Proper organizational hierarchy
```

### The customData → KPI Pipeline

**Include this explanation in any step involving KPIs or customData:**

```
IMPORTANT: How customData becomes KPIs

SDK customData → CustomDataConfig (Schema) → Context Variable → KPI Formula → kpiData

Key rules:
1. SDK accepts ANY JSON in customData
2. But ONLY CustomDataConfig fields become KPI variables
3. Create CustomDataConfigs FIRST, then write SDK code
4. Field names in SDK must EXACTLY match CustomDataConfig names
5. KPIs are UNIQUE PER AGENT — each KPI belongs to one agent only
6. If multiple agents need the same KPI, create it separately for each
7. CustomDataConfigs are account-level (shared), but KPIs are agent-level (NOT shared)

What NOT to send in customData (already tracked):
- sessionId, agentId (automatic)
- userEmail (use parameter instead)
- timestamp, tokens, model, provider (automatic)

Only send: KPI variables + fields for filtering/grouping
```

### SDK Quick Reference - TypeScript

**Include in any step involving TypeScript SDK:**

```typescript
// Installation: npm install @olakai/sdk

import { OlakaiSDK } from "@olakai/sdk";
import OpenAI from "openai";

// Initialize (once at startup)
const olakai = new OlakaiSDK({
  apiKey: process.env.OLAKAI_API_KEY!,
  debug: true  // Enable for troubleshooting
});
await olakai.init();

// Wrap your OpenAI client
const openai = olakai.wrap(
  new OpenAI({ apiKey: process.env.OPENAI_API_KEY }),
  { provider: "openai" }
);

// Make calls with customData (fields MUST match CustomDataConfigs)
const response = await openai.chat.completions.create(
  { model: "gpt-4", messages: [...] },
  {
    userEmail: "user@example.com",
    task: "task-name",
    customData: {
      fieldName: value,  // Must match a CustomDataConfig
    }
  }
);
```

### SDK Quick Reference - Python

**Include in any step involving Python SDK:**

```python
# Installation: pip install olakai-sdk

import os
from openai import OpenAI
from olakaisdk import olakai_config, instrument_openai, olakai_context

# Initialize (once at startup)
olakai_config(
    os.getenv("OLAKAI_API_KEY"),
    debug=True  # Enable for troubleshooting
)
instrument_openai()

# Create client after instrumentation
client = OpenAI()

# Make calls with context (fields MUST match CustomDataConfigs)
with olakai_context(
    userEmail="user@example.com",
    task="task-name",
    customData={
        "fieldName": value,  # Must match a CustomDataConfig
    }
):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[...]
    )
```

### CLI Commands Reference

**Include in any step involving CLI operations:**

```bash
# Authentication
olakai login              # Interactive login
olakai whoami             # Check current user
olakai logout             # Log out

# Agents
olakai agents list [--json]
olakai agents create --name "Name" --with-api-key [--json]
olakai agents get AGENT_ID [--json]

# Activity/Events
olakai activity list [--limit N] [--agent-id ID] [--json]
olakai activity get EVENT_ID [--json]

# KPIs (agent-specific: each KPI belongs to ONE agent, cannot be shared)
olakai kpis list --agent-id ID [--json]
olakai kpis create --name "Name" --formula "X" --agent-id ID
olakai kpis validate --formula "X" --agent-id ID
olakai kpis update KPI_ID --formula "X"

# CustomData (account-level: shared across ALL agents, unlike KPIs)
olakai custom-data list [--json]
olakai custom-data create --name "Name" --type NUMBER|STRING
```

---

## Example: Complete Self-Contained Plan

Here's a model plan that an agent can follow after context is cleared:

```markdown
# Implementation Plan: Add Monitoring to Support Chatbot

## Skill Reference
| Task | Skill | Description |
|------|-------|-------------|
| Add monitoring | `/olakai-add-monitoring` | SDK integration, customData setup |
| Create KPIs | `/olakai-add-monitoring` | KPI creation and formula setup |
| Troubleshoot | `/olakai-troubleshoot` | Diagnose any issues |

## Prerequisites
- [ ] CLI installed: `which olakai`
- [ ] Authenticated: `olakai whoami`
- [ ] Agent exists for this app: `olakai agents list --json`

---

## Step 1: Define Custom Data Schema

**Invoke skill**: `/olakai-add-monitoring` (Section: "Define Your Schema First")

### What to do:
Create CustomDataConfigs for fields we'll track. These MUST exist before SDK sends data, or fields won't become KPI variables.

**IMPORTANT - The customData → KPI Pipeline:**
```
SDK customData → CustomDataConfig → Context Variable → KPI Formula → kpiData
Only CustomDataConfig fields can be used in KPI formulas!
```

### Commands:
```bash
# Check existing configs
olakai custom-data list --json

# Create required configs (run each command)
olakai custom-data create --name "ticketCategory" --type STRING
olakai custom-data create --name "resolutionTime" --type NUMBER
olakai custom-data create --name "customerSatisfaction" --type NUMBER
```

### Validation:
```bash
olakai custom-data list --json | jq '.[] | {name, type}'
# Should show all 3 fields with correct types
```

### If this fails:
Invoke `/olakai-troubleshoot` with symptoms: "custom-data create command failing"

---

## Step 2: Create KPIs

**Invoke skill**: `/olakai-add-monitoring` (Section: "Create KPIs")

### What to do:
Create KPI formulas using CustomDataConfig field names as variables. Variable names must match CustomDataConfig names exactly (case-insensitive in formulas).

### Commands:
```bash
# Get your agent ID first
AGENT_ID=$(olakai agents list --json | jq -r '.[0].id')

# Create KPIs
olakai kpis create --name "Avg Resolution Time" --formula "AVG(resolutionTime)" --agent-id $AGENT_ID
olakai kpis create --name "CSAT Score" --formula "AVG(customerSatisfaction)" --agent-id $AGENT_ID

# Verify formulas are valid
olakai kpis validate --formula "AVG(resolutionTime)" --agent-id $AGENT_ID
```

### Validation:
```bash
olakai kpis list --agent-id $AGENT_ID --json
# Should show 2 KPIs with status "active" or similar
```

### If this fails:
Invoke `/olakai-troubleshoot` with symptoms: "KPI formula validation failing" or "KPI shows null values"

---

## Step 3: Add SDK Integration

**Invoke skill**: `/olakai-add-monitoring` (Section: "SDK Integration")

### What to do:
Wrap the existing OpenAI client and pass customData with every LLM call. Field names MUST exactly match the CustomDataConfigs from Step 1.

### TypeScript pattern:
```typescript
import { OlakaiSDK } from "@olakai/sdk";
import OpenAI from "openai";

// Initialize once at startup
const olakai = new OlakaiSDK({ apiKey: process.env.OLAKAI_API_KEY! });
await olakai.init();

// Wrap your client
const openai = olakai.wrap(
  new OpenAI({ apiKey: process.env.OPENAI_API_KEY }),
  { provider: "openai" }
);

// In your chat handler - customData fields match CustomDataConfigs:
const response = await openai.chat.completions.create(
  { model: "gpt-4", messages },
  {
    userEmail: user.email,
    task: "support-chat",
    customData: {
      ticketCategory: ticket.category,      // STRING
      resolutionTime: elapsedSeconds,       // NUMBER
      customerSatisfaction: rating          // NUMBER
    }
  }
);
```

### Validation:
Run the code once with test data, then proceed to Step 4.

---

## Step 4: Validate with Golden Rule

**Invoke skill**: `/olakai-troubleshoot` if any issues found

### Commands:
```bash
# Wait 30 seconds for event to process, then fetch
AGENT_ID=$(olakai agents list --json | jq -r '.[0].id')
olakai activity list --agent-id $AGENT_ID --limit 1 --json

# Get the event ID from above output, then:
EVENT_ID="[paste from above]"
olakai activity get $EVENT_ID --json | jq '{customData, kpiData}'
```

### Expected output:
```json
{
  "customData": {
    "ticketCategory": "billing",
    "resolutionTime": 45,
    "customerSatisfaction": 4
  },
  "kpiData": {
    "Avg Resolution Time": 45,
    "CSAT Score": 4
  }
}
```

### Red flags - invoke `/olakai-troubleshoot` if you see:
| Symptom | Problem |
|---------|---------|
| kpiData values are strings like `"resolutionTime"` | Formula using wrong variable |
| kpiData values are `null` | CustomDataConfig missing or wrong type |
| customData missing fields | SDK not sending them |
| No events appearing | SDK init issue or wrong API key |
```

---

## Planning Checklist

Before finalizing your plan, verify:

- [ ] **Skill Reference table** at the top with all skills needed
- [ ] **Every Olakai step** specifies which skill to invoke and why
- [ ] **Prerequisites section** includes CLI and auth checks
- [ ] **CustomDataConfigs** are created BEFORE SDK code references them
- [ ] **KPI formulas** use variable names that match CustomDataConfigs
- [ ] **SDK code snippets** are complete (imports, initialization, usage)
- [ ] **Validation commands** use `--json` flag for parseability
- [ ] **Golden Rule** validation step with expected output
- [ ] **Troubleshooting skill** referenced for handling failures
- [ ] **"If this fails"** section on each step

---

## For the Executing Agent

If you're reading this plan after context was cleared:

1. **Check the Skill Reference table** at the top of the plan
2. **Each step tells you which skill to invoke** - use `/skill-name` to load detailed guidance
3. **Run prerequisites first** - don't skip CLI/auth checks
4. **Follow the validation commands** - they confirm each step worked
5. **If something fails**, invoke `/olakai-troubleshoot` for diagnosis

The skills contain comprehensive implementation guidance. This plan provides structure and sequence; the skills provide the domain expertise.

---

## When NOT to Use This Skill

- **For executing implementation**: Use `/olakai-create-agent` or `/olakai-add-monitoring`
- **For troubleshooting**: Use `/olakai-troubleshoot`
- **For generating reports**: Use `/generate-analytics-reports`
- **For simple tasks**: If the task is a single step, just invoke the appropriate skill directly

This skill is specifically for **structuring multi-step plans** that need to survive context clearing and be executable by an agent without prior knowledge of Olakai patterns.
