---
name: prod-ready
description: Production-readiness audit covering linting, security, edge cases, and deployment checks. Only trigger when the user explicitly says "run prod-ready workflow" — do not run proactively.
---

# PRODUCTION READY

Perform a production-readiness audit before deployment. Verify the codebase meets security, reliability, and quality standards.

---

## PHASE 1: RUN OFFICIAL LINTING & BUILD CHECKS

Run all available project tooling. Every check must pass before deployment.

### Detect project type and run ALL applicable commands:

**JavaScript/TypeScript projects:**
```bash
pnpm lint          # ESLint / project linter
pnpm typecheck     # or: tsc --noEmit
pnpm test          # full test suite
pnpm build         # production build must succeed
pnpm audit         # dependency vulnerabilities
```

**Python projects:**
```bash
ruff check .       # or: pylint src/ OR flake8
mypy .             # type checking
pytest             # full test suite
pip-audit          # dependency vulnerabilities
```

**Go projects:**
```bash
go vet ./...
golangci-lint run
go test ./...
```

**Rust projects:**
```bash
cargo clippy -- -D warnings
cargo test
cargo audit
```

If a command doesn't exist (e.g., no `typecheck` script), skip it and note that in the report.

**All checks must pass.** If any fail, document the failures - they must be addressed before deployment.

---

## PHASE 2: SECURITY AUDIT

### 2.1 Sensitive Files in Repository

Check for files that should NEVER be committed:

```bash
# Files that shouldn't be in git
git ls-files | rg -i '\.(env|pem|key|p12|pfx|sqlite|db)$' | rg -v '\.example|\.sample|\.template'

# Credentials and secrets files
git ls-files | rg -i 'credentials|secrets|private.*key|id_rsa|\.keystore'

# Check .gitignore covers common sensitive patterns
cat .gitignore 2>/dev/null | rg -q '\.env' || echo "WARNING: .env not in .gitignore"
```

**Any sensitive files found = BLOCKER. They must be removed and rotated.**

### 2.2 Hardcoded Secrets

Scan for secrets that should be environment variables:

```bash
# API keys and tokens (look for actual values, not variable names)
rg -i '(api[_-]?key|api[_-]?secret|auth[_-]?token|access[_-]?token)\s*[=:]\s*["\047][A-Za-z0-9_\-]{16,}' -g '!*.lock' -g '!node_modules' -g '!*.md'

# AWS keys pattern
rg 'AKIA[0-9A-Z]{16}' -g '!*.lock' -g '!node_modules'

# Private keys embedded in code
rg 'BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY' -g '!*.lock' -g '!node_modules'

# Connection strings with credentials
rg -i '(mongodb|postgres|mysql|redis)://[^:]+:[^@]+@' -g '!*.lock' -g '!node_modules' -g '!*.md'
```

### 2.3 Dangerous Code Patterns

```bash
# eval/exec with potential user input
rg '\b(eval|exec)\s*\(' --type ts --type js --type py

# SQL injection risks (string concatenation in queries)
rg -i '(query|execute)\s*\(\s*[`"\047].*\+|\$\{' --type ts --type js --type py

# Command injection risks
rg -i '(child_process|subprocess|os\.system|shell_exec)\s*\(' --type ts --type js --type py

# innerHTML / dangerouslySetInnerHTML without sanitization
rg '(innerHTML|dangerouslySetInnerHTML)' --type ts --type js --type tsx

# Disabled security features
rg -i 'verify\s*[=:]\s*false|rejectUnauthorized\s*[=:]\s*false' --type ts --type js --type py
```

### 2.4 Authentication & Authorization

Review these areas in the codebase:
- **API routes** - Do all sensitive endpoints have auth guards?
- **Role checks** - Are permissions verified before sensitive operations?
- **Token handling** - Are tokens stored securely (not localStorage for sensitive apps)?

```bash
# Find API route definitions to verify auth coverage
rg '(app\.(get|post|put|delete|patch)|router\.(get|post|put|delete|patch)|@(Get|Post|Put|Delete|Patch))' --type ts --type js -l

# Find auth middleware/decorators
rg -i '(auth|protect|guard|middleware|@Authorized|@Auth|requireAuth)' --type ts --type js --type py -l
```

---

## PHASE 3: EDGE CASE & ERROR HANDLING

### 3.1 Unhandled Errors

```bash
# Async functions - check for try-catch or .catch()
rg 'async\s+\w+\s*\([^)]*\)\s*\{' --type ts --type js -l

# Empty catch blocks (swallowing errors)
rg 'catch\s*\([^)]*\)\s*\{\s*\}' --type ts --type js

# Promises without .catch()
rg '\.then\s*\([^)]+\)\s*[^.]' --type ts --type js

# Unhandled promise rejection risk
rg 'new Promise\s*\(' --type ts --type js -l
```

Review the files found to ensure proper error handling exists.

### 3.2 Null/Undefined Handling

```bash
# Optional chaining opportunities (potential null access)
rg '\w+\.\w+\.\w+' --type ts --type js | head -20

