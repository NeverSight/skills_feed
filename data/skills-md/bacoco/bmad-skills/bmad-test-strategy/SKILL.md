---
name: bmad-test-strategy
description: Creates test strategy and ATDD scenarios.
allowed-tools: ["Read", "Write", "Grep"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "how should we test"
      - "create test strategy"
      - "test plan"
      - "ATDD"
      - "quality assurance"
    keywords:
      - test
      - testing
      - strategy
      - QA
      - quality
      - ATDD
      - automation
  capabilities:
    - test-strategy
    - atdd-scenarios
    - quality-gates
    - test-planning
  prerequisites:
    - architecture-decisions
  outputs:
    - test-strategy-doc
    - atdd-scenarios
    - quality-checklist
---

# Quality Assurance Skill

## When to Invoke

**Automatically activate when user:**
- Says "How should we test?", "Create test strategy"
- Asks "Test plan?", "ATDD?", "Quality assurance?"
- Mentions "testing", "test strategy", "QA"
- Planning or architecture phase (for test strategy)
- Uses words like: test, testing, strategy, QA, quality, ATDD

**Specific trigger phrases:**
- "How should we test this?"
- "Create test strategy"
- "Test plan for [project]"
- "ATDD scenarios"
- "Quality assurance approach"
- "Testing framework"

**Can invoke:**
- During Phase 2 (Planning) for test strategy
- During Phase 4 (Implementation) for ATDD

**Do NOT invoke when:**
- No requirements yet (need PRD first)
- Simple testing questions (answer directly)
- Already have test strategy (reference existing)

## Mission
Provide risk-focused quality strategies, acceptance tests, and governance that ensure BMAD deliverables meet agreed standards before release.

## Inputs Required
- prd_and_epics: requirements and roadmap produced by product-requirements skill
- architecture: technical decisions and constraints
- stories: delivery-planning outputs for upcoming work
- existing_quality_assets: current test suites, tooling, and metrics

## Outputs
- **Test strategy** (from `assets/test-strategy-template.md.template`)
- **ATDD scenarios** (from `assets/atdd-scenarios-template.md.template`)
- **Quality checklist** (from `assets/quality-checklist-template.md.template`)
- Coverage matrices or CI/CD gate definitions stored with project docs
- Recommendations for instrumentation, monitoring, or regression prevention

**Template locations:** `.claude/skills/bmad-test-strategy/assets/*.template`

## Process
1. Confirm prerequisites using `CHECKLIST.md`.
2. Review requirements, architecture, and delivery plans to identify risk areas.
3. Define quality approach (test types, automation, environments, data) proportionate to risk.
4. Author executable artifacts (ATDD scenarios, scripts, dashboards) or instructions.
5. Partner with development-execution and orchestrator to integrate quality gates and track follow-ups.

**Note on automation:** This skill currently operates through quality planning conversation using templates. No automation scripts are required—test strategies and ATDD scenarios are created manually using templates from `assets/`. See `scripts/README.md` for future automation roadmap.

## Quality Gates
Ensure all checklist items are satisfied before sign-off. Traceability from requirements to test coverage must be explicit.

## Error Handling
- When prerequisites are missing, halt work and request specific artifacts.
- If tools or environments are unavailable, document gaps and remediation plan.
- Escalate high-risk issues (compliance, data privacy) immediately with evidence.
