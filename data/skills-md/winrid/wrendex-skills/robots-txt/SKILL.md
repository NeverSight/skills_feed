---
name: 'robots-txt'
description: 'Check robots.txt and the indexing directives around it: an unreachable robots.txt, noindex and nofollow pages, and conflicting meta-tag versus header signals. Use when the user says "robots.txt", "am I blocking Google", "noindex", "nofollow", or "my pages are excluded from search".'
---

# robots.txt

Check robots.txt reachability and the noindex/nofollow directives around it.

Backed by [Wrendex](https://wrendex.com), which crawls the site and runs 7 of its checks, across 2 categories.

## When to use this

- "check my robots.txt"
- "am I accidentally blocking Google?"
- "which pages are noindex?"

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
| `ROBOTS_TXT_INACCESSIBLE` | ERROR | robots.txt inaccessible |
| `NOINDEX_CONFLICT` | WARNING | Conflicting noindex signals |
| `NOINDEX_NOFOLLOW` | WARNING | noindex, nofollow |
| `NOINDEX_PAGE` | WARNING | Page is noindex |
| `NOFOLLOW_CONFLICT` | NOTICE | Conflicting nofollow signals |
| `NOFOLLOW_PAGE` | NOTICE | Page-level nofollow |
| `NOINDEX_FOLLOW` | NOTICE | noindex, follow |

## Working the findings

- ROBOTS_TXT_INACCESSIBLE is an ERROR because a 5xx on robots.txt makes well-behaved crawlers back off the whole site. A 404 is fine; a timeout is not.
- Read the noindex findings as an inventory, not a defect list. The useful question for the user is which of these they intended.
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
