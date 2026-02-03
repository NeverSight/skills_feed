---
name: tabctl
description: Manage and analyze Edge tabs and groups with tabctl. Use when asked to list, search, analyze stale or duplicate tabs, generate reports, or organize tabs. Prefer read-only commands and only run mutating actions with explicit targets and confirmation.
---

# Tab Control

Use tabctl to inspect and analyze tabs safely, then perform targeted actions only when requested.

## Safety

- Prefer read-only commands: list, analyze, inspect, report.
- Never run `archive --all` or `close --apply` in a normal session.
- Only mutate explicit targets (`--tab`, `--group`, `--window`) and use `--confirm` for close.
- Respect policy: protected tabs are excluded.

## Common tasks

- "Which tabs I didn't look at for a week?": run `tabctl analyze --stale-days 7` and report candidates with a `stale` reason.
- List tabs in a window: `tabctl list --window <id>`
- List ungrouped tabs: `tabctl list --ungrouped`
- Generate a report: `tabctl report --format md` (add scope flags as needed)
- Get page metadata: `tabctl inspect --tab <id> --signal page-meta`
- Extract links (selector auto-enabled): `tabctl inspect --tab <id> --selector '{"name":"links","selector":"a[href]","attr":"href","all":true}'`
- Undo most recent change: `tabctl undo --latest`
- Undo by txid: `tabctl undo <txid>` (from `tabctl history --json | jq -r '.data[] | .txid'`)

## Filter results (jq / node)

When you need custom filtering, pipe the JSON output to jq or node.

- Stale candidates only (jq): `tabctl analyze --stale-days 7 | jq '.data.candidates[] | select(.reasons | any(.type == "stale")) | {tabId,title,url}'`
- Only GitHub URLs (jq): `tabctl analyze --stale-days 7 | jq '.data.candidates[] | select(.url | test("github.com"))'`
- Stale candidates only (node): `tabctl analyze --stale-days 7 | node -e 'const fs=require("fs"); const data=JSON.parse(fs.readFileSync(0,"utf8")); const stale=(data.data?.candidates||[]).filter(c=> (c.reasons||[]).some(r=>r.type==="stale")); console.log(JSON.stringify(stale,null,2));'`
- List tabs (jq): `tabctl list --json | jq -r '.data.windows[].tabs[] | select(.url | contains("devportal")) | {tabId,title,url}'`

## Narrow scope

Use one or more of: `--window`, `--group`, `--group-id`, `--tab`, `--ungrouped`.
If scope is unclear, ask for it before running mutating commands.
