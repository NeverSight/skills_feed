---
name: akash
description: >
  Comprehensive Akash Network skill for deployers, providers, and node operators.
  Covers SDL generation, CLI deployments, Console API, TypeScript/Go SDKs,
  provider setup, and validator operations. Use for "deploy to Akash",
  "generate SDL", "Akash provider", "Akash CLI", "Akash SDK", or "Akash validator".
license: MIT
metadata:
  author: baktun14
  version: "2.0.0"
  argument-hint: <task-description>
---

# Akash Network Skill

Comprehensive skill for working with the Akash Network - the decentralized cloud computing marketplace.

## Capabilities

This skill covers all aspects of the Akash Network:

| Area | Description |
|------|-------------|
| **SDL Generation** | Create valid Stack Definition Language configurations |
| **Deployments** | Deploy via CLI, Console API, or SDKs |
| **Provider Operations** | Set up and manage Akash providers |
| **Node Operations** | Run full nodes and validators |
| **SDK Integration** | TypeScript and Go SDK usage |

## Critical Rules

**NEVER use `:latest` or omit image tags.** Always specify explicit version tags for reproducible deployments.

```yaml
# CORRECT
image: nginx:1.25.3
image: node:20-alpine
image: postgres:16

# WRONG - will cause deployment issues
image: nginx:latest
image: nginx          # implies :latest
```

## Quick Reference

### SDL Structure

Every SDL file has four required sections:

```yaml
version: "2.0"  # or "2.1" for IP endpoints

services:       # Container definitions
profiles:       # Compute resources & placement
deployment:     # Service-to-profile mapping
```

Optional section for IP endpoints:
```yaml
endpoints:      # IP lease endpoints (requires version 2.1)
```

### Minimal SDL Template

```yaml
version: "2.0"

services:
  web:
    image: nginx:1.25.3
    expose:
      - port: 80
        as: 80
        to:
          - global: true

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    dcloud:
      pricing:
        web:
          denom: uakt
          amount: 1000

deployment:
  web:
    dcloud:
      profile: web
      count: 1
```

## Documentation Structure

### Core Concepts
- **@overview.md** - Akash Network introduction and architecture
- **@terminology.md** - Key terms (lease, bid, dseq, gseq, oseq)
- **@pricing.md** - Payment with uakt, USDC, IBC denoms

### SDL Configuration
- **@sdl/schema-overview.md** - Version requirements and SDL structure
- **@sdl/services.md** - Service configuration (image, expose, env, credentials)
- **@sdl/compute-resources.md** - CPU, memory, storage, and GPU specifications
- **@sdl/placement-pricing.md** - Provider selection and pricing (uakt/USDC)
- **@sdl/deployment.md** - Service-to-profile mapping
- **@sdl/endpoints.md** - IP endpoint configuration (v2.1)
- **@sdl/validation-rules.md** - All constraints and validation rules

### SDL Examples
- **@sdl/examples/web-app.md** - Simple web deployment
- **@sdl/examples/wordpress-db.md** - Multi-service with persistent storage
- **@sdl/examples/gpu-workload.md** - GPU deployment with NVIDIA
- **@sdl/examples/ip-lease.md** - IP endpoint configuration

### Deployment Methods
- **@deploy/overview.md** - Comparison of deployment options
- **@deploy/cli/** - Akash CLI installation and usage
- **@deploy/console-api/** - Console API for programmatic deployments
- **@deploy/certificates/** - Authentication methods (JWT, mTLS)

### SDK Documentation
- **@sdk/overview.md** - SDK comparison and selection
- **@sdk/typescript/** - TypeScript SDK for web and Node.js
- **@sdk/go/** - Go SDK for backend services

### AuthZ (Delegated Permissions)
- **@authz/** - Fee grants and deployment authorization

### Provider Operations
- **@provider/overview.md** - Provider requirements and setup
- **@provider/setup/** - Kubernetes and provider installation
- **@provider/configuration/** - Attributes, pricing, bid engine
- **@provider/operations/** - Monitoring and troubleshooting

### Node Operations
- **@node/overview.md** - Running Akash nodes
- **@node/full-node/** - Full node setup and state sync
- **@node/validator/** - Validator operations and security

### Reference
- **@reference/storage-classes.md** - beta2, beta3, ram storage
- **@reference/gpu-models.md** - Supported NVIDIA GPUs
- **@reference/ibc-denoms.md** - Payment denominations
- **@reference/rpc-endpoints.md** - Public RPC endpoints

## Common Patterns

### Environment Variables
```yaml
services:
  app:
    env:
      - "DATABASE_URL=postgres://..."
      - "NODE_ENV=production"
```

### Persistent Storage
```yaml
profiles:
  compute:
    app:
      resources:
        storage:
          - size: 10Gi
            attributes:
              persistent: true
              class: beta2
```

### GPU Workloads
```yaml
profiles:
  compute:
    ml:
      resources:
        gpu:
          units: 1
          attributes:
            vendor:
              nvidia:
                - model: a100
```

### Payment Options
- **uakt**: Native Akash Token (e.g., `amount: 1000`)
- **USDC**: Via IBC denom (e.g., `denom: ibc/170C677610AC31DF0904FFE09CD3B5C657492170E7E52372E48756B71E56F2F1`)

## Additional Resources

- **[awesome-akash](https://github.com/akash-network/awesome-akash)** - 100+ production-ready SDL templates
- **[Akash Network Docs](https://akash.network/docs/)** - Official documentation
- **[Console](https://console.akash.network)** - Web-based deployment interface
- **[Console API](https://console-api.akash.network/v1/swagger)** - REST API documentation
- **[chain-sdk](https://github.com/akash-network/chain-sdk)** - Official TypeScript SDK
