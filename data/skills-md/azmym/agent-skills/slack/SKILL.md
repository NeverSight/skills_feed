---
name: slack
description: Interact with Slack via the Web API. Read, summarize, search, post messages, react, pin, and manage channels. Use when the user (1) shares a Slack URL, (2) asks to read or summarize a channel, (3) searches Slack messages, (4) asks to send/post a message, (5) asks to react to or pin a message, (6) looks up a user, or (7) mentions a Slack channel by name (e.g., "#channel-name"). Also triggers for Slack threads, daily standups, conversation digests, or any Slack interaction.
---

# Slack Web API Skill

Interact with Slack: read, write, search, react, pin, and manage conversations via the Web API.

## IMPORTANT: First-Use Initialization

**Before executing any Slack operation**, check if the mode config file exists:

    cat ~/.agents/config/slack/config.env

If the file does **not** exist (or does not contain `SLACK_MODE`), you **must** ask the user which mode they want to use. Present these three options:

1. **Token** (macOS only): Extracts session tokens directly from Chrome. Fastest option. Requires Chrome with Slack open, AppleScript enabled, and `uvx` installed.
2. **Browser** (cross-platform): Uses a local Playwright browser to make API calls. Works on macOS, Linux, and Windows. Requires Node.js 18+. Supports SSO and 2FA login.
3. **Auto-detect** (recommended): Automatically uses browser mode if a Playwright session exists, otherwise falls back to token mode. Best of both worlds.

Once the user selects a mode, save it immediately:

    mkdir -p ~/.agents/config/slack
    echo 'SLACK_MODE=<selected_value>' > ~/.agents/config/slack/config.env

Where `<selected_value>` is `token`, `browser`, or `auto`.

**After saving, never ask again.** On all subsequent invocations, the config file will exist and the skill will use the saved mode automatically.

If the user selected `browser` mode, also run the browser session setup:

    {SKILL_DIR}/scripts/slack-browser-session.sh login-manual

This opens a visible browser for the user to log in to Slack (supports SSO/2FA). The session is saved and reused for all future API calls.

---

## Mode Selection

The skill supports three modes. Set via `~/.agents/config/slack/config.env` or the `SLACK_MODE` environment variable:

| Mode | Value | Behavior |
|------|-------|----------|
| Token | `token` | Direct curl calls using Chrome session tokens. Fast. macOS only. |
| Browser | `browser` | API calls through a local Playwright browser session. Cross-platform. |
| Auto-detect | `auto` | Use browser if a session exists, otherwise fall back to token. **(default)** |

### Configure the mode

Option 1: Config file (persistent)

    echo 'SLACK_MODE=token' > ~/.agents/config/slack/config.env
    # or
    echo 'SLACK_MODE=browser' > ~/.agents/config/slack/config.env
    # or
    echo 'SLACK_MODE=auto' > ~/.agents/config/slack/config.env

Option 2: Environment variable (per-call override)

    SLACK_MODE=browser slack-api.sh conversations.history channel=C041RSY6DN2 limit=20

The environment variable takes priority over the config file.

## Config and State Directory

All skill config and state lives under `~/.agents/config/slack/`:

| File | Purpose |
|------|----------|
| `config.env` | Mode selection (`SLACK_MODE=auto\|token\|browser`) |
| `tokens.env` | Cached session tokens (xoxc, xoxd, user-agent) |
| `browser-session` | Active browser session ID |
| `sessions/<id>/storageState.json` | Playwright session cookies and localStorage |

This directory is created automatically on first use.

## API Wrapper

All calls go through a single unified script:

    {SKILL_DIR}/scripts/slack-api.sh <method> [key=value ...]

Where `{SKILL_DIR}` is the base directory provided when this skill is loaded (e.g., `~/.agents/skills/slack`).

The script automatically routes to the correct mode based on your configuration. For the full method reference, see [references/api-methods.md](references/api-methods.md).

## Token Mode (macOS)

Token mode extracts session tokens from your running Chrome browser and makes direct curl calls to the Slack Web API.

Prerequisites:
- Chrome running with Slack open at app.slack.com
- Chrome > View > Developer > Allow JavaScript from Apple Events
- `uvx` installed (`brew install uv`)

