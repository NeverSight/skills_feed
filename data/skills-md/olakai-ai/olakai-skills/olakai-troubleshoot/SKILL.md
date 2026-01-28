---
name: olakai-troubleshoot
description: >
  Troubleshoot Olakai monitoring issues when something isn't working.

  AUTO-INVOKE when user mentions: events not appearing, KPIs showing wrong values,
  KPIs showing strings instead of numbers, custom data missing, null KPIs,
  authentication errors, CLI not working, events not associated with agent,
  monitoring broken, SDK errors, or any Olakai-related problem.

  TRIGGER KEYWORDS: olakai, troubleshoot, debug, not working, events missing,
  KPI wrong, KPI null, KPI string, customData missing, authentication failed,
  CLI error, no events, events not appearing, diagnose, fix olakai, broken,
  SDK error, monitoring issue, API key invalid, events not tracked.

  DO NOT load for: initial setup (use olakai-create-agent or olakai-add-monitoring),
  or generating reports (use generate-analytics-reports).
license: MIT
metadata:
  author: olakai
  version: "1.8.0"
---

# Troubleshoot Olakai Agent Monitoring

This skill helps diagnose and fix common issues with Olakai AI agent monitoring, KPI calculations, and SDK integration.

For full documentation, see: https://app.olakai.ai/llms.txt

## The Golden Rule: Test → Fetch → Validate

**Always diagnose by generating a real event and inspecting it.** Don't guess - look at the actual data.

```bash
# 1. Trigger your agent/app to generate an event
# 2. Fetch the event
olakai activity list --agent-id YOUR_AGENT_ID --limit 1 --json

# 3. Inspect it completely
olakai activity get EVENT_ID --json | jq '{customData, kpiData}'
```

This reveals exactly what's happening:
- No event? → SDK/API key problem
- customData missing fields? → SDK code problem
- kpiData shows strings? → Formula storage problem
- kpiData shows null? → CustomDataConfig or field name problem

---

## Quick Diagnosis Commands

Run these first to understand the current state:

```bash
# Check CLI authentication
olakai whoami

# List recent events (are any coming through?)
olakai activity list --limit 10

# List agents (is your agent registered?)
olakai agents list

# List custom data configs (are they set up?)
olakai custom-data list

# List KPIs for an agent
olakai kpis list --agent-id YOUR_AGENT_ID
```

---

## Issue: No Events Appearing

### Symptom
Events from your agent aren't showing up in `olakai activity list` or the dashboard.

### Diagnostic Steps

**1. Verify API Key**
```bash
# Check environment variable is set
echo $OLAKAI_API_KEY

# Should start with "sk_" and be ~40+ characters
# If empty or wrong, set it:
export OLAKAI_API_KEY="sk_your_key_here"
```

**2. Check SDK Initialization**

TypeScript - ensure `init()` is awaited:
```typescript
const olakai = new OlakaiSDK({ apiKey: process.env.OLAKAI_API_KEY! });
await olakai.init();  // <-- Must await this!
```

Python - ensure config is called before instrumentation:
```python
olakai_config(os.getenv("OLAKAI_API_KEY"))  # <-- Must be first
instrument_openai()  # <-- Then instrument
```

**3. Enable Debug Mode**

TypeScript:
```typescript
const olakai = new OlakaiSDK({
  apiKey: process.env.OLAKAI_API_KEY!,
  debug: true,  // <-- Add this
});
```

Python:
```python
olakai_config(api_key, debug=True)
```

Look for error messages in console output.

**4. Test Direct API Call**

```bash
curl -X POST "https://app.olakai.ai/api/monitoring/prompt" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $OLAKAI_API_KEY" \
  -d '{
    "prompt": "Test prompt",
    "response": "Test response",
    "app": "test-agent"
  }'
```

Expected: `200 OK` with event ID
If `401`: Invalid API key
If `400`: Check request format

**5. Check Network/Firewall**

Ensure your environment can reach `https://app.olakai.ai`

```bash
curl -I https://app.olakai.ai/api/health
```

### Common Fixes

| Problem | Solution |
|---------|----------|
| API key not set | Export `OLAKAI_API_KEY` environment variable |
| Wrong API key | Generate new key via CLI: `olakai agents create --with-api-key` |
| `init()` not awaited | Add `await` before `olakai.init()` |
| SDK not wrapping client | Ensure you're using the returned wrapped client |
| Firewall blocking | Whitelist `app.olakai.ai` |

