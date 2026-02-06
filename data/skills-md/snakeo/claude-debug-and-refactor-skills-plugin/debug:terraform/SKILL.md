---
name: debug:terraform
description: Debug Terraform infrastructure-as-code issues systematically. This skill helps diagnose and resolve Terraform-specific problems including state lock conflicts, provider authentication failures, resource dependency cycles, state drift detection, import failures, module version conflicts, and plan/apply errors. Provides TF_LOG debugging, terraform console usage, state manipulation commands, and CI/CD best practices for infrastructure automation.
---

# Terraform Debugging Guide

Debug Terraform configurations and state issues using a systematic four-phase approach with provider-specific considerations.

## Error Classification

Terraform errors fall into four categories:

1. **Language Errors** - Syntax and configuration issues
2. **State Errors** - State file corruption, drift, or lock issues
3. **Core Errors** - Terraform engine problems
4. **Provider Errors** - Cloud provider authentication or API issues

## Phase 1: Reproduce and Isolate

### Gather Initial Information

```bash
# Check Terraform and provider versions
terraform version

# Validate configuration syntax
terraform validate

# Review current state
terraform state list
terraform state show <resource_address>

# Check for state drift
terraform plan -refresh-only
```

### Enable Debug Logging

```bash
# Set log level (TRACE, DEBUG, INFO, WARN, ERROR)
export TF_LOG=DEBUG

# Write logs to file (recommended for large outputs)
export TF_LOG_PATH="./terraform-debug.log"

# For provider-specific debugging
export TF_LOG_PROVIDER=DEBUG

# Run command with logging
terraform plan
```

**Log Levels:**
- `TRACE` - Maximum verbosity, every action logged
- `DEBUG` - Detailed debugging for complex issues
- `INFO` - General informative messages
- `WARN` - Non-critical warnings
- `ERROR` - Critical errors only

### Isolate the Problem

```bash
# Target specific resource
terraform plan -target=aws_instance.example

# Check specific module
terraform plan -target=module.networking

# Validate single file
terraform validate -json
```

## Phase 2: Analyze Root Cause

### Common Error Patterns and Solutions

#### State Lock Errors

```
Error: Error acquiring the state lock
```

**Diagnosis:**
```bash
# Check if another process is running
ps aux | grep terraform

# View lock info (for S3 backend)
aws dynamodb get-item --table-name terraform-locks --key '{"LockID":{"S":"your-state-path"}}'
```

**Solution:**
```bash
# Force unlock (use with caution!)
terraform force-unlock <LOCK_ID>

# For S3/DynamoDB backend
aws dynamodb delete-item --table-name terraform-locks --key '{"LockID":{"S":"your-state-path"}}'
```

#### Provider Authentication Failures

```
Error: error configuring Terraform AWS Provider: no valid credential sources found
```

**Diagnosis:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify environment variables
env | grep AWS

# Check credential file
cat ~/.aws/credentials
```

**Solution:**
```hcl
# Explicit provider configuration
provider "aws" {
  region  = "us-east-1"
  profile = "my-profile"

  # Or use assume_role
  assume_role {
    role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
  }
}
```

#### Resource Dependency Cycles

```
Error: Cycle: aws_security_group.a, aws_security_group.b
```

**Diagnosis:**
```bash
# Generate dependency graph
terraform graph | dot -Tpng > graph.png

# Or view in text format
terraform graph
```

**Solution:**
```hcl
# Break cycle with explicit dependencies
resource "aws_security_group" "a" {
  name = "sg-a"
  # Remove circular reference
}

resource "aws_security_group_rule" "a_to_b" {
  security_group_id        = aws_security_group.a.id
  source_security_group_id = aws_security_group.b.id
  # ...
}
```

#### State Drift

```
Note: Objects have changed outside of Terraform
```

**Diagnosis:**
```bash
# Detect drift
terraform plan -refresh-only

# Show current state
terraform show

# Pull remote state for inspection
terraform state pull > state.json
```

**Solution:**
```bash
# Accept external changes into state
terraform apply -refresh-only

# Or reimport drifted resource
terraform import aws_instance.example i-1234567890abcdef0

# Or replace resource to match config
terraform apply -replace=aws_instance.example
```

#### Import Failures

```
Error: Cannot import non-existent remote object
```

**Diagnosis:**
```bash
# Verify resource exists
aws ec2 describe-instances --instance-ids i-1234567890abcdef0

# Check import syntax for resource type
terraform providers schema -json | jq '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas["aws_instance"]'
```

**Solution:**
```bash
# Correct import command
terraform import aws_instance.example i-1234567890abcdef0

# For modules
terraform import module.ec2.aws_instance.example i-1234567890abcdef0

# Generate import blocks (Terraform 1.5+)
terraform plan -generate-config-out=generated.tf
```

#### Module Version Conflicts

```
Error: Module version requirements have changed
```

**Diagnosis:**
```bash
# Check current module versions
terraform providers lock -platform=linux_amd64

