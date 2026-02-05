---
name: openapi-typescript-sdk-generator
description: Generate a production TypeScript SDK from an OpenAPI 3.0/3.1 spec (URL or local file), with human-friendly method names, interactive confirmation, and deterministic output. Use when the user wants a type-safe, fetch-based SDK or a drop-in client. Do not use for streaming/SSE/WebSockets or interactive OAuth flows.
---

# OpenAPI TypeScript SDK generator

Generate a production-quality TypeScript SDK from an OpenAPI specification.
Behave like a real SDK generator, not a thin OpenAPI wrapper.

## Scope and guarantees

- **Analyze the OpenAPI spec first** to propose intelligent defaults based on its contents
- Propose sensible defaults derived from the spec (title, servers, security schemes, operations, etc.)
- Ask required questions and require explicit confirmation
- Derive human-friendly method names from context, not OpenAPI identifiers
- Produce deterministic output
- Support OpenAPI 3.0 and 3.1
- Generate a typed ApiError and runtime features (retries, rate limiting, caching)
- Explain spec issues and tolerate non-blocking drift

## Inputs (prefill only)

If the user provides JSON, treat it as prefilled answers.
Still show defaults and require explicit confirmation before generating.

Example prefill:

```json
{
  "openapi_url": "https://api.example.com/openapi.yaml",
  "openapi_path": "C:/specs/openapi.yaml",
  "output_mode": "standalone_package | folder_only",
  "output_path": "sdk",
  "package_name": "@example/api-sdk",
  "client_name": "ExampleClient",
  "runtime_target": "node_and_browser",
  "node_version": "22",
  "auth_method": "bearer"
}
```

Either `openapi_url` or `openapi_path` must be provided or collected.

## Spec analysis (mandatory first step)

Before asking any questions, the agent must:

1. Load and parse the OpenAPI spec (from URL or file path)
2. Analyze the spec to extract:
   - `info.title` → for package/client naming
   - `info.version` → for package version suggestion
   - `servers` → for base URL defaults
   - `components.securitySchemes` → for auth method defaults
   - `security` (global and per-operation) → for auth method analysis
   - Operation patterns → for naming style suggestions
   - Response headers → for rate limiting/caching hints
   - Operation methods → for runtime target suggestions
3. Propose defaults based on this analysis
4. Show reasoning for each proposed default

## Mandatory interaction flow

1. **Parse and analyze the OpenAPI spec first** (if provided or collected)
   - Load the spec from URL or file path
   - Analyze the spec to propose intelligent defaults
   - Extract relevant information (title, servers, security schemes, operations, etc.)
2. Ask all required intake questions in one concise block.
3. **Show defaults for every question, proposing values derived from the OpenAPI spec analysis**
4. Require explicit confirmation of answers or defaults.
5. Show a naming preview and allow overrides.
6. Ask for a final confirmation gate before any code generation.

Do not generate code until the user explicitly confirms.

## Required intake questions (always ask)

Ask these questions in a single block and show defaults **proposed from the OpenAPI spec analysis**.

1. SDK identity
   - Package name  
     Default: derive from OpenAPI `info.title` (sanitized, lowercased, kebab-case), or `openapi-sdk` if unavailable
     Example: `"Pet Store API"` → `@pet-store/api-sdk` or `pet-store-api-sdk`
   - Exported client name  
     Default: derive from OpenAPI `info.title` (sanitized, PascalCase + "Client"), or `ApiClient` if unavailable
     Example: `"Pet Store API"` → `PetStoreClient`

2. Output
   - Output mode: `folder_only` or `standalone_package`  
     Default: `folder_only`
   - Output path (folder)  
     Default: `sdk/`

3. Spec source
   - OpenAPI URL or local file path  
     Default: use provided value; otherwise ask
   - If URL: does it require auth headers?  
     Default: no

4. Base URL
   - Default: first entry in OpenAPI `servers`
   - If no servers exist, default to empty string and warn

