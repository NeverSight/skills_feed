---
name: intent-and-automation
description: Handling user intent and automating memory tasks.
---

# Skill: TraceMem Intent and Automation Modes

## Purpose
This skill explains how to choose the correct `intent` and `automation_mode` for a Decision Envelope. Correct classification is critical for potential policy checks and audit clarity.

## When to Use
- When calling `decision_create` and you need to populate the arguments.
- When determining if a task requires human-in-the-loop (`propose`) or can be done automatically (`autonomous`).

## When NOT to Use
- Do not invent new automation modes. Stick to the strict list.

## Core Rules
- **Intent is Hierarchical**: Intents must be dot-separated strings ordered from general to specific (Category -> Entity -> Action). Example: `customer.order.refund`.
- **Automation Mode is Binding**: The mode you select declares your authority level.
  - `propose`: You will only read data and suggest actions. You will NOT write/execute.
  - `approve`: You will execute, but only after explicit human approval (often enforced by policy).
  - `override`: You are explicitly breaking a rule (requires high permission).
  - `autonomous`: You will execute immediately without human intervention.

## Correct Usage Pattern

### Choosing an Intent
Structure: `<Domain>.<Entity>.<Action>`
- **Good**: `security.access_log.scan`, `billing.invoice.void`, `support.ticket.reply`.
- **Bad**: `scan_logs`, `fix_thing`, `decision_1`.

### Choosing Automation Mode
1. **Are you just looking?**
   - Mode: `autonomous` (if read-only duties are pre-approved) or `propose` (if you are just gathering info for a human).
2. **Are you planning to change state (write/delete)?**
   - If you need permission first: Mode `propose` (stop after planning).
   - If you have permission but need confirmation: Mode `approve` (TraceMem might force this anyway).
   - If you are fully trusted logic: Mode `autonomous`.

### Example
```json
{
  "intent": "network.firewall.block_ip",
  "automation_mode": "autonomous",
  "actor": "security-agent-v2"
}
```

## Common Mistakes
- **Mismatched Mode**: interacting as `propose` but then trying to `decision_write` (TraceMem may block this or flag it as a violation).
- **Inconsistent Intents**: Using `user.create` in one decision and `create.user` in another. Be consistent.

## Safety Notes
- **Policy Triggers**: Policies are often attached to specific intents. Using the wrong intent might bypass safety checks or trigger unnecessary alarms.
- **Escalation**: If you start as `autonomous` but policy returns `requires_exception`, you effectively switch to an approval flow. The initial mode was your *desired* mode.
