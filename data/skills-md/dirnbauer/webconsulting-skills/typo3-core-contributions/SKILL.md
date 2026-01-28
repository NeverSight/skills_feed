---
name: typo3-core-contributions
description: TYPO3 Core contribution workflow. Use when working with Forge issues, submitting patches to Gerrit, or contributing docs.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - core
  - contributions
  - gerrit
  - forge
  - patch
---

# TYPO3 Core Contributions Skill

Guide for TYPO3 Core contribution workflow from account setup to patch submission.

## When to Use

- Forge issue URLs (e.g., `https://forge.typo3.org/issues/105737`)
- Contributing patches, fixing TYPO3 bugs
- Gerrit review workflow, rebasing, CI failures

## Prerequisites

Before contributing, ensure you have:

1. **TYPO3.org Account**: Register at https://my.typo3.org/
2. **Gerrit SSH Key**: Upload to https://review.typo3.org/settings/#SSHKeys
3. **Git Config**: Email must match your Gerrit account

```bash
# Verify git config
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add Gerrit remote
git remote add gerrit ssh://your-username@review.typo3.org:29418/Packages/TYPO3.CMS.git
```

## Environment Setup

### Clone TYPO3 Core

```bash
# Clone via Gerrit
git clone ssh://your-username@review.typo3.org:29418/Packages/TYPO3.CMS.git
cd TYPO3.CMS

# Or clone from GitHub (read-only mirror)
git clone https://github.com/TYPO3/typo3.git
cd typo3

# Add Gerrit remote for pushing
git remote add gerrit ssh://your-username@review.typo3.org:29418/Packages/TYPO3.CMS.git
```

### Install Commit Hook

```bash
# Install commit-msg hook for Change-Id
scp -p -P 29418 your-username@review.typo3.org:hooks/commit-msg .git/hooks/
chmod +x .git/hooks/commit-msg
```

## Contribution Workflow

### 1. Find or Create Issue

- Check existing issues: https://forge.typo3.org/projects/typo3cms-core/issues
- Create new issue if needed with detailed description

### 2. Create Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/105737-fix-cache-issue
```

### 3. Implement Changes

- Follow TYPO3 coding guidelines
- Write tests (unit, functional)
- Update documentation if needed

### 4. Commit with Proper Format

```bash
git add .
git commit
```

**Commit Message Format:**

```
[TYPE] Subject line (imperative, max 52 chars)

Description explaining how and why the change was made.
Can be multiple paragraphs.

Resolves: #12345
Releases: main, 13.4
```

### 5. Push to Gerrit

```bash
# Push for review
git push gerrit HEAD:refs/for/main
```

## Commit Message Format

### Types

| Type | Description |
|------|-------------|
| `[BUGFIX]` | Bug fix |
| `[FEATURE]` | New feature |
| `[TASK]` | Refactoring, cleanup, maintenance |
| `[DOCS]` | Documentation only |
| `[SECURITY]` | Security fix (coordinate with security team) |
| `[!!!]` | Breaking change prefix (e.g., `[!!!][TASK]`) |

### Required Footer

```
Resolves: #12345
Releases: main, 13.4
```

- `Resolves:` - Issue number on forge.typo3.org
- `Releases:` - Target branches (main, 13.4, 12.4)

### Example Commit Messages

**Bug Fix:**
```
[BUGFIX] Fix cache invalidation for page translations

The cache was not properly invalidated when updating
translated page properties. This patch ensures the
cache is cleared for all language variants.

Resolves: #105737
Releases: main, 13.4
```

**Breaking Change:**
```
[!!!][TASK] Remove deprecated DataHandler hooks

The legacy hooks have been deprecated since v12 and
are now removed. Use PSR-14 events instead.

See migration guide in the documentation.

Resolves: #98765
Releases: main
```

## Gerrit Workflow

### Update Existing Patch

When changes are requested:

```bash
# Make changes
# ...

# Amend commit (keep same Change-Id!)
git add .
git commit --amend

# Push again
git push gerrit HEAD:refs/for/main
```

### Rebase on Latest Main

```bash
# Fetch latest
git fetch origin main

# Rebase
git rebase origin/main

# Force push (allowed for your own patches)
git push gerrit HEAD:refs/for/main --force
```

### Cherry-pick to Other Branches

After approval on main:

```bash
# Switch to target branch
git checkout 13.4
git pull origin 13.4

# Cherry-pick with original Change-Id
git cherry-pick -x <commit-hash>

# Push for review
git push gerrit HEAD:refs/for/13.4
```

## Code Review

### Review States

| Vote | Meaning |
|------|---------|
| +2 | Approved, ready for merge |
| +1 | Looks good, needs second review |
| 0 | Comment only |
| -1 | Changes needed |
| -2 | Major issues, do not merge |

### CI Requirements

All patches must pass:
- [ ] Coding standards (PHP-CS-Fixer)
- [ ] PHPStan level 8
- [ ] Unit tests
- [ ] Functional tests
- [ ] Acceptance tests (if applicable)

## Troubleshooting

### Push Rejected

```bash
# Missing Change-Id
# Ensure commit hook is installed
scp -p -P 29418 your-username@review.typo3.org:hooks/commit-msg .git/hooks/

# Amend to add Change-Id
git commit --amend
```

### Merge Conflicts

```bash
# Rebase on latest
git fetch origin main
git rebase origin/main

# Resolve conflicts
# Edit conflicting files
git add .
git rebase --continue

# Push updated patch
git push gerrit HEAD:refs/for/main --force
```

### CI Failures

1. Check CI output at review.typo3.org
2. Run tests locally:

```bash
# Run specific test suite
Build/Scripts/runTests.sh -s unit
Build/Scripts/runTests.sh -s functional

# Run PHP-CS-Fixer
Build/Scripts/runTests.sh -s cgl
```

## Related Skills

- **typo3-ddev**: Local development environment
- **typo3-testing**: Writing tests for patches
- **typo3-conformance**: Code quality validation

## Resources

- **Gerrit**: https://review.typo3.org/
- **Forge**: https://forge.typo3.org/
- **Contribution Guide**: https://docs.typo3.org/m/typo3/guide-contributionworkflow/main/en-us/
- **Git Setup**: https://docs.typo3.org/m/typo3/guide-contributionworkflow/main/en-us/Setup/Git/

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-core-contributions-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
