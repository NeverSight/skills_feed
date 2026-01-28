---
name: railway-deployment
description: Comprehensive Railway.com deployment management for GitHub, Docker, and local sources. Use when deploying to Railway, redeploying services, rolling back deployments, monitoring deployment status, managing staging/production deployments, or verifying deployment health.
---

# Railway Deployment Management

Complete deployment workflows for Railway.com including deployment from multiple sources, rollback strategies, health verification, and staging-to-production promotion.

## Overview

This skill provides comprehensive deployment management for Railway:
- **Deploy from sources**: GitHub auto-deploy, Docker images, local directory
- **Monitor deployments**: Real-time logs, status tracking, build progress
- **Verify health**: Automated health checks and validation
- **Rollback strategies**: Safe rollback to previous deployments
- **Environment management**: Staging → production workflows
- **CI/CD integration**: Automated deployment pipelines

## Prerequisites

- Railway CLI installed and authenticated (use `railway-auth` skill)
- Project linked (use `railway-project-management` skill)
- Service created in target environment

## When to Use

- Deploying new code to Railway
- Redeploying after configuration changes
- Rolling back failed deployments
- Promoting staging to production
- Setting up automated deployments
- Monitoring deployment progress
- Verifying deployment health

---

## 5-Step Deployment Workflow

### Step 1: Prepare Deployment

Verify authentication, project context, and service health before deploying.

**Commands**:
```bash
# Verify authentication
railway whoami

# Check project and environment context
railway status

# List services in current environment
railway list

# Check current deployment status
railway status --json
```

**Pre-deployment checklist**:
- [ ] Authenticated with Railway
- [ ] Correct project linked
- [ ] Target environment selected
- [ ] Service exists in environment
- [ ] No pending deployments
- [ ] Environment variables set

**Use automation**:
```bash
.claude/skills/railway-deployment/scripts/pre-deploy-check.sh
```

---

### Step 2: Deploy

Deploy from GitHub, Docker, or local directory.

#### Deploy from GitHub (Auto-Deploy)

**Setup auto-deploy**:
```bash
# Link service to GitHub repo
railway add --repo owner/repository

# Configure branch (via dashboard or railway.json)
railway open
```

**Trigger deployment**:
```bash
# Push to configured branch
git push origin main

# Railway automatically deploys
# Monitor in real-time:
railway logs --deployment
```

**Manual redeploy**:
```bash
# Redeploy latest commit
railway redeploy

# Redeploy specific deployment ID
railway redeploy --deployment <deployment-id>
```

#### Deploy from Local Directory

**Deploy current directory**:
```bash
# Deploy and wait for completion
railway up

# Deploy without waiting (detached)
railway up --detach

# Deploy in CI mode (build logs only)
railway up --ci

# Deploy specific service
railway up --service backend
```

**What happens**:
1. CLI uploads local directory to Railway
2. Railway detects build configuration (Nixpacks/Dockerfile)
3. Build starts automatically
4. Deployment triggers on successful build
5. Service restarts with new code

#### Deploy from Docker Image

**Public image**:
```bash
# Deploy Docker Hub image
railway add --image postgres:15

# Deploy with tag
railway add --image myapp/backend:v1.2.3
```

**Private registry**:
```bash
# Set registry credentials
railway variables set --sealed DOCKER_USERNAME=user
railway variables set --sealed DOCKER_PASSWORD=pass

# Deploy from private registry
railway add --image registry.example.com/app:latest
```

**Update image tag** (rollback/upgrade):
```bash
# Via environment variable
railway variables set IMAGE_TAG=v1.2.2

# Force redeploy with new tag
railway redeploy
```

See `references/deployment-sources.md` for detailed configuration.

---

### Step 3: Monitor Deployment

Track deployment progress and identify issues in real-time.

**Real-time logs**:
```bash
# Follow deployment logs
railway logs --deployment

# Filter by service
railway logs --service backend --deployment

# Show last 100 lines
railway logs --tail 100

# Include timestamps
railway logs --timestamps
```

**Deployment status**:
```bash
# Check deployment status
railway status

# Get detailed JSON status
railway status --json | jq '.deployments[0]'

# List recent deployments
railway list deployments

# Check specific deployment
railway deployment <deployment-id>
```

**Build progress indicators**:
```
Building... ████████░░░░░░░░ 60%
Installing dependencies...
Running build script...
Optimizing assets...
```

**Watch for issues**:
- Build failures (missing dependencies)
- Environment variable errors
- Port binding issues
- Memory/CPU limits exceeded
- Health check failures

**Automated monitoring**:
```bash
# Monitor and alert on failures
.claude/skills/railway-deployment/scripts/monitor-deployment.sh
```

