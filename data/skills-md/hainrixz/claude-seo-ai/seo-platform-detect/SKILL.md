---
name: seo-platform-detect
description: Build the SiteProfile for an audited site — platform, framework, CMS plugins, hosting, environment, capabilities and write targets — by running scripts/detect-platform.mjs over the persisted PageSnapshot, then pick the knowledge cards each subagent needs. Support skill for seo-orchestrator; it merges this output with seo-vertical-detect into <run_dir>/profile.json.
user-invocable: false
allowed-tools: Read, Bash(node "${CLAUDE_PLUGIN_ROOT}/scripts/*")
---

# seo-platform-detect

The profile decides three things no module can decide on its own: which platform-conditional check
ids fire, which findings are `not_applicable` because the platform owns the thing, and which fix
adapter `fix` will reach for. Run it once per audit, right after the snapshot, before dispatch.

Detection is orthogonal to the vertical: `seo-vertical-detect` answers *what kind of site is this*,
this skill answers *what is it built on*. Both feed one `profile.json`.

## When to run

In the normal `/audit` and `/geo` flow you do **not** run this yourself: `audit.mjs` already calls the
same `detect()` over the run's homepage snapshot and persists the result as `<run_dir>/profile.json`.
Read that file first. Run the script directly only when you need a signal the headless pass could not
use — `--path <project>` for repo/package signals, `--probe` for the WordPress plugin verdict — or when
you are working outside the runner. Either way it is one run per audit, before the dispatch envelopes
are built; every subagent reads the same profile.

## How to run

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/detect-platform.mjs" --snapshot "<run_dir>/pages/<home-slug>.json"
```

Add flags when they apply, and only then:

- `--path <project>` when the user gave a local project (`--project`). This is the **only** way repo
  and package signals are consulted; without it, Payload is undetectable and Next.js router
  detection falls back to DOM markers. It is also what turns `capabilities.local_files` on, which is
  what makes local file fixes possible at all.
- `--probe` when the target is reachable and a WordPress plugin verdict matters. It requests
  `/wp-json/`, `/.well-known/ucp`, `/products.json` and `/wp-sitemap.xml` — four GETs, no more. The
  REST namespace list is the only reliable way to tell Yoast from Rank Math from AIOSEO; HTML
  comments name a plugin that printed a comment, not one that is active.
- `--out "<run_dir>/profile.platform.json"` to persist it instead of piping the stdout JSON.

Offline / fixture mode (used by the tests, and by you when there is no network):
`--html <file> [--headers <json>] [--cookies <json>] [--probes <json>] [--url <u>]`.

Exit codes: 0 ok · 1 bad invocation or unreadable input · 2 fetch failure.

## What comes back

`{ version: "detect-platform/1", target, platform, framework, cms_plugins[], hosting, environment,
capabilities, write_targets[], candidates, vertical_hints[], cards[], sources, notes[] }`.

Each of `platform` / `framework` / `cms_plugins[]` / `hosting` carries its own `confidence`
(`high` ≥ 8 with ≥ 2 signal kinds, `medium` ≥ 5, `low` ≥ 2) and the `signals` that produced it.
A layer with less evidence than that is `null` — **an unresolved platform is a result, not a gap**.
Report it as unresolved and let the run continue on `instructions`; never round a `low` up in prose.

Four layers are scored independently, so headless setups resolve correctly: a WordPress backend with
a Next.js front end yields `platform: wordpress` **and** `framework: nextjs`, and
`capabilities.head_owner` becomes `framework`. Follow `head_owner` whenever the cards disagree.

## Merging into profile.json

`<run_dir>/profile.json` is the union of this output and `seo-vertical-detect`'s. `audit.mjs` writes it: it
refreshes every key `detect()` owns and preserves the ones you added, so a `vertical` block already in the
file survives a re-run (a `--vertical` flag overrides it). Shape:

```json
{ "version": "detect-platform/1", "platform": {…}, "framework": {…}, "cms_plugins": [],
  "hosting": {…}, "environment": {…}, "capabilities": {…}, "write_targets": [],
  "candidates": {…}, "vertical_hints": [], "cards": [], "sources": {…}, "notes": [],
  "vertical": { "primary": "ecommerce", "also": [], "multilingual": false, "locales": [] } }
```

Pass `vertical_hints[]` to `seo-vertical-detect` as *signals*, never as verdicts — it must still cite
its own evidence. Pass `environment.kind` to the scorer
(`score.mjs --environment preview|staging|local`), which suppresses noindex-type severity-5 caps on
a non-production host and reports them as expected instead.

## Which card goes to which subagent

`profile.cards[]` already lists the paths (`references/platforms/<id>.md`). Put them in every
dispatch envelope as `platform_cards`, alongside the `platform` field (the absolute `profile.json`
path) and a one-line summary
(`"shopify (high) · theme head · staging theme available · environment production"`), with these two
instructions verbatim:

- **emit the card's §10 check ids** when the rule matches;
- **card §4 items ⇒ `not_applicable`** naming the owner in `evidence.observed` — never a silent pass,
  never a `fail` for something the platform will not let anyone change.

Hand out the platform card, the framework card and any plugin card together; a headless site legibly
needs all three. When `capabilities.instructions_only` is true, also tell the agents that every fix
they propose will be delivered as a click-path, so `fix_preview` must be human-readable prose rather
than a diff.

## Honesty

- `needs` in `write_targets` lists credential **key names**. Presence is checked for
  `CLAUDE_PLUGIN_OPTION_<KEY>` / `<KEY>` — values are never read, printed or logged. `ready: false`
  means "not configured", never "wrong key".
- Cookie **names** are evidence; cookie values are never recorded.
- Repo signals are absent without `--path`, probe signals absent without `--probe`, and the profile's
  `notes[]` says so. Repeat that in the report rather than presenting a partial profile as complete.
- A signal marked `UNVERIFIED` in a card's §12 may support a detection verdict but must never
  support a write. When a fix depends on an unverified API detail, the answer is `needs_api`.
