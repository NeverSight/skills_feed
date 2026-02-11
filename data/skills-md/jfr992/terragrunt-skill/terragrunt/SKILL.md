---
name: terragrunt
description: |
  Use this skill when working with Terragrunt infrastructure configurations. Triggers include:
  - Setting up a new Terragrunt infrastructure catalog from scratch
  - Creating or managing Terragrunt stacks (terragrunt.stack.hcl)
  - Creating units that wrap OpenTofu modules from separate repos
  - Configuring live infrastructure repositories with root.hcl hierarchy
  - Setting up remote state backends (S3 with DynamoDB locking)
  - Multi-account/multi-environment deployments with cross-account role assumption
---

# Terragrunt Infrastructure Skill

## Overview

This skill provides guidance for setting up and managing infrastructure using Terragrunt with OpenTofu, following a pattern with:

1. **Infrastructure Catalog** - Units and stacks that reference modules from separate repos
2. **Infrastructure Live** - Environment-specific deployments consuming the catalog
3. **Module Repos** - Separate repositories for each OpenTofu module

## Key Concepts

### Modules in Separate Repos (Recommended)

Consider maintaining modules in **separate Git repositories** rather than in the catalog. Units reference modules via Git URLs:

```hcl
terraform {
  source = "git::git@github.com:YOUR_ORG/modules/rds.git//app?ref=${values.version}"
}
```

This enables:
- Independent versioning per module
- Separate CI/CD pipelines
- Team ownership boundaries

### Values Pattern

Units receive configuration through `values.xxx`:

```hcl
inputs = {
  name        = values.name
  environment = values.environment
  # Optional with defaults
  instance_class = try(values.instance_class, "db.t3.medium")
}
```

### Reference Resolution

Units resolve symbolic references like `"../acm"` to dependency outputs:

```hcl
inputs = {
  acm_certificate_arn = try(values.acm_certificate_arn, "") == "../acm" ?
    dependency.acm.outputs.acm_certificate_arn :
    values.acm_certificate_arn
}
```

## Naming Conventions

### Repository Names

**Catalog Repositories:**
| Pattern | Example | Use Case |
|---------|---------|----------|
| `infrastructure-<org>-catalog` | `infrastructure-acme-catalog` | Single cloud or multi-cloud catalog |
| `infrastructure-<cloud>-<org>-catalog` | `infrastructure-aws-acme-catalog` | Cloud-specific catalogs |

**Live Repositories:**
| Pattern | Example | Use Case |
|---------|---------|----------|
| `infrastructure-<org>-live` | `infrastructure-acme-live` | Single live repo |
| `infrastructure-<cloud>-<org>-live` | `infrastructure-aws-acme-live` | Cloud-specific live repos |

**Module Repositories:**
| Pattern | Example |
|---------|---------|
| `terraform-<provider>-<name>` | `terraform-aws-rds`, `terraform-gcp-gke` |
| `modules-<org>-<name>` | `modules-acme-networking` |

### Directory and Resource Names

- **Units:** lowercase, hyphen-separated (`eks-config`, `argocd-registration`)
- **Stacks:** lowercase, hyphen-separated, descriptive (`serverless-api`, `eks-cluster`)
- **Environments:** lowercase (`staging`, `production`, `dev`)
- **Accounts:** lowercase with org prefix (`acme-prod`, `acme-nonprod`)

## Infrastructure Catalog Structure

```
infrastructure-catalog/
├── units/                      # Terragrunt units (building blocks)
│   ├── acm/
│   │   └── terragrunt.hcl
│   ├── cloudfront/
│   │   └── terragrunt.hcl
│   ├── dynamodb/
│   │   └── terragrunt.hcl
│   ├── eks/
│   │   └── terragrunt.hcl
│   ├── rds/
│   │   └── terragrunt.hcl
│   ├── route53/
│   │   └── terragrunt.hcl
│   └── s3/
│       └── terragrunt.hcl
└── stacks/                     # Template stacks (compositions)
    ├── frontend/
    │   └── terragrunt.stack.hcl
    ├── backend-api/
    │   └── terragrunt.stack.hcl
    └── data-platform/
        └── terragrunt.stack.hcl
```

Reference: [catalog-structure](assets/catalog-structure/)

## Infrastructure Live Structure

