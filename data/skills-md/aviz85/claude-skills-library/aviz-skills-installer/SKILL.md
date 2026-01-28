---
name: aviz-skills-installer
description: Install skills from the AVIZ Skills Library. Use when user wants to install a skill, browse available skills, set up Claude Code skills, or asks about skill installation. Triggers on "install skill", "add skill", "setup skill", "available skills", "skill library", "browse skills".
version: "1.0.0"
author: aviz85
tags:
  - installer
  - setup
  - claude-code
---

# AVIZ Skills Installer

A conversational guide to installing skills from the AVIZ Skills Library.

## Important: Fetch Real-Time Data

**DO NOT use hardcoded skill lists.** Always fetch current data from these sources:

1. **Skills List & Setup Guides**: https://aviz.github.io/claude-skills-library/
2. **GitHub Repository**: https://github.com/aviz85/claude-skills-library
3. **Individual Skill Pages**: https://aviz.github.io/claude-skills-library/skills/{skill-name}.html

Use WebFetch or WebSearch to get the latest available skills and their setup instructions.

## Conversational Flow

### Step 1: Discover Intent
Ask the user what they want:
- See available skills → Fetch from site
- Install a specific skill → Proceed to installation
- Learn about a skill → Fetch its documentation page

### Step 2: Fetch Available Skills
Use WebFetch on https://aviz.github.io/claude-skills-library/ to get the current list of skills.

### Step 3: Choose Installation Scope
Ask the user:
```
Where would you like to install this skill?
1. User-based (~/.claude/skills/) - Personal, available everywhere
2. Project-based (.claude/skills/) - Shared with team via git
```

### Step 4: Install the Skill
```bash
# Clone and copy
TEMP=$(mktemp -d)
git clone https://github.com/aviz85/claude-skills-library.git "$TEMP/lib" --depth 1

# For user-based:
mkdir -p ~/.claude/skills
cp -r "$TEMP/lib/skills/SKILL_NAME" ~/.claude/skills/

# For project-based:
mkdir -p .claude/skills
cp -r "$TEMP/lib/skills/SKILL_NAME" .claude/skills/

# Cleanup
rm -rf "$TEMP"
```

### Step 5: Install Dependencies (if needed)
```bash
cd DESTINATION/SKILL_NAME/scripts
npm install 2>/dev/null || true
```

### Step 6: Provide Setup Guide
Fetch the skill's documentation page and guide the user through any required configuration:
```
https://aviz.github.io/claude-skills-library/skills/{skill-name}.html
```

## Conventions for Skill Documentation

Each skill in the library MUST have:
1. **SKILL.md** - Main skill file with YAML frontmatter
2. **Setup page on GitHub Pages** - At `docs/skills/{skill-name}.html`

Skills requiring API keys should include:
- `.env.example` file with required variables
- Setup instructions on their documentation page

## See Also

- Library Website: https://aviz.github.io/claude-skills-library/
- GitHub Repository: https://github.com/aviz85/claude-skills-library
