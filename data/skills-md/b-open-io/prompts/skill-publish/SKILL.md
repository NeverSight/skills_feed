---
name: skill-publish
description: This skill should be used when the user asks to "publish a plugin", "release a plugin", "bump plugin version", "update a Claude Code plugin", "publish skills", or mentions plugin publishing, plugin release, or skill distribution. Handles version bumping, changelog updates, git workflow, and publishing for both Claude Code plugins and standalone Agent Skills.
metadata:
  author: b-open-io
  version: "1.0.0"
---

# Skill Publish

Publish Claude Code plugins and standalone Agent Skills with proper versioning, changelog management, and git workflow.

## Determine Publish Type

Before starting, identify the publish type based on project structure:

| Indicator | Type |
|-----------|------|
| `.claude-plugin/plugin.json` exists | **Claude Code Plugin** |
| Standalone `SKILL.md` with no plugin manifest | **Standalone Agent Skill** |

Claude Code plugins publish by pushing to GitHub — the marketplace picks up the latest commit on the default branch automatically. No registry upload or OTP is needed.

Standalone Agent Skills follow the agentskills.io specification and distribute as directories containing `SKILL.md`.

## Claude Code Plugin Workflow

### 1. Check Current State

```bash
# Read current version from manifest
cat .claude-plugin/plugin.json | grep '"version"'

# Check git is clean and up to date
git fetch origin && git status

# Review commits since last version bump
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~10)..HEAD
```

### 2. Bump Version in plugin.json

Edit `.claude-plugin/plugin.json` to increment the version field. For early-stage plugins (0.x.x or 1.0.x), bump the patch version unless the user requests otherwise:

```
0.1.6 → 0.1.7
1.0.23 → 1.0.24
```

### 3. Update CHANGELOG.md

If a changelog exists, add an entry following the existing format:

```markdown
## [X.X.X] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes
```

Summarize commits since the last release into appropriate categories.

### 4. Validate Plugin Structure

Before publishing, verify the plugin is well-formed:

- `.claude-plugin/plugin.json` has required `name` field
- Component directories (commands/, agents/, skills/, hooks/) contain valid files
- Skills have `SKILL.md` with valid YAML frontmatter (name + description)
- Agents and commands have `.md` files with YAML frontmatter
- Referenced files and scripts exist

### 5. Commit and Push

**Critical: Pushing to the default branch IS publishing.** The Claude Code plugin marketplace automatically picks up the latest commit.

```bash
git add .claude-plugin/plugin.json CHANGELOG.md
# Also stage any changed skill/agent/command files
git add -A
git commit -m "Release vX.X.X"
git push origin <default-branch>
```

### 6. Verify Publication

After pushing, verify the plugin update is available:

```bash
CLAUDECODE= claude plugin update <plugin-name>@<publisher>
```

The `CLAUDECODE=` prefix is required to avoid nested session errors when running from within Claude Code.

**Note:** The marketplace may take a few minutes to reflect the new version.

### 7. Update Downstream References

If the plugin version is tracked elsewhere (e.g., a marketplace page, documentation, or `lib/plugins.ts`), update those references to match the new version.

## Standalone Agent Skill Workflow

For skills not bundled in a Claude Code plugin, follow the agentskills.io specification.

### 1. Validate SKILL.md

Verify frontmatter meets the spec. For details, consult `references/agentskills-spec.md`.

Required fields:
- `name`: 1-64 chars, lowercase alphanumeric + hyphens, must match directory name
- `description`: 1-1024 chars, describes what and when

Optional fields:
- `license`, `compatibility`, `metadata`, `allowed-tools`

### 2. Validate Structure

```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional executables
├── references/       # Optional docs loaded on demand
└── assets/           # Optional static resources
```

### 3. Version via Metadata

Track version in the frontmatter `metadata` field:

```yaml
metadata:
  author: org-name
  version: "1.1.0"
```

### 4. Distribute

Standalone skills distribute as directories. Common methods:
- Git repository (push to GitHub)
- Archive (zip the skill directory)
- Package registry (if applicable)

## Common Issues

### Plugin Not Updating

If `claude plugin update` does not pick up changes:
- Verify the push landed on the default branch (usually `main` or `master`)
- Check that `.claude-plugin/plugin.json` is valid JSON
- Wait a few minutes for marketplace propagation

### Version Already Exists

If the version string was already used in a previous commit, bump again to the next patch before pushing.

### Nested Session Error

Always prefix CLI commands with `CLAUDECODE=` when running from within an active Claude Code session to avoid the "nested session" error.

## Additional Resources

### Reference Files

- **`references/agentskills-spec.md`** — Complete agentskills.io specification summary for standalone skills
