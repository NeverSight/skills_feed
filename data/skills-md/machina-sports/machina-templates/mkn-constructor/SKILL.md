---
name: mkn-constructor
description: Construct and scaffold Machina agent-templates and connectors with correct YAML structure, then install them via MCP. Use when users ask to "create a template", "scaffold an agent", "init template", "build a new connector", "install template", "validate template", "analyze template", "trace agent", or "configure secrets".
---

# Template Constructor

End-to-end skill for building, validating, and deploying Machina agent-templates and connectors.

## References

Procedural guides for each lifecycle stage:

| Reference | Description |
|-----------|-------------|
| [init.md](references/init.md) | Scaffold new template project from scratch |
| [create.md](references/create.md) | Generate individual YAML components |
| [validate.md](references/validate.md) | Check YAML files against correct patterns |
| [install.md](references/install.md) | Import templates via MCP (local or Git) |
| [analyze.md](references/analyze.md) | Analyze template structure and dependencies |
| [trace.md](references/trace.md) | Trace agent execution chain with variable propagation |
| [secrets.md](references/secrets.md) | Configure vault secrets for connectors |
| [api.md](references/api.md) | MCP operations for all entities (CRUD, execute, search) |
| [yaml-reference.md](references/yaml-reference.md) | Complete YAML syntax and patterns |
| [connectors.md](references/connectors.md) | All available connectors with docs |
| [frontend-api.md](references/frontend-api.md) | Next.js frontend API integration |

## Schemas

Authoritative field definitions for every Machina entity:

| Schema | Entity |
|--------|--------|
| [agent.md](schemas/agent.md) | Agent definition |
| [connector.md](schemas/connector.md) | Connector (PyScript + REST API) |
| [document.md](schemas/document.md) | Document task type |
| [mapping.md](schemas/mapping.md) | Data transformation mapping |
| [prompt.md](schemas/prompt.md) | Prompt definition + JSON Schema |
| [setup.md](schemas/setup.md) | `_install.yml` + `_index.yml` |
| [skill.md](schemas/skill.md) | SDK skill registration |
| [workflow.md](schemas/workflow.md) | Workflow + task types |

## Intent Routing

When the user triggers this skill, load the appropriate reference:

| User Says | Reference |
|-----------|-----------|
| "init template", "scaffold template", "new template project" | [init.md](references/init.md) |
| "create agent", "create workflow", "scaffold YAML" | [create.md](references/create.md) |
| "validate", "check YAML", "verify template" | [validate.md](references/validate.md) |
| "install", "import", "deploy template" | [install.md](references/install.md) |
| "analyze", "what's in this template", "overview" | [analyze.md](references/analyze.md) |
| "trace", "execution chain", "variable flow", "debug agent" | [trace.md](references/trace.md) |
| "secrets", "credentials", "configure API key" | [secrets.md](references/secrets.md) |
| "API", "MCP operations", "search agents", "execute workflow" | [api.md](references/api.md) |
| "YAML syntax", "task types", "expression syntax", "foreach" | [yaml-reference.md](references/yaml-reference.md) |
| "connectors", "list connectors", "connector docs" | [connectors.md](references/connectors.md) |
| "frontend", "Next.js", "API integration", "document search" | [frontend-api.md](references/frontend-api.md) |
| "report bug", "found issue", "feedback", "suggest improvement" | Show **Feedback & Contributing** section below |

For YAML field specifics, read the relevant schema from `schemas/`.

## Workflow

**Name**: `mkn-constructor-check-setup`

Validates that the `doc-structure` document exists and returns its content.

| Input | Default | Description |
|-------|---------|-------------|
| `document_name` | `doc-structure` | Document to check |

| Output | Description |
|--------|-------------|
| `doc-structure` | Document content |
| `check-status` | Workflow execution status |

## Feedback & Contributing

Found a bug, unexpected behavior, or have an improvement idea while using this skill?

- **Report issues**: [Open an issue](https://github.com/machina-sports/machina-templates/issues/new?labels=skill:mkn-constructor) with the label `skill:mkn-constructor`
- **Contribute fixes**: Fork the repo, apply your fix, and [open a PR](https://github.com/machina-sports/machina-templates/pulls) against `main`
- **What to include**: Describe what you expected vs. what happened. For schema/reference fixes, include before/after YAML examples.

When the user encounters an error, unexpected scaffold output, or expresses frustration with a skill behavior, proactively mention this section and suggest opening an issue.

## Key Constraints

- **Connector .py files**: No helper functions outside command functions. Each function must be self-contained.
- **Expression syntax**: Always use `$.get('field')` — never `${field}` or `$field`
- **Prompt files**: Use `prompts:` array (not `prompt:`) with `instruction:` (not `messages:`)
- **Connector YAML**: Use `filetype:` (not `type:`) and `filename:` (not `script:`)
- **Install order**: connectors → documents → prompts → mappings → workflows → agents → skills
