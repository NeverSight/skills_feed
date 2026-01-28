---
name: deploy
description: Deploy the Pitfal Solutions website to AWS. Use when user says deploy, push to production, or update live site. Runs pre-checks, builds Next.js, deploys Terraform infrastructure, syncs to S3, and invalidates CloudFront cache.
---

# Deploy to AWS

Deploy the Pitfal Solutions website following this sequence:

## Pre-deployment Checks
1. Verify all tests pass: `pnpm test`
2. Verify TypeScript compiles: `pnpm type-check`
3. Check for uncommitted changes: `git status`

## Build Process
1. Build the Next.js application: `pnpm build`
2. Verify the `out/` directory was created

## Infrastructure Deployment
1. Navigate to terraform: `cd infrastructure/terraform`
2. Initialize if needed: `terraform init`
3. Plan changes: `terraform plan -out=tfplan`
4. Show plan summary to user and confirm before applying
5. Apply changes: `terraform apply tfplan`

## Static Site Deployment
1. Sync static assets to S3:
   ```bash
   aws s3 sync out/ s3://pitfal-static-site \
     --delete \
     --cache-control "public, max-age=31536000, immutable" \
     --exclude "*.html" \
     --profile pitfal
   ```
2. Sync HTML with no-cache:
   ```bash
   aws s3 sync out/ s3://pitfal-static-site \
     --cache-control "public, max-age=0, must-revalidate" \
     --include "*.html" \
     --profile pitfal
   ```

## Post-deployment
1. Get CloudFront Distribution ID (if not already known):
   ```bash
   # Option 1: From Terraform output
   cd infrastructure/terraform && terraform output cloudfront_distribution_id

   # Option 2: From AWS CLI (finds distribution for pitfal.solutions)
   aws cloudfront list-distributions --profile pitfal \
     --query "DistributionList.Items[?contains(Aliases.Items, 'pitfal.solutions')].Id" \
     --output text

   # Option 3: Export as environment variable for reuse
   export DISTRIBUTION_ID=$(terraform -chdir=infrastructure/terraform output -raw cloudfront_distribution_id)
   ```

2. Invalidate CloudFront cache:
   ```bash
   aws cloudfront create-invalidation \
     --distribution-id $DISTRIBUTION_ID \
     --paths "/*" \
     --profile pitfal
   ```
   Note: Cache invalidation takes 1-5 minutes to propagate globally.

3. Verify site is accessible at https://pitfal.solutions
4. Run smoke tests if available

## Rollback
If deployment fails:
1. Check Terraform state: `terraform state list`
2. Restore previous S3 version if needed
3. Provide specific rollback instructions based on failure point
