---
name: requirements-traceability
description: |
  Create or audit requirements-to-design-to-code-to-test traceability. Builds a
  traceability matrix (REQ → design/ADR → implementation files → tests →
  evidence) and flags gaps (unimplemented requirements, untested changes,
  undocumented decisions). Use when you need a requirements traceability check
  for a PR/release, regulated/compliance work, or when requirements are drifting
  from implementation.
license: Apache-2.0
---

# Requirements Traceability

## Overview

You are a traceability engineer. Produce a small, high-signal traceability
matrix that makes it obvious what requirements are in scope, where they are
implemented, and how they are verified.

## Inputs (Ask If Missing)

- Requirement sources (in priority order):
  - Spec documents, ADRs, tickets, PR description
  - `docs/requirements*.md` (if present)
- Design artifacts (if present): ADRs, architecture docs, diagrams
- Implementation scope: changed files, modules, or commit range
- Test suite entrypoints and how to run them

## Requirement ID Convention

Prefer stable IDs like `REQ-001` / `NFR-001`. If no IDs exist, propose a minimal
convention and apply it consistently in the matrix (do not rename existing IDs
without approval).

## Workflow

### 1) Enumerate Requirements (No Guessing)

- Extract explicit requirements verbatim where possible.
- If requirements are implicit, list them as `INFERRED-…` and request
  confirmation.
- Keep scope tight: only requirements impacted by the change/PR.

### 2) Map Requirements → Design

For each requirement, link the nearest design artifact:
- ADR (`docs/adr/ADR-…`)
- Module design doc
- API spec / schema

If there is no design artifact, record `Design: MISSING` and propose the
smallest useful artifact to add (often a short ADR or README section).

### 3) Map Requirements → Implementation

Link:
- File(s) and key types/functions
- Configuration/feature flags
- Migrations or infra changes (if relevant)

### 4) Map Requirements → Verification Evidence

Each in-scope requirement must have at least one verification path:
- Unit/integration tests (`testing`)
- Acceptance tests (`acceptance-testing`)
- Visual regression tests (`visual-testing`) for UI requirements
- Security evidence (`security-audit`) for security requirements
- Performance evidence (`rust-performance`) for latency/throughput/memory budgets
- Manual verification steps (last resort; include owner + date)

Evidence must be specific (paths, commands, logs). “Looks good” is not evidence.

### 5) Produce Outputs

- Traceability matrix
- Gap list (blockers vs follow-ups)
- Recommendations for closing gaps (smallest changes first)

## Traceability Matrix Template

```markdown
| Req ID | Requirement | Design Ref | Impl Ref | Tests | Evidence | Status |
|-------:|-------------|------------|----------|-------|----------|--------|
| REQ-001 | … | ADR-001 | `src/...` | `tests/...` | `docs/quality/...` / command output | ✅/⚠️/❌ |
```

## Gap Severity Rules

- ❌ **Blocker**: requirement in scope has no implementation link OR no verification path.
- ⚠️ **Follow-up**: implementation exists but evidence is incomplete (e.g., only manual steps for critical regressions).
- ℹ️ **Note**: documentation/formatting improvements not affecting traceability.

## Output Format

```markdown
# Traceability Report: {change}

## Requirements Enumerated
- REQ-…

## Traceability Matrix
{table}

## Gaps
- ❌ {Req} missing {design/tests/evidence}
- ⚠️ {Req} has {partial evidence}
```

## ZDP Integration (Optional)

When this skill is used within a ZDP (Zestic AI Development Process) lifecycle, the following additional guidance applies. **This section can be ignored for standalone usage.**

### ZDP Traceability Chain

ZDP defines a full artefact chain. When tracing requirements in a ZDP context, extend the matrix to cover:

```
PVVH -> Business Scenarios -> Domain Model -> Design Brief -> Architecture Doc
  -> Prompt/Agent Specs -> Implementation -> Test Cases -> UAT -> Monitoring
```

### Extended Matrix Template

Add ZDP artefact IDs alongside standard REQ IDs:

| Req ID | ZDP Artefact | Requirement | Design Ref | Impl Ref | Tests | Evidence | Status |
|-------:|-------------|-------------|------------|----------|-------|----------|--------|
| REQ-001 | BS-003 | ... | ADR-001 | `src/...` | `tests/...` | ... | ... |

### Cross-References

If available, coordinate with:
- `/business-scenario-design` -- business scenario IDs for traceability
- `/product-vision` -- PVVH as the root of the traceability chain
- `/responsible-ai` -- Responsible-AI requirements traceability

## Constraints

- Don't claim coverage you can't point to (paths/tests/commands/logs).
- Prefer adding/expanding tests over adding manual steps for regressions.
- Keep the matrix small and in-scope; link out to details.
