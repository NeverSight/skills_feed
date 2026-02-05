---
name: improve-sdk-naming
description: Use when you want AI-powered suggestions for SDK naming improvements via the `speakeasy suggest` command (not manual overlay creation). Triggers on "suggest improvements", "speakeasy suggest", "AI suggestions", "suggest operation-ids", "suggest error-types", "auto-improve naming", "get AI recommendations".
license: Apache-2.0
---

# improve-sdk-naming

Improve SDK method naming using AI-powered suggestions or manual overrides. Covers both automatic `speakeasy suggest` commands and manual naming with `x-speakeasy-group` and `x-speakeasy-name-override` extensions.

## When to Use

Use this skill when you want **AI-powered suggestions** from Speakeasy:

- SDK methods have ugly auto-generated names like `GetApiV1Users`
- You want Speakeasy AI to suggest better operation IDs
- You want AI-generated suggestions for error types
- Looking to improve spec quality automatically using `speakeasy suggest`
- User says: "suggest improvements", "speakeasy suggest", "AI suggestions", "suggest operation-ids", "suggest error-types", "get AI recommendations"

**NOT for**: Manually creating overlays (see `manage-openapi-overlays` instead)

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

### Step 2: Review and Apply the Overlay

The AI-generated overlay (from `-o`) creates naming improvements using `x-speakeasy-group` and `x-speakeasy-name-override`.

**Note**: For manual overlay creation, use the `manage-openapi-overlays` skill instead of this skill.

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
