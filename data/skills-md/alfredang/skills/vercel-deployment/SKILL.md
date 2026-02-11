---
name: vercel-deployment
description: Deploy projects to Vercel with automatic configuration. Sets project name from folder name, deploys with --yes flag, and disables Vercel Authentication (SSO protection) post-deploy via API. Use when deploying to Vercel, running "deploy to vercel", "vercel deploy", or any Vercel deployment task. Handles both preview and production deployments.
---

# Vercel Deployment

Deploy to Vercel with automatic project naming from the folder name and auto-disable of Vercel Authentication after deployment.

## Workflow

### Phase 1: Pre-flight Checks

1. Verify Vercel CLI is installed (`vercel --version`). If not: `npm i -g vercel`
2. Verify authentication: `vercel whoami`. If not logged in: `vercel login`
3. Determine project name from the **current working directory folder name** using `basename "$(pwd)"`

### Phase 2: Deploy

Deploy using the `--yes` flag to skip interactive prompts. The project name is inferred from the folder name automatically.

**Preview deployment (default):**
```bash
vercel --yes
```

**Production deployment:**
```bash
vercel --yes --prod
```

The `--yes` flag auto-confirms project setup using the folder name as the project name.

### Phase 3: Disable Vercel Authentication

After deployment, disable Vercel Authentication (SSO protection) so the deployment is publicly accessible without Vercel login.

#### Option A: Using the deploy script (preferred)

Run the bundled script which handles deployment + auth disable in one step:

```bash
# Set token for API access
export VERCEL_TOKEN="<token>"
# Optional: set team ID if using a team
export VERCEL_TEAM_ID="<team-id>"

# Preview deploy
bash scripts/deploy.sh /path/to/project

# Production deploy
bash scripts/deploy.sh /path/to/project prod
```

#### Option B: Manual API call after deploying

Use the Vercel API to disable `ssoProtection` on the project:

```bash
PROJECT_NAME=$(basename "$(pwd)")

curl -X PATCH "https://api.vercel.com/v9/projects/$PROJECT_NAME" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ssoProtection": null}'
```

For team projects, append `?teamId=<TEAM_ID>` to the URL.

#### Option C: Using Vercel CLI curl

```bash
vercel curl -X PATCH "/v9/projects/$(basename "$(pwd)")" \
  -H "Content-Type: application/json" \
  -d '{"ssoProtection": null}'
```

### Phase 4: Verify

1. Confirm deployment URL is accessible without Vercel login
2. Print the deployment URL for the user

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VERCEL_TOKEN` | For auth disable | API token from https://vercel.com/account/tokens |
| `VERCEL_TEAM_ID` | For team projects | Team ID from Vercel dashboard |

## Notes

- The `--yes` flag uses the folder name as the project name by default
- If `VERCEL_TOKEN` is not set, deployment still works but Vercel Authentication won't be auto-disabled. Inform the user they can disable it manually in: **Vercel Dashboard > Project > Settings > Deployment Protection > Vercel Authentication > Off**
- Setting `ssoProtection` to `null` disables Vercel Authentication for all deployments (preview and production)
