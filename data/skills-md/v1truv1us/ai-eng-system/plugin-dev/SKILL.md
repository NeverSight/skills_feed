---
name: plugin-dev
description: This skill should be used when creating extensions for Claude Code or OpenCode, including plugins, commands, agents, skills, and custom tools. Covers both platforms with format specifications, best practices, and the ai-eng-system build system.
version: 1.0.0
---

# Plugin Development for Claude Code & OpenCode

## Critical Importance

**Creating high-quality plugins is critical to your development workflow's long-term success.** Plugins are used repeatedly by yourself and others. Design flaws, poor documentation, or broken functionality compound over time and across users. A well-designed plugin becomes a trusted tool used daily; a poorly designed plugin becomes abandoned technical debt. Invest time in architecture, testing, and documentation—the returns multiply across all future uses.

## Systematic Approach

** approach plugin development systematically.** Plugins require careful planning: understand the problem, design the API, implement incrementally, test thoroughly, and document comprehensively. Don't rush to code—clarify requirements, define interfaces, and consider edge cases first. Build iteratively, validate frequently, and refactor continuously. Every design decision impacts maintainability and extensibility.

## The Challenge

**The create a plugin that balances specificity with flexibility perfectly, but if you can:**

- Your plugin will be a joy to use and extend
- Others will build on top of your work
- The plugin will remain useful as needs evolve
- You'll establish patterns for future plugin development

The challenge is designing plugins that solve specific problems while staying flexible enough for future use cases. Can you create focused, opinionated tools that don't paint yourself into corners?

## Plugin Confidence Assessment

After completing or reviewing plugin development, rate your confidence from **0.0 to 1.0**:

- **0.8-1.0**: Plugin well-architected, fully tested, thoroughly documented, follows platform conventions
- **0.5-0.8**: Plugin functional but missing some tests or documentation, some technical debt
- **0.2-0.5**: Plugin works but design unclear, minimal testing, poor documentation
- **0.0-0.2**: Plugin incomplete or broken, unclear purpose, significant rework needed

Identify uncertainty areas: Is the plugin's purpose clear? Are there edge cases unhandled? Will the plugin work as requirements change? What's the maintenance burden?

## Overview

The ai-eng-system supports extension development for both Claude Code and OpenCode through a unified content system with automated transformation. Understanding this system enables creating well-organized, maintainable extensions that integrate seamlessly with both platforms.

## Extension Types

| Type | Claude Code | OpenCode | Shared Format |
|------|-------------|----------|---------------|
| Commands | ✅ YAML frontmatter | ✅ Table format | YAML frontmatter |
| Agents | ✅ YAML frontmatter | ✅ Table format | YAML frontmatter |
| Skills | ✅ Same format | ✅ Same format | SKILL.md |
| Hooks | ✅ hooks.json | ✅ Plugin events | Platform-specific |
| Custom Tools | ❌ (use MCP) | ✅ tool() helper | OpenCode only |
| MCP Servers | ✅ .mcp.json | ✅ Same format | Same format |

## Development Approaches

### 1. Canonical Development (Recommended)

Create content in `content/` directory, let build.ts transform to platform formats:

```
content/
├── commands/my-command.md  → dist/.claude-plugin/commands/
│                           → dist/.opencode/command/ai-eng/
└── agents/my-agent.md      → dist/.claude-plugin/agents/
                            → dist/.opencode/agent/ai-eng/
```

### 2. Platform-Specific Development

Create directly in platform directories:

- Claude Code: `.claude/commands/`, `.claude-plugin/`
- OpenCode: `.opencode/command/`, `.opencode/agent/`

### 3. Global vs Project-Local

| Location | Claude Code | OpenCode |
|----------|-------------|----------|
| **Project** | `.claude/` | `.opencode/` |
| **Global** | `~/.claude/` | `~/.config/opencode/` |

## Quick Reference

### Command Frontmatter

**Canonical (content/):**
```yaml
---
name: my-command
description: What this command does
agent: build           # Optional: which agent handles this
subtask: true          # Optional: run as subtask
temperature: 0.3      # Optional: temperature
tools:                 # Optional: tool restrictions
  read: true
  write: true
---
```

**Claude Code Output:** Same format (YAML frontmatter)

**OpenCode Output:** Table format
```markdown
| description | agent |
|---|---|
| Description here | build |
```

### Agent Frontmatter

**Canonical (content/):**
```yaml
---
name: my-agent
description: Use this agent when... <example>...</example>
mode: subagent
color: cyan
temperature: 0.3
tools:
  read: true
  write: true
---
```

**Claude Code Output:** Same format (YAML frontmatter)

**OpenCode Output:** Table format
```markdown
| description | mode |
|---|---|
| Description here | subagent |
```

### Skill Structure

Both platforms use identical format:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown body (1,000-3,000 words)
└── Bundled Resources (optional)
    ├── references/       # Detailed documentation
    ├── examples/         # Working code
    └── scripts/          # Utility scripts
