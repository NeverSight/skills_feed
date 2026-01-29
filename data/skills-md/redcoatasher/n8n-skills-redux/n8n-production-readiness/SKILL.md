---
name: n8n-production-readiness
description: Dynamic tier system for right-sizing n8n workflow hardening. Use this skill on ANY n8n workflow request to determine appropriate validation, logging, and error handling levels. Adapts to user needs — from quick prototypes to mission-critical production systems.
---

# n8n Production Readiness

**Match workflow hardening to actual risk.** Not every workflow needs the same rigor.

> *"The workflow you build locally... that's maybe 20% of what you actually need. The other 80% is security, validation, logging, and error handling."*

---

## How to Use This Skill (AI Instructions)

**The tier system adapts to the user.** Some users want to specify a tier, others just want to build. Support both modes while always being ready to recommend changes based on what you observe.

### After the Initial Prompt: Ask Once

After the user's first message about an n8n workflow, **ask once** to establish the tier — but make it easy to skip:

> "Quick question before we dive in — what level of hardening does this workflow need?
>
> - **Tier 1 (Internal/Prototype):** Quick and simple. Basic error handling, minimal setup.
> - **Tier 2 (Production):** Client-facing or business-critical. Full validation, logging, proper error responses.
> - **Tier 3 (Mission-Critical):** Payments, compliance, high-volume. Everything plus monitoring, rollback plans, idempotency.
>
> Or just say **'autopilot'** and I'll figure it out as we go based on what you're building."

**If the user picks a tier:** Build to that tier. Respect their choice, but still monitor for signals that suggest they need to adjust (see Tier Change Recommendations below).

**If the user says "autopilot" or skips the question:** Infer the tier silently from context and adapt as you go. Don't mention tiers again unless recommending a change.

**If the user doesn't respond to the tier question:** Assume autopilot mode and proceed.

### Respecting Explicit Tier Requests

**If a user explicitly asks for a tier** (now or later in the conversation):
- Build exactly to that tier's specifications
- If they ask "what's in Tier 2?" — explain it
- If they say "make this Tier 3" — upgrade accordingly
- If they say "just keep it Tier 1" — simplify and remove hardening

**Users who understand tiers get full control.** Don't second-guess them on every decision — but still flag concerns if you observe serious issues.

### Tier Lookup Requests

If a user asks to see the tiers, explain them, or wants to understand the differences, provide the full breakdown:

> **Tier 1 (Internal/Prototype)**
> - Basic null checks, simple try-catch
> - n8n's built-in error handling
> - ~10% extra build time
> - *Example: Slack notifications, personal automations*
>
> **Tier 2 (Production)**
> - Full input validation at entry point
> - External logging (Supabase/Postgres)
> - Proper HTTP status codes (400, 401, 404, 500)
> - Error notifications to team
> - Pre-deployment breaking tests
> - ~80% extra build time
> - *Example: Client form handlers, business integrations*
>
> **Tier 3 (Mission-Critical)**
> - Everything in Tier 2, plus:
> - Monitoring dashboards, alerting (PagerDuty)
> - Idempotency keys, rate limiting
> - Rollback strategy, audit logging
> - 2-3x build time
> - *Example: Payment processing, HIPAA compliance*

### Autopilot Mode: Silent Tier Assessment

When in autopilot (or if the user skipped tier selection), infer the tier from context clues:

| Context Clues | Internal Tier | Your Approach |
|---------------|---------------|---------------|
| "quick", "test", "just for me", "internal", "prototype", "playing around" | Tier 1 | Build fast, basic error handling only |
| "client", "customer", "users", "production", "deploy", "business", "launch" | Tier 2 | Include validation, logging, status codes |
| "payment", "Stripe", "checkout", "HIPAA", "compliance", "SLA", "enterprise", "high volume", "can't fail" | Tier 3 | Full hardening + discuss monitoring/ops |
| Ambiguous or no clear signals | Tier 1 | Start simple, monitor for escalation triggers |

**In autopilot mode, don't announce the tier.** Just build appropriately and intervene if a tier change is needed.

---

## Tier Change Recommendations (Up or Down)

**Whether the user picked a tier or is in autopilot**, monitor the conversation and **recommend tier changes in either direction** when the task and outcome warrant it.

### Recommend Moving UP a Tier

#### Tier 1 → Tier 2 triggers:

**Troubleshooting is going in circles:**
- 3+ back-and-forth messages on the same issue
- User repeats "it's still not working" or "same problem"
- You're guessing at what the data looks like

