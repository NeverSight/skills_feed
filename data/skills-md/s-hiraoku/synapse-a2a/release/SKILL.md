---
name: release
description: Update version in pyproject.toml, plugin.json, and add changelog entry. This skill should be used when the user wants to bump the version number and update CHANGELOG.md. Triggered by /release or /version commands.
---

# Release Version Update

This skill updates the project version, plugin version, and changelog.

## Usage

```
/release <version-type-or-number> [description]
```

### Version Types

- `patch` - Increment patch version (e.g., 0.2.12 → 0.2.13)
- `minor` - Increment minor version (e.g., 0.2.12 → 0.3.0)
- `major` - Increment major version (e.g., 0.2.12 → 1.0.0)
- `X.Y.Z` - Set specific version (e.g., 1.0.0)

### Description (Optional)

If provided, use as the changelog entry description. Otherwise, analyze recent commits to generate the changelog.

## Workflow

### Step 1: Read Current Version

Read `pyproject.toml` and extract current version:

```python
# Look for: version = "X.Y.Z"
```

### Step 2: Calculate New Version

Based on the version type:

- **patch**: `major.minor.patch` → `major.minor.(patch+1)`
- **minor**: `major.minor.patch` → `major.(minor+1).0`
- **major**: `major.minor.patch` → `(major+1).0.0`
- **specific**: Use the provided version directly

Validate the new version is greater than current (unless forced).

### Step 3: Update pyproject.toml

Edit `pyproject.toml`:

```toml
version = "NEW_VERSION"
```

### Step 3.5: Update plugin.json

Edit `plugins/synapse-a2a/.claude-plugin/plugin.json`:

```json
"version": "NEW_VERSION",
```

**Important:** Keep plugin version in sync with pyproject.toml version.

### Step 4: Analyze Changes for Changelog

If no description provided, analyze recent changes:

```bash
git log --oneline HEAD~10..HEAD
git diff HEAD~10..HEAD --stat
```

Categorize changes into:
- **Added** - New features
- **Changed** - Modifications to existing features
- **Fixed** - Bug fixes
- **Removed** - Removed features
- **Documentation** - Doc updates
- **Tests** - Test additions/changes

### Step 5: Update CHANGELOG.md

Add new entry at the top (after the header):

```markdown
## [NEW_VERSION] - YYYY-MM-DD

### Added
- Feature description

### Changed
- Change description

### Fixed
- Fix description
```

Use today's date in YYYY-MM-DD format.

### Step 6: Report Results

Display:
- Old version → New version
- Changelog entry preview
- Files modified

## Examples

### Bump patch version
```
/release patch
```

### Bump minor version with description
```
/release minor "Add new authentication system"
```

### Bump major version
```
/release major
```

### Set specific version
```
/release 1.0.0
```

### Shorthand
```
/version patch    # Same as /release patch
```

## File Locations

- Version: `pyproject.toml` (line with `version = "..."`)
- Plugin Version: `plugins/synapse-a2a/.claude-plugin/plugin.json` (line with `"version": "..."`)
- Changelog: `CHANGELOG.md`

## Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Fixed
- Bug fixes

### Removed
- Removed features

### Documentation
- Documentation updates

### Tests
- Test updates
```

Only include sections that have entries. Order sections as shown above.
