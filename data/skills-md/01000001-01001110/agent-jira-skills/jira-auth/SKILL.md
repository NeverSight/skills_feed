---
name: jira-auth
description: Authenticate with Jira Cloud REST API using API tokens. Use when setting up Jira connections, validating credentials, or handling rate limiting.
---

# Jira Authentication Skill

## Purpose
Authenticate with Jira Cloud REST API using API tokens or OAuth 2.0. Handle connection setup, credential validation, and rate limiting.

## When to Use
- Setting up Jira API connections
- Validating Jira credentials
- Testing API connectivity
- Managing authentication headers

## Prerequisites
- Jira Cloud instance URL (e.g., `mycompany.atlassian.net`)
- API token (generate at Atlassian account settings)
- Email address associated with the Jira account

## Environment Variables

Create a `.env` file in the jira skill root directory (`.claude/skills/jira/.env`):

```bash
# Required
JIRA_EMAIL=user@example.com
JIRA_API_TOKEN=ATATT3xFfGF0...
JIRA_BASE_URL=https://mycompany.atlassian.net

# Optional (defaults shown)
JIRA_PROJECT_KEY=SCRUM
JIRA_BOARD_ID=1
```

Copy from `.env.example` template:
```bash
cp .env.example .env
# Edit .env with your credentials
```

Get your API token at: https://id.atlassian.com/manage-profile/security/api-tokens

## Test Scripts

Test authentication using the cross-platform runner:

```bash
# From .claude/skills/jira directory
node scripts/run.js test           # Auto-detect runtime
node scripts/run.js --python test  # Force Python
node scripts/run.js --node test    # Force Node.js
```

## Implementation Pattern

### Node.js (ES Modules)

```javascript
// Load from environment variables (set by run.js or manually)
const JIRA_EMAIL = process.env.JIRA_EMAIL;
const JIRA_API_TOKEN = process.env.JIRA_API_TOKEN;
const JIRA_BASE_URL = process.env.JIRA_BASE_URL;
const PROJECT_KEY = process.env.JIRA_PROJECT_KEY || 'SCRUM';

// Validate required env vars
if (!JIRA_EMAIL || !JIRA_API_TOKEN || !JIRA_BASE_URL) {
  console.error('Error: Missing required environment variables.');
  process.exit(1);
}

// Build auth header
const auth = Buffer.from(`${JIRA_EMAIL}:${JIRA_API_TOKEN}`).toString('base64');
const headers = {
  'Authorization': `Basic ${auth}`,
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};
```

### Python

```python
import base64
import os
import sys
from pathlib import Path

# Load .env file from parent directory (jira skill root)
def load_env():
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env()

# Configuration from environment variables
JIRA_EMAIL = os.environ.get('JIRA_EMAIL')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')
JIRA_BASE_URL = os.environ.get('JIRA_BASE_URL')
PROJECT_KEY = os.environ.get('JIRA_PROJECT_KEY', 'SCRUM')

# Validate required env vars
if not all([JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL]):
    print('Error: Missing required environment variables.', file=sys.stderr)
    sys.exit(1)

# Build auth header
auth_string = f'{JIRA_EMAIL}:{JIRA_API_TOKEN}'
auth_bytes = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
HEADERS = {
    'Authorization': f'Basic {auth_bytes}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
```

### TypeScript (Reference Pattern)

```typescript
function buildJiraAuthHeader(email: string, apiToken: string): string {
  const credentials = Buffer.from(`${email}:${apiToken}`).toString('base64');
  return `Basic ${credentials}`;
}
```

### Step 2: Create Jira Client

```typescript
interface JiraConfig {
  baseUrl: string;
  email: string;
  apiToken: string;
}

class JiraClient {
  private baseUrl: string;
  private headers: Record<string, string>;

  constructor(config: JiraConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.headers = {
      'Authorization': buildJiraAuthHeader(config.email, config.apiToken),
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    };
  }

  async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}/rest/api/3${path}`;
    const response = await fetch(url, {
      ...options,
      headers: { ...this.headers, ...options.headers },
    });

    if (response.status === 429) {
      const resetTime = response.headers.get('X-RateLimit-Reset');
      throw new Error(`Rate limited. Reset at: ${resetTime}`);
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`Jira API error: ${response.status} - ${JSON.stringify(error)}`);
    }

    return response.json();
  }
}
```

### Step 3: Validate Connection

```typescript
async function validateJiraConnection(client: JiraClient): Promise<boolean> {
  try {
    const user = await client.request<{ accountId: string; displayName: string }>('/myself');
    console.log(`Connected as: ${user.displayName} (${user.accountId})`);
    return true;
  } catch (error) {
    console.error('Jira connection failed:', error);
    return false;
  }
}
```

## curl Examples

### Test Authentication
```bash
curl -X GET "https://mycompany.atlassian.net/rest/api/3/myself" \
  -H "Authorization: Basic $(echo -n 'email@example.com:API_TOKEN' | base64)" \
  -H "Accept: application/json"
```

### Expected Success Response
```json
{
  "self": "https://mycompany.atlassian.net/rest/api/3/user?accountId=...",
  "accountId": "5e10b8dbf0cab60d71f4a9cd",
  "displayName": "John Doe",
  "active": true,
  "timeZone": "America/New_York"
}
```

## Rate Limiting

| Metric | Limit |
|--------|-------|
| Authenticated requests | 60/minute |
| Unauthenticated requests | 20/minute |

### Rate Limit Headers
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 57
X-RateLimit-Reset: 1640000000
```

### Handle Rate Limiting
```typescript
async function withRateLimitRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      if (error.message.includes('Rate limited') && i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, 60000));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

## Common Mistakes
- Using password instead of API token (deprecated)
- Forgetting to base64 encode credentials
- Missing the space after "Basic " in header
- Using wrong base URL format (must include `https://`)

## References
- [Jira Cloud REST API Authentication](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-authentication/)
- [API Tokens](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
- [Rate Limiting](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/)

## Version History
- 2025-12-11: Added .env file setup and test script documentation
- 2025-12-10: Created
