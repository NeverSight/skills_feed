---
name: publish-skill
description: Publish a skill to GitHub for discovery via `npx skills`. Use when asked to "publish skill", "share skill", "make skill discoverable", or "upload skill to GitHub".
---

# Publish Skill

Publish skills to GitHub so they're discoverable via `npx skills add <org>/<repo>`.

## How Skills Discovery Works

The `npx skills` CLI discovers skills from GitHub repositories with this structure:

```
<repo>/
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

Users install skills with: `npx skills add <org>/<repo>`

## Publishing Workflow

### 1. Gather Information

Use AskUserQuestion to collect:
- **Which skill to publish** - Path to the local skill directory (must contain SKILL.md)
- **GitHub org/user** - The GitHub organization or username to publish under
- **Repository name** - Name for the skills repository (e.g., "agent-skills", "my-skills")

### 2. Validate the Skill

Before publishing, verify:
- `SKILL.md` exists and has valid YAML frontmatter with `name` and `description`
- SKILL.md is under 200 lines (recommended)
- Any `references/`, `scripts/`, or `assets/` directories are included

### 3. Publish to GitHub

Use the GitHub CLI (`gh`) to publish:

```bash
# Check if repo exists
gh repo view <org>/<repo> 2>/dev/null

# If repo doesn't exist, create it
gh repo create <org>/<repo> --public --description "Agent skills collection"

# Clone the repo (or use existing clone)
gh repo clone <org>/<repo> /tmp/skills-publish-<repo>

# Create skills directory structure
mkdir -p /tmp/skills-publish-<repo>/skills/<skill-name>

# Copy skill files
cp -r <local-skill-path>/* /tmp/skills-publish-<repo>/skills/<skill-name>/

# Commit and push
cd /tmp/skills-publish-<repo>
git add .
git commit -m "Add <skill-name> skill"
git push origin main
```

### 4. Verify Publication

After publishing, verify the skill is discoverable:

```bash
npx skills add <org>/<repo> --list
```

## Example Session

```
Agent: Which skill would you like to publish?
User: ~/.claude/skills/my-awesome-skill

Agent: What GitHub org or username should this be published under?
User: my-github-org

Agent: What repository name? (e.g., "agent-skills")
User: my-skills

Agent: Publishing my-awesome-skill to my-github-org/my-skills...
[Creates repo if needed, copies skill, commits, pushes]

Agent: Done! Install with: npx skills add my-github-org/my-skills
```

## Notes

- Skills repos can contain multiple skills in the `skills/` directory
- The skill name in the directory should match the `name` in SKILL.md frontmatter
- Public repos are required for skills discovery
- Consider adding a README.md to the repo root describing your skills collection
