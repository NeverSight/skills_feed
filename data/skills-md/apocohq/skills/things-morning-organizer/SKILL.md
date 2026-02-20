---
name: things-morning-organizer
description: "Morning review and prioritization of Things todos. Use this skill every morning, or whenever the user asks to review, triage, categorize, or prioritize their Things tasks. Also trigger when the user says things like 'what should I work on today', 'organize my todos', 'morning routine', or 'daily review'."
metadata:
  author: apoco
  version: "1.0.1"
  argument-hint: "[silent|learning]"
---

# Morning Review

Help the user start their day by organizing their Things todos and providing a clear, prioritized briefing.

## Step 0. Load Configuration

Check for `assets/config.json` in this skill's directory.

**If config exists** → Load it and proceed to Step 1.

**If config does NOT exist** → Auto-generate it:

1. Fetch areas (`things_get_areas`) and tags (`things_get_tags`)
2. Fetch todos across all lists (`things_get_today`, `things_get_anytime`, `things_get_upcoming`, `things_get_someday`) to infer what each area and tag is used for
3. Generate short descriptions and examples for each area and tag based on the todos they contain
4. Ask the user if they have any daily routine todos (recurring tasks to auto-create on weekdays), or skip if they don't
5. Present the generated config for confirmation, then save to `assets/config.json`
6. Proceed to Step 1

### Config Format

```json
{
  "areas": {
    "work": {
      "description": "Day job tasks, meetings, team communication",
      "examples": ["Prepare slides for team standup", "Coordinate with project lead"]
    },
    "personal": {
      "description": "Family, home, errands, health",
      "examples": ["Book a doctor appointment", "Handle home admin"]
    }
  },
  "tags": {
    "important": {
      "description": "Has a hard deadline, scheduled meeting, or clear strategic urgency",
      "examples": ["Finish something by a deadline", "Prepare for a scheduled meeting"]
    },
    "waiting": {
      "description": "Explicitly blocked on another person — waiting for someone or pending a response",
      "examples": ["Waiting for a review or approval", "Pending a response"]
    },
    "quick": {
      "description": "Single-step task under 15 minutes — not multi-step work",
      "examples": ["Reply to a message", "Check a status", "Approve a request"]
    }
  },
  "daily_routine": [
    { "title": "Check email", "area": null },
    { "title": "Review calendar", "area": null }
  ]
}
```

Areas, tags, and daily routines are fully customizable. The examples above are defaults — the user defines what fits their workflow. A `null` area means uncategorized.

Each area and tag has up to 10 examples. Examples should cover distinct categories without overlap — no need to fill all 10 slots, just enough to represent the range. Area examples should include domain context to distinguish between areas (e.g. "Coordinate with IBM team"). Tag examples should be generic patterns about the nature of the task (e.g. "Reply to a message").

## Step 1. Gather Data

Call in parallel: `things_get_today`, `things_get_inbox`, `things_get_areas`, `things_get_anytime`

Check day of week with `date` (working days Mon-Fri have daily habits).

## Step 2. Categorize, Move & Tag

Process items from Today, Inbox, and Anytime that are missing an area or tags. Skip items that already have them.

### A. Categorize Uncategorized Items

For items without an area, use the config area descriptions and examples to determine the best fit and move with `things_update_todo`. If a todo doesn't clearly fit any area, flag it in the briefing.

### B. Tag Untagged Items

For items without tags, use the config tag descriptions and examples to determine which apply. **Be conservative** — only apply a tag when the todo title clearly and obviously matches the tag description and is similar to the examples. Do not infer or guess.

**Wait for all `things_update_todo` calls to complete before proceeding.**

## Step 3. Create Daily Routine Todos (Weekdays Only)

Check if the todos from `daily_routine` in config exist in Today. If missing, create each with `things_add_todo` set to today, with the area from config.

Match flexibly (case-insensitive, similar wording counts). Skip on weekends.

## Step 4. Prioritize & Brief

Use Peter Drucker's "Effective Executive" lens — prioritize by contribution, not busyness. *"First things first, second things not at all."*

**🔴 Must do** — Deadlines, meetings, items tagged as important. *"What can only I do that, if done really well, will make a real difference?"*
**🟡 Should do** — High-impact strategic work. *"What is the greatest contribution I can make?"*
**🟢 Could do** — Non-urgent items, learning, low-priority personal.
**📋 Daily Routine** — Items from `daily_routine` in config.

Output brief summary:
```
Good morning! [weekend note if applicable]

> "[Relevant Drucker quote for the day]"

🔴 Must do (X)
- **[item]** — [why this matters today]

🟡 Should do (X)
- **[item]**

🟢 Could do (X)
- **[item]**

📋 Daily Routine
- [routine items from config]

Categorized: X items moved
[Ambiguous items if any]
[Drucker-inspired closing nudge — e.g. "You have 3 must-dos. Protect your morning for the one that only you can do." or "Heavy list today — what can you delegate or defer?"]
```

Keep it tight. 30 seconds to read max.

## Creating Todos

If no config exists yet, run Step 0 first.

When the user asks to add a todo to Things:

1. **Rephrase for clarity** — Convert the user's message into a clear, actionable todo title in English
2. **Assign to area** — Use config area descriptions and examples to pick the best fit; default to the first area if ambiguous
3. **Schedule appropriately** — Use `when="today"` by default, or adjust based on context
4. **Extract details** — If the message contains specific information (names, numbers, deadlines), include them in the title or notes

## Silent Mode

Activate when the argument is "silent" (e.g. `/things-morning-organizer silent`). Designed for automated/headless execution via `-p` mode.

**Requirements:**
- Config MUST already exist — if `assets/config.json` is missing, output an error message and exit
- Skip Step 0 entirely (no configuration, no questions)
- Execute Steps 1 → 2 → 3 → 4 in a single pass
- Do NOT ask any questions or wait for user input
- Do NOT use `AskUserQuestion` tool
- Output ONLY the final briefing from Step 4 (no intermediate status messages)

## Learning Mode

Activate when the user asks to run in learning mode (e.g. "learning mode", "learn", "improve config").

1. Load `assets/config.json`
2. Fetch todos across all lists (`things_get_today`, `things_get_anytime`, `things_get_upcoming`, `things_get_someday`)
3. Compare todos against the current config and identify gaps:
   - Todos that don't fit any existing area well
   - Todos where no tag description clearly applies but a tag probably should
   - Area or tag descriptions that are too narrow to cover the todos they contain
4. Propose config updates — refine area and tag descriptions, add/rotate examples, add new areas or tags if needed
5. Present the diff to the user for confirmation, then save to `assets/config.json`
6. Ask the user if they want to proceed with the normal morning review (Steps 1-4)

## Principles

- Don't change scheduling (today/tomorrow/someday) — but inbox items without a clear schedule should be moved to Today if actionable, or flagged in the briefing
- **NEVER delete or mark todos complete** unless user explicitly requests it
- Be opinionated about priority
- Focus on contribution and impact
