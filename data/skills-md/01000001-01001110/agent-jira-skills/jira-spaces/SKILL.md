---
name: jira-spaces
description: Manage Confluence spaces for project documentation. Create, list, and delete spaces with templates. Use when setting up project documentation structure or managing Confluence content areas.
---

# Jira Spaces Skill

Manage Confluence spaces through the Confluence Cloud REST API. Spaces are the top-level containers for organizing project documentation, wikis, and knowledge bases.

## When to Use

- Setting up documentation structure for a new project
- Creating spaces for different teams or initiatives
- Listing available spaces to find documentation
- Archiving or deleting obsolete spaces

## Prerequisites

- Confluence Cloud instance (same Atlassian account as Jira)
- API token with Confluence access
- Environment variables configured in `.env`

## API Reference

### Base URL

Confluence Cloud uses the same base URL as Jira Cloud but different API path:

```
https://your-domain.atlassian.net/wiki/rest/api
```

### Authentication

Same as Jira - Basic Auth with email:token.

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/space` | GET | List all spaces |
| `/space` | POST | Create a new space |
| `/space/{spaceKey}` | GET | Get space details |
| `/space/{spaceKey}` | DELETE | Delete a space |
| `/space/{spaceKey}/content` | GET | List space content |

## Space Types

| Type | Description | Use Case |
|------|-------------|----------|
| `global` | Site-wide space | Company wikis, shared docs |
| `personal` | User's personal space | Individual notes, drafts |

## Creating a Space

### Request

```typescript
const response = await fetch(`${CONFLUENCE_URL}/wiki/rest/api/space`, {
  method: 'POST',
  headers: {
    'Authorization': `Basic ${auth}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    key: 'PROJ',           // Unique space key (uppercase)
    name: 'Project Docs',   // Display name
    type: 'global',         // 'global' or 'personal'
    description: {
      plain: {
        value: 'Documentation for the project',
        representation: 'plain'
      }
    }
  })
});
```

### Response

```json
{
  "id": 12345,
  "key": "PROJ",
  "name": "Project Docs",
  "type": "global",
  "status": "current",
  "_links": {
    "webui": "/spaces/PROJ",
    "self": "https://your-domain.atlassian.net/wiki/rest/api/space/PROJ"
  }
}
```

## Listing Spaces

### Request

```typescript
const response = await fetch(`${CONFLUENCE_URL}/wiki/rest/api/space?limit=25&type=global`, {
  headers: {
    'Authorization': `Basic ${auth}`,
    'Accept': 'application/json'
  }
});
```

### Response

```json
{
  "results": [
    {
      "id": 12345,
      "key": "PROJ",
      "name": "Project Docs",
      "type": "global",
      "status": "current"
    }
  ],
  "start": 0,
  "limit": 25,
  "size": 1,
  "_links": {}
}
```

## Deleting a Space

**WARNING**: Deleting a space removes all pages and content permanently!

### Request

```typescript
const response = await fetch(`${CONFLUENCE_URL}/wiki/rest/api/space/PROJ`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Basic ${auth}`
  }
});
```

Returns 202 Accepted (deletion is async) or 204 No Content.

## Space Keys

Space keys must:
- Be unique across the Confluence instance
- Use only uppercase letters and numbers
- Be 1-255 characters
- Not start with a number

Conventions:
- `PROJ` - Project-specific
- `TEAM` - Team-specific
- `DOC` - Documentation
- `KB` - Knowledge base

## Common Patterns

### Create Project Documentation Space

```typescript
// Create space with home page
await createSpace({
  key: 'TUSTLE',
  name: 'Tustle Project Documentation',
  description: 'Technical documentation and guides for Tustle MVP'
});

// Add standard pages
await createPage('TUSTLE', 'Getting Started', 'Overview and setup instructions...');
await createPage('TUSTLE', 'Architecture', 'System architecture documentation...');
await createPage('TUSTLE', 'API Reference', 'API endpoint documentation...');
```

### List Team Spaces

```typescript
const spaces = await listSpaces({ type: 'global', limit: 50 });
const teamSpaces = spaces.filter(s => s.name.includes('Team'));
```

## Error Handling

| Status | Meaning | Resolution |
|--------|---------|------------|
| 400 | Invalid space key | Check key format (uppercase, no special chars) |
| 401 | Unauthorized | Check API token and email |
| 403 | Forbidden | User lacks space admin permissions |
| 404 | Space not found | Verify space key exists |
| 409 | Conflict | Space key already exists |

## Scripts

| Script | Description |
|--------|-------------|
| `create-space` | Create a new Confluence space |
| `delete-space` | Delete a space (with confirmation) |
| `list-spaces` | List all accessible spaces |

## Usage Examples

```bash
# List all spaces
node run.js list-spaces

# Create a new space
node run.js create-space DOCS "Documentation Space"

# Delete a space (interactive confirmation)
node run.js delete-space DOCS

# Force delete without confirmation
node run.js delete-space DOCS --confirm
```

## Related Skills

- `jira-projects` - Jira project management
- `jira-issues` - Issue creation for documentation tasks
