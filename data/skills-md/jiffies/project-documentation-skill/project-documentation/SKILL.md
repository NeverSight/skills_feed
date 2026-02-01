---
name: project-documentation
description: >
  Create high-quality README and system documentation for software projects.
  Use when you need to: (1) Write or update project README documentation,
  (2) Add system operation principle flowcharts using Mermaid,
  (3) Write detailed step-by-step usage instructions,
  (4) Organize and optimize configuration descriptions (environment variables, config files),
  (5) Make documentation more user-friendly and easier to understand.
  Applicable to open-source projects, internal tools, API services,
  and any project requiring improved documentation.
---

# Project Documentation

Create clear, complete, and user-friendly README and system documentation for software projects.

## Core Capabilities

This skill helps you create high-quality project documentation with:

1. **Mermaid Flowcharts** - Visualize system operation principles
2. **Step-by-Step Instructions** - Detailed beginner-friendly guides
3. **Configuration Documentation** - Clear organization of environment variables and config files

## Workflow

### 1. Understand the Project

Before writing documentation, gather essential information:

- Project's core features and purpose
- Tech stack (frontend, backend, database, external services)
- User workflows (startup process, core operations)
- External dependencies (API Keys, accounts, tools)
- Configuration items (required vs optional)

**Information sources**: README, package.json, .env.example, main code files (main.ts, app.ts, routes/)

### 2. Create Mermaid Flowcharts

Choose appropriate diagrams based on project needs:

- **Core Flow Diagram** (Required) - User operation flow from startup to task completion
- **Data Flow Diagram** (Recommended) - System component interactions and API calls
- **Technical Architecture Diagram** (Recommended) - Tech stack and layered structure

**Complete templates and patterns**: See [references/mermaid-patterns.md](references/mermaid-patterns.md)

### 3. Write Step-by-Step Instructions

Organize usage steps in this sequence:

1. Prerequisites (software, accounts, tools)
2. Clone project and install dependencies
3. Obtain external service credentials (if needed)
4. Configure environment variables
5. Initialize system (if needed)
6. Start services
7. Use features
8. Verify system operation

**Each step should include**: Purpose, commands, expected output, tips, and warnings.

**Complete writing guide**: See [references/step-by-step-guide.md](references/step-by-step-guide.md)

### 4. Organize Configuration Documentation

Structure .env.example with clear separators:

```bash
# ========================================
# Main Category Title
# ========================================
CONFIG_ITEM=example_value

# ----------------------------------------
# Subcategory Title
# ----------------------------------------
CONFIG_ITEM=example_value
```

Document each configuration item with:
- Required vs optional status
- Purpose and usage
- Acquisition method (for external services)
- Default values
- Complete examples

**Complete organization guide**: See [references/config-organization.md](references/config-organization.md)

### 5. Recommended README Structure

```markdown
# Project Name - Brief Description
## Features
## System Operation Principles (Mermaid diagrams)
## Quick Start (Step by Step)
## Common Commands
## API Examples
## Tech Stack
## Project Structure
## Documentation
## Important Notes
## License
```

## Quality Checklist

Before finalizing documentation:

**Flowcharts**:
- [ ] Core flow shows user operations clearly
- [ ] Data flow reflects system interactions accurately
- [ ] Architecture diagram shows complete tech stack
- [ ] Appropriate colors and moderate complexity (<20 nodes)

**Usage Steps**:
- [ ] Complete prerequisites list
- [ ] Clear titles and purpose for each step
- [ ] Copy-paste ready commands
- [ ] Expected output explained
- [ ] Common problem tips included

**Configuration**:
- [ ] Required vs optional clearly marked
- [ ] Purpose explained for each item
- [ ] Acquisition methods provided
- [ ] Clear separators and grouping
- [ ] Multi-option comparisons (if applicable)

**User-Friendliness**:
- [ ] Clear icons used (✅ ⚠️ 💡)
- [ ] Multiple options provided (if applicable)
- [ ] Troubleshooting tips included
- [ ] Concise and clear language
- [ ] All links accessible

## Reference Resources

- **[mermaid-patterns.md](references/mermaid-patterns.md)** - Flowchart design patterns and templates
- **[step-by-step-guide.md](references/step-by-step-guide.md)** - Step-by-step instruction writing guide
- **[config-organization.md](references/config-organization.md)** - Configuration documentation organization guide
- **[complete-example.md](examples/complete-example.md)** - Complete documentation example with all three diagram types

## Best Practices

1. **User Perspective First** - Assume zero background knowledge
2. **Actionability** - All commands should be copy-pasteable
3. **Completeness** - Include all necessary information
4. **Clarity** - Use diagrams, tables, code blocks
5. **Verifiability** - Provide verification steps

## Common Scenarios

**New Project**: Understand structure → Create diagrams → Write steps → Organize config → Verify quality

**Update Existing**: Read current README → Identify gaps → Add/optimize content → Verify quality

**Optimize Config**: Group by function → Add separators → Mark required/optional → Link acquisition methods
