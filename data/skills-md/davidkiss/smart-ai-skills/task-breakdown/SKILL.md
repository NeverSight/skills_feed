---
name: task-breakdown
description: Use when you have specs or requirements for a multi-step task to break it down into detailed tasks, before executing it
---

# Writing Task Breakdown

## Overview

Write comprehensive task breakdowns assuming the expert who is going to implement the specs has zero context for our project and questionable taste. Document everything they need to know: which existing files to check, which files to touch for each task and what changes to make to them. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD.

Assume they are a skilled worker, but know almost nothing about our toolset or problem domain. Assume they don't know how to verify they are doing the right thing.

Review available skills and propose creating new skills if needed. If you propose creating new skills, you MUST create them before creating the task breakdown.

**Announce at start:** "I'm using the task-breakdown skill to create a plan."

**Save tasks to:** `docs/YYYY-MM-DD-<feature-name>-tasks.md`

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Task Breakdown Document Header

**Every task breakdown MUST start with this header:**

```markdown
# [Task Name] Task Breakdown

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plan skill to execute this task breakdown task-by-task.

**Goal:** [One sentence describing what this achieves]

**Approach:** [2-3 sentences about approach]

**Skills:** [List of skills to use]

**Tech Details:** [Key tools, services, technologies/libraries to use]

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Remember
- Exact file paths always
- For coding tasks, complete code in task breakdown (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD

## Execution Handoff

After saving the task breakdown, offer task execution:

**"Task breakdown complete and saved to `docs/YYYY-MM-DD-<feature-name>-tasks.md`.**

**Subagent-based task execution (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

- **REQUIRED SUB-SKILL:** Use subagent-task-execution
- Stay in this session
- Fresh subagent per task + code review