5. Naming style
   - Verb-first (`listPlants`, `getPlant`)
   - Resource-first (`plantsList`, `plantsGet`)  
     Default: verb-first

6. Runtime target
   - `node_only`, `browser_only`, or `node_and_browser`  
     Default: `node_and_browser`
   - Node version (if Node is included)  
     Default: `22`

7. Primary authentication method
   - API key
   - Bearer token
   - OAuth2 access token (passthrough only)
   - Basic auth
   - None  
     Default: analyze OpenAPI `security` and `components.securitySchemes` to propose the most common/primary auth method, or `none` if none exist
     - If multiple schemes exist, prefer: Bearer > API Key > OAuth2 > Basic > None
     - Show which operations use which auth methods if they differ

8. Integration tests
   - Yes, generate real integration tests (env-based, disabled by default)
   - No, generate mock-only tests  
     Default: no

## Naming preview step (mandatory)

Before generation:

- Show a preview of representative endpoints with proposed names.
- Allow user overrides.
- Proceed only after confirmation.
- Record overrides in `sdk-decisions.md`.

## Confirmation gate (mandatory)

After collecting answers and naming overrides, present a final summary and ask for explicit confirmation.

Example:

Here is what I am going to generate:

- Package name: `openapi-sdk`
- Client name: `ApiClient`
- Output mode: `folder_only`
- Output path: `sdk/`
- Base URL: `https://api.example.com`
- Naming style: verb-first
- Runtime target: node_and_browser (Node 22)
- Auth method: bearer token
- Integration tests: disabled

Reply with:

- `confirm` to proceed
- or list any changes you want

Do not generate code until the user confirms.

## Decision recording (mandatory)

After confirmation, write:

```
sdk-decisions.md
```

Record all final decisions and whether each one was explicit or default.

Example:

```md
- package_name: openapi-sdk (default, confirmed)
- client_name: ApiClient (default, confirmed)
- output_mode: folder_only (explicit)
- output_path: sdk/ (default, confirmed)
- naming_style: verb-first (default, confirmed)
- runtime_target: node_and_browser (default, confirmed)
- node_version: 22 (default, confirmed)
- integration_tests: false (default, confirmed)
```

## Output modes

### folder_only

Generate a minimal SDK folder suitable for copying into an existing codebase.

```
sdk/
├── index.ts
├── client.ts
├── operations.ts
├── errors.ts
├── types/
├── utils/
├── openapi-report.md
└── sdk-decisions.md
```

### standalone_package

Generate a full, publishable SDK project.

```
<package>/
├── package.json
├── tsconfig.json
├── tsdown.config.ts
├── README.md
├── src/
│   ├── index.ts
│   ├── client.ts
│   ├── operations.ts
│   ├── errors.ts
│   ├── types/
│   └── utils/
├── examples/
├── tests/
├── openapi-report.md
└── sdk-decisions.md
```

## Naming strategy (critical)

Do not use raw OpenAPI operationId values.

Derive names deterministically from context.

### Naming goals

- Human-friendly
- Stable across regenerations
- Flat function surface
- Predictable
- Collision-free

### Naming algorithm

1. Extract the primary resource from the path  
   Ignore version prefixes such as `/v1` or `/api`.

Examples:

- `/plants` → `plants`
- `/plants/{id}/events` → primary `plants`, secondary `events`

2. Infer the action from HTTP method and path shape

| Method | Path shape | Action |
| ------ | ---------- | ------ |
| GET    | collection | list   |
| GET    | item       | get    |
| POST   | collection | create |
| PUT    | item       | update |
| PATCH  | item       | update |
| DELETE | item       | remove |

3. Apply naming style

Verb-first:

- `listPlants`
- `getPlant`
- `updatePlant`
- `removePlant`
- `listPlantEvents`
- `createPlantEvent`

Resource-first:

