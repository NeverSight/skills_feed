---
name: tpm-spec-verify
description: Enrich a Phase Sepc/PRD with Quality Requirements (Q-nnn) and Acceptance Criteria (AC-nnnn). Use when user wants to add QA perspective, define test criteria, identify non-functional requirements, add verification steps, or prepare a Phase PRD for test planning.
---

# PRD QA Enricher

Add Quality Requirements and Acceptance Criteria to a Phase PRD, preparing it for test planning.

## Inputs Required

- **Phase PRD** — With R-nnnn requirements (use `prd-phase-generator` first if missing)

## Workflow

1. **Audit for Quality Requirements** — Identify missing non-functional concerns
2. **Add Q-nnn entries** — Security, performance, accessibility, etc.
3. **Write Acceptance Criteria** — Happy path, edge cases, error conditions for each R-nnnn
4. **Update traceability** — Link ACs to requirements

## Step 1: Quality Requirements Audit

Review the Phase PRD and ask: what cross-cutting concerns are missing?

### Quality Categories Checklist

| Tag | Category | Questions to Ask |
|-----|----------|------------------|
| `[PERF]` | Performance | Response times? Throughput? Caching? |
| `[SEC]` | Security | Auth? Input validation? Data protection? |
| `[AVAIL]` | Availability | Uptime requirements? Failover? Recovery? |
| `[SCALE]` | Scalability | Concurrent users? Data volume limits? |
| `[ACCESS]` | Accessibility | WCAG level? Keyboard nav? Screen readers? |
| `[COMPAT]` | Compatibility | Browsers? Devices? Integrations? |
| `[I18N]` | Internationalization | Languages? Locales? RTL support? |
| `[API]` | API Standards | Versioning? Rate limits? Error formats? |

### Writing Quality Requirements

```markdown
Q-007 [COMPAT]: The system shall support Chrome, Firefox, Safari, and Edge (latest 2 versions)

**Applies to:** F-001, F-002, F-003
**Priority:** Must
```

Each Q-nnn should:
- Have a category tag in brackets
- List which features it applies to
- Be testable and specific

## Step 2: Acceptance Criteria

For each R-nnnn, write AC-nnnn entries covering:

### Coverage Categories

1. **Happy path** — Normal successful flow
2. **Edge cases** — Boundary conditions, limits, empty states
3. **Error handling** — Invalid input, failures, recovery
4. **State transitions** — Before/after, concurrent access

### AC Format

```markdown
**Acceptance Criteria:**
- AC-R0142-01: Form accepts valid email formats (user@domain.tld)
- AC-R0142-02: Form rejects invalid emails with inline error message
- AC-R0142-03: Form requires non-empty name field
- AC-R0142-04: Form preserves input on validation failure
- AC-R0142-05: Submit button disabled until required fields populated
```

### AC Writing Guidelines

| Do | Don't |
|----|-------|
| Specific, testable conditions | Vague ("works correctly") |
| One behavior per AC | Multiple behaviors combined |
| Observable outcomes | Implementation details |
| Include error states | Only happy path |

### Typical AC Count

- Simple requirement: 2-3 ACs
- Standard requirement: 3-5 ACs
- Complex requirement: 5-8 ACs

If a requirement needs >10 ACs, recommend splitting the requirement.

## Step 3: Update Traceability

After adding ACs, update the Traceability Matrix:

| Requirement | Feature | Priority | Status | AC Count |
|-------------|---------|----------|--------|----------|
| R-0142 | F-014 | Must | Draft | 5 |

## Quality Requirements Numbering

Q-nnn is sequential across the entire product (like R-nnnn). Check previous Phase PRDs for last used Q-nnn.

## Reference

See `references/naming-conventions.md` for ID format details and category tags.