```
infrastructure-live/
├── root.hcl                    # Root configuration
├── setup-state-backend.sh      # State bucket setup script
├── <account>/                  # Account directories
│   ├── account.hcl             # Account config (id, name, role_arn, vpc, tags)
│   └── <region>/
│       ├── region.hcl          # Region config
│       └── <environment>/
│           ├── env.hcl         # Environment config (state_bucket_suffix)
│           └── <service>/
│               └── <resource>/
│                   └── terragrunt.stack.hcl
```

Reference: [live-structure](assets/live-structure/)

## Root Configuration (root.hcl)

```hcl
locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  env_vars     = try(read_terragrunt_config(find_in_parent_folders("env.hcl")), { locals = {} })

  account_name = local.account_vars.locals.account_name
  account_id   = local.account_vars.locals.aws_account_id
  aws_region   = local.region_vars.locals.aws_region
  role_arn     = local.account_vars.locals.role_arn
}

# Generate AWS provider with role assumption
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region              = "${local.aws_region}"
  allowed_account_ids = ["${local.account_id}"]
  assume_role {
    role_arn = "${local.role_arn}"
  }
  default_tags {
    tags = {
      Environment = "${try(local.env_vars.locals.environment, "default")}"
      ManagedBy   = "Terragrunt"
    }
  }
}
EOF
}

# Generate OpenTofu version constraints
generate "versions" {
  path      = "versions.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}
EOF
}

# Remote state with environment-based bucket suffix
remote_state {
  backend = "s3"
  config = {
    encrypt        = true
    bucket         = format("tfstate-%s%s-%s",
                      local.account_name,
                      try(local.env_vars.locals.state_bucket_suffix, "") != "" ? "-${local.env_vars.locals.state_bucket_suffix}" : "",
                      local.aws_region)
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = local.aws_region
    dynamodb_table = format("tfstate-locks-%s%s-%s",
                      local.account_name,
                      try(local.env_vars.locals.state_bucket_suffix, "") != "" ? "-${local.env_vars.locals.state_bucket_suffix}" : "",
                      local.aws_region)
    role_arn       = local.role_arn
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

catalog {
  urls = [
    "git@github.com:YOUR_ORG/infrastructure-catalog.git"
  ]
}

inputs = merge(
  local.account_vars.locals,
  local.region_vars.locals,
  local.env_vars.locals
)
```

Reference: [root.hcl](assets/live-structure/root.hcl)

## Account Configuration (account.hcl)

```hcl
locals {
  aws_account_id = "123456789012"
  account_name   = "myproject-prod"
  role_arn       = "arn:aws:iam::123456789012:role/TerraformRole"

  environment = "production"

  # Network configuration
  vpc_id             = "vpc-xxxxxxxxx"
  private_subnet_ids = ["subnet-xxx", "subnet-yyy"]
  public_subnet_ids  = ["subnet-aaa", "subnet-bbb"]

  tags = {
    Project     = "MyProject"
    Environment = "production"
  }
}
```

## Environment Configuration (env.hcl)

```hcl
locals {
  environment         = "staging"
  state_bucket_suffix = local.environment  # Creates separate state bucket per env
}
```

## Unit Pattern

Units wrap modules from separate repos:

```hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  # Module in separate repo - use Git URL with version from values
  source = "git::git@github.com:YOUR_ORG/modules/rds.git//app?ref=${values.version}"
}

dependency "vpc" {
  config_path  = try(values.vpc_path, "../vpc")
  skip_outputs = !try(values.use_vpc, true)

  mock_outputs = {
    vpc_id          = "vpc-mock"
    private_subnets = ["subnet-mock"]
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

inputs = {
  name        = values.name
  environment = values.environment
  vpc_id      = dependency.vpc.outputs.vpc_id

  # Auto-detect from config presence
  create_feature = try(values.create_feature, length(try(values.feature_config, {})) > 0)

  # Reference resolution
  some_arn = try(values.some_arn, "") == "../other_unit" ?
    dependency.other_unit.outputs.arn :
    values.some_arn
}
```

Reference: [unit-template](assets/catalog-structure/units/template/)

## Unit Interdependencies

Units within a stack can depend on each other, creating a DAG (Directed Acyclic Graph) of resources.

### Dependency Patterns

**Fan-Out Pattern (EKS Example):**
```
eks (core cluster)
├── eks-config (depends on eks)
├── karpenter (depends on eks)
└── argocd-registration (depends on eks)
```

**Chain Pattern (Frontend Example):**
```
s3 → cloudfront → route53
      ↑
     acm
```

**Multiple Dependencies (CloudFront Example):**
```
cloudfront
├── depends on acm (for SSL certificate)
└── depends on s3 (for origin bucket)
```

