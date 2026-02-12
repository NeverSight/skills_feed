---
name: discover-skills
description: Identify missing skills and recommend installations from AI Cortex or public skill catalogs. Use when discovering capabilities or suggesting skills to fill gaps.
tags: [automation, infrastructure, generalization]
version: 1.3.0
license: MIT
related_skills: [refine-skill-design]
recommended_scope: user
metadata:
  author: ai-cortex
---

# Skill: Discover Skills

## Purpose

Help the Agent identify missing skills for a task and recommend concrete installation steps. This skill discovers candidates and suggests what to install, but does not install or inject skills automatically.

## Use Cases

- **Initial bootstrap**: The Agent starts with only this skill, then recommends which skills to install for the current task.
- **On-demand extension**: When a task requires a Skill that is not available, suggest the best matches and how to install them.
- **Capability discovery**: Help users find relevant skills from local indexes or public catalogs.

## Behavior

1. **Discovery**: Prefer local `skills/INDEX.md` and `manifest.json` for the capability map. If the user asks for external options and network access is available, search a public catalog (e.g. SkillsMP).
2. **Matching**: Match the user task to `name`, `description`, and `tags`; select the best 1–3 skills.
3. **Recommendation**: Explain why each skill matches and whether it is local or external.
4. **Installation guidance**: Provide the exact install command for each recommended skill (e.g. `npx skills add owner/repo --skill name`).
5. **Confirmation**: If the user asks the Agent to install, request explicit confirmation before running any command.

## Input & Output

- **Input**:
  - Description of the current task.
  - Optional: list of already installed skills.
  - Optional: allowed sources (local only vs public catalogs).
- **Output**:
  - Recommended skills with rationale.
  - Install commands for each recommendation.

## Restrictions

- **No auto-install**: Do not execute install commands without explicit user confirmation.
- **No auto-injection**: Do not fetch or inject remote SKILL.md content automatically.
- **No bulk discovery**: Avoid listing large catalogs; return only the top 1–3 matches.

## Self-Check

- [ ] **Relevance**: Are the recommendations strongly related to the current task?
- [ ] **Actionable**: Are install commands concrete and correct?
- [ ] **Consent**: Did the Agent avoid running installs without explicit confirmation?

## Examples

### Example 1: Recommend a local skill

- **Scenario**: User asks for a standardized README.
- **Steps**:
  1. Agent checks `skills/INDEX.md`.
  2. Finds `generate-standard-readme`.
  3. Recommends it and provides: `npx skills add nesnilnehc/ai-cortex --skill generate-standard-readme`.

### Example 2: Edge case - no local match

- **Scenario**: The task is niche and no local skill matches.
- **Expected**: Offer 1–3 external suggestions (if allowed) with install commands, or say "no match found" and ask for clarification. Do not install automatically.

---

## Appendix: Output contract

When this skill produces recommendations, it follows this contract:

| Element | Requirement |
| :--- | :--- |
| Count | Top 1–3 matches only; no bulk catalog listing. |
| Per skill | Name, rationale (why it matches), install command (e.g. `npx skills add owner/repo --skill name`). |
| Source | Prefer local `skills/INDEX.md` and `manifest.json`; external only when user asks and network available. |
| Interaction | Do not run install commands without explicit user confirmation. |
