---
name: subagent-driven-development
description: Use when executing implementation plans. Dispatches independent subagents for individual tasks with code review checkpoints between iterations for rapid, controlled development.
---

# Subagent-Driven Development

## Core Principle

**Fresh context per task. Review between tasks.**

Each task gets a clean subagent with no accumulated confusion. You review between tasks.

## How It Works

1. Load the implementation plan
2. For each task:
   - Dispatch fresh subagent
   - Subagent implements ONLY that task
   - Review the changes
   - Approve or request fixes
   - Move to next task

## Benefits

- **Clean Context**: Each subagent starts fresh
- **Focused Work**: One task at a time
- **Review Points**: Catch issues early
- **Controlled Progress**: You stay in charge

## Execution Flow

### Step 1: Load the Plan

```markdown
Loading plan from: docs/plans/YYYY-MM-DD-feature-name.md

Tasks identified:
1. [ ] Task 1: Description
2. [ ] Task 2: Description
3. [ ] Task 3: Description

Starting with Task 1...
```

### Step 2: Dispatch Subagent

For each task, create a focused prompt:

```markdown
## Task: [Task Name]

### Context
- Project: [brief description]
- Current branch: [branch name]
- Dependencies: [relevant info]

### Instructions
[Exact instructions from plan]

### Files to Modify
- `path/to/file.ts`

### Test to Write First
[Test code from plan]

### Implementation
[Implementation code from plan]

### Success Criteria
- [ ] Test passes
- [ ] No other tests broken
- [ ] Code follows project style
```

### Step 3: Review Changes

After subagent completes:

```markdown
## Task 1 Complete

### Changes Made:
- Modified: `path/to/file.ts` (+25/-3)
- Added: `path/to/file.test.ts` (+40)

### Test Results:
✅ All tests passing (47 total)

### Review Checklist:
- [ ] Test covers the requirement
- [ ] Implementation is correct
- [ ] No unnecessary changes
- [ ] Code style matches project

**Approve and continue to Task 2?**
```

### Step 4: Handle Issues

If review finds problems:

```markdown
## Issues Found in Task 1

1. Test doesn't cover edge case X
2. Missing error handling for Y

**Options:**
A) Request fixes from subagent
B) Fix manually
C) Skip and note for later

Which approach?
```

## Subagent Guidelines

### What Subagents Should Do
- Follow the plan exactly
- Write tests first
- Make minimal changes
- Report what was done

### What Subagents Should NOT Do
- Make "improvements" outside scope
- Skip tests
- Refactor unrelated code
- Change the plan

## Progress Tracking

Maintain task status:

```markdown
## Progress: Feature Name

- [x] Task 1: Setup database schema ✅
- [x] Task 2: Create API endpoint ✅
- [ ] Task 3: Add validation (IN PROGRESS)
- [ ] Task 4: Write integration tests
- [ ] Task 5: Update documentation

Current: Task 3 of 5
```

## Checkpoints

### After Each Task
- Run all tests
- Review diff
- Commit if approved

### After All Tasks
- Run integration tests
- Manual verification
- Final review

## Rollback

If things go wrong:

```bash
# Revert last task
git revert HEAD

# Or reset to checkpoint
git reset --hard <commit-before-task>
```

## Communication Pattern

### Starting
"I'm using subagent-driven-development to implement [feature]. I'll dispatch a fresh subagent for each task and review between them."

### Between Tasks
"Task [N] complete. Changes: [summary]. Ready to review before Task [N+1]?"

### Completing
"All [N] tasks complete. Running final verification..."
