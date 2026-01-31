---
name: skill-consolidator
description: Create and maintain first-party custom skills by strategically consolidating overlapping third-party skills. Scans globally installed skills (prefer ~/.agents/skills, or $CODEX_HOME/skills, or ~/.codex/skills) to produce an overlap report, then guides merging into a smaller, linked set inside this repo’s `skills/` directory. Use when asked to "clean up skills", "merge skills", "remove duplicates", "consolidate overlapping skills", "organize my skills", or "create a custom skill from other skills".
---

# Skill Consolidator

Create our own “best version” skills by consolidating globally installed skills into a smaller, linked set **inside this repo**, without directly editing the global skills directory.

## When to Use This Skill

Use this skill when the user:

- Wants to consolidate overlapping skills into one first-party skill
- Says “merge skills”, “remove duplicates”, or “organize my skills”
- Wants to create a custom skill by strategically combining third-party skills
- Has a cluster of similar skills (e.g. Playwright) and wants one canonical version
- Needs a safe workflow for reviewing and decommissioning old skill copies

## Safety & constraints

- Treat globally installed skills as **read-only** (default target: `~/.agents/skills`, or `$CODEX_HOME/skills`, or `~/.codex/skills`).
- Prefer **duplication over mutation**: copy skills into this repo before editing.
- Never delete skills as part of consolidation; deprecate via documentation and links instead.

## Skill locations (repo vs global)

- **Repo first-party skills (source of truth):** `./skills/` (edit here first)
- **Global installed skills (source of truth):** `~/.agents/skills/`
  - `~/.codex/skills/` often contains symlinks pointing into `~/.agents/skills/`

## Quick start

1. Generate an overlap report from globally installed skills (read-only):
   - `python3 skills/skill-consolidator/scripts/scan_installed_skills.py --out-dir tmp/skill-consolidator`
2. Pick the first cluster in `tmp/skill-consolidator/overlap_report.md`.
3. Build the canonical result as a first-party skill in `skills/<new-skill-name>/`.

## What “counts” as a good first-party skill (required standard)

Our skills are intentionally **docs-driven**: `SKILL.md` + bundled `references/` + optional `scripts/` are the “product”.

Before considering a consolidation “done”, the first-party skill must meet:

- The required standard: `skills/skill-consolidator/references/first-party-skill-standard.md`

## Workflow

### 1) Vendor upstream skills (third-party and/or personal global skills)

Goal: treat upstream skills as read-only; copy locally only if you truly need diffs.

Common sources:

- Global: `~/.agents/skills/` (recommended global home)
- Codex links: `~/.codex/skills/` (often symlinks into `~/.agents/skills/`)

Recommended default: don’t copy; reference upstream via `~/.agents/skills/`.

### 2) Inventory + overlap report

Run the scanner to produce:

- `inventory.json` (machine-readable)
- `overlap_report.md` (human-readable clusters)

Examples:

- Scan globally installed skills directly (read-only):
  - `python3 skills/skill-consolidator/scripts/scan_installed_skills.py --out-dir tmp/skill-consolidator`
- Scan a custom root:
  - `python3 skills/skill-consolidator/scripts/scan_installed_skills.py --skills-root /path/to/skills --out-dir tmp/skill-consolidator`

### 2) Pick a consolidation strategy per cluster

For each overlapping cluster, choose **one** primary pattern:

- **Merge into one canonical skill**: best when content is truly duplicative.
- **Hub + leaf skills**: best when workflows differ but share concepts (create a hub that routes to specialized skills).
- **Shared references**: best when multiple skills share long “best practices” sections (extract into references and link).

Use: `skills/skill-consolidator/references/combining-best-practices.md` for decision rules and anti-patterns.
Use: `skills/skill-consolidator/references/opinionated-defaults.md` to align the “canonical” result with our preferred tech stack and tooling defaults (when relevant).

### 3) Build the first-party canonical skill in `./skills/`

- Create `skills/<canonical-skill-name>/SKILL.md` that:
  - Routes common trigger phrases (in `description`)
  - Links to leaf skills or reference docs
  - Keeps detailed content in `references/` and reusable code in `scripts/`
  - Meets the required standard in `skills/skill-consolidator/references/first-party-skill-standard.md`

If you keep old skills around inside this repo:
- Narrow triggers or remove their `SKILL.md` so they don’t compete with the canonical skill.

### 4) Consolidate content with progressive disclosure

- Keep `SKILL.md` short and procedural.
- Move detailed “how-to” / long reference content into `references/`.
- When two skills share the same long section, keep it in **one canonical location** and link to it (do not duplicate).

If you need a shared, cross-skill home for references inside this repo, use a `_shared/` folder (see `skills/skill-consolidator/references/combining-best-practices.md`).

### 5) Link skills together (without creating deep dependency chains)

- Add a small “See also” section (a few bullets) at the bottom of related skills.
- Avoid multi-hop references (Skill A -> Skill B -> Skill C). Keep links one hop from the skill you’re editing.

### 6) Install the first-party skill globally (Skills CLI)

After the canonical skill lives in this repo, install it like other skills using the Skills CLI:

- `npx skills add <owner/repo@skill-name> -g -y`

(This assumes the repo/skill is available from the source you use with `npx skills add`.)

### 7) Verify changes

At minimum:

- Re-run the scanner to ensure consolidated skills still parse cleanly.
- Run the script tests:
  - `python3 -m unittest skills/skill-consolidator/scripts/test_scan_installed_skills.py`

If packaging scripts exist in the user’s environment, also validate packaging for the new/edited skills.

### 8) Second-agent review (required)

Before decommissioning any upstream skills, run a second-agent review of the consolidation:

- Focus: “Did we lose important capability? Are triggers safe? Are links and routing clear?”

Use: `skills/skill-consolidator/references/review-and-decommission.md` for the review checklist and a copy/paste review prompt.

### 9) Human check (recommended default)

After the second-agent review passes, do a quick human check to confirm:

- The canonical skill triggers the right scenarios
- The old skills won’t compete with it
- The consolidation is reversible

Use: `skills/skill-consolidator/references/review-and-decommission.md`.

### 10) Decommission upstream copies (safe + reversible)

Do **not** delete upstream skills immediately.

Prefer one of:

- Remove/rename `SKILL.md` files in any local copies so they can’t trigger
- If you keep old first-party copies around, mark them deprecated and narrow triggers

Use: `skills/skill-consolidator/references/review-and-decommission.md` for rules and acceptance criteria.

Note: when scanning this repo’s `skills/`, the overlap scanner won’t include global skills unless you explicitly scan them.
