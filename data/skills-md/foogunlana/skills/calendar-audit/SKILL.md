---
name: calendar-audit
description: Protect your deep work time. Calendar Audit scores every meeting on your calendar, calculates your deep work gap, and makes specific suggestions to reclaim focus time. Supports multiple calendar tools (screenshot, Google Calendar MCP, Apple Calendar, icalBuddy, gcalcli) and scoring frameworks (5-Dimension, Eisenhower, RACI, Value vs Effort, Custom). Value first — your first audit takes 2 minutes with just a screenshot. Just say "calendar-audit" to get going.
---

# Calendar Audit

A skill that protects deep work time by auditing your calendar and scoring every meeting.

> *Protect the maker. Score the meetings. Reclaim the time.*

## Core Design Principle

**Value first, setup later.** A new user sees their first audit within 2 minutes. No tools to install. No questions to answer first. Screenshot in, audit out.

## Two Flows

| Condition | Flow |
|-----------|------|
| No `.claude/calendar-audit.md` exists | **Onboarding Flow** — instant audit from screenshot, then setup |
| `.claude/calendar-audit.md` exists | **Regular Flow** — FAST approach, scores from configured calendar tool |

---

## Onboarding Flow (First Run Only)

**Detection:** Check if `.claude/calendar-audit.md` exists. If no config exists, run this flow. Otherwise skip to Regular Flow.

**Goal:** Deliver an audit immediately, then calibrate preferences.

### Step 1: Welcome (10 seconds)

Read `references/branding.md` and display verbatim:
1. Logo
2. Origin quote
3. Workflow diagram
4. Key concepts

Then immediately:

```
Let's audit your calendar right now. No setup needed.

Take a screenshot of your calendar for this week (the week view works best)
and paste it here.

This is a fast first pass — we can set up automated calendar access afterwards
so future audits are hands-free.
```

**Wait for screenshot.**

### Step 2: Quick Focus Question (30 seconds)

After receiving the screenshot, before auditing, ask ONE question:

```
How much focus time do you think you need each week?

Research says knowledge workers need 3-4 hours of uninterrupted focus daily.
I recommend at least 60% focus / 40% meetings — that's ~24h focus out of a
40h week, with at least one 4-hour contiguous block of deep work per day.

What feels right for you?
→ 60/40 (recommended — player-coach, technical leader)
→ 70/30 (IC-heavy, needs more building time)
→ 50/50 (manager-heavy, lots of direct reports)
→ Other
```

**Wait for answer.** Use their choice as the focus target for the audit.

### Step 3: Instant Audit (2 minutes)

Using the screenshot + focus target, immediately run the full audit:

1. **Extract events** from the screenshot using vision — for each event capture: day, time, title, duration
2. **Calculate totals** — meeting hours, focus hours, contiguous blocks, per-day breakdown (see Regular Flow Step 1a for formulas)
3. **Score every meeting** using the **5-Dimension framework as default** (no framework choice yet — that comes in setup). See `references/frameworks.md` for scoring rules.
4. **Present the full audit** in the standard output format (Red/Orange/Yellow/Green zones with suggestions — see Regular Flow Step 3 output format)
5. **Show the gap**: current vs target

Then ask:

```
Here's your audit. Take a look at the scores.

Anything look wrong? Correct any scores and I'll regenerate suggestions.
For example: "Abdul 1:1 should be Green not Yellow" or "Sales standup
score is right but I need to keep it for political reasons"
```

**Wait for corrections.** When user provides corrections:
- Update scores
- Record overrides with reasons
- Regenerate the zone tables and suggestions
- Repeat until user is satisfied

### Step 4: Full Setup (after audit is done)

Once the user is happy with the audit:

```
Great — that's your first audit done.

Let's set up so next time is automated. I'll ask a few quick questions
to save your preferences.
```

Then run the setup wizard:

```
1. What should I call you?

2. What's your role? (e.g. CTO, Engineering Manager, IC)

3. How many direct reports? (helps score 1:1s correctly)

4. Top 3 priorities that need deep work this quarter?

5. How should I access your calendar going forward?

   Zero setup (you provide data each time):
   a) Screenshot — paste an image each week
   b) Copy-paste — paste your schedule as text
   c) ICS file — export from any calendar app

   Automated (one-time setup, then hands-free):
   d) Google Calendar MCP [recommended for Google users]
   e) Apple Calendar MCP [recommended for macOS]
   f) icalBuddy [macOS CLI]
   g) gcalcli [Google Calendar CLI]

   See references/calendar-setup.md for setup instructions.

6. Which decision framework do you prefer?

   a) 5-Dimension [default] — what we just used. Scores 5 factors. Most comprehensive.
   b) Eisenhower — simple Urgent vs Important grid. Fastest.
   c) RACI — classifies your role (Accountable/Responsible/Consulted/Informed). Best for cutting meetings where you're just "Informed".
   d) Value vs Effort — scores value generated vs time invested.
   e) Custom — define your own dimensions and scoring.

   See references/frameworks.md for details on each.
```

