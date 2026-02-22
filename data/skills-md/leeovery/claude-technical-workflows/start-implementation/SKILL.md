---
name: start-implementation
description: "Start an implementation session from an existing plan. Discovers available plans, checks environment setup, and invokes the technical-implementation skill."
disable-model-invocation: true
allowed-tools: Bash(.claude/skills/start-implementation/scripts/discovery.sh), Bash(.claude/hooks/workflows/write-session-state.sh)
hooks:
  PreToolUse:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/workflows/system-check.sh"
          once: true
---

Invoke the **technical-implementation** skill for this conversation.

> **⚠️ ZERO OUTPUT RULE**: Do not narrate your processing. Produce no output until a step or reference file explicitly specifies display content. No "proceeding with...", no discovery summaries, no routing decisions, no transition text. Your first output must be content explicitly called for by the instructions.

## Workflow Context

This is **Phase 5** of the six-phase workflow:

| Phase | Focus | You |
|-------|-------|-----|
| 1. Research | EXPLORE - ideas, feasibility, market, business | |
| 2. Discussion | WHAT and WHY - decisions, architecture, edge cases | |
| 3. Specification | REFINE - validate into standalone spec | |
| 4. Planning | HOW - phases, tasks, acceptance criteria | |
| **5. Implementation** | DOING - tests first, then code | ◀ HERE |
| 6. Review | VALIDATING - check work against artifacts | |

**Stay in your lane**: Execute the plan via strict TDD - tests first, then code. Don't re-debate decisions from the specification or expand scope beyond the plan. The plan is your authority.

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

!`.claude/skills/start-implementation/scripts/discovery.sh`

If the above shows a script invocation rather than YAML output, the dynamic content preprocessor did not run. Execute the script before continuing:

```bash
.claude/skills/start-implementation/scripts/discovery.sh
```

If YAML content is already displayed, it has been run on your behalf.

Parse the discovery output to understand:

**From `plans` section:**
- `exists` - whether any plans exist
- `files` - list of plans with: name, topic, status, date, format, specification, specification_exists, plan_id (if present)
- Per plan `external_deps` - array of dependencies with topic, state, task_id
- Per plan `has_unresolved_deps` - whether plan has unresolved dependencies
- Per plan `unresolved_dep_count` - count of unresolved dependencies
- `count` - total number of plans

**From `implementation` section:**
- `exists` - whether any implementation tracking files exist
- `files` - list of tracking files with: topic, status, current_phase, completed_phases, completed_tasks

**From `dependency_resolution` section:**
- Per plan `deps_satisfied` - whether all resolved deps have their tasks completed
- Per plan `deps_blocking` - list of deps not yet satisfied with reason

**From `environment` section:**
- `setup_file_exists` - whether environment-setup.md exists
- `requires_setup` - true, false, or unknown

**From `state` section:**
- `scenario` - one of: `"no_plans"`, `"single_plan"`, `"multiple_plans"`
- `plans_concluded_count` - plans with status concluded
- `plans_with_unresolved_deps` - plans with unresolved external deps
- `plans_ready_count` - concluded plans with all deps satisfied
- `plans_in_progress_count` - implementations in progress
- `plans_completed_count` - implementations completed

**IMPORTANT**: Use ONLY this script for discovery. Do NOT run additional bash commands (ls, head, cat, etc.) to gather state - the script provides everything needed.

→ Proceed to **Step 2**.

---

## Step 2: Route Based on Scenario

Use `state.scenario` from the discovery output to determine the path:

#### If scenario is "no_plans"

No plans exist yet.

> *Output the next fenced block as a code block:*

```
Implementation Overview

No plans found in docs/workflow/planning/

The implementation phase requires a plan.
Run /start-planning first to create a plan from a specification.
```

**STOP.** Do not proceed — terminal condition.

#### If scenario is "single_plan" or "multiple_plans"

Plans exist.

→ Proceed to **Step 3** to present options.

---

## Step 3: Present Plans and Select

Present all discovered plans. Classify each plan into one of three categories based on its state.

**Classification logic:**

A plan is **Implementable** if:
- It has `status: concluded` AND all deps are satisfied (`deps_satisfied: true` or no deps) AND no tracking file or tracking `status: not-started`, OR
- It has an implementation tracking file with `status: in-progress`

A plan is **Implemented** if:
- It has an implementation tracking file with `status: completed`

A plan is **Not implementable** if:
- It has `status: concluded` but deps are NOT satisfied (blocking deps exist)
- It has `status: planning` or other non-concluded status
- It has unresolved deps (`has_unresolved_deps: true`)

**Present the full state:**

Show implementable and implemented plans as numbered tree items.

> *Output the next fenced block as a code block:*

```
Implementation Overview

{N} plans found. {M} implementations in progress.

1. {topic:(titlecase)}
   └─ Plan: {plan_status:[concluded]} ({format})
   └─ Implementation: @if(has_implementation) {impl_status:[in-progress|completed]} @else (not started) @endif

2. ...
```

**Tree rules:**

Implementable:
- Implementation `status: in-progress` → `Implementation: in-progress (Phase N, Task M)`
- Concluded plan, deps met, not started → `Implementation: (not started)`

Implemented:
- Implementation `status: completed` → `Implementation: completed`

**Ordering:**
1. Implementable first: in-progress, then new (foundational before dependent)
2. Implemented next: completed
3. Not implementable last (separate block below)

Numbering is sequential across Implementable and Implemented. Omit any section entirely if it has no entries.

**If non-implementable plans exist**, show them in a separate code block:

> *Output the next fenced block as a code block:*

```
Plans not ready for implementation:
These plans are either still in progress or have unresolved
dependencies that must be addressed first.

  • advanced-features (blocked by core-features:core-2-3)
  • reporting (in-progress)
```

