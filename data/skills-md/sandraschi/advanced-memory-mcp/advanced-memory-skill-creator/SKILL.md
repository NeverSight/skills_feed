---
name: advanced-memory-skill-creator
description: Use when planning, scaffolding, validating, or packaging Claude skills inside Advanced Memory MCP.
license: Proprietary
---

# Advanced Memory Skill Creator
> **Status**: ✅ Research complete
>
> **Last validated**: 2025-11-08
>
> **Confidence**: 🟡 Medium — Ready for packaging – keep sources current

## When to load this skill
- You need to build a new Claude skill that matches Anthropic’s gold-standard structure.
- You are upgrading a legacy skill (single SKILL.md file) into the modular layout.
- You must validate a skill before sharing it with teammates or packaging it for SkillsMP.
- You want to create repeatable automation around scaffolding, validation, or packaging.

## Quick start workflow
1. **Collect requirements** using the prompts in [modules/process-guide.md](modules/process-guide.md#step-1-understanding).
2. **Run the MCP tool**:
   ```python
   adn_skills_creator(
       operation="scaffold",
       skill_name="my-new-skill",
       output_dir="skills/custom",
       category="developer"
   )
   ```
3. **Fill in content** following the templates in `modules/core-guidance.md`.
4. **Validate** and **package**:
   ```python
   adn_skills_creator(operation="validate", skill_path="skills/custom/my-new-skill")
   adn_skills_creator(operation="package", skill_path="skills/custom/my-new-skill", output_dir="dist")
   ```
5. Record sources, update `the status banner`, and publish.

## CLI equivalents
- Scaffold: `uv run am-skill-creator scaffold my-new-skill --output-dir skills/custom`
- Validate: `uv run am-skill-creator validate skills/custom/my-new-skill`
- Package: `uv run am-skill-creator package skills/custom/my-new-skill --output-dir dist`
- Upgrade legacy skill: `uv run am-skill-creator upgrade skills/legacy/old-skill`

## Module overview
- [Core guidance](modules/core-guidance.md) — Complete playbooks for scaffolding, validation, packaging, and automation.
- [Process guide](modules/process-guide.md) — Anthropic six-step methodology tailored to Advanced Memory.
- [Known gaps](modules/known-gaps.md) — Validation tasks, pending research, and integration TODOs.
- [Research checklist](modules/research-checklist.md) — Mandatory workflow to capture sources and verify freshness.

## Research status
- Research complete as of 2025-11-08 (see sources above); rerun checklist quarterly or after Anthropic updates.
- Document new sources inside `the Source Log` and [modules/research-checklist.md](modules/research-checklist.md) when revisions are made.
- Update `the status banner` to 🟢 High after field validation and peer review.

## Related tools and references
- `adn_skills_creator` portmanteau – runtime interface for all operations.
- `scripts/refactor_skills_modular.py` – bulk upgrade helper.
- `docs/patterns/claude-skills/skill-creator-reference.md` – Anthropic gold standard.
