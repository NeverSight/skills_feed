---
name: living-docs
description: "Generate living documentation from git diffs — analyze branch comparisons or last N commits to automatically create or update Component Docs, Changelogs, ADRs, and Runbooks in Markdown with Obsidian-compatible YAML frontmatter. Use when asked to: (1) document changes from a branch diff, (2) generate release notes, (3) update service documentation, (4) analyze commits and produce docs, (5) create ADRs from architectural changes. Triggers: 'document the diff', 'generate docs from commits', 'update docs for [service]', 'release notes', 'what changed and document it', 'living docs', 'analiza el diff y genera documentacion'."
---

# Living Docs

Generate documentation driven by actual code changes. Every document traces to specific commits and files. When code changes, docs change.

**Language policy**: Generate all documentation in English. Include Spanish translations in the `aliases` frontmatter field.

## Folder Structure

All generated docs live under `${GIT_REPO_ROOT}/docs/` (relative to the repository root). Create this structure if it doesn't exist:

```
docs/
├── components/          # Component Docs (services, apps, libraries)
│   ├── auth-service.md
│   ├── user-service.md
│   └── shared-utils.md
├── changelogs/          # Changelogs and release notes
│   ├── changelog-auth-service-2026-02-13.md
│   └── changelog-global-2026-02-13.md
├── adrs/                # Architecture Decision Records
│   ├── adr-001-redis-caching.md
│   └── adr-002-event-driven-auth.md
├── runbooks/            # Runbooks and SOPs
│   ├── runbook-deploy-auth-service.md
│   └── runbook-database-migration.md
└── index.md             # Auto-generated index linking all docs
```

### File Naming Conventions

| Doc Type | Directory | Filename Pattern |
|----------|-----------|-----------------|
| Component Doc | `docs/components/` | `{component-name}.md` |
| Changelog | `docs/changelogs/` | `changelog-{scope}-{YYYY-MM-DD}.md` |
| ADR | `docs/adrs/` | `adr-{NNN}-{slug}.md` |
| Runbook | `docs/runbooks/` | `runbook-{operation-slug}.md` |
| Index | `docs/` | `index.md` |

### Index File

After generating or updating docs, update `docs/index.md` with links to all docs:

```markdown
# Documentation Index

> Auto-generated. Last updated: YYYY-MM-DD

## Components
- [[auth-service]] — Authentication and authorization service
- [[shared-utils]] — Shared utility library

## Recent Changelogs
- [[changelog-auth-service-2026-02-13]] — Added OAuth2 support

## Architecture Decisions
- [[adr-001-redis-caching]] — Accepted

## Runbooks
- [[runbook-deploy-auth-service]] — Deployment procedure
```

---

## Workflow

```
1. Gather context     → Determine diff scope
2. Extract diff data  → Run extract-diff.sh or git commands
3. Classify changes   → Identify what matters (see references/analysis-patterns.md)
4. Select templates   → Pick doc types (see references/templates.md)
5. Generate docs      → Write markdown with full YAML frontmatter
6. Verify output      → Cross-check generated docs against diff
7. Present summary    → Show what was generated and why
```

### Step 1: Gather Context

Determine from the user's message (ask only if not inferrable):
- **Diff scope**: Branch comparison (e.g., `feature/X` vs `Develop`) or last N commits?
- **Existing docs**: Any docs to update rather than create from scratch?

**Defaults (when not specified):**
- **Diff scope**: Current branch vs default branch (auto-detected from repo)
- **Output path**: Always `${GIT_REPO_ROOT}/docs/` (using the folder structure above)
- **Existing docs**: Search `${GIT_REPO_ROOT}/docs/` for matching filenames before creating new docs

### Step 2: Extract Diff Data

Run the extraction script from this skill's directory:

```bash
# Branch comparison (auto-detects default branch)
bash <this-skill-path>/scripts/extract-diff.sh <repo-path> --branch <target>

# Last N commits
bash <this-skill-path>/scripts/extract-diff.sh <repo-path> --commits 20

# Filtered by path (for monorepos)
bash <this-skill-path>/scripts/extract-diff.sh <repo-path> --branch Develop --path services/auth/
```

For multi-repo workspaces, run per repository.

#### Large Diff Strategy

When the diff is large (100+ files changed or output exceeds ~50KB):

1. **Start with `--stat` only** — Use the file list and change counts to plan
2. **Read full diff only for high-impact files** — APIs, schemas, configs, contracts, new files
3. **Read only changed hunks for medium-impact files** — Business logic, services
4. **Skip full diff for low-impact files** — Tests, formatting, comments
5. **Split by directory** — If still too large, analyze one component/service at a time

### Step 3: Classify Changes

Read `references/analysis-patterns.md` for the full classification guide.

**Priority**: High-impact changes (new components, public API changes, business logic changes, schema migrations, new dependencies, infra changes) are always documented. Medium-impact (internal refactors, test changes) only if significant. Low-impact (formatting, comments, patch bumps) are skipped.

**Key distinctions** (from analysis-patterns.md):
- **Business logic vs refactor**: Did test expectations change? → business logic. Same tests pass? → refactor.
- **Interface exposure**: External (public API) > Inter-component (shared packages) > Internal (same module). Document proportionally.

Map each significant change to doc types:

