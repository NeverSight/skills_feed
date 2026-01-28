---
name: skills-repo-maintenance
description: "Add or update skills in a skills repository for Codex and/or Claude Code. Use when creating new skills, packaging .skill files for Codex, or converting a skill into a Claude Code plugin (marketplace.json + plugin.json)."
---

# Skills Repo Maintenance

## Overview

Maintain a skills repository and keep Codex and Claude Code artifacts in sync.

## Workflow

### 0) Defaults to apply

- Target runtime: **Codex + Claude Code** (both).
- Package output: **must be specified by the user every time** (no default).

### 1) Identify the repo root

- Use the current repo (git root) as the base.
- Example: `git rev-parse --show-toplevel`

### 2) Decide the target runtime(s)

- Default is **both**. If the user explicitly asks for only one runtime, confirm before skipping the other.
- **Codex**: add a skill folder with `SKILL.md` at repo root.
- **Claude Code**: add a plugin folder with `.claude-plugin/plugin.json` and update `.claude-plugin/marketplace.json`.
  - For both, do both and package `.skill` files for Codex distribution.

### 3) Create or update the skill content

- Skill folder must contain `SKILL.md` with YAML frontmatter (`name`, `description`).
- Use lowercase + hyphens for skill names.
- Put extra materials under `references/`, `scripts/`, `assets/` as needed.

### 4) Claude Code plugin requirements (if applicable)

- Plugin lives at repo root (e.g. `drawio/`, `gh-fix-ci/`, `cli-design/`).
- Add `.claude-plugin/plugin.json` inside the plugin folder.
- Add an entry to `<repo-root>/.claude-plugin/marketplace.json`:
  - `name`, `source`, `description`, `version`, `category`, `keywords`
- If the plugin contains multiple skills, place them under
  `<plugin>/skills/<skill-name>/SKILL.md`.

### 5) Codex packaging (if applicable)

- Package to the **user-specified output directory** using the skill packager.
- On Windows, set UTF-8 to avoid decode errors.

```powershell
$env:PYTHONUTF8=1
$codexHome = $env:CODEX_HOME
if (-not $codexHome) { $codexHome = "$env:USERPROFILE\.codex" }
$outDir = "<output-dir>"
python "$codexHome\skills\.system\skill-creator\scripts\package_skill.py" `
  "<repo-root>\\<skill-folder>" `
  $outDir
```

```bash
export PYTHONUTF8=1
codex_home="${CODEX_HOME:-$HOME/.codex}"
out_dir="<output-dir>"
python "$codex_home/skills/.system/skill-creator/scripts/package_skill.py" \
  "<repo-root>/<skill-folder>" \
  "$out_dir"
```

Repeat for each Codex-supported skill.

### 6) Update documentation

- `README.md`
  - Add to **Available Plugins** and **Usage (Claude Code)** when pluginized.
  - Add to **Available Codex skills** and **Usage (Codex)** when packaged.

### 7) Commit + push

- Ensure `codex-skills/dist/*.skill` are tracked for Codex delivery.
- Push changes and open PR if required by your workflow.

## Notes

- Codex reads skills from `.codex/skills` folders; `.skill` is a packaged zip for distribution.
- Claude Code requires the plugin entry in `.claude-plugin/marketplace.json`.
