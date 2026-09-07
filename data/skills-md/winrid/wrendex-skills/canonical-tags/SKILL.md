---
name: 'canonical-tags'
description: 'Audit rel=canonical tags across a site: canonicals pointing at redirects, 404s or non-indexable pages, http/https mismatches, and pages canonicalized away with no incoming links. Use when the user says "canonical tags", "canonicalization", "rel=canonical", "wrong canonical URL", or "which version of this page does Google index".'
---

# Canonical Tags

Audit rel=canonical: self-reference, redirect targets, protocol mismatches, orphans.

Backed by [Wrendex](https://wrendex.com), which crawls the site and runs 8 of its checks, across 1 categories.

## When to use this

- "check my canonical tags"
- "my canonicals point to the wrong URL"
- "fix canonicalization on example.com"

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
| `CANONICAL_HTTPS_TO_HTTP` | ERROR | Canonical https to http |
| `CANONICAL_POINTS_TO_4XX` | ERROR | Canonical points to 4xx |
| `CANONICAL_POINTS_TO_5XX` | ERROR | Canonical points to 5xx |
| `CANONICAL_POINTS_TO_REDIRECT` | WARNING | Canonical points to redirect |
| `DUPLICATES_NO_CANONICAL` | WARNING | Duplicates without canonical |
| `NON_CANONICAL_AS_CANONICAL` | WARNING | Non-canonical declared as canonical |
| `CANONICAL_HTTP_TO_HTTPS` | NOTICE | Canonical http to https |
| `CANONICAL_NO_INCOMING_LINKS` | NOTICE | Canonical has no incoming links |

## Working the findings

- CANONICAL_POINTS_TO_REDIRECT wastes the signal entirely: the canonical should name the final 200 URL, never a hop.
- CANONICAL_HTTP_TO_HTTPS and its mirror usually mean the canonical is built from a hardcoded origin somewhere in a template. Fix the template, not the pages.
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
