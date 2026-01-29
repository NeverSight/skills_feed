---
name: generate-terraform-provider
description: >-
  Use when generating a Terraform provider from an OpenAPI spec with Speakeasy.
  Covers entity annotations, CRUD mapping, type inference, workflow configuration,
  and publishing. Triggers on "terraform provider", "generate terraform",
  "create terraform provider", "CRUD mapping", "x-speakeasy-entity",
  "terraform resource", "terraform registry".
license: Apache-2.0
---

# generate-terraform-provider

Generate a Terraform provider from an OpenAPI specification using the Speakeasy CLI. This skill covers the full lifecycle: annotating your spec with entity metadata, mapping CRUD operations, generating the provider, configuring workflows, and publishing to the Terraform Registry.

## When to Use

- Generating a new Terraform provider from an OpenAPI spec
- Annotating an OpenAPI spec with `x-speakeasy-entity` and `x-speakeasy-entity-operation`
- Mapping API operations to Terraform CRUD methods
- Understanding Terraform type inference from OpenAPI schemas
- Configuring `workflow.yaml` for Terraform provider generation
- Publishing a provider to the Terraform Registry
- User says: "terraform provider", "generate terraform", "create terraform provider", "CRUD mapping", "x-speakeasy-entity", "terraform resource", "terraform registry"

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| OpenAPI spec | Yes | OpenAPI 3.0 or 3.1 specification (local file, URL, or registry source) |
| Provider name | Yes | PascalCase name for the provider (e.g., `Petstore`) |
| Package name | Yes | Lowercase package identifier (e.g., `petstore`) |
| Entity annotations | Yes | `x-speakeasy-entity` on schemas, `x-speakeasy-entity-operation` on operations |

## Outputs

| Output | Location |
|--------|----------|
| Workflow config | `.speakeasy/workflow.yaml` |
| Generation config | `gen.yaml` |
| Generated Go provider | Output directory (default: current dir) |
| Terraform examples | `examples/` directory |

## Prerequisites

1. **Speakeasy CLI** installed and authenticated
2. **OpenAPI 3.0 or 3.1** specification with entity annotations
3. **Go** installed (Terraform providers are written in Go)
4. **Authentication**: Set `SPEAKEASY_API_KEY` env var or run `speakeasy auth login`

```bash
export SPEAKEASY_API_KEY="<your-api-key>"
```

Run `speakeasy auth login` to authenticate interactively, or set the `SPEAKEASY_API_KEY` environment variable.

## Command

### First-time generation (quickstart)

```bash
speakeasy quickstart --skip-interactive --output console \
  -s <spec-path> \
  -t terraform \
  -n <ProviderName> \
  -p <package-name>
```

### Regenerate after changes

```bash
speakeasy run --output console
```

### Regenerate a specific target

```bash
speakeasy run -t <target-name> --output console
```

## Entity Annotations

Before generating, annotate your OpenAPI spec with two extensions:

### 1. Mark schemas as entities

Add `x-speakeasy-entity` to component schemas that should become Terraform resources:

```yaml
components:
  schemas:
    Pet:
      x-speakeasy-entity: Pet
      type: object
      properties:
        id:
          type: string
          readOnly: true
        name:
          type: string
        price:
          type: number
      required:
        - name
        - price
```

### 2. Map operations to CRUD methods

Add `x-speakeasy-entity-operation` to each API operation:

```yaml
paths:
  /pets:
    post:
      x-speakeasy-entity-operation: Pet#create
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Pet"
      responses:
        "200":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Pet"
  /pets/{id}:
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: string
    get:
      x-speakeasy-entity-operation: Pet#read
      responses:
        "200":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Pet"
    put:
      x-speakeasy-entity-operation: Pet#update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Pet"
      responses:
        "200":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Pet"
    delete:
      x-speakeasy-entity-operation: Pet#delete
      responses:
        "204":
          description: Deleted
```

### CRUD Mapping Summary

| HTTP Method | Path | Annotation | Purpose |
|-------------|------|------------|---------|
| `POST` | `/resource` | `Entity#create` | Create a new resource |
| `GET` | `/resource/{id}` | `Entity#read` | Read a single resource |
| `PUT` | `/resource/{id}` | `Entity#update` | Update a resource |
| `DELETE` | `/resource/{id}` | `Entity#delete` | Delete a resource |

**Data sources (list):** For list endpoints (`GET /resources`), use a separate plural entity name with `#read` (e.g., `Pets#read`). Do NOT use `#list` -- it is not a valid operation type.

## Terraform Type Inference

Speakeasy infers Terraform schema types from the OpenAPI spec automatically:

| Rule | Condition | Terraform Attribute |
|------|-----------|---------------------|
| **Required** | Property is `required` in CREATE request body | `Required: true` |
| **Optional** | Property is not `required` in CREATE request body | `Optional: true` |
| **Computed** | Property appears in response but not in CREATE request | `Computed: true` |
| **ForceNew** | Property exists in CREATE request but not in UPDATE request | `ForceNew` (forces resource recreation) |
| **Enum validation** | Property defined as enum | `Validator` added for runtime checks |

Every parameter needed for READ, UPDATE, or DELETE must either appear in the CREATE response or be required in the CREATE request.

## Example

### Full workflow: Petstore provider

