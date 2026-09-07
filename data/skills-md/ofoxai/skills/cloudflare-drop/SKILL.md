---
name: cloudflare-drop
description: Publish a static site (a folder of HTML/CSS/JS/images/fonts) to Cloudflare and get back a live, shareable URL in seconds. Use when you have a finished static page or site and need to hand someone a link they can open on any device — reports, mockups, one-off landing pages, AI-generated HTML, "give me a link I can share". Runs one packaged command (references/deploy.mjs) built on the Wrangler CLI, which is what Cloudflare's own agent guidance tells agents to use. Deploys permanently to your Cloudflare account when credentials are present, or as a 60-minute claimable preview when they are not — and says plainly which one you got. Bakes an expiry countdown into previews (matched to the real 60-minute limit; --ttl to shorten it), and fails open (deliver the file) rather than invent a link.
license: MIT
version: "2.2.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/cloudflare-drop
metadata:
  author: ofoxai
  version: "2.2.0"
  openclaw:
    requires:
      bins: [node, npx]
    envVars:
      - name: CLOUDFLARE_API_TOKEN
        required: false
        description: Cloudflare API token with Workers Scripts:Edit. When set, deploys permanently to your account; when absent, publishes a 60-minute claimable preview instead.
      - name: CF_API_TOKEN
        required: false
        description: Accepted as an alias for CLOUDFLARE_API_TOKEN.
    emoji: "🚀"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/cloudflare-drop
---

# cloudflare-drop: publish a static site as a shareable link

Turn a finished static page into a live URL with one command. Cloudflare serves it
from its edge at `https://<name>.<account>.workers.dev` in seconds.

**Two hosting modes, and the skill picks the one that will actually work:**

| | when | lifetime |
|---|---|---|
| **permanent** | `CLOUDFLARE_API_TOKEN` is set | forever — it's in your account |
| **temporary preview** | no usable credentials | **60 minutes**, unless claimed |

The mode is detected, not guessed, and always reported back — so you never hand
someone a link believing it's permanent when it dies in an hour.

## The one command

```bash
node references/deploy.mjs <page.html> [--ttl 30m] [--name my-report] [--permanent]
```

It resolves the countdown window → stages the page as `index.html` at a clean root
→ deploys via Wrangler → **curl-verifies HTTP 200** → prints:

```
RESULT_URL   https://my-report.ethereal-composer.workers.dev
MODE         temporary
CLAIM_LINK   https://dash.cloudflare.com/claim-preview?claimToken=…
EXPIRY_EPOCH 1785499999
```

It never prints a URL it didn't verify, and never invents one. The verify is
**content, not just status**: after the 200 backoff, the served page must match
the source's byte size (within the injected countdown's growth) and carry a body
sentinel — a blank/truncated page that still 200s fails as `URL_UNVERIFIED`.

