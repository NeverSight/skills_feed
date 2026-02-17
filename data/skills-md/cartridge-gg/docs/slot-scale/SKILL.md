---
name: slot-scale
description: Scale Slot deployments with paid tiers, replicas, and multi-region support.
---

# Slot Scale

Scale deployments from development to production with paid tiers, replicas, and multi-region.

## Instance Tiers

| Tier      | Specs                | Storage | Cost       |
|-----------|----------------------|---------|------------|
| Basic     | Limited CPU & memory | 1GB     | $10/month  |
| Pro       | 2 vCPU, 4GB RAM      | auto    | $50/month  |
| Epic      | 4 vCPU, 8GB RAM      | auto    | $100/month |
| Legendary | 8 vCPU, 16GB RAM     | auto    | $200/month |

First 3 Basic tier deployments are free.
Storage on premium tiers: $0.20/GB/month (auto-scaling).

### Basic tier behavior

- Scaled down automatically after a few hours of inactivity
- Revived on first request
- Deleted if unused for 30+ days

### Premium tiers (Pro+)

- Never scaled down or deleted while the team has credits
- Auto storage scaling (never runs out of disk space)

## Replicas

Torii supports multiple replicas on premium tiers:

```sh
slot d create --tier epic my-project torii --replicas 3
```

Billed per replica (3 replicas = 3× tier cost).
Katana does not support replicas.

## Regions

| Region        |
|---------------|
| `us-east`     |
| `europe-west` |

Deploy in multiple regions with `--regions`:

```sh
# Torii: multi-region with replicas
slot d create --tier pro my-project torii --regions us-east,europe-west

# Katana: single region only
slot d create --tier pro my-project katana --regions europe-west
```

Billing: tier cost × regions × replicas.

## Creating Paid Tier Deployments

Ensure the team has credits (see `slot-teams` skill), then:

```sh
slot d create --tier epic --team my-team my-instance torii
```

## Upgrading an Existing Deployment

Tiers can only be upgraded, not downgraded:

```sh
slot d update --tier epic my-instance torii
```

The team that owns the deployment must have sufficient credits.
