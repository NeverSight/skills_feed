---
name: obsidian-second-brain
description: >-
  Comprehensive guide for integrating Obsidian vaults as AI-powered second brains with Claude Code.
  Covers MCP integration, vault manifests, self-evolving patterns, auto-linking, and knowledge
  graph automation. Use when setting up Claude Code + Obsidian workflows, implementing
  bidirectional sync, creating CLAUDE.md manifests, or building self-healing knowledge systems.
---

# Obsidian Second Brain + Claude Code Integration

## Overview

Transform your Obsidian vault into an AI-powered second brain by integrating it with Claude Code.
This skill covers multiple integration patterns from minimal setup to advanced self-evolving systems.

**Key Insight**: An Obsidian vault is essentially a codebase of markdown files. Claude Code is
already excellent at navigating file structures and making surgical edits - no special plugin required.

## Integration Patterns

### Decision Tree

```text
What integration level do you need?
├── Minimal (just works)?
│   └── Pattern A: Direct Access
│       └── Claude Code reads vault directly (no setup needed)
├── Enhanced discovery?
│   └── Pattern B: Manifest-Based
│       └── Add CLAUDE.md to vault root
├── Real-time bidirectional?
│   └── Pattern C: MCP Plugin
│       └── Install obsidian-claude-code-mcp
├── Self-evolving PKM?
│   └── Pattern D: COG Pattern
│       └── Git + automation + self-healing refs
└── Pre-configured structure?
    └── Pattern E: Claudesidian
        └── Adopt opinionated vault structure
```

## Pattern A: Direct Access (Zero Setup)

Claude Code can already read and edit your vault. No configuration needed.

### How It Works

```bash
# Claude Code navigates your vault like any codebase
cd /path/to/your/vault
claude

# Example interactions:
# "Read my daily note from today"
# "Find all notes mentioning project X"
# "Add backlinks to people mentioned in this note"
```

### Best Practices

- Open Claude Code from vault root directory
- Use natural language to describe what you want
- Reference files by name or topic, not exact paths

### Use Cases

| Task | Claude Code Capability |
|------|------------------------|
| Read notes | Direct file access |
| Edit notes | Surgical markdown edits |
| Add backlinks | Find references, insert wikilinks |
| Create notes | Write new files with proper frontmatter |
| Search content | Grep across all markdown files |
| Refactor structure | Move files, update references |

## Pattern B: Manifest-Based (CLAUDE.md)

Add a project manifest to help Claude Code understand your vault's structure and conventions.

### CLAUDE.md Template

Create `CLAUDE.md` at your vault root:

```markdown
# Obsidian Vault Manifest

## Vault Overview
This is a personal knowledge management vault using [describe your system].

## Folder Structure
- `00 - Inbox/` - Quick capture, unsorted notes
- `01 - Projects/` - Active project notes
- `02 - Areas/` - Ongoing responsibilities
- `03 - Resources/` - Reference materials
- `04 - Archive/` - Completed/inactive content
- `Daily/` - Daily notes (YYYY/MM/DD.md format)
- `Templates/` - Note templates

## Conventions
- Frontmatter: Always include `created`, `updated`, `tags`
- Links: Use `[[wikilinks]]` not markdown links
- Tags: Hierarchical (e.g., `#project/client-name`)
- Dates: ISO 8601 format (YYYY-MM-DD)

## Important Files
- `_index.md` - Main dashboard/MOC
- `project-context.md` - Current project context

## When Creating Notes
1. Always add proper frontmatter
2. Include backlinks to related notes
3. Tag appropriately for discoverability
4. Place in correct folder based on type

