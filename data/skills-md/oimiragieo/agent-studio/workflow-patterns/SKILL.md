---
name: workflow-patterns
description: TDD task implementation patterns - red-green-refactor cycle, phase checkpoints, git commits, and verification protocols for quality assurance.
version: 1.0
model: sonnet
invoked_by: both
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Workflow Patterns

Guide for implementing tasks using TDD workflow, managing phase checkpoints, handling git commits, and executing the verification protocol that ensures quality throughout implementation.

## When to Use This Skill

- Implementing tasks from a track's plan.md
- Following TDD red-green-refactor cycle
- Completing phase checkpoints
- Managing git commits and notes
- Understanding quality assurance gates
- Handling verification protocols
- Recording progress in plan files

## TDD Task Lifecycle

Follow these 11 steps for each task:

### Step 1: Select Next Task

Read plan.md and identify the next pending `[ ]` task. Select tasks in order within the current phase. Do not skip ahead to later phases.

### Step 2: Mark as In Progress

Update plan.md to mark the task as `[~]`:

```markdown
- [~] **Task 2.1**: Implement user validation
```

Commit this status change separately from implementation.

### Step 3: RED - Write Failing Tests

Write tests that define the expected behavior before writing implementation:

- Create test file if needed
- Write test cases covering happy path
- Write test cases covering edge cases
- Write test cases covering error conditions
- Run tests - they should FAIL

Example:

```python
def test_validate_user_email_valid():
    user = User(email="test@example.com")
    assert user.validate_email() is True

def test_validate_user_email_invalid():
    user = User(email="invalid")
    assert user.validate_email() is False
```

### Step 4: GREEN - Implement Minimum Code

Write the minimum code necessary to make tests pass:

- Focus on making tests green, not perfection
- Avoid premature optimization
- Keep implementation simple
- Run tests - they should PASS

### Step 5: REFACTOR - Improve Clarity

With green tests, improve the code:

- Extract common patterns
- Improve naming
- Remove duplication
- Simplify logic
- Run tests after each change - they should remain GREEN

### Step 6: Verify Coverage

Check test coverage meets the 80% target:

```bash
pytest --cov=module --cov-report=term-missing
```

If coverage is below 80%:

- Identify uncovered lines
- Add tests for missing paths
- Re-run coverage check

### Step 7: Document Deviations

If implementation deviated from plan or introduced new dependencies:

- Update tech-stack.md with new dependencies
- Note deviations in plan.md task comments
- Update spec.md if requirements changed

### Step 8: Commit Implementation

Create a focused commit for the task:

```bash
git add -A
git commit -m "feat(user): implement email validation

- Add validate_email method to User class
- Handle empty and malformed emails
- Add comprehensive test coverage

Task: 2.1
Track: user-auth_20250115"
```

Commit message format:

- Type: feat, fix, refactor, test, docs, chore
- Scope: affected module or component
- Summary: imperative, present tense
- Body: bullet points of changes
- Footer: task and track references

### Step 9: Attach Git Notes

Add rich task summary as git note:

```bash
git notes add -m "Task 2.1: Implement user validation

Summary:
- Added email validation using regex pattern
- Handles edge cases: empty, no @, no domain
- Coverage: 94% on validation module

Files changed:
- src/models/user.py (modified)
- tests/test_user.py (modified)

Decisions:
- Used simple regex over email-validator library
- Reason: No external dependency for basic validation"
```

### Step 10: Update Plan with SHA

Update plan.md to mark task complete with commit SHA:

```markdown
- [x] **Task 2.1**: Implement user validation `abc1234`
```

### Step 11: Commit Plan Update

Commit the plan status update:

```bash
git add .claude/context/tracks/*/plan.md
git commit -m "docs: update plan - task 2.1 complete

Track: user-auth_20250115"
```

## Phase Completion Protocol

When all tasks in a phase are complete, execute the verification protocol:

### Identify Changed Files

List all files modified since the last checkpoint:

```bash
git diff --name-only <last-checkpoint-sha>..HEAD
```

### Ensure Test Coverage

For each modified file:

1. Identify corresponding test file
2. Verify tests exist for new/changed code
3. Run coverage for modified modules
4. Add tests if coverage < 80%

### Run Full Test Suite

Execute complete test suite:

```bash
pytest -v --tb=short
```

All tests must pass before proceeding.

### Generate Manual Verification Steps

Create checklist of manual verifications:

```markdown
## Phase 1 Verification Checklist

- [ ] User can register with valid email
- [ ] Invalid email shows appropriate error
- [ ] Database stores user correctly
- [ ] API returns expected response codes
```

### WAIT for User Approval

Present verification checklist to user:

