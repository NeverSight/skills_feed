---
name: agent-auditor
description: Audit all agents in a project. Lists built-in and project agents, their skill dependencies, and validates skill references exist.
---

# Agent Auditor

Audit all agents in a project, listing their configurations and skill dependencies.

## Instructions

When this skill is invoked, perform the following audit:

### Step 1: Find Project Agents

Search for project-specific agents:

```
Glob: .claude/agents/*.md
```

### Step 2: Parse Each Agent File

For each agent file found, extract from the YAML frontmatter:
- `name` - Agent name
- `description` - What the agent does
- `tools` - Tools available to the agent
- `disallowedTools` - Tools the agent cannot use
- `skills` - Skills preloaded via frontmatter (always loaded when agent starts)
- `model` - Model override if specified

### Step 3: Find Manual Skill References

Search each agent's body (after frontmatter) for patterns that indicate skills loaded by context:
- `/skill <name>` or `load the <name> skill`
- References to "use the X skill" or "load X skill"

These are skills the agent may load during execution, not preloaded at startup.

### Step 4: Find Available Skills

Skills can exist in two locations. Search both:

**Project skills:**
```
Glob: .claude/skills/*/SKILL.md
```

**User skills:**
```
Bash: ls -1 ~/.claude/skills/
```

Extract the skill name from each path (the directory name).

### Step 5: Cross-Reference Skills

For each skill referenced by agents (both frontmatter and by-context):
1. Check if it exists in project skills (`.claude/skills/`)
2. If not found, check if it exists in user skills (`~/.claude/skills/`)
3. Mark as "missing" only if not found in either location

### Step 5b: Measure Skill Context Size

For each skill referenced in agent frontmatter (preloaded skills):

1. Find the skill's main file (`SKILL.md`) and any supporting files in its directory
2. Count the total characters/lines of all files that would be loaded
3. Estimate token count (roughly 1 token per 4 characters)

**How to measure:**
```bash
# For a skill directory, count all markdown files
wc -c ~/.claude/skills/skill-name/*.md
# or
wc -c .claude/skills/skill-name/*.md
```

**Calculate per-agent totals:**
- Sum the context size of all frontmatter skills for each agent
- Add the agent's own `.md` file size

**Thresholds for recommendations:**
| Context Size | Tokens (approx) | Recommendation |
|--------------|-----------------|----------------|
| < 20KB | < 5K tokens | ✓ Good |
| 20-50KB | 5-12K tokens | ⚠️ Moderate - consider if all skills are needed |
| 50-100KB | 12-25K tokens | ⚠️ Heavy - may impact agent performance |
| > 100KB | > 25K tokens | ❌ Too much - reduce preloaded skills |

### Step 6: Generate Output

Display results in the following format:

```markdown
## Built-in Agents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| Explore | Haiku | Read-only (Glob, Grep, Read, WebFetch, WebSearch) | Fast codebase exploration |
| Plan | Inherited | Read-only (all except Task, ExitPlanMode, Edit, Write, NotebookEdit) | Plan mode research and design |
| general-purpose | Inherited | All tools | Complex multi-step tasks |
| Bash | Inherited | Bash only | Terminal command execution |
| statusline-setup | Sonnet | Read, Edit | Status line configuration |
| claude-code-guide | Haiku | Glob, Grep, Read, WebFetch, WebSearch | Claude Code documentation help |

## Project Agents

| Agent | Description | Skills (Frontmatter) | Context Size | Status |
|-------|-------------|---------------------|--------------|--------|
| ... | ... | `skill1`, `skill2` | 45KB (~11K tokens) | ⚠️ Moderate |

### Context Size Details

For agents with moderate or heavy context, show breakdown:

| Agent | Skill | Size |
|-------|-------|------|
| architect | architecture | 8KB |
| architect | api-handlers | 12KB |
| ... | ... | ... |
| **Total** | | **45KB** |

## All Referenced Skills - Validation

| Skill | Location | Status |
|-------|----------|--------|
| skill-name | Project / User | ✓ or ✗ |

## Skills Available

### Project Skills (`.claude/skills/`)
List all skills found in project

### User Skills (`~/.claude/skills/`)
List all skills found in user directory

## Validation Summary

- **Total project agents**: X
- **Total skills referenced**: X (Y unique)
- **Missing skills**: X (list them)
- **Skills never referenced**: X (list them)
- **Agents with heavy context**: X (list agents exceeding 50KB)
```

## Notes

- **Frontmatter skills** are preloaded when the agent starts - they're always available
- **By-context skills** are loaded manually via `/skill` command during execution
- Built-in agents don't have skills frontmatter but can be extended via CLI flags
- Skills can be loaded from either project (`.claude/skills/`) or user (`~/.claude/skills/`) locations
- A "missing" skill means the agent references a skill that doesn't exist in either location
- **Context size matters** - agents with too many preloaded skills consume context before they start working, leaving less room for the actual task. Keep preloaded skills focused on what the agent always needs.

## Reference

See `REFERENCE.md` in this skill directory for built-in agents data.
