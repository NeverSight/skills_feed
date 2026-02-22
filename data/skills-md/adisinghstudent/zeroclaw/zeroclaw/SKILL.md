---
name: zeroclaw
description: Comprehensive operational knowledge for ZeroClaw, the fast, small, fully autonomous AI assistant infrastructure built in Rust. Covers CLI, 30 providers, 14 channels, config, hardware, deployment, and security.
---

# ZeroClaw — Complete Reference Skill

> Comprehensive operational knowledge for ZeroClaw, the fast, small, fully autonomous AI assistant infrastructure built in Rust.
> Source: https://github.com/zeroclaw-labs/zeroclaw | Version: 0.1.1 | Last updated: 2026-02-21

---

## What Is ZeroClaw

- **Language:** 100% Rust, single binary (~3.4-8.8MB release)
- **Memory:** <5MB RAM at runtime
- **Startup:** <10ms cold start
- **Platforms:** ARM, x86, RISC-V — runs on $10 hardware
- **Architecture:** Trait-driven, everything is swappable (providers, channels, tools, memory, tunnels, security)
- **Config:** `~/.zeroclaw/config.toml` (TOML format)
- **Workspace:** `~/.zeroclaw/workspace/` (SOUL.md, AGENTS.md, IDENTITY.md, USER.md, MEMORY.md, TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md)
- **Identity:** ZeroClaw introduces itself as ZeroClaw, never as ChatGPT/Claude/etc.

---

## Installation

```bash
# Option A: Clone + build
git clone https://github.com/zeroclaw-labs/zeroclaw.git
cd zeroclaw && ./bootstrap.sh

# Option B: Remote one-liner
curl -fsSL https://raw.githubusercontent.com/zeroclaw-labs/zeroclaw/main/scripts/bootstrap.sh | bash

# Fresh machine (install Rust + system deps)
./bootstrap.sh --install-system-deps --install-rust

# Quick onboard after install
zeroclaw onboard --api-key "your-api-key" --provider openrouter
```

### Updating ZeroClaw

```bash
# Fastest: prebuilt binary (no compile)
git clone https://github.com/zeroclaw-labs/zeroclaw.git /tmp/zeroclaw-update
cd /tmp/zeroclaw-update && bash scripts/bootstrap.sh --prefer-prebuilt
rm -rf /tmp/zeroclaw-update

# With browser-native feature (requires compile)
git clone https://github.com/zeroclaw-labs/zeroclaw.git /tmp/zeroclaw-update
cd /tmp/zeroclaw-update && cargo install --path . --force --locked --features browser-native
rm -rf /tmp/zeroclaw-update

# Verify
zeroclaw --version
```

**Note:** There is no built-in `zeroclaw update` command. Re-running `bootstrap.sh --prefer-prebuilt` from a fresh clone is the quickest path. The prebuilt binary does **not** include `browser-native` — you must build from source with `--features browser-native` if you need the `rust_native` browser backend.

---

## CLI Reference (All Commands)

### Top-Level

| Command | Purpose |
|---|---|
| `zeroclaw onboard` | Initialize workspace/config (quick setup) |
| `zeroclaw onboard --interactive` | Full interactive wizard |
| `zeroclaw onboard --channels-only` | Reconfigure channels only |
| `zeroclaw agent` | Interactive AI chat |
| `zeroclaw agent -m "Hello"` | Single message mode |
| `zeroclaw agent --provider <ID> --model <MODEL>` | Override provider/model |
| `zeroclaw agent --peripheral <board:path>` | Attach hardware peripheral |
| `zeroclaw gateway [--host H] [--port P]` | Start webhook/websocket gateway |
| `zeroclaw daemon [--host H] [--port P]` | Full autonomous runtime (gateway + channels + heartbeat + scheduler) |
| `zeroclaw status` | Show full system status |
| `zeroclaw doctor` | Run diagnostics |
| `zeroclaw providers` | List 30 supported AI providers |

### Service Management (launchd/systemd)

```bash
zeroclaw service install      # Install for auto-start
zeroclaw service start        # Start service
zeroclaw service stop         # Stop service
zeroclaw service status       # Check status
zeroclaw service uninstall    # Remove service
```

### Channel Management

```bash
zeroclaw channel list                      # List all channels + status
zeroclaw channel start                     # Start all configured channels
zeroclaw channel doctor                    # Health check channels
zeroclaw channel add <type> <json>         # Add channel (type + JSON config)
zeroclaw channel remove <name>             # Remove channel
zeroclaw channel bind-telegram <IDENTITY>  # Add Telegram user to allowlist
```

