---
name: clawdtalk-client
version: 2.0.0
description: ClawdTalk — Voice calls, SMS, and AI Missions for Clawdbot
metadata: {"clawdbot":{"emoji":"📞","requires":{"bins":["bash","node","jq","python3"]}}}
---

# ClawdTalk

Voice calling, SMS messaging, and AI Missions for Clawdbot. Call your bot by phone, send texts, or run autonomous multi-step outreach campaigns — powered by ClawdTalk.

---

# ⚠️ CRITICAL: SLUG CONSISTENCY

`init` auto-generates a slug from the mission name (lowercased, spaces → hyphens).
**Every command that takes a slug (`setup-agent`, `save-memory`, `complete`) MUST use the EXACT same slug.**

Mismatched slugs = agent not linked = scheduled events invisible on the frontend.

```bash
# After init, ALWAYS confirm the slug:
python scripts/telnyx_api.py list-state
# Output: find-window-washing-contractors: Find window washing contractors [running]
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ COPY-PASTE THIS. NEVER ABBREVIATE.
```

---

# ⚠️ CRITICAL: YOU OWN THE MISSION LIFECYCLE

**The server does NOT automatically update plan steps or mission status.** That is YOUR job as the bot. If you don't update steps and complete the mission, the UI will show "Running" forever with all steps "Pending".

## Your Responsibilities

For every mission, YOU must:
1. **Update plan steps** — mark each step `in_progress` → `completed` (or `failed`)
2. **Log events** — after every significant action
3. **Poll for completion** — check if scheduled calls/SMS finished
4. **Complete the mission** — mark the run as `succeeded` or `failed`
5. **Clean up** — remove any polling cron jobs when the mission ends

The UI reflects exactly what you tell it. No updates from you = no updates on screen.

---

# 🚨 MANDATORY: SAVE TO MEMORY AFTER EVERY ACTION

**Every significant action MUST be persisted using `save-memory` or `append-memory` IMMEDIATELY after the action succeeds.** The frontend reads from server memory. If you don't save it, it doesn't show up. `log-event` alone is NOT enough.

> **Rule: If you did something, save it to memory. No exceptions. No "I'll do it later." Do it NOW.**

Example (scheduling an SMS):
```bash
# 1. Schedule it
python scripts/telnyx_api.py schedule-sms $AID "$TO" "$FROM" "$DATETIME" "$MESSAGE" $MID $RID $STEP_ID

# 2. IMMEDIATELY save to memory
python scripts/telnyx_api.py append-memory "$SLUG" "scheduled_events" \
  '{"event_id": "<id>", "type": "sms", "to": "<to>", "message": "<msg>", "scheduled_at": "<dt>", "step_id": "<step>"}'

# 3. Then log the event
python scripts/telnyx_api.py log-event $MID $RID custom "Scheduled SMS event_id=<id>" $STEP_ID
```

**Skipping step 2 is the #1 cause of "nothing shows on the frontend" bugs.**

---

# 🚨 MANDATORY: CHECK MISSION STATUS AFTER EVERY STEP

**After completing or failing ANY step, you MUST check whether the mission should be completed or failed.** Never leave a mission in "running" state when it's actually done or dead.

> **Rule: After every step change, ask yourself: is this mission finished?**

### Decision tree (run after EVERY step):

```
Step finished →
  ├── Succeeded?
  │     ├── All steps done? → COMPLETE MISSION (update-run succeeded)
  │     ├── More steps remain? → Continue to next step
  │     └── Only verify left? → Set up polling cron
  └── Failed?
        ├── Recoverable (retry/reschedule)? → Retry
        └── Unrecoverable? → FAIL MISSION NOW:
              1. update-step <step_id> failed
              2. log-event error "Failed: <reason>" <step_id>
              3. save-memory "$SLUG" "error_<step_id>" '{"error": "...", "recoverable": false}'
              4. update-run $MID $RID failed
              5. save-memory "$SLUG" "result" '{"status": "failed", "reason": "...", "failed_step": "..."}'
              6. Clean up any polling cron jobs
```

