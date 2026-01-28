---
name: freeagent-api
description: Interacts with the FreeAgent accounting API to manage invoices, contacts, projects, expenses, timeslips, and other financial data. Use when the user needs to retrieve, create, update, or analyze FreeAgent accounting information via the API.
allowed-tools: Bash, Read, Write, Edit, WebFetch
version: 2.0
---

# FreeAgent API Orchestration Skill

FreeAgent is an online accounting system for freelancers and small businesses. This skill provides intelligent navigation to FreeAgent API resources and orchestrates common workflows.

## Quick Reference: Which Resource Do I Need?

| Task | Load Resource | API Domains |
|------|---------------|-------------|
| Set up OAuth, manage tokens, test API | `resources/authentication-setup.md` | OAuth 2.0, token management |
| Create/update contacts, manage clients/suppliers | `resources/contacts-organizations.md` | Contacts, companies, users |
| Manage invoices, projects, expenses, timeslips | `resources/accounting-objects.md` | Core financial entities |
| Bank accounts, transactions, reconciliation | `resources/banking-financial.md` | Banking, cash flow |
| Error handling, rate limits, retries, caching | `resources/advanced-patterns.md` | Production patterns |
| Common workflows, code examples, integration tips | `resources/examples.md` | Real-world usage |
| All endpoints (reference only) | `resources/endpoints.md` | Complete API reference |

## Orchestration Protocol

### Phase 1: Task Analysis

Identify what the user needs:

**By Resource Type:**
- **Authentication issue?** → `authentication-setup.md`
- **Managing contacts/clients?** → `contacts-organizations.md`
- **Financial data (invoices, expenses, projects)?** → `accounting-objects.md`
- **Banking/reconciliation?** → `banking-financial.md`
- **Error or production concern?** → `advanced-patterns.md`
- **Practical example needed?** → `examples.md`

**By HTTP Method:**
- GET: List or retrieve → check relevant domain resource
- POST: Create → load resource file, check required fields
- PUT: Update → load resource file, verify patch fields
- DELETE: Remove → check resource-specific constraints

### Phase 2: Resource Navigation

Load the appropriate resource file and:
1. Find the endpoint section (e.g., "Contacts", "Invoices", "Bank Accounts")
2. Review required/optional parameters
3. Check request and response formats
4. Use provided curl or Python examples

For template code: `templates/api-request-template.sh` (bash) or `templates/python-client.py` (Python)

### Phase 3: Execution & Validation

**Before API call:**
- Verify authentication is set up (check `authentication-setup.md` if needed)
- Validate required fields are present
- Format dates as ISO 8601 (YYYY-MM-DD) and timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Use correct resource URLs (e.g., `https://api.freeagent.com/v2/contacts/123`)

**During API call:**
- Use templates as starting points
- Monitor rate limit headers: `X-RateLimit-Remaining`
- Implement retry logic for 429 errors (see `advanced-patterns.md`)

**After API call:**
- Check response status code
- Parse JSON response (resource name is top-level key)
- Apply error handling patterns if needed

## Quick Start: Authentication

1. Create OAuth app: https://dev.freeagent.com/
2. Get authorization code: `https://api.freeagent.com/v2/approve_app?client_id=YOUR_ID`
3. Exchange for tokens at `https://api.freeagent.com/v2/token_endpoint`
4. Store in environment variables: `FREEAGENT_ACCESS_TOKEN`, `FREEAGENT_REFRESH_TOKEN`
5. Include in every request: `Authorization: Bearer $FREEAGENT_ACCESS_TOKEN`

→ See [Authentication & Setup](resources/authentication-setup.md) for detailed walkthrough

## API Domain Overview

**Production URL:** `https://api.freeagent.com/v2/`
**Sandbox URL:** `https://api.sandbox.freeagent.com/v2/` (test without affecting production)

| Domain | Primary Endpoints | Use Case |
|--------|------------------|----------|
| **Authentication** | `/token_endpoint` | OAuth flows, token refresh |
| **Contacts & Organizations** | `/contacts`, `/company`, `/users` | Client/supplier management |
| **Accounting Objects** | `/invoices`, `/projects`, `/expenses`, `/timeslips`, `/estimates`, `/credit_notes` | Core financial workflow |
| **Banking & Financial** | `/bank_accounts`, `/bank_transactions`, `/categories`, `/tasks` | Cash flow, reconciliation |

**Rate Limits:** 120 requests/minute, 3600 requests/hour
**Response Format:** JSON with resource wrapper (e.g., `{"contact": {...}}` or `{"contacts": [...]}`)

## Common HTTP Patterns

| Operation | Method | Example |
|-----------|--------|---------|
| List items | GET | `GET /v2/contacts?view=active&page=1&per_page=100` |
| Get one item | GET | `GET /v2/contacts/123` |
| Create item | POST | `POST /v2/contacts` (with JSON body) |
| Update item | PUT | `PUT /v2/invoices/456` (with partial JSON) |
| Delete item | DELETE | `DELETE /v2/timeslips/789` |
| Filter results | GET params | `?view=open_or_overdue`, `?updated_since=2025-01-01T00:00:00Z` |

## Templates & Code Examples

**Bash/cURL Template:** `templates/api-request-template.sh`
- Flexible curl template for any endpoint
- GET/POST/PUT/DELETE support
- Header and parameter configuration

**Python Client:** `templates/python-client.py`
- Reusable FreeAgentClient class
- Error handling and rate limit support
- Convenience methods for common resources

**Practical Examples:** `resources/examples.md`
- Real-world workflows (create invoice, log timeslip, etc.)
- Python code patterns with the client class
- Error handling examples
- Bulk operations (import/export)

## Resource Files Summary

| File | Lines | Focus |
|------|-------|-------|
| `authentication-setup.md` | ~180 | OAuth setup, token management, security |
| `contacts-organizations.md` | ~250 | Contact CRUD, bulk operations, company info |
| `accounting-objects.md` | ~350 | Invoices, projects, expenses, timeslips, pagination |
| `banking-financial.md` | ~250 | Bank accounts, transactions, reconciliation, categories |
| `advanced-patterns.md` | ~350 | Error handling, rate limits, retries, caching, validation |
| `examples.md` | ~400 | Practical code examples, integration patterns |
| `endpoints.md` | ~300 | Complete API reference (use for quick lookup) |

## Troubleshooting Quick Links

**401 Unauthorized** → [Authentication Setup](resources/authentication-setup.md#troubleshooting)
**422 Validation Error** → [Advanced Patterns](resources/advanced-patterns.md#validation-patterns)
**429 Rate Limit** → [Advanced Patterns](resources/advanced-patterns.md#rate-limiting)
**Specific Endpoint Help** → Check relevant domain resource file above

---

**Remember:** Load only the resource file(s) you need for the current task. Start with the Quick Reference table above to identify which resource contains your answer.
