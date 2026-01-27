---
name: ac-security-sandbox
description: Security sandbox for autonomous coding. Use when validating commands, configuring permissions, managing allowlists, or ensuring safe execution.
version: 1.0.0
layer: foundation
category: auto-claude-replication
triggers:
  - "validate command"
  - "security check"
  - "sandbox config"
  - "allowlist"
---

# AC Security Sandbox

Defense-in-depth security for autonomous code execution.

## Overview

Provides three layers of security:
1. **OS-Level Sandbox**: Isolated execution environment
2. **Filesystem Permissions**: Restricted path access
3. **Command Allowlist**: Pre-approved commands only

## Quick Start

### Validate Command
```python
from scripts.security_sandbox import SecuritySandbox

sandbox = SecuritySandbox(project_dir)

# Check if command is allowed
is_safe, reason = sandbox.validate_command("npm install")
if is_safe:
    # Execute command
    pass
else:
    print(f"Blocked: {reason}")
```

### Configure Allowlist
```python
sandbox.configure_allowlist([
    "ls", "cat", "head", "tail",
    "npm", "node", "python",
    "git", "grep"
])
```

## Security Layers

### Layer 1: OS-Level Sandbox

```python
# Enable sandbox mode
sandbox_config = {
    "enabled": True,
    "isolation": "strict",
    "network": "restricted"
}
```

### Layer 2: Filesystem Permissions

```python
permissions = {
    "allow": [
        "Read(./**)",      # Read project files
        "Write(./**)",     # Write project files
        "Edit(./**)",      # Edit project files
    ],
    "deny": [
        "Read(/etc/**)",   # No system files
        "Write(/usr/**)",  # No system writes
        "Bash(rm -rf /)",  # No destructive commands
    ]
}
```

### Layer 3: Command Allowlist

```python
ALLOWED_COMMANDS = {
    # File inspection
    "ls", "cat", "head", "tail", "wc", "grep", "find",

    # File operations
    "cp", "mv", "mkdir", "chmod", "touch",

    # Node.js
    "npm", "node", "npx", "yarn", "pnpm",

    # Python
    "python", "python3", "pip", "pip3",

    # Version control
    "git",

    # Process management
    "ps", "lsof", "sleep", "pkill",

    # Build tools
    "make", "cmake", "cargo", "go",

    # Testing
    "jest", "pytest", "vitest", "playwright"
}
```

## Command Validation

### Pre-Tool-Use Hook

```python
async def bash_security_hook(input_data, tool_use_id, context):
    command = input_data.get("tool_input", {}).get("command", "")

    # Extract all commands (handles pipes, &&, etc.)
    commands = extract_commands(command)

    for cmd in commands:
        if cmd not in ALLOWED_COMMANDS:
            return {
                "decision": "block",
                "reason": f"Command '{cmd}' not in allowlist"
            }

    return {}  # Allow execution
```

### Command Extraction

```python
def extract_commands(command: str) -> list[str]:
    """
    Extract base commands from complex command strings.

    Examples:
        "npm install && npm test" → ["npm", "npm"]
        "cat file.txt | grep error" → ["cat", "grep"]
        "git add . && git commit -m 'msg'" → ["git", "git"]
    """
    # Parse command string
    # Handle: pipes (|), chains (&&, ||), semicolons (;)
    # Return list of base command names
```

## Blocked Command Patterns

### Always Blocked

```python
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",       # Recursive delete root
    r"dd\s+if=",           # Direct disk writes
    r"mkfs",               # Format filesystems
    r":(){ :|:& };:",      # Fork bombs
    r"chmod\s+777",        # Overly permissive
    r"curl.*\|\s*bash",    # Pipe to shell
    r"wget.*\|\s*sh",      # Pipe to shell
]
```

### Context-Dependent

```python
# Allowed in project directory only
RESTRICTED_COMMANDS = {
    "rm": lambda path: path.startswith("./"),
    "mv": lambda src, dst: src.startswith("./") and dst.startswith("./"),
    "cp": lambda src, dst: dst.startswith("./"),
}
```

## Configuration

### .claude/security-config.json

```json
{
  "sandbox": {
    "enabled": true,
    "isolation": "strict"
  },
  "permissions": {
    "filesystem": {
      "read": ["./**", "~/.config/claude/**"],
      "write": ["./**"],
      "deny": ["/etc/**", "/usr/**", "~/.ssh/**"]
    },
    "network": {
      "allow": ["localhost", "api.anthropic.com"],
      "deny": ["*"]
    }
  },
  "allowlist": {
    "commands": ["npm", "node", "git", "python"],
    "custom": []
  }
}
```

## Operations

### 1. Initialize Sandbox

```python
sandbox = SecuritySandbox(project_dir)
await sandbox.initialize()
# Loads config, sets up hooks
```

### 2. Validate Command

```python
is_safe, reason = sandbox.validate_command(command)
# Returns (True, None) or (False, "reason")
```

### 3. Validate Path

```python
is_allowed = sandbox.validate_path(path, operation="write")
# Checks against filesystem permissions
```

### 4. Register Hook

```python
hook = sandbox.create_pre_tool_hook()
# Returns hook function for Claude SDK
```

### 5. Add Custom Command

```python
sandbox.add_allowed_command("my-custom-tool")
# Adds to allowlist (persists to config)
```

### 6. Audit Log

```python
# Get recent security events
events = sandbox.get_audit_log(limit=100)
for event in events:
    print(f"{event.timestamp}: {event.action} - {event.command}")
```

## Audit Logging

All security decisions are logged:

```json
// .claude/security-audit.jsonl
{"timestamp": "2025-01-15T10:00:00Z", "action": "ALLOW", "command": "npm install", "reason": null}
{"timestamp": "2025-01-15T10:01:00Z", "action": "BLOCK", "command": "rm -rf /", "reason": "Dangerous pattern"}
{"timestamp": "2025-01-15T10:02:00Z", "action": "ALLOW", "command": "git commit", "reason": null}
```

## Best Practices

### DO
- Start with minimal allowlist
- Add commands as needed
- Review audit logs regularly
- Use project-relative paths

### DON'T
- Allow `sudo` commands
- Allow system path writes
- Disable sandbox in production
- Ignore blocked command logs

## Integration Points

- **ac-session-manager**: Provides security hooks
- **ac-build-runner**: Validates build commands
- **ac-coder-agent**: Restricts agent commands
- **ac-config-manager**: Loads security config

## References

- `references/ALLOWLIST.md` - Complete command list
- `references/PATTERNS.md` - Blocked patterns
- `references/AUDIT.md` - Audit log format

## Scripts

- `scripts/security_sandbox.py` - Core SecuritySandbox
- `scripts/command_validator.py` - Command validation
- `scripts/path_validator.py` - Path validation
- `scripts/audit_logger.py` - Security audit logging
