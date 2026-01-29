---
name: jss
description: JavaScript stack ecosystem. Best practices, patterns, and guidelines for React, RN, Next.js, Nest.js, etc.
---

# JSS (JavaScript stack skills)

## Command Structure

Commands follow flag-based pattern: `/jss --<stack> --<action> [args-flag] optional extra user message instructions`

## Workflow Execution

### 1. Parse Flags

Extract stack and action from flag args or user message instructions:

**Pattern matching:**

- Match `skills/<stack>/references/<action>` for stack and action.
- Capture remaining text as args-flag (extra user message instructions).

### 2. Validate

Check if workflow exists for the stack/action combination.
If not implemented, inform user it's coming soon with status.

### 3. Load Reference

Read appropriate workflow from `skills/<stack>/references/<action>.md`.

### 4. Execute

Follow workflow steps:

- Parse arguments (if provided)
- Gather requirements (AskUserQuestion if needed)
- Run commands
- Configure files
- Report completion