→ **Recommend:** "We're spending a lot of time guessing. I'd recommend adding logging so we can see exactly what data is coming in and where it's failing. This is a Tier 2 pattern — want me to add it?"

**Silent or unclear failures:**
- User says "it just doesn't work" or "nothing happens"
- User says "sometimes it works, sometimes it doesn't"
- No error messages to work with

→ **Recommend:** "The workflow is failing silently, which makes this hard to diagnose. I'd suggest adding entry-point validation and external logging — that way we'll see exactly what's coming in and where it breaks. Want me to upgrade this to Tier 2 patterns?"

**User mentions deployment or sharing:**
- "ready to deploy", "going live", "share with the team"
- "my client", "users will", "in production"
- Moving from test to real environment

→ **Recommend:** "Since this is going to production, I'd recommend hardening it first — input validation, proper error responses, and logging. It's the difference between 'works on my machine' and 'survives in the wild.' Should I add Tier 2 patterns?"

**The "null vs empty string" pattern:**
- Data that "should" be there is missing
- Workflow processes but outputs garbage
- Inconsistent behavior with same inputs

→ **Recommend:** "This looks like a data shape issue — probably null values or missing fields slipping through. Tier 2 validation would catch this at the entry point. Want me to add it?"

#### Tier 2 → Tier 3 triggers:

**Scale or volume concerns:**
- User mentions request counts (1000+/day)
- User asks about performance or speed
- User asks "what if I get a lot of traffic?"

→ **Recommend:** "At that volume, you'll want Tier 3 patterns — rate limiting, idempotency handling for duplicate requests, and queue-based processing for traffic spikes. Want me to walk through what that looks like?"

**Reliability concerns:**
- User asks "what if [service] goes down?"
- User asks about retries or fallbacks
- User mentions uptime requirements or SLAs

→ **Recommend:** "For that level of reliability, I'd recommend Tier 3 — monitoring so you know when something's wrong before users tell you, intelligent retries, and a rollback plan. Should we upgrade?"

**Financial or compliance context:**
- Payment processing, billing, invoicing
- Healthcare, legal, financial data
- User mentions audits or compliance requirements

→ **Recommend:** "Since this handles [payments/sensitive data], I'd strongly recommend Tier 3 patterns — idempotency keys so duplicate requests don't double-charge, audit logging for compliance, and error handling that doesn't expose sensitive data. This is important — want me to add it?"

---

### Recommend Moving DOWN a Tier

#### Tier 3 → Tier 2 triggers:

**Over-engineered for actual use case:**
- User's volume is actually low (< 1000/day)
- No real compliance requirements after clarification
- User is spending too much time on ops concerns for a simple workflow

→ **Recommend:** "Looking at this more, I think we might be over-engineering. If you're not dealing with high volume or strict compliance requirements, we could drop to Tier 2 — still production-ready, but without the monitoring and idempotency overhead. Would that be simpler for your needs?"

**User wants to ship faster:**
- User expresses frustration with complexity
- User says "this is taking too long"
- Iteration speed is suffering

→ **Recommend:** "We've been building this with full Tier 3 hardening, but it's slowing us down. Want to drop to Tier 2 for now and add the monitoring/idempotency later once the core logic is stable?"

#### Tier 2 → Tier 1 triggers:

**It's actually just a prototype:**
- User reveals "this is just a test" or "I'm experimenting"
- User says "I just want to see if it works"
- The workflow is for personal/internal use only

→ **Recommend:** "If this is just for testing the concept, we don't need all this validation and logging yet. Want me to simplify to Tier 1? We can always add the production hardening later once you're happy with the logic."

**Complexity is blocking progress:**
- User is stuck on logging/validation setup, not core logic
- The hardening is more work than the actual workflow
- User seems overwhelmed

→ **Recommend:** "I think we're getting bogged down in the production hardening before the core workflow is even working. Let's drop to Tier 1, get the basic flow working, and then add validation and logging once we know the logic is right. Sound good?"

**Scope changed:**
- User initially said "client" but now it's "just for me"
- Requirements relaxed during conversation
- Stakes are lower than initially understood

→ **Recommend:** "Since this is actually just for internal use, we don't need the full Tier 2 treatment. Want me to strip out the external logging and simplify the error handling? It'll be easier to maintain."

---

### When NOT to Recommend a Change

**Don't recommend moving up if:**
- User explicitly chose a lower tier and the workflow is working fine
- The issue is a simple bug, not a systemic pattern
- User is in early exploration/prototyping phase

