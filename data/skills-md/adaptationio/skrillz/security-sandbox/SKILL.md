---
name: security-sandbox
description: Secure command execution with allowlists and validation hooks. Use when validating bash commands, configuring security policies, implementing pre-tool-use hooks, or sandboxing autonomous agent operations.
version: 1.0.0
category: autonomous-coding
layer: foundation
---

# Security Sandbox

Provides defense-in-depth security for autonomous coding operations through command validation, allowlists, and execution hooks.

## Quick Start

### Validate a Command
```python
from scripts.command_validator import validate_command

result = validate_command("npm install express")
if result.allowed:
    # Safe to execute
    pass
else:
    print(f"Blocked: {result.reason}")
```

### Use Security Hook
```python
from scripts.security_manager import create_bash_security_hook

hook = create_bash_security_hook()

# Hook returns decision for Claude SDK
decision = await hook({
    "tool_input": {"command": "rm -rf /"}
})
# decision = {"decision": "block", "reason": "Command 'rm' requires approval"}
```

### Configure Allowlist
```python
from scripts.allowlist import Allowlist

allowlist = Allowlist()
allowlist.add("docker")
allowlist.add("kubectl")
allowlist.remove("rm")  # Disallow rm
```

## Security Model

```
┌─────────────────────────────────────────────────────────────┐
│                   DEFENSE IN DEPTH                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  LAYER 1: SANDBOX                                           │
│  ├─ OS-level isolation                                      │
│  ├─ Filesystem restrictions                                 │
│  └─ Network limitations                                     │
│                                                              │
│  LAYER 2: PERMISSIONS                                       │
│  ├─ Tool allowlist (Read, Write, Bash...)                  │
│  ├─ Path restrictions (./**)                               │
│  └─ Operation limits                                        │
│                                                              │
│  LAYER 3: COMMAND VALIDATION                                │
│  ├─ Command extraction & parsing                            │
│  ├─ Allowlist checking                                      │
│  └─ Dangerous pattern detection                             │
│                                                              │
│  LAYER 4: HOOKS                                             │
│  ├─ PreToolUse validation                                   │
│  ├─ Real-time blocking                                      │
│  └─ Audit logging                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Default Allowlist

```python
ALLOWED_COMMANDS = {
    # File inspection
    "ls", "cat", "head", "tail", "wc", "grep", "find",
    # File operations
    "cp", "mkdir", "chmod", "touch",
    # Node.js
    "npm", "node", "npx", "yarn", "pnpm",
    # Python
    "python", "python3", "pip", "pip3", "poetry",
    # Version control
    "git",
    # Process management
    "ps", "lsof", "sleep", "pkill", "kill",
    # System info
    "pwd", "whoami", "uname", "which", "env",
    # Network (limited)
    "curl", "wget",
}
```

## Dangerous Patterns

These patterns are always blocked:

| Pattern | Risk | Example |
|---------|------|---------|
| `rm -rf /` | System destruction | Wipes filesystem |
| `> /dev/sda` | Disk corruption | Overwrites disk |
| `chmod 777` | Security hole | World-writable |
| `curl \| bash` | Code injection | Remote execution |
| `:(){ :\|:& };:` | Fork bomb | DoS attack |
| `dd if=/dev/zero` | Disk fill | Resource exhaustion |

## Hook Integration

```python
# For Claude SDK integration
from scripts.security_manager import SecurityManager

manager = SecurityManager()

# Configure SDK with hooks
sdk_options = {
    "hooks": {
        "PreToolUse": [manager.pre_tool_hook]
    }
}
```

## Integration Points

- **autonomous-session-manager**: Provides security during sessions
- **coding-agent**: Uses hooks for safe command execution
- **autonomous-loop**: Ensures safety in continuous operation

## References

- `references/ALLOWED-COMMANDS.md` - Full allowlist documentation
- `references/SECURITY-MODEL.md` - Security architecture
- `references/CUSTOM-RULES.md` - Custom rule configuration

## Scripts

- `scripts/security_manager.py` - Core security manager
- `scripts/command_validator.py` - Command validation
- `scripts/allowlist.py` - Allowlist management
- `scripts/sandbox_config.py` - Sandbox configuration
