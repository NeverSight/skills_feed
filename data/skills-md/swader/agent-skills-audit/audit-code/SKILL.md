---
name: audit-code
description: Run a two-pass, multidisciplinary code audit led by a tie-breaker lead, combining security, performance, UX, DX, and edge-case analysis into one prioritized report with concrete fixes. Use when the user asks to audit code, perform a deep review, stress-test a codebase, or produce a risk-ranked remediation plan across backend, frontend, APIs, infra scripts, and product flows. Keep the audit stack-agnostic first, then add runtime-specific checks as an overlay.
---

# Audit Code

## Overview

Run an expert-panel audit with strict sequencing and one unified output document.
Produce findings first, sorted by severity, with file references, exploit/perf/flow impact, and actionable fixes.

Load `references/audit-framework.md` before starting the analysis.

## Required Inputs

Collect or infer the following:
- Audit scope: paths, modules, PR diff, or whole repository.
- Product context: PRD/spec/user stories, trust boundaries, and critical business flows.
- Runtime context: deployment model, queue/cron/background jobs, traffic profile, data sensitivity, and abuse assumptions.
- Constraints: timeline, acceptable risk, and preferred remediation style.

If product context is missing, state assumptions explicitly and continue.

## Team Roles

Use exactly these roles:
- Security expert
- Performance expert
- UX expert
- DX expert
- Edge case master
- Tie-breaker team lead

The tie-breaker lead resolves conflicts, prioritizes issues, and produces the final single report.

## Workflow

Follow this sequence every time:

1. Build Context
Read code + product flows. Identify assets, entry points, high-risk operations, privileged actions, external dependencies, and "failure hurts" journeys.

2. Build Invariant Coverage Matrix
Before specialist pass 1, map critical invariants to every mutating path (HTTP routes, webhooks, async jobs, scripts):
- Data-integrity invariants: linked records, transaction boundaries, and conflict handling must preserve consistency.
- Access lifecycle invariants: permission changes (disable/revoke/role change) must take effect across active credentials and privileged actions.
- Entitlement invariants: plan/tier/feature gates must be enforced on every trigger path (API/UI/webhook/job), and queued work must re-check entitlement at execution time.
- Input/protocol invariants: validation, canonicalization, parser behavior, and payload size/media-type policy must be consistent across equivalent paths.
- Sentinel semantics invariants: special values (for example `0`, empty, `NULL`) must have one canonical meaning across UI/API/webhook/worker paths.
- State-transition invariants: lifecycle transitions (active/archived/deleted/expired) must be explicit, legal, and consistently enforced.
- Cross-trigger policy invariants: business rules (for example downgrade timing, reset authority, pause/resume criteria) must remain consistent across user actions, provider callbacks, and background workers.
- Mutation outcome invariants: state-changing handlers must only signal success (UX/audit/events) after durable write success; persistence failures must be surfaced.
- Write-freshness invariants: callback/verification paths must avoid stale full-record rewrites; use conditional field-scoped updates for concurrent edit safety.
- Idempotency/order invariants: retries, duplicates, and out-of-order events must not corrupt state or duplicate side effects.
- Time-window invariants: timezone and boundary behavior (expiry, rollovers, DST) must be deterministic.
- Resource-boundedness invariants: loops, fan-out, queues, and in-memory maps must have caps/backpressure/cleanup.
- External dependency invariants: timeouts, partial failures, fallback behavior, stale-cache behavior, and explicit provider policy parameters must be intentional.
- Observability invariants: high-risk state changes and failures must emit actionable, traceable signals with required schema fields (actor/target and before/after context where applicable).
- Deployment/automation invariants: deployment docs and release scripts must align with CI artifact strategy, branch policy, and path-specific ingress controls.
Add domain-specific invariants discovered during context build; do not constrain to this list.
Treat missing parity across equivalent paths as a finding candidate.

3. Pass 1 Specialist Reviews
Run role-specific analysis in this order:
- Security
- Performance
- UX
- DX
- Edge case master
Capture findings using the schema in `references/audit-framework.md`.

4. Tie-Breaker Reconciliation
Resolve disagreements:
- Decide whether contested items are true issues.
- Set severity and confidence.
- Remove duplicates and merge overlapping findings.

