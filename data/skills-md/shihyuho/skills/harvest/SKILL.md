---
name: harvest
description: "Use when users ask to capture conversation decisions, problems, and lessons into persistent notes (e.g. 'harvest', '/harvest', 'save this to second brain', 'document this work')."
license: MIT
metadata:
  author: shihyuho
  version: "1.2.0"
---

# Harvest

Capture high-signal conversation knowledge into `docs/notes/` for reuse across sessions.

## When to Trigger

**Explicit request**:
- "harvest", "/harvest"
- "harvest this", "harvest this conversation"
- "save this to second brain"
- "document this work", "capture this knowledge"

**Natural breakpoints** — AI may **suggest** (never auto-execute):
- Significant decision made
- Complex problem solved after multiple attempts
- Important lesson learned
- Discussion wrapping up with valuable content

```
We just [made a decision/solved X/learned Y].
Would you like me to update the second brain?
```

Wait for user confirmation. Never auto-execute.

## Non-Negotiables

- Never auto-execute. Always wait for explicit user confirmation.
- Use template files as the single source of structure.
- Keep `context_id` in frontmatter for smart merge.
- Keep MOCs as index files: link to context anchors, do not duplicate full lesson content.
- Omit optional empty sections. Do not write empty headers or "None" placeholders.

## Quick Start

1. Ensure `docs/notes/` exists (initialize when missing).
2. Run lesson review for this harvest run.
3. Detect `context_id` and check whether matching context file exists.
4. Create new context or smart-merge existing context.
5. Update `docs/notes/00-INDEX.md` and related MOCs.
6. Confirm created/updated files to user.

## Workflow

### Phase 1: Prepare

1. Initialize second brain storage when `docs/notes/` is missing:
   - Create `docs/notes/contexts/` and `docs/notes/mocs/`.
   - Create `docs/notes/00-INDEX.md` from [references/INDEX_TEMPLATE.md](references/INDEX_TEMPLATE.md).
   - Create `docs/notes/contexts/contexts.base` and `docs/notes/mocs/mocs.base` from [references/CONTEXTS_BASE_TEMPLATE.base](references/CONTEXTS_BASE_TEMPLATE.base) and [references/MOCS_BASE_TEMPLATE.base](references/MOCS_BASE_TEMPLATE.base) when `obsidian-bases` is available.
   - Check `AGENTS.md` then `CLAUDE.md`; if both exist or neither exists, ask user which file to append, then append section from [references/AGENTS_LESSONS_SECTION.md](references/AGENTS_LESSONS_SECTION.md).
2. Mandatory lesson review for this harvest run:
   - Read `docs/notes/00-INDEX.md` when available.
   - Scan `docs/notes/mocs/lessons-learned.md` when available.
   - Apply matched lessons (tech, operation type, error pattern).

### Phase 2: Detect + Route

1. Build `context_id`:
   - First env var that matches `*SESSION*ID*`, `*CONVERSATION*ID*`, or `*THREAD*ID*` (case-insensitive).
   - Fallback timestamp `YYYYMMDDHHmmss`.
2. Look for `docs/notes/contexts/<context_id>-*.md`.

| Condition | Action |
|---|---|
| Matching context file exists | Run **Phase 4 (Smart Merge)** |
| No matching context file | Run **Phase 3 (New Context)** |
| User rejects suggested filename | Ask for new slug and regenerate filename |
| User cancels confirmation | Stop without writing files |

### Phase 3: New Context

1. Extract high-signal items: work, decisions (with rationale), unsolved, lessons.
2. Generate filename `<context_id>-<topic-slug>.md` and confirm:

```
Found: [N] decisions, [N] unsolved, [N] lessons
Suggested: contexts/<context_id>-<topic-slug>.md
1. Use this  2. Change slug  3. Cancel
```

3. Create `docs/notes/contexts/<filename>.md` from [references/CONTEXT_TEMPLATE.md](references/CONTEXT_TEMPLATE.md).
4. Use `obsidian-markdown` when available for wikilinks/frontmatter/anchors.
5. Update `docs/notes/00-INDEX.md` according to [references/INDEX_TEMPLATE.md](references/INDEX_TEMPLATE.md):
   - Recent Updates (top 5), Topics, Key Decisions, Open Questions, Recent Lessons, Stats.
6. Manage MOCs:
   - Lessons MOC: for error-related lessons (>15 min impact), ensure `docs/notes/mocs/lessons-learned.md` exists via [references/LESSONS_LEARNED_MOC_TEMPLATE.md](references/LESSONS_LEARNED_MOC_TEMPLATE.md), then append links only.
   - Topic MOC: when a topic appears in 3+ contexts without MOC, ask user first; create from [references/MOC_TEMPLATE.md](references/MOC_TEMPLATE.md) after confirmation.
7. Confirm:

```
✓ Created: contexts/<filename>.md
✓ Updated: 00-INDEX.md
✓ Updated: mocs/lessons-learned.md (when relevant)
✓ Created: mocs/<topic>.md (when relevant)
```

### Phase 4: Smart Merge

1. Read the existing context file.
2. Merge new items from current conversation.

| Section | Existing Topic | New Item |
|---|---|---|
| Decisions Made | Update existing entry, note update time | Append |
| Still Unsolved | Move resolved items to Decisions | Append |
| Lessons Learned | Merge same lesson and preserve anchor | Append |
| What We Worked On | Keep existing | Append |

3. Update frontmatter (`updated`, tags), keep `created` unchanged.
4. Update `00-INDEX.md` stats and recent updates.
5. Update `mocs/lessons-learned.md` with links only when new error-related lessons were added.
6. Confirm:

```
✓ Updated: contexts/<filename>.md
Changes: [added/updated/moved items]
```

## Content Quality Rules

- Quality over quantity: concise, reusable, high-signal notes.
- One idea per bullet; include rationale for decisions.
- Keep content relevant for future reuse (3+ months horizon).
- Skip raw transcripts, dead ends without insight, and obvious process noise.
- For lessons, use anchored headings and include: what happened, root cause, solution, apply-when.

Recommended section limits:

| Section | Requirement | Typical Size |
|---|---|---|
| Summary | Required | 1-2 sentences |
| What We Worked On | Required | 5-7 bullets |
| Decisions | Optional | up to 5-7 items |
| Still Unsolved | Optional | up to 3-5 items |
| Lessons Learned | Optional | up to 3-5 items |
| Notes | Optional | short snippets only |

---

## Integration

**Recommended**: `obsidian-markdown` skill for enhanced Obsidian compatibility. Without it, AI may write files directly and suggest installation:

```
For optimal Obsidian compatibility, consider installing obsidian-markdown skill:
npx skills add <obsidian-markdown-repo>
```

## See Also

Use these files as references (single source for structure and formats).

- [CONTEXT_TEMPLATE.md](references/CONTEXT_TEMPLATE.md)
- [MOC_TEMPLATE.md](references/MOC_TEMPLATE.md)
- [INDEX_TEMPLATE.md](references/INDEX_TEMPLATE.md)
- [LESSONS_LEARNED_MOC_TEMPLATE.md](references/LESSONS_LEARNED_MOC_TEMPLATE.md)
- [CONTEXTS_BASE_TEMPLATE.base](references/CONTEXTS_BASE_TEMPLATE.base)
- [MOCS_BASE_TEMPLATE.base](references/MOCS_BASE_TEMPLATE.base)
- [AGENTS_LESSONS_SECTION.md](references/AGENTS_LESSONS_SECTION.md)