# View dependency tree
cat .terraform.lock.hcl
```

**Solution:**
```bash
# Upgrade modules
terraform init -upgrade

# Clear cache and reinitialize
rm -rf .terraform
terraform init

# Pin specific version
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
}
```

#### Resource Already Exists

```
Error: Error creating S3 bucket: BucketAlreadyExists
```

**Solution:**
```bash
# Import existing resource
terraform import aws_s3_bucket.example my-bucket-name

# Or use data source to reference
data "aws_s3_bucket" "existing" {
  bucket = "my-bucket-name"
}
```

## Phase 3: Fix and Verify

### Interactive Debugging

```bash
# Open Terraform console for expression testing
terraform console

# Test expressions
> var.instance_type
> aws_instance.example.id
> length(var.subnets)
> jsonencode(local.tags)
```

### State Manipulation (Use with Caution)

```bash
# Remove resource from state (doesn't destroy)
terraform state rm aws_instance.orphaned

# Move resource in state
terraform state mv aws_instance.old aws_instance.new

# Move to different state file
terraform state mv -state-out=other.tfstate aws_instance.example aws_instance.example

# Replace provider in state
terraform state replace-provider hashicorp/aws registry.terraform.io/hashicorp/aws
```

### Safe Apply Strategies

```bash
# Preview changes
terraform plan -out=tfplan

# Apply with plan file (recommended)
terraform apply tfplan

# Apply specific resource only
terraform apply -target=aws_instance.example

# Destroy and recreate
terraform apply -replace=aws_instance.problematic
```

## Phase 4: Document and Prevent

### Pre-Commit Validation

```bash
# Validate syntax
terraform validate

# Format check
terraform fmt -check -recursive

# Use tflint for best practices
tflint --init
tflint

# Security scanning with checkov
checkov -d .

# Cost estimation
infracost breakdown --path=.
```

### CI/CD Best Practices

```bash
# CI-friendly commands
terraform init -input=false
terraform plan -input=false -no-color -out=tfplan
terraform apply -input=false -no-color tfplan

# Lock provider versions
terraform providers lock -platform=linux_amd64 -platform=darwin_amd64
```

### Configuration Best Practices

```hcl
# Pin Terraform version
terraform {
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Use variables with validation
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# Add lifecycle rules for critical resources
resource "aws_instance" "critical" {
  # ...
  lifecycle {
    prevent_destroy = true
    create_before_destroy = true
  }
}
```

## Quick Reference Commands

| Command | Purpose |
|---------|---------|
| `terraform validate` | Check syntax and configuration |
| `terraform plan` | Preview changes |
| `terraform plan -refresh-only` | Detect state drift |
| `terraform state list` | List all resources in state |
| `terraform state show <addr>` | Show resource details |
| `terraform state pull` | Download remote state |
| `terraform state rm <addr>` | Remove from state |
| `terraform import <addr> <id>` | Import existing resource |
| `terraform force-unlock <id>` | Release state lock |
| `terraform console` | Interactive expression testing |
| `terraform graph` | Generate dependency graph |
| `terraform providers` | Show required providers |
| `terraform output` | Show output values |
| `terraform taint <addr>` | Mark for recreation (deprecated) |
| `terraform apply -replace=<addr>` | Force resource replacement |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `TF_LOG` | Set log level (TRACE/DEBUG/INFO/WARN/ERROR) |
| `TF_LOG_PATH` | Write logs to file |
| `TF_LOG_PROVIDER` | Provider-specific logging |
| `TF_INPUT` | Disable interactive prompts (0/false) |
| `TF_VAR_name` | Set variable value |
| `TF_CLI_ARGS` | Additional CLI arguments |
| `TF_DATA_DIR` | Custom data directory (default: .terraform) |
| `TF_WORKSPACE` | Set workspace |
| `TF_IN_AUTOMATION` | Adjust output for automation |
| `TF_PLUGIN_CACHE_DIR` | Share providers across projects |

## Debugging Checklist

- [ ] Read the complete error message carefully
- [ ] Check Terraform and provider versions
- [ ] Run `terraform validate` for syntax issues
- [ ] Enable debug logging with `TF_LOG=DEBUG`
- [ ] Check state with `terraform state list`
- [ ] Verify provider credentials and permissions
- [ ] Check for resource dependencies with `terraform graph`
- [ ] Review `.terraform.lock.hcl` for version conflicts
- [ ] Test expressions with `terraform console`
- [ ] Check cloud provider console for external changes
- [ ] Review recent changes in version control
- [ ] Search provider documentation for resource-specific issues

## Security Reminders

- Never commit state files or `.tfvars` with secrets to version control
- Sanitize debug logs before sharing (may contain credentials)
- Disable `TF_LOG` in production to prevent sensitive data exposure
- Use remote state with encryption for team environments
- Rotate credentials if exposed in logs