## When Editing Notes
1. Update the `updated` timestamp
2. Maintain existing link structure
3. Preserve block references (^block-id)
```

See: [templates/CLAUDE.md](templates/CLAUDE.md) for full template.

## Pattern C: MCP Plugin Integration

Real-time bidirectional communication via Model Context Protocol.

### Installation

```bash
# Install the MCP plugin from Obsidian Community Plugins
# Plugin: obsidian-claude-code-mcp
# Repository: github.com/iansinnott/obsidian-claude-code-mcp
```

### Configuration

1. Enable plugin in Obsidian
2. Default WebSocket port: 22360
3. Claude Code auto-discovers running Obsidian instances

### MCP Capabilities

| Capability | Description |
|------------|-------------|
| `read_note` | Read note content with metadata |
| `write_note` | Create or update notes |
| `search` | Semantic search across vault |
| `list_notes` | Browse vault structure |
| `get_backlinks` | Find notes linking to a file |
| `get_outlinks` | Find notes a file links to |
| `get_tags` | List all tags in vault |

### Claude Code MCP Configuration

Add to your Claude Code settings if not auto-discovered:

```json
{
  "mcpServers": {
    "obsidian": {
      "transport": "websocket",
      "url": "ws://localhost:22360"
    }
  }
}
```

## Pattern D: COG Self-Evolving Pattern

Git-based self-evolving second brain with auto-organization.

### Architecture

```text
vault/
├── .git/                    # Version control
├── CLAUDE.md                # AI manifest
├── _meta/
│   ├── patterns.md          # Learned patterns
│   ├── conventions.md       # Auto-discovered rules
│   └── maintenance-log.md   # Self-healing log
├── notes/                   # Content
└── daily/                   # Journal
```

### Self-Healing Features

1. **Auto cross-references**: Updates links when notes are moved
2. **Pattern learning**: Discovers and applies your conventions
3. **Orphan detection**: Identifies unlinked notes
4. **Consistency checks**: Validates frontmatter, tags

### Git Hooks Setup

```bash
# .git/hooks/post-commit
#!/bin/bash
# Trigger Claude Code maintenance after commits

claude --print "Check for broken links and orphan notes in the vault.
Fix any issues and update _meta/maintenance-log.md with actions taken."
```

### Maintenance Commands

```bash
# Ask Claude Code to perform maintenance
claude "Analyze my vault for orphan notes and suggest connections"
claude "Find notes without proper frontmatter and fix them"
claude "Update all daily notes with missing navigation links"
```

## Pattern E: Claudesidian Structure

Adopt a pre-configured vault structure optimized for AI interaction.

### Folder Structure

```text
vault/
├── CLAUDE.md                # Manifest (required)
├── Inbox/                   # Quick capture
├── Projects/                # Active work
├── Knowledge/               # Permanent notes
├── Journal/                 # Daily reflection
├── Templates/               # Note templates
└── _meta/                   # System files
    ├── prompts/             # Saved prompts
    ├── contexts/            # Context files
    └── exports/             # Generated outputs
```

### Key Conventions

- Every note has frontmatter with `id`, `created`, `updated`
- Tags follow hierarchy: `#type/subtype`
- Daily notes link to previous/next
- Templates include Claude Code prompts

## Common Workflows

### Auto-Linking People, Places, Books

```text
User: "Read my journal entry from today and add backlinks to all
people, places, and books mentioned"

Claude Code:
1. Reads today's daily note
2. Extracts entity mentions
3. Searches vault for existing notes
4. Creates new notes if needed
5. Inserts [[wikilinks]] throughout
```

### Knowledge Graph Maintenance

```text
User: "Find orphan notes and suggest connections"

Claude Code:
1. Identifies notes with no incoming/outgoing links
2. Analyzes content for potential connections
3. Suggests or creates links
4. Updates MOCs (Maps of Content)
```

### Research Synthesis

```text
User: "Synthesize all my notes on [topic] into a summary note"

Claude Code:
1. Searches for relevant notes
2. Extracts key insights
3. Creates structured summary
4. Links back to source notes
```

### Daily Note Enhancement

```text
User: "Review today's note and add structure"

Claude Code:
1. Reads raw capture
2. Adds proper frontmatter
3. Identifies tasks → adds checkboxes
4. Identifies mentions → adds links
5. Suggests tags based on content
```

## Best Practices

