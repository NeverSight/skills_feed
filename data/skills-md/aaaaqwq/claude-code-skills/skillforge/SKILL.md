---
name: skillforge
description: "Intelligent skill router and creator. Analyzes ANY input to recommend existing skills, improve them, or create new ones. Uses deep iterative analysis with 11 thinking models, regression questioning, evolution lens, and multi-agent synthesis panel. Phase 0 triage ensures you never duplicate existing functionality."
license: MIT
metadata:
  version: 4.0.0
  model: claude-opus-4-5-20251101
  subagent_model: claude-opus-4-5-20251101
  domains: [meta-skill, automation, skill-creation, orchestration, agentic, routing]
  type: orchestrator
  inputs: [any-input, user-goal, domain-hints]
  outputs: [SKILL.md, references/, scripts/, SKILL_SPEC.md, recommendations]
---

# SkillForge 4.0 - Intelligent Skill Router & Creator

Analyzes ANY input to find, improve, or create the right skill.

## When to use

- **Skill discovery**: "Do I have a skill for X?"
- **Skill creation**: "Create a skill for Y"
- **Skill improvement**: "Improve the Z skill"
- **Routing**: Any ambiguous request that needs skill matching

## How it works

1. **Phase 0 Triage**: Check if skill exists (no duplicates)
2. **Analysis**: 11 thinking models evaluate the request
3. **Action**: Route to existing skill OR create new one
4. **Synthesis**: Multi-agent panel validates output

## Triggers

- `SkillForge: {goal}` - Direct activation
- `create skill` / `improve skill` - Natural language
- `do I have a skill for X?` - Discovery

## Core Principles

- **No duplication**: Always check existing skills first
- **Iterative**: Refine through multiple analysis passes
- **Practical**: Focus on actionable skills, not theory

## Outputs

- New skill: `SKILL.md`, references/, scripts/
- Improvement: Modified SKILL.md + recommendations
- Discovery: List of matching existing skills
