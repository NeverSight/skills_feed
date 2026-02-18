---
name: technical-integrations
description: Hunt existing integration patterns and design vendor/framework-agnostic API, RFC, SDK, and integration plans for new external vendor integrations.
license: AGPL-3.0-only
metadata:
  source: "https://github.com/vincentkoc/dotskills"
---

# Technical Integrations

## Purpose

Design and review external-vendor integrations using existing internal patterns, with vendor/framework-agnostic workflows for API, RFC, SDK, and rollout planning.

## When to use

- Adding a new third-party/vendor integration.
- Evolving an existing integration surface without breaking compatibility.
- Writing or reviewing integration RFCs before implementation.
- Defining SDK/API integration points and delivery plans.

## Workflow

1. Classify mode: `discover`, `design`, `review`, or `implementation-plan`.
2. Run `references/hunt-and-inventory.md` to gather current integration evidence and patterns.
3. Use `references/principles.md` to enforce vendor/framework-agnostic constraints.
4. For architecture and proposal work, follow `references/design-and-rfc.md`.
5. For execution sequencing, follow `references/implementation-plan.md`.
6. For QA pass, apply `references/review-checklist.md`.
7. Return deliverables with explicit decisions, tradeoffs, and open risks.

## Inputs

- Integration objective and target vendor capability.
- Existing repo patterns (API, SDK, auth, observability, error model).
- Compatibility constraints (backward compatibility, versioning, rollout policy).
- Scope (discovery only, RFC draft, implementation plan, or full review).

## Outputs

- Integration inventory and pattern baseline.
- RFC-quality proposal with options and decision rationale.
- API and SDK integration design plan.
- Validation and rollout checklist with unresolved risks.
