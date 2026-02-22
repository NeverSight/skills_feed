---
name: docker-compose-setup
description: Set up multi-container applications with Docker Compose including services, networks, and volumes
sasmp_version: "1.3.0"
bonded_agent: 05-docker-compose
bond_type: PRIMARY_BOND
---

# Docker Compose Setup Skill

Master Docker Compose for multi-container application orchestration with service dependencies, health checks, and environment management.

## Purpose

Design and configure Docker Compose files for development and production environments with proper service orchestration.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| services | array | No | - | List of services to configure |
| environment | enum | No | dev | dev/staging/prod |
| include_monitoring | boolean | No | false | Add monitoring services |

## Modern Compose File (2024-2025)

**Note**: The `version` field is deprecated. Start directly with `services:`.

```yaml
services:
  frontend:
    build:
      context: ./frontend
      target: production
    ports:
      - "80:80"
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  backend:
    build: ./backend
    expose:
      - "3000"
    environment:
      DATABASE_URL: postgres://user:${DB_PASSWORD}@database:5432/app
    depends_on:
      database:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  database:
    image: postgres:16-alpine
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  db_data:
```

## Environment Management

### Base + Override Pattern
```yaml
# docker-compose.yaml (base)
services:
  app:
    image: myapp:latest

# docker-compose.override.yaml (dev - auto-loaded)
services:
  app:
    build: .
    volumes:
      - ./src:/app/src
    environment:
      - DEBUG=true

# docker-compose.prod.yaml (production)
services:
  app:
    deploy:
      replicas: 3
    restart: always
```

```bash
# Development (loads override automatically)
docker compose up

# Production
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d
```

### Environment Variables
```bash
# .env file (auto-loaded)
DB_PASSWORD=secret123
APP_VERSION=1.2.3
```

```yaml
# Using in compose
environment:
  - DB_PASSWORD=${DB_PASSWORD}
  - VERSION=${APP_VERSION:-latest}  # Default value
```

## Service Profiles
```yaml
services:
  app:
    image: myapp

  # Only with --profile debug
  debugger:
    image: debug-tools
    profiles:
      - debug

  # Only with --profile testing
  test-db:
    image: postgres:alpine
    profiles:
      - testing
```

```bash
docker compose up                     # app only
docker compose --profile debug up     # app + debugger
```

## Common Commands
```bash
# Start services
docker compose up -d

# Rebuild and start
docker compose up -d --build

# View logs
docker compose logs -f backend

# Scale service
docker compose up -d --scale backend=3

# Stop and clean
docker compose down -v

# Validate config
docker compose config
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `undefined service` | Dependency missing | Define service |
| `yaml syntax error` | Indentation | Fix YAML |
| `port already in use` | Port conflict | Change port |
| `healthcheck failing` | Service not ready | Increase start_period |

### Fallback Strategy
1. Validate with `docker compose config`
2. Start services individually
3. Use `--no-deps` to skip dependencies

## Troubleshooting

### Debug Checklist
- [ ] Valid YAML? `docker compose config`
- [ ] Images available? `docker compose pull`
- [ ] Dependencies healthy? Check healthchecks
- [ ] Environment set? Check .env file

### Health Check Debugging
```bash
# Check health status
docker inspect --format='{{json .State.Health}}' <container>

# View health logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' <container>
```

## Usage

```
Skill("docker-compose-setup")
```

## Related Skills
- docker-networking
- docker-volumes
- docker-production
