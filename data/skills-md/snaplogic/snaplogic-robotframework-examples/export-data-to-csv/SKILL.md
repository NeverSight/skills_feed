---
name: export-data-to-csv
description: Creates Robot Framework test cases for exporting database table data to CSV files. Use when the user wants to export Oracle, Snowflake, PostgreSQL, or other database data to CSV for verification or comparison purposes.
user-invocable: true
---

# SnapLogic Export Data to CSV Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/export-data-to-csv/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Which database type? (Oracle, Snowflake, PostgreSQL, etc.)
- Which table to export?
- What column to order by?
- Where to save the CSV output file?
- Is this standalone or part of a larger test suite?

### Step 3: Follow the Guide — Create ALL Required Files (MANDATORY)
When creating export data test cases, you **MUST call the Write tool** to create ALL required files. Never skip any file. Never say "file already exists". Always write them fresh:
1. **Robot test file** (`.robot`) in `test/suite/pipeline_tests/[type]/` — WRITE this
2. **EXPORT_DATA_README.md** with file structure tree diagram in the same test directory — WRITE this

Use the detailed instructions from the file you loaded in Step 1 for templates and conventions.

### Step 4: Respond to User
Provide the created files or requested information based on the complete guide.

---

## Quick Reference

**Key keyword:**
- `Export DB Table Data To CSV` — Export database table data to a CSV file

**Arguments:**
1. `table_name` — The database table to export (e.g., DEMO.TEST_TABLE1)
2. `order_by_column` — Column to use for ordering rows (e.g., DCEVENTHEADERS_USERID)
3. `output_file` — Local path to save the CSV file

**Prerequisites:**
- Database connection must be established in Suite Setup
- Table must exist and contain data

**Invoke with:** `/export-data-to-csv`
