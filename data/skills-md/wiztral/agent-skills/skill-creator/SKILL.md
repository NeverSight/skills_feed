---
name: skill-creator
description: Create and validate new AI agent skills. This skill provides standards, templates, and validation tools to ensure high-quality, interoperable skills across different AI agents.
license: Apache-2.0
---

# Skill Creator

This skill provides guidance and tools for creating effective, high-quality, and agent-agnostic skills.

## Core Principles

1. **High Quality & Output**: Focus on clear, actionable instructions that produce reliable results.
2. **Efficiency**: Keep `SKILL.md` concise (< 500 lines) by moving heavy documentation to `references/` and automation to `scripts/`.
3. **Token Economy**: Be mindful of context usage. Use "High Density" practices where appropriate (imperative language, bullet points) but prioritize clarity.

## Directory Structure

To determine where to place a new skill, follow this priority:

1.  **User Instructions**: If the user has explicitly provided instructions on how to structure the skill or where to place it, proceed with that first.
2.  **Check README**: Read the root `README.md` if it exists and follow any stated structural guidelines.
3.  **Check `skills/` folder**: If no instructions are found, look for a `skills/` directory and follow the existing organizational pattern (e.g., `skills/[skill]/`).
4.  **Ask if Unclear**: If the location is still ambiguous or if the project might prefer skills in a different location (like the `.agent/` directory), ask the user for clarification.

### Standard Skill Structure

Once the location is determined, follow the standard folder layout:

```text
[skill-name]/
├── SKILL.md                # Required: Core instructions and metadata (< 500 lines)
├── scripts/                # Optional: Executable code for automation
├── references/             # Optional: Detailed documentation, patterns, examples
└── assets/                 # Optional: Static files for output (templates)
```

## Skill Creation Lifecycle

### 1. Plan

Define use cases and effective resource strategy. See [references/lifecycle.md](references/lifecycle.md).

### 2. Initialize

Run the initialization script to scaffold a new skill with the correct structure.

```bash
python scripts/init_skill.py <new-skill-name>
```

### 3. Edit

- **SKILL.md**: Update description (triggers) and body (core workflow).
- **Resources**: Add scripts and references. See [references/resource-organization.md](references/resource-organization.md).

### 4. Validate

Run the validation script to ensure quality and structure.

```bash
python scripts/validate_skill.py <new-skill-name>
```

## Reference & Guides

- **Template**: [references/TEMPLATE.md](references/TEMPLATE.md)
- **Lifecycle**: [references/lifecycle.md](references/lifecycle.md)
- **Organization**: [references/resource-organization.md](references/resource-organization.md)
- **Patterns**: [references/patterns.md](references/patterns.md)

## Validation Rules

- **Name**: Lowercase alphanumeric with hyphens.
- **Description**: Mandatory and detailed (used for triggering).
- **Size**: Keep `SKILL.md` concise. Move details to `references/`.
