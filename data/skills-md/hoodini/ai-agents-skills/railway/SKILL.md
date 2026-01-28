---
name: railway
description: Deploy applications on Railway platform. Use when deploying containerized apps, setting up databases, configuring private networking, or managing Railway projects. Triggers on Railway, railway.app, deploy container, Railway database.
---

# Railway Deployment

Deploy and manage applications on Railway's platform.

## Quick Start

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

## railway.toml Configuration

```toml
[build]
builder = "nixpacks"
buildCommand = "npm run build"

[deploy]
startCommand = "npm start"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3

[service]
internalPort = 3000
```

## Nixpacks Configuration

```toml
# nixpacks.toml
[phases.setup]
nixPkgs = ["nodejs-18_x", "python311"]

[phases.install]
cmds = ["npm ci"]

[phases.build]
cmds = ["npm run build"]

[start]
cmd = "npm start"
```

## Environment Variables

```bash
# Set variable
railway variables set DATABASE_URL="postgres://..."

# Set from file
railway variables set < .env

# Link to service
railway service
railway variables set API_KEY="secret"
```

## Database Services

### PostgreSQL
```bash
# Add PostgreSQL
railway add -d postgres

# Get connection string
railway variables get DATABASE_URL
```

### Redis
```bash
railway add -d redis
# Access via REDIS_URL
```

### MySQL
```bash
railway add -d mysql
# Access via MYSQL_URL
```

## Private Networking

```yaml
# Services can communicate via internal DNS
# Format: ${{service-name}}.railway.internal

# Example: API calling database service
DATABASE_HOST: ${{postgres.railway.internal}}
DATABASE_PORT: 5432
```

## Volumes (Persistent Storage)

```bash
# Create volume
railway volume create my-data

# Mount in service
railway volume attach my-data:/app/data
```

In code:
```javascript
// Data persists across deploys
const dataPath = '/app/data';
fs.writeFileSync(`${dataPath}/file.json`, JSON.stringify(data));
```

## Cron Jobs

```toml
# railway.toml
[deploy]
startCommand = "node cron.js"
cronSchedule = "0 */6 * * *"  # Every 6 hours
```

## Multi-Service Setup

```
my-project/
├── api/
│   ├── railway.toml
│   └── ...
├── worker/
│   ├── railway.toml
│   └── ...
└── frontend/
    ├── railway.toml
    └── ...
```

Deploy each:
```bash
cd api && railway up
cd ../worker && railway up
cd ../frontend && railway up
```

## Dockerfile Deploy

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
```

```toml
# railway.toml
[build]
builder = "dockerfile"
dockerfilePath = "./Dockerfile"
```

## Health Checks

```typescript
// Express health endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy',
    timestamp: new Date().toISOString()
  });
});
```

```toml
# railway.toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 100
```

## Resources

- **Railway Docs**: https://docs.railway.app
- **Railway CLI**: https://docs.railway.app/develop/cli
