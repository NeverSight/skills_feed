---
name: app-platform-router
version: 1.0.0
min_doctl_version: "1.82.0"
description: Routes DigitalOcean App Platform tasks to specialized sub-skills. Use when working with App Platform deployments, migrations, database configuration, networking, or troubleshooting.
related_skills: [designer, deployment, migration, postgres, managed-db-services, networking, spaces, ai-services, troubleshooting, devcontainers, sandbox, planner]
deprecated: false
---

# App Platform Skills — Router

## Overview

This skill routes DigitalOcean App Platform tasks to specialized sub-skills. Each sub-skill is optimized for a specific workflow, keeping context focused and responses precise.

**Philosophy**: These skills are opinionated playbooks, not documentation replicas. They make decisions for you (VPC by default, GitHub Actions for CI/CD, etc.) and only defer to docs for edge cases.

**Key Principle**: Skills contain only DO-specific knowledge the LLM doesn't have from training. Generic SQL, SDK patterns, and programming concepts are NOT duplicated here.

**Trust the AI**: The AI assistant should reason about the full workflow, chain skills together when needed, and adapt based on context (greenfield vs brownfield vs troubleshooting). Skills provide domain knowledge, not rigid scripts to follow blindly.

## Available Skills

### Development Phase

| Skill | Purpose | Key Artifacts |
|-------|---------|---------------|
| **devcontainers** | Local development environment with prod parity | `.devcontainer/`, `docker-compose.dev.yml` |

### Architecture Phase

| Skill | Purpose | Key Artifacts |
|-------|---------|---------------|
| **designer** | Natural language → production-ready App Spec | `.do/app.yaml` |
| **migration** | Convert existing apps (Heroku, AWS, etc.) to App Platform | `.do/app.yaml`, migration checklist |
| **planner** | Generate staged project plans from design to deployment | `Plan/*.md` stage files |

### Operations Phase

| Skill | Purpose | Key Artifacts |
|-------|---------|---------------|
| **deployment** | Ship code to production via GitHub Actions | `.github/workflows/deploy.yml` |
| **troubleshooting** | Debug running apps with pre-built debug container, analyze logs | Fixes, diagnostic reports |
| **sandbox** | Isolated containers for AI agent code execution, testing | Ephemeral sandboxes |

### Data Services

| Skill | Purpose | Key Artifacts |
|-------|---------|---------------|
| **postgres** | Full PostgreSQL setup: schemas, users, permissions, multi-tenant | SQL scripts (user-executed) |
| **managed-db-services** | MySQL, MongoDB, Valkey, Kafka, OpenSearch (bindable vars) | App spec snippets |
| **spaces** | S3-compatible object storage configuration | CORS config, app spec snippets |

### AI Services

| Skill | Purpose | Key Artifacts |
|-------|---------|---------------|
| **ai-services** | Gradient AI inference endpoints | App spec snippets |

---

## Console SDK for AI Assistants

**CRITICAL**: AI assistants cannot use `doctl apps console` — it opens an interactive WebSocket session that requires human input. Use the `do-app-sandbox` Python package instead.

```bash
# Install
uv pip install do-app-sandbox  # or: pip install do-app-sandbox
```

### Two Use Cases (Same Package, Different Skills)

| Use Case | SDK Method | Skill |
|----------|------------|-------|
| Debug EXISTING app | `Sandbox.get_from_id(app_id, component)` | **troubleshooting** |
| Create NEW sandbox | `Sandbox.create()`, `SandboxManager` | **sandbox** |

```python
# Debug existing app (troubleshooting skill)
app = Sandbox.get_from_id(app_id="your-app-id", component="web")

# Create new isolated sandbox (sandbox skill)
sandbox = Sandbox.create(image="python")
```

**Full guide**: See [shared/console-sdk-patterns.md](shared/console-sdk-patterns.md)

---

## Routing Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER REQUEST                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │ Setting up development? │
                └─────────────────────────┘
                              │
                      "local" / "devcontainer"
                              ▼
                      ┌───────────┐
                      │devcontainers│
                      └───────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │ Designing or creating?  │
                └─────────────────────────┘
                      │           │           │
             "new app"│           │ "migrate" │ "plan" / "staged"
                      ▼           ▼           ▼
              ┌───────────┐  ┌───────────┐  ┌───────────┐
              │ designer  │  │ migration │  │  planner  │
              └───────────┘  └───────────┘  └───────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │    Shipping code?       │
                └─────────────────────────┘
                              │
                      "deploy" / "ship" / "release"
                              ▼
                      ┌───────────┐
                      │deployment │
                      └───────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │   Something broken?     │
                └─────────────────────────┘
                              │
                      "broken" / "failing" / "debug" / "logs"
                              ▼
                    ┌───────────────┐
                    │troubleshooting│
                    └───────────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │ Need isolated execution?│
                └─────────────────────────┘
                              │
                      "sandbox" / "isolated" / "execute code" / "code interpreter"
                              ▼
                      ┌───────────┐
                      │  sandbox  │
                      └───────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │ Configuring data?       │
                └─────────────────────────┘
                      │           │           │
           "postgres" │  "mysql"  │           │ "storage" / "S3" / "spaces"
           (complex)  │  "mongo"  │           │
                      │  "valkey" │           │
                      │  "kafka"  │           │
                      │  "opensearch"         │
                      ▼           ▼           ▼
              ┌───────────┐  ┌─────────────────────┐  ┌───────────┐
              │ postgres  │  │ managed-db-services │  │  spaces   │
              └───────────┘  └─────────────────────┘  └───────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │ AI inference needed?    │
                └─────────────────────────┘
                              │
                      "gradient" / "LLM" / "inference"
                              ▼
                      ┌─────────────┐
                      │ ai-services │
                      └─────────────┘
