---
name: api-security-spectral
description: Run Spectral to lint OpenAPI and AsyncAPI specs for security issues. Validates API design for authentication, authorization, rate limiting, and input validation patterns.
---

# API Spec Linting with Spectral

You are a security engineer linting OpenAPI/AsyncAPI specifications using **Spectral** to enforce security best practices in API design.

## When to use

Use this skill when asked to review an OpenAPI (Swagger) or AsyncAPI spec for security issues before deployment.

## Prerequisites

- Spectral installed (`npm install -g @stoplight/spectral-cli`)
- Verify: `spectral --version`

## Instructions

1. **Identify the target** — Determine the API spec file (YAML/JSON).
2. **Run the scan:**
   ```bash
   spectral lint <spec-file> --format json > spectral-results.json
   ```
   - With custom ruleset: `spectral lint <spec> --ruleset .spectral.yml --format json`
   - Specific format: `spectral lint openapi.yaml --format pretty`
3. **Parse the results** — Read JSON output and present findings:

```
| # | Severity | Rule | Path | Message | Line |
|---|----------|------|------|---------|------|
```

4. **Summarize** — Provide total issues by severity and specific spec fixes.

## Key Security Rules to Check

| Rule | Description |
|------|-------------|
| `oas3-api-servers` | API servers must use HTTPS |
| `operation-operationId` | All operations need unique IDs |
| `operation-description` | Operations should be documented |
| Security scheme defined | OAuth2/API key/Bearer token present |
| Input validation | Request body schema with constraints |
| Error responses | 401, 403, 429 responses defined |
| Rate limiting | Headers for rate limit documented |
| No eval/dynamic paths | Path parameters properly constrained |

## Custom Security Ruleset

Create `.spectral.yml` with security-focused rules:
```yaml
extends: ["spectral:oas"]
rules:
  oas3-server-https:
    description: Server URLs must use HTTPS
    given: "$.servers[*].url"
    then:
      function: pattern
      functionOptions:
        match: "^https://"
```
