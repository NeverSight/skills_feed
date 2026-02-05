---
name: docker
description: |
  Production-grade Docker containerization for Python and Node.js applications.
  This skill should be used when users ask to containerize applications, create Dockerfiles,
  dockerize projects, or set up Docker Compose. Auto-detects project structure,
  analyzes .env for secrets, validates security, and generates tested Dockerfiles.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-docker.sh"
---

# Docker

Production-grade Docker containerization with security-first defaults.

---

## Resource Detection & Adaptation

**Before generating Dockerfiles/Compose, detect the environment:**

```bash
# Detect host machine memory
sysctl -n hw.memsize 2>/dev/null | awk '{print $0/1024/1024/1024 " GB"}' || \
  grep MemTotal /proc/meminfo | awk '{print $2/1024/1024 " GB"}'

# Detect Docker allocated resources
docker info --format 'Memory: {{.MemTotal}}, CPUs: {{.NCPU}}'

# Detect available disk space
docker system df
```

**Adapt configurations based on detection:**

| Detected Docker Memory | Profile | Build Memory | Container Limits |
|-----------------------|---------|--------------|------------------|
| < 4GB | Constrained | 1GB | 256Mi |
| 4-8GB | Minimal | 2GB | 512Mi |
| 8-12GB | Standard | 4GB | 1Gi |
| > 12GB | Extended | 8GB | 2Gi |

### Agent Behavior

1. **Detect** Docker resources before generating compose.yaml
2. **Adapt** resource limits to available memory
3. **Warn** if build may fail due to insufficient resources
4. **Calculate** safe limits: `docker_memory * 0.6 / container_count`

### Adaptive Compose Templates

**Constrained (< 4GB Docker):**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.25'
    build:
      args:
        - BUILDKIT_STEP_LOG_MAX_SIZE=10000000
```
⚠️ Agent should warn: "Docker memory low. Multi-stage builds may fail."

**Standard (4-8GB Docker):**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
```

**Extended (> 8GB Docker):**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
```

### Pre-Build Validation

Before running `docker build`, agent should verify:
```bash
# Check available memory
docker info --format '{{.MemTotal}}' | awk '{if ($1 < 4000000000) print "WARNING: Low memory"}'
```

If constrained: use `--memory` flag and warn user about potential build failures.

---

## What This Skill Does

**Analysis & Detection:**
- Auto-detects runtime, framework, version, entrypoint (no questions)
- Scans .env files, classifies secrets vs build-args vs runtime config
- Detects native dependencies, generates correct build deps
- Identifies missing configs (Next.js standalone, health endpoints)

**Generation:**
- Creates multi-stage Dockerfiles customized to YOUR project structure
- Generates compose.yaml with security defaults (non-root, read-only, resource limits)
- Adds health endpoints if missing
- Fixes configuration issues (adds `output: 'standalone'` to Next.js, etc.)

**Validation:**
- Builds both dev and production targets before delivering
- Verifies health endpoints work
- Confirms non-root user in production
- Warns about any secrets that would leak into image
- Reports image size

**Security:**
- Never bakes secrets into images
- Non-root user by default
- Minimal attack surface (multi-stage builds)
- Pinned versions (no `:latest`)
- Security scan command included

## What This Skill Does NOT Do

- Generate Kubernetes manifests (use dedicated k8s skill)
- Create Helm charts (use dedicated helm skill)
- Handle Bun/Deno (use dedicated skills)
- Copy templates blindly without customization

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Package files, existing Dockerfile, .env patterns |
| **Conversation** | Dev vs production target, base image preferences |
| **Skill References** | Framework patterns, multi-stage builds, security |
| **User Guidelines** | Registry conventions, naming standards |

---

## Required Clarifications

Ask when not auto-detectable:

| Question | When to Ask |
|----------|-------------|
| Target environment | "Building for development or production?" |
| Base image preference | "Standard slim images or enterprise hardened?" |
| Existing Docker files | "Enhance existing Dockerfile or create new?" |
| Registry target | "Local only or pushing to registry?" |

---

## Detect Runtime

| File Present | Runtime | Package Manager |
|--------------|---------|-----------------|
| `requirements.txt`, `pyproject.toml`, `uv.lock` | Python | pip/uv |
| `pnpm-lock.yaml` | Node.js | pnpm |
| `yarn.lock` | Node.js | yarn |
| `package-lock.json` | Node.js | npm |

---

## Auto-Detection (Do NOT ask - detect from files)

### Python
| What | Detect From |
|------|-------------|
| Python version | `pyproject.toml` (requires-python), `.python-version`, `runtime.txt` |
| Framework | Imports in code (`from fastapi`, `from flask`, `import django`) |
| Package manager | `uv.lock` → uv, `poetry.lock` → poetry, else pip |
| Native deps | Scan requirements: `psycopg2`, `cryptography`, `numpy`, `pillow` |
| App entrypoint | Find `app = FastAPI()`, `app = Flask()`, or `manage.py` |

### Node.js
| What | Detect From |
|------|-------------|
| Node version | `.nvmrc`, `.node-version`, `package.json` (engines.node) |
| Framework | `package.json` dependencies (next, express, @nestjs/core) |
| Package manager | `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, else npm |
| Output type | Next.js: check `next.config.js` for `output: 'standalone'` |

### Fix Issues Automatically
| Issue | Action |
|-------|--------|
| Next.js missing `output: 'standalone'` | **Add it** to next.config.js |
| No health endpoint found | **Create** `/health/live` and `/health/ready` |
| Using uv but no uv.lock | Run `uv lock` first |
| pyproject.toml but no build system | Use `uv pip install -r pyproject.toml` |

