---
name: terraform-best-practices
version: 1.0.0
description: Comprehensive best practices for Terraform infrastructure as code from Anton Babenko's community guide
author: Anton Babenko (terraform-best-practices.com)
last_updated: 2026-01-29
skill_level: intermediate
prerequisites:
  - Basic Terraform knowledge (resources, variables, outputs)
  - Understanding of IaC concepts
  - Familiarity with cloud providers (AWS/Azure/GCP)
when-to-use:
  - Designing Terraform project structure
  - Implementing infrastructure as code patterns
  - Scaling Terraform from small to large infrastructures
  - Choosing between Terraform and Terragrunt workflows
  - Establishing naming conventions and code styling
  - Managing Terraform state and modules
---

# Terraform Best Practices Skill

Comprehensive community best practices for Terraform infrastructure as code, based on Anton Babenko's widely-adopted guide at terraform-best-practices.com.

## When to Use This Skill

Activate this skill when:
- **Designing project structure** - Choosing how to organize Terraform code for small, medium, or large infrastructure
- **Implementing IaC patterns** - Following community best practices for modules, compositions, and state management
- **Scaling infrastructure** - Growing from simple setups to complex multi-environment deployments
- **Evaluating tools** - Deciding between vanilla Terraform vs Terragrunt orchestration
- **Establishing standards** - Creating team conventions for naming, styling, and code organization
- **Troubleshooting common issues** - Resolving frequent Terraform problems (dependency hell, state management, etc.)

## Key Concepts

### Infrastructure Sizes & Patterns

**Small Infrastructure** (< 20 resources)
- Single Terraform directory
- Minimal module structure
- Direct resource definitions
- Simple state management

**Medium Infrastructure** (20-100 resources)
- Multiple environment directories
- Reusable modules
- Remote state backend
- Workspaces or directory-based environments

**Large Infrastructure** (100+ resources)
- Module composition approach
- Terragrunt for orchestration
- Hierarchical state structure
- Infrastructure vs resource modules

### Module Types

**Resource Modules**
- Create individual AWS/Azure/GCP resources
- Highly reusable across projects
- Published to registries
- Examples: `terraform-aws-modules/vpc/aws`

**Infrastructure Modules**
- Combine resource modules
- Environment-specific configurations
- Less portable, more opinionated
- Example: Company VPC + security groups + bastion

**Compositions**
- Top-level infrastructure assembly
- Orchestrate multiple modules
- Environment-specific values
- No reusable logic, only wiring

### Code Structure Patterns

```
# Small Infrastructure
terraform/
  main.tf
  variables.tf
  outputs.tf
  terraform.tfvars

# Medium Infrastructure
terraform/
  modules/
    vpc/
    compute/
  environments/
    dev/
    prod/

# Large Infrastructure (Terragrunt)
infrastructure/
  _global/
  dev/
    vpc/
      terragrunt.hcl
    compute/
      terragrunt.hcl
  prod/
    vpc/
    compute/
```

## Naming Conventions

### Resource Naming
```hcl
# Pattern: {project}-{environment}-{resource-type}-{name}
resource "aws_s3_bucket" "main" {
  bucket = "myapp-prod-data-customer-uploads"
}

# Pattern: this for single resource of type
resource "aws_security_group" "this" {
  name = "${var.project}-${var.environment}-app"
}
```

### Variable Naming
- Use snake_case: `instance_type`, `vpc_cidr_block`
- Boolean prefix with `enable_` or `create_`: `enable_monitoring`, `create_vpc`
- Plural for lists: `subnet_ids`, `availability_zones`

### File Organization
- `main.tf` - Primary resource definitions
- `variables.tf` - Input variables
- `outputs.tf` - Output values
- `versions.tf` - Provider and Terraform version constraints
- `data.tf` - Data sources (optional)
- `locals.tf` - Local values (optional)

## Code Styling Best Practices

