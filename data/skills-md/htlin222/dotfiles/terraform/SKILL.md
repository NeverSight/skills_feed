---
name: terraform
description: Write Terraform modules, manage state, and implement IaC. Use for infrastructure automation or state management.
---

# Terraform

Infrastructure as Code with Terraform.

## When to Use

- Creating infrastructure modules
- Managing Terraform state
- Multi-environment deployments
- Importing existing resources
- Troubleshooting drift

## Module Structure

```
modules/
└── vpc/
    ├── main.tf       # Resources
    ├── variables.tf  # Input variables
    ├── outputs.tf    # Output values
    └── versions.tf   # Provider requirements
```

## Best Practices

### Variables

```hcl
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

### Resources

```hcl
resource "aws_instance" "main" {
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}"
  })

  lifecycle {
    create_before_destroy = true
  }
}
```

### Outputs

```hcl
output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.main.id
}
```

## State Management

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "project/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

## Common Commands

```bash
# Initialize and plan
terraform init
terraform plan -out=tfplan

# Apply with auto-approve (CI/CD)
terraform apply -auto-approve tfplan

# Import existing resource
terraform import aws_instance.main i-1234567890abcdef0

# State operations
terraform state list
terraform state show aws_instance.main
terraform state mv aws_instance.old aws_instance.new
```

## Workspace Strategy

```bash
# Create workspaces per environment
terraform workspace new dev
terraform workspace new prod

# Use in configuration
locals {
  env_config = {
    dev  = { instance_type = "t3.micro" }
    prod = { instance_type = "t3.large" }
  }
  config = local.env_config[terraform.workspace]
}
```

## Examples

**Input:** "Create a VPC module"
**Action:** Create module with subnets, route tables, NAT gateway, proper outputs

**Input:** "Fix state drift"
**Action:** Run plan, identify drift, decide refresh vs import vs manual fix
