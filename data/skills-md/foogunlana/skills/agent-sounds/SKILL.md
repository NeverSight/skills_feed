---
name: agent-sounds
description: Add audible notifications (chimes) to Claude Code and other coding agents. Provides a small script that plays configurable sounds on common lifecycle hooks like plan completion, task completion, errors, and long-running command completion. Defaults work out of the box on macOS (system sounds) with cross-platform fallbacks.
---

# Agent Sounds

This skill adds audible cues (like an "oven ding") to agent workflows by running a tiny local script that plays a configured sound for a given hook event.

## Quick Start

1. Generate a default config (optional):

```bash
python3 .claude/skills/agent-sounds/scripts/agent_sounds.py init
```

2. When a hook happens, run:

```bash
python3 .claude/skills/agent-sounds/scripts/agent_sounds.py emit plan.done
```

If no config exists, defaults are used (macOS system sounds when available, otherwise terminal bell).

## Hooks (Recommended Defaults)

Use these hook names consistently so different agents and workflows can share the same config:

- `plan.done` - when the final plan is complete (your "oven ding")
- `task.done` - when a user-visible task is completed
- `run.done` - when a long-running command finishes
- `error` - when the agent hits an error or needs attention
- `waiting` - when the agent is blocked waiting for user input

## Default Behavior In This Skill

When this skill is active, follow these rules:

1. After producing a plan (a numbered plan or clearly labeled "Plan"), immediately emit `plan.done`.
2. After implementing a user request and finishing verification (tests/lint/build), emit `task.done`.
3. After running a command that took noticeable time, emit `run.done`.
4. If an error occurs (failed command, exception, missing dependency), emit `error` after you present the next action to the user.
5. If you ask the user a question and must wait, emit `waiting` right after the question.

## Onboarding Flow (First Use)

If `.claude/agent-sounds.json` does not exist:

1. Create it with a sensible default mapping (see `references/config-guide.md`).
2. Offer the user a short customization pass:
   - Choose the "ding" sound for `plan.done`
   - Choose whether `error` should be louder/different
   - Enable/disable any hooks they find noisy

## Configuration

Config lives at `.claude/agent-sounds.json`.

- Schema, defaults, and examples: `references/config-guide.md`
- How to integrate with other agent frameworks: `references/integrations.md`
