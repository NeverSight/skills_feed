---
name: skill-security-audit
description: Detect malicious patterns in AI Agent skills — 13 detectors for backdoors, credential theft, data exfiltration, and supply-chain attacks. Based on SlowMist's ClawHub threat intelligence (472+ malicious skills). Pure Python, zero dependencies.
---

# Skill Security Audit

Detect malicious patterns in installed Claude and OpenClaw skills. Based on SlowMist's analysis of 472+ malicious skills on ClawHub platform.

## Triggers

Use this skill when the user mentions: 安全审计, security audit, skill 检查, 技能安全, scan skills, supply chain security, 扫描技能, 恶意检测, malicious skill, skill 安全扫描

## Quick Audit Workflow

When the user requests a security audit, follow these 5 steps:

### Step 1: Run the Scanner

```bash
python3 ~/.claude/skills/skill-security-audit/scripts/skill_audit.py
```

This auto-discovers and scans all skills in:
- `~/.claude/skills/`
- `~/.openclaw/workspace/skills/`
- Extra directories from `~/.openclaw/openclaw.json` → `skills.load.extraDirs`

### Step 2: Analyze Results

Read the scanner output. Findings are grouped by skill and sorted by severity:

| Severity | Meaning | Action Required |
|----------|---------|----------------|
| **CRITICAL** | Known malicious IOC match, credential theft, or download-and-execute | Immediate removal and credential rotation |
| **HIGH** | Obfuscation, persistence mechanisms, privilege escalation | Manual review required, likely malicious |
| **MEDIUM** | Suspicious patterns (Base64, network calls, high entropy) | Review context — may be legitimate |
| **LOW** | Social engineering naming, informational | Note for awareness |

### Step 3: Report to User

Present findings in this format:

```
## Audit Summary
- Skills scanned: N
- Files scanned: N
- CRITICAL: N | HIGH: N | MEDIUM: N | LOW: N

## Critical/High Findings (if any)
For each finding:
- Skill name and file path
- What was detected and why it's dangerous
- Recommended action

## Medium/Low Findings (if any)
Brief summary, noting which are likely false positives
```

### Step 4: Recommend Actions

For CRITICAL findings:
1. Read `references/remediation-guide.md` for incident response steps
2. Guide user through credential rotation if credential theft was detected
3. Help quarantine the malicious skill

For HIGH findings:
1. Help user manually review the flagged code
2. Determine if the pattern is legitimate or malicious in context

### Step 5: Follow Up

- Offer to scan a specific skill in detail: `python3 skill_audit.py --path /path/to/skill`
- Offer to explain any finding in depth using `references/threat-patterns.md`

## Scanner Command Reference

```bash
# Scan all discovered skills
python3 ~/.claude/skills/skill-security-audit/scripts/skill_audit.py

# Scan a single skill directory
python3 ~/.claude/skills/skill-security-audit/scripts/skill_audit.py --path /path/to/skill

# JSON output (for programmatic use)
python3 ~/.claude/skills/skill-security-audit/scripts/skill_audit.py --json

# Filter by minimum severity
python3 ~/.claude/skills/skill-security-audit/scripts/skill_audit.py --severity high

# Disable colored output
python3 ~/.claude/skills/skill-security-audit/scripts/skill_audit.py --no-color

# Use custom IOC database
python3 ~/.claude/skills/skill-security-audit/scripts/skill_audit.py --ioc-db /path/to/ioc.json
```

**Exit codes:** 0 = clean, 1 = low/medium risk, 2 = high risk, 3 = critical, 4 = scanner error

## 13 Detection Categories

| Detector | What It Finds | Severity |
|----------|--------------|----------|
| Base64Detector | Encoded strings >50 chars (excluding data:image) | MEDIUM→HIGH |
| DownloadExecDetector | curl\|bash, wget\|sh, fetch+eval patterns | CRITICAL |
| IOCMatchDetector | Known malicious IPs, domains, URLs, file hashes | CRITICAL |
| ObfuscationDetector | eval/exec with non-literal args, hex encoding, chr() chains | HIGH |
| ExfiltrationDetector | ZIP+upload combos, sensitive directory enumeration | HIGH |
| CredentialTheftDetector | osascript password dialogs, keychain access, SSH key reading | CRITICAL |
| PersistenceDetector | crontab, launchd, systemd, shell profile modification | HIGH |
| PostInstallHookDetector | npm postinstall, pip setup.py cmdclass | HIGH→CRITICAL |
| HiddenCharDetector | Zero-width characters, Unicode bidi overrides | MEDIUM |
| EntropyDetector | Shannon entropy >5.5 on long lines | MEDIUM |
| SocialEngineeringDetector | crypto/wallet/airdrop/security-update naming | LOW→MEDIUM |
| NetworkCallDetector | socket, http, urllib, requests, fetch, curl, wget | MEDIUM |
| PrivilegeEscalationDetector | sudo, chmod 777, setuid, admin group modification | HIGH |

## Understanding Confidence Scores

Each finding includes a confidence score (0-100):
- **80-100**: Very likely a genuine threat
- **50-79**: Suspicious, manual review recommended
- **30-49**: Possible false positive, check context
- **<30**: Informational, low confidence

## Manual Review Checklist

When the scanner flags something, also check:

1. **Source verification** — Is the skill from an official/verified source? Check author reputation.
2. **Permission scope** — Does the skill request more permissions than its stated functionality needs?
3. **Script audit** — Read all `.sh`, `.py`, `.js` files. Look for obfuscation, unexpected network calls.
4. **Dependency check** — Run `npm audit` or `pip-audit` if the skill has package dependencies.
5. **Changelog review** — Were suspicious changes introduced in a recent update?

## Updating the IOC Database

The IOC database is at `scripts/ioc_database.json`. To add new indicators:

1. Edit the JSON file following the existing schema
2. Run the scanner to verify your new IOCs are detected
3. Update `references/ioc-database.md` to keep the human-readable version in sync

## Reference Documents

For detailed information, read these files as needed:
- `references/ioc-database.md` — Full IOC list with context and attribution
- `references/threat-patterns.md` — 9 attack patterns in detail (two-stage payload, Base64 backdoor, password phishing, etc.)
- `references/remediation-guide.md` — Step-by-step incident response (quarantine, credential rotation, persistence cleanup, reporting)
