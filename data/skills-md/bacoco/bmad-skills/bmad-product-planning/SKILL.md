---
name: bmad-product-planning
description: Creates PRDs and plans features.
allowed-tools: ["Read", "Write", "Grep"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "create a PRD"
      - "I want to build"
      - "plan this feature"
      - "write requirements"
      - "product document"
    keywords:
      - PRD
      - requirements
      - plan
      - build
      - feature
      - epic
      - roadmap
      - product
  capabilities:
    - prd-creation
    - requirements-gathering
    - feature-planning
    - roadmap-design
  prerequisites:
    - discovery-brief
  outputs:
    - product-requirements-document
    - feature-specs
    - epic-breakdown
---

# Product Requirements Skill

## When to Invoke

**Automatically activate this skill when the user:**
- Says "I want to build...", "Let's build...", "Create a..."
- Asks "Create a PRD", "Write requirements", "Plan this feature"
- Mentions "product requirements", "PRD", "epic roadmap"
- Has completed discovery phase and needs formal requirements
- Is starting a Level 2-4 project requiring structured planning
- Uses words like: build, create, PRD, requirements, plan, feature, product

**Specific trigger phrases:**
- "I want to build [something]"
- "Create a PRD for [project]"
- "Plan this feature"
- "Write the requirements"
- "What should be in the PRD?"
- "Break this into epics"
- "Product requirements for [project]"

**Prerequisites check:**
- If Level 3-4 project: verify analysis phase complete (discovery brief exists)
- If missing analysis: recommend invoking bmad-discovery-research first
- If Level 0-1: suggest OpenSpec workflow instead

**Do NOT invoke when:**
- User is still exploring/brainstorming (use bmad-discovery-research first)
- User is ready for architecture (use bmad-architecture-design instead)
- User wants to code directly (check if prerequisites exist first)
- Project is Level 0-1 simple change (use OpenSpec)

## Mission
Transform validated discovery insights into a production-ready Product Requirements Document (PRD) and epic roadmap that align stakeholders and prepare downstream architecture, UX, and delivery work.

## Inputs Required
- business_goal: clear outcome statement tied to measurable success metrics
- stakeholders: decision makers plus their approvals or open concerns
- constraints: technical, regulatory, financial, or timeline guardrails
- discovery_artifacts: briefs, research memos, or notes from the discovery-analysis skill

If any input is missing or stale, pause and request the exact artifact before proceeding.

## Outputs
Produce two markdown artifacts aligned to the templates in `assets/`:
1. `PRD.md` populated from `assets/prd-template.md.template`
2. `epics.md` populated from `assets/epic-roadmap-template.md.template`

Deliverables must be written to the project documentation folder (default `docs/`) and summarized for the requestor.

## Process
1. Validate readiness using the gate in `CHECKLIST.md`.
2. Review discovery inputs and clarify remaining unknowns.
3. Map goals, scope, and constraints into structured PRD sections.
4. Prioritize epics, sequencing, and acceptance signals for delivery.
5. Run `scripts/generate_prd.py` when structured data exists; otherwise compose outputs manually following templates.
6. Apply the quality checklist before returning deliverables and recommended next steps.

## Quality Gates
Confirm every item in `CHECKLIST.md` is satisfied before delivering the PRD package. Stop and fix any unmet criteria.

## Error Handling
If prerequisites are missing or contradictions surface:
- Identify which required input is absent and why it blocks progress.
- Provide a minimal list of follow-up questions or stakeholders needed.
- Recommend re-engaging the discovery-analysis skill or orchestrator when scope is unclear.
