---
name: agents-md-generator
description: Analyze repository structure and generate standardized AGENTS.md files that serve as contributor guides for AI agents. Measures LOC to determine character limits and produces 5-section documents covering overview, folder structure, patterns, conventions, and working agreements.
license: MIT
---

# AGENTS.md Generation Capability

This skill enables the agent to generate `AGENTS.md` files that serve as contributor guides for AI agents working on a codebase.

## Core Capability

- **Function**: Analyze repository structure and generate a standardized `AGENTS.md` document
- **Output Format**: Markdown file with structured sections
- **Character Limit**: Dynamic, based on repository LOC (Lines of Code)

## Output Sections

The generated `AGENTS.md` consists of exactly 5 sections:

| # | Section | Purpose |
|---|---------|---------|
| 1 | Overview | 1-2 sentence project description (abstract, no tool/framework lists) |
| 2 | Folder Structure | Key directories and their contents |
| 3 | Core Behaviors & Patterns | Logging, error handling, control flow patterns observed in code |
| 4 | Conventions | Naming, comments, code style derived from analysis |
| 5 | Working Agreements | Rules for agent behavior and communication |

## Domain Knowledge

- **LOC Measurement**: Capability to measure repository size and determine character limits. See [./references/loc_measurement.md](./references/loc_measurement.md)
- **Repository Analysis**: Capability to inspect and understand codebase structure. See [./references/read_only_commands.md](./references/read_only_commands.md)
- **Output Template**: Standardized AGENTS.md structure specification. See [./references/agents_md_template.md](./references/agents_md_template.md)
- **Working Agreements**: Agent behavior rules for generated documents. See [./references/working_agreements.md](./references/working_agreements.md)

## Constraints

- **Read-Only Analysis**: Repository inspection uses only non-destructive commands
- **No Run/Test/Build/Deploy**: Generated AGENTS.md excludes execution instructions
- **Files to Ignore**: Lock files (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, etc.)