**Note:** `channel add/remove` is not a full config mutator yet — prefer editing `~/.zeroclaw/config.toml` directly or using `zeroclaw onboard`.

### Cron / Scheduling

```bash
zeroclaw cron list                              # List tasks
zeroclaw cron add "<cron-expr>" "<command>"      # Add recurring task
zeroclaw cron add --tz America/New_York "..."    # With timezone
zeroclaw cron add-at <rfc3339> "<command>"       # One-shot at timestamp
zeroclaw cron add-every <ms> "<command>"         # Fixed interval
zeroclaw cron once <delay> "<command>"           # One-shot delayed (e.g. "30m", "2h")
zeroclaw cron remove <id>
zeroclaw cron pause <id>
zeroclaw cron resume <id>
```

### Models & Providers

```bash
zeroclaw providers                          # List all 30 providers
zeroclaw models refresh                     # Refresh model catalogs
zeroclaw models refresh --provider <ID>     # Refresh specific provider
zeroclaw models refresh --force             # Force refresh
```

### Skills

```bash
zeroclaw skills list                        # List installed skills
zeroclaw skills install <source>            # Install from GitHub URL or local path
zeroclaw skills remove <name>               # Remove skill
```

### Integrations

```bash
zeroclaw integrations info <name>           # Show integration details
# Examples: Telegram, Discord, Slack, iMessage, Matrix, Signal, WhatsApp, Email, DingTalk, Ollama
```

### Auth

```bash
zeroclaw auth login --provider <ID>         # OAuth login (e.g. openai-codex)
zeroclaw auth login --provider <ID> --device-code  # Device code flow
zeroclaw auth paste-token                   # Paste auth token (Anthropic)
zeroclaw auth setup-token                   # Alias for paste-token
zeroclaw auth refresh                       # Refresh OAuth token
zeroclaw auth logout                        # Remove auth profile
zeroclaw auth use --provider <ID>           # Set active profile
zeroclaw auth list                          # List profiles
zeroclaw auth status                        # Show token expiry info
```

### Hardware & Peripherals

```bash
zeroclaw hardware discover                  # Enumerate USB devices (VID/PID)
zeroclaw hardware introspect <path>         # Introspect device
zeroclaw hardware info [--chip <name>]      # Chip info via probe-rs

zeroclaw peripheral list                    # List configured boards
zeroclaw peripheral add <board> <path>      # Add board (e.g. nucleo-f401re /dev/ttyACM0)
zeroclaw peripheral flash [--port <port>]   # Flash Arduino firmware
zeroclaw peripheral setup-uno-q             # Setup Arduino Uno Q Bridge
zeroclaw peripheral flash-nucleo            # Flash Nucleo-F401RE firmware
```

### Migration

```bash
zeroclaw migrate openclaw [--source <path>] [--dry-run]  # Import from OpenClaw
```

---

## Supported Providers (30 total)

| ID | Description |
|---|---|
| `openrouter` | OpenRouter (default) |
| `anthropic` | Anthropic |
| `openai` | OpenAI |
| `openai-codex` | OpenAI Codex (OAuth) |
| `ollama` | Ollama [local] |
| `gemini` | Google Gemini |
| `venice` | Venice |
| `vercel` | Vercel AI Gateway |
| `cloudflare` | Cloudflare AI |
| `moonshot` | Moonshot / Kimi |
| `opencode` | OpenCode Zen |
| `zai` | Z.AI |
| `glm` | GLM (Zhipu) |
| `minimax` | MiniMax |
| `bedrock` | Amazon Bedrock |
| `qianfan` | Qianfan (Baidu) |
| `qwen` | Qwen (DashScope) |
| `groq` | Groq |
| `mistral` | Mistral |
| `xai` | xAI (Grok) |
| `deepseek` | DeepSeek |
| `together` | Together AI |
| `fireworks` | Fireworks AI |
| `perplexity` | Perplexity |
| `cohere` | Cohere |
| `copilot` | GitHub Copilot |
| `lmstudio` | LM Studio [local] |
| `nvidia` | NVIDIA NIM |
| `ovhcloud` | OVHcloud AI Endpoints |
| `custom:<URL>` | Any OpenAI-compatible endpoint |
| `anthropic-custom:<URL>` | Any Anthropic-compatible endpoint |

