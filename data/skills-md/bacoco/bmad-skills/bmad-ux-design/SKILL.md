---
name: bmad-ux-design
description: Designs UX and creates wireframes.
allowed-tools: ["Read", "Write", "Grep"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "what should UI look like"
      - "design the UX"
      - "user experience"
      - "wireframes"
      - "user flow"
    keywords:
      - UX
      - UI
      - design
      - wireframe
      - interface
      - usability
      - flow
  capabilities:
    - ux-design
    - wireframe-creation
    - user-flow-design
    - interface-design
  prerequisites:
    - product-requirements-document
  outputs:
    - user-flows
    - wireframes
    - design-system
---

# UX Blueprint Skill

## When to Invoke

**Automatically activate when user:**
- Says "What should the UI look like?", "Design the UX"
- Asks "How should users interact?", "User flow?"
- Mentions "wireframes", "user experience", "interface design"
- Has PRD with UI-heavy features (Level 2-4)
- Uses words like: UX, UI, design, wireframe, interface, usability

**Specific trigger phrases:**
- "What should the UI look like?"
- "Design the UX for [feature]"
- "Create wireframes"
- "User experience for [feature]"
- "Interface design"
- "User flow for [scenario]"

**Do NOT invoke when:**
- No UI/interface in project (backend-only)
- PRD not ready (use bmad-product-planning first)
- Already have UX specs (skip to architecture or stories)

## Mission
Design user experiences that align with BMAD requirements, documenting flows, interaction states, and validation plans that unblock architecture, delivery, and development.

## Inputs Required
- prd_sections: user journeys, functional requirements, constraints
- architecture_notes: technical or platform limits impacting UX
- brand_guidelines: accessibility, tone, device targets, or visual standards

## Outputs
- **User flows** (from `assets/user-flows-template.md.template`)
- **Wireframes** (from `assets/wireframes-template.md.template`)
- **Design system** (from `assets/design-system-template.md.template`)
- UX requirements checklist linked to PRD and stories
- Validation plan (usability or experimentation) for quality-assurance alignment

**Template locations:** `.claude/skills/bmad-ux-design/assets/*.template`

## Process
1. Confirm prerequisites via `CHECKLIST.md`.
2. Clarify personas, scenarios, and surfaces requiring design.
3. Produce information architecture, flows, and state diagrams.
4. Document component specifications and content rules tied to requirements.
5. Define validation approach (tests, instrumentation, success signals) and share with delivery-planning and quality-assurance skills.

**Note on automation:** This skill currently operates through collaborative design conversation using templates. No automation scripts are required—wireframes and design artifacts are created manually using templates from `assets/`. See `scripts/README.md` for future automation roadmap.

## Quality Gates
Ensure every UX decision traces back to requirements or constraints. Run `CHECKLIST.md` prior to handoff.

## Error Handling
- If requirements conflict or are missing, request clarification before designing.
- Flag technical limitations that impact user experience and loop architecture-design.
- Provide alternate recommendations when constraints prevent ideal UX outcomes.
