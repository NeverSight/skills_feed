---
name: curate-skills
description: Evaluate, score (ASQM strict), tag, and normalize all Skills; writes agent.yaml and README per skill, detects overlaps, produces ASQM_AUDIT.md or chat summary. Use when auditing skills, after adding/changing skills, or when generating repo-level skill summaries.
tags: [meta-skill, eng-standards, documentation]
version: 1.0.0
license: MIT
related_skills: [refine-skill-design, generate-standard-readme]
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Curate Skills

## Purpose

Govern the skill inventory by evaluating, scoring, tagging, and normalizing every Skill in the repository (including this one). Produce a single source of truth: machine-readable scores and status per skill, normalized human-facing README, overlap detection, and a repo-level summary. Agent-first; README for humans, agent.yaml for Agents.

## Use Cases

- **After adding or changing skills**: Re-score and update status and docs so the inventory stays consistent.
- **Audit**: Review all skills for lifecycle (validated / experimental / archive_candidate) and overlap.
- **Repo summary**: Generate or refresh ASQM_AUDIT.md or a structured chat summary for the whole skills directory.
- **Self-evaluation**: Run curation on the repo including this meta-skill so governance is itself a skill.

## Behavior

1. **Scan**: List all skill directories under the given `skills_directory` (e.g. `skills/`).
2. **Read**: For each skill, read `agent.yaml` if present; otherwise read README or SKILL.md. Prefer agent.yaml when it exists.
3. **Score**: For each skill, assign four ASQM scores 0–5 **strictly**: `agent_native`, `cognitive`, `composability`, `stance`. Apply **strict scoring** (evidence-based, no inflation; see below). Compute **Quality** (linear): `asqm_quality = agent_native + cognitive + composability + stance` (0–20). Write scores and asqm_quality to `agent.yaml`.
4. **Lifecycle**: Apply dual-gate rules. **Gate A** (agent readiness): agent_native ≥ 4. **Gate B** (design integrity): stance ≥ 3. **validated**: Quality ≥ **17** AND Gate A AND Gate B. **experimental**: Quality ≥ 10. **archive_candidate**: otherwise.
5. **Overlaps and position**: For each skill, assign `overlaps_with` (list of overlapping skills in **Git-repo form** `owner/repo:skill-name`, same format for this repo and others; e.g. `nesnilnehc/ai-cortex:generate-standard-readme`, `softaworks/agent-toolkit:commit-work`) and `market_position` (`differentiated` | `commodity` | `experimental`).
6. **Write**: Per skill, write or update `agent.yaml` (scores, status, overlaps_with, market_position) and normalize `README.md` to standard sections (what it does, when to use, inputs/outputs, etc.).
7. **Summary**: Either write `ASQM_AUDIT.md` at repo level or print a structured summary in chat. **ASQM_AUDIT.md must include a final recommendations section** (e.g. “Recommendation”): actionable next steps (e.g. score adjustments, SKILL changes) or an explicit “no changes recommended” conclusion, so every audit ends with clear guidance. Required sections: lifecycle by status, scoring formula, dimension checklist, overlaps, ecosystem, findings, **recommendations** (final), and a short summary table.

**Conceptual split**

- **Scores (ASQM)** measure intrinsic quality: how well the skill is designed for Agents, reasoning offloaded, composability, and stance.
- **Overlaps and market_position** describe ecosystem position: how the skill relates to others in the inventory.

**Scoring model: ASQM (linear quality + dual-gate)**

- **Quality** (linear): `asqm_quality = agent_native + cognitive + composability + stance`; each dimension 0–5, total 0–20.
- **Gate A** (agent readiness): agent_native ≥ 4.
- **Gate B** (design integrity): stance ≥ 3.
- **Lifecycle**: validated ↔ Quality ≥ **17** AND Gate A AND Gate B; experimental ↔ Quality ≥ 10; archive_candidate ↔ otherwise. (Bar set so validated = clearly production-ready: 17/20 + both gates.)
- **Dimensions**: agent_native — Agent consumption (contracts, machine-readable metadata). cognitive — Reasoning offloaded from user to Agent. composability — Ease of combining with other skills or pipelines. stance — Design stance (spec alignment, principles).

**Strict scoring (required)**

- **Evidence-based**: Each score must be justified by the skill’s SKILL.md (e.g. presence of Appendix: Output contract, related_skills, Restrictions, Self-Check).
- **No inflation**: agent_native = 5 only when the skill has an **explicit, machine-parseable output contract** (e.g. Appendix: Output contract or equivalent table/spec in SKILL.md). If output is described only in prose, agent_native ≤ 4.
- **Consistency**: Apply the same criteria across all skills; do not relax for a single skill without justification.

**Ecosystem position (per skill)**

