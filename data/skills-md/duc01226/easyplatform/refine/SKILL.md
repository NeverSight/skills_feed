---
name: refine
version: 2.1.0
description: Transform ideas into Product Backlog Items using BA best practices, hypothesis validation, and domain research. Use when converting ideas to PBIs, validating problem hypotheses, adding acceptance criteria, or refining requirements. Triggers on "create pbi", "refine idea", "convert to pbi", "acceptance criteria", "make actionable", "validate hypothesis".
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite, WebSearch, AskUserQuestion
infer: true
---

# Idea Refinement to PBI

Transform captured ideas into actionable Product Backlog Items using BA best practices, Hypothesis-Driven Development, and domain research.

## ⚠️ MUST READ References

**IMPORTANT: You MUST read these reference files for complete protocol. Do NOT skip.**

- **⚠️ MUST READ** `.claude/skills/shared/team-frameworks.md` — RICE, MoSCoW, INVEST, SPIDR frameworks
- **⚠️ MUST READ** `.claude/skills/shared/bdd-gherkin-templates.md` — BDD/Gherkin scenario templates
- **⚠️ MUST READ** `.claude/skills/shared/module-detection-keywords.md` — module detection keywords
- **⚠️ MUST READ** `references/refinement-workflow.md` — detailed phases 2-8
- **⚠️ MUST READ** `references/bravosuite-workflow.md` — domain context integration

## When to Use

- Idea artifact ready for refinement
- Need to validate problem hypothesis before building
- Converting concept to implementable item
- Adding acceptance criteria to requirements

## Workflow

| Phase | Name                | Key Activity                 | Output                 |
| ----- | ------------------- | ---------------------------- | ---------------------- |
| 1     | Idea Intake         | Load artifact, detect module | Context loaded         |
| 2     | Domain Research     | WebSearch market/competitors | Research summary       |
| 3     | Problem Hypothesis  | Validate problem exists      | Confirmed hypothesis   |
| 4     | Elicitation         | Apply BABOK techniques       | Requirements extracted |
| 5     | Acceptance Criteria | Write BDD scenarios (min 3)  | GIVEN/WHEN/THEN        |
| 6     | Prioritization      | Apply RICE/MoSCoW            | Priority assigned      |
| 7     | Validation          | Interview user (MANDATORY)   | Assumptions confirmed  |
| 8     | PBI Generation      | Create artifact              | PBI file saved         |

## Phase 1: Idea Intake & Context Loading

1. Read idea artifact from path or find by ID in `team-artifacts/ideas/`
2. Extract: problem statement, value proposition, target users, scope
3. Check `module` field in frontmatter

**If module present:** Load domain context (see `references/bravosuite-workflow.md`)
**If module absent:** Run `Glob("docs/business-features/*/README.md")`, analyze keywords, prompt if ambiguous
**Skip:** Infrastructure ideas, cross-cutting concerns

## Phase 5: Acceptance Criteria (BDD Format)

**⚠️ MUST READ** `.claude/skills/shared/bdd-gherkin-templates.md` for templates.

| Practice                  | Description                       |
| ------------------------- | --------------------------------- |
| Single trigger            | "When" clause has ONE action      |
| 3 scenarios minimum       | Happy path, edge case, error case |
| No implementation details | Focus on behavior, not how        |
| Testable outcomes         | "Then" must be verifiable         |
| Stakeholder language      | No technical jargon               |

## Output

- **Path:** `team-artifacts/pbis/{YYMMDD}-pbi-{slug}.md`
- **ID Pattern:** `PBI-{YYMMDD}-{NNN}`

## Related

| Type               | Reference                              |
| ------------------ | -------------------------------------- |
| **Role Skill**     | `business-analyst`                     |
| **Input**          | `/idea` output                         |
| **Next Step**      | `/story`, `/test-spec`, `/design-spec` |
| **Prioritization** | `/prioritize`                          |

## Triggers

Activates on: refine, refinement, pbi, backlog item, acceptance criteria, hypothesis, validate idea


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