> **`URL_UNVERIFIED` = deploy failed — do NOT deliver that URL; fall back to the
> file.** If the script prints `URL_UNVERIFIED` (no 200, or a blank/truncated page
> that didn't match the content self-verify), the deploy did not succeed. Never
> hand that URL to the user — treat it as a failure, say so plainly, and offer the
> HTML file instead (fail-open, discipline #3).

> **Why Wrangler and not the browser dropzone**: `cloudflare.com/drop`'s own
> "For AI agents" section instructs agents to prefer Wrangler for local CLI
> workflows. The packaged playwright path was **removed in 2.0.0** — the dropzone
> DOM changed and it silently returned no URL. v1 predicted this switch; this is it.

## Flags

| flag | effect |
|---|---|
| `--ttl 30m` | countdown window shown on the page. Accepts `s`/`m`/`h`/`d`; a bare number is minutes. Default **60m** (the real preview lifetime), or `$CLOUDFLARE_DROP_TTL`. Values above 60m are clamped — see below. |
| `--name my-report` | worker name (becomes the subdomain). Defaults to a sanitized filename. |
| `--permanent` | force a normal (account) deploy. Requires credentials. |
| `--no-pause-oauth` | never touch the local OAuth file (see below). |
| `--no-countdown` | skip baking the countdown into the page. The real expiry is unchanged — a temporary preview still dies at 60 minutes and the CLI still prints `EXPIRY_EPOCH`; only the on-page banner is omitted. Use when the reader finds the banner noisy and you (the operator) own the claim-before-expiry responsibility. |

## The TTL is a display, not a lifetime

The countdown baked into the page says *how long the link is expected to be
useful*. It does **not** control the real lifetime — Cloudflare does:

- On a **temporary preview**, Cloudflare hard-expires at 60 minutes. A longer TTL
  is **clamped down** and `TTL_CLAMPED` is printed. The page must never promise
  three hours on a link that dies in one.
- On a **permanent deploy**, no countdown is injected at all — a countdown on a
  link that never dies is the same lie in the other direction.

**The default is 60m for exactly this reason.** A longer default would be dead
configuration: previews clamp it away, permanent deploys drop it entirely, so it
would never once reach a reader's screen. `--ttl` is therefore for *shortening*
the window ("this is only good for the next 30 minutes"), not extending it.

**Want a link that outlives the hour?** That's not a TTL problem — set
`CLOUDFLARE_API_TOKEN` and deploy permanently, or claim the preview.

## The OAuth trap (why `--no-pause-oauth` exists)

Wrangler **refuses `--temporary` when it detects any existing auth**, but a
non-interactive shell **can't complete an OAuth login** either. A machine with a
browser-based `wrangler login` therefore deadlocks: too authenticated for a
preview, not authenticated enough to deploy.

The escape is to move the OAuth config aside for the duration of the deploy. This
touches the user's credential file, so it is:

- **opt-out-able** (`--no-pause-oauth`),
- restored in a `finally` block — **even if the deploy crashes**,
- covered by a test that asserts restoration after a thrown deploy.

If you want the permanent path instead, set `CLOUDFLARE_API_TOKEN` (Workers
Scripts: Edit is enough) and the pause never happens.

## Renewing an expired preview

```bash
node references/deploy.mjs renew <old-url|id> [--ttl 30m]
```

What it does: resolves the id from the url (the worker name — the first
`*.workers.dev` host label; legacy `drop-{id}` urls stay recognised) → reads the
deploy index → takes the archived HTML copy → **strips the stale countdown and
re-injects a fresh one** → redeploys via Wrangler under the ORIGINAL worker name
(so the renewed link stays recognisable) → self-verifies the full content is
live (size + sentinel, not just a 200) → records `renewed_from` (the chain back
to the original) → prints the **NEW** url, expiry, `RENEWED_FROM`, and
`RENEW_COUNT`.

**Expectation honesty — renew returns a *new* url, not the original.** Drop
cannot revive a dead link; a renew is a fresh deploy of the same content, so the
`*.workers.dev` address changes. Say this plainly when you deliver a renewed
link. If the id was never archived (deployed before indexing, or from another
machine), renew **fails loudly** — it won't guess or invent a link.

**Claim etiquette — offer the permanent link only at the 3rd renew (U1b).** Most
deliveries are just **the new link + a one-line expiry reminder, nothing else,
like a normal person** — no "claim it to keep it forever" pitch on every message.
The command gates this for you: it prints `RENEW_COUNT` and only surfaces a
`CLAIM_LINK` once the same content has been renewed **3 times** (`RENEW_COUNT >=
3`); before that it prints `CLAIM_OFFER none`. Follow that signal — deliver just
the link + expiry on the first delivery and the first two renews, and mention
claiming only when the tool surfaces the claim link (a page renewed three times
is one the viewer keeps returning to, so keeping it permanently is finally worth
raising).

### The deploy index, briefly

- **Home** resolves in exactly two portable layers: `$CLOUDFLARE_DROP_HOME` >
  (standalone) `~/.cloudflare-drop/`. It is **never** the skill dir or a session
  workspace — those get committed or cleaned up, so an index there would dangle.
  The skill carries no host-app awareness; an embedding app points the index at
  an instance-specific dir purely by setting `CLOUDFLARE_DROP_HOME` in the deploy
  environment (there is no baked-in middle layer).
- **`index.jsonl`** — one line per deploy, keyed on the drop id
  (title/summary/deploy-time/`expires_at`/`claim_url`/`sha256`/`renewed_from`).
- **`artifacts/<sha256>.html`** — a content-addressed copy of the deployed page;
  identical content is stored once (sha256 dedupe).
- **Pruning** (keep it small, don't over-build a GC): artifacts are
  content-addressed, so it's safe to periodically delete old files —
  `find <home>/artifacts -mtime +2 -delete`. An expired drop can't be renewed
  once its content is gone anyway, and a fresh deploy re-archives.

## When NOT to use

- The deliverable **isn't a static site** (a server app, an image, a PDF to
  download) → wrong tool.
- You have **no Node/npm** → can't run Wrangler; offer the file instead.

## Delivery discipline

1. **Always state the mode.** Permanent → say it's permanent. Temporary → say it
   expires in ~60 minutes and offer the claim link.
2. **Upload the whole folder for multi-file pages.** A lone `index.html` that
   references `style.css` renders broken. The stager copies siblings automatically.
3. **Fail open, never fabricate.** No URL, failed verify, no Node? Say so plainly
   and offer the HTML file: *"I couldn't publish it just now — want the file?"*
   A made-up `workers.dev` link is worse than an honest failure.
4. **Check the content before publishing.** Deploying makes it publicly reachable
   by URL; don't publish credentials or someone else's private data.

## Anti-patterns

- Handing back a preview URL **without the 60-minute caveat** — it silently breaks
  an hour later.
- **Inventing** a `*.workers.dev` link, or reporting one that never returned 200.
- Passing `--ttl 3h` and then telling the user the link lasts 3 hours — the clamp
  exists precisely because it doesn't. Only a permanent deploy outlives the hour.
- Leaving the user's OAuth config parked (only possible if you bypass the CLI and
  call `deployWithWrangler` yourself without the `finally`).
- Using this for something that must persist without setting a token — use the
  permanent path or Pages/Workers.
- **Uploading a page without its assets** — a lone `index.html` that references
  `style.css`/`app.js`/images renders broken.
