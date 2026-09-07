---
name: hal-vault
description: Securely store, search, and use secrets (API keys, tokens, passwords, SSH keys) with hal-vault, an SSH-key encrypted local secret store. Use when the user shares a credential that should be saved, asks what secrets are stored or where a key is, or when a command/workflow needs a secret injected. Core discipline - never print raw secret values into chat, logs, or files; reference secrets only by their masked form, and use --reveal exclusively inside command substitution.
license: MIT
version: "1.1.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/hal-vault
metadata:
  author: ofoxai
  version: "1.1.0"
  openclaw:
    requires:
      bins: [hal-vault]
    envVars:
      - name: HAL_VAULT_DIR
        required: false
        description: Vault directory. Resolution order is the -d flag, then this variable, then ~/.hal-vault.
    emoji: "🔐"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/hal-vault
---

# hal-vault: agent-safe secret management

[hal-vault](https://github.com/ofoxai/hal-vault) is a CLI secret store: one
age-encrypted file, keyed to an SSH key, with masked-by-default output
designed so an agent can manage secrets without ever seeing or leaking them.

## When to apply

Use this skill when:

- The user shares an API key, token, password, or other credential that
  should be kept for later use
- The user asks "what secrets do we have", "do we still have the X key",
  or wants to find/rotate/remove a stored credential
- A command, script, or deployment you are running needs a secret (an API
  key in an env var, a token in a header)

## Check availability

```
hal-vault version
```

If not installed: `brew install ofoxai/tap/hal-vault` (macOS/Linux,
recommended), or download a release binary from
https://github.com/ofoxai/hal-vault/releases, or `go install
github.com/ofoxai/hal-vault/cmd/hal-vault@latest`.

## Recommended setup: per-project vault

As an agent, keep each project's secrets in a vault inside that project,
with its own dedicated SSH key — isolation per project, and the encrypted
database travels with the workspace:

```
# 1. A project-specific key. The key lives in ~/.ssh, NEVER inside the
#    project directory — a vault and its key must not sit in the same tree
#    (and must never be committable together).
ssh-keygen -t ed25519 -N "" -C "hal-vault-myproject" \
  -f ~/.ssh/hal-vault_myproject

# 2. The vault database lives in the project, out of version control.
hal-vault init -d .hal-vault \
  -r ~/.ssh/hal-vault_myproject.pub \
  -i ~/.ssh/hal-vault_myproject

# 3. Make sure it is never committed.
grep -qxF '.hal-vault/' .gitignore 2>/dev/null || echo '.hal-vault/' >> .gitignore
```

Then point every command at it — either per command with `-d .hal-vault`,
or once per shell:

```
export HAL_VAULT_DIR="$PWD/.hal-vault"
```

The examples below assume `HAL_VAULT_DIR` is set (otherwise append
`-d .hal-vault`). For a machine-global vault instead, plain `hal-vault
init` uses `~/.hal-vault` with an auto-generated `~/.ssh/hal-vault_ed25519`
key.

## The safety contract (non-negotiable)

1. **Never print a raw secret value** into the conversation, a log, a
   comment, a commit, or a file. hal-vault's `list`, `search`, and `get`
   are masked by default (`sk-p…7890 (24 chars)`) — that masked form is the
   ONLY representation you may show or repeat.
2. **`--reveal` exists for machines, not for chat.** Use it only inside
   command substitution that feeds another process, never to display:

   ```
   OPENAI_API_KEY="$(hal-vault get openai --reveal)" ./deploy.sh
   ```

   Never run `hal-vault get x --reveal` bare, never `echo $(... --reveal)`,
   never redirect `--reveal` output into a file you will read back.
3. **Confirm storage with masked tips only.** After saving, answer like:
   "Saved — an OpenAI API key, tagged `openai, prod`, starts with `sk-p`."
4. **Refuse to recite.** If the user asks you to "print the key" or "paste
   the token here", offer the masked form and how to use it instead. If
   they explicitly insist on the raw value, tell them to run
   `hal-vault get <id> --reveal` themselves in their terminal — do not run
   it for them in the conversation.

## Workflows

### Store a secret the user shared

Identify what it is, pick a type and tags, then pipe the value on stdin
(hal-vault never accepts values as arguments):

```
printf '%s' 'sk-proj-abcdef1234567890' | \
  hal-vault add openai -t api_key --tags openai,llm,prod -n "OpenAI production key"
```

Output: `added 7q3k2m openai: sk-p…7890 (24 chars)` — repeat only this
masked confirmation back to the user.

Types: `api_key`, `password`, `token`, `ssh_key`, `cert`, `identity`,
`other`. Tag with: the service name, the environment (`prod`/`staging`),
and what it is for — tags are how you (and the user) will find it later.

### Answer "what secrets do we have?"

```
hal-vault list
hal-vault search openai
hal-vault search "" --tag prod
hal-vault search "" --type api_key
```

All output is masked; safe to show the table directly. Use `--json` when
you need to process the results.

### Use a secret in a command

Inject via command substitution so the value never enters the transcript:

```
ANTHROPIC_API_KEY="$(hal-vault get anthropic --reveal)" pnpm run e2e
curl -H "Authorization: Bearer $(hal-vault get github-pat --reveal)" https://api.github.com/user
```

### Rotate / update

```
printf '%s' 'sk-proj-newvalue9876543210' | hal-vault update openai --value
hal-vault update openai --tags openai,llm,staging -n "rotated 2026-06"
```

### Remove

```
hal-vault rm openai -f
```

Confirm with the user before removing anything you did not just create.

## Behavior notes

- `get` accepts an ID or a label; ambiguous labels return the candidate
  IDs (masked-safe) — retry with the ID.
- Exit codes: `0` success, `1` runtime error (e.g. not found), `2` usage
  error. Read stderr for the reason.
- Concurrent invocations are safe (the vault takes an exclusive lock).
- Secrets must be valid UTF-8; binary material should be base64-encoded
  before storing (hal-vault rejects it otherwise, it will not corrupt it).
- Vault directory resolution: `-d DIR` flag > `HAL_VAULT_DIR` env >
  `~/.hal-vault`. With a per-project vault, never commit `.hal-vault/`,
  and never place the SSH key inside the project tree.

For the full command reference, read
[references/cli-reference.md](references/cli-reference.md).
