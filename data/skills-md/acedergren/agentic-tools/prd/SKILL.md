---
name: prd
description: "Create, validate, and evolve Product Requirements Documents with interactive discovery, technical architecture, phasing, TDD protocol, and dependency analysis. Use when: writing a PRD, planning a feature, defining requirements, or updating an existing PRD. Supports /prd (create), /prd --update (incremental update), /prd --validate (run checklist), /prd --audit-deps (dependency analysis only), /prd --to-plan (generate orchestrate-ready task plan)."
---

# PRD Skill

Produce comprehensive, drift-proof Product Requirements Documents through iterative discovery.

Output: `.claude/reference/PRD.md` (the living requirements document for the project).

## Mode Routing

Parse `$ARGUMENTS` to determine the mode:

| Argument         | Mode     | Description                              |
| ---------------- | -------- | ---------------------------------------- |
| _(empty)_        | Create   | Interactive PRD creation from scratch    |
| `<feature text>` | Create   | Start with context, then iterate         |
| `--update`       | Update   | Incremental update to existing PRD       |
| `--validate`     | Validate | Run validation checklist on existing PRD |
| `--audit-deps`   | Audit    | Run dependency/drift analysis only       |
| `--to-plan`      | Plan     | Generate orchestrate-ready task plan     |

---

## Plan Mode (`--to-plan`)

Transform the PRD's phasing section into a task plan that `/orchestrate` can execute directly.

### Input

Read `.claude/reference/PRD.md`. If it doesn't exist, report error and stop. Validate V5 (DAG) passes first.

### Transformation Rules

For each **Phase** in the PRD:

1. **Extract requirements** mapped to this phase (M1, S1, etc.)
2. **Generate tasks** from each requirement's acceptance criteria
3. **Assign waves** within each phase:
   - Wave 1: Foundation tasks (schemas, types, migrations, config)
   - Wave 2: Implementation tasks (routes, services, repositories)
   - Wave 3: Integration tasks (wiring, UI, end-to-end flows)
   - Wave 4: Polish tasks (error handling, edge cases, docs)
4. **Assign agent types**:
   - `haiku`: Type definitions, config changes, simple CRUD, test writing
   - `sonnet`: Business logic, complex integrations, security-sensitive code
5. **Set dependencies** from the PRD's phase prerequisites
6. **Generate verification commands** from the PRD's test file mapping

### Output Format

Write to `docs/plans/<feature-name>-plan.md`:

```markdown
# Task Plan: [Feature Name]

Generated from PRD: `.claude/reference/PRD.md`
Generated at: [ISO timestamp]

## Phase 1: [Title]

### Wave 1: Foundation

| ID     | Task                      | Agent | Files              | Depends | Verify           |
| ------ | ------------------------- | ----- | ------------------ | ------- | ---------------- |
| 1-1.01 | Create Zod schemas for M1 | haiku | packages/types/... | —       | npx tsc --noEmit |

### Wave 2: Implementation

| ID     | Task                        | Agent  | Files             | Depends | Verify                |
| ------ | --------------------------- | ------ | ----------------- | ------- | --------------------- |
| 1-2.01 | Implement repository for M1 | sonnet | src/repositories/ | 1-1.01  | npx vitest run <test> |
```

---

## Create Mode

### Phase 1: Codebase Scan (automatic)

Before asking questions, build context:

1. Launch an **Explore agent** to map relevant codebase areas
2. Read roadmap/changelog for prior decisions
3. Check for outdated dependencies in scope

### Phase 2: Interactive Discovery (2-4 rounds)

**Round 1 — Problem & Vision**: What problem, who, success criteria, personas
**Round 2 — Scope & Boundaries**: MoSCoW priorities, out-of-scope, interactions
**Round 3 — Technical Constraints**: Architecture, database, auth, performance
**Round 4 — Phasing & Risk** (if needed): Phases, parallelization, risks

**Rules**: Never >4 questions. Never ask what the scan answered. Never draft before Round 2.

### Phase 3: Draft Generation

1. Read `template.md` from this skill directory
2. Write PRD to `.claude/reference/PRD.md`
3. Mark gaps with `[NEEDS CLARIFICATION: ...]`
4. Populate Architecture Decisions with AD-N entries
5. Build phasing DAG with explicit dependency arrows

### Phase 4: Multi-Angle Validation

Read `validation.md` and run every check. Present pass/fail results. Iterate until critical gates pass.

### Phase 5: Finalize

Remove markers, print summary, commit with `docs(prd): add <feature-name> requirements`.

---

## Update Mode (`--update`)

1. Read existing PRD
2. Ask what changed (new requirement, scope change, dependency update, etc.)
3. Launch Explore agent to detect codebase drift
4. Generate diff-style updates with `[ADDED]`, `[CHANGED]`, `[REMOVED]`, `[DRIFT DETECTED]` markers
5. Present changes for approval, apply, re-validate

---

## Validate Mode (`--validate`)

Read `validation.md` and run all gates. Print pass/fail with line references.

---

## Audit-Deps Mode (`--audit-deps`)

Read `drift-prevention.md` and run dependency freshness + architectural drift checks.

---

## Anti-Patterns (NEVER)

- NEVER generate a PRD without scanning the codebase first
- NEVER write acceptance criteria as "should work correctly" — use Given/When/Then
- NEVER skip dependency analysis
- NEVER batch all questions into one wall of text
- NEVER assume a library version — check `package.json` and npm
- NEVER write phasing without dependency arrows (phases must be a DAG)
- NEVER leave `[NEEDS CLARIFICATION]` markers in a finalized PRD

## Arguments

- `/prd` — interactive creation
- `/prd Workflow Designer` — start with context
- `/prd --update` — incremental update
- `/prd --validate` — run validation only
- `/prd --audit-deps` — dependency audit only
- `/prd --to-plan` — generate orchestrate-ready task plan
