---
name: obsidian-vault-management
description: Creates, edits, and manages Obsidian vault content including notes, templates, daily notes, and dataview queries. Use when working with markdown files in an Obsidian vault, creating notes, writing templates, building dataview queries, or organizing knowledge management content.
---

# Obsidian Vault Management

## Vault Structure (PARA-Based)

This vault uses a PARA-like organization:

| Folder | Purpose |
|--------|---------|
| `00 - Maps of Content` | Index notes linking related topics |
| `01 - Projects` | Active project notes |
| `02 - Areas` | Ongoing responsibilities |
| `03 - Resources` | Reference materials |
| `04 - Permanent` | Evergreen/zettelkasten notes |
| `05 - Fleeting` | Quick capture notes |
| `06 - Daily` | Daily notes (YYYY/MM/YYYYMMDD.md) |
| `07 - Archives` | Completed/inactive content |
| `08 - books` | Book notes and clippings |
| `99 - Meta` | Templates, settings |
| `Clippings` | Web clips and imports |

## Quick Reference

### Linking Syntax

```markdown
[[Note Name]]                    # Basic wikilink
[[Note Name|Display Text]]       # Aliased link
[[Note Name#Heading]]            # Link to heading
[[Note Name#^block-id]]          # Link to block
![[Note Name]]                   # Embed note
![[image.png]]                   # Embed image
![[Note Name#Heading]]           # Embed section
```

### Frontmatter Template

```yaml
---
created: {{date:YYYY-MM-DDTHH:mm}}
updated: {{date:YYYY-MM-DDTHH:mm}}
title: "Note Title"
type: note
status: draft
tags:
  - tag1
  - tag2
aliases:
  - "Alternate Name"
cssclasses:
  - custom-class
---
```

### Callouts

```markdown
> [!note] Title
> Content

> [!warning] Important
> Warning content

> [!tip] Helpful tip
> Tip content

> [!info]+ Collapsible (open by default)
> Content

> [!danger]- Collapsed by default
> Content
```

**Available callout types**: note, abstract, info, todo, tip, success, question, warning, failure, danger, bug, example, quote

## Creating Notes

### Daily Note

Create in `06 - Daily/YYYY/MM/` with filename `YYYYMMDD.md`:

```yaml
---
created: 2025-12-09T09:00
updated: 2025-12-09T09:00
title: "20251209"
type: daily-note
status: true
tags:
  - daily
  - journal
  - 2025
  - 2025-12
aliases:
  - "2025-12-09"
date_formatted: 2025-12-09
topics:
  - "[[daily]]"
  - "[[journal]]"
related:
  - "[[2025-12-08]]"
  - "[[2025-12-10]]"
cssclasses:
  - daily
---

# Daily Note - 2025-12-09

### Tasks
- [ ] Task 1

### Journal
...

### Navigation
<< [[2025-12-08]] | **Today** | [[2025-12-10]] >>
```

### Zettelkasten Note

Create in `04 - Permanent/`:

```yaml
---
created: {{date}}
type: zettelkasten
tags:
  - permanent
  - topic
---

# Note Title

## Main Insight
**Key Idea**: [Main point]

## Connections
- [[Related Note 1]]
- [[Related Note 2]]

## References
- Source citation
```

## Dataview Queries

For dataview query syntax, see [references/dataview.md](references/dataview.md).

**Quick examples:**

```dataview
LIST FROM "06 - Daily" WHERE file.cday = date(today) SORT file.ctime DESC
```

```dataview
TABLE status, tags FROM "01 - Projects" WHERE status != "completed"
```

## Templates

Templates location: `99 - Meta/00 - Templates/`

For Templater syntax, see [references/templater.md](references/templater.md).

**Common Templater variables:**

```markdown
<% tp.file.title %>              # Current file name
<% tp.date.now("YYYY-MM-DD") %>  # Current date
<% tp.file.cursor(1) %>          # Cursor position
<% tp.system.prompt("Question") %> # User input prompt
```

## Installed Plugins

| Plugin | Purpose |
|--------|---------|
| **Dataview** | Query and display data from notes |
| **Templater** | Advanced templates with scripting |
| **Auto Note Mover** | Auto-organize notes by tags |
| **Periodic Notes** | Daily/weekly/monthly notes |
| **Kanban** | Kanban boards in markdown |
| **Tag Wrangler** | Bulk tag management |
| **Table Editor** | Markdown table editing |
| **Advanced URI** | Deep links to notes |
| **Local REST API** | External API access |

## File Operations

### Creating a Note

1. Determine appropriate folder based on note type
2. Add proper frontmatter
3. Use consistent naming conventions
4. Include relevant tags for auto-organization

### Best Practices

- Use descriptive filenames (avoid special characters except hyphens)
- Always include `created` and `updated` timestamps
- Tag notes for discoverability
- Link to related notes bidirectionally
- Use callouts for important information
- Include navigation links in daily notes

## Advanced Features

- **Dataview queries**: [references/dataview.md](references/dataview.md)
- **Templater scripting**: [references/templater.md](references/templater.md)
- **Canvas diagrams**: [references/canvas.md](references/canvas.md)
- **Plugin configurations**: [references/plugins.md](references/plugins.md)
