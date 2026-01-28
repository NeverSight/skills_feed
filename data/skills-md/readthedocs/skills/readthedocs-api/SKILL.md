---
name: readthedocs-api
description: Full Read the Docs API v3 client guidance. Use when building or updating an API client, generating requests, or answering questions about Read the Docs API v3 endpoints (projects, versions, builds, subprojects, translations, redirects, environment variables, organizations, remote VCS resources, or embed content).
---

# Read the Docs API v3 client

Build or update API v3 requests against Read the Docs, and use the bundled references for endpoint-specific details.

## Workflow

1. Choose the correct host.
   - Community: `https://app.readthedocs.org`
   - Read the Docs for Business: `https://app.readthedocs.com`

2. Authenticate when needed.
   - Use `Authorization: Token <token>` for user-scoped data and write operations.
   - Session authentication is allowed for dashboard/internal uses.

3. Pick the endpoint from the short reference.
   - Use `references/api-v3-short.md` to select the method, path, and high-level parameters.

4. Fill in details from the full reference.
   - Use `references/api-v3-full.md` for request bodies, query parameters, response fields, status codes, and notes.

5. Handle shared API behavior.
   - Pagination: list endpoints return `count`, `next`, `previous`, and `results`; use `limit` and `offset`.
   - Field selection: `?fields=`, `?omit=`, and `?expand=` are supported on resources that allow expansion.
   - Rate limits: unauthenticated requests are more limited than authenticated requests; retry on `429`.

## Notes and constraints

- Use the marketing names: "Read the Docs Community" and "Read the Docs Business".
- Organization endpoints and privacy-level fields are only available on Read the Docs Business.
- `expand` values are endpoint-specific; rely on the full reference for allowed values.

## Resources

- Short endpoint reference: `references/api-v3-short.md`
- Full endpoint reference: `references/api-v3-full.md`
- Additional full reference: `https://docs.readthedocs.com/platform/stable/api/v3.html`
