---
name: birdy
description: Install, operate, and troubleshoot birdy (multi-account proxy for the bird CLI on X/Twitter). Use when configuring birdy accounts/auth cookies, selecting rotation strategies, forwarding bird commands, setting up CI via BIRDY_ACCOUNTS, or debugging why bird/birdy-bird/bundled bird cannot be found or executed (Node 22+ requirement).
---

# Birdy

## Workflow

Use birdy to run `bird` commands through a rotating pool of X/Twitter sessions (auth cookies), reducing rate-limit risk.

### 0. Preflight (CLI Required)

If you need to run commands, ensure the `birdy` CLI is installed first:

```bash
bash skills/birdy/scripts/ensure_birdy.sh
birdy version
```

### 1. Install

Prefer the installer (bundles bird as `birdy-bird`):

```bash
curl -fsSL https://raw.githubusercontent.com/guzus/birdy/main/install.sh | bash
```

Notes:

- The installer requires GitHub CLI `gh`.
- Bundled `birdy-bird` requires Node `>= 22`.

Alternative installs:

```bash
# Installs birdy only (no bundled bird); you must provide bird yourself.
go install github.com/guzus/birdy@latest
```

### 2. Add Accounts

birdy needs two cookies per account: `auth_token` and `ct0`.

Optional: extract tokens automatically from your local browser cookies:

```bash
# Default tries Chrome, Safari, Firefox
bash skills/birdy/scripts/extract_x_tokens.sh

# Force a specific browser backend
bash skills/birdy/scripts/extract_x_tokens.sh --browsers chrome

# Pick a Chrome profile interactively (arrow keys)
bash skills/birdy/scripts/extract_x_tokens.sh --interactive
```

```bash
birdy account add personal
birdy account add work --auth-token "xxx" --ct0 "yyy"
birdy account list
```

Stored by default:

- `~/.config/birdy/accounts.json`
- `~/.config/birdy/state.json`

### 3. Run Bird Commands Through Birdy

Any unknown command/flag is forwarded to bird using the selected account.

```bash
# Auto-rotate accounts
birdy home
birdy search "golang"
birdy read 1234567890

# Show which account was used
birdy -v home

# Force an account and skip rotation
birdy --account personal whoami

# Choose rotation strategy
birdy --strategy least-used home
```

### 4. Use In CI (Non-Interactive)

Provide accounts via `BIRDY_ACCOUNTS` JSON:

```bash
export BIRDY_ACCOUNTS='[{"name":"bot1","auth_token":"xxx","ct0":"yyy"}]'
birdy -v home
```

### 5. Troubleshoot Bird Detection

birdy locates the underlying bird command in this order:

1. `BIRDY_BIRD_PATH` (explicit override)
2. `birdy-bird` on `PATH` (installed by the birdy installer)
3. Bundled package next to the `birdy` binary at `bird/dist/cli.js`
4. `bird` on `PATH`

Fixes:

- If `birdy-bird` is installed but fails: ensure `node` is available and `node --version` is `>= 22`.
- If you installed via `go install`: install bird separately, or point `BIRDY_BIRD_PATH` to a working `bird`.
- If running from a git clone: the repo vendors bird at `third_party/@steipete/bird/dist/cli.js`.

### Security

- Treat `auth_token` and `ct0` as secrets.
- Avoid pasting tokens into logs; prefer environment variables and secrets managers in CI.
