---
name: gh-pages-deploy
description: Deploy static or interactive frontend content to GitHub Pages using gh CLI. Use when the user wants to publish, share, or make accessible any HTML/CSS/JS content - including demos, prototypes, visualizations, landing pages, portfolios, documentation, interactive tools, games, or any browser-based project. Activate whenever content needs to be publicly viewable via URL, not just when "website" is explicitly mentioned.
version: "1.0.0"
author: aviz85
tags:
  - deployment
  - github
  - hosting
  - frontend
---

# GitHub Pages Deployment

Deploy static frontend websites to GitHub Pages using the GitHub CLI.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Git installed
- A frontend project (HTML, CSS, JS) ready to deploy

## Deployment Workflow

### 1. Initialize Git Repository (if needed)

```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. Create GitHub Repository

```bash
# Create public repo (required for free GitHub Pages)
gh repo create <repo-name> --public --source=. --push
```

### 3. Enable GitHub Pages

```bash
# Enable GitHub Pages from main branch root
gh api repos/{owner}/{repo}/pages -X POST -f build_type=legacy -f source='{"branch":"main","path":"/"}'
```

Or for docs folder:
```bash
gh api repos/{owner}/{repo}/pages -X POST -f build_type=legacy -f source='{"branch":"main","path":"/docs"}'
```

### 4. Check Deployment Status

```bash
# Get pages info
gh api repos/{owner}/{repo}/pages

# View deployment status
gh api repos/{owner}/{repo}/pages/builds/latest
```

### 5. Get Site URL

The site will be available at: `https://<username>.github.io/<repo-name>/`

## Quick Deploy Script

For a complete deployment in one flow:

```bash
# Variables
REPO_NAME="my-site"

# Initialize and commit
git init
git add .
git commit -m "Initial commit"

# Create repo and push
gh repo create $REPO_NAME --public --source=. --push

# Wait for push to complete, then enable pages
sleep 2
OWNER=$(gh api user --jq '.login')
gh api repos/$OWNER/$REPO_NAME/pages -X POST -f build_type=legacy -f source='{"branch":"main","path":"/"}'

# Get the URL
echo "Site will be at: https://$OWNER.github.io/$REPO_NAME/"
```

## Troubleshooting

- **Pages not enabled**: Ensure repo is public or you have GitHub Pro
- **404 error**: Wait 1-2 minutes for deployment, check if index.html exists at root
- **Build failed**: Check GitHub Actions tab for errors

## Updating the Site

After making changes:
```bash
git add .
git commit -m "Update site"
git push
```

GitHub Pages will automatically rebuild.