---

## Workflow

```
1. SCAN PROJECT
   - Detect runtime, framework, version, entrypoint
   - Find dependency files, native deps
   - Locate existing Docker files (don't blindly overwrite)
         ↓
2. ANALYZE ENVIRONMENT
   - Scan all .env* files
   - Classify: SECRET (never bake) / BUILD_ARG / RUNTIME
   - Flag security issues
         ↓
3. FIX CONFIGURATION
   - Add Next.js `output: 'standalone'` if missing
   - Create health endpoints if missing
   - Generate .env.example with safe placeholders
         ↓
4. GENERATE FILES
   - Dockerfile (customized CMD, paths, build deps)
   - .dockerignore (excludes .env, secrets)
   - compose.yaml (with security defaults)
         ↓
5. VALIDATE & TEST
   - docker build --target dev -t app:dev .
   - docker build --target production -t app:prod .
   - Test health endpoints
   - Verify non-root user
   - Report image size
         ↓
6. DELIVER WITH CONTEXT
   - All files with explanations
   - Security scan command
   - Any warnings about secrets
   - Rollback instructions if replacing existing
```

**Only ask if genuinely ambiguous** (e.g., multiple apps in monorepo, conflicting configs)

---

## Base Image Decision Matrix

| Choice | When to Use | Tradeoffs |
|--------|-------------|-----------|
| **Slim** `{runtime}:X-slim` | General production (default) | Works everywhere, no auth |
| **DHI** `dhi.io/{runtime}:X` | SOC2/HIPAA, enterprise | Requires `docker login dhi.io` |
| **Alpine** `{runtime}:X-alpine` | Smallest size | musl issues with native deps |

Default: **Slim** (works everywhere without authentication)

---

## Stage Structure

```
deps/base  → Install dependencies (cached layer)
    ↓
builder    → Build/compile application
    ↓
dev        → Hot-reload, volume mounts (--target dev)
    ↓
production → Minimal DHI runtime (--target production)
```

### Build Commands

```bash
docker build --target dev -t myapp:dev .
docker build --target production -t myapp:prod .
```

---

## Python Patterns

### Framework CMD

| Framework | Development | Production |
|-----------|-------------|------------|
| **FastAPI** | `uvicorn app.main:app --reload` | `uvicorn app.main:app --workers 4` |
| **Flask** | `flask run --debug` | `gunicorn -w 4 app:app` |
| **Django** | `python manage.py runserver` | `gunicorn -w 4 project.wsgi` |

### Cache Mount (uv/pip)

```dockerfile
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/root/.cache/pip \
    uv pip install -r requirements.txt
```

### Graceful Shutdown (FastAPI)

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # startup
    # shutdown logic here
```

---

## Node.js Patterns

### Framework Build

| Framework | Build | Output |
|-----------|-------|--------|
| **Next.js** | `next build` | `.next/standalone` |
| **Express** | `tsc` | `dist/` |
| **NestJS** | `nest build` | `dist/` |

### Cache Mounts

```dockerfile
# pnpm
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile

# npm
RUN --mount=type=cache,target=/root/.npm npm ci

# yarn
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn install --frozen-lockfile
```

### Graceful Shutdown (Node.js)

```javascript
process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});
```

---

## Security Checklist

Before delivering, verify:

- [ ] Non-root USER in production stage
- [ ] No secrets in Dockerfile or image layers
- [ ] .dockerignore excludes `.env`, `.git`, secrets
- [ ] Multi-stage separates build tools from runtime
- [ ] DHI or hardened base image used
- [ ] HEALTHCHECK instruction defined
- [ ] No package install in production stage
- [ ] Secrets via runtime env vars or mounted files

---

## Output Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage, multi-target build |
| `.dockerignore` | Exclude sensitive/unnecessary files |
| `compose.yaml` | Local development stack |
| `health.py` / health endpoint | Framework-specific health checks |

---

## Reference Files

### Always Read First
| File | Purpose |
|------|---------|
| `references/env-analysis.md` | **CRITICAL**: Secret detection, .env classification |
| `references/production-checklist.md` | **CRITICAL**: Validation before delivery |

### Framework-Specific
| File | When to Read |
|------|--------------|
| `references/python/fastapi.md` | FastAPI: uvicorn, lifespan |
| `references/python/flask.md` | Flask: gunicorn, blueprints |
| `references/python/django.md` | Django: gunicorn, middleware |
| `references/python/native-deps.md` | Detect psycopg2, cryptography, etc. |
| `references/node/nextjs.md` | Next.js: standalone, ISR |
| `references/node/package-managers.md` | npm/yarn/pnpm caching |

### Optional
| File | When to Read |
|------|--------------|
| `references/docker-hardened-images.md` | If user needs enterprise security (DHI) |
| `references/multi-stage-builds.md` | Complex build patterns |

## Templates (Reference Patterns)

Templates in `templates/` are **reference patterns**, not copy-paste files.

**Agent must:**
1. Read template to understand structure
2. Customize paths, CMDs, and stages for actual project
3. Generate Dockerfile with correct entrypoint (e.g., `src.app.main:app`)
4. Never output placeholder comments like "# Replace based on framework"

**Example customization:**
```dockerfile
# Template says:
CMD ["uvicorn", "app.main:app", ...]

# Agent detects app at src/api/main.py, generates:
CMD ["uvicorn", "src.api.main:app", ...]
```
