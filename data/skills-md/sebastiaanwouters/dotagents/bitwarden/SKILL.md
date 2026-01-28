---
name: bitwarden
description: Retrieves API keys, passwords, secrets from Bitwarden vault using bw CLI. Triggers on missing env variables, missing API keys, missing secrets, "secret not found", "env not set", or "use bw".
---

# Bitwarden CLI

Retrieve secrets when environment variables are missing.

## Quick Reference

```bash
# Get password by name
bw get password "item-name"

# Get specific field
bw get item "item-name" | jq -r '.fields[] | select(.name=="API_KEY") | .value'

# Search items
bw list items --search "github"
```

## Session Management

Check status first:
```bash
bw status
```

If locked, unlock and export session:
```bash
export BW_SESSION=$(bw unlock --raw)
```

## Finding API Keys

**API keys are often stored in notes** - either in a login item's notes field or as a standalone secure note.

1. **Search first** to find the right item:
   ```bash
   bw list items --search "openai"
   ```

2. **Check notes** - API keys are commonly here:
   ```bash
   bw get notes "item-name"
   ```

3. Check custom fields if not in notes:
   ```bash
   bw get item "item-name" | jq -r '.fields[] | select(.name=="API_KEY") | .value'
   ```

## Common Patterns

| Need | Command |
|------|---------|
| **Search items** | `bw list items --search "query"` |
| **Notes (API keys!)** | `bw get notes "name"` |
| Password | `bw get password "name"` |
| Username | `bw get username "name"` |
| TOTP | `bw get totp "name"` |
| Custom field | `bw get item "name" \| jq -r '.fields[] \| select(.name=="FIELD") \| .value'` |

## CLI Help

```
bw [options] [command]

Commands:
  login [email] [password]    Log into account
  unlock [password]           Unlock vault, returns session key
  lock                        Lock vault
  status                      Show vault status
  list <object>               List objects (items, folders, collections)
  get <object> <id>           Get object (item, username, password, totp, notes)
  sync                        Pull latest vault data
```
