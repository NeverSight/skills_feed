---
name: astro-security
description: Security patterns for Astro lead generation websites on Cloudflare. Forms, headers, bot protection, GDPR. Use for any production lead gen site.
---

# Astro Security Skill

Security patterns for lead generation sites.

## Core Rules (Non-Negotiable)

| Violation | Result |
|-----------|--------|
| Production form without Turnstile + honeypot | **FAIL** |
| Secret exposed client-side | **FAIL** |
| User input stored without server validation | **FAIL** |
| Indexable staging environment | **FAIL** |
| Missing security headers | **FAIL** |
| Cookie banner missing before analytics | **FAIL** |

## Form Security (Required)

Every form must have:

| Protection | Implementation |
|------------|----------------|
| Turnstile | Cloudflare captcha (invisible mode) |
| Honeypot | Hidden field, reject if filled |
| Rate limit | Max 5 submissions/IP/hour |
| Validation | Server-side Zod, never trust client |
| Sanitize | Strip HTML, trim whitespace |

See [references/forms.md](references/forms.md).

## Security Headers (Required)

**CSP Rules:**
- MUST disallow inline scripts unless hashed
- MUST restrict script-src to required domains only
- MUST test in report-only before enforcement

Add to `_headers`:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Content-Security-Policy: [see references]
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

See [references/headers.md](references/headers.md).

## Environment Variables

```
# .env.example (commit this)
TURNSTILE_SITE_KEY=
TURNSTILE_SECRET_KEY=
RESEND_API_KEY=
GOOGLE_SHEETS_ID=

# .env (never commit)
# Add to .gitignore
```

**Rules:**
- Never expose secrets client-side
- Use `import.meta.env` for public vars only
- Validate all env vars on build

## Bot Protection

**Cloudflare (free tier):**
- Bot Fight Mode: ON
- Security Level: Medium
- Challenge Passage: 30 minutes

**Application level:**
- Turnstile on all forms
- Honeypot fields
- Rate limiting per IP
- Block empty referrer (optional)

## Third-Party Scripts

- Use SRI (integrity hash) for CDN scripts
- Load async/defer
- Minimize scripts
- Review GTM tags regularly

## GDPR Compliance

**Required:**
- Cookie banner (before non-essential cookies)
- Privacy policy page
- Form consent checkbox (if marketing)
- Data retention policy
- Right to deletion process

**Cookie categories:**
| Type | Consent | Examples |
|------|---------|----------|
| Necessary | No | Session, CSRF |
| Analytics | Yes | GA4, Hotjar |
| Marketing | Yes | Meta Pixel, Google Ads |

See [references/gdpr.md](references/gdpr.md).

## Input Validation

**Never:** Trust client-side alone, store raw input, render unsanitized HTML.

See forms.md for Zod schemas.

## File Uploads

If needed: Max 5MB, whitelist types, rename files, store outside webroot.

## Staging Protection

Password protect OR Cloudflare Access. Add `noindex`, block in robots.txt.

## Error Handling

- Error messages MUST NOT reveal stack traces or internals
- API errors MUST return generic messages (`Something went wrong`)
- Detailed errors allowed ONLY in development
- 404/500 pages must not leak tech stack info

## Dependencies

- Minimize third-party scripts
- Remove unused dependencies before launch
- Review third-party access quarterly
- Prefer self-hosted over CDN when possible

## Definition of Done

Security requirements before launch:

- [ ] Turnstile on all forms
- [ ] Honeypot fields added
- [ ] Rate limiting configured
- [ ] Security headers set
- [ ] HTTPS enforced
- [ ] .env in .gitignore
- [ ] No secrets in client code
- [ ] Cookie banner working
- [ ] Privacy policy linked
- [ ] Staging protected
- [ ] Error pages don't leak info

## References

- [forms.md](references/forms.md) — Form security patterns
- [headers.md](references/headers.md) — CSP and headers
- [gdpr.md](references/gdpr.md) — GDPR compliance
