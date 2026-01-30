---
name: openspec-change-implementation
description: Implements L0-1 changes from proposals.
allowed-tools: ["Read", "Write", "Grep", "Bash"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "apply this change"
      - "implement the fix"
      - "execute proposal"
      - "apply the bug fix"
      - "implement it"
    keywords:
      - apply
      - execute
      - implement
      - fix
      - proposal
  capabilities:
    - change-implementation
    - code-execution
    - test-execution
    - logging
  prerequisites:
    - proposal
  outputs:
    - implemented-code
    - execution-log
    - test-results
---

# OpenSpec Implement Skill

## When to Invoke

**Automatically activate when user:**
- Says "Implement this change", "Apply the fix", "Execute proposal"
- Asks "Apply this bug fix", "Implement the proposal", "Execute the change"
- Has an approved OpenSpec proposal ready to implement
- Mentions "implement", "apply", "execute" with Level 0-1 context
- Uses words like: apply, execute, implement, change, fix, proposal

**Specific trigger phrases:**
- "Implement this change"
- "Apply the bug fix"
- "Execute the proposal"
- "Apply this change: [proposal-id]"
- "Implement proposal [X]"
- "Execute the fix"

**Prerequisites:**
- OpenSpec proposal exists and is approved
- Change is still Level 0-1 (hasn't grown in scope)
- Environment and dependencies are clear

**Do NOT invoke when:**
- No proposal exists (use openspec-change-proposal first)
- Scope has grown beyond Level 1 (escalate to BMAD)
- Implementing a BMAD story (use bmad-development-execution instead)

**Auto-escalate to BMAD when:**
- Implementation reveals hidden complexity
- Scope expands beyond original proposal
- Tests fail repeatedly indicating design issues

## Mission
Apply small code or configuration changes approved via OpenSpec proposals, ensuring each task is executed transparently with testing evidence.

## Inputs Required
- proposal: latest proposal.md with decision history
- tasks: tasks.md with sequenced work items and owners
- environment: information about repositories, branches, and tooling needed for execution

## Outputs
- Code or configuration changes committed according to tasks
- Test results demonstrating acceptance criteria were met
- Updated proposal/tasks capturing status and follow-ups
- `execution-log.md` documenting commands and evidence (template: `assets/execution-log-template.md.template`)

`scripts/update_execution_log.py` appends timestamped entries to the execution log inside `openspec/changes/<change-id>/`.

## Process
1. Confirm scope and prerequisites via `CHECKLIST.md`.
2. Plan work referencing affected files and dependencies.
3. Implement tasks iteratively, documenting commands and results in `execution-log.md` via the script or manual edits.
4. Run relevant tests or validation steps after each change and capture evidence in the log.
5. Update artifacts and communicate completion or blockers.

## Quality Gates
All checklist items must pass. If complexity grows beyond Level 1, escalate back to BMAD pathways.

## Error Handling
- When prerequisites or environment setup are missing, stop and request clarity.
- If tests fail or scope expands, log findings and recommend next actions, including potential migration to BMAD development-execution.
