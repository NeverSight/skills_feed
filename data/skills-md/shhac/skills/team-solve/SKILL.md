---
name: team-solve
description: Investigate and solve problems using a team of specialist agents. Use when facing complex, multi-faceted problems that benefit from parallel research and structured implementation.
---

# Team Solve

Investigate and solve one or more problems using parallel research, then serial implementation.

## When to Use

- A task with multiple distinct problems or themes to address
- A codebase change that benefits from researching several areas at once
- Work that can be decomposed into independent investigation tracks
- Situations where you want structured evidence-gathering before making changes

---

## Instructions for Claude

You are the **team lead** orchestrating an investigate-then-solve workflow.

### Coordination Protocol

Messages between teammates are **asynchronous** — a message sent now may not be read until the recipient finishes their current work. You cannot rely on message timing for coordination. Instead, **task status is the shared state** that tells every agent where things stand.

#### Task Status as Position Marker

When a teammate receives a message, they determine where it sits in the conversation by checking their task status — not by assuming it arrived "just now."

| Status | Who sets it | Meaning |
|--------|------------|---------|
| `pending` | Lead | Not started, waiting for assignment |
| `in_progress` | Teammate | Working, or finished and **parked** waiting for lead to acknowledge |
| `completed` | **Lead only** | Lead has read the teammate's report — this IS the acknowledgment |

**The lead marks tasks `completed` — not the teammate.** When a teammate sees their task marked `completed`, they know the lead has processed their report and any new message is current.

#### Teammate Protocol

Include these rules in every teammate's spawn prompt:

1. Mark your task `in_progress` when you begin work
2. When done, send your report via `SendMessage`, then **park** — stop all work, do not check `TaskList` or claim new tasks. Just wait.
3. Before acting on any received message, **check your task status via `TaskGet`**:
   - Still `in_progress` → lead hasn't acknowledged your report yet. This message may pre-date your report. Reply with your current state instead of re-executing.
   - `completed` → lead has processed your report. If a new task is assigned to you, this message contains current instructions — proceed.
4. Wait for all spawned subagents to finish before sending your report. Do not leave background work running.

#### Lead Protocol

1. After reading a teammate's report, mark their task `completed` (your acknowledgment)
2. Before sending new instructions, ensure the previous task is `completed` and the new task is created/assigned
3. Verify phase completion via `TaskList` — check that all relevant tasks show the expected status, don't track messages mentally
4. Between implementation tracks, run `git status` to confirm a clean working tree before proceeding

### Phase 1: Problem Decomposition

1. Parse the user's input to identify distinct problems or themes
2. If the problems are ambiguous or underspecified, ask clarifying questions before proceeding
3. Group related problems into 2-5 investigation tracks (one per teammate)
4. Present the decomposition to the user:
   - List each track with its assigned problems
   - Name each teammate descriptively (e.g., `filter-investigator`, `output-researcher`)
   - Ask: "I'll spin up N investigators in parallel. Proceed?"

### Phase 2: Parallel Investigation

Investigations run **in parallel**.

1. Create a team with `TeamCreate`
2. Create tasks for each investigation track with `TaskCreate`
3. Spawn one `general-purpose` teammate per track using `Task` with `team_name`
   - Each teammate's prompt must include:
     - The specific problems to investigate
     - Instruction to **research only, do not make changes**
     - The **Teammate Protocol** from the Coordination Protocol above (copy it into their prompt verbatim)
     - The subagent guidance below (copy it into their prompt)
     - Instruction to report findings via `SendMessage` using the report format below
   - **Spawn all investigators in parallel** — do not wait for one to finish before starting the next
4. **Do NOT shut down investigators when they report back** — they retain context for Phase 4

#### Subagent Guidance for Investigators

Include the following in each investigator's prompt:

> **Use subagents (`Task` tool) to keep your context focused.** Spawn subagents for:
> - Exploring specific files, modules, or subsystems
> - Searching through git history, logs, or large codebases
> - Any research tangent that might not pan out
>
> Each subagent should report back:
> 1. **Relevant findings** — what it discovered that matters to your investigation
> 2. **Red herrings** (1-2 sentences) — anything that *looks* related but *isn't*, and why. Calling these out early prevents wasted cycles re-exploring dead ends.
>
> Report red herrings even when your main findings are conclusive — they prevent other agents from re-exploring the same dead ends.
>
> After receiving a subagent's report, decide whether to:
> - **Use its findings directly** — if the summary gives you enough to proceed
> - **Dive in yourself** — if the subagent found something promising and you want full, first-hand context in that area before drawing conclusions. Examples: conflicting evidence that needs direct examination, low confidence in the subagent's assessment, or complex state/flow where first-hand context matters.
>
> When choosing subagent types, prefer read-only or exploration-focused types for open-ended codebase searches, and full-capability types for targeted analysis that needs deeper tool access.

#### Investigator Report Format

Each investigator should structure their report as:

```
## Track: {description}

### Findings
- {what was discovered, root causes, relevant code paths}

### Proposed Approach
- {what to change, which files, how}

### Risks & Edge Cases
- {what could go wrong with this approach}
- {what adjacent code/features could be affected}
- {what happens if data is unexpected or flow is interrupted}

### Red Herrings
- {things explored that weren't relevant, and why}

### Confidence: {high/medium/low}
{brief justification}

### Dependencies
- {does this approach depend on or conflict with other tracks?}
```

### Phase 3: Discussion Checkpoint

1. As investigators report back, mark each investigation task `completed` (acknowledging the report) and give the user brief progress updates
2. Once all investigation tasks show `completed` in `TaskList`, synthesize findings:
   - Key findings per track
   - Proposed approaches and confidence levels
   - Any conflicts or dependencies between tracks
   - **Ripple effects** — Evaluate across all tracks:
     - *"What happens to..."* — documentation, adjacent features, API consumers, shared state, caching
     - *"What happens if..."* — unexpected data, interrupted flows, concurrent access, rollback
   - Recommended implementation order (dependencies first, then highest-risk, then the rest)
3. If investigation reveals the problem is different than expected, say so — propose revised tracks rather than forcing the original plan
4. Ask the user: "Ready to implement, or want to revise the approach?"

### Phase 4: Serial Implementation

Implementations happen **one track at a time**. This prevents:
- Mixed, unrelated work in a single commit
- Confusing build/test failures caused by concurrent changes in flight
- File conflicts when teammates touch shared code

1. For each track (in the order agreed with the user), follow the **Lead Protocol**:
   a. Create an implementation task for this track and assign it to the original investigator
   b. Send the investigator an implementation message with: the work to do, the subagent guidance below, and (for subsequent tracks) the previous track's "what changed" summary
   c. **Wait** — the investigator will work, send a report, and park
   d. Read the report. Mark the implementation task `completed` (your acknowledgment).
   e. Run `git status` to confirm a clean working tree — no uncommitted changes, no leftover files
   f. Run relevant tests/checks as a quick sanity check
   g. Only then proceed to the next track
2. **Parallel exception**: Only consider parallel implementation if tracks have **zero file overlap** AND the codebase has no shared build/test pipeline that could produce confusing interleaved failures. If you think parallel is safe, explain why and ask the user.
3. **Partial failures**:
   - If an investigator reported low confidence or found nothing actionable, discuss with the user before implementing — options are to drop the track, merge it into another, or investigate further
   - If implementation fails mid-track, stop and discuss with the user whether to roll back or adjust the approach before continuing to the next track

#### Subagent Guidance for Implementation

Include the following when sending implementation instructions:

> **Use subagents to keep your main context focused on implementation logic.** Spawn subagents for:
> - **Repetitive edits** — similar changes across many files (updating imports, renaming across test files, applying a pattern to multiple modules)
> - **Impact analysis** — finding all callers of a function before changing its signature, checking all consumers of an API
> - **Exploratory reading** — checking whether a module's assumptions break with your change, verifying edge cases in adjacent code
> - **Background test runs** — running tests while you continue working on the next change
>
> **Important:** Wait for all subagents to complete before reporting your track as done. Do not leave background work running when you report completion.

### Phase 5: Validation

1. Before spawning the validator, verify via `TaskList` that all implementation tasks are `completed`, and run `git status` to confirm a clean working tree
2. Spawn a fresh `general-purpose` teammate named `validator`. The validator's spawn prompt must include: the **Teammate Protocol** from the Coordination Protocol (verbatim), the original problems from Phase 1, the agreed implementation approach from Phase 3, risk areas flagged by investigators, and the list of all changed files (or a `git diff` range). Instruct the validator to:
   - Detect the project's test/lint/typecheck tooling and run appropriate checks
   - Review all changed files for correctness and consistency
   - Check that each problem from Phase 1 is actually addressed
   - Look for unintended side effects or regressions
   - Report pass/fail with details via `SendMessage`
3. If validation fails:
   - Route failures back to the responsible investigator for fixes
   - Re-run validation after fixes
4. Once validation passes, send shutdown requests to all teammates and **wait for each to confirm** before reporting final results to the user

### Rules

- **Investigate in parallel, implement in series** — research benefits from parallelism; implementation benefits from sequencing
- **Task status is the source of truth** — coordinate through `TaskUpdate` status, not message timing. Always check `TaskList` to verify state.
- **Teammates park after reporting** — after sending a report, stop and wait. Do not self-assign new work or act on queued messages without checking task status first.
- **Lead owns `completed`** — only the lead marks tasks `completed`. This is the acknowledgment that closes the loop.
- **Subagents are cheap, context is expensive** — teammates should offload research tangents and repetitive edits to subagents rather than doing everything inline
- **Finish subagents before reporting** — wait for all spawned subagents to complete before sending your report
- **3-5 teammates max** — if more problems than that, group into themes
- **Never `git add .`** — teammates must add specific files
- **Validator is always fresh** — do not reuse an investigator as validator
- If a teammate goes idle, that's normal — send them a message when it's their turn
- **Unresponsive teammate?** — if a teammate hasn't reported within a reasonable timeframe, check their task status and `git status`. If stuck, spawn a replacement and inform the user.
