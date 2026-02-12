---
name: slidev-deployment
description: Deploy Slidev presentations to the web. Use this skill for GitHub Pages, Netlify, Vercel, and Docker deployments.
---

# Deploying Slidev Presentations

This skill covers deploying Slidev presentations as static websites to various hosting platforms, making your presentations accessible online.

## When to Use This Skill

- Sharing presentations via URL
- Hosting for conferences/events
- Creating permanent presentation archives
- Setting up CI/CD for presentations
- Embedding presentations in websites

## Building for Production

### Build Command

```bash
npx slidev build
```

Or via npm script:
```bash
npm run build
```

### Output

Creates `dist/` directory containing:
- `index.html`
- JavaScript bundles
- CSS files
- Asset files

### Build Options

```bash
# Custom output directory
npx slidev build --out public

# With base path (for subdirectories)
npx slidev build --base /presentations/my-talk/

# Enable PDF download
npx slidev build --download

# Exclude presenter notes (security)
npx slidev build --without-notes
```

## GitHub Pages

### Method 1: GitHub Actions (Recommended)

1. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: GitHub Actions

2. **Create workflow file** `.github/workflows/deploy.yml`:

```yaml
name: Deploy Slidev

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build -- --base /${{ github.event.repository.name }}/

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

3. **Push to trigger deployment**

4. **Access at**: `https://<username>.github.io/<repo>/`

### Method 2: gh-pages Branch

```bash
npm install -D gh-pages
```

Add to `package.json`:
```json
{
  "scripts": {
    "deploy": "slidev build --base /repo-name/ && gh-pages -d dist"
  }
}
```

Then:
```bash
npm run deploy
```

## Netlify

### Method 1: Netlify UI

1. Push code to GitHub/GitLab
2. Connect repo in Netlify dashboard
3. Configure:
   - Build command: `npm run build`
   - Publish directory: `dist`

### Method 2: netlify.toml

Create `netlify.toml`:

```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Push and Netlify auto-deploys.

### Custom Domain

In Netlify dashboard:
1. Domain settings
2. Add custom domain
3. Configure DNS

## Vercel

### Method 1: Vercel CLI

```bash
npm install -g vercel
vercel
```

### Method 2: vercel.json

Create `vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": null,
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Automatic Deployment

1. Import project in Vercel dashboard
2. Connect GitHub repo
3. Vercel auto-detects and deploys

## Cloudflare Pages

### Setup

1. Connect repo in Cloudflare Pages
2. Configure:
   - Build command: `npm run build`
   - Output directory: `dist`
3. Deploy

### wrangler.toml (Optional)

```toml
name = "my-presentation"
compatibility_date = "2024-01-01"

[site]
bucket = "./dist"
```

## Docker

### Dockerfile

```dockerfile
FROM node:20-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
```

### Build and Run

```bash
docker build -t my-presentation .
docker run -p 8080:80 my-presentation
```

### Docker Compose

```yaml
version: '3.8'
services:
  presentation:
    build: .
    ports:
      - "8080:80"
    restart: unless-stopped
```

## Self-Hosted (Static Server)

### Using serve

```bash
npm install -g serve
npm run build
serve dist
```

### Using http-server

```bash
npm install -g http-server
npm run build
http-server dist
```

### Using Python

```bash
npm run build
cd dist
python -m http.server 8080
```

## Base Path Configuration

### For Subdirectories

If hosting at `https://example.com/slides/`:

```bash
npx slidev build --base /slides/
```

Or in frontmatter:

```yaml
---
base: /slides/
---
```

### Root Path

If hosting at root `https://example.com/`:

```bash
npx slidev build --base /
```

## Security Considerations

### Excluding Presenter Notes

```bash
npx slidev build --without-notes
```

Removes speaker notes from built version.

### Password Protection

For private presentations:

**Netlify**:
Use Netlify Identity or password protection feature.

**Vercel**:
Use Vercel Authentication.

**Custom**:
Add basic auth in server config.

### No Remote Control in Build

Built presentations don't include remote control by default.

## Environment Variables

### In Build

Create `.env`:

```
VITE_API_URL=https://api.example.com
```

Access in slides:
```vue
<script setup>
const apiUrl = import.meta.env.VITE_API_URL
</script>
```

### Platform-Specific

Set in platform dashboards (Netlify, Vercel, etc.)

## Custom Domain Setup

### DNS Configuration

| Type | Name | Value |
|------|------|-------|
| CNAME | www | platform-subdomain |
| A | @ | Platform IP |

### SSL/HTTPS

Most platforms provide free SSL:
- Netlify: Automatic
- Vercel: Automatic
- Cloudflare: Automatic
- GitHub Pages: Automatic

## CI/CD Workflows

### GitHub Actions (Full Example)

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install
        run: npm ci

      - name: Build
        run: npm run build

      - name: Export PDF
        run: npm run export

      - name: Upload Build
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Upload PDF
        uses: actions/upload-artifact@v4
        with:
          name: pdf
          path: '*.pdf'

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Download Build
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Deploy to Production
        # Add your deployment step
```

## Troubleshooting

### Build Fails

1. Check Node version (≥18)
2. Clear node_modules: `rm -rf node_modules && npm install`
3. Check for syntax errors in slides

### Assets Not Loading

1. Verify base path configuration
2. Check asset paths (use `/` prefix for public/)
3. Rebuild with correct base

### Fonts Missing

1. Use web fonts
2. Check font loading in styles

### Blank Page After Deploy

1. Check browser console for errors
2. Verify SPA routing configuration
3. Check base path matches URL

## Best Practices

1. **Test Build Locally**:
   ```bash
   npm run build && npx serve dist
   ```

2. **Use CI/CD**: Automate deployments

3. **Version Your Deployments**: Use git tags

4. **Monitor Performance**: Check load times

5. **Keep URLs Stable**: Don't change paths frequently

## Output Format

When deploying:

```
PLATFORM: [GitHub Pages | Netlify | Vercel | Docker]

BUILD COMMAND:
npm run build --base [path]

CONFIGURATION FILES:
- [config file name and content]

DEPLOYMENT URL:
https://[your-domain]/[path]/

CHECKLIST:
- [ ] Build succeeds locally
- [ ] Assets load correctly
- [ ] Base path configured
- [ ] SSL/HTTPS enabled
- [ ] (Optional) Custom domain
- [ ] (Optional) Password protection
```
