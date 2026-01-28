---
name: microsoft-graph
description: Orchestration hub for Microsoft Graph API across Microsoft 365 services. Use for Graph API integrations, querying Microsoft 365 data, and building applications that interact with Azure AD.
version: 2.1
---

# Microsoft Graph API Orchestration Skill

Microsoft Graph is a unified REST API endpoint for accessing Microsoft Cloud resources across Microsoft 365, Windows, and Enterprise Mobility + Security. Base URL: `https://graph.microsoft.com/{version}/{resource}`

**API Versions:** `v1.0` (production) or `beta` (preview)  
**Authentication:** OAuth 2.0 via Azure AD  
**Data Format:** JSON

## When to Load Which Resource

| Task | Service | Load Resource |
|------|---------|---------------|
| Setup auth, register apps, manage credentials | Applications & Auth | [resources/authentication-apps.md](resources/authentication-apps.md) |
| Manage users, groups, organization, directory | Identity & Access | [resources/identity-access.md](resources/identity-access.md) |
| Email, folders, attachments, rules, signatures | Mail Operations | [resources/mail-operations.md](resources/mail-operations.md) |
| Calendar, events, scheduling, meetings, free/busy | Calendar & Scheduling | [resources/calendar-scheduling.md](resources/calendar-scheduling.md) |
| Upload files, folders, share, OneDrive, SharePoint | Files & Storage | [resources/files-storage.md](resources/files-storage.md) |
| Teams, channels, chats, presence, online meetings | Teams & Communications | [resources/teams-communications.md](resources/teams-communications.md) |
| Planner tasks, To Do lists, OneNote notebooks | Planning & Notes | [resources/planning-notes.md](resources/planning-notes.md) |
| Security alerts, compliance, device management, reports | Security & Governance | [resources/security-governance.md](resources/security-governance.md) |

## Orchestration Protocol

### Phase 1: Analyze Your Task

Identify which service area you need by answering:
- **What resource?** (users, files, messages, events, etc.)
- **What action?** (read, create, update, delete)
- **Who?** (signed-in user or service account)
- **Permissions?** (delegated or application)

### Phase 2: Load the Right Resource

Use the decision table above to find your resource file. Each resource includes:
- Complete endpoint reference with base paths
- Request/response examples for all CRUD operations
- Query parameters and filter options
- Required permissions (delegated and application)
- Error handling patterns and best practices
- Common workflows and patterns

### Phase 3: Implement with Confidence

Each resource shows practical, copy-paste-ready examples for your use case.

## Universal Graph Concepts

**Standard Query Parameters:**
```
$select=prop1,prop2              Choose properties to return
$filter=startsWith(name,'A')     Filter results by condition
$orderby=name desc               Sort results (asc or desc)
$top=25                          Limit to 25 results (default 20)
$skip=50                         Skip first 50 results
$expand=members                  Include related/nested data
$count=true                      Include total count in response
$search="keyword"                Full-text search across content
```

**Standard CRUD Operations:**
```http
GET /me/messages?$select=subject&$top=10        # Read
POST /me/events {"subject": "Meeting", ...}     # Create
PATCH /users/{id} {"jobTitle": "Manager"}       # Update
DELETE /me/messages/{id}                        # Delete
```

**Pagination:** Always follow `@odata.nextLink` in responses for complete data sets

**Batch Requests:** Use `POST /$batch` to combine 1-20 operations into single call

**Delta Queries:** Use `GET /users/delta` to track changes since last query via `@odata.deltaLink`

**Error Response Format:**
```json
{"error": {"code": "Code", "message": "Description"}}
```

**Common Status Codes:**
- 200/201/204: Success
- 400: Invalid request
- 401: Authentication required
- 403: Insufficient permissions
- 404: Resource not found
- 429: Rate limited (check Retry-After header)
- 500-503: Server error (implement exponential backoff)

## Resource File Index

| File | Focus | Lines |
|------|-------|-------|
| [authentication-apps.md](resources/authentication-apps.md) | App registration, OAuth, credentials | 350+ |
| [identity-access.md](resources/identity-access.md) | Users, groups, organization, directory | 350+ |
| [mail-operations.md](resources/mail-operations.md) | Email, folders, attachments, rules | 400+ |
| [calendar-scheduling.md](resources/calendar-scheduling.md) | Events, recurring, meetings, free/busy | 350+ |
| [files-storage.md](resources/files-storage.md) | OneDrive, SharePoint, uploads, sharing | 400+ |
| [teams-communications.md](resources/teams-communications.md) | Teams, channels, chats, presence | 350+ |
| [planning-notes.md](resources/planning-notes.md) | Planner, To Do, OneNote | 350+ |
| [security-governance.md](resources/security-governance.md) | Security, compliance, devices, reports | 400+ |

## Best Practices

**Performance:** Use `$select` for specific properties, implement pagination, cache tokens, use batch for bulk ops, apply delta queries for sync scenarios

**Security:** Store tokens securely (never in code), request least-privilege permissions, use managed identities for Azure, rotate credentials every 90 days, validate all responses

**Development:** Test in `beta` endpoint first, monitor deprecation notices, implement exponential backoff for retries, respect rate limiting, check Graph health status

**Troubleshooting:**
- 401 Unauthorized → Check token validity and scopes
- 403 Forbidden → Verify permissions are configured in Azure AD
- 404 Not Found → Verify resource ID and that resource exists
- 429 Too Many Requests → Implement retry with exponential backoff

## Tools & SDK Resources

**Interactive Testing:** Graph Explorer at https://developer.microsoft.com/graph/graph-explorer

**SDKs:** 
- .NET: `Microsoft.Graph` NuGet
- JavaScript/TypeScript: `@microsoft/microsoft-graph-client` npm
- Python: `msgraph-sdk-python` pip

**Documentation:**
- API Reference: https://docs.microsoft.com/graph/api/overview
- Permissions Reference: https://docs.microsoft.com/graph/permissions-reference
- Changelog: https://docs.microsoft.com/graph/changelog

---

**Skill Version:** 2.1 | **API Versions:** v1.0 (production), beta (preview) | **Updated:** December 2025