Parse the response and use sensible defaults for skipped fields:
- role: "Engineering Leader"
- focus_ratio: value from Step 2 (default 60)
- calendar.tool: "screenshot"
- framework.name: "5-dimension"
- maker_days: ["Tuesday", "Thursday"]

If user picks Custom framework, run the guided creation flow from `references/frameworks.md` (Custom section).

Write `.claude/calendar-audit.md` config with all answers (see `references/config-guide.md` for format).

Create `.claude/modules/meeting-scores.md` with scores from the first audit (see Regular Flow Step 5 for format).

```
You're all set. Run /calendar-audit anytime — ideally Monday mornings.

Your config: .claude/calendar-audit.md
Meeting history: .claude/modules/meeting-scores.md
```

**Exit after onboarding and first audit.**

---

## Regular Flow (Every Subsequent Run)

**FAST approach — no questions, just audit:**
1. Gather context (calendar, goals, config)
2. Calculate deep work budget and gap
3. Score every meeting using configured framework
4. Present audit with specific suggestions
5. User reviews and overrides
6. Save decisions to meeting memory

### Step 1: Gather Context

#### 1a. Calendar

Read `calendar.tool` from config and pull the week's events:

| Tool | How |
|------|-----|
| `google-calendar-mcp` | Call MCP `list-events` for current week (Mon-Fri) |
| `apple-calendar-mcp` | Call MCP tool for current week |
| `icalbuddy` | Run: `icalBuddy -f "" -nc -nrd -df "%Y-%m-%d" -tf "%H:%M" eventsFrom:today to:+5d` |
| `gcalcli` | Run: `gcalcli agenda "$(date +%Y-%m-%d)" "$(date -v+5d +%Y-%m-%d)" --details all --tsv` |
| `ics-file` | Read file at `calendar.ics_path`, parse VEVENT components, filter to current week |
| `screenshot` | Ask user: "Paste a screenshot of your calendar for this week (week view works best)" — extract events via vision |
| `copy-paste` | Ask user: "Paste your schedule for this week as text" — parse events |
| `manual` | Ask user: "List your meetings for this week (name, day, time, duration)" |

- If invoked on a weekend or late Friday, pull next week instead
- Calculate:
  - **Total meeting hours** (raw duration of all meetings)
  - **Effective meeting cost** (raw hours + 15 min context-switch per meeting)
  - **Total focus hours** (remaining time after effective meeting cost)
  - **Contiguous focus blocks** (2+ hours uninterrupted by meetings)
  - **Per-day breakdown** (meetings vs focus per day)
- Flag:
  - Days without a contiguous focus block of at least `min_daily_focus` hours (default 4)
  - Days with 5+ meetings
  - Back-to-back meetings without breaks
  - Scheduling conflicts (overlapping events)

#### 1b. Goals & Work Profile

Read context to understand what deep work is needed:

- **User config** (`.claude/calendar-audit.md`) for role, priorities, preferences
- **Weekly note** (if exists) for this week's tasks — estimate deep work hours needed
- **Monthly goals** (if exists) for north star priorities
- **Meeting memory** (`.claude/modules/meeting-scores.md`) for previous scores and overrides

If no weekly note or goals exist, ask: "What's the most important deep work you need to do this week?"

#### 1c. Calculate Deep Work Budget

Based on context, calculate:

```
Deep Work Budget
────────────────
Work week:              [work_hours, default 40]h
Target focus ratio:     [focus_ratio, default 60]%
Target focus hours:     [work_hours * ratio]h
Target meeting hours:   [work_hours * (1-ratio)]h
Min daily focus block:  [min_daily_focus, default 4]h contiguous

Current meetings:       Xh (raw) / Yh (with transitions)
Current focus:          Zh
Current ratio:          Z/work_hours = N%

Gap:                    [target - current]h to reclaim
```

**Minimum thresholds (always flag if violated):**
- Every day must have at least one contiguous block of `min_daily_focus` hours (default 4h) — scattered focus doesn't count
- No day with zero focus time
- At least 1 "maker day" (4+ contiguous hours focus) per week

### Step 2: Set Deep Work Goals

Based on tasks and priorities, propose specific deep work goals with time estimates and proposed calendar slots.

**Format:**

```
## Deep Work Goals This Week

| # | Goal | Est. Time | Priority | Proposed Slot |
|---|------|-----------|----------|---------------|
| 1 | [goal from tasks/priorities] | [hours] | P1 | [day, time range] |
| 2 | [goal] | [hours] | P2 | [day, time range] |

**Total deep work needed:** Xh
**Total deep work available:** Yh
**Gap:** Zh (need to free up Z hours from meetings)
```

If there's a gap, proceed to Step 3 to find meeting time to reclaim.
If no gap, still run the audit — meeting load creeps up over time.

### Step 3: Score and Rank Meetings

Read `framework.name` from config (default: "5-dimension"). Apply that framework's scoring model from `references/frameworks.md`.

Score every non-focus, non-personal event on the calendar.

#### Framework-Specific Scoring

