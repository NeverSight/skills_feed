---
name: contributor-codebase-analyzer
description: >
  Deep-dive code analysis with periodic saving. Contributor mode reads every
  commit diff for annual reviews, accuracy rates, and promotion readiness.
  Codebase mode maps repository structure, cross-repo relationships, and
  enterprise governance. Works with GitHub (gh) and GitLab (glab). Saves
  checkpoints incrementally for resume across sessions.
license: MIT
user-invocable: true
agentic: true
compatibility: "Requires git and either gh (GitHub CLI) or glab (GitLab CLI). Optional: jq, bc."
metadata:
  author: anivar
  version: 3.0.0
  tags: contributor-review, codebase-analysis, enterprise-governance, periodic-saving, github, gitlab
allowed-tools: Bash(git:*) Bash(gh:*) Bash(glab:*) Bash(jq:*) Bash(bc:*)
---

# Contributor Codebase Analyzer

Deep-dive code analysis with periodic saving. Two modes:

- **Contributor mode** — reads every commit diff, calculates accuracy, assesses promotion readiness
- **Codebase mode** — maps repo structure, cross-repo relationships, enterprise governance

Works with **GitHub** (`gh`) and **GitLab** (`glab`). Saves checkpoints to `$PROJECT/.cca/` for resume across sessions.

## Getting Started

First-time users: run onboarding to detect your platform and configure the skill.

```bash
./scripts/checkpoint.sh onboard
```

This will:
1. Detect your git platform (GitHub or GitLab)
2. Identify the repo and org/group
3. Create `.cca/` directory with config
4. Verify CLI tools are available
5. Optionally add your first contributor to track

See `references/onboarding.md` for the full guided setup.

## Mode Detection

| Trigger | Mode | Action |
|---------|------|--------|
| "analyze @user" / "annual review" / "promotion" / "contributor" | Contributor | Deep-dive commit analysis |
| "analyze repo" / "codebase" / "architecture" / "governance" / "dependencies" | Codebase | Repository structure analysis |
| "compare engineers" / "team comparison" | Contributor | Multi-engineer comparison |
| "ownership" / "SPOF" / "who owns" | Contributor | Production ownership mapping |
| "tech debt" / "security audit" / "portfolio" | Codebase | Governance analysis |
| "resume" / "checkpoint" / "continue analysis" | Either | Load last checkpoint, resume |
| "onboard" / "setup" / "getting started" | Setup | Run onboarding flow |

## Platform Support

All analysis uses local `git` for commit-level work. Platform CLIs are used only for PR/MR metadata:

| Feature | GitHub (`gh`) | GitLab (`glab`) |
|---------|--------------|----------------|
| PR/MR counts | `gh search prs` | `glab mr list` |
| Reviews | `gh search prs --reviewed-by` | `glab mr list --reviewer` |
| User lookup | `gh api users/NAME` | `glab api users?username=NAME` |
| Org repos | `gh repo list ORG` | `glab project list --group GROUP` |
| API access | `gh api` | `glab api` |

**Auto-detection:** The skill reads git remote URLs to determine the platform. No manual configuration needed.

## Periodic Saving

All analysis saves incrementally to `$PROJECT/.cca/`. See `references/periodic-saving.md`.

```
$PROJECT/.cca/
├── contributors/@username/
│   ├── profile.jsonl            # Append-only analysis runs
│   ├── checkpoints/2025-Q1.md   # Quarterly snapshots
│   ├── latest-review.md         # Most recent annual review
│   └── .last_analyzed           # ISO timestamp + last SHA
├── codebase/
│   ├── structure.json           # Repo structure map
│   ├── dependencies.json        # Dependency catalog
│   └── .last_analyzed
├── governance/
│   ├── portfolio.json           # Technology portfolio
│   ├── debt-registry.json       # Technical debt items
│   └── .last_analyzed
└── .cca-config.json             # Skill configuration
```

**Resume protocol:** On every invocation, check `.last_analyzed` files. If prior state exists, resume from the gap — never re-analyze already-saved work.

## Quick Reference

### Contributor Mode

**Step 0 — Check before analyzing (mandatory):**
```bash
./scripts/checkpoint.sh check contributors/@USERNAME --author EMAIL
```
- `FRESH` → run full analysis
- `CURRENT` → skip, already analyzed, no new commits
- `INCREMENTAL` → analyze only new commits since last checkpoint

**Count commits before launching agents:**
```bash
git log --author="EMAIL" --after="YEAR-01-01" --before="YEAR+1-01-01" --oneline | wc -l
```

**Batch sizing (hard limits from real failures):**

| Commits | Action |
|---------|--------|
| <=40 | Read in main session |
| 41-70 | Single agent writes findings to file |
| 71-90 | Split into 2 agents |
| 91+ | WILL FAIL — split into 3+ or monthly agents |

**Agents write to files, return 3-line summaries.** Never return raw analysis inline.

**7-phase annual review process:**
1. Identity Discovery — find all git email variants
2. Metrics — commits, PRs/MRs, reviews, lines (git + platform CLI)
3. Read ALL Diffs — quarterly parallel agents, file-based output
4. Bug Introduction — self-reverts, crash-fixes, same-day fixes, hook bypass
5. Code Quality — anti-patterns and strengths from diff reading
6. Report Generation — structured markdown with growth assessment + development plan
7. Comparison — multi-engineer strengths comparison with evidence

