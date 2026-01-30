---
name: terraform
description: >-
  Guide for writing production-quality Terraform and Terragrunt infrastructure code following
  HashiCorp and community best practices. Triggers on "terraform", "terragrunt", "tf", "hcl",
  "infrastructure as code", "iac", "aws terraform", "gcp terraform", "azure terraform",
  "terraform module", "terraform state", "terraform plan", "terraform apply", "terraform init",
  "terraform workspace", "terraform backend", "terraform provider", "terraform resource",
  "terraform data", "terraform variable", "terraform output", "terraform locals",
  "terraform for_each", "terraform count", "terraform dynamic", "tfvars", "terraform validate",
  "terraform fmt", "tflint", "terraform import", "terraform destroy", "remote state",
  "state locking", "terraform cloud", "opentofu".
  PROACTIVE: MUST invoke when writing ANY .tf or .hcl file.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: Terraform and Terragrunt skill for production-quality infrastructure code
# ABOUTME: Enforces HashiCorp best practices, DRY patterns, and security-first design

# Terraform & Terragrunt Skill

## Quick Reference

| Principle | Rule |
|-----------|------|
| DRY | Use modules and Terragrunt to eliminate repetition |
| Immutability | Prefer replacement over modification |
| Security | No secrets in state; use data sources for sensitive values |
| Naming | `<provider>_<resource>_<purpose>` format |
| State | Remote backend always; never local for shared infra |
| Modules | Input validation, sensible defaults, documented outputs |

## 🛑 FILE OPERATION CHECKPOINT (BLOCKING)

**Before EVERY `Write` or `Edit` tool call on a `.tf` or `.hcl` file:**

```
╔══════════════════════════════════════════════════════════════════╗
║  🛑 STOP - TERRAFORM SKILL CHECK                                 ║
║                                                                  ║
║  You are about to modify a Terraform/Terragrunt file.            ║
║                                                                  ║
║  QUESTION: Is /terraform skill currently active?                 ║
║                                                                  ║
║  If YES → Proceed with the edit                                  ║
║  If NO  → STOP! Invoke /terraform FIRST, then edit               ║
║                                                                  ║
║  This check applies to:                                          ║
║  ✗ Write tool with file_path ending in .tf                       ║
║  ✗ Edit tool with file_path ending in .tf                        ║
║  ✗ Write/Edit with file_path ending in .hcl                      ║
║  ✗ Files named terragrunt.hcl                                    ║
║  ✗ ANY Terraform file, regardless of conversation topic          ║
║                                                                  ║
║  Examples that REQUIRE this skill:                               ║
║  - "add a new resource" (edits main.tf)                          ║
║  - "update the variables" (edits variables.tf)                   ║
║  - "configure the backend" (edits terragrunt.hcl)                ║
╚══════════════════════════════════════════════════════════════════╝
```

**Why this matters:** Terraform code with hardcoded secrets or missing validations
creates security risks. The skill ensures remote state and proper variable handling.

## 🔄 RESUMED SESSION CHECKPOINT

