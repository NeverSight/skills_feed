---
name: github-app-scaffold
description: "Scaffold and implement GitHub Apps from existing automation ideas using Probot + @octokit/app. Use when turning scripts, bots, or manual GitHub workflows into a proper GitHub App."
---

# GitHub App Scaffold

Turn existing GitHub automation into a real GitHub App with Probot and the modern Octokit stack.

## Stack (2026 Standard)

- Runtime: Node.js + TypeScript
- Framework: Probot
- Auth + App primitives: `@octokit/app`
- API client: `@octokit/rest` (via `context.octokit`)

Why this stack:
- Probot gives webhook-first structure, fast.
- `@octokit/app` handles JWT + installation tokens clean.
- You can drop to raw Octokit when you need control.

## Scaffold CLI

Use Probot’s official scaffolder:

```bash
npx create-probot-app my-github-app
cd my-github-app
npm run dev
```

During setup:
- Choose TypeScript.
- Choose a minimal template.
- Keep scope narrow. One automation loop per app if possible.

## Workflow

Follow this sequence. Keep it tight.

1. Identify automation opportunities.
2. Map them to webhook events + repo actions.
3. Scaffold with Probot.
4. Implement webhook handlers.
5. Lock permissions to minimum viable.
6. Deploy.
7. Verify in a staging repo/org.

Automation discovery checklist:
- What exact event starts the automation?
- What repo/issue/PR state is required?
- What GitHub writes will happen?
- What permissions are required for those writes?
- What is the failure mode? (retry, comment, label, noop)

## Project Structure

Default Probot layout is already decent:

```text
my-github-app/
├─ src/
│  └─ index.ts          # App entry, register webhooks
├─ test/                # Probot tests (add early)
├─ app.yml              # App metadata + permissions (if used)
├─ package.json
└─ tsconfig.json
```

Suggested internal structure once logic grows:

```text
src/
├─ index.ts             # wire events only
├─ handlers/
│  ├─ pull-request.ts
│  ├─ issues.ts
│  └─ push.ts
├─ domain/
│  └─ <automation>.ts   # core decision logic, testable
└─ github/
   └─ client.ts         # small helpers around octokit
```

Rule: keep webhook glue thin. Put decisions in deep modules.

## Common Use Cases

PR automation:
- Auto-label by paths changed.
- Enforce checklist comments.
- Auto-request reviewers.

Issue management:
- Triage labels by templates.
- Auto-close stale issues with escape hatches.
- Route issues to teams.

Code review bots:
- Comment on risky diffs.
- Enforce conventions on PR open/sync.
- Block merge with a status check.

CI integration:
- Trigger external systems on PR/push.
- Mirror commit status back to GitHub.
- Manage deployments via checks.

## Permissions Model

Treat permissions as an interface. Small surface.

Approach:
- Start from events + writes.
- Add only required read/write scopes.
- Prefer read-only unless you must write.

Typical mappings:
- Labeling issues/PRs → Issues: Read & Write, Pull requests: Read & Write
- Commenting → Issues or Pull requests: Read & Write
- Status checks → Commit statuses or Checks: Read & Write
- Repo config reads → Metadata: Read-only (always)

Keep a simple table in the repo:
- Action
- API call
- Permission required

## Deployment Options

Pick the simplest host that fits the webhook model.

Good defaults:
- Vercel: fast for webhook handlers.
- Cloud functions: AWS Lambda, GCP Cloud Functions, Azure Functions.
- Self-hosted: long-lived workers, queues, custom infra.

Notes:
- Probot can run serverless with light glue.
- For heavier automations, use queues and idempotency keys.
- Keep webhook latency low; defer heavy work.

## Verification Steps

Do not skip this.

Local loop:

```bash
npm run dev
```

Then:
1. Create a GitHub App (dev) and install it on a staging repo.
2. Point the webhook URL to your dev tunnel.
3. Trigger the event (open PR, edit issue, push).
4. Confirm logs show the expected handler path.
5. Confirm the GitHub side effect happened (label, comment, check).
6. Run tests for decision logic + handlers.

Minimal verification checklist:
- Event received.
- Guardrails applied (repo, org, branch filters).
- API calls succeed.
- No duplicate side effects.
- Permissions are sufficient but not excessive.

See: `skills/github-app-scaffold/references/probot-patterns.md`.