**A mission stuck in "running" when it's actually done or dead is a bug. The user sees it and thinks work is still happening.**

---

# Architecture Overview

## How It Fits Together

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  You (Bot)   │────▶│  ClawdTalk Server │────▶│  Telnyx API  │
│              │     │  (dev/prod)       │     │  (cloud)     │
│ telnyx_api.py│     │  Local DB + proxy │     │  Executes    │
│              │     │  to Telnyx        │     │  calls/SMS   │
└──────────────┘     └──────────────────┘     └──────────────┘
```

- **telnyx_api.py** — Python CLI script. Every command you run goes through this. It talks to the ClawdTalk server, never directly to Telnyx.
- **ClawdTalk Server** — Node.js backend. Stores missions, assistants, and events in a local Postgres DB. Proxies requests to the Telnyx API.
- **Telnyx API** — Cloud service. Actually makes the calls and sends the SMS at the scheduled time.

## Key Files

| File | Purpose |
|---|---|
| `scripts/telnyx_api.py` | CLI tool for all mission/assistant/event operations |
| `scripts/connect.sh` | WebSocket client for inbound voice call routing |
| `skill-config.json` | API key and server URL |
| `.missions_state.json` | Local state tracking for active missions |
| `.connect.log` | WebSocket connection logs |

## Two Sets of IDs

Every entity exists in two places with different IDs:
- **Local DB ID** — what the ClawdTalk server returns (e.g. `3df24dde-...`)
- **Telnyx ID** — what the Telnyx API uses internally

The script always works with local IDs. You don't need to worry about Telnyx IDs.

---

## Quick Start

1. **Sign up** at [clawdtalk.com](https://clawdtalk.com)
2. **Add your phone** in Settings
3. **Get API key** from Dashboard
4. **Run setup**: `./setup.sh`
5. **Start connection**: `./scripts/connect.sh start`

## Voice Calls

The WebSocket client routes calls to your gateway's main agent session, giving full access to memory, tools, and context.

```bash
./scripts/connect.sh start     # Start connection
./scripts/connect.sh stop      # Stop
./scripts/connect.sh status    # Check status
```

### Outbound Calls

Have the bot call you or others:

```bash
./scripts/call.sh                              # Call your phone
./scripts/call.sh "Hey, what's up?"            # Call with greeting
./scripts/call.sh --to +15551234567            # Call external number*
./scripts/call.sh --to +15551234567 "Hello!"   # External with greeting
./scripts/call.sh status <call_id>             # Check call status
./scripts/call.sh end <call_id>                # End call
```

*External calls require a paid account with a dedicated number. The AI will operate in privacy mode when calling external numbers (won't reveal your private info).

## SMS

Send and receive text messages:

```bash
./scripts/sms.sh send +15551234567 "Hello!"
./scripts/sms.sh list
./scripts/sms.sh conversations
```

## AI Missions (Full Tracking via Python)

For complex, multi-step missions with full tracking, state persistence, retries, and conversation insights, use the Python-based missions API.

**Required**: Python 3.7+, `CLAWDTALK_API_KEY` environment variable. Optionally set `CLAWDTALK_API_URL` to override the default endpoint (defaults to `https://clawdtalk.com/v1`).

```bash
python scripts/telnyx_api.py check-key    # Verify setup
```

# CRITICAL: SAVE STATE FREQUENTLY

**You MUST save your progress after EVERY significant action.** If the session crashes or restarts, unsaved work is LOST.

## Two-Layer Persistence: Memory + Events

Always save to BOTH:
1. **Local Memory** (`.missions_state.json`) - Fast, survives restarts
2. **Events API** (cloud) - Permanent audit trail, survives local file loss

## When to Save (After EVERY action!)

