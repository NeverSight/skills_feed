---
name: bmad-architecture-design
description: Creates technical architecture and system design.
allowed-tools: ["Read", "Write", "Grep"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "how should we build"
      - "what's the architecture"
      - "tech stack"
      - "system design"
      - "how to build this"
    keywords:
      - architecture
      - design
      - system
      - build
      - technical
      - structure
      - stack
  capabilities:
    - architecture-design
    - tech-stack-selection
    - system-design
    - decision-documentation
  prerequisites:
    - product-requirements-document
  outputs:
    - architecture-decisions
    - system-design-doc
    - tech-stack-rationale
---

# Architecture Design Skill

## When to Invoke

**Automatically activate when user:**
- Says "How should we build this?", "What's the architecture?"
- Asks "Tech stack?", "System design?", "How to architect?"
- Mentions "architecture", "technical decisions", "stack"
- PRD and epics are approved (Phase 3)
- Uses words like: architecture, tech stack, design, system, build, technical

**Specific trigger phrases:**
- "How should we build this?"
- "What's the architecture?"
- "Choose tech stack"
- "System design for [project]"
- "Technical architecture"
- "How to architect [feature]"

**Prerequisites:**
- PRD exists and approved
- Epics defined

**Do NOT invoke when:**
- PRD not ready (use bmad-product-planning first)
- Already have architecture (skip to stories)
- Simple Level 0-1 project (may not need formal architecture)

## Mission
Convert approved product requirements into a Decision Architecture that communicates component structure, technology choices, and rationale for implementation teams.

## Inputs Required
- prd: latest PRD plus epic roadmap from product-requirements skill
- constraints: non-functional requirements, compliance rules, and integrations
- existing_assets: repositories, current architecture diagrams, or technology standards
- project_level: BMAD level sizing to guide depth of design

Missing inputs must be escalated to the orchestrator or originating skill before work proceeds.

## Outputs
- `ARCHITECTURE.md` written using `assets/decision-architecture-template.md.template`
- Updated risk and decision log entries summarized for stakeholders

Deliverables should highlight decisions, rejected options, and implementation guardrails.

## Process
1. Validate prerequisites via `CHECKLIST.md` and confirm planning artifacts are approved.
2. Identify architecture drivers (quality attributes, constraints, integrations).
3. Design component topology, data flows, and technology selections with traceability to requirements.
4. Record key decisions, alternatives, and mitigation strategies.
5. Generate or update architecture artifact using `scripts/generate_architecture.py` if structured data is available.
6. Review the quality checklist and publish summary plus follow-up actions for delivery-planning and development-execution skills.

## Quality Gates
Follow `CHECKLIST.md` to ensure completeness, feasibility, and stakeholder alignment. Stop if guardrails fail.

## Error Handling
When contradictions or gaps exist:
- Cite the specific requirement or assumption causing the conflict.
- Request clarifications from product-requirements, UX, or discovery-analysis skills.
- Recommend holding implementation until resolution is documented.
