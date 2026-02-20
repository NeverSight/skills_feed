---
name: create-triggered-task
description: Creates Robot Framework test cases for creating and executing SnapLogic triggered tasks. Use when the user wants to create triggered tasks for on-demand pipeline execution, execute triggered tasks with parameters, or wants to see triggered task test case examples.
user-invocable: true
---

# SnapLogic Triggered Task Creation & Execution Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/create-triggered-task/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Which pipeline is the triggered task for?
- What parameters need to be passed?
- Need notifications configured?
- Create task only, or create AND execute?
- Create test case or show template?

### Step 3: Follow the Guide — Create ALL Required Files (MANDATORY)
When creating triggered task test cases, you **MUST call the Write tool** to create ALL required files. Never skip any file. Never say "file already exists". Always write them fresh:
1. **Robot test file** (`.robot`) in `test/suite/pipeline_tests/[type]/` — WRITE this
2. **TRIGGERED_TASK_README.md** with file structure tree diagram in the same test directory — WRITE this

Use the detailed instructions from the file you loaded in Step 1 for templates and conventions.

### Step 4: Respond to User
Provide the created files or requested information based on the complete guide.

---

## Quick Reference

**Template keywords:**
- `Create Triggered Task From Template` — Creates a triggered task
- `Run Triggered Task With Parameters From Template` — Executes a triggered task

**Prerequisites:**
- Pipeline must be imported first (`/import-pipeline`)
- Accounts must be created first (`/create-account`)

**Invoke with:** `/create-triggered-task`
