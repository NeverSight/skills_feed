---
name: discovery
displayName: Discovery
description: "Capture interesting finds to the Vault via Inngest. Triggers when the user shares a URL, repo, or idea with signal words like \"interesting\", \"cool\", \"neat\", \"check this out\", \"look at this\", \"came across\", or when sharing content with minimal context that implies it should be remembered. Also triggers on bare URL drops with no explicit ask. Fires a discovery/noted event and continues the conversation — the pipeline handles everything else."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, discovery, vault, inngest, capture]
---

# Discovery — Capture What's Interesting

When Joel flags something as interesting, fire it into the pipeline and keep moving.

## Trigger Detection

Signal words/patterns (case-insensitive):
- "interesting", "cool", "neat", "nice", "wild", "clever"
- "check this out", "look at this", "came across", "found this"
- "bookmarking", "save this", "remember this"
- Bare URL/repo link with minimal context (1-2 words + link)
- Sharing a link then immediately moving on

**When NOT to trigger**: If Joel is asking for help with the thing (debugging, implementing, reviewing), that's a task — not a discovery.

## Workflow

### 1. Fire `joelclaw discover`

```bash
joelclaw discover <url>
# or with context if Joel said something specific:
joelclaw discover <url> -c "what Joel said about it"
```

That's it. The pipeline handles investigation, titling, tagging, writing, and slogging.

### 2. Assess for Monitoring (before moving on)

After firing the discovery event, quickly assess:

1. **Is this monitorable?** — Does it have ongoing updates? (blog with feed, GitHub repo with releases, living document that changes)
2. **Is it relevant to Joel's interests?** — Check the interest profile in the `monitor` skill. If it maps to 2+ areas, it's a strong candidate.

**If both yes** → recommend monitoring via MCQ:
```
"This looks like an active [blog/repo/guide] covering [matched interests]. Want to add it to the monitoring list?"
  1. Yes, monitor it (hourly/daily)
  2. Not now
```

If the agent recommends monitoring and Joel accepts, add the subscription per the `monitor` skill workflow.

**If monitorable but low relevance** → mention briefly: "This has a feed if you ever want to track it" — don't push.

**If not monitorable** (one-shot article, tweet, static page) → skip, don't mention monitoring at all.

### 3. Continue conversation

Don't wait. Joel flagged something and moved on — match that energy.

## What the Pipeline Does (background, in system-bus worker)

1. **Investigate** — clone repos, extract articles via defuddle, read content
2. **Analyze via pi** — decides title, tags, relevance, writes summary in Joel's voice
3. **Embed media** — if source is a video (YouTube, etc.), auto-embeds `<YouTubeEmbed url="..." />` in the note
4. **Write** — vault note to `~/Vault/Resources/discoveries/{slug}.md`
5. **Sync** — fires `discovery/captured` event which syncs to joelclaw.com/cool/
6. **Log** — `slog write --action noted --tool discovery`

## X/Twitter URL Enrichment

When the source URL is an X/Twitter post (`x.com/*/status/*` or `twitter.com/*/status/*`):
- X blocks web scraping — **do NOT use url_to_markdown or web_search** for tweet content
- Instead, use the **x-api skill** to fetch tweet text, author, and metrics via the Twitter API v2
- Extract the tweet ID from the URL and call `GET /2/tweets/:id?tweet.fields=text,author_id,created_at,public_metrics&expansions=author_id&user.fields=name,username`
- Include tweet text, author handle, and engagement metrics in the discovery note
- See `x-api` skill for OAuth 1.0a signing details

## Deep Dig — Inngest Enrichment Pipeline (ADR-0150)

Enrichment is **not manual agent work**. The `discovery/noted` event triggers a durable Inngest function (`discovery/enrich`) that handles all enrichment automatically:

1. **Classify URL** — tweet, repo, article, video
2. **Fetch content** — X API for tweets, defuddle for articles, repo clone for repos
3. **Match tracked projects** — opencode, opentui, course-builder, pi-tools
4. **Deep dig if matched** — recent commits, PRs, issues from upstream
5. **Profile the poster** — git authors, web search, contact lookup (fires `contact/enrich` if new)
6. **Write enriched vault note** — full context, not a bare URL

The agent's job is just to fire `discovery/noted` with whatever context Joel provided. The pipeline does the rest.

### Tracked projects (canonical list in `packages/system-bus/src/config/tracked-projects.ts`)
- `anomalyco/opencode` (fork of `sst/opencode`)
- `anomalyco/opentui` (fork of `sst/opentui`)
- `badass-courses/course-builder`
- `joelhooks/pi-tools`
- `joelhooks/joelclaw`

## Video/Media Handling

When the source URL is a YouTube video (youtube.com or youtu.be):
- The discovery note gets a `<YouTubeEmbed url="..." />` component right after the title
- This renders an embedded video player on the cool page at joelclaw.com
- The note body still includes analysis/summary — the embed is supplemental, not a replacement for writing about it