### How Dependencies Work

**1. Stack passes dependency paths via values:**

```hcl
# terragrunt.stack.hcl
unit "eks" {
  source = "${local.catalog_path}//units/eks?ref=main"
  path   = "eks"
  values = { ... }
}

unit "karpenter" {
  source = "${local.catalog_path}//units/eks-karpenter?ref=main"
  path   = "karpenter"
  values = {
    eks_path = "../eks"  # Relative path to eks unit
    version  = "v1.0.0"
  }
}

unit "argocd-registration" {
  source = "${local.catalog_path}//units/argocd-cluster-configuration?ref=main"
  path   = "argocd-registration"
  values = {
    eks_path = "../eks"  # Same dependency, different unit
    version  = "v1.0.0"
  }
}
```

**2. Catalog units resolve paths to dependencies:**

```hcl
# units/eks-karpenter/terragrunt.hcl
dependency "eks" {
  config_path = values.eks_path  # "../eks" from stack

  mock_outputs = {
    cluster_name = "mock-eks-cluster"
    eks_managed_node_groups = {
      mock = { iam_role_arn = "arn:aws:iam::123456789012:role/mock" }
    }
  }
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "destroy"]
}

inputs = {
  cluster_name = dependency.eks.outputs.cluster_name
  node_iam_role_arn = values(dependency.eks.outputs.eks_managed_node_groups)[0].iam_role_arn
}
```

### Conditional Dependencies

Enable/disable dependencies based on configuration:

```hcl
# units/cloudfront/terragrunt.hcl

# Only enable ACM dependency if using ACM certificate
dependency "acm" {
  enabled      = try(values.use_acm_certificate, false)
  config_path  = try(values.acm_path, "../acm")
  mock_outputs = {
    acm_certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/mock"
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

# Only enable S3 dependency if using S3 origin
dependency "s3" {
  enabled      = try(values.use_s3_origin, false)
  config_path  = try(values.s3_path, "../s3")
  mock_outputs = {
    s3_bucket_bucket_domain_name = "mock-bucket.s3.amazonaws.com"
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}
```

### Smart Skip Outputs

Skip dependency outputs based on whether they're actually needed:

```hcl
# units/route53/terragrunt.hcl
dependency "cloudfront" {
  config_path = try(values.cloudfront_path, "../cloudfront")

  # Only fetch outputs if records actually reference CloudFront
  skip_outputs = !try(
    anytrue([
      for record in try(values.records, []) :
        try(record.alias.name == "../cloudfront", false)
    ]),
    false
  )

  mock_outputs = {
    cloudfront_distribution_domain_name    = "d111111abcdef8.cloudfront.net"
    cloudfront_distribution_hosted_zone_id = "Z2FDTNDATAQYW2"
  }
}
```

### Reference Resolution in Inputs

Resolve symbolic references to actual dependency outputs:

```hcl
inputs = {
  # Replace "../cloudfront" with actual CloudFront domain
  origin = {
    for key, origin_config in values.origin :
    key => merge(
      origin_config,
      origin_config.domain_name == "../s3" ? {
        domain_name = dependency.s3.outputs.s3_bucket_bucket_domain_name
      } : {}
    )
  }

  # Replace "../acm" with actual certificate ARN
  viewer_certificate = merge(
    values.viewer_certificate,
    try(values.viewer_certificate.acm_certificate_arn, "") == "../acm" ? {
      acm_certificate_arn = dependency.acm.outputs.acm_certificate_arn
    } : {}
  )
}
```

### Provider Generation from Dependencies

Generate providers that authenticate using dependency outputs:

```hcl
# units/eks-config/terragrunt.hcl
generate "provider_kubectl" {
  path      = "cluster_auth.tf"
  if_exists = "overwrite"
  contents  = <<EOF
data "aws_eks_cluster_auth" "eks" {
  name = "${dependency.eks.outputs.cluster_name}"
}

provider "kubectl" {
  host                   = "${dependency.eks.outputs.cluster_endpoint}"
  cluster_ca_certificate = base64decode("${dependency.eks.outputs.cluster_certificate_authority_data}")
  token                  = data.aws_eks_cluster_auth.eks.token
  load_config_file       = false
}
EOF
}
```

### Applying Single Units with Dependencies

When applying a single unit that has dependencies, the dependencies must already exist:

```bash
# First apply the base unit
terragrunt stack run apply --filter '.terragrunt-stack/eks'

# Then apply dependent units (eks must be applied first)
terragrunt stack run apply --filter '.terragrunt-stack/karpenter'

# Or apply a unit and all its dependencies
terragrunt stack run apply --filter '.terragrunt-stack/karpenter...'
```

### Dependency Best Practices

1. **Always provide mock outputs** - Required for plan/validate without real dependencies
2. **Use `enabled` for optional dependencies** - Don't fetch outputs for unused features
3. **Use `skip_outputs` for conditional fetching** - Based on actual usage in inputs
4. **Allow path overrides** - `try(values.X_path, "../default")` for flexibility
5. **Document required outputs** - In mock_outputs, show what the dependency must provide

## Stack Pattern (terragrunt.stack.hcl)

### Template Stacks (in catalog)

```hcl
locals {
  service     = values.service
  environment = values.environment
  domain      = values.domain

  fqdn = "${values.service}-${values.environment}.${values.domain}"

  common_tags = merge(try(values.tags, {}), {
    Stack       = "frontend"
    Service     = values.service
    Environment = values.environment
  })
}

unit "s3" {
  source = "git::git@github.com:YOUR_ORG/infrastructure-catalog.git//units/s3?ref=${values.catalog_version}"
  path   = "s3"

  values = {
    version = values.module_version
    bucket  = "my-bucket-${values.environment}"
    tags    = local.common_tags
  }
}

unit "cloudfront" {
  source = "git::git@github.com:YOUR_ORG/infrastructure-catalog.git//units/cloudfront?ref=${values.catalog_version}"
  path   = "cloudfront"

  values = {
    version  = values.module_version
    acm_path = "../acm"  # Reference to ACM unit
  }
}
```

### Deployment Stacks (in live repo)

```hcl
locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  env_vars     = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  environment  = local.env_vars.locals.environment
  service      = "my-service"
}

unit "database" {
  source = "git::git@github.com:YOUR_ORG/infrastructure-catalog.git//units/dynamodb?ref=main"
  path   = "database"

  values = {
    version    = "v1.0.0"
    name       = "${local.service}-${local.environment}"
    hash_key   = "PK"
    range_key  = "SK"
    attributes = [
      { name = "PK", type = "S" },
      { name = "SK", type = "S" }
    ]
    tags = merge(local.account_vars.locals.tags, {
      Service = local.service
    })
  }
}
```

Reference: [stack-template](assets/catalog-structure/stacks/template/)

## State Backend Setup (AWS)

> **Note:** This script currently only supports AWS (S3 + DynamoDB). GCP and Azure are not yet supported.

The `setup-state-backend.sh` script auto-discovers accounts, regions, and environments from your directory structure and creates S3 buckets and DynamoDB lock tables.

### Required Directory Structure

```
infrastructure-live/
├── setup-state-backend.sh        # Run from here
├── root.hcl
├── <account>/                    # Directory name (e.g., "non-prod", "prod")
│   ├── account.hcl               # REQUIRED
│   └── <region>/                 # AWS region (e.g., "us-east-1")
│       ├── region.hcl
│       ├── env.hcl               # Optional: region-level state bucket
│       └── <environment>/        # Environment (e.g., "staging", "dev")
│           ├── env.hcl           # Optional: env-level state bucket
│           └── <service>/
│               └── terragrunt.stack.hcl
```

### Required HCL Variables

**account.hcl** (required):
```hcl
locals {
  account_name   = "myproject-nonprod"  # Used in bucket name
  aws_account_id = "123456789012"       # For bucket policy
}
```

**env.hcl** (optional - for environment isolation):
```hcl
locals {
  environment         = "staging"
  state_bucket_suffix = local.environment  # Creates separate bucket
}
```

### Bucket Naming Convention

| With suffix | Without suffix |
|-------------|----------------|
| `tfstate-{account_name}-{suffix}-{region}` | `tfstate-{account_name}-{region}` |
| `tfstate-myproject-nonprod-staging-us-east-1` | `tfstate-myproject-nonprod-us-east-1` |

### Usage

```bash
# Create all state backends
./setup-state-backend.sh

# Dry run - see what would be created
./setup-state-backend.sh --dry-run

# Specific account only
./setup-state-backend.sh --account prod
```

### What It Creates

For each discovered account/region/environment:
- **S3 Bucket** with versioning, KMS encryption, public access blocked, TLS-enforced policy
- **DynamoDB Table** with `LockID` key for state locking

