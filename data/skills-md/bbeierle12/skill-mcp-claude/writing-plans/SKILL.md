---
name: writing-plans
description: Use after brainstorming/design phase to create detailed implementation plans. Creates step-by-step plans clear enough for execution by any developer.
---

# Writing Plans

## Core Principle

Write plans clear enough for **an enthusiastic junior engineer with poor taste, no judgement, no project context, and an aversion to testing** to follow.

## Plan Structure

Save plans to: `docs/plans/YYYY-MM-DD-<feature-name>.md`

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** Use executing-plans skill to implement this plan task-by-task.

## Overview
Brief description of what we're building and why.

## Prerequisites
- [ ] Dependency 1 installed
- [ ] Service 2 running
- [ ] Access to X configured

## Tasks

### Task 1: [Descriptive Name]
**File:** `path/to/file.ts`
**Test:** `path/to/file.test.ts`

#### Test First (RED)
```typescript
// Exact test code to write
describe('FeatureName', () => {
  it('should do specific thing', () => {
    // Arrange
    // Act  
    // Assert
  });
});
```

#### Implementation (GREEN)
```typescript
// Exact implementation code
export function featureName() {
  // Implementation
}
```

#### Verification
```bash
npm test -- --grep "FeatureName"
# Expected: 1 passing
```

### Task 2: [Next Task]
...

## Integration Tests
After all tasks complete:
```bash
# Commands to run
npm run test:integration
```

## Manual Verification
Steps to manually verify the feature works:
1. Step 1
2. Step 2
3. Expected result

## Rollback Plan
If something goes wrong:
1. `git revert HEAD`
2. ...
```

## Plan Quality Checklist

### Every Task Must Have:
- [ ] Exact file paths
- [ ] Complete code (not "add validation")
- [ ] Test written BEFORE implementation
- [ ] Verification command with expected output
- [ ] Clear success criteria

### Plan Must Include:
- [ ] Prerequisites listed
- [ ] Tasks in dependency order
- [ ] Integration test at end
- [ ] Rollback instructions

## Writing Guidelines

### Be Explicit
❌ "Add error handling"
✅ "Wrap the API call in try/catch, log errors with context, return null on failure"

### Be Complete
❌ "Update the config"
✅ ```json
{
  "setting": "value",
  "newSetting": "newValue"
}
```

### Be Ordered
Tasks should be executable in sequence:
1. No forward dependencies
2. Each task builds on previous
3. Tests pass after each task

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved. Two execution options:**

**1. Subagent-Driven (this session)**
- Fresh subagent per task
- Review between tasks
- Fast iteration

**2. Parallel Session (separate)**
- Open new session with executing-plans skill
- Batch execution with checkpoints

**Which approach?"**

## DRY, YAGNI, TDD Reminders

Include at top of every plan:

```markdown
## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits
```

## Anti-Patterns

### Don't Do This
- Vague task descriptions
- Missing file paths
- Incomplete code snippets
- Implementation before tests
- No verification steps
- Assuming context
