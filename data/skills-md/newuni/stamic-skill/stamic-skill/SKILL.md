---
name: stamic-skill
description: Statamic 6 development skill with documentation-backed guidance from statamic.dev + the statamic/docs mirror. Includes actionable steps/snippets for blueprints, Antlers, tags, addons, CP, caching, and common workflows.
license: MIT
metadata:
  author: newuni
  version: "1.0.7"
---

# stamic-skill (Statamic 6 Dev)

Provide Statamic 6 documentation-backed guidance and implementation help, optimized for developer workflows.

## Workflow (recommended)

1. **Clarify target + context**
   - Confirm: Statamic **6** (and Laravel version), project type (fresh vs existing), and whether the request is **Statamic-specific** (content model, Antlers, blueprints, structures) vs **Laravel-specific** (DB, Eloquent, queues, debugging).

2. **Prefer canonical docs, but keep it searchable**
   - Ensure the local docs mirror exists before searching:
     ```bash
     ./scripts/update_statamic_docs.sh
     ```
   - If you need parallel searches, do this:
     1. Bootstrap once with `./scripts/update_statamic_docs.sh --docs-dir <shared-path>`.
     2. Run parallel `search_statamic_docs.sh` calls with the same `--docs-dir <shared-path>` and `--no-bootstrap`.
   - Use **statamic.dev** for canonical explanations.
   - Use **GitHub mirror** (statamic/docs) for fast full-text search, diffs, and linking to exact Markdown.
   - If information conflicts, treat **statamic.dev** as source of truth and mention the discrepancy.

3. **Search → quote → answer**
   - Search for the relevant page/section.
   - Answer with short, actionable steps.
   - Include links (statamic.dev and/or specific docs file paths) so the team can verify.

4. **Separate Statamic vs Laravel concerns**
   - Use this skill for Statamic concepts and conventions (blueprints/fieldsets, entries, taxonomies, Antlers, tags/modifiers, Stache/cache, sites).
   - For Laravel framework mechanics (Artisan, Eloquent, queues, debugging, environment), rely on official Laravel documentation and project conventions.

## What to do for common requests

### “Find the latest docs for X”
- Search the GitHub mirror first (fast), then open the canonical statamic.dev page.
- Provide: the best page link, the key excerpt/summary, and 1–3 do/don’t bullets.

### “How do we implement X in Statamic 6?”
- Return a minimal implementation plan + code/config snippets.
- Call out:
  - where files live (blueprints, templates, addons)
  - expected conventions/naming
  - caches to clear (when relevant)

### “Is this best practice / is this supported in v6?”
- Confirm version explicitly.
- Prefer citing a doc section or a clear upstream source.

## Bundled resources

### references/
- `references/sources.md`: canonical sources and how to treat them.
- `references/response-guidelines.md`: domain taxonomy + response checklist for consistent Statamic 6 answers.

### scripts/
Use these scripts when you need deterministic, repeatable doc lookup.

1) Update/bootstrap local docs mirror (runtime-safe):
```bash
./scripts/update_statamic_docs.sh
```
From this repository root, maintainers may also use:
```bash
./dev-scripts/update_statamic_docs.sh
```

2) Search locally:
```bash
./scripts/search_statamic_docs.sh "your query"
```
If the mirror is missing, this command auto-runs `./scripts/update_statamic_docs.sh` unless `--no-bootstrap` is provided.
Use `--rank-mode fzf` (or `--rank-mode hybrid` with `--top`) for non-interactive fuzzy ranking. If `fzf` is unavailable, search continues with plain `rg/grep` output.

Parallel-safe pattern:
```bash
./scripts/update_statamic_docs.sh --docs-dir /tmp/statamic-docs-shared
./scripts/search_statamic_docs.sh --docs-dir /tmp/statamic-docs-shared --no-bootstrap --top 20 "antlers"
```

If the query is broad, narrow it with ripgrep flags:
```bash
./scripts/search_statamic_docs.sh --top 20 "antlers"
./scripts/search_statamic_docs.sh --rank-mode hybrid --top 20 "assets container"
```
