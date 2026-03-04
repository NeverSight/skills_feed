---
name: system-health-check
description: Comprehensive system health scanner that checks security risks, performance metrics, and optimization opportunities. Leverages agent parallelism for fast multi-category scanning. Works on Windows, macOS, and Linux.
license: MIT
metadata:
  author: chenxizhang
  version: "3.0"
---

# System Health Check

A comprehensive scanner that analyzes your system for security risks, performance issues, and optimization opportunities — **using parallel execution for maximum speed**.

## When to Use

- Setting up a new machine
- Periodic security audits
- Troubleshooting performance issues
- Before deploying to production

## Options

Users may request a subset:
- **Full check** (default): All three categories
- **Security only**: Security checks only
- **Performance only**: Performance checks only
- **Optimization only**: Optimization suggestions only

## Strict Execution Flow

**Do NOT use any scripts. Do NOT skip or merge phases. Execute each phase in order.**

---

### Phase 1: Environment Detection (MANDATORY — must display results before proceeding)

Detect and **explicitly display** the following before doing anything else:

1. **Operating System**: Run a command to detect the OS and version.
   - Windows: `[System.Environment]::OSVersion` and `(Get-CimInstance Win32_OperatingSystem).Caption`
   - macOS: `sw_vers`
   - Linux: `cat /etc/os-release | head -5`
2. **Shell environment**: Identify the current shell.
   - PowerShell: `$PSVersionTable.PSVersion`
   - bash/zsh: `echo $SHELL` and version
3. **Agent identity**: Identify which agent is running this skill (Claude Code, GitHub Copilot CLI, Cursor, etc.) based on the agent's own context/identity.
4. **Privilege level**: Check if running as admin/root.
   - Windows PowerShell: `([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)`
   - macOS/Linux: `whoami` (check if root) or `id -u` (0 = root)
5. **Hostname**: `hostname`

**Display the detection results clearly**, for example:
```
Environment Detection:
  OS:        Windows 11 Pro (10.0.22631)
  Shell:     PowerShell 7.4
  Agent:     GitHub Copilot CLI
  Privilege: Standard user (not admin)
  Hostname:  DESKTOP-ABC123
```

**CRITICAL: All subsequent phases MUST use ONLY commands for the detected OS and shell. Never include commands from other platforms — not in execution, not in recommendations, not anywhere.**

---

### Phase 2: Plan (generate environment-specific execution plan)

Based on Phase 1 results:

1. **Select commands**: From the reference tables below, pick ONLY the column matching the detected OS. Ignore all other columns entirely.
2. **Plan parallelism** based on the detected agent:

| Agent | Parallel Strategy |
|-------|------------------|
| **GitHub Copilot CLI** | Use three sub-agents (task tool with agent_type "task" or "general-purpose") — one for Security, one for Performance, one for Optimization. |
| **Claude Code** | Use Agent Teams — dispatch three sub-agents in parallel, one per category. |
| **Other agents** | Use whatever parallel execution mechanism is available. |

3. **Display the plan** before executing, e.g.:
```
Plan:
  Checks: Security + Performance + Optimization
  Strategy: 3 parallel sub-agents (GitHub Copilot CLI)
  Platform: All commands use PowerShell (Windows)
```

---

### Phase 3: Execute (parallel)

**CRITICAL: The three check categories are COMPLETELY INDEPENDENT. Run them ALL in PARALLEL!**

Launch three independent workstreams simultaneously. Each workstream uses ONLY the commands selected in Phase 2 for the detected platform.

Within each workstream, individual checks can also be parallelized for even more speed.

---

### Phase 4: Report & Recommendations

#### Compile Report

After all parallel workstreams complete, compile a unified report:

```
================================================================================
                         SYSTEM HEALTH CHECK REPORT
================================================================================
Generated: <timestamp>
System:    <OS and version>
Shell:     <shell and version>
Agent:     <agent identity>
Hostname:  <hostname>

[Security Analysis results...]
[Performance Analysis results...]
[Optimization Suggestions...]
```

Use severity indicators:
- `[✓]` — Check passed / healthy
- `[!]` — Warning / needs attention
- `[✗]` — Critical issue / security risk

Focus on **actionable findings** — interpret results, don't dump raw output.

#### Recommendations

**CRITICAL: ALL recommendations MUST be specific to the detected environment.**
- If on Windows: only recommend PowerShell commands, Windows tools, Windows settings
- If on macOS: only recommend macOS commands and tools
- If on Linux: only recommend Linux commands and tools
- **NEVER suggest `chmod` on Windows. NEVER suggest `Get-Acl` on Linux. NEVER suggest `icacls` on macOS. NEVER mix platforms.**

---

## Command Reference Tables

**The agent MUST only use commands from the column matching the detected OS. Ignore other columns.**

### 🔒 Security Analysis