- **overlaps_with**: List of overlapping skills in **Git-repo form** `owner/repo:skill-name`. Use the same format for this repo and for other repos (no separate internal/external). Examples: `nesnilnehc/ai-cortex:refine-skill-design`, `softaworks/agent-toolkit:commit-work`. Empty `[]` if none.
- **market_position**:
  - `differentiated`: Clear differentiator, minimal overlap, distinct value in the inventory.
  - `commodity`: Common capability, overlaps with many skills, standard pattern.
  - `experimental`: Early-stage, niche, or unclear positioning in the ecosystem.

**Interaction**: Before overwriting many skill files or writing ASQM_AUDIT.md, confirm with the user unless they have explicitly requested a full run (e.g. “curate all skills” or “run curate-skills”).

## Input & Output

**Input**

- `skills_directory`: Root path containing skill subdirectories (e.g. `skills/`).

**Output**

- Per skill: updated `agent.yaml` (scores, status, overlaps_with, market_position); normalized `README.md`.
- Repo-level: `ASQM_AUDIT.md` or structured summary in chat.
- Overlap and market_position report: per-skill overlaps_with (owner/repo:skill-name), market_position.

## Restrictions

- Do not change spec/skill.md or manifest.json from within this skill; metadata sync (INDEX, manifest) is a separate step per spec.
- Do not overwrite SKILL.md with this skill; curate-skills updates agent.yaml and README per skill. SKILL.md remains the canonical definition per spec.
- **INDEX.md** is the canonical capability list (registry, tags, version, purpose); do not overwrite it. **ASQM_AUDIT.md** is the repo-level curation artifact: quality, lifecycle, overlaps, ecosystem, findings, and **final recommendations** (actionable next steps or “no changes”); write or update it on full curation runs and commit it.
- Respect existing tags from skills/INDEX.md when normalizing; add or suggest tags only when clearly aligned with the tagging system.
- **Strict scoring**: Apply ASQM dimensions strictly; do not inflate scores. agent_native = 5 only when the skill has an explicit output contract (Appendix or equivalent) in SKILL.md.

## Self-Check

- [ ] All skill directories under the given root were scanned?
- [ ] agent.yaml was read before README when present?
- [ ] Scores (0–5) assigned strictly (evidence-based; agent_native 5 only with explicit output contract)?
- [ ] asqm_quality (0–20) computed and written consistently?
- [ ] Lifecycle status set from Quality + Gate A + Gate B (validated / experimental / archive_candidate)?
- [ ] Per-skill agent.yaml and README written or updated as specified?
- [ ] overlaps_with (owner/repo:skill-name) and market_position assigned and written per skill?
- [ ] ASQM_AUDIT.md or chat summary produced, with a final recommendations section (actionable or “no changes”)?
- [ ] User confirmed before bulk overwrite if required by interaction policy?

## Examples

### Example 1: Full curation run

- **Input**: `skills_directory: skills/`; user said “curate all skills in this repo.”
- **Expected**: Scan all subdirs of `skills/`; read each skill’s agent.yaml or README/SKILL.md; score; assign overlaps_with (owner/repo:skill-name) and market_position per skill; write back agent.yaml and normalized README; report overlaps and market_position; write ASQM_AUDIT.md or print structured summary. Confirm once before writing if policy applies.

### Example 2: Single-skill re-score

- **Input**: User says “re-score and update only refine-skill-design.”
- **Expected**: Read that skill’s agent.yaml or docs; compute scores, status, overlaps_with, and market_position; update only that skill’s agent.yaml and README; do not write ASQM_AUDIT.md unless requested.

### Edge case: New skill with no agent.yaml

- **Input**: A new skill directory has only SKILL.md (no agent.yaml, no README).
- **Expected**: Read SKILL.md; derive scores, overlaps_with, and market_position; create agent.yaml with scores, status, overlaps_with, and market_position; generate a minimal normalized README from SKILL.md. Report in summary that the skill was newly instrumented.

---

## Appendix: Output contract (agent.yaml per skill)

When this skill writes or updates a skill’s `agent.yaml`, it uses this structure so Agents can consume it without reading README:

```yaml
name: [kebab-case skill name]
status: validated | experimental | archive_candidate

primary_use: [one-line purpose]

inputs:
  - [list of input names]

outputs:
  - [list of output artifacts]

scores:
  agent_native: [0-5]
  cognitive: [0-5]
  composability: [0-5]
  stance: [0-5]

asqm_quality: [0-20, linear: agent_native + cognitive + composability + stance]

overlaps_with:   # Git-repo form: owner/repo:skill-name (this repo and others alike)
  - [owner/repo:skill-name]
  - [owner/repo:other-skill]

market_position: differentiated | commodity | experimental
```

- **Scores** (ASQM) measure intrinsic quality. **asqm_quality** = agent_native + cognitive + composability + stance (0–20). **Lifecycle**: validated ↔ Quality ≥ **17** AND agent_native ≥ 4 AND stance ≥ 3; experimental ↔ Quality ≥ 10; archive_candidate ↔ otherwise.
- **overlaps_with** lists overlapping skills in Git-repo form `owner/repo:skill-name` (same format for this repo and other repos); empty `[]` when none.
