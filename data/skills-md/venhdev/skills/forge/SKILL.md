---
name: forge
description: Use when implementing features, bugfixes, or tasks from approved changesets, tickets, or specifications.
---

# forge — Implementation & Verification Engine

Implement approved specifications, tickets, or changesets through test-driven verification, and deliver clean commits.

## Operating Invariants

- **Pre-Mutation Gate**: Verify target scope and acceptance criteria before mutating files. Forbid creating or editing files on ambiguous or unapproved requirements.
- **Scope Discipline**: Confine modifications strictly to target acceptance criteria, approved changeset, and direct mechanical cascades (imports, signatures, tests). Forbid adjacent refactoring.
- **Specialist Boundary**: Keep implementation focused strictly on the target task. Forbid unsolicited mid-stream execution of on-demand specialist skills (`simplify`, `ssot`, `to-tasks`, `diagnose`).
- **Verification Integrity**: Deliver commit handoff exclusively after 100% clean typecheck, lint, and test runs.
- **Circuit Breaker on Verification Failure**: Upon post-mutation verification failure, stop execution immediately, report stderr, and ask the user whether to revert or keep debugging. Forbid silent lossy reversions or unguided retry loops.

## Domain Engine & Standards

### 1. Construction Sequencing (Topological Ordering)
Execute filesystem modifications in strict dependency order:
1. `[CREATE]`: New types, interfaces, schemas, and foundational modules.
2. `[MOVE]`: Relocations and renames.
3. `[UPDATE]`: Implementation logic, callers, and cascade updates.
4. `[DELETE]`: Deprecated files and obsolete tests.

### 2. Test-Driven Verification Standards
- **Red Baseline**: For bugfixes, confirm or author a failing test verifying the issue before modifying code. For features, confirm test harness covers target acceptance criteria.
- **Green Implementation**: Apply minimal code necessary to pass the failing baseline.
- **Verification Cascade**: Run verification in order: typecheck → linter → targeted tests → affected subsystem tests.

### 3. Guardrails (When NOT to Touch)
- Forbid modifying files, functions, or configurations outside the approved blast radius.
- Forbid bundling cosmetic formatting churn or unsolicited helper abstractions.

## Execution Protocol

**SUB-SKILL:** changeset, clarify, ssot

### Phase 1: Readiness Audit & Scope Staging
1. Ingest input (ticket, spec, changeset, or user prompt).
2. Evaluate readiness before mutating workspace:
   - If requirements contain unresolved trade-offs: halt turn and request deliberation, recommending sub-skill `clarify`.
   - If multi-file scope lacks an atomic blast radius map: halt turn and map changes, recommending sub-skill `changeset`.
   - If acceptance criteria and scope are defined: stage target files and proceed (or halt for approval if scope was not pre-authorized).

### Phase 2: Construction & Test-Driven Verification
1. Execute file modifications in topological dependency order (`[CREATE]` → `[MOVE]` → `[UPDATE]` → `[DELETE]`).
2. Follow Test-Driven Verification Standards: establish Red baseline, apply minimal Green code, and execute Verification Cascade.
3. Apply the Circuit Breaker: If tests fail or consecutive identical tool errors occur, stop execution immediately, report stderr with file citations, and ask the user whether to revert or keep debugging.
4. Verify all ticket acceptance criteria are satisfied `[x]`.

### Phase 3: Delivery & Git Commit Handoff
1. Present a high-density Delta Summary of modified files and passing test proof. Forbid dumping raw diffs into chat by default.
2. Deliver the ready-to-run Conventional Commit command linking the issue:
   ```bash
   git add <approved_files>
   git commit -m "<type>(<scope>): <subject> (<issue-ref>)" -m "<body>"
   ```
3. Offer execution options: run the commit directly upon approval or provide for manual terminal execution.