| Action | Save Memory | Log Event |
|--------|-------------|-----------|
| Web search returns results | append-memory | log-event (tool_call) |
| Found a contractor/lead | append-memory | log-event (custom) |
| Created assistant | save-memory | log-event (custom) |
| Assigned phone number | save-memory | log-event (custom) |
| Scheduled a call/SMS | append-memory | log-event (custom) |
| Call completed | save-memory | log-event (custom) |
| Got quote/insight | save-memory | log-event (custom) |
| Made a decision | save-memory | log-event (message) |
| Step started | save-memory | update-step (in_progress) + log-event (step_started) |
| Step completed | save-memory | update-step (completed) + log-event (step_completed) |
| Step failed | save-memory | update-step (failed) + log-event (error) |
| Error occurred | save-memory | log-event (error) |

## Memory Commands (Local Backup)

```bash
# Save a single value
python scripts/telnyx_api.py save-memory "<slug>" "key" '{"data": "value"}'

# Append to a list (great for collecting multiple items)
python scripts/telnyx_api.py append-memory "<slug>" "contractors" '{"name": "ABC Co", "phone": "+1234567890"}'

# Retrieve memory
python scripts/telnyx_api.py get-memory "<slug>"           # Get all memory
python scripts/telnyx_api.py get-memory "<slug>" "key"     # Get specific key
```

## Event Commands (Cloud Backup)

```bash
# Log an event (step_id is REQUIRED - links event to a plan step)
python scripts/telnyx_api.py log-event <mission_id> <run_id> <type> "<summary>" <step_id> '[payload_json]'

# Event types: tool_call, custom, message, error, step_started, step_completed
# step_id: Use the step_id from your plan (e.g., "research", "setup", "calls")
#          Use "-" if event doesn't belong to a specific step
```

---

## When to Use Missions

This skill has two modes: **full missions** (tracked, multi-step) and **simple calls** (one-off, no mission overhead). Pick the right one.

### Use a Full Mission When:
- The task involves **multiple calls or SMS** (batch outreach, surveys, sweeps)
- You need a **complete audit trail** with events, plans, and state tracking
- The task is **multi-step** and takes significant effort across phases
- **Retries and failure tracking** matter
- You need to **compare results** across multiple calls

Examples:
- "Find me window washing contractors in Chicago, call them and negotiate rates"
- "Contact all leads in this list and schedule demos"
- "Call 10 weather stations and find the hottest one"

### Do NOT Use a Mission When:
- The task is a **single outbound call** — just create an assistant (or reuse one) and schedule the call directly
- It's a **one-off SMS** — schedule it and done
- The task doesn't need tracking, plans, or state recovery
- You'd be creating a mission with one step and one call — that's overengineering

**For simple calls, just:**
```bash
# Reuse or create an assistant
python scripts/telnyx_api.py list-assistants --name=<relevant>
# Schedule the call
python scripts/telnyx_api.py schedule-call <assistant_id> <to> <from> <datetime> <mission_id> <run_id>
# Poll for completion
python scripts/telnyx_api.py get-event <assistant_id> <event_id>
# Get insights
python scripts/telnyx_api.py get-insights <conversation_id>
```

No mission, no run, no plan. Keep it simple.

## State Persistence

The script automatically manages state in `.missions_state.json`. This survives restarts and supports multiple concurrent missions.

```bash
python scripts/telnyx_api.py list-state                              # List all active missions
python scripts/telnyx_api.py get-state "find-window-washing-contractors"  # Get state for specific mission
python scripts/telnyx_api.py remove-state "find-window-washing-contractors" # Remove mission from state
```

---

# Core Workflow

## Phase 1: Initialize Tracking

### Step 1.1: Create a Mission

```bash
python scripts/telnyx_api.py create-mission "Brief descriptive name" "Full description of the task"
```

**Save the returned `mission_id`** - you'll need it for all subsequent calls.

### Step 1.2: Start a Run

```bash
python scripts/telnyx_api.py create-run <mission_id> '{"original_request": "The exact user request", "context": "Any relevant context"}'
```

**Save the returned `run_id`**.

