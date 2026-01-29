---
name: skill-manager
description: Manage your installed Claude Code skills - install, update, rename, uninstall, and list skills from GitHub URLs. Use when the user wants to install a skill, update a skill, list installed skills, rename a skill, remove/delete/uninstall a skill, or provides a GitHub URL to a skills directory.
---

# Skill Manager

Manage Claude Code skills from GitHub - install, update, rename, uninstall, and list with version tracking.

## Scripts

| Script | Purpose |
|--------|---------|
| `install-skill.sh` | Install a skill from GitHub URL |
| `update-skill.sh` | Update an installed skill from upstream |
| `update-all-skills.sh` | Update all managed skills at once |
| `list-skills.sh` | List all installed skills |
| `uninstall-skill.sh` | Remove an installed skill |
| `rename-skill.sh` | Rename an installed skill |
| `skill-accept.sh` | Accept pending update changes |
| `skill-reject.sh` | Reject pending update changes |

## Quick start

```bash
# Install a skill
~/.claude/skills/skill-manager/scripts/install-skill.sh "<github-url>"

# List installed skills
~/.claude/skills/skill-manager/scripts/list-skills.sh

# Update a skill
~/.claude/skills/skill-manager/scripts/update-skill.sh <skill-name>

# Update all managed skills
~/.claude/skills/skill-manager/scripts/update-all-skills.sh
```

## Instructions for Claude

### When user provides a GitHub URL to install

1. Run the install script:
   ```bash
   ~/.claude/skills/skill-manager/scripts/install-skill.sh "<github-url>"
   ```
2. If user wants a custom name, add `--target <name>`
3. If conflict occurs, ask user: overwrite (`--force`) or rename (`--target`)?
4. Tell user to restart Claude Code to load the new skill

### When user asks to update a skill

1. Run update:
   ```bash
   ~/.claude/skills/skill-manager/scripts/update-skill.sh <skill-name>
   ```
2. If changes detected, show the diff summary to user
3. Ask user to accept or reject
4. Run the appropriate script:
   ```bash
   ~/.claude/skills/skill-manager/scripts/skill-accept.sh <skill-name>   # if accept
   ~/.claude/skills/skill-manager/scripts/skill-reject.sh <skill-name>  # if reject
   ```

### When user asks to list/show installed skills

```bash
~/.claude/skills/skill-manager/scripts/list-skills.sh
```

### When user asks to update all skills

```bash
~/.claude/skills/skill-manager/scripts/update-all-skills.sh
```

This script will:
1. Check all managed skills for updates from their upstream sources
2. Skip any skills with uncommitted local changes (reports them in summary)
3. Report which skills have updates available (with pending changes to review)
4. Report which skills are already up to date
5. List any unmanaged skills that were skipped

If any skills have pending changes, ask the user if they want to accept or reject each one.

If any skills were skipped due to local changes, tell the user they need to commit or discard their changes first, then run update again.

### When user asks to uninstall/remove a skill

```bash
~/.claude/skills/skill-manager/scripts/uninstall-skill.sh <skill-name>
```

### When user asks to rename a skill

```bash
~/.claude/skills/skill-manager/scripts/rename-skill.sh <current-name> <new-name>
```

### Conflict handling

- **Same source exists**: Treated as update, show changes
- **Different source exists**: Ask user to `--force` (overwrite) or `--target <new-name>` (install alongside)
- **Unmanaged skill exists**: Ask user to `--force` to take over management
- **Local changes exist**: Script prompts for confirmation before overwriting (or use `--force` to skip prompt)

## Examples

Install from claude-code repo:
```bash
~/.claude/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills/hook-development"
```

Install with custom name:
```bash
~/.claude/skills/skill-manager/scripts/install-skill.sh "https://github.com/metabase/metabase/tree/master/.claude/skills/clojure-write" --target metabase-clojure
```

Force overwrite:
```bash
~/.claude/skills/skill-manager/scripts/install-skill.sh "<url>" --force
```

## Metadata file

Each installed skill has `.skill-manager.json`:
```json
{
  "source_url": "https://github.com/owner/repo/tree/branch/path",
  "owner": "owner",
  "repo": "repo",
  "branch": "branch",
  "path": "path/to/skill"
}
```

## Version tracking

- Each skill is a local git repository
- Initial install creates first commit
- Updates stage changes for review before committing
- Full git history of all changes

## Requirements

- `curl` - for downloading files
- `jq` - for parsing JSON
- `git` - for version tracking

## Troubleshooting

**API rate limit**: GitHub allows 60 requests/hour unauthenticated. Wait or use authenticated requests.

**Conflict detected**: Use `--force` to overwrite or `--target` for different name.

**No changes detected**: Skill is already up to date with upstream.

**Pending changes**: Run `skill-accept.sh` or `skill-reject.sh` to resolve.

**Local changes detected**: The skill has uncommitted modifications. Either commit them (`git add . && git commit -m "Local changes"`) or discard them (`git checkout .`) before updating.
