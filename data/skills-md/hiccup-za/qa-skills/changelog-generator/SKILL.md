---
name: changelog-generator
description: |
  Automated changelog generation with semantic versioning. Triggers on: generating changelogs,
  updating versions, releasing software, version bumps, changelog updates, semantic versioning,
  and when users ask to "update changelog", "bump version", "create release", or "generate changelog".

  Use when user: needs to update CHANGELOG.md, bump package.json version, create a release,
  generate changelog entries, or follow semantic versioning and Keep a Changelog standards.
metadata:
  version: "1.0.0"
---

# Changelog Generator

Automated changelog generation following semantic versioning (SemVer) and Keep a Changelog standards. This skill guides agents through reviewing staged changes, determining appropriate version bumps, and updating both `@package.json` and `@CHANGELOG.md` files consistently.

## Overview

The Changelog Generator skill automates the process of:
- Analyzing staged git changes to determine change types
- Calculating appropriate semantic version bumps (MAJOR.MINOR.PATCH)
- Updating the version in `@package.json`
- Generating properly formatted changelog entries in `@CHANGELOG.md`
- Ensuring consistency between version numbers and changelog entries

This skill follows the [Semantic Versioning 2.0.0](https://semver.org/) specification and the [Keep a Changelog](https://keepachangelog.com/) format standards.

## When to Apply

Reference this skill when:
- User requests to "update changelog" or "generate changelog"
- User asks to "bump version" or "create release"
- Preparing for a new release
- Need to document changes in a standardized format
- Ensuring version numbers follow semantic versioning
- Maintaining consistent changelog formatting

**Preconditions:**
- Git repository with staged changes
- Existing `@package.json` file with a `version` field
- Existing `@CHANGELOG.md` file following Keep a Changelog format
- Access to git commands (`git diff`, `git status`)

## Workflow

The changelog generation process follows these 7 steps:

### Step 1: Review All Staged Changes

**Objective:** Understand what changes have been staged and categorize them.

**Actions:**
1. Check git status to see what's staged:
   ```bash
   git status
   ```

2. Review all staged changes:
   ```bash
   git diff --cached
   ```

3. Analyze the changes to identify:
   - **Breaking changes**: API changes, removed features, incompatible changes
   - **New features**: Added functionality, new APIs, new components
   - **Bug fixes**: Fixes to existing functionality
   - **Documentation**: README updates, doc changes (usually don't affect version)
   - **Refactoring**: Code improvements without behavior changes (usually PATCH)

4. Review commit messages if available:
   ```bash
   git log --oneline --cached
   ```

**Categorization Guidelines:**
- Breaking changes → MAJOR version bump
- New features → MINOR version bump
- Bug fixes → PATCH version bump
- Documentation only → Usually no version bump (or PATCH if significant)
- Refactoring → Usually PATCH version bump

**Output:** List of categorized changes ready for changelog entry.

### Step 2: Determine the Appropriate Version Bump

**Objective:** Calculate the new version number based on semantic versioning rules.

**Actions:**
1. Read current version from `@package.json`:
   ```bash
   # Read the version field
   cat package.json | grep '"version"'
   ```

2. Apply semantic versioning rules:
   - **MAJOR (X.0.0)**: Increment when you make incompatible API changes
     - Breaking API changes
     - Removed features
     - Changed behavior that breaks existing code
     - Example: `1.2.3` → `2.0.0`
   
   - **MINOR (0.X.0)**: Increment when you add functionality in a backward-compatible manner
     - New features
     - New APIs (backward compatible)
     - Deprecated features (still functional)
     - Example: `1.2.3` → `1.3.0`
   
   - **PATCH (0.0.X)**: Increment when you make backward-compatible bug fixes
     - Bug fixes
     - Security patches
     - Performance improvements
     - Documentation updates (if versioned)
     - Example: `1.2.3` → `1.2.4`

3. **Priority order**: If multiple change types exist, use the highest:
   - MAJOR > MINOR > PATCH
   - If any breaking changes exist → MAJOR
   - Else if any new features exist → MINOR
   - Else → PATCH

**Decision Tree:**
```
Are there breaking changes?
├─ Yes → MAJOR version bump (X.0.0)
└─ No → Are there new features?
    ├─ Yes → MINOR version bump (0.X.0)
    └─ No → PATCH version bump (0.0.X)
```

**Output:** New version number (e.g., `1.2.4`).

### Step 3: Update @package.json Version Accordingly

**Objective:** Update the version field in the root `@package.json` file.

**Actions:**
1. Read the current `@package.json` file
2. Locate the `"version"` field (usually near the top)
3. Update the version number to the new version determined in Step 2
4. **Preserve all formatting:**
   - Keep the same indentation (spaces or tabs)
   - Maintain the same JSON structure
   - Don't modify other fields
   - Don't reorder fields
   - Keep trailing commas if they exist

**Example:**
```json
// Before
{
  "name": "qa-skills",
  "version": "0.4.0",
  "private": true,
  ...
}

// After (PATCH bump)
{
  "name": "qa-skills",
  "version": "0.4.1",
  "private": true,
  ...
}
```

**Important:**
- Only update the `version` field
- Don't change any other content
- Maintain JSON validity
- Preserve file formatting and style

**Output:** Updated `@package.json` with new version number.

### Step 4: Update @CHANGELOG.md with a New Version Block

**Objective:** Add a new version section to `@CHANGELOG.md` following Keep a Changelog format.

**Actions:**
1. Read the current `@CHANGELOG.md` file
2. Locate the `## [Unreleased]` section (should be at the top)
3. Insert a new version block **after** `## [Unreleased]` and **before** the previous version
4. Use the format: `## [X.Y.Z] - YYYY-MM-DD`
   - `X.Y.Z` is the new version number
   - `YYYY-MM-DD` is the current date (see Step 5)

**Example Structure:**
```markdown
# Changelog

## [Unreleased]

## [0.4.1] - 2026-01-25

### Added
- New feature description

## [0.4.0] - 2026-01-25
...
```

**Important:**
- Place new version block between `[Unreleased]` and the previous release
- Use exact format: `## [X.Y.Z] - YYYY-MM-DD`
- Maintain consistent spacing with existing entries
- Don't modify existing version entries

**Output:** `@CHANGELOG.md` with new version header added.

### Step 5: Add the Version and the Date

**Objective:** Ensure the version block has the correct version number and current date.

**Actions:**
1. Get the current date in YYYY-MM-DD format
   - Use system date/time information
   - Never assume or hardcode dates
   - Format: `YYYY-MM-DD` (e.g., `2026-01-25`)

2. Verify the version number matches Step 2 and Step 3
   - Version in changelog header must match `@package.json` version
   - Format: `[X.Y.Z]` where X, Y, Z are numbers

3. Update the version block header if needed:
   ```markdown
   ## [0.4.1] - 2026-01-25
   ```

**Date Format Rules:**
- Always use `YYYY-MM-DD` format
- Use 4-digit year
- Use 2-digit month (01-12)
- Use 2-digit day (01-31)
- Match the format of existing changelog entries

**Example:**
```markdown
## [1.2.4] - 2026-01-25
```

**Output:** Version block with correct version number and date.

### Step 6: Add the Changelog Data

**Objective:** Populate the version block with categorized change entries.

**Actions:**
1. Organize changes from Step 1 into appropriate sections
2. Use the standard Keep a Changelog sections:
   - `### Added` - New features
   - `### Changed` - Changes in existing functionality
   - `### Deprecated` - Soon-to-be removed features
   - `### Removed` - Removed features
   - `### Fixed` - Bug fixes
   - `### Security` - Security vulnerabilities

3. Format each entry:
   - Use bullet points with `- ` prefix
   - Start with a capital letter
   - End without a period (unless it's a full sentence)
   - Be concise and descriptive
   - Focus on user-facing changes

4. **Section Guidelines:**
   - **Added**: New features, new APIs, new components, new capabilities
   - **Changed**: Modified behavior, API changes (non-breaking), improvements
   - **Deprecated**: Features marked for removal in future versions
   - **Removed**: Features that were removed (usually indicates MAJOR bump)
   - **Fixed**: Bug fixes, corrections, patches
   - **Security**: Security-related fixes and improvements

5. Only include sections that have changes
6. Order sections: Added, Changed, Deprecated, Removed, Fixed, Security

**Example:**
```markdown
## [0.4.1] - 2026-01-25

### Added
- New changelog generator skill for cursor agents
- Support for semantic versioning automation

### Fixed
- Corrected version bump logic for patch releases
- Fixed date formatting in changelog entries

### Changed
- Improved changelog entry categorization
```

**Writing Guidelines:**
- Write from the user's perspective
- Use present tense ("Adds feature" not "Added feature")
- Be specific but concise
- Group related changes together
- Avoid technical jargon when possible
- Focus on what changed, not how it was implemented

**Output:** Complete version block with all categorized changes.

### Step 7: One Final Review

**Objective:** Verify everything is correct and consistent before completion.

**Checklist:**

1. **Version Consistency:**
   - [ ] Version in `@package.json` matches version in `@CHANGELOG.md` header
   - [ ] Version format is correct (X.Y.Z where X, Y, Z are numbers)

2. **Date Format:**
   - [ ] Date is in YYYY-MM-DD format
   - [ ] Date matches current date (not future or past)
   - [ ] Date format matches existing changelog entries

3. **Changelog Content:**
   - [ ] All staged changes are represented in the changelog
   - [ ] Changes are in the correct sections
   - [ ] No duplicate entries
   - [ ] Entries are clear and descriptive

4. **Formatting:**
   - [ ] Markdown formatting is correct
   - [ ] Version block is in the correct location (after `[Unreleased]`)
   - [ ] Proper spacing between sections
   - [ ] Consistent with existing changelog style

5. **Semantic Versioning:**
   - [ ] Version bump type matches change types (MAJOR/MINOR/PATCH)
   - [ ] Breaking changes → MAJOR bump
   - [ ] New features → MINOR bump
   - [ ] Bug fixes → PATCH bump

6. **File Integrity:**
   - [ ] `@package.json` is valid JSON
   - [ ] `@CHANGELOG.md` is valid markdown
   - [ ] No syntax errors
   - [ ] Files are properly formatted

**If any issues are found:**
- Fix them before completing
- Re-verify the checklist
- Ensure consistency across all files

**Output:** Verified and consistent changelog and version updates.

## File References

This skill references files using the `@` syntax convention:

- **`@package.json`**: The root `package.json` file in the repository
  - Contains the `version` field that needs updating
  - Located at the repository root

- **`@CHANGELOG.md`**: The changelog file following Keep a Changelog format
  - Contains version history and change documentation
  - Located at the repository root
  - Format: Markdown with version blocks

**Usage in skill:**
When the skill mentions `@package.json` or `@CHANGELOG.md`, it refers to these specific files at the repository root. Always read these files before making changes and verify their current state.

## Semantic Versioning Rules

Follow [Semantic Versioning 2.0.0](https://semver.org/) specification:

### Version Format: MAJOR.MINOR.PATCH

- **MAJOR version (X.0.0)**: Increment when you make incompatible API changes
  - Breaking changes to public APIs
  - Removed features or functionality
  - Changed behavior that breaks existing code
  - Example: `1.2.3` → `2.0.0`

- **MINOR version (0.X.0)**: Increment when you add functionality in a backward-compatible manner
  - New features added
  - New APIs (backward compatible)
  - Deprecated features (still functional)
  - Example: `1.2.3` → `1.3.0`

- **PATCH version (0.0.X)**: Increment when you make backward-compatible bug fixes
  - Bug fixes
  - Security patches
  - Performance improvements
  - Documentation updates (if versioned)
  - Example: `1.2.3` → `1.2.4`

### Pre-release and Build Metadata

- Pre-release versions: `1.0.0-alpha.1`, `1.0.0-beta.2`, `1.0.0-rc.1`
- Build metadata: `1.0.0+20130313144700`

For standard releases, use the three-part version number (X.Y.Z).

### Decision Priority

When multiple change types exist:
1. **Any breaking changes** → MAJOR bump
2. **Any new features** (without breaking changes) → MINOR bump
3. **Only bug fixes** → PATCH bump

## Keep a Changelog Format

Follow the [Keep a Changelog](https://keepachangelog.com/) format standards:

### Structure

```markdown
# Changelog

## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security vulnerabilities
```

### Section Guidelines

- **Added**: New features, capabilities, or functionality
- **Changed**: Modifications to existing functionality
- **Deprecated**: Features that will be removed in a future version
- **Removed**: Features that have been removed
- **Fixed**: Bug fixes and corrections
- **Security**: Security-related fixes and improvements

### Formatting Rules

- Use `##` for version headers: `## [X.Y.Z] - YYYY-MM-DD`
- Use `###` for change type sections: `### Added`
- Use `- ` for bullet points
- Date format: `YYYY-MM-DD`
- Only include sections that have changes
- Order: Added, Changed, Deprecated, Removed, Fixed, Security

### Best Practices

- Write from the user's perspective
- Be clear and concise
- Group related changes
- Use present tense
- Focus on what changed, not implementation details
- Keep `[Unreleased]` section for future changes

## Quick Reference

### Git Commands

```bash
# Check staging status
git status

# Review staged changes
git diff --cached

# View commit history
git log --oneline --cached
```

### Version Bump Examples

```bash
# Current: 1.2.3

# Breaking change → 2.0.0
# New feature → 1.3.0
# Bug fix → 1.2.4
```

### Changelog Entry Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Description of new feature

### Changed
- Description of change

### Fixed
- Description of fix
```

## Common Patterns

### Pattern: Feature Release
- Changes: New features, no breaking changes
- Version: MINOR bump (0.X.0)
- Sections: `### Added`, possibly `### Changed`

### Pattern: Bug Fix Release
- Changes: Only bug fixes
- Version: PATCH bump (0.0.X)
- Sections: `### Fixed`

### Pattern: Major Release
- Changes: Breaking changes
- Version: MAJOR bump (X.0.0)
- Sections: `### Removed`, `### Changed`, possibly `### Added`

### Pattern: Security Release
- Changes: Security fixes
- Version: PATCH bump (usually) or MAJOR (if breaking)
- Sections: `### Security`, `### Fixed`

## Troubleshooting

### Issue: Version mismatch between files
**Solution:** Ensure Step 3 and Step 4 use the same version number. Re-check both files.

### Issue: Can't determine version bump type
**Solution:** Review Step 1 changes carefully. Use priority: MAJOR > MINOR > PATCH.

### Issue: Changelog format doesn't match existing
**Solution:** Review existing `@CHANGELOG.md` entries and match their style exactly.

### Issue: Missing changes in changelog
**Solution:** Re-run Step 1 to ensure all staged changes are reviewed and categorized.

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Git Documentation](https://git-scm.com/doc)
