---
name: agents-md
description: Expert AGENTS.md file assistant. Use when users want to create, verify, or improve AGENTS.md files. Helps with creating minimal, focused AGENTS.md files following progressive disclosure principles, verifying existing files for issues (bloat, contradictions, stale info), and refactoring bloated files.
---

This skill provides expert guidance for creating, verifying, and improving AGENTS.md files - the open standard format for guiding AI coding agents.

## What is AGENTS.md?

AGENTS.md is a simple, open format for guiding coding agents, used by over 60k open-source projects. Think of it as a README for agents: a dedicated, predictable place to provide context and instructions to help AI coding agents work on your project.

**Key principle:** Unlike README.md (which is for humans), AGENTS.md contains the extra, detailed context coding agents need: build steps, tests, conventions, and instructions that might clutter a README.

**Learn more:** https://agents.md/ | https://www.aihero.dev/a-complete-guide-to-agents-md

## Quick Start

### When users want to create an AGENTS.md file

Start by asking these clarifying questions:

1. **Project type:** Monorepo or single package?
2. **Tech stack:** What languages/frameworks?
3. **Package manager:** npm, pnpm, yarn, bun, or something else?
4. **Build/test commands:** Any non-standard commands?
5. **Specific concerns:** Any patterns you want to encourage or avoid?

Then create a minimal AGENTS.md following the template below.

### When users want to verify an existing AGENTS.md

