---
name: GitHub Pages
description: Deploy to GitHub Pages with auto-generated Actions workflow. Detects project type, creates deploy workflow, enables GitHub Pages and Actions automatically via API. Use when deploying static sites, React, Vite, or Next.js apps to GitHub Pages.
---

# GitHub Pages Deployment

## Command
`/github-page` or `github-page`

## Navigate
Deployment

## Keywords
github pages, deploy pages, static site, gh-pages, github actions, deploy website, host website, github hosting, deploy static, pages deploy, free hosting, github site, publish site, deploy html, deploy react to github

## Description
Deploy any project to GitHub Pages with zero manual configuration. Automatically detects your project type, generates the correct GitHub Actions workflow, enables GitHub Pages and Actions on the repo via API, and gives you a live URL.

## Execution
This skill runs using **Claude Code with subscription plan**. Do NOT use pay-as-you-go API keys. All AI operations should be executed through the Claude Code CLI environment with an active subscription.

## Response
I'll help you deploy to GitHub Pages!

The workflow includes:

| Step | Description |
|------|-------------|
| **Pre-flight** | Verify `gh` CLI, git remote, and repo access |
| **Detect Project** | Auto-detect project type and build config |
| **Generate Workflow** | Create `.github/workflows/deploy-pages.yml` |
| **Push & Enable** | Push workflow, enable GitHub Pages + Actions via API |
| **Verify** | Confirm deployment and provide live URL |

## Instructions

When executing `/github-page`, follow this workflow:

### Phase 1: Pre-flight Checks

#### 1.1 Verify GitHub CLI
```bash
gh --version
```

If not installed, inform the user:
```
ERROR: GitHub CLI (gh) not found.
Install: https://cli.github.com/
```

#### 1.2 Verify & Auto-Authenticate
```bash
gh auth status
```

If not authenticated, automatically initiate browser-based login:
```bash
gh auth login --hostname github.com --git-protocol https --web
```

This opens the user's browser for OAuth authentication — no manual steps required. After login completes, verify success:
```bash
gh auth status
```

If authentication still fails after the browser flow (e.g., user cancelled):
```
ERROR: GitHub CLI authentication failed.
Please try again or run manually: gh auth login
```

#### 1.3 Verify Git Remote
```bash
git remote get-url origin
```

Extract OWNER and REPO from the remote URL:
```bash
# For HTTPS: https://github.com/OWNER/REPO.git
# For SSH: git@github.com:OWNER/REPO.git
REMOTE_URL=$(git remote get-url origin)
OWNER=$(echo "$REMOTE_URL" | sed -E 's#.*(github\.com)[:/]([^/]+)/([^/.]+)(\.git)?$#\2#')
REPO=$(echo "$REMOTE_URL" | sed -E 's#.*(github\.com)[:/]([^/]+)/([^/.]+)(\.git)?$#\3#')
```

If no remote exists:
```
ERROR: No GitHub remote found.
Add one with: git remote add origin https://github.com/USER/REPO.git
```

### Phase 2: Detect Project Type

Analyze the project to determine build commands and output directory.

#### 2.1 Detection Rules

| Indicator | Project Type | Build Command | Output Dir |
|-----------|-------------|---------------|------------|
| `vite.config.*` | Vite (React/Vue/Svelte) | `npm install && npm run build` | `./dist` |
| `next.config.*` | Next.js (static export) | `npm install && npm run build` | `./out` |
| `angular.json` | Angular | `npm install && npm run build` | `./dist/<project>` |
| `package.json` with `build` script | Node.js project | `npm install && npm run build` | `./dist` or `./build` |
| `index.html` in root | Static HTML | None | `./` |
| `public/index.html` | Static in public/ | None | `./public` |
| `requirements.txt` + `mkdocs.yml` | MkDocs | `pip install -r requirements.txt && mkdocs build` | `./site` |
| None of the above | Unknown | Ask user | Ask user |

#### 2.2 Framework-Specific Configuration

**Vite projects** — Ensure `base` is set in `vite.config.*`:
```js
export default defineConfig({
  base: '/<REPO>/',
})
```
Inform the user if `base` is not set — the site will have broken asset paths without it.

