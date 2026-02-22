---
name: technical-implementation
description: "Orchestrate implementation of plans using agent-based TDD workflow with per-task review and approval gate (auto mode available). Use when: (1) Implementing a plan from docs/workflow/planning/{topic}/plan.md, (2) User says 'implement', 'build', or 'code this' with a plan available, (3) Ad hoc coding that should follow TDD and quality standards, (4) Bug fixes or features benefiting from structured implementation. Dispatches executor and reviewer agents per task, commits after review approval."
user-invocable: false
---

# Technical Implementation

Orchestrate implementation by dispatching **executor** and **reviewer** agents per task. Each agent invocation starts fresh — flat context, no accumulated state.

- **Executor** (`../../agents/implementation-task-executor.md`) — implements one task via strict TDD
- **Reviewer** (`../../agents/implementation-task-reviewer.md`) — independently verifies the task (opus)

The orchestrator owns: plan reading, task extraction, agent invocation, git operations, tracking, task gates.

## Purpose in the Workflow

This skill can be used:
- **Sequentially**: To execute a plan created by technical-planning
- **Standalone** (Contract entry): To execute any plan that follows plan-format conventions

Either way: dispatch agents per task — executor implements via TDD, reviewer verifies independently.

### What This Skill Needs

- **Plan content** (required) - Phases, tasks, and acceptance criteria to execute
- **Plan format** (required) - How to parse tasks (from plan frontmatter)
- **Specification content** (optional) - For context when task rationale is unclear
- **Environment setup** (optional) - First-time setup instructions

**Before proceeding**, verify all required inputs are available and unambiguous. If anything is missing or unclear, **STOP** — do not proceed until resolved.

#### If no plan provided

> *Output the next fenced block as a code block:*

```
I need an implementation plan to execute. Could you point me to the plan file
(e.g., docs/workflow/planning/{topic}/plan.md)?
```

**STOP.** Wait for user response.

#### If plan has no `format` field in frontmatter

> *Output the next fenced block as a code block:*

```
The plan at {path} doesn't specify an output format in its frontmatter.
Which format does this plan use?
```

**STOP.** Wait for user response.

#### If plan status is not `concluded`

> *Output the next fenced block as a code block:*

```
The plan at {path} has status '{status}' — it hasn't completed the review
process. Should I proceed anyway, or should the plan be reviewed first?
```

**STOP.** Wait for user response.

If no specification is available, the plan becomes the sole authority for design decisions.

---

## Resuming After Context Refresh

Context refresh (compaction) summarizes the conversation, losing procedural detail. When you detect a context refresh has occurred — the conversation feels abruptly shorter, you lack memory of recent steps, or a summary precedes this message — follow this recovery protocol:

1. **Re-read this skill file completely.** Do not rely on your summary of it. The full process, steps, and rules must be reloaded.
2. **Check task progress in the plan** — use the plan adapter's instructions to read the plan's current state. Also read the implementation tracking file and any other working documents for additional context.
3. **Check `task_gate_mode`, `fix_gate_mode`, `analysis_gate_mode`, `fix_attempts`, and `analysis_cycle`** in the tracking file — if gates are `auto`, the user previously opted out. If `fix_attempts` > 0, you're mid-fix-loop for the current task. If `analysis_cycle` > 0, you've completed analysis cycles — check for findings files on disk (`analysis-*-c{cycle-number}.md` in `{topic}/`) to determine mid-analysis state.
4. **Check git state.** Run `git status` and `git log --oneline -10` to see recent commits. Commit messages follow a conventional pattern that reveals what was completed.
5. **Announce your position** to the user before continuing: what step you believe you're at, what's been completed, and what comes next. Wait for confirmation.

Do not guess at progress or continue from memory. The files on disk and git history are authoritative — your recollection is not.

---

## Orchestrator Hard Rules

1. **No autonomous decisions on spec deviations** — when the executor reports a blocker or spec deviation, present to user and STOP. Never resolve on the user's behalf.
2. **All git operations are the orchestrator's responsibility** — agents never commit, stage, or interact with git.

## Output Formatting

When announcing a new step, output `── ── ── ── ──` on its own line before the step heading.

---

## Step 1: Environment Setup

Run setup commands EXACTLY as written, one step at a time.
Do NOT modify commands based on other project documentation (CLAUDE.md, etc.).
Do NOT parallelize steps — execute each command sequentially.
Complete ALL setup steps before proceeding.

Load **[environment-setup.md](references/environment-setup.md)** and follow its instructions.

#### If `docs/workflow/environment-setup.md` states "No special setup required"

→ Proceed to **Step 2**.

#### If setup instructions exist

Follow them. Complete ALL steps before proceeding.

→ Proceed to **Step 2**.

#### If no setup file exists

> *Output the next fenced block as a code block:*

```
No environment setup document found. Are there any setup instructions
I should follow before implementing?
```

**STOP.** Wait for user response.

Save their instructions to `docs/workflow/environment-setup.md` (or "No special setup required." if none needed). Commit.

→ Proceed to **Step 2**.

---

## Step 2: Read Plan + Load Plan Adapter

1. Read the plan from the provided location (typically `docs/workflow/planning/{topic}/plan.md`)
2. Plans can be stored in various formats. The `format` field in the plan's frontmatter identifies which format this plan uses.
3. Load the format's per-concern adapter files from `../technical-planning/references/output-formats/{format}/`:
   - **reading.md** — how to read tasks from the plan
   - **updating.md** — how to write progress to the plan
