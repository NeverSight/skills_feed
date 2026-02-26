---
name: solo-init
description: One-time founder onboarding — generates personalized manifest, STREAM calibration, dev principles, and stack selection. Use when user says "set up solo factory", "initialize profile", "configure defaults", "first time setup", or "onboard me". Safe to re-run. Do NOT use for project scaffolding (use /scaffold).
license: MIT
metadata:
  author: fortunto2
  version: "2.1.1"
  openclaw:
    emoji: "🎬"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion
argument-hint: "[project-path]"
---

# /init

One-time founder onboarding. Asks key questions, generates personalized configuration files. Everything stored as readable markdown/YAML — edit anytime.

Two layers of config:
- **`~/.solo-factory/defaults.yaml`** — org-level (bundle IDs, GitHub org, Apple Team ID). Shared across all projects.
- **`.solo/`** in project — founder philosophy, dev principles, STREAM calibration, selected stacks. Per-project but usually the same.

The templates in `solo-factory/templates/` are defaults. This skill personalizes them based on your answers.

Run once after installing solo-factory. Safe to re-run — shows current values and lets you update them.

## Output Structure

```
~/.solo-factory/
└── defaults.yaml              # Org defaults (bundle IDs, GitHub, Team ID)

.solo/
├── manifest.md                # Your founder manifesto (generated from answers)
├── stream-framework.md         # STREAM calibrated to your risk/decision style
├── dev-principles.md          # Dev principles tuned to your preferences
└── stacks/                    # Only your selected stack templates
    ├── nextjs-supabase.yaml
    └── python-api.yaml
```

Other skills read from these:
- `/scaffold` reads `defaults.yaml` for `<org_domain>`, `<apple_dev_team>` placeholders + `.solo/stacks/` for stack templates
- `/validate` reads `manifest.md` for manifesto alignment check
- `/setup` reads `dev-principles.md` for workflow config
- `/stream` reads `stream-framework.md` for decision framework

## Steps

### 1. Check existing config

- Read `~/.solo-factory/defaults.yaml` — if exists, show current values
- Check if `.solo/` exists in project path
- If both exist, ask: "Reconfigure from scratch?" or "Keep existing and skip?"
- If neither exists, continue to step 2

### 2. Determine project path

If `$ARGUMENTS` contains a path, use it. Otherwise use current working directory.

### 3. Ask org defaults (AskUserQuestion, 5 questions)

See `references/questions.md` → "Round 0: Org Defaults" for full question specs.

### 4. Create org defaults

```bash
mkdir -p ~/.solo-factory
```

Write `~/.solo-factory/defaults.yaml`:
```yaml
# Solo Factory — org defaults
# Used by /scaffold and other skills for placeholder replacement.
# Re-run /init to update these values.

org_domain: "<answer from 3.1>"
apple_dev_team: "<answer from 3.2>"
github_org: "<answer from 3.3>"
projects_dir: "<answer from 3.4>"
knowledge_base_repo: "<answer from 3.5>"
```

### 5. Ask Round 1 — Philosophy & Values (AskUserQuestion, 4 questions)

See `references/questions.md` → "Round 1: Philosophy & Values" for full question specs.

### 6. Ask Round 2 — Development Preferences (AskUserQuestion, 4 questions)

See `references/questions.md` → "Round 2: Development Preferences" for full question specs.

### 7. Ask Round 3 — Decision Style & Stacks (AskUserQuestion, 3 questions)

See `references/questions.md` → "Round 3: Decision Style & Stacks" for full question specs.

### 8. Load default templates + generate personalized files

See `references/generation-rules.md` for:
- Template source locations
- Output file structure (defaults.yaml, manifest.md, stream-framework.md, dev-principles.md, stacks/)
- Personalization rules per file (how answers map to generated content)
- Stack template mapping (answer → YAML file)

### 10. Verify Solograph MCP (optional check)

- Try running `uvx solograph --help` or check if MCP tools are available
- If available: "Solograph detected — code graph ready"
- If not: "Tip: install Solograph for code search across projects (`pip install solograph` or `uvx solograph`)"

### 11. Summary

```
Solo Factory initialized!

Org config:
  Config:         ~/.solo-factory/defaults.yaml
  org_domain:     <value>
  apple_dev_team: <value>
  github_org:     <value>
  projects_dir:   <value>

Founder profile:
  Manifest:       .solo/manifest.md
  Dev Principles: .solo/dev-principles.md
  STREAM:          .solo/stream-framework.md
  Stacks:         .solo/stacks/ (N stacks)

These files are yours — edit anytime.
Other skills read from .solo/ automatically.

Next steps:
  /validate "your idea"          — validate with your manifest
  /scaffold app nextjs-supabase  — scaffold with your stack
```

### Edge cases

See `references/generation-rules.md` → "Edge Cases" for full list.

## Common Issues

### Templates directory not found
**Cause:** solo-factory not installed as submodule or templates moved.
**Fix:** Skill generates from inline knowledge if templates missing. To fix permanently, ensure `solo-factory/templates/` exists.

### Stacks not copied to .solo/
**Cause:** Stack selection answer didn't map to a template file.
**Fix:** Check available stacks in `templates/stacks/`. Re-run `/init` and select from the list.

### defaults.yaml already exists
**Cause:** Previously initialized.
**Fix:** Skill detects existing config and asks whether to reconfigure. Choose "Reconfigure from scratch" to overwrite.
