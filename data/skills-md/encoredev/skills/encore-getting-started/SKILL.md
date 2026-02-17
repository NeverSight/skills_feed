---
name: encore-getting-started
description: Get started with Encore.ts - create and run your first app.
---

# Getting Started with Encore.ts

## Instructions

### Install Encore CLI

```bash
# macOS
brew install encoredev/tap/encore

# Linux/WSL
curl -L https://encore.dev/install.sh | bash

# Windows (PowerShell)
iwr https://encore.dev/install.ps1 | iex
```

### Create a New App

```bash
# Interactive - choose from templates
encore app create my-app

# Or start with a blank app
encore app create my-app --example=ts/hello-world
```

### Project Structure

A minimal Encore.ts app:

```
my-app/
├── encore.app           # App configuration
├── package.json         # Dependencies
├── tsconfig.json        # TypeScript config
├── encore.service.ts    # Service definition
└── api.ts               # API endpoints
```

### The encore.app File

```cue
// encore.app
{
    "id": "my-app"
}
```

This file marks the root of your Encore app. The `id` is your app's unique identifier.

### Define a Service

Create `encore.service.ts` to define a service:

```typescript
// encore.service.ts
import { Service } from "encore.dev/service";

export default new Service("my-service");
```

### Create Your First API

```typescript
// api.ts
import { api } from "encore.dev/api";

interface HelloResponse {
  message: string;
}

export const hello = api(
  { method: "GET", path: "/hello", expose: true },
  async (): Promise<HelloResponse> => {
    return { message: "Hello, World!" };
  }
);
```

### Run Your App

```bash
# Start the development server
encore run

# Your API is now available at http://localhost:4000
```

### Open the Local Dashboard

```bash
# Opens the local development dashboard
encore run
# Then visit http://localhost:9400
```

The dashboard shows:
- All your services and endpoints
- Request/response logs
- Database queries
- Traces and spans

### Common CLI Commands

| Command | Description |
|---------|-------------|
| `encore run` | Start the local development server |
| `encore test` | Run tests |
| `encore db shell <db>` | Open a psql shell to a database |
| `encore gen client` | Generate API client code |
| `encore app link` | Link to an existing Encore Cloud app |

### Add a Database

```typescript
// db.ts
import { SQLDatabase } from "encore.dev/storage/sqldb";

const db = new SQLDatabase("mydb", {
  migrations: "./migrations",
});
```

Create a migration:

```sql
-- migrations/1_create_table.up.sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
```

### Next Steps

- Add more endpoints (see `encore-api` skill)
- Add authentication (see `encore-auth` skill)
- Add infrastructure like Pub/Sub, cron jobs (see `encore-infrastructure` skill)
- Deploy to Encore Cloud: `encore app link` then `git push encore`
