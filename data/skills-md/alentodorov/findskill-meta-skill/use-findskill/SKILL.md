---
name: use-findskill
description: A meta skill that teaches AI agents how to discover, install, and use skills from the findskill.md ecosystem. Use when you need to extend capabilities by finding specialized skills, when a user asks to perform tasks that would benefit from specialized skills, or when explicitly asked to find or install skills.
compatibility: Requires Node.js and npm. Designed for Claude Code or similar products.
---

# Use Findskill

A meta skill that teaches AI agents how to discover, install, and use skills from the findskill.md ecosystem.

## Description

This skill enables you to extend your capabilities by finding and installing specialized skills from the findskill.md registry. When a user asks you to do something you don't have a skill for, or when you need specialized functionality, use findskill to discover and install relevant skills.

## When to Use Findskill

Use findskill when:
- A user asks you to perform a task that would benefit from a specialized skill
- You need domain-specific knowledge or workflows (git commits, code review, documentation, etc.)
- The user explicitly asks you to find or install a skill
- You want to check if there's a better way to accomplish a common task

## Running Findskill

You have two options to run findskill commands:

### Option 1: Use npx (no installation required)
Run commands directly without installing:
```bash
npx findskill <command>
```

### Option 2: Install globally
Install once, then run without npx prefix:
```bash
npm install -g findskill
findskill <command>
```

## Available Commands

All examples below use `npx findskill`. If you installed globally, omit the `npx` prefix.

### Search for Skills
Find skills by name, description, or tags:
```bash
npx findskill search <query>
```

Example:
```bash
npx findskill search "git commit"
npx findskill search "documentation"
npx findskill search "review"
```

### Get Skill Information
View detailed information about a specific skill before installing:
```bash
npx findskill info <skill-name>
```

This shows the author, description, tags, star count, and installation instructions.

### Install a Skill
Install a skill to make it available for use:
```bash
npx findskill install <skill-name>
```

Skills are installed to `~/.claude/skills/` by default. Each skill contains a SKILL.md file with instructions you should read and follow.

### List Installed Skills
See what skills are already available:
```bash
npx findskill list
```

### Update Skills
Update installed skills to their latest versions:
```bash
npx findskill update           # Update all skills
npx findskill update <name>    # Update specific skill
```

## Workflow for Agents

1. **Assess the task**: Determine if a specialized skill would help accomplish the user's goal more effectively.

2. **Search for relevant skills**:
   ```bash
   npx findskill search "<relevant keywords>"
   ```

3. **Review skill details**: Before installing, check what the skill does:
   ```bash
   npx findskill info <skill-name>
   ```

4. **Install if appropriate**: If the skill matches the user's needs:
   ```bash
   npx findskill install <skill-name>
   ```

5. **Read the installed skill**: After installation, read the SKILL.md to understand how to use it:
   ```bash
   cat ~/.claude/skills/<skill-name>/SKILL.md
   ```

6. **Apply the skill**: Follow the instructions in the skill's SKILL.md to complete the user's task.

## Best Practices

- **Check installed skills first**: Run `npx findskill list` before searching to see what's already available.
- **Read before using**: Always read a skill's SKILL.md after installing to understand its capabilities and proper usage.
- **Match skills to tasks**: Don't install skills unnecessarily. Only install when there's a clear benefit for the current task.
- **Inform the user**: Let the user know when you're installing a new skill and why it will help with their request.

## Example Interaction

User: "Help me write a good git commit message for my changes"

Agent thought process:
1. This is a common task that likely has a specialized skill
2. Search for relevant skills: `npx findskill search "commit"`
3. Found "commit" skill - check details: `npx findskill info commit`
4. Install it: `npx findskill install commit`
5. Read the skill instructions: `cat ~/.claude/skills/commit/SKILL.md`
6. Follow the skill's workflow to help the user craft a proper commit message

## Environment Variables

- `FINDSKILL_DIR`: Custom installation directory (default: `~/.claude/skills/`)
- `FINDSKILL_API`: Custom API endpoint (for self-hosted registries)

## Tags

skills, meta, findskill, discovery, installation, package-manager, claude-skills
