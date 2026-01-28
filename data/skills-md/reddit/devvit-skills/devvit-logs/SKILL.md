---
name: devvit-logs
description: 'Stream Devvit logs for an installed app (trigger phrases: "devvit logs", "stream logs", "check logs", "show logs"). Requires the user to provide the target subreddit.'
---

# Devvit Logs

Stream log events from an installed Devvit app for quick debugging. This skill wraps `devvit logs` and auto-exits after a short window (5 seconds) to avoid hanging on a streaming command.

## How It Works

1. Ask the user for the target subreddit (required).
2. Optionally accept an app name and `--since=...` flag.
3. Run `devvit logs` and capture output.
4. Exit automatically after the first burst of output or 5 seconds, whichever comes first.

## Usage

```bash
node /mnt/skills/user/devvit-logs/scripts/devvit-logs.js <subreddit> [app-name] [--since=1h]
```

**Arguments:**

- `subreddit` - Required. Subreddit to stream logs from.
- `app-name` - Optional. App name if streaming from another folder.
- `--since=Xd` - Optional. Historical logs window (e.g., `--since=30m`, `--since=1d`).

**Examples:**

```bash
node /mnt/skills/user/devvit-logs/scripts/devvit-logs.js my-subreddit
node /mnt/skills/user/devvit-logs/scripts/devvit-logs.js my-subreddit my-app --since=1h
```

## Output

```json
{
  "ok": true,
  "reason": "timeout",
  "exitCode": null,
  "signal": null,
  "stdout": "=============================== streaming logs for my-app on my-subreddit ================================\n[DEBUG] Dec 8 15:55:23 Action called!",
  "stderr": ""
}
```

## Present Results to User

- If the user did not provide a subreddit, ask for it explicitly.
- Summarize the captured logs (if any) and mention the 5-second capture window.
- If no logs were captured, say so and suggest retrying with activity or `--since=...`.

## Troubleshooting

- **Devvit CLI not found**: Install or ensure `devvit` is in PATH.
- **Not logged in**: Run `devvit login` and try again.
- **No logs**: Trigger an action in the app or use `--since=...`.
- **Permission errors**: Confirm the app is installed in the subreddit and you have access.
