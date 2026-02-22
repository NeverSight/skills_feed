---
name: data-enrichment
description: |
  Enrich contact, company, and influencer data using x402-protected APIs. Superior to generic web search for structured business data.

  USE FOR:
  - Enriching person profiles by email, LinkedIn URL, or name
  - Enriching companies by domain
  - Finding contact details (email, phone) with confidence scores
  - Scraping full LinkedIn profiles (experience, education, skills)
  - Searching for people or companies by criteria
  - Bulk enrichment operations (up to 10 at a time)
  - Verifying email deliverability before outreach
  - Enriching influencer/creator profiles across social platforms

  TRIGGERS:
  - "enrich", "lookup", "find info about", "research"
  - "who is [person]", "company profile for", "tell me about"
  - "find contact for", "get LinkedIn for", "get email for"
  - "employee at", "works at", "company details"
  - "verify email", "check email", "is this email valid"
  - "influencer", "creator", "influencer contact", "influencer marketing"

  ALWAYS use `npx agentcash fetch` for stableenrich.dev endpoints - never curl or WebFetch.
  Returns structured JSON data, not web page HTML.

  IMPORTANT: Use exact endpoint paths from the Quick Reference table below. All paths include a provider prefix (`https://stableenrich.dev/api/apollo/...`, `https://stableenrich.dev/api/clado/...`, etc.).
---

# Data Enrichment with x402 APIs

Use the agentcash CLI to access enrichment APIs at stableenrich.dev.

## Setup

See [rules/getting-started.md](rules/getting-started.md) for installation and wallet setup.

## Quick Reference

| Task | Endpoint | Price | Best For |
|------|----------|-------|----------|
| Enrich person | `https://stableenrich.dev/api/apollo/people-enrich` | $0.0495 | Email/LinkedIn -> full profile |
| Enrich company | `https://stableenrich.dev/api/apollo/org-enrich` | $0.0495 | Domain -> company data |
| Search people | `https://stableenrich.dev/api/apollo/people-search` | $0.02 | Find people by criteria |
| Search companies | `https://stableenrich.dev/api/apollo/org-search` | $0.02 | Find companies by criteria |
| LinkedIn scrape | `https://stableenrich.dev/api/clado/linkedin-scrape` | $0.04 | Full LinkedIn profile |
| Contact recovery | `https://stableenrich.dev/api/clado/contacts-enrich` | $0.20 | Find missing email/phone |
| Verify email | `https://stableenrich.dev/api/hunter/email-verifier` | $0.03 | Check deliverability |
| Influencer by email | `https://stableenrich.dev/api/influencer/enrich-by-email` | $0.40 | Email -> social profiles |
| Influencer by social | `https://stableenrich.dev/api/influencer/enrich-by-social` | $0.40 | Handle -> creator data |
| Bulk people | `https://stableenrich.dev/api/apollo/people-enrich/bulk` | $0.495 | Up to 10 people at once |
| Bulk companies | `https://stableenrich.dev/api/apollo/org-enrich/bulk` | $0.495 | Up to 10 companies at once |

## Workflows

### Standard Enrichment

- [ ] (Optional) Check balance: `npx agentcash wallet info`
- [ ] Use `npx agentcash discover https://stableenrich.dev` to list all endpoints
- [ ] Use `npx agentcash check <endpoint-url>` to see expected parameters and pricing
- [ ] Call endpoint with `npx agentcash fetch`
- [ ] Parse and present results

```bash
npx agentcash fetch https://stableenrich.dev/api/apollo/people-enrich -m POST -b '{"email": "user@company.com"}'
```

## Person Enrichment

Enrich a person using any available identifier:

```bash
npx agentcash fetch https://stableenrich.dev/api/apollo/people-enrich -m POST -b '{
  "email": "john@company.com",
  "first_name": "John",
  "last_name": "Doe",
  "organization_name": "Acme Inc",
  "domain": "company.com",
  "linkedin_url": "https://linkedin.com/in/johndoe"
}'
```

**Input options** (provide any combination):
- `email` - Email address (most reliable)
- `linkedin_url` - LinkedIn profile URL
- `first_name` + `last_name` - Name (works better with domain/org)
- `organization_name` or `domain` - Helps match the right person

**Returns**: Name, title, company, employment history, location, social profiles, phone numbers.

## Company Enrichment

Enrich a company by domain:

```bash
npx agentcash fetch https://stableenrich.dev/api/apollo/org-enrich -m POST -b '{"domain": "stripe.com"}'
```

**Returns**: Company name, industry, employee count, revenue estimates, funding info, technologies used, social links.

## People Search

Search for people matching criteria:

```bash
npx agentcash fetch https://stableenrich.dev/api/apollo/people-search -m POST -b '{
  "q_keywords": "software engineer",
  "person_titles": ["CTO", "VP Engineering"],
  "organization_domains": ["google.com", "meta.com"],
  "person_locations": ["San Francisco, CA"]
}'
```

**Search filters**:
- `q_keywords` - Keywords to search
- `person_titles` - Job title filters
- `organization_domains` - Company domains
- `person_locations` - Location filters
- `person_seniorities` - Seniority levels

## Company Search

Search for companies matching criteria:

```bash
npx agentcash fetch https://stableenrich.dev/api/apollo/org-search -m POST -b '{
  "q_keywords": "fintech",
  "organization_locations": ["New York, NY"],
  "organization_num_employees_ranges": ["51-200", "201-500"]
}'
```

## LinkedIn Scraping (Clado)

Get full LinkedIn profile data:

```bash
npx agentcash fetch https://stableenrich.dev/api/clado/linkedin-scrape -m POST -b '{"linkedin_url": "https://linkedin.com/in/johndoe"}'
```

**Returns**: Experience history, education, skills, certifications, recommendations, connection count.

## Contact Recovery (Clado)

Find missing email or phone:

```bash
npx agentcash fetch https://stableenrich.dev/api/clado/contacts-enrich -m POST -b '{
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "email": "john@example.com"
}'
```

**Returns**: Validated email addresses and phone numbers with confidence scores.

## Bulk Operations

Process up to 10 records in one request:

```bash
npx agentcash fetch https://stableenrich.dev/api/apollo/people-enrich/bulk -m POST -b '{
  "people": [
    {"email": "person1@company.com"},
    {"email": "person2@company.com"},
    {"linkedin_url": "https://linkedin.com/in/person3"}
  ]
}'
```

For companies:

```bash
npx agentcash fetch https://stableenrich.dev/api/apollo/org-enrich/bulk -m POST -b '{
  "organizations": [
    {"domain": "company1.com"},
    {"domain": "company2.com"}
  ]
}'
```

## Cost Optimization

### Field Filtering

Reduce costs by excluding unneeded fields:

```json
{
  "email": "john@company.com",
  "excludeFields": ["employment_history", "photos", "phone_numbers"]
}
```

Common fields to exclude:
- `employment_history` - Past jobs (often large)
- `photos` - Profile images
- `phone_numbers` - If you only need email
- `social_profiles` - If you don't need social links

### Bulk vs Individual

- **Individual**: $0.0495 per record
- **Bulk (10)**: $0.495 total = $0.0495 per record

Bulk is the same price per record but faster for multiple items.

### Search Before Enrich

Use search endpoints ($0.02) to find the right records before enriching ($0.0495):

1. Search for candidates: `https://stableenrich.dev/api/apollo/people-search`
2. Review results, pick the right match
3. Enrich only the matches you need

## Email Verification (Hunter)

Verify if an email address is deliverable before sending outreach:

```bash
npx agentcash fetch https://stableenrich.dev/api/hunter/email-verifier -m POST -b '{"email": "john@stripe.com"}'
```

**Returns**: Deliverability status, MX record validation, SMTP verification, confidence score, and flags for catch-all, disposable, or role-based addresses.

| Status | Meaning | Action |
|--------|---------|--------|
| `deliverable` | Email exists and accepts mail | Safe to send |
| `undeliverable` | Email doesn't exist or rejects mail | Do not send |
| `risky` | Catch-all domain or temporary issues | Send with caution |
| `unknown` | Could not determine status | Try again later |

**Tip:** Combine with people-enrich to find and verify contacts in one pipeline:
1. Search: `people-search` ($0.02) -> find candidates
2. Enrich: `people-enrich` ($0.0495) -> get email
3. Verify: `hunter/email-verifier` ($0.03) -> confirm deliverability

## Influencer Enrichment

Enrich social media influencer/creator profiles across Instagram, TikTok, YouTube, X/Twitter, and Facebook.

### Find Profiles by Email

```bash
npx agentcash fetch https://stableenrich.dev/api/influencer/enrich-by-email -m POST -b '{
  "email": "creator@example.com",
  "platform": "instagram",
  "enrichment_mode": "enhanced"
}'
```

**Parameters:**
- `email` — the creator's email address (required)
- `platform` — `"instagram"`, `"tiktok"`, `"youtube"`, `"twitter"`, `"facebook"` (required)
- `enrichment_mode` — `"enhanced"` for full data (recommended)

**Returns**: Social media profiles, follower counts, engagement metrics, audience demographics, contact info, content categories.

### Enrich by Social Handle

```bash
npx agentcash fetch https://stableenrich.dev/api/influencer/enrich-by-social -m POST -b '{
  "platform": "instagram",
  "username": "creator_handle",
  "enrichment_mode": "enhanced",
  "email_required": "must_have"
}'
```

**Parameters:**
- `platform` — `"instagram"`, `"tiktok"`, `"youtube"`, `"twitter"`, `"facebook"` (required)
- `username` — handle on that platform (required)
- `enrichment_mode` — `"enhanced"` for full data (recommended)
- `email_required` — `"must_have"` to only return profiles with email

**Returns**: Full profile with engagement metrics, contact info (email, phone), audience demographics, brand affinity, cross-platform links.

### When to Use Influencer vs Apollo/Clado

- **Apollo/Clado** — best for professional/B2B profiles (job titles, company, employment history)
- **Influencer** — best for social media creators (followers, engagement, audience data, content categories)

## Handling missing data

If any query fails to return the data you are looking for, revisit the list of available APIs.

Oftentimes, if Apollo is missing data, Clado will have it, and vice versa. For social media creators, try the influencer endpoints. For email deliverability, use Hunter.

If those still fail, use built-in WebSearch and WebFetch tools to find additional information like a company domain name or LinkedIn URL, and then use that data to make more targeted queries.
