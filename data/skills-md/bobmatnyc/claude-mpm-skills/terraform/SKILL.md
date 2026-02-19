---
name: terraform
description: "Terraform infrastructure-as-code workflow patterns: state and environments, module design, safe plan/apply, drift control, and CI guardrails"
version: 1.0.0
category: universal
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Manage infrastructure safely with Terraform: remote state, reproducible plans, reviewable changes, and guardrails"
    when_to_use: "When provisioning cloud or platform resources, standardizing environments, or building safe IaC workflows"
    quick_start: "1. Pin versions 2. terraform init/fmt/validate 3. Plan in CI 4. Review + approve 5. Apply with locking"
  token_estimate:
    entry: 140
    full: 8000
context_limit: 900
tags:
  - terraform
  - iac
  - infrastructure
  - provisioning
  - ci
  - state
requires_tools:
  - terraform
---

# Terraform

## Quick Start (workflow)

```bash
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

## Safety Checklist

- State: remote backend + locking; separate state per environment
- Reviews: plan in CI; apply from a trusted runner with approvals
- Guardrails: `prevent_destroy` and policy checks for prod

## Load Next (References)

- `references/state-and-environments.md` — backends, locking, workspaces vs separate state, drift
- `references/modules-and-composition.md` — module interfaces, versioning, composition patterns
- `references/workflows-and-guardrails.md` — CI plan/apply, policy-as-code, safe migrations
