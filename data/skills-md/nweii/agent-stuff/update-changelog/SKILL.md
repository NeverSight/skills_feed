---
name: update-changelog
description: "Update changelog files following Keep a Changelog conventions. Use for project changelogs or skill changelogs. Handles version sections, change type groupings, and skill-specific metadata updates."
metadata:
  author: nweii
  version: "1.0.0"
---

# Update Changelog

Update changelog files following [Keep a Changelog](https://keepachangelog.com) conventions.

## Usage

```
/update-changelog <version> <change_type> <message>
/update-changelog <skill_path> <version> <change_type> <message>
```

## Parameters

- `<version>`: Version number (e.g., "1.1.0")
- `<change_type>`: One of: "added", "changed", "deprecated", "removed", "fixed", "security"
- `<message>`: Description of the change
- `<skill_path>` (optional): Path to skill folder for skill changelogs

## Process

1. Check for existing changelog (CHANGELOG.md or changelog.md), create if missing
2. Find or create section for the specified version with today's date
3. Add the new entry under the appropriate change type heading
4. Format according to Keep a Changelog conventions
5. Write the updated changelog back to file

## Format Conventions

- Group changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
- List changes as bullet points
- Include date for version sections (YYYY-MM-DD)
- Keep entries concise but descriptive
- No emojis

## Example Output

```markdown
## [1.2.0] - 2025-01-24

### Added
- New markdown to BlockDoc conversion feature

### Fixed
- Bug in HTML renderer causing incorrect output
```

---

## Skill & Plugin Changelogs

For skill-specific conventions (updating `metadata.version` in SKILL.md) or plugin changelog formats, see [skill-plugin-conventions.md](skill-plugin-conventions.md).
