---
name: process-rules
description: Standard Operating Procedures manager - owns all process, rule, and workflow changes. Use this skill when adding workflows, recording lessons learned, proposing rule changes, or auditing process consistency.
---

# Process Rules

Single authority for changes to processes, rules, and workflows.

## When This Skill Activates

- Adding a new workflow
- Recording a mistake/lesson
- Updating process documentation
- Proposing new rules
- After sessions with repeated errors
- Process consistency audits

## Scope

This skill exclusively owns:
- Workflow definitions
- Lessons learned documentation
- Process guides and references
- Rule proposals

## Responsibilities

### 1. Create/Edit Workflows
- Check existing workflows for conflicts
- Follow standard templates
- Update guides if adding new workflow

### 2. Record Lessons Learned
When a mistake is identified:
```markdown
## Lesson: [Title]
- **Date**: YYYY-MM-DD
- **Mistake**: What went wrong
- **Symptom**: How it manifested
- **Fix**: How to prevent it
- **Rule**: (Optional) Proposed rule
```

### 3. Propose Rule Changes
For rules that should apply automatically:
1. Draft the rule text
2. Present to user for approval
3. User applies in settings

### 4. Audit Consistency
Periodically check:
- Workflows don't contradict each other
- Guides match actual workflows
- Lessons learned is up to date

## Change Log Protocol

When making changes:
```markdown
## SOP Change - [DATE]
- **What**: [Description of change]
- **Why**: [Rationale]
- **Files**: [List of files modified]
```

## Anti-Patterns

- Editing workflows without proper review
- Adding lessons without date/context
- Creating overlapping workflows
- Proposing rules without user approval

## Files Under Management

| File Type | Purpose |
|-----------|---------|
| `workflows/*.md` | Role and process definitions |
| `LESSONS_LEARNED.md` | Persistent mistake memory |
| `GUIDE.md` | Quick reference |
| `pre-commit hooks` | Automated checks |
