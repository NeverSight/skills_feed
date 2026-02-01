---
name: create-skill-from-repo
description: Creates Agent Skills from an arbitrary repository when no existing reference exists. Clones the repo to .temp/repos, generates skills under a user-defined name following project conventions, iterates until major modules are covered, then removes the temp clone. Use when the user provides a repo URL and a skills name to bootstrap skills for a framework or project.
metadata:
  author: hairy
  version: "2026.2.1"
  source: Hand-written, scripts at https://github.com/hairyf/skills
---

# Create Skills from Repo

Workflow for quickly producing a skill set from any repository and applying it in the project. Use when the user supplies `<repo-url>` and `<skills-name>` and there is no existing skill source for that framework or project (i.e. not in `meta.ts` submodules or vendors).

## When to Use

- User provides a repository URL and a desired skills name.
- No entry exists in `meta.ts` submodules or vendors for that project.
- Goal is to bootstrap skills from docs/source in this repo (output under `skills/`).

## Prerequisites

- User has given: `<repo-url>` (e.g. `https://github.com/org/repo`) and `<skills-name>` (kebab-case, e.g. `my-framework`).
- Workspace is the skills generator repo (contains `meta.ts`, `skills/`).

## Workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Clone repo to .temp/repos
- [ ] Step 2: Identify docs/source in clone
- [ ] Step 3: Generate initial skill set (SKILL.md + references)
- [ ] Step 4: Loop — review coverage, add missing major modules
- [ ] Step 5: Add generated skills to user's AGENTS.md (create file if missing)
- [ ] Step 6: Remove .temp/repos and inform user
```

### Step 1: Clone repo to .temp/repos

1. Create `.temp/repos` if it does not exist.
2. Derive a **slug** from the repo URL (e.g. `github.com/org/repo` → `org-repo` or last path segment `repo`). Use a single, consistent folder name to avoid collisions.
3. Clone **shallow** into `.temp/repos/<slug>`:
   ```bash
   git clone --depth 1 <repo-url> .temp/repos/<slug>
   ```
4. Do **not** add the clone to `meta.ts` submodules; this is a one-off temp source.

### Step 2: Identify docs/source in clone

1. Locate documentation in the cloned repo. Common paths: `docs/`, `documentation/`, `packages/*/docs/`, or repo root with README + MD files.
2. Treat this path as the **source root** for reading (equivalent to `sources/{project}/docs/` in a Type 1 workflow).
3. If the skills repo has `instructions/<project>.md` for this project, follow it; otherwise focus on agent capabilities and practical usage; categorize references as `core`, `features`, `best-practices`, `advanced` and prefix filenames accordingly; skip user-facing guides, get-started, and content agents already know.

### Step 3: Generate initial skill set

1. **Output directory:** `skills/<skills-name>/`. Create it if needed. Structure: `SKILL.md`, `references/*.md`, `GENERATION.md`; optional `scripts/`, `assets/`.
2. **Read** from the source root in `.temp/repos/<slug>`: structure, main topics, and entry points (README, sidebar, nav).
3. **Create**:
   - **`skills/<skills-name>/SKILL.md`** — Frontmatter: `name`, `description`, `metadata` (author, version, source). Body: short intro, then sections with tables of references (e.g. Core References, Features). Use kebab-case for names. See `skills/pinia/SKILL.md` or `skills/slidev/SKILL.md` for examples.
   - **`skills/<skills-name>/references/*.md`** — One concept per file; filename prefix by category (`core-*`, `features-*`, `best-practices-*`, `advanced-*`). Each file: frontmatter `name`, `description`; heading; brief description; **Usage** (code examples); **Key Points** (bullets); at the end a comment block `<!-- Source references: ... -->` with URLs to the source docs.
   - **`skills/<skills-name>/GENERATION.md`** — Tracking metadata:
     ```markdown
     # Generation Info
     - **Source:** `.temp/repos/<slug>` (one-off clone of <repo-url>)
     - **Git SHA:** <sha>
     - **Generated:** <date>
     ```
4. **Writing:** Rewrite for agents; be practical and concise; one concept per file; include working code examples; explain when and why, not only how. Do not copy docs verbatim.

### Step 4: Loop until no major modules missing

Review, identify missing modules, supplement, update SKILL.md (and GENERATION.md if re-read). The “source” is the temp clone’s docs.

1. **Review** — Compare `skills/<skills-name>/references/` and `SKILL.md` to the repo’s documented surface (docs tree, README, nav).
2. **Identify** — Missing **major modules**: central or commonly needed topics (core concepts, main APIs, primary features), not minor edge cases. Criteria: see [coverage-loop](references/coverage-loop.md).
3. **Supplement** — Add new reference files in `skills/<skills-name>/references/` with correct naming (`core-*`, `features-*`, etc.); update `SKILL.md` tables; update `GENERATION.md` if the source was re-read.
4. **Repeat** until no important gaps remain (do not skip the review; stop when major surface is covered).

### Step 5: Add generated skills to user's AGENTS.md (create file if missing)

**User's project** = the workspace where the agent is running (repository root). **User's AGENTS.md** = `AGENTS.md` at that root.

1. **If `AGENTS.md` does not exist** in the user's project root, create it (e.g. a short intro and a section for skills).
2. **Add the generated skills** to `AGENTS.md`. Include at least:
   - The skill name: `<skills-name>`
   - Where it lives: `skills/<skills-name>/` (or the path relative to the user's project)
   - Optionally: a one-line description or when to use it (from `skills/<skills-name>/SKILL.md` frontmatter).
3. Place the addition in a clear section (e.g. "Generated skills", "Agent skills", "Skills from repo"). If the file already lists skills, append or merge in the same format; do not remove existing content.

### Step 6: Remove .temp/repos and inform user

1. Delete the temp clone:
   ```bash
   rm -rf .temp/repos/<slug>
   ```
   If `.temp/repos` is empty, you may remove `.temp/repos` as well (or leave it for future runs).
2. Tell the user that the skill set is ready: output is under `skills/<skills-name>/`, the user's `AGENTS.md` has been updated with the new skill, and they can use or extend it from there. Optionally summarize what was created (SKILL.md + N references).

## Key Points

- **Temp only:** The clone in `.temp/repos` is temporary; do not add it to `meta.ts`. The canonical source is the user’s `<repo-url>`; record it in `GENERATION.md`.
- **One skill set per run:** One `<repo-url>` + `<skills-name>` produces one directory under `skills/<skills-name>/`.
- **User's AGENTS.md:** Always add the generated skill to the user's project root `AGENTS.md` (create the file if it does not exist). We only register our output there; we do not require the user to follow any other project's rules.
- **Naming:** Use kebab-case for `<skills-name>` and for reference filenames (e.g. `core-syntax.md`, `features-routing.md`).
- **No Windows paths:** Use forward slashes in instructions and examples (e.g. `.temp/repos/slug`).

## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Coverage loop | When to stop the loop and what counts as a major module | [coverage-loop](references/coverage-loop.md) |

## Additional Resources

- Coverage criteria and when to stop the loop: [coverage-loop](references/coverage-loop.md).
