---
name: add-test
description: Creates new Robot Framework test cases for SnapLogic pipeline testing. Use when the user wants to create a new test file, add test cases to existing files, or needs test templates for specific system types (Oracle, PostgreSQL, Snowflake, etc.).
user-invocable: true
---

# Add Test Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/add-test/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Create a new test file from scratch?
- Add test cases to existing file?
- Which system type? (oracle, postgres, snowflake, etc.)
- What kind of test? (smoke, regression, data validation)

### Step 3: Follow the Guide
Use the detailed instructions from the file you loaded in Step 1 to:
- Use correct file structure and templates
- Apply proper naming conventions
- Add appropriate tags
- Include setup/teardown as needed

### Step 4: Respond to User
Create the test file or provide guidance based on the complete guide.

---

## Quick Reference

This guide covers:
- Quick start template
- Test file structure
- Naming conventions
- Tags system
- Setup and teardown patterns
- Variable usage
- Complete test examples
