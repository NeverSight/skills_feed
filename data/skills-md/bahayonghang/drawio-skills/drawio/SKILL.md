---
name: drawio
version: 2.0.0
description: AI-powered Draw.io diagram generation with Design System, 3 workflows, and real-time browser preview
category: visual-design
tags: [diagram, flowchart, architecture, drawio, design-system]
---

# Draw.io Skill

AI-powered Draw.io diagram generation with real-time browser preview for Claude Code.

## Quick Start

| What you want to do | Command | Description |
|---------------------|---------|-------------|
| Create new diagram | `/drawio-create` | Natural language → diagram |
| Replicate image | `/drawio-replicate` | Image → A-H → diagram |
| Edit diagram | `/drawio-edit` | Modify existing diagram |

> **Tip**: You can also use natural language keywords like "create", "replicate", "edit" to trigger workflows.

## Features

- **Design System** - Unified visual language with themes, tokens, and semantic shapes
- **Real-time Preview** - Diagrams update in browser as Claude creates them
- **Version History** - Restore previous diagram versions
- **Natural Language** - Describe diagrams in plain text
- **Cloud Architecture** - AWS, GCP, Azure with official icons
- **Animated Connectors** - Dynamic connector animations
- **Semantic Shapes** - Auto-select shapes based on node type
- **Math Typesetting** - LaTeX/AsciiMath equations in labels
- **IEEE Academic Style** - Publication-ready diagrams

## Design System

The skill includes a unified design system providing consistent visual language:

### Themes

| Theme | Use Case |
|-------|----------|
| **Tech Blue** | Software architecture, DevOps (default) |
| **Academic Color** ⭐ | Academic papers, research (recommended) |
| **Academic** | IEEE grayscale print only |
| **Nature** | Environmental, lifecycle diagrams |
| **Dark Mode** | Presentations, slides |

### Semantic Shapes

Automatic shape selection based on node type:

```yaml
nodes:
  - id: api
    label: API Gateway
    type: service     # → Rounded rectangle

  - id: db
    label: User Database
    type: database    # → Cylinder

  - id: check
    label: Valid?
    type: decision    # → Diamond
```

### Typed Connectors

| Type | Style | Usage |
|------|-------|-------|
| `primary` | Solid 2px, filled arrow | Main flow |
| `data` | Dashed 2px, filled arrow | Data/async flow |
| `optional` | Dotted 1px, open arrow | Weak relation |
| `dependency` | Solid 1px, diamond | Dependencies |

### 8px Grid System

All spacing and positions align to 8px grid for professional results:
- Node margin: 32px minimum
- Container padding: 24px
- Canvas padding: 32px

→ [Full Design System Documentation](docs/design-system/README.md)

## Installation

MCP server auto-configures on first use:

```json
{
  "command": "npx",
  "args": ["--yes", "@next-ai-drawio/mcp-server@latest"]
}
```

Default port: `6002` (auto-increments if in use)

For manual setup, see [scripts/](scripts/).

## MCP Tools

| Tool | Description |
|------|-------------|
| `start_session` | Opens browser with real-time preview |
| `create_new_diagram` | Create diagram from XML |
| `edit_diagram` | Edit by ID-based operations |
| `get_diagram` | Get current diagram XML |
| `export_diagram` | Save to `.drawio` file |

Details: [docs/mcp-tools.md](docs/mcp-tools.md)

## Workflows

### `/drawio-create` - Create from Scratch

Create diagrams from natural language descriptions.

```
/drawio-create a login flowchart with validation and error handling
```

**A-H format**: Optional (use `--structured` for complex diagrams)

→ [Full workflow](workflows/create.md)

### `/drawio-replicate` - Replicate Existing

Recreate images/screenshots using structured A-H extraction.

```
/drawio-replicate
【领域】软件架构
[Upload image]
```

**A-H format**: Required

→ [Full workflow](workflows/replicate.md)

### `/drawio-edit` - Modify Diagram

Edit existing diagrams with natural language instructions.

```
/drawio-edit
Change "User Service" to "Auth Service"
Make database nodes green
```

**A-H format**: Optional (use for structural changes)

→ [Full workflow](workflows/edit.md)

## Documentation

### Design System

| Topic | File |
|-------|------|
| Design System Overview | [docs/design-system/README.md](docs/design-system/README.md) |
| Design Tokens | [docs/design-system/tokens.md](docs/design-system/tokens.md) |
| Themes | [docs/design-system/themes.md](docs/design-system/themes.md) |
| Semantic Shapes | [docs/design-system/shapes.md](docs/design-system/shapes.md) |
| Connectors | [docs/design-system/connectors.md](docs/design-system/connectors.md) |
| Icons | [docs/design-system/icons.md](docs/design-system/icons.md) |
| Formulas | [docs/design-system/formulas.md](docs/design-system/formulas.md) |
| Specification Format | [docs/design-system/specification.md](docs/design-system/specification.md) |

### Reference

| Topic | File |
|-------|------|
| Math Typesetting | [docs/math-typesetting.md](docs/math-typesetting.md) |
| IEEE Diagrams | [docs/ieee-diagrams.md](docs/ieee-diagrams.md) |
| Usage Examples | [docs/examples.md](docs/examples.md) |
| XML Format | [docs/xml-format.md](docs/xml-format.md) |
| MCP Tools | [docs/mcp-tools.md](docs/mcp-tools.md) |

## Architecture

```
Claude Code <--stdio--> MCP Server <--http--> Browser (draw.io)
```

1. Ask Claude to create a diagram
2. Claude calls `start_session` to open browser
3. Claude generates diagram XML
4. Diagram appears in real-time!

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "d.setId is not a function" | Use numeric `mxCell` IDs only |
| Port already in use | Server auto-tries ports 6002-6020 |
| "No active session" | Call `start_session` first |
| Browser not updating | Check URL has `?mcp=` parameter |
| Math not rendered | Enable `Extras > Mathematical Typesetting` |

## Links

- [Homepage](https://next-ai-drawio.jiang.jp)
- [GitHub Repository](https://github.com/DayuanJiang/next-ai-draw-io)
- [MCP Server Documentation](https://github.com/DayuanJiang/next-ai-draw-io/tree/main/packages/mcp-server)

## License & Author

- **License**: Apache-2.0
- **Author**: DayuanJiang
- **Skill Version**: 1.1.0