4. If no `format` field exists, ask the user which format the plan uses.
5. These adapter files apply during Step 6 (task loop) and Step 7 (analysis).
6. Also load the format's **authoring.md** adapter — needed in Step 7 if analysis tasks are created.

→ Proceed to **Step 3**.

---

## Step 3: Initialize Implementation Tracking

#### If `docs/workflow/implementation/{topic}/tracking.md` already exists

Reset `task_gate_mode`, `fix_gate_mode`, and `analysis_gate_mode` to `gated`, `fix_attempts` to `0`, and `analysis_cycle` to `0` (fresh session = fresh gates/cycles).

→ Proceed to **Step 4**.

#### If no tracking file exists

Create `docs/workflow/implementation/{topic}/tracking.md`:

```yaml
---
topic: {topic}
plan: ../../planning/{topic}/plan.md
format: {format from plan}
status: in-progress
task_gate_mode: gated
fix_gate_mode: gated
analysis_gate_mode: gated
fix_attempts: 0
linters: []
analysis_cycle: 0
project_skills: []
current_phase: 1
current_task: ~
completed_phases: []
completed_tasks: []
started: YYYY-MM-DD  # Use today's actual date
updated: YYYY-MM-DD  # Use today's actual date
completed: ~
---

# Implementation: {Topic Name}

Implementation started.
```

Commit: `impl({topic}): start implementation`

→ Proceed to **Step 4**.

---

## Step 4: Project Skills Discovery

#### If `project_skills` is populated in the tracking file

Present the existing configuration for confirmation:

> *Output the next fenced block as markdown (not a code block):*

```
Previous session used these project skills:
- `{skill-name}` — {path}
- ...

· · · · · · · · · · · ·
- **`y`/`yes`** — Keep these, proceed
- **`c`/`change`** — Re-discover and choose skills
· · · · · · · · · · · ·
```

**STOP.** Wait for user choice.

- **`yes`**: → Proceed to **Step 5**.
- **`change`**: Clear `project_skills` and fall through to discovery below.

#### If `.claude/skills/` does not exist or is empty

> *Output the next fenced block as a code block:*

```
No project skills found. Proceeding without project-specific conventions.
```

→ Proceed to **Step 5**.

#### If project skills exist

Scan `.claude/skills/` for project-specific skill directories. Present findings:

> *Output the next fenced block as markdown (not a code block):*

```
Found these project skills that may be relevant to implementation:
- `{skill-name}` — {brief description}
- `{skill-name}` — {brief description}
- ...

· · · · · · · · · · · ·
- **`a`/`all`** — Use all listed skills
- **`n`/`none`** — Skip project skills
- **Or list the ones you want** — e.g. "golang-pro, react-patterns"
· · · · · · · · · · · ·
```

**STOP.** Wait for user to confirm which skills are relevant.

Store the selected skill paths in the tracking file.

→ Proceed to **Step 5**.

---

## Step 5: Linter Discovery

Load **[linter-setup.md](references/linter-setup.md)** and follow its discovery process to identify project linters.

If `linters` is already populated in the tracking file, present the existing configuration for confirmation (same pattern as project skills in Step 4). If confirmed, skip discovery and proceed.

Otherwise, present discovery findings to the user:

> *Output the next fenced block as markdown (not a code block):*

```
**Linter discovery:**
- {tool} — `{command}` (installed / not installed)
- ...

Recommendations: {any suggested tools with install commands}

· · · · · · · · · · · ·
- **`y`/`yes`** — Approve these linter commands
- **`c`/`change`** — Modify the linter list
- **`s`/`skip`** — Skip linter setup (no linting during TDD)
· · · · · · · · · · · ·
```

**STOP.** Wait for user choice.

- **`yes`**: Store the approved linter commands in the tracking file.
- **`change`**: Adjust based on user input, re-present for confirmation.
- **`skip`**: Store empty linters array.

→ Proceed to **Step 6**.

---

## Step 6: Task Loop

Load **[task-loop.md](references/task-loop.md)** and follow its instructions as written.

After the loop completes:

→ If the task loop exited early (user chose `stop`), proceed to **Step 8**.

→ Otherwise, proceed to **Step 7**.

---

## Step 7: Analysis Loop

Load **[analysis-loop.md](references/analysis-loop.md)** and follow its instructions as written.

→ If new tasks were created in the plan, return to **Step 6**.

→ If no tasks were created, proceed to **Step 8**.

---

## Step 8: Mark Implementation Complete

Before marking complete, present the sign-off:

> *Output the next fenced block as markdown (not a code block):*

```
· · · · · · · · · · · ·
- **`y`/`yes`** — Mark implementation as completed
- **Comment** — Add context before completing
· · · · · · · · · · · ·
```

**STOP.** Wait for user response.

#### If comment

Discuss the user's context. If additional work is needed, route back to **Step 6** or **Step 7** as appropriate. Otherwise, re-present the sign-off prompt above.

#### If yes

Update the tracking file (`docs/workflow/implementation/{topic}/tracking.md`):
- Set `status: completed`
- Set `completed: YYYY-MM-DD` (use today's actual date)
- Update `updated` date

Commit: `impl({topic}): complete implementation`


