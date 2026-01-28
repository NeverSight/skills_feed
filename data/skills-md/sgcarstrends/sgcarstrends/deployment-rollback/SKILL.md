---
name: deployment-rollback
description: Rollback failed deployments, restore previous versions, and handle deployment emergencies. Use when deployments fail, bugs are discovered in production, or emergency recovery is needed.
allowed-tools: Read, Edit, Write, Bash, Grep
---

# Deployment Rollback Skill

This skill helps you safely rollback failed deployments and restore previous working versions.

## When to Use This Skill

- Deployment failures
- Critical bugs in production
- Performance degradation after deployment
- Security vulnerabilities discovered
- Database migration issues
- Emergency recovery situations

## Rollback Strategy

### Deployment Stages

```
Development → Staging → Production
     ↓           ↓          ↓
   Rollback   Rollback   Rollback
```

**Rollback Points:**
1. **Before deployment**: Cancel deployment
2. **During deployment**: Stop and revert
3. **After deployment**: Quick rollback to previous version

## SST Rollback

### Quick Rollback

```bash
# View deployment history
sst version list

# Output:
# Version  Stage       Deployed
# v1.2.0   production  2024-01-15 10:00:00
# v1.1.0   production  2024-01-10 09:30:00
# v1.0.0   production  2024-01-05 08:00:00

# Rollback to previous version
sst deploy --stage production --to v1.1.0

# Or rollback to specific git commit
git checkout v1.1.0
sst deploy --stage production
```

### Service-Specific Rollback

```bash
# Rollback API only
sst deploy api --stage production --to v1.1.0

# Rollback Web only
sst deploy web --stage production --to v1.1.0

# Rollback infrastructure only
sst deploy --stage production --only infra --to v1.1.0
```

## Database Rollback

### Migration Rollback

```bash
# Check current migration status
pnpm -F @sgcarstrends/database db:status

# Rollback last migration
pnpm -F @sgcarstrends/database db:rollback

# Rollback to specific migration
pnpm -F @sgcarstrends/database db:rollback --to 20240115_initial

# Rollback multiple migrations
pnpm -F @sgcarstrends/database db:rollback --step 3
```

### Backup and Restore

```bash
# Create backup before deployment
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d-%H%M%S).sql

# Restore from backup
psql $DATABASE_URL < backup-20240115-100000.sql

# Or use automated backup
# Restore from RDS snapshot (AWS)
aws rds restore-db-instance-from-snapshot \
  --db-instance-identifier sgcarstrends-restored \
  --db-snapshot-identifier sgcarstrends-snapshot-20240115
```

## Lambda Rollback

### AWS Lambda Version Rollback

```bash
# List Lambda versions
aws lambda list-versions-by-function \
  --function-name sgcarstrends-api-prod

# Update alias to previous version
aws lambda update-alias \
  --function-name sgcarstrends-api-prod \
  --name production \
  --function-version 42  # Previous working version

# Verify rollback
aws lambda get-alias \
  --function-name sgcarstrends-api-prod \
  --name production
```

### Lambda Environment Variable Rollback

```bash
# Get previous configuration
aws lambda get-function-configuration \
  --function-name sgcarstrends-api-prod \
  --qualifier 42  # Previous version

# Update environment variables
aws lambda update-function-configuration \
  --function-name sgcarstrends-api-prod \
  --environment Variables="{KEY1=value1,KEY2=value2}"
```

## Next.js Rollback

### Vercel/AWS Rollback

```bash
# If deployed with SST
sst deploy web --stage production --to v1.1.0

# If using custom deployment
# Redeploy previous version
git checkout v1.1.0
pnpm -F @sgcarstrends/web build
pnpm -F @sgcarstrends/web deploy:prod

# Or point CloudFront to previous S3 deployment
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

## Git-Based Rollback

### Revert Deployment Commit

```bash
# Find deployment commit
git log --oneline

# Revert specific commit
git revert <commit-hash>

# Or revert multiple commits
git revert <commit1>..<commit2>

# Push revert
git push origin main

# CI automatically deploys reverted version
```

### Reset to Previous Version

```bash
# Create rollback branch
git checkout -b rollback/v1.1.0

# Reset to previous version
git reset --hard v1.1.0

# Force push (use with caution)
git push origin rollback/v1.1.0 --force

