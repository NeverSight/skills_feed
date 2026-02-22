---
name: openclaw-agent-builder
description: Build specialized openclaw agents with proper workspace structure, identity, and skills
---

# OpenClaw Agent Builder

Create specialized openclaw agents with complete workspace structure, identity files, and skills.

## When to Use

When building a new openclaw agent for a specific purpose:
- Domain-specific agents (Android dev, SEO, content writing, etc.)
- Multi-agent routing scenarios
- Isolated agent personalities
- Workspace-based AI assistants

## Core Concepts

### OpenClaw Agent Structure

Each agent = isolated brain with:
- **Workspace**: Files (AGENTS.md, SOUL.md, USER.md, IDENTITY.md, TOOLS.md, etc.)
- **State dir**: `~/.openclaw/agents/<agentId>/agent` (auth, config)
- **Sessions**: `~/.openclaw/agents/<agentId>/sessions` (chat history)

### Workspace Files

**Required:**
- `AGENTS.md` - Operating instructions, memory management, behavior rules
- `SOUL.md` - Persona, tone, communication style
- `USER.md` - User context and how to address them
- `IDENTITY.md` - Agent name, emoji, role, mission
- `TOOLS.md` - Tool notes and conventions

**Optional:**
- `HEARTBEAT.md` - Heartbeat checklist (keep short)
- `BOOT.md` - Startup checklist when gateway restarts
- `memory/` - Daily memory logs (YYYY-MM-DD.md)
- `MEMORY.md` - Curated long-term memory
- `skills/` - Workspace-specific skills

## Agent Builder Workflow

### 1. Ask Questions First

Before building, clarify:
- **Agent purpose**: What problem does this agent solve?
- **Domain expertise**: What specialized knowledge needed?
- **Communication style**: Professional? Casual? Technical?
- **Tools/integrations**: APIs, databases, external systems?
- **Skills needed**: Custom capabilities or workflows?

### 2. Create Workspace Structure

```bash
# Create agent workspace
mkdir -p ~/.openclaw/workspace-<agent-name>
cd ~/.openclaw/workspace-<agent-name>

# Initialize git (recommended)
git init
```

### 3. Build Core Files

**IDENTITY.md** - Who the agent is:
```markdown
# IDENTITY.md

## Name
[Agent Name]

## Emoji
[1-2 relevant emojis]

## Role
[Short role description - e.g., "Android spec writer", "SEO optimizer"]

## Mission
[Concise mission statement - what the agent does and why]
```

**SOUL.md** - Personality and tone:
```markdown
# SOUL.md - [Agent Name]

## Who You Are

[Description of expertise, background, strengths]

## Your Expertise

### [Domain 1]
- [Specific skill or knowledge area]
- [Another capability]

### [Domain 2]
- [Capability]

## Your Approach

### [Trait 1 - e.g., Analytical, Pragmatic]
- [How this manifests]

### [Trait 2]
- [Behavior pattern]

## Your Tone

[Communication style - concise/verbose, formal/casual, technical level]

## Your Values

1. **[Value 1]** - [Why it matters]
2. **[Value 2]** - [Explanation]
```

**AGENTS.md** - Operating instructions:
```markdown
# AGENTS.md - [Agent Name]

[Brief agent description and primary role]

## Primary Responsibilities

1. **[Task 1]** - [Description]
2. **[Task 2]** - [Description]

## Workflow

### On User Request: "[Trigger Pattern]"

1. **[Step 1]** [Action description]
   [Details, commands, or sub-steps]

2. **[Step 2]** [Next action]

### On User Request: "[Another Pattern]"

[Workflow steps]

## [Domain-Specific Section - e.g., "iOS Codebase Structure"]

[Relevant context, file paths, patterns]

## [Another Section - e.g., "Translation Guidelines"]

[Reference tables, mappings, rules]

## Memory

- Log [what to track] in `memory/YYYY-MM-DD.md`
- [Memory strategy specific to agent purpose]

## Tools

See `TOOLS.md` for [domain-specific tools or integrations]

## Skills

- **[skill-name]** - [Purpose]
- **[another-skill]** - [Purpose]
```

**USER.md** - User context:
```markdown
# USER.md

## Who You Are

[User description, preferences, context]

## Your Goals

[What user wants to achieve with this agent]

## Communication Preferences

[How user prefers to interact]
```

**TOOLS.md** - Tool conventions:
```markdown
# TOOLS.md

## [Domain] Tools

- **[Tool/API name]**: [Purpose and usage notes]
- **[Another tool]**: [Notes]

## Authentication

[If agent needs API keys, credentials, etc.]

## Conventions

[Domain-specific conventions or patterns]
```

