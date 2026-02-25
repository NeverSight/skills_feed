---
name: deployment
description: "Load PROACTIVELY when task involves deploying, hosting, or CI/CD pipelines. Use when user says \"deploy this\", \"set up CI/CD\", \"add Docker\", \"configure Vercel\", or \"set up monitoring\". Covers platform-specific deployment (Vercel, Railway, Fly.io, AWS), Dockerfile creation, environment variable management, CI/CD pipeline configuration (GitHub Actions), preview deployments, health checks, rollback strategies, and production monitoring setup."
metadata:
  version: "1.0.0"
  category: outcome
  tags: [deployment, devops, ci-cd, docker, vercel, monitoring]
---

## Resources
```
scripts/
  validate-deployment.sh
references/
  deployment-platforms.md
```

# Deployment

This skill guides you through deploying applications to production using modern platforms and tools. Use this workflow when deploying Next.js, full-stack apps, containerized services, or serverless functions.

## When to Use This Skill

- Deploying applications to Vercel, Railway, Fly.io, or AWS
- Setting up CI/CD pipelines with GitHub Actions
- Configuring Docker containers for production
- Implementing health checks and monitoring
- Creating preview deployments for pull requests
- Setting up rollback and canary deployment strategies

## Platform Selection

Choose the right platform based on your application needs:

### Vercel (Best for Next.js)

**When to use:**
- Next.js applications (App Router or Pages Router)
- Static sites with edge functions
- Automatic preview deployments per PR
- Zero-config deployments

**Setup:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

**Environment variables:**
```bash
# Set production secrets
vercel env add DATABASE_URL production
vercel env add NEXTAUTH_SECRET production
```

### Railway (Best for Full-Stack)

**When to use:**
- Full-stack apps with databases
- Monorepo deployments
- PostgreSQL, Redis, MongoDB hosting
- WebSocket support

**Setup:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway up
```

**railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build"
  },
  "deploy": {
    "startCommand": "npm start",
    "healthcheckPath": "/api/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

### Fly.io (Best for Containers)

**When to use:**
- Custom container requirements
- Global edge deployment
- Long-running processes
- Fine-grained scaling control

**Setup:**
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Initialize and deploy
fly launch
fly deploy
```

**fly.toml:**
```toml
app = "my-app"
primary_region = "sjc"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/api/health"

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Docker (Best for Self-Hosted)

**When to use:**
- Self-hosted infrastructure
- VPS deployments (DigitalOcean, Linode)
- Local development parity
- Multi-service orchestration

See references/deployment-platforms.md for Dockerfile examples.

### AWS (Best for Enterprise)

**When to use:**
- Enterprise requirements
- Compliance/regulatory needs
- Complex infrastructure
- Multi-region deployments

**Services:**
- **ECS Fargate**: Serverless containers
- **Lambda**: Serverless functions
- **Amplify**: Full-stack deployments
- **Elastic Beanstalk**: Managed platform

## Environment Configuration

### .env Management

Never commit secrets to git. Always use .env.example for documentation:

**.env.example:**
```bash
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"

# Authentication
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="generate-with-openssl-rand-base64-32"

# External APIs
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS="false"
```

### Environment Variable Validation

Validate environment variables at build time to fail fast:

**src/env.mjs:**
```javascript
import { z } from 'zod';

const server = z.object({
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
});

const client = z.object({
  NEXT_PUBLIC_APP_URL: z.string().url(),
});

const processEnv = {
  DATABASE_URL: process.env.DATABASE_URL,
  NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
  STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
  NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
};

const merged = server.merge(client);
const parsed = merged.safeParse(processEnv);

if (!parsed.success) {
  console.error('[FAIL] Invalid environment variables:', parsed.error.flatten().fieldErrors);
  throw new Error('Invalid environment variables');
}

export const env = parsed.data;
```

Import at the top of your app to validate on startup:

```typescript
import { env } from './env.mjs';

