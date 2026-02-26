---
name: solo-community-outreach
description: Find relevant Reddit, HN, and ProductHunt threads and draft value-first community responses with launch checklist. Use when user says "find communities", "draft outreach", "Reddit promotion", "ProductHunt launch", or "community marketing". Do NOT use for social media posts (use /content-gen) or video scripts (use /video-promo).
license: MIT
metadata:
  author: fortunto2
  version: "1.1.1"
  openclaw:
    emoji: "💬"
allowed-tools: Read, Grep, Glob, Write, WebSearch, WebFetch, AskUserQuestion, mcp__solograph__web_search, mcp__solograph__kb_search, mcp__solograph__project_info
argument-hint: "<project-name or idea>"
---

# /community-outreach

Find relevant community threads (Reddit, Hacker News, ProductHunt) and draft contextual, value-first responses. NOT spam — genuine helpful answers that naturally mention the product.

## MCP Tools (use if available)

- `web_search(query, engines, include_raw_content)` — search Reddit, HN, web
- `kb_search(query)` — find related methodology
- `project_info(name)` — get project details

If MCP tools are not available, use WebSearch/WebFetch as fallback.

## Steps

1. **Parse project** from `$ARGUMENTS`.
   - Read PRD/README to understand: problem, solution, ICP, key features.
   - If empty: ask via AskUserQuestion.

2. **Extract search keywords:**
   - Problem keywords (what users complain about)
   - Solution keywords (what users search for)
   - Category keywords (the market/niche)
   - Competitor names (for "vs" and "alternative" threads)

3. **Search communities** (run searches in parallel):

   ### 3a. Reddit
   For each keyword group, search via MCP `web_search(query)` or WebSearch:
   - `"{problem} reddit"` — pain point threads
   - `"{solution category} recommendations reddit"` — recommendation requests
   - `"{competitor} alternative reddit"` — competitor frustration
   - `"{competitor} vs reddit"` — comparison threads

   For each result, extract: subreddit, title, URL, post date, comment count.
   Filter: prefer threads < 6 months old, > 5 comments (active).

   ### 3b. Hacker News
   Search via `site:news.ycombinator.com`:
   - `"Show HN: {similar product category}"` — similar launches
   - `"Ask HN: {problem domain}"` — questions in the space
   - `"{competitor name} site:news.ycombinator.com"` — competitor mentions

   Extract: title, URL, points, comment count.

   ### 3c. ProductHunt
   Search via `site:producthunt.com`:
   - `"{product category} site:producthunt.com"` — similar launches
   - `"{competitor} site:producthunt.com"` — competitor pages

   Extract: product names, launch dates, upvote counts, taglines.

   ### 3d. Other Communities (optional)
   - `site:indiehackers.com "{problem}"` — Indie Hackers
   - `site:dev.to "{solution category}"` — Dev.to (if technical product)

4. **Forced reasoning — outreach strategy:**
   Before drafting, write out:
   - **Best 5 threads** to engage with (highest relevance + activity)
   - **Tone per community:** Reddit (casual, self-deprecating), HN (technical, data-driven), PH (enthusiastic, builder)
   - **Value-first angle:** What genuine help can we offer BEFORE mentioning the product?
   - **Red lines:** No astroturfing, no fake accounts, always disclose you're the builder

5. **Draft responses** for top 5 threads:

   For each thread:
   ```markdown
   ### Thread: {title}
   **URL:** {url}
   **Subreddit/Community:** {community}
   **Why relevant:** {1 sentence}

   **Draft response:**
   {2-4 paragraph response that:
   - Directly addresses the question/problem
   - Provides genuine value (tips, experience, data)
   - Mentions the product naturally (last paragraph)
   - Includes "disclaimer: I'm the developer" for transparency
   }
   ```

6. **Generate ProductHunt launch checklist:**

   ```markdown
   ## ProductHunt Launch Checklist

   ### Pre-Launch (1 week before)
   - [ ] Hunter identified (or self-hunting)
   - [ ] Tagline ready (< 60 chars): "{tagline}"
   - [ ] Description ready (< 260 chars)
   - [ ] 5+ screenshots/GIF prepared
   - [ ] Maker comment drafted (story + problem + solution)
   - [ ] Launch day scheduled (Tuesday-Thursday, 00:01 PST)

   ### Launch Day
   - [ ] Post live and verified
   - [ ] Maker comment posted immediately
   - [ ] Share in relevant communities (not vote-begging)
   - [ ] Respond to all comments within 1 hour
   - [ ] Share progress on Twitter/LinkedIn

   ### Post-Launch
   - [ ] Thank supporters
   - [ ] Collect feedback from comments
   - [ ] Update product based on feedback
   ```

7. **Write outreach plan** to `docs/outreach-plan.md`:

   ```markdown
   # Community Outreach Plan: {Project Name}

   **Generated:** {YYYY-MM-DD}
   **Product:** {one-line description}
   **ICP:** {target persona}

   ## Target Communities

   | Community | Relevant Threads Found | Priority |
   |-----------|----------------------|----------|
   | r/{subreddit} | N | high/medium/low |
   | Hacker News | N | high/medium/low |
   | ProductHunt | N | high/medium/low |

   ## Top Threads to Engage

   {5 thread drafts from step 5}

   ## ProductHunt Launch Checklist

   {checklist from step 6}

   ## Search Keywords Used
   - {keyword1}: N results
   - {keyword2}: N results

   ---
   *Generated by /community-outreach. Review all drafts before posting.*
   ```

8. **Output summary** — communities found, top 3 threads to engage, PH readiness.

## Critical Rules

1. **Value first, product second** — every response must genuinely help the person
2. **Always disclose** — "I'm the developer" or "disclaimer: I built this"
3. **No vote manipulation** — never ask for upvotes
4. **No astroturfing** — never pretend to be a user
5. **Respect community rules** — check subreddit rules before posting
6. **Quality over quantity** — 5 great responses > 50 generic ones

## Common Issues

### Web search not available
**Cause:** MCP web_search tool not configured or WebSearch not accessible.
**Fix:** Use WebSearch/WebFetch as primary. For better results with engine routing (Reddit, HN), set up [SearXNG](https://github.com/fortunto2/searxng-docker-tavily-adapter) (private, self-hosted, free) and configure solograph MCP.

### No relevant threads found
**Cause:** Niche too small or wrong keywords.
**Fix:** Broaden search terms. Try competitor names, problem descriptions, or adjacent categories.

### Responses sound promotional
**Cause:** Product mention too prominent or lacks genuine value.
**Fix:** Rewrite with value-first approach: 80% helpful answer, 20% product mention. Always include builder disclosure.