### Prerequisites

- AWS CLI configured with credentials that can create S3 buckets and DynamoDB tables
- Must be run from the live repo root directory

Reference: [setup-state-backend.sh](scripts/setup-state-backend.sh)

## Catalog Scaffolding

The `terragrunt catalog` command provides an interactive way to browse available units and stacks from your catalog and scaffold new deployments.

### Browsing the Catalog

Run from your live repository (where `root.hcl` with a `catalog` block exists):

```bash
# Launch interactive catalog browser
terragrunt catalog
```

This displays all available units and stacks from the configured catalog:

![Terragrunt Catalog Browser](assets/images/terragrunt-catalog.png)

### Using Boilerplate for Scaffolding

When you select a unit or stack from the catalog, Terragrunt uses [Boilerplate](https://github.com/gruntwork-io/boilerplate) to scaffold the configuration. Units and stacks can include a `boilerplate.yml` to prompt for required values:

```yaml
# units/rds/boilerplate.yml
variables:
  - name: name
    description: "Name of the RDS instance"
    type: string

  - name: environment
    description: "Environment (dev, staging, prod)"
    type: string
    default: "dev"

  - name: instance_class
    description: "RDS instance class"
    type: string
    default: "db.t3.medium"

  - name: version
    description: "Module version to use"
    type: string
    default: "v1.0.0"
```

### Scaffold a New Deployment

```bash
# Navigate to target directory
cd non-prod/us-east-1/staging/my-service

# Browse and scaffold from catalog
terragrunt catalog

# Or scaffold directly by URL
terragrunt scaffold git@github.com:YOUR_ORG/infrastructure-catalog.git//units/rds
```

### Catalog Configuration in root.hcl

```hcl
catalog {
  urls = [
    "git@github.com:YOUR_ORG/infrastructure-catalog.git",
    "git@github.com:YOUR_ORG/infrastructure-aws-catalog.git"  # Multiple catalogs supported
  ]
}
```

## Stack Commands

### Basic Operations

```bash
# Generate stack units (creates .terragrunt-stack/ directory)
terragrunt stack generate

# Plan all units
terragrunt stack run plan

# Apply all units
terragrunt stack run apply

# Destroy all units
terragrunt stack run destroy

# Get outputs from all units
terragrunt stack output

# Clean generated files
terragrunt stack clean
```

### Targeting Specific Units

Apply only a single unit from a stack using `--queue-include-dir` or the modern `--filter` syntax:

```bash
# Target a specific unit (legacy syntax)
terragrunt stack run apply --queue-include-dir ".terragrunt-stack/argocd-registration"

# Target a specific unit (modern filter syntax - equivalent)
terragrunt stack run apply --filter '.terragrunt-stack/argocd-registration'

# Target multiple specific units
terragrunt stack run plan --filter '.terragrunt-stack/rds' --filter '.terragrunt-stack/secrets'

# Target by pattern (all units starting with "db-")
terragrunt stack run plan --filter '.terragrunt-stack/db-*'

# Exclude specific units
terragrunt stack run apply --filter '!.terragrunt-stack/expensive-resource'
```

### Filter Expressions

| Legacy Flag | Modern Filter | Description |
|-------------|---------------|-------------|
| `--queue-include-dir=./path` | `--filter='./path'` | Include only this path |
| `--queue-exclude-dir=./path` | `--filter='!./path'` | Exclude this path |
| `--queue-include-external` | `--filter='{./**}...'` | Include external dependencies |

### Advanced Filtering

```bash
# Target unit and its dependencies
terragrunt stack run apply --filter '.terragrunt-stack/api...'

# Target unit and its dependents (reverse)
terragrunt stack run apply --filter '.../.terragrunt-stack/vpc'

# Combine filters (intersection)
terragrunt stack run plan --filter '.terragrunt-stack/** | type=unit'

# Git-based: only changed units since main
terragrunt stack run plan --filter '[main...HEAD]'

# Use filters file
terragrunt stack run apply --filters-file my-filters.txt
```

### Parallelism Control

```bash
# Limit concurrent unit execution
terragrunt stack run apply --parallelism 3

# Save plans to directory structure
terragrunt stack run plan --out-dir ./plans
```

### Visualize Dependencies

```bash
# Generate DAG in DOT format
terragrunt dag graph

# List with dependencies
terragrunt list --format=dot --dependencies
```

## Common Operations

### Create New Unit

1. Create `units/<name>/terragrunt.hcl`
2. Reference module via Git URL with `${values.version}`
3. Use `values.xxx` for inputs
4. Add dependencies with mock outputs
5. Implement reference resolution for `"../unit"` patterns

### Create New Stack

1. Create `stacks/<name>/terragrunt.stack.hcl`
2. Define `locals` for computed values
3. Add `unit` blocks referencing catalog units
4. Pass values including version and dependency paths

### Deploy to New Environment

1. Create environment directory structure
2. Add `env.hcl` with `state_bucket_suffix`
3. Run `./setup-state-backend.sh` to create state resources
4. Add stack files referencing catalog

## Best Practices

1. **Pin module versions** - Use Git tags in `values.version`
2. **Pin catalog versions** - Use refs in unit source URLs
3. **Use reference resolution** - `"../unit"` → dependency outputs
4. **Provide mock outputs** - Enable plan/validate without dependencies
5. **Auto-detect features** - `length(keys(try(values.X, {}))) > 0`
6. **Override paths** - `try(values.X_path, "../default")`
7. **Separate state per environment** - Use `state_bucket_suffix`

## Common Pitfalls

1. **Git refspec error** - Use `//path?ref=branch` NOT `?ref=branch//path`
2. **Heredoc in ternary** - Wrap in parentheses: `condition ? (\n<<-EOF\n...\nEOF\n) : ""`
3. **Missing mock outputs** - Always provide for plan/validate
4. **Hardcoded paths** - Use local paths only for testing

## Version Management

- **Development:** Branch refs (`ref=feature-branch`)
- **Testing:** RC tags (`ref=v1.0.0-rc1`)
- **Production:** Stable tags (`ref=v1.0.0`)

## Performance Optimization

### Quick Wins

Enable provider caching for batch operations:

```bash
terragrunt run --all plan --provider-cache
```

### Environment Variables

```bash
export TG_PROVIDER_CACHE=1
export TG_PROVIDER_CACHE_DIR=/path/to/cached/providers
export TG_DOWNLOAD_DIR=/path/to/cached/modules
```

### Expected Speedups

| Scenario | Speedup |
|----------|---------|
| Cold cache | 1.73x (42% faster) |
| Warm cache | 2.07x (51% faster) |

### Experimental: Direct State Fetching

For S3 backends, bypass `tofu output -json`:

```bash
terragrunt run --all plan --experiment=dependency-fetch-output-from-state
```

Reference: [Performance Optimization Guide](references/performance.md)

## CI/CD Pipelines

### GitLab CI

```yaml
# Base templates with OIDC auth
.gcp-oidc-auth:
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://iam.googleapis.com/projects/${GC_PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WORKLOAD_IDENTITY_POOL}/providers/${WORKLOAD_IDENTITY_PROVIDER}
  before_script:
    - |
      echo $GITLAB_OIDC_TOKEN > $CI_BUILDS_DIR/.workload_identity.jwt
      cat << EOF > $GOOGLE_APPLICATION_CREDENTIALS
      {
        "type": "external_account",
        "audience": "//iam.googleapis.com/projects/$GC_PROJECT_NUMBER/locations/global/workloadIdentityPools/$WORKLOAD_IDENTITY_POOL/providers/$WORKLOAD_IDENTITY_PROVIDER",
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "token_url": "https://sts.googleapis.com/v1/token",
        "credential_source": { "file": "$CI_BUILDS_DIR/.workload_identity.jwt" },
        "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/$SERVICE_ACCOUNT:generateAccessToken"
      }
      EOF

my-service:plan:
  extends: [.terragrunt_plan_template, .gcp-oidc-auth]
  variables:
    TG_PATH: "gcp-dev/us-east4/api"
```

### GitHub Actions

```yaml
- name: Authenticate to GCP
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: 'projects/123456789012/locations/global/workloadIdentityPools/github-pool/providers/github-provider'
    service_account: 'sa-tf-admin@my-project.iam.gserviceaccount.com'

- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::111111111111:role/TerraformCrossAccount
    aws-region: us-east-1
```

Reference: [CI/CD Pipeline Examples](references/cicd-pipelines.md)

## References

- [Terragrunt Patterns Guide](references/patterns.md)
- [State Management Best Practices](references/state-management.md)
- [Multi-Account Strategy](references/multi-account.md)
- [Performance Optimization Guide](references/performance.md)
- [CI/CD Pipeline Examples](references/cicd-pipelines.md) (GitLab CI & GitHub Actions for AWS/GCP)