```

### OpenCode Custom Tools

Use TypeScript with `tool()` helper:

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Tool description",
  args: {
    param: tool.schema.string().describe("Parameter description"),
  },
  async execute(args, context) {
    // Tool implementation
    return result
  },
})
```

## Directory Locations

### For Development in ai-eng-system

```
ai-eng-system/
├── content/
│   ├── commands/              # Add new commands here
│   └── agents/                # Add new agents here
├── skills/
│   └── plugin-dev/           # This skill
└── build.ts                   # Transforms to both platforms
```

### For User Projects

**Project-local:**
- Claude Code: `.claude/commands/`, `.claude-plugin/`
- OpenCode: `.opencode/command/`, `.opencode/agent/`

**Global:**
- Claude Code: `~/.claude/commands/`, `~/.claude-plugin/`
- OpenCode: `~/.config/opencode/command/`, `~/.config/opencode/agent/`

## Platform-Specific Features

### Claude Code

**Components:**
- Commands with YAML frontmatter
- Agents with YAML frontmatter
- Skills with SKILL.md format
- Hooks via `hooks/hooks.json`
- MCP servers via `.mcp.json`

**Manifest:** `.claude-plugin/plugin.json`
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description",
  "commands": ["./commands/*"],
  "mcpServers": "./.mcp.json"
}
```

### OpenCode

**Components:**
- Commands with table format
- Agents with table format
- Skills via opencode-skills plugin
- Custom tools with TypeScript
- Plugin events via TypeScript

**Plugin:** `.opencode/plugin/plugin.ts`
```typescript
import { Plugin } from "@opencode-ai/plugin"

export default (async ({ client, project, directory, worktree, $ }) => {
  return {
    // Plugin hooks here
  }
}) satisfies Plugin
```

## Development Workflow

### 1. Create Component

Use plugin-dev commands:
- `/ai-eng/create-agent` - Create new agent
- `/ai-eng/create-command` - Create new command
- `/ai-eng/create-skill` - Create new skill
- `/ai-eng/create-tool` - Create new custom tool

### 2. Build

```bash
cd ai-eng-system
bun run build              # Build all platforms
bun run build --watch        # Watch mode
bun run build --validate      # Validate content
```

### 3. Test

**Claude Code:**
```bash
claude plugin add https://github.com/v1truv1us/ai-eng-system
```

**OpenCode:**
```bash
# Project-local
./setup.sh

# Global
./setup-global.sh
```

## Best Practices

### Content Quality
- Use third-person in skill descriptions
- Write commands/agents FOR Claude, not to user
- Include specific trigger phrases
- Follow progressive disclosure for skills

### File Organization
- One component per file
- Clear naming conventions (kebab-case)
- Proper frontmatter validation

### Cross-Platform Compatibility
- Use canonical format in `content/`
- Test build output for both platforms
- Document platform differences

### Security
- No hardcoded credentials
- Use HTTPS/WSS for external connections
- Validate user inputs
- Follow principle of least privilege

## Additional Resources

### References

- `references/claude-code-plugins.md` - Claude Code specifics
- `references/opencode-plugins.md` - OpenCode specifics
- `references/command-format.md` - Command syntax guide
- `references/agent-format.md` - Agent configuration guide
- `references/skill-format.md` - Skills specification
- `references/opencode-tools.md` - Custom tool development

### Examples

Study existing components in ai-eng-system:
- `content/commands/plan.md` - Command structure
- `content/agents/architect-advisor.md` - Agent structure
- `skills/prompting/incentive-prompting/SKILL.md` - Skill structure

## Troubleshooting

### Build Issues
- Run `bun run build --validate` to check content
- Check file permissions in output directories
- Verify YAML frontmatter syntax

### Platform Testing
- Test commands in both Claude Code and OpenCode
- Verify agents trigger correctly
- Check skills load via opencode-skills plugin

### Common Errors
- Missing required frontmatter fields
- Incorrect directory structure
- Invalid YAML syntax
- Wrong file permissions

## Integration with Ferg Engineering

The plugin-dev system integrates seamlessly with existing ai-eng-system components:

### Existing Commands
- `/ai-eng/plan` - Implementation planning
- `/ai-eng/review` - Code review
- `/ai-eng/work` - Task execution

### Existing Agents
- `ai-eng/architect-advisor` - Architecture guidance
- `ai-eng/frontend-reviewer` - Frontend review
- `ai-eng/seo-specialist` - SEO optimization

### Plugin-Dev Commands
- `/ai-eng/create-plugin` - Full plugin development workflow
- `/ai-eng/create-agent` - Quick agent creation
- `/ai-eng/create-command` - Quick command creation
- `/ai-eng/create-skill` - Quick skill creation
- `/ai-eng/create-tool` - Quick tool creation

All use the same quality standards and research-backed prompting techniques.