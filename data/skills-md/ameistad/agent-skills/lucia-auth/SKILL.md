---
name: lucia-auth
description: Implement authentication following Lucia Auth best practices. Use when users ask to "add auth", "implement authentication", "setup login", "add sessions", "implement OAuth", "add 2FA/MFA", "password hashing", or reference "lucia auth" or "copenhagen book" patterns.
license: MIT
metadata:
  author: andreas
  version: "1.0.0"
---

# Lucia Auth

Implements secure authentication following the patterns from [Lucia Auth](https://lucia-auth.com) and [The Copenhagen Book](https://thecopenhagenbook.com).

## How It Works

1. Identify what type of authentication the user needs
2. Read the relevant reference documentation
3. Use the provided templates as a starting point
4. Adapt the templates to the user's framework and database

## Decision Tree

When a user asks for authentication, determine which components they need:

### Basic Auth (Username/Password)
- Read: `references/copenhagen-book/password-authentication.md`
- Read: `references/copenhagen-book/sessions.md`
- Read: `references/lucia/sessions-basic.md`
- Templates: `assets/password-utils.ts`, `assets/session-manager.ts`, `assets/session-schema.sql`

### OAuth (Social Login)
- Read: `references/copenhagen-book/oauth.md`
- Read: `references/lucia/tutorial-github-oauth.md` or `tutorial-google-oauth.md`
- Templates: `assets/oauth-handler.ts`

### Email Verification
- Read: `references/copenhagen-book/email-verification.md`
- Templates: `assets/email-verification.ts`

### Multi-Factor Authentication (MFA/2FA)
- Read: `references/copenhagen-book/mfa.md`
- For TOTP: Templates: `assets/totp-mfa.ts`
- For WebAuthn: Read: `references/copenhagen-book/webauthn.md`

### Session Management Only
- Read: `references/lucia/sessions-overview.md`
- Read: `references/lucia/sessions-basic.md`
- Read: `references/lucia/sessions-inactivity-timeout.md`
- Templates: `assets/session-manager.ts`

### Security Concerns
- CSRF: Read: `references/copenhagen-book/csrf.md`
- Rate Limiting: Read: `references/lucia/rate-limit-token-bucket.md`
- Password Reset: Read: `references/copenhagen-book/password-reset.md`

## Key Security Principles

Always follow these principles when implementing auth:

### Passwords
- Hash with Argon2id (or Scrypt/Bcrypt as fallbacks)
- Minimum 8 characters, no artificial maximum under 64
- Check against haveibeenpwned for compromised passwords
- Use constant-time comparison

### Sessions
- Generate IDs with 120+ bits of entropy using crypto.getRandomValues()
- Store secret hash, not the raw secret
- Set HttpOnly, Secure, SameSite=Lax cookies
- Implement sliding expiration for user-friendly apps
- Invalidate all sessions on password change

### OAuth
- Always use PKCE (code_challenge with S256)
- Store state in HttpOnly cookies
- Verify state on callback
- Link accounts by verified email only

### General
- Never trust client-provided data
- Implement rate limiting on all auth endpoints
- Use generic error messages ("Incorrect username or password")
- Verify CSRF tokens on state-changing operations

## Template Usage

The templates in `assets/` are framework-agnostic TypeScript. When using them:

1. Adapt the database interface to match the user's ORM/driver
2. Adjust cookie handling for the user's framework
3. Keep the core security logic unchanged
4. Add any framework-specific middleware

## When to Read Full References

Read the full reference documentation when:
- The user has specific questions about security tradeoffs
- Implementing edge cases (stateless tokens, sudo mode, etc.)
- The user explicitly asks about best practices
- You need to understand the "why" behind a pattern

## Example Scenarios

### User asks: "Add authentication to my Express app"
1. Ask if they need OAuth, password auth, or both
2. Read relevant references based on their choice
3. Create session table migration
4. Implement password hashing with `assets/password-utils.ts`
5. Implement session management with `assets/session-manager.ts`
6. Add login/logout/register routes
7. Add session middleware

### User asks: "Add Google OAuth"
1. Read `references/copenhagen-book/oauth.md`
2. Use `assets/oauth-handler.ts` as base
3. Create routes: GET /auth/google, GET /auth/google/callback
4. Implement user creation/linking on callback
5. Create session after successful OAuth

### User asks: "Add 2FA to existing auth"
1. Read `references/copenhagen-book/mfa.md`
2. Use `assets/totp-mfa.ts`
3. Add TOTP secret column to user table
4. Create setup flow (generate secret, show QR, verify)
5. Add 2FA check to login flow
6. Generate and store hashed recovery codes

## Updating Resources

The reference documentation can be updated by running:
```bash
./scripts/fetch-resources.sh
```

Check `references/VERSION.md` for current source versions.
