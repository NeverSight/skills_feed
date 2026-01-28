---
name: bloomerang-api
description: Bloomerang CRM API integration reference for building donor management features. Use when writing code that interacts with the Bloomerang API, including fetchers, normalizers, or any backend integration with Bloomerang donor data. Covers Constituents, Transactions, Pledges, Campaigns, Appeals, Interactions, Tasks, and Relationships.
---

# Bloomerang API

Reference for integrating with the Bloomerang CRM REST API (OpenAPI 3.0, v2.0.0).

## Base URL

```
https://api.bloomerang.co/v2
```

## Authentication

**API Key (recommended for integrations):**
```
X-API-KEY: <your-api-key>
```

**OAuth 2.0 (for user-based interactions):**
- Authorization URL: `https://crm.bloomerang.com/authorize/`
- Token URL: `https://api.bloomerang.co/v2/oauth/token`
- Scopes: `ViewOnly`, `StandardEditFinancialData`, `Standard`, `OrgAdmin`

## Pagination

All list endpoints use `skip` and `take` parameters:
- `take`: Max 50 items per request (default)
- `skip`: Offset for pagination
- Response includes `Total`, `TotalFiltered`, `Start`, `ResultCount`

## Key Endpoints

### Constituents (Donors)
```
GET    /constituents                    # List constituents
GET    /constituent/{id}                # Get single constituent
POST   /constituent                     # Create constituent
PUT    /constituent/{id}                # Update constituent
DELETE /constituent/{id}                # Delete constituent
GET    /constituents/search             # Search constituents
GET    /constituent/{id}/timeline       # Get constituent timeline
GET    /constituent/{id}/relationships  # Get relationships
POST   /constituent/merge               # Merge duplicates
```

### Households
```
GET    /households                      # List households
GET    /household/{id}                  # Get household
POST   /household                       # Create household
PUT    /household/{id}                  # Update household
```

### Transactions (Gifts)
```
GET    /transactions                    # List transactions
GET    /transaction/{id}                # Get single transaction
POST   /transaction                     # Create transaction
PUT    /transaction/{id}                # Update transaction
DELETE /transaction/{id}                # Delete transaction
GET    /transactions/designations       # Get designations
```

### Pledges
```
GET    /pledge/{id}/installments        # Get pledge installments
GET    /pledge/{id}/payments            # Get pledge payments
POST   /pledge/generateInstallments     # Generate installments
POST   /pledge/{id}/writeOff            # Write off pledge
```

### Interactions
```
GET    /interactions                    # List interactions
GET    /interaction/{id}                # Get interaction
POST   /interaction                     # Create interaction
PUT    /interaction/{id}                # Update interaction
DELETE /interaction/{id}                # Delete interaction
```

### Campaigns & Appeals
```
GET    /campaigns                       # List campaigns
GET    /campaign/{id}                   # Get campaign
POST   /campaign                        # Create campaign
GET    /appeals                         # List appeals
GET    /appeal/{id}                     # Get appeal
POST   /appeal                          # Create appeal
```

### Tasks
```
GET    /tasks                           # List tasks
GET    /task/{id}                       # Get task
POST   /task                            # Create task
PUT    /task/{id}                       # Update task
POST   /task/{id}/complete              # Complete task
```

### Other Resources
```
GET    /funds                           # List funds
GET    /notes                           # List notes
GET    /refunds                         # List refunds
GET    /softcredits                     # List soft credits
GET    /tributes                        # List tributes
GET    /walletitems                     # List wallet items
GET    /relationshiproles               # List relationship roles
```

## ID vs AccountNumber

Bloomerang distinguishes between:
- **ID**: API identifier (use in API calls)
- **AccountNumber**: UI-friendly reference (displayed to users)

## Full API Reference

For complete endpoint specifications, request/response schemas, and examples, search the OpenAPI spec (do not read the full file - it's 1.5MB):

```
references/bloomerang-openapi.json
```

Search patterns (use grep or jq):
- Endpoints: `jq '.paths | keys'`
- Schemas: `jq '.components.schemas | keys'`
- Specific endpoint: `jq '.paths["/constituent/{id}"]'`

## Disclaimer

This skill is not affiliated with, endorsed by, or sponsored by Bloomerang. It references publicly available API documentation for educational and integration purposes. The information may be outdated or incomplete. Always refer to the official Bloomerang documentation for the most current API specifications.
