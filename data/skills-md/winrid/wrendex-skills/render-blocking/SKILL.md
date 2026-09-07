---
name: 'render-blocking'
description: 'Find render-blocking CSS and JavaScript, oversized or broken bundles, and code duplicated across bundles that ships to the browser twice. Use when the user says "render-blocking", "my site loads slowly", "too much JavaScript", "duplicate scripts", "duplicate trackers", or "reduce bundle size".'
---

# Render-Blocking Resources

Find render-blocking CSS and JS, oversized bundles, and code duplicated across bundles.

Backed by [Wrendex](https://wrendex.com), which crawls the site and runs 10 of its checks, across 4 categories.

## When to use this

- "why does my site render so slowly?"
- "find render-blocking resources"
- "am I loading the same script twice?"
- "my bundles are too big"

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
| `BROKEN_CSS` | ERROR | Broken stylesheet |
| `BROKEN_JS` | ERROR | Broken script |
| `OVERSIZED_CSS` | WARNING | Oversized stylesheet |
| `OVERSIZED_JS` | WARNING | Oversized script |
| `RENDER_BLOCKING_CSS` | WARNING | Render-blocking CSS |
| `RENDER_BLOCKING_JS` | WARNING | Render-blocking JS |
| `DUPLICATE_CSS_CODE` | NOTICE | Duplicate CSS |
| `DUPLICATE_JS_CODE` | NOTICE | Duplicate JavaScript |
| `REDIRECTED_CSS` | NOTICE | Stylesheet redirects |
| `REDIRECTED_JS` | NOTICE | Script redirects |

## Working the findings

- DUPLICATE_JS_CODE is the check most other tools do not have: it compares the actual bytes across bundles, so it catches the same library or tracker shipped twice under two filenames. Use get_duplicate_code_regions (GET /api/alerts/{alertId}/duplicate-regions) for the exact regions.
- Two tag managers, or a tag manager plus a hardcoded snippet, is the usual cause of a duplicated tracker. Check the HTML head before touching the build config.
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
