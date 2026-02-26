---
name: release
description: Create versioned releases with consolidated changelogs. Gathers shipped items, generates CHANGELOG.md entry, creates git tag, and GitHub Release. Use after multiple /ship tasks are merged.
model: haiku
---

# /release - Release Management Agent

## Command Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--help` | `-h` | Show available commands and options |
| `--version` | `-v` | Show workflow skills version |
| `auto` | | Auto-determine version from task types |
| `patch` | | Force patch increment |
| `minor` | | Force minor increment |
| `major` | | Force major increment |

### Flag Handling

**On `-h` or `--help`:**
```
/release - Release Management Agent

Usage:
  /release                           Auto-determine version (recommended)
  /release auto                      Same as above
  /release patch                     Force patch bump (v1.0.0 → v1.0.1)
  /release minor                     Force minor bump (v1.0.0 → v1.1.0)
  /release major                     Force major bump (v1.0.0 → v2.0.0)
  /release v1.2.3                    Explicit version
  /release -h, --help                Show this help message
  /release -v, --version             Show version

Version Auto-Detection:
  - Reads "Version Impact" from each task document
  - Any major → major bump
  - Any minor → minor bump
  - All patch → patch bump

Creates:
  - CHANGELOG.md entry
  - Git tag
  - GitHub Release

Examples:
  /release                           # Auto-detect version
  /release minor                     # Force minor bump
  /release v2.0.0                    # Explicit version
```

**On `-v` or `--version`:**
Display:
```
Workflow Skills v1.4.1
https://github.com/eljun/claude-skills
```

---

## When to Use

Invoke `/release` when:
- Multiple features/fixes have been merged via `/ship`
- Items are in "Ready to Ship" section of TASKS.md
- Ready to create a versioned release

**Examples:**
```bash
/release             # Auto-determine version from task docs (RECOMMENDED)
/release auto        # Same as above - auto-determine
/release patch       # Force patch increment (v1.1.21 → v1.1.22)
/release minor       # Force minor increment (v1.1.21 → v1.2.0)
/release major       # Force major increment (v1.1.21 → v2.0.0)
/release v1.1.22     # Explicit version
```

## Workflow

```
/release [version|auto]
       ↓
1. Get current version from git tags
2. Read "Ready to Ship" items from TASKS.md
3. Filter: Only include items with "Merged" status (✅)
4. Read each task document for Type & Version Impact
5. Auto-calculate version (if not explicit)
   ├── Any major → major bump
   ├── Any minor → minor bump
   └── All patch → patch bump
6. Categorize changes by type
7. Generate changelog entry
8. Update CHANGELOG.md
9. Commit changelog
10. Create git tag
11. Push to remote
12. Create GitHub Release
13. Move ONLY merged items to "Shipped" with release version
        ↓
Release complete!
```

**IMPORTANT:** Only items with "Merged" status (✅) in "Ready to Ship" are included in the release. Unmerged PRs stay in "Ready to Ship" for the next release.

## Pre-Release Checklist

Before running `/release`:

- [ ] All PRs in "Ready to Ship" are merged
- [ ] Main branch is up to date (`git pull`)
- [ ] No uncommitted changes (`git status`)
- [ ] All tests passing

## Step-by-Step Process

### Step 1: Get Current Version

```bash
# Get the latest tag
git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0"

# List recent tags for context
git tag --list --sort=-v:refname | head -5
```

### Step 2: Determine New Version

**If explicit version provided:**
```bash
/release v1.1.22
# Use v1.1.22 directly
```

**If semantic increment provided:**
```bash
/release patch  # v1.1.21 → v1.1.22
/release minor  # v1.1.21 → v1.2.0
/release major  # v1.1.21 → v2.0.0
```

**Version parsing logic:**
```
Current: v1.1.21
         │ │ │
         │ │ └── Patch (bug fixes, small changes)
         │ └──── Minor (new features, backwards compatible)
         └────── Major (breaking changes)
```

### Step 3: Auto-Calculate Version (Recommended)

When using `/release` or `/release auto`, read each task document to determine version:

