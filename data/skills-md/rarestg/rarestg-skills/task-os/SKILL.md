---
name: task-os
description: >-
  Operating protocol that uses Taskwarrior as the continuity layer across
  conversations. Grounds every interaction in real task state before acting.
  Activate on "morning" / "briefing" for daily overview, on "status" /
  "what's next" for current state, when capturing tasks ("remind me to",
  "add task", "I need to"), when recovering from stalls, or when executing
  structured work across projects, repos, and life domains.
---

# Task OS

Taskwarrior (`task`) is the source of truth — not memory, not chat history,
not assumptions. Ground every interaction in task state before acting.

## Orient

Before acting on any request, check current state:

```bash
task next limit:10             # highest urgency
task +OVERDUE list             # past due
task +waiting list             # blocked on others
```

For software tasks, also check the repo:
```bash
git -C <repo-path> status --short
git -C <repo-path> log --oneline -5
```

Skip git checks for non-code domains (stocks, life, errands).

After orienting, fix state hygiene:
- Every active project should have at least one `+next` task.
- Re-evaluate stale `+waiting` tasks.
- Close work that's already done but not yet marked.

## Periodic check-in

When waking on a timer or heartbeat with no user message:

1. Orient (as above).
2. Check for stalls — any active task with no recent progress?
3. If something is stalled, attempt recovery.
4. If there's a clear `+next` task with no blockers, pick it up.
5. If nothing needs attention, go idle. Don't manufacture work.

## Morning briefing

When the user starts their day ("morning", "briefing", "what's on today"):

```bash
task +OVERDUE list
task +TODAY list
task +next list
task +WEEK list
task summary
```

Deliver a concise rundown:
- Overdue (needs attention now)
- Due today
- Top next actions across projects
- Anything waiting that may have unblocked

Keep it scannable — short lines, no wide tables. This lands on a phone screen.

## Quick capture

Any "remind me", "I need to", "add a task", or loose intent → straight to inbox:

```bash
task add project:inbox "The thing they said"
```

Assign project/tags/priority only if the user provides enough context.
Otherwise capture fast, organize later.

## Execution

### Evidence over claims

Progress means different things per domain:
- **Code:** a commit, a file written, a test result.
- **Stocks/research:** an annotation, an analysis note, a saved artifact.
- **Life/errands:** marking the task done is sufficient.

Never say "I worked on X" without pointing to the result.

### One thing at a time

Break work into steps. Finish and record each before moving to the next.

### Task lifecycle

```
task add project:X "Do the thing" +next
task <id> start
task <id> annotate "what happened, what's left"
task <id> done
task add project:X "Next step" +next
```

When blocked:
```
task <id> modify +blocked
task add project:X "Unblock: <reason>" +next
```

When waiting on someone/something:
```
task <id> modify +waiting
task <id> annotate "Waiting on: <who/what>"
```

## Stall detection

Flag work as stalled when:
- An active task has no progress and no annotation since it was started.
- A previous attempt failed with no retry or blocker task created.
- A plan was made but no execution task exists.
- The user asked for something and no task captures it.

## Recovery

1. Root-cause in one sentence.
2. Record it: `task <id> annotate "Stalled: <cause>"`.
3. Create a path forward:
   - Blocker task if external (`+blocked` or `+waiting`)
   - Retry task with narrower scope (`+next`)
4. Execute the smallest viable next step.
5. Report the state change.

## State hygiene

After completing work or ending a conversation:

1. Every piece of in-progress work has a task.
2. Tasks have enough annotations for someone with zero prior context.
3. Every active project has a `+next` task.
4. Blockers and open questions are captured.

This is not optional. Future conversations depend on clean state.

## Weekly review

When the user says "review" or "weekly review":

1. Process inbox to zero — assign project, tags, priority, or delete.
2. Review `+waiting` — anything unblocked? Poke anyone?
3. Review `+OVERDUE` — reschedule or escalate.
4. Check each project has a `+next` task: `task summary`.
5. Review `+someday` — promote or drop.
6. Show completed this week: `task end.after:today-7d completed`.
7. Show burndown: `task burndown.weekly`.

## Status report

When the user asks "status":

**Active** — what's in flight
**Done** — what completed (with evidence)
**Blocked** — what's stuck and why
**Next** — what comes after

Short. Concrete. No filler.

## Conventions

### Project hierarchy

```
work.{org}.{repo}            # software projects
stocks.{TICKER}              # per-ticker analysis
stocks.macro                 # market-level
life.{area}                  # health, finances, errands, travel
personal.{area}              # personal projects
inbox                        # unprocessed capture
```

Run `task projects` first. Follow existing structure before creating new ones.

### Dynamic grouping

Start narrow — one task or sub-project per distinct concern:
```
stocks.AAPL                        # single ticker
inbox.jodie_lamp                   # one conversation thread
work.acme.backend_auth             # one work stream
```

When multiple tasks share context, consolidate under a topic:
```
inbox.nordic_lamps_feb2026         # absorbs jodie_lamp + marcus_lamp + ikea_order
stocks.ai_chip_plays               # groups NVDA + AMD analysis
work.acme.q1_launch                # groups backend_auth + frontend_onboarding
```

- Name grouped projects by topic, not by source, once it's multi-party.
- Move existing tasks into the new parent rather than duplicating.
- This applies everywhere: inbox threads, stock themes, work initiatives, research topics.

### Tags

**State:** `+next` `+waiting` `+blocked` `+someday`
**Type:** `+bug` `+feature` `+refactor` `+research` `+review`
**Effort:** `+quick` (< 15 min) `+deep` (focused session)

### Priorities

- `H` — blocking others or time-sensitive
- `M` — important, not urgent
- `L` — nice to have
- None — backlog

## Communication

- Short, stateful updates. What changed, what's next.
- Don't announce intent — do the thing, then report.
- Surface blockers proactively.
- Format for a phone screen: short lines, no wide tables, scannable.