```

---

## Workflow Chaining

**The AI assistant should reason about the full workflow, not just route to a single skill.**

### Workflow Types

| Request Type | Workflow | Skills Chain |
|--------------|----------|--------------|
| **Full Greenfield** | "Build a new app from scratch" | devcontainers → designer → planner → deployment |
| **Migration** | "Migrate from Heroku/AWS" | migration → (then full greenfield workflow) |
| **Brownfield** | "Deploy my existing app" | planner → deployment |
| **Enhancement** | "Add Kafka to my app" | managed-db-services → update app.yaml → deployment |
| **Troubleshooting** | "My app is broken" | troubleshooting (standalone) |
| **AI Agent Execution** | "Run code in isolation" | sandbox (standalone) |
| **Specific Task** | "Set up PostgreSQL" | postgres (standalone) |

### Chaining Logic

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNDERSTAND THE GOAL                           │
│  Is this a single task or a multi-phase workflow?                │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
       ┌─────────────┐                 ┌─────────────┐
       │ Single Task │                 │  Workflow   │
       │             │                 │             │
       │ Route to    │                 │ Chain       │
       │ one skill   │                 │ multiple    │
       └─────────────┘                 └─────────────┘
              │                               │
              ▼                               ▼
       troubleshooting              migration → designer →
       postgres                     planner → deployment
       spaces
       etc.
```

### Examples

**"I want to build a new event-driven app with Kafka"**
1. Start with **designer** → create `.do/app.yaml` with Kafka
2. Use **managed-db-services** for Kafka-specific bindable variables
3. Use **planner** → generate staged Plan/ files
4. Execute with **deployment** skill

**"Migrate my Heroku app to DigitalOcean"**
1. Start with **migration** → convert Procfile, analyze addons
2. Creates `.do/app.yaml` (migration produces this)
3. Use **planner** → plan the staged deployment
4. Execute with **deployment** skill

**"My deployed app keeps returning 502"**
1. Route directly to **troubleshooting** (single skill, no chaining)
2. Use debug container, analyze logs, fix issue

**"Add PostgreSQL to my existing app"**
1. Use **postgres** for schema/user setup
2. Update `.do/app.yaml` with database binding
3. Redeploy with **deployment** skill

### Key Principle

**The AI assistant should:**
1. Understand the overall goal (not just the immediate request)
2. Identify which skills are needed and in what order
3. Chain skills together, passing artifacts between them
4. Adapt based on what already exists (greenfield vs brownfield)

**Trust the AI to reason.** These skills provide domain knowledge, not rigid scripts.

---

## Trigger Phrases Reference

| Route To | Trigger Phrases |
|----------|----------------|
| devcontainers | "local dev", "docker compose", "run locally", "devcontainer" |
| designer | "design my app", "create app spec", "new application", "architect" |
| migration | "migrate", "convert", "move from Heroku", "move from AWS" |
| planner | "create a plan", "plan this project", "staged approach", "plan deployment", "how should I deploy" |
| deployment | "deploy", "ship", "release", "GitHub Actions", "CI/CD" |
| troubleshooting | "broken", "failing", "debug", "logs", "502", "crash", "error" |
| sandbox | "sandbox", "isolated environment", "execute code", "code interpreter", "run untrusted code", "agent execution", "hot pool" |
| postgres | "postgres", "postgresql", "schema isolation", "multi-tenant database" |
| managed-db-services | "mysql", "mongodb", "mongo", "valkey", "redis", "kafka", "opensearch" |
| spaces | "object storage", "S3", "Spaces", "file upload", "bucket" |
| ai-services | "gradient", "inference", "LLM endpoint", "AI platform" |

---

## Third-Party Integrations (No Skill Needed)

For integrations not covered by dedicated skills (DataDog, Sentry, New Relic, Stripe, etc.):

1. **Get credentials** from the vendor
2. **Add to GitHub Secrets** (Repo → Settings → Secrets → Actions)
3. **Reference in app spec**:
   ```yaml
   envs:
     - key: DATADOG_API_KEY
       scope: RUN_TIME
       value: ${DATADOG_API_KEY}  # From GitHub Secrets
   ```