- `plantsList`
- `plantsGet`
- `plantEventsList`

4. Singularize item resources

- Prefer `getPlant` over `getPlants`
- Use a small irregular map (`people` → `person`, `children` → `child`)
- If uncertain, keep plural and document it

5. Collision handling

- Prefer param-based disambiguation (`getPlantById`, `getPlantBySlug`)
- If unresolved, append a deterministic suffix (`__get`, `__post`)
- Document all collisions and resolutions in `openapi-report.md`

## OpenAPI validation and report

Validate the spec and tolerate non-blocking issues.

Generate:

```
openapi-report.md
```

Include:

- Blocking issues
- Non-blocking issues
- Why each issue matters
- What assumptions were made
- A mapping table of generated method names to original `operationId` (if present)

## SDK runtime behavior

### Transport

- Use native `fetch`
- Isomorphic (Node and browser where possible)
- ESM only

### Errors

Generate a typed ApiError with:

- status
- code
- message
- body
- headers
- method
- url

Throw ApiError for all non-2xx responses, except 304 handled by cache.

### Retries

- Retry on network errors, 429, and 5xx
- Default max attempts: 3
- Exponential backoff with jitter
- Honor `Retry-After`
- Allow per-request overrides
- Default to idempotent methods only; require explicit opt-in for POST/PATCH

### Rate limiting

- In-memory limiter per client instance
- Respect rate-limit headers and Retry-After

### Caching

- GET requests only by default
- In-memory cache with TTL
- Manual busting
- ETag / If-None-Match support
- Respect Cache-Control and Pragma
- Do not cache when Authorization is present unless explicitly enabled

## Integration tests (optional)

If enabled:

- Generate real integration tests
- Disabled by default in CI
- Credentials loaded from environment variables
- Tests perform simple read operations and validate response shape
- Required env vars documented in README

If disabled:

- Generate mock-based tests only

## Generated API surface

Each operation exports a flat async function:

```ts
listPlants(params, options?): Promise<Plant[]>
```

Options allow:

- Auth overrides
- Retry overrides
- Cache overrides
- AbortSignal
- Extra headers

## Determinism

- Sort operations by path + method for stable output
- Keep naming stable across regenerations
- Record decisions in `sdk-decisions.md`

## Acceptance criteria

Output is correct only if:

- All required questions were asked
- Defaults were shown and explicitly confirmed
- Code generation occurred only after confirmation
- Names were derived from context, not operationId
- Types compile under strict TypeScript
- Retry, cache, and rate limiting work as specified
- `openapi-report.md` and `sdk-decisions.md` exist
- Optional integration tests are safe and documented
- Output is deterministic

## Defaults (proposed from OpenAPI spec analysis)

The agent must analyze the OpenAPI spec and propose intelligent defaults:

- **Package name**: Derive from `info.title` (sanitized, kebab-case), fallback to `openapi-sdk`
- **Client name**: Derive from `info.title` (sanitized, PascalCase + "Client"), fallback to `ApiClient`
- **Base URL**: First entry in OpenAPI `servers` array, or empty string with warning if none
- **Auth method**: Analyze `security` and `components.securitySchemes` to propose primary method (prefer: Bearer > API Key > OAuth2 > Basic > None)
- **Naming style**: verb-first (unless spec patterns suggest resource-first)
- **Output mode**: folder_only
- **Output path**: sdk/ (or derive from package name if standalone_package)
- **Runtime target**: node_and_browser (analyze operations to suggest if browser-only or node-only would be more appropriate)
- **Node version**: 22
- **Cache enabled**: For GET requests (analyze spec to see if caching headers are used)
- **Retries**: Enabled for idempotent methods (analyze operations to determine idempotency)
- **Rate limiting**: Enabled (check if spec includes rate limit headers/documentation)
- **Integration tests**: Disabled

Always show the reasoning behind each proposed default based on the spec analysis.
