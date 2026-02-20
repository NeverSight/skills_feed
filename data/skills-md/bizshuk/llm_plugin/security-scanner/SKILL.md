---
name: Security Scanner
description: Scan workspace for potential security risks including exposed passwords, API keys, tokens, and other sensitive data
---

# Security Scanner

This skill helps you identify potential security vulnerabilities in your workspace by scanning for hardcoded credentials, API keys, tokens, and other sensitive information that should not be committed to version control.

## What It Scans For

The security scanner looks for common patterns of sensitive data:

### Credentials & Authentication

- Passwords (hardcoded, plaintext)
- Usernames in authentication contexts
- Private keys (RSA, SSH, PGP)
- Authentication tokens
- Session IDs
- PIN codes

### API Keys & Tokens

- AWS Access Keys (AKIA...)
- GitHub Personal Access Tokens (ghp*, gho*, ghu\_)
- Slack Tokens (xox[baprs]-)
- Google API Keys
- Stripe API Keys (sk*live*, pk*live*)
- JWT tokens
- OAuth tokens
- Bearer tokens

### Database & Service Credentials

- Database connection strings
- MongoDB URIs
- PostgreSQL connection strings
- MySQL credentials
- Redis URLs with passwords

### Cloud Provider Secrets

- AWS Secret Access Keys
- Azure Storage Keys
- Google Cloud Service Account Keys
- Heroku API Keys
- DigitalOcean Access Tokens

### Generic Patterns

- Base64 encoded secrets (suspicious patterns)
- Hexadecimal keys (32+ chars)
- Environment variable assignments with sensitive keys
- Configuration files with credentials

## How to Use

### Basic Scan

Scan the entire workspace for all security risks:

```bash
# The assistant will:
# 1. Search for common secret patterns
# 2. Check for hardcoded credentials
# 3. Identify suspicious files (e.g., .env not in .gitignore)
# 4. Report findings with file locations and line numbers
```

Simply ask: **"Run a security scan"** or **"Check for exposed secrets"**

### Targeted Scans

You can also request specific scans:

- **"Scan for API keys"** - Focus on API key patterns
- **"Check for passwords"** - Look for password patterns
- **"Find AWS credentials"** - Search for AWS-specific secrets
- **"Scan database connection strings"** - Find DB credentials

### Custom Pattern Scan

Request a scan for specific patterns:

- **"Search for tokens matching pattern X"**
- **"Find all base64 encoded strings longer than 40 characters"**

## Scan Process

When you invoke this skill, the assistant will:

1. **Identify Scan Scope**
   - Determine workspace boundaries
   - Exclude common directories (node_modules, .git, vendor, dist, build)
   - Respect .gitignore patterns

2. **Pattern Matching**
   - Use regex patterns to find sensitive data
   - Check file contents using grep/ripgrep
   - Flag suspicious variable names and comments

3. **Contextual Analysis**
   - Examine surrounding code for context
   - Identify if secrets are in test files (lower risk)
   - Check if files are tracked in git

4. **Report Generation**
   - List all findings with severity levels
   - Provide file paths and line numbers
   - Suggest remediation steps

## Example Patterns Detected

### High Severity

```python
# ❌ Hardcoded AWS credentials
AWS_ACCESS_KEY_ID = "example"
AWS_SECRET_ACCESS_KEY = "example"

# ❌ Database password in connection string
DATABASE_URL = "postgresql://user:MyP@ssw0rd@localhost:5432/db"

# ❌ Private API key
STRIPE_SECRET_KEY = "example"
```

### Medium Severity

```javascript
// ⚠️ Suspicious base64 string
const token = "example";

// ⚠️ Hardcoded password variable
let password = "example";
```

### Lower Risk (But Still Flagged)

```bash
# ℹ️ In test files or examples
export TEST_API_KEY="test_abc123"

# ℹ️ Placeholder patterns
password = "YOUR_PASSWORD_HERE"
```

## Remediation Recommendations

For each finding, the assistant will suggest:

1. **Move to Environment Variables**

   ```bash
   # Instead of hardcoding:
   API_KEY = "abc123"

   # Use:
   API_KEY = os.getenv("API_KEY")
   ```

2. **Use Secret Management**
   - HashiCorp Vault
   - AWS Secrets Manager
   - Azure Key Vault
   - Google Secret Manager

3. **Update .gitignore**
   - Ensure .env files are ignored
   - Add patterns for credential files

4. **Rotate Compromised Secrets**
   - If secrets are in git history, rotate them immediately
   - Use tools like `git-secrets` or `truffleHog` for history scanning

5. **Use Git Hooks**
   - Install pre-commit hooks to prevent secret commits
   - Tools: `pre-commit`, `detect-secrets`, `git-secrets`

## Files and Directories

This skill uses a scanning script located at:

- `scripts/scan_secrets.sh` - Main scanning logic

## Exclusions

The scanner automatically excludes:

- `node_modules/`, `vendor/`, `.git/`
- `dist/`, `build/`, `target/`
- Binary files and large data files
- Test fixtures with placeholder credentials
- Documentation with example credentials (marked as such)

## Best Practices

1. **Regular Scans**: Run security scans regularly, especially before commits
2. **CI/CD Integration**: Add secret scanning to your CI/CD pipeline
3. **Developer Education**: Ensure team knows not to commit secrets
4. **Secret Rotation**: Regularly rotate credentials and API keys
5. **Least Privilege**: Use minimal permissions for API keys and tokens

## Limitations

- **False Positives**: May flag test data or examples - use judgment
- **Encoded Secrets**: May not catch all obfuscated or encrypted secrets
- **Custom Patterns**: Very custom secret formats may not be detected
- **Performance**: Large codebases may take time to scan

## Security Note

⚠️ **This skill scans local files only and does not transmit secrets anywhere.** However, findings are shown in the assistant's output, so be cautious when sharing scan results.

## Getting Started

To run your first security scan, simply say:

> **"Scan my workspace for security risks"**

The assistant will scan your workspace and provide a detailed report of any potential security issues found.
