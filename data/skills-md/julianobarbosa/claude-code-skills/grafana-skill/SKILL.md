---
name: grafana-skill
description: Comprehensive skill for interacting with Grafana's HTTP API to manage dashboards, data sources, folders, alerting, annotations, users, teams, and organizations. Use when Claude needs to (1) Create, read, update, or delete Grafana dashboards, (2) Manage data sources and connections, (3) Configure alerting rules, contact points, and notification policies, (4) Work with folders and permissions, (5) Manage users, teams, and service accounts, (6) Create or query annotations, (7) Execute queries against data sources, or any other Grafana automation task via API.
---

# grafana-skill

Programmatically manage Grafana resources using TypeScript tools and HTTP API workflows.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **DashboardCrud** | "create dashboard", "update dashboard", "delete dashboard", "list dashboards", "export dashboard" | `Tools/DashboardCrud.ts` |
| **GrafanaClient** | "grafana API", "grafana client", "TypeScript grafana" | `Tools/GrafanaClient.ts` |
| **ApiReference** | "grafana API reference", "grafana endpoints" | `References/` |

## Tools

### DashboardCrud CLI

```bash
# Set environment variables
export GRAFANA_URL="https://grafana.example.com"
export GRAFANA_TOKEN="your-service-account-token"

# List dashboards
bun run Tools/DashboardCrud.ts list
bun run Tools/DashboardCrud.ts list --query production --tag monitoring

# Get dashboard by UID
bun run Tools/DashboardCrud.ts get abc123

# Export dashboard to JSON
bun run Tools/DashboardCrud.ts export abc123 --output dashboard.json

# Create dashboard from JSON file
bun run Tools/DashboardCrud.ts create --file dashboard.json --folder my-folder

# Update dashboard
bun run Tools/DashboardCrud.ts update abc123 --file updated.json --message "Updated panels"

# Clone dashboard
bun run Tools/DashboardCrud.ts clone abc123 --title "Production Copy" --folder prod-folder

# View version history
bun run Tools/DashboardCrud.ts versions abc123

# Restore to previous version
bun run Tools/DashboardCrud.ts restore abc123 --version 5

# Delete dashboard
bun run Tools/DashboardCrud.ts delete abc123
```

### GrafanaClient TypeScript Library

```typescript
import { GrafanaClient, createGrafanaClient } from './Tools/GrafanaClient';

// Initialize from environment variables
const client = createGrafanaClient();

// Or with explicit config
const client = new GrafanaClient({
  baseUrl: 'https://grafana.example.com',
  token: 'your-service-account-token',
  orgId: 1, // optional
});

// Dashboard operations
const dashboards = await client.searchDashboards({ query: 'production', tag: 'monitoring' });
const dashboard = await client.getDashboardByUid('abc123');
const saved = await client.saveDashboard({ dashboard: myDashboard, folderUid: 'folder-uid' });
await client.deleteDashboard('abc123');

// Version management
const versions = await client.getDashboardVersions('abc123');
await client.restoreDashboardVersion('abc123', 5);

// Folders, Data sources, Alerting, Annotations also available
```

## Authentication

```bash
# Service Account Token (Recommended)
export GRAFANA_TOKEN="glsa_xxxxxxxxxxxxxxxxxxxx"

# Multi-Organization Header
curl -H "Authorization: Bearer $GRAFANA_TOKEN" \
     -H "X-Grafana-Org-Id: 2" \
     https://grafana.example.com/api/org
```

## Quick API Reference

| Resource | List | Get | Create | Update | Delete |
|----------|------|-----|--------|--------|--------|
| Dashboards | `GET /api/search` | `GET /api/dashboards/uid/:uid` | `POST /api/dashboards/db` | `POST /api/dashboards/db` | `DELETE /api/dashboards/uid/:uid` |
| Folders | `GET /api/folders` | `GET /api/folders/:uid` | `POST /api/folders` | `PUT /api/folders/:uid` | `DELETE /api/folders/:uid` |
| Data Sources | `GET /api/datasources` | `GET /api/datasources/uid/:uid` | `POST /api/datasources` | `PUT /api/datasources/uid/:uid` | `DELETE /api/datasources/uid/:uid` |
| Alert Rules | `GET /api/v1/provisioning/alert-rules` | `GET /api/v1/provisioning/alert-rules/:uid` | `POST /api/v1/provisioning/alert-rules` | `PUT /api/v1/provisioning/alert-rules/:uid` | `DELETE /api/v1/provisioning/alert-rules/:uid` |

## Reference Documentation

- **[Dashboards](References/Dashboards.md)**: Complete dashboard CRUD, versions, permissions
- **[DataSources](References/DataSources.md)**: Data source management, queries, health checks
- **[Alerting](References/Alerting.md)**: Alert rules, contact points, notification policies
- **[Folders](References/Folders.md)**: Folder management and permissions
- **[Annotations](References/Annotations.md)**: Create, query, update annotations
- **[UsersTeams](References/UsersTeams.md)**: User management, team operations
- **[CommonPatterns](References/CommonPatterns.md)**: Error handling, pagination, utilities

## Examples

**Example 1: List and export dashboards**
```
User: "List all production dashboards and export them"
→ bun run Tools/DashboardCrud.ts list --tag production
→ For each: bun run Tools/DashboardCrud.ts export <uid>
→ Returns list of exported JSON files
```

**Example 2: Create dashboard from JSON**
```
User: "Create a new dashboard from this JSON file"
→ bun run Tools/DashboardCrud.ts create --file dashboard.json --folder monitoring
→ Returns new dashboard UID and URL
```

**Example 3: Clone dashboard to another folder**
```
User: "Clone the CPU dashboard to the production folder"
→ bun run Tools/DashboardCrud.ts clone cpu-uid --title "CPU Prod" --folder prod-folder
→ Returns cloned dashboard details
```

**Example 4: Restore dashboard version**
```
User: "Restore dashboard abc123 to version 5"
→ bun run Tools/DashboardCrud.ts versions abc123
→ bun run Tools/DashboardCrud.ts restore abc123 --version 5
→ Dashboard restored, new version created
```

**Example 5: Programmatic bulk update**
```typescript
User: "Write TypeScript to bulk update dashboard tags"
→ Uses GrafanaClient library:
   const client = createGrafanaClient();
   const dashboards = await client.searchDashboards({ tag: 'old-tag' });
   for (const dash of dashboards) {
     const full = await client.getDashboardByUid(dash.uid);
     full.dashboard.tags = full.dashboard.tags.filter(t => t !== 'old-tag');
     full.dashboard.tags.push('new-tag');
     await client.saveDashboard({ dashboard: full.dashboard, message: 'Updated tags' });
   }
```

## Error Handling

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad request (invalid JSON, missing required fields) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not found |
| 409 | Conflict (resource already exists) |
| 412 | Precondition failed (version mismatch) |

## Tips

1. **Use UIDs over IDs**: UIDs are portable across Grafana instances
2. **Include version for updates**: Prevents overwriting concurrent changes
3. **Use `overwrite: true` carefully**: Only when you want to force-update
4. **Service accounts over API keys**: API keys are deprecated in newer Grafana versions