### Formatting
```hcl
# Use terraform fmt
# Group related settings
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  tags = {
    Name        = "${var.project}-web"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Align equals signs in blocks
variable "instance_config" {
  type = object({
    instance_type = string
    volume_size   = number
    volume_type   = string
  })
}
```

### Module Structure
```hcl
# versions.tf - Pin versions
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# variables.tf - Document everything
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be valid IPv4 CIDR."
  }
}
```

## State Management

### Backend Configuration
```hcl
# Use remote state for team collaboration
terraform {
  backend "s3" {
    bucket         = "myapp-terraform-state"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### State Best Practices
- **Never commit** `.tfstate` files to version control (contains plaintext secrets)
- Use **remote backend** (S3, Azure Storage, GCS) with locking
- **CRITICAL**: State files contain sensitive data (passwords, keys, IPs)
  - Enable versioning on backend storage for rollback capability
  - Restrict access via IAM policies (least privilege principle)
  - Consider using `sensitive = true` for sensitive outputs
- Separate state files by environment and component
- Use **state file encryption** at rest (AES-256)
- Implement **state file backups** and disaster recovery procedures
- Use `terraform_remote_state` data source for cross-stack references

## Terraform vs Terragrunt

### When to Use Vanilla Terraform
✅ Small to medium infrastructure (< 50 resources)
✅ Single cloud provider
✅ Few environments (dev/prod)
✅ Team comfortable with DRY through modules

### When to Use Terragrunt
✅ Large infrastructure (100+ resources)
✅ Many environments (dev/staging/prod/dr)
✅ Deep directory hierarchies
✅ Need for inheritance and composition
✅ Complex dependency orchestration

### Terragrunt Benefits
- DRY backend configuration
- Dependency orchestration
- Variable inheritance
- Before/after hooks
- Auto-init and auto-retry

## Recommended Tools

### Essential
- **terraform** - Core IaC tool
- **terraform fmt** - Code formatter (built-in)
- **terraform validate** - Syntax validator (built-in)

### Quality & Linting
- **tflint** - Terraform linter with provider-specific rules
- **tfsec** - Security scanner for Terraform code
- **checkov** - Policy-as-code scanner
- **terraform-docs** - Auto-generate documentation

### Version Management
- **tfenv** - Terraform version manager (like nvm for Node)
- **tgenv** - Terragrunt version manager

### Workflow Automation
- **pre-commit-terraform** - Git hooks for quality gates
- **Atlantis** - Pull request automation for Terraform
- **Infracost** - Cost estimation in PRs

### Orchestration
- **Terragrunt** - DRY orchestration wrapper
- **Terramate** - Stack orchestration and code generation

## Common Patterns

### Multi-Environment Setup
```hcl
# environments/dev/main.tf
module "infrastructure" {
  source = "../../modules/infrastructure"

  environment    = "dev"
  instance_type  = "t3.micro"
  instance_count = 1
}

# environments/prod/main.tf
module "infrastructure" {
  source = "../../modules/infrastructure"

  environment    = "prod"
  instance_type  = "t3.large"
  instance_count = 3
}
```

### Module Composition
```hcl
# modules/infrastructure/main.tf
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project}-${var.environment}"
  cidr = var.vpc_cidr
}

module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name   = "${var.project}-${var.environment}-app"
  vpc_id = module.vpc.vpc_id
}
```

### Conditional Resources
```hcl
resource "aws_instance" "bastion" {
  count = var.create_bastion ? 1 : 0

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
}

# Access with: aws_instance.bastion[0]
```

## Frequent Terraform Problems (FTP)

### Dependency Hell
**Problem**: Circular dependencies between modules, version conflicts
**Solution**:
- Pin provider and module versions explicitly
- Use Dependabot for automated updates
- Implement testing for version upgrades
- Avoid cross-module dependencies; use data sources instead

### State Lock Issues
**Problem**: "Error acquiring state lock"
**Solution**:
- Implement DynamoDB table for S3 backend locking
- Use `terraform force-unlock` cautiously
- Never delete `.terraform.lock.hcl`

### Resource Drift
**Problem**: Manual changes outside Terraform
**Solution**:
- Run `terraform plan` regularly in CI
- Use `terraform refresh` to detect drift
- Implement policy-as-code (OPA, Sentinel)
- Restrict manual changes via IAM policies

### Count vs For_Each
**Problem**: Changing count causes resource recreation
**Solution**:
- Prefer `for_each` with maps for stable resources
- Use `count` only for simple on/off toggles
```hcl
# Bad - index changes cause recreation
resource "aws_subnet" "example" {
  count      = length(var.azs)
  cidr_block = cidrsubnet(var.vpc_cidr, 8, count.index)
}

# Good - stable keys prevent recreation with explicit mapping
locals {
  az_cidrs = {
    "us-east-1a" = cidrsubnet(var.vpc_cidr, 8, 0)
    "us-east-1b" = cidrsubnet(var.vpc_cidr, 8, 1)
    "us-east-1c" = cidrsubnet(var.vpc_cidr, 8, 2)
  }
}

resource "aws_subnet" "example" {
  for_each          = local.az_cidrs
  availability_zone = each.key
  cidr_block        = each.value
}
```

## Working with This Skill

### For Beginners
1. Start with the **Small Infrastructure** pattern
2. Read `references/terraform.md` for code structure examples
3. Review naming conventions before writing code
4. Use `terraform fmt` and `tflint` from day one

### For Scaling Up
1. Review **Medium Infrastructure** patterns when hitting 20+ resources
2. Evaluate Terragrunt when managing 3+ environments
3. Implement module composition for reusability
4. Set up remote state and locking

### For Production Readiness
1. Pin all provider and module versions
2. Implement pre-commit hooks for quality gates
3. Use Atlantis or similar for PR-based workflows
4. Add security scanning (tfsec, checkov) to CI/CD
5. Set up cost estimation (Infracost)

## Reference Files

### references/terraform.md
Complete documentation extracted from terraform-best-practices.com covering:
- Code structure patterns for all infrastructure sizes
- Module types and composition strategies
- Real-world examples from small to large setups
- Tool recommendations and integration guides

### references/examples.md
Practical examples demonstrating:
- Small/medium/large infrastructure implementations
- Terraform vs Terragrunt comparisons
- Module composition patterns
- Environment-specific configurations

### references/llms.md
Multilingual index of all content (20+ languages available on source website)

## Quick Reference Commands

```bash
# Initialize and validate
terraform init
terraform validate
terraform fmt -recursive

# Plan and apply
terraform plan -out=tfplan
terraform apply tfplan

# State management
terraform state list
terraform state show aws_instance.web
terraform state mv aws_instance.old aws_instance.new

# Workspace management
terraform workspace list
terraform workspace select dev
terraform workspace new staging

# Import existing resources
terraform import aws_instance.web i-1234567890abcdef0

# Debugging
TF_LOG=DEBUG terraform apply
terraform console  # Interactive evaluation
```

## Additional Resources

- **Source**: [terraform-best-practices.com](https://www.terraform-best-practices.com) (Anton Babenko)
- **Workshop**: [GitHub Workshop](https://github.com/antonbabenko/terraform-best-practices-workshop)
- **Community Modules**: [Terraform AWS Modules](https://github.com/terraform-aws-modules)
- **Official Docs**: [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)

## Notes

- This skill represents **community best practices** (Anton Babenko), not official HashiCorp documentation
- Content is based on Terraform 1.0+ patterns and recommendations
- Focuses on AWS examples but principles apply to all providers
- Reference files extracted from multilingual source (English content emphasized)

## Updating This Skill

To refresh with latest best practices:
```bash
skill-seekers scrape https://www.terraform-best-practices.com/ \
  --name terraform-best-practices \
  --max-pages 50
```
