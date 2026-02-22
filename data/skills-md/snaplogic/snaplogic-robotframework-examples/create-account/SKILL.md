---
name: create-account
description: Creates Robot Framework test cases for SnapLogic account creation. Use when the user wants to create accounts (Oracle, PostgreSQL, Snowflake, Kafka, S3, etc.), needs to know what environment variables to configure, or wants to see account test case examples.
user-invocable: true
---

# SnapLogic Account Creation Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/create-account/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Which account type? (oracle, postgres, snowflake, etc.)
- Create test case?
- Check environment variables?
- Show template or examples?
- Multiple accounts needed?

### Step 3: Follow the Guide — Create ALL Required Files (MANDATORY)
When creating account test cases, you **MUST call the Write tool** to create ALL 4 files for EVERY account type (supported or new). Never skip any file. Never say "file already exists". Always write them fresh:
1. **Payload file** (`acc_[type].json`) in `test/suite/test_data/accounts_payload/` — WRITE this
2. **Env file** (`.env.[type]`) in `env_files/[category]_accounts/` — WRITE this
3. **Robot test file** (`.robot`) in `test/suite/pipeline_tests/[type]/` — WRITE this
4. **ACCOUNT_SETUP_README.md** with file structure tree diagram in the same test directory — WRITE this

Use the detailed instructions from the file you loaded in Step 1 for templates and conventions.

### Step 4: Respond to User
Provide the created files or requested information based on the complete guide.

---

## Quick Reference

**Supported account types:**
`oracle`, `postgres`, `mysql`, `sqlserver`, `snowflake`, `snowflake-keypair`, `db2`, `teradata`, `kafka`, `jms`, `s3`, `email`, `salesforce`

**Invoke with:** `/create-account`
