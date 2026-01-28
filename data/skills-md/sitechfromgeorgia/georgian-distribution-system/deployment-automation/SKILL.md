---
name: deployment-automation
description: Expert DevOps automation consultant for building production-grade CI/CD deployment pipelines using Vercel, GitHub Actions, and Railway. Implements build/test/preview/production workflows, automated rollbacks, canary deployments, blue-green strategies, environment promotion, secrets management, health checks, smoke testing, and live monitoring. Use when deploying web applications, setting up CI/CD pipelines, configuring automated deployments, implementing deployment strategies, managing production releases, or troubleshooting deployment issues.
license: Apache-2.0
---

# Deployment Automation Guide

## Overview

This skill provides comprehensive deployment automation patterns for modern web applications using industry-leading platforms: **Vercel** (frontend), **Railway** (backend), and **GitHub Actions** (CI/CD orchestration).

**Core Capabilities**:
- CI/CD pipeline design and implementation
- Preview and production deployment workflows
- Canary and blue-green deployment strategies
- Automated rollback mechanisms
- Environment variable and secrets management
- Health checks and smoke testing
- Status monitoring and notifications
- Performance optimization and caching
- Multi-environment orchestration

**Updated for 2025**: This guide reflects the latest platform features, security best practices, and deployment patterns validated by production teams.

---

## 2025 Deployment Best Practices

### Key Principles

1. **Test Before Deploy**: Always run linting, type checking, and tests in CI before deploying
2. **Progressive Rollout**: Start with 10% traffic, monitor, then gradually increase
3. **Automated Rollback**: Configure automatic rollback on error rate > 1% or latency spike > 20%
4. **Health Checks**: Implement `/health` endpoints that verify all dependencies
5. **Zero-Downtime**: Use blue-green or canary deployments for production changes
6. **Environment Parity**: Keep staging and production configurations as similar as possible
7. **Secrets Rotation**: Rotate credentials every 90 days, use short-lived tokens when possible
8. **Monitoring First**: Set up alerts BEFORE deploying, not after incidents occur

### Modern CI/CD Pipeline Structure

```
┌─────────────┐    ┌──────────┐    ┌─────────────┐    ┌──────────┐
│   Commit    │ -> │   Test   │ -> │   Deploy    │ -> │  Monitor │
│   & Push    │    │  & Lint  │    │   Preview   │    │  Health  │
└─────────────┘    └──────────┘    └─────────────┘    └──────────┘
                                           │
                                           v
                                    ┌─────────────┐
                                    │   Deploy    │
                                    │  Production │
                                    │  (Canary)   │
                                    └─────────────┘
                                           │
                                           v
                                    ┌─────────────┐
                                    │   Promote   │
                                    │  or Rollback│
                                    └─────────────┘
```

### Performance Targets (2025 Standards)

| Metric | Target | Action if Exceeded |
|--------|--------|-------------------|
| Build Time | < 5 minutes | Investigate caching, optimize dependencies |
| Deployment Time | < 2 minutes | Check network, reduce asset size |
| Health Check Response | < 500ms | Optimize endpoint, check database |
| P95 Latency | < 200ms | Add caching, optimize queries |
| Error Rate | < 0.1% | Automatic rollback + investigation |

---

## Quick Start Decision Matrix

**Choose Your Platform**:

| Use Case | Platform | Why |
|----------|----------|-----|
| Next.js, React, Vue, Static Sites | **Vercel** | Zero-config, edge network, instant previews |
| Node.js, Python, Go backends | **Railway** | Simple setup, good DX, affordable |
| Custom workflows, monorepos | **GitHub Actions** | Full control, free for public repos |

---

## Platform-Specific Deployment Guides

### 1. Vercel Deployment Strategy

**When to Use**: Frontend applications, Next.js, static sites, serverless functions

**Key Features**:
- Automatic preview deployments for every PR
- Production deployments on merge to main
- Edge network CDN
- Built-in SSL certificates
- Environment-specific configurations

**Standard Workflow with Testing** (2025 Pattern):

```yaml
# .github/workflows/vercel-preview.yml
name: Vercel Preview Deployment
env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  # Step 1: Run tests first
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ESLint
        run: npm run lint
      
      - name: Run type checking
        run: npm run type-check
      
      - name: Run tests
        run: npm test
  
  # Step 2: Deploy only if tests pass
  deploy-preview:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Vercel CLI
        run: npm install --global vercel@latest
      
      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=preview --token=${{ secrets.VERCEL_TOKEN }}
      
      - name: Build Project
        run: vercel build --token=${{ secrets.VERCEL_TOKEN }}
      
      - name: Deploy to Vercel
        id: deploy
        run: |
          URL=$(vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }})
          echo "preview-url=$URL" >> $GITHUB_OUTPUT
      
      - name: Comment PR with Preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚀 Preview deployment ready!\n\n**URL:** ${{ steps.deploy.outputs.preview-url }}'
            })
```

```yaml
# .github/workflows/vercel-production.yml
name: Vercel Production Deployment
env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

on:
  push:
    branches:
      - main

jobs:
  # Step 1: Full test suite
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run full test suite
        run: |
          npm run lint
          npm run type-check
          npm test
          npm run test:e2e  # End-to-end tests
  
  # Step 2: Deploy to production
  deploy-production:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Vercel CLI
        run: npm install --global vercel@latest
      
      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
      
      - name: Build Project
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}
      
      - name: Deploy to Vercel
        id: deploy
        run: |
          URL=$(vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }})
          echo "production-url=$URL" >> $GITHUB_OUTPUT
      
      - name: Post-deployment smoke tests
        run: |
          chmod +x ./scripts/smoke-test.sh
          ./scripts/smoke-test.sh ${{ steps.deploy.outputs.production-url }}
      
      - name: Notify on success
        if: success()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
               -H 'Content-Type: application/json' \
               -d '{"text":"✅ Production deployment successful!\n**URL:** ${{ steps.deploy.outputs.production-url }}"}'
      
      - name: Notify on failure
        if: failure()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
               -H 'Content-Type: application/json' \
               -d '{"text":"❌ Production deployment failed! Check GitHub Actions logs."}'
```

**Required Secrets**:
- `VERCEL_TOKEN`: Create at vercel.com/account/tokens
- `VERCEL_ORG_ID`: Found in `.vercel/project.json` after running `vercel link`
- `VERCEL_PROJECT_ID`: Found in `.vercel/project.json`

**Best Practices**:
- Disable Vercel's auto-deployment when using GitHub Actions (gives you more control)
- Run linting and tests before deployment
- Use environment-specific variables (Preview vs Production)
- Cache dependencies to speed up builds

See `references/VERCEL_ADVANCED.md` for advanced patterns, caching strategies, and troubleshooting.

---

### 2. Railway Deployment Strategy

**When to Use**: Backend services, databases, Node.js/Python/Go apps, APIs

**Key Features**:
- Simple container-based deployments
- Automatic HTTPS with custom domains
- Built-in database support (PostgreSQL, MySQL, Redis)
- Environment management
- Zero-downtime deployments

**Standard Workflow**:

```yaml
# .github/workflows/railway-deploy.yml
name: Deploy to Railway

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    container: ghcr.io/railwayapp/cli:latest
    env:
      RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      SERVICE_ID: ${{ secrets.RAILWAY_SERVICE_ID }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        run: railway up --service=${{ env.SERVICE_ID }}
```

**Alternative: Custom Docker Workflow**

```yaml
# .github/workflows/railway-docker.yml
name: Railway Docker Deploy

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      
      - name: Link Railway Project
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          railway link --project=${{ secrets.RAILWAY_PROJECT_ID }} \
                       --environment=${{ secrets.RAILWAY_ENVIRONMENT_ID }}
      
      - name: Deploy
        run: railway redeploy --yes
```

**Required Secrets**:
- `RAILWAY_TOKEN`: Create at railway.app/account/tokens
- `RAILWAY_SERVICE_ID`: Found in service settings
- `RAILWAY_PROJECT_ID`: Found in project settings
- `RAILWAY_ENVIRONMENT_ID`: Found in environment settings (production/staging)

**Best Practices**:
- Use separate Railway projects for staging and production
- Configure health check endpoints
- Set up automatic rollback on failed deployments
- Monitor deployment logs in Railway dashboard

See `references/RAILWAY_ADVANCED.md` for monorepo deployments, database migrations, and optimization strategies.

---

### 3. Canary Deployment Strategy

**What is Canary Deployment?**

Gradually roll out changes to a small subset of users before full production release. This minimizes blast radius if issues occur.

**When to Use**:
- High-traffic production applications
- Changes with uncertain performance impact
- Features requiring real-world validation
- Risk-sensitive deployments

**Implementation Pattern**:

**Stage 1: Deploy Canary (10% traffic)**
```yaml
# .github/workflows/canary-deploy.yml
name: Canary Deployment

on:
  push:
    branches:
      - main

jobs:
  deploy-canary:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Deploy to canary environment (separate service or slot)
      - name: Deploy Canary Version
        run: |
          # Deploy to Railway with canary tag
          railway up --service=${{ secrets.CANARY_SERVICE_ID }} \
                     --environment=production
      
      # Route 10% traffic to canary
      - name: Configure Traffic Split
        run: |
          # Use your platform's traffic management API
          # Vercel: Update deployment alias with traffic routing
          # Railway: Use load balancer configuration
          echo "Routing 10% traffic to canary"
      
      # Wait and monitor for 15 minutes
      - name: Monitor Canary Health
        run: |
          sleep 900  # 15 minutes
          # Run health checks (see scripts/health-check.sh)
          ./scripts/health-check.sh ${{ secrets.CANARY_URL }}
```

**Stage 2: Promote or Rollback**

```yaml
  promote-or-rollback:
    needs: deploy-canary
    runs-on: ubuntu-latest
    steps:
      - name: Check Canary Metrics
        id: metrics
        run: |
          # Fetch error rate, latency, success rate from monitoring
          # Example: Query Prometheus/Datadog/custom metrics endpoint
          ERROR_RATE=$(curl -s ${{ secrets.METRICS_API }}/error-rate)
          
          if [ "$ERROR_RATE" -lt "1" ]; then
            echo "status=success" >> $GITHUB_OUTPUT
          else
            echo "status=failure" >> $GITHUB_OUTPUT
          fi
      
      - name: Promote Canary
        if: steps.metrics.outputs.status == 'success'
        run: |
          # Route 100% traffic to new version
          railway up --service=${{ secrets.PRODUCTION_SERVICE_ID }}
          echo "✅ Canary promoted to production"
      
      - name: Rollback Canary
        if: steps.metrics.outputs.status == 'failure'
        run: |
          # Route all traffic back to stable version
          railway rollback --service=${{ secrets.CANARY_SERVICE_ID }}
          echo "⚠️ Canary rolled back due to high error rate"
```

**Progressive Rollout Schedule**:
1. **10% traffic** → Monitor for 15 minutes
2. If stable: **25% traffic** → Monitor for 15 minutes  
3. If stable: **50% traffic** → Monitor for 30 minutes
4. If stable: **100% traffic** → Full production

**Rollback Triggers**:
- Error rate > 1%
- P95 latency increase > 20%
- Success rate < 99%
- Manual intervention required

See `references/CANARY_DEPLOYMENTS.md` for detailed canary strategies, A/B testing, and feature flags.

---

## 4. Rollback Procedures

### Automated Rollback

**Railway Rollback**:
```bash
# Rollback to previous deployment
railway rollback --service=my-service

# Rollback to specific deployment ID
railway rollback --service=my-service --deployment=dep_abc123
```

**Vercel Rollback**:
```bash
# List recent deployments
vercel ls

# Promote previous deployment to production
vercel promote [deployment-url] --prod
```

**GitHub Actions Rollback Workflow**:
```yaml
# .github/workflows/rollback.yml
name: Emergency Rollback

on:
  workflow_dispatch:
    inputs:
      target_version:
        description: 'Version to rollback to'
        required: true
        type: string

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ inputs.target_version }}
      
      - name: Rollback Vercel
        run: |
          vercel promote [previous-deployment-url] --prod \
                --token=${{ secrets.VERCEL_TOKEN }}
      
      - name: Rollback Railway
        run: railway rollback --service=${{ secrets.SERVICE_ID }}
      
      - name: Notify Team
        run: |
          # Send Slack/Discord notification
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
               -d '{"text":"🚨 Rollback to version ${{ inputs.target_version }} completed"}'
```

### Manual Rollback Checklist

1. **Identify Issue**: Check monitoring dashboards (error rates, latency, logs)
2. **Stop Current Deployment**: Pause or cancel ongoing deployments
3. **Revert Code**: `git revert` or `git reset` to stable commit
4. **Redeploy Stable Version**: Trigger production deployment workflow
5. **Verify Rollback**: Run smoke tests, check health endpoints
6. **Notify Team**: Alert via Slack/Discord with incident details
7. **Post-Mortem**: Document what failed and prevention strategies

See `references/ROLLBACK_STRATEGIES.md` for advanced rollback patterns and disaster recovery.

---

## 5. Environment Variable Management

### Secret Storage Strategy

**GitHub Secrets** (for CI/CD):
- Repository Settings → Secrets and variables → Actions → New repository secret
- Store: API tokens, deployment credentials, webhook URLs

**Vercel Environment Variables**:
```bash
# Via CLI
vercel env add VARIABLE_NAME production
vercel env add VARIABLE_NAME preview

# Via Dashboard
Project Settings → Environment Variables → Add
```

**Railway Environment Variables**:
```bash
# Via CLI
railway variables set VARIABLE_NAME=value

# Via Dashboard
Service Settings → Variables → Add Variable
```

### Environment Variable Patterns

**Development**:
```env
NODE_ENV=development
API_URL=http://localhost:3000
DATABASE_URL=postgresql://localhost:5432/dev_db
DEBUG=true
```

**Preview/Staging**:
```env
NODE_ENV=staging
API_URL=https://api-staging.example.com
DATABASE_URL=postgresql://staging-db.railway.app/db
DEBUG=true
SENTRY_ENVIRONMENT=staging
```

**Production**:
```env
NODE_ENV=production
API_URL=https://api.example.com
DATABASE_URL=postgresql://prod-db.railway.app/db
DEBUG=false
SENTRY_ENVIRONMENT=production
```

**Security Best Practices**:
- ✅ Never commit secrets to git
- ✅ Use separate credentials for each environment
- ✅ Rotate secrets every 90 days
- ✅ Use least-privilege access tokens
- ✅ Audit secret access logs
- ❌ Don't hardcode secrets in code
- ❌ Don't share production secrets in Slack/email
- ❌ Don't use same password across environments

---

## 6. Health Checks and Smoke Tests

### Health Check Endpoint Pattern

**Implementation Example (Express.js)**:
```javascript
// /health endpoint
app.get('/health', (req, res) => {
  const health = {
    uptime: process.uptime(),
    status: 'UP',
    timestamp: Date.now(),
    checks: {
      database: checkDatabaseConnection(),
      redis: checkRedisConnection(),
      api: checkExternalAPI()
    }
  };
  
  const isHealthy = Object.values(health.checks).every(check => check === true);
  res.status(isHealthy ? 200 : 503).json(health);
});
```

### Automated Smoke Tests

Use `scripts/smoke-test.sh`:
```bash
#!/bin/bash
# Health check script for post-deployment verification

DEPLOYMENT_URL=$1
MAX_RETRIES=10
RETRY_DELAY=5

for i in $(seq 1 $MAX_RETRIES); do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $DEPLOYMENT_URL/health)
  
  if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Health check passed (attempt $i/$MAX_RETRIES)"
    exit 0
  else
    echo "⚠️ Health check failed with status $HTTP_CODE (attempt $i/$MAX_RETRIES)"
    sleep $RETRY_DELAY
  fi
done

echo "❌ Health check failed after $MAX_RETRIES attempts"
exit 1
```

**Integration in Workflow**:
```yaml
- name: Smoke Test Deployment
  run: |
    chmod +x ./scripts/smoke-test.sh
    ./scripts/smoke-test.sh https://my-app.vercel.app
```

---

## 7. Status Monitoring

### Monitoring Stack Recommendations

**Frontend (Vercel)**:
- Vercel Analytics (built-in)
- Sentry for error tracking
- LogRocket for session replay

**Backend (Railway)**:
- Railway Observability (built-in logs)
- Prometheus + Grafana for metrics
- Datadog or New Relic for APM

### Alert Configuration

**Railway Health Check**:
```yaml
# Railway service configuration
healthCheckPath: /health
healthCheckTimeout: 30
restartPolicyMaxRetries: 3
```

**Uptime Monitoring**:
- UptimeRobot (free tier: 5-minute checks)
- Better Uptime (paid: 30-second checks)
- StatusCake (free tier: 5-minute checks)

---

## Deployment Workflow Templates

### Complete CI/CD Pipeline

**Full Example: Frontend + Backend**

```yaml
# .github/workflows/deploy-full-stack.yml
name: Deploy Full Stack Application

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  # Step 1: Lint and Test
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install Dependencies
        run: npm ci
      
      - name: Run Linter
        run: npm run lint
      
      - name: Run Tests
        run: npm test
  
  # Step 2: Deploy Frontend to Vercel
  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
        run: |
          npm i -g vercel
          vercel pull --yes --environment=production --token=$VERCEL_TOKEN
          vercel build --prod --token=$VERCEL_TOKEN
          vercel deploy --prebuilt --prod --token=$VERCEL_TOKEN
  
  # Step 3: Deploy Backend to Railway
  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    container: ghcr.io/railwayapp/cli:latest
    env:
      RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      SERVICE_ID: ${{ secrets.RAILWAY_SERVICE_ID }}
    steps:
      - uses: actions/checkout@v3
      - run: railway up --service=$SERVICE_ID
  
  # Step 4: Post-Deployment Verification
  verify-deployment:
    needs: [deploy-frontend, deploy-backend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Health Check Frontend
        run: |
          curl -f ${{ secrets.FRONTEND_URL }}/api/health || exit 1
      
      - name: Health Check Backend
        run: |
          curl -f ${{ secrets.BACKEND_URL }}/health || exit 1
      
      - name: Notify Success
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
               -d '{"text":"✅ Deployment successful: Frontend + Backend deployed"}'
```

---

## Quick Reference: Common Commands

### Vercel CLI
```bash
vercel login                              # Authenticate
vercel link                               # Link to project
vercel                                    # Deploy preview
vercel --prod                             # Deploy production
vercel ls                                 # List deployments
vercel inspect [url]                      # Inspect deployment
vercel logs [url]                         # View logs
vercel env ls                             # List environment variables
vercel domains add example.com            # Add custom domain
```

### Railway CLI
```bash
railway login                             # Authenticate
railway init                              # Initialize project
railway up                                # Deploy service
railway status                            # Check status
railway logs                              # View logs
railway run [command]                     # Run command
railway variables                         # List variables
railway open                              # Open in browser
railway rollback                          # Rollback deployment
```

### GitHub CLI
```bash
gh workflow list                          # List workflows
gh workflow run [name]                    # Trigger workflow
gh run list                               # List workflow runs
gh run view [id]                          # View run details
gh secret set [name]                      # Set secret
```

---

## Troubleshooting Guide

### Common Issues

**Vercel: Build Failed**
- Check build logs in Vercel dashboard
- Verify Node.js version matches local (`node -v`)
- Check environment variables are set
- Clear cache: `vercel build --force`

**Railway: Service Not Starting**
- Check service logs: `railway logs`
- Verify health check endpoint is responding
- Check resource limits (CPU/memory)
- Ensure environment variables are correctly set

**GitHub Actions: Workflow Failed**
- Check Actions tab for error logs
- Verify secrets are correctly set
- Check workflow YAML syntax
- Review job dependencies and conditions

**Deployment Stuck**
- Cancel current deployment
- Check for resource locks
- Verify credentials haven't expired
- Try manual deployment via CLI

---

## Additional Resources

**References** (detailed documentation):
- `references/VERCEL_ADVANCED.md` - Advanced Vercel patterns, caching, optimization
- `references/RAILWAY_ADVANCED.md` - Railway monorepos, databases, Docker optimization
- `references/CANARY_DEPLOYMENTS.md` - Progressive delivery, A/B testing, feature flags
- `references/ROLLBACK_STRATEGIES.md` - Disaster recovery, incident response procedures
- `references/SECURITY_BEST_PRACTICES.md` - Comprehensive security guide for CI/CD pipelines (NEW 2025)

**Scripts** (automation tools):
- `scripts/smoke-test.sh` - Post-deployment health verification
- `scripts/setup-secrets.sh` - Automate GitHub secrets configuration
- `scripts/health-check.sh` - Comprehensive health check script for production monitoring

---

## Best Practices Summary

✅ **DO**:
- Run tests before every deployment
- Use separate environments (dev/staging/prod)
- Implement health check endpoints
- Monitor deployments with alerts
- Document rollback procedures
- Automate everything possible
- Use semantic versioning for releases

❌ **DON'T**:
- Deploy directly to production without testing
- Hardcode secrets in code or workflows
- Skip health checks after deployment
- Ignore monitoring alerts
- Deploy on Fridays without rollback plan
- Use production credentials in staging

---

## Getting Started Checklist

- [ ] Set up GitHub repository with `.github/workflows/` directory
- [ ] Create Vercel project and link to repository
- [ ] Create Railway project for backend services
- [ ] Configure GitHub secrets (tokens, IDs, credentials)
- [ ] Set up environment variables in Vercel and Railway
- [ ] Create health check endpoints in backend
- [ ] Implement smoke test scripts
- [ ] Configure monitoring and alerting
- [ ] Test preview deployment workflow
- [ ] Test production deployment workflow
- [ ] Document rollback procedure
- [ ] Schedule regular secret rotation

---

**This skill provides production-ready deployment automation patterns. Adapt workflows to your specific needs and always test thoroughly in non-production environments first.**