No manual setup needed. On first API call, tokens are extracted automatically.

## Browser Mode (Cross-Platform)

Browser mode uses a local Playwright Chromium instance to maintain a Slack session. API calls are made via `fetch()` inside the browser context, so no token extraction is needed. This works on macOS, Linux, and Windows.

Prerequisites:
- Node.js 18+ installed
- Playwright auto-installs on first use (downloads Chromium, ~150 MB)

For detailed documentation, see [references/browser-mode.md](references/browser-mode.md).

### Quick Start (Browser Mode)

    # 1. Set mode to browser
    echo 'SLACK_MODE=browser' > ~/.agents/config/slack/config.env

    # 2. Start a browser session and log in manually (supports SSO/2FA)
    {SKILL_DIR}/scripts/slack-browser-session.sh login-manual

    # Or: automated email+password login
    {SKILL_DIR}/scripts/slack-browser-session.sh start
    {SKILL_DIR}/scripts/slack-browser-session.sh login user@example.com mypassword

    # 3. Verify login succeeded
    {SKILL_DIR}/scripts/slack-browser-session.sh status

    # 4. Make API calls (same script, routes through browser automatically)
    {SKILL_DIR}/scripts/slack-api.sh conversations.history channel=C041RSY6DN2 limit=20

    # 5. Close when done
    {SKILL_DIR}/scripts/slack-browser-session.sh stop

### UI Automation (API Gaps)

Browser mode also enables direct interaction with Slack's web UI for features that lack API support:

    # Get the session ID
    SESSION_ID=$({SKILL_DIR}/scripts/slack-browser-session.sh get)

    # Navigate to a specific channel
    node {SKILL_DIR}/scripts/playwright-bridge.js --function interact --session $SESSION_ID \
      --input '{"action": "goto", "url": "https://app.slack.com/client/TEAM_ID/CHANNEL_ID"}'

    # Take a snapshot to see interactive elements
    node {SKILL_DIR}/scripts/playwright-bridge.js --function snapshot --session $SESSION_ID --input '{}'

    # Interact with UI elements using @e refs from the snapshot
    node {SKILL_DIR}/scripts/playwright-bridge.js --function interact --session $SESSION_ID \
      --input '{"action": "click", "ref": "@e5"}'

    # Take a screenshot for visual verification
    node {SKILL_DIR}/scripts/playwright-bridge.js --function screenshot --session $SESSION_ID --input '{}'

Use cases for UI automation:

- Canvas creation and editing (no public API)
- Huddle interactions (no API)
- Workflow Builder configuration
- Slack Connect invitations
- Admin and settings pages
- Visual message verification via screenshots

## Parsing Slack URLs

Extract channel and timestamp from Slack URLs:

    https://{WORKSPACE}.slack.com/archives/{CHANNEL_ID}/p{TIMESTAMP_WITHOUT_DOT}

Insert a dot before the last 6 digits of the timestamp:
- URL: p1770725748342899 -> ts: 1770725748.342899

For threaded messages, the URL may include ?thread_ts= parameter.

## Read Operations

### Read a thread

    slack-api.sh conversations.replies channel=CHANNEL_ID ts=THREAD_TS limit=100

### Read channel history

    slack-api.sh conversations.history channel=CHANNEL_ID limit=20

Optional: `oldest` / `latest` (Unix timestamps) to bound the time range.

### Search messages

    slack-api.sh search.messages query="search terms" count=10

Modifiers: `in:#channel`, `from:@user`, `before:YYYY-MM-DD`, `after:YYYY-MM-DD`, `has:link`, `has:reaction`, `has:pin`.

### Find a channel by name

    slack-api.sh conversations.list types=public_channel limit=200 | python3 -c "import sys,json; channels=json.load(sys.stdin).get('channels',[]); matches=[c for c in channels if 'TARGET' in c['name']]; [print(f\"{c['id']} #{c['name']}\") for c in matches]"

### Look up a user

    slack-api.sh users.info user=USER_ID

Name: `.user.real_name` or `.user.profile.display_name`.

### List pinned items

    slack-api.sh pins.list channel=CHANNEL_ID

### List channel members

    slack-api.sh conversations.members channel=CHANNEL_ID limit=100

## Write Operations