# Create PR to merge rollback
gh pr create --title "Rollback to v1.1.0" --body "Emergency rollback"
```

## Automated Rollback

### Health Check-Based Rollback

```yaml
# .github/workflows/deploy-with-rollback.yml
name: Deploy with Rollback

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get previous version
        id: prev
        run: |
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^)
          echo "tag=$PREV_TAG" >> $GITHUB_OUTPUT

      - name: Deploy
        id: deploy
        run: pnpm deploy:prod

      - name: Health check
        id: health
        run: |
          sleep 30  # Wait for deployment
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.sgcarstrends.com/health)
          if [ $STATUS -ne 200 ]; then
            echo "Health check failed: $STATUS"
            exit 1
          fi

      - name: Smoke tests
        if: success()
        run: pnpm test:e2e:prod

      - name: Rollback on failure
        if: failure()
        run: |
          echo "Deployment failed, rolling back to ${{ steps.prev.outputs.tag }}"
          git checkout ${{ steps.prev.outputs.tag }}
          pnpm deploy:prod

      - name: Notify on rollback
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          payload: |
            {
              "text": "🚨 Deployment failed and was rolled back to ${{ steps.prev.outputs.tag }}"
            }
```

## Rollback Checklist

### Pre-Rollback

- [ ] Identify issue and severity
- [ ] Determine rollback scope (full/partial)
- [ ] Check backup availability
- [ ] Notify team of rollback
- [ ] Document reason for rollback

### During Rollback

- [ ] Stop incoming traffic (if critical)
- [ ] Rollback application code
- [ ] Rollback database if needed
- [ ] Clear caches (Redis, CDN)
- [ ] Verify health checks pass
- [ ] Run smoke tests

### Post-Rollback

- [ ] Monitor error rates
- [ ] Verify functionality restored
- [ ] Notify team of completion
- [ ] Document what went wrong
- [ ] Create postmortem
- [ ] Fix root cause
- [ ] Plan re-deployment

## Rollback Scenarios

### Scenario 1: Critical Bug in Production

```bash
# 1. Assess impact
# Check error rates, user reports

# 2. Quick rollback via SST
sst deploy --stage production --to v1.1.0

# 3. Verify rollback
curl https://api.sgcarstrends.com/health

# 4. Clear CDN cache
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"

# 5. Monitor
# Check logs, metrics, error rates

# 6. Communicate
# Update status page, notify users
```

### Scenario 2: Database Migration Failure

```bash
# 1. Stop application (prevent data corruption)
# Scale down or put in maintenance mode

# 2. Rollback migration
pnpm -F @sgcarstrends/database db:rollback

# 3. Restore from backup if needed
psql $DATABASE_URL < backup-latest.sql

# 4. Verify database state
pnpm -F @sgcarstrends/database db:status

# 5. Rollback application code
git checkout v1.1.0
pnpm deploy:prod

# 6. Resume application
# Remove maintenance mode
```

### Scenario 3: Performance Degradation

```bash
# 1. Check metrics
# Response times, CPU, memory usage

# 2. Quick rollback
sst deploy --stage production --to v1.1.0

# 3. Clear caches
redis-cli FLUSHALL
aws cloudfront create-invalidation --distribution-id E123 --paths "/*"

# 4. Monitor performance
# Check if performance restored

# 5. Investigate
# Profile code, check database queries
```

### Scenario 4: Partial Rollback (API Only)

```bash
# Keep web app, rollback API only
# 1. Rollback API
sst deploy api --stage production --to v1.1.0

# 2. Verify API health
curl https://api.sgcarstrends.com/health

# 3. Test web app still works
# Check web app functionality

# 4. Monitor for errors
# Watch for API compatibility issues
```

## Traffic Management

### Gradual Rollback

```bash
# If using load balancer with multiple instances

# 1. Deploy old version to 50% of instances
# Update 1 instance at a time

# 2. Monitor metrics
# Check error rates on rolled-back instances

# 3. Gradually increase rollback
# Update more instances if stable

# 4. Complete rollback
# Once verified, update all instances
```

### Blue-Green Rollback

```bash
# Switch traffic back to blue environment

# 1. Update load balancer
aws elbv2 modify-listener \
  --listener-arn arn:aws:... \
  --default-actions TargetGroupArn=arn:aws:...-blue

# 2. Wait for traffic to shift
sleep 60

# 3. Verify metrics
# Check error rates on blue environment

# 4. Keep green for investigation
# Don't destroy immediately
```

## Cache Invalidation

### Clear Application Caches

```bash
# Redis cache
redis-cli -h $REDIS_HOST -p $REDIS_PORT FLUSHALL

# Or selective flush
redis-cli -h $REDIS_HOST -p $REDIS_PORT --scan --pattern "cache:*" | xargs redis-cli DEL

# Upstash Redis (via API)
curl -X POST https://your-redis.upstash.io/flushall \
  -H "Authorization: Bearer $UPSTASH_TOKEN"
```

### Clear CDN Cache

```bash
# CloudFront invalidation
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"

# Wait for invalidation
aws cloudfront wait invalidation-completed \
  --distribution-id E1234567890ABC \
  --id I2J3K4L5M6N7O8P9
```

## Monitoring During Rollback

### Health Checks

```bash
# API health
curl -f https://api.sgcarstrends.com/health || echo "API unhealthy"

# Web app health
curl -f https://sgcarstrends.com || echo "Web unhealthy"

# Database connectivity
psql $DATABASE_URL -c "SELECT 1" || echo "Database unreachable"

# Redis connectivity
redis-cli -h $REDIS_HOST ping || echo "Redis unreachable"
```

### Error Rate Monitoring

```bash
# Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-prod \
  --start-time $(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 60 \
  --statistics Sum

# Check logs for errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/sgcarstrends-api-prod \
  --start-time $(($(date +%s) - 300))000 \
  --filter-pattern "ERROR"
```

## Communication During Rollback

### Status Page Update

```markdown
# Status Page Template

## Incident: Deployment Rollback in Progress

**Status:** Investigating
**Started:** 2024-01-15 10:00 UTC
**Services Affected:** API, Web Application

### Timeline

**10:00 UTC** - Deployment completed
**10:05 UTC** - Increased error rates detected
**10:10 UTC** - Rollback initiated
**10:15 UTC** - Rollback completed
**10:20 UTC** - Services restored

### Impact

Some users may have experienced errors during the rollback.

### Next Steps

We're investigating the root cause and will provide updates.
```

### Team Notification

```bash
# Slack notification
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "🚨 Rollback in progress",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Deployment Rollback*\nRolling back from v1.2.0 to v1.1.0\nReason: Critical bug affecting user login"
        }
      }
    ]
  }'
```

## Best Practices

### 1. Always Have Backups

```bash
# ✅ Create backups before deployment
pg_dump $DATABASE_URL > backup-pre-deploy-$(date +%Y%m%d-%H%M%S).sql

# Store in S3
aws s3 cp backup.sql s3://sgcarstrends-backups/$(date +%Y%m%d)/
```

### 2. Test Rollback Procedures

```bash
# ✅ Practice rollback in staging
sst deploy --stage staging --to v1.0.0

# Verify functionality
pnpm test:e2e:staging
```

### 3. Use Feature Flags

```typescript
// ✅ Enable gradual rollout and quick disable
const ENABLE_NEW_FEATURE = process.env.ENABLE_NEW_FEATURE === "true";

if (ENABLE_NEW_FEATURE) {
  // New feature code
} else {
  // Old feature code
}

// Disable feature without rollback
// Set ENABLE_NEW_FEATURE=false
```

### 4. Monitor Continuously

```bash
# ✅ Set up alerts for key metrics
# - Error rate
# - Response time
# - CPU/Memory usage
# - Database connections
```

## Troubleshooting

### Rollback Fails

```bash
# Issue: Rollback command fails
# Solution: Manual intervention

# 1. Check current state
sst version list

# 2. Force redeploy previous version
git checkout v1.1.0
pnpm install
pnpm build
pnpm deploy:prod --force

# 3. Verify deployment
curl https://api.sgcarstrends.com/health
```

### Database Schema Mismatch

```bash
# Issue: Code rolled back but database not
# Solution: Rollback database

# 1. Rollback migrations
pnpm -F @sgcarstrends/database db:rollback

# 2. Or restore backup
psql $DATABASE_URL < backup-pre-deploy.sql

# 3. Verify schema version
pnpm -F @sgcarstrends/database db:status
```

## References

- SST Deployments: https://docs.sst.dev/deployment
- AWS Lambda Versions: https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html
- Database Migrations: https://orm.drizzle.team/docs/migrations
- Related files:
  - `.github/workflows/` - Deployment workflows
  - Root CLAUDE.md - Deployment guidelines

## Best Practices Summary

1. **Always Backup**: Create backups before deployments
2. **Test Rollback**: Practice rollback procedures in staging
3. **Monitor Closely**: Watch metrics during and after rollback
4. **Document Everything**: Record what happened and why
5. **Communicate**: Keep team and users informed
6. **Feature Flags**: Use for quick feature disabling
7. **Gradual Rollout**: Test with small percentage first
8. **Postmortem**: Learn from rollbacks to prevent recurrence
