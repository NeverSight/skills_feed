---
name: auto-claude-updater
description: Auto-update system for Auto-Claude skills and documentation. Use when checking for updates, synchronizing with upstream, updating skills automatically, or managing version compatibility.
version: 1.0.0
auto-claude-version: 2.7.2
---

# Auto-Claude Updater

Automatic synchronization of skills and documentation with upstream Auto-Claude releases.

## Overview

This skill provides:
- **Version checking** - Detect new Auto-Claude releases
- **Skill synchronization** - Update local skills with latest docs
- **Changelog parsing** - Extract relevant changes
- **Compatibility checks** - Ensure skill-version alignment

## Quick Commands

### Check for Updates

```bash
# Check if new version available
auto-claude-update --check

# Or using git
cd /path/to/Auto-Claude
git fetch origin
git log main..origin/main --oneline
```

### Update Auto-Claude

```bash
# Update from source
cd /path/to/Auto-Claude
git pull origin main
npm run install:all

# Or download new release
# https://github.com/AndyMik90/Auto-Claude/releases/latest
```

### Sync Skills

```bash
# Run skill update script
cd /path/to/skills-repo
./scripts/sync-auto-claude-skills.sh
```

## Update Workflow

### 1. Check Version

```bash
# Current version
cat /path/to/Auto-Claude/package.json | grep '"version"'

# Latest release
curl -s https://api.github.com/repos/AndyMik90/Auto-Claude/releases/latest | grep '"tag_name"'
```

### 2. Review Changelog

```bash
# View recent changes
cat /path/to/Auto-Claude/CHANGELOG.md | head -100

# Or fetch from GitHub
curl -s https://raw.githubusercontent.com/AndyMik90/Auto-Claude/main/CHANGELOG.md | head -100
```

### 3. Update Repository

```bash
cd /path/to/Auto-Claude

# Stash local changes
git stash

# Pull latest
git pull origin main

# Reinstall dependencies
npm run install:all

# Restore local changes
git stash pop
```

### 4. Sync Skills

After updating, synchronize skill documentation:

```bash
# Copy latest docs to skills
./scripts/sync-auto-claude-skills.sh

# Or manually update
cp /path/to/Auto-Claude/README.md /path/to/skills/auto-claude-setup/references/
cp /path/to/Auto-Claude/CLAUDE.md /path/to/skills/auto-claude-cli/references/
cp /path/to/Auto-Claude/guides/CLI-USAGE.md /path/to/skills/auto-claude-cli/references/
```

## Automatic Update Script

### sync-auto-claude-skills.sh

```bash
#!/bin/bash
# Auto-Claude Skills Sync Script

AUTO_CLAUDE_PATH="${AUTO_CLAUDE_PATH:-/mnt/c/data/github/external/Auto-Claude}"
SKILLS_PATH="${SKILLS_PATH:-.claude/skills}"

echo "Syncing Auto-Claude skills..."

# Check current version
CURRENT_VERSION=$(cat "$AUTO_CLAUDE_PATH/package.json" | grep '"version"' | sed 's/.*"version": "\(.*\)".*/\1/')
echo "Auto-Claude version: $CURRENT_VERSION"

# Update setup skill references
echo "Updating auto-claude-setup..."
cp "$AUTO_CLAUDE_PATH/README.md" "$SKILLS_PATH/auto-claude-setup/references/"
cp "$AUTO_CLAUDE_PATH/CONTRIBUTING.md" "$SKILLS_PATH/auto-claude-setup/references/"

# Update CLI skill references
echo "Updating auto-claude-cli..."
cp "$AUTO_CLAUDE_PATH/CLAUDE.md" "$SKILLS_PATH/auto-claude-cli/references/"
cp "$AUTO_CLAUDE_PATH/guides/CLI-USAGE.md" "$SKILLS_PATH/auto-claude-cli/references/" 2>/dev/null || true

# Update memory skill references
echo "Updating auto-claude-memory..."
cp "$AUTO_CLAUDE_PATH/apps/backend/.env.example" "$SKILLS_PATH/auto-claude-memory/references/"

# Update version in all skills
echo "Updating version references..."
for skill_dir in "$SKILLS_PATH"/auto-claude-*; do
    if [ -f "$skill_dir/SKILL.md" ]; then
        sed -i "s/auto-claude-version: 2.7.2
    fi
done

echo "Sync complete!"
```

Save to `.claude/skills/auto-claude-updater/scripts/sync-auto-claude-skills.sh` and make executable:

