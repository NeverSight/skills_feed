---
name: competing-hypotheses
description: Debug problems by investigating multiple hypotheses in parallel. Use when you have a bug, unexpected behaviour, or mystery where the root cause is unclear. Spawns parallel investigator agents each pursuing a different theory, then compares evidence to identify the most likely cause and fix.
---

# Competing Hypotheses

Debug problems by racing multiple theories in parallel. Each investigator pursues a different hypothesis, gathers evidence, and reports back. The lead compares findings to identify the root cause.

## When to Use

- "I have no idea why this is broken"
- A bug that could have multiple root causes
- Unexpected behaviour with no obvious source
- Performance regressions with unclear origin
- Intermittent failures that are hard to reproduce

---

## Instructions for Claude

You are the **lead investigator** coordinating a parallel hypothesis investigation.

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
4. Between implementation steps, run `git status` to confirm a clean working tree before proceeding

### Phase 1: Hypothesize

1. Understand the problem from the user's input:
   - What's the symptom? (error message, wrong output, unexpected behaviour)
   - When does it happen? (always, sometimes, after a recent change)
   - What's already been tried?
2. Generate 2-5 plausible hypotheses for the root cause
   - Each should be distinct and testable
   - Cover different areas (data, logic, infrastructure, external dependencies, timing)
3. Present the hypotheses to the user:
   - List each hypothesis with a brief rationale
   - Ask: "I'll spin up N investigators to pursue these in parallel. Proceed?"
   - Incorporate any hypotheses the user wants to add or remove

### Phase 2: Parallel Investigation

1. Create a team with `TeamCreate`
2. Create tasks for each hypothesis with `TaskCreate`
3. Spawn one `general-purpose` teammate per hypothesis using `Task` with `team_name`
   - Name them after their hypothesis (e.g., `race-condition-investigator`, `data-corruption-investigator`)
   - Each investigator's prompt should include:
     - The overall problem description
     - Their specific hypothesis to pursue
     - Instruction to **investigate only, do not make changes**
     - The **Teammate Protocol** from the Coordination Protocol above (copy it into their prompt verbatim)
     - What evidence to look for (see Investigation Guide below)
     - Instruction to report findings via `SendMessage`
4. Spawn all investigators in parallel
5. As investigators report back, mark each investigation task `completed` (acknowledging the report) and give the user brief progress updates
6. If an investigator discovers a recent commit already resolved the issue, report the finding to the user and end early if they confirm it's fixed

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
> When choosing subagent types, prefer read-only or exploration-focused types for open-ended codebase searches, and full-capability types for targeted analysis or tasks that need write access.

### Investigation Guide

Each investigator should:

1. **Search for evidence** supporting their hypothesis
   - Read relevant code paths
   - Check logs, error messages, stack traces if available
   - Look at recent changes (git log, git diff) that could be related
   - Examine configuration, environment, data
2. **Search for counter-evidence** that would disprove their hypothesis
3. **Rate their confidence** based on what they found
4. **Report** using the output format below

### Investigator Output Format

```
## Hypothesis: {description}

### Evidence For
- {evidence point}: {where found, what it means}

### Evidence Against
- {evidence point}: {where found, what it means}

### Red Herrings
- {code paths or areas explored that looked related but weren't, and why}

### Confidence: {high/medium/low}

### Root Cause (if found)
{specific root cause, file, line, mechanism}

### Suggested Fix
{what to change and why}

### Open Questions
- {anything unresolved that could help narrow it down}
```

### Phase 3: Compare & Conclude

1. Once all investigation tasks show `completed` in `TaskList`, compare findings:
   - Which hypothesis has the strongest evidence?
   - Did any investigator find definitive proof?
   - Do findings from different investigators corroborate each other?
   - Are there open questions that could be quickly resolved?
   - **Compound bugs** — if multiple hypotheses are confirmed, present as a multi-root-cause scenario and propose fixing in dependency order (fix the cause that enables the others first)
2. Present the analysis to the user:
   - Rank hypotheses by evidence strength
   - Highlight the most likely root cause
   - Note any surprising findings or ruled-out theories
   - Recommend next steps (fix, further investigation, or targeted test)

### Phase 4: Fix (Optional)

Skip this phase if the user only wanted diagnosis, not a fix.

1. If the root cause is clear and the user wants to proceed, follow the **Lead Protocol**:
   a. Create an implementation task and assign it to the investigator who found the root cause
   b. Send them an implementation message with the fix details
   c. **Wait** — the investigator will implement, send a report, and park
   d. Read the report. Mark the implementation task `completed` (your acknowledgment).
   e. Run `git status` to confirm a clean working tree
2. If the root cause is unclear:
   - Propose targeted experiments to disambiguate
   - Ask the user which direction to pursue
3. For **compound bugs** (multiple root causes), implement fixes one at a time — repeat step 1 for each, verifying clean git state between each fix
4. After all fixes, verify via `TaskList` that all implementation tasks are `completed` and `git status` shows a clean working tree. Then spawn a fresh `validator` teammate. The validator's spawn prompt must include: the **Teammate Protocol** (verbatim), the original symptom, the confirmed hypothesis/root cause, and what the fix was intended to do.
5. If validation fails, route the failure back to the investigator who implemented the fix for corrections, then re-validate

### Rules

- **Task status is the source of truth** — coordinate through `TaskUpdate` status, not message timing. Always check `TaskList` to verify state.
- **Teammates park after reporting** — after sending a report, stop and wait. Do not self-assign new work or act on queued messages without checking task status first.
- **Lead owns `completed`** — only the lead marks tasks `completed`. This is the acknowledgment that closes the loop.
- **Keep investigators alive** until the conclusion — they may need follow-up questions
- **2-5 hypotheses max** — too many dilutes focus
- **Investigators don't communicate** — they work independently to avoid confirmation bias
- **Evidence over intuition** — rank hypotheses by concrete evidence, not plausibility
- **Counter-evidence matters** — a hypothesis with strong counter-evidence should be deprioritized even if it seems likely
- **Finish subagents before reporting** — wait for all spawned subagents to complete before sending your report
- **Shut down when done** — after validation passes, or after the user declines to fix, send shutdown requests and **wait for confirmations** before reporting final results
- **Unresponsive teammate?** — if a teammate hasn't reported within a reasonable timeframe, check their task status. If stuck, spawn a replacement and inform the user.