**5-Dimension:** Score 5 dimensions (Decision Power, Delegation, Async Potential, Frequency Fit, Duration Fit) 1-3 each. Total 5-15. Zones: Green (5-7), Yellow (8-9), Orange (10-11), Red (12-15).

**Eisenhower:** Score Urgency and Importance 1-3 each. Total 2-6. Zones: Green/Do (2), Yellow/Schedule (3), Orange/Delegate (4-5), Red/Delete (6).

**RACI:** Classify role: Accountable (Green), Responsible (Green), Consulted (Yellow), Informed (Red).

**Value vs Effort:** Score Value and Effort 1-3 each. Total 2-6. Quadrants: Quick Win/Green (2), Strategic-or-Evaluate/Yellow (3), Filler-or-Evaluate/Orange (4-5), Trap/Red (6).

**Custom:** Use dimensions and zones from `framework.custom` config.

See `references/frameworks.md` for complete scoring rules and guidelines for each framework.

#### Applying Overrides

Before presenting results, check `scoring.overrides` in config. For any meeting matching an override, use the override zone instead of the calculated score. Note in output: "(override: [reason])".

If the meeting has been scored before (from meeting memory), note any changes in score and flag if a previously optimised meeting has regressed.

#### Output Format

Present the audit sorted by zone (Red first). Use the output columns specified in `references/frameworks.md` for the active framework.

```
## Meeting Audit — Week of [date]

**Framework:** [framework name]
**Current:** Xh meetings / Yh focus (Z% focus)
**Target:** Ah meetings / Bh focus (C% focus)
**Gap:** Need to reclaim ~Dh

### Red Zone (Eliminate/Delegate) — saves ~Xh
[framework-specific columns]

### Orange Zone (Restructure) — saves ~Xh
[framework-specific columns]

### Yellow Zone (Optimise) — saves ~Xh
[framework-specific columns]

### Green Zone (Keep)
[framework-specific columns]

**Total recoverable:** ~Xh
**Projected after changes:** Xh meetings / Yh focus (Z% focus)
```

### Step 4: User Review

After presenting the audit:

1. Ask user to confirm, override, or adjust any scores
2. For overrides, record the reason (e.g. "Keep despite score — important relationship")
3. Save all decisions to meeting memory

If user is resistant to cutting a meeting, ask:
- "What would happen if you skipped this for 2 weeks as an experiment?"
- "Could you send a delegate and get a 2-line summary?"

### Step 5: Save to Meeting Memory

Update `.claude/modules/meeting-scores.md` with:
- Current scores for all meetings (with framework used)
- User overrides and reasons
- Week-over-week comparison
- Running trend (are meetings increasing or decreasing?)

If the file doesn't exist, create it:

```markdown
# Meeting Scores

> Running log of meeting audit scores and decisions.

## Current Scores

| Meeting | Last Scored | Framework | Score | Zone | User Decision | Notes |
|---------|-------------|-----------|-------|------|---------------|-------|

## Weekly Snapshots

<!-- Append weekly totals here -->

| Week | Framework | Meetings (h) | Focus (h) | Focus % | Meetings Optimised |
|------|-----------|-------------|-----------|---------|-------------------|
```

---

## Key Principles

- **Contiguous blocks matter more than total hours.** 3 hours scattered across 30-min gaps is worth less than 1 contiguous 2-hour block. The target is one 4-hour uninterrupted stretch per day — that's where real work happens.
- **Don't just count meetings — count transitions.** Each meeting has ~15 min of context-switching cost. A day with 6x30min meetings costs ~4.5h, not 3h.
- **Batch meetings on specific days** when possible. Aim for 1-2 "maker days" (mostly focus) and 2-3 "manager days" (meetings batched).
- **Morning focus is often more valuable than afternoon focus** for creative and learning work.
- **The goal is not zero meetings** — it's the right meetings at the right frequency and duration.
- **Meeting load creeps.** Without regular audits, meetings accumulate 1-2 per month. This skill is the counterweight.
- **Career items are the first to drop** when meetings increase. Deep work protection is career protection.

---

## Research & References

This skill draws from:

- **Cal Newport, Deep Work** — Knowledge workers need 3-4h of uninterrupted focus daily for meaningful output
- **Paul Graham, Maker's Schedule** — Meetings destroy maker productivity disproportionately; a single meeting can ruin a half-day
- **Parkinson's Law** — Meetings expand to fill the time allotted; default to 25min or 50min
- **Context-switching research (Gloria Mark, UC Irvine)** — Takes ~23 minutes to fully refocus after an interruption
- **Meeting cost formula** — A 1h meeting with 8 people costs 8 person-hours + 8x15min context switches = 10h of organisational productivity

---

## File Paths

| Type | Path |
|------|------|
| Config | `.claude/calendar-audit.md` |
| Meeting Memory | `.claude/modules/meeting-scores.md` |
| Calendar Setup Guide | `references/calendar-setup.md` |
| Decision Frameworks | `references/frameworks.md` |
| Config Reference | `references/config-guide.md` |
| Branding | `references/branding.md` |
| Weekly Notes | Varies by user's planning setup |
| Monthly Goals | Varies by user's planning setup |
