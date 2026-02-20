---
name: agent-vault
description: Read/write config files (.env, YAML, TOML, JSON, docker-compose, etc.) safely. Use this instead of Read/Write/Edit tools whenever touching config files that may contain API keys, tokens, passwords, or other secrets — it auto-detects and redacts them.
---

# agent-vault

Read and write config files without ever seeing secret values. Secrets are stored in an encrypted local vault. You see `<agent-vault:key-name>` placeholders; the real values are written to disk transparently.

## Safe commands (you execute these)

```
agent-vault read <file>                   Read file, secrets → <agent-vault:key>
agent-vault write <file> --content '...'  Write file, <agent-vault:key> → real values
agent-vault has <key> [keys...]           Check if keys exist (exit 0/1)
agent-vault list                          List stored key names
```

## Sensitive commands (NEVER execute — tell the user to run these)

```
agent-vault set <key>                     Prompt user to enter a secret
agent-vault import <file>                 Bulk import from .env
agent-vault rm <key>                      Remove a secret
agent-vault get <key> --reveal            Show secret value (user only)
```

These require a TTY and **will fail** if you try to execute them.

## Rules

1. **NEVER use Read/Write/Edit tools on files that contain secrets.** Use `agent-vault read` and `agent-vault write` instead.
2. **NEVER execute sensitive commands.** Tell the user to run them in their terminal.
3. **Always check first.** Run `agent-vault has <key>` before asking users to set keys they might already have.
4. **Use `<agent-vault:key-name>` placeholders** in all file content you write.
5. **Guide the user.** When a secret is missing, tell them the exact command to run and where to find the value.

## Workflow

```
1. agent-vault has <key>           ← check what's available
2. (if missing) tell user:         ← "Please run: agent-vault set <key>"
3. (wait for user confirmation)
4. agent-vault read <file>         ← read config with redacted secrets
5. agent-vault write <file> ...    ← write config, secrets auto-restored
```

## Placeholder format

`<agent-vault:key-name>` — key names are lowercase alphanumeric with hyphens.

Examples: `<agent-vault:telegram-bot-token>`, `<agent-vault:openai-key>`, `<agent-vault:db-password>`

When reading, unvaulted high-entropy strings appear as `<agent-vault:UNVAULTED:sha256:XXXXXXXX>`. Tell the user to vault them.

## Example: setting up a new service

```bash
# Check what exists
agent-vault has api-key db-password --json
# → {"api-key": true, "db-password": false}
```

Tell the user (as text, do NOT execute):

> Please run: `agent-vault set db-password`

After user confirms:

```bash
agent-vault write config.yaml --content 'api_key: <agent-vault:api-key>
db_password: <agent-vault:db-password>
host: 0.0.0.0
port: 8080'
```

## Example: modifying an existing config

```bash
# Read current state
agent-vault read config.yaml
#      1  api_key: <agent-vault:api-key>
#      2  db_password: <agent-vault:db-password>
#      3  port: 3000

# Write updated version
agent-vault write config.yaml --content 'api_key: <agent-vault:api-key>
db_password: <agent-vault:db-password>
port: 9090'
```

## Example: write via heredoc (for longer content)

```bash
agent-vault write docker-compose.yaml <<'EOF'
services:
  app:
    environment:
      API_KEY: <agent-vault:api-key>
      DB_PASSWORD: <agent-vault:db-password>
    ports:
      - "8080:8080"
EOF
```