5. Cross-Review Pass 2
After edge-case findings, rerun specialists:
- Security/Performance/UX/DX reassess prior findings and new edge-triggered scenarios.
- Edge case master performs a final pass on residual risk after proposed mitigations.

6. Final Report
Publish one document from the tie-breaker lead with:
- Findings first (ordered by severity, then blast radius, then exploitability).
- Open questions/assumptions.
- Remediation plan with priority, owner type, and verification tests.
- Short executive summary at the end.

## Quality Bar

Enforce these requirements:
- Use concrete evidence with file references and line numbers where available.
- Include reproduction steps for security/performance/edge findings when feasible.
- Prefer actionable fixes over abstract advice.
- Separate confirmed defects from speculative risks.
- Mark confidence for each finding.
- Run a cross-route consistency sweep: equivalent endpoints/jobs must enforce equivalent invariants.
- Run a required runtime-agnostic edge sweep using `references/audit-framework.md` (`Runtime-Agnostic Edge Sweep`).
- Verify deprecation path integrity: explicit failure semantics, replacement guidance, and docs/spec/skill parity.
- For fan-out integration endpoints, verify bounded concurrency and partial-failure behavior expectations.
- Verify state-switch UX integrity for whichever context selector exists in the product (for example workspace/account/tenant/environment): changing it should refresh active views and reset invalid local filters/groupings.
- Verify partial-update invariants against resulting state (`existing + patch`), not only provided fields.
- Verify derived-metric parity: UI formulas and summaries include all policy-required components (for example top-ups, adjustments, and resets), not just base plan values.
- Verify external billing/provider contract explicitness: behavioral requirements (for example proration/cancel timing/status sync) must be set in code/webhook handling, not left to provider defaults.
- Verify pagination/filter carryover safety: user-supplied query params survive page transitions without raw interpolation/encoding drift.
- Verify cross-trigger lifecycle parity: the same business rule is enforced across interactive routes, provider webhooks, and async workers.
- Verify sentinel-value parity: special configuration values (for example `0` limits) have consistent semantics across all interfaces and documentation.
- Verify mutation-outcome integrity: state-changing handlers do not swallow write errors and then emit success UX/audit outcomes.
- Verify deployment artifact policy parity: if CI publishes production artifacts, runbooks/scripts/services should deploy artifacts directly unless explicitly documented otherwise.
- Verify ingress isolation for signed callbacks/webhooks: deployment docs should define dedicated path controls (header gates/rate policy), not only generic catch-all routing.
- Verify simulation endpoint parity: test/sandbox endpoint payloads should match production contract shape plus explicit test marker fields.
- Verify release automation branch parity: branch checks, push targets, and docs use the same canonical branch name.
- Verify evidence boundaries: classify acceptance criteria as repo-verifiable vs environment-verifiable; report external infra items as unverified assumptions unless runtime evidence is provided.
- Verify security-hardening doc parity: when implementation is stricter/safer than spec, treat as doc/criteria drift to reconcile, not an implementation regression.
- Verify remediation traceability: findings-to-fixes status should remain mapped in a live checklist/spec so handoff can continue without hidden assumptions.
- For each High/Critical finding, include at least one focused regression test/check.

## Safety and Policy Guardrails

Apply these guardrails while auditing:
- Do not provide operational abuse instructions or exploit weaponization details.
- Evaluate manipulative UX patterns as legal/trust/reputation risk, not as recommended growth tactics.
- Prioritize user safety, system integrity, and maintainable engineering outcomes.

## Output Format

Follow this response structure:

1. Findings
List only validated issues. Use the finding schema in `references/audit-framework.md`.

2. Open Questions / Assumptions
State missing context that could change priority or validity.

3. Change Summary
Summarize high-impact remediation themes in a few lines.

4. Suggested Verification
List focused tests/checks to confirm each major fix.

## Runtime Heuristics

Always apply the runtime-agnostic checklist in `references/audit-framework.md` (`Runtime-Agnostic Edge Sweep`).
If a stack-specific module exists in that file and matches the target stack, apply it as an additive overlay, not a replacement.
If no module matches, infer and state the top stack-specific risk assumptions, then continue the audit.