| Change Type | Impact | Doc Types |
|-------------|--------|-----------|
| New component / module | High | Component Doc (new) |
| Public API change | High | Component Doc + Changelog (Breaking if contract changed) |
| Business logic change | High | Component Doc + Changelog |
| Inter-component interface change | High | Component Doc + flag downstream consumers |
| Schema / data model change | High | ADR + Component Doc |
| Major dependency added | Medium-High | ADR + Component Doc |
| Infrastructure / deployment change | Medium | Runbook |
| Internal refactor (same behavior) | Low | Changelog (Internal) or skip |
| Release milestone | — | Changelog |

### Step 4: Select and Fill Templates

Read `references/templates.md` for all templates and the frontmatter schema.

Frontmatter rules:
- ALWAYS include all required fields: `aliases`, `type`, `layer`, `status`, `owner`, `tech_stack`, `last_updated`, `source_branch`, `commit_range`
- Use `[[wiki-links]]` for owner, tech_stack, and cross-references
- Set `last_updated` to today's date
- Set `source_branch` and `commit_range` from the actual diff
- Set `status` honestly: `active`, `debt`, `zombie`, or `gap`
- Populate `aliases` with English keywords + Spanish equivalents
- Infer `owner` and `tech_stack` using the heuristics in templates.md → "Inferring Frontmatter from Diffs"
- **Omit template sections that don't apply** (e.g., don't include "Events Published" for a REST-only service)

### Step 5: Generate Docs

Write docs to the folder structure defined above.

**Updating existing docs**: Read first, preserve frontmatter structure, update `last_updated` and `commit_range`, modify only affected sections, append to "Recent Changes".

#### Merge Strategy for Incremental Updates

When a doc already exists:

| Section | Strategy |
|---------|----------|
| Frontmatter | **Merge**: Update `last_updated`, `commit_range`, `status`. Preserve `owner`, `aliases` (append new ones) |
| What It Does | **Replace only if** the component's purpose fundamentally changed |
| API Surface / Exported API | **Merge**: Add new entries, update changed entries, mark removed entries as deprecated |
| Dependencies | **Replace** with current state |
| Configuration | **Merge**: Add new env vars, update changed ones |
| Key Files | **Replace** with current state |
| Recent Changes | **Append** new changes at the top, keep last 5-10 entries |

### Step 6: Verify Output

Before presenting to the user, cross-check:

- [ ] Every endpoint/export mentioned in docs exists in the diff or codebase
- [ ] All frontmatter required fields are populated (no empty or placeholder values except `owner: "[[TBD]]"`)
- [ ] File paths referenced in "Key Files" actually exist
- [ ] Breaking changes flagged in Changelog match actual contract changes in the diff
- [ ] No duplicate docs (check existing files before creating new ones)

### Step 7: Present Summary

Show the user what was generated:

```
## Documentation Generated

| File | Type | Reason |
|------|------|--------|
| docs/components/auth-service.md | Component Doc | New endpoints in routes/users.ts |
| docs/changelogs/changelog-auth-2026-02-13.md | Changelog | 12 commits with 3 features, 2 fixes |

### Key Changes Documented
- [bullets]

### Skipped (Low Impact)
- [what and why]
```

Always update `${GIT_REPO_ROOT}/docs/index.md` with links to all generated docs (for multi-repo workspaces, do this per repository).

---

## Quality Rules

- **No fluff**: Every sentence carries information. Cut filler.
- **Trace to code**: Every claim references a file, commit, or config.
- **Tables over prose**: For endpoints, env vars, dependencies — always tables.
- **Be honest**: If the diff reveals tech debt, set `status: debt`. Living docs tell the truth.
- **Aliases matter**: Include concept name, Spanish translation, common abbreviations.
- **Omit empty sections**: Don't include template sections that have no content for this component.

---

## Few-Shot Example

### Input: Diff Summary

```
=== FILE STATS ===
 services/auth/src/routes/auth.ts   | 45 +++++++++--
 services/auth/src/services/oauth.ts | 120 ++++++++++++++++++++++++++++
 services/auth/src/types/auth.dto.ts |  15 ++++
 packages/shared-types/src/user.ts   |   8 ++--
 services/auth/package.json          |   2 +  (added passport-google-oauth20)
 services/auth/tests/oauth.test.ts   |  85 ++++++++++++++++++++

=== COMMIT LOG ===
a1b2c3d feat: add Google OAuth2 login flow
d4e5f6g feat: add OAuth callback handler
h7i8j9k fix: handle missing email in OAuth profile
l0m1n2o chore: add passport-google-oauth20 dependency
```

### Output: Classification

1. **New OAuth service file** (oauth.ts, 120 lines) → High impact, new feature → Component Doc update
2. **Route changes** (auth.ts, 45 lines) → Public API change → Component Doc + Changelog
3. **Shared types change** (packages/shared-types/user.ts) → Inter-component interface → Component Doc + flag consumers
4. **New major dependency** (passport-google-oauth20) → ADR candidate
5. **New tests with different expectations** → Confirms business logic change, not refactor

### Output: Generated Docs

- `docs/components/auth-service.md` — Updated: added OAuth endpoints, new dependency, new key files
- `docs/changelogs/changelog-auth-2026-02-13.md` — New: 2 features (OAuth login, callback handler), 1 fix
- `docs/adrs/adr-003-google-oauth.md` — New: Decision to use passport-google-oauth20 for social login
- `docs/components/shared-types.md` — Updated: flag that `UserDTO` interface changed (consumed by 2 services)

---

## Resources

- `scripts/extract-diff.sh` — Extract structured diff data (file stats, commit log, full diff)
- `references/templates.md` — All doc templates with frontmatter schema
- `references/analysis-patterns.md` — How to classify changes from diffs
