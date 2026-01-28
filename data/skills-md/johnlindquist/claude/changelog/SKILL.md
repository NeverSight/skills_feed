---
name: changelog
description: Generate and manage changelogs from git history. Use for release notes, tracking breaking changes, and maintaining project history.
---

# Changelog Generator

Generate changelogs from git commits and manage release notes.

## Prerequisites

```bash
# Git
git --version

# GitHub CLI (for release notes)
brew install gh
gh auth login

# Gemini (for AI summaries)
pip install google-generativeai
export GEMINI_API_KEY=your_api_key
```

## CLI Reference

### Git History Commands

```bash
# Recent commits
git log --oneline -20

# Since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Between tags
git log v1.0.0..v1.1.0 --oneline

# With full messages
git log v1.0.0..v1.1.0 --pretty=format:"%h %s%n%b"

# By author
git log --author="name" --oneline -10

# With dates
git log --format="%h %ad %s" --date=short
```

### Finding Tags

```bash
# List all tags
git tag

# List tags with dates
git tag --sort=-creatordate --format='%(refname:short) %(creatordate:short)'

# Latest tag
git describe --tags --abbrev=0

# Tags matching pattern
git tag -l "v1.*"
```

### Generating Changelogs

#### From Git Log
```bash
# Simple changelog since tag
git log v1.0.0..HEAD --oneline > CHANGELOG_DRAFT.md

# Categorized by conventional commits
git log v1.0.0..HEAD --oneline | grep "^[a-f0-9]* feat:"
git log v1.0.0..HEAD --oneline | grep "^[a-f0-9]* fix:"
git log v1.0.0..HEAD --oneline | grep "^[a-f0-9]* chore:"
```

#### Using GitHub CLI
```bash
# Generate release notes
gh release create v1.1.0 --generate-notes

# View release notes draft
gh release create v1.1.0 --generate-notes --notes-start-tag v1.0.0 --dry-run

# From existing release
gh release view v1.0.0
```

### AI-Generated Changelog

```bash
# Get commits since last tag
COMMITS=$(git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%s%n%b")

# Generate polished changelog
gemini -m pro -o text -e "" "Generate a changelog from these commits:

$COMMITS

Format as:
## [Version] - Date

### Added
- New features

### Changed
- Modifications

### Fixed
- Bug fixes

### Breaking Changes
- Any breaking changes

Write user-friendly descriptions, not raw commit messages."
```

## Workflow Patterns

### Release Preparation

```bash
#!/bin/bash
VERSION=$1
LAST_TAG=$(git describe --tags --abbrev=0)

echo "# Release $VERSION"
echo ""
echo "Changes since $LAST_TAG:"
echo ""

# Categorize commits
echo "## Features"
git log $LAST_TAG..HEAD --oneline | grep -i "feat:" | sed 's/^[a-f0-9]* feat: /- /'

echo ""
echo "## Fixes"
git log $LAST_TAG..HEAD --oneline | grep -i "fix:" | sed 's/^[a-f0-9]* fix: /- /'

echo ""
echo "## Other"
git log $LAST_TAG..HEAD --oneline | grep -v -i "feat:\|fix:" | sed 's/^[a-f0-9]* /- /'
```

### Breaking Changes Detection

```bash
# Find breaking changes in commit messages
git log v1.0.0..HEAD --oneline | grep -i "breaking\|BREAKING"

# Find in commit bodies
git log v1.0.0..HEAD --grep="BREAKING" --pretty=format:"%h %s"
```

### Maintaining CHANGELOG.md

Standard format (Keep a Changelog):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature X

### Changed
- Updated Y

### Fixed
- Bug in Z

## [1.1.0] - 2024-01-15

### Added
- Feature A
- Feature B

### Fixed
- Issue #123
```

### Update Script

```bash
#!/bin/bash
VERSION=$1
DATE=$(date +%Y-%m-%d)

# Generate new section
NEW_SECTION="## [$VERSION] - $DATE

$(git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"- %s")
"

# Prepend to changelog (after header)
head -7 CHANGELOG.md > CHANGELOG_NEW.md
echo "" >> CHANGELOG_NEW.md
echo "$NEW_SECTION" >> CHANGELOG_NEW.md
echo "" >> CHANGELOG_NEW.md
tail -n +8 CHANGELOG.md >> CHANGELOG_NEW.md
mv CHANGELOG_NEW.md CHANGELOG.md
```

## Statistics

```bash
# Commits by author since tag
git shortlog -sn v1.0.0..HEAD

# Files changed
git diff --stat v1.0.0..HEAD | tail -1

# Commits per day
git log --format="%ad" --date=short v1.0.0..HEAD | sort | uniq -c

# Most changed files
git diff --stat v1.0.0..HEAD | sort -k3 -n -r | head -10
```

## GitHub Releases

```bash
# Create release with notes
gh release create v1.1.0 --title "v1.1.0" --notes-file RELEASE_NOTES.md

# Create from tag with auto-notes
gh release create v1.1.0 --generate-notes

# Edit existing release
gh release edit v1.1.0 --notes-file UPDATED_NOTES.md

# List releases
gh release list

# Download release assets
gh release download v1.1.0
```

## Best Practices

1. **Use conventional commits** - Enables automatic categorization
2. **Tag releases** - Clean boundaries for changelogs
3. **Write for users** - Translate technical to user impact
4. **Note breaking changes** - Prominently marked
5. **Include issue references** - Link to related issues
6. **Date your releases** - Clear timeline
7. **Keep unreleased section** - Track ongoing work
