---
name: codex-custom-model-provider
description: >-
  Fix Codex Groq/OpenRouter providers and profiles, unsupported project-local keys, wire_api
  mismatches, and Codex 0.134+ migrations.
author: Claude Code
version: 2.0.0
date: 2026-06-18
---

# Codex Custom Model Provider Configuration

## Problem

Custom providers and profiles fail when credential-affecting settings are placed in project
`.codex/config.toml`, or when Codex 0.134+ is given the legacy `[profiles.*]` format.

## Context / Trigger Conditions

- `Ignored unsupported project-local config keys ... model_providers, profiles`
- `--profile NAME cannot be used while ... config.toml contains legacy ... [profiles.NAME]`
- A named profile selects the project model instead of its own model
- A custom provider returns authentication, endpoint, or `wire_api` errors
- Migrating a machine from Codex 0.133 or earlier to 0.134 or later

## Solution

### 1. Keep Provider Settings in a User Layer

Provider definitions can live in `~/.codex/config.toml` or a selected user profile file. Do not
put `model_provider`, `model_providers`, or `profiles` in project `.codex/config.toml`;
Codex ignores those keys there for security.

```toml
# ~/.codex/config.toml
[model_providers.groq]
base_url = "https://api.groq.com/openai/v1"
env_key = "GROQ_API_KEY"
name = "Groq"
wire_api = "responses"
```

Keep credentials in the environment. `env_key` names the variable; it does not contain the
secret.

### 2. Use Separate Profile Files on Codex 0.134+

Each profile is `$CODEX_HOME/<name>.config.toml`. Use top-level keys rather than a
`[profiles.<name>]` table.

```toml
# ~/.codex/groq-gpt.config.toml
model = "openai/gpt-oss-120b"
model_provider = "groq"
```

A self-contained profile may also include its `[model_providers.groq]` table. Run it with:

```bash
codex --profile groq-gpt
codex exec --profile groq-gpt "Reply with OK"
```

Codex 0.133 and earlier reads `[profiles.*]` from `config.toml`. Upgrade the CLI before
removing those legacy tables.

### 3. Account for Configuration Precedence

The effective order is CLI override, project config, selected profile, user config, system config,
then built-in defaults. A project-level `model` overrides the selected profile's `model`.
Remove that project key if named profiles must choose their own models.

### 4. Select the Correct Wire API

Prefer `wire_api = "responses"` when the provider implements the Responses API. Chat
Completions support is deprecated in Codex and may be removed; use it only when the installed
Codex version and provider still require it. A 404 on the selected endpoint usually means the
provider and `wire_api` do not match.

## Verification

```bash
codex --version
codex doctor --json
codex --profile groq-gpt debug prompt-input diagnostic >/dev/null
```

Confirm that:

- `config.load.status` is `ok` and has no project-local-key warning.
- The named-profile command exits successfully.
- A small `codex exec --profile ...` smoke test succeeds when the provider key is available.

## Notes

- `codex login status` can report ChatGPT login even when the stored refresh token is stale.
  Verify authentication with a small real execution after upgrading.
- If a config file is shared by symlink across machines, detach it before changing formats so a
  repository pull cannot silently rewrite another machine's user settings.
- Project config cannot select a user profile; pass `--profile <name>` explicitly.
- Model availability and endpoint support depend on the provider.

## References

- [Codex advanced configuration](https://developers.openai.com/codex/config-advanced/)
- [Codex configuration basics](https://developers.openai.com/codex/config-basic/)
- [Codex configuration reference](https://developers.openai.com/codex/config-reference/)
