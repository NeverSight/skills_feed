---
name: leadgenius-api
description: Comprehensive toolset for interacting with LeadGenius Pro Agent APIs. Use for managing ABM campaigns, lead lifecycle, AI enrichment, target accounts, outreach sequences, and system integrations. Supports listing, creating, and updating resources via the LeadGenius RESTful API.
---

# LeadGenius Pro Agent API

This skill provides a comprehensive interface for interacting with the LeadGenius Pro Agent API.

## Core Workflows

### 1. Lead Management
- **Bulk List (EnrichLeads)**: Use `GET /enrich-leads/list` for high-volume data extraction from the enriched leads table (requires Amplify API key).
- **Bulk List (SourceLeads)**: Use `GET /source-leads/list` for raw source data extraction (requires Amplify API key).
- **Update Status**: Use `PUT /leads/{id}/status` to track progress (New -> Qualified -> Contacted).
- **Batch Operations**: Create or delete multiple leads simultaneously with `POST /leads/batch` or `DELETE /leads/batch`.

### 2. Campaign Operations
- **Overview**: List all active ABM campaigns with `GET /campaigns`.
- **Performance**: Monitor ROI with `GET /campaigns/{id}/metrics`.
- **Creation**: Launch new initiatives with `POST /campaigns`.

### 3. Targeted ABM
- **Account Lists**: Manage high-value targets with `GET /target-accounts`.
- **Scoring**: Update account intent and fit scores with `PUT /target-accounts/{id}/score`.

### 4. Outreach & Engagement
- **Sequences**: List communication sequences with `GET /sequences`.
- **Enrollment**: Enroll leads into a specific sequence with `POST /sequences/{id}/enroll`.

### 5. Automation & Workflows
- **Custom Workflows**: Manage automated processes and agent handoffs with `GET /workflows`.
- **Status Jobs**: Monitor long-running processes (like enrichment or exports) with `GET /enrichment/status/{jobId}`.

### 6. Analytics & Insights
- **Pipeline Health**: Total visibility into conversion rates and pipeline velocity with `GET /analytics/pipeline`.

### 7. Maintenance & System Health
- **Bug Reporting**: Use `POST /maintenance/bugs` to report issues discovered by agents.
- **Enhancement Requests**: Use `POST /maintenance/enhancements` to suggest features.

### 8. Master Administration
- **Global Visibility**: List all companies and users across the platform (Admin only).
- **API Key Management**: Generate and rotate API keys for agent access.

## Technical Reference

### Base URLs
The API uses separate root paths depending on the operation scope. Standard agent interaction occurs via the **Agent Scope**, while high-volume extraction uses the **System Scope**.

1. **Agent API Operations**: `/api/agent` (e.g., `https://last.leadgenius.app/api/agent/leads`). Requires `X-API-Key` (lgp_...).
2. **Bulk Data Extraction (System Scope)**: `/api` (e.g., `https://last.leadgenius.app/api/enrich-leads/list`). Requires `x-api-key` (Amplify API key).
3. **Admin Scope**: `/api/admin` (e.g., `.../api/admin/companies`).

### Unified CLI (lgp.py)
The primary way to interact with LeadGenius is via the `lgp` CLI tool.

#### 1. Setup & Auth
Authentication is a two-step process:
1. **Login**: Authenticate with your email and password to get a temporary session (JWTokens are stored).
2. **Generate Key**: Create a long-lived API Key (`lgp_...`) for your scripts/agent using the session.

```bash
# 1. Login to get session (email/password)
python3 scripts/lgp.py auth --email your@email.com

# 2. Generate an API Key (this will be automatically saved)
python3 scripts/lgp.py generate-key --name "Production Agent"
```

Once generated, the key is saved to `~/.leadgenius_auth.json` and will be automatically used by the CLI. You can also explicitly set it via `LGP_API_KEY` environment variable.

#### 2. Manage Leads
```bash
# List leads
python3 scripts/lgp.py leads list

# Find specific leads
python3 scripts/lgp.py leads find --full-name "Hugo Sanchez"

# Enrich specific leads
python3 scripts/lgp.py leads enrich --ids lead_1 lead_2
```

#### 3. Manage Campaigns
```bash
# List active campaigns
python3 scripts/lgp.py campaigns list

# Create a new campaign
python3 scripts/lgp.py campaigns create --name "Q3 Expansion"
```

#### 4. Insights & Analytics
```bash
# Show pipeline health for a specific period
python3 scripts/lgp.py pipeline --start 2026-01-01 --end 2026-02-08
```

#### 5. Maintenance & Support
```bash
# List and report bugs
python3 scripts/lgp.py maintenance bugs list
python3 scripts/lgp.py maintenance bugs report --desc "Enrichment fails on LinkedIn URLs"

# List and request enhancements
python3 scripts/lgp.py maintenance enhancements list
python3 scripts/lgp.py maintenance enhancements request --desc "Add support for Google Maps leads"
```

#### 6. Global Administration (Admin Only)
```bash
# View system-wide data
python3 scripts/lgp.py admin companies
python3 scripts/lgp.py admin users
```

### Reference Material
- **API Reference**: See [api_reference.md](references/api_reference.md) for detailed endpoint descriptions.
- **OpenAPI Spec**: See [openapi.json](references/openapi.json) for machine-readable schemas.

### Helper Scripts
- **[scripts/lgp.py](scripts/lgp.py)**: Unified CLI for all common operations.
- **[scripts/api_call.py](scripts/api_call.py)**: Low-level utility for custom raw API requests.
- **[scripts/auth.py](scripts/auth.py)**: Standalone auth utility.



## Common Payloads

### Create Campaign
```json
{
  "name": "Q1 ABM Tech Giants",
  "description": "Targeting top 50 tech firms for SaaS expansion",
  "campaignType": "abm",
  "status": "active"
}
```

### Enrich Leads
```json
{
  "leadIds": ["lead_123", "lead_456"],
  "enrichmentType": "technographic",
  "priority": "high"
}
```




## Data Architecture & Logic
### 1. Multi-Tenant Isolation
All data is strictly isolated by `company_id`. Even though agents use their own API keys, the system enforces that they only see leads associated with their assigned `company_id`.

### 2. Search Logic (LeadService)
The standard lead listing (`GET /leads`) uses a dual-query strategy to ensure no leads are missed:
- **By Company**: Queries the `company_id-GSI` to find all company-level leads.
- **By Owner**: Queries the `owner-GSI` to find leads specifically created by/assigned to the agent.
- **Merging**: Results are deduplicated and merged to provide a unified view.

### 3. Bulk Data Access
High-volume extraction (`GET /enrich-leads/list`) bypasses standard CRM logic in favor of raw GSI performance, requiring an explicit `companyId` parameter and matching Amplify API key.

### 4. Guardrails & Limits
- **Rate Limits**: 
  - **Minute**: 60 requests.
  - **Hour**: 1,000 requests.
  - **Day**: 10,000 requests.
- **Batching**: 
  - **Lead Creation**: Max 100 leads per request.
  - **Enrichment Trigger**: Max 500 leads per request.
- **Pagination**:
  - **Standard API**: Default 20, Max 100 per page.
  - **Bulk API**: Default 1,000, Max 5,000 per page.
- **Search Depth**: LeadService scans up to 1,000 records per GSI before in-memory merging.