```
Phase 1 complete. Please verify:
1. [ ] Test suite passes (automated)
2. [ ] Coverage meets target (automated)
3. [ ] Manual verification items (requires human)

Respond with 'approved' to continue, or note issues.
```

Do NOT proceed without explicit approval.

### Create Checkpoint Commit

After approval, create checkpoint commit:

```bash
git add -A
git commit -m "checkpoint: phase 1 complete - user-auth_20250115

Verified:
- All tests passing
- Coverage: 87%
- Manual verification approved

Phase 1 tasks:
- [x] Task 1.1: Setup database schema
- [x] Task 1.2: Implement user model
- [x] Task 1.3: Add validation logic"
```

### Record Checkpoint SHA

Update plan.md checkpoints table:

```markdown
## Checkpoints

| Phase   | Checkpoint SHA | Date       | Status   |
| ------- | -------------- | ---------- | -------- |
| Phase 1 | def5678        | 2025-01-15 | verified |
| Phase 2 |                |            | pending  |
```

## Quality Assurance Gates

Before marking any task complete, verify these gates:

### Passing Tests

- All existing tests pass
- New tests pass
- No test regressions

### Coverage >= 80%

- New code has 80%+ coverage
- Overall project coverage maintained
- Critical paths fully covered

### Style Compliance

- Code follows style guides
- Linting passes
- Formatting correct

### Documentation

- Public APIs documented
- Complex logic explained
- README updated if needed

### Type Safety

- Type hints present (if applicable)
- Type checker passes
- No type: ignore without reason

### No Linting Errors

- Zero linter errors
- Warnings addressed or justified
- Static analysis clean

### Security Audit

- No secrets in code
- Input validation present
- Authentication/authorization correct
- Dependencies vulnerability-free

## Git Integration

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change without feature/fix
- `test`: Adding tests
- `docs`: Documentation
- `chore`: Maintenance

### Git Notes for Rich Summaries

Attach detailed notes to commits:

```bash
git notes add -m "<detailed summary>"
```

View notes:

```bash
git log --show-notes
```

Benefits:

- Preserves context without cluttering commit message
- Enables semantic queries across commits
- Supports track-based operations

### SHA Recording in plan.md

Always record the commit SHA when completing tasks:

```markdown
- [x] **Task 1.1**: Setup schema `abc1234`
- [x] **Task 1.2**: Add model `def5678`
```

This enables:

- Traceability from plan to code
- Semantic revert operations
- Progress auditing

## Handling Deviations

During implementation, deviations from the plan may occur. Handle them systematically:

### Types of Deviations

**Scope Addition**
Discovered requirement not in original spec.

- Document in spec.md as new requirement
- Add tasks to plan.md
- Note addition in task comments

**Scope Reduction**
Feature deemed unnecessary during implementation.

- Mark tasks as `[-]` (skipped) with reason
- Update spec.md scope section
- Document decision rationale

**Technical Deviation**
Different implementation approach than planned.

- Note deviation in task completion comment
- Update tech-stack.md if dependencies changed
- Document why original approach was unsuitable

**Requirement Change**
Understanding of requirement changes during work.

- Update spec.md with corrected requirement
- Adjust plan.md tasks if needed
- Re-verify acceptance criteria

### Deviation Documentation Format

When completing a task with deviation:

```markdown
- [x] **Task 2.1**: Implement validation `abc1234`
  - DEVIATION: Used library instead of custom code
  - Reason: Better edge case handling
  - Impact: Added email-validator to dependencies
```

## Error Recovery

### Failed Tests After GREEN

If tests fail after reaching GREEN:

1. Do NOT proceed to REFACTOR
2. Identify which test started failing
3. Check if refactoring broke something
4. Revert to last known GREEN state
5. Re-approach the implementation

### Checkpoint Rejection

If user rejects a checkpoint:

1. Note rejection reason in plan.md
2. Create tasks to address issues
3. Complete remediation tasks
4. Request checkpoint approval again

### Blocked by Dependency

If task cannot proceed:

1. Mark task as `[!]` with blocker description
2. Check if other tasks can proceed
3. Document expected resolution timeline
4. Consider creating dependency resolution track

## Best Practices

1. **Never skip RED**: Always write failing tests first
2. **Small commits**: One logical change per commit
3. **Immediate updates**: Update plan.md right after task completion
4. **Wait for approval**: Never skip checkpoint verification
5. **Rich git notes**: Include context that helps future understanding
6. **Coverage discipline**: Don't accept coverage below target
7. **Quality gates**: Check all gates before marking complete
8. **Sequential phases**: Complete phases in order
9. **Document deviations**: Note any changes from original plan
10. **Clean state**: Each commit should leave code in working state
11. **Fast feedback**: Run relevant tests frequently during development
12. **Clear blockers**: Address blockers promptly, don't work around them

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
