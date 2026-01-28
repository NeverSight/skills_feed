---
name: spec-gathering
description: 'Requirements gathering workflow for specification creation. Use when starting a new feature, task, or project that needs structured requirements.'
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, AskUserQuestion]
best_practices:
  - Ask smart questions, produce structured output
  - Confirm understanding before proceeding
  - Identify services and dependencies early
error_handling: graceful
streaming: supported
source: auto-claude
---

# Requirements Gathering Skill

## Overview

Gather user requirements through structured questioning and produce a validated requirements document. This skill transforms vague task descriptions into actionable, structured requirements.

**Core principle:** Ask smart questions, produce valid structured output. Nothing else.

## When to Use

**Always:**

- Starting a new feature or project
- Clarifying ambiguous task descriptions
- When user provides high-level goals without specifics
- Before spec writing begins

**Exceptions:**

- Simple bug fixes with clear reproduction steps
- Single-file changes with obvious scope
- User explicitly provides complete requirements

## The Iron Law

```
NO SPEC WRITING WITHOUT VALIDATED REQUIREMENTS FIRST
```

Requirements must be confirmed by the user before proceeding to spec creation.

## Workflow

### Phase 1: Load Project Context

Understand the project structure before engaging the user.

**Steps:**

1. Read project structure files if they exist
2. Identify services, tech stack, and ports
3. Understand existing patterns and conventions

```bash
# Read project structure
cat .claude/context/product.md 2>/dev/null || echo "No product context"
cat .claude/context/tech-stack.md 2>/dev/null || echo "No tech stack"
```

### Phase 2: Understand the Task

If a task description was provided, confirm it:

> "I understand you want to: [task description]. Is that correct? Any clarifications?"

If no task was provided, ask:

> "What would you like to build or fix? Please describe the feature, bug, or change you need."

**Wait for user response.**

### Phase 3: Determine Workflow Type

Based on the task, determine the workflow type:

| If task sounds like...              | Workflow Type   |
| ----------------------------------- | --------------- |
| "Add feature X", "Build Y"          | `feature`       |
| "Migrate from X to Y", "Refactor Z" | `refactor`      |
| "Fix bug where X", "Debug Y"        | `investigation` |
| "Migrate data from X"               | `migration`     |
| Single service, small change        | `simple`        |

Ask to confirm:

> "This sounds like a **[workflow_type]** task. Does that seem right?"

### Phase 4: Identify Services and Scope

Based on the project context and task, suggest affected areas:

> "Based on your task and project structure, I think this involves:
>
> - **[service1]** (primary) - [why]
> - **[service2]** (integration) - [why]
>
> Any other services or areas involved?"

Wait for confirmation or correction.

### Phase 5: Gather Detailed Requirements

Ask targeted questions:

1. **"What exactly should happen when [key scenario]?"**
2. **"Are there any edge cases I should know about?"**
3. **"What does success look like? How will you know it works?"**
4. **"Any constraints?"** (performance, compatibility, etc.)

Collect answers.

### Phase 6: Confirm and Output

Summarize what you understood:

> "Let me confirm I understand:
>
> **Task**: [summary]
> **Type**: [workflow_type]
> **Scope**: [list of affected areas]
>
> **Requirements**:
>
> 1. [req 1]
> 2. [req 2]
>
> **Success Criteria**:
>
> 1. [criterion 1]
> 2. [criterion 2]
>
> Is this correct?"

Wait for confirmation.

### Phase 7: Create Requirements Document

Create the structured requirements output:

```markdown
# Requirements: [Task Name]

## Overview

[One paragraph summary]

## Workflow Type

[feature|refactor|investigation|migration|simple]

## Scope

- **[area1]** (primary) - [role]
- **[area2]** (integration) - [role]

## Requirements

1. [Requirement 1]
2. [Requirement 2]

## Acceptance Criteria

1. [Criterion 1]
2. [Criterion 2]

## Constraints

- [Constraint 1 if any]

## Out of Scope

- [What this task does NOT include]
```

Save to `.claude/context/requirements/[task-name].md`

## Verification Checklist

Before completing requirements gathering:

- [ ] Task description confirmed with user
- [ ] Workflow type determined and confirmed
- [ ] Scope and affected areas identified
- [ ] Specific requirements captured
- [ ] Acceptance criteria defined
- [ ] Constraints documented
- [ ] User confirmed final summary

## Common Mistakes

### Assuming Instead of Asking

**Why it's wrong:** Assumptions lead to building the wrong thing.

**Do this instead:** Ask clarifying questions. Confirm understanding.

### Skipping Confirmation

**Why it's wrong:** User may have misunderstood your summary.

**Do this instead:** Always summarize and wait for explicit confirmation.

### Vague Requirements

**Why it's wrong:** "Make it better" is not actionable.

**Do this instead:** Get specific: What behavior? What outcome? How to verify?

## Integration with Other Skills

This skill works well with:

- **spec-writing**: Use gathered requirements as input for spec creation
- **complexity-assessment**: Assess complexity after requirements are clear
- **brainstorming**: Use for creative exploration before requirements gathering

## Examples

### Example 1: Feature Request

**Input:** "Add user authentication to the app"

**Process:**

1. Confirm: "You want to add user authentication. Is this username/password, OAuth, or something else?"
2. Identify scope: "This will touch the backend API, database, and frontend login page."
3. Get specifics: "Should users be able to reset passwords? Need email verification?"
4. Define success: "Users can sign up, log in, and access protected routes."

**Output:** Structured requirements document with clear scope and acceptance criteria.

### Example 2: Bug Investigation

**Input:** "The page loads slowly"

**Process:**

1. Clarify: "Which page specifically? What do you consider slow?"
2. Context: "When did this start? Any recent changes?"
3. Metrics: "What load time would be acceptable?"

**Output:** Investigation requirements with specific pages, metrics, and success criteria.

## Troubleshooting

### Issue: User gives one-word answers

**Symptoms:** "Yes", "No", "That's fine" without detail.

**Solution:** Ask more specific questions. Provide options: "Would you prefer A, B, or C?"

### Issue: Scope keeps expanding

**Symptoms:** Every answer adds new features.

**Solution:** Document "Out of Scope" explicitly. Confirm: "Should we include this in this task or save for later?"

## Memory Protocol

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
