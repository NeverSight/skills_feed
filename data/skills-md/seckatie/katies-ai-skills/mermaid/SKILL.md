---
name: mermaid
description: Generate diagrams and flowcharts from mermaid definitions using the mermaid-cli (mmdc). Supports themes, custom CSS, and various output formats including SVG, PNG, and PDF. Mermaid supports 20+ diagram types including flowcharts, sequence diagrams, class diagrams, state diagrams, entity relationship diagrams, user journeys, Gantt charts, pie charts, quadrant charts, requirement diagrams, GitGraph, C4 diagrams, mindmaps, timelines, ZenUML, Sankey diagrams, XY charts, block diagrams, packet diagrams, Kanban boards, architecture diagrams, radar charts, and treemaps. This skill is triggered when the user says things like "create a diagram", "make a flowchart", "generate a sequence diagram", "create a mermaid chart", "visualize this as a diagram", "render mermaid code", or "create an architecture diagram".
---

# Mermaid Documentation Guide

Mermaid is a JavaScript-based diagramming and charting tool that uses text definitions to create diagrams dynamically. This skill includes the complete official documentation from the mermaid repository.

**Quick Start:** Read mermaid-cli/README.md for installation and usage. Always use mermaid-cli to validate code and generate diagrams. Adjust width/height for readability (default PNGs are often too small).

## Documentation Structure

### Quick Start
- **mermaid-README.md** - Main Mermaid project README with overview, features, and quick examples

### Getting Started
- **intro/getting-started.md** - Quick start guide for using Mermaid
- **intro/index.md** - Introduction and overview
- **intro/syntax-reference.md** - General syntax reference across all diagram types
- **config/usage.md** - How to use Mermaid in different environments

