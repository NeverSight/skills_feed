---
name: skills-scout
description: Use when a user wants you to discover and optionally install new agent skills for a task, and you must get explicit consent before any global install into Codex.
---

# Skills Scout

## Overview

Discover relevant skills from `skills.sh` and install them globally for Codex **only after** the user reviews options and explicitly approves installation.

Core principle: **Search before building; ask before installing.**

## How this differs from `find-skills` (vercel-labs/skills)

There is an upstream skill that covers “how to use `npx skills find`”. `skills-scout` is intentionally stricter and Codex-focused:
- Adds hard‑mode vetting (repo metadata + risky command scan) before recommending installs.
- Enforces explicit consent gates and Codex global install defaults (`-g -a codex`).
- Optionally pins installed skills into the repo `AGENTS.md` so they’re actually visible per repo.

Reference: https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md

## When to Use

Use this skill when the user:
- Asks “is there a skill for X?” / “find a skill for X”
- Mentions wanting to extend agent capabilities for the task
- Says “install whatever you need” but still expects transparency/consent
- Has a common task where a skill likely exists (testing, CI/CD, PR review, docs, deploy)

Do not use this skill when the user:
- Explicitly forbids installs or network access
- Only wants an explanation (no execution)

## Workflow

### 0) Confirm constraints (Codex global install)

- Install scope: **global** (`-g`)
- Target agent: **codex** (`-a codex`)
- Search scope: **allow all** (entire ecosystem), but **vet credibility before recommending**
- Install count: **unlimited**, but **never install without explicit consent**

If the user wants the “project start” workflow to happen by default in new repos, recommend adding a small routine to their global `~/.codex/AGENTS.md` (do not edit without consent):
- Preview (dry-run): `node ~/.codex/skills/skills-scout/scripts/pin-agents-md.mjs --repo .`
- Apply (write): `node ~/.codex/skills/skills-scout/scripts/pin-agents-md.mjs --repo . --write`

### 1) Check what’s already installed

```bash
npx -y skills ls -g -a codex
ls -la ~/.codex/skills
```

If a suitable skill is already installed, use it instead of installing duplicates.

### 1.5) Quick project scan (to refine search + compatibility)

Before searching, do a quick scan to identify the project’s stack so you don’t recommend irrelevant skills.

Look for:
- Language/runtime (Node/Python/Go/etc.)
- Package manager (pnpm/npm/yarn/bun)
- Framework (Next.js/React/Vite/etc.)
- CI system (GitHub Actions, etc.)

Example commands (keep it fast; don’t read secrets like `.env`):

```bash
ls
rg --files | rg -i '^(package\\.json|pnpm-lock\\.yaml|yarn\\.lock|package-lock\\.json|bun\\.lockb|bun\\.lock|next\\.config\\.|vite\\.config\\.|tsconfig\\.json|pyproject\\.toml|requirements\\.txt|go\\.mod|cargo\\.toml|dockerfile|docker-compose\\.|\\.github/workflows/)'
```

Use this context to:
- build a better query (e.g., “playwright e2e pnpm nextjs”)
- mark candidates **Caution/Avoid** if they assume the wrong stack (e.g., bun-only skill on a pnpm repo)

### 2) Search for candidate skills

Turn the user request into a short keyword query (2–6 words), then run:

```bash
npx -y skills find "<query>"
```

Never invent results. Always run the search and present the real output (or say “no skills found”).

Tip (clean output for copy/paste/notes):

```bash
npx -y skills find "<query>" | sed -r 's/\x1B\[[0-9;]*[mK]//g'
```

### 3) Vet candidates (credibility + risk)

Before recommending any skill for installation, do a quick credibility/risk pass. “Allow all” means *search all*, not *trust all*.

**Hard mode (default): evidence before labels.**
- Never claim “MIT”, “recent push”, “safe”, “maintained”, etc. unless you actually verified it.
- If you cannot verify key facts (license/activity/archived), treat it as **unknown** and classify as **Caution** or **Avoid**.

**Credibility signals (prefer):**
- Maintained repo (recent activity, not archived)
- Clear owner identity (org or known maintainer)
- License present
- Multiple users/adoption signals (stars/downloads/usage), where available
- Skill text is specific, not vague marketing
- Looks compatible with this repo’s stack (package manager/framework/CI)

**Risk signals (avoid or require explicit “I accept risk”):**
- Asks for secrets/tokens in plaintext, or to paste credentials
- Contains destructive commands (`rm -rf`, `sudo`, editing `~/.ssh`, changing shells/rc files)
- Pipes remote scripts to shell (`curl ... | sh`, `wget ... | bash`)
- Downloads/runs opaque binaries without provenance
- Broad filesystem operations outside the current repo without justification

**Hard gating checks (do these, don’t guess):**
1) Identify the backing repo (`owner/repo`) from the skill spec.
2) Fetch repo metadata (GitHub API) and record the facts:

```bash
curl -fsSL "https://api.github.com/repos/<owner>/<repo>" \
  | python -c 'import sys,json; d=json.load(sys.stdin); print(\"archived:\", d.get(\"archived\")); print(\"pushed_at:\", d.get(\"pushed_at\")); print(\"license:\", (d.get(\"license\") or {}).get(\"spdx_id\")); print(\"stars:\", d.get(\"stargazers_count\"))'
```

If `gh` is available, you may use it instead of `curl`:

```bash
gh api repos/<owner>/<repo> --jq '{archived, pushed_at, license:(.license.spdx_id // \"NONE\"), stars:.stargazers_count}'
```

