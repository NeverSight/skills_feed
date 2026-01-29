---
name: write-article
description: Write newsletter articles for The Hybrid Builder (chatwithgpt.substack.com) with intelligent cross-referencing of the full article archive. Includes sitemap-based article cache with theme indexing, reference suggestions, session transcript export, and cover image generation. Use when asked to write a blog post, article, or newsletter about a collaboration or technical topic.
---

# Write Article for The Hybrid Builder

Write a newsletter article about our collaboration for https://chatwithgpt.substack.com/s/the-hybrid-builder

## Context
- This publication is explicitly stated as AI-written
- Article documents our collaboration on: $ARGUMENTS

## Before Writing: Find Related Articles

**Always check the article archive first.** The cache includes all 33+ articles with theme indexing and cross-reference tracking.

### Article Cache Commands

```bash
# Update cache from sitemap (full archive)
python3 ~/.claude/skills/write-article/scripts/update-cache.py

# Get reference suggestions for your topic
python3 ~/.claude/skills/write-article/scripts/update-cache.py --suggest "your topic here"

# List all cached articles
python3 ~/.claude/skills/write-article/scripts/update-cache.py --list

# Browse by theme
python3 ~/.claude/skills/write-article/scripts/update-cache.py --themes

# Find articles related to a specific article
python3 ~/.claude/skills/write-article/scripts/update-cache.py --related "article-slug"

# Search by keyword
python3 ~/.claude/skills/write-article/scripts/update-cache.py --search "compound engineering"
```

### Reference Workflow
1. Run `--suggest "topic"` to get ranked candidates with phrasing suggestions
2. Review the theme index to spot thematic connections
3. For top candidates, use WebFetch to read full content if needed
4. Apply natural reference patterns from [references/reference-patterns.md](references/reference-patterns.md)

## Writing Style & Tone
- Conversational technical narrative blending storytelling with technical detail
- First-person collaborative perspective (emphasize the partnership)
- Enthusiastic, exploratory, and optimistic tone
- Transparent about challenges, failures, and iterative process
- High technical specificity with code examples and implementation details
- Meta-narrative about the AI-human collaboration itself

## Structure & Format
- Narrative-driven with chronological progression
- Use clear sections with timestamps/development phases
- Include headers and bullet points for readability
- Typical length: 1500-2500 words
- Always include: context, technical details, lessons learned, future implications

## Natural Cross-Referencing

Avoid mechanical patterns. See [references/reference-patterns.md](references/reference-patterns.md) for natural styles.

**Quick reference:**
| Style | Example |
|-------|---------|
| Callback | "The compound engineering loop kept surfacing..." (no link needed) |
| Context-first | "When I built X, I discovered... [that journey](url) taught me..." |
| Aside | "This approach (which I've been [systematizing](url))..." |
| Thematic echo | Name the concept, link becomes supplementary |

**Themes to watch for:** compound-engineering, skills, mcp, teaching, ai-collaboration, context-engineering, automation, research, microsim

## Data Sources
- Read git history and recent commits in current repo
- Check `/articles/chat-sessions/` for exported session data if available
- Cross-reference conversation context from this session
- Use `aichat search "topic"` to find related past sessions if relevant
- **Run `--suggest` for intelligent reference recommendations**

## Output
- Create both Markdown (.md) and HTML (.html) versions
- Store in `/articles` subfolder at the project root (create if needed)
- Filename format: `YYYY-MM-DD-descriptive-slug`
- HTML version should be publication-ready with basic styling

## Cover Images

Generate cover images using Python/PIL:

| Platform | Dimensions | Filename |
|----------|------------|----------|
| LinkedIn | 1200×628 | `YYYY-MM-DD-cover-image.png` |
| Substack | 1100×220 | `YYYY-MM-DD-substack-banner.png` |
| Twitter | 1200×675 | `YYYY-MM-DD-twitter-card.png` |

**Design:** Dark slate (#0F172A) background, amber (#FBBF24) accents, left-aligned text, large typography (48-76px titles), decorative nodes on right.

## Session Transcript Integration

After writing, ask: "Would you like me to publish this session as a shareable transcript?"

**If yes:**

First, find the current session file (most recent .jsonl for this project):
```bash
# Find the current session file
ls -t ~/.claude/projects/-Users-*-$(basename $(pwd))/*.jsonl 2>/dev/null | head -1
```

Then export using the `json` command (works non-interactively, unlike `local`):
```bash
# Use 'json' command with direct file path - works from Claude Code
uvx claude-code-transcripts json <SESSION_FILE.jsonl> --gist 2>&1 | tee /tmp/transcript-output.txt
```

**Note:** The `local` command requires interactive terminal input for session selection. Use `json` with a direct file path when running from Claude Code or scripts.

Add to article:
```markdown
## Session Transcript
This article was written during a live collaboration session.
[View the full conversation](GIST_URL) to see how we built this together.
```

## Instructions

1. **Get reference suggestions**: Run `--suggest "topic"` for the current topic
2. **Gather context**: Read git log, relevant files, session exports
3. **Outline narrative arc** of the collaboration
4. **Ask the user** about specific aspects to emphasize before writing
5. **Write article** with technical depth and conversational tone
6. **Include natural cross-references** (1-3 articles, using patterns from reference guide)
7. Create both .md and .html versions in /articles
8. **Preview**: `open /path/to/article.html`
9. **Create cover images** for all three platforms
10. **Session transcript** (ask user, add if yes)
11. Final review: Confirm all assets are ready