### Installation and CLI
- **mermaid-cli/README.md** - Complete mermaid-cli (mmdc) installation and usage guide
- **config/mermaidCLI.md** - Additional CLI usage information from the main docs
- **config/setup/** - Setup instructions for different environments

### CLI Troubleshooting
- **mermaid-cli/already-installed-chromium.md** - Using already-installed Chromium instead of downloading
- **mermaid-cli/linux-sandbox-issue.md** - Fixing Linux sandbox issues
- **mermaid-cli/docker-permission-denied.md** - Fixing Docker permission issues
- **mermaid-cli/reviewing.md** - Code review guidelines for mermaid-cli

### Diagram Type Syntax
For detailed syntax, examples, and best practices for each diagram type, refer to files in the `syntax/` folder:

#### Core Diagrams
- **syntax/flowchart.md** - Process flows, decision trees, and workflows with various node shapes and arrow types
- **syntax/sequenceDiagram.md** - Actor interactions over time, showing message flows and activations
- **syntax/classDiagram.md** - Object-oriented structures with classes, attributes, methods, and relationships
- **syntax/stateDiagram.md** - State machines showing states and transitions
- **syntax/entityRelationshipDiagram.md** - Database schemas and data model relationships

#### Planning & Project Management
- **syntax/userJourney.md** - User experience mapping with satisfaction scores
- **syntax/gantt.md** - Project schedules, timelines, and task dependencies
- **syntax/kanban.md** - Workflow visualization with columns and cards
- **syntax/timeline.md** - Chronological events and project histories
- **syntax/requirementDiagram.md** - System requirements and verification methods

#### Data Visualization
- **syntax/pie.md** - Data proportions and percentages
- **syntax/quadrantChart.md** - 2x2 prioritization and analysis matrices
- **syntax/xyChart.md** - Line and bar charts for data trends
- **syntax/sankey.md** - Flow quantities and data transfers between stages

#### Technical Diagrams
- **syntax/gitgraph.md** - Git branching, merging, and workflow patterns
- **syntax/c4.md** - Software architecture at multiple abstraction levels
- **syntax/block.md** - System components and relationships
- **syntax/packet.md** - Network packet structures and protocol headers
- **syntax/architecture.md** - System design with icons and groupings

#### Advanced & Specialized
- **syntax/mindmap.md** - Hierarchical information and brainstorming
- **syntax/zenuml.md** - Alternative sequence diagram syntax with code-like format
- **syntax/radar.md** - Multi-axis comparisons
- **syntax/treemap.md** - Hierarchical data as nested rectangles

### Configuration and Customization
- **config/configuration.md** - Mermaid configuration options
- **config/theming.md** - Theme customization and styling
- **config/directives.md** - Using directives in diagrams
- **config/icons.md** - Using icons in diagrams
- **config/layouts.md** - Layout configuration options
- **config/math.md** - Mathematical expressions in diagrams
- **config/accessibility.md** - Accessibility features and best practices

### Troubleshooting and FAQs
- **config/faq.md** - Frequently asked questions
- **syntax/examples.md** - Collection of example diagrams

## Common Usage Patterns

When the user asks to:
- **Get an overview** → Check `mermaid-README.md`
- **Create a flowchart** → Check `syntax/flowchart.md`
- **Create a sequence diagram** → Check `syntax/sequenceDiagram.md`
- **Create a class diagram** → Check `syntax/classDiagram.md`
- **Create a Gantt chart** → Check `syntax/gantt.md`
- **Create an ER diagram** → Check `syntax/entityRelationshipDiagram.md`
- **Customize appearance** → Check `config/theming.md` and `config/configuration.md`
- **Install or use the CLI** → Check `mermaid-cli/README.md`
- **Use the CLI (additional info)** → Check `config/mermaidCLI.md`
- **Troubleshoot CLI issues** → Check `mermaid-cli/linux-sandbox-issue.md`, `mermaid-cli/already-installed-chromium.md`, or `mermaid-cli/docker-permission-denied.md`
- **Troubleshoot general issues** → Check `config/faq.md`
- **See examples** → Check `syntax/examples.md`
- **Learn syntax basics** → Check `intro/syntax-reference.md`

## Using Mermaid CLI

The mermaid-cli (mmdc) is the command-line tool for generating diagrams. For complete installation and usage details, see `mermaid-cli/README.md`.

### Basic CLI Usage
```bash
# Generate PNG from mermaid file
mmdc -i input.mmd -o output.png

# Generate SVG
mmdc -i input.mmd -o output.svg

# Generate PDF
mmdc -i input.mmd -o output.pdf

# Specify theme
mmdc -i input.mmd -o output.png -t dark

# Specify background color
mmdc -i input.mmd -o output.png -b transparent

# Specify width
mmdc -i input.mmd -o output.png -w 1920

# Specify height
mmdc -i input.mmd -o output.png -H 1080
```

**Important Notes:**
- By default, PNG files might be too small. Adjust width and height to be large enough to be readable.
- Always test diagrams with mermaid-cli to validate syntax before finalizing.
- PNG output typically requires explicit width/height for good quality.

## Quick Reference by Use Case

### For Basic Diagram Creation
1. Choose the diagram type from the syntax/ folder
2. Read the syntax documentation for that type
3. Create your .mmd file with the diagram definition
4. Generate output using mmdc command

### For Styling and Theming
1. Check `config/theming.md` for theme options
2. Check `config/configuration.md` for global settings
3. Use directives (see `config/directives.md`) for inline configuration

### For Integration
1. Check `config/usage.md` for embedding in web pages
2. Check `mermaid-cli/README.md` for command-line usage
3. Check `intro/getting-started.md` for basic setup

### For Troubleshooting
1. Check `config/faq.md` first for general issues
2. Check `mermaid-cli/` folder for CLI-specific troubleshooting (Linux sandbox, Chromium, Docker)
3. Validate syntax against the specific diagram type documentation
4. Check `syntax/examples.md` for working examples
5. Review `config/accessibility.md` for rendering issues

## Common Troubleshooting Tips

### Line Breaks & Multi-line Text
- ✅ Use `<br/>` for line breaks: `Node["Text<br/>More text"]`
- ✅ Use `<br/><br/>` for paragraph spacing
- ❌ Never use plain newlines (`\n`) - causes "Unsupported markdown: list" errors
- Keep bullet points concise (2-4 words), limit to 3-4 per node

### Text & Canvas Size
- Increase font size: `classDef style font-size:20px`
- Vertical flowcharts: `mmdc -i file.mmd -o file.png -w 2000 -H 2800`
- Horizontal flowcharts: `mmdc -i file.mmd -o file.png -w 3000 -H 1400`

### Special Characters
- Avoid starting labels with numbers
- Escape quotes with `\"`
- **Ampersands**: Avoid `&` (renders as `&amp;`) - use "and" or "+" instead
- Use `&lt;` for <, `&gt;` for > only when necessary

## General Tips

- Start with the appropriate diagram type for your use case
- Refer to the specific diagram documentation in syntax/ for detailed syntax
- Test diagrams with mermaid-cli before finalizing
- Use consistent formatting and naming conventions
- Add comments with `%%` for documentation
- Consider your audience when choosing detail level
- Check the intro/syntax-reference.md for cross-diagram syntax patterns

## File Organization

- **mermaid-README.md** - Main Mermaid project README
- **mermaid-cli/** - Complete mermaid-cli documentation and troubleshooting
- **intro/** - Getting started guides and general reference
- **syntax/** - Complete syntax documentation for all diagram types
- **config/** - Configuration, theming, CLI, and troubleshooting
- **diagrams/** - Additional diagram documentation and examples
- **ecosystem/** - Information about the Mermaid ecosystem
- **community/** - Community resources and contributions

## Notes

- Some diagram types may be experimental or have evolving syntax
- Always validate your diagrams with the mermaid-cli tool
- The official documentation is continuously updated
- For the latest updates, refer to https://mermaid.js.org/
