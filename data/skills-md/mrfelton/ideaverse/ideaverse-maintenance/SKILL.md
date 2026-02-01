---
name: ideaverse-maintenance
description: Keep Ideaverse vaults healthy through audits, diagnostics, and maintenance workflows. Use when running vault diagnostics, detecting link rot, identifying orphan notes, finding MOC bloat, suggesting archival candidates, validating frontmatter, or generating vault health reports. Triggers on requests like "audit my vault", "find broken links", "check vault health", "what needs archiving", "find orphan notes", or "run maintenance".
---

# Ideaverse Maintenance Skill

Run audits, diagnostics, and maintenance workflows to keep Ideaverse-based Obsidian vaults healthy. Assume familiarity with the core Ideaverse methodology.

## Requirements

- Python 3.8 or later
- No external dependencies (uses only Python standard library)

## Vault Health Diagnostics

### Quick Health Check

Run these in sequence for a complete vault audit. Scripts can be invoked directly (if executable) or via `python3`:

```bash
# 1. Find broken links (critical)
./scripts/find_broken_links.py /path/to/vault
# or: python3 scripts/find_broken_links.py /path/to/vault

# 2. Find orphan notes (structural)
./scripts/find_orphans.py /path/to/vault

# 3. Check frontmatter compliance (consistency)
./scripts/check_frontmatter.py /path/to/vault

# 4. Detect MOC bloat (scale)
./scripts/detect_moc_bloat.py /path/to/vault

# 5. Find squeeze points (opportunities)
./scripts/validate_squeeze_points.py /path/to/vault

# 6. Suggest archival candidates (hygiene)
./scripts/suggest_archival.py /path/to/vault
```

> **Note:** If `python3` is not available on your system, use `python` if it points to Python 3.x.

### Script Descriptions

| Script | Purpose | Output |
|--------|---------|--------|
| `find_broken_links.py` | Discover wikilinks pointing to non-existent notes | List of source files with broken links |
| `find_orphans.py` | Identify notes with no incoming links | List of orphan note paths |
| `check_frontmatter.py` | Verify required properties (up, created) | Issues grouped by type |
| `detect_moc_bloat.py` | Find MOCs with 50+ direct links | MOCs sorted by link count |
| `validate_squeeze_points.py` | Find unstructured clusters needing MOCs | Terms linked 10+ times without MOC |
| `suggest_archival.py` | Identify stale notes for archival consideration | Notes sorted by staleness indicators |

All scripts accept a vault path argument and return structured output. Exit code 0 = healthy, 1 = issues found.

## Maintenance Cadences

### Daily (5 minutes)
- Review today's daily log for unprocessed fleeting notes
- Quick scan for any broken links introduced today

### Weekly (15-30 minutes)
- Run `find_broken_links.py` and fix any issues
- Run `find_orphans.py` - triage: link, archive, or delete
- Spot-check frontmatter on recently created notes

### Monthly (1-2 hours)
- Full diagnostic suite (all 6 scripts)
- Review MOC bloat - split any MOCs over 50 links
- Process squeeze points - create MOCs where warranted
- Review archival suggestions - archive confirmed stale notes
- Generate and save vault health report

### Quarterly (Half day)
- Comprehensive vault audit
- Review and clean Archive folder
- Assess MOC hierarchy - simplify or restructure as needed
- Update any vault-level documentation

## Deep Dives

Use reference docs for detailed decision trees, workflows, and maintenance playbooks:

- [references/vault-hygiene.md](references/vault-hygiene.md) - Hygiene workflows, cadences, and reporting
- [references/troubleshooting.md](references/troubleshooting.md) - Diagnosis and resolution guides