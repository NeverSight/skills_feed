---
name: kavak-documentation
description: Kavak internal documentation integration. Use when planning features, architecture, kbroker, auth, SDKs, databases, GitLab pipelines, Docker configs, or creating new services/workloads.
tools: Read, CallMcpTool
model: opus
---

# Kavak Documentation

Search Kavak's internal documentation first via `plati_query` MCP tool, then complement with other sources.

> **Related Skills:**
>
> - `backend-development` - After finding Kavak patterns, implement using backend best practices
> - Check `references/` folder for detailed Kavak implementation guides

## Core Principle

**Search Kavak docs first, always.** Internal platform knowledge reduces agent errors and ensures proper Kavak patterns.

## When to Use

- Planning new features or architecture
- Architecture, kbroker, STS, SDKs, databases
- Creating new services/workloads (Go, TypeScript, Python, Java)
- **GitLab CI/CD pipelines and configurations**
- **Docker/container configurations**
- Development workflow, logs, metrics best practices
- Kavak CLI usage/installation

## Quick Start

1. Verify `kavak-platform` MCP is configured in Cursor
2. Use `plati_query` tool with a focused question
3. Complement results with other tools as needed

## Workflow

### 1. Check MCP Availability

Ensure `kavak-platform` MCP server is enabled in Cursor settings.

### 2. Query Documentation

**Rules for `plati_query`:**

- One question per query (avoid compound questions)
- Keep questions clear and concise (prevents timeouts)
- Be specific about the topic

**Good queries:**

```
"How to create a new Go workload?"
"What is kbroker and how to publish events?"
"How does STS authentication work?"
"What are the logging best practices?"
"How to configure GitLab CI pipeline for a Go service?"
"What is the standard Dockerfile for TypeScript services?"
"How to set up container registry in GitLab?"
```

**Bad queries:**

```
"Tell me about architecture, kbroker, and how to create services"  # Too many topics
"Explain everything about the platform"  # Too broad
```

### 3. Interpret Results

The response comes from an LLM - extract key information and apply to your context.

### 4. Complement if Needed

After Kavak docs, use additional sources:

- Context7 for external library docs
- Web search for general patterns
- Codebase search for existing implementations

## Topics & References

| Topic              | Example Query                                     | Reference                               |
| ------------------ | ------------------------------------------------- | --------------------------------------- |
| Architecture       | "What is the platform architecture?"              | -                                       |
| Kbroker (pub/sub)  | "How to publish events with kbroker?"             | `references/kbroker.md`                 |
| STS (auth)         | "How does secure token service work?"             | `references/microservice-auth.md`       |
| Workload creation  | "How to scaffold a new TypeScript service?"       | `references/workload-config.md`         |
| SDKs               | "What internal SDKs are available?"               | `references/logging-metrics.md`         |
| Databases          | "Database best practices for platform?"           | -                                       |
| Logs & Metrics     | "How to implement structured logging?"            | `references/logging-metrics.md`         |
| CLI                | "How to install and use kavak CLI?"               | -                                       |
| **GitLab CI/CD**   | "How to configure GitLab pipeline for deployment?"| `references/gitlab-ci.md`               |
| **Docker**         | "What is the standard Dockerfile template?"       | `references/docker-images.md`           |
| Container Registry | "How to push images to Kavak registry?"           | `references/docker-images.md`           |
| Pipeline Stages    | "What are the required CI stages for a service?"  | `references/gitlab-ci.md`               |
| Job Queues         | "How to implement rate limiting?"                 | `references/queues-ratelimit.md`        |

## CI/CD & Docker Queries

When working with pipelines or containers, query these topics:

```
"What is the standard .gitlab-ci.yml template?"
"How to configure multi-stage Docker builds?"
"What are the required pipeline stages for production?"
"How to configure environment variables in CI?"
"What base images should I use for Go/TypeScript/Python?"
"How to set up automated testing in GitLab CI?"
"How to configure deployment to staging/production?"
```

## Anti-Patterns

- Skipping Kavak docs and going straight to external sources
- Asking multiple questions in one query
- Writing overly long or vague queries
- Ignoring platform-specific patterns in favor of generic solutions
- Using generic Dockerfile templates instead of Kavak standards
- Copying CI configs from external projects without checking Kavak patterns

## References

| Reference                       | When to Use                                      |
| ------------------------------- | ------------------------------------------------ |
| `references/kbroker.md`         | Publish/subscribe events between services        |
| `references/queues-ratelimit.md`| Job queues, rate limiting with River/pg-boss     |
| `references/microservice-auth.md`| Authenticate between services (STS)             |
| `references/gitlab-ci.md`       | Set up kavak-it/ci-jobs v3 pipelines             |
| `references/docker-images.md`   | Build with docker-debian base                    |
| `references/workload-config.md` | Configure `.kavak/` dir, cron jobs               |
| `references/logging-metrics.md` | Use kvklog, kvkmetric SDKs                       |
