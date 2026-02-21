---
name: compare-csv
description: Creates Robot Framework test cases for comparing actual vs expected CSV output files. Use when the user wants to compare CSV files, validate pipeline output against expected results, or needs to exclude dynamic columns from comparison.
user-invocable: true
---

# SnapLogic Compare CSV Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/compare-csv/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Which files to compare? (actual vs expected)
- Should row order be ignored?
- Which columns to exclude from comparison? (timestamps, dynamic IDs, etc.)
- What is the expected status? (IDENTICAL, DIFFERENT, SUBSET)
- Is this standalone or part of a larger test suite?

### Step 3: Follow the Guide — Create ALL Required Files (MANDATORY)
When creating CSV comparison test cases, you **MUST call the Write tool** to create ALL required files. Never skip any file. Never say "file already exists". Always write them fresh:
1. **Robot test file** (`.robot`) in `test/suite/pipeline_tests/[type]/` — WRITE this
2. **COMPARE_CSV_README.md** with file structure tree diagram in the same test directory — WRITE this

Use the detailed instructions from the file you loaded in Step 1 for templates and conventions.

### Step 4: Respond to User
Provide the created files or requested information based on the complete guide.

---

## Quick Reference

**Key keywords:**
- `Compare CSV Files With Exclusions Template` — Compare CSV files with column exclusions
- `Compare CSV Files Template` — Compare CSV files without exclusions

**Arguments for `Compare CSV Files With Exclusions Template`:**
1. `file1_path` — Path to actual output CSV file
2. `file2_path` — Path to expected output CSV file
3. `ignore_order` — Whether to ignore row order (`${TRUE}` or `${FALSE}`)
4. `show_details` — Whether to show detailed differences (`${TRUE}` or `${FALSE}`)
5. `expected_status` — Expected comparison result (`IDENTICAL`, `DIFFERENT`, `SUBSET`)
6. `@exclude_keys` — Columns to exclude from comparison (varargs)
7. `&options` — Additional options like `match_key=column_name`

**Invoke with:** `/compare-csv`
