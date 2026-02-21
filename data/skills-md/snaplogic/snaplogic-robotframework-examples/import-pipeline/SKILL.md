---
name: import-pipeline
description: Creates Robot Framework test cases for importing SnapLogic pipelines. Use when the user wants to import pipelines (.slp files), needs to know prerequisites for pipeline import, or wants to see pipeline import test case examples.
user-invocable: true
---

# SnapLogic Pipeline Import Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/import-pipeline/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Import a single pipeline or multiple pipelines?
- Need prerequisites checklist?
- Create test case?
- Show template or examples?
- Questions about pipeline parameterization?

### Step 3: Follow the Guide — Create ALL Required Files (MANDATORY)
When creating pipeline import test cases, you **MUST call the Write tool** to create ALL required files. Never skip any file. Never say "file already exists". Always write them fresh:
1. **Robot test file** (`.robot`) in `test/suite/pipeline_tests/[type]/` — WRITE this
2. **PIPELINE_IMPORT_README.md** with file structure tree diagram in the same test directory — WRITE this

Use the detailed instructions from the file you loaded in Step 1 for templates and conventions.

### Step 4: Respond to User
Provide the created files or requested information based on the complete guide.

---

## Quick Reference

**Pipeline file location:**
```
src/pipelines/your_pipeline.slp
```

**Required variables:**
- `${pipeline_name}` - Logical name (without .slp extension)
- `${pipeline_file_name}` - Physical file name (with .slp extension)
- `${PIPELINES_LOCATION_PATH}` - SnapLogic destination path
- `${unique_id}` - Generated in suite setup

**Invoke with:** `/import-pipeline`