Run through the verification checklist (see [Verification](#verification) below).

### When users want to improve an existing AGENTS.md

Assess the file and suggest progressive disclosure refactoring (see [Improvement](#improvement) below).

## Core Principles

### 1. Minimal Root AGENTS.md

The root AGENTS.md should be as small as possible. Every token gets loaded on every request, so keep only what's relevant to **every single task**.

**Essential elements only:**
- One-sentence project description (acts as a role-based prompt)
- Package manager (if not npm; or use corepack for warnings)
- Non-standard build/typecheck commands
- Links to progressive disclosure files

### 2. Progressive Disclosure

Instead of cramming everything into AGENTS.md, give the agent only what it needs right now, and point to other resources when needed.

**Example - Don't do this:**
```markdown
## Code style

- Always use const instead of let
- Use interface instead of type when possible
- Prefer functional patterns
- No semicolons
- Single quotes only
- ... (50 more lines)
```

**Do this instead:**
```markdown
For TypeScript conventions, see docs/TYPESCRIPT.md
```

**Benefits:**
- TypeScript rules only load when the agent writes TypeScript
- Other tasks don't waste tokens
- File stays focused and portable across model changes

### 3. Describe Capabilities, Not File Structure

File paths change constantly. Documenting structure leads to stale information that actively poisons context.

**Don't:**
```markdown
Authentication logic lives in src/auth/handlers.ts
```

**Do:**
```markdown
Authentication uses JWT tokens with refresh token rotation.
Look for modules matching **/auth/**/*.ts for implementation.
```

### 4. Nested AGENTS.md for Monorepos

Place AGENTS.md files in subdirectories - they merge with the root level.

| Level | Content |
|-------|---------|
| **Root** | Monorepo purpose, navigation, shared tools |
| **Package** | Package purpose, tech stack, specific conventions |

**Root AGENTS.md:**
```markdown
This is a monorepo containing web services and CLI tools.

Use pnpm workspaces to manage dependencies.

See each package's AGENTS.md for specific guidelines.
```

**Package AGENTS.md (packages/api/AGENTS.md):**
```markdown
This package is a Node.js GraphQL API using Prisma.

Follow docs/API_CONVENTIONS.md for API design patterns.
```

## Templates

### Minimal Single-Package AGENTS.md

```markdown
# AGENTS.md

[One-sentence description of what this project is]

## Package Manager

This project uses [pnpm/yarn/bun]. [Optional: brief note if workspaces/monorepo]

## Build & Test

- Build: `command here`
- Test: `command here`
- Typecheck: `command here` (if non-standard)

## Progressive Disclosure

- [Domain-specific]: [path/to/file.md]
```

### Minimal Monorepo Root AGENTS.md

```markdown
# AGENTS.md

This is a monorepo containing [brief description of packages].

## Package Manager

Use [pnpm workspaces/yarn workspaces] to manage dependencies.

## Navigation

- Use `pnpm --filter <package_name>` to run commands in specific packages
- Each package has its own AGENTS.md with specific guidelines

## Packages

- [`package-name`](packages/package-name): [brief purpose]
- [`package-name`](packages/package-name): [brief purpose]
```

### Package-Level AGENTS.md (Monorepo)

```markdown
# AGENTS.md

[One-sentence description of this package]

## Tech Stack

- [Framework]
- [Language]
- [Key libraries]

## Commands

- Build: `command here`
- Test: `command here`
- Dev: `command here`

## Progressive Disclosure

- [Domain]: [path/to/file.md]
```

## Verification

When verifying an existing AGENTS.md, check for these issues:

### Bloat Indicators

- [ ] File is longer than 50-75 lines
- [ ] Contains detailed coding style rules that belong in separate files
- [ ] Documents file paths extensively
- [ ] Has extensive examples that should be in documentation
- [ ] Contains git workflow instructions that belong in CONTRIBUTING.md

### Contradiction Detection

Look for conflicting instructions:
- [ ] "Use functional patterns" vs "Use classes for X"
- [ ] "Prefer composition" vs "Use inheritance for Y"
- [ ] "Always use X" vs "In cases of Y, use Z"

### Stale Information Risks

- [ ] Specific file paths (especially src/ directories)
- [ ] Lists of files or modules
- [ ] Version-specific toolchain commands
- [ ] Outdated architecture descriptions

### Best Practices Compliance

- [ ] Has one-sentence project description
- [ ] Specifies package manager (if not npm)
- [ ] Links to progressive disclosure files
- [ ] Uses conversational tone (not "ALWAYS", "MUST", "NEVER")
- [ ] Describes capabilities, not structure

## Improvement

### Refactoring Bloated AGENTS.md

Use this process to refactor a bloated AGENTS.md:

1. **Find contradictions**: Identify conflicting instructions and ask which to keep
2. **Extract essentials**: Keep only what belongs in root AGENTS.md
3. **Group the rest**: Organize remaining instructions into logical categories
4. **Create file structure**: Set up progressive disclosure hierarchy
5. **Flag for deletion**: Remove redundant, vague, or obvious instructions

**Prompt template to use:**
```text
I want you to refactor my AGENTS.md file to follow progressive disclosure principles.

1. **Find contradictions**: Identify any instructions that conflict with each other.
   For each contradiction, ask me which version I want to keep.

2. **Identify the essentials**: Extract only what belongs in the root AGENTS.md:
   - One-sentence project description
   - Package manager (if not npm)
   - Non-standard build/typecheck commands
   - Anything truly relevant to every single task

3. **Group the rest**: Organize remaining instructions into logical categories
   (e.g., TypeScript conventions, testing patterns, API design, Git workflow).

4. **Create the file structure**: Output:
   - A minimal root AGENTS.md with markdown links to the separate files
   - Each separate file with its relevant instructions
   - A suggested docs/ folder structure

5. **Flag for deletion**: Identify any instructions that are:
   - Redundant (the agent already knows this)
   - Too vague to be actionable
   - Overly obvious (like "write clean code")
```

### Creating Progressive Disclosure Files

**Suggested structure:**
```
docs/
├── TYPESCRIPT.md       # TypeScript patterns and conventions
├── TESTING.md          # Testing strategies and frameworks
├── API_CONVENTIONS.md  # API design patterns (if applicable)
├── ARCHITECTURE.md     # High-level architecture (capabilities, not file paths)
└── Git worklow items → CONTRIBUTING.md
```

**Each file should:**
- Be focused on one domain
- Link to related files for navigation
- Describe principles, not prescriptions
- Include examples where helpful

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Agent uses wrong package manager | Explicitly specify: "This project uses pnpm" |
| Agent generates wrong commands | List non-standard build/test commands |
| File gets too large | Apply progressive disclosure - move domain rules to separate files |
| Instructions conflict | Review for contradictions and resolve |
| Agent looks in wrong places | Describe capabilities, not file paths |
| Mixed conventions over time | Treat AGENTS.md as living documentation, review periodically |

## AGENTS.md vs CLAUDE.md

**Claude Code** uses `CLAUDE.md` instead of `AGENTS.md`. To maintain compatibility:

```bash
# Create a symlink from AGENTS.md to CLAUDE.md
ln -s AGENTS.md CLAUDE.md
```

Both files serve the same purpose - customize how AI coding agents behave in your repository.

## Tools Supporting AGENTS.md

AGENTS.md is an open standard supported by many tools:
- OpenAI Codex, Jules (Google), Factory, Aider, goose, opencode
- VS Code, Devin (Cognition), Cursor, RooCode, Gemini CLI
- GitHub Copilot coding agent, Windsurf (Cognition), and more

See https://agents.md/ for the full list.

## Your Approach

1. **Start minimal**: Begin with essential information only
2. **Apply progressive disclosure**: Move domain-specific rules to separate files
3. **Avoid file paths**: Describe capabilities, not structure
4. **Keep it conversational**: Use natural language, not rigid commands
5. **Review periodically**: Treat as living documentation
6. **Use nested files**: For monorepos, place AGENTS.md in subdirectories
7. **Link, don't duplicate**: Point to other resources instead of repeating

## Progressive Disclosure

**Deep dive on specific topics:**
- **Verification checklist**: [VERIFICATION.md](references/VERIFICATION.md)
- **Refactoring guide**: [REFACTORING.md](references/REFACTORING.md)
- **Template gallery**: [TEMPLATES.md](references/TEMPLATES.md)
- **Monorepo patterns**: [MONOREPO.md](references/MONOREPO.md)
- **Common anti-patterns**: [ANTI_PATTERNS.md](references/ANTI_PATTERNS.md)
