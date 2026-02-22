---
name: arazzo-writer
description: >-
  Create and edit Arazzo workflow specification files (.arazzo.yaml) for API testing
  and orchestration. Use when building API test workflows, defining multi-step API
  sequences, writing API integration tests, or documenting API usage patterns.
  Triggers include: "arazzo", "workflow spec", "API workflow", "multi-step API
  test", ".arazzo.yaml", "orchestrate calls", or any request to describe API
  workflows with assertions.
---

# Arazzo Workflow Authoring Guide

## Overview

Arazzo describes end-to-end API workflows: ordered steps, shared data, assertions, and branching. Use this skill whenever you must express API testing scenarios, integration guides, or automation flows as reusable YAML/JSON documents that complement OpenAPI specs.

**Scope focus:** API testing workflows (success criteria, failure handling, reusable components) with moderate depth. Load the reference files when you need the full syntax:
- [Runtime expressions](references/expression-syntax.md)
- [Validation + tooling](references/validation-guide.md)

## When to Activate This Skill
- User asks for an ".arazzo.yaml" file or says "write an Arazzo workflow"
- They need multi-step API test cases, orchestration, regression flows, or scenario documentation
- Tasks mention chaining OpenAPI operations, asserting responses, or coordinating multiple APIs
- They ask to explain how data flows between API calls in a workflow narrative

## Document Structure (Root Object)
| Field | Required | Notes |
| --- | --- | --- |
| `arazzo` | ✅ | Version string, e.g. `"1.0.1"`
| `info` | ✅ | `title`, `version`, optional `summary`/`description`
| `sourceDescriptions` | ✅ | Each entry = API source (OpenAPI/Arazzo)
| `workflows` | ✅ | One or more workflow objects
| `components` | ➖ | Optional reusable inputs/parameters/actions

Minimal skeleton:
```yaml
arazzo: 1.0.1
info:
  title: My Workflow Suite
  version: 0.1.0
sourceDescriptions:
  - name: petStore
    url: https://example.com/petstore.yaml
    type: openapi
workflows: []
```

## Authoring Workflow Objects
1. **Name it:** `workflowId` must be unique and `[A-Za-z0-9_-]+`.
2. **Describe purpose:** Use `summary`/`description` to explain the scenario.
3. **Inputs:** Provide a JSON Schema (2020-12). Reuse `components.inputs` where possible.
4. **Dependencies:** Use `dependsOn` if another workflow must finish first.
5. **Defaults:** `parameters`, `successActions`, `failureActions` here cascade to every step.
6. **Outputs:** Map friendly names to runtime expressions for later workflows or end users.

Pattern:
```yaml
workflows:
  - workflowId: applyCoupon
    summary: Apply discounts during checkout
    inputs:
      $ref: '#/components/inputs/apply_coupon'
    parameters:
      - reference: $components.parameters.defaultLocale
    steps: [...]
    outputs:
      confirmationId: $steps.submitOrder.outputs.orderId
```

## Designing Steps
Each `step` executes an OpenAPI operation or another workflow.

| Field | Requirement |
| --- | --- |
| `stepId` | Unique per workflow |
| `operationId`/`operationPath`/`workflowId` | Exactly one must be present |
| `operationPath` | Must concatenate the source `url` with a JSON Pointer (e.g. `"{$sourceDescriptions.petApi.url}#/paths/~1foo/get"`) |
| `parameters` | Required `in` when calling operations, omitted for workflow calls |
| `requestBody` | `contentType`, `payload`, optional `replacements` |
| `successCriteria` | Assertions (status, body, headers, custom logic) |
| `outputs` | Runtime expressions that downstream steps can consume |
| `onSuccess` / `onFailure` | Action arrays (in addition to workflow-level defaults) |