```bash
# 1. Ensure your spec has entity annotations (see above)

# 2. Generate the provider
speakeasy quickstart --skip-interactive --output console \
  -s ./openapi.yaml \
  -t terraform \
  -n Petstore \
  -p petstore

# 3. Build and test
cd terraform-provider-petstore
go build ./...
go test ./...

# 4. After spec changes, regenerate
speakeasy run --output console
```

This produces a Terraform resource usable as:

```hcl
resource "petstore_pet" "my_pet" {
  name  = "Buddy"
  price = 1500
}
```

## Workflow Configuration

### Local spec

```yaml
# .speakeasy/workflow.yaml
workflowVersion: 1.0.0
speakeasyVersion: latest
sources:
  my-api:
    inputs:
      - location: ./openapi.yaml
targets:
  my-provider:
    target: terraform
    source: my-api
```

### Remote spec with overlays

For providers built against third-party APIs, fetch the spec remotely and apply local overlays:

```yaml
# .speakeasy/workflow.yaml
workflowVersion: 1.0.0
speakeasyVersion: latest
sources:
  vendor-api:
    inputs:
      - location: https://api.vendor.com/openapi.yaml
    overlays:
      - location: terraform_overlay.yaml
    output: openapi.yaml
targets:
  vendor-provider:
    target: terraform
    source: vendor-api
```

Use `speakeasy overlay compare` to track upstream API changes:

```bash
speakeasy overlay compare \
  --before https://api.vendor.com/openapi.yaml \
  --after terraform_overlay.yaml \
  --out overlay-diff.yaml
```

## Repository and Naming Conventions

### Repository naming

Name the repository `terraform-provider-XXX`, where `XXX` is the provider type name. The provider type name should be lowercase alphanumeric (`[a-z][a-z0-9]`), though hyphens and underscores are permitted.

### Entity naming

Use **PascalCase** for entity names so they translate correctly to Terraform's underscore naming:

| Entity Name | Terraform Resource |
|-------------|-------------------|
| `Pet` | `petstore_pet` |
| `GatewayControlPlane` | `konnect_gateway_control_plane` |
| `MeshControlPlane` | `konnect_mesh_control_plane` |

For list data sources, use the plural PascalCase form (e.g., `Pets`).

## Resource Importing

Generated providers support importing existing resources into Terraform state.

### Simple keys

For resources with a single ID field:

```bash
terraform import petstore_pet.my_pet my_pet_id
```

### Composite keys

For resources with multiple ID fields, pass a JSON-encoded object:

```bash
terraform import my_test_resource.my_example \
  '{ "primary_key_one": "9cedad30-...", "primary_key_two": "e20c40a0-..." }'
```

Or use an import block:

```hcl
import {
  id = jsonencode({
    primary_key_one: "9cedad30-..."
    primary_key_two: "e20c40a0-..."
  })
  to = my_test_resource.my_example
}
```

Then generate configuration:

```bash
terraform plan -generate-config-out=generated.tf
```

## Publishing to the Terraform Registry

Publishing requires:

1. A **public** GitHub repository named `terraform-provider-{name}`
2. A **GPG signing key** for release signing
3. A **GoReleaser** configuration and GitHub Actions workflow
4. **Registration** with the Terraform Registry at [registry.terraform.io](https://registry.terraform.io)

The Speakeasy Generation GitHub Action automates versioning and release. After initial registration, subsequent updates publish automatically when PRs are merged.

For detailed publishing steps, set up GPG signing keys, configure a GitHub Actions workflow with `speakeasy-api/sdk-generation-action`, and use GoReleaser to build and publish the provider binary.

## Beta Provider Pattern

For large APIs, maintain separate **stable** and **beta** providers:

- **Stable**: `terraform-provider-{name}` with semver (`x.y.z`)
- **Beta**: `terraform-provider-{name}-beta` with `0.x` versioning

Users can install both simultaneously. When beta features mature, graduate them to the stable provider. To set up a beta provider, create a separate `terraform-provider-{name}-beta` repository with its own `gen.yaml` using `0.x` versioning, and publish it alongside the stable provider.

## What NOT to Do

- **Do NOT** use `#list` as an operation type -- only `create`, `read`, `update`, `delete` are valid
- **Do NOT** modify generated Go code directly -- changes are overwritten on regeneration. Use overlays or hooks instead
- **Do NOT** omit the CREATE response body -- Terraform needs the response to populate computed fields (e.g., `id`)
- **Do NOT** skip `x-speakeasy-entity` on schemas -- without it, Speakeasy cannot identify Terraform resources
- **Do NOT** use camelCase or snake_case for entity names -- use PascalCase so Terraform underscore naming works
- **Do NOT** generate Terraform providers in monorepo mode -- HashiCorp requires a dedicated repository

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `invalid entity operation type: list` | Used `#list` instead of `#read` | Change to `Entity#read`; list endpoints use a plural entity name |
| Resource missing fields after import | READ operation does not return all attributes | Ensure the GET endpoint returns the complete resource schema |
| `ForceNew` on unexpected field | Field exists in CREATE but not UPDATE request | Add the field to the UPDATE request body if it should be mutable |
| Provider fails to compile | Missing Go dependencies | Run `go mod tidy` in the provider directory |
| Computed field not populated | Field absent from CREATE response | Ensure the CREATE response returns the full resource including computed fields |
| Entity not appearing as resource | Missing `x-speakeasy-entity` annotation | Add `x-speakeasy-entity: EntityName` to the component schema |
| Auth not working | Missing API key | Set `SPEAKEASY_API_KEY` env var or run `speakeasy auth login` |
