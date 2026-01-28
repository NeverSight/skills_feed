---
name: skill-create
description: Instructions for AI agents to create new skills and add them to the skills repository
---

# Purpose

This skill instructs AI agents on how to create new skills and add them to the shared `skills` repository at `https://github.com/sourman/skills`.

# Repository Location

The skills repository is located at:
- **Remote:** `https://github.com/sourman/skills`
- **Local working copy:** `/tmp/skills` (or `~/skills` in some environments)

# Skill Structure

Each skill is a directory at the repository root containing a `SKILL.md` file:

```
skills/
├── skill-name-1/
│   └── SKILL.md
├── skill-name-2/
│   └── SKILL.md
└── README.md
```

The `SKILL.md` file must have:
1. **YAML frontmatter** with `name` and `description`
2. **Markdown content** with instructions for the AI agent

# Creating a New Skill

## Step 1: Navigate to the Repository

```bash
cd /tmp/skills
# OR if it doesn't exist:
git clone git@github.com:sourman/skills.git /tmp/skills
cd /tmp/skills
```

## Step 2: Create the Skill Directory

```bash
mkdir <skill-name>
```

Use **kebab-case** for skill names (e.g., `react-best-practices`, `typescript-eslint`, `docker-workflow`).

## Step 3: Create the SKILL.md File

Create `<skill-name>/SKILL.md` with the following structure:

```markdown
---
name: skill-name
description: Brief one-line description of what this skill teaches the AI agent
---

# Skill Title

A clear, concise description of what this skill covers.

## What This Skill Covers

- Topic area 1
- Topic area 2
- Topic area 3

## Key Commands

```bash
# Example commands relevant to this skill
command --option value
```

## Detailed Instructions

Provide detailed instructions, best practices, and workflows here.

## When to Use This Skill

Use this skill when:
- Condition 1
- Condition 2
```

**Frontmatter Requirements:**
- `name`: Must match the directory name (kebab-case)
- `description`: One-line summary for the skills directory

## Step 4: Add and Commit to Git

```bash
# Ensure you're on the master branch
git checkout master

# Add the new skill
git add <skill-name>/

# Commit with a descriptive message
git commit -m "Add <skill-name> skill"

# If the master branch doesn't exist, you might be on main:
git checkout main
```

## Step 5: Push to GitHub

```bash
# Push the changes
git push origin master
# OR if on main:
git push origin main
```

# Example: Creating a New Skill

Here's a complete example of creating a skill called `git-workflow`:

```bash
# 1. Navigate to repo
cd /tmp/skills

# 2. Create directory
mkdir git-workflow

# 3. Create SKILL.md
cat > git-workflow/SKILL.md << 'EOF'
---
name: git-workflow
description: Git best practices, branching strategies, and commit conventions
---

# Git Workflow

This skill covers Git best practices for collaborative development.

## Branch Naming

Use descriptive branch names:
- `feature/add-user-authentication`
- `fix/login-page-bug`
- `refactor/database-connection`

## Commit Messages

Follow conventional commits:
- `feat: add user authentication`
- `fix: resolve login redirect issue`
- `docs: update API documentation`
EOF

# 4. Commit
git add git-workflow/
git commit -m "Add git-workflow skill"

# 5. Push
git push origin master
```

# Updating an Existing Skill

To update an existing skill:

```bash
cd /tmp/skills

# Edit the skill file
vim <skill-name>/SKILL.md

# Commit and push
git add <skill-name>/SKILL.md
git commit -m "Update <skill-name> skill: describe changes"
git push origin master
```

# Verifying the Skill

After pushing, verify the skill is accessible:

1. Check GitHub: https://github.com/sourman/skills/tree/main/<skill-name>
2. Test installation in another project:
   ```bash
   bun x skills add sourman/skills/<skill-name>
   ```

# Important Notes

1. **Always use kebab-case** for skill directory names
2. **Frontmatter `name` must match** the directory name
3. **Write clear descriptions** - this is what agents see when listing skills
4. **Test your skill** by installing it in a different project
5. **Keep skills focused** - each skill should cover a specific domain or technology

# Troubleshooting

## Git Push Fails

If push fails with "remote does not support password authentication":
```bash
# Ensure SSH is set up correctly
ssh -T git@github.com
```

## Branch Name Issues

If you're not sure which branch you're on:
```bash
git branch
# Use 'main' or 'master' accordingly
```

## Permission Denied

If you can't push:
1. Verify you have push access to sourman/skills
2. Check that you're authenticated as the correct user: `gh auth status`
