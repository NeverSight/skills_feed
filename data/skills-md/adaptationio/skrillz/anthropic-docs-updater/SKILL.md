---
name: anthropic-docs-updater
description: Automated documentation update mechanism for anthropic-expert skill. Five-step workflow from update detection through documentation fetching and processing to skill integration and validation. Use when updating Anthropic documentation, checking for new releases, fetching latest docs, keeping anthropic-expert current, or synchronizing with Anthropic product changes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Anthropic Docs Updater

## Overview

anthropic-docs-updater automatically keeps the anthropic-expert skill current by detecting, fetching, and integrating Anthropic documentation updates.

**Purpose**: Automated documentation maintenance for anthropic-expert

**Update Workflow** (5 steps):
1. **Check for Updates** - Detect new releases and documentation changes
2. **Fetch Documentation** - Download updated content from official sources
3. **Process Content** - Convert to skill reference format
4. **Update Skill** - Integrate new content into anthropic-expert
5. **Validate Updates** - Ensure quality maintained, no regressions

**Automation**: 80% automated (manual review for breaking changes)

**Update Sources**:
- GitHub Releases (SDK version updates)
- docs.claude.com/en/release-notes (API updates)
- code.claude.com/docs/en/changelog (Claude Code updates)
- anthropic.com/news (model announcements)

## When to Use

- Weekly/monthly update checks (stay current)
- After Anthropic announces new features
- Before starting new Anthropic project (ensure latest docs)
- When anthropic-expert seems outdated
- Automated scheduled updates (cron job)

## Prerequisites

- anthropic-expert skill installed
- Python 3.7+ with requests library
- GitHub API access (for release checking)
- Internet access (for fetching docs)

## Update Workflow

### Step 1: Check for Updates

**Purpose**: Detect new releases, documentation changes, feature announcements

**Process**:

1. **Check GitHub Releases**
   ```bash
   python scripts/check-updates.py --github
   ```
   - Queries GitHub API for latest releases
   - Checks: anthropic-sdk-python, claude-agent-sdk-python
   - Compares to current versions in changelog.md
   - Reports new releases found

2. **Check Release Notes**
   ```bash
   python scripts/check-updates.py --docs
   ```
   - Fetches docs.claude.com/en/release-notes
   - Compares to last check date
   - Identifies new entries

3. **Check Claude Code Changelog**
   ```bash
   python scripts/check-updates.py --claude-code
   ```
   - Fetches code.claude.com/docs/en/changelog
   - Detects new versions or features

4. **Generate Update Report**
   ```bash
   python scripts/check-updates.py --all
   ```
   - Runs all checks
   - Aggregates findings
   - Outputs: update-report.txt with detected changes

**Validation**:
- [ ] GitHub releases checked
- [ ] Release notes checked
- [ ] Claude Code changelog checked
- [ ] Update report generated
- [ ] New updates detected (or confirmed current)

