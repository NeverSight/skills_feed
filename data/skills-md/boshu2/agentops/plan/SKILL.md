---
name: plan
description: 'Epic decomposition into trackable issues. Triggers: "create a plan", "plan implementation", "break down into tasks", "decompose into features", "create beads issues from research", "what issues should we create", "plan out the work".'
---

# Plan Skill

> **Quick Ref:** Decompose goal into trackable issues with waves. Output: `.agents/plans/*.md` + bd issues.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Execution Steps

Given `/plan <goal>`:

### Step 1: Setup
```bash
mkdir -p .agents/plans
```

### Step 2: Check for Prior Research

Look for existing research on this topic:
```bash
ls -la .agents/research/ 2>/dev/null | head -10
```

Use Grep to search `.agents/` for related content. If research exists, read it with the Read tool to understand the context before planning.

### Step 3: Explore the Codebase (if needed)

**USE THE TASK TOOL** to dispatch an Explore agent:

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Understand codebase for: <goal>"
  prompt: |
    Explore the codebase to understand what's needed for: <goal>

    1. Find relevant files and modules
    2. Understand current architecture
    3. Identify what needs to change

    Return: key files, current state, suggested approach
```

### Step 4: Decompose into Issues

Analyze the goal and break it into discrete, implementable issues. For each issue define:
- **Title**: Clear action verb (e.g., "Add authentication middleware")
- **Description**: What needs to be done
- **Dependencies**: Which issues must complete first (if any)
- **Acceptance criteria**: How to verify it's done

### Step 5: Compute Waves

Group issues by dependencies for parallel execution:
- **Wave 1**: Issues with no dependencies (can run in parallel)
- **Wave 2**: Issues depending only on Wave 1
- **Wave 3**: Issues depending on Wave 2
- Continue until all issues assigned

### Step 6: Write Plan Document

**Write to:** `.agents/plans/YYYY-MM-DD-<goal-slug>.md`

```markdown
# Plan: <Goal>

**Date:** YYYY-MM-DD
**Source:** <research doc if any>

## Overview
<1-2 sentence summary of what we're building>

## Issues

### Issue 1: <Title>
**Dependencies:** None
**Acceptance:** <how to verify>
**Description:** <what to do>

### Issue 2: <Title>
**Dependencies:** Issue 1
**Acceptance:** <how to verify>
**Description:** <what to do>

## Execution Order

**Wave 1** (parallel): Issue 1, Issue 3
**Wave 2** (after Wave 1): Issue 2, Issue 4
**Wave 3** (after Wave 2): Issue 5

## Next Steps
- Run `/crank` for autonomous execution
- Or `/implement <issue>` for single issue
```

### Step 7: Create Tasks for In-Session Tracking

**Use TaskCreate tool** for each issue:

```
Tool: TaskCreate
Parameters:
  subject: "<issue title>"
  description: |
    <Full description including:>
    - What to do
    - Acceptance criteria
    - Dependencies: [list task IDs that must complete first]
  activeForm: "<-ing verb form of the task>"
```

**After creating all tasks, set up dependencies:**

```
Tool: TaskUpdate
Parameters:
  taskId: "<task-id>"
  addBlockedBy: ["<dependency-task-id>"]
```

**IMPORTANT: Create persistent issues for ratchet tracking:**

If bd CLI available, create beads issues to enable progress tracking across sessions:
```bash
# Create epic first
bd create --title "<goal>" --type epic --label "planned"

# Create child issues (note the IDs returned)
bd create --title "<wave-1-task>" --body "<description>" --parent <epic-id> --label "planned"
# Returns: na-0001

bd create --title "<wave-2-task-depends-on-wave-1>" --body "<description>" --parent <epic-id> --label "planned"
# Returns: na-0002

# Add blocking dependencies to form waves
bd dep add na-0001 na-0002
# Now na-0002 is blocked by na-0001 → Wave 2
```

**Waves are formed by `blocks` dependencies:**
- Issues with NO blockers → Wave 1 (appear in `bd ready` immediately)
- Issues blocked by Wave 1 → Wave 2 (appear when Wave 1 closes)
- Issues blocked by Wave 2 → Wave 3 (appear when Wave 2 closes)

**`bd ready` returns the current wave** - all unblocked issues that can run in parallel.

Without bd issues, the ratchet validator cannot track gate progress. This is required for `/crank` autonomous execution and `/post-mortem` validation.

### Step 8: Request Human Approval (Gate 2)

**USE AskUserQuestion tool:**

```
Tool: AskUserQuestion
Parameters:
  questions:
    - question: "Plan complete with N tasks in M waves. Approve to proceed?"
      header: "Gate 2"
      options:
        - label: "Approve"
          description: "Proceed to /pre-mortem or /crank"
        - label: "Revise"
          description: "Modify the plan before proceeding"
        - label: "Back to Research"
          description: "Need more research before planning"
      multiSelect: false
```

**Wait for approval before reporting completion.**

### Step 9: Report to User

Tell the user:
1. Plan document location
2. Number of issues identified
3. Wave structure for parallel execution
4. Tasks created (in-session task IDs)
5. Next step: `/pre-mortem` for failure simulation, then `/crank` for execution

## Key Rules

- **Read research first** if it exists
- **Explore codebase** to understand current state
- **Identify dependencies** between issues
- **Compute waves** for parallel execution
- **Always write the plan** to `.agents/plans/`
