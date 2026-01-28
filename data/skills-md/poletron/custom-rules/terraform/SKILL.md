---
name: terraform
description: >
  Terraform infrastructure as code patterns and best practices.
  Trigger: When writing Terraform infrastructure code.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with terraform"

## When to Use

Use this skill when:
- Writing Terraform HCL configurations
- Managing cloud infrastructure as code
- Creating reusable modules
- Implementing state management

---

## Critical Patterns

### Module Structure (REQUIRED)

```hcl
# ✅ ALWAYS: Standard module structure
# modules/vpc/
# ├── main.tf
# ├── variables.tf
# ├── outputs.tf
# └── README.md

# variables.tf
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# outputs.tf
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}
```

### Naming Conventions (REQUIRED)

```hcl
# ✅ ALWAYS: snake_case for resources and variables
resource "aws_instance" "web_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  
  tags = {
    Name        = "${var.project_name}-web-server"
    Environment = var.environment
  }
}

# ❌ NEVER: Mixed or unclear naming
resource "aws_instance" "WebServer" { ... }
```

### State Management (REQUIRED)

```hcl
# ✅ ALWAYS: Remote state with locking
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

---

## Decision Tree

```
Need reusability?          → Create module
Need environment config?   → Use workspaces or tfvars
Need secrets?              → Use SSM/Secrets Manager
Need state locking?        → Use DynamoDB table
Need validation?           → Add variable validation
```

---

## Code Examples

### Variable Validation

```hcl
variable "environment" {
  description = "Environment name"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### For Each Pattern

```hcl
resource "aws_security_group_rule" "ingress" {
  for_each = var.ingress_rules
  
  type              = "ingress"
  from_port         = each.value.port
  to_port           = each.value.port
  protocol          = each.value.protocol
  cidr_blocks       = each.value.cidr_blocks
  security_group_id = aws_security_group.main.id
}
```

---

## Commands

```bash
terraform init              # Initialize providers
terraform plan              # Preview changes
terraform apply             # Apply changes
terraform destroy           # Destroy infrastructure
terraform fmt               # Format code
terraform validate          # Validate syntax
```
