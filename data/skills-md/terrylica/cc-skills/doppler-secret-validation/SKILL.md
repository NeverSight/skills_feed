---
name: doppler-secret-validation
description: Validate and test Doppler secrets. TRIGGERS - add to Doppler, store secret, validate token, test credentials.
allowed-tools: Read, Bash
---

# Doppler Secret Validation

## Overview

Workflow for securely adding, validating, and testing API tokens and credentials in Doppler secrets management.

## When to Use This Skill

Use this skill when:

- User provides API tokens or credentials (PyPI, GitHub, AWS, etc.)
- User mentions "add to Doppler", "store secret", "validate token"
- User wants to test authentication before production use
- User needs to verify secret storage and retrieval

## Workflow

### Step 1: Test Token Format (Before Adding to Doppler)

Before storing in Doppler, validate token format:

```bash
# Check token format, length, prefix
python3 -c "token = 'TOKEN_VALUE'; print(f'Prefix: {token[:20]}...'); print(f'Length: {len(token)}')"
```

**Common token formats**:

- PyPI: `pypi-...` (179 chars)
- GitHub: `ghp_...` (40+ chars)
- AWS: 20-char access key + 40-char secret

### Step 2: Add Secret to Doppler

```bash
doppler secrets set SECRET_NAME="value" --project PROJECT --config CONFIG
```

**Example**:

```bash
doppler secrets set PYPI_TOKEN="pypi-AgEI..." \
  --project claude-config --config prd
```

**Important**: CLI doesn't support `--note`. Add notes via dashboard:

1. <https://dashboard.doppler.com>
2. Navigate: PROJECT → CONFIG → SECRET_NAME
3. Edit → Add descriptive note

### Step 3: Validate Storage

Use the bundled validation script:

```bash
/usr/bin/env bash << 'VALIDATE_EOF'
cd ${CLAUDE_PLUGIN_ROOT}/skills/doppler-secret-validation
uv run scripts/validate_secret.py \
  --project PROJECT \
  --config CONFIG \
  --secret SECRET_NAME
VALIDATE_EOF
```

This validates:

1. Secret exists in Doppler
2. Secret retrieval works
3. Environment injection works via `doppler run`

**Example**:

```bash
uv run scripts/validate_secret.py \
  --project claude-config \
  --config prd \
  --secret PYPI_TOKEN
```

### Step 4: Test API Authentication

Use the bundled auth test script (adapt test_api_authentication() for specific API):

```bash
/usr/bin/env bash << 'CONFIG_EOF'
cd ${CLAUDE_PLUGIN_ROOT}/skills/doppler-secret-validation
doppler run --project PROJECT --config CONFIG -- \
  uv run scripts/test_api_auth.py \
    --secret SECRET_NAME \
    --api-url API_ENDPOINT
CONFIG_EOF
```

**Example (PyPI)**:

```bash
doppler run --project claude-config --config prd -- \
  uv run scripts/test_api_auth.py \
    --secret PYPI_TOKEN \
    --api-url https://upload.pypi.org/legacy/
```

### Step 5: Document Usage

After validation, document the usage pattern for the user:

```bash
/usr/bin/env bash << 'CONFIG_EOF_2'
# Pattern 1: Doppler run (recommended for CI/scripts)
doppler run --project PROJECT --config CONFIG -- COMMAND

# Pattern 2: Manual export (for troubleshooting)
export SECRET_NAME=$(doppler secrets get SECRET_NAME \
  --project PROJECT --config CONFIG --plain)
CONFIG_EOF_2
```

### Step 5b: mise [env] Integration (Recommended for Local Development)

For multi-account GitHub setups or per-directory credential needs, integrate Doppler secrets with mise `[env]`:

```toml
# .mise.toml
[env]
# Option A: Direct Doppler CLI fetch (slower, always fresh)
GH_TOKEN = "{{ exec(command='doppler secrets get GH_TOKEN --project myproject --config prd --plain') }}"
GITHUB_TOKEN = "{{ exec(command='doppler secrets get GH_TOKEN --project myproject --config prd --plain') }}"

# Option B: Cache for performance (1 hour cache)
GH_TOKEN = "{{ cache(key='gh_token', duration='1h', run='doppler secrets get GH_TOKEN --project myproject --config prd --plain') }}"
GITHUB_TOKEN = "{{ cache(key='gh_token', duration='1h', run='doppler secrets get GH_TOKEN --project myproject --config prd --plain') }}"
```

**Note**: Set BOTH `GH_TOKEN` and `GITHUB_TOKEN` - different tools check different variable names (gh CLI vs npm scripts).

**Why mise [env]?** Doppler `doppler run` is session-scoped; mise `[env]` provides directory-scoped credentials that persist across commands.

See [`mise-configuration` skill](../../../itp/skills/mise-configuration/SKILL.md#github-token-multi-account-patterns) for complete patterns.

## Common Patterns

### Multiple Configs (dev, stg, prd)

Add secret to multiple environments:

```bash
# Production
doppler secrets set TOKEN="prod-value" --project foo --config prd

# Development
doppler secrets set TOKEN="dev-value" --project foo --config dev
```

### Verify Secret Across Configs

```bash
/usr/bin/env bash << 'CONFIG_EOF_3'
for config in dev stg prd; do
  echo "=== $config ==="
  doppler secrets get TOKEN --project foo --config $config --plain | head -c 20
  echo "..."
done
CONFIG_EOF_3
```

## Security Guidelines

1. **Never log full secrets**: Use `${SECRET:0:20}...` masking
2. **Prefer doppler run**: Scopes secrets to single command
3. **Use --plain only for piping**: Human-readable view masks secrets
4. **Separate configs per environment**: dev/stg/prd isolation

## Bundled Resources

- **scripts/validate_secret.py** - Complete validation suite (existence, retrieval, injection)
- **scripts/test_api_auth.py** - Template for API authentication testing
- **references/doppler-patterns.md** - Common CLI patterns and examples

## Reference

- Doppler docs: <https://docs.doppler.com/docs>
- CLI install: `brew install dopplerhq/cli/doppler`
- See [doppler-patterns.md](./references/doppler-patterns.md) for comprehensive patterns

---

## Troubleshooting

| Issue                       | Cause                          | Solution                                              |
| --------------------------- | ------------------------------ | ----------------------------------------------------- |
| Secret not found            | Wrong project/config specified | Verify with `doppler secrets ls --project X --config` |
| Auth test fails with 401    | Token expired or invalid       | Regenerate token, re-add to Doppler                   |
| doppler run hangs           | CLI waiting for input          | Add `--no-interactive` flag                           |
| Token prefix mismatch       | Wrong token type used          | Check expected format (pypi-, ghp-, AKIA, etc.)       |
| Validation script not found | Wrong directory context        | Ensure CLAUDE_PLUGIN_ROOT is set correctly            |
| Secret retrieval empty      | Secret name typo               | List secrets: `doppler secrets ls --project X`        |
| mise cache stale            | Duration expired               | Clear cache or reduce duration setting                |
| Multiple configs confusion  | Secrets differ across envs     | Use explicit --config flag for each command           |
