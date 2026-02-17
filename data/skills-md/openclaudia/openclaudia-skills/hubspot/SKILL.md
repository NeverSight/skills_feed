---
name: hubspot
description: Manage HubSpot CRM contacts, companies, deals, and CMS content via API. Use when the user says "add contact to HubSpot", "create deal", "search CRM", "HubSpot contacts", "update deal stage", "CRM report", "HubSpot pages", or asks about managing their sales pipeline, CRM data, or HubSpot content.
---

# HubSpot CRM & CMS Skill

You are a HubSpot CRM and CMS automation expert. Use the HubSpot API to manage contacts, companies, deals, owners, associations, properties, CMS pages, and files.

## Prerequisites

This skill requires `HUBSPOT_ACCESS_TOKEN` (Private App token). Check for it in environment variables or `~/.claude/.env.global`. If not found, inform the user:

```
This skill requires a HubSpot Private App access token. Set it via:
  export HUBSPOT_ACCESS_TOKEN=your_token_here
Or add it to ~/.claude/.env.global

Create a Private App at: Settings > Integrations > Private Apps
Required scopes: crm.objects.contacts, crm.objects.companies, crm.objects.deals, content
```

## API Reference

Base URL: `https://api.hubapi.com`
Auth header: `Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}`
Rate limit: 100 requests per 10 seconds for private apps.

### Contacts

**List contacts:**
```bash
curl -s "https://api.hubapi.com/crm/v3/objects/contacts?limit=10&properties=firstname,lastname,email,company,phone" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

**Search contacts:**
```bash
curl -s -X POST "https://api.hubapi.com/crm/v3/objects/contacts/search" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "filterGroups": [{
      "filters": [{
        "propertyName": "email",
        "operator": "CONTAINS_TOKEN",
        "value": "example.com"
      }]
    }],
    "properties": ["firstname", "lastname", "email", "company"],
    "limit": 10
  }'
```

**Create contact:**
```bash
curl -s -X POST "https://api.hubapi.com/crm/v3/objects/contacts" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "firstname": "John",
      "lastname": "Doe",
      "email": "john@example.com",
      "company": "Acme Inc",
      "phone": "+1234567890"
    }
  }'
```

**Get contact by email:**
```bash
curl -s -X POST "https://api.hubapi.com/crm/v3/objects/contacts/search" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "filterGroups": [{
      "filters": [{
        "propertyName": "email",
        "operator": "EQ",
        "value": "john@example.com"
      }]
    }],
    "properties": ["firstname", "lastname", "email", "company", "phone", "lifecyclestage"]
  }'
```

### Companies

**List companies:**
```bash
curl -s "https://api.hubapi.com/crm/v3/objects/companies?limit=10&properties=name,domain,industry,numberofemployees" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

**Search companies by domain:**
```bash
curl -s -X POST "https://api.hubapi.com/crm/v3/objects/companies/search" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "filterGroups": [{
      "filters": [{
        "propertyName": "domain",
        "operator": "EQ",
        "value": "example.com"
      }]
    }],
    "properties": ["name", "domain", "industry", "numberofemployees", "annualrevenue"]
  }'
```

### Deals

**Create deal:**
```bash
curl -s -X POST "https://api.hubapi.com/crm/v3/objects/deals" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "dealname": "New Enterprise Deal",
      "dealstage": "appointmentscheduled",
      "pipeline": "default",
      "amount": "50000",
      "closedate": "2026-06-30"
    }
  }'
```

**List deals:**
```bash
curl -s "https://api.hubapi.com/crm/v3/objects/deals?limit=10&properties=dealname,dealstage,amount,closedate,pipeline" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

**Update deal stage:**
```bash
curl -s -X PATCH "https://api.hubapi.com/crm/v3/objects/deals/{dealId}" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"dealstage": "closedwon"}}'
```

### Owners

**List owners (sales reps):**
```bash
curl -s "https://api.hubapi.com/crm/v3/owners/" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

### Associations

Associate contacts with companies or deals:

```bash
# Associate deal with contact (type 3)
curl -s -X PUT "https://api.hubapi.com/crm/v3/objects/deals/{dealId}/associations/contacts/{contactId}/3" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"

# Associate deal with company (type 5)
curl -s -X PUT "https://api.hubapi.com/crm/v3/objects/deals/{dealId}/associations/companies/{companyId}/5" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"

# Associate contact with company (type 1)
curl -s -X PUT "https://api.hubapi.com/crm/v3/objects/contacts/{contactId}/associations/companies/{companyId}/1" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

**Get associated contacts for a deal:**
```bash
curl -s "https://api.hubapi.com/crm/v3/objects/deals/{dealId}/associations/contacts" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

### Properties

**List all contact properties:**
```bash
curl -s "https://api.hubapi.com/crm/v3/properties/contacts" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

### CMS Pages

**List site pages:**
```bash
curl -s "https://api.hubapi.com/cms/v3/pages/site-pages?limit=10" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

**List landing pages:**
```bash
curl -s "https://api.hubapi.com/cms/v3/pages/landing-pages?limit=10" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

### Search Operators

| Operator | Description |
|----------|-------------|
| `EQ` | Equal to |
| `NEQ` | Not equal to |
| `LT` / `LTE` | Less than / Less than or equal |
| `GT` / `GTE` | Greater than / Greater than or equal |
| `CONTAINS_TOKEN` | Contains word |
| `NOT_CONTAINS_TOKEN` | Does not contain word |
| `HAS_PROPERTY` | Property exists |
| `NOT_HAS_PROPERTY` | Property does not exist |

### Pagination

All list endpoints support pagination via the `after` parameter:
```bash
curl -s "https://api.hubapi.com/crm/v3/objects/contacts?limit=100&after={next_cursor}" \
  -H "Authorization: Bearer ${HUBSPOT_ACCESS_TOKEN}"
```

The `after` value comes from `paging.next.after` in the response.

## Common Workflows

### Pipeline Report
1. List all deals with `dealstage`, `amount`, `closedate`
2. Group by stage
3. Sum amounts per stage
4. Present as pipeline summary table

### Contact Enrichment
1. Search contacts missing key properties (`NOT_HAS_PROPERTY`)
2. For each, check if company domain exists
3. Pull company data and update contact

### Deal Health Check
1. List deals in active stages
2. Flag deals with no activity in 14+ days
3. Flag deals past expected close date
4. Present prioritized action list

## Important Notes

- Always use pagination for large datasets. Default limit is 10, max is 100.
- HubSpot property names are lowercase with no spaces (e.g., `firstname`, `dealstage`, `closedate`).
- Deal stages vary by pipeline. List pipeline stages via the Pipelines API if needed.
- Rate limit: 100 requests per 10 seconds. Batch operations when possible.