### Send a message

    slack-api.sh chat.postMessage channel=CHANNEL_ID text="Hello world"

Thread reply: add `thread_ts=PARENT_TS`. Broadcast to channel: add `reply_broadcast=true`.

### Edit a message

    slack-api.sh chat.update channel=CHANNEL_ID ts=MESSAGE_TS text="Updated text"

### Delete a message

    slack-api.sh chat.delete channel=CHANNEL_ID ts=MESSAGE_TS

### Add a reaction

    slack-api.sh reactions.add channel=CHANNEL_ID timestamp=MESSAGE_TS name=thumbsup

Emoji name without colons. Supports skin tones: `thumbsup::skin-tone-3`.

### Remove a reaction

    slack-api.sh reactions.remove channel=CHANNEL_ID timestamp=MESSAGE_TS name=thumbsup

### Pin a message

    slack-api.sh pins.add channel=CHANNEL_ID timestamp=MESSAGE_TS

### Unpin a message

    slack-api.sh pins.remove channel=CHANNEL_ID timestamp=MESSAGE_TS

## Image and File Handling

Messages may contain files. In token mode:

    source ~/.agents/config/slack/tokens.env
    curl -s "FILE_URL_PRIVATE" \
      -H "Authorization: Bearer ${SLACK_XOXC}" \
      -H "Cookie: d=${SLACK_XOXD}" \
      -o /tmp/slack-image-N.png

In browser mode, navigate to the file URL and screenshot:

    node {SKILL_DIR}/scripts/playwright-bridge.js --function interact --session $SESSION_ID \
      --input '{"action": "goto", "url": "FILE_URL_PRIVATE"}'
    node {SKILL_DIR}/scripts/playwright-bridge.js --function screenshot --session $SESSION_ID --input '{}'

Then use the Read tool to view the downloaded image.

## Output Formatting

1. Parse JSON with python3 -c "import sys,json; ..."
2. Resolve user IDs (U...) to real names via users.info (cache lookups)
3. Present messages with timestamps and names
4. Replace <@U...> mentions with resolved real names
5. Decode Slack markup (entities, link syntax, channel references) to plain text

## Rate Limiting

- Add sleep 1 between consecutive API calls
- Never bulk-paginate large datasets (users.list), it kills the session
- Prefer targeted queries over bulk fetches
- Browser mode has additional latency per call; batch where possible

## Token Refresh (Token Mode, Automatic)

Token refresh is fully automatic. The API wrapper:
1. Auto-refreshes if `~/.agents/config/slack/tokens.env` is missing
2. Auto-refreshes on `invalid_auth` errors and retries the call

Tokens are extracted from the running Chrome browser:
- xoxc: from Slack's localStorage via AppleScript
- xoxd: from Chrome's cookie database via `lsof` + `pycookiecheat`

## Setup

### Token Mode (macOS)

1. Open Chrome with Slack at app.slack.com
2. Enable Chrome > View > Developer > Allow JavaScript from Apple Events
3. Install uv: `brew install uv`
4. Set mode (optional, auto-detect works by default):

       echo 'SLACK_MODE=token' > ~/.agents/config/slack/config.env

### Browser Mode (Cross-Platform)

1. Install Node.js 18+ from https://nodejs.org
2. Set mode and start a session:

       echo 'SLACK_MODE=browser' > ~/.agents/config/slack/config.env
       {SKILL_DIR}/scripts/slack-browser-session.sh login-manual

   Playwright and Chromium install automatically on first use.

### Auto-detect (Default)

No configuration needed. The skill checks for an active browser session with a valid storageState first, and falls back to token mode if none exists.

## Full API Reference

For additional methods (bookmarks, user groups, reminders, emoji, files, user profiles, etc.), see [references/api-methods.md](references/api-methods.md).

## Error Handling

- not_in_channel: User does not have access to this channel
- channel_not_found: Invalid channel ID
- invalid_auth: Token expired, auto-refresh attempted (token mode)
- ratelimited: Wait and retry with sleep 5
- cant_update_message / cant_delete_message: Can only modify own messages
- no_browser_session: No active browser session; run slack-browser-session.sh start
- node_not_found: Node.js not installed; install from https://nodejs.org
- no_teams_found: Slack has not loaded workspace data in browser; wait and retry
