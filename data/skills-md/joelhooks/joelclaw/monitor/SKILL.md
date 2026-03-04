---
name: monitor
displayName: Resource Monitor
description: "Manage feed subscriptions that track blogs, repos, and living pages for changes. Use when adding, listing, removing, or checking monitored resources. Also use when the discovery skill flags a resource as monitorable. Triggers on: 'monitor this', 'subscribe to', 'track this repo', 'watch this blog', 'what are we monitoring', 'check feeds', 'unsubscribe', 'stop monitoring', or any task involving feed subscriptions."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, monitor, feeds, subscriptions, rss, github, discovery]
---

# Resource Monitor — Track What Matters

Manage the feed subscription system (ADR-0127). Inngest cron checks subscriptions hourly, detects changes, summarizes via LLM, and notifies Joel via gateway with approve/dismiss for `/cool` publishing.

## Joel's Interest Profile

Use this to assess whether a discovered resource is worth monitoring. If a resource clearly maps to 2+ of these, **recommend monitoring** with a brief explanation.

- **Agentic AI** — agent patterns, agent infrastructure, tool use, MCP, multi-agent systems
- **Developer education** — course platforms, learning design, course-builder ecosystem
- **TypeScript tooling** — Effect ecosystem, Bun, type-level programming, compiler work
- **Inngest / durable workflows** — event-driven systems, step functions, background jobs
- **Personal AI systems** — local-first AI, semantic memory, knowledge management, RAG
- **BEAM / Elixir / OTP** — Erlang ecosystem, actor model, fault tolerance
- **Video infrastructure** — Mux, transcription, media pipelines
- **Next.js / React** — RSC, App Router, cache components, Vercel platform
- **CLI design** — agent-first interfaces, HATEOAS, terminal UIs
- **Knowledge management** — Obsidian, digital gardens, PKM, zettelkasten
- **Self-hosted infra** — homelab, k8s, Tailscale, NAS, local services
- **AT Protocol / Bluesky** — decentralized web, PDS, lexicons
- **Convex** — real-time database, reactive backends

## CLI Commands

```bash
# List all monitored subscriptions
joelclaw subscribe list

# Add a subscription (auto-detects type from URL)
joelclaw subscribe add <url> --name "Simon Willison" --interval hourly
joelclaw subscribe add <url> --name "json-render" --type github --interval daily

# Remove a subscription
joelclaw subscribe remove <id>

# Force-check a specific subscription now
joelclaw subscribe check --id <id>

# Force-check all subscriptions
joelclaw subscribe check

# Show recent updates across all subscriptions
joelclaw subscribe summary
```

### Direct Inngest Fallback (alternative)

```bash
# Add subscription via event
joelclaw send subscription/add -d '{
  "id": "simon-willison-blog",
  "name": "Simon Willison",
  "feedUrl": "https://simonwillison.net/atom/everything/",
  "type": "atom",
  "checkInterval": "hourly",
  "notify": true,
  "summarize": true,
  "publishToCool": false,
  "active": true
}'

# Force check all
joelclaw send subscription/check-feeds

# Check single
joelclaw send subscription/check-single -d '{"subscriptionId": "simon-willison-blog"}'
```

## Subscription Types

| Type | Detection | Method | Best For |
|------|-----------|--------|----------|
| `atom` / `rss` | URL ends in `/atom/`, `/feed/`, `/rss` or has XML content-type | Standard feed parse | Blogs, newsletters |
| `github` | `github.com/<owner>/<repo>` | GitHub API (releases, commits) | Open source projects |
| `page` | Any other URL | Content hash diff via defuddle | Living documents, guides |
| `bluesky` | `bsky.app` or AT Protocol handle | AT Protocol feed | Social/microblog |

## Auto-Detection Heuristics

When adding a subscription, detect the type:

1. **GitHub URL** → `github` type, check releases + significant commits
2. **URL with `/atom/` or `/feed/`** → `atom` type
3. **URL with `/rss`** → `rss` type  
4. **Blog root URL** → try `{url}/atom/`, `{url}/feed/`, `{url}/rss.xml` before falling back to `page`
5. **Everything else** → `page` type (content hash diff)

## How Updates Flow

```
Inngest cron (hourly) → subscription/check-feeds
  → fans out: subscription/check-single per subscription
    → fetch feed / API / page hash
    → new entries detected?
      → YES: subscription/summarize → LLM summary
        → gateway notification with [Publish to /cool] [Dismiss]
        → Joel approves → discovery/noted → vault note → /cool
      → NO: log quiet check, move on
```

## Notification Format

Gateway notifications for feed updates include:
- **Source name** and subscription type
- **Brief LLM summary** of what changed
- **Entry count** and links to significant items
- **Relevance tag** (which interest areas it maps to)
- **Action buttons**: [Publish to /cool] [Dismiss]

## Adding from Discovery

When the discovery skill fires and the agent assesses the resource is monitorable, use MCQ to recommend:

```
After firing joelclaw discover:

1. Assess: Is this a blog, repo, or living page with ongoing updates?
2. Assess: Does it map to 2+ items in Joel's Interest Profile above?
3. If both yes → recommend monitoring via MCQ with brief reasoning
4. If monitorable but low relevance → mention it's monitorable but don't push
5. If not monitorable (one-shot article, tweet, etc.) → don't mention monitoring
```

## Backend

- **Redis storage**: `joelclaw:subscriptions` hash (lib at `packages/system-bus/src/lib/subscriptions.ts`)
- **Inngest functions**: `packages/system-bus/src/inngest/functions/subscriptions.ts`
- **Feed checker**: `packages/system-bus/src/lib/feed-checker.ts`
- **ADR**: `~/Vault/docs/decisions/0127-feed-subscriptions-and-resource-monitoring.md`
