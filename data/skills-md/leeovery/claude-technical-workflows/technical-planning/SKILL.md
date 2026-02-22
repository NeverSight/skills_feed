---
name: technical-planning
description: "Transform specifications into actionable implementation plans with phases, tasks, and acceptance criteria. Use when: (1) User asks to create/write an implementation plan, (2) User asks to plan implementation from a specification, (3) Converting specifications from docs/workflow/specification/{topic}/specification.md into implementation plans, (4) User says 'plan this' or 'create a plan', (5) Need to structure how to build something with phases and concrete steps. Creates plans in docs/workflow/planning/{topic}/plan.md that can be executed via strict TDD."
user-invocable: false
---

# Technical Planning

Act as **expert technical architect**, **product owner**, and **plan documenter**. Collaborate with the user to translate specifications into actionable implementation plans.

Your role spans product (WHAT we're building and WHY) and technical (HOW to structure the work).

## Purpose in the Workflow

This skill can be used:
- **Sequentially**: From a validated specification
- **Standalone** (Contract entry): From any specification meeting format requirements

Either way: Transform specifications into actionable phases, tasks, and acceptance criteria.

### What This Skill Needs

- **Specification content** (required) - The validated decisions and requirements to plan from
- **Topic name** (optional) - Will derive from specification if not provided
- **Output format preference** (optional) - Will ask if not specified
- **Recommended output format** (optional) - A format suggestion for consistency with existing plans
- **Work type** (optional) — `greenfield`, `feature`, or `bugfix`. Determines which context-specific guidance is loaded during phase and task design. Defaults to `greenfield` when not provided.
- **Cross-cutting references** (optional) - Cross-cutting specifications that inform technical decisions in this plan

**Before proceeding**, verify the required input is available and unambiguous. If anything is missing or unclear, **STOP** — do not proceed until resolved.

#### If no specification content provided

> *Output the next fenced block as a code block:*

```
I need the specification content to plan from. Could you point me to the
specification file (e.g., docs/workflow/specification/{topic}/specification.md),
or provide the content directly?
```

**STOP.** Wait for user response.

#### If specification seems incomplete or not concluded

> *Output the next fenced block as a code block:*

```
The specification at {path} appears to be {concern — e.g., 'still in-progress'
or 'missing sections that are referenced elsewhere'}. Should I proceed with
this, or is there a more complete version?
```

**STOP.** Wait for user response.

---

## Resuming After Context Refresh

Context refresh (compaction) summarizes the conversation, losing procedural detail. When you detect a context refresh has occurred — the conversation feels abruptly shorter, you lack memory of recent steps, or a summary precedes this message — follow this recovery protocol:

1. **Re-read this skill file completely.** Do not rely on your summary of it. The full process, steps, and rules must be reloaded.
2. **Read all tracking and state files** for the current topic — plan index files, review tracking files, implementation tracking files, or any working documents this skill creates. These are your source of truth for progress. Check for scratch files at `docs/workflow/.cache/planning/{topic}/`. If a scratch file exists, you are mid-authoring for that phase — resume the approval loop in author-tasks.md.
3. **Check git state.** Run `git status` and `git log --oneline -10` to see recent commits. Commit messages follow a conventional pattern that reveals what was completed.
4. **Announce your position** to the user before continuing: what step you believe you're at, what's been completed, and what comes next. Wait for confirmation.
5. **Check `task_list_gate_mode`, `author_gate_mode`, and `finding_gate_mode`** in the Plan Index File frontmatter — if `auto`, the user previously opted in during this session. Preserve these values.

Do not guess at progress or continue from memory. The files on disk and git history are authoritative — your recollection is not.

---

## The Process

This process constructs a plan from a specification. A plan consists of:

- **Plan Index File** — `docs/workflow/planning/{topic}/plan.md`. Contains frontmatter (topic, format, status, progress), phases with acceptance criteria, and task tables tracking status. This is the single source of truth for planning progress.
- **Authored Tasks** — Detailed task files written to the chosen **Output Format** (selected during planning). The output format determines where and how task detail is stored.

Follow every step in sequence. No steps are optional.

## Output Formatting

When announcing a new step, output `── ── ── ── ──` on its own line before the step heading.

---

## Step 0: Resume Detection

Check if a Plan Index File already exists at `docs/workflow/planning/{topic}/plan.md`.

#### If no Plan Index File exists

→ Proceed to **Step 1**.

#### If Plan Index File exists

If `status: concluded`, update it to `status: planning`.

Note the current phase and task position from the `planning:` block.

Load **[spec-change-detection.md](references/spec-change-detection.md)** to check whether the specification has changed since planning started. Then present the user with an informed choice:

Found existing plan for **{topic}** (previously reached phase {N}, task {M}).

{spec change summary from spec-change-detection.md}

> *Output the next fenced block as markdown (not a code block):*

```
· · · · · · · · · · · ·
- **`c`/`continue`** — Walk through the plan from the start. You can review, amend, or navigate at any point — including straight to the leading edge.
- **`r`/`restart`** — Erase all planning work for this topic and start fresh. This deletes the Plan Index File and any Authored Tasks. Other topics are unaffected.
· · · · · · · · · · · ·
```

**STOP.** Wait for user response.

#### If `continue`

If the specification changed, update `spec_commit` in the Plan Index File frontmatter to the current commit hash.

Reset `task_list_gate_mode`, `author_gate_mode`, and `finding_gate_mode` to `gated` in the Plan Index File frontmatter (fresh invocation = fresh gates).

→ Proceed to **Step 1**.

#### If `restart`

1. Read **[output-formats.md](references/output-formats.md)**, find the entry matching the `format:` field in the Plan Index File, and load the format's **[authoring.md](references/output-formats/{format}/authoring.md)**
2. Follow the authoring file's cleanup instructions to remove Authored Tasks for this topic
3. Delete the scratch directory if it exists: `rm -rf docs/workflow/.cache/planning/{topic}/`
4. Delete the Plan Index File
5. Commit: `planning({topic}): restart planning`

→ Proceed to **Step 1**.

---

## Step 1: Initialize Plan

#### If Plan Index File already exists

Read **[output-formats.md](references/output-formats.md)**, find the entry matching the `format:` field, and load the format's **[about.md](references/output-formats/{format}/about.md)** and **[authoring.md](references/output-formats/{format}/authoring.md)**.

→ Proceed to **Step 2**.

#### If no Plan Index File exists

First, choose the Output Format.

**If a recommended output format was provided** (non-empty, not "none"):

Present the recommendation:

Existing plans use **{format}**. Use the same format for consistency?

> *Output the next fenced block as markdown (not a code block):*

```
· · · · · · · · · · · ·
- **`y`/`yes`** — Use {format}
- **`n`/`no`** — See all available formats
· · · · · · · · · · · ·
```

**STOP.** Wait for user choice. If declined, fall through to the full list below.

**If no recommendation, or user declined:**

Present the formats from **[output-formats.md](references/output-formats.md)** to the user — including description, pros, cons, and "best for". Number each format and ask the user to pick.

**STOP.** Wait for the user to choose.

Once selected:

1. Read **[output-formats.md](references/output-formats.md)**, find the chosen format entry, and load the format's **[about.md](references/output-formats/{format}/about.md)** and **[authoring.md](references/output-formats/{format}/authoring.md)**
2. Capture the current git commit hash: `git rev-parse HEAD`
3. Create the Plan Index File at `docs/workflow/planning/{topic}/plan.md` using the **Frontmatter** and **Title** templates from **[plan-index-schema.md](references/plan-index-schema.md)**. Set `status: planning`, `spec_commit` to the captured git hash, today's actual date for `created` and `updated`, and `work_type` to the value provided by the caller (or `greenfield` if not provided).

3. Commit: `planning({topic}): initialize plan`

→ Proceed to **Step 2**.

---

## Step 2: Load Planning Principles

Load **[planning-principles.md](references/planning-principles.md)** and follow its instructions as written.

→ Proceed to **Step 3**.

---

## Step 3: Verify Source Material

Load **[verify-source-material.md](references/verify-source-material.md)** and follow its instructions as written.

→ Proceed to **Step 4**.

---

## Step 4: Plan Construction

Load **[plan-construction.md](references/plan-construction.md)** and follow its instructions as written.

→ Proceed to **Step 5**.

---

## Step 5: Analyze Task Graph

Load **[analyze-task-graph.md](references/analyze-task-graph.md)** and follow its instructions as written.

→ Proceed to **Step 6**.

---

## Step 6: Resolve External Dependencies

Load **[resolve-dependencies.md](references/resolve-dependencies.md)** and follow its instructions as written.

→ Proceed to **Step 7**.

---

## Step 7: Plan Review

Load **[plan-review.md](references/plan-review.md)** and follow its instructions as written.

→ Proceed to **Step 8**.

---

## Step 8: Conclude the Plan

> **CHECKPOINT**: Do not conclude if any tasks in the Plan Index File show `status: pending`. All tasks must be `authored` before concluding.

> *Output the next fenced block as markdown (not a code block):*

```
· · · · · · · · · · · ·
- **`y`/`yes`** — Conclude plan and mark as concluded
- **Comment** — Add context before concluding
· · · · · · · · · · · ·
```

**STOP.** Wait for user response.

#### If comment

Discuss the user's context. If additional work is needed, route back to **Step 6** or **Step 7** as appropriate. Otherwise, re-present the sign-off prompt above.

#### If yes

1. **Update plan status** — Set `status: concluded` in the Plan Index File frontmatter
2. **Final commit** — Commit the concluded plan: `planning({topic}): conclude plan`
3. **Present completion summary**:

> *Output the next fenced block as markdown (not a code block):*

```
Planning is complete for **{topic}**.

The plan contains **{N} phases** with **{M} tasks** total, reviewed for traceability against the specification and structural integrity.

Status has been marked as `concluded`. The plan is ready for implementation.
```
