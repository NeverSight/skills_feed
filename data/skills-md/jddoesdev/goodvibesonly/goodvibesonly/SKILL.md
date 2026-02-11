---
name: goodvibesonly
description: Security scanner for vibe-coded projects. AUTO-INVOKE this skill before any git commit, git push, or when user says "commit", "push", "ship it", "deploy", "is this safe?", "check for security issues", or "goodvibesonly". Also invoke after generating code that handles user input, authentication, database queries, or file operations.
---

# GoodVibesOnly - Security Scanner

Automatically scan for security vulnerabilities before code leaves the developer's machine.

## When to Auto-Invoke

Run this skill BEFORE executing any:
- `git commit`
- `git push`
- Deploy commands

Run this skill WHEN user says:
- "commit this"
- "push to main"
- "ship it"
- "is this safe?"
- "check security"
- "goodvibesonly"
- "ready to deploy"

## Quick Scan Checklist

Scan changed files for:

### 🔴 CRITICAL (Stop and fix)

```
# Hardcoded secrets
sk-[a-zA-Z0-9]{20,}              # OpenAI
sk-ant-[a-zA-Z0-9-]{20,}         # Anthropic
AKIA[0-9A-Z]{16}                  # AWS
ghp_[a-zA-Z0-9]{36}              # GitHub
sk_(live|test)_[a-zA-Z0-9]{24,}  # Stripe
api_key\s*=\s*["'][^"']+["']     # Generic API key
password\s*=\s*["'][^"']+["']    # Hardcoded password
-----BEGIN.*PRIVATE KEY-----      # Private key

# Injection
query.*\+.*user                   # SQL injection (concat)
execute.*\$\{                     # SQL injection (template)
exec\(.*\+                        # Command injection
subprocess.*shell=True            # Shell injection
eval\(.*[a-zA-Z_]                 # Code injection

# Dangerous config
origin.*["']\*["']                # CORS allow all
verify\s*=\s*False                # SSL disabled
rejectUnauthorized.*false         # SSL disabled (Node)
```

### 🟡 HIGH (Warn)

```
innerHTML\s*=                     # XSS
dangerouslySetInnerHTML           # XSS (React)
v-html=                           # XSS (Vue)
pickle\.loads                     # Insecure deserialization
yaml\.load\(                      # Unsafe YAML
md5\(.*password                   # Weak crypto
sha1\(.*password                  # Weak crypto
```

### 🟢 MEDIUM (Note)

```
debug.*=.*true                    # Debug mode
console\.log.*password            # Logged secrets
TODO.*security                    # Security TODOs
http://(?!localhost)              # Non-HTTPS
```

## Response Protocol

**If CRITICAL issues found:**
1. List all issues with file:line
2. Show the problematic code
3. Explain the fix
4. Ask: "Want me to fix these before committing?"
5. Do NOT proceed with commit until fixed or user explicitly overrides

**If HIGH issues found:**
1. List issues
2. Ask: "These should be fixed. Continue anyway?"

**If only MEDIUM or clean:**
1. Brief summary
2. Proceed with the requested action

## Allowlist Flow

When a user wants to suppress a specific finding, follow this flow:

1. **User says** something like "allow the dangerouslySetInnerHTML one" or "ignore the XSS finding"
2. **Ask**: "One-time (this commit only) or permanent?"
3. **Ask for reason**: "What's the reason for allowing this?" (e.g., "Sanitized with DOMPurify")

### One-Time Allow

1. Read existing `.goodvibesonly.json` (or create `{ "allow": [] }` if missing)
2. Add the temporary entry to the `allow` array
3. Write the file (**do not** stage it with `git add`)
4. Re-run the commit command
5. After commit completes, remove the temporary entry from `.goodvibesonly.json`
6. If the file is now empty (`{ "allow": [] }`), delete it

### Permanent Allow

1. Read existing `.goodvibesonly.json` (or create `{ "allow": [] }` if missing)
2. Add the entry to the `allow` array with the user's reason
3. Write the file (leave it for the user to commit when ready)
4. Re-run the commit command
5. Tell the user: "Added permanent allowlist rule. You can commit `.goodvibesonly.json` when ready."

### Config Format: `.goodvibesonly.json`

```json
{
  "allow": [
    { "pattern": "XSS via dangerouslySetInnerHTML", "reason": "Sanitized with DOMPurify" },
    { "path": "test/**", "reason": "Test files contain intentional patterns" },
    { "pattern": "SQL Injection", "path": "src/db/raw.js", "reason": "Parameterized at call site" }
  ]
}
```

- `pattern` only: suppress that pattern in all files
- `path` only: suppress all patterns in matching files (supports `*` and `**` globs)
- `pattern` + `path`: suppress specific pattern in specific files
- Pattern names must match exactly — run `node bin/scan.js --list-patterns` to see all names

### Show the User What Changed

After adding an entry, show the user what was added:
```
Added to .goodvibesonly.json:
  { "pattern": "XSS via dangerouslySetInnerHTML", "reason": "Sanitized with DOMPurify" }
```

## Example Output

```
🛡️ GoodVibesOnly Security Scan

Scanned 8 files with changes.

🔴 CRITICAL - Must fix:

1. Hardcoded API Key
   src/config.js:15
   const API_KEY = "sk-abc123..."
   → Move to environment variable

2. SQL Injection
   src/db/users.js:42
   db.query("SELECT * FROM users WHERE id = " + id)
   → Use parameterized query: db.query("SELECT * FROM users WHERE id = ?", [id])

🟡 HIGH - Should fix:

3. XSS Risk
   src/components/Comment.jsx:28
   <div dangerouslySetInnerHTML={{__html: comment.body}} />
   → Sanitize with DOMPurify before rendering

Found 2 critical, 1 high, 0 medium issues.
Commit blocked. Want me to fix the critical issues?
```
