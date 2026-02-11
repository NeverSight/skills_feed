---
name: clawpilot
description: >
  Expert skill for OpenClaw (v2026.2.9) — self-hosted AI gateway connecting chat apps (WhatsApp, Telegram, Discord, Slack,
  iMessage, Signal, LINE, Matrix, Teams, Google Chat, BlueBubbles) to AI agents. Use when user asks about:
  (1) Installing, configuring, or updating OpenClaw,
  (2) Setting up or troubleshooting chat channels (e.g. "my WhatsApp bot isn't responding"),
  (3) Security hardening, auditing, or checking a local OpenClaw installation,
  (4) Inspecting openclaw.json config, prompts (SOUL.md/AGENTS.md), or session transcripts,
  (5) Multi-agent routing, session management, agent isolation,
  (6) Cloud deployment (AWS/GCP/Fly.io/Docker) and remote access (Tailscale/SSH),
  (7) Upgrading or migrating OpenClaw versions,
  (8) Discovering or installing OpenClaw skills from ClawHub,
  (9) Any mention of "openclaw", "openclaw.json", "~/.openclaw", or gateway config.
  Includes bundled scripts for security audit (CVE detection, OWASP/NIST mapping, supply chain scan),
  config inspection, prompt checking, and session scanning.
  Do NOT use for: general chatbot frameworks (Botpress, Rasa, etc.), non-OpenClaw AI gateways,
  or generic Docker/cloud questions unrelated to OpenClaw deployment.
---

# OpenClaw Expert Skill

## Security-First Principle

**Every configuration action MUST pass a security review before recommending it.**

For each setting change, evaluate:
1. **Blast radius** — If this setting is exploited, what can an attacker reach?
2. **Credential exposure** — Are secrets stored safely? Permissions correct?
3. **Network surface** — Is the gateway exposed beyond what's necessary?
4. **Prompt injection risk** — Can untrusted message content manipulate the agent?
5. **Supply chain risk** — Are installed skills/plugins from trusted sources?

When recommending configuration, always present the secure baseline first, then explain trade-offs of relaxing it.

### Critical CVEs (Must Check)

- **CVE-2026-25253** (CVSS 8.8): Token exfiltration via Control UI — fixed in 2026.1.29
- **CVE-2026-24763**: Command injection — fixed in 2026.1.29
- **CVE-2026-25157**: Command injection (chainable with 25253) — fixed in 2026.1.29

**Always verify user's version is >= 2026.1.29 before any other advice.**

## Quick Reference

| Task | Command |
|------|---------|
| Install | `npm install -g openclaw@latest` |
| Onboard | `openclaw onboard --install-daemon` |
| Start gateway | `openclaw gateway --port 18789` |
| Login channel | `openclaw channels login` |
| Health check | `openclaw health` |
| Security audit | `openclaw security audit --deep` |
| Skill safety scan | `openclaw skills scan <path>` |
| Diagnostics | `openclaw doctor` |
| Update | `openclaw update` |
| View logs | `openclaw logs` |
| Status (redacted) | `openclaw status --all` |
| Agent management | `openclaw agents list` |
| iOS/macOS node | `openclaw nodes` |

Run `openclaw --help` for full command list.

## Documentation Source

Use the reference files bundled in this skill as the primary source. They cover the core config schema, security hardening (including CVEs, OWASP mapping, NIST alignment), cloud deployment, and multi-agent routing.

Fetch from https://docs.openclaw.ai/ only when:
- The bundled references do not cover a feature the user asks about
- Version-specific behavior requires the latest docs
- A command or config key is absent from the bundled references

Full docs index: https://docs.openclaw.ai/llms.txt

## Core Architecture

```
Chat Apps --> Gateway (single process) --> AI Agent(s)
             |                              |
             +- Session manager             +- Workspace (SOUL.md, AGENTS.md, MEMORY.md)
             +- Channel routing             +- Auth profiles
             +- Tool policies               +- Memory (daily logs + vector search)
             +- Sandbox (Docker)            +- Sessions
             +- Cron scheduler              +- Skills
             +- Safety scanner              +- Subagents
             +- Agent mgmt RPC             +- iOS/macOS nodes
```

- **Gateway**: Single source of truth for sessions, routing, channel connections. Binds to `127.0.0.1:18789` by default.
- **Agents**: Isolated entities with own workspace, state dir, auth profiles, session store. Manageable via RPC (`agents.create`, `agents.update`, `agents.delete`).
- **Channels**: Plugin-based — WhatsApp, Telegram, Discord, Slack, iMessage, Signal, LINE, Matrix, Teams, Google Chat, Mattermost, BlueBubbles, Feishu, Zalo.
- **Config**: `~/.openclaw/openclaw.json` (JSON5 format). `OPENCLAW_HOME` env var overrides home directory for path resolution.
- **Nodes**: iOS alpha + macOS nodes for remote code execution via pairing.

## Secure Baseline

Always start from the secure baseline and relax only with justification. Key defaults: `bind: "loopback"`, `dmPolicy: "pairing"`, `sandbox: { mode: "non-main" }`, `redactSensitive: "tools"`.

Full baseline template and memory system config: see [Configuration Reference](references/configuration.md) and [Security Hardening](references/security.md).

## Common Workflows

### Initial Setup
1. `npm install -g openclaw@latest`
2. `openclaw onboard --install-daemon`
3. `openclaw channels login` (select channel)
4. `openclaw gateway --port 18789`
5. **Run `openclaw security audit --deep`** — fix any findings
6. **Run `openclaw skills scan`** — verify installed skills are safe
7. Verify: `openclaw health` and open `http://127.0.0.1:18789/`

### Add a Channel
1. `openclaw channels login` -> select channel
2. Configure allowlists in `openclaw.json` (never use `"*"` for production)
3. Set `dmPolicy: "pairing"` or `"allowlist"`
4. For groups: `requireMention: true`
5. **Security review**: Verify allowlist, check tool access for that channel

### Remote Access (Secure)
**Preferred: Tailscale Serve** — keeps loopback bind, no public exposure.
**Alternative: SSH tunnel** — `ssh -N -L 18789:127.0.0.1:18789 user@host`
**Never**: Bind to `0.0.0.0` without auth token + firewall.

### Troubleshooting
1. `openclaw doctor` — config validation
2. `openclaw health` — gateway status
3. `openclaw logs` — recent logs
4. `openclaw status --all` — full state (secrets redacted)
5. `openclaw memory search "topic"` — search agent memory
6. `openclaw sessions list` — view active sessions
7. Check `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

### Discover & Install Skills

When user asks about extending OpenClaw with new skills or asks "what skills are available":

1. Official registry: https://clawhub.com
2. Community curated list (1,715+ skills, 31 categories): https://github.com/VoltAgent/awesome-openclaw-skills
3. Install via CLI: `npx clawhub@latest install <skill-slug>`
4. Manual install: copy skill folder to `~/.openclaw/skills/` (global) or `<project>/skills/` (workspace)

**Security**: Third-party skills execute as trusted code. **Hundreds of malicious skills were discovered on ClawHub in early 2026.** Always:
- Run `openclaw skills scan <skill-path>` before installing (v2026.2.6+)
- Review source code, especially skills using `exec`, `browser`, or `web_fetch` tools
- Pin versions and avoid auto-updating untrusted skills

For skills config schema (load order, per-skill env/apiKey, hot reload), see [Configuration Reference](references/configuration.md#skills). For skill ecosystem URLs (ClawHub registry, community lists), see [Security Hardening — Skill Supply Chain](references/security.md#skill-supply-chain-security).

## Local Inspection Scripts

> **Prefer native CLI when available**: `openclaw security audit --deep`, `openclaw doctor`, `openclaw config get` provide authoritative results. Use the scripts below only for deeper heuristic checks or when the CLI is unavailable.

Run these scripts against the local OpenClaw installation. All accept `--state-dir PATH` to override `~/.openclaw`. Scripts use heuristic grep-based parsing of JSON5 config — results are best-effort.

### Full Security Audit
```bash
bash scripts/security_audit.sh [--state-dir ~/.openclaw]
```
Check: version/CVE status, file permissions, hardcoded credentials, network binding, DM policies, sandbox config, tool policies, log redaction, plugins, **skill supply chain** (exfiltration/reverse shell/obfuscation patterns), **Control UI security** (CVE-2026-25253), **reverse proxy config** (CVE-2026-24763), gateway process exposure, synced folder detection, session secret scanning. Maps to OWASP Agentic Top 10 and NIST CSF. Return CRITICAL/WARNING/PASS summary.

### Configuration Inspector
```bash
bash scripts/config_inspector.sh [--section gateway|channels|agents|tools|sessions|logging|all]
```
Parse `openclaw.json` and report security-relevant settings per section with colored recommendations.

### Prompt & System Instruction Checker
```bash
bash scripts/prompt_checker.sh [--workspace PATH]
```
Scan AGENTS.md, SOUL.md, USER.md, CLAUDE.md, and other bootstrap files for: missing security guardrails, overly permissive instructions, hardcoded secrets, infrastructure exposure, prompt injection vulnerabilities, and missing identity boundaries.

### Session Transcript Scanner
```bash
bash scripts/session_scanner.sh [--agent AGENT_ID] [--max-files 20] [--deep]
```
Scan `.jsonl` session files for leaked credentials (AWS keys, GitHub PATs, API keys, private keys, bot tokens, Google API keys). With `--deep`: also check for IP addresses, base64 blobs, file paths, and old files.

### Example Output

**security_audit.sh** (abbreviated):
```
============================================
  1. Version & Known Vulnerabilities
============================================
[PASS]     Version 2026.2.9 includes CVE-2026-25253/24763/25157 patches
[PASS]     Version includes skill/plugin safety scanner (v2026.2.6+)
...
============================================
  Audit Summary
============================================
  0 CRITICAL
  2 Warnings
  3 Informational
  8 Passed
```

**config_inspector.sh** (abbreviated):
```
=== Gateway Configuration ===
  Mode:      local (default)
  Bind:      loopback (default)
  Port:      18789 (default)
  ✓ Loopback bind (secure default)
```

**session_scanner.sh** (abbreviated):
```
Found 5 session file(s) to scan (max: 20)
--- agents/main/sessions/2026-02-10.jsonl (1.2M) ---
[CRITICAL]   AWS Access Key: 1 match(es)
=== Summary ===
  1 file(s) contain potential secrets (1 total matches)
```

### Script Prerequisites & Error Handling

All scripts require `bash` and standard Unix utilities (`grep`, `awk`, `wc`, `stat`). If a script fails:

- **`~/.openclaw` not found**: Pass `--state-dir PATH` to point to the actual OpenClaw home, or set `OPENCLAW_HOME`.
- **`jq` not installed**: `config_inspector.sh` uses heuristic grep-based parsing and does NOT require `jq`. Other scripts also avoid `jq`.
- **Permission denied**: Scripts only read files — ensure the current user has read access to `~/.openclaw/`. Do not run as root.
- **No session files found**: `session_scanner.sh` looks in `agents/*/sessions/*.jsonl`. If sessions are stored elsewhere, pass `--state-dir`.
- **Empty or missing `openclaw.json`**: Scripts will report warnings for missing keys but will not crash. A missing config file is treated as "all defaults."

### When to Run Scripts

| User Request | Script |
|-------------|--------|
| "Check my OpenClaw security" | `security_audit.sh` |
| "Is my config safe?" | `config_inspector.sh` |
| "Review my agent prompts" | `prompt_checker.sh` |
| "Are there leaked secrets?" | `session_scanner.sh --deep` |
| "Full security review" | Run all four in sequence |
| "Check for malicious skills" | `security_audit.sh` (section 9) + `openclaw skills scan` |

## Reference Files

Read these as needed based on the user's task:

- **[Security Hardening](references/security.md)** — Known CVEs, OWASP Agentic Top 10 mapping, NIST CSF alignment, skill supply chain security, allowlists, sandbox, tool policies, credential management, audit checklist, incident response, prompt injection defense. **Read this for ANY security-related question or before recommending config changes.**
  - Quick lookup: `grep -n "CVE\|sandbox\|dmPolicy\|tool.polic\|prompt.inject\|incident" references/security.md`

- **[Configuration Reference](references/configuration.md)** — All config keys, environment variables, channel setup (WhatsApp/Telegram/Discord/Slack/iMessage/Signal/BlueBubbles/etc.), session management, model providers, tools, logging, OPENCLAW_HOME.
  - Quick lookup: `grep -n "whatsapp\|telegram\|discord\|slack\|imessage\|signal\|bind\|sandbox\|dmPolic\|session" references/configuration.md`

- **[Cloud Deployment](references/cloud-deployment.md)** — Docker, GCP, AWS Bedrock, Fly.io, Railway, Render, Hetzner, Northflank, Nix, Ansible, macOS VM. Network architecture, IAM, volumes, remote access via Tailscale/SSH.

- **[Multi-Agent & Routing](references/multi-agent.md)** — Agent isolation, routing rules, per-agent sandbox/tools, bindings, session scoping, subagents, heartbeat, agent-to-agent communication.
