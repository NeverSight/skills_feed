---
name: version-bump
description: This skill automates version bumping during the release process for the Claude Code Handbook monorepo. It should be used when the user requests to bump versions, prepare a release, or increment version numbers across the repository.
---

# Version Bump Skill

Per-plugin version bumping for the Claude Code Handbook monorepo. Each plugin can have independent versions.

## When to Use This Skill

Trigger this skill when users mention:
- "bump version" or "bump the version"
- "increment version" or "update version numbers"
- Any mention of "major", "minor", or "patch" version changes

## Version Locations

Each plugin has versions in two places (kept in sync):
1. `.claude-plugin/marketplace.json` → plugin entry version
2. `plugins/<name>/.claude-plugin/plugin.json` → individual plugin version

The marketplace top-level `version` and `metadata.version` are schema versions and remain unchanged.

## Workflow Instructions

### Step 1: List Current Versions

Show current plugin versions:

```bash
python .claude/skills/version-bump/scripts/validate_versions.py
```

### Step 2: Ask User Which Plugin(s) to Bump

Ask the user:
1. Which plugin(s) to bump (can be multiple, or "all")
2. Which bump type: major, minor, or patch

### Step 3: Execute Version Bump

Run the script with the selected plugins:

```bash
# Single plugin
python .claude/skills/version-bump/scripts/bump_version.py <bump_type> --plugin <name>

# Multiple plugins
python .claude/skills/version-bump/scripts/bump_version.py <bump_type> --plugin <name1> --plugin <name2>

# All plugins
python .claude/skills/version-bump/scripts/bump_version.py <bump_type> --all
```

### Step 4: Report Results

After successful completion, display:
- Plugins bumped with old → new versions
- Next steps for git commit

## CLI Reference

```bash
# Show help
python .claude/skills/version-bump/scripts/bump_version.py --help

# Error + list plugins when no --plugin flag
python .claude/skills/version-bump/scripts/bump_version.py patch

# Bump specific plugin(s)
python .claude/skills/version-bump/scripts/bump_version.py patch --plugin handbook-dotnet
python .claude/skills/version-bump/scripts/bump_version.py minor --plugin handbook --plugin handbook-extras

# Bump all plugins (legacy monorepo behavior)
python .claude/skills/version-bump/scripts/bump_version.py patch --all
```

## Examples

### Example 1: Bump Single Plugin
```
User: "Bump the version for handbook-dotnet"
Claude: "I'll check current versions first..."

[Runs validate_versions.py]

Claude: "handbook-dotnet is currently at 1.19.5. What bump type: major, minor, or patch?"
User: "patch"

[Runs: python bump_version.py patch --plugin handbook-dotnet]

Claude: "Done!
  handbook-dotnet: 1.19.5 → 1.19.6

Next steps:
1. git diff
2. git add . && git commit -m 'chore: bump handbook-dotnet to 1.19.6'"
```

### Example 2: Bump Multiple Plugins
```
User: "Bump handbook and handbook-extras to a new minor version"

[Runs: python bump_version.py minor --plugin handbook --plugin handbook-extras]

Claude: "Done!
  handbook: 1.19.5 → 1.20.0
  handbook-extras: 1.19.5 → 1.20.0"
```

### Example 3: Bump All Plugins
```
User: "Bump all plugins patch version"

[Runs: python bump_version.py patch --all]

Claude: "Done! All 13 plugins bumped from their current versions."
```

## Notes

- The script does NOT create git commits - user handles version control
- Plugins can now have different versions (independent versioning)
- Changelog updates are manual - user maintains CHANGELOG.md as needed
