---
name: railway-automation
description: Railway CI/CD integration and automation. Use when setting up GitHub Actions, GitLab CI, automated deployments, migration scripts, or programmatic Railway workflows.
---

# Railway CI/CD Automation

Automate Railway deployments with CI/CD pipelines, migration scripts, and event-driven workflows.

## Quick Start

**GitHub Actions (5 minutes)**
```yaml
# .github/workflows/railway.yml
- uses: railway/deploy@v1
  with:
    railway_token: ${{ secrets.RAILWAY_TOKEN }}
    service: api
```

**GitLab CI (5 minutes)**
```yaml
# .gitlab-ci.yml
deploy:
  script:
    - railway up --service api
  only: [main]
```

**Migration (10 minutes)**
```bash
./scripts/migrate.sh --from heroku --project myapp
```

## Workflow Overview

### 1. GitHub Actions Integration

**Setup Process**
1. Generate Railway token (`railway login && railway token`)
2. Add token to GitHub secrets (`RAILWAY_TOKEN`)
3. Create workflow file (`.github/workflows/railway.yml`)
4. Configure deployment triggers
5. Test with PR or push

**Use Cases**
- Deploy on push to main/staging
- PR preview environments
- Multi-environment promotion
- Scheduled deployments
- Manual approval gates

**Template**: See `templates/github-workflow.yml`

**Reference**: `references/github-actions.md` for complete guide with 5+ workflow examples

---

### 2. GitLab CI Integration

**Setup Process**
1. Generate Railway token
2. Add to GitLab CI/CD variables (`RAILWAY_TOKEN`)
3. Create `.gitlab-ci.yml`
4. Define stages (test → staging → production)
5. Configure manual gates

**Use Cases**
- Multi-stage pipelines
- Environment-specific deployments
- Review apps for merge requests
- Parallel service deployments
- Artifact-based deployments

**Template**: See `templates/gitlab-ci.yml`

**Reference**: `references/gitlab-ci.md` for complete guide with pipeline examples

---

### 3. Custom CI/CD Integration

**Generic Pattern (Any Platform)**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login with token
export RAILWAY_TOKEN=$YOUR_TOKEN

# Link project
railway link $PROJECT_ID

# Deploy
railway up --service $SERVICE_NAME --environment $ENVIRONMENT
```

**Environment Variables**
- `RAILWAY_TOKEN`: Authentication token
- `RAILWAY_PROJECT_ID`: Project identifier (optional if linked)
- `RAILWAY_SERVICE`: Service name (optional)
- `RAILWAY_ENVIRONMENT`: Environment name (optional)

**Health Check Pattern**
```bash
# Deploy and wait for health
railway up --service api
sleep 30

# Verify deployment
DEPLOY_URL=$(railway status --json | jq -r '.url')
curl -f $DEPLOY_URL/health || exit 1
```

**Supported Platforms**
- CircleCI
- Travis CI
- Jenkins
- Bitbucket Pipelines
- Azure DevOps
- Any platform with shell access

---

### 4. Migration Automation

**Interactive Migration Script**
```bash
# From Heroku
./scripts/migrate.sh --from heroku --project myapp

# From Vercel
./scripts/migrate.sh --from vercel --project myapp --env production

# Dry run (preview changes)
./scripts/migrate.sh --from render --project myapp --dry-run
```

**Script Features**
- Platform detection
- Environment variable export/import
- Railway project creation
- Service configuration
- Database migration
- DNS cutover planning
- Verification checks

**Supported Migrations**
- Heroku → Railway
- Vercel → Railway
- Render → Railway
- Docker Compose → Railway
- Kubernetes → Railway

**Reference**: `references/migration-patterns.md` for detailed guides per platform

---

### 5. Scheduled Tasks

**Cron-Based Deployments**
```yaml
# GitHub Actions - Deploy every night at 2 AM
on:
  schedule:
    - cron: '0 2 * * *'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
```

**Database Backups**
```yaml
# Scheduled backup workflow
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  backup:
    steps:
      - name: Backup database
        run: |
          railway run pg_dump > backup.sql
          aws s3 cp backup.sql s3://backups/$(date +%Y%m%d).sql
```

**Health Check Monitoring**
```yaml
# Hourly health checks
on:
  schedule:
    - cron: '0 * * * *'

jobs:
  health:
    steps:
      - name: Check service health
        run: |
          curl -f ${{ secrets.SERVICE_URL }}/health || \
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"Service down!"}'
```

---

### 6. Webhook Integration

**GitHub Webhook → Railway Deploy**
```javascript
// Webhook handler
app.post('/webhook/github', async (req, res) => {
  const { ref, repository } = req.body;

  if (ref === 'refs/heads/main') {
    const { exec } = require('child_process');
    exec('railway up --service api', (error, stdout) => {
      console.log(stdout);
    });
  }

  res.json({ status: 'ok' });
});
```

**Railway Webhook Events**
Railway supports webhooks for:
- Deployment started
- Deployment completed
- Deployment failed
- Service crashed
- Build logs

**Configure Webhooks**
```bash
# Via Railway CLI
railway webhooks add \
  --url https://yourapp.com/webhook \
  --events deployment.success,deployment.failure