Example API-testing step:
```yaml
- stepId: verifyInventory
  operationId: getInventory
  successCriteria:
    - condition: $statusCode == 200
    - context: $response.body
      type: jsonpath
      condition: $[?(@.inStock >= $inputs.minimumRequired)]
      # For null checks use: $[?(@.user != null)]
      # For comparisons with step outputs: $[?(@.article.slug == $steps.createArticle.outputs.slug)]
  outputs:
    remaining: $response.body#/inStock
```

## Request Bodies & Payload Replacements
- `payload` can embed expressions (`"{$inputs.orderId}"`).
- Use `replacements` for large bodies or to avoid fragile string interpolation.
```yaml
requestBody:
  contentType: application/json
  payload: !include ./payloads/cart.json
  replacements:
    - target: /customer/id
      value: $inputs.customerId
    - target: /items/0/sku
      value: $steps.pickSku.outputs.selectedSku
```

## Sharing Data Between Steps
- `outputs` expose data from responses (`$response.body#/id`).
- Reference them via `$steps.stepId.outputs.key`.
- Workflow outputs return values upward or to sibling workflows via `goto`.
- Chain external workflows using `$workflows.workflowId.outputs.key`.

Refer to `references/expression-syntax.md` for every valid prefix (`$inputs`, `$steps`, `$response`, etc.), JSON Pointer usage, and embedding expressions inside strings.

## Assertions & Criteria (API Testing Focus)
Use `successCriteria` (per step) and optional `criteria` arrays inside actions.

Common patterns:
- **Status check:** `- condition: $statusCode == 201`
- **Header assertion:** `- condition: $response.header.Location != null`
- **JSONPath:**
  ```yaml
  - context: $response.body
    type: jsonpath
    condition: $[?(@.errors == null)]
  ```
- **Regex:** verify formatted IDs.
- **XPath:** only when responses are XML.

> Criteria arrays are ANDed: every entry must pass. Keep conditions granular so failures are obvious.

## Success & Failure Actions
- **Success actions:** `type: end` or `goto` another step/workflow.
- **Failure actions:** `end`, `goto`, or `retry` (with `retryAfter` seconds + optional `retryLimit`).
- Scope: define at workflow level for defaults, override at step level when necessary.

Example failure handling:
```yaml
failureActions:
  - name: abortOn429
    type: retry
    retryAfter: 5
    retryLimit: 3
    criteria:
      - condition: $statusCode == 429
  - name: escalate
    type: end
```

## Reusable Components
Keep `SKILL.md` concise by reusing objects:
```yaml
components:
  parameters:
    tenantHeader:
      name: X-Tenant
      in: header
      value: $inputs.tenant
```
Reference via `reference: $components.parameters.tenantHeader` and optionally override `value`.

## Writing Process (Recommended Steps)
1. **Gather references:** OpenAPI docs, sample payloads, business rules.
2. **Define sources:** Add each OpenAPI/Arazzo document under `sourceDescriptions`.
3. **Sketch workflows:** Outline user goals and dependencies.
4. **Model inputs:** Use JSON Schema, include enums/formats (`date-time`, `uri`, etc.).
5. **Enumerate steps:** Identify API calls/workflows, required params, and success assertions.
6. **Plan data flow:** Decide which response fields become outputs.
7. **Add branching:** Use `onSuccess/onFailure` with criteria for conditional paths.
8. **Document outputs:** Summaries of what the workflow returns to callers.
9. **Validate:** See validation section.
10. **Package:** Keep file names meaningful (e.g., `checkout-tests.arazzo.yaml`).

## Validation Workflow
1. **YAML syntax:** Use PyYAML or another parser before semantic checks.
2. **CLI detection (agentic loop):** Run `command -v openapi` (or `which openapi` on Windows `where openapi`). If the binary exists, execute `openapi arazzo validate path/to/workflow.arazzo.yaml` yourself and include the output in your response. This validation step is part of the agentic workflow, not a user todo.
3. **Schema fallback:** If the CLI is unavailable, explicitly state that you attempted to detect it, then follow the manual instructions in `references/validation-guide.md` (install the CLI or run the official Node validator) and proceed with whichever option is possible in the current environment.

