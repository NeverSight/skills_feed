---
name: react-dockerfile
description: Create optimized, secure multi-stage Dockerfiles for React applications (Vite, CRA, Next.js static). Use when (1) creating a new Dockerfile for a React project, (2) containerizing a React/Vite application, (3) optimizing an existing React Dockerfile, (4) setting up Docker for React with Nginx, or (5) user mentions React and Docker/container together.
---

# React Dockerfile Generator

Generate production-ready multi-stage Dockerfiles for React applications served with Nginx.

## Workflow

1. Determine build tool: Vite (default), Create React App, or Next.js static export
2. Identify Node.js version from `.nvmrc`, `package.json` engines, or use Node 22 LTS
3. Check for existing nginx configuration files
4. Choose optimization: standard, non-root (recommended), or runtime env vars

> **Key Insight**: Unlike server-side Node.js apps, React apps only need Node.js for building—the runtime is static files served by Nginx. This reduces image size from ~1GB to ~50MB.

## Image Selection Guide

| Scenario | Runtime Image | Compressed Size |
|----------|--------------|-----------------|
| Standard Nginx | `nginx:stable-alpine` | ~45 MB |
| Non-root (recommended) | `nginx:stable-alpine` + USER | ~45 MB |
| With Brotli compression | `fholzer/nginx-brotli:latest` | ~55 MB |

## Standard Pattern

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:stable-alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Required nginx.conf

Always create `nginx.conf` with SPA routing, caching, and security headers:

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Hide Nginx version
    server_tokens off;

    # SPA routing - serve index.html for all routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache hashed assets forever (Vite generates unique hashes)
    location ~* \.(?:css|js)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # Cache static assets
    location ~* \.(?:ico|gif|jpe?g|png|svg|woff2?|ttf|eot)$ {
        expires 6M;
        add_header Cache-Control "public, max-age=15552000";
    }

    # No cache for index.html (entry point must always be fresh)
    location = /index.html {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript
               application/xml+rss application/atom+xml image/svg+xml;

    # Deny hidden files
    location ~ /\. {
        deny all;
    }
}
```

## Non-Root Pattern (Recommended)

For production security, run Nginx as non-root on port 8080:

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:stable-alpine AS production

# Create nginx directories with correct permissions
RUN mkdir -p /var/run/nginx && \
    chown -R nginx:nginx /var/cache/nginx /var/run/nginx && \
    chmod -R g+w /var/cache/nginx

# Copy nginx configs
COPY nginx-main.conf /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files
COPY --from=builder --chown=nginx:nginx /app/dist /usr/share/nginx/html

USER nginx
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
```

**Required nginx-main.conf** for non-root operation:

```nginx
worker_processes auto;
pid /var/run/nginx/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    sendfile on;
    keepalive_timeout 65;
    include /etc/nginx/conf.d/*.conf;
}
```

**Update nginx.conf** to listen on port 8080:

```nginx
server {
    listen 8080;
    # ... rest of config
}
```

## Build-Time Environment Variables (Vite)

Vite embeds environment variables at build time. Pass them via build arguments:

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS builder
WORKDIR /app

# Accept build arguments
ARG VITE_API_URL
ARG VITE_APP_TITLE

# Make available to Vite build
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_APP_TITLE=$VITE_APP_TITLE

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:stable-alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build with:

```bash
docker build \
  --build-arg VITE_API_URL=https://api.example.com \
  --build-arg VITE_APP_TITLE="My App" \
  -t myapp:prod .
```

**Important**: All Vite environment variables must be prefixed with `VITE_`.

## Runtime Environment Variables (Advanced)

For "build once, deploy anywhere" workflows, inject environment variables at container startup:

**Step 1**: Create `public/config.js.template`:

```javascript
window.__ENV__ = {
  VITE_API_URL: "__VITE_API_URL__",
  VITE_FEATURE_FLAG: "__VITE_FEATURE_FLAG__"
};
```

**Step 2**: Create `docker-entrypoint.sh`:

