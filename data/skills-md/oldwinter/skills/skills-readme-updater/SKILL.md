---
name: skills-readme-updater
description: This skill should be used after creating or modifying skills to update the main README.md file. It scans all skills in ~/.claude/skills/, extracts metadata from SKILL.md files, and regenerates the README with categorized skill listings. Triggers on requests mentioning "update skills readme", "refresh skills list", or after adding new skills.
---

# Skills README Updater

Automatically scan and update the skills README.md when skills are added, modified, or removed.

## Usage

After adding or modifying a skill, run the update script:

```bash
python3 ~/.claude/skills/skills-readme-updater/scripts/update_readme.py
```

The script will:
1. Scan all subdirectories in `~/.claude/skills/`
2. Parse YAML frontmatter from each `SKILL.md`
3. Categorize skills based on predefined categories
4. Generate an updated `README.md` with:
   - Categorized skill tables
   - Directory structure
   - Usage instructions
   - Timestamp

## Categories

Skills are organized into these categories:

| Category | Skills |
|----------|--------|
| 云基础设施 | aws-cli, aws-cost-explorer, eksctl |
| Kubernetes & GitOps | kubectl, argocd-cli, kargo-cli, sync-to-prod |
| 代码仓库 | github-cli, gitlab-cli, changelog-generator |
| 开发工具 | justfile, skill-creator, skills-readme-updater |
| 内容处理 | humanizer-zh, obsidian-dashboard |

To add a new category or reassign skills, edit the `CATEGORIES` dict in `scripts/update_readme.py`.

## Workflow: Adding a New Skill

1. Create the skill using `skill-creator`
2. Edit `SKILL.md` with proper metadata
3. Run the README updater:
   ```bash
   python3 ~/.claude/skills/skills-readme-updater/scripts/update_readme.py
   ```
4. Verify the README was updated correctly