## API Testing Patterns to Reuse
| Pattern | Description |
| --- | --- |
| **Authentication + reuse** | Authenticate once, export token in workflow outputs, reuse via `$workflows.auth.outputs.token` |
| **CRUD regression** | Steps: create -> read -> update -> delete, each with assertions |
| **Error path coverage** | Simulate failure inputs, assert expected error codes and messages |
| **Pagination sweep** | Loop via workflow recursion or repeated `goto` while `nextPage` exists |
| **Third-party fallback** | Chain multiple sourceDescriptions, branch on availability |

## Critical Rules & Gotchas
- `operationId`, `operationPath`, `workflowId`: exactly one per step.
- **operationPath format:** Must use the exact format `{$sourceDescriptions.<name>.url}#/paths/~1<path>/<method>` where:
  - `<name>` is the sourceDescription name
  - `<path>` is the API path with `/` escaped as `~1`
  - `<method>` is get, post, put, delete, etc.
  - Example: `{$sourceDescriptions.petApi.url}#/paths/~1pets/get`
- **JSONPath filter expressions:** The validator uses RFC 9535 syntax. Filter expressions must use the full filter syntax:
  - ❌ `$[?@.user != null]` - invalid
  - ❌ `@.user != null` - invalid  
  - ✅ `$[?(@.user != null)]` - valid
  - ✅ `$[?(@.article.slug == $steps.createArticle.outputs.slug)]` - valid for comparisons
- **outputs expressions:** Must start with `$`. Do not use literal values:
  - ❌ `true` - invalid
  - ❌ `$statusCode == 204` - invalid (this is a condition, not an output)
  - ✅ `$response.body#/id` - valid
- Parameter objects calling OpenAPI ops must include `in` (`path`, `query`, `header`, `cookie`).
- Output keys must match `^[a-zA-Z0-9._-]+$`.
- `successCriteria` arrays default to logical AND; there is no implicit OR.
- JSON Pointer fragments must escape `/` as `~1` and `~` as `~0`.
- `retry` failure actions must provide `retryAfter` (seconds) and optional `retryLimit` (default 1).
- When referencing other sourceDescriptions in runtime expressions, always prefix with `$sourceDescriptions.name...` if more than one non-Arazzo source exists.
- Keep SKILL.md under 500 lines; move deep dives into reference files.

## Troubleshooting Checklist
- **Validation fails immediately:** Confirm `arazzo` version string is `1.0.x` and matches schema.
- **operationPath errors ("must contain a json pointer" or "must reference the url"):** Ensure format is exactly `{$sourceDescriptions.<name>.url}#/paths/~1<path>/<method>`. The `url` part is required - do not use other properties.
- **jsonpath expression errors ("unexpected token when parsing segment"):** Filter expressions must use RFC 9535 format `$[?(@.<field> <operator> <value>)]`. Do NOT use bare filter expressions like `@.user != null`.
- **outputs expression errors ("must begin with $"):** Outputs must be runtime expressions starting with `$`. Use JSON Pointer syntax like `$response.body#/fieldName` to extract values.
- **Operation resolution errors:** Ensure each `operationId` exists within the referenced OpenAPI source.
- **Missing data:** Check that the previous step's `outputs` actually expose the field you reference.
- **Circular `goto`:** Validate that branching paths eventually terminate or return to safe steps.
- **YAML anchors/aliases:** Supported, but avoid overuse—explicit values are easier to validate.

## Reference Library
Load these as needed:
- [Runtime expression catalog](references/expression-syntax.md)
- [Validation + tooling guide](references/validation-guide.md)
- Official spec (latest): https://github.com/OAI/Arazzo-Specification/tree/main/versions
- Examples (1.0.0): https://github.com/OAI/Arazzo-Specification/tree/main/examples/1.0.0

> Keep this skill focused on practical authoring steps. When edge cases arise (custom expression engines, exotic media types, etc.), cite the official spec within the conversation instead of copying large excerpts here.