If rate-limited, do **not** ask the user to paste a token. Ask them to set `GITHUB_TOKEN` in the environment (out of band) or proceed without installs.

3) Skim the skill’s `SKILL.md` (and any scripts it references) for the risk signals above.

Assign one of: **Recommended**, **Caution**, **Avoid**.

**Classification rules (harder defaults):**
- **Avoid** if any are true:
  - `archived: true`
  - `license: None` / `NOASSERTION` / missing
  - Any risk signal is present (secrets-in-chat, destructive commands, `curl|sh`, opaque binaries, etc.)
  - `pushed_at` is very old (e.g., > ~12 months)
- **Caution** if any are true:
  - Repo activity is not clearly recent (e.g., pushed > ~6 months ago) or you can’t easily tell
  - Low adoption signal (e.g., very low stars) *or* unclear scope (project-specific)
  - The skill references helper scripts/binaries you have not reviewed yet
  - You can’t verify metadata due to tooling/rate limits
- **Recommended** only if:
  - Not archived, license is present, activity is recent, and no risk signals were found.

Minimum info to show the user per candidate:
- Skill spec (e.g. `owner/repo@skill`)
- `skills.sh` link
- The exact install command
- Your assessment: **Recommended / Caution / Avoid** (with 1-line reason)
- Evidence summary (don’t paste huge blobs): `archived=… license=… pushed_at=… stars=…`

### 4) Present options and ask for consent

Always present choices first. Use a numbered list and ask the user to pick:
- “Install 1 and 3”
- “Install all”
- “Install none; proceed without skills”

Hard mode consent rules:
- Install **Recommended** only after the user explicitly chooses.
- Install **Caution** only after the user explicitly chooses **and** acknowledges risk.
- Do **not** offer **Avoid** for installation by default. Only proceed if the user names it explicitly and says they accept the risk.

### 5) Install the selected skills (global)

```bash
npx -y skills add -g -a codex -y <owner/repo@skill>
```

If the skill spec contains spaces, quote it:

```bash
npx -y skills add -g -a codex -y 'owner/repo@Skill With Spaces'
```

Install multiple skills by repeating the command for each selection.

### 6) Verify installation and proceed

```bash
npx -y skills ls -g -a codex
```

Then load and follow the installed skill(s)’ instructions while doing the user’s task.

### 7) (Optional) Pin installed skills into this repo’s `AGENTS.md`

If you install skills globally, Codex may not “see” them for this repo unless they’re listed in the repo’s `AGENTS.md`.

This repo includes a helper script that:
- scans the current repo to infer stack keywords
- scans installed skills (global + repo-local)
- writes/updates a generated pinned section in `<repo>/AGENTS.md` (creates it if missing)

Dry-run (prints the would-be `AGENTS.md`):

```bash
node ~/.codex/skills/skills-scout/scripts/pin-agents-md.mjs --repo .
```

Apply changes:

```bash
node ~/.codex/skills/skills-scout/scripts/pin-agents-md.mjs --repo . --write
```

Notes:
- Only the block between `<!-- skills-scout:start -->` and `<!-- skills-scout:end -->` is managed.
- Re-running is idempotent.

## Quick Reference

| Goal | Command |
|------|---------|
| Search skills | `npx -y skills find "<query>"` |
| Install (global) | `npx -y skills add -g -a codex -y <owner/repo@skill>` |
| List installed (global) | `npx -y skills ls -g -a codex` |
| Remove (global) | `npx -y skills remove -g -a codex -y <skill-name>` |

## Example (Playwright e2e setup)

User: “Playwright로 e2e 테스트 셋업 해줘. 필요한 스킬 있으면 설치해도 돼.”

1) Search:
```bash
npx -y skills find "playwright e2e"
```

2) Present options (example format):
- 1) `microsoft/playwright@playwright-cli` — https://skills.sh/microsoft/playwright/playwright-cli
  - Install: `npx -y skills add -g -a codex -y microsoft/playwright@playwright-cli`
- 2) `sickn33/antigravity-awesome-skills@playwright-skill` — https://skills.sh/sickn33/antigravity-awesome-skills/playwright-skill
  - Install: `npx -y skills add -g -a codex -y sickn33/antigravity-awesome-skills@playwright-skill`

3) Ask:
“Which ones should I install (e.g., `1`, `2`, `1 2`, or `none`)? I’ll install globally for Codex.”

## Common Mistakes

- Installing immediately because “the user said it’s ok” (still must ask per-task)
- Making up skill search results instead of running `npx skills find`
- Recommending skills without vetting credibility/risk
- Installing project-level (forgetting `-g`) when the user wants global
- Forgetting `-a codex` and installing to the wrong agent
- Treating unknown repos as trusted (always show source + ask first)

## Red Flags — STOP and Ask

- “I’ll install first and explain after”
- “I can just recommend skills without searching”
- “It’s probably fine; no need to vet the repo/scripts”
- “Searching is slow; I’ll skip it”
- “They approved once, so I can keep installing”

## Rationalizations to Counter

| Rationalization | Counter-rule |
|---|---|
| “Time pressure: just start fixing CI” | Run a quick `skills find` first; then ask. If user says “skip”, proceed without installs. |
| “User said ‘install whatever’, so no need to ask” | Still present options and ask which to install (explicit consent each time). |
| “It’s faster to proceed without skills” | At least check; if nothing relevant shows up, proceed normally. |
| “I already know what skills exist” | Don’t guess. Run `npx skills find` and present the real results. |
| “We can trust any skill from skills.sh” | Search is open; trust is earned. Vet credibility and scan for risky commands. |
