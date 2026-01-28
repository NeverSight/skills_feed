---
name: deployment
description: "Next.js deployment - Vercel, Docker, self-hosting strategies"
sasmp_version: "1.3.0"
bonded_agent: nextjs-expert
bond_type: PRIMARY_BOND
---

# Deployment Skill

## Overview

Deploy Next.js applications to various platforms with optimal configurations.

## Capabilities

- **Vercel**: Zero-config deployment
- **Docker**: Containerized deployment
- **Self-Hosting**: Node.js server
- **Static Export**: Static site generation
- **Edge Runtime**: Edge function deployment

## Examples

```dockerfile
# Dockerfile for Next.js
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
# Vercel deployment
npm i -g vercel
vercel --prod

# Docker deployment
docker build -t nextjs-app .
docker run -p 3000:3000 nextjs-app
```

## next.config.js Options

```js
module.exports = {
  output: 'standalone', // For Docker
  // output: 'export', // For static
}
```

