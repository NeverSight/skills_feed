---
name: agents-reminder
description: Reminds the agent to refresh on AGENTS.md guidelines before proceeding with tasks. Use at the start of a session or when unsure about agent policies.
---

# AGENTS.md Refresh Reminder

## When to Use This Skill

Use this skill when the user:

- Starts a new session and you need to re-sync on repo rules
- Mentions or references `AGENTS.md`
- Asks you to follow “the rules” and you need to confirm what they are
- You suspect policy drift and want to avoid accidental violations (git, db, filesystem, tests, etc.)

Prompt the agent to re-read and apply the current guidelines in AGENTS.md before continuing work.

## Workflow

1. Locate AGENTS.md in the repository root (or specified path).
2. Read the full file to refresh constraints and required behaviors and re-answer the previous question

## Scope Boundaries

**DO:** Locate and read AGENTS.md, summarize the rules, and align actions accordingly.

**DO NOT:** Skip reading AGENTS.md when this skill is invoked or assume prior knowledge.

## Reminder Template

Use this short reminder when beginning a task:

"Before proceeding, I will review AGENTS.md to refresh the current guidelines and ensure compliance."

## Example

**Scenario:** Starting a new user request where policies may have changed.

**Response:**

"Before proceeding, I will review AGENTS.md to refresh the current guidelines and ensure compliance."
