---
name: release
tier: solo
description: 'Release your software. Pre-flight validation, changelog generation, version bumps, release commit, tag, draft GitHub Release. Boundary: everything up to the git tag. Triggers: "release", "cut a release", "prepare release", "release check".'
dependencies: []
---

# Release Skill

> **Purpose:** Take a project from "code is ready" to "tagged and ready to push."

Pre-flight validation, changelog from git history, version bumps across package files, release commit, annotated tag, and optional draft GitHub Release. Everything is local and reversible. Publishing is CI's job.

---

## Quick Start

```bash
/release 1.7.0                # full release: changelog + bump + commit + tag
/release 1.7.0 --dry-run      # show what would happen, change nothing
/release --check               # readiness validation only (GO/NO-GO)
/release                       # suggest version from commit analysis
/release 1.7.0 --no-gh-release # skip GitHub Release draft
```

---

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `version` | No | Semver string (e.g., `1.7.0`). If omitted, suggest based on commit analysis |
| `--check` | No | Readiness validation only — don't generate or write anything |
| `--dry-run` | No | Show generated changelog + version bumps without writing |
| `--skip-checks` | No | Skip pre-flight validation (tests, lint) |
| `--no-gh-release` | No | Skip draft GitHub Release creation |
| `--changelog-only` | No | Only update CHANGELOG.md — no version bumps, no commit, no tag |

---

## Modes

### Default: Full Release

`/release [version]` — the complete local release workflow.

Steps: pre-flight → changelog → release notes → version bump → user review → write → release commit → tag → draft GitHub Release → guidance.

### Check Mode

`/release --check` — standalone readiness validation.

Runs all pre-flight checks and reports GO/NO-GO. Useful before starting the release, in CI as a gate, or composed with `/vibe`. Does not generate or write anything.

### Changelog Only

`/release 1.7.0 --changelog-only` — just update CHANGELOG.md.

Generates the changelog entry and writes it. No version bumps, no commit, no tag.

---

## Workflow

### Step 1: Pre-flight

Run these checks before anything else:

```bash
git rev-parse --git-dir           # must be in a git repo
git status --porcelain            # warn if dirty
git branch --show-current         # show current branch
```

**Checks:**

| Check | How | Severity |
|-------|-----|----------|
| Git repo | `git rev-parse --git-dir` | Block — cannot proceed |
| CHANGELOG.md exists | Glob for changelog (case-insensitive) | Offer to create if missing |
| Has `[Unreleased]` section | Read CHANGELOG.md | Warn |
| Working tree clean | `git status --porcelain` | Warn (show dirty files) |
| On expected branch | `git branch --show-current` | Warn if not main/master/release |
| Tests pass | Detect and run test command | Warn (show failures) |
| Lint clean | Detect and run lint command | Warn (show issues) |
| Version consistency | Compare versions across package files | Warn (show mismatches) |
| Commits since last tag | `git log --oneline <range>` | Block if empty — nothing to release |

**Test/lint detection:**

| File | Test Command | Lint Command |
|------|-------------|--------------|
| `go.mod` | `go test ./...` | `golangci-lint run` (if installed) |
| `package.json` | `npm test` | `npm run lint` (if script exists) |
| `pyproject.toml` | `pytest` | `ruff check .` (if installed) |
| `Cargo.toml` | `cargo test` | `cargo clippy` (if installed) |
| `Makefile` with `test:` | `make test` | `make lint` (if target exists) |

If `--skip-checks` is passed, skip tests and lint (still check git state and versions).

In `--check` mode, run all checks and output a summary table:

```
Release Readiness: NO-GO

  [PASS] Git repo
  [PASS] CHANGELOG.md exists
  [PASS] Working tree clean
  [WARN] Branch: feature/foo (expected main)
  [FAIL] Tests: 2 failures in auth_test.go
  [PASS] Lint clean
  [PASS] Version consistency (1.6.0 in all 2 files)
  [PASS] 14 commits since v1.6.0
```

