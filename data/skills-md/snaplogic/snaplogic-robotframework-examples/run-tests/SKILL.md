---
name: run-tests
description: Guides users on running Robot Framework tests in the SnapLogic project. Use when the user wants to run tests, needs to know which make command to use, or wants to understand test tags and execution options.
user-invocable: true
---

# SnapLogic Test Execution Skill

## Usage Examples

| What You Want | Example Prompt |
|---------------|----------------|
| Run specific tests | `How do I run Oracle tests?` |
| Run multiple tests | `How do I run both Snowflake and Kafka tests?` |
| First time setup | `I'm running tests for the first time, what should I do?` |
| Understand tags | `What tags are available for running tests?` |
| Quick iteration | `I want to run tests quickly without Groundplex setup` |
| View results | `Where are the test results stored?` |
| Troubleshoot | `My tests are failing, how do I debug?` |
| Explain execution | `Explain how to run robot tests in this project` |

---

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/run-tests/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- Run tests for a specific system?
- First time setup or subsequent run?
- With or without Groundplex management?

### Step 3: Provide Quick Answer First
For simple questions, give the command immediately.

### Step 4: Offer More Details If Needed
Only provide additional context if asked.

---

## Quick Command Reference

| Test Type | Command |
|-----------|---------|
| Oracle | `make robot-run-all-tests TAGS="oracle" PROJECT_SPACE_SETUP=True` |
| PostgreSQL | `make robot-run-all-tests TAGS="postgres" PROJECT_SPACE_SETUP=True` |
| Snowflake | `make robot-run-all-tests TAGS="snowflake" PROJECT_SPACE_SETUP=True` |
| Kafka | `make robot-run-all-tests TAGS="kafka" PROJECT_SPACE_SETUP=True` |
| Multiple | `make robot-run-all-tests TAGS="oracle OR postgres" PROJECT_SPACE_SETUP=True` |

**Note:** Use `PROJECT_SPACE_SETUP=True` for first run, omit for subsequent runs.

**Invoke with:** `/run-tests`
