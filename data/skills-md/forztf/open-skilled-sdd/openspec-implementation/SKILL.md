---
name: openspec-implementation
description: Implements approved specification proposals by working through tasks sequentially with testing and validation. Use when implementing changes, applying proposals, executing spec tasks, or building from approved plans. Triggers include "openspec implement", "implement", "apply change", "execute spec", "work through tasks", "build feature", "start implementation".
---

# Specification Implementation

Systematically implements approved spec proposals by executing tasks sequentially with proper testing and validation.

## Quick Start

Implementation follows a read → execute → test → validate cycle for each task:
1. Read the full proposal and task list
2. Execute tasks one at a time, in order
3. Test each completed task
4. Mark complete only after verification

**Critical rule**: Use TodoWrite to track progress. Never skip tasks or mark incomplete work as done.

## Workflow

Copy this checklist and track progress:

```
Implementation Progress:
- [ ] Step 1: Load and understand the proposal
- [ ] Step 2: Set up TodoWrite task tracking
- [ ] Step 3: Execute tasks sequentially
- [ ] Step 4: Test and validate each task
- [ ] Step 5: Update living specifications (if applicable)
- [ ] Step 6: Mark proposal as implementation-complete
```

### Step 1: Load and understand the proposal

Before starting, read all context:

```bash
# Read the proposal
cat spec/changes/{change-id}/proposal.md

# Read all tasks
cat spec/changes/{change-id}/tasks.md

# Read spec deltas to understand requirements
find spec/changes/{change-id}/specs -name "*.md" -exec cat {} \;
```

**Understand**:
- Why this change is needed (from proposal.md)
- What the expected outcomes are
- Which specs will be affected
- What the acceptance criteria are (from scenarios)

### Step 2: Set up TodoWrite task tracking

Load tasks from tasks.md into TodoWrite **before starting work**:

```markdown
**Pattern**:
Read tasks.md → Extract numbered list → Create TodoWrite entries

**Example**:
If tasks.md contains:
1. Create database migration
2. Implement API endpoint
3. Add tests
4. Update documentation

Then create TodoWrite with:
- content: "Create database migration", status: "in_progress"
- content: "Implement API endpoint", status: "pending"
- content: "Add tests", status: "pending"
- content: "Update documentation", status: "pending"
```

**Why this matters**: TodoWrite gives the user visibility into progress and ensures nothing gets skipped.

### Step 3: Execute tasks sequentially

Work through tasks **one at a time, in order**:

```markdown
For each task:
1. Mark as "in_progress" in TodoWrite
2. Execute the work
3. Test the work
4. Only mark "completed" after verification

NEVER skip ahead or batch multiple tasks before testing.
```

**Task execution pattern**:

```markdown
## Task: {Task Description}

**What**: [Brief explanation of what this task does]

**Implementation**:
[Code changes, file edits, commands run]

**Verification**:
[How to verify this task is complete]
- [ ] Code compiles/runs
- [ ] Tests pass
- [ ] Meets requirement scenarios

**Status**: ✓ Complete / ✗ Blocked / ⚠ Partial
```

### Step 4: Test and validate each task

After each task, verify it works:

**For code tasks**:
```bash
# Run relevant tests
npm test # or pytest, cargo test, etc.

# Run linter
npm run lint

# Check types (if applicable)
npm run type-check
```

**For database tasks**:
```bash
# Verify migration runs
npm run db:migrate

# Check schema matches expected
npm run db:schema
```

**For API tasks**:
```bash
# Test endpoint manually
curl -X POST http://localhost:3000/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Or run integration tests
npm run test:integration
```

**Only mark task complete after all verifications pass**.

### Step 5: Update living specifications (if applicable)

**During implementation**, if you discover the spec deltas need updates:

1. **Document the discovery** in proposal.md or a notes file
2. **Do NOT modify spec deltas** during implementation
3. **After implementation completes**, consider whether spec needs adjustment

**Note**: Spec deltas are merged during archiving (Step 6), not during implementation.

### Step 6: Mark proposal as implementation-complete

