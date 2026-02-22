---
name: secrets
description: "Enforce secure secrets management across all platforms. Never hardcode OAuth2 secrets, API keys, tokens, passwords, or credentials in source code. Store all secrets in .env files, load from environment variables, and ensure .env is gitignored. Use this skill when: (1) writing any code that uses API keys, OAuth2 client secrets, tokens, or credentials, (2) setting up authentication or third-party integrations, (3) creating new projects that need environment configuration, (4) reviewing code for security issues related to secrets, (5) configuring CI/CD pipelines or Docker deployments with secrets. Triggers: API key, OAuth, client secret, token, credentials, .env, environment variables, secret, password, authentication setup, third-party integration."
---

# Secrets Management

## Core Rules

1. **NEVER hardcode** secrets, API keys, OAuth2 client IDs/secrets, tokens, passwords, or credentials in source code
2. **ALWAYS store** secrets in `.env` files (or platform-native equivalents like `local.properties`, `.xcconfig`)
3. **ALWAYS load** secrets from environment variables at runtime
4. **ALWAYS add** `.env` to `.gitignore` before first commit
5. **ALWAYS provide** a `.env.example` documenting required variables (with empty values)

## Workflow

### When Writing Code That Uses Secrets

1. **Detect the platform/framework** from the project files
2. **Check if `.env` and `.gitignore` are set up** — if not, create them
3. **Load secrets from environment variables** using the platform's standard pattern
4. **Never use string literals** for secret values — always reference `process.env.*`, `os.getenv()`, etc.
5. **Add the variable name** to `.env.example` with an empty value and a descriptive comment
6. **Run the scan script** to verify no secrets leaked: `python3 scripts/scan_secrets.py .`

### When Setting Up a New Project

1. Create `.env` with required variables
2. Create `.env.example` mirroring `.env` structure with empty values (use [env-example-template](assets/env-example-template.txt) as a starting point)
3. Add secret-related entries to `.gitignore` (use [gitignore-secrets](assets/gitignore-secrets.txt) as reference)
4. Install the `.env` loading library for the platform
5. Add loading code at the application entry point

### When Reviewing Code

Run `python3 scripts/scan_secrets.py <project-directory>` to detect:
- Hardcoded API keys, tokens, and passwords
- OAuth2 client secrets in source
- AWS keys, Google API keys, Stripe keys, GitHub tokens
- Embedded private keys
- Connection strings with credentials
- Missing `.gitignore` entries for `.env`
- Missing `.env.example`

## Quick Reference by Platform

For platform-specific `.env` loading patterns (install, load, access, framework variants), see [references/platforms.md](references/platforms.md). Covers:

- **JavaScript/TypeScript**: Node.js, Next.js, Vite, React, Nuxt, Remix, Express, NestJS
- **Python**: Django, Flask, FastAPI
- **Ruby**: Rails
- **Go**: godotenv
- **Java/Kotlin**: Spring Boot
- **PHP**: Laravel
- **Rust**: dotenvy
- **Swift/iOS**: Xcode .xcconfig, Vapor
- **Android/Kotlin**: local.properties + BuildConfig
- **Flutter/Dart**: flutter_dotenv
- **C#/.NET**: DotNetEnv, User Secrets
- **Docker**: --env-file, docker-compose env_file
- **CI/CD**: GitHub Actions, GitLab CI, Vercel, Netlify, AWS, GCP, Azure

## Anti-Patterns to Block

Never generate code like:
```
# BAD - hardcoded secrets
api_key = "sk-1234567890abcdef"
client_secret = "my-oauth-secret"
DATABASE_URL = "postgres://user:password@host/db"
const token = "ghp_xxxxxxxxxxxxxxxxxxxx";
```

Always generate code like:
```
# GOOD - loaded from environment
api_key = os.getenv("API_KEY")
const token = process.env.GITHUB_TOKEN;
```

## Mobile Platform Notes

- **iOS**: Use `.xcconfig` files (gitignored) referenced from Xcode build settings — not `.env` at runtime
- **Android**: Use `local.properties` (gitignored by default) injected via `buildConfigField` — not `.env` at runtime
- **Flutter**: `flutter_dotenv` bundles `.env` into the app binary. For truly sensitive secrets, use a backend proxy instead of embedding in the mobile app
