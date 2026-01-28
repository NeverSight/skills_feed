---
name: docker-guide
description: Best practices for Dockerizing Remix/Shopify apps. Includes multi-stage builds, Alpine images, and local dev setups with pnpm.
---

# Docker Guide for Shopify/Remix Apps

This guide covers how to containerize your Shopify App for consistent deployment across any VPS or cloud provider.

## 1. Production Dockerfile (Multi-stage)
This optimized Dockerfile uses multi-stage builds to keep the final image size small (<200MB usually) and secure.

```dockerfile
# base node image
FROM node:20-alpine AS base

# set for base and all layer that inherit from it
ENV NODE_ENV=production

# Install all node_modules, including dev dependencies
FROM base AS deps
WORKDIR /myapp
ADD package.json package-lock.json ./
# Or COPY package.json pnpm-lock.yaml ./ if using pnpm
RUN npm ci --include=dev

# Setup production node_modules
FROM base AS production-deps
WORKDIR /myapp
COPY --from=deps /myapp/node_modules /myapp/node_modules
ADD package.json package-lock.json ./
RUN npm prune --omit=dev

# Build the app
FROM base AS build
WORKDIR /myapp
COPY --from=deps /myapp/node_modules /myapp/node_modules
ADD . .
RUN npm run build

# Finally, build the production image with minimal footprint
FROM base
WORKDIR /myapp
COPY --from=production-deps /myapp/node_modules /myapp/node_modules
COPY --from=build /myapp/build /myapp/build
COPY --from=build /myapp/public /myapp/public
COPY --from=build /myapp/package.json /myapp/package.json
COPY --from=build /myapp/prisma /myapp/prisma

# Start the server
CMD ["npm", "run", "start"]
```

## 2. Local Development (docker-compose.yml)
Don't install Postgres/Redis locally on your Mac. Run them in Docker.

```yaml
services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: shopify_app
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    restart: always
    ports:
      - "6379:6379"
    command: redis-server --save 60 1 --loglevel warning

volumes:
  db_data:
```

## 3. Important Notes for Shopify Apps

### `SHOPIFY_APP_URL`
In production, your `SHOPIFY_APP_URL` must match your domain (e.g., `https://app.example.com`).
When running in Docker behind a proxy (like Nginx), ensure `X-Forwarded-Proto` headers are passed, otherwise Remix/Shopify auth might think it's HTTP and reject the session.

### Port Mapping
Remix usually runs on port 3000. In Docker:
`EXPOSE 3000`
And map it when running: `docker run -p 8080:3000 my-app`

### Alpine Issues
If you use extensive native modules (like `sharp` or some crypto libs), Alpine might miss dependencies. If builds fail, switch from `node:20-alpine` to `node:20-slim`.

## 4. Commands

```bash
# Build
docker build -t my-shopify-app .

# Run locally to test
docker run -p 3000:3000 --env-file .env my-shopify-app
```
