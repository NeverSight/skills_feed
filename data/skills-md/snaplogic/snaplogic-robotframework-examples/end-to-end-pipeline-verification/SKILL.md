---
name: end-to-end-pipeline-verification
description: Creates a complete Robot Framework test suite with account creation, file uploads, pipeline import, triggered task creation/execution, and data verification. Use when the user needs to set up accounts, upload test files, import pipelines, create/execute triggered tasks, AND verify results together in a single test file.
user-invocable: true
---

# SnapLogic End-to-End Pipeline Verification Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/end-to-end-pipeline-verification/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Which account type(s)? (oracle, postgres, snowflake, etc.)
- Which file(s) to upload? (JSON, CSV, .expr, .jar, etc.)
- Which pipeline(s) to import?
- Create triggered task? What parameters?
- Execute triggered task?
- Verify data in database? Expected record count?
- Single test file or separate files?

### Step 3: Follow the Guide — Create ALL Required Files (MANDATORY)
When creating pipeline setup test cases, you **MUST call the Write tool** to create ALL required files. Never skip any file. Never say "file already exists". Always write them fresh:
1. **Account payload file(s)** (`acc_[type].json`) in `test/suite/test_data/accounts_payload/` — WRITE this
2. **Account env file(s)** (`.env.[type]`) in `env_files/[category]_accounts/` — WRITE this
3. **Combined Robot test file** (`.robot`) in `test/suite/pipeline_tests/[type]/` — WRITE this (includes account creation, file uploads, pipeline import, triggered task creation/execution, AND data verification)
4. **SETUP_README.md** with file structure tree diagram in the same test directory — WRITE this

Use the detailed instructions from the file you loaded in Step 1 for templates and conventions.

### Step 4: Respond to User
Provide the created files or requested information based on the complete guide.

---

## Quick Reference

**This skill combines:**
- `/create-account` — Account creation test cases
- `/upload-file` — File upload test cases
- `/import-pipeline` — Pipeline import test cases
- `/create-triggered-task` — Triggered task creation and execution test cases
- `/verify-data-in-db` — Data verification test cases
- `/export-data-to-csv` — Export database data to CSV for comparison
- `/compare-csv` — Compare actual vs expected CSV output

**Into a single test file that does all seven.**

**Execution order:** Accounts → Files → Pipeline → Create Task → Execute Task → Verify Data → Export CSV → Compare CSV

**Invoke with:** `/end-to-end-pipeline-verification`
