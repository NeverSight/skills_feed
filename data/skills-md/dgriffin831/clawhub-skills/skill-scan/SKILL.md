---
name: skill-scan
description: Security scanner for OpenClaw skill packages. Scans skills for malicious code, evasion techniques, prompt injection, and misaligned behavior BEFORE installation. Use to audit any skill from ClawHub or local directories.
---

# Skill-Scan — Security Auditor for Agent Skills

Multi-layered security scanner for OpenClaw skill packages. Detects malicious code, evasion techniques, prompt injection, and misaligned behavior through static analysis and optional LLM-powered deep inspection. Run this BEFORE installing or enabling any untrusted skill.

## Features

- **6 analysis layers** — pattern matching, AST/evasion, prompt injection, LLM deep analysis, alignment verification, meta-analysis
- **60+ detection rules** — execution threats, credential theft, data exfiltration, obfuscation, behavioral signatures
- **Context-aware scoring** — reduces false positives for legitimate API skills
- **ClawHub integration** — scan skills directly from the registry by slug
- **Multiple output modes** — text report (default), `--json`, `--compact`, `--quiet`
- **Exit codes** — 0 for safe, 1 for risky (easy scripting integration)

## When to Use

**MANDATORY** before installing or enabling:
- Skills from ClawHub (any skill not authored by you)
- Skills shared by other users or teams
- Skills from public repositories
- Any skill package you haven't personally reviewed

**RECOMMENDED** for periodic audits of already-installed skills.

## Quick Start

```bash
# Scan a local skill directory
skill-scan scan /path/to/skill

# Scan a skill from ClawHub before installing it
skill-scan scan-hub some-skill-slug

# Batch scan all installed skills
skill-scan batch /path/to/skills-directory

# JSON output for programmatic use
skill-scan scan-hub some-skill-slug --json

# Quiet mode (just score + verdict)
skill-scan scan-hub some-skill-slug --quiet
```

## Risk Scoring

| Risk | Score | Action |
|------|-------|--------|
| LOW | 80-100 | Safe to install |
| MEDIUM | 50-79 | Review findings before installing |
| HIGH | 20-49 | Do NOT install — serious threats detected |
| CRITICAL | 0-19 | Do NOT install — multiple critical threats |

## Exit Codes

- `0` — LOW risk (safe to proceed)
- `1` — MEDIUM or higher (block installation)

## LLM Options

```bash
skill-scan scan-hub slug --llm        # Always run deep analysis (layers 4-5)
skill-scan scan-hub slug --llm-auto   # LLM only if pattern scan finds MEDIUM+
skill-scan scan-hub slug --llm-only   # Skip patterns, LLM analysis only
```

Provider auto-detected from environment:
- `OPENAI_API_KEY` -> gpt-4o-mini
- `ANTHROPIC_API_KEY` -> claude-sonnet-4-5

## For the Agent

When the user asks to install a skill from ClawHub, follow this workflow:

1. **Scan first** — run `skill-scan scan-hub <slug>` BEFORE installing
2. **Check the result**:
   - If **LOW risk** (exit code 0): proceed with installation
   - If **MEDIUM risk**: show findings to the user and ask whether to proceed
   - If **HIGH or CRITICAL risk**: block installation and show the report
3. **Report** — always show the user the scan summary (score, risk level, finding count)

### Alert Format

When a scan finds MEDIUM or higher risk:

```
🛡️ Skill-Scan Alert: {RISK_LEVEL} ({SCORE}/100)
Skill: {slug}
Findings: {count} issue(s) detected
Top threat: {highest severity finding title}
Action: Installation blocked pending review.
```

## AGENTS.md Integration

To integrate skill-scan into your agent's workflow, add ONE of the following templates to your `AGENTS.md` (or equivalent agent instructions file).

### Option A: Automatic Scanning (Recommended)

All ClawHub skill installs are automatically scanned before installation. No manual step needed.

```markdown
## Skill-Scan — Automatic Pre-Install Security Scanning

BEFORE installing any skill from ClawHub, you MUST scan it with skill-scan first. This is non-negotiable — never skip the scan.

### Workflow

1. When the user asks to install a skill (e.g. `clawhub install <slug>`), run the scan FIRST:
   ```bash
   skill-scan scan-hub <slug>
   ```
2. **Check the exit code and output**:
   - **Exit code 0 (LOW risk)** — proceed with `clawhub install <slug>`
   - **Exit code 1 (MEDIUM risk)** — show findings to the user, ask whether to proceed
   - **Exit code 1 (HIGH/CRITICAL risk)** — BLOCK installation, show the full report
3. **Never install a HIGH or CRITICAL risk skill** without explicit user override
4. **Always show the scan summary** to the user before proceeding with installation

### Periodic Audits

When asked to audit installed skills, batch scan the skills directory:
```bash
skill-scan batch {skillsDir}
```

### LLM Deep Analysis

For high-stakes installs or when pattern scan returns MEDIUM, escalate to LLM analysis:
```bash
skill-scan scan-hub <slug> --llm-auto
```
```

### Option B: Manual On-Demand Scanning

Skills are only scanned when the user explicitly asks. Installation proceeds without automatic checks.

```markdown
## Skill-Scan — On-Demand Skill Security Scanning

skill-scan is available to audit skill packages for security threats. Use it when the user requests a security scan.

### Commands

- **Scan a ClawHub skill**: `skill-scan scan-hub <slug>`
- **Scan a local skill**: `skill-scan scan /path/to/skill`
- **Batch scan installed skills**: `skill-scan batch {skillsDir}`
- **Deep analysis with LLM**: add `--llm` or `--llm-auto` to any scan command

### Risk Levels

- **LOW (80-100)** — safe, no significant threats
- **MEDIUM (50-79)** — review findings, use caution
- **HIGH (20-49)** — serious threats, do not install
- **CRITICAL (0-19)** — multiple critical threats, do not install

### When the User Asks to Scan

1. Run the appropriate scan command
2. Show the scan summary (score, risk level, finding count)
3. If MEDIUM+, list the top findings with severity and description
4. Let the user decide what to do
```

## Install-Time Setup

When this skill is first installed, ask the user:

> **How should skill-scan integrate with your workflow?**
>
> 1. **Automatic** (Recommended) — Every `clawhub install` is scanned first. HIGH/CRITICAL installs are blocked automatically.
> 2. **Manual** — Scanning only happens when you explicitly ask for it.

Based on their choice, add the corresponding template (Option A or Option B above) to the project's `AGENTS.md`.

## Detection Categories

**Execution threats** — `eval()`, `exec()`, `child_process`, dynamic imports

**Credential theft** — `.env` access, API keys, tokens, private keys, wallet files

**Data exfiltration** — `fetch()`, `axios`, `requests`, sockets, webhooks

**Filesystem manipulation** — Write/delete/rename operations

**Obfuscation** — Base64, hex, unicode encoding, string construction

**Prompt injection** — Jailbreaks, invisible characters, homoglyphs, roleplay framing, encoded instructions

**Behavioral signatures** — Compound patterns: data exfiltration, trojan skills, evasive malware, persistent backdoors

## Requirements

- Python 3.10+
- `httpx>=0.27` (for LLM API calls only)
- API key only needed for `--llm` modes (static analysis is self-contained)

## Related Skills

- **input-guard** — External input scanning
- **memory-scan** — Agent memory security
- **guardrails** — Security policy configuration
