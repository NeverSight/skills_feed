---
name: start-specification
description: "Start a specification session from concluded discussions. Discovers available discussions, offers consolidation assessment for multiple discussions, and invokes the technical-specification skill."
disable-model-invocation: true
allowed-tools: Bash(.claude/skills/start-specification/scripts/discovery.sh), Bash(mkdir -p docs/workflow/.state), Bash(rm docs/workflow/.state/discussion-consolidation-analysis.md), Bash(.claude/hooks/workflows/write-session-state.sh)
hooks:
  PreToolUse:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/workflows/system-check.sh"
          once: true
---

Invoke the **technical-specification** skill for this conversation.

> **⚠️ ZERO OUTPUT RULE**: Do not narrate your processing. Produce no output until a step or reference file explicitly specifies display content. No "proceeding with...", no discovery summaries, no routing decisions, no transition text. Your first output must be content explicitly called for by the instructions.

## Workflow Context

This is **Phase 3** of the six-phase workflow:

| Phase                | Focus                                              | You    |
|----------------------|----------------------------------------------------|--------|
| 1. Research          | EXPLORE - ideas, feasibility, market, business     |        |
| 2. Discussion        | WHAT and WHY - decisions, architecture, edge cases |        |
| **3. Specification** | REFINE - validate into standalone spec             | ◀ HERE |
| 4. Planning          | HOW - phases, tasks, acceptance criteria           |        |
| 5. Implementation    | DOING - tests first, then code                     |        |
| 6. Review            | VALIDATING - check work against artifacts          |        |

**Stay in your lane**: Validate and refine discussion content into standalone specifications. Don't jump to planning, phases, tasks, or code. The specification is the "line in the sand" - everything after this has hard dependencies on it.

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

## Step 1: Discovery State

!`.claude/skills/start-specification/scripts/discovery.sh`

If the above shows a script invocation rather than YAML output, the dynamic content preprocessor did not run. Execute the script before continuing:

```bash
.claude/skills/start-specification/scripts/discovery.sh
```

If YAML content is already displayed, it has been run on your behalf.

Parse the discovery output to understand:

**From `discussions` array:** Each discussion's name, status, and whether it has an individual specification.

**From `specifications` array:** Each specification's name, status, sources, and superseded_by (if applicable). Specifications with `status: superseded` should be noted but excluded from active counts.

**From `cache` section:** `status` (valid/stale/none), `reason`, `generated`, `anchored_names`.

**From `current_state`:** `concluded_count`, `spec_count`, `has_discussions`, `has_concluded`, `has_specs`, and other counts/booleans for routing.

**IMPORTANT**: Use ONLY this script for discovery. Do NOT run additional bash commands (ls, head, cat, etc.) to gather state - the script provides everything needed.

→ Proceed to **Step 2**.

---

## Step 2: Check Prerequisites

#### If has_discussions is false or has_concluded is false

→ Load **[display-blocks.md](references/display-blocks.md)** and follow its instructions. **STOP.**

#### Otherwise

→ Proceed to **Step 3**.

---

## Step 3: Route

Based on discovery state, load exactly ONE reference file:

#### If concluded_count == 1

→ Load **[display-single.md](references/display-single.md)** and follow its instructions.

#### If cache status is "valid"

→ Load **[display-groupings.md](references/display-groupings.md)** and follow its instructions.

#### If spec_count == 0 and cache is "none" or "stale"

→ Load **[display-analyze.md](references/display-analyze.md)** and follow its instructions.

#### Otherwise

→ Load **[display-specs-menu.md](references/display-specs-menu.md)** and follow its instructions.

