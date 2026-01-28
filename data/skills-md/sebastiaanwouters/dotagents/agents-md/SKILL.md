---
name: agents-md
description: Create/refactor AGENTS.md files. Only trigger on `/agents-md`.
---

# AGENTS.md Creation & Refactoring

Create minimal, focused AGENTS.md files that use progressive disclosure.

## Core Principles

1. **Instruction budget**: LLMs can follow ~150-200 instructions consistently. Every token loads on every request.
2. **Progressive disclosure**: Give agents only what they need now, point elsewhere for specifics.
3. **Avoid staleness**: Don't document file paths—they change. Document capabilities and domain concepts.

## What Belongs in Root AGENTS.md

Only these essentials:

- **One-sentence project description** (anchors agent decisions)
- **Package manager** (if not npm)
- **Non-standard build/typecheck commands**

Everything else goes elsewhere.

## Refactoring Workflow

When refactoring an existing AGENTS.md:

1. **Find contradictions**: Identify conflicting instructions, ask user which to keep
2. **Extract essentials**: Pull out only what belongs at root level
3. **Group the rest**: Organize into logical categories (TypeScript, testing, API design, etc.)
4. **Create file structure**: Output minimal root + separate files with markdown links
5. **Flag for deletion**: Remove instructions that are:
   - Redundant (agent already knows)
   - Too vague to be actionable
   - Overly obvious ("write clean code")

## Progressive Disclosure Patterns

### Separate Files
```markdown
# Root AGENTS.md
For TypeScript conventions, see docs/TYPESCRIPT.md
```

### Nested Documentation
```
docs/
├── TYPESCRIPT.md → references TESTING.md
├── TESTING.md → references test runners
└── BUILD.md → references build config
```

### Monorepo Structure

| Level   | Content                                    |
|---------|-------------------------------------------|
| Root    | Monorepo purpose, navigation, shared tools |
| Package | Package purpose, tech stack, conventions   |

## Example Minimal AGENTS.md

```markdown
React component library for accessible data visualization.

Uses pnpm workspaces.

## Conventions
- TypeScript: see docs/TYPESCRIPT.md
- Testing: see docs/TESTING.md
- API patterns: see docs/API.md
```

## Anti-Patterns to Fix

- **Auto-generated files**: Bloated with "useful for most scenarios" content
- **File path documentation**: Goes stale quickly, poisons context
- **Accumulated rules**: "Ball of mud" from months of one-off additions
- **Forcing language**: Excessive "ALWAYS", "NEVER", all-caps directives
- **Obvious instructions**: Things the model already knows

## Creation Workflow

When creating a new AGENTS.md:

1. Ask user for one-sentence project description
2. Identify package manager (default npm needs no mention)
3. Check for non-standard build/typecheck commands
4. Keep it under 10 lines if possible
5. Create separate docs/ files for domain-specific guidance
