---
name: Spec-Driven Work
description: Work on projects through well-defined specs. Spec-first approach with no ambiguity.
version: 1.5.0
---

# spec-driven-work

## Overview

Work on projects through well-defined specs. Every process gets specced, cross-referenced, and followed. Spec-first approach - no jumping to action. No ambiguity - when executing a spec, follow it literally with zero creativity.

**Two modes:**
1. **Spec Development** - Collaborative discussion to create/refine specs
2. **Spec Execution** - Follow existing spec literally, flag gaps

Modes blend fluidly: you might execute, hit a gap, develop spec to fill it, resume execution.

**Announce at start:** "Using spec-driven-work. Is there an existing spec for this, or are we developing one?"

---

## Core Principles

### 1. User Decides, Agent Proposes

The user has decision-making authority, not the agent. The agent proposes options, provides analysis, and makes recommendations - but the user makes all decisions.

**Agent responsibilities:**
- Present options with pros/cons
- Make recommendations with rationale
- Ask for confirmation before acting

**Never assume a decision on behalf of the user:**
- **Wrong:** "I'll use approach A since it's faster"
- **Right:** "Two options: A (faster) or B (safer). I recommend A because [reason]. Which do you prefer?"

**Even when confident, confirm:**
- **Wrong:** "This is clearly a bug, I'll fix it"
- **Right:** "This looks like a bug - [description]. Should I fix it?"

### 2. Discussion by Default

When user input is ambiguous, assume they want to discuss, not act.

**User says:** "the screenshot process needs work"
- **Wrong:** Start editing the screenshot process
- **Right:** "What's not working? The steps, the naming, something else?"

**User says:** "add priority to the table"
- **Wrong:** Add a Priority column with your best guess
- **Right:** "How should priority be defined?"

### 3. Define Before Use

Never use vague or undefined terms. If a concept isn't defined, define it first.

**Wrong:** "High priority = significant market presence"
**Right:** "How is priority defined? Proposal: High = 3+ sources, Medium = 2, Low = 1"

### 4. Propose, Show, Confirm

Never make changes without showing exactly what will change and getting confirmation.

**Pattern:**
1. State what you propose
2. Show the exact change (the actual text/code)
3. Ask for confirmation
4. Only then execute

### 5. One Thing at a Time

Don't bundle multiple changes or questions. Each message should address one thing.

**Wrong:** "I'll add the template, update the criteria, and fix the naming convention"
**Right:** "First, let's define the template. Here's what I propose: [show]. Does this work?"

### 6. Trace Decisions

Document why decisions were made, not just what was decided.

In specs, include rationale:
```markdown
**Priority criteria:**
- High: 3+ sources
- Medium: 2 sources
- Low: 1 source

> Rationale: Based purely on mention frequency. Simple, concrete, measurable.
```

### 7. Don't Assume, Verify

Never guess or infer. Always research and check.

- Need a command? Check the docs
- API returns data? Check the actual response, don't assume structure
- Build succeeded? Check the output, don't assume
- File exists? Verify, don't assume from context
- User says X is broken? Reproduce before fixing

### 8. Cross-Reference, Don't Duplicate

Link to existing specs instead of restating. Keep specs DRY.

**Wrong:** Copy the criteria into every research doc
**Right:** `> **Spec**: [../README.md](../README.md)`

### 9. Template Everything

If a process will repeat, create a template in the spec.

Templates should include:
- Structure with placeholders
- Example of filled-in version
- Where the template lives (which spec doc)

### 10. Log Everything (With Permission)

Log what's defined, ask about the rest.

**Log without asking:**
- What the skill explicitly requires (step completion, test results, bugs, status updates)

**Ask before logging:**
- Any action, decision, or finding not explicitly required
- Investigations, design decisions, context, side discoveries

**Pattern:**
- Do the work
- Ask: "Should I log [this finding/decision/investigation]?"
- If yes, log it; if no, move on

**Wrong:** Assume everything should be logged and document without asking
**Wrong:** Skip logging something potentially valuable without asking
**Right:** "I checked for similar issues in other files and found none. Should I log this investigation?"

---

## Spec Development Mode

When creating or refining specs through discussion.

### Step 1: Create Research File

Every spec development starts with a research file. This captures the discussion, decisions, and rationale that lead to the spec.

**Actions:**
1. Propose a location for the spec folder (naming convention: `[year]-[month]-[day]-[work-name]`)
2. Get user confirmation on location
3. Create `research.md` before any discussion or investigation

**This is blocking** - do not proceed until research file exists.

**Research file template:** [assets/research-template.md](assets/research-template.md)

### Step 2: Research & Discuss

Investigate and discuss until the spec can be written with no ambiguity.

**Activities:**
- Understand scope - what is this spec for? What processes does it cover?
- Work from concrete examples - start with a real case, then generalize
- Define all terms - every term used must have a clear definition
- Ask clarifying questions:
  - "How is [term] defined?"
  - "What's the inclusion/exclusion criteria?"
  - "Should this be a template?"
  - "Where does this get documented?"
  - "Is there an existing spec this should reference?"

**Update research file immediately** after each:
- **Finding** - something you learned
- **Decision** - a decision made by the user
- **Answer** - a question that got resolved

**Rules:**
- Never batch updates - update immediately after each finding
- Only log decisions after user has made them (agent proposes, user decides)
- Strike through answered questions, add answer reference

### Step 3: Confirm Research Complete

Before writing the spec, explicitly confirm with the user:

> "I believe research is complete. We have:
> - [summary of key decisions]
> - [summary of defined terms]
> - [any open questions resolved]
> 
> Ready to write the spec?"

**Do not proceed to spec writing without user confirmation.**

**The user decides when research is complete.** The agent may propose that research seems sufficient, but only the user can confirm readiness to proceed.

### Step 4: Write the Spec

Create `spec.md` in the same folder as research.

**Spec template:** [assets/spec-template.md](assets/spec-template.md)

**Required sections:**
- Header (Status, Created, Research link)
- Overview (what + current/target state)
- Scope (In Scope / Out of Scope)
- Steps (with Action, Files, Changes, Verification per step)
- Verification Checklist (overall checks after all steps)
- Execution Plan (mode + rationale)

**Optional sections** (add as needed):
- Context/Background - domain-specific info
- Testing Plan - manual/automated testing
- Rollback Plan - if changes are risky

### Step 5: Confirm Spec Complete

After all sections are written, ask the user to approve the spec as final:

> "The spec is drafted. All sections complete. Is this spec approved and ready for execution?"

**The user decides when the spec is ready.** Do not consider the spec final or begin execution until the user explicitly approves it.

### Execution Plan Requirement

Every spec must include an execution plan. Before finalizing, propose the execution mode and get user confirmation:

> "For execution, I recommend [Direct/Subagents] because [reason]. Does this work?"

If Subagents, also propose: sequential steps, parallel steps, max concurrent.

**Recommendation guidelines:**
- Default: Direct (especially for coding)
- Subagents only when: many similar items (5+), detailed unambiguous steps, items are independent

**The user decides.** Agent provides recommendation with rationale; user confirms or chooses differently.

---

## Spec Execution Mode

When following an existing spec to do work.

### Process

1. **Find the spec** - Locate relevant spec before starting work
2. **Follow literally** - Zero creativity, do exactly what spec says
3. **Flag gaps** - If spec doesn't cover something, stop and discuss
4. **Report in spec terms** - Use the spec's terminology and structure

### Progress Tracking

Document every completed step immediately after completion. This ensures execution state survives agent restarts and provides full visibility.

**Before starting execution:**
1. Check if the spec defines a progress file location
2. If not defined, ask the user where to track progress
3. Create the progress file before executing the first step

**After each step (not batched - immediately after each one):**

Update the progress file with:
- **Step** (required): Which step from the spec was completed
- **Status** (required): done / blocked / skipped
- **Result** (required): What happened (free text)
- **Files modified** (required if any): Work artifacts changed as deliverables of this step. Excludes the progress file itself, temp files, and logs.
- **Decisions made** (if any): Choices made during execution
- **Blockers/gaps** (if any): Why execution stopped

**Progress file template:** [assets/progress-template.md](assets/progress-template.md)

**Rules:**
- Never batch updates - document immediately after each step
- Keep progress files permanently (do not delete on completion)
- Update status field at top when execution completes or blocks

### Verification Tracking

When the spec defines verification criteria (testing, review, validation), track results and issues in the progress file.

After all steps complete, add a Verification section. See [assets/progress-template.md](assets/progress-template.md) for the format.

