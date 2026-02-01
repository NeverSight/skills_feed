---
name: knowledge-base
description: Manage your personal knowledge base of curated resources, bookmarks, and excerpts. Triggers include "knowledge base", "kb", "add to knowledge", "add tabs to", "what do I have on", "what do we know about", "find resources about". Use with safari-tabs skill for bulk ingestion from Safari windows. Location is ~/knowledge/.
---

# Knowledge Base

Topic-based collection of curated links and notes at `~/knowledge/`.

## Structure

```
~/knowledge/
├── _index.md          # Topic listing
├── _inbox.md          # Unprocessed items
├── topics/*.md        # Articles, concepts, best practices
├── tools/*.md         # Software, libraries (organized by use case)
└── archive/YYYY-MM/   # Full article content (link rot protection)
```

## Entry Formats

**Topics** (articles/concepts):
```markdown
**[Title](url)** — Author

1-2 paragraph summary focusing on core insights. Be extremely concise, disregard grammar.
```

**Tools** (software/libraries):
```markdown
### [tool-name](url)

**Platform:** macOS / JavaScript / Web Service
**Install:** Installation method
**Use case:** Problem it solves

Brief summary of why it's useful and when to use it.

**Alternatives:** other-tool (tradeoff)
```

## Workflow: Adding from Safari

1. Get tabs: `get_tabs.sh markdown` or `get_tabs.sh -w N markdown`
2. **Process in batches of 8-10** to avoid context overflow
3. For each batch:
   - Fetch content from URLs
   - Read existing topic files
   - Route to appropriate topic based on content
   - Archive substantial/unique articles to `archive/YYYY-MM/`
   - Items not fitting existing topics → `_inbox.md`
4. Update `_index.md` when done

## Routing

**Articles/concepts** → `topics/`:
- Match by content, not just title
- Prefer more specific topics
- If unsure, add to `_inbox.md` with suggested topic
- If topic >500 lines or >30 entries, ask user to split

**Software/tools** → `tools/` by use case:
- Libraries, CLI tools, apps, web services all go here
- Articles *about* tools → `topics/`
- Create new use-case files as needed

## Quality Control

When bulk adding, **pause and ask** if you encounter:
- Out of place or low-quality content
- GitHub repos/gists (ask for routing confirmation)
- Failed fetches (summarize at end, ask if should add URL-only)

## Archiving

Archive to `archive/YYYY-MM/` when:
- Substantial content (>500 words)
- Likely to disappear (personal blogs)
- Unique insights

Skip: GitHub repos, YouTube, frequently-updated docs, news

## File Format Reference

Topic files: YAML frontmatter with `tags`, `updated`, then sections with entries
Tools files: Same frontmatter, then `### [tool](url)` entries with metadata

Update `_index.md` with new topics/tools after adding resources.

## Finding Resources

Check `tools/` before web search when user needs software/library.
