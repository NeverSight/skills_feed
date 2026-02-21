---
name: awesome-copilot-sync
version: 1.0.0
description: |
  Monitors awesome-copilot releases for drift against the amplihack integration.
  Checks latest commits on github/awesome-copilot via the GitHub API and reports
  whether the local integration is current or has drifted behind upstream changes.
  Use when auditing integration freshness or before updating awesome-copilot features.
---

# Awesome-Copilot Sync Skill

## Purpose

This skill monitors the github/awesome-copilot repository for new releases and changes, comparing against the last time amplihack's integration was synchronized. It detects drift early so the awesome-copilot MCP server config, native agents, and marketplace registration stay current.

## When to Use This Skill

- **Periodic audits**: Check if the awesome-copilot integration is up to date
- **Before updates**: Verify if upstream changes require local adjustments
- **CI/CD gates**: Include in release checks to flag stale integrations
- **Manual checks**: User asks "is awesome-copilot up to date?"

## How It Works

1. Queries the GitHub API for recent commits on github/awesome-copilot
2. Compares the latest commit timestamp against a local state file
3. Reports one of three statuses:
   - **CURRENT**: No new commits since last check
   - **DRIFT_DETECTED**: New upstream commits found since last sync
   - **ERROR**: Could not reach GitHub API or parse response

## Usage

### Standalone Script

```bash
python .claude/skills/awesome-copilot-sync/check_drift.py
```

### Output Format

```
awesome-copilot sync status: CURRENT
Last checked: 2026-02-16T10:30:00Z
Latest upstream commit: 2026-02-15T08:00:00Z
```

or

```
awesome-copilot sync status: DRIFT_DETECTED
Last checked: 2026-02-10T10:30:00Z
Latest upstream commit: 2026-02-16T14:00:00Z
New commits since last check: 5
```

## State File

The sync state is stored at `~/.amplihack/awesome-copilot-sync-state.json`:

```json
{
  "last_checked": "2026-02-16T10:30:00Z",
  "latest_commit_sha": "abc123",
  "latest_commit_date": "2026-02-15T08:00:00Z"
}
```

## Dependencies

- `gh` CLI (GitHub CLI) -- used for authenticated API access
- No Python package dependencies beyond the standard library
