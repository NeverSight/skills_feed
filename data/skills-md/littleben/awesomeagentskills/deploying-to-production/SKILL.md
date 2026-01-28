---
name: Deploying to Production
description: Automates GitHub repository creation and Vercel deployment for Next.js websites. Use when deploying new websites, pushing to production, setting up CI/CD pipelines, or when the user mentions deployment, GitHub, Vercel, or going live.
---

# Deploying to Production

Automated deployment workflow for Next.js websites using GitHub and Vercel.

## When to use this Skill

- Creating a new website and need to deploy it
- Setting up GitHub repository for version control
- Deploying to Vercel production environment
- User mentions: "deploy", "GitHub", "Vercel", "go live", "publish"

## Deployment Workflow

Copy this checklist and track your progress:

```
Deployment Progress:
- [ ] Step 1: Pre-deployment validation (build + E-E-A-T check)
- [ ] Step 2: Create GitHub repository
- [ ] Step 3: Push code to GitHub
- [ ] Step 4: Deploy to Vercel
- [ ] Step 5: Post-deployment verification
```

### Step 1: Pre-deployment validation

**Run build and verify no errors**:
```bash
cd "$PROJECT_DIR"
npm run build
```

**CRITICAL: Only proceed if build succeeds with no errors.**

**Pre-deployment checklist** - See [CHECKLIST.md](CHECKLIST.md) for complete list:
- [ ] `npm run build` completes successfully
- [ ] All environment variables configured
- [ ] E-E-A-T elements present (About page, author info)
- [ ] Core Web Vitals acceptable
- [ ] SEO meta tags complete

### Step 2: Create GitHub repository

Run the script to create a private GitHub repository:

```bash
bash scripts/create-github-repo.sh <project-name>
```

**What this script does**:
- Creates a private GitHub repository
- Initializes Git (if needed)
- Commits all changes
- Pushes to GitHub

**If the script fails**, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

### Step 3: Verify GitHub push

Check the repository URL:
```bash
gh repo view --web
```

Verify all files are pushed correctly.

### Step 4: Deploy to Vercel

Run the deployment script:

```bash
bash scripts/deploy-to-vercel.sh <project-name>
```

**What this script does**:
- Links the project to Vercel
- Deploys to production environment
- Returns deployment URL

**If deployment fails**, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

### Step 5: Post-deployment verification

**Verify deployment**:
1. Visit the deployment URL
2. Test core functionality:
   - Homepage loads correctly
   - Navigation works
   - Core features functional
3. Check Core Web Vitals (use PageSpeed Insights)
4. Verify SEO meta tags (use browser inspector)

**If issues found**:
- Review Vercel build logs: `vercel logs`
- Check environment variables in Vercel dashboard
- Verify DNS settings (if custom domain)
- Return to Step 1 and fix issues

**Only mark deployment complete when all verifications pass.**

## Script locations

All deployment scripts are in the `scripts/` directory:
- `create-github-repo.sh` - GitHub repository creation
- `deploy-to-vercel.sh` - Vercel deployment

## Important notes

**Prerequisites**:
- GitHub CLI (`gh`) installed and authenticated
- Vercel CLI installed and authenticated
- Project must be in `/Volumes/Time/go to wild/websites/` directory

**Project naming convention**:
- Format: `keyword-site-lang` (e.g., `pdf-converter-jp`)
- Use lowercase and hyphens only

**Environment variables**:
- Configure in Vercel dashboard after first deployment
- Required variables depend on project features (database, auth, etc.)

## Next steps after deployment

1. **Set up monitoring**:
   - Add Google Analytics or Plausible
   - Configure Google Search Console
   - Set up Vercel Analytics

2. **Configure custom domain** (if needed):
   - Add domain in Vercel dashboard
   - Update DNS records
   - Wait for SSL certificate

3. **Enable automatic deployments**:
   - Push to `main` branch auto-deploys to production
   - Push to other branches creates preview deployments

For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
