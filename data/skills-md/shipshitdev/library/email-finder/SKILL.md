---
name: email-finder
description: This skill should be used when users need to find email addresses associated with a domain. It activates when users ask to scan a domain for emails, find contact emails, discover email addresses, or replace email hunter functionality.
version: 1.0.0
tags:
  - email
  - domain
  - contact-discovery
  - lead-generation
---

# Email Finder

## Overview

Discover email addresses associated with a domain using a hybrid approach: free methods first (web scraping, pattern guessing, WHOIS lookup), then APIs (Hunter.io, Apollo.io, etc.) when keys are available.

## When to Use

- Scan a domain to find associated emails
- Find contact emails for a company
- Replace email hunter functionality
- Find email patterns for a domain
- Verify email addresses
- Enrich contact data with discovered emails

## Project Context Discovery

Before finding emails:

1. Check for existing email discovery tools
2. Review available API keys (Hunter.io, Apollo.io)
3. Check compliance/privacy requirements
4. Look for project-specific `[project]-email-finder` skill

## Methodology

### Free Methods (Primary)

1. **Web Scraping** - Scan `/contact`, `/about`, `/team` pages for emails
2. **WHOIS Lookup** - Query domain registration data
3. **Pattern Guessing** - Generate patterns from names found on site:
   - `firstname.lastname@domain.com`
   - `firstnamelastname@domain.com`
   - `firstname@domain.com`
   - `f.lastname@domain.com`

### API Methods (If Keys Available)

| API | Env Variable | Purpose |
|-----|-------------|---------|
| Hunter.io | `HUNTER_API_KEY` | Domain search + verification |
| Apollo.io | `APOLLO_API_KEY` | Contact discovery |
| Snov.io | `SNOV_CLIENT_ID/SECRET` | Email finder |
| Clearbit | `CLEARBIT_API_KEY` | Company enrichment |

## Email Result Interface

```typescript
interface EmailResult {
  email: string;
  source: 'web-scraping' | 'whois' | 'pattern-guessing' | 'hunter' | 'apollo';
  confidence?: number;
  firstName?: string;
  lastName?: string;
  position?: string;
  verified?: boolean;
}
```

## Best Practices

- **Rate limiting**: Delay between requests (1s recommended)
- **Respect robots.txt**: Check before scraping
- **Deduplicate**: Normalize emails (lowercase, trim)
- **Verify**: Use MX record checks or API verification
- **Filter**: Remove noreply@, donotreply@ addresses

## Legal & Ethical

- Comply with GDPR/CCPA
- Respect terms of service
- Honor opt-out requests
- Don't spam discovered emails

## Integration

Works well with:

- `leads-researcher` - Discover contact emails after researching companies
- `copywriter` - Use found emails for outreach campaigns

---

**For complete implementation code, API examples, verification patterns, and rate limiting utilities, see:** `references/full-guide.md`
