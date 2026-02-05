---
name: powerlifter
description: Migrates AWS Lambda/API Gateway/RDS/SQS/S3/CloudFront backends into an existing Next.js monorepo on Vercel with Planetscale Postgres, Vercel AI Gateway, Vercel env, and Workflow Devkit. Use for node-to-next migrations, backend repo consolidation into a Next.js frontend repo, or mapping AWS serverless services to Vercel primitives with security parity.
---

# Powerlifter

Node-to-Next migration skill for consolidating a backend repo into an existing Next.js frontend repo.

## Quick start
1) Audit `serverless*.yml` (dev/prod) and inventory AWS services, routes,
   runtimes, memory, timeouts, and secrets.
2) Rank hottest endpoints/Lambdas via CloudWatch metrics and confirm
   priorities with the user.
3) Define the monorepo merge strategy and runtime boundaries.
4) Map API Gateway + Lambda routes to Next Route Handlers or Server Actions.
5) Plan data migration from RDS to Planetscale Postgres (PG dump staging).
6) Replace SQS jobs with Vercel Workflow Devkit flows.
7) Swap OpenAI SDK usage to Vercel AI Gateway.
8) Move secrets to Vercel env and rewire observability.
9) Cut over with parity tests and rollback plan.

## Safety (read-only discovery)
- Do not run `serverless deploy` commands during discovery.
- Avoid any command that modifies AWS environments or production data.

## Use when
- The frontend is already on Next.js and the backend lives in a separate repo.
- AWS serverless services must be replaced or integrated with Vercel.
- You need a secure monorepo with shared types and a single deployment surface.

## Current -> future stack map
- Compute: AWS Lambda -> Next Route Handlers / Server Actions
- Edge/CDN: CloudFront -> Vercel Edge Network
- API routing: API Gateway -> Next App Router API routes
- DB: AWS RDS -> Planetscale Postgres
- Queue: SQS -> Vercel Workflow Devkit
- AI: OpenAI SDK -> Vercel AI Gateway
- Secrets: AWS Secrets Manager -> Vercel env
- Logs: CloudWatch -> Vercel logging + external sinks
- Storage: S3 -> S3 (keep) or migrate by strategy

## Non-goals
- Rewriting the frontend UI or changing auth providers.
- Changing data semantics or removing legacy endpoints.
- Introducing new infrastructure without a clear need.

## Monorepo guardrails
- Keep the existing Next.js frontend stable; add backend code under server-only boundaries.
- Do not expose secrets in client bundles; isolate server-only modules.
- Keep routing stable: path + method parity for existing API clients.
- Favor shared types in a single location to reduce drift.

## Migration phases
1) Discovery and inventory
2) Monorepo merge and runtime boundaries
3) API surface migration
4) Data migration and cutover
5) Jobs and async flows
6) AI gateway swap
7) Secrets, observability, and security hardening
8) Staged deploy and verification

## Rule index
- Setup and inventory: `rules/setup-inventory.md`
- Monorepo merge: `rules/architecture-monorepo-merge.md`
- API migration: `rules/api-lambda-to-next.md`
- Data migration: `rules/data-rds-to-planetscale.md`
- Queues/workflows: `rules/queue-sqs-to-vercel-workflow.md`
- AI gateway: `rules/ai-openai-to-vercel-ai-gateway.md`
- Storage strategy: `rules/storage-s3-strategy.md`
- Secrets/env: `rules/secrets-env-migration.md`
- Observability: `rules/observability-cloudwatch-to-vercel.md`
- Security: `rules/security-hardening.md`
- Deploy/cutover: `rules/deploy-cutover.md`
- Testing parity: `rules/testing-parity.md`

## Verification checklist
- Route parity: same methods, paths, status codes, and payload shapes.
- Auth parity: same guards, redirects, and role-based access.
- Data parity: row counts, key constraints, and critical query results match.
- Job parity: async flows run with idempotency and reliable retries.
- Observability parity: errors and key events are logged and traceable.
- Rollback plan exists and is tested for critical flows.

## Version policy
Use the latest stable versions of Next.js and the chosen data/AI libraries.
