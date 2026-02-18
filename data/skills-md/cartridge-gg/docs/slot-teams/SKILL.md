---
name: slot-teams
description: Manage Slot teams, billing, credits, and collaborators.
---

# Slot Teams

Teams are the billing entity in Slot.
They own credits used to pay for deployments, paymasters, RPC requests, and other services.

## Credit System

- Prepaid credits, deducted automatically
- 1 CREDIT = $0.01 USD
- Daily billing cycle (minimum 1-day charge)
- Fund via credit card or cryptocurrency

## Creating a Team

```sh
slot teams <team-name> create --email <email> [--address "address"] [--tax-id "id"]
```

A team is also auto-created when you create a deployment with a new project name.

## Funding

```sh
slot auth fund
```

Opens a browser interface to select a team and add credits.
Direct URL: `https://x.cartridge.gg/slot/fund`

## Team Info

```sh
# View balance and details
slot teams <team-name> info

# View billing history
slot teams <team-name> invoices

# Update billing info
slot teams <team-name> update [--email <email>] [--address "address"] [--tax-id "id"]
```

## Collaborators

```sh
# List members
slot teams <team-name> list

# Add a member (by controller username)
slot teams <team-name> add <username>

# Remove a member
slot teams <team-name> remove <username>
```

## What Uses Credits

| Service              | Cost                                          |
|----------------------|-----------------------------------------------|
| Basic deployment     | $10/month (first 3 free)                      |
| Pro deployment       | $50/month                                     |
| Epic deployment      | $100/month                                    |
| Legendary deployment | $200/month                                    |
| Storage (premium)    | $0.20/GB/month                                |
| Paymaster budget     | Funded from team credits                      |
| RPC requests         | Free 1M/month, then $5/1M                    |
| Multi-region         | Tier cost × regions × replicas                |
| Observability        | $10/month per deployment                      |

## Troubleshooting

### Insufficient credits

```sh
# Check balance
slot teams <team-name> info

# Fund the team
slot auth fund

# Retry your operation
```

### Service not starting

- Verify team has credits: `slot teams <team-name> info`
- Ensure service was created with `--team <team-name>`
- Check that you're a member of the team
