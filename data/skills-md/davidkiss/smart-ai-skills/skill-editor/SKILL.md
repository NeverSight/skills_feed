---
name: skill-editor
description: Creates, updates, and manages Agent Skills following the Claude Code style. Use this skill when the user wants to add a new capability, create a new skill, or modify an existing skill.
---

# Skills Editor Skill

## Description

This skill enables the agent to create and maintain "Agent Skills" - modular capabilities that extend the agent's functionality. It ensures that all skills follow the standardized directory structure and file format required by the deepagents environment.

## When to Use

- When the user asks to "create a skill" or "add a capability".
- When the user wants to package a specific workflow (e.g., "teach the agent how to handle PDF invoices").
- When modifying existing skills to add new resources or update instructions.

## Skill Structure Rules

Every skill must reside in its own directory and contain a `SKILL.md` file.

### 1. Directory Structure
Create a new directory for the skill (e.g., `pdf-processing/`).
Inside, the `SKILL.md` is mandatory. Other files are optional but recommended for complex tasks to keep the context window light (Progressive Disclosure).

```text
skill-name/
├── SKILL.md          # (Required) Main instructions and metadata
├── REFERENCE.md      # (Optional) Detailed API docs or reference material
├── FORMS.md          # (Optional) Specialized guides
└── scripts/          # (Optional) Executable scripts
    └── utility.py
```

### 2. SKILL.md Format
The `SKILL.md` file **must** start with YAML frontmatter, followed by markdown instructions.

**Frontmatter Requirements:**
- `name`: Max 64 chars, lowercase letters, numbers, and hyphens only. No reserved words ("anthropic", "claude").
- `description`: Max 1024 chars. Must explain **what** the skill does and **when** to use it.

**Content Sections:**
- `# [Skill Name]`
- `## Instructions`: Step-by-step guidance.
- `## Examples`: Concrete usage examples.

## Instructions - How to Create a Skill
MUST use the `todowrite` and `todoread` tools to track progress of the execution of the below steps:

### Step 1: Check for Similar Online Skills
Before creating or editing a skill, MUST run a quick web-search (use the `webfetch` tool) to find any existing, similar skills online (for example, Anthropic's official skills at https://github.com/anthropics/skills/tree/main/skills or community-maintained lists). If similar skills are found:
  - If the license and terms allow reuse, prefer adapting them as a template and include a clear reference/link in the new skill's SKILL.md ("Based on: <url>").
  - If the license requires attribution or imposes conditions, include the original LICENSE.txt (or a pointer) in the new skill directory and follow the license terms. If the license is incompatible with your intended use, notify the user and request guidance before importing.

### Step 2: Check for Existing Skills
Before creating a new skill and not using an online skill as a template, search for existing or similar local skills and reuse their structure, examples, and patterns as a starting point.

### Step 3: Create the Directory
Create a directory under `.opencode/skills/` with a kebab-case name matching the skill's purpose.

### Step 4: Create SKILL.md
Write the `SKILL.md` file with the required frontmatter and sections.

**Template:**
```markdown
---
name: my-new-skill
description: Brief description of what this skill does and when to use it.
---

# My New Skill

## Instructions
[Clear, step-by-step guidance for the agent to follow]

## Examples
[Concrete examples of using this skill]
```

### Step 5: Add Supporting Files (Optional)
If the skill requires large reference texts or scripts, create separate files (e.g., `scripts/main.py`, `docs/api.md`) and reference them in `SKILL.md`. The agent will read these only when needed.

### Step 6: Update dependencies (Optional)

Add any required dependencies to the project's `requirements.txt` file using `uv pip install <package>` so the project's virtual environment is updated.

### Step 7: Highlight necessary environment variables (Optional)

If a skill's scripts require environment variables (API keys, tokens, credentials), list them clearly in the SKILL.md `Credentials` section with the expected variable names (e.g., `GITHUB_ACCESS_TOKEN`, `YOUTUBE_API_KEY`). When creating a new skill, surface these required env vars to the user and advise adding them to the project's .env file or system environment before running the scripts.

## Best Practices

- **Progressive Disclosure**: Don't put everything in `SKILL.md`. Use it as an entry point that links to other files.
- **Deterministic Code**: Prefer Python scripts for complex logic or data processing over natural language instructions.
- **Concise Scripts**: When creating script files, keep them concise—clear purpose, small functions, minimal external dependencies, and avoid unnecessary complexity.
- **Clear Triggers**: Ensure the `description` clearly states *when* the skill should be used so the router can pick it up correctly.
- **Confirm changes**: Confirm changes with the user before executing any steps.