// Use typed, validated env
const db = new PrismaClient({
  datasources: { db: { url: env.DATABASE_URL } },
});
```

## CI/CD Pipelines

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
        env:
          SKIP_ENV_VALIDATION: true

  deploy:
    runs-on: ubuntu-latest
    needs: [build]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Caching Strategies

Speed up CI/CD with proper caching:

```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      .next/cache
    key: ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-${{ hashFiles('**/*.js', '**/*.jsx', '**/*.ts', '**/*.tsx') }}
    restore-keys: |
      ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-
      ${{ runner.os }}-nextjs-
```

## Docker Production Setup

### Multi-Stage Dockerfile

Create an optimized production Dockerfile:

**Dockerfile (Next.js):**
```dockerfile
FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

**next.config.js:**
```javascript
module.exports = {
  output: 'standalone', // Required for Docker
};
```

### .dockerignore

Exclude unnecessary files from the Docker build:

```
Dockerfile
.dockerignore
node_modules
npm-debug.log
README.md
.next
.git
.gitignore
.env*.local
.vscode
.idea
dist
build
coverage
*.md
!README.md
```

### Build and Run

```bash
# Build the image
docker build -t my-app .

# Run with environment variables
docker run -p 3000:3000 \
  -e DATABASE_URL="postgresql://..." \
  -e NEXTAUTH_SECRET="..." \
  my-app
```

## Health Checks

### Health Check Endpoint

Create a health check endpoint for monitoring:

**app/api/health/route.ts:**
```typescript
import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  try {
    // Check database connection
    await prisma.$queryRaw`SELECT 1`;
    
    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      database: 'connected',
    });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        database: 'disconnected',
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 503 }
    );
  }
}
```

### Docker Health Check

Add health check to Dockerfile:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"
```

### Kubernetes Liveness/Readiness

```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 15
  periodSeconds: 20

readinessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10
```

## Preview Deployments

### Automatic PR Previews

Vercel and Railway automatically create preview deployments for pull requests.

**GitHub Actions for Railway:**
```yaml
on:
  pull_request:
    branches: [main]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Railway (PR)
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: ${{ secrets.RAILWAY_SERVICE }}
```

### Comment on PR with Preview URL

```yaml
- name: Comment PR
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '[DEPLOY] Preview deployed to: https://pr-${{ github.event.number }}.myapp.com'
      })
```

## Rollback Strategies

### Instant Rollback (Vercel)

```bash
# List deployments
vercel ls

# Promote a previous deployment to production
vercel promote <deployment-url>
```

### Blue-Green Deployment

Deploy new version alongside old, then switch traffic:

```bash
# Deploy new version (green)
fly deploy --strategy bluegreen

# Traffic switches automatically after health checks pass
# Rollback if needed:
fly releases rollback
```

### Canary Deployment

Gradually shift traffic to new version:

**Fly.io canary:**
```bash
# Deploy canary (10% traffic)
fly deploy --strategy canary

# Promote to 100% if successful
fly releases promote
```

## Monitoring and Error Tracking

### Sentry Integration

```bash
npm install @sentry/nextjs
```

**sentry.client.config.ts:**
```typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  environment: process.env.NODE_ENV,
  enabled: process.env.NODE_ENV === 'production',
});
```

**sentry.server.config.ts:**
```typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
  environment: process.env.NODE_ENV,
});
```

### Uptime Monitoring

Use external services to monitor availability:

- **Better Uptime**: https://betteruptime.com
- **Pingdom**: https://www.pingdom.com
- **UptimeRobot**: https://uptimerobot.com

Monitor your `/api/health` endpoint every 1-5 minutes.

### Log Aggregation

**Vercel:**
- Built-in log streaming
- Integration with Datadog, LogDNA, Axiom

**Railway:**
- Built-in logs in dashboard
- Export to external services

**Self-hosted:**
```bash
# Use Docker logging driver
docker run --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  my-app
```

## Database Migrations in CI/CD

### Prisma Migrations

Run migrations before deployment:

**GitHub Actions:**
```yaml
- name: Run migrations
  run: npx prisma migrate deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

**Railway:**
Add to railway.json:
```json
{
  "deploy": {
    "startCommand": "npx prisma migrate deploy && npm start"
  }
}
```

### Migration Safety

Never run destructive migrations automatically:

1. **Backwards compatible migrations first**
   - Add new columns as nullable
   - Deploy code that works with old and new schema
   - Run migration
   - Deploy code that requires new schema
   - Remove old columns in future migration

2. **Manual approval for production**
   ```yaml
   - name: Run migrations
     if: github.event_name == 'workflow_dispatch'
     run: npx prisma migrate deploy
   ```

## Precision Tool Integration

### Validate Deployment with precision_exec

Use `precision_exec` to run deployment commands with expectations:

```yaml
precision_exec:
  commands:
    - cmd: "npm run build"
      expect:
        exit_code: 0
    - cmd: "docker build -t my-app ."
      expect:
        exit_code: 0
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
  verbosity: minimal
```

### Health Check with precision_fetch

Validate deployment health:

```yaml
precision_fetch:
  requests:
    - url: "https://my-app.com/api/health"
      method: GET
      expect:
        status: 200
        body_contains: '"status":"healthy"'
```

### Discover Deployment Gaps

Before deploying, check for missing configuration:

```yaml
discover:
  queries:
    - id: env_example
      type: glob
      patterns: [".env.example"]
    - id: dockerfile
      type: glob
      patterns: ["Dockerfile", "docker-compose.yml"]
    - id: ci_config
      type: glob
      patterns: [".github/workflows/*.yml"]
    - id: health_check
      type: grep
      pattern: '/api/health|/health'
      glob: "**/*.{ts,tsx,js,jsx}"
  output_mode: count_only
```

## Pre-Deployment Checklist

Run the validation script:

```bash
./plugins/goodvibes/skills/outcome/deployment/scripts/validate-deployment.sh /path/to/project
```

The script checks:
1. Dockerfile exists
2. .env.example exists and documents required variables
3. CI/CD configuration present
4. Health check endpoint implemented
5. .dockerignore exists
6. No hardcoded secrets in code
7. Build command succeeds
8. Database migration configuration present

## Common Pitfalls

### 1. Missing Environment Variables

**Problem:** Deployment fails because environment variables aren't set.

**Solution:** Document all variables in .env.example and validate at build time with zod.

### 2. Database Connection Pooling

**Problem:** Serverless functions exhaust database connections.

**Solution:** Use connection pooling (PgBouncer, Prisma Accelerate, Supabase pooler).

```typescript
// Use connection pooler in serverless
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL, // Use pooled connection string
    },
  },
});
```

### 3. Build Output Not Optimized

**Problem:** Large Docker images, slow cold starts.

**Solution:** Use multi-stage builds, standalone output for Next.js, proper .dockerignore.

### 4. Migrations Run on Every Deploy

**Problem:** Prisma migrations run on every container start.

**Solution:** Separate migration step from app startup in CI/CD.

### 5. No Rollback Plan

**Problem:** Bad deployment breaks production with no easy fix.

**Solution:** Use platforms with instant rollback (Vercel, Railway, Fly.io) or maintain previous Docker images.

## Summary

**Key Principles:**

1. **Validate environment variables at build time** - Fail fast, not in production
2. **Automate everything** - CI/CD should handle lint, test, build, deploy
3. **Health checks are mandatory** - Every service needs a health endpoint
4. **Preview deployments for every PR** - Catch issues before merging
5. **Always have a rollback plan** - Instant rollback > fixing forward
6. **Monitor from day one** - Error tracking and uptime monitoring are not optional
7. **Migrations are dangerous** - Run them carefully with backwards compatibility

**Next Steps:**

1. Run `validate-deployment.sh` on your project
2. Set up CI/CD pipeline with GitHub Actions
3. Configure environment variables in your platform
4. Add health check endpoint
5. Test deployment to staging environment
6. Deploy to production
7. Set up monitoring and alerting

For detailed platform configurations and templates, see `references/deployment-platforms.md`.