---

### Step 4: Verify Deployment

Validate that deployment is healthy and functioning correctly.

**Health check commands**:
```bash
# Check service health endpoint
curl https://your-service.railway.app/health

# Verify with custom validation
.claude/skills/railway-deployment/scripts/verify-health.sh
```

**Validation checklist**:
- [ ] Service is running (not crashed)
- [ ] Health endpoint returns 200 OK
- [ ] Environment variables loaded correctly
- [ ] Database connections established
- [ ] API endpoints responding
- [ ] Static assets loading
- [ ] No error logs present

**Automated validation**:
```bash
# Run full health check suite
.claude/skills/railway-deployment/scripts/deploy.sh --verify

# Output:
# ✅ Service running
# ✅ Health check passed (200 OK)
# ✅ Environment variables loaded
# ✅ Database connection successful
# ✅ API responding correctly
```

**Common validation issues**:

| Issue | Symptom | Solution |
|-------|---------|----------|
| Service not starting | Status: "crashed" | Check logs for startup errors |
| Health check failing | 503 Service Unavailable | Verify health endpoint path |
| Variables missing | Application errors | Check `railway variables list` |
| Port binding error | "EADDRINUSE" | Ensure PORT variable used |
| Database connection | "ECONNREFUSED" | Verify DATABASE_URL set |

---

### Step 5: Rollback if Needed

Safely rollback to previous deployment if issues are detected.

**Quick rollback**:
```bash
# Redeploy previous deployment
railway redeploy --deployment <previous-deployment-id>

# List recent deployments to find ID
railway list deployments
```

**Automated rollback**:
```bash
# Rollback with safety checks
.claude/skills/railway-deployment/scripts/rollback.sh

# Rollback to specific version
.claude/skills/railway-deployment/scripts/rollback.sh v1.2.3
```

**Rollback strategies**:

1. **Redeploy Previous Commit** (GitHub):
   ```bash
   # Find previous working commit
   git log --oneline

   # Revert to previous commit
   git revert HEAD
   git push origin main

   # Railway auto-deploys
   ```

2. **Redeploy Previous Deployment** (any source):
   ```bash
   # List deployments
   railway list deployments

   # Redeploy specific deployment ID
   railway redeploy --deployment dep_abc123xyz
   ```

3. **Docker Image Tag Rollback**:
   ```bash
   # Update image tag to previous version
   railway variables set IMAGE_TAG=v1.2.2

   # Redeploy with previous tag
   railway redeploy
   ```

4. **Environment Variable Rollback**:
   ```bash
   # Restore previous variable values
   railway variables set API_VERSION=v1
   railway variables set FEATURE_FLAGS=old-config

   # Redeploy with previous config
   railway redeploy
   ```

See `references/rollback-strategies.md` for detailed rollback procedures.

**Rollback verification**:
```bash
# After rollback, verify health
.claude/skills/railway-deployment/scripts/verify-health.sh

# Check logs for errors
railway logs --tail 50

# Verify specific functionality
curl https://your-service.railway.app/api/test
```

---

## Staging → Production Workflow

**Typical promotion flow**:

```bash
# 1. Deploy to staging first
railway environment staging
railway up

# 2. Verify staging deployment
.claude/skills/railway-deployment/scripts/verify-health.sh

# 3. Run staging tests
npm run test:staging

# 4. Promote to production
railway environment production

# 5. Deploy same code
railway up

# 6. Verify production
.claude/skills/railway-deployment/scripts/verify-health.sh

# 7. Monitor production logs
railway logs --deployment
```

**Automated staging workflow**:
```bash
# Complete staging → production workflow
.claude/skills/railway-deployment/scripts/promote-to-production.sh
```

See `references/staging-workflow.md` for detailed staging strategies.

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          railway up --ci

      - name: Verify Deployment
        run: |
          sleep 30
          curl -f https://your-service.railway.app/health || exit 1
```

### GitLab CI

```yaml
deploy:staging:
  stage: deploy
  image: node:20
  script:
    - npm install -g @railway/cli
    - railway environment staging
    - railway up --ci
  environment:
    name: staging
  only:
    - develop

deploy:production:
  stage: deploy
  image: node:20
  script:
    - npm install -g @railway/cli
    - railway environment production
    - railway up --ci
  environment:
    name: production
  only:
    - main
  when: manual
```

---

## Advanced Deployment Patterns

### Blue-Green Deployment

```bash
# 1. Deploy to "green" environment
railway environment green
railway up

# 2. Verify green is healthy
.claude/skills/railway-deployment/scripts/verify-health.sh

# 3. Switch traffic to green
# (Update DNS or load balancer)

# 4. Keep blue as rollback option
railway environment blue
# (Don't delete until green is stable)
```

### Canary Deployment

```bash
# 1. Deploy canary version
railway environment canary
railway up

# 2. Route small % of traffic to canary
# (Configure via load balancer)

# 3. Monitor canary metrics
railway logs --service canary

# 4. Gradually increase traffic
# (Adjust load balancer weights)

# 5. Promote to production if successful
railway environment production
railway up
```

### Rolling Deployment

```bash
# Deploy to instances one at a time
# (Requires horizontal scaling)

# Railway handles rolling deploys automatically
# when multiple replicas are configured
railway up

# Monitors health and rolls back on failure
```

---

## Deployment Troubleshooting

### Build Failures

```bash
# Check build logs
railway logs --deployment

# Common issues:
# - Missing package.json
# - Node/Python version mismatch
# - Build command failures
# - Environment variables not set

# Fix and redeploy
railway up
```

### Deployment Stuck

```bash
# Check deployment status
railway status --json

# Cancel stuck deployment
railway deployment cancel <deployment-id>

# Redeploy
railway up
```

### Health Check Failures

```bash
# Check service logs
railway logs

# Verify health endpoint exists
curl -v https://your-service.railway.app/health

# Check port configuration
railway variables list | grep PORT

# Verify restart policy
railway open  # Check service settings
```

### Memory/CPU Limits

```bash
# Check resource usage
railway metrics

# Increase limits (via dashboard)
railway open

# Or upgrade plan
```

---

## Quick Reference

### Core Deployment Commands

| Command | Description |
|---------|-------------|
| `railway up` | Deploy local directory |
| `railway up --detach` | Deploy without waiting |
| `railway up --ci` | Deploy in CI mode |
| `railway redeploy` | Redeploy latest deployment |
| `railway logs --deployment` | Monitor deployment logs |
| `railway status` | Check deployment status |

### Deployment Sources

| Source | Command | Auto-Deploy |
|--------|---------|-------------|
| GitHub | `railway add --repo owner/repo` | ✅ Yes (on push) |
| Local | `railway up` | ❌ Manual |
| Docker | `railway add --image image:tag` | ❌ Manual |

### Environment Workflow

```bash
# Staging
railway environment staging
railway up

# Production
railway environment production
railway up
```

---

## Automated Scripts

### Smart Deployment with Health Checks

```bash
# Deploy with automatic health verification
.claude/skills/railway-deployment/scripts/deploy.sh

# Deploy specific service
.claude/skills/railway-deployment/scripts/deploy.sh backend

# Deploy with custom health endpoint
.claude/skills/railway-deployment/scripts/deploy.sh backend /api/health
```

### Safe Rollback

```bash
# Rollback with confirmation prompt
.claude/skills/railway-deployment/scripts/rollback.sh

# Rollback to specific deployment
.claude/skills/railway-deployment/scripts/rollback.sh dep_abc123

# Emergency rollback (no confirmation)
.claude/skills/railway-deployment/scripts/rollback.sh --force
```

### Pre-Deployment Validation

```bash
# Check all prerequisites
.claude/skills/railway-deployment/scripts/pre-deploy-check.sh

# Validates:
# - Railway authentication
# - Project linked
# - Environment selected
# - No pending deployments
# - Variables configured
```

---

## Related Skills

- **railway-auth**: Authenticate with Railway CLI and manage tokens
- **railway-project-management**: Create projects, manage environments, configure variables
- **railway-observability**: Monitor metrics, logs, and traces
- **railway-api**: GraphQL API automation for advanced workflows

---

## Additional Resources

- **References**:
  - `references/deployment-sources.md`: GitHub, Docker, and local deployment details
  - `references/rollback-strategies.md`: Comprehensive rollback procedures
  - `references/staging-workflow.md`: Staging → production best practices

- **Scripts**:
  - `scripts/deploy.sh`: Smart deployment with health checks
  - `scripts/rollback.sh`: Safe rollback with confirmation
  - `scripts/verify-health.sh`: Automated health validation
  - `scripts/pre-deploy-check.sh`: Pre-deployment validation
  - `scripts/promote-to-production.sh`: Staging → production automation

- **Railway Documentation**:
  - [Deployments](https://docs.railway.app/reference/deployments)
  - [CLI Commands](https://docs.railway.app/reference/cli-api)
  - [GitHub Integration](https://docs.railway.app/guides/github-integration)
  - [Docker Deployments](https://docs.railway.app/guides/dockerfiles)

---

**Last Updated**: November 2025
**Status**: Production-ready
**Version**: 1.0.0