**Read Version Impact from task docs:**
```markdown
> **Type:** feature
> **Version Impact:** minor  ← Use this field
```

**Auto-calculation logic:**
```
Ready to Ship items:
├── feature-1      → Version Impact: minor
├── bug-fix-1      → Version Impact: patch
└── enhancement-1  → Version Impact: patch

Highest impact = minor
Current version = v1.2.0
New version = v1.3.0
```

**Priority order:**
1. `major` (any major = major bump)
2. `minor` (any minor, no major = minor bump)
3. `patch` (all patch = patch bump)

**Fallback if Version Impact missing:**
- Use Type field to infer:
  - `feature` → `minor`
  - `bugfix` → `patch`
  - `enhancement` → `patch`
  - `documentation` → `patch`
  - `chore` → `patch`

### Step 4: Read "Ready to Ship" Items (Merged Only)

Parse TASKS.md for items in "Ready to Ship" section. **Only include items with Merged = ✅**:

```markdown
## Ready to Ship

| Task | Branch | PR | Merged | Task Doc |
|------|--------|----|--------|----------|
| Quick Actions Redesign | feature/quick-actions | #123 | ✅ Jan 25 | [link](...) | ← INCLUDE
| Session Fix | fix/session-persist | #124 | ✅ Jan 25 | [link](...) | ← INCLUDE
| New Feature | feature/new | #125 | No | [link](...) | ← SKIP (not merged)
```

**Filter logic:**
- `✅` or date in Merged column → Include in release
- `No` or empty in Merged column → Skip (not ready)

### Step 4: Categorize Changes

Read each task document to get the `Type` field:

| Type | Changelog Section |
|------|-------------------|
| `feature` | New Features |
| `bugfix` | Bug Fixes |
| `enhancement` | Enhancements |
| `documentation` | Documentation |
| `chore` | Other Changes |

**Task document type field:**
```markdown
> **Status:** SHIPPED
> **Type:** feature
```

### Step 5: Generate Changelog Entry

Create formatted entry:

```markdown
## [v1.1.22] - January 26, 2026

### New Features
- **Web:** Dashboard redesign with new widgets (#123)

### Bug Fixes
- Fixed session persistence on embed chat (#124)

### Enhancements
- Improved booking calendar performance (#125)

### Documentation
- Updated authentication guide (#126)
```

### Step 6: Update CHANGELOG.md

**Location:** `docs/changelogs/CHANGELOG.md`

Insert new version at the top (after header):

```markdown
# Changelog

All notable changes to this project.

## [v1.1.22] - January 26, 2026
← INSERT HERE

### New Features
...

---

## [v1.1.21] - January 20, 2026
...
```

**If CHANGELOG.md doesn't exist, create it:**

```markdown
# Changelog

All notable changes to this project.

Format based on [Keep a Changelog](https://keepachangelog.com/).

---

## [v1.1.22] - January 26, 2026

### New Features
...
```

### Step 7: Commit Changelog

```bash
git add docs/changelogs/CHANGELOG.md
git commit -m "chore(release): v1.1.22

Release v1.1.22 with:
- Quick Actions grid redesign
- Session persistence fix
- [other items...]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### Step 8: Create Git Tag

```bash
# Create annotated tag with message
git tag -a v1.1.22 -m "Release v1.1.22