### Custom Provider Setup

```toml
# OpenAI-compatible
default_provider = "custom:https://your-api.com"
api_key = "your-api-key"
default_model = "your-model"

# Anthropic-compatible
default_provider = "anthropic-custom:https://your-api.com"
api_key = "your-api-key"
default_model = "your-model"
```

---

## Channels (14 supported)

### Channel Matrix

| Channel | Config Section | Access Control Field | Setup |
|---|---|---|---|
| CLI | always enabled | n/a | Built-in |
| Telegram | `[channels_config.telegram]` | `allowed_users` | `zeroclaw onboard` |
| Discord | `[channels_config.discord]` | `allowed_users` | `zeroclaw onboard` |
| Slack | `[channels_config.slack]` | `allowed_users` | `zeroclaw onboard` |
| Mattermost | `[channels_config.mattermost]` | `allowed_users` | Manual config |
| Webhook | `[channels_config.webhook]` | `secret` (optional) | Manual / onboard |
| iMessage | `[channels_config.imessage]` | `allowed_contacts` | macOS only |
| Matrix | `[channels_config.matrix]` | `allowed_users` | `zeroclaw onboard` |
| Signal | `[channels_config.signal]` | `allowed_from` | Manual config |
| WhatsApp | `[channels_config.whatsapp]` | `allowed_numbers` | `zeroclaw onboard` |
| Email | `[channels_config.email]` | `allowed_senders` | Manual config |
| IRC | `[channels_config.irc]` | `allowed_users` | `zeroclaw onboard` |
| Lark | `[channels_config.lark]` | `allowed_users` | Manual config |
| DingTalk | `[channels_config.dingtalk]` | `allowed_users` | `zeroclaw onboard` |

### Deny-by-Default Allowlist Rules

- `[]` (empty) = **deny all**
- `["*"]` = **allow all** (not recommended for production)
- `["123456789", "username"]` = exact match only

### Telegram Setup

```toml
[channels_config.telegram]
bot_token = "your-bot-token"
allowed_users = []
```

```bash
# 1. Get bot token from @BotFather on Telegram
# 2. Add config above to ~/.zeroclaw/config.toml
# 3. Bind your user:
zeroclaw channel bind-telegram <USER_ID_OR_USERNAME>
# 4. Start:
zeroclaw daemon
```

