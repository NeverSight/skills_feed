---
name: mcp-to-skill
description: |
  Convert MCP (Model Context Protocol) servers to Claude Code Skills. Use when:
  (1) User wants to convert an MCP server project to a skill
  (2) User mentions "MCP to skill", "convert MCP", or "MCP 转 skill"
  (3) User has an MCP server codebase and wants to make it a reusable skill
  (4) User wants to analyze MCP server structure for skill creation
  Supports TypeScript/JavaScript and Python MCP servers. Generates complete skill package with SKILL.md, scripts, and references.
category: skill-management
tags: [mcp, skill-conversion, model-context-protocol, automation]
---

# MCP to Skill Converter

Convert MCP servers into Claude Code Skills for easier distribution and usage.

## Conversion Workflow

### 1. Analyze MCP Server

Read and understand the MCP server structure:

```bash
# Key files to analyze
- package.json / pyproject.toml  # Dependencies and entry point
- src/index.ts / main.py         # Entry point and tool registration
- src/**/*.ts / **/*.py          # Tool implementations
```

Extract this information:
- **Server name and description**
- **Available tools** (name, description, parameters, implementation)
- **Dependencies** (runtime requirements)
- **Execution method** (node, python, etc.)

### 2. Map MCP Tools to Skill Structure

| MCP Concept | Skill Equivalent |
|-------------|------------------|
| Tool name | Script or instruction section |
| Tool description | Used in SKILL.md description |
| Tool parameters | Script arguments or instruction parameters |
| Tool implementation | `scripts/` executable or inline instructions |

### 3. Generate Skill Structure

```
{skill-name}/
├── SKILL.md                    # Core instructions
├── scripts/
│   ├── run_server.sh          # Server startup script (optional)
│   └── {tool_name}.{ext}      # Individual tool scripts
└── references/
    └── tools.md               # Tool reference documentation
```

### 4. Write SKILL.md

Template structure:

```markdown
---
name: {skill-name}
description: |
  {Original MCP server description}. Use when:
  (1) {Primary use case}
  (2) {Secondary use case}
  {List all tool capabilities}
---

# {Skill Name}

{Brief description of what this skill does}

## Prerequisites

{Any setup requirements - permissions, API keys, etc.}

## Available Tools

{List each tool with usage instructions}

### {Tool Name}

{Description}

**Usage:**
{How to invoke - either via script or direct instruction}

**Parameters:**
- `{param}`: {description}

**Example:**
{Concrete usage example}
```

## Conversion Patterns

### Pattern A: Script-based (for complex tools)

When MCP tool has complex logic, create executable script:

```python
# scripts/tool_name.py
#!/usr/bin/env python3
import argparse
# ... implementation
```

Reference in SKILL.md:
```markdown
Run `scripts/tool_name.py --param value`
```

### Pattern B: Instruction-based (for simple tools)

When MCP tool is simple, use inline instructions:

```markdown
### Send Notification

To send a system notification:
1. Use AppleScript: `display notification "message" with title "title"`
```

### Pattern C: Hybrid (server-dependent tools)

When tools require the MCP server runtime:

```markdown
## Setup

Start the MCP server:
\`\`\`bash
cd {project-path}
npm start  # or: node dist/index.js
\`\`\`

Then use MCP tools via the running server.
```

## AppleScript MCP Example

For applescript-mcp specifically:

1. **No server needed** - Tools are standalone AppleScripts
2. **Use instruction-based pattern** - Each tool becomes a section
3. **Group by category** - System, Calendar, Finder, etc.
4. **Include permission notes** - macOS security requirements

## Output Checklist

Before packaging, verify:

- [ ] SKILL.md has proper frontmatter (name, description)
- [ ] Description includes all use cases and triggers
- [ ] All MCP tools are documented
- [ ] Scripts are executable and tested
- [ ] References are complete but not redundant
- [ ] No unnecessary files (README, CHANGELOG, etc.)

## Package the Skill

```bash
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py /path/to/skill
```
