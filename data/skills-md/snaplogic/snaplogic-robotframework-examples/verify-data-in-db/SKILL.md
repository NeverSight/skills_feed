---
name: verify-data-in-db
description: Creates Robot Framework test cases for verifying data in database tables. Use when the user wants to verify record counts, export data to CSV, compare actual vs expected output, or validate pipeline execution results.
user-invocable: true
---

# SnapLogic Data Verification Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/verify-data-in-db/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Verify record count in a table?
- Export data to CSV for comparison?
- Compare actual vs expected output?
- Which database type? (Oracle, Snowflake, PostgreSQL, etc.)
- What verification criteria?

### Step 3: Follow the Guide — Create ALL Required Files (MANDATORY)
When creating data verification test cases, you **MUST call the Write tool** to create ALL required files. Never skip any file. Never say "file already exists". Always write them fresh:
1. **Robot test file** (`.robot`) in `test/suite/pipeline_tests/[type]/` — WRITE this
2. **VERIFY_DATA_README.md** with file structure tree diagram in the same test directory — WRITE this

Use the detailed instructions from the file you loaded in Step 1 for templates and conventions.

### Step 4: Respond to User
Provide the created files or requested information based on the complete guide.

---

## Quick Reference

**Key keywords:**
- `Capture And Verify Number of records From DB Table` — Verify record count
- `Export DB Table Data To CSV` — Export table data to CSV
- `Compare CSV Files With Exclusions Template` — Compare actual vs expected CSV

**Prerequisites:**
- Pipeline must have been executed (triggered task completed)
- Database connection must be established in Suite Setup

**Invoke with:** `/verify-data-in-db`
