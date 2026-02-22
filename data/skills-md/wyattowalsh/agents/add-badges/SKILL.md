---
name: add-badges
description: >-
  Scan a codebase to detect languages, frameworks, CI/CD pipelines, package
  managers, and tools, then generate and insert shields.io badges into the
  README with correct icons, brand colors, and live data endpoints. Use when
  adding badges, updating badges, removing badges, improving README appearance,
  adding shields, adding CI status badges, or making a README look more
  professional. Supports shields.io, badgen.net, and forthebadge.com with all
  styles including for-the-badge. Handles badge grouping, ordering, style
  matching, custom badges, and incremental updates.
argument-hint: "[--profile active] [--include status,package] [--exclude social] [--style flat-square] [--layout centered] [--yes] [--replace] [--dry-run] [--readme PATH] [--dark-mode]"
hooks:
  PreToolUse:
    - matcher: Edit
      hooks:
        - command: "git diff --quiet HEAD -- README.md 2>/dev/null || echo 'WARNING: README.md has uncommitted changes that may be overwritten'"
---

## Phase 1 — Detect

Run the detection script via the Bash tool:

```
uv run python skills/add-badges/scripts/detect.py <path>
```

Parse the JSON output. The script detects: repo info, languages, package managers, frameworks, CI/CD, infrastructure, code quality, testing, docs, license, release, security, community, developer tooling, databases, monorepo signals, and existing badges.

If the script fails (uv unavailable, Python missing, script error, invalid JSON), fall back to manual detection:
- Glob for manifest files (pyproject.toml, package.json, go.mod, Cargo.toml, etc.)
- Read `.git/config` or run `git remote get-url origin` for owner/repo
- Glob `.github/workflows/*.yml` for CI badge candidates
- Read LICENSE first line for SPDX type
- Check for Dockerfile, .pre-commit-config.yaml, codecov.yml, etc.

## Phase 2 — Select

Read `references/badge-catalog-core.md` (always). Read `references/badge-catalog-extended.md` when detection reports any non-basic signals (any of: frameworks, infrastructure, code_quality linters/formatters/type_checkers, docs, release, security, monorepo, databases, developer_tooling, community).

Read `references/style-guide.md` for layout, ordering, and URL conventions.

**Selection rules:**
- Prefer dynamic endpoints over static — never hardcode version numbers, coverage %, download counts
- Include `?logo={slug}&logoColor={white|black}` on every badge with a Simple Icons slug
- Match existing badge style if README already has badges (from `existing_badges.style`); default to `flat-square`
- If platform is GitLab or Bitbucket, use shields.io platform paths (`/gitlab/...`, `/bitbucket/...`)
- `--profile <name>`: preset badge selection by maturity. `new` (3-5 badges: status, license, language), `active` (8-12: core + quality, code-style, frameworks), `mature` (12-18: core + all extended except developer-tooling), `enterprise` (15-20: ALL 16 categories including OpenSSF). Overrides `--include`/`--exclude`. No profile = auto-select based on detected features
- Target 8-15 badges; group by display super-groups: Status > Quality > Package > Tech Stack > Social

**Display super-group → category mapping:**

| Super-group | Categories |
|---|---|
| Status | status |
| Quality | quality, code-style, security |
| Package | package, license |
| Tech Stack | language, frameworks, infrastructure, docs, release, databases, monorepo, developer-tooling |
| Social | social, community |
- Deduplicate against existing badges by comparing badge URL service/metric paths
- For CI status: prefer native badge URL (e.g., `github.com/{owner}/{repo}/actions/workflows/{file}/badge.svg`) — works for private repos. For repos with 5+ workflows, prioritize CI/test workflows; let user select others in Phase 3
- If `repo.visibility` is `"private"`, skip badges marked `requires: public-api` and warn user. Prefer native URLs for CI and direct service URLs for coverage
- If existing badges reference dead services (from `existing_badges.dead_services`), flag them and suggest catalog replacements
- Custom badge support: if user requests a badge not in the catalog (Discord server, sponsor, custom API), construct from shields.io static badge API or endpoint badge API (`/badge/dynamic/json?url=...&query=...`). Ask for required params
- If user requests forthebadge.com-style decorative badges, use forthebadge.com API. Note: forthebadge is decorative only — no dynamic data. For dynamic badges in large bold style, use shields.io `?style=for-the-badge`

