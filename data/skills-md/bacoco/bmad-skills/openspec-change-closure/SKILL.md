---
name: openspec-change-closure
description: Archives completed L0-1 changes.
allowed-tools: ["Read", "Write", "Grep", "Bash"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "archive this change"
      - "close change"
      - "document change"
      - "finalize change"
      - "archive"
    keywords:
      - archive
      - close
      - document
      - finalize
      - complete
  capabilities:
    - change-archival
    - documentation
    - spec-merging
    - closure
  prerequisites:
    - implemented-code
  outputs:
    - archive-doc
    - merged-specs
    - closure-report
---

# OpenSpec Archive Skill

## When to Invoke

**Automatically activate when user:**
- Says "Archive this change", "Close the change", "Finalize change"
- Asks "Document this change", "Mark as complete", "Archive proposal [X]"
- Has completed an OpenSpec change that needs closure
- Mentions "archive", "close", "document", "finalize" with change context
- Uses words like: archive, close, document, finalize, complete, wrap up

**Specific trigger phrases:**
- "Archive this change"
- "Close change [proposal-id]"
- "Document the change"
- "Finalize the implementation"
- "Mark proposal [X] as complete"
- "Wrap up this change"

**Prerequisites:**
- OpenSpec change has been implemented
- Tests pass and validation is complete
- Deployment or rollout is done (or documented)

**Do NOT invoke when:**
- Change not yet implemented (use openspec-change-implementation)
- Tests failing or validation incomplete
- Missing approvals or sign-offs
- Change still in progress

**Auto-document:**
- Learnings and deviations
- Metrics (time, lines changed, tests added)
- Follow-up tasks if any

## Mission
Document the outcome of Level 0-1 work, ensuring artifacts, approvals, and follow-up actions are captured before closing the OpenSpec workflow.

## Inputs Required
- proposal: original proposal.md with approvals
- implementation_log: execution notes or commits from implement skill
- validation_evidence: test results or reviewer feedback

## Outputs
- Archive summary (`archive.md`) with outcomes, metrics, and learnings (template: `assets/archive-template.md.template`)
- Updated proposal/tasks reflecting completion status
- Deployment or rollback notes stored with project documentation
- Canonical specs in `openspec/specs/` synchronized with approved deltas

`scripts/archive_change.py` copies validated spec deltas from `openspec/changes/<change-id>/specs/` into `openspec/specs/`.

## Process
1. Verify closure conditions using `CHECKLIST.md`.
2. Gather final state: what shipped, what remains, and any deviations.
3. Record metrics, approvals, and validation evidence in `archive.md`.
4. Run `scripts/archive_change.py <change-id>` to merge spec deltas into `openspec/specs/`.
5. Capture learnings and recommended follow-up actions, then update artifacts and communicate closure.

## Quality Gates
All checklist items must pass before marking work as archived.

## Error Handling
- If validation evidence or approvals are missing, request them before closing.
- Surface outstanding tasks and assign owners if work cannot be fully archived.
