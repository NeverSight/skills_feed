---
name: tasks-generator
description: Generate development tasks from a PRD file with sprint-based planning. Use when users ask to "create tasks from PRD", "break down the PRD", "generate sprint tasks", or want to convert product requirements into actionable development tasks. Creates tasks.md with POC → MVP → Full Features approach and dependency analysis.
---

# Tasks Generator

Transform PRD documents into structured, sprint-based development tasks with dependency analysis.

## Input

PRD file path provided in `$ARGUMENTS`. If empty, ask user for the path.

## Pre-checks

1. Verify `prd.md` exists at provided path
2. Check for existing `tasks.md` - create backup if exists: `tasks_backup_YYYY_MM_DD_HHMMSS.md`
3. Look for supporting docs in same directory: `tad.md`, `ux_design.md`, `brand_kit.md`

## Workflow

### Phase 1: Extract Requirements

From PRD, extract:
- Core features and value proposition
- User stories and personas
- Functional requirements
- Non-functional requirements (performance, security)
- Technical constraints and dependencies

### Phase 2: Define Development Phases

**POC (Proof of Concept):**
- Single most important feature proving core value
- Minimal implementation, 1-2 sprints

**MVP (Minimum Viable Product):**
- Essential features for first release
- Core user workflows

**Full Features:**
- Remaining enhancements
- Nice-to-haves and polish

### Phase 3: Create Sprint Plan

| Sprint | Focus | Scope |
|--------|-------|-------|
| Sprint 1 | POC | Core differentiating feature |
| Sprint 2 | MVP Foundation | Auth, data models, primary workflows |
| Sprint 3 | MVP Completion | UI/UX, integration, validation |
| Sprint 4+ | Full Features | Enhancements, optimization, polish |

### Phase 4: Analyze Dependencies

1. **Map Dependencies**: For each task, identify "Depends On" and "Blocks"
2. **Group Parallel Tasks**: Assign tasks to execution waves
3. **Calculate Critical Path**: Longest dependency chain = minimum duration
4. **Validate**: Check for circular dependencies, broken references

### Phase 5: Generate tasks.md

Create `tasks.md` in same directory as PRD. See [references/tasks-template.md](references/tasks-template.md) for full template.

## Task Format

Each task must include:

```markdown
### Task X.Y: [Action-oriented Title]

**Description**: What and why, referencing PRD

**Acceptance Criteria**:
- [ ] Specific, testable condition 1
- [ ] Specific, testable condition 2

**Dependencies**: None / Task X.X

**PRD Reference**: [Section]
```

## Task Guidelines

- **Title**: Action-oriented (e.g., "Implement user authentication API")
- **Size**: 1-3 days of work; break larger features
- **Criteria**: Cover happy path and edge cases
- **Dependencies**: List prerequisites and external dependencies

## Quality Checks

Before finalizing:
- [ ] All PRD requirements addressed
- [ ] Each task links to PRD
- [ ] No circular dependencies
- [ ] Clear MVP vs post-MVP distinction
- [ ] Ambiguous requirements flagged
- [ ] All tasks in dependency table
- [ ] Critical path identified

## Output Summary

After generating, provide:
1. File location
2. Sprint overview (count, tasks per sprint)
3. MVP scope summary
4. Dependency analysis (waves, critical path, bottlenecks)
5. Flagged ambiguous requirements
6. Next steps: Review Sprint 1 and Wave 1 tasks first
