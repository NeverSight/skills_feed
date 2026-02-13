---
name: openclaw-security
description: "Unified security suite for agent workspaces. Installs, configures, and orchestrates all 11 OpenClaw security tools in one command — integrity, secrets, permissions, network, audit trail, signing, supply chain, credentials, injection defense, compliance, and incident response."
user-invocable: true
metadata: {"openclaw":{"emoji":"🔒","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Security Suite

One skill to install, configure, and orchestrate the entire OpenClaw security stack.

## Install All Security Tools

```bash
python3 {baseDir}/scripts/security.py install --workspace /path/to/workspace
```

Installs all 11 free security skills from ClawHub.

## Unified Dashboard

```bash
python3 {baseDir}/scripts/security.py status --workspace /path/to/workspace
```

Aggregated health check across all installed security tools.

## Full Security Scan

```bash
python3 {baseDir}/scripts/security.py scan --workspace /path/to/workspace
```

Runs every scanner: integrity verification, secret detection, permission audit, network DLP, supply chain analysis, injection scanning, credential exposure, and compliance audit.

## First-Time Setup

```bash
python3 {baseDir}/scripts/security.py setup --workspace /path/to/workspace
```

Initializes all tools that need it: integrity baseline, skill signing, audit ledger, compliance policy.

## Update All Tools

```bash
python3 {baseDir}/scripts/security.py update --workspace /path/to/workspace
```

Updates all installed security skills to latest versions via ClawHub.

## List Installed Tools

```bash
python3 {baseDir}/scripts/security.py list --workspace /path/to/workspace
```

Shows which security tools are installed and their versions.

## Pro Protection Sweep

```bash
python3 {baseDir}/scripts/security.py protect --workspace /path/to/workspace
```

Runs automated countermeasures across all installed Pro tools. Requires Pro versions.

## What Gets Orchestrated

| Tool | Domain | Free | Pro |
|------|--------|------|-----|
| **warden** | Workspace integrity, injection detection | Detect | Restore, rollback, quarantine |
| **sentry** | Secret/credential scanning | Detect | Redact, quarantine |
| **arbiter** | Permission auditing | Detect | Revoke, enforce |
| **egress** | Network DLP, exfiltration detection | Detect | Block, allowlist |
| **ledger** | Hash-chained audit trail | Record | Freeze, forensics |
| **signet** | Cryptographic skill signing | Verify | Reject, restore |
| **sentinel** | Supply chain security | Scan | Quarantine, block |
| **vault** | Credential lifecycle | Audit | Fix, rotate |
| **bastion** | Prompt injection defense | Scan | Sanitize, enforce |
| **marshal** | Compliance/policy enforcement | Audit | Enforce, hooks |
| **triage** | Incident response & forensics | Investigate | Contain, remediate |

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- Cross-platform: Windows, macOS, Linux
