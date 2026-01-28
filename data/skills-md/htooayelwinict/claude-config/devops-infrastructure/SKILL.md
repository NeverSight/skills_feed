---
name: devops-infrastructure
description: Manage deployment, Docker, CI/CD, server hardening, and infrastructure security. EXCLUSIVE to devops-engineer agent.
allowed-tools: Read, Edit, Bash, Grep, Glob, Write, mcp_context7
---
# DevOps Infrastructure

**Exclusive to:** `devops-engineer` agent

## 📚 Context7 (Memory) — Up-to-Date Docs

Lookup latest deployment patterns and configs:
```
mcp_context7_resolve-library-id(libraryName="docker", query="multi-stage build")
mcp_context7_query-docs(libraryId="/docker/docs", query="compose healthcheck")
```

## Instructions

1. Review existing infrastructure files (Dockerfile, docker-compose, .github/workflows)
2. Understand deployment requirements
3. Propose configuration with rollback plan
4. Implement with safety checks
5. Verify deployment succeeds

## Docker Patterns

### Multi-stage Build
```dockerfile
FROM composer:2 AS vendor
# Install dependencies

FROM node:20-alpine AS assets
# Build frontend

FROM php:8.3-fpm-alpine
# Final production image
```

### Docker Compose
```yaml
services:
  app:
    build: .
  db:
    image: mysql:8.0
  redis:
    image: redis:alpine
```

## CI/CD Workflow

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: composer test
```

## Deployment Checklist
- [ ] Tests pass
- [ ] Environment variables set
- [ ] Database migrations ready
- [ ] Backup exists
- [ ] SSL configured

## Examples
- "Create Dockerfile for Laravel"
- "Set up GitHub Actions pipeline"
- "Configure production environment"
