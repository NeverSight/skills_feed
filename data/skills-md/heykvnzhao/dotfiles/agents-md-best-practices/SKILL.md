---
name: agents-md-best-practices
description: Refactor AGENTS.md instructions to follow progressive disclosure and AGENTS.md best practices. Use when asked to audit, reorganize, or split AGENTS.md into a minimal root file plus linked docs; includes contradiction checks, essential extraction, grouping, and deletion flags.
---

# Agents MD Best Practices

## Overview

Refactor an AGENTS.md into a minimal root file with links to focused docs, following progressive disclosure. Produce contradictions to resolve, a root essentials set, grouped files, a suggested docs/ structure, and deletion flags.

## Workflow

### 0) Gather inputs

- Ask which AGENTS.md to refactor (path or pasted content).
- Ask whether to apply file changes or draft only.
- Ask where to place new docs/ (default: `docs/agents/`).

### 1) Parse and normalize

- Read the AGENTS.md content.
- Split into individual instructions (one per line/bullet/paragraph).
- Keep original wording; annotate with a short label so you can reference items precisely.

### 2) Find contradictions

- Identify instructions that conflict (opposing directives, incompatible tools, or contradictory constraints).
- Present each contradiction as a pair (or set) and ask which to keep.
- Pause before restructuring until contradictions are resolved.

### 3) Identify essentials for root AGENTS.md

Keep only what belongs in the root file:
- One-sentence project description.
- Package manager if not npm.
- Non-standard build/typecheck commands.
- Anything truly relevant to every single task.

Ask if the user wants any other item in root before finalizing.

### 4) Group the rest into categories

- Cluster remaining instructions into logical, named categories (e.g., TypeScript, Testing, API design, Git workflow, UI, Infra).
- Create a separate markdown file per category.
- Keep categories actionable and scoped; avoid mixed topics.

### 5) Create the file structure

Provide:
- A minimal root `AGENTS.md` with markdown links to the category files.
- Each category file with its relevant instructions.
- A suggested `docs/` folder structure.

Use the template in `references/output-template.md` when helpful.

### 6) Flag for deletion

Identify instructions that are:
- Redundant (agent already knows this).
- Too vague to be actionable.
- Overly obvious (e.g., “write clean code”).

List these separately with a short reason and ask for confirmation before removing.

## Output requirements

- If no contradictions, explicitly say “No contradictions found.”
- Use clear section headings in the response: Contradictions, Root AGENTS.md, New Files, Suggested docs/ Structure, Flags for Deletion.
- Provide file contents in fenced code blocks with filenames.

## Guardrails

- Do not delete or rewrite instructions without user confirmation when conflicts exist or items are flagged.
- Do not expand scope beyond the AGENTS.md content unless the user asks.