### 4. Add Skills (Optional)

Create workspace-specific skills:

```bash
mkdir -p skills/<skill-name>
```

Each skill needs `SKILL.md`:
```markdown
---
name: skill-name
description: What the skill does
---

# Skill Name

[Skill documentation following agentskills.io format]

## When to Use

[Trigger conditions]

## Steps

[Detailed workflow]

## Examples

[Usage examples]
```

### 5. Setup Memory System

```bash
mkdir -p memory
touch memory/$(date +%Y-%m-%d).md
```

Optional `MEMORY.md` for curated knowledge:
```markdown
# MEMORY.md

## [Category]

- [Key fact or pattern]
- [Lesson learned]

## [Another Category]

[Organized knowledge]
```

### 6. Register Agent

```bash
# Add agent to openclaw
openclaw agents add <agent-name>

# Set workspace path
# Edit ~/.openclaw/openclaw.json:
{
  "agents": {
    "list": [
      {
        "id": "<agent-name>",
        "workspace": "~/.openclaw/workspace-<agent-name>"
      }
    ]
  }
}
```

### 7. Add Bindings (Multi-Agent Routing)

Route specific channels/users to this agent:

```json5
{
  "bindings": [
    {
      "agentId": "<agent-name>",
      "match": {
        "channel": "whatsapp",
        "peer": { "kind": "direct", "id": "+1234567890" }
      }
    }
  ]
}
```

## Design Principles

### Agent Identity
- **Clear purpose**: Single, focused responsibility
- **Distinct personality**: Unique tone/approach vs other agents
- **Expertise depth**: Deep knowledge in specific domain

### Communication Style
- **Concise**: Default to brevity unless domain requires detail
- **Professional**: Match industry standards
- **Actionable**: Focus on what to do, not just description

### Memory Strategy
- **Daily logs**: Track important events/decisions
- **Curated knowledge**: Extract patterns into MEMORY.md
- **Context preservation**: Save state before `/new` or `/reset`

### Skill Organization
- **Workspace skills**: Agent-specific capabilities
- **Shared skills**: Common utilities in `~/.openclaw/skills/`
- **Override pattern**: Workspace skills override shared/bundled

## Example Agents

### Android Spec Generator
```
Purpose: Analyze iOS features, generate Android requirement specs
Style: Concise, technical, requirement-focused
Skills: ios-analyzer, android-spec-generator, github-issue-creator
```

### SEO Expert
```
Purpose: Content optimization, keyword research, SEO strategy
Style: Data-driven, analytical, actionable
Skills: keyword-research, content-analyzer, competitor-analysis
```

### Content Writer
```
Purpose: Blog posts, documentation, technical writing
Style: Clear, engaging, audience-aware
Skills: content-planner, seo-writer, editor
```

## Anti-Patterns

❌ **Don't:**
- Mix multiple unrelated domains in one agent
- Create verbose, chatty agents unless purpose requires it
- Duplicate content across AGENTS.md, SOUL.md, TOOLS.md
- Store secrets in workspace (use `~/.openclaw/credentials/`)

✅ **Do:**
- Keep single, clear focus per agent
- Match communication style to domain norms
- Organize by responsibility (identity/soul/operations)
- Use git for workspace backup (private repo)

## Testing Agent

```bash
# Start gateway with agent
openclaw gateway --agent <agent-name>

# Or use binding to route to agent
openclaw gateway

# Send test message via WhatsApp/Telegram/Discord
# Verify agent responds with expected personality/capability
```

## Maintenance

### Update Agent
```bash
cd ~/.openclaw/workspace-<agent-name>
git add .
git commit -m "Update [what changed]"
git push
```

### Add New Skill
```bash
cd ~/.openclaw/workspace-<agent-name>/skills
mkdir new-skill
# Create SKILL.md
```

### Backup Agent
```bash
# Workspace already in git
# Separately backup sessions if needed:
tar -czf sessions-backup.tar.gz ~/.openclaw/agents/<agent-name>/sessions/
```

## Resources

- [OpenClaw Multi-Agent Routing](https://docs.openclaw.org/concepts/multi-agent)
- [Agent Workspace Structure](https://docs.openclaw.org/concepts/agent-workspace)
- [AgentSkills.io Format](https://agentskills.io/specification)
- [Skills.sh Marketplace](https://skills.sh/)

## Questions Before Building?

Ask user to clarify:
1. **Agent purpose and scope**
2. **Communication style preferences**
3. **Required integrations/APIs**
4. **Routing strategy** (dedicated channel vs shared)
5. **Skill requirements**