**When a session is resumed from context compaction, verify Terraform development state:**

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION RESUMED - TERRAFORM SKILL VERIFICATION             │
│                                                             │
│  Before continuing Terraform implementation:                │
│                                                             │
│  1. Was I in the middle of writing Terraform/Terragrunt?    │
│     → Check summary for ".tf", "module", "terragrunt"       │
│                                                             │
│  2. Did I follow all Terraform skill guidelines?            │
│     → No hardcoded secrets                                  │
│     → Remote state backend configured                       │
│     → Variables have descriptions and validations           │
│     → ABOUTME headers on new files                          │
│                                                             │
│  3. Check code quality before continuing:                   │
│     → Run: terraform fmt -check -recursive                  │
│     → Run: terraform validate                               │
│     → Run: tflint (if available)                            │
│                                                             │
│  If implementation was in progress:                         │
│  → Review the partial code for completeness                 │
│  → Ensure all resources have proper naming                  │
│  → Verify no sensitive data in outputs                      │
│  → Re-invoke /terraform if skill context was lost           │
└─────────────────────────────────────────────────────────────┘
```

## When to Use Terraform

**Use Terraform for:**
- Cloud infrastructure provisioning (AWS, GCP, Azure, etc.)
- Multi-cloud and hybrid deployments
- Infrastructure that requires versioning and audit trails
- Reproducible environments (dev, staging, prod)
- Kubernetes cluster provisioning (not workloads)

**Use Terragrunt for:**
- Managing multiple environments with DRY configurations
- Orchestrating module dependencies
- Managing remote state configuration
- Running Terraform across multiple modules

**Do NOT use Terraform for:**
- Application deployment (use Kubernetes, Docker, or CI/CD)
- Configuration management (use Ansible, Chef, Puppet)
- Secret management storage (use Vault, AWS Secrets Manager)

## Project Structure

### Standard Module Structure

```
module/
├── main.tf           # Primary resources
├── variables.tf      # Input variable declarations
├── outputs.tf        # Output value declarations
├── versions.tf       # Provider and terraform version constraints
├── locals.tf         # Local values (optional)
├── data.tf           # Data sources (optional)
└── README.md         # Module documentation
```

### Terragrunt Project Structure

```
infrastructure/
├── terragrunt.hcl              # Root configuration
├── modules/                    # Reusable modules
│   ├── vpc/
│   ├── eks/
│   └── rds/
├── environments/
│   ├── common.hcl              # Shared variables
│   ├── dev/
│   │   ├── terragrunt.hcl      # Environment config
│   │   ├── vpc/
│   │   │   └── terragrunt.hcl
│   │   └── eks/
│   │       └── terragrunt.hcl
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
└── README.md
```

## Core Patterns

### Provider Configuration

```hcl
# versions.tf
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
      Project     = var.project_name
    }
  }
}
```

### Variable Definitions with Validation

```hcl
# variables.tf
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "instance_type" {
  description = "EC2 instance type for the application servers"
  type        = string
  default     = "t3.medium"

  validation {
    condition     = can(regex("^t3\\.", var.instance_type))
    error_message = "Instance type must be from the t3 family."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid CIDR block."
  }
}
```

### Resource Naming Convention

```hcl
# Use locals for consistent naming
locals {
  name_prefix = "${var.project_name}-${var.environment}"

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-vpc"
  })
}
```

### Output Definitions

```hcl
# outputs.tf
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

# NEVER expose sensitive values without marking them
output "database_password" {
  description = "Database master password"
  value       = random_password.db.result
  sensitive   = true
}
```

## Terragrunt Patterns

### Root Configuration

```hcl
# terragrunt.hcl (root)
locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  env_vars     = read_terragrunt_config(find_in_parent_folders("env.hcl"))

  account_id = local.account_vars.locals.account_id
  aws_region = local.region_vars.locals.aws_region
  environment = local.env_vars.locals.environment
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"

  default_tags {
    tags = {
      Environment = "${local.environment}"
      ManagedBy   = "terragrunt"
    }
  }
}
EOF
}

remote_state {
  backend = "s3"
  config = {
    encrypt        = true
    bucket         = "terraform-state-${local.account_id}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = local.aws_region
    dynamodb_table = "terraform-locks"
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

inputs = {
  aws_region  = local.aws_region
  environment = local.environment
}
```

### Module Configuration

```hcl
# environments/prod/vpc/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../modules/vpc"
}

inputs = {
  vpc_cidr            = "10.0.0.0/16"
  availability_zones  = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnet_cidrs  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}
```

### Dependency Management

```hcl
# environments/prod/eks/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../modules/eks"
}

dependency "vpc" {
  config_path = "../vpc"

  mock_outputs = {
    vpc_id             = "vpc-00000000000000000"
    private_subnet_ids = ["subnet-00000000", "subnet-11111111"]
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

inputs = {
  vpc_id             = dependency.vpc.outputs.vpc_id
  private_subnet_ids = dependency.vpc.outputs.private_subnet_ids
  cluster_version    = "1.29"
}
```

## Security Best Practices

### State Security

```hcl
# Always use encrypted remote state
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    # Use server-side encryption with KMS
    kms_key_id     = "arn:aws:kms:us-east-1:ACCOUNT_ID:key/KEY_ID"
  }
}
```

### Secrets Management

```hcl
# BAD: Hardcoded secrets
resource "aws_db_instance" "bad" {
  password = "hardcoded-password-123"  # NEVER DO THIS
}