```bash
chmod +x .claude/skills/auto-claude-updater/scripts/sync-auto-claude-skills.sh
```

## Update Detection

### Check for Breaking Changes

```bash
# Compare versions
CURRENT="2.7.0"
LATEST=$(curl -s https://api.github.com/repos/AndyMik90/Auto-Claude/releases/latest | jq -r '.tag_name' | sed 's/v//')

# Major version change = breaking
if [[ "${CURRENT%%.*}" != "${LATEST%%.*}" ]]; then
    echo "BREAKING: Major version change detected!"
fi
```

### Monitor GitHub Releases

```bash
# Watch for new releases
gh release list -R AndyMik90/Auto-Claude --limit 5

# Get release notes
gh release view v2.7.2 -R AndyMik90/Auto-Claude
```

## Version Compatibility

### Skill Version Matrix

| Skill Version | Auto-Claude Version | Status |
|---------------|---------------------|--------|
| 1.0.0 | 2.7.x | Current |
| 1.0.0 | 2.6.x | Compatible |
| 1.0.0 | 2.5.x | Limited |
| 1.0.0 | 2.4.x | Not tested |

### Breaking Changes Log

Track breaking changes that affect skills:

```markdown
## Breaking Changes

### v2.7.0
- Memory system switched to LadybugDB (no Docker)
- New Ollama embedding support

### v2.6.0
- New spec pipeline phases
- Changed implementation_plan.json format

### v2.5.0
- Claude Agent SDK required
- Removed direct Anthropic API support
```

## Automation

### GitHub Actions Workflow

```yaml
# .github/workflows/sync-auto-claude.yml
name: Sync Auto-Claude Skills

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check for updates
        id: check
        run: |
          LATEST=$(curl -s https://api.github.com/repos/AndyMik90/Auto-Claude/releases/latest | jq -r '.tag_name')
          echo "latest=$LATEST" >> $GITHUB_OUTPUT

      - name: Clone Auto-Claude
        run: |
          git clone --depth 1 https://github.com/AndyMik90/Auto-Claude.git /tmp/Auto-Claude

      - name: Sync skills
        run: |
          AUTO_CLAUDE_PATH=/tmp/Auto-Claude ./scripts/sync-auto-claude-skills.sh

      - name: Create PR
        uses: peter-evans/create-pull-request@v5
        with:
          title: "chore: sync Auto-Claude skills to ${{ steps.check.outputs.latest }}"
          body: "Automated skill sync with upstream Auto-Claude"
          branch: auto-claude-sync
```

### Pre-commit Hook

```bash
# .husky/pre-commit
#!/bin/sh

# Check Auto-Claude version
CURRENT=$(grep 'auto-claude-version:' .claude/skills/auto-claude-setup/SKILL.md | sed 's/.*: //')
LATEST=$(curl -s https://api.github.com/repos/AndyMik90/Auto-Claude/releases/latest | jq -r '.tag_name' | sed 's/v//')

if [ "$CURRENT" != "$LATEST" ]; then
    echo "Warning: Auto-Claude skills may be outdated"
    echo "  Current: $CURRENT"
    echo "  Latest:  $LATEST"
    echo "Run: ./scripts/sync-auto-claude-skills.sh"
fi
```

## Manual Updates

### Update Specific Skill

```bash
# Update just the CLI skill
cd /path/to/skills/auto-claude-cli

# Get latest CLAUDE.md
curl -o references/CLAUDE.md https://raw.githubusercontent.com/AndyMik90/Auto-Claude/main/CLAUDE.md

# Update version
sed -i 's/auto-claude-version: 2.7.2
```

### Add New Feature Documentation

When Auto-Claude adds new features:

1. Read the changelog
2. Update relevant SKILL.md
3. Add new examples
4. Update references

## Troubleshooting

### Sync Fails

```bash
# Check paths
echo $AUTO_CLAUDE_PATH
ls -la $AUTO_CLAUDE_PATH

# Check permissions
ls -la .claude/skills/
```

### Version Mismatch

```bash
# Force version update
VERSION="2.7.2"
for skill in .claude/skills/auto-claude-*; do
    sed -i "s/auto-claude-version: 2.7.2
done
```

### Missing References

```bash
# Ensure reference directories exist
for skill in .claude/skills/auto-claude-*; do
    mkdir -p "$skill/references"
done
```

## Related Skills

- **auto-claude-setup**: Installation guide
- **auto-claude-cli**: CLI reference
- **auto-claude-troubleshooting**: Debugging
