---
name: agent-browser-relay
description: Read metadata and DOM payloads from an attached Chrome tab through a local Agent Browser Relay extension.
---

# Agent Browser Relay

Use this skill to attach to a chosen Chrome tab through the bundled Agent Browser Relay extension and extract tab metadata or DOM data for analysis.

## Quick start

Defaults are set in code:
- Host: `127.0.0.1`
- Port: `18793`
- Attach timeout: `120000` ms
Override per command with `--host`, `--port`, and `--attach-timeout-ms` when needed.

1. Install dependencies and start relay

   ```bash
   npm run relay:start -- --status-timeout-ms 3000
   ```

   Or pin host/port explicitly:

   ```bash
   npm run relay:start -- --host "127.0.0.1" --port "18793" --status-timeout-ms 3000
   ```

   `relay:start` auto-stops after 2 hours by default. Override if needed:

   ```bash
   node scripts/relay-manager.js start --auto-stop-ms 10800000
   node scripts/relay-manager.js start --auto-stop-ms 0
   ```

2. Load extension in Chrome

   - `chrome://extensions`
   - Enable developer mode
   - Load unpacked from `~/agent-browser-relay/extension` (this is the visible folder created by the skill helper)

3. Attach the extension to the target tab (open toolbar popup and click attach)

   Optional per-tab relay: in the popup, set **Tab port** before clicking attach if this tab should use a non-default relay port.

   Agent requirement: after `relay:start`, pause and ask the human to do this attach step, then wait for confirmation before continuing.

   If your `.agents` skill folder drops `extension/` after a `git fetch` or pull, repair it from the repo:

   ```bash
   cd ~/.agents/skills/agent-browser-relay 2>/dev/null || cd ~/.agents/skills/private/agent-browser-relay
   git sparse-checkout disable
   git config --unset-all core.sparseCheckout || true
   git config --unset-all core.sparseCheckoutCone || true
   git checkout -- .
   ```

4. Check readiness and attach state

   ```bash
   node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --tab-id "<TAB_ID>" --check --wait-for-attach --attach-timeout-ms "120000"
   ```

   Resolve `<TAB_ID>` from status first (`npm run relay:status -- --all --status-timeout-ms 3000`).
   For all agent runs, use the assigned tab id:

   ```bash
   node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --tab-id "<TAB_ID>" --check --wait-for-attach --attach-timeout-ms "120000"
   ```

   Continue only if this command returns success.

### Per-tab relay port behavior
- If you run one relay process with multiple ports, the extension can manage different relay ports per attached tab.
- A tab with no saved relay-port mapping uses the global default relay port (`18793`).
- After a successful attach, the extension saves that tab’s mapped relay port and reuses it automatically.
- Closed tabs have their mapping removed automatically.


## Mandatory behavior for agents
- Use fixed commands from this repo. Do not try to "discover" alternate script names.
- Gateway-only rule: always communicate through the local relay gateway (`/status` and `node scripts/read-active-tab.js`).
- Never use direct browser-control tooling for this workflow (for example Playwright, Puppeteer, Selenium, `agent-browser`, or ad-hoc Chrome control scripts).
- Never take control of a random Chrome window/profile. Only operate on the explicitly attached target tab leased via `--tab-id`.
- Canonical commands:
  - `npm run relay:start`
  - `npm run relay:status`
  - `npm run relay:stop`
  - `node scripts/read-active-tab.js`
- For relay health checks, always use explicit timeouts to avoid hangs:
  - `npm run relay:status -- --status-timeout-ms 3000`
  - `curl --max-time 3 -sS "http://127.0.0.1:18793/status"`
  - `npm run relay:status -- --all --status-timeout-ms 3000`
- After `relay:start`, pause and ask the human to attach the target tab before any read.
- Run `node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --tab-id "<TAB_ID>" --check --wait-for-attach --attach-timeout-ms "120000"` before reads and proceed only when it succeeds.
- If the workflow will open tabs via `Target.createTarget`, run the same check with `--require-target-create` and proceed only when it succeeds.
- For all agent runs (single-agent and concurrent), always pass `--tab-id <tabId>` on check/read commands so every operation is lease-scoped.
- Do not stop/restart relay during the task unless the human requests it or recovery is explicitly required.
- Do not restart relay only because code was updated locally; updates are applied on next explicit human-approved restart.
- If the requested `tabId` is missing from relay status `attachedTabs`, stop and ask the human to re-attach the target tab in the popup before continuing.
- If the page shows human-verification gates (for example "Are you human?" or CAPTCHA), stop immediately, alert the human with [$attention-please](/Users/mathiasasberg/.codex/skills/public/attention-please/SKILL.md), and wait for explicit human confirmation before continuing.

5. Read structured tab payload

   ```bash
   node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --tab-id "<TAB_ID>"
   ```

6. Optional one-command smoke test

   ```bash
   ./scripts/preflight.sh
   ```

## Capabilities

`read-active-tab.js` returns capability metadata in every successful payload under:

`source.capabilities`

Version compatibility checks are also included under `source.extension`:
- `installedVersion`
- `sourceVersion`
- `relayVersion`
- `observedExtensionVersion`
- `versionMismatch`

If a mismatch is detected, the command also prints a human-friendly update hint to stderr on every run.

- `scripts/read-active-tab.js` default extraction: `url`, `title`, `text`, `links`, `metaDescription`.
- Relay session leases (`--tab-id`) for concurrent agent isolation per tab on one relay port.
- `Runtime.evaluate` expression mode with `--expression`.
- Screenshot capture mode via `--screenshot` (optional `--screenshot-full-page`, `--screenshot-path`).
- Preset extraction for WhatsApp and generic chat-auditing with regex filters.
- Attach-state polling with `--check --wait-for-attach`.

## Presets and filters

- `--preset` values: `default`, `whatsapp`, `wa`, `whatsapp-messages`, `chat-audit`, `chat`.
- Regex filters: `--text-regex`, `--exclude-text-regex`, `--link-text-regex`, `--link-href-regex`.
- WhatsApp/chat filters: `--message-regex`, `--exclude-message-regex`, `--sender-regex`, `--exclude-sender-regex`.

## Common command examples

In agent workflows, use the `--tab-id` variants. Unscoped commands are for manual/local debugging only.

```bash
node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --pretty false
node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --tab-id 123 --pretty false
node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --tab-id 123 --check --wait-for-attach --require-target-create --attach-timeout-ms 120000
node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --expression "document.documentElement.outerHTML"
node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --screenshot --screenshot-full-page --screenshot-path "./tmp/page.png"
node scripts/read-active-tab.js --host "127.0.0.1" --port "18793" --preset whatsapp-messages --max-messages 200 --selector "#main"
node scripts/read-active-tab.js --preset chat-audit --selector "body" --message-regex ".*"
```

All successful commands return a `source` object with `relayHost`, `relayPort`, `relayStatusUrl`, and `relayWebSocketUrl`.

## Recommended flow with agents

Before fetching data in an automation flow, run a lightweight preflight once to ensure relay + attached tab state are ready.

For multiple agents on one relay:
- Resolve tab ids from relay status (`npm run relay:status -- --all --status-timeout-ms 3000`).
- Assign one tab id per agent.
- Use `--tab-id` in every `read-active-tab.js` call for that agent.
