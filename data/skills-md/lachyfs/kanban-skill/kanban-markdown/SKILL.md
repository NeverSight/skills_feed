---
name: kanban-markdown
description: Create, read, update, move, and manage kanban board feature files backed by markdown with YAML frontmatter. Use when working with kanban boards, task/feature tracking, `.devtool/features/` directories, feature files with status/priority frontmatter, or any project management tasks involving markdown-based kanban workflows.
---

# Kanban Markdown

Manage kanban board features stored as markdown files with YAML frontmatter. Each feature is a `.md` file; the VS Code kanban-markdown extension renders them as a board.

## File Format

Every feature file follows this exact format:

```markdown
---
id: "my-feature-2026-02-20"
status: "backlog"
priority: "medium"
assignee: null
dueDate: null
created: "2026-02-20T10:00:00.000Z"
modified: "2026-02-20T10:00:00.000Z"
completedAt: null
labels: []
order: "a0"
---

# My Feature

Description and details here.
```

**Serialization rules** (must match exactly for the extension to parse correctly):
- String fields: always `"double-quoted"`
- Nullable fields (`assignee`, `dueDate`, `completedAt`): bare `null` when unset
- Labels: inline array `["bug", "ui"]` or `[]`
- Order: `"double-quoted"` string — fractional index for lexicographic sorting (see below)
- Field order: `id`, `status`, `priority`, `assignee`, `dueDate`, `created`, `modified`, `completedAt`, `labels`, `order`

**Valid values:**
- status: `backlog` | `todo` | `in-progress` | `review` | `done`
- priority: `critical` | `high` | `medium` | `low`

For full field specs, see [references/data-model.md](references/data-model.md).

## Features Directory

Default: `.devtool/features/` relative to workspace root. Configurable via VS Code setting `kanban-markdown.featuresDirectory`.

- Active features (backlog, todo, in-progress, review): `{featuresDir}/{id}.md`
- Completed features (done): `{featuresDir}/done/{id}.md`

## Fractional Index Ordering

The `order` field uses fractional indexing — lexicographically sortable strings that allow inserting between any two items without reindexing. The extension uses the `fractional-indexing` npm package internally.

**When creating features**, determine the order by reading existing features in the target column (sorted by `order`):
- If the column is empty: use `"a0"`
- To append after the last item: increment the trailing character — `"a0"` → `"a1"`, `"a1"` → `"a2"`, ..., `"a9"` → `"aA"`, etc.
- The full character sequence is `0-9`, `A-Z`, `a-z` (base-62, ASCII order)

When moving features via drag-and-drop, the extension computes fractional keys between neighbors automatically. The skill only needs to handle appending new features to the end of a column.

## Creating Features

1. Generate ID: lowercase title, keep only `a-z 0-9 - space`, replace spaces with `-`, collapse multiple `-`, trim `-` from ends, truncate to 50 chars, append `-YYYY-MM-DD`. If empty, use `feature-YYYY-MM-DD`.
2. Set `created` and `modified` to current ISO timestamp. Set `order` by reading existing features in the target column and generating a key that sorts after the last one (see Fractional Index Ordering above).
3. If status is `done`, set `completedAt` to now and place in `done/` subfolder.
4. Write frontmatter in exact field order above, then `# Title` and body.

## Updating Features

- Always update `modified` to current ISO timestamp
- Never change `id` or `created`
- Preserve exact serialization format

## Moving Features

Update `status` and `modified`. When crossing the done boundary:
- **To done**: set `completedAt` to current ISO timestamp, move file to `done/` subfolder
- **From done**: set `completedAt` to `null`, move file back to root

## Writing Content

Start with `# Title` (the extension extracts the display title from the first `# heading`). Use acceptance criteria checklists, notes, etc. as needed.