**Accuracy rate:**
```
Effective Accuracy = 100% - (fix-related commits / total commits)
```

| Rate | Assessment |
|------|-----------|
| >90% | Excellent |
| 85-90% | Good |
| 80-85% | Concerning |
| <80% | Needs focused improvement |

**Tool separation:**
- **Platform CLI** (`gh`/`glab`): Get commit lists, PR/MR counts, review counts, user lookup
- **Local `git`**: Read commit diffs, blame, shortlog from cloned repo (faster, no rate limits)
- Use CLI to discover what to analyze, use local repo to read the actual code

### Codebase Mode

**Three tiers of analysis:**

| Tier | Scope | Output |
|------|-------|--------|
| Repo Structure | Single repo internals | `codebase/structure.json` |
| Cross-Repo | Multi-repo relationships | `codebase/dependencies.json` |
| Governance | Enterprise portfolio | `governance/portfolio.json` |

**Cross-repo analysis:**
```bash
# GitHub
gh repo list ORG --limit 100 --json name,language,updatedAt

# GitLab
glab project list --group GROUP --per-page 100 -o json
```

### API Rate Limits

Contributor analysis is mostly rate-limit-free (Phases 3-7 use local `git` only). Cross-repo analysis (Tier 2-3) loops over org repos via API — check limits before heavy operations:

```bash
./scripts/checkpoint.sh ratelimit
```

If rate-limited mid-scan, progress is saved automatically. Resume skips already-processed repos.

### Checkpoint Commands

```bash
# Onboard (first-time setup)
./scripts/checkpoint.sh onboard

# Save current state
./scripts/checkpoint.sh save contributors/@alice

# Resume from last checkpoint
./scripts/checkpoint.sh resume contributors/@alice

# Show checkpoint status
./scripts/checkpoint.sh status
```

## Priority-Ordered References

| Priority | Reference | Impact | Mode |
|----------|-----------|--------|------|
| 0 | `onboarding.md` | SETUP | Both |
| 1 | `periodic-saving.md` | CRITICAL | Both |
| 2 | `contributor-analysis.md` | CRITICAL | Contributor |
| 3 | `accuracy-analysis.md` | HIGH | Contributor |
| 4 | `code-quality-catalog.md` | HIGH | Contributor |
| 5 | `qualitative-judgment.md` | HIGH | Contributor |
| 6 | `report-templates.md` | HIGH | Contributor |
| 7 | `codebase-analysis.md` | HIGH | Codebase |

## Problem to Reference Mapping

| Problem | Start With |
|---------|------------|
| First time using this skill | `onboarding.md` |
| Annual review for 1 engineer | `contributor-analysis.md` then `report-templates.md` |
| Comparing 2+ engineers | `contributor-analysis.md` then `qualitative-judgment.md` |
| Engineer has 200+ commits | `contributor-analysis.md` (batch sizing section) |
| Resume interrupted analysis | `periodic-saving.md` |
| Is this engineer promotion-ready? | `qualitative-judgment.md` then `accuracy-analysis.md` |
| Who owns the payment system? | `contributor-analysis.md` (production ownership section) |
| Map repo architecture | `codebase-analysis.md` (Tier 1) |
| Cross-repo dependencies | `codebase-analysis.md` (Tier 2) |
| Enterprise tech portfolio | `codebase-analysis.md` (Tier 3) |
| Quality assessment from code | `code-quality-catalog.md` then `accuracy-analysis.md` |
| Plateau detection | `qualitative-judgment.md` (growth trajectory section) |
| Tech debt inventory | `codebase-analysis.md` (governance section) |

## QMD Pairing

This skill complements QMD (knowledge search). Division of responsibility:

| Concern | Tool |
|---------|------|
| Search documentation, wikis, specs | QMD |
| Analyze commit diffs, code quality | Contributor Codebase Analyzer |
| Find API references, tutorials | QMD |
| Map repository structure | Contributor Codebase Analyzer |
| Answer "how does X work?" | QMD |
| Answer "who built X and how well?" | Contributor Codebase Analyzer |

## Usage Examples

```
# First-time setup
"Set up contributor-codebase-analyzer for this repo"

# Annual review — provide GitHub/GitLab username (email auto-discovered from git log)
"Analyze github.com/alice-dev for 2025 annual review in repo org/repo"

# Multi-engineer comparison
"Analyze github.com/alice-dev, github.com/bob-eng, gitlab.com/charlie for 2025 reviews.
 I need to decide which 2 get promoted."

# Production ownership mapping
"Analyze production code ownership in this repo"

# Resume interrupted analysis
"Resume the contributor analysis for github.com/alice-dev"

# Repository structure analysis
"Analyze the codebase structure of this repo"

# Cross-repo dependency mapping (works with GitHub orgs or GitLab groups)
"Map dependencies across all repos in our org"

# Enterprise governance audit
"Run a governance analysis: tech portfolio, debt registry, security posture"

# Checkpoint status
"Show me the current analysis checkpoint status"
```

## Full Compiled Document

For the complete guide with all references expanded: `AGENTS.md`