After all tasks are complete:

```bash
# Create a completion marker
echo "Implementation completed: $(date)" > spec/changes/{change-id}/IMPLEMENTED
```

**Tell the user**:
```markdown
## Implementation Complete

**Change**: {change-id}
**Tasks completed**: {count}
**Tests**: All passing

**Next step**: Archive this change to merge spec deltas into living documentation.
Say "openspec archive {change-id}" or "archive this change" when ready.
```

## Best Practices

### Pattern 1: Blocked Tasks

If a task cannot be completed:

```markdown
**Mark as blocked**:
- Keep status as "in_progress" (NOT "completed")
- Document the blocker clearly
- Create a new task for resolving the blocker
- Inform the user immediately

**Example**:
Task: "Implement payment processing"
Blocker: "Missing API credentials for payment gateway"
Action: Create new task "Obtain payment gateway credentials"
```

### Pattern 2: Task Dependencies

If tasks have dependencies, verify prerequisites before starting:

```bash
# Example: Database migration must run before API code
# Check migration status
npm run db:status

# Only proceed with API task if migration succeeded
```

### Pattern 3: Incremental Testing

Test incrementally, not at the end:

**Good**:
```
Task 1: Create model → Test model → Mark complete
Task 2: Create API → Test API → Mark complete
Task 3: Add validation → Test validation → Mark complete
```

**Bad**:
```
Task 1, 2, 3 → Implement all → Test everything → Debug failures
```

### Pattern 4: Living Documentation

Keep README, API docs, and comments up to date **as you go**:

```markdown
When adding a new API endpoint, also:
- Update API documentation
- Add example request/response
- Update OpenAPI/Swagger spec
- Add inline code comments
```

## Advanced Topics

**Parallel work**: If tasks are truly independent (e.g., separate modules), you can work on them in parallel, but each must be tested independently.

**Integration points**: When task dependencies exist, use integration tests to verify the connection works.

**Rollback strategy**: For risky changes, create rollback tasks before deploying.

## Common Patterns

### Pattern 1: Database + API + UI

Typical order:
1. Database schema/migration
2. Data access layer (models)
3. Business logic layer (services)
4. API endpoints (controllers)
5. UI integration
6. End-to-end tests

### Pattern 2: Feature Flags

For gradual rollouts:
1. Implement feature behind flag
2. Test with flag enabled
3. Deploy with flag disabled
4. Enable flag incrementally
5. Remove flag after full rollout

### Pattern 3: Breaking Changes

For API breaking changes:
1. Implement new version (v2)
2. Keep old version (v1) working
3. Add deprecation warnings to v1
4. Migrate users to v2
5. Remove v1 (separate task/proposal)

## Anti-Patterns to Avoid

**Don't**:
- Skip testing individual tasks
- Mark tasks complete before verification
- Ignore failing tests ("I'll fix it later")
- Batch multiple tasks before testing
- Modify living specs during implementation
- Work out of order (dependencies break)

**Do**:
- Test each task immediately
- Fix failing tests before proceeding
- Update TodoWrite in real-time
- Document blockers clearly
- Communicate progress to user
- Keep commits atomic and descriptive

## Troubleshooting

### Issue: Tests failing after task completion

**Solution**:
```markdown
1. Do NOT mark task complete
2. Debug the failure
3. Fix the code
4. Re-run tests
5. Only mark complete after pass
```

### Issue: Task is too large

**Solution**:
```markdown
1. Break into subtasks
2. Update TodoWrite with subtasks
3. Complete subtasks sequentially
4. Mark parent task complete after all subtasks done
```

### Issue: Dependency not met

**Solution**:
```markdown
1. Pause current task
2. Complete dependency first
3. Test dependency
4. Resume original task
```

## Reference Materials

- [TASK_PATTERNS.md](reference/TASK_PATTERNS.md) - Common task execution patterns
- [TESTING_STRATEGIES.md](reference/TESTING_STRATEGIES.md) - Testing approaches by task type

---

**Token budget**: This SKILL.md is approximately 430 lines, under the 500-line recommended limit.
