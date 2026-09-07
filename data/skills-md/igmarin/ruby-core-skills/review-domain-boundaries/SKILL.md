---
name: review-domain-boundaries
license: MIT
description: >
  Use when reviewing a Ruby app for DDD (domain-driven design) boundaries, module boundaries,
  service boundaries, or code organization: detects bounded contexts, language leakage,
  cross-context orchestration, and unclear ownership — uses `rg` to find cross-context
  references and leaked terms, identifies misplaced domain models and documents ownership
  direction (which context owns invariants, transitions, and side effects), proposes the
  smallest credible
  boundary improvement before large reorganizations, outputs findings first then open
  questions then recommended next skills, and loads boundary-leakage examples only when
  their content is needed. Covers context mapping, leakage detection, and cross-context
  coupling.
metadata:
  version: 1.0.0
  user-invocable: "true"
  origin: "Extracted from igmarin/rails-agent-skills v5.1.17"
---
# Review Domain Boundaries

## Quick Reference

| Area | What to check |
|------|---------------|
| Bounded contexts | Distinct language, rules, and ownership |
| Context leakage | One area reaching across another's concepts casually |
| Shared models | Same object name used with conflicting meanings |
| Orchestration | Use cases coordinating multiple contexts without a clear owner |
| Ownership | Who owns invariants, transitions, and side effects |

## HARD-GATE

```text
DO NOT recommend splitting code into new contexts unless the business boundary is explicit enough to name.
DO NOT treat every large module as a bounded context automatically.
ALWAYS identify the leaked language or ownership conflict before proposing structural changes.
```

## Core Process

**Core principle:** Fix context leakage before adding more patterns.

### When to Use

- **Next step:** Chain to `model-domain` when a context is clear enough to model tactically, or to `refactor-process` when boundaries need incremental extraction.

### Review Order

1. **Map entry points:** Start from controllers, jobs, services, APIs, and UI flows that expose business behavior.
2. **Name the contexts:** Group flows and rules by business capability, not by current folder names alone.
3. **Find leakage:** Look for terms, validations, workflows, or side effects crossing context boundaries.
4. **Check ownership:** Decide which context should own invariants, transitions, and external side effects.
   - For Fleet/Billing examples, Billing owns invoice generation triggers and invoice side effects; Fleet owns vehicle state and availability. Flag `Fleet::Vehicle` triggering invoice generation as leakage into Billing, not the reverse.
5. **Propose the smallest credible improvement:** Rename, extract, isolate, or wrap before attempting large reorganizations.

### Detecting Leakage

Use search tools to find cross-context references before reading code manually:

```bash
# Find references from one context into another
rg 'Billing.*Fleet|Fleet.*Billing' lib/ app/

# Find cross-namespace constant usage
rg 'Billing::[A-Z]' lib/services/fleet/ services/fleet/
rg 'Fleet::[A-Z]' lib/services/billing/ services/billing/

# Find callbacks or triggers that touch foreign concepts
rg 'after_(create|update|save).*Job|after_(create|update|save).*Mailer' lib/ app/

# Find invoice-generation triggers leaking out of Billing
rg 'invoice|Invoice|Billing' lib/ app/ services/
```

### Common Pitfalls

- Treating a shared database table as proof of a shared context — storage and domain boundaries are independent concerns.
- Splitting into new contexts before the business language is stable enough to name them clearly.
- Mistaking a large Ruby namespace for a bounded context without checking whether it has a single, coherent set of rules and an identifiable owner.

## Ownership Direction

When documenting ownership, state **which context owns which capability** and **what the other context must not do**. Apply to the project's domain, not pre-existing examples.

| Pattern | Good | Bad |
|---------|------|-----|
| **State ownership** | `Billing owns invoice state; Fleet never writes invoice columns` | `Billing and Fleet both manage invoice state` |
| **Trigger ownership** | `Billing owns invoice-generation triggers; Fleet emits events instead` | `Fleet::Vehicle calls Billing::InvoiceGenerator directly` |
| **Validation ownership** | `Fleet owns vehicle availability rules; Billing queries a read model` | `Billing::InvoiceService checks Fleet::Vehicle.available?` |
| **Side-effect ownership** | `Billing owns email/sidekiq after invoice creation; Fleet has no invoice callbacks` | `Fleet::Reservation after_save generates an invoice` |
| **Crossing pattern** | `Fleet publishes ReservationCompleted; Billing subscribes` | `Billing::InvoiceService.new.call(Fleet::Reservation.last)` |

Document the direction explicitly: `Context X owns <capability>; Context Y must not <action>.`

## Output Style

1. **Finding Format**: For each finding include:
   - **Severity**
   - **Contexts involved**
   - **Leaked term / ownership conflict**
   - **Why the current boundary is risky**
   - **Smallest credible improvement**
   Include the ownership direction when it matters (e.g. Billing should own invoice-generation triggers; Fleet should not trigger invoices from `Fleet::Vehicle`).
2. **Structure**: Write findings first, then list open questions and recommended next skills.
3. **Language**: Must be in English unless explicitly requested otherwise.

## Extended Resources

Load only when a concrete boundary-leakage example is needed:

- [EXAMPLES.md](./EXAMPLES.md) — Billing/Fleet leakage example with smallest credible fix.

## Integration

| Skill | When to chain |
|-------|---------------|
| **define-domain-language** | When the review is blocked by fuzzy or overloaded terminology |
| **model-domain** | When a context is clear and needs entities/value objects/services modeled cleanly |
| **refactor-process** | When the recommended improvement needs incremental extraction instead of a rewrite |