### Step 1.3: Create a Plan

Before executing, outline your plan:

```bash
python scripts/telnyx_api.py create-plan <mission_id> <run_id> '[
  {"step_id": "step_1", "description": "Research contractors online", "sequence": 1},
  {"step_id": "step_2", "description": "Create voice agent for calls", "sequence": 2},
  {"step_id": "step_3", "description": "Schedule calls to each contractor", "sequence": 3},
  {"step_id": "step_4", "description": "Monitor call completions", "sequence": 4},
  {"step_id": "step_5", "description": "Analyze results and select best options", "sequence": 5}
]'
```

### Step 1.4: Set Run to Running

```bash
python scripts/telnyx_api.py update-run <mission_id> <run_id> running
```

### High-Level Alternative: Initialize Everything at Once

Use the `init` command to create mission, run, plan, and set status in one step:

```bash
python scripts/telnyx_api.py init "Find window washing contractors" "Find contractors in Chicago, call them, negotiate rates" "User wants window washing quotes" '[
  {"step_id": "research", "description": "Find contractors online", "sequence": 1},
  {"step_id": "setup", "description": "Create voice agent", "sequence": 2},
  {"step_id": "calls", "description": "Schedule and make calls", "sequence": 3},
  {"step_id": "analyze", "description": "Analyze results", "sequence": 4}
]'
```

This also automatically resumes if a mission with the same name already exists.

**⚠️ Immediately after `init`, run `list-state` and copy the exact slug. Use it for ALL subsequent commands.**

---

## Phase 2: Voice/SMS Agent Setup

When your task requires making calls or sending SMS, create an AI assistant first.

### Step 2.1: Create a Voice/SMS Assistant

**For phone calls:**
```bash
python scripts/telnyx_api.py create-assistant "Contractor Outreach Agent" "You are calling on behalf of [COMPANY]. Your goal is to [SPECIFIC GOAL]. Be professional and concise. Collect: [WHAT TO COLLECT]. If they cannot talk now, ask for a good callback time." "Hi, this is an AI assistant calling on behalf of [COMPANY]. Is this [BUSINESS NAME]? I am calling to inquire about your services. Do you have a moment?" '["telephony", "messaging"]'
```

**For SMS:**
```bash
python scripts/telnyx_api.py create-assistant "SMS Outreach Agent" "You send SMS messages to collect information. Keep messages brief and professional." "Hi! I am reaching out on behalf of [COMPANY] regarding [PURPOSE]. Could you please reply with [REQUESTED INFO]?" '["telephony", "messaging"]'
```

**Save the returned `assistant_id`**.

### Step 2.2: Find and Assign a Phone Number

```bash
python scripts/telnyx_api.py get-available-phone                          # Get first available
python scripts/telnyx_api.py get-connection-id <assistant_id> telephony   # Get connection ID
python scripts/telnyx_api.py assign-phone <phone_number_id> <connection_id> voice  # Assign
```

### High-Level Alternative: Setup Agent in One Step

```bash
python scripts/telnyx_api.py setup-agent "find-window-washing-contractors" "Contractor Caller" "You are calling to get quotes for commercial window washing. Ask about: rates per floor, availability, insurance. Be professional." "Hi, I am calling to inquire about your commercial window washing services. Do you have a moment to discuss rates?"
```

This automatically creates the assistant, links it to the mission run, finds an available phone number, assigns it, and saves all IDs to the state file.

**⚠️ The slug MUST match what `init` created. If it doesn't, the agent won't be linked and scheduled events won't appear on the frontend.**

**Verify linking worked immediately after:**
```bash
python scripts/telnyx_api.py list-linked-agents <mission_id> <run_id>
# Must show your assistant_id. If empty → slug was wrong. Fix with:
python scripts/telnyx_api.py link-agent <mission_id> <run_id> <assistant_id>
```

### Step 2.3: Link Agent to Mission Run

**If using `setup-agent`**: Linking is done automatically (only if slug matches `init`).

**If setting up manually**:
```bash
python scripts/telnyx_api.py link-agent <mission_id> <run_id> <assistant_id>
python scripts/telnyx_api.py list-linked-agents <mission_id> <run_id>
python scripts/telnyx_api.py unlink-agent <mission_id> <run_id> <assistant_id>
```

---

## Phase 3: Scheduling Calls/SMS

### Business Hours Consideration

**CRITICAL**: Before scheduling calls, consider business hours (9 AM - 5 PM local time). `scheduled_at` must be in the future (at least 1 minute from now).

```bash
python scripts/telnyx_api.py schedule-call <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" <mission_id> <run_id>
python scripts/telnyx_api.py schedule-sms <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" "Your message here"
```

**Save the returned event `id`**.

---

## Phase 4: Monitoring Call Completion

### ⚠️ THIS IS THE MOST IMPORTANT PART

After scheduling a call or SMS, **Telnyx executes it autonomously** at the scheduled time. You need to **poll** to find out when it's done, then update the mission accordingly.

### Check Scheduled Event Status

```bash
python scripts/telnyx_api.py get-event <assistant_id> <event_id>
```

### Use Cron Jobs to Poll

Use your bot's cron system to schedule polling. **Do NOT block the main session waiting.** Match the poll interval to the expected wait time:

| Expected completion | Poll interval | Example |
|---|---|---|
| < 5 minutes | Every 30 seconds | SMS sent 1 min from now |
| 5–30 minutes | Every 2–5 minutes | Call scheduled in 15 min |
| 1–24 hours | Every 15–30 minutes | Call scheduled for tonight |
| Days/weeks | Every 4–8 hours | Call scheduled for next week |

**If you know the exact scheduled time**, don't start polling until after that time. Schedule your first poll for `scheduled_time + 2 minutes`.

### Cron Job Pattern

When you schedule a call/SMS, create a cron job to poll for it:

```
Create cron: poll at appropriate interval
  → Run get-event <assistant_id> <event_id>
  → If completed: update step, log event, complete mission if last step, DELETE THIS CRON
  → If failed: update step as failed, log error, DELETE THIS CRON
  → If pending/in_progress: do nothing, cron runs again at next interval
```

**⚠️ ALWAYS clean up cron jobs when a mission reaches a terminal state (completed, failed, cancelled). Never leave polling crons running after a mission ends.**

### Adjusting Poll Frequency

You can update the cron interval as circumstances change:
- Scheduled for 2 weeks from now? Start with 8-hour polling.
- As the scheduled time approaches (within 1 hour), tighten to 5-minute intervals.
- After the scheduled time passes, tighten to 30-second intervals.

### Event Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Waiting for scheduled time | Keep polling |
| `in_progress` | Call/SMS in progress | Keep polling |
| `completed` | Finished successfully | Update step, get insights if call |
| `failed` | Failed after retries | Update step as failed, consider retry |

### Call Status Values (Phone Calls Only)

| call_status | Meaning | Action |
|-------------|---------|--------|
| `ringing` | Phone is ringing | Poll again in 1-2 minutes |
| `in-progress` | Call is active | Poll again in 2-3 minutes |
| `completed` | Call finished normally | Get insights |
| `no-answer` | Nobody picked up | **Retryable** — reschedule |
| `busy` | Line is busy | **Retryable** — retry in 10-15 min |
| `canceled` | Call was canceled | Check if intentional |
| `failed` | Network/system error | **Retryable** — retry in 5-10 min |

---

## Phase 5: Getting Conversation Insights

Once a call completes with a `conversation_id`, retrieve insights. **Poll until status is "completed"** (wait 10 seconds between retries).

```bash
python scripts/telnyx_api.py get-insights <conversation_id>
```

Telnyx automatically creates default insight templates when an assistant is created. You don't need to manage these — just read the results.

---

## Phase 6: Complete the Mission

```bash
python scripts/telnyx_api.py update-run <mission_id> <run_id> succeeded

# Or with full results:
python scripts/telnyx_api.py complete "find-window-washing-contractors" <mission_id> <run_id> "Summary of results" '{"key": "payload"}'
```

---

# Event Logging Reference

**Log EVERY action as an event.** Always update step status via `update-step` AND log corresponding events.

```bash
# When STARTING a step:
python scripts/telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "research" "in_progress"
python scripts/telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" step_started "Starting: Research" "research"

# When COMPLETING a step:
python scripts/telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "research" "completed"
python scripts/telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" step_completed "Completed: Research" "research"

# When a step FAILS:
python scripts/telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "calls" "failed"
python scripts/telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" error "Failed: Could not reach contractors" "calls"
```

---

# Quick Reference: All Python Commands

```bash
# Check setup
python scripts/telnyx_api.py check-key

# Missions
python scripts/telnyx_api.py create-mission <name> <instructions>
python scripts/telnyx_api.py get-mission <mission_id>
python scripts/telnyx_api.py list-missions

# Runs
python scripts/telnyx_api.py create-run <mission_id> <input_json>
python scripts/telnyx_api.py get-run <mission_id> <run_id>
python scripts/telnyx_api.py update-run <mission_id> <run_id> <status>
python scripts/telnyx_api.py list-runs <mission_id>

# Plan
python scripts/telnyx_api.py create-plan <mission_id> <run_id> <steps_json>
python scripts/telnyx_api.py get-plan <mission_id> <run_id>
python scripts/telnyx_api.py update-step <mission_id> <run_id> <step_id> <status>

# Events
python scripts/telnyx_api.py log-event <mission_id> <run_id> <type> <summary> <step_id> [payload_json]
python scripts/telnyx_api.py list-events <mission_id> <run_id>

# Assistants
python scripts/telnyx_api.py list-assistants [--name=<filter>] [--page=<n>] [--size=<n>]
python scripts/telnyx_api.py create-assistant <name> <instructions> <greeting> [options_json]
python scripts/telnyx_api.py get-assistant <assistant_id>
python scripts/telnyx_api.py update-assistant <assistant_id> <updates_json>
python scripts/telnyx_api.py get-connection-id <assistant_id> [telephony|messaging]

# Phone Numbers
python scripts/telnyx_api.py list-phones [--available]
python scripts/telnyx_api.py get-available-phone
python scripts/telnyx_api.py assign-phone <phone_id> <connection_id> [voice|sms]

# Scheduled Events
python scripts/telnyx_api.py schedule-call <assistant_id> <to> <from> <datetime> <mission_id> <run_id>
python scripts/telnyx_api.py schedule-sms <assistant_id> <to> <from> <datetime> <text>
python scripts/telnyx_api.py get-event <assistant_id> <event_id>
python scripts/telnyx_api.py cancel-scheduled-event <assistant_id> <event_id>
python scripts/telnyx_api.py list-events-assistant <assistant_id>

# Insights
python scripts/telnyx_api.py get-insights <conversation_id>

# Mission Run Agents
python scripts/telnyx_api.py link-agent <mission_id> <run_id> <telnyx_agent_id>
python scripts/telnyx_api.py list-linked-agents <mission_id> <run_id>
python scripts/telnyx_api.py unlink-agent <mission_id> <run_id> <telnyx_agent_id>

# State Management
python scripts/telnyx_api.py list-state
python scripts/telnyx_api.py get-state <slug>
python scripts/telnyx_api.py remove-state <slug>

# Memory
python scripts/telnyx_api.py save-memory <slug> <key> <value_json>
python scripts/telnyx_api.py get-memory <slug> [key]
python scripts/telnyx_api.py append-memory <slug> <key> <item_json>

# High-Level Workflows
python scripts/telnyx_api.py init <name> <instructions> <request> [steps_json]
python scripts/telnyx_api.py setup-agent <slug> <name> <instructions> <greeting>
python scripts/telnyx_api.py complete <slug> <mission_id> <run_id> <summary> [payload_json]
```

