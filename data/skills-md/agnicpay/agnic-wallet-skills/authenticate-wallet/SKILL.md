---
name: authenticate-wallet
description: Sign in to AgnicPay wallet via browser-based OAuth. Use when you or the user want to authenticate, sign in, log in, connect wallet, or set up the CLI. Covers phrases like "sign in", "log in", "authenticate", "connect my wallet", "set up agnic".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx agnic@latest status*)", "Bash(npx agnic@latest auth *)"]
---

# Authenticating the AgnicPay Wallet

Use `npx agnic@latest auth login` to authenticate via browser-based OAuth. This opens the user's default browser to AgnicPay where they sign in and set spending limits for the CLI session.

## Confirm wallet is initialized and authed

```bash
npx agnic@latest status
```

If already authenticated, no further action is needed. If not authenticated, proceed with login.

## Login Flow

```bash
npx agnic@latest auth login
```

This command:
1. Starts a temporary local server on a random port
2. Opens the user's default browser to AgnicPay's OAuth consent screen
3. The user signs in (email, Google, or wallet) and approves spending limits
4. The browser redirects back to `http://localhost:<port>/callback`
5. The CLI exchanges the authorization code for tokens and saves them locally

Wait for the CLI to print `✓ Authenticated!` before proceeding.

## Verify Authentication

After login, confirm the session is active:

```bash
npx agnic@latest status
```

Expected output:

```
Wallet Status
✓ Authenticated

Email:    user@example.com
Wallet:   0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7
Expires:  2026-05-22 14:30:00 UTC
```

## Logout

To remove stored credentials:

```bash
npx agnic@latest auth logout
```

## Token Storage

Credentials are stored in `~/.agnic/config.json` with restricted permissions (`0600`). Tokens auto-refresh on 401 responses — no manual re-authentication needed until the refresh token expires (90 days).

## Error Handling

Common errors:

- "Not authenticated" — Run `npx agnic@latest auth login`
- "Authentication failed" — User cancelled the browser flow or the timeout (5 min) expired
- "Could not open browser" — The CLI prints a URL to copy and open manually
- "Token expired" — Tokens auto-refresh; if refresh also fails, re-run `npx agnic@latest auth login`
