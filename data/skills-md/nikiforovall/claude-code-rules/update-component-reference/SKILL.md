---
name: update-component-reference
description: This skill should be used when the user wants to add components (commands, agents, skills, hooks, or MCP servers) to the Component Reference section of the website.
---

# Update Component Reference Skill

Add documentation for Claude Code components (commands, agents, skills, hooks, MCP servers) to the website's Component Reference section.

## When to Use

Use this skill when the user requests to:
- Add a new component to the Component Reference documentation
- Document a newly created command, agent, skill, hook, or MCP server
- Update component documentation in the reference section

## Prerequisites Checklist

Before documenting a component, ensure:

1. **Component exists** in the appropriate plugin directory:
   - Commands: `plugins/handbook/commands/{name}.md`
   - Agents: `plugins/handbook/agents/{name}.md`
   - Skills: `plugins/handbook/skills/{name}/SKILL.md`
   - Hooks: `plugins/{plugin-name}/hooks/hooks.json` and hook scripts
   - MCP Servers: `plugins/{plugin-name}/.mcp.json`

2. **For skills only**: Component is registered in plugin.json:
   ```json
   {
     "skills": [
       "./skills/skill-creator",
       "./skills/{new-skill-name}"
     ]
   }
   ```

3. **Verify plugin name**: Check `.claude-plugin/plugin.json` for the badge (e.g., "handbook", "handbook-dotnet")

## Implementation Process

### Step 1: Determine Target Directory

Component documentation goes in: `website/docs/component-reference/{type}/`

- Commands → `website/docs/component-reference/commands/`
- Agents → `website/docs/component-reference/agents/`
- Skills → `website/docs/component-reference/skills/`
- Hooks → `website/docs/component-reference/hooks/`
- MCP Servers → `website/docs/component-reference/mcp-servers/`

All category directories and `_category_.json` files already exist for these types.

### Step 2: Determine sidebar_position

Read existing `.mdx` files in the target directory to find the highest `sidebar_position` and add 1.

Example:
```bash
grep -h "sidebar_position:" website/docs/component-reference/skills/*.mdx | sort -n
```

### Step 3: Create Component Documentation File

**Filename convention**: Use kebab-case matching the component name
- Command `/commit` → `commit.mdx`
- Agent `@backend-architect` → `backend-architect.mdx`
- Skill `skill-creator` → `skill-creator.mdx`
- Hook `csharp-formatter` → `csharp-formatter.mdx`
- MCP Server `context7` → `context7.mdx`

### Step 4: Write MDX Content

Use the appropriate template based on component type:

#### Commands Template

```mdx
---
title: "/command-name"
sidebar_position: N
---

import CommandNameSource from '!!raw-loader!../../../../plugins/handbook/commands/command-name.md'
import CodeBlock from '@theme/CodeBlock';

# Use `/command-name`

<span className="badge badge--handbook">handbook</span>

Brief description of what this command does (1-2 sentences).

More detailed explanation of the command's purpose and benefits.

## Command Specification

<CodeBlock language="markdown">
{CommandNameSource}
</CodeBlock>

## Additional sections as needed
- Example usage
- Tips and tricks
- Related commands
```

#### Agents Template

```mdx
---
title: "@agent-name"
sidebar_position: N
---

import AgentNameSource from '!!raw-loader!../../../../plugins/handbook/agents/agent-name.md'
import CodeBlock from '@theme/CodeBlock';

# Use `@agent-name` agent

<span className="badge badge--handbook">handbook</span>

Brief description of what this agent specializes in (1-2 sentences).

More detailed explanation of the agent's capabilities and when to use it.

## Agent Specification

<CodeBlock language="markdown">
{AgentNameSource}
</CodeBlock>

## Additional sections as needed
- Key strengths
- Example use cases
- Related agents
```

#### Skills Template

```mdx
---
title: "skill-name"
sidebar_position: N
---

import SkillNameSource from '!!raw-loader!../../../../plugins/handbook/skills/skill-name/SKILL.md'
import CodeBlock from '@theme/CodeBlock';

# Use `skill-name` skill

<span className="badge badge--handbook">handbook</span>

Brief description of what this skill provides (1-2 sentences).

More detailed explanation of the skill's purpose and capabilities.

## When to Use This Skill

Use the `skill-name` skill when you want to:

- Primary use case
- Secondary use case
- Additional scenarios

## Skill Specification

<CodeBlock language="markdown">
{SkillNameSource}
</CodeBlock>

## Additional sections as needed
- Key concepts
- Example workflows
- Related skills
```

