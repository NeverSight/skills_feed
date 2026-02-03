---
name: split-tasks
description: "Split 3+ independent tasks across parallel agents. Triggers: run in parallel, split tasks, do these at once"
---

# Split Tasks Across Parallel Agents

Dispatch multiple Task agents simultaneously to complete independent work faster.

## When to Use

- 3+ independent tasks with no shared dependencies
- Tasks that don't modify the same files
- Parallel investigations or searches

## When NOT to Use

- Tasks depend on each other's output
- Multiple agents would edit the same file
- Sequential workflow required

## Agent Types

| Type | Use for |
|------|---------|
| `Bash` | Running commands, tests, builds |
| `general-purpose` | Code changes, file edits, research |
| `Explore` | Codebase investigation, finding patterns |

## Process

1. Identify remaining tasks from conversation
2. Filter to independent tasks only
3. Launch 3-6 Task agents in a **SINGLE message** (parallel tool calls)
4. Wait for all to complete
5. Consolidate results and report summary

## Agent Prompt Template

Each agent needs:
- **Goal**: What to accomplish
- **Context**: Relevant background
- **Success criteria**: How to know it's done

## Example

User: "Fix failing tests, update API docs, and add input validation to forms"

Launch in parallel:
- **Agent 1** (Bash): Run tests, diagnose failures, fix them
- **Agent 2** (general-purpose): Update API documentation to match current endpoints
- **Agent 3** (general-purpose): Add validation to form components

After completion: "All 3 tasks complete. Tests passing (fixed X). Docs updated for Y endpoints. Validation added to Z forms."

## Red Flags

- **Never** dispatch agents that touch the same files
- **Never** assume one agent's output for another (no dependencies)
- **Never** launch more than 6 agents (diminishing returns)
- **Always** consolidate results after all complete

## If an Agent Fails

- Report which agent failed and why
- Do NOT retry automatically (let user decide)
- Other agents' work is still valid