In `--check` mode, stop here. In default mode, continue (warnings don't block).

### Step 2: Determine range

Find the last release tag:

```bash
git tag --sort=-version:refname -l 'v*' | head -1
```

- If no `v*` tags exist, use the first commit: `git rev-list --max-parents=0 HEAD`
- The range is `<last-tag>..HEAD`
- If range is empty (no new commits), stop and tell the user

### Step 3: Read git history

Gather commit data for classification:

```bash
git log --oneline --no-merges <range>
git log --format="%H %s" --no-merges <range>
git diff --stat <range>
```

Use `--oneline` for the summary view and full hashes for detail lookups when a commit message is ambiguous.

### Step 4: Classify and group

Classify each commit into one of four categories:

| Category | Signal |
|----------|--------|
| **Added** | New features, new files, "add", "create", "implement", "introduce", `feat` |
| **Changed** | Modifications, updates, refactors, "update", "refactor", "rename", "migrate" |
| **Fixed** | Bug fixes, corrections, "fix", "correct", "resolve", "patch" |
| **Removed** | Deletions, "remove", "delete", "drop", "deprecate" |

**Grouping rules:**

- Group related commits that share a component prefix (e.g., `auth:`, `api:`, `feat(users)`)
- Combine grouped commits into a single bullet with a merged description
- **Match the existing CHANGELOG style** — read the most recent versioned entry and replicate its bullet format, separator style, and heading structure
- If a commit message is ambiguous, read the diff with `git show --stat <hash>` to clarify

**Key rules:**

- **Don't invent** — only document what git log shows
- **Omit empty sections** — don't include `### Removed` if nothing was removed
- **Commits, not diffs** — classify from commit messages; read diffs only when ambiguous
- **Merge-commit subjects are noise** — already filtered by `--no-merges`

### Step 5: Suggest version

If no version was provided, suggest one based on the commit classification:

| Condition | Suggestion |
|-----------|------------|
| Any commit contains "BREAKING", "breaking change", or `!:` (conventional commits) | **Major** bump |
| Any commits classified as Added (new features) | **Minor** bump |
| Only Fixed/Changed commits | **Patch** bump |

Show the suggestion with reasoning:

```
Suggested version: 1.7.0 (minor)
Reason: 3 new features added, no breaking changes

Current version: 1.6.0 (from package.json, go tags)
```

Use AskUserQuestion to confirm or let the user provide a different version.

### Step 6: Generate changelog entry

Produce a markdown block in [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- description of new feature

### Changed
- description of change

### Fixed
- description of fix
```

Use today's date in `YYYY-MM-DD` format.

**Style adaptation:** Read the existing CHANGELOG entries and match their conventions:
- Bullet format (plain text vs bold names vs backtick names)
- Separator style (em-dash ` — `, hyphen ` - `, colon `: `)
- Grouping patterns (flat list vs sub-sections)
- Level of detail (terse vs verbose)

If no existing entries to reference (first release), use plain Keep a Changelog defaults.

### Step 7: Detect and offer version bumps

Scan for files containing version strings:

| File | Pattern | Example |
|------|---------|---------|
| `package.json` | `"version": "X.Y.Z"` | `"version": "1.6.0"` |
| `pyproject.toml` | `version = "X.Y.Z"` | `version = "1.6.0"` |
| `Cargo.toml` | `version = "X.Y.Z"` | `version = "1.6.0"` |
| `*.go` | `const Version = "X.Y.Z"` or `var version = "X.Y.Z"` | `const Version = "1.6.0"` |
| `version.txt` | Plain version string | `1.6.0` |
| `VERSION` | Plain version string | `1.6.0` |
| `.goreleaser.yml` | Version from ldflags (show, don't modify — goreleaser reads from git tags) | — |

Show what was found:

```
Version strings detected:

  package.json:       "version": "1.6.0"  → "1.7.0"
  src/version.go:     const Version = "1.6.0"  → "1.7.0"
  .goreleaser.yml:    (reads from git tag — no change needed)
```

Use AskUserQuestion: "Update these version strings?" — "Yes, update all" / "Let me choose" / "Skip version bumps"

### Step 8: User review

Present everything that will change:

1. The generated changelog entry (fenced markdown block)
2. The version bumps (file-by-file diff preview)
3. What will happen: "Will write CHANGELOG.md, update 2 version files, create release commit, create tag v1.7.0"

If `--dry-run` was passed, stop here.

Use AskUserQuestion:
- "Proceed with this release?"
- Options: "Yes, do it" / "Let me edit the changelog first" / "Abort"

### Step 9: Write changes

After user confirms:

1. **Update CHANGELOG.md:**
   - Find the `## [Unreleased]` line
   - Find where the unreleased section ends (next `## [` line or EOF)
   - Replace with: fresh empty `## [Unreleased]` + blank line + versioned entry
2. **Update version files** (if user accepted bumps)

### Step 10: Release commit

Stage and commit all release changes together:

```bash
git add CHANGELOG.md <version-files...>
git commit -m "Release v<version>"
```

The commit message is intentionally simple. The changelog has the details.

### Step 11: Tag

Create an annotated tag:

```bash
git tag -a v<version> -m "Release v<version>"
```

### Step 12: Generate release notes

Release notes are **not the changelog**. The changelog is comprehensive and developer-facing. Release notes are what users see on the GitHub Release page — they should be approachable and highlight what matters.

**Audience:** People scrolling their GitHub feed. They haven't read your commit log, don't know your internal architecture names, and will spend 10 seconds deciding if this release matters to them. Write for THEM, not for contributors.

**Quality bar — the feed test:**

- Would a first-time visitor understand every bullet?
- Are internal code names explained or omitted? (e.g., "Gate 4" means nothing — say "retry loop after validation failure")
- Does the Highlights paragraph answer "why should I care?" in plain English?
- Is every bullet about user-visible impact, not implementation detail?

**Structure:**

```markdown
## Highlights

<2-4 sentence plain-English summary of what's new and why it matters.
Written for users, not contributors. No jargon. No internal architecture names.
Answer: "What can I do now that I couldn't before?">

## What's New

<Top 3-5 most important changes, each as a short bullet.
Pick from Added/Changed/Fixed — prioritize user-visible impact.
Explain internal terms or don't use them.>

## All Changes

<CONDENSED version of the changelog — NOT a raw copy-paste from CHANGELOG.md.
Strip: issue IDs (ag-xxx), file paths, internal tool names, architecture jargon.
Keep: what changed, described in plain English.
Each bullet: one sentence, no bold lead-in, no parenthetical issue refs.
End with a link to the full CHANGELOG.md for those who want raw detail.>

[Full changelog](../../CHANGELOG.md)
```

**The All Changes section is NOT the CHANGELOG.** The CHANGELOG is for contributors who want file paths, issue IDs, and implementation detail. The release page condenses that into plain-English bullets a user can scan in 15 seconds. When in doubt, leave it out — the link is there for the curious.

**Condensing rules:**
- Remove issue IDs: `(ag-ab6)` → gone
- Remove file paths: `skills/council/scripts/validate-council.sh` → "council validation script"
- Remove internal terms: "progressive-disclosure reference files" → "reference content loaded on demand"
- Collapse related items: "5 broken links" + "7 doc inaccuracies" → "12 broken links and doc inaccuracies fixed"
- Bold sparingly: only in What's New section, not in All Changes

**Example:**

```markdown
## Highlights

Three security vulnerabilities patched in hook scripts. The validation lifecycle
now retries automatically when validation fails instead of stopping — no manual
intervention needed. The five largest skills now load significantly faster by
loading reference docs only when needed.

## What's New

- **Self-healing validation** — Failed code reviews now retry automatically with failure context, instead of stopping and waiting for you
- **Faster skill loading** — Five core skills restructured to load reference content on demand instead of all at once
- **3 security fixes** — Command injection, regex injection, and JSON injection vulnerabilities patched in hook scripts

## All Changes

### Added

- Self-healing retry loop for the validation lifecycle
- Security and documentation sections for Go, Python, Rust, JSON, YAML standards
- 26 hook integration tests (injection resistance, kill switches, allowlist enforcement)
- Monorepo-friendly quickstart detection

### Fixed

- Command injection in task validation hook (now allowlist-based)
- Regex injection in task validation hook (now literal matching)
- JSON injection in prompt nudge hook (now safe escaping)
- 12 broken links and doc inaccuracies fixed across the project

### Removed

- Deprecated `/judge` skill (use `/council` instead)

[Full changelog](https://github.com/example/project/blob/main/CHANGELOG.md#version)
```

**Always write release notes to a file immediately after generating:**

```bash
mkdir -p .agents/releases
```

Write to `.agents/releases/YYYY-MM-DD-v<version>-notes.md` — this is the **public-facing** file used by `gh release create` and is what users see. It contains ONLY the Highlights + What's New + All Changes structure above, ending with a link to the full CHANGELOG.md. No internal metadata, no pre-flight results, no next steps, no issue IDs, no file paths.

**Show the release notes to the user** as part of Step 8 review, alongside the changelog and version bumps.

### Step 13: Draft GitHub Release

Unless `--no-gh-release` was passed, create a draft GitHub Release using the notes file written in Step 12.

Check for `gh` CLI:
```bash
which gh
```

If available:
```bash
gh release create v<version> --draft --title "v<version>" --notes-file .agents/releases/YYYY-MM-DD-v<version>-notes.md
```

If the tag hasn't been pushed yet (common — we don't push), `gh release create` will fail. In that case, tell the user to push first, then create the release:

```
Tag not pushed yet. After pushing, create the release with:
  gh release create v<version> --draft --title "v<version>" --notes-file .agents/releases/YYYY-MM-DD-v<version>-notes.md
```

Draft, not published — the user reviews and publishes from the GitHub UI or via `gh release edit v<version> --draft=false`.

If `gh` is not available, tell the user the notes file is ready to paste into the GitHub Release page manually.

### Step 14: Post-release guidance

Show the user what to do next:

```
Release v1.7.0 prepared locally.

Next steps:
  git push origin main --tags     # push commit + tag

Your CI will handle: build, validate, publish
  (detected: .github/workflows/release.yml, .goreleaser.yml)
```

If no CI detected:
```
Next steps:
  git push origin main --tags     # push commit + tag
  gh release edit v1.7.0 --draft=false  # publish the GitHub Release

No release CI detected. Consider adding a workflow for automated publishing.
```

### Step 15: Audit trail

Write an internal release record (separate from the public release notes written in Step 12):

```bash
mkdir -p .agents/releases
```

Write to `.agents/releases/YYYY-MM-DD-v<version>-audit.md`:

```markdown
# Release v<version> — Audit

**Date:** YYYY-MM-DD
**Previous:** v<previous-version>
**Commits:** N commits in range

## Version Bumps

<files updated>

## Pre-flight Results

<check summary table>
```

This is an **internal** record for the knowledge flywheel. It does NOT go on the GitHub Release page — that's the `-notes.md` file from Step 12.

**Two files, two audiences:**

| File | Audience | Contains |
|------|----------|----------|
| `*-notes.md` | GitHub feed readers | Highlights, What's New, All Changes |
| `*-audit.md` | Internal/flywheel | Version bumps, pre-flight results |

---

## New Changelog Template

When no `CHANGELOG.md` exists and the user accepts creation, write:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
```

Then proceed with the normal workflow to populate the first versioned entry.

---

## Boundaries

### What this skill does

- Pre-flight validation (tests, lint, clean tree, versions, branch)
- Changelog generation from git history
- Semver suggestion from commit classification
- Version string bumps in package files
- Release commit + annotated tag
- Release notes (highlights + changelog) for GitHub Release page
- Draft GitHub Release (default, opt-out with `--no-gh-release`)
- Post-release guidance
- Audit trail

### What this skill does NOT do

- **No publishing** — no `npm publish`, `cargo publish`, `twine upload`. CI handles this.
- **No building** — no `go build`, `npm pack`, `docker build`. CI handles this.
- **No pushing** — no `git push`, no `git push --tags`. The user decides when to push.
- **No CI triggering** — the tag push (done by the user) triggers CI.
- **No monorepo multi-version** — one version, one changelog, one tag. Scope for v2.

Everything this skill does is local and reversible:
- Bad changelog → edit the file
- Wrong version bump → `git reset HEAD~1`
- Bad tag → `git tag -d v<version>`
- Draft GitHub Release → delete from the UI

---

## Universal Rules

- **Don't invent** — only document what git log shows
- **No commit hashes** in the final output
- **No author names** in the final output
- **Concise** — one sentence per bullet, technical but readable
- **Adapt, don't impose** — match the project's existing style rather than forcing a particular format
- **User confirms** — never write without showing the draft first
- **Local only** — never push, publish, or trigger remote actions
- **Two audiences** — CHANGELOG.md is for contributors (file paths, issue IDs, implementation detail). Release notes are for feed readers (plain English, user-visible impact, no insider jargon). Never copy-paste the changelog into the release notes.
