---
name: op-cli
description: Secure 1Password CLI patterns for reading secrets, discovering vaults/items, and piping credentials to other tools. Use when reading from 1Password, rotating secrets, or piping credentials to wrangler/kubectl/etc. Triggers on op CLI, 1Password, secret rotation, or credential piping tasks.
---

# 1Password CLI (`op`) — Secure Handling

## Core Rule: Never Print Secrets

**NEVER** use `op` commands that would print secret values into the conversation. Always pipe directly to the consuming tool or use `wc -c` / redaction to verify without exposing.

```bash
# WRONG — would print secret to stdout (do not run)
# op item get ITEM_ID --vault VAULT --fields label=PASSWORD --reveal

# RIGHT — pipe directly to consumer
op item get ITEM_ID --vault VAULT --fields label=PASSWORD --reveal | \
  wrangler secret put SECRET_NAME --env ENV

# RIGHT — verify a value exists without exposing it
op item get ITEM_ID --vault VAULT --fields label=PASSWORD --reveal 2>/dev/null | wc -c
```

## Item Titles with Slashes

Many 1Password items use path-style titles (e.g. `pool-party/testnet-pool-party-public/credentials`). The `op://` URI format **breaks** with these because it uses `/` as a delimiter.

```bash
# BROKEN — too many '/' segments
op read "op://pool-party-testnet/pool-party/testnet-pool-party-public/credentials/PASSWORD"
# ERROR: too many '/': secret references should match op://<vault>/<item>[/<section>]/<field>

# WORKS — use item ID instead (avoid printing values)
op item get ITEM_ID --vault VAULT --fields label=FIELD --reveal 2>/dev/null | wc -c
```

### Discovery Workflow

When you don't know the item ID:

```bash
# 1. List items in a vault to find the title and ID
op item list --vault VAULT_NAME

# 2. Use the ID (first column) for all subsequent reads
op item get ITEM_ID --vault VAULT_NAME --fields label=FIELD_NAME --reveal 2>/dev/null | wc -c
```

## Reading Multiple Fields from One Item

```bash
# Verify which fields exist (safe — shows labels not values)
op item get ITEM_ID --vault VAULT_NAME --format json 2>/dev/null | \
  python3 -c "import json,sys; [print(f['label']) for s in json.load(sys.stdin).get('fields',[]) for f in [s] if f.get('label')]"

# Pipe each field to its destination
op item get ITEM_ID --vault VAULT --fields label=USERNAME --reveal | consumer_cmd ...
op item get ITEM_ID --vault VAULT --fields label=PASSWORD --reveal | consumer_cmd ...
```

## Common Piping Patterns

### Cloudflare Workers (wrangler)
```bash
op item get ITEM_ID --vault VAULT --fields label=PASSWORD --reveal | \
  npx wrangler secret put POOL_PARTY_PUBLIC_PASSWORD --env testnet
```

### Environment Variable (subshell)
```bash
SECRET="$(op item get ITEM_ID --vault VAULT --fields label=TOKEN --reveal 2>/dev/null)"
# Use $SECRET in subsequent commands within the same shell — it won't appear in output
```

### kubectl
```bash
op item get ITEM_ID --vault VAULT --fields label=PASSWORD --reveal | \
  kubectl create secret generic my-secret --from-file=password=/dev/stdin
```

## Verification Without Exposure

```bash
# Check a value is non-empty (char count)
op item get ITEM_ID --vault VAULT --fields label=PASSWORD --reveal 2>/dev/null | wc -c

# Compare two sources match (exit code only)
if cmp -s <(op item get ID1 --vault V --fields label=F --reveal 2>/dev/null) \
        <(op item get ID2 --vault V --fields label=F --reveal 2>/dev/null); then
  echo "match"
else
  echo "differ"
fi
```

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `too many '/'` | Item title has slashes, `op://` can't parse it | Use item ID with `op item get` |
| `could not find item` | Wrong vault or title mismatch | Run `op item list --vault VAULT` to discover |
| Empty output | Missing `--reveal` flag | Add `--reveal` and pipe to consumer (or `| wc -c`) |
| `not signed in` | Session expired | Run `eval "$(op signin)"` (avoid printing the session token) |
