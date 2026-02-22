---
name: init-docs
description: Initializes the standard docs/ directory structure for a new project. Creates docs/specifications/, docs/issue/, docs/reference/, docs/policy/, and docs/dev/ subdirectories, seeds initial policy documents in both English and Korean, and places a CLAUDE.md in the project root. Use this when starting a fresh project that should follow the standard documentation system.
---

# init-docs

Sets up the standard project documentation structure from scratch.

## When to Use

- Starting a new project that needs the standard `docs/` layout
- User says "set up the project structure", "initialize docs", "프로젝트 초기화", or "docs 만들어줘"
- The project has no `docs/` directory yet

## What This Skill Creates

```
docs/
├── specifications/
├── issue/
├── reference/
├── policy/
│   ├── policy.md
│   ├── commit-message-rule.md
│   ├── naming-conventions.md
│   └── reference-convention.md
└── dev/
    ├── specifications/
    ├── issue/
    └── policy/
        ├── policy.ko.md
        ├── commit-message-rule.ko.md
        ├── naming-conventions.ko.md
        └── reference-convention.ko.md
CLAUDE.md  (placed in project root)
```

## Step-by-Step Instructions

### Step 1: Confirm Before Acting

Tell the user:

> I'm about to set up the standard `docs/` structure in this project. This will
> create the docs/ directory tree, three initial policy documents (English +
> Korean), and a CLAUDE.md. Shall I proceed?

Wait for confirmation before creating anything.

### Step 2: Create Directory Structure

Run the setup script if available:

```bash
bash .skills/init-docs/scripts/create-structure.sh
```

Or fall back to the global install:

```bash
bash ~/.agents/skills/init-docs/scripts/create-structure.sh
```

If neither is available, create directories manually and add `.gitkeep` files
so Git tracks the empty directories:

```bash
mkdir -p docs/specifications docs/issue docs/reference docs/policy
mkdir -p docs/dev/specifications docs/dev/issue docs/dev/policy
touch docs/specifications/.gitkeep docs/issue/.gitkeep docs/reference/.gitkeep docs/policy/.gitkeep
touch docs/dev/specifications/.gitkeep docs/dev/issue/.gitkeep docs/dev/policy/.gitkeep
```

### Step 3: Place CLAUDE.md

Copy the content from the skill's template (see `references/CLAUDE-template.md`
or the `templates/CLAUDE.md` in the source repository) into the project root.

- If `CLAUDE.md` **does not exist**: create it with the template content.
- If `CLAUDE.md` **already exists**: do NOT overwrite it. Show the user the
  template and offer to merge relevant sections.

### Step 4: Create Initial Policy Files

Create the following English policy files in `docs/policy/`:

---

**docs/policy/policy.md**

```markdown
# Project Policy

## Documentation

- All documentation lives in `docs/` and is the source of truth
- All `docs/` content (except `docs/dev/`) is written in English
- `docs/dev/` contains Korean translations with `.ko.md` suffix
- `docs/reference/` is user-managed only — never create or edit files there

## Workflow

- Every task begins with an issue document in `docs/issue/`
- Issue files are numbered sequentially: issue001.md, issue002.md, ...
- Do not begin implementation before an issue document exists
- Update documentation in the same commit as the code change

## Policy Updates

- Changes to policy files must be discussed with the user first
- Policy changes require updating both the English and Korean versions

## Related Policy Files

- [@docs/policy/commit-message-rule.md](docs/policy/commit-message-rule.md) — Commit message format
- [@docs/policy/naming-conventions.md](docs/policy/naming-conventions.md) — Naming conventions for files, code, and branches
- [@docs/policy/reference-convention.md](docs/policy/reference-convention.md) — Document linking convention
```

---

**docs/policy/commit-message-rule.md**

```markdown
# Commit Message Rules

## Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes only
- `style`: Formatting or whitespace (no logic change)
- `refactor`: Code restructuring (no feature or fix)
- `test`: Adding or updating tests
- `chore`: Build process, dependency updates, tooling

## Rules

- Subject line: 72 characters maximum
- Subject: imperative mood, lowercase, no trailing period
- Example: `feat(auth): add OAuth2 login flow`
- Reference the issue number in the body or footer:
  `Refs: issue003`
- Separate body from subject with a blank line
```

---

**docs/policy/naming-conventions.md**

```markdown
# Naming Conventions

## Files and Directories

- All filenames: lowercase, hyphen-separated (kebab-case)
- Issue documents: `issue001.md`, `issue002.md` (zero-padded to 3 digits)
- Korean mirrors: append `.ko` before `.md`
  - English: `requirements.md` → Korean: `requirements.ko.md`
- No spaces in file or directory names

## Code (language-agnostic defaults)

- Variables and functions: camelCase
- Constants: UPPER_SNAKE_CASE
- Classes and types: PascalCase
- Private members: prefix with underscore `_`

## Branch Names

- Feature: `feat/issue<NNN>-<short-description>`
  - Example: `feat/issue003-user-authentication`
- Bug fix: `fix/issue<NNN>-<short-description>`
- Documentation: `docs/issue<NNN>-<short-description>`

## Notes

- Language-specific conventions override these defaults
- Add language-specific rules to this file as the project evolves
```

---

**docs/policy/reference-convention.md**

```markdown
# Document Reference Convention

## Purpose

Establishes a consistent way to mark documents that must be read or loaded
as prerequisite context, distinguishing them from paths mentioned as
examples or illustrations.

## Syntax

Use a markdown link with an `@` prefix to indicate **required context**:

    [@docs/policy/policy.md](docs/policy/policy.md)

A bare backtick path without `@` is informational or illustrative only:

    `docs/issue/issue003.md`

## Rules

1. An `@`-reference means "this file MUST be loaded before proceeding."
2. Use `@`-references in CLAUDE.md, policy files, issue documents, and
   skill definitions where prerequisite files exist.
3. `@`-references use project-root-relative paths (no leading slash).
4. Do not `@`-reference files in `docs/reference/`.
5. When an `@`-referenced file itself contains `@`-references, load them
   recursively (up to 2 levels deep).
6. The markdown link format `[@path](path)` ensures clickable navigation
   in GitHub and IDEs.

## Revision History

- <YYYY-MM-DD>: Initial version
```

---

### Step 5: Create Korean Policy Mirrors

Translate the four policy files into Korean and place them in `docs/dev/policy/`:

- `docs/dev/policy/policy.ko.md`
- `docs/dev/policy/commit-message-rule.ko.md`
- `docs/dev/policy/naming-conventions.ko.md`
- `docs/dev/policy/reference-convention.ko.md`

Translation rules:
- All prose and headings → Korean
- Code blocks (``` ... ```) → keep as-is (English)
- File paths, type names, branch examples → keep in English
- Technical acronyms (API, URL, HTTP) → keep in English

### Step 6: Offer First Issue

After completing setup, ask:

> Setup complete. Would you like me to create the first issue document
> (`docs/issue/issue001.md`) to track the initial project setup tasks?

### Step 7: Report

List every file and directory created so the user can verify.
