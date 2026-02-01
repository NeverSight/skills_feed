---
name: update-jamdesk
description: Use when user-facing code changes need documentation, user says "update docs"/"document this"/"add to jamdesk docs", or after implementing APIs, CLI commands, or UI components.
---

# Update Jamdesk

Updates customer-facing documentation in external repositories (not CLAUDE.md). Locates docs via `.jamdesk-docs-path`, asks clarifying questions, writes documentation, and verifies with the jamdesk CLI.

**Announce:** "I'm using the update-jamdesk skill to update your documentation."

**Use when:** User-facing changes to APIs, CLI commands, UI, config options, or component behavior.

**Skip when:** Internal refactors, test-only changes, build/CI config, performance work without behavior change.

## Critical Rules

| Always | Never |
|--------|-------|
| Include frontmatter (`title` minimum) | Create stub pages with "TODO" |
| Use built-in components first | Use `mint.json` (use `docs.json`) |
| Ask clarifying questions before writing | Skip verification |
| Reference https://jamdesk.com/docs | Commit to main without asking |

## Flags

| Flag | Behavior |
|------|----------|
| (none) | Full workflow: locate → clarify → analyze → write → verify → commit |
| `--preview` | Phases 1-3 only, describe changes without making them |

**Proactive:** After `/commit` with changes to `**/api/**`, `**/cli/**`, or `**/components/**`, suggest running this skill.

## Phase 1: Locate Documentation

Find `.jamdesk-docs-path` by walking up from current directory to git root.

```yaml
docs_path: ../customer-docs    # Required - relative or absolute path
docs_branch: main              # Optional, default: main
```

**First-time setup:** If config doesn't exist, ask user for their docs repo path and create the file. This only happens once per project. Point users to https://jamdesk.com/docs for help getting started with Jamdesk.

**Validation:** Path exists, contains `docs.json`, check for uncommitted changes. If same git repo as code, skip separate git operations.

## Phase 2: Clarify Scope

Review conversation to identify what changed, then ask:

1. **Branch strategy:** Feature branch (recommended), main, or current branch?
2. **Scope confirmation:** "I plan to [create/update] these pages: ... Any changes?"
3. **Additional context** (if needed): Terminology, related features, edge cases

**Principle:** Ask first, write later. 30-second clarification prevents 10-minute rework.

## Phase 3: Analyze Existing Docs

Search docs repo for existing coverage of the feature. Present findings:

```
Existing: getting-started.mdx mentions feature briefly
Missing: No dedicated page

Recommended:
1. Create: features/new-feature.mdx
2. Update: getting-started.mdx (add link)
```

**Decision matrix:**

| Scenario | Action |
|----------|--------|
| New feature | Create new page |
| Behavior change | Update existing page describing that behavior |
| Small addition | Add section to existing page |
| Major capability | New standalone page |
| Deprecation/removal | Update existing + add migration notes |
| Advanced usage | Add `<Accordion>` to existing |

## Phase 4: Write Documentation

Reference https://jamdesk.com/docs for full standards.

**Content quality:** Explain *why*, not just *what*. Show the simplest working example first. Use real values in examples, not placeholders. One concept per section.

**Page structure:**
1. Opening paragraph (what + why)
2. Quick Start (simplest example)
3. Configuration/Details
4. Examples (basic → advanced)
5. What's Next (related pages)

**Minimal template:**
```mdx
---
title: Feature Name
description: SEO description (50-160 chars)
---

What this does and why it's useful.

## Quick Start

\`\`\`bash
command --example
\`\`\`

## What's Next?

<Card title="Related" href="/path">Description</Card>
```

**Components:** `<Tabs>`, `<Steps>`, `<Accordion>`, `<Cards>`, `<Note>`/`<Warning>`/`<Tip>`, `<CodeGroup>`. See https://jamdesk.com/docs/components

**Images:** Store in `/images/<feature>/`, use absolute paths, always include alt text.

**Links:** Relative paths, no `.mdx` extension, avoid orphan pages.

**API docs:** Prefer OpenAPI auto-generation when available.

**Navigation:** Add new pages to `docs.json` navigation.

## Phase 5: Verify

**With CLI (recommended):**
```bash
jamdesk dev          # Preview locally
jamdesk validate     # Check docs.json schema
jamdesk broken-links # Find broken links
```

**Without CLI:** Verify manually - code examples have language tags, frontmatter has title/description, links use correct paths (no `.mdx`), new pages added to `docs.json`.

**Fix errors before proceeding.** If user dislikes changes, they can `git checkout .` to revert before commit.

## Phase 6: Commit

Present summary of changes, then ask user preference:
1. Commit to feature branch
2. Show diff first
3. Make additional changes

After commit, offer to push and create PR.

**Commit format:** `docs: [action] [what]` (e.g., `docs: add webhook configuration guide`)

## Quick Reference

| Situation | Action |
|-----------|--------|
| No config file | Ask user, create `.jamdesk-docs-path` |
| External repo | Feature branch, separate git ops |
| Same-repo docs | No separate git ops needed |
| `--preview` flag | Analyze only, no changes |
| CLI unavailable | Manual verification checklist |

## Example

```
User: Document the new webhook feature

Claude: I'm using the update-jamdesk skill...

Found docs at ../customer-docs

Branch strategy?
1. Feature branch (recommended)
2. Main
3. Current

User: 1

Claude: I'll create docs/webhooks. Scope look right?

User: Yes, also update API reference

[Writes docs, runs verification]

✓ validate passed
✓ broken-links passed

Files: webhooks/overview.mdx (new), api/reference.mdx (updated), docs.json (updated)

Commit? [Y/n]

User: Y

Claude: Committed. Push and create PR?
```

## Red Flags

Stop if you catch yourself:
- Skipping clarifying questions
- Creating pages without updating `docs.json`
- Using full URLs for internal links
- Adding images without alt text
- Making changes with `--preview` flag