| Check | Windows (PowerShell) | macOS (bash/zsh) | Linux (bash) |
|-------|---------------------|-------------------|--------------|
| Firewall | `Get-NetFirewallProfile` | `defaults read /Library/Preferences/com.apple.alf globalstate` | `ufw status` or `iptables -L` |
| Open ports | `Get-NetTCPConnection -State Listen` | `lsof -i -P -n \| grep LISTEN` | `ss -tlnp` |
| SSH config | `Get-Content $env:ProgramData\ssh\sshd_config -ErrorAction SilentlyContinue` | `cat /etc/ssh/sshd_config 2>/dev/null` | `cat /etc/ssh/sshd_config 2>/dev/null` |
| Updates | `Get-HotFix \| Sort InstalledOn -Desc \| Select -First 5` | `softwareupdate -l` | `apt list --upgradable 2>/dev/null` or `yum check-update` |
| AV status | `Get-MpComputerStatus` | _(skip — not standard)_ | _(skip or check ClamAV)_ |
| Users | `Get-LocalUser \| Where-Object Enabled` | `dscl . -list /Users \| grep -v '^_'` | `awk -F: '$3>=1000{print $1}' /etc/passwd` |
| File permissions | `Get-Acl $env:USERPROFILE\.ssh\* -ErrorAction SilentlyContinue` | `ls -la ~/.ssh/` | `ls -la ~/.ssh/` |

#### AI Agent Security Scanning

Scan these config directories for risky patterns (use the agent's file search capabilities or platform-appropriate grep):

**User-level:** `~/.claude/`, `~/.copilot/`, `~/.continue/`, `~/.cursor/`, `~/.aider/`, `~/.agents/`, `~/.codeium/`, `~/.codeflow/`

**Project-level:** `.claude/`, `.continue/`, `.cursor/`, `.copilot/`, `.github/copilot/`

| Category | Risk Level | Patterns |
|----------|-----------|----------|
| Network outbound | HIGH | `curl.*POST`, `wget --post`, `Invoke-WebRequest.*POST` |
| Credential access | HIGH | `.ssh/`, `.aws/`, `API_KEY`, `SECRET`, `TOKEN`, `PASSWORD` |
| Obfuscation | HIGH | `base64 -d`, `base64 --decode`, `String.fromCharCode` |
| Dynamic execution | MEDIUM | `eval(`, `exec(`, `source <(`, `Function(` |
| Package installation | MEDIUM | `npx -y`, `pip install` from URLs |
| Permission bypass | MEDIUM | `bypassPermissions`, `skipVerify`, `dangerouslyAllow` |

### 📊 Performance Analysis

| Check | Windows (PowerShell) | macOS (bash/zsh) | Linux (bash) |
|-------|---------------------|-------------------|--------------|
| CPU | `Get-CimInstance Win32_Processor \| Select LoadPercentage` and `Get-Process \| Sort CPU -Desc \| Select -First 5` | `top -l 1 -n 0 \| grep "CPU usage"` and `ps aux --sort=-%cpu \| head -6` | `top -bn1 \| head -5` and `ps aux --sort=-%cpu \| head -6` |
| Memory | `Get-CimInstance Win32_OperatingSystem \| Select TotalVisibleMemorySize,FreePhysicalMemory` | `vm_stat` and `sysctl hw.memsize` | `free -h` |
| Disk | `Get-PSDrive -PSProvider FileSystem \| Select Name,Used,Free` | `df -h` | `df -h` |
| Network | `(Get-NetTCPConnection).Count` | `netstat -an \| grep ESTABLISHED \| wc -l` | `ss -s` |
| Processes | `(Get-Process).Count` | `ps aux \| wc -l` | `ps aux \| wc -l` |
| Startup | `Get-CimInstance Win32_StartupCommand \| Select Name,Command` | `launchctl list \| wc -l` | `systemctl list-unit-files --state=enabled --no-pager` |

### 🔧 Optimization Suggestions

| Check | Windows (PowerShell) | macOS (bash/zsh) | Linux (bash) |
|-------|---------------------|-------------------|--------------|
| Temp files | `Get-ChildItem $env:TEMP -Recurse -ErrorAction SilentlyContinue \| Measure-Object -Property Length -Sum` | `du -sh /tmp/ ~/Library/Caches/ 2>/dev/null` | `du -sh /tmp/ /var/tmp/ 2>/dev/null` |
| Services | `Get-Service \| Where-Object {$_.Status -eq 'Running'} \| Measure-Object` | `launchctl list \| wc -l` | `systemctl list-units --type=service --state=running --no-pager \| wc -l` |
| Top CPU | `Get-Process \| Sort CPU -Desc \| Select -First 10 Name,CPU,WorkingSet64` | `ps aux --sort=-%cpu \| head -11` | `ps aux --sort=-%cpu \| head -11` |
| Top Memory | `Get-Process \| Sort WorkingSet64 -Desc \| Select -First 10 Name,@{N='MemMB';E={[math]::Round($_.WorkingSet64/1MB)}}` | `ps aux --sort=-%mem \| head -11` | `ps aux --sort=-%mem \| head -11` |

---

## Notes

- Some checks may require elevated privileges — if a command fails due to permissions, note it in the report and continue
- Adapt commands based on what's actually installed (e.g., if `ufw` is not available, try `iptables`; if neither, skip and note)
- The command reference tables are hints for the detected platform — the agent may use its knowledge to pick even better available commands, as long as they match the detected OS
