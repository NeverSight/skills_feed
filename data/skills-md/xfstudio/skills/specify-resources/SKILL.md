---
name: specify-resources
description: Shared resources (scripts, templates) for Spec-Driven Development workflow. This skill is a dependency for all spec-* skills and should NOT be invoked directly by users. It provides bash scripts for feature branch management, prerequisite checking, and templates for specifications, plans, tasks, and checklists.
---

# Specify Resources

Shared scripts and templates for the Spec-Driven Development workflow. This skill is automatically referenced by other spec-* skills.

## Directory Structure

After initializing in a project, the `.specify/` directory structure should be:

```
.specify/
├── memory/
│   └── constitution.md      # Project principles and constraints
├── scripts/
│   └── bash/
│       ├── common.sh              # Shared functions
│       ├── check-prerequisites.sh # Validate feature environment
│       ├── create-new-feature.sh  # Initialize new feature branch
│       ├── setup-plan.sh          # Setup planning phase
│       └── update-agent-context.sh # Update AI agent context files
└── templates/
    ├── spec-template.md      # Feature specification template
    ├── plan-template.md      # Implementation plan template
    ├── tasks-template.md     # Task list template
    ├── checklist-template.md # Checklist template
    └── ...
```

## Setup Instructions

To use spec-* skills in a new project:

1. Create `.specify/` directory structure:
```bash
mkdir -p .specify/{memory,scripts/bash,templates}
```

2. Copy scripts from this skill's `scripts/bash/` to `.specify/scripts/bash/`

3. Copy templates from this skill's `references/templates/` to `.specify/templates/`

4. Copy constitution template from `references/memory/constitution.md` to `.specify/memory/`

5. Make scripts executable:
```bash
chmod +x .specify/scripts/bash/*.sh
```

## Scripts Reference

### check-prerequisites.sh

Validates feature environment and returns paths.

```bash
# JSON output with feature directory and available docs
.specify/scripts/bash/check-prerequisites.sh --json

# Require tasks.md to exist
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks

# Paths only (no validation)
.specify/scripts/bash/check-prerequisites.sh --json --paths-only
```

### create-new-feature.sh

Creates new feature branch and spec directory.

```bash
.specify/scripts/bash/create-new-feature.sh --json "Feature description" --short-name "feature-name"
```

### setup-plan.sh

Initializes planning phase for a feature.

```bash
.specify/scripts/bash/setup-plan.sh --json
```

### update-agent-context.sh

Updates AI agent context files with project information.

```bash
.specify/scripts/bash/update-agent-context.sh claude
```

## Templates Reference

- **spec-template.md**: Feature specification with user stories, requirements, success criteria
- **plan-template.md**: Implementation plan with technical context, project structure
- **tasks-template.md**: Task list organized by user story with dependency tracking
- **checklist-template.md**: Quality validation checklist template
- **constitution.md**: Project principles and governance rules
