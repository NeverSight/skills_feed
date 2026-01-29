---
name: sdk-tf-generation-best-practices
description: >-
  Use when generating SDKs, Terraform providers, or MCP servers with Speakeasy,
  or when needing best practices for SDK/Terraform generation, customization,
  testing, or OpenAPI spec management. Triggers on "generate SDK", "regenerate
  SDK", "update SDK", "create terraform provider", "generate MCP server", "SDK
  best practices", "speakeasy generation", "SDK customization", "fix generation",
  "SDK hooks", "SDK testing", "test my SDK", "openapi overlay", "upgrade
  speakeasy", "bump version", "SDK readme", "SDK documentation", "add examples
  to spec".
license: Apache-2.0
---

# sdk-tf-generation-best-practices

Comprehensive best-practices reference for generating SDKs and Terraform providers with Speakeasy. Covers the full lifecycle: OpenAPI spec preparation, code-first extraction, generation workflows, language-specific guides, customization, and testing.

## When to Use

- Generating an SDK from an OpenAPI spec
- Generating a Terraform provider from an OpenAPI spec
- Generating an MCP server from an OpenAPI spec
- Extracting an OpenAPI spec from existing code (FastAPI, Flask, Django, Spring Boot, NestJS, Hono, Rails, Laravel)
- Customizing SDK generation (hooks, auth, error handling, retries, pagination)
- Fixing OpenAPI validation errors or applying overlays
- Testing generated SDKs (integration, contract, Arazzo)
- Understanding language-specific SDK patterns (TypeScript, Python, Go, Java, C#, Ruby, PHP)
- Upgrading or bumping the Speakeasy CLI version in workflow.yaml
- Regenerating an SDK after spec or version changes
- Customizing SDK README documentation
- Adding examples to an OpenAPI spec via overlays
- Testing generated SDK endpoints
- User says: "generate SDK", "regenerate SDK", "update SDK", "SDK best practices", "terraform provider", "generate MCP server", "SDK customization", "SDK testing", "test my SDK", "upgrade speakeasy", "bump version", "SDK readme", "SDK documentation", "add examples to spec"

## How to Use

This skill contains detailed guides in the `content/` subdirectory relative to this file. **Read the specific guide** for the user's task rather than trying to answer from this index alone.

These guides are also accessible via the Speakeasy CLI:
```bash
speakeasy agent context [path]
```

To find the right guide, use the routing table below or the decision tree.

## Quick Routing Table

**What are you trying to do?**

| Goal | Start Here |
|------|------------|
| Generate an SDK from an OpenAPI spec | `content/plans/sdk-generation.md` |
| Generate a Terraform provider | `content/plans/tf-provider-generation.md` |
| Extract OpenAPI from existing code | `content/code-first/[framework].md` |
| Fix OpenAPI validation errors | `content/spec-first/validation.md` |
| Customize SDK generation | `content/sdk-customization/` |
| Generate multiple SDK variants (Azure, GCP, etc.) | `content/sdk-customization/multi-target-sdks.md` |
| Set up a multi-SDK monorepo | `content/plans/sdk-generation.md#advanced-multi-sdk-monorepos` |
| Use overlay recipes (open enums, global headers) | `content/spec-first/overlays.md#overlay-recipes` |
| Use multi-overlay workflows | `content/spec-first/overlays.md#multi-overlay-workflow-patterns` |
| Track overlay changes with metadata | `content/spec-first/overlays.md#overlay-metadata-tracking` |
| Implement custom security (HMAC, signatures) | `content/spec-first/overlays.md#custom-security-schemes-via-overlay` |
| Add SDK hooks (user-agent, telemetry) | `content/sdk-customization/hooks.md` |
| Implement HTTP signature authentication | `content/sdk-customization/hooks.md#custom-security-hook-http-signature-authentication` |
| Configure SDK retries, timeouts, pagination | `content/sdk-customization/runtime-configuration.md` |
| Configure SDK authentication and security | `content/sdk-customization/authentication-config.md` |
| Customize SDK error handling | `content/sdk-customization/error-handling.md` |
| Persist custom code changes across regenerations | `content/sdk-customization/custom-code.md` |
| Generate MCP server for AI assistants | `content/sdk-customization/mcp-server.md` |
| Orchestrate multi-repo SDK generation | `content/sdk-customization/multi-repo-workflows.md` |
| Understand SDK language specifics | `content/sdk-languages/[language].md` |
| Add custom utilities to Python SDKs | `content/sdk-languages/python.md#extending-the-sdk-with-sidecar-utilities` |
| Publish Java SDK to Maven Central | `content/sdk-languages/java.md#maven-central-publishing` |
| Add custom code to TypeScript SDKs | `content/sdk-languages/typescript.md#custom-code-regions` |
| Publish TypeScript SDK to JSR (Deno) | `content/sdk-languages/typescript.md#jsr-deno-publishing` |
| Configure Ruby SDK with Sorbet typing | `content/sdk-languages/ruby.md#sorbet-type-checking` |
| Publish Ruby SDK to RubyGems | `content/sdk-languages/ruby.md#rubygems-publishing` |
| Configure PHP SDK with Laravel integration | `content/sdk-languages/php.md#laravel-integration` |
| Publish PHP SDK to Packagist | `content/sdk-languages/php.md#publishing-to-packagist` |
| Generate Go SDK with interfaces for testing | `content/sdk-languages/go.md#interface-generation` |
| Use Go SDK in Kubernetes operators | `content/sdk-languages/go.md#kubernetes-operator-integration` |
| Set up SDK integration tests | `content/sdk-testing/integration-testing.md` |
| Configure Arazzo API testing | `content/sdk-testing/arazzo-testing.md` |
| Disable tests for specific endpoints | `content/sdk-testing/arazzo-testing.md#disabling-tests-via-overlay` |
| Run AI-powered contract tests | `content/sdk-testing/contract-testing.md` |
| Fix ResponseValidationError at runtime | `content/sdk-testing/contract-testing.md` |
| Validate spec matches live API | `content/spec-first/validation.md#dynamic-validation-contract-testing` |
| Upgrade Speakeasy version in workflow.yaml | `content/plans/sdk-generation.md#version-management` |
| Bump pinned speakeasyVersion to latest | `content/plans/sdk-generation.md#version-management` |
| Regenerate SDK after spec or version change | `content/plans/sdk-generation.md` |
| Customize SDK README with documentation | `content/sdk-customization/readme-customization.md` |
| Add branding, examples, or guides to SDK README | `content/sdk-customization/readme-customization.md` |
| Add examples to OpenAPI spec via overlay | `content/spec-first/overlays.md#add-examples` |
| Add API-response-based examples to spec | `content/spec-first/overlays.md#add-examples` |
| Test SDK against live API | `content/sdk-testing/integration-testing.md` |
| Run contract tests for generated SDK | `content/sdk-testing/contract-testing.md` |

## Directory Structure

```
content/
├── INDEX.md                    # This index (SKILL.md)
├── plans/                      # Decision trees for workflows
│   ├── sdk-generation.md       # Full SDK generation workflow
│   └── tf-provider-generation.md
├── code-first/                 # Extract OpenAPI from code
│   ├── fastapi.md
│   ├── flask.md
│   ├── django.md
│   ├── spring-boot.md
│   ├── nestjs.md
│   ├── hono.md
│   ├── rails.md
│   └── laravel.md
├── spec-first/                 # OpenAPI validation and fixes
│   ├── validation.md
│   ├── overlays.md             # OpenAPI overlays and recipes
│   ├── security-schemes.md
│   ├── pagination.md
│   └── schemas.md
├── sdk-languages/              # Language-specific SDK guides
│   ├── python.md
│   ├── typescript.md           # TS: code regions, extra modules, Zod
│   ├── go.md                   # Go: hooks, interfaces, mocks, K8s
│   ├── java.md
│   ├── csharp.md
│   ├── ruby.md                 # Ruby: Sorbet typing, RubyGems publishing
│   └── php.md
├── sdk-customization/          # Cross-language SDK customization
│   ├── hooks.md                # SDK hooks (UA, telemetry, custom security)
│   ├── runtime-configuration.md # Retries, timeouts, pagination, servers
│   ├── authentication-config.md # Global/per-op security, env vars
│   ├── error-handling.md       # Custom error classes and schemas
│   ├── custom-code.md          # Persist changes across regenerations
│   ├── multi-target-sdks.md    # Multiple variants from one repo
│   ├── multi-repo-workflows.md # Cross-repo SDK orchestration (CI/CD)
│   ├── mcp-server.md           # MCP server for AI assistant integration
│   └── readme-customization.md # SDK README branding
├── sdk-testing/                # SDK testing patterns
│   ├── integration-testing.md  # Integration test infrastructure
│   ├── arazzo-testing.md       # Arazzo API testing format
│   └── contract-testing.md     # AI-powered contract testing
├── terraform/                  # Terraform provider specifics
│   ├── crud-mapping.md
│   ├── customization.md
│   ├── testing-guide.md
│   └── publishing.md
└── CLI_REFERENCE.md            # Canonical CLI command documentation
```

## Decision Tree: Where to Start

```
START
  │
  ├─ Do you have an OpenAPI/Swagger spec?
  │    │
  │    ├─ YES ──► Is the spec valid?
  │    │           │
  │    │           ├─ YES ──► What do you want to generate?
  │    │           │           │
  │    │           │           ├─ SDK ──► plans/sdk-generation.md
  │    │           │           └─ Terraform Provider ──► plans/tf-provider-generation.md
  │    │           │
  │    │           └─ NO/UNSURE ──► spec-first/validation.md
  │    │
  │    └─ NO ──► Do you have API code?
  │               │
  │               ├─ YES ──► What framework?
  │               │           ├─ FastAPI ──► code-first/fastapi.md
  │               │           ├─ Flask ──► code-first/flask.md
  │               │           ├─ Django ──► code-first/django.md
  │               │           ├─ Spring Boot ──► code-first/spring-boot.md
  │               │           ├─ NestJS ──► code-first/nestjs.md
  │               │           ├─ Hono ──► code-first/hono.md
  │               │           ├─ Rails ──► code-first/rails.md
  │               │           └─ Laravel ──► code-first/laravel.md
  │               │
  │               └─ NO ──► Cannot proceed without spec or code
```

## Troubleshooting Tree

```
PROBLEM
  │
  ├─ Getting ResponseValidationError at runtime?
  │    │
  │    └─ SDK types don't match server responses
  │         ├─ Run contract tests to identify all mismatches
  │         │    → sdk-testing/contract-testing.md
  │         └─ Fix spec or create overlay to correct types
  │              → spec-first/validation.md#dynamic-validation-contract-testing
  │
  ├─ SDK doesn't match live API behavior?
  │    │
  │    ├─ Spec may have drifted from API
  │    │    → Run contract tests to detect drift
  │    │       sdk-testing/contract-testing.md
  │    │
  │    └─ Third-party spec may be inaccurate
  │         → Validate with contract testing before trusting
  │            sdk-testing/contract-testing.md
  │
  ├─ Type mismatch errors in generated SDK?
  │    │
  │    ├─ At compile time ──► Check spec schema definitions
  │    │                       spec-first/validation.md
  │    │
  │    └─ At runtime ──► Server returns unexpected types
  │                      → Contract testing required
  │                         sdk-testing/contract-testing.md
  │
  └─ Enum value not recognized?
       │
       └─ API returned value not in spec enum
            ├─ Add missing value to spec/overlay
            │    → spec-first/overlays.md
            └─ Or use open enums for anti-fragility
                 → spec-first/overlays.md#overlay-recipes
```

## Working with Large OpenAPI Documents

OpenAPI specs can be thousands of lines. **Do not load the full spec into context.** Use `yq` (YAML) or `jq` (JSON) to extract only the sections you need.

```bash
# List all paths
yq '.paths | keys' spec.yaml

# Inspect a specific endpoint
yq '.paths["/users/{id}"]' spec.yaml

# List all schema names
yq '.components.schemas | keys' spec.yaml

# Inspect a specific schema
yq '.components.schemas.User' spec.yaml

# Check server URLs
yq '.servers' spec.yaml

# List all operationIds
yq '[.paths[][].operationId // empty] | unique' spec.yaml

# For JSON specs, use jq
jq '.paths | keys' spec.json
jq '.components.schemas.User' spec.json
```

> **Note:** If `yq`/`jq` aren't available, use targeted `grep` searches instead of copying the full spec into context:
> ```bash
> grep -n 'operationId:' spec.yaml
> grep -n 'x-speakeasy-entity' spec.yaml
> ```

## Common Workflows

### Workflow A: First-Time SDK Generation

1. Read `content/plans/sdk-generation.md`
2. Run `speakeasy quickstart --skip-interactive --output console -s spec.yaml -t python -o ./sdk`
3. SDK generated in output directory

### Workflow B: Existing Codebase → SDK

1. Identify framework in `content/code-first/`
2. Extract OpenAPI spec
3. Validate with `speakeasy lint openapi --non-interactive -s spec.yaml`
4. Fix issues using `content/spec-first/` guides
5. Generate SDK via `content/plans/sdk-generation.md`

### Workflow C: SDK Customization

1. Ensure `gen.yaml` exists (from quickstart)
2. Read `content/sdk-customization/` guides
3. Modify `gen.yaml`
4. Regenerate with `speakeasy run -y --output console`

### Workflow D: Multi-Target SDK (Azure, GCP, etc.)

1. Read `content/sdk-customization/multi-target-sdks.md`
2. Configure multiple sources in `workflow.yaml`
3. Set up target outputs to `packages/` subdirectories
4. Create CI workflows per target

### Workflow E: SDK Extensions (Hooks, Custom Methods)

1. For persistent changes anywhere → `content/sdk-customization/custom-code.md`
2. For cross-cutting concerns → `content/sdk-customization/hooks.md`
3. For predefined extension points → `content/sdk-languages/typescript.md#custom-code-regions`
4. For complex logic → `content/sdk-languages/typescript.md#extra-modules-pattern`

### Workflow F: Upgrade and Regenerate

1. Check current `speakeasyVersion` in `.speakeasy/workflow.yaml`
2. Update `speakeasyVersion` to `latest` or a specific version → `content/plans/sdk-generation.md#version-management`
3. Regenerate with `speakeasy run` → `content/plans/sdk-generation.md`
4. Test the regenerated SDK → `content/sdk-testing/integration-testing.md` or `content/sdk-testing/contract-testing.md`
5. Commit changes

## Essential CLI Commands

| Command | Purpose |
|---------|---------|
| `speakeasy quickstart --skip-interactive --output console -s spec.yaml -t python -o ./sdk` | Non-interactive SDK setup |
| `speakeasy run -y --output console` | Regenerate SDK from gen.yaml |
| `speakeasy lint openapi --non-interactive -s spec.yaml` | Validate OpenAPI spec |
| `speakeasy auth login` | Authenticate with Speakeasy |

## Getting Help

- **Authentication issues:** Run `speakeasy auth login`
- **Validation errors:** See `content/spec-first/validation.md`
- **Unsupported feature:** Check language guide in `content/sdk-languages/`
- **CLI errors:** See `content/CLI_REFERENCE.md` or run `speakeasy --help`

## Providing Feedback

If you encounter missing documentation, unclear instructions, or incorrect examples in this agent context, submit feedback directly:

```bash
# General feedback
speakeasy agent feedback -m "Description of the issue or suggestion"

# Feedback about a specific document
speakeasy agent feedback -m "Description of the issue" --context-path "path/to/document.md"
```

Feedback helps improve these documents for all agents. Submit feedback when:
- A guide is missing steps needed to complete a task
- An example does not work as documented
- A CLI command behaves differently than described
- You cannot find documentation for a supported feature

## Related Skills

- `start-new-sdk-project` - Quick interactive setup with `speakeasy quickstart`
- `regenerate-sdk` - Re-run generation after config changes
- `validate-openapi-spec` - Lint and validate OpenAPI specs
- `diagnose-generation-failure` - Troubleshoot failed generation runs
- `create-openapi-overlay` - Create overlays for spec customization
- `fix-validation-errors-with-overlays` - Fix lint errors with overlays