---

# Complete Example: SMS Mission with Cron Polling

Here's the full flow for an SMS mission with proper lifecycle tracking and cron-based polling:

```bash
# 1. Init mission
python scripts/telnyx_api.py init "SMS Test 003" \
  "Send a test SMS to +13322200013" \
  "SMS test with full tracking" \
  '[{"step_id": "setup", "description": "Create SMS agent", "sequence": 1},
    {"step_id": "sms", "description": "Schedule SMS", "sequence": 2},
    {"step_id": "verify", "description": "Verify delivery", "sequence": 3}]'
# Save: mission_id, run_id

# 2. Step 1: Setup agent
python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID setup in_progress
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_started "Starting: Create SMS agent" setup

python scripts/telnyx_api.py setup-agent "sms-test-003" "SMS Agent" "Send test messages" "Test from bot"
# Save: assistant_id, phone_number

python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID setup completed
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_completed "Completed: Created assistant $ASSISTANT_ID" setup

# 3. Step 2: Schedule SMS
python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID sms in_progress
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_started "Starting: Schedule SMS" sms

python scripts/telnyx_api.py schedule-sms $ASSISTANT_ID "+13322200013" "$PHONE" "2026-02-19T18:43:00Z" \
  "What do you call a bear with no teeth? A gummy bear!" \
  $MISSION_ID $RUN_ID sms
# Save: event_id

python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID sms completed
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_completed "Completed: SMS scheduled" sms

# 4. Step 3: Verify delivery — CREATE A CRON JOB TO POLL
python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID verify in_progress
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_started "Starting: Poll for delivery" verify

# >>> Create a cron job that fires AFTER the scheduled time <<<
# >>> Cron runs: get-event $ASSISTANT_ID $EVENT_ID <<<
# >>> On completed: update-step verify completed, log-event, update-run succeeded, DELETE CRON <<<
# >>> On failed: update-step verify failed, log-event, update-run failed, DELETE CRON <<<
# >>> On pending/in_progress: do nothing, cron fires again next interval <<<

# 5. (Cron fires, detects completion)
python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID verify completed
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_completed "Completed: SMS delivered" verify
python scripts/telnyx_api.py update-run $MISSION_ID $RUN_ID succeeded
# DELETE the polling cron job!
```

---

# Mission Classes

Not all missions are the same. Identify which class before planning.

```
Does call N depend on results of call N-1?
  YES -> Is it negotiation (leveraging previous results)?
    YES -> Class 3: Sequential Negotiation
    NO  -> Does it have distinct rounds with human approval?
      YES -> Class 4: Multi-Round / Follow-up
      NO  -> Class 5: Information Gathering -> Action
  NO  -> Do you need structured scoring/ranking?
    YES -> Class 2: Parallel Screening with Rubric
    NO  -> Class 1: Parallel Sweep
```

## Class 1: Parallel Sweep
Fan out calls in parallel batches. Same question to many targets. Schedule all calls in one batch (stagger by 1-2 min). Analysis happens after ALL calls complete.

## Class 2: Parallel Screening with Rubric
Fan out calls in parallel with structured scoring criteria. Results are ranked post-hoc via insights.

## Class 3: Sequential Negotiation
Calls MUST run serially. Each call's strategy depends on previous results. Use `update-assistant` between calls to inject context. **Never parallelize these.**

## Class 4: Multi-Round / Follow-up
Two or more distinct phases. Round 1 is broad outreach, human approval gate, then Round 2 targets a subset.

## Class 5: Information Gathering -> Action
Call to find something, then act on it. Early termination when goal is met — cancel remaining calls.

---

# Operational Guide

## Default Tools
The `send_dtmf` tool is included by default. Most outbound calls hit an IVR first.

## IVR Navigation
Expect IVRs even when calling businesses. Instruct the assistant to press 0 or say 'representative'.

## Call Limits and Throttling
Stagger calls in batches of 5-10, space scheduled times 1-2 minutes apart, monitor for 429 errors.

## Answering Machine Detection (AMD)
- **Enable** for human contacts (leave voicemail or skip machines)
- **Disable** for IVR systems, businesses with phone trees — set action to `continue_assistant`

## Polling for Results: Use Cron Jobs
After scheduling calls, set up a cron job to poll periodically. Don't block the main session.

## Retry Strategy
Track every number's status in mission memory. Retry based on recipient type:
- **Automated systems**: retry in 5-15 min, up to 3 times
- **Service industry**: retry in 30 min - 2 hours, avoid peak hours
- **Professionals**: retry next business day, leave one voicemail max

---

## Approval Requests (Sensitive Actions)

For destructive or sensitive actions during voice calls, request user approval first:

```bash
./scripts/approval.sh request "Delete GitHub repo myproject"
./scripts/approval.sh request "Send $500 to John" --biometric
./scripts/approval.sh request "Post tweet about X" --details "Full text: ..."
```

**When to request approval:**
- Deleting repos, files, or data
- Sending money or making purchases
- Posting to social media
- Sending emails/messages to others
- Any irreversible action

**Response values:**
- `approved` → Execute the action, confirm completion
- `denied` → Tell user "Okay, I won't do that"
- `timeout` → "I didn't get a response, should I try again?"
- `no_devices` → Skip approval, action not executed (no mobile app)

**Example flow in voice call:**
1. User: "Delete my test-repo on GitHub"
2. You: "I'll need your approval for that. Check your phone."
3. Run: `approval.sh request "Delete GitHub repo test-repo"`
4. If approved: Delete the repo, then say "Done, test-repo has been deleted"
5. If denied: "Got it, I won't delete it"

## Gateway Requirements

Voice calls route requests to the main agent via `sessions_send`. This tool is **blocked by default** on the Gateway HTTP tools API. You must explicitly allow it:

```json5
// In openclaw.json → gateway.tools
{
  "gateway": {
    "tools": {
      "allow": ["sessions_send"]
    }
  }
}
```

Or via CLI: `openclaw config patch '{"gateway":{"tools":{"allow":["sessions_send"]}}}'`

Without this, voice calls will connect but the agent won't be able to process any requests (deep tool calls return 404).

## ❌ Common Pitfalls

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Different slug for `init` vs `setup-agent` | Scheduled events missing from frontend | `list-state` after `init`, copy-paste slug |
| Forgetting `save-memory` after actions | Frontend shows nothing | Save immediately after every action |
| Not checking mission status after step changes | Mission stuck "running" forever | Run decision tree after every step |
| Leaving polling crons running | Wasted resources, stale polls | Delete cron on any terminal state |
| Not verifying `list-linked-agents` after `setup-agent` | Agent not linked, events invisible | Always verify, fix with `link-agent` |

## Configuration

Edit `skill-config.json`:

| Option | Description |
|--------|-------------|
| `api_key` | API key from clawdtalk.com |
| `server` | Server URL (default: `https://clawdtalk.com`) |
| `owner_name` | Your name (auto-detected from USER.md) |
| `agent_name` | Agent name (auto-detected from IDENTITY.md) |
| `greeting` | Custom greeting for inbound calls |

Environment variables for the Python missions API:
- `CLAWDTALK_API_KEY` — your ClawdTalk API key (required for missions)
- `CLAWDTALK_API_URL` — override the API endpoint (default: `https://clawdtalk.com/v1`)

## Troubleshooting

- **Auth failed**: Regenerate API key at clawdtalk.com
- **Empty responses**: Run `./setup.sh` and restart gateway
- **Slow responses**: Try a faster model in your gateway config
- **Debug mode**: `DEBUG=1 ./scripts/connect.sh restart`
- **Missions API key**: Run `python scripts/telnyx_api.py check-key` to verify
- **JSON parsing errors**: Use single quotes around JSON arguments
