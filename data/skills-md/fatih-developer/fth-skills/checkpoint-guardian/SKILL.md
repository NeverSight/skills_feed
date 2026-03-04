---
name: checkpoint-guardian
description: Automatic risk assessment before every critical action in agentic workflows. Detects irreversible operations (file deletion, database writes, deployments, payments), classifies risk level, and requires confirmation before proceeding. Triggers on destructive keywords like deploy, delete, send, publish, update database, process payment.
---

# Checkpoint Guardian Protocol

Stop before every critical action, assess the risk level, and require confirmation when needed. Goal: catch irreversible mistakes before they happen.

---

## Workflow

```
1. Detect critical action in the current step
2. Classify risk level (LOW / MEDIUM / HIGH)
3. Apply checkpoint behavior based on level
4. Log the checkpoint decision
5. Show audit trail at end of task
```

---

## Risk Levels

### LOW RISK — Pass Silently

Reversible, limited side effects, common operations:
- Reading files, listing directories
- Creating new files (without overwriting)
- Read-only API calls (GET)
- Writing to console/logs
- Creating temporary files

**Behavior:** No checkpoint shown. Log the action silently for audit trail.

---

### MEDIUM RISK — Brief Confirmation

Reversible but requiring attention:
- Overwriting an existing file (backup possible)
- Inserting new database records (not update/delete)
- POST request to external service (read-purpose)
- Deploying to test/staging environment

**Behavior:** Show a brief checkpoint and ask for confirmation before proceeding.

Use `templates/checkpoint-medium.md.tmpl` for the output format.

---

### HIGH RISK — Full Confirmation Required

Irreversible or wide-impact operations:
- Deleting files or directories
- Updating or deleting database records
- Payment or money transfer
- Deploying to production
- Bulk operations (50+ records, multiple services)
- Operations involving credentials or secrets

**Behavior:** Stop completely. Show detailed checkpoint with impact assessment, reversibility status, and safer alternatives. Do not proceed without explicit "yes" or "proceed" from the user.

Use `templates/checkpoint-high.md.tmpl` for the output format.

---

## Risk Classification

See `references/RISK_MATRIX.md` for the complete risk classification table and escalation rules.

### Escalation Rules

Any of these conditions bumps risk one level up:
- **Bulk operation**: 50+ records or files
- **Production environment**: tagged `prod`, `production`, `live`
- **No rollback path**: no backup, no soft-delete
- **Sensitive data**: PII, payment info, credentials
- **Chain reaction**: this step triggers other critical steps

---

## After Checkpoint Resolution

**User approves:**
1. Execute the action
2. Report result briefly: `Completed: [what was done]`

**User rejects:**
1. Do not execute the action
2. Suggest alternatives: safer path, partial operation, dry-run
3. Wait for the user to set a new direction

---

## Audit Trail

Log every checkpoint decision throughout the task:

```
[CHECKPOINT LOG]
Step     : [step number or sequence]
Action   : [summary]
Risk     : LOW / MEDIUM / HIGH
Decision : Passed silently / Approved / Rejected
```

**At the end of every task**, show the complete checkpoint log summary to the user. This is mandatory — never skip the audit trail.

---

## Guardrails

- **Never skip HIGH RISK checkpoints** — no exceptions, even if the user previously said "approve all."
- **When in doubt, escalate** — if risk level is ambiguous, choose the higher level.
- **Always suggest alternatives** for HIGH RISK actions — give the user a safer path.
- **Audit trail is mandatory** — even LOW RISK actions must be logged silently.
- **Respect explicit user intent** — if the user clearly states "I know the risks, proceed," honor it for that specific action only (not blanket approval).
- This skill applies to **every agent action** — it is not opt-in per step.

---

## Examples

See `references/EXAMPLES.md` for worked examples across all risk levels.

## Templates

- Use `templates/checkpoint-high.md.tmpl` for HIGH RISK checkpoint format.
- Use `templates/checkpoint-medium.md.tmpl` for MEDIUM RISK checkpoint format.
