---
name: distill
description: |
  DISTILL
---

---
description: Rewrite repo CLAUDE.md into the best onboarding guide for this project
---

# DISTILL

Distill this repo's knowledge into a single, sharp `CLAUDE.md`.

## Purpose

- Rewrite the current repository's `CLAUDE.md` into the best possible onboarding + operating guide for this project.
- Output must let a new contributor start useful work in minutes, without asking questions.
- Scope is this repo only; global philosophy lives in `~/.claude/CLAUDE.md`.

## Inputs

- Always read, if present:
  - Repo `AGENTS.md`.
  - Existing repo `CLAUDE.md`.
  - Root `README` and any high-signal docs in `docs/`.
  - Key config / entry files (e.g. `package.json`, `pyproject.toml`, `docker-compose.yml`, main entrypoints).

## Target Shape for `CLAUDE.md`

```markdown
# CLAUDE

## Purpose
- What this repo is and why it exists.

## Architecture Map
- Main domains / services and how they fit.
- Where to start reading code (file:line).

## Run & Test
- Commands to run app, tests, lint, typecheck.
- Required env, secrets, or services.

## Quality & Pitfalls
- Definition of done, PR expectations, review norms.
- Non-obvious invariants, footguns, "never do X".

## References
- Key docs / ADRs / diagrams (paths).
- External systems / dashboards / runbooks.
```

## The Codex First-Draft Pattern

**Codex drafts the new CLAUDE.md. You review and refine.**

```bash
codex exec "DISTILL: Rewrite CLAUDE.md for this repo. Read README, ARCHITECTURE.md, docs/, and key code. Follow target shape below. Output to /tmp/claude-draft.md" \
  --output-last-message /tmp/codex-distill.md 2>/dev/null
```

Review Codex's draft. Refine for accuracy and compression.

## Algorithm

1. **Gather** (Codex does this)
   - Read inputs; understand what the repo does, how it runs, and how it fits into the wider system.
2. **Classify existing CLAUDE content**
   - Tag each line as:
     - Repo-specific + useful → keep or rewrite.
     - General / global → belongs in `~/.claude/CLAUDE.md`, do not restate here.
     - Noise / obsolete → drop.
3. **Draft new `CLAUDE.md`** (Codex produces first draft)
   - Fill the target shape above with tight, repo-specific bullets.
   - Prefer bullets over paragraphs; every line must earn its place.
   - Link to existing docs instead of duplicating them.
4. **Compress**
   - Apply the 3-2-1 test:
     - 3 key decisions or invariants newcomers must know.
     - 2 critical insights about architecture or workflow.
     - 1 clear starting point in the codebase.
   - Rewrite soft prose into sharp, actionable lines.
5. **Validate**
   - Run the checklist below.
   - Only propose the new `CLAUDE.md` once all checks pass.

## Checklist (must pass)

- [ ] Readable in ≤3 minutes; roughly ≤120 lines.
- [ ] Explains what this repo is and how it fits into the wider system.
- [ ] Tells me exactly how to run and test locally.
- [ ] Points to at least one concrete starting file/area (file:line ideal).
- [ ] Captures non-obvious invariants and footguns; omits trivia.
- [ ] Links to deeper docs / ADRs instead of copying them.
- [ ] Does not restate global behavior or philosophy from `~/.claude/CLAUDE.md`.

## Compression Examples

**Bad**: "We spent time discussing the authentication approach and eventually decided to use JWT tokens because they seemed like a good fit for our use case."

**Good**: "Purpose: auth + user accounts; legacy billing hooks remain here until `billing-service` migration completes."

**Bad**: "The tests are currently not all passing because there's an issue with the mock setup that needs to be fixed."

**Good**: "Pitfall: `auth.test.ts` flakiness if `docker-compose up db redis` not running; fix env instead of tests."

## Philosophy

- Maximum signal per word.
- Document what is not obvious from code or README.
- If you can't find 3 decisions, 2 insights, and 1 starting point, read more code before writing.

## Graduation Rules

CLAUDE.md is a staging area for learnings. When sections grow, graduate them:

- **Patterns section > 10 lines** → extract to a skill
- **Rules section > 5 items** → extract to an agent
- **Workflow section > 3 steps** → extract to a command

Keep CLAUDE.md lean. Knowledge graduates to executable artifacts.
