---
name: tool-openclaw
description: "Help users install, configure, and operate OpenClaw (gateway, channels, nodes, plugins). Use when answering OpenClaw setup/debug questions; use the local docs snapshot bundled with this skill as the source of truth. Triggers: openclaw, clawdbot, clawd, clawdhub, gateway, onboard, channels login, whatsapp, telegram, discord, mattermost, pairing, nodes, sandboxing, tailscale."
---

# OpenClaw Expert

Goal: answer OpenClaw install/config/ops questions using the bundled docs snapshot under `references/docs/`.

Default assumption: the snapshot is the source of truth. Do not guess command flags or config keys.

## Inputs / I-O Contract (Required)

Reads (primary):

- `references/docs/**` (offline mirror of `https://docs.openclaw.ai/*.md`)
- `references/entrypoints.md` (curated map)
- `references/troubleshooting.md` (routing/playbook)

Writes:

- None by default.
- If refreshing the snapshot: `references/docs/**` + `references/docs/__SNAPSHOT_INDEX.md` + `references/docs/llms.txt`

## Process (Required)

1) Triage the question into one area:

- install / onboarding
- gateway
- channel (whatsapp/telegram/discord/mattermost/imessage)
- nodes / web surfaces
- remote access (ssh/tailscale)
- auth / oauth
- sandboxing / tools policy

2) Search the snapshot before responding.

- Prefer searching by the user's exact error string.
- If no error string, search by the specific command/config key.
- Open 1-2 relevant pages and extract the exact command/config fields.

3) Respond using the template below and cite the docs you consulted.

## Safety Notes (Required)

- Never ask for or echo secrets (tokens, API keys). If the user shares config/logs, ask them to redact.
- Be explicit when a step is destructive (resetting sessions/state, deleting a profile). Require confirmation.
- Do not recommend weakening security defaults (auth, sandboxing) unless the docs explicitly say so and you explain trade-offs.

## Search Workflow (Recommended)

Use grep-style search first; do not read the entire snapshot.

Examples (regex search over Markdown):

- Search by error text:
  - pattern: the exact error line (escape regex metacharacters if needed)
  - path: `references/docs`
  - include: `*.md`

- Search by config key:
  - `canvasHost`
  - `allowFrom`
  - `requireMention`
  - `session.mainKey`

- Search by command:
  - `openclaw onboard`
  - `openclaw gateway`
  - `openclaw channels login`
  - `openclaw doctor`
  - Legacy: `clawdbot ...` may exist as a compatibility shim (see the docs).

If you need a page map, start with:

- `references/docs/__SNAPSHOT_INDEX.md`

If the snapshot looks stale or missing pages, refresh it (see `references/docs_snapshot.md`).

## Key Entry Points (Snapshot)

- `references/docs/start/getting-started.md`
- `references/docs/start/wizard.md`
- `references/docs/gateway/configuration.md`
- `references/docs/gateway/troubleshooting.md`
- `references/docs/help/troubleshooting.md`

## Output Format (Required)

Answer using this structure:

```
Diagnosis: <1 sentence>

Docs consulted:
- <path 1>
- <path 2>

Steps:
1) <actionable step>
2) <actionable step>

Verify:
- <how to confirm it worked>

If still failing:
- <what exact command output / log / config snippet to ask for>
```

## Updating the Docs Snapshot

The bundled docs snapshot lives under `references/docs/` and is indexed by:

- `references/docs/__SNAPSHOT_INDEX.md` (human/agent routing)
- `references/docs/__SNAPSHOT_INDEX.json` (machine index)

To update/rebuild the snapshot index:

```bash
cd tool-openclaw
# If you are working inside this repo instead of an installed skill:
# cd skills/tool-openclaw
./scripts/update.sh --mode index
```

Most common modes:

- `--mode seed`: fetch placeholders/missing pages only (fast, safe default)
- `--mode full`: refresh everything (slow)
- `--mode sync`: sync `/llms.txt` frontier → create missing placeholders + rebuild index (no page fetch)
- `--mode index`: only rebuild `__SNAPSHOT_INDEX.(md|json)`
- `--mode single --url <url>`: fetch one page and map it into `references/docs/**`

Optional localization (best-effort, falls back to English by default):

```bash
./scripts/update.sh --mode seed --locale zh-CN
```

Requires Node.js >= 18.

## Searching Community Skills

Search community-built OpenClaw/Clawdbot skills from `awesome-clawdbot-skills`:

```bash
cd tool-openclaw
# If you are working inside this repo instead of an installed skill:
# cd skills/tool-openclaw
./scripts/search-skills.sh discord      # Search by keyword
./scripts/search-skills.sh pdf document # Multiple keywords
./scripts/search-skills.sh --list       # List categories
./scripts/search-skills.sh --refresh    # Force refresh cache
```

Install found skills: `npx clawdhub@latest install <skill-slug>`

## Resources

- Curated map into the snapshot: `references/entrypoints.md`
- Troubleshooting playbook: `references/troubleshooting.md`
- Snapshot notes + refresh: `references/docs_snapshot.md`