# Via API
curl -X POST https://backboard.railway.app/graphql \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "query": "mutation { webhookCreate(input: {...}) }"
  }'
```

**Notification Integration**
```bash
# Slack notification on deploy
railway webhooks add \
  --url $SLACK_WEBHOOK_URL \
  --events deployment.success \
  --transform '{
    "text": "Deployed {{service}} to {{environment}}"
  }'
```

---

## Common Patterns

### Multi-Environment Deployment
```yaml
# Deploy to staging first, then production
jobs:
  staging:
    environment: staging
    steps:
      - uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          environment: staging

  production:
    needs: staging
    environment: production
    steps:
      - uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          environment: production
```

### PR Preview Environments
```yaml
# Create preview for each PR
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  preview:
    steps:
      - uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: api-pr-${{ github.event.pull_request.number }}
```

### Rollback on Failure
```yaml
# Automatic rollback if health check fails
jobs:
  deploy:
    steps:
      - name: Deploy
        id: deploy
        run: railway up --service api

      - name: Health check
        run: curl -f $SERVICE_URL/health

      - name: Rollback on failure
        if: failure()
        run: railway rollback --service api
```

### Matrix Deployments
```yaml
# Deploy multiple services in parallel
strategy:
  matrix:
    service: [api, worker, cron]

steps:
  - uses: railway/deploy@v1
    with:
      railway_token: ${{ secrets.RAILWAY_TOKEN }}
      service: ${{ matrix.service }}
```

---

## Token Management

**Generate Token**
```bash
# CLI method
railway login
railway token

# Copy token to clipboard
railway token | pbcopy  # macOS
railway token | xclip   # Linux
```

**Add to CI Platform**

**GitHub**
```
Settings → Secrets and variables → Actions → New repository secret
Name: RAILWAY_TOKEN
Value: [paste token]
```

**GitLab**
```
Settings → CI/CD → Variables → Add variable
Key: RAILWAY_TOKEN
Value: [paste token]
Protected: Yes
Masked: Yes
```

**CircleCI**
```
Project Settings → Environment Variables → Add Variable
Name: RAILWAY_TOKEN
Value: [paste token]
```

**Token Rotation**
```bash
# Generate new token
NEW_TOKEN=$(railway token)

# Update in CI (platform-specific)
# Then invalidate old token via dashboard
```

---

## Environment-Specific Configuration

**Detect Environment in Code**
```javascript
const env = process.env.RAILWAY_ENVIRONMENT || 'development';

const config = {
  development: { db: 'localhost:5432' },
  staging: { db: process.env.DATABASE_URL },
  production: { db: process.env.DATABASE_URL }
};

export default config[env];
```

**Conditional Deployment**
```yaml
# Only deploy staging on feature branches
jobs:
  deploy-staging:
    if: github.ref != 'refs/heads/main'
    steps:
      - uses: railway/deploy@v1
        with:
          environment: staging

  deploy-production:
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: railway/deploy@v1
        with:
          environment: production
```

**Environment Variable Management**
```bash
# Export from staging
railway env --environment staging > .env.staging

# Import to production (selective)
cat .env.staging | grep -v SECRET | railway env --environment production
```

---

## Best Practices

### Security
- Use masked/protected CI variables
- Rotate tokens quarterly
- Use service tokens (not personal) for production
- Never commit tokens to git
- Limit token scope to specific projects

### Performance
- Cache dependencies in CI
- Use Railway's built-in caching
- Deploy only changed services
- Run tests before deploy
- Use health checks before traffic

### Reliability
- Always include rollback mechanism
- Monitor deployment notifications
- Set deployment timeouts
- Use staging before production
- Test migrations in preview environments

### Monitoring
- Log all deployments
- Track deployment duration
- Alert on failures
- Monitor health checks
- Track rollback frequency

---

## Troubleshooting

**Deployment Fails in CI**
```bash
# Check token validity
railway whoami

# Verify project link
railway status

# Check service exists
railway list

# View deployment logs
railway logs --service api
```

**Token Authentication Errors**
```bash
# Regenerate token
railway logout
railway login
railway token

# Update in CI secrets
# Test locally first
RAILWAY_TOKEN=$NEW_TOKEN railway status
```

**Environment Not Found**
```bash
# List available environments
railway environment list

# Verify environment name matches
railway status --environment production
```

**Service Not Deploying**
```bash
# Check service name
railway list

# Verify service configuration
railway status --service api

# Check for build errors
railway logs --service api --deployment latest
```

---

## Related Skills

- **railway-auth**: Token management and authentication setup
- **railway-api**: Programmatic Railway API automation
- **railway-deployment**: Deployment patterns and strategies
- **railway-database**: Database automation and backups
- **railway-monitoring**: Health checks and alerting

---

## References

- **references/github-actions.md**: Complete GitHub Actions guide with 5+ workflow examples
- **references/gitlab-ci.md**: Complete GitLab CI guide with pipeline examples
- **references/migration-patterns.md**: Platform migration guides (Heroku, Vercel, Render, etc.)

## Templates

- **templates/github-workflow.yml**: Production-ready GitHub Actions template
- **templates/gitlab-ci.yml**: Production-ready GitLab CI template

## Scripts

- **scripts/migrate.sh**: Interactive migration script supporting multiple platforms
