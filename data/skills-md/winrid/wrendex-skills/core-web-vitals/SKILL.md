---
name: 'core-web-vitals'
description: 'Audit the page-weight and server-response side of Core Web Vitals: slow TTFB, missing compression, oversized HTML, and the oversized or undimensioned images behind poor LCP and CLS. Use when the user says "core web vitals", "my site is slow", "improve LCP", "layout shift", "TTFB", or "PageSpeed score".'
---

# Core Web Vitals

Server-side vitals: TTFB, compression, page weight, and the images driving LCP and CLS.

Backed by [Wrendex](https://wrendex.com), which crawls the site and runs 9 of its checks, across 2 categories.

## When to use this

- "my site is slow, what should I fix?"
- "improve my core web vitals"
- "fix layout shift on my pages"

## Running it

Node 18 or newer. No dependencies to install.

**A free scan, no account:**

```bash
node scripts/wrendex.mjs preview https://example.com
```

Returns issue **counts** by check type. It does not return which URLs are
affected - that needs a workspace.

**The full fix list:**

```bash
node scripts/wrendex.mjs signup                          # once per machine
node scripts/wrendex.mjs audit https://example.com --wait --max-pages 200
node scripts/wrendex.mjs issues <crawlId>
```

`signup` takes no email and no password. It creates a workspace, saves a
`wrn_` token to `~/.wrendex/credentials.json` (mode 0600), and returns a
**claim link**. Hand that link to the user: whoever opens it becomes the owner
of the workspace. Until someone does, the workspace cannot be funded and is
deleted after 7 days.

A new workspace starts with **500 free credits** - one per page fetched, two
when JS rendering is on - so the first audit runs immediately, before anyone
pays. Cap a large site with `--max-pages` to make them last. When they run
out, `audit` returns `{"ok": false, "code": "NO_CREDITS"}` with the claim
link: the workspace has to be claimed before it can be funded.

## Reading the output

Every command writes JSON to stdout and progress to stderr.

`issues` returns one entry per **unique problem**, ranked by `pageCount` -
how many pages it affects. The checks fire per page, so a single dead URL
linked from 400 pages is one entry with `pageCount: 400`, not 400 findings.
`pageUrls` is a capped sample; trust `pageCount` for reach.

```json
{
  "type": "LINKS_TO_BROKEN",
  "severity": "ERROR",
  "target": "https://example.com/old-pricing",
  "pageCount": 412,
  "pageUrls": ["https://example.com/", "https://example.com/blog"]
}
```

Fix in `pageCount` order. High-reach items are nearly always one edit in a
shared template.

## What this covers

| Check | Severity | What it means |
| --- | --- | --- |
| `BROKEN_IMAGE` | ERROR | Broken image |
| `MISSING_ALT_TEXT` | WARNING | Missing alt text |
| `NO_COMPRESSION` | WARNING | No HTTP compression |
| `OVERSIZED_IMAGE` | WARNING | Oversized image |
| `SLOW_PAGE` | WARNING | Slow page response |
| `SLOW_TTFB` | WARNING | Slow time-to-first-byte |
| `IMAGE_REDIRECT` | NOTICE | Image URL redirects |
| `MISSING_IMAGE_DIMENSIONS` | NOTICE | Missing image dimensions |
| `OVERSIZED_HTML` | NOTICE | Oversized HTML |

## Working the findings

- These are lab-side causes, not field measurements. Wrendex measures what the server sent; it does not report a CrUX score. Say so rather than implying a vitals number.
- MISSING_IMAGE_DIMENSIONS is the cheapest CLS fix there is: width and height attributes on the img tag, no layout change.
- NO_COMPRESSION is usually one line of server or CDN config and affects every page at once. Do it before per-page work.
- Re-run `audit` after fixing to confirm. `GET /api/crawls/{crawlId}/diff`
  shows what a crawl resolved against the previous one.
- Do not edit files you were not asked to touch. Report what you found, fix
  what the user agreed to, and leave the rest in the list.

## Reference

- [references/checks.md](references/checks.md) - every check this skill uses,
  with the fix for each.
- API reference: <https://wrendex.com/docs/api>
- Agent guide: <https://wrendex.com/agents.md> - the same crawl is reachable
  over MCP at `https://app.wrendex.com/mcp` using the token from `signup`.
