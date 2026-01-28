---
name: faion-user-researcher
description: "User research: personas, user interviews, jobs-to-be-done, pain point research."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, Task, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# User Research Domain Skill

**Communication: User's language. Docs: English.**

## Purpose

User research and validation for product/startup development. Handles personas, user interviews, jobs-to-be-done, pain point mining, problem validation, survey design, and value proposition testing.

---

## Quick Reference

| Research Area | Key Files |
|---------------|-----------|
| **Personas** | persona-building.md, ai-persona-building.md, audience-segmentation.md |
| **Interviews** | user-interviews.md, user-interviews-methods.md, ai-interview-analysis.md |
| **Pain Points** | pain-point-research.md, problem-validation.md |
| **Validation** | validation-methods.md, user-validation-methods.md, problem-validation-2026.md |
| **JTBD** | jobs-to-be-done.md |
| **Value Prop** | value-proposition-design.md |
| **Surveys** | survey-design.md, user-research-at-scale.md |
| **Use Cases** | use-case-mapping.md, feature-discovery.md |

---

## Decision Tree

| If you need... | Use |
|---------------|-----|
| User profiles | persona-building.md, ai-persona-building.md |
| Pain points | pain-point-research.md, problem-validation.md |
| User motivations | jobs-to-be-done.md |
| Value proposition | value-proposition-design.md |
| Interview structure | user-interviews.md, user-interviews-methods.md |
| Validate problem | problem-validation.md, validation-methods.md |
| Survey questions | survey-design.md |
| Segment users | audience-segmentation.md |
| Map use cases | use-case-mapping.md, feature-discovery.md |
| Define success metrics | success-metrics-definition.md |

---

## Research Modes

| Mode | Output | Files Used |
|------|--------|------------|
| personas | user-personas.md | persona-building.md, ai-persona-building.md |
| pains | pain-points.md | pain-point-research.md, problem-validation.md |
| validate | problem-validation.md | validation-methods.md, problem-validation-2026.md |
| interviews | interview-guide.md | user-interviews.md, user-interviews-methods.md |
| jtbd | jobs-to-be-done.md | jobs-to-be-done.md |

---

## Methodologies (21)

### Persona Building (4)
- Persona building
- AI-assisted persona building
- AI persona building
- Audience segmentation

### User Interviews (4)
- User interviews
- User interviews methods
- AI interview analysis
- User research at scale

### Problem & Pain Points (3)
- Pain point research
- Problem validation
- Problem validation 2026

### Validation Methods (3)
- Validation methods
- User validation methods
- Synthetic users

### Jobs-to-be-Done (1)
- Jobs-to-be-done framework

### Value & Use Cases (4)
- Value proposition design
- Use case mapping
- Feature discovery
- Opportunity solution trees

### Research Instruments (2)
- Survey design
- Success metrics definition

---

## Key Frameworks

| Framework | Purpose | File |
|-----------|---------|------|
| **JTBD** | User motivations & context | jobs-to-be-done.md |
| **Value Prop Canvas** | Problem-solution fit | value-proposition-design.md |
| **Mom Test** | Interview questions | user-interviews-methods.md |
| **Persona Template** | User archetypes | persona-building.md |
| **Opportunity Solution Trees** | Feature prioritization | opportunity-solution-trees.md |

---

## Output Files

All outputs go to `.aidocs/product_docs/`:

| Module | Output File |
|--------|-------------|
| Personas | user-personas.md |
| Pain Points | pain-points.md |
| Validation | problem-validation.md |
| Interviews | interview-guide.md |
| JTBD | jobs-to-be-done.md |
| Value Prop | value-proposition.md |
| Surveys | survey-questionnaire.md |

---

## Integration

### Parent Skill
Orchestrated by `faion-researcher` skill.

### Related Sub-Skills
- **faion-market-researcher** - Market sizing, competitors, pricing

### Next Steps
After user research complete:
- UX design → `faion-ux-ui-designer`
- Feature specs → `faion-sdd`
- Product roadmap → `faion-product-manager`

---

*faion-user-researcher v1.0*
*Sub-skill of faion-researcher*
*21 methodologies | User Research & Validation*