> *Output the next fenced block as a code block:*

```
If a blocked dependency has been resolved outside this workflow,
name the plan and the dependency to unblock it.
```

**Key/Legend** — show only statuses that appear in the current display. No `---` separator before this section.

> *Output the next fenced block as a code block:*

```
Key:

  Implementation status:
    in-progress — work is ongoing
    completed   — all tasks implemented

  Blocking reason:
    blocked     — depends on another plan's task
    in-progress — plan not yet concluded
```

**Then prompt based on what's actionable:**

**If single implementable plan and no implemented plans (auto-select):**

> *Output the next fenced block as a code block:*

```
Automatically proceeding with "{topic:(titlecase)}".
```

→ Proceed directly to **Step 4**.

**If nothing selectable (no implementable or implemented):**

Show "not ready" block only (with unblock hint above).

> *Output the next fenced block as a code block:*

```
Implementation Overview

No implementable plans found.

Complete blocking dependencies first, or finish plans still
in progress with /start-planning. Then re-run /start-implementation.
```

**STOP.** Do not proceed — terminal condition.

**Otherwise (multiple selectable plans, or implemented plans exist):**

The verb in the menu depends on the implementation state:
- Implementation in-progress → **Continue**
- Not yet started → **Start**
- Completed → **Re-review**

> *Output the next fenced block as markdown (not a code block):*

```
· · · · · · · · · · · ·
1. Continue "Billing" — in-progress (Phase 2, Task 3)
2. Start "Core Features" — not yet started
3. Re-review "User Auth" — completed

Select an option (enter number):
· · · · · · · · · · · ·
```

Recreate with actual topics and states from discovery.

**STOP.** Wait for user response.

#### If the user requests an unblock

1. Identify the plan and the specific dependency
2. Confirm with the user which dependency to mark as satisfied
3. Update the plan's `external_dependencies` frontmatter: set `state` to `satisfied_externally`
4. Commit the change
5. Re-run classification and re-present Step 3

→ Based on user choice, proceed to **Step 4**.

---

## Step 4: Check External Dependencies

**This step is a confirmation gate.** Dependencies have been pre-analyzed by the discovery script.

After the plan is selected:

1. **Check the plan's `external_deps` and `dependency_resolution`** from the discovery output

#### If all deps satisfied (or no deps)

> *Output the next fenced block as a code block:*

```
External dependencies satisfied.
```

→ Proceed to **Step 5**.

#### If any deps are blocking

This should not normally happen for plans classified as "Implementable" in Step 3. However, as an escape hatch:

> *Output the next fenced block as a code block:*

```
Missing Dependencies

Unresolved (not yet planned):
  • {topic}: {description}
    No plan exists. Create with /start-planning or mark as
    satisfied externally.

Incomplete (planned but not implemented):
  • {topic}: {plan}:{task-id} not yet completed
    This task must be completed first.
```

> *Output the next fenced block as markdown (not a code block):*

```
· · · · · · · · · · · ·
- **`i`/`implement`** — Implement the blocking dependencies first
- **`l`/`link`** — Run /link-dependencies to wire up recently completed plans
- **`s`/`satisfied`** — Mark a dependency as satisfied externally
· · · · · · · · · · · ·
```

**STOP.** Wait for user response.

#### Escape Hatch

If the user says a dependency has been implemented outside the workflow:

1. Ask which dependency to mark as satisfied
2. Update the plan frontmatter: Change the dependency's `state` to `satisfied_externally`
3. Commit the change
4. Re-check dependencies

→ Proceed to **Step 5**.

---

## Step 5: Check Environment Setup

> **IMPORTANT**: This step is for **information gathering only**. Do NOT execute any setup commands at this stage. The skill contains instructions for handling environment setup.

Use the `environment` section from the discovery output:

**If `setup_file_exists: true` and `requires_setup: false`:**

> *Output the next fenced block as a code block:*

```
Environment: No special setup required.
```
→ Proceed to **Step 6**.

**If `setup_file_exists: true` and `requires_setup: true`:**

> *Output the next fenced block as a code block:*

```
Environment setup file found: docs/workflow/environment-setup.md
```
→ Proceed to **Step 6**.

**If `setup_file_exists: false` or `requires_setup: unknown`:**

> *Output the next fenced block as a code block:*

```
Are there any environment setup instructions I should follow before implementation?
(Or "none" if no special setup is needed)
```

**STOP.** Wait for user response.

- If the user provides instructions, save them to `docs/workflow/environment-setup.md`, commit and push
- If the user says no/none, create `docs/workflow/environment-setup.md` with "No special setup required." and commit

→ Proceed to **Step 6**.

---

## Step 6: Invoke the Skill

Before invoking the processing skill, save a session bookmark.

> *Output the next fenced block as a code block:*

```
Saving session state so Claude can pick up where it left off if the conversation is compacted.
```

```bash
.claude/hooks/workflows/write-session-state.sh \
  "{topic}" \
  "skills/technical-implementation/SKILL.md" \
  "docs/workflow/implementation/{topic}/tracking.md"
```

After completing the steps above, this skill's purpose is fulfilled.

Invoke the [technical-implementation](../technical-implementation/SKILL.md) skill for your next instructions. Do not act on the gathered information until the skill is loaded - it contains the instructions for how to proceed.

**Example handoff:**
```
Implementation session for: {topic}
Plan: docs/workflow/planning/{topic}/plan.md
Format: {format}
Plan ID: {plan_id} (if applicable)
Specification: {specification} (exists: {true|false})
Implementation tracking: {exists | new} (status: {in-progress | not-started | completed})

Dependencies: {All satisfied | List any notes}
Environment: {Setup required | No special setup required}

Invoke the technical-implementation skill.
```