#### Hooks Template

```mdx
---
title: "Hook Name"
sidebar_position: N
---

# Hook Name

<span className="badge badge--{plugin-name}">{plugin-name}</span>

Brief description (1-2 sentences).

## Configuration

```json
{ hook config from hooks.json }
```

## Use Cases

- Bullet points

## Installation

Setup notes.

## Related

- Links
```

#### MCP Servers Template

```mdx
---
title: "server-name"
sidebar_position: N
---

# Server Name MCP Server

<span className="badge badge--{plugin-name}">{plugin-name}</span>

Brief description (1-2 sentences).

## Configuration

```json
{ config from .mcp.json }
```

## Coverage

- Bullet list

## Example Usage

```
"Example query"
```

## Installation

Setup notes.

## Related

- Links
```

### Step 5: Verify Import Paths (Commands, Agents, Skills Only)

**Note**: Hooks and MCP Servers show configuration directly (no raw-loader imports needed).

For commands, agents, and skills, double-check the raw-loader import path:

- Commands: `'!!raw-loader!../../../../plugins/handbook/commands/{name}.md'`
- Agents: `'!!raw-loader!../../../../plugins/handbook/agents/{name}.md'`
- Skills: `'!!raw-loader!../../../../plugins/handbook/skills/{name}/SKILL.md'` ⚠️ Note the `/SKILL.md` suffix

The path goes up 4 directories (`../../../../`) from the `.mdx` file to reach the repo root.

## Common Pitfalls

1. **Forgetting plugin.json registration for skills**
   - Skills MUST be in plugin.json or they won't be available
   - Commands, agents, hooks, and MCP servers are auto-discovered

2. **Incorrect import paths**
   - Skills use `/SKILL.md` suffix: `skills/{name}/SKILL.md`
   - Commands and agents use `.md` directly: `commands/{name}.md`
   - Hooks and MCP servers don't use raw-loader (show config directly)

3. **Wrong relative path depth (commands, agents, skills only)**
   - Always use 4 levels up: `../../../../`
   - Path starts from the `.mdx` file location

4. **Inconsistent naming**
   - File names should match component names exactly (kebab-case)
   - Title in frontmatter should include prefix (`/` for commands, `@` for agents)

5. **Wrong plugin badge**
   - Badge class follows pattern: `badge--{plugin-name}`
   - Badge text is the plugin name (e.g., "handbook", "handbook-dotnet")

## Quick Reference

### Import Variable Naming Convention (Commands, Agents, Skills)
Match the component name in PascalCase + "Source":
- `commit.md` → `CommitCommandSource`
- `backend-architect.md` → `BackendArchitectAgentSource`
- `skill-creator/SKILL.md` → `SkillCreatorSource`

**Note**: Hooks and MCP servers don't use imports.

### Badge
Badge format: `<span className="badge badge--{plugin-name}">{plugin-name}</span>`

Examples:
- handbook: `<span className="badge badge--handbook">handbook</span>`
- handbook-dotnet: `<span className="badge badge--handbook-dotnet">handbook-dotnet</span>`

## Adding a New Plugin

When documenting components from a **new plugin**, also update:

1. **Badge CSS**: Add style to `website/src/css/custom.css` (pick unique color)
2. **Plugin index**: Add entry to `website/docs/plugins.md` (both main list and Direct Installation section)

## Example Workflow

**User**: "Add the new @pair-programmer agent to the documentation"

1. **Verify** component exists: `plugins/handbook/agents/pair-programmer.md` ✓
2. **Check** it's an agent (auto-discovered, no plugin.json needed) ✓
3. **Find** next sidebar_position in `website/docs/component-reference/agents/`
4. **Create** `website/docs/component-reference/agents/pair-programmer.mdx`
5. **Write** content using agent template
6. **Import** using: `'!!raw-loader!../../../../plugins/handbook/agents/pair-programmer.md'`
7. **Verify** documentation renders correctly