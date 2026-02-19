---
name: env-manager
description: "Environment variable validation, security scanning, and management for Next.js, Vite, React, and Node.js applications"
progressive_disclosure:
  entry_point:
    summary: "Environment variable validation, security scanning, and management for Next.js, Vite, React, and Node.js applications"
    when_to_use: "When working with env-manager or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
  references:
    - frameworks.md
    - security.md
    - synchronization.md
    - troubleshooting.md
    - validation.md
---
# Environment Variable Manager (env-manager)

**Comprehensive environment variable validation, security scanning, and management for modern web applications.**

[![Security Audited](https://img.shields.io/badge/security-audited-success)](references/security.md)
[![Test Coverage](https://img.shields.io/badge/coverage-85%25%2B-success)](tests/)
[![Performance](https://img.shields.io/badge/performance-80x_faster-success)](#performance)

## Overview

The env-manager skill provides systematic environment variable management across local development, CI/CD pipelines, and deployment platforms. It prevents common issues like missing variables, exposed secrets, and framework-specific configuration errors.

**Key Features:**
- **Framework-Aware Validation**: Next.js, Vite, React, Node.js, Flask support
- **Security-First**: Never logs secrets, detects exposed credentials
- **Platform Integration**: Ready for Vercel, Railway, Heroku, and CI/CD
- **Fast**: Validates 1000 variables in 0.025s (80x faster than 2s target)
- **Zero Dependencies**: Pure Python, works anywhere

## Why Use env-manager?

**Common problems this solves:**
- "Works on my machine, but not in production" (missing env vars)
- Accidentally exposing API keys in client-side code (NEXT_PUBLIC_ with secrets)
- Missing required variables during deployment
- Inconsistent .env files across team members
- No documentation of required environment variables
- Security vulnerabilities from exposed secrets

## Quick Start

### Installation

No installation needed! env-manager is a bundled skill in Claude MPM.

**Requirements:**
- Python 3.7+
- No external dependencies

### 5-Minute Quick Start

```bash
# 1. Validate your .env file
python3 scripts/validate_env.py .env

# 2. Check for framework-specific issues (Next.js example)
python3 scripts/validate_env.py .env --framework nextjs

# 3. Compare with .env.example to find missing vars
python3 scripts/validate_env.py .env --compare-with .env.example

# 4. Generate .env.example for documentation
python3 scripts/validate_env.py .env --generate-example .env.example

# 5. Get JSON output for CI/CD integration
python3 scripts/validate_env.py .env --json
```

That's it! Environment variables are now validated professionally.

## Usage Examples

### Basic Validation

Validate a .env file for structural issues:

```bash
python3 scripts/validate_env.py .env
```

**What it checks:**
- Valid key=value format
- No duplicate keys
- Proper naming conventions (UPPERCASE_WITH_UNDERSCORES)
- No empty values (unless explicitly allowed)
- Proper quoting for values with spaces

**Example output:**
```
✅ Validation successful!
   - 15 variables validated
   - 0 errors
   - 0 warnings
```

### Framework-Specific Validation

#### Next.js

Validate Next.js environment variables:

```bash
python3 scripts/validate_env.py .env.local --framework nextjs
```

**Next.js-specific checks:**
- NEXT_PUBLIC_* variables are client-exposed (warns if secrets detected)
- .env.local, .env.production, .env file hierarchy
- Detects secrets in client-side variables

**Example:**
```bash
# .env.local
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_API_KEY=secret123  # ⚠️  WARNING: Secret in client-exposed variable!
DATABASE_URL=postgresql://...   # ✅ Server-side only
```

#### Vite

```bash
python3 scripts/validate_env.py .env --framework vite
```

**Vite-specific checks:**
- VITE_* variables are client-exposed
- Warns if secrets detected in VITE_ prefixed vars

#### React (Create React App)

```bash
python3 scripts/validate_env.py .env --framework react
```

**React-specific checks:**
- REACT_APP_* variables are client-exposed
- Warns if secrets in REACT_APP_ prefixed vars

#### Node.js/Express

```bash
python3 scripts/validate_env.py .env --framework nodejs
```

**Node.js-specific checks:**
- Common NODE_ENV, PORT, DATABASE_URL patterns
- Standard Node.js conventions

#### Flask/Python

```bash
python3 scripts/validate_env.py .env --framework flask
```

**Flask-specific checks:**
- FLASK_APP, FLASK_ENV variables
- SQLAlchemy DATABASE_URL format

### Comparing with .env.example

Ensure your .env has all required variables:

```bash
python3 scripts/validate_env.py .env --compare-with .env.example
```

**What it checks:**
- All variables in .env.example exist in .env
- No extra undocumented variables in .env

**Example output:**
```
❌ Missing variables:
   - DATABASE_URL (required in .env.example)
   - STRIPE_SECRET_KEY (required in .env.example)

⚠️  Extra variables not in .env.example:
   - DEBUG_MODE (consider adding to .env.example)
```

**Perfect for:**
- Onboarding new team members
- CI/CD validation
- Deployment pre-checks

### Generating .env.example

Create documentation for your environment variables:

```bash
python3 scripts/validate_env.py .env --generate-example .env.example
```

**What it does:**
- Reads your .env file
- Sanitizes secret values (replaces with placeholders)
- Generates .env.example with safe defaults

**Example:**

```bash
# Input: .env
DATABASE_URL=postgresql://user:pass@localhost/db  # pragma: allowlist secret
STRIPE_SECRET_KEY=sk_live_abc123xyz
NEXT_PUBLIC_API_URL=https://api.example.com

# Output: .env.example
DATABASE_URL=postgresql://user:password@localhost/dbname  # pragma: allowlist secret
STRIPE_SECRET_KEY=your_stripe_secret_key_here
NEXT_PUBLIC_API_URL=https://api.example.com
```

**Security note:** env-manager detects common secret patterns and replaces them with safe placeholders.

### CI/CD Integration

Get machine-readable JSON output for automated workflows:

```bash
python3 scripts/validate_env.py .env.example --strict --json
```

**JSON output format:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "stats": {
    "total_vars": 15,
    "errors": 0,
    "warnings": 0
  }
}
```

**Exit codes:**
- `0`: Validation passed
- `1`: Validation errors found
- `2`: Missing required file
- `3`: Warnings found (only in --strict mode)

**GitHub Actions example:**

```yaml
name: Validate Environment Variables

on: [push, pull_request]

jobs:
  validate-env:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate .env.example
        run: |
          python3 scripts/validate_env.py .env.example --strict --json
        working-directory: ./path/to/skill

      - name: Check for framework-specific issues
        run: |
          python3 scripts/validate_env.py .env.example --framework nextjs --json
        working-directory: ./path/to/skill
```

### Strict Mode

Treat warnings as errors (useful for CI/CD):

```bash
python3 scripts/validate_env.py .env --strict
```

**When to use:**
- Pre-deployment validation
- CI/CD pipelines
- Release gates
- Team standard enforcement

### Quiet Mode

Show only errors, suppress warnings:

```bash
python3 scripts/validate_env.py .env --quiet
```

**When to use:**
- You've already reviewed warnings
- Automated scripts that only care about errors
- Noisy environments where warnings are distracting

## Supported Frameworks

| Framework | Prefix | Client-Exposed | Notes |
|-----------|--------|----------------|-------|
| **Next.js** | `NEXT_PUBLIC_*` | Yes | Auto-exposed in browser |
| **Vite** | `VITE_*` | Yes | Bundled into client code |
| **React (CRA)** | `REACT_APP_*` | Yes | Embedded in production build |
| **Node.js** | N/A | No | Server-side only |
| **Flask** | N/A | No | Server-side only |

**Security warning:** Never put secrets in client-exposed variables (NEXT_PUBLIC_, VITE_, REACT_APP_). env-manager will warn you if it detects common secret patterns.

## CLI Reference

### Command Structure

```bash
python3 scripts/validate_env.py <file> [options]
```

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `--compare-with FILE` | Compare with .env.example | `--compare-with .env.example` |
| `--framework {nextjs\|vite\|react\|nodejs\|flask\|generic}` | Framework-specific validation | `--framework nextjs` |
| `--strict` | Treat warnings as errors | `--strict` |
| `--json` | JSON output for automation | `--json` |
| `--quiet` | Only show errors | `--quiet` |
| `--generate-example OUTPUT` | Generate .env.example | `--generate-example .env.example` |

### Exit Codes

| Code | Meaning | When |
|------|---------|------|
| `0` | Success | No errors (warnings OK unless --strict) |
| `1` | Validation errors | Structural issues, duplicates, etc. |
| `2` | File not found | Specified .env file doesn't exist |
| `3` | Warnings in strict mode | Warnings exist and --strict enabled |

## Common Use Cases

### Scenario 1: New Developer Onboarding

```bash
# New developer clones repo
git clone <repo>
cd <project>

# Copy example and fill in values
cp .env.example .env
# Edit .env with actual values...

# Validate setup
python3 scripts/validate_env.py .env --compare-with .env.example

# If missing variables, fix them
# Validation passes ✅
```

### Scenario 2: Pre-Deployment Check

```bash
# Before deploying to Vercel/Railway/Heroku
python3 scripts/validate_env.py .env.production --framework nextjs --strict

# Fix any errors
# Deploy with confidence ✅
```

### Scenario 3: Security Audit

```bash
# Check for accidentally exposed secrets
python3 scripts/validate_env.py .env.local --framework nextjs

# Look for warnings like:
# ⚠️  NEXT_PUBLIC_STRIPE_SECRET: Contains potential secret in client-exposed variable
```

### Scenario 4: Team Documentation

```bash
# After adding new environment variable
echo "NEW_API_KEY=abc123" >> .env

# Regenerate .env.example
python3 scripts/validate_env.py .env --generate-example .env.example

# Commit updated .env.example
git add .env.example
git commit -m "docs: add NEW_API_KEY to environment variables"
```

### Scenario 5: CI/CD Quality Gate

```yaml
# In your CI pipeline
- name: Validate environment configuration
  run: |
    python3 scripts/validate_env.py .env.example --strict --json > validation.json

    # Fail pipeline if validation fails
    if [ $? -ne 0 ]; then
      cat validation.json
      exit 1
    fi
```

## Performance

env-manager is designed for speed:

**Benchmarks:**
- Validates 1000 variables in **0.025s**
- 80x faster than 2s target
- Zero external dependencies
- Minimal memory footprint

**Why it matters:**
- Fast feedback during development
- No CI/CD slowdown
- Works in resource-constrained environments

## Security Notes

**Critical security features:**

1. **Never Logs Secrets**: env-manager NEVER displays actual secret values in output
2. **Client-Exposure Detection**: Warns when secrets are in NEXT_PUBLIC_, VITE_, REACT_APP_ variables
3. **Secret Sanitization**: When generating .env.example, replaces secrets with safe placeholders
4. **No Network Calls**: All validation is local, no data leaves your machine

**Security-audited:** This skill has undergone security review. See [references/security.md](references/security.md) for details.

**Best practices:**
- Never commit .env files with secrets
- Always use .env.example for documentation
- Use platform secret managers (Vercel, Railway, etc.) for production
- Validate before every deployment
- Run security scan regularly

## Common Issues

### "Missing equals sign" error

**Cause:** Line in .env doesn't have = separator

**Fix:**
```bash
# ❌ Bad
API_KEY

# ✅ Good
API_KEY=your_key_here
```

### "Duplicate key" error

**Cause:** Same variable defined multiple times

**Fix:**
```bash
# ❌ Bad
API_KEY=value1
API_KEY=value2

# ✅ Good
API_KEY=value2
```

### "Invalid variable name" warning

**Cause:** Variable name doesn't follow UPPERCASE_WITH_UNDERSCORES convention

**Fix:**
```bash
# ❌ Bad
apiKey=value
api-key=value

# ✅ Good
API_KEY=value
```

### "Potential secret in client-exposed variable" warning

**Cause:** NEXT_PUBLIC_, VITE_, or REACT_APP_ variable contains secret-like value

**Fix:**
```bash
# ❌ Bad (secret exposed to client!)
NEXT_PUBLIC_STRIPE_SECRET=sk_live_abc123

# ✅ Good (server-side only)
STRIPE_SECRET_KEY=sk_live_abc123
NEXT_PUBLIC_STRIPE_PUBLISHABLE=pk_live_xyz789
```

### "Empty value" warning

**Cause:** Variable has no value

**Fix:**
```bash
# ❌ Bad
DATABASE_URL=

# ✅ Good (if optional, document it)
DATABASE_URL=  # Optional, uses SQLite if not set

# ✅ Better
DATABASE_URL=postgresql://localhost/mydb
```

### File not found error

**Cause:** Specified .env file doesn't exist

**Fix:**
```bash
# Check file exists
ls -la .env

# Or create it
touch .env
```

## Troubleshooting

### Validation passes locally but fails in CI

**Check:**
1. Line endings (CRLF vs LF)
2. File encoding (UTF-8 expected)
3. File permissions
4. Python version (3.7+ required)

### Warnings about client-exposed variables

**This is intentional!** env-manager is warning you that variables like NEXT_PUBLIC_API_KEY will be visible in the browser.

**Options:**
1. Move secret to server-side variable (remove NEXT_PUBLIC_ prefix)
2. Use public/publishable keys only in client-exposed variables
3. If truly not a secret, ignore the warning

### .env.example generation replaces too much

env-manager is conservative about secrets. If it over-sanitizes:
1. Manually edit .env.example after generation
2. Use specific placeholder values in .env that won't trigger sanitization

## Advanced Usage

### Custom Validation Patterns

See [references/validation.md](references/validation.md) for advanced validation patterns.

### Platform-Specific Deployment

See [references/synchronization.md](references/synchronization.md) for Vercel, Railway, Heroku integration patterns.

### Framework-Specific Guides

See [references/frameworks.md](references/frameworks.md) for comprehensive framework guides.

## Related Documentation

- **[Validation Reference](references/validation.md)**: Complete validation workflows and checks
- **[Security Reference](references/security.md)**: Secret scanning and security patterns
- **[Synchronization Reference](references/synchronization.md)**: Platform sync patterns (coming soon)
- **[Frameworks Reference](references/frameworks.md)**: Framework-specific patterns and conventions
- **[Troubleshooting Guide](references/troubleshooting.md)**: Common issues and solutions

## Integration with Claude MPM

env-manager is a bundled skill in Claude MPM. Agents can use it for:
- Pre-deployment validation
- Security scanning
- Environment setup verification
- Documentation generation

See [INTEGRATION.md](INTEGRATION.md) for agent integration patterns.

## Contributing

env-manager follows Claude MPM contribution guidelines:

1. Run `make lint-fix` during development
2. Run `make quality` before commits
3. Add tests for new features (85%+ coverage required)
4. Update documentation

See [CONTRIBUTING.md](../../../../../../CONTRIBUTING.md) for details.

## License

MIT License - Part of Claude MPM project

## Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: See references/ directory
- **Examples**: See examples/ directory
- **Integration**: See INTEGRATION.md

---

**Version**: 1.0.0
**Status**: Stable, Security-Audited
**Test Coverage**: 85%+
**Performance**: 80x faster than target
