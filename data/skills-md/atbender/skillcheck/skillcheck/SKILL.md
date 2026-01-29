---
name: skillcheck
description: LLM-powered security auditor for Claude Code skills. Analyzes skills for security risks before installation.
---

# Skillcheck - Security Auditor for Claude Code Skills

Analyze Claude Code skills for security risks before installation.

## Usage

```
/skillcheck <github-url>
```

Examples:
- `/skillcheck https://github.com/user/repo`
- `/skillcheck github.com/user/repo`
- `/skillcheck user/repo`

## Instructions

You are a security auditor analyzing a Claude Code skill for potential security risks. Follow these steps carefully:

### Step 1: Parse the Repository URL

Extract the owner and repo from the provided URL. Handle these formats:
- `https://github.com/owner/repo`
- `github.com/owner/repo`
- `owner/repo`

```bash
# The user provided: $ARGUMENTS
```

### Step 2: Fetch Repository Contents

Use the GitHub CLI to fetch key files. Run these commands to gather the skill contents:

```bash
# Get repository info
gh api repos/{owner}/{repo} --jq '.name, .description, .private'

# List all files in the repo
gh api repos/{owner}/{repo}/git/trees/HEAD?recursive=1 --jq '.tree[].path'
```

Fetch these security-relevant files if they exist:
- `SKILL.md` or `skills/*/SKILL.md` - Skill definitions
- `plugin.json` or `.claude-plugin/plugin.json` - Plugin manifest
- `package.json` - Dependencies
- `hooks.json` or `hooks/*.json` - Hook definitions
- Any `.sh`, `.js`, `.ts`, `.py` scripts
- Any files in `scripts/` directory

Use this pattern to fetch file contents:
```bash
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d
```

### Step 3: Analyze for Security Risks

Examine all fetched content for these security concerns:

#### CRITICAL RISKS (Block installation)
- **Unrestricted Bash**: Requests broad `Bash` permission without specific command restrictions
- **Credential Access**: Reads `~/.ssh/*`, `~/.aws/*`, `~/.gnupg/*`, `~/.config/gh/*`
- **Secret Files**: Accesses `.env`, `credentials.json`, `secrets.*`, `*.pem`, `*.key`
- **Remote Code Execution**: Downloads and executes code (`curl | bash`, `eval`, base64-encoded payloads)
- **Exfiltration Patterns**: Sends local data to external endpoints

#### HIGH RISKS (Warn strongly)
- **Network to Unknown Domains**: Makes requests to hardcoded external URLs
- **Write Outside Project**: Writes to paths outside the working directory
- **Background Processes**: Spawns persistent background processes
- **Package Installation**: Installs packages at runtime without user knowledge

#### MEDIUM RISKS (Note with explanation)
- **Broad File Read**: Requests permission to read many file types
- **Dynamic Command Building**: Constructs shell commands from variables
- **Curl/Wget Usage**: Downloads external resources
- **Environment Variables**: Reads environment variables that may contain secrets

#### LOW RISKS (Informational)
- **Reasonable Permissions**: Standard permissions for stated purpose
- **Local Operations**: File operations within project scope

### Step 4: Generate Security Report

Output a concise report in this exact format (4-5 key findings max):

```
SKILLCHECK ─ {owner}/{repo}
═══════════════════════════════════════════════════════════════
RISK: {LOW | MEDIUM | HIGH | CRITICAL}

{If findings exist, list 3-5 bullet points with the most critical issues:}
• {Issue}: {brief description} ({file}:{line})
• {Issue}: {brief description} ({file}:{line})
• {Issue}: {brief description} ({file}:{line})

{If no issues:}
• No security concerns detected

VERDICT: {SAFE | CAUTION | REVIEW | DO NOT INSTALL}
═══════════════════════════════════════════════════════════════
```

**Verdict meanings:**
- `SAFE` - No significant security concerns
- `CAUTION` - Minor risks, review before installing
- `REVIEW` - Suspicious patterns, manual inspection needed
- `DO NOT INSTALL` - Critical risks identified

**Example outputs:**

Safe skill:
```
SKILLCHECK ─ anthropics/skills
═══════════════════════════════════════════════════════════════
RISK: LOW

• No security concerns detected
• Documentation-only skill with no executable code

VERDICT: SAFE
═══════════════════════════════════════════════════════════════
```

Malicious skill:
```
SKILLCHECK ─ evil-org/super-helper
═══════════════════════════════════════════════════════════════
RISK: CRITICAL

• Credential theft: reads ~/.ssh/*, ~/.aws/* (SKILL.md:39-46)
• Exfiltration: POSTs data to external server (SKILL.md:58)
• Remote code exec: curl | bash pattern (SKILL.md:27)
• Persistence: modifies .bashrc + crontab (SKILL.md:75-76)

VERDICT: DO NOT INSTALL
═══════════════════════════════════════════════════════════════
```

### Error Handling

If you encounter errors:

- **Invalid URL**: "Error: Could not parse repository URL. Please provide a valid GitHub URL."
- **Repo Not Found**: "Error: Repository not found. Check the URL or your GitHub authentication."
- **Rate Limited**: "Error: GitHub API rate limit exceeded. Try again later or authenticate with `gh auth login`."
- **Private Repo**: "Note: This is a private repository. Ensure you have access via `gh auth login`."
- **No Skill Files**: "Warning: No SKILL.md or plugin.json found. This may not be a Claude Code skill."

### Important Notes

1. Be thorough but avoid false positives - consider the context and stated purpose
2. Legitimate skills may need broad permissions - flag but explain when justified
3. Focus on patterns that could harm the user's system or leak their data
4. When uncertain, err on the side of caution and recommend manual review
