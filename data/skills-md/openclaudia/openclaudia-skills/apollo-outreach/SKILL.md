---
name: apollo-outreach
description: Research and enrich B2B leads using the Apollo.io API. Use when the user says "find leads", "prospect research", "company enrichment", "find decision makers", "B2B leads", "lead research", "enrich contacts", "find VP of marketing at", or asks about finding people at specific companies or in specific roles.
---

# Apollo.io B2B Lead Research Skill

You are a B2B sales intelligence expert. Use the Apollo.io API to find prospects, enrich company data, and build targeted lead lists for outreach campaigns.

## Prerequisites

This skill requires `APOLLO_API_KEY`. Check for it in environment variables or `~/.claude/.env.global`. If not found, inform the user:

```
This skill requires an Apollo.io API key. Set it via:
  export APOLLO_API_KEY=your_key_here
Or add it to ~/.claude/.env.global

Get your API key at: https://app.apollo.io/#/settings/integrations/api
```

## API Reference

Base URL: `https://api.apollo.io`
Auth: `X-Api-Key` header or `api_key` query parameter.
Rate limit: ~600 requests/hour (varies by plan).

### People Search

Find prospects by role, company, location, and more:

```bash
curl -s -X POST "https://api.apollo.io/api/v1/mixed_people/search" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${APOLLO_API_KEY}" \
  -d '{
    "q_keywords": "vp marketing",
    "person_titles": ["VP Marketing", "Head of Marketing", "CMO"],
    "organization_num_employees_ranges": ["51,200"],
    "person_locations": ["United States"],
    "page": 1,
    "per_page": 10
  }'
```

**Useful filters:**
- `q_keywords` - Keyword search across name, title, company
- `person_titles` - Array of job titles
- `person_locations` - Array of locations
- `organization_industry_tag_ids` - Industry filter
- `organization_num_employees_ranges` - Employee count (e.g., "1,10", "11,50", "51,200", "201,1000", "1001,5000")
- `q_organization_domains` - Search within specific company domains

### Organization Enrichment

Get detailed company info from a domain:

```bash
curl -s -X POST "https://api.apollo.io/api/v1/organizations/enrich" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${APOLLO_API_KEY}" \
  -d '{"domain": "example.com"}'
```

Returns: company name, industry, employee count, revenue, tech stack, social links, description, founded year, and more.

### Bulk Organization Lookup

```bash
curl -s -X POST "https://api.apollo.io/api/v1/organizations/bulk_enrich" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${APOLLO_API_KEY}" \
  -d '{"domains": ["example.com", "company2.com", "company3.com"]}'
```

### People Enrichment

Enrich a contact by email:

```bash
curl -s -X POST "https://api.apollo.io/api/v1/people/match" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${APOLLO_API_KEY}" \
  -d '{
    "email": "john@example.com",
    "reveal_personal_emails": false,
    "reveal_phone_number": false
  }'
```

## Lead Research Process

### Step 1: Define ICP (Ideal Customer Profile)

Ask or infer:
- **Target titles:** What roles are you selling to?
- **Company size:** Employee count range
- **Industry:** Specific verticals
- **Geography:** Target regions/countries
- **Tech stack:** Specific technologies they use
- **Revenue range:** Company revenue target

### Step 2: Build Search Query

Translate ICP into Apollo search filters. Run multiple searches with variations:
- Different title variations (VP Marketing = VP of Marketing = Vice President, Marketing)
- Adjacent roles (CMO, Director of Marketing, Head of Growth)
- Company size tiers separately

### Step 3: Enrich Results

For each prospect found:
1. Note their current title, company, and location
2. Enrich their company domain for additional context
3. Look for mutual connections or shared background

### Step 4: Qualify & Prioritize

Score leads on:

| Factor | Weight | Criteria |
|--------|--------|----------|
| Title match | 30% | Exact title vs. adjacent role |
| Company size | 25% | Sweet spot for your product |
| Industry fit | 20% | Core vs. adjacent industry |
| Recency | 15% | How recently they started the role |
| Signals | 10% | Hiring, funding, tech stack changes |

### Step 5: Output Lead List

Format results as:

```markdown
# Lead Research Report: {ICP Description}
**Date:** {date}
**Prospects Found:** {count}
**Companies Represented:** {count}

## Top Prospects

| # | Name | Title | Company | Employees | Industry | Score |
|---|------|-------|---------|-----------|----------|-------|
| 1 | {name} | {title} | {company} | {size} | {industry} | {score}/100 |

## Company Insights

### {Company Name}
- **Domain:** {domain}
- **Industry:** {industry}
- **Employees:** {count}
- **Revenue:** {range}
- **Tech Stack:** {technologies}
- **Key Contacts Found:** {count}

## Outreach Recommendations

### Personalization Angles
1. {Specific angle based on company data}
2. {Specific angle based on role/industry}

### Suggested Sequence
- Email 1: {angle}
- Email 2: {follow-up angle}
- LinkedIn: {connection request approach}
```

## Important Notes

- Apollo rate limits are strict (~600/hour). Batch requests and cache results.
- Some endpoints require a paid plan. Handle 403 responses gracefully.
- Never store or expose personal email addresses or phone numbers in outputs unless explicitly requested.
- Respect opt-out lists and GDPR/CAN-SPAM compliance.
- Use enrichment data for personalization, not for unsolicited spam.