**Next.js projects** — Ensure `output: 'export'` is in `next.config.*`:
```js
const nextConfig = {
  output: 'export',
  basePath: '/<REPO>',
}
```

#### 2.3 Node.js Version Detection

Check for `.nvmrc`, `.node-version`, or `engines.node` in `package.json` to set the correct Node.js version in the workflow. Default to `20` if not specified.

### Phase 3: Generate GitHub Actions Workflow

Create `.github/workflows/deploy-pages.yml`:

#### 3.1 Static HTML (No Build Step)

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v4
        with:
          path: '.'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

#### 3.2 Node.js Project (React/Vite/Next.js/Angular)

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '<NODE_VERSION>'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v4
        with:
          path: '<OUTPUT_DIR>'

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

Replace `<NODE_VERSION>` and `<OUTPUT_DIR>` with detected values from Phase 2.

#### 3.3 Create the Workflow File

```bash
mkdir -p .github/workflows
```

Write the appropriate workflow YAML to `.github/workflows/deploy-pages.yml`.

### Phase 4: Enable GitHub Pages & Actions (Auto-configure)

#### 4.1 Commit and Push the Workflow

```bash
git add .github/workflows/deploy-pages.yml
git commit -m "$(cat <<'EOF'
ci: add GitHub Pages deployment workflow

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
git push origin main
```

**Important:** Always add specific files. Never use `git add .` or `git add -A`.

#### 4.2 Enable GitHub Pages via API

First, check if Pages is already enabled:
```bash
gh api "/repos/$OWNER/$REPO/pages" 2>/dev/null
```

If not enabled (404 response), create it:
```bash
gh api -X POST "/repos/$OWNER/$REPO/pages" -f build_type=workflow
```

If already enabled but using a different source, update it:
```bash
gh api -X PUT "/repos/$OWNER/$REPO/pages" -f build_type=workflow
```

#### 4.3 Enable the Workflow

```bash
gh workflow enable deploy-pages.yml
```

#### 4.4 Trigger Initial Deployment (if push didn't trigger it)

```bash
gh workflow run deploy-pages.yml
```

### Phase 5: Verify & Report

#### 5.1 Check Workflow Run

Wait a few seconds, then check:
```bash
gh run list --workflow=deploy-pages.yml --limit 1
```

#### 5.2 Print Results

```
=== GitHub Pages Deployment ===

Workflow: .github/workflows/deploy-pages.yml (created)
GitHub Pages: ENABLED (source: GitHub Actions)
GitHub Actions: ENABLED

Deployment URL: https://<OWNER>.github.io/<REPO>/
Workflow runs: https://github.com/<OWNER>/<REPO>/actions

Status: Deploying... (check Actions tab for progress)
```

#### 5.3 If Errors Occur

**Pages API returns 409 (conflict):**
- Pages may already be configured with a branch source
- Update with PUT instead of POST

**Workflow not triggering:**
- Ensure the branch name matches (main vs master)
- Check if Actions are enabled at the repo level:
  ```bash
  gh api -X PUT "/repos/$OWNER/$REPO/actions/permissions" -f enabled=true
  ```

**Build fails:**
- Check the workflow run logs:
  ```bash
  gh run view --log
  ```
- Common issues: missing `base` config for Vite, missing `output: 'export'` for Next.js

## Capabilities

- Auto-detect project type (static HTML, React, Vite, Next.js, Angular, MkDocs)
- Generate correct GitHub Actions workflow for the project
- Enable GitHub Pages with Actions source via API
- Enable GitHub Actions on the repo automatically
- Trigger initial deployment
- Support for custom build commands and output directories
- Node.js version detection from project config

## Next Steps

After running `/github-page`:
1. Check the Actions tab: `https://github.com/<OWNER>/<REPO>/actions`
2. Wait for the first deployment to complete (usually 1-2 minutes)
3. Visit your live site: `https://<OWNER>.github.io/<REPO>/`
4. For custom domains, configure in repo Settings > Pages > Custom domain
5. Future pushes to `main` will auto-deploy via the workflow