**Flag handling:**
- `--include <categories>`: only generate badges from named categories (comma-separated). Category names: status, quality, package, license, language, social, code-style, frameworks, infrastructure, docs, release, databases, monorepo, community, security, developer-tooling. **Mutually exclusive with `--exclude`** — error if both provided
- `--exclude <categories>`: skip named categories. Same names as `--include`. Also accepts display group alias: `tech-stack` expands to language,frameworks,infrastructure,docs,release,databases,monorepo,developer-tooling. **Mutually exclusive with `--include`**
- `--style <style>`: override badge style (flat, flat-square, plastic, for-the-badge, social)
- `--layout <layout>`: badge arrangement — inline (default), centered, grouped, table, collapsible. `collapsible` wraps secondary groups (Tech Stack, Social) in `<details><summary>` elements — ideal for 15+ badges. See style-guide.md
- `--readme <path>`: target a specific file instead of auto-detected README
- `--dark-mode`: generate `<picture>` elements with `<source media="(prefers-color-scheme: dark)">` for theme-aware badges on GitHub. Produce HTML instead of pure markdown
- `--dry-run`: output proposed badge block and diff without modifying any file. Exit after preview
- `--yes`: skip approval prompt before modifying files
- `--replace`: replace content within markers AND consolidate scattered badges into the marker block

## Phase 3 — Present

Show grouped preview with category headers. Render badges as actual `[![alt](url)](link)` markdown so the user can see them.

Diff indicators when updating existing badges:
- `[+]` new badge being added
- `[=]` existing badge being kept
- `[-]` existing badge being removed

If scattered badges exist outside markers, show their locations and offer to consolidate into the marker block.

If user requests removal only (e.g., "remove social badges"), skip detection, read existing badge block, remove specified badges, present updated block.

Offer to reorder, add, or remove individual badges before finalizing. Accept natural language adjustments ("move stars before license", "drop the forks badge", "add a Discord badge").

Ask for approval before modifying files. Skip approval if `--yes` passed. **Never skip prompts for missing required info** (owner/repo, workflow file names, etc.) even with `--yes`.

If `--dry-run`, output the proposed block and exit without modifying files.

## Phase 4 — Insert

Find existing `<!-- BADGES:START -->` / `<!-- BADGES:END -->` markers or create them.

Insert approved badges grouped by display super-group (Status, Quality, Package, Tech Stack, Social). Separate groups with a blank line. Add `<!-- generated by add-badges YYYY-MM-DD -->` comment inside the marker block.

Insertion point priority:
1. Existing markers (replace content between them)
2. After first `# Title` heading
3. Top of file if no heading found

If no README exists, create one with `# {repo-name}` heading then add badges.

If `--dark-mode`, wrap each badge in `<picture>` elements per style-guide.md.

`--replace` consolidates any scattered badges found outside markers into the marker block. Show user exactly what will be moved — nothing silently deleted.

Preserve any manual content outside markers.

After insertion, optionally run `uv run python skills/add-badges/scripts/validate-badges.py <readme-path>` via Bash to verify all badge URLs return valid responses. Report any broken or slow badges to the user.

## Style Rules

Default style: `flat-square`. Match existing style if badges already present. Use `for-the-badge` for hero/landing sections. Use `social` style for star/follow count badges. Separate display groups with a blank line in the output.

## Error Handling

- No git remote: prompt for `owner/repo`. If user declines, generate only static language/framework/tooling badges (no remote-dependent badges)
- No manifest files: static-only badges
- RST/AsciiDoc README: use appropriate image syntax (see style-guide.md for format-specific syntax)
- Mixed existing styles: recommend standardizing, ask user which style
- Style-only change (`--style` with no other changes): preserve current badge set, update style param only
- Private repo detected: skip `requires: public-api` badges, prefer native badge URLs, warn user
- detect.py produces partial results: work with what is available, note missing sections

## Tricky Icon Slugs

Common Simple Icons gotchas: `gnubash` not `bash`, `nodedotjs` not `node`, `vuedotjs` not `vue`, `nextdotjs` not `next`, `.env` is `dotenv`, `springboot` not `spring-boot`, `flydotio` not `fly`. Note: `nuxt` is now correct (was `nuxtdotjs`). For icons not in the catalog, use lowercase brand name; check simpleicons.org if unsure.

## Golden Example

```markdown
<!-- BADGES:START -->
<!-- generated by add-badges 2025-01-15 -->
[![CI](https://github.com/{owner}/{repo}/actions/workflows/ci.yml/badge.svg)](https://github.com/{owner}/{repo}/actions)
[![PyPI](https://img.shields.io/pypi/v/{package}?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/{package}/)
[![License](https://img.shields.io/github/license/{owner}/{repo}?style=flat-square)](https://github.com/{owner}/{repo}/blob/main/LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/{owner}/{repo}/badge)](https://scorecard.dev/viewer/?uri=github.com/{owner}/{repo})
<!-- BADGES:END -->
```