4. **Follow vendor documentation** for SDK/agent setup

→ The agent's training covers vendor-specific patterns — no skill required.

---

## Credential Handling Philosophy

**CRITICAL**: These skills are designed to keep credentials out of agent hands.

### Priority Order (Most to Least Preferred)

```
1. GITHUB SECRETS (RECOMMENDED DEFAULT)
   ├── Agent never sees credentials
   ├── User manually adds: Repo → Settings → Secrets → Actions
   ├── Workflow references: ${{ secrets.DATABASE_URL }}
   └── Agent generates workflow, user handles secrets

2. APP PLATFORM BINDABLE VARIABLES
   ├── For DO Managed Databases (Postgres, MySQL, MongoDB, etc.)
   ├── Credentials injected via ${db.DATABASE_URL}
   ├── Agent configures app spec, never sees credentials
   └── Best for: Apps using DO managed services

3. LOCAL .ENV + EPHEMERAL APP SPEC
   ├── User maintains .env file locally
   ├── Agent creates temp app spec with placeholders
   └── Substitutes values → Deploys → Deletes temp file

4. EXTERNAL SERVICES
   ├── Same patterns as #1 or #3
   └── User responsible for credential management
```

---

## Artifact Contracts

All skills produce and consume artifacts with consistent naming:

| Artifact | Filename | Producer | Consumer |
|----------|----------|----------|----------|
| App Spec | `.do/app.yaml` | designer, migration | deployment, planner |
| Deploy Button | `.do/deploy.template.yaml` | designer, migration | GitHub |
| Deployment Plan | `Plan/0N-*.md` | planner | User, deployment |
| Dev Environment | `.devcontainer/devcontainer.json` | devcontainers | VS Code, Cursor |
| Docker Compose | `docker-compose.yml` | devcontainers | Docker Desktop |
| CI/CD Workflow | `.github/workflows/deploy.yml` | deployment, planner | GitHub Actions |
| SQL Scripts | `db-*.sql` | postgres | User (manual execution) |
| CORS Config | `spaces-cors.json` | spaces | DO Console |

### Handoff Protocol

When a skill completes, it should:

1. **State the artifact(s) produced**: "Created `.do/app.yaml` with 3-component architecture"
2. **Indicate the file path**: Relative to project root
3. **Suggest next skill if applicable**: "To deploy this, use the **deployment skill**"

---

## Plugin/Tool Requirements

| Skill | Required | Optional |
|-------|----------|----------|
| devcontainers | filesystem, docker, git | gh |
| designer | filesystem | — |
| migration | filesystem, doctl, git, python | gh, DigitalOcean MCP |
| deployment | filesystem, doctl, git, python | gh, GitHub MCP |
| troubleshooting | filesystem, python, doctl | — |
| sandbox | filesystem, python, doctl | — |
| postgres | filesystem, psql | — (scripts only) |
| managed-db-services | filesystem, doctl | — |
| spaces | filesystem | s3cmd (for bucket ops; doctl only manages keys) |
| ai-services | filesystem | — |

---

## Sub-Skill Locations

```
app-platform-skills/
├── SKILL.md                              # This file (router)
├── skills/
│   ├── devcontainers/SKILL.md
│   ├── designer/SKILL.md
│   ├── migration/SKILL.md
│   ├── deployment/SKILL.md
│   ├── planner/SKILL.md                  # Staged project plans (design to deployment)
│   │   └── templates/                    # Local + Tier 1, 2, 3 stage templates
│   ├── troubleshooting/SKILL.md
│   ├── sandbox/SKILL.md                  # Isolated containers for AI agent execution
│   ├── postgres/SKILL.md
│   ├── managed-db-services/SKILL.md      # MySQL, MongoDB, Valkey, Kafka, OpenSearch
│   ├── spaces/SKILL.md
│   └── ai-services/SKILL.md              # Gradient AI
└── shared/
    ├── app-spec-schema.yaml
    ├── artifact-contracts.md
    └── credential-patterns.md
```

---

## Opinionated Defaults Summary

| Domain | Default | Override Trigger |
|--------|---------|-----------------|
| Networking | VPC-only, internal routing | User explicitly requests public |
| CI/CD | GitHub + GitHub Actions | User specifies GitLab/Bitbucket |
| Secrets | GitHub Secrets | User has existing vault |
| Build | Dockerfile | User explicitly prefers buildpacks |
| Database | DO Managed + Bindable Variables | User has external DB |
| Monorepo | Supported by default (source_dir) | N/A |
| Python env | uv for package/venv management | User prefers pip/poetry |
| Node env | nvm for version management | User prefers n/volta |

---

## Escalation

If a task doesn't fit any skill or spans multiple skills ambiguously:

1. Ask clarifying question to determine primary intent
2. Suggest skill sequence if task is multi-phase
3. For truly novel tasks, fall back to App Platform documentation: https://docs.digitalocean.com/products/app-platform/
