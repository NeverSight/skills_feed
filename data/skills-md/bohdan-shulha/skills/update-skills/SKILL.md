---
name: update-skills
description: >-
  Update skills in ~/Projects/skills. Use when learning new patterns, fixing documentation, or adding new skills.
---

# Update Skills

Skills repo location: `~/Projects/skills`

## Workflow

1. Identify what needs updating (new skill, fix, or enhancement)
2. Edit or create files in the appropriate skill directory
3. Commit and push changes

## Creating a New Skill

```bash
mkdir -p ~/Projects/skills/<skill-name>
```

Create `skill.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: >-
  One-line description of when to use this skill.
---

# Skill Title

Content here.
```

## Committing Changes

```bash
cd ~/Projects/skills
git add -A
git commit -m "docs: description of change

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

## Existing Skills

Check current skills:

```bash
ls ~/Projects/skills/
```