---

## Issue: KPIs Showing String Values Instead of Numbers

### Symptom
KPI values display as `"VariableName"` instead of numeric values like `42`.

Example:
```json
"kpiData": {
  "Tools Discovered": "ToolsDiscovered",  // Wrong: string
  "New Tools Found": "NewToolsFound"       // Wrong: string
}
```

Should be:
```json
"kpiData": {
  "Tools Discovered": 20,  // Correct: number
  "New Tools Found": 3     // Correct: number
}
```

### Root Cause

KPI formulas are stored as raw strings instead of parsed AST objects.

### Diagnostic Steps

**1. Check KPI Formula Storage**

```bash
olakai kpis list --agent-id YOUR_AGENT_ID --json | jq '.[] | {name, calculatorParams}'
```

**Wrong** (raw string):
```json
{
  "name": "Tools Discovered",
  "calculatorParams": {
    "formula": "ToolsDiscovered"  // <-- String, not object
  }
}
```

**Correct** (AST object):
```json
{
  "name": "Tools Discovered",
  "calculatorParams": {
    "formula": {
      "type": "variable",
      "name": "ToolsDiscovered"
    }
  }
}
```

**2. Check CustomDataConfig Exists**

```bash
olakai custom-data list --json | jq '.[].name'
```

Ensure every variable referenced in KPI formulas has a corresponding CustomDataConfig.

### Fix

**Option A: Update via CLI (Recommended)**

The CLI now validates and parses formulas automatically:

```bash
# This will parse "ToolsDiscovered" into proper AST
olakai kpis update KPI_ID --formula "ToolsDiscovered"
```

**Option B: Validate First, Then Check**

```bash
# Validate the formula
olakai kpis validate --formula "ToolsDiscovered" --agent-id YOUR_AGENT_ID

# Should return:
# {
#   "valid": true,
#   "type": "number",
#   "parsedFormula": { "type": "variable", "name": "ToolsDiscovered" }
# }
```

**Option C: Recreate the KPI**

```bash
# Delete the broken KPI
olakai kpis delete KPI_ID --force

# Create with proper formula (CLI now parses automatically)
olakai kpis create \
  --name "Tools Discovered" \
  --agent-id YOUR_AGENT_ID \
  --calculator-id formula \
  --formula "ToolsDiscovered" \
  --aggregation SUM
```

### Post-Fix Verification

After fixing, trigger a new event and check:

```bash
olakai activity list --agent-id YOUR_AGENT_ID --limit 1 --json | jq '.prompts[0].kpiData'
```

Should now show numeric values.

---

## Issue: CustomData Not Appearing in Events

### Symptom
You're sending `customData` but it's not showing in event details.

### Diagnostic Steps

**1. Check Event Details**

```bash
olakai activity get EVENT_ID --json | jq '.customData'
```

If `null` or missing fields, the SDK isn't sending them.

**2. Verify SDK Code**

TypeScript - customData in call options:
```typescript
const response = await openai.chat.completions.create(
  { model: "gpt-4o", messages },
  {
    customData: {
      myField: "value",      // <-- Check this is present
      myNumber: 42,
    },
  }
);
```

TypeScript - customData in manual event:
```typescript
olakai.event({
  prompt,
  response,
  customData: {
    myField: "value",
    myNumber: 42,
  },
});
```

**3. Check Field Names Match CustomDataConfig**

Field names are **case-sensitive**. Ensure exact match:

```bash
# What you configured
olakai custom-data list --json | jq '.[].name'
# Output: "ToolsDiscovered", "NewToolsFound"

# What you're sending (must match exactly)
customData: {
  ToolsDiscovered: 20,    // Correct
  toolsDiscovered: 20,    // WRONG - case mismatch
  tools_discovered: 20,   // WRONG - different format
}
```

### Common Fixes

| Problem | Solution |
|---------|----------|
| Field name case mismatch | Match exact case from `custom-data list` |
| customData not in options | Move to second argument of `create()` |
| Missing CustomDataConfig | Create with `olakai custom-data create --name X --type NUMBER` |
| Sending wrong data type | NUMBER fields need numbers, STRING fields need strings |

---

## Issue: customData Fields Not Available in KPIs

### Symptom
You're sending fields in `customData` but they can't be used in KPI formulas - they don't appear as available variables.

### Root Cause

**The SDK accepts any JSON in `customData`, but only fields with CustomDataConfigs become KPI variables.**

```
SDK customData → CustomDataConfig (Schema) → Context Variable → KPI Formula
                        ↑
                  REQUIRED for field
                  to be usable in KPIs
```

Fields without CustomDataConfigs:
- ✅ Are stored in the event record
- ❌ Cannot be referenced in KPI formulas
- ❌ Don't appear in formula variable suggestions
- ❌ Effectively wasted for analytics purposes

### Diagnostic

**1. List what CustomDataConfigs exist:**
```bash
olakai custom-data list --json | jq '.[].name'
```

**2. Compare to what you're sending in SDK:**
```typescript
// If you're sending these fields:
customData: {
  ItemsProcessed: 10,   // Is there a CustomDataConfig for this?
  SuccessRate: 0.95,    // Is there a CustomDataConfig for this?
  RandomField: "xyz",   // Is there a CustomDataConfig for this?
}
```

**3. Check for mismatches:**
- Field sent but no config → Cannot use in KPIs
- Config exists but field not sent → KPI shows `null`

### Fix

**Create CustomDataConfigs for every field you want to use in KPIs:**

```bash
# For each field you need in KPIs, create a config
olakai custom-data create --name "ItemsProcessed" --type NUMBER
olakai custom-data create --name "SuccessRate" --type NUMBER
olakai custom-data create --name "RandomField" --type STRING

# Verify
olakai custom-data list
```

**Best Practice:** Design your CustomDataConfigs FIRST, then write SDK code that sends only those fields.

### Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Sending extra "helpful" fields | They're ignored for KPIs | Only send registered fields |
| Different casing in SDK vs config | May cause issues | Match exact case |
| Creating KPI before CustomDataConfig | Formula can't resolve variable | Create config first |

---

## Issue: KPIs from Another Agent Not Working

### Symptom

You created KPIs for one agent and expected them to apply to a different agent. The second agent's events show no `kpiData`, or `olakai kpis list --agent-id SECOND_AGENT_ID` returns an empty list.

### Root Cause

**KPIs are unique per agent.** Each KPI definition is bound to exactly one agent by its `agentId`. KPIs cannot be shared, inherited, or reused across agents — even within the same workflow or account.

| Concept | Scope | Shared Across Agents? |
|---------|-------|-----------------------|
| **CustomDataConfig** | Account-level | ✅ Yes — created once, available to all agents |
| **KPI** | Agent-level | ❌ No — belongs to one agent only |

### Diagnostic

```bash
# Check KPIs on the FIRST agent (where they were originally created)
olakai kpis list --agent-id AGENT_A_ID --json | jq '.[].name'
# Output: "Items Processed", "Success Rate"

# Check KPIs on the SECOND agent (where you expected them to work)
olakai kpis list --agent-id AGENT_B_ID --json | jq '.[].name'
# Output: (empty) ← KPIs don't carry over
```

### Fix

Create the KPIs separately for the second agent:

```bash
# Recreate each KPI for the new agent
olakai kpis create \
  --name "Items Processed" \
  --agent-id AGENT_B_ID \
  --calculator-id formula \
  --formula "ItemsProcessed" \
  --aggregation SUM

olakai kpis create \
  --name "Success Rate" \
  --agent-id AGENT_B_ID \
  --calculator-id formula \
  --formula "SuccessRate * 100" \
  --aggregation AVERAGE
```

### Prevention

When creating a new agent, always:
1. Check if KPIs are needed: "Does this agent need performance metrics?"
2. Create KPIs explicitly for the new agent — don't assume they exist from another agent
3. Verify with `olakai kpis list --agent-id NEW_AGENT_ID`

> **Note:** CustomDataConfigs do NOT need to be recreated — they are account-level and shared. Only KPIs are agent-specific.

---

## Issue: Redundant customData Fields

### Symptom
CustomDataConfigs exist for fields that are already tracked by the platform (sessionId, agentId, timestamps, etc.), cluttering the configuration.

### Why This Happens
The SDK accepts any JSON in customData, so agents sometimes send "helpful" extra data that's already tracked elsewhere.

### What's Already Tracked (Don't Duplicate)

| Field | How It's Tracked | Don't Create Config For |
|-------|------------------|------------------------|
| Session ID | SDK automatic grouping | `sessionId`, `session` |
| Agent ID | API key association | `agentId`, `agent` |
| User email | `userEmail` parameter | `email`, `userEmail` |
| Timestamps | Event metadata | `timestamp`, `createdAt` |
| Token count | `tokens` parameter | `tokenCount`, `totalTokens` |
| Model | Auto-detected from call | `model`, `modelName` |
| Provider | Wrapped client config | `provider` |

### Fix

**1. Identify redundant configs:**
```bash
olakai custom-data list --json | jq '.[].name'
```

Look for names like: `sessionId`, `agentId`, `timestamp`, `model`, `provider`, `tokenCount`

**2. Check if they're used in KPIs:**
```bash
olakai kpis list --agent-id YOUR_AGENT_ID --json | jq '.[].calculatorParams.formula'
```

**3. If not used in KPIs, remove from SDK code:**
Don't delete the configs (they may have historical data), but stop sending these fields.

**4. Update SDK code to only send KPI-relevant fields:**
```typescript
customData: {
  // ✅ Keep: Used in KPI formulas
  ItemsProcessed: 10,
  SuccessRate: 1.0,

  // ❌ Remove: Already tracked by platform
  // sessionId: session.id,      // Already tracked
  // agentId: agentConfig.id,    // Already tracked
  // timestamp: Date.now(),      // Already tracked
}
```

### Best Practice
Before creating a CustomDataConfig, ask:
- "Will I use this in a KPI formula?" → Yes = Create
- "Will I filter events by this?" → Yes = Create
- "Is this already tracked by the platform?" → Yes = Don't create

---

## Issue: KPIs Show `null` Values

### Symptom
KPI values are `null` instead of numbers.

```json
"kpiData": {
  "Success Rate": null,
  "Items Processed": null
}
```

### Root Cause Options

1. **CustomData field not sent** - The event doesn't include that field
2. **CustomDataConfig doesn't exist** - Platform can't resolve the variable
3. **Type mismatch** - Sending string when NUMBER expected

### Diagnostic Steps

**1. Check if CustomData is Present**

```bash
olakai activity get EVENT_ID --json | jq '.customData'
```

If the field is missing from customData, the KPI can't calculate.

**2. Check CustomDataConfig Exists**

```bash
olakai custom-data list --json | jq '.[].name'
```

Every field referenced in KPI formulas needs a config.

**3. Check Formula Validity**

```bash
olakai kpis validate --formula "YourVariable" --agent-id YOUR_AGENT_ID
```

If invalid, you'll see the error.

### Fix

**1. Ensure CustomDataConfig Exists**
```bash
olakai custom-data create --name "YourVariable" --type NUMBER
```

**2. Ensure SDK Sends the Field**
```typescript
customData: {
  YourVariable: 42,  // Must be present and correct type
}
```

**3. Trigger New Event**

Old events won't recalculate. Generate a new event to verify the fix.

---

## Issue: CLI Authentication Failed

### Symptom
```
Error: Authentication required
Error: Token expired
Error: Unauthorized
```

### Fix

**1. Re-authenticate**
```bash
olakai logout
olakai login
```

**2. Verify Authentication**
```bash
olakai whoami
```

**3. Check Credentials File**
```bash
ls -la ~/.config/olakai/
cat ~/.config/olakai/credentials.json
```

Should contain `accessToken` and `refreshToken`.

**4. Check Environment**
```bash
# Default is production
olakai whoami

# For staging
OLAKAI_ENV=staging olakai whoami
```

---

## Issue: Events Not Associated with Agent

### Symptom
Events appear in general activity but not under your agent.

### Root Cause
The `app` field in events doesn't match the agent name.

### Diagnostic

```bash
# Check agent name
olakai agents list --json | jq '.[] | {id, name}'

# Check event app field
olakai activity get EVENT_ID --json | jq '.app'
```

### Fix

**Option A: Match App Name to Agent**

In your SDK code, ensure the app name matches:
```typescript
olakai.event({
  prompt,
  response,
  app: "Your Agent Name",  // Must match agent name exactly
});
```

Or with wrapped client:
```typescript
const openai = olakai.wrap(new OpenAI({ apiKey }), {
  provider: "openai",
  defaultContext: {
    app: "Your Agent Name",
  },
});
```

**Option B: Update Agent Name**

```bash
olakai agents update AGENT_ID --name "App Name From Events"
```

---

## Issue: High Latency / Slow Events

### Symptom
LLM calls take much longer when monitoring is enabled.

### Diagnostic

Check if it's the SDK or the LLM:
```typescript
const startSDK = Date.now();
const response = await openai.chat.completions.create(...);
console.log(`Total time: ${Date.now() - startSDK}ms`);
```

### Fixes

**1. SDK Uses Fire-and-Forget**

The SDK should NOT block your application. If it is:

```typescript
// Ensure you're not awaiting event()
olakai.event(params);  // No await - fire and forget
```

**2. Check Network Latency**

```bash
time curl -I https://app.olakai.ai/api/health
```

If >500ms, consider:
- Running in a region closer to US-East
- Checking for proxy/VPN overhead

**3. Disable Debug Mode in Production**

```typescript
const olakai = new OlakaiSDK({
  apiKey: process.env.OLAKAI_API_KEY!,
  debug: false,  // Disable in production
});
```

---

## Issue: Duplicate Events

### Symptom
Each LLM call creates multiple events.

### Root Cause
Usually double-initialization or multiple wrapping.

### Diagnostic

Search your code for:
- Multiple `olakai.init()` calls
- Multiple `olakai.wrap()` calls
- Multiple `instrument_openai()` calls

### Fix

**Use Singleton Pattern**

```typescript
// lib/olakai.ts
let instance: OlakaiSDK | null = null;

export async function getOlakai(): Promise<OlakaiSDK> {
  if (!instance) {
    instance = new OlakaiSDK({ apiKey: process.env.OLAKAI_API_KEY! });
    await instance.init();
  }
  return instance;
}
```

---

## Diagnostic Commands Reference

```bash
# Authentication
olakai whoami                          # Check current user
olakai login                           # Re-authenticate

# Events/Activity
olakai activity list --limit N         # Recent events
olakai activity list --agent-id ID     # Events for specific agent
olakai activity get EVENT_ID --json    # Full event details

# Agents
olakai agents list                     # All agents
olakai agents list --json | jq '.[].name'  # Just names

# KPIs
olakai kpis list --agent-id ID         # KPIs for agent
olakai kpis list --agent-id ID --json | jq '.[] | {name, calculatorParams}'
olakai kpis validate --formula "X"     # Test formula

# Custom Data
olakai custom-data list                # All configs
olakai custom-data list --json | jq '.[].name'  # Just names

# Quick Health Check
olakai whoami && olakai activity list --limit 1 && echo "OK"
```

## Troubleshooting Decision Tree

```
Events not appearing?
├── Check API key is set → export OLAKAI_API_KEY=sk_...
├── Check SDK initialized → await olakai.init()
├── Enable debug mode → debug: true
└── Test direct API → curl POST /api/monitoring/prompt

KPIs showing strings?
├── Check formula storage → olakai kpis list --json
├── Formula is raw string → olakai kpis update ID --formula "X"
└── Missing CustomDataConfig → olakai custom-data create

KPIs showing null?
├── Check customData sent → olakai activity get ID --json
├── Field missing → Add to customData in SDK
├── CustomDataConfig missing → olakai custom-data create
└── Type mismatch → NUMBER needs number, STRING needs string

customData field not usable in KPIs?
├── Check CustomDataConfig exists → olakai custom-data list
├── Config missing → olakai custom-data create --name "Field" --type NUMBER
└── Case mismatch → Ensure exact case match between SDK and config

Events not under agent?
├── Check app name matches → Compare event.app to agent.name
├── Mismatch → Update agent name or SDK app field

KPIs not appearing on new agent?
├── KPIs are agent-specific, NOT shared across agents
├── Check KPIs exist for THIS agent → olakai kpis list --agent-id THIS_AGENT_ID
├── If empty → Create KPIs for this agent (can't reuse from other agents)
└── CustomDataConfigs ARE shared → no need to recreate those
```

## Key Insight: The customData → KPI Pipeline

Only fields registered as CustomDataConfigs become available in KPI formulas:

```
SDK customData → CustomDataConfig → Context Variable → KPI Formula → kpiData
       ↓                ↓                  ↓               ↓            ↓
  Any JSON         Schema definition   Available var   Expression   Computed value
                   (REQUIRED)
```

**Common pitfall:** Sending extra fields in `customData` without CustomDataConfigs - they're stored but unusable for KPIs.
