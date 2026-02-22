---
name: find-skills
description: Search and discover Claude Code skills from the community. Helps users find, evaluate, and install skills from GitHub repositories and the skills registry.
source: https://github.com/vercel-labs/skills
---

# Find Skills

Search and discover Claude Code skills from the community.

## How to Search for Skills

### Using npx skills CLI

```bash
# Search for skills by keyword
npx skills search <keyword>

# Browse popular skills
npx skills search --sort=popular

# Search by category
npx skills search --category=<category>
```

### Categories

- **architecture** - System design, patterns, decision frameworks
- **debugging** - Bug investigation, root cause analysis
- **testing** - Test strategies, TDD, coverage
- **frontend** - UI/UX, React, Vue, CSS
- **backend** - APIs, databases, servers
- **devops** - CI/CD, Docker, Kubernetes
- **security** - Auth, encryption, vulnerability scanning
- **productivity** - Workflow automation, code generation

## How to Install Skills

```bash
# Install from GitHub repository
npx skills add https://github.com/<owner>/<repo> --skill <skill-name>

# Install from registry
npx skills add <skill-name>

# List installed skills
npx skills list

# Remove a skill
npx skills remove <skill-name>
```

## How to Create Skills

### Skill Structure

```
skills/
└── my-skill/
    ├── SKILL.md          # Main skill file (required)
    ├── references/       # Reference documentation
    │   └── guide.md
    └── scripts/          # Automation scripts
        └── tool.py
```

### SKILL.md Format

```markdown
---
name: my-skill
description: Brief description of what the skill does
allowed-tools: Read, Glob, Grep  # Optional: restrict tool access
---

# Skill Name

## When to Use
Describe when this skill should be activated.

## Instructions
Step-by-step instructions for the AI assistant.

## Examples
Show example inputs and expected outputs.
```

### Publishing

```bash
# Validate skill structure
npx skills validate

# Publish to registry
npx skills publish
```

## Evaluating Skills

When choosing skills, consider:

1. **Relevance** - Does it solve your specific problem?
2. **Quality** - Is the SKILL.md well-written with clear instructions?
3. **Maintenance** - Is the repository actively maintained?
4. **Compatibility** - Does it work with your tech stack?
5. **Reviews** - What do other users say?

## Useful Repositories

- [vercel-labs/skills](https://github.com/vercel-labs/skills) - Official skills registry
- [anthropics/claude-code](https://github.com/anthropics/claude-code) - Claude Code documentation
