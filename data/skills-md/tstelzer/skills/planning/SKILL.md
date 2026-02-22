---
name: planning
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Planning

## Overview

Write comprehensive implementation plans assuming the engineer has zero context
for our codebase and questionable taste. Document everything they need to know:
which files to touch for each task, code, testing, docs they might need to
check, how to test it. Give them the whole plan as bite-sized tasks.

Assume they are a skilled developer, but know almost nothing about our toolset
or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the planning skill to create the implementation plan."

**Save plans to:** `<repository-root>/plans/YYYY-MM-DD_HH:MM_<plan-name>.md`

## Plan Structure

```markdown
# Plan: <Feature Name>

## Summary
<One paragraph describing what this builds>

## Prerequisites
<Setup steps, deps to install, docs to read — skip if none>

## Open Questions
<Unknowns or decisions to resolve before/during implementation — skip if none>

## Out of Scope
<What this plan explicitly does NOT cover>

## Overview
<A couple of paragraphs about approach>

## Task <n>: <name>
**Files:** `path/to/file.ts:42`, ...
**Depends on:** Task <m> (if any)

<What to do and why. Verbose — include code when useful.>

**Verify:** <How to confirm this task is done — command, test, manual check>
```

## Remember

- Exact file paths always, with line-numbers if relevant
- Verbose description of implementation, or even complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills
- Order tasks by dependency; call out blocking relationships
- Each task should be independently verifiable
- When open questions are answered, integrate the answers into the plan and remove them from **Open Questions**
- When prerequisites are satisfied or resolved, integrate them into the plan and remove them from **Prerequisites**