**Important:** Telegram uses long-polling — no inbound port or public IP required. Only one poller per bot token allowed (don't run multiple daemons).

### Discord Setup

1. Go to https://discord.com/developers/applications
2. Create app, enable Bot, copy token
3. Enable MESSAGE CONTENT intent
4. Run `zeroclaw onboard`

### Slack Setup

1. Go to https://api.slack.com/apps
2. Create app, add Bot Token Scopes, install
3. Run `zeroclaw onboard`

### Mattermost Setup

```toml
[channels_config.mattermost]
url = "https://mm.your-domain.com"
bot_token = "your-bot-access-token"
channel_id = "your-channel-id"
allowed_users = ["user-id-1"]
thread_replies = true
mention_only = true
```

### WhatsApp Setup

```toml
[channels_config.whatsapp]
access_token = "your-access-token"
phone_number_id = "your-phone-number-id"
verify_token = "your-verify-token"
allowed_numbers = ["+1234567890"]
```

WhatsApp requires a **public URL** (webhook) — use a tunnel (Tailscale/ngrok/Cloudflare).

### Signal Setup

```toml
[channels_config.signal]
http_url = "http://127.0.0.1:8686"
account = "+1234567890"
allowed_from = ["+1987654321"]
ignore_attachments = true
ignore_stories = true
```

### Lark Setup

```toml
[channels_config.lark]
app_id = "your-app-id"
app_secret = "your-app-secret"
allowed_users = ["your-user-id"]
receive_mode = "websocket"   # or "webhook"
```

### In-Chat Commands (Telegram/Discord)

While channel server is running, users can execute:
- `/models` — show available providers
- `/models <provider>` — switch provider (sender-scoped)
- `/model` — show current model
- `/model <model-id>` — switch model (sender-scoped)

Switching clears that sender's conversation history to avoid cross-model contamination.

---

## Config Reference (`~/.zeroclaw/config.toml`)

### Core

| Key | Default | Notes |
|---|---|---|
| `default_provider` | `openrouter` | Provider ID or alias |
| `default_model` | `anthropic/claude-sonnet-4.5` | Model routed through provider |
| `default_temperature` | `0.7` | 0.0-2.0 |

### Gateway

| Key | Default | Purpose |
|---|---|---|
| `gateway.host` | `127.0.0.1` | Bind address |
| `gateway.port` | `3000` | Listen port |
| `gateway.require_pairing` | `true` | Require pairing for auth |
| `gateway.allow_public_bind` | `false` | Block accidental public exposure |

### Memory

| Key | Default | Purpose |
|---|---|---|
| `memory.backend` | `sqlite` | `sqlite`, `lucid`, `markdown`, `none` |
| `memory.auto_save` | `true` | Auto-persist |
| `memory.embedding_provider` | `none` | `none`, `openai`, or custom |
| `memory.vector_weight` | `0.7` | Hybrid search vector weight |
| `memory.keyword_weight` | `0.3` | Hybrid search keyword weight |

### Autonomy / Security

| Key | Default | Purpose |
|---|---|---|
| `autonomy.level` | `supervised` | `readonly`, `supervised`, `full` |
| `autonomy.workspace_only` | `true` | Restrict to workspace |
| `autonomy.allowed_commands` | `[git, npm, cargo, ls, cat, grep, find, echo, pwd, wc, head, tail]` | Whitelisted commands |
| `autonomy.max_actions_per_hour` | `20` | Rate limit |
| `autonomy.max_cost_per_day_cents` | `500` | Cost cap |

### Agent

| Key | Default |
|---|---|
| `agent.max_tool_iterations` | `10` |
| `agent.max_history_messages` | `50` |
| `agent.parallel_tools` | `false` |

### Browser Control

| Key | Default | Purpose |
|---|---|---|
| `browser.enabled` | `false` | Enable browser tools |
| `browser.allowed_domains` | `[]` | Domain allowlist (`["*"]` for all) |
| `browser.session_name` | (none) | Optional session identifier for persistence |
| `browser.backend` | `agent_browser` | `agent_browser`, `rust_native`, `computer_use`, `auto` |
| `browser.native_headless` | `true` | Headless mode for rust_native backend |
| `browser.native_webdriver_url` | `http://127.0.0.1:9515` | WebDriver endpoint for rust_native |
| `browser.native_chrome_path` | (auto) | Optional explicit Chrome binary path |
| `browser.computer_use.endpoint` | `http://127.0.0.1:8787/v1/actions` | Computer-use sidecar endpoint |
| `browser.computer_use.api_key` | (none) | Optional bearer token for sidecar auth (encrypted) |
| `browser.computer_use.timeout_ms` | `15000` | Per-action timeout |
| `browser.computer_use.allow_remote_endpoint` | `false` | Only allow localhost sidecar |
| `browser.computer_use.window_allowlist` | `[]` | Restrict which OS windows are targetable |
| `browser.computer_use.max_coordinate_x` | (none) | Optional X boundary for coordinate validation |
| `browser.computer_use.max_coordinate_y` | (none) | Optional Y boundary for coordinate validation |

### HTTP Requests

| Key | Default | Purpose |
|---|---|---|
| `http_request.enabled` | `false` | Enable HTTP request tool |
| `http_request.allowed_domains` | `[]` | Domain allowlist (`["*"]` for all) |
| `http_request.max_response_size` | `0` | Max response bytes (0 = unlimited) |
| `http_request.timeout_secs` | `0` | Request timeout (0 = unlimited) |

### Other Notable Sections

- `[runtime]` — native or docker sandbox
- `[reliability]` — provider retries, backoff, fallback
- `[scheduler]` — task scheduling (max 64 tasks, 4 concurrent)
- `[heartbeat]` — periodic check-ins (disabled by default)
- `[cron]` — cron scheduling
- `[tunnel]` — provider: `none`, `tailscale`, `ngrok`, `cloudflare`
- `[composio]` — Composio integration (250+ app integrations)
- `[secrets]` — encrypted secrets
- `[web_search]` — DuckDuckGo by default
- `[proxy]` — HTTP proxy support
- `[cost]` — daily/monthly limits, per-model pricing
- `[peripherals]` — hardware boards

---

## Browser Control Setup

### Browser Backends

| Backend | Mechanism | Runtime Requirement | Build Requirement |
|---|---|---|---|
| `agent_browser` (default) | Calls Vercel's `agent-browser` CLI as subprocess | `agent-browser` on `$PATH` | None (default build / prebuilt binary) |
| `rust_native` | In-process WebDriver via fantoccini | ChromeDriver running | `cargo install --features browser-native` (must build from source) |
| `computer_use` | HTTP POST to sidecar for OS-level mouse/keyboard/screen | Computer-use sidecar server | None |
| `auto` | Auto-detects best available backend | Depends on what's installed | None |

**`auto` detection priority order:** rust_native (if compiled + WebDriver reachable) -> agent_browser (if CLI installed) -> computer_use (if sidecar reachable). Falls back with helpful error if nothing is available.

**Prebuilt binary note:** The prebuilt binary from `bootstrap.sh --prefer-prebuilt` does **not** include `browser-native`. If you set `backend = "rust_native"` with the prebuilt binary, the agent will report the feature isn't enabled. You must build from source: `cargo install --path . --force --locked --features browser-native`.

### Browser Actions (17 total)

**Standard actions (all backends):**

| Action | Purpose | Notes |
|---|---|---|
| `open` | Navigate to URL | All backends |
| `snapshot` | Get accessibility tree with `@ref` element handles | **agent_browser only** — returns null on rust_native |
| `click` | Click element by CSS selector or `@ref` | `@ref` only works with agent_browser |
| `fill` | Clear field and fill with value | |
| `type` | Type text into focused element | |
| `get_text` | Extract text from element | |
| `get_title` | Get page title | |
| `get_url` | Get current URL | |
| `screenshot` | Capture page screenshot | Options: path, full_page |
| `wait` | Wait for element/time/text | |
| `press` | Press keyboard key | |
| `hover` | Hover over element | |
| `scroll` | Scroll page | Options: direction, pixels |
| `is_visible` | Check element visibility | Strict mode — selector must match exactly one element |
| `close` | Close browser | |
| `find` | Find by semantic locator | Options: role, text, label, placeholder, testid |

**Computer-use only actions (6 extra — OS-level, not DOM):**

| Action | Purpose |
|---|---|
| `mouse_move` | Move mouse to coordinates |
| `mouse_click` | Click at coordinates |
| `mouse_drag` | Drag from one point to another |
| `key_type` | Type keys via sidecar |
| `key_press` | Press individual keys |
| `screen_capture` | Capture OS screen |

Using computer-use actions on a non-computer-use backend returns a backend-specific error.

### Backend Comparison (Tested)

| Capability | agent_browser | rust_native | computer_use |
|---|---|---|---|
| open / close | yes | yes | yes |
| get_title / get_text / get_url | yes | yes | yes |
| click / fill / type | yes (CSS + @ref) | yes (CSS only) | yes (coordinates) |
| hover / scroll / press | yes | yes | yes |
| screenshot | yes | yes | yes (screen_capture) |
| is_visible | yes (strict mode) | yes | n/a |
| **snapshot (a11y tree)** | **yes (full @ref tree)** | **no (returns null)** | n/a |
| **find (semantic locator)** | partial | no | n/a |
| **Element @refs** | **yes** | **no** | n/a |
| Session persistence | yes (profile path) | no | n/a |
| Headed mode | config + executablePath | `native_headless = false` | n/a (OS-level) |
| Subprocess overhead | yes (shells out per action) | none (in-process) | yes (HTTP per action) |
| OS-level mouse/keyboard | no | no | **yes** |

**Recommendation for AI-driven automation:** Use `agent_browser`. The accessibility tree snapshot with `@ref` handles is essential — it lets the agent "see" page structure and target specific elements (e.g. `@e12`) rather than guessing CSS selectors. Use `rust_native` only for zero-Node deployments or simple scraping where you already know the selectors. Use `computer_use` when you need OS-level control beyond the browser DOM.

### Recommended Setup: `agent_browser` with Visible Chrome Window

This gives you a **visible Chrome window** that pops up on your desktop (like OpenClaw) — you can watch the AI browse, log into sites, and the profile persists cookies/sessions.

#### Step 1: Install agent-browser

```bash
npm install -g agent-browser
# Verify:
agent-browser --version
```

#### Step 2: Configure agent-browser for headed mode

Create `~/.agent-browser/config.json`:

```json
{
  "headed": true,
  "profile": "~/.agent-browser/profile",
  "executablePath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
}
```

**CRITICAL: The `executablePath` is required for headed (visible) mode.** By default, agent-browser uses Playwright's bundled Chromium (`~/Library/Caches/ms-playwright/chromium-*/`) which ignores the `headed` flag and always runs headless. Pointing to your real Google Chrome install fixes this.

Common Chrome paths:
- **macOS:** `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- **Linux:** `/usr/bin/google-chrome` or `/usr/bin/chromium`
- **Windows:** `C:\Program Files\Google\Chrome\Application\chrome.exe`

The `profile` path gives you persistent cookies/logins across sessions.

#### Step 3: Configure ZeroClaw

In `~/.zeroclaw/config.toml`:

```toml
[browser]
enabled = true
allowed_domains = ["*"]
backend = "agent_browser"
```

#### Step 4: Start daemon with headed env var (belt and suspenders)

```bash
AGENT_BROWSER_HEADED=true zeroclaw daemon
```

Or for service install, export the env var in your shell profile first.

### agent-browser CLI Reference

```bash
agent-browser open <url>              # Navigate to URL
agent-browser click <selector>        # Click element
agent-browser type <sel> <text>       # Type into element
agent-browser fill <sel> <text>       # Clear and fill
agent-browser screenshot [path]       # Take screenshot
agent-browser snapshot                # Accessibility tree with @refs (for AI)
agent-browser eval <js>               # Run JavaScript
agent-browser close                   # Close browser
agent-browser --headed open <url>     # Force visible window
agent-browser --session <name> ...    # Isolated session
agent-browser --profile <path> ...    # Persistent browser profile
```

### agent-browser Environment Variables

| Var | Purpose |
|---|---|
| `AGENT_BROWSER_HEADED` | Show browser window (not headless) |
| `AGENT_BROWSER_SESSION` | Session name |
| `AGENT_BROWSER_SESSION_NAME` | Auto-save/restore state persistence |
| `AGENT_BROWSER_PROFILE` | Persistent browser profile path |
| `AGENT_BROWSER_EXECUTABLE_PATH` | Custom browser binary |
| `AGENT_BROWSER_PROXY` | Proxy server URL |
| `AGENT_BROWSER_CONFIG` | Path to config file |
| `AGENT_BROWSER_AUTO_CONNECT` | Auto-discover running Chrome |
| `AGENT_BROWSER_STREAM_PORT` | WebSocket streaming port |

### Browser Security Model

- All URLs pass through `validate_url()` which enforces `allowed_domains`
- `file://` scheme is blocked (prevents local file exfiltration)
- Private/reserved IP ranges are rejected
- For `computer_use`: coordinate validation, endpoint must be localhost unless `allow_remote_endpoint = true`

### Troubleshooting Browser

| Problem | Solution |
|---|---|
| Browser opens but invisible (headless) | Set `executablePath` in `~/.agent-browser/config.json` to real Chrome, not Playwright Chromium |
| "domain not in allowed list" | Set `browser.allowed_domains = ["*"]` in ZeroClaw config and restart daemon |
| agent-browser not found | `npm install -g agent-browser` |
| Browser closes immediately | Check `agent-browser --version`; ensure Chrome is installed |
| Stale session | `agent-browser close` then retry |
| rust_native "feature not enabled" | Prebuilt binary lacks `browser-native` — rebuild: `cargo install --path . --force --locked --features browser-native` |
| rust_native snapshot returns null | Expected — rust_native does not support accessibility tree snapshots. Switch to `agent_browser` for snapshot/`@ref` support |
| ChromeDriver version mismatch | ChromeDriver version must match Chrome version. On macOS: `brew install --cask chromedriver` then `xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver` |
| computer_use actions fail on agent_browser | OS-level actions (mouse_move, mouse_click, etc.) only work on `computer_use` backend |
| is_visible strict mode error | Selector matched multiple elements. Use a more specific CSS selector or an `@ref` from snapshot |

---

## Full Autonomy Setup (Max Power Mode)

To unlock all capabilities and remove all restrictions:

### Config (`~/.zeroclaw/config.toml`)

```toml
[autonomy]
level = "full"
workspace_only = false
allowed_commands = ["*"]
forbidden_paths = []
max_actions_per_hour = 200
max_cost_per_day_cents = 5000
require_approval_for_medium_risk = false
block_high_risk_commands = false
auto_approve = [
    "shell",
    "file_read",
    "file_write",
    "memory_store",
    "memory_recall",
    "memory_forget",
]
always_ask = []

[agent]
compact_context = false
max_tool_iterations = 50
max_history_messages = 200
parallel_tools = true
tool_dispatcher = "auto"

[scheduler]
enabled = true
max_tasks = 128
max_concurrent = 8

[heartbeat]
enabled = true
interval_minutes = 30

[browser]
enabled = true
allowed_domains = ["*"]
backend = "agent_browser"

[http_request]
enabled = true
allowed_domains = ["*"]
max_response_size = 10485760
timeout_secs = 30

[composio]
enabled = true
entity_id = "default"

[web_search]
enabled = true
provider = "duckduckgo"
max_results = 5
timeout_secs = 15
```

### External Dependencies for Full Power

```bash
# Browser control (visible Chrome window)
npm install -g agent-browser

# agent-browser config (~/.agent-browser/config.json)
{
  "headed": true,
  "profile": "~/.agent-browser/profile",
  "executablePath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
}

# Start daemon with headed browser
AGENT_BROWSER_HEADED=true zeroclaw daemon
```

### What Each Setting Unlocks

| Setting | What it does |
|---|---|
| `autonomy.level = "full"` | No approval needed for any action |
| `autonomy.workspace_only = false` | Can access files anywhere on system |
| `autonomy.allowed_commands = ["*"]` | Can run any shell command |
| `autonomy.forbidden_paths = []` | No path restrictions |
| `block_high_risk_commands = false` | Destructive commands allowed |
| `auto_approve = [all tools]` | All tools run without confirmation |
| `agent.max_tool_iterations = 50` | 5x more tool calls per task |
| `agent.parallel_tools = true` | Run multiple tools simultaneously |
| `browser.enabled = true` | Browser automation active |
| `browser.allowed_domains = ["*"]` | Can browse any website |
| `http_request.enabled = true` | Can make HTTP requests to any domain |
| `composio.enabled = true` | 250+ app integrations (Gmail, Calendar, GitHub, etc.) |
| `heartbeat.enabled = true` | Proactive background checks every 30 min |
| `scheduler.max_concurrent = 8` | 8 parallel scheduled tasks |

### Security Warning

Full autonomy mode removes all guardrails. The agent can:
- Run any command on your system
- Read/write any file
- Browse any website with your Chrome profile (cookies, logins)
- Make HTTP requests to any domain
- Execute shell commands without approval

Only use this on trusted, personal machines. For shared/production use, keep `supervised` mode with explicit allowlists.

---

## Operations Runbook

### Runtime Modes

| Mode | Command | When |
|---|---|---|
| Foreground runtime | `zeroclaw daemon` | Local debugging |
| Gateway only | `zeroclaw gateway` | Webhook testing |
| User service | `zeroclaw service install && start` | Persistent runtime |

### Operator Checklist

```bash
zeroclaw status          # Check config
zeroclaw doctor          # Run diagnostics
zeroclaw channel doctor  # Check channel health
zeroclaw daemon          # Start runtime
```

### Safe Config Change Flow

1. Backup `~/.zeroclaw/config.toml`
2. Apply one logical change
3. Run `zeroclaw doctor`
4. Restart daemon/service
5. Verify with `status` + `channel doctor`

### Logs

- macOS/Windows: `~/.zeroclaw/logs/daemon.stdout.log`, `daemon.stderr.log`
- Linux systemd: `journalctl --user -u zeroclaw.service -f`

---

## Network Deployment

### Telegram/Discord/Slack (No Port Needed)

These use **long-polling** — outbound only. Works behind NAT, on RPi, in home labs.

```bash
zeroclaw daemon --host 127.0.0.1 --port 3000
```

### Webhook Channels (WhatsApp, etc.)

Need a public URL. Options:
- `[tunnel] provider = "tailscale"` — Tailscale Funnel
- `[tunnel] provider = "ngrok"` — ngrok tunnel
- Cloudflare Tunnel

### LAN Access

```toml
[gateway]
host = "0.0.0.0"
allow_public_bind = true
```

---

## Hardware Peripherals

### Supported Boards

| Board | Transport | Path |
|---|---|---|
| nucleo-f401re | serial | /dev/ttyACM0 |
| arduino-uno | serial | /dev/ttyACM0, /dev/cu.usbmodem* |
| arduino-uno-q | bridge | (IP) |
| rpi-gpio | native | native |
| esp32 | serial | /dev/ttyUSB0 |

### Adding a Board

```bash
zeroclaw peripheral add nucleo-f401re /dev/ttyACM0
```

Or in config:
```toml
[peripherals]
enabled = true
datasheet_dir = "docs/datasheets"

[[peripherals.boards]]
board = "nucleo-f401re"
transport = "serial"
path = "/dev/ttyACM0"
baud = 115200
```

### Two Operation Modes

1. **Edge-Native:** ZeroClaw runs directly on device (ESP32, RPi) with local GPIO/I2C/SPI
2. **Host-Mediated:** ZeroClaw on host (Mac/Linux) connects to device via USB/J-Link for development/debugging

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---|---|
| `cargo` not found | `./bootstrap.sh --install-rust` |
| `zeroclaw` not found | `export PATH="$HOME/.cargo/bin:$PATH"` |
| Gateway unreachable | Check `gateway.host`/`gateway.port` in config |
| Telegram `terminated by other getUpdates` | Stop extra daemon/channel processes — only one poller per token |
| Channel unhealthy | `zeroclaw channel doctor` then verify credentials + allowlist |
| Service not running | `zeroclaw service stop && zeroclaw service start` |
| Config world-readable warning | `chmod 600 ~/.zeroclaw/config.toml` |
| Browser opens headless (invisible) | Set `executablePath` in `~/.agent-browser/config.json` to real Chrome — Playwright's bundled Chromium ignores `headed` flag |
| "domain not in allowed list" for browser | Set `browser.allowed_domains = ["*"]` in config + restart daemon |
| Agent claims domain restrictions that don't exist | The LLM is hallucinating — tell it "allowed_domains is wildcard, browse it now" |
| `agent-browser` not found | `npm install -g agent-browser` |
| rust_native browser feature not in binary | Prebuilt binary lacks it — build from source with `--features browser-native` |
| No built-in update command | Clone repo + `bash scripts/bootstrap.sh --prefer-prebuilt` for quick update |

### Diagnostic Commands

```bash
zeroclaw --version
zeroclaw status
zeroclaw doctor
zeroclaw channel doctor
zeroclaw channel list
```

---

## Workspace Files

| File | Purpose |
|---|---|
| `SOUL.md` | Agent personality, identity, communication style |
| `AGENTS.md` | Session protocol, memory system, safety rules |
| `IDENTITY.md` | Name, creature type, vibe, emoji |
| `USER.md` | User profile, preferences, work context |
| `MEMORY.md` | Long-term curated memories (auto-injected in main session) |
| `TOOLS.md` | Local notes — SSH hosts, device names, environment specifics |
| `HEARTBEAT.md` | Periodic tasks (empty = skip heartbeat) |
| `BOOTSTRAP.md` | First-run onboarding (delete after initial setup) |

### Memory System

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs (on-demand via tools)
- **Long-term:** `MEMORY.md` — curated, auto-injected each session
- Tools: `memory_store`, `memory_recall`, `memory_forget`

---

## Security Model

- **Deny-by-default** channel allowlists
- **Gateway pairing** required by default
- **Public bind** disabled by default
- **Workspace-scoped** filesystem access
- **Command allowlist** for shell execution
- **Rate limiting** (actions/hour, cost/day)
- **Encrypted secrets** storage
- **Pluggable sandboxing** (Landlock, Firejail, Bubblewrap, Docker — feature-gated)
- **Audit logging** (proposal/roadmap — HMAC-signed tamper-evident logs)

---

## LangGraph / Python Integration

`zeroclaw-tools` Python package provides LangGraph-based tool calling for consistent behavior with any OpenAI-compatible provider:

```bash
pip install zeroclaw-tools
```

```python
from zeroclaw_tools import create_agent, shell, file_read, file_write
agent = create_agent(tools=[shell, file_read, file_write], model="glm-5", api_key="your-api-key", base_url="your-base-url")
```

---

## Open Skills Integration

ZeroClaw integrates with Open Skills (https://github.com/besoeasy/open-skills) — pre-built execution playbooks that reduce token usage by 95-98%.

Skills are synced to `~/.zeroclaw/workspace/skills/` and installed via:
```bash
zeroclaw skills install <github-url-or-local-path>
```

---

## Key Design Principles

1. **Zero overhead** — <5MB RAM, <10ms startup, ~3.4MB binary
2. **Zero compromise** — full security without sacrificing performance
3. **100% Rust** — single binary, no runtime dependencies
4. **100% Agnostic** — swap providers, channels, tools, memory, tunnels at will
5. **Trait-driven** — every subsystem is a trait, making everything pluggable
6. **Secure by default** — pairing, scoping, allowlists, encrypted secrets