**Outputs**:
- update-report.txt (what's new)
- List of detected changes
- Recommended update actions

**Time Estimate**: 10-15 minutes (automated)

**Example Output**:
```
Anthropic Documentation Update Check
=====================================
Date: 2025-11-15

GitHub Releases:
✅ anthropic-sdk-python: v0.45.0 (current: v0.42.0) - UPDATE AVAILABLE
✅ claude-agent-sdk-python: v1.12.0 (current: v1.10.0) - UPDATE AVAILABLE

Release Notes (docs.claude.com):
✅ New feature: Batch API cost reduction increased to 60%
✅ New model: Claude Sonnet 4.6 announced

Claude Code Changelog:
- No new updates since last check

Recommendation: UPDATE AVAILABLE
- 2 SDK updates
- 2 API feature updates
- Proceed to Step 2 (Fetch Documentation)
```

---

### Step 2: Fetch Documentation

**Purpose**: Download updated content from official sources

**Process**:

1. **Fetch SDK Documentation**
   ```bash
   python scripts/fetch-docs.py --github-readmes
   ```
   - Downloads README.md from SDK repositories
   - Gets changelog/release notes from GitHub
   - Saves to temp/sdk-docs/

2. **Fetch API Documentation**
   ```bash
   python scripts/fetch-docs.py --api-docs
   ```
   - Fetches updated pages from docs.claude.com
   - Downloads release notes
   - Saves to temp/api-docs/

3. **Fetch Claude Code Documentation**
   ```bash
   python scripts/fetch-docs.py --claude-code-docs
   ```
   - Fetches updated pages from code.claude.com
   - Downloads changelog
   - Saves to temp/claude-code-docs/

4. **Verify Downloads**
   - Check all files downloaded successfully
   - Validate file integrity
   - Confirm no download errors

**Validation**:
- [ ] SDK docs fetched successfully
- [ ] API docs fetched successfully
- [ ] Claude Code docs fetched (if updates)
- [ ] All files saved to temp directory
- [ ] No download errors

**Outputs**:
- temp/sdk-docs/ (SDK documentation)
- temp/api-docs/ (API documentation)
- temp/claude-code-docs/ (Claude Code documentation)
- fetch-log.txt (download log)

**Time Estimate**: 15-30 minutes (automated, depends on amount of content)

---

### Step 3: Process Documentation

**Purpose**: Convert fetched content to skill reference format

**Process**:

1. **Parse Fetched Documentation**
   ```bash
   python scripts/process-docs.py --input temp/ --output processed/
   ```
   - Parses markdown from temp/
   - Extracts relevant sections
   - Identifies code examples
   - Structures by product

2. **Convert to Reference Format**
   - Organize by product/capability
   - Format consistently with existing references
   - Extract code examples properly
   - Add navigation headers

3. **Merge with Existing Content**
   - Compare new vs existing documentation
   - Identify additions, changes, removals
   - Preserve custom examples/notes
   - Generate diff report

4. **Validate Processed Content**
   - Check markdown syntax
   - Verify code examples
   - Ensure consistent formatting

**Validation**:
- [ ] All fetched docs processed
- [ ] Content converted to reference format
- [ ] Organized by product/capability
- [ ] Code examples extracted correctly
- [ ] Diff report generated (what changed)
- [ ] Processed content validated

**Outputs**:
- processed/ (processed documentation)
- diff-report.txt (what changed)
- Formatted content ready for integration

**Time Estimate**: 20-40 minutes (automated with manual review of diff)

---

### Step 4: Update anthropic-expert Skill

**Purpose**: Integrate new content into anthropic-expert skill safely

**Process**:

1. **Backup Current Skill**
   ```bash
   python scripts/update-skill.py --backup
   ```
   - Creates backup of anthropic-expert
   - Saves to anthropic-expert.backup-YYYYMMDD/
   - Preserves all files

2. **Integrate New Content**
   ```bash
   python scripts/update-skill.py --integrate processed/
   ```
   - Updates relevant reference files
   - Adds new features to appropriate sections
   - Preserves custom content
   - Updates changelog.md with changes

3. **Update Version**
   - Increments version number
   - Updates changelog with:
     - Version number
     - Date
     - Changes summary
     - New features
     - Updated documentation

4. **Review Changes**
   - Display diff of what changed
   - Prompt for confirmation (if manual mode)
   - Allow rollback if issues

**Validation**:
- [ ] Current skill backed up
- [ ] New content integrated successfully
- [ ] Changelog updated with version and changes
- [ ] No merge conflicts
- [ ] All reference files valid markdown
- [ ] Ready for validation step

**Outputs**:
- Updated anthropic-expert skill
- Backup in anthropic-expert.backup-*/
- Updated changelog.md
- Integration log

**Time Estimate**: 15-30 minutes (automated, quick review)

---

### Step 5: Validate Updates

**Purpose**: Ensure updates maintain quality and don't introduce regressions

**Process**:

1. **Run Structure Validation**
   ```bash
   python ../../review-multi/scripts/validate-structure.py ../anthropic-expert
   ```
   - Validates YAML frontmatter
   - Checks file structure
   - Verifies naming conventions
   - Ensures progressive disclosure
   - Must pass (5/5 or 4/5)

2. **Test Search Functionality**
   ```bash
   python ../anthropic-expert/scripts/search-docs.py "test query"
   ```
   - Verify search still works
   - Check can find content in updated files
   - Ensure no search errors

3. **Manual Spot Check**
   - Review 2-3 updated sections
   - Verify accuracy of new content
   - Check code examples valid
   - Ensure formatting consistent

4. **Validation Decision**
   - **PASS**: All validations successful → Finalize update
   - **FAIL**: Issues found → Rollback and investigate

5. **Rollback if Failed** (if validation fails)
   ```bash
   python scripts/update-skill.py --rollback
   ```
   - Restores from backup
   - Reverts to previous version
   - Logs failure for investigation

**Validation**:
- [ ] Structure validation passes (≥4/5)
- [ ] Search functionality works
- [ ] Spot check confirms accuracy
- [ ] No regressions detected
- [ ] Quality maintained
- [ ] Update finalized OR rolled back if issues

**Outputs**:
- Validation report
- Final updated skill (if passed)
- OR restored backup (if failed)
- Update success/failure status

**Time Estimate**: 20-30 minutes

---

## Post-Workflow: Update Complete

**If Successful**:
1. ✅ anthropic-expert updated with latest documentation
2. ✅ Changelog.md updated with changes
3. ✅ Quality validated (structure 5/5)
4. ✅ Ready to use with latest Anthropic features

**If Failed**:
1. ❌ Updates rolled back
2. 📋 Investigation needed (check logs)
3. 🔄 Manual review of changes
4. 🛠️ Fix issues and retry

**Next Check**: Weekly or when Anthropic announces updates

---

## Best Practices

### 1. Schedule Regular Updates
**Practice**: Weekly automated check for updates

**Implementation**: Cron job or scheduled task
```bash
# Weekly check (Mondays at 9am)
0 9 * * 1 cd /path/to/skills && python anthropic-docs-updater/scripts/check-updates.py --all
```

### 2. Review Breaking Changes Manually
**Practice**: For major version updates, review changes before applying

**Why**: Breaking changes may require manual updates to examples

### 3. Backup Before Updating
**Practice**: Always backup (Step 4 does this automatically)

**Why**: Can rollback if updates cause issues

### 4. Validate After Updates
**Practice**: Always run Step 5 (validation)

**Why**: Ensures updates don't break skill quality

### 5. Track Update History
**Practice**: Maintain detailed changelog

**Why**: Understand what changed when, aids troubleshooting

---

## Quick Reference

### The 5-Step Update Workflow

| Step | Focus | Time | Automation | Output |
|------|-------|------|------------|--------|
| 1. Check Updates | Detect changes | 10-15m | 100% | update-report.txt |
| 2. Fetch Docs | Download content | 15-30m | 100% | temp/docs/ |
| 3. Process Content | Convert format | 20-40m | 90% | processed/docs/ |
| 4. Update Skill | Integrate content | 15-30m | 95% | Updated skill |
| 5. Validate | Ensure quality | 20-30m | 70% | Validation report |

**Total Time**: 1.5-2.5 hours (mostly automated)

### Update Sources

| Source | What It Tracks | Check Method |
|--------|----------------|--------------|
| GitHub Releases | SDK versions | GitHub API |
| Release Notes | API features | Web scraping |
| Claude Code Changelog | CLI updates | Web scraping |
| Anthropic News | Model announcements | Manual/RSS |

### Common Commands

```bash
# Check for updates
python scripts/check-updates.py --all

# Fetch new documentation
python scripts/fetch-docs.py --all

# Process fetched docs
python scripts/process-docs.py --input temp/ --output processed/

# Apply updates
python scripts/update-skill.py --integrate processed/

# Validate
python scripts/update-skill.py --validate

# Rollback if needed
python scripts/update-skill.py --rollback
```

### Automation Schedule

**Recommended**: Weekly checks, monthly comprehensive updates

**Cron Example** (check weekly, update monthly):
```bash
# Check for updates every Monday
0 9 * * 1 python check-updates.py --all > /tmp/anthropic-updates.log

# Full update first Monday of month
0 10 1-7 * 1 bash run-full-update.sh
```

---

**anthropic-docs-updater ensures anthropic-expert stays current with the latest Anthropic products, features, and documentation through automated update detection, fetching, processing, and integration.**
