---
name: create-skill
description: Creates Agent Skills from the current project directory (local docs/source). Use when the user wants to bootstrap skills for their project using existing documentation in the workspace—no GitHub clone. Output goes under skills/<name>/ in the same project; AGENTS.md is updated.
metadata:
  author: hairy
  version: "2026.2.1"
  source: Hand-written, adapted from create-skill-from-repo, scripts at https://github.com/hairyf/skills
---

# Create Skills from Current Directory

Workflow for producing a skill set from the **current project** using local documentation. Use when the user supplies `<skills-name>` and optionally a source path; there is no clone from GitHub—the source is the workspace (or a subpath like `docs/`).

## When to Use

- User wants skills for **this project** (the workspace where the agent is running).
- Source is **local**: current directory, or a path such as `docs/`, `documentation/`, or repo root.
- Goal is to bootstrap skills from existing docs/source and output under `skills/<skills-name>/` in the same project.

## Prerequisites

- User has given: `<skills-name>` (kebab-case, e.g. `my-project`). Optionally: `<source-path>` (e.g. `docs/`, `.`, or default to `docs/` or repo root).
- Workspace is the **user’s project** (any repo); not necessarily the skills generator repo.

## Workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Identify docs/source in workspace
- [ ] Step 2: Generate initial skill set (SKILL.md + references)
- [ ] Step 3: Loop — review coverage, add missing major modules
- [ ] Step 4: Add generated skills to AGENTS.md (create file if missing)
```

### Step 1: Identify docs/source in workspace

1. **Source root**: Use `<source-path>` if provided; otherwise look for common paths: `docs/`, `documentation/`, `packages/*/docs/`, or repo root (README + MD files).
2. Treat this path as the **source root** for reading (no clone; read directly from the workspace).
3. If the project has an instructions file (e.g. `instructions/<project>.md`) for skill generation, follow it; otherwise focus on agent capabilities and practical usage; categorize references as `core`, `features`, `best-practices`, `advanced` and prefix filenames accordingly; skip user-facing guides, get-started, and content agents already know.

### Step 2: Generate initial skill set

1. **Output directory:** `skills/<skills-name>/` in the **current project**. Create it if needed. Structure: `SKILL.md`, `references/*.md`, `GENERATION.md`; optional `scripts/`, `assets/`.
2. **Read** from the source root in the workspace: structure, main topics, and entry points (README, sidebar, nav).
3. **Create**:
   - **`skills/<skills-name>/SKILL.md`** — Frontmatter: `name`, `description`, `metadata` (author, version, source). Body: short intro, then sections with tables of references (e.g. Core References, Features). Use kebab-case for names. See existing skills in this repo for examples.
   - **`skills/<skills-name>/references/*.md`** — One concept per file; filename prefix by category (`core-*`, `features-*`, `best-practices-*`, `advanced-*`). Each file: frontmatter `name`, `description`; heading; brief description; **Usage** (code examples); **Key Points** (bullets); at the end a comment block `<!-- Source references: ... -->` with paths or URLs to the source docs.
   - **`skills/<skills-name>/GENERATION.md`** — Tracking metadata:
     ```markdown
     # Generation Info
     - **Source:** <source-path> (current project)
     - **Generated:** <date>
     ```
4. **Writing:** Rewrite for agents; be practical and concise; one concept per file; include working code examples; explain when and why, not only how. Do not copy docs verbatim.

### Step 3: Loop until no major modules missing

Review, identify missing modules, supplement, update SKILL.md (and GENERATION.md if re-read). The source is the workspace docs.

1. **Review** — Compare `skills/<skills-name>/references/` and `SKILL.md` to the project’s documented surface (docs tree, README, nav).
2. **Identify** — Missing **major modules**: central or commonly needed topics (core concepts, main APIs, primary features), not minor edge cases. Criteria: see [coverage-loop](references/coverage-loop.md).
3. **Supplement** — Add new reference files in `skills/<skills-name>/references/` with correct naming (`core-*`, `features-*`, etc.); update `SKILL.md` tables; update `GENERATION.md` if the source was re-read.
4. **Repeat** until no important gaps remain (do not skip the review; stop when major surface is covered).

### Step 4: Add generated skills to AGENTS.md (create file if missing)

**User's project** = the workspace (repository root). **AGENTS.md** = `AGENTS.md` at that root.

1. **If `AGENTS.md` does not exist** at the project root, create it (e.g. a short intro and a section for skills).
2. **Add the generated skills** to `AGENTS.md`. Include at least:
   - The skill name: `<skills-name>`
   - Where it lives: `skills/<skills-name>/` (or the path relative to the project root)
   - Optionally: a one-line description or when to use it (from `skills/<skills-name>/SKILL.md` frontmatter).
3. Place the addition in a clear section (e.g. "Generated skills", "Agent skills", "Skills from current directory"). If the file already lists skills, append or merge in the same format; do not remove existing content.

## Key Points

- **Local only:** No clone; source is the current project (or given path). Record the source path in `GENERATION.md`.
- **One skill set per run:** One `<skills-name>` (and optional `<source-path>`) produces one directory under `skills/<skills-name>/`.
- **AGENTS.md:** Always add the generated skill to the project root `AGENTS.md` (create the file if it does not exist).
- **Naming:** Use kebab-case for `<skills-name>` and for reference filenames (e.g. `core-syntax.md`, `features-routing.md`).
- **Paths:** Use forward slashes in instructions and examples (e.g. `docs/`, `skills/my-project/`).

## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Coverage loop | When to stop the loop and what counts as a major module | [coverage-loop](references/coverage-loop.md) |

## Additional Resources

- Coverage criteria and when to stop the loop: [coverage-loop](references/coverage-loop.md).
