---
name: sentry-issue
description: Use when given a Sentry issue URL and you need to fetch exception details, stacktrace, and request context using sentry-cli (and Sentry API fallback when needed).
---

# Sentry Issue Investigation

## Overview

Fetch and debug a Sentry exception from a URL with a repeatable CLI workflow.

**Core principle:** Use `sentry-cli` for auth/org/project discovery first, then fetch issue + event details. If your `sentry-cli` version has no `api` subcommand, use `curl` with the same auth token.

## When to Use

Use this skill when:
- User gives a Sentry issue URL
- You need stacktrace, request/job context, release, and tags
- You need quick root-cause clues before changing code

Do not use this skill for generic app debugging without a Sentry issue reference.

## URL Parsing

Given:
`https://buildrtech.sentry.io/issues/7261708580/?environment=demo&project=4510025524707328`

Extract:
- org slug: `buildrtech`
- issue id: `7261708580`
- project id: `4510025524707328`
- environment: `demo` (if present)

## Workflow

### 1) Verify CLI and auth

```bash
sentry-cli --version
sentry-cli info
sentry-cli organizations list
sentry-cli projects list --org <org_slug>
```

Capture whether `sentry-cli` has an `api` command:
```bash
sentry-cli --help
```

### 2) Get high-level issue metadata

If `sentry-cli` supports direct issue fetching in your version, use it.
Otherwise use REST API with token from your Sentry CLI config.

Token discovery pattern:
```bash
TOKEN=$(rg '^token=' ~/.sentryclirc | head -n1 | cut -d'=' -f2-)
```

Issue metadata:
```bash
curl -sS -H "Authorization: Bearer $TOKEN" \
  "https://sentry.io/api/0/issues/<issue_id>/"
```

This gives title, culprit, level, firstSeen, lastSeen, count, release, and status.

### 3) Get latest event for stacktrace + request context

```bash
curl -sS -H "Authorization: Bearer $TOKEN" \
  "https://sentry.io/api/0/issues/<issue_id>/events/latest/?environment=<env>"
```

If env is unknown, omit the environment query.

### 4) List all events for pattern analysis

```bash
curl -sS -H "Authorization: Bearer $TOKEN" \
  "https://sentry.io/api/0/issues/<issue_id>/events/?environment=<env>"
```

Then inspect each event by ID:

```bash
curl -sS -H "Authorization: Bearer $TOKEN" \
  "https://sentry.io/api/0/issues/<issue_id>/events/<event_id>/?environment=<env>"
```

Use this to compare users, branches, params, releases, and frequency.

## What to Extract

Always report:
- Issue title/type/message
- Culprit (controller/service/method)
- First/last seen, count, status
- Top in-app stack frames (file + line)
- Request/job context (route, params, identifiers)
- Environment, release, user info, request_id tags
- Recurrence pattern (same path? same branch id? same commit type?)

## Debugging Standard (Root Cause First)

Before proposing fixes:
1. Confirm exact throw site from in-app frame
2. Trace caller chain in local code
3. Match stacktrace behavior to request parameters
4. Identify whether failure is expected business condition vs true system fault
5. Propose fix at the boundary where error should be handled

## Output Template

```markdown
## Sentry Issue: <title>

- Issue ID: <id>
- Env: <env>
- Level: <level>
- Status: <status>
- First seen: <timestamp>
- Last seen: <timestamp>
- Occurrences: <count>

### Error
- Type: <exception class>
- Message: <message>
- Culprit: <culprit>

### In-app stacktrace highlights
- path/to/file.rb:123 in `method_name`
- ...

### Request/Job context
- Route/URL: <...>
- Key params: <...>
- User: <...>
- Release: <...>

### Root cause hypothesis
<why this fails based on evidence>

### Recommended fix
<where to handle and why>
```

## Common Pitfalls

- Assuming `sentry-cli api` exists in all versions (it may not)
- Using issue list commands and expecting full stacktrace output
- Ignoring environment filter and mixing unrelated events
- Proposing fixes before confirming throw site and call chain
- Treating expected domain errors as 500s instead of handling paths

## Quick Reference

```bash
# Auth/context
sentry-cli info
sentry-cli organizations list
sentry-cli projects list --org <org>

# Token from CLI config
TOKEN=$(rg '^token=' ~/.sentryclirc | head -n1 | cut -d'=' -f2-)

# Issue
curl -sS -H "Authorization: Bearer $TOKEN" "https://sentry.io/api/0/issues/<issue_id>/"

# Latest event
curl -sS -H "Authorization: Bearer $TOKEN" "https://sentry.io/api/0/issues/<issue_id>/events/latest/?environment=<env>"

# Event list
curl -sS -H "Authorization: Bearer $TOKEN" "https://sentry.io/api/0/issues/<issue_id>/events/?environment=<env>"
```
