---
name: here-now
description: >
  Publish files and folders to the web instantly. Use when asked to "publish this",
  "host this", "deploy this", "share this on the web", "make a website", or
  "put this online". Outputs a live URL at <slug>.here.now.
---

# here.now

**Skill version: 1.3**

Publish any file or folder to the web and get a live URL back. Static hosting only.

To check for skill updates: `npx skills add heredotnow/skill --skill here-now`

## Publish

```bash
./scripts/publish.sh <file-or-dir>
```

Outputs the live URL (e.g. `https://bright-canvas-a7k2.here.now/`).

Without an API key this creates an **anonymous publish** that expires in 24 hours.
With `--api-key` or `$HERENOW_API_KEY`, the publish is permanent.

## Update an existing publish

```bash
./scripts/publish.sh <file-or-dir> --slug <slug>
```

The script auto-loads the `claimToken` from `.herenow/state.json` when updating anonymous publishes. Pass `--claim-token <token>` to override.

Authenticated updates require `--api-key` or `$HERENOW_API_KEY`.

## State file

After every publish, the script writes to `.herenow/state.json` in the working directory:

```json
{
  "publishes": {
    "bright-canvas-a7k2": {
      "siteUrl": "https://bright-canvas-a7k2.here.now/",
      "claimToken": "abc123",
      "claimUrl": "https://here.now/claim?slug=bright-canvas-a7k2&token=abc123",
      "expiresAt": "2026-02-18T01:00:00.000Z"
    }
  }
}
```

Before publishing, check this file. If the user already has a publish for the same content, update it with `--slug` instead of creating a new one.

## What to tell the user

- Always share the `siteUrl`.
- For anonymous publishes, also share the `claimUrl` so they can keep it permanently.
- Warn: the claim token is only returned once and cannot be recovered.

## Limits

|                | Anonymous          | Authenticated                |
| -------------- | ------------------ | ---------------------------- |
| Max file size  | 250 MB             | 5 GB                         |
| Expiry         | 24 hours           | Permanent (or custom TTL)    |
| Rate limit     | 5 / hour / IP      | Unlimited                    |
| Account needed | No                 | Yes (get key at here.now)    |

## Getting an API key

To upgrade from anonymous (24h) to permanent publishing:

1. Ask the user for their email address.
2. Call the sign-up endpoint to send them a magic link:

```bash
curl -sS https://here.now/api/auth/login \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```

3. Tell the user: "Check your inbox for a sign-in link from here.now. Click it, then copy your API key from the dashboard."
4. Once the user provides the key, pass it with `--api-key` or set `$HERENOW_API_KEY`.

## Script options

| Flag                   | Description                                  |
| ---------------------- | -------------------------------------------- |
| `--api-key <key>`      | API key (or set `$HERENOW_API_KEY`)               |
| `--slug <slug>`        | Update existing publish instead of creating   |
| `--claim-token <token>`| Override claim token for anonymous updates    |
| `--title <text>`       | Viewer title (non-site publishes)             |
| `--description <text>` | Viewer description                            |
| `--ttl <seconds>`      | Set expiry (authenticated only)               |
| `--base-url <url>`     | API base URL (default: `https://here.now`)    |

## Beyond the script

For delete, metadata patch, claim, list, and other operations, see [references/REFERENCE.md](references/REFERENCE.md).

Full docs: https://here.now/docs