### For All Patterns

1. **Keep vault in version control** - Git enables rollback and change tracking
2. **Use consistent frontmatter** - Helps Claude Code understand note types
3. **Maintain a manifest** - CLAUDE.md provides context and conventions
4. **Regular maintenance** - Ask Claude Code to check for issues periodically

### For MCP Integration

1. **Keep Obsidian running** - MCP requires active connection
2. **Use semantic search** - Leverage MCP's search capabilities
3. **Handle conflicts** - Be aware of simultaneous edits

### For Self-Evolving Systems

1. **Review AI changes** - Check git diff before committing
2. **Train on preferences** - Correct mistakes to improve patterns
3. **Document exceptions** - Update manifest with edge cases

## Troubleshooting

### Claude Code Not Finding Notes

```bash
# Ensure you're in the vault directory
pwd  # Should show vault path

# Check file permissions
ls -la *.md

# Verify markdown extension
find . -name "*.md" | head -20
```

### MCP Connection Failed

```bash
# Check Obsidian is running
pgrep -l Obsidian

# Verify plugin is enabled
# Settings → Community Plugins → obsidian-claude-code-mcp

# Check port availability
lsof -i :22360

# Test WebSocket connection
websocat ws://localhost:22360
```

### Broken Wikilinks After Edits

```bash
# Ask Claude Code to fix
claude "Find all broken wikilinks in the vault and fix them"

# Or use grep to find issues
grep -r "\[\[" --include="*.md" | grep -v "\.obsidian"
```

## Integration Comparison

| Feature | Direct | Manifest | MCP | COG | Claudesidian |
|---------|--------|----------|-----|-----|--------------|
| Setup Required | None | Minimal | Plugin | Git + hooks | Structure |
| Real-time Sync | No | No | Yes | No | No |
| Semantic Search | Basic | Basic | Yes | Basic | Basic |
| Self-Healing | No | No | No | Yes | Partial |
| Vendor Lock-in | None | None | Low | None | Structure |
| Best For | Simple | Organized | Power users | Automation | New vaults |

## Resources

### References

- [references/mcp-integration.md](references/mcp-integration.md) - MCP protocol details
- [references/cog-pattern.md](references/cog-pattern.md) - Self-evolving architecture
- [references/workflows.md](references/workflows.md) - Common automation workflows

### Templates

- [templates/CLAUDE.md](templates/CLAUDE.md) - Vault manifest template
- [templates/daily-note.md](templates/daily-note.md) - AI-friendly daily note
- [templates/project-note.md](templates/project-note.md) - Project note template

### External Resources

- [obsidian-claude-code-mcp](https://github.com/iansinnott/obsidian-claude-code-mcp) - MCP Plugin
- [COG-second-brain](https://github.com/huytieu/COG-second-brain) - Self-evolving pattern
- [Claudesidian](https://github.com/heyitsnoah/claudesidian) - Pre-configured vault
- [minimal-second-brain](https://github.com/gokhanarkan/minimal-second-brain) - Minimal template

## Quick Start

### Fastest Path (Pattern A + B)

```bash
# 1. Navigate to your vault
cd /path/to/your/obsidian/vault

# 2. Create a minimal manifest
cat > CLAUDE.md << 'EOF'
# Vault Manifest

This is my Obsidian vault. Key conventions:
- Daily notes in `Daily/YYYY/MM/DD.md`
- Use `[[wikilinks]]` for internal links
- Frontmatter with `created`, `updated`, `tags`
EOF

# 3. Start using Claude Code
claude "What notes do I have about [topic]?"
```

### Full Integration (Pattern C)

1. Install obsidian-claude-code-mcp plugin
2. Create CLAUDE.md manifest
3. Enable plugin in Obsidian settings
4. Claude Code auto-connects via WebSocket

### Self-Evolving Setup (Pattern D)

1. Initialize git in vault
2. Create CLAUDE.md manifest
3. Add git hooks for maintenance
4. Schedule periodic Claude Code reviews