**Don't recommend moving down if:**
- User explicitly chose a higher tier for good reasons
- The workflow handles sensitive data or money
- User has mentioned compliance or SLA requirements

**Trust user judgment, but flag concerns:**
> "I know you want to keep this at Tier 1, and that's fine for now — just know that once this goes to production, you'll probably want to add logging at minimum. I can help with that when you're ready."

---

## How to Recommend Changes

When suggesting tier changes, **be direct but not pushy:**

1. **State what you're observing** — the pattern that triggered the recommendation
2. **Explain the benefit** — why this tier's patterns would help
3. **Ask, don't mandate** — "Want me to add it?" / "Should we upgrade?"
4. **Respect the answer** — if they say no, continue at current tier

**If the user explicitly chose a tier and you're recommending a change:**
> "I know you said Tier 1, but we've been debugging this for a while and I think Tier 2 logging would save us time here. Up to you — want me to add it, or keep it simple?"

**If in autopilot mode:**
> "I'm going to add some validation and logging here — we're hitting the kind of silent failures that these patterns are designed to catch. This'll take a few extra minutes but should make debugging much faster."

---

## Lifecycle-Aware Behavior

Adjust your approach based on where the user is in the workflow lifecycle:

| Lifecycle Stage | How to Detect | Your Approach |
|-----------------|---------------|---------------|
| **Exploring/Prototyping** | "trying to figure out", "is this possible?", "how would I..." | Tier 1. Fast, minimal. Get it working first. |
| **Building** | "build me", "create", "I need a workflow that..." | Ask tier or infer from context. |
| **Testing** | "let me test", "trying it out", "it works but..." | Stay at current tier. Focus on the specific issue. |
| **Debugging** | "not working", "error", "broken", "help" | Monitor for escalation triggers. Recommend logging if stuck. |
| **Pre-deployment** | "ready to deploy", "going live", "production" | Recommend Tier 2 minimum if not already there. |
| **Post-deployment issues** | "was working, now broken", "users are reporting", "in production" | Tier 2+. Recommend logging immediately to diagnose. |
| **Scaling** | "more users", "growing", "volume increasing" | Discuss Tier 3 patterns as relevant. |

---

## Tier Definitions (Reference)

### Tier 1: Internal / Prototype

**Context signals:** "quick", "simple", "just for me", "internal", "prototype", "test", "playing around"

**What to include:**
- Basic null checks (`|| {}`, `|| ''`)
- Simple try-catch around risky operations
- n8n's built-in error handling (Error Trigger → Slack notification)

**What to skip:**
- External logging database
- Comprehensive input validation
- Full status code handling
- Extensive breaking tests

**Example workflows:** "New GitHub issue → Slack notification", "Daily weather → personal email", "RSS feed → Discord"

**Build time impact:** ~10% extra beyond core logic

---

### Tier 2: Production / Client-Facing

**Context signals:** "client", "customer", "production", "deploy", "users will...", "business", "launch", "going live"

**Escalation triggers:** Debugging going in circles, silent failures, user mentions deployment, "works sometimes" issues

**What to include:**
- Full entry-point validation (user exists? auth valid? data shaped right?)
- Explicit null vs empty string handling
- External logging to Supabase/Postgres
- Proper HTTP status codes (400, 401, 403, 404, 500)
- Error notifications to team (Slack/email)
- Pre-deployment breaking tests
- Test database before production

**What to skip:**
- Real-time monitoring dashboards
- Automated rollback
- Rate limiting / idempotency (unless high volume)

**Example workflows:** "Customer form → CRM + email sequence", "Payment webhook → order fulfillment", "AI chatbot for client website"

**Build time impact:** ~80% extra beyond core logic (the 80/20 rule)

---

### Tier 3: Mission-Critical / High-Volume

**Context signals:** "payment", "Stripe", "checkout", "HIPAA", "compliance", "SLA", "enterprise", "high volume", "can't fail", "audit"

**Escalation triggers:** Volume/performance questions, "what if X goes down?", financial transactions, compliance mentions

**What to include:**
- Everything from Tier 2, plus:
- Real-time monitoring dashboard (Grafana, Datadog)
- Automated alerting with escalation (PagerDuty)
- Idempotency keys for duplicate request handling
- Rate limiting to prevent cascade failures
- Request queuing for traffic spikes
- Rollback strategy (workflow versioning, feature flags)
- Audit logging for compliance
- Regular chaos testing (simulate failures)
- Documented runbooks for incident response

