---
name: obsidian
description: This skill should be used when working with Obsidian files including .md notes with wikilinks/callouts/properties, .base database views with filters/formulas, or .canvas visual diagrams. Routes to specialized sub-skills based on file type and task context. Features self-iterative learning that improves with use.
user-invocable: true
context: fork
agent: obsidian-file-agent
model: sonnet
hooks:
  SessionStart:
    - type: command
      command: bash ${CLAUDE_PLUGIN_ROOT}/scripts/hooks/session-start.sh
      timeout: 10
  PostToolUse:
    - matcher: Write|Edit
      type: command
      command: bash ${CLAUDE_PLUGIN_ROOT}/scripts/hooks/post-tool-use.sh
      timeout: 5
  SessionEnd:
    - type: command
      command: bash ${CLAUDE_PLUGIN_ROOT}/scripts/hooks/session-end.sh
      timeout: 10
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Obsidian Skill

**Version**: 2.2.0 | **SDK**: Claude Code Skills 2.1+

## Directory Index

- [markdown/obsidian-markdown.md](markdown/obsidian-markdown.md) - Wikilinks, embeds, callouts, properties
- [bases/obsidian-bases.md](bases/obsidian-bases.md) - Filters, formulas, database views
- [canvas/obsidian-canvas.md](canvas/obsidian-canvas.md) - JSON Canvas nodes, edges, groups
- [agents/obsidian-file-agent.md](agents/obsidian-file-agent.md) - Master agent (Sonnet)
- [agents/obsidian-markdown.md](agents/obsidian-markdown.md) - Markdown agent (Haiku)
- [agents/obsidian-bases.md](agents/obsidian-bases.md) - Bases agent (Sonnet)
- [agents/obsidian-canvas.md](agents/obsidian-canvas.md) - Canvas agent (Haiku)

---

Comprehensive skill for creating and editing Obsidian vault files. Routes to specialized sub-skills based on file type. **Self-iterative**: learns your patterns and preferences over time through hot-reloadable memory.

## File Type Detection

| Extension | File Type | Sub-skill |
|-----------|-----------|-----------|
| `.md` | Markdown notes | [obsidian-markdown](markdown/obsidian-markdown.md) |
| `.base` | Database views | [obsidian-bases](bases/obsidian-bases.md) |
| `.canvas` | Visual diagrams | [obsidian-canvas](canvas/obsidian-canvas.md) |

## Sub-skill Routing

### When to use each sub-skill:

**[Obsidian Markdown](markdown/obsidian-markdown.md)** - Use when:
- Creating or editing `.md` files in Obsidian vaults
- Working with wikilinks (`[[Note]]`), embeds (`![[Note]]`)
- Adding callouts, frontmatter properties, or tags
- Using Obsidian-specific syntax (block references, comments)

**[Obsidian Bases](bases/obsidian-bases.md)** - Use when:
- Creating or editing `.base` files
- Building database-like views of notes
- Working with filters, formulas, or summaries
- Creating table, cards, list, or map views

**[JSON Canvas](canvas/obsidian-canvas.md)** - Use when:
- Creating or editing `.canvas` files
- Building visual mind maps or flowcharts
- Working with nodes, edges, and groups
- Creating project boards or research canvases

## Quick Syntax Reference

### Markdown (`.md`)
```markdown
[[Note Name]]              # Wikilink
![[Note Name]]             # Embed
> [!note] Title            # Callout
#tag                       # Tag
```

### Bases (`.base`)
```yaml
filters:
  and:
    - file.hasTag("project")
views:
  - type: table
    order: [file.name, status]
```

### Canvas (`.canvas`)
```json
{
  "nodes": [
    {"id": "1", "type": "text", "x": 0, "y": 0, "width": 300, "height": 150, "text": "# Node"}
  ],
  "edges": []
}
```

## Progressive Loading

For detailed documentation, load the appropriate sub-skill:

- **Detailed syntax** → `references/*.md` in each sub-skill
- **Working examples** → `examples/*` in each sub-skill
- **Starter templates** → `templates/*` in each sub-skill

## Self-Iterative Memory

This skill learns and improves over time:

### How It Works
1. **SessionStart** - Loads your usage history and preferences
2. **Pattern Tracking** - Records which Obsidian features you use most
3. **SessionEnd** - Derives preferences from usage patterns
4. **Hot-Reload** - Changes to skill files are immediately available

### Memory Storage
- Location: `.claude/obsidian-memory.json` in project directory
- Tracks: pattern usage, vault context, learned preferences

### Memory Commands
```bash
# View usage statistics
python scripts/hooks/memory-manager.py stats

# Add a learning note
python scripts/hooks/memory-manager.py learn "Discovered useful pattern"

# Reset memory
python scripts/hooks/memory-manager.py reset
```

### What's Tracked
| Category | Patterns |
|----------|----------|
| Markdown | wikilinks, callouts, embeds, properties, tags |
| Bases | filters, formulas, views, summaries |
| Canvas | textNodes, fileNodes, linkNodes, groupNodes, edges |

## Validation

Run validation scripts to check file syntax:
```bash
./scripts/validate-all.sh
```

## Hooks Architecture

| Hook | Trigger | Purpose |
|------|---------|---------|
| SessionStart | Session begins | Load memory, detect vault |
| PostToolUse | Write/Edit completes | Track pattern usage |
| SessionEnd | Session ends | Save learnings, derive preferences |

## Specialized Agents

This skill uses `context: fork` with specialized agents for optimal Obsidian file handling.

### Default Agent
- **obsidian-file-agent** - Master agent handling all three file types with domain-specific expertise

### Domain-Specific Agents
Located in `agents/` directory:

| Agent | Model | Specialization |
|-------|-------|----------------|
| [obsidian-markdown](agents/obsidian-markdown.md) | Haiku | Fast markdown note operations |
| [obsidian-bases](agents/obsidian-bases.md) | Sonnet | Complex formula calculations |
| [obsidian-canvas](agents/obsidian-canvas.md) | Haiku | JSON canvas generation |
| [obsidian-file-agent](agents/obsidian-file-agent.md) | Sonnet | Master agent (default) |

### Agent Installation

For the specialized agents to work, install them to your global agents directory:

```bash
# Install all obsidian agents
./scripts/install-agents.sh

# Or manually symlink
ln -s "$(pwd)/agents/"*.md ~/.claude/agents/
```

### Agent Selection
- The skill uses `agent: obsidian-file-agent` by default
- Specialized agents can be invoked directly if installed:
  - Use `obsidian-markdown` for fast note operations
  - Use `obsidian-bases` for complex formula work
  - Use `obsidian-canvas` for visual diagram creation

## References

- [Obsidian Help](https://help.obsidian.md/)
- [JSON Canvas Spec](https://jsoncanvas.org/spec/1.0/)
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills)
