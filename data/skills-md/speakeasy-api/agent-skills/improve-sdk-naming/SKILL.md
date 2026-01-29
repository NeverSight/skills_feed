---
name: improve-sdk-naming
description: Use when SDK methods have ugly auto-generated names or you want AI-powered naming and error type suggestions. Triggers on "suggest improvements", "improve my spec", "speakeasy suggest", "better operation names", "ugly method names", "GetApiV1Users", "improve operation IDs", "sdk.users.list() style", "better SDK naming", "x-speakeasy-group", "suggest error types", "AI suggestions"
license: Apache-2.0
---

# improve-sdk-naming

Improve SDK method naming using AI-powered suggestions or manual overrides. Covers both automatic `speakeasy suggest` commands and manual naming with `x-speakeasy-group` and `x-speakeasy-name-override` extensions.

## When to Use

- SDK methods have ugly auto-generated names like `GetApiV1Users`
- You want grouped methods like `sdk.users.list()`
- You want AI-generated suggestions for operation IDs or error types
- Looking to improve spec quality automatically
- User says: "suggest improvements", "improve my spec", "better operation names", "ugly method names", "improve operation IDs", "better SDK naming", "suggest error types", "AI suggestions"

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| OpenAPI spec | Yes | Path to the spec file (`-s`) |
| Authentication | Yes | Via `speakeasy auth login` or `SPEAKEASY_API_KEY` env var |
| Output file | No | Path for overlay output (`-o`) |

## Outputs

| Output | Description |
|--------|-------------|
| Suggestions | Better operation names or error types printed to console |
| Overlay file | Optional: saves suggestions as an overlay YAML file (`-o`) |

## Prerequisites

For non-interactive environments (CI/CD, AI agents), set the API key as an environment variable:

```bash
export SPEAKEASY_API_KEY="<your-api-key>"
```

For interactive use, authenticate directly:

```bash
speakeasy auth login
```

## Command

### AI-Powered Suggestions

```bash
# Suggest better operation IDs (SDK method names)
speakeasy suggest operation-ids -s <spec-path>

# Suggest error type definitions
speakeasy suggest error-types -s <spec-path>

# Output suggestions as an overlay file
speakeasy suggest operation-ids -s <spec-path> -o suggested-overlay.yaml
```

### Check Current Operation IDs

Run the suggest command without `-o` to preview what would change:

```bash
speakeasy suggest operation-ids -s openapi.yaml
```

## SDK Method Naming Convention

Speakeasy generates grouped SDK methods from operation IDs. The naming convention uses `x-speakeasy-group` for the namespace and `x-speakeasy-name-override` for the method name.

| HTTP Method | SDK Usage | Operation ID |
|-------------|-----------|--------------|
| GET (list) | `sdk.users.list()` | `users_list` |
| GET (single) | `sdk.users.get()` | `users_get` |
| POST | `sdk.users.create()` | `users_create` |
| PUT | `sdk.users.update()` | `users_update` |
| DELETE | `sdk.users.delete()` | `users_delete` |

The operation ID format is `{group}_{method}`. Speakeasy splits on the underscore to create the namespace and method name in the generated SDK.

## Example

### Step 1: Get AI Suggestions

```bash
speakeasy suggest operation-ids -s openapi.yaml -o operation-ids-overlay.yaml
```

This analyzes your spec and generates an overlay that transforms names like:
- `get_api_v1_users_list` -> `listUsers`
- `post_api_v1_users_create` -> `createUser`

### Step 2: Manual Naming with an Overlay

If you need more control, create an overlay manually. This overlay sets `x-speakeasy-group` and `x-speakeasy-name-override` on specific operations:

```yaml
overlay: 1.0.0
info:
  title: SDK naming improvements
  version: 1.0.0
actions:
  - target: "$.paths['/api/v1/users'].get"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: list
  - target: "$.paths['/api/v1/users/{id}'].get"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: get
  - target: "$.paths['/api/v1/users'].post"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: create
  - target: "$.paths['/api/v1/users/{id}'].put"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: update
  - target: "$.paths['/api/v1/users/{id}'].delete"
    update:
      x-speakeasy-group: users
      x-speakeasy-name-override: delete
```

This produces SDK methods like `sdk.users.list()`, `sdk.users.get()`, `sdk.users.create()`, etc.

### Step 3: Add the Overlay to workflow.yaml

```yaml
sources:
  my-api:
    inputs:
      - location: ./openapi.yaml
    overlays:
      - location: ./operation-ids-overlay.yaml
```

### Step 4: Regenerate the SDK

```bash
speakeasy run --output console
```

## Error Type Suggestions

The `suggest error-types` command analyzes your API and suggests structured error responses:

```bash
speakeasy suggest error-types -s openapi.yaml
```

This suggests:
- Common HTTP error codes (400, 401, 404, 500)
- Custom error schemas appropriate for your API

Output as an overlay:

```bash
speakeasy suggest error-types -s openapi.yaml -o error-types-overlay.yaml
```

## What NOT to Do

- **Do NOT** modify operationIds directly in the source spec if it is externally managed. Use overlays instead.
- **Do NOT** use generic names like `get` or `post` without a group. Always pair `x-speakeasy-name-override` with `x-speakeasy-group`.
- **Do NOT** forget to add the generated overlay to `workflow.yaml` after creating it. Without this step, the names will not change in the generated SDK.
- **Do NOT** create duplicate operation names across different groups. Each `{group}_{method}` combination must be unique.

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "unauthorized" | Missing or invalid API key | Set `SPEAKEASY_API_KEY` env var or run `speakeasy auth login` |
| Names unchanged after regeneration | Overlay not added to workflow | Add the overlay to the `overlays` list in `workflow.yaml` |
| No suggestions returned | Spec already has good naming | No action needed; names are already well-structured |
| Duplicate method names | Similar endpoints share names | Use unique `x-speakeasy-name-override` values for each endpoint |
| Timeout during suggest | Very large spec | Try running on a smaller subset or increase timeout |
