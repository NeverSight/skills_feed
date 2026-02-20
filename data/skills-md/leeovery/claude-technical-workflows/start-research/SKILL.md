---
name: start-research
description: "Start a research exploration using the technical-research skill. For early-stage ideas, feasibility checks, and broad exploration before formal discussion."
disable-model-invocation: true
allowed-tools: Bash(.claude/hooks/workflows/write-session-state.sh)
hooks:
  PreToolUse:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/workflows/system-check.sh"
          once: true
---

Invoke the **technical-research** skill for this conversation.

## Workflow Context

This is **Phase 1** of the six-phase workflow:

| Phase             | Focus                                              | You    |
|-------------------|----------------------------------------------------|--------|
| **1. Research**   | EXPLORE - ideas, feasibility, market, business     | ◀ HERE |
| 2. Discussion     | WHAT and WHY - decisions, architecture, edge cases |        |
| 3. Specification  | REFINE - validate into standalone spec             |        |
| 4. Planning       | HOW - phases, tasks, acceptance criteria           |        |
| 5. Implementation | DOING - tests first, then code                     |        |
| 6. Review         | VALIDATING - check work against artifacts          |        |

**Stay in your lane**: Explore freely. This is the time for broad thinking, feasibility checks, and learning. Surface options and tradeoffs — don't make decisions. When a topic converges toward a conclusion, that's a signal it's ready for discussion phase, not a cue to start deciding. Park it and move on.

---

## Instructions

Follow these steps EXACTLY as written. Do not skip steps or combine them. Present output using the EXACT format shown in examples - do not simplify or alter the formatting.

**CRITICAL**: This guidance is mandatory.

- After each user interaction, STOP and wait for their response before proceeding
- Never assume or anticipate user choices
- Even if the user's initial prompt seems to answer a question, still confirm with them at the appropriate step
- Complete each step fully before moving to the next
- Do not act on gathered information until the skill is loaded - it contains the instructions for how to proceed

---

## Step 0: Run Migrations

**This step is mandatory. You must complete it before proceeding.**

Invoke the `/migrate` skill and assess its output.

**If files were updated**: STOP and wait for the user to review the changes (e.g., via `git diff`) and confirm before proceeding to Step 1. Do not continue automatically.

**If no updates needed**: Proceed to Step 1.

---

## Step 1: Gather Context

Load **[gather-context.md](references/gather-context.md)** and follow its instructions as written.

→ Proceed to **Step 2**.

---

## Step 2: Invoke the Skill

Before invoking the processing skill, save a session bookmark.

> *Output the next fenced block as a code block:*

```
Saving session state so Claude can pick up where it left off if the conversation is compacted.
```

```bash
.claude/hooks/workflows/write-session-state.sh \
  "{topic}" \
  "skills/technical-research/SKILL.md" \
  "docs/workflow/research/{topic}.md"
```

Load **[invoke-skill.md](references/invoke-skill.md)** and follow its instructions as written.