# GOOD: Use data sources or variables marked sensitive
variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

# BETTER: Generate and store in Secrets Manager
resource "random_password" "db" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name = "${local.name_prefix}-db-password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}

resource "aws_db_instance" "good" {
  password = random_password.db.result
}
```

### IAM Least Privilege

```hcl
# Use policy documents with specific permissions
data "aws_iam_policy_document" "lambda_exec" {
  statement {
    sid    = "AllowS3Read"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      aws_s3_bucket.data.arn,
      "${aws_s3_bucket.data.arn}/*",
    ]
  }

  # Avoid wildcards when possible
  # BAD:  actions = ["s3:*"]
  # BAD:  resources = ["*"]
}
```

## Resource Patterns

### Conditional Resources

```hcl
# Create resource only in certain environments
resource "aws_cloudwatch_log_group" "debug" {
  count = var.environment == "dev" ? 1 : 0

  name              = "/app/${local.name_prefix}/debug"
  retention_in_days = 7
}

# Using for_each for more complex conditions
resource "aws_route53_record" "alias" {
  for_each = var.create_dns_records ? toset(var.dns_names) : []

  zone_id = data.aws_route53_zone.main.zone_id
  name    = each.value
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}
```

### Dynamic Blocks

```hcl
resource "aws_security_group" "main" {
  name        = "${local.name_prefix}-sg"
  description = "Security group for application"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      description     = ingress.value.description
      from_port       = ingress.value.port
      to_port         = ingress.value.port
      protocol        = "tcp"
      cidr_blocks     = ingress.value.cidr_blocks
      security_groups = ingress.value.security_groups
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}
```

### Moved Blocks (Refactoring)

```hcl
# When refactoring, use moved blocks instead of state manipulation
moved {
  from = aws_instance.web
  to   = aws_instance.application
}

moved {
  from = module.vpc.aws_subnet.private
  to   = module.networking.aws_subnet.private
}
```

## Testing

### Terraform Validate

```bash
# Always validate before planning
terraform init -backend=false
terraform validate
```

### TFLint Rules

```hcl
# .tflint.hcl
plugin "aws" {
  enabled = true
  version = "0.27.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}
```

### Terratest (Integration Testing)

```go
// test/vpc_test.go
package test

import (
    "testing"

    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVPCModule(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "vpc_cidr":    "10.0.0.0/16",
            "environment": "test",
        },
    })

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcID := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcID)
}
```

## Common Commands

| Command | Purpose |
|---------|---------|
| `terraform init` | Initialize working directory |
| `terraform fmt -recursive` | Format all .tf files |
| `terraform validate` | Validate configuration |
| `terraform plan -out=tfplan` | Create execution plan |
| `terraform apply tfplan` | Apply saved plan |
| `terraform state list` | List resources in state |
| `terragrunt run-all plan` | Plan all modules |
| `terragrunt run-all apply` | Apply all modules |

## Checklist

Before considering Terraform code complete, verify:

- [ ] `terraform fmt` produces no changes
- [ ] `terraform validate` passes
- [ ] All variables have descriptions
- [ ] Sensitive variables marked `sensitive = true`
- [ ] No hardcoded secrets in code
- [ ] Remote state backend configured with encryption
- [ ] Resource naming follows convention
- [ ] Outputs documented and sensitive ones marked
- [ ] Provider versions pinned
- [ ] Required Terraform version specified
- [ ] Tags applied to all resources
- [ ] Security groups follow least privilege
- [ ] IAM policies use specific permissions
- [ ] Module has README.md documentation
- [ ] **If using Terragrunt**: DRY configuration applied

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Hardcoded values | No reusability | Use variables with defaults |
| Missing state locking | Concurrent modifications | Use DynamoDB for S3 backend |
| Secrets in state | Security risk | Use Secrets Manager/Vault |
| Monolithic configs | Hard to maintain | Split into modules |
| No version pins | Breaking changes | Pin provider versions |
| Local state | No collaboration | Use remote backend |
| `terraform taint` | Deprecated | Use `-replace` flag |
| Manual state edits | Corruption risk | Use `terraform state` commands |

## Additional Resources

- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
- [HashiCorp Learn](https://learn.hashicorp.com/terraform)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
