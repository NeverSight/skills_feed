---
name: clawdbot-security
description: Security hardening for Clawdbot Gateway. Use when running security audits, interpreting audit findings, configuring DM/group policies, setting up sandboxing, managing elevated tools, extracting secrets to .env, or responding to security incidents. Also triggers on questions about prompt injection defense, access control, network exposure, or the three-layer security model (sandbox, tool policy, elevated).
---

# Clawdbot Security

Harden Clawdbot Gateway deployments by fetching current security practices and applying them.

## Fetch Current Docs First

Before advising on security, fetch the latest official documentation:

```bash
# Primary security guide
web_fetch https://raw.githubusercontent.com/clawdbot/clawdbot/main/docs/gateway/security.md

# Specific topics
web_fetch https://raw.githubusercontent.com/clawdbot/clawdbot/main/docs/gateway/sandboxing.md
web_fetch https://raw.githubusercontent.com/clawdbot/clawdbot/main/docs/gateway/authentication.md
web_fetch https://raw.githubusercontent.com/clawdbot/clawdbot/main/docs/gateway/pairing.md
```

## Quick Commands

```bash
clawdbot security audit           # Basic check
clawdbot security audit --deep    # Live Gateway probe
clawdbot security audit --fix     # Auto-apply safe fixes
clawdbot sandbox explain          # Debug sandbox/tool policy
```

## Decision Tree

```
User needs help with security
├── Running audit or interpreting findings?
│   └── Run `clawdbot security audit`, explain findings, suggest fixes
├── Configuring access control (DM/group policies)?
│   └── Fetch security.md, explain pairing vs allowlist vs open
├── Setting up sandboxing?
│   └── Fetch sandboxing.md, explain mode/scope/workspaceAccess
├── Managing secrets in config?
│   └── Run scripts/extract_secrets.py or guide manual .env creation
├── Responding to incident?
│   └── Follow contain → rotate → audit workflow
└── General security question?
    └── Fetch security.md, consult references/quick-reference.md
```

## Three-Layer Model (Quick Summary)

1. **Sandbox** — Where tools run (Docker vs host)
2. **Tool Policy** — Which tools are allowed
3. **Elevated** — Exec-only host escape hatch

For details, read [references/quick-reference.md](references/quick-reference.md).

## Extract Secrets Script

Automate moving hardcoded secrets from config to `.env`:

```bash
python scripts/extract_secrets.py --dry-run  # Preview
python scripts/extract_secrets.py            # Execute
```

## Audit Priority Order

1. **Open groups + tools** → Lock down with allowlists
2. **Network exposure** → Fix immediately
3. **Browser control** → Require token auth
4. **File permissions** → `chmod 600` config, `chmod 700` dirs
5. **Plugins** → Only load trusted ones
6. **Model choice** → Use instruction-hardened models (Opus 4.5)

## Incident Response

1. **Contain**: Stop gateway, `bind: "loopback"`, freeze policies
2. **Rotate**: gateway.auth.token, API keys, browser control token
3. **Audit**: Check logs (`/tmp/clawdbot/*.log`) and transcripts
4. **Re-run**: `clawdbot security audit --deep`
