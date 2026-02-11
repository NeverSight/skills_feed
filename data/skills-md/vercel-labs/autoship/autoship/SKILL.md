---
name: autoship
description: CLI tool for automated changeset-based releases with AI-generated descriptions. Use when the user needs to release a package, create changesets, bump versions, or automate npm publishing workflows. Triggers include requests to "release a package", "create a changeset", "publish to npm", "bump the version", "automate releases", or any task involving version management and package publishing for repositories using the changesets workflow.
allowed-tools: Bash(autoship:*), Bash(npx autoship:*)
---

# Automated Releases with autoship

## Core Workflow

Every release follows this pattern:

1. **Configure**: `autoship add <name>` (one-time setup)
2. **Release**: `autoship <name>` (interactive) or `autoship <name> -t patch -y` (automated)

The tool handles the complete release cycle:
- Clone repository
- Analyze changes and suggest release type (patch/minor/major)
- Generate AI-powered changeset description
- Create and merge changeset PR
- Wait for and merge Version Packages PR
- Trigger npm publish

## Requirements

Before using autoship, ensure:

```bash
# GitHub CLI must be authenticated
gh auth login

# API key for AI features
export AI_GATEWAY_API_KEY="your-key"
```

## Essential Commands

```bash
# One-time setup: add a repository
autoship add myproject
# Prompts for: owner, repo name, base branch

# List configured repositories
autoship list

# Interactive release (prompts for type and message)
autoship myproject

# Automated release (no prompts)
autoship myproject -t patch -y
autoship myproject -t minor -y
autoship myproject -t major -y

# Release with custom message (skips AI generation)
autoship myproject -t patch -m "Fixed login bug" -y
```

## Command Options

```bash
autoship [repo]                    # Interactive repo selection if omitted
  -t, --type <type>                # Release type: patch, minor, major
  -m, --message <message>          # Custom changeset description
  -y, --yes                        # Skip all confirmations
  -h, --help                       # Show help
```

## Common Patterns

### Fully Automated Patch Release

```bash
autoship myproject -t patch -y
```

### AI-Assisted Interactive Release

```bash
autoship myproject
# 1. AI analyzes commits since last release
# 2. AI suggests release type (patch/minor/major)
# 3. You confirm or change the type
# 4. AI generates changeset description
# 5. You review and approve
# 6. Tool handles PR creation and merging
```

### Custom Message Release

```bash
autoship myproject -t minor -m "Added new authentication providers" -y
```

### CI/CD Integration

```bash
# In GitHub Actions or CI pipeline
export AI_GATEWAY_API_KEY="${{ secrets.AI_GATEWAY_API_KEY }}"
npx autoship myproject -t patch -y
```

## What autoship Does (10 Steps)

1. **Clone** - Clones the repository from the base branch
2. **Analyze** - Finds latest version tag, analyzes commits and diff
3. **Suggest** - AI suggests release type based on changes
4. **Generate** - AI generates changeset description
5. **Branch** - Creates release branch with changeset file
6. **PR** - Creates pull request for the changeset
7. **Wait** - Waits for CI checks to pass
8. **Merge** - Merges the changeset PR
9. **Version PR** - Waits for changesets action to create Version Packages PR
10. **Publish** - Merges Version Packages PR to trigger npm publish

## Output Format

autoship provides clear step-by-step output:

```
[1/10] Cloning repository from main...
  > Repository cloned
  > Package: my-package @ 1.2.3

[2/10] Creating release branch...
  > Branch created: release/patch-1706123456789

[3/10] Generating changeset...
  > Changeset created: fluffy-pants-dance.md

...

Release Complete!
The patch release has been published.
```

## Configuration

Config is stored at `~/.autoship/config.json`:

```json
{
  "repos": {
    "myproject": {
      "owner": "vercel-labs",
      "repo": "myproject",
      "baseBranch": "main",
      "cloneUrl": "https://github.com/vercel-labs/myproject.git"
    }
  }
}
```

## Deep-Dive Documentation

| Reference | When to Use |
|-----------|-------------|
| [references/commands.md](references/commands.md) | Full command reference with all options |
| [references/configuration.md](references/configuration.md) | Config file format and repository setup |
| [references/ci-integration.md](references/ci-integration.md) | GitHub Actions and CI/CD setup |

## Ready-to-Use Templates

| Template | Description |
|----------|-------------|
| [templates/automated-release.sh](templates/automated-release.sh) | Fully automated release script |
| [templates/setup-repo.sh](templates/setup-repo.sh) | Non-interactive repository setup |

```bash
./templates/automated-release.sh myproject patch
./templates/setup-repo.sh myproject vercel-labs myproject main
```

## Troubleshooting

### "No repositories configured"

Run `autoship add <name>` to configure a repository first.

### "Repository not found"

Check `autoship list` for available repos. The name is case-sensitive.

### CI checks failing

The tool will show which checks failed. Fix the issues in the target repository, then retry.

### AI generation failed

If AI fails, autoship falls back to manual input. Ensure `AI_GATEWAY_API_KEY` is set.
