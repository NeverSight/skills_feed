---
name: orchestrate-multi-target-sdks
description: >-
  Use when generating multiple SDK variants from one repository. Covers workflow.yaml
  multi-target configuration, per-target gen.yaml, monorepo structure, versioning strategies.
  Triggers on "multi-target SDK", "multiple SDK variants", "Azure SDK variant",
  "GCP SDK", "cloud-specific SDK", "SDK monorepo".
license: Apache-2.0
---

# Orchestrate Multi-Target SDKs

Generate multiple SDK variants (e.g., core, Azure, GCP) from different OpenAPI sources in a single repository.

## When to Use

- Generating cloud-specific SDK variants (Azure, GCP, AWS)
- Creating regional API variants (US, EU, APAC)
- Building partner-branded/white-label SDKs
- Managing multiple OpenAPI sources in one repo
- User says: "multi-target SDK", "Azure variant", "SDK monorepo"

## Quick Start

Configure multiple sources and targets in `workflow.yaml`:

```yaml
workflowVersion: 1.0.0
speakeasyVersion: latest

sources:
  main-source:
    inputs:
      - location: registry.speakeasyapi.dev/org/repo/main-openapi:main
  azure-source:
    inputs:
      - location: registry.speakeasyapi.dev/org/repo/azure-openapi:main

targets:
  main-sdk:
    target: typescript
    source: main-source
    output: ./
  azure-sdk:
    target: typescript
    source: azure-source
    output: ./packages/azure
```

## Repository Structure

```
my-multi-sdk/
├── .speakeasy/
│   ├── workflow.yaml       # Multi-target config
│   └── gen.yaml            # Main SDK config
├── src/                    # Main SDK source
├── packages/
│   ├── azure/
│   │   ├── .speakeasy/
│   │   │   └── gen.yaml    # Azure-specific config
│   │   └── src/
│   └── gcp/
│       ├── .speakeasy/
│       │   └── gen.yaml    # GCP-specific config
│       └── src/
├── .github/workflows/
│   ├── sdk_generation_main.yaml
│   ├── sdk_generation_azure.yaml
│   └── sdk_generation_gcp.yaml
└── package.json
```

## Per-Target gen.yaml

Each variant has its own configuration:

```yaml
# packages/azure/.speakeasy/gen.yaml
configVersion: 2.0.0
generation:
  sdkClassName: MySDKAzure
typescript:
  version: 1.0.0
  packageName: '@myorg/mysdk-azure'
  envVarPrefix: MYSDK_AZURE
```

## Naming Conventions

| Variant | Package Name | Class Name |
|---------|--------------|------------|
| Main | `@myorg/mysdk` | `MySDK` |
| Azure | `@myorg/mysdk-azure` | `MySDKAzure` |
| GCP | `@myorg/mysdk-gcp` | `MySDKGCP` |

## CI Workflow Per Target

Create separate workflows for independent regeneration:

```yaml
# .github/workflows/sdk_generation_azure.yaml
name: Generate Azure SDK
on:
  workflow_dispatch:
    inputs:
      force:
        type: boolean
        default: false

jobs:
  generate:
    uses: speakeasy-api/sdk-generation-action/.github/workflows/workflow-executor.yaml@v15
    with:
      target: azure-sdk
      mode: pr
    secrets:
      github_access_token: ${{ secrets.GITHUB_TOKEN }}
      speakeasy_api_key: ${{ secrets.SPEAKEASY_API_KEY }}
```

## Versioning Strategies

**Lockstep**: All variants share the same version (simpler).

**Independent**: Each variant has its own version (more flexible).

```yaml
# Independent versioning
# Main: version: 2.1.0
# Azure: version: 1.8.0
# GCP: version: 1.3.0
```

## Sharing Code Across Variants

**Option 1**: Duplicate hooks in each variant (simpler)

**Option 2**: Create shared package:
```
shared/
├── package.json          # @myorg/mysdk-shared
└── src/
    └── hooks.ts
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong target generated | Specify `-t target-name` in `speakeasy run` |
| Config not found | Ensure `.speakeasy/gen.yaml` exists in output dir |
| Circular dependencies | Use workspace protocols in package.json |

## Related Skills

- `start-new-sdk-project` - Initial SDK setup
- `configure-sdk-options` - Language-specific configuration
- `manage-openapi-overlays` - Per-source overlays
- `orchestrate-multi-repo-sdks` - Single repo per language