```bash
#!/bin/sh
set -e

# Replace placeholders with actual environment variables
envsubst < /usr/share/nginx/html/config.js.template > /usr/share/nginx/html/config.js

# Start nginx
exec nginx -g "daemon off;"
```

**Step 3**: Update Dockerfile:

```dockerfile
FROM nginx:stable-alpine AS production
RUN apk add --no-cache gettext

COPY --from=builder /app/dist /usr/share/nginx/html
COPY public/config.js.template /usr/share/nginx/html/config.js.template
COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN chmod +x /docker-entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/docker-entrypoint.sh"]
```

**Step 4**: Access in React app:

```javascript
const apiUrl = window.__ENV__?.VITE_API_URL || import.meta.env.VITE_API_URL;
```

## Development Stage

Add a development stage for local dev with hot reload:

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS development
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

FROM base AS builder
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:stable-alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build targets:

```bash
# Development with hot reload
docker build --target development -t myapp:dev .
docker run -p 5173:5173 -v $(pwd)/src:/app/src myapp:dev

# Production
docker build --target production -t myapp:prod .
```

## Vite Configuration for Docker HMR

Configure `vite.config.ts` for hot module replacement in Docker:

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Listen on all interfaces
    port: 5173,
    watch: {
      usePolling: true,  // Required for Docker file watching
    },
    hmr: {
      host: 'localhost',
      port: 5173,
    },
  },
});
```

**Note**: `usePolling: true` increases CPU usage but is required for reliable file change detection in Docker.

## Memory Optimization for Large Builds

Node.js defaults to 512MB memory, which may be insufficient for large Vite builds:

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

# Increase Node.js memory limit for large builds
ENV NODE_OPTIONS="--max-old-space-size=4096"
RUN npm run build
```

## Cache Optimization

Use BuildKit cache mount for npm packages:

```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

## Complete Production Example

```dockerfile
# syntax=docker/dockerfile:1

ARG NODE_VERSION=22

# Stage 1: Dependencies
FROM node:${NODE_VERSION}-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Stage 2: Build
FROM node:${NODE_VERSION}-alpine AS builder
WORKDIR /app

# Build arguments for Vite
ARG VITE_API_URL
ARG VITE_APP_VERSION

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_APP_VERSION=$VITE_APP_VERSION
ENV NODE_OPTIONS="--max-old-space-size=4096"

COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production
FROM nginx:stable-alpine AS production
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.description="Production React application"

# Security: Create non-root setup
RUN mkdir -p /var/run/nginx && \
    chown -R nginx:nginx /var/cache/nginx /var/run/nginx /usr/share/nginx/html && \
    chmod -R g+w /var/cache/nginx

# Copy nginx configs
COPY nginx-main.conf /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files
COPY --from=builder --chown=nginx:nginx /app/dist /usr/share/nginx/html

USER nginx
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

## Required .dockerignore

Always create `.dockerignore`:

```dockerignore
node_modules
npm-debug.log*
dist
build
.git
.gitignore
*.md
.env
.env.*
.vscode
.idea
coverage
*.test.*
*.spec.*
__tests__
Dockerfile*
docker-compose*
.dockerignore
```

## Create React App Adjustments

For Create React App (CRA) projects:

- Build output is in `build/` instead of `dist/`
- Environment variables use `REACT_APP_` prefix instead of `VITE_`

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app

ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:stable-alpine AS production
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Verification Checklist

- Node.js Alpine image for build stage, Nginx Alpine for production
- Include nginx.conf with SPA routing (`try_files $uri $uri/ /index.html`)
- Copy build output: `dist/` for Vite, `build/` for CRA
- Use `USER nginx` for non-root execution (listen on 8080)
- Cache hashed assets (js/css) with long expiration
- Never cache index.html (entry point must be fresh)
- Include .dockerignore to exclude node_modules
- Consider memory limits for large builds (`NODE_OPTIONS`)
- Use `usePolling: true` in Vite config for Docker HMR