# Check for nullish coalescing and optional chaining usage
rg '(\?\.|\ \?\?)' --type ts --type js --count || echo "Limited null-safety patterns found"
```

### 3.3 Input Validation

```bash
# API endpoints - verify input validation exists
rg '(req\.body|req\.params|req\.query|request\.json)' --type ts --type js --type py -l

# Check for validation libraries in use
rg -i '(zod|yup|joi|class-validator|pydantic|marshmallow)' --type ts --type js --type py -l || echo "No validation library detected"
```

### 3.4 Debug & Development Artifacts

```bash
# Console statements (excessive logging in production)
rg 'console\.(log|debug|trace|info)' --type ts --type js --count

# Debugger statements (must be zero)
rg '\bdebugger\b' --type ts --type js

# Debug flags
rg -i 'DEBUG\s*[=:]\s*true|VERBOSE\s*[=:]\s*true' -g '!node_modules'

# TODO/FIXME in critical code
rg '(TODO|FIXME|HACK|XXX):?' --type ts --type js --type py --count
```

**Debugger statements = BLOCKER.** Console.logs should be minimal. TODOs should be reviewed if in critical paths.

---

## PHASE 4: CONFIGURATION & ENVIRONMENT

### 4.1 Environment Variables

```bash
# Find all env var usage
rg '(process\.env|import\.meta\.env|os\.environ|os\.getenv)' --type ts --type js --type py -l

# Check .env.example exists and documents required vars
ls -la .env.example .env.sample 2>/dev/null || echo "WARNING: No .env.example file"

# Verify no .env files committed
git ls-files | rg '^\.env$|^\.env\.(local|production|development)$'
```

### 4.2 Hardcoded Configuration

```bash
# Localhost/staging URLs that should be env vars
rg -i '(localhost|127\.0\.0\.1|staging\.|\.local)' --type ts --type js --type py -g '!*.test.*' -g '!*.spec.*' -g '!node_modules'

# Hardcoded ports
rg ':\d{4,5}["\047/]' --type ts --type js -g '!node_modules' -g '!*.lock'
```

### 4.3 Third-Party Integrations

Verify production configuration for:
- API endpoints pointing to production (not staging/sandbox)
- Webhook URLs configured for production
- Analytics/monitoring enabled

---

## PHASE 5: DEPENDENCY HEALTH

### 5.1 Vulnerability Audit

```bash
# JavaScript
pnpm audit --audit-level=high

# Python
pip-audit

# Go
govulncheck ./...

# Rust
cargo audit
```

**Critical or high severity vulnerabilities = BLOCKER** unless documented with mitigation.

### 5.2 Outdated Dependencies

```bash
# Check for significantly outdated packages
pnpm outdated 2>/dev/null || npm outdated 2>/dev/null

# Python
pip list --outdated 2>/dev/null
```

Note major version updates that may be needed.

---

## OUTPUT REPORT

Provide a structured report:

```
## Production Readiness Report

### Linting & Build
| Check | Status | Notes |
|-------|--------|-------|
| Lint | PASS/FAIL | |
| Types | PASS/FAIL | |
| Tests | PASS/FAIL/SKIPPED | |
| Build | PASS/FAIL | |

### Security
| Check | Status | Notes |
|-------|--------|-------|
| Sensitive files | CLEAR/FOUND | |
| Hardcoded secrets | CLEAR/FOUND | |
| Dangerous patterns | CLEAR/FOUND | List any |
| Auth coverage | VERIFIED/NEEDS REVIEW | |

### Edge Cases & Error Handling
| Check | Status | Notes |
|-------|--------|-------|
| Error handling | ADEQUATE/NEEDS WORK | |
| Input validation | PRESENT/MISSING | |
| Debug artifacts | CLEAR/FOUND | Counts |

### Configuration
| Check | Status | Notes |
|-------|--------|-------|
| Env vars documented | YES/NO | |
| Hardcoded URLs | CLEAR/FOUND | |

### Dependencies
| Check | Status | Notes |
|-------|--------|-------|
| Vulnerabilities | X critical, Y high | |
| Outdated | X major updates available | |

### Blockers (must fix before deploy)
- [List any blockers]

### Warnings (should address)
- [List warnings]

### Recommendation
[READY TO DEPLOY / FIX BLOCKERS FIRST / NEEDS SIGNIFICANT WORK]
```

---

## CONSTRAINTS

- **Run all official linting tools** - Don't manually lint, but run eslint/ruff/etc.
- **Security issues are blockers** - Secrets, vulnerabilities, and dangerous patterns must be fixed
- **Don't auto-fix issues** - Report findings for the user to decide
- **Adapt to project type** - Skip inapplicable checks (no Python tooling for JS projects)
- **Be thorough but efficient** - Use grep patterns to scan, then review flagged areas