**Issue statuses:**
- `investigating` - Issue identified, looking into root cause
- `resolution applied, pending verification` - Changes made, awaiting confirmation
- `resolved` - Verified after fix (ONLY after confirmed)
- `wont fix` - Intentional behavior or out of scope

**Rules:**
- Log issues immediately when identified (even before root cause is known)
- Update issue status as investigation progresses
- NEVER mark as "resolved" until verified - no inferring
- Use "resolution applied, pending verification" after applying a fix
- Update check results after issues are resolved and re-verified

### Completion

After all steps are executed and verification passes, confirm completion with the user:

> "All steps complete. Verification [passed/results summary]. Is this work done?"

**The user decides when work is done.** Even if all steps pass verification, the user may identify additional needs, request changes, or want further validation. Do not declare work complete without user confirmation.

### Choosing Execution Mode

Before starting execution, ask the user how to run the steps:

> "Before executing, how should I run the steps?
> - **Direct** (sequential, you review each step)
> - **Subagents** (parallel where possible, faster)
> 
> My recommendation: [direct/subagents] because [reason]."

**If the spec defines an execution plan** → follow it without asking.

**Recommendation criteria:**

| Recommend | When |
|-----------|------|
| **Direct** | Steps have room for interpretation, likely gaps, dependencies, or need user input. Most coding work falls here. |
| **Subagents** | Many similar items (5+), spec has detailed implementation steps (no interpretation needed), items are independent. |

### Direct Execution

Execute steps sequentially in the main process. User can review each step.

1. Invoke the `spec-step-execution` skill
2. Execute the step following that skill
3. Re-invoke `spec-driven-work` skill to restore orchestration context

Re-invoking ensures this skill is fresh in context (not compacted) before continuing to next step.

### Subagent Execution

Delegate step execution to `spec-step-executor` agents. Main process orchestrates; subagents execute.

**Parallel execution:**

The spec MUST explicitly define what can run in parallel:

```markdown
## Execution Plan

**Mode:** Subagents

### Sequential
Steps 1-3 must execute in order.

### Parallel
Steps 4a, 4b, 4c can run in parallel (no shared state).
Max concurrent: 3
Wait for all before Step 5.
```

To launch parallel agents, use multiple Task tool calls in a single message:

```
[Task: spec-step-executor for step 4a]
[Task: spec-step-executor for step 4b]
[Task: spec-step-executor for step 4c]
```

**What to pass to subagents:**
- Spec file path
- Step number/name to execute
- Progress file path (if exists)
- Research file path (if exists)

**Main process responsibilities:**
- Launch subagents (parallel when spec allows)
- Update progress file with results (single writer)
- Handle gap responses from subagents

**Subagent result format:**

| Result | Meaning | Action |
|--------|---------|--------|
| SUCCESS | Step completed, verification passed | Update progress file, proceed to next step |
| FAILED | Step attempted but errored | Investigate error, retry or escalate to user |
| GAP | Spec doesn't cover this situation | Discuss with user, update spec if needed, re-dispatch or execute directly |

---

## Mode Transitions

| Situation | Mode | Action |
|-----------|------|--------|
| User gives clear action + spec exists | Execution | Follow spec |
| User gives clear action + no spec | Development | Create spec first |
| User asks question | Discussion | Discuss, don't act |
| User makes statement | Discussion | Clarify intent before acting |
| Gap found during execution | Development | Pause, fill gap, resume |
| Spec change needed during execution | Development | Propose change, confirm, update spec, resume |

---

## Anti-Patterns

**Don't do these:**

| Anti-Pattern | Instead |
|--------------|---------|
| Jump to editing when user mentions a file | Ask what they want to change |
| Use undefined terms ("market presence") | Define terms first |
| Bundle multiple changes | One change at a time |
| Assume file contents | Read the file |
| Guess at commands | Check documentation |
| Fill spec gaps silently | Flag gaps, discuss |
| Say "I'll do X, Y, and Z" | "First, let's address X. [details]. OK?" |

---

## Checklist

Before taking any action:
- [ ] Is there a spec for this? If yes, am I following it?
- [ ] If no spec, should I create one first?
- [ ] Have I defined all terms I'm using?
- [ ] Have I shown exactly what I'll change?
- [ ] Have I confirmed with user?
- [ ] Am I doing one thing, not multiple things?