New Features:
- Quick Actions grid redesign (#123)

Bug Fixes:
- Session persistence fix (#124)"
```

### Step 9: Push to Remote

```bash
# Push commit
git push origin main

# Push tag
git push origin v1.1.22
```

### Step 10: Create GitHub Release

```bash
gh release create v1.1.22 \
  --title "v1.1.22" \
  --notes "## What's New

### New Features
- **Web:** Dashboard redesign with new widgets (#123)

### Bug Fixes
- Fixed session persistence on embed chat (#124)

---

**Full Changelog:** https://github.com/owner/repo/compare/v1.1.21...v1.1.22"
```

### Step 11: Update TASKS.md

Move **only merged items** from "Ready to Ship" to "Shipped". Unmerged items stay for next release:

**Before:**
```markdown
## Ready to Ship

| Task | Branch | PR | Merged | Task Doc |
|------|--------|----|--------|----------|
| Quick Actions Redesign | feature/quick-actions | #123 | ✅ Jan 25 | [link](...) |
| Session Fix | fix/session-persist | #124 | ✅ Jan 25 | [link](...) |
| New Feature | feature/new | #125 | No | [link](...) |
```

**After:**
```markdown
## Ready to Ship

| Task | Branch | PR | Merged | Task Doc |
|------|--------|----|--------|----------|
| New Feature | feature/new | #125 | No | [link](...) |

---

## Shipped

| Task | PR | Release | Shipped |
|------|-----|---------|---------|
| Quick Actions Grid Redesign | #123 | v1.1.22 | Jan 26 |
| Session Persistence Fix | #124 | v1.1.22 | Jan 26 |
```

**Key points:**
- Only merged items (✅) move to "Shipped"
- Each item gets the release version (v1.1.22)
- Unmerged items stay in "Ready to Ship" for next release
- This ensures `/release` always knows exactly what to include

---

## Changelog Format Guidelines

### Changelog Entry Structure

```markdown
## [vX.Y.Z] - Month DD, YYYY

### New Features
- **Scope:** Description (#PR)

### Bug Fixes
- Description (#PR)

### Enhancements
- Description (#PR)

### Documentation
- Description (#PR)

### Breaking Changes (if any)
- Description of what breaks and migration path
```

### Writing Good Changelog Entries

**Do:**
- Start with verb (Added, Fixed, Improved, Updated)
- Include scope when helpful (Web, API)
- Reference PR number
- Be user-focused (what changed for them)

**Don't:**
- Include internal refactors users don't see
- Be too technical
- Include duplicate entries

**Examples:**
```markdown
# Good
- **Web:** Added dashboard widgets with custom icons (#123)
- Fixed booking calendar not loading on slow connections (#124)

# Bad
- Updated home.tsx
- Refactored Dashboard component
```

---

## Summary Output

After completing `/release`:

```
Release v1.1.22 created successfully!

Changes included:
- New Features: 2
- Bug Fixes: 1
- Enhancements: 1
- Documentation: 1

Files updated:
- docs/changelogs/CHANGELOG.md
- TASKS.md

Git:
- Tag: v1.1.22
- Commit: abc1234

GitHub:
- Release: https://github.com/owner/repo/releases/tag/v1.1.22

Next release will be: v1.1.23 (patch) / v1.2.0 (minor) / v2.0.0 (major)
```

---

## Handling Edge Cases

### No Merged Items in "Ready to Ship"

```
Error: No merged items found in "Ready to Ship" section.

Please ensure:
1. PRs have been created via /ship
2. PRs have been merged (Merged column shows ✅)
3. TASKS.md "Ready to Ship" section has items with Merged = ✅

Current "Ready to Ship" items:
- {task-name}: Not merged (Merged = No)
```

### Tag Already Exists

```
Error: Tag v1.1.22 already exists.

Options:
1. Use a different version: /release v1.1.23
2. Delete existing tag (if mistake): git tag -d v1.1.22
```

### Missing Task Type

If a task document doesn't have a `Type` field:
- Default to "enhancement"
- Warn user to add types for better categorization

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `/ship` | Before /release - gets items to "Ready to Ship" |
| `/task` | Add `Type` field when planning tasks |
| `/document` | Ensure docs are updated before release |

## Recommended Plugins (Optional)

These plugins provide best practices reference but must be installed separately:

| Plugin | Install From | When Useful |
|--------|--------------|-------------|
| `vercel-react-best-practices` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | React/Next.js optimization reference |
| `supabase-postgres-best-practices` | [supabase/agent-skills](https://github.com/supabase/agent-skills) | Database best practices reference |

---

## Task Document Type Field

When using `/task`, include the Type field:

```markdown
> **Status:** PLANNED
> **Priority:** HIGH
> **Type:** feature | bugfix | enhancement | documentation | chore
> **Created:** January 25, 2026
> **Platform:** Web
```

This enables automatic categorization in changelogs.