**Example workflows:** "Stripe payment → inventory + fulfillment + accounting", "HIPAA-compliant patient data sync", "High-traffic API gateway"

**Build time impact:** 2-3x the core logic development time

---

### Tier Escalation Triggers Summary

**You've outgrown Tier 1 when:**
- You're debugging the same workflow for the third time
- You find yourself saying "it works sometimes"
- You can't tell what data the workflow actually received
- Someone other than you will use or depend on it
- A failure would cause more than minor annoyance

**You've outgrown Tier 2 when:**
- You're processing 10,000+ requests/day
- You're handling payments or sensitive PII
- You have contractual SLAs
- A 1-hour outage would cause significant revenue loss or legal exposure
- You're asking "what happens if [external service] goes down?"

**Downgrade is okay too:**
- Built Tier 2 for a prototype, realized it's overkill? Strip it back.
- The goal is right-sized investment, not maximum hardening.

---

## The 80/20 Rule by Tier

| Component | Tier 1 | Tier 2 | Tier 3 |
|-----------|--------|--------|--------|
| **Core logic** | 70% | 20% | 10% |
| **Validation** | 10% | 20% | 15% |
| **Error handling** | 10% | 20% | 20% |
| **Logging** | 5% | 20% | 20% |
| **Testing** | 5% | 20% | 15% |
| **Monitoring/Ops** | — | — | 20% |

**The workflow logic is the easy part. The hard part is everything else — but only invest in "everything else" proportional to your risk.**

---

## Pre-Deployment Checklists

### Tier 1 Checklist
- [ ] Basic null/undefined checks on critical fields
- [ ] Try-catch around external API calls
- [ ] Error Trigger workflow sends Slack/email on failure
- [ ] Tested manually with happy path

### Tier 2 Checklist
- [ ] **Validation**: Every input field is validated
- [ ] **Null handling**: Explicitly handle `null` vs empty string vs undefined
- [ ] **Type checking**: Verify data types match expectations
- [ ] **Logging**: External logging configured at entry, decisions, output, errors
- [ ] **Error responses**: Proper HTTP status codes for all failure modes
- [ ] **Error notifications**: Team gets alerted on failures (Slack, email)
- [ ] **Empty data test**: Workflow handles empty inputs gracefully
- [ ] **Wrong type test**: Workflow rejects malformed data
- [ ] **Auth test**: Missing/invalid auth returns 401/403
- [ ] **Downstream failure test**: External service failures handled
- [ ] **Test database**: All tests run against test environment first
- [ ] **Documentation**: Workflow purpose and data flow documented

### Tier 3 Checklist
- [ ] Everything from Tier 2, plus:
- [ ] **Monitoring**: Real-time dashboard configured
- [ ] **Alerting**: PagerDuty/escalation set up
- [ ] **Idempotency**: Duplicate requests handled safely
- [ ] **Rate limiting**: Traffic spikes won't cascade
- [ ] **Rollback plan**: Can revert to previous version quickly
- [ ] **Runbook**: Incident response documented
- [ ] **Load test**: Tested at 2-3x expected volume
- [ ] **Chaos test**: Simulated downstream failures

---

## Summary: Adaptive Tier Management

1. **Ask once after initial prompt** — let user pick tier or choose autopilot
2. **Respect explicit tier choices** — if they ask for a tier, build to it
3. **Support tier lookups** — explain tiers when asked
4. **Infer silently in autopilot** — don't mention tiers unless recommending a change
5. **Monitor for tier change triggers** — both UP (more hardening needed) and DOWN (over-engineered)
6. **Recommend, don't mandate** — ask permission, respect the answer
7. **Trust user judgment** — but flag serious concerns even if they decline

**The goal:** Users who know tiers get control. Users who don't get invisible guidance. The AI adapts to the user, the task, and the project — recommending more hardening when complexity demands it, and simplification when it's getting in the way.

---

## Related Skills

For implementation patterns, see:
- **[../n8n-workflow-patterns/webhook_processing.md](../n8n-workflow-patterns/)** — Validation, logging, status codes
- **[../n8n-code-javascript/COMMON_PATTERNS.md](../n8n-code-javascript/)** — Validation and logging code templates
- **[../n8n-code-javascript/ERROR_PATTERNS.md](../n8n-code-javascript/)** — Null handling, silent failure prevention

---

*"Learn this stuff before your first emergency call. I've broken enough things to have most of the answers now."*
