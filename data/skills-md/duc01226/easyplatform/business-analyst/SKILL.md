---
name: business-analyst
description: Assist Business Analysts with requirements refinement, user story writing, acceptance criteria in BDD format, and gap analysis. Use when creating user stories, writing acceptance criteria, analyzing requirements, or mapping business processes. Triggers on keywords like "requirements", "user story", "acceptance criteria", "BDD", "GIVEN WHEN THEN", "gap analysis", "process flow", "business rules".
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite
---

# Business Analyst

Role: requirements refinement, user stories, acceptance criteria, business process analysis, gap analysis.

## When to Activate

- User asks BA-related questions (requirements, stories, acceptance criteria)
- Requirements need refinement or gap analysis
- User stories or BDD scenarios need creation
- Business rules need documentation

## Workflow

1. Understand business context -- load relevant module docs from `docs/business-features/`
2. Route to the appropriate task skill below
3. Validate output against quality checklist

## Task Routing

| Task                | Skill      | Command       |
| ------------------- | ---------- | ------------- |
| Capture idea        | idea       | `/idea`       |
| Refine idea to PBI  | refine     | `/refine`     |
| Create user stories | story      | `/story`      |
| Prioritize backlog  | prioritize | `/prioritize` |
| Generate test specs | test-spec  | `/test-spec`  |
| Generate test cases | test-cases | `/test-cases` |

## ⚠️ MUST READ Frameworks Reference

**⚠️ MUST READ** `.claude/skills/shared/team-frameworks.md` — RICE, INVEST, MoSCoW, SMART, 5 Whys frameworks.
**⚠️ MUST READ** `.claude/skills/shared/bdd-gherkin-templates.md` — BDD/Gherkin scenario templates.

## Business Documentation Paths

| Content           | Path                                                 |
| ----------------- | ---------------------------------------------------- |
| Feature Index     | `docs/business-features/{Module}/INDEX.md`           |
| Requirements      | `docs/business-features/{Module}/README.md`          |
| Test Specs        | `docs/test-specs/{Module}/README.md`                 |
| Detailed Features | `docs/business-features/{Module}/detailed-features/` |

## BA-Specific Guidelines

- Transform vague requests into specific, testable requirements -- never accept ambiguity
- Every user story must have at least 3 BDD scenarios: happy path, edge case, error case
- Cross-reference existing FR-XX and TC-XX IDs from module docs to prevent duplicate work
- Use `domain_path` from module frontmatter for entity inspection during gap analysis
- Requirements must be user-focused outcomes, not solution-speak

## Output Conventions

- User stories: `{YYMMDD}-ba-story-{slug}.md`
- Requirements: `{YYMMDD}-ba-requirements-{slug}.md`
- Requirement IDs: `FR-{MOD}-{NNN}`, `NFR-{MOD}-{NNN}`, `BR-{MOD}-{NNN}`
- Acceptance criteria IDs: `AC-{NNN}` per story/PBI

## Quality Checklist

- [ ] User story follows "As a... I want... So that..." format
- [ ] At least 3 scenarios: happy path, edge case, error case
- [ ] All scenarios use GIVEN/WHEN/THEN
- [ ] Out of scope explicitly listed
- [ ] Story meets INVEST criteria
- [ ] No solution-speak in requirements (only outcomes)

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
