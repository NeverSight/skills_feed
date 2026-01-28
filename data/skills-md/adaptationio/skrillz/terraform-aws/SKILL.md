---
name: terraform-aws
description: Comprehensive AWS infrastructure management with Terraform. Covers provider configuration, state management (S3 backend with native locking in Terraform 1.11+), common resource patterns (VPC, IAM, S3, RDS, EKS), module usage, and production best practices. Use when provisioning AWS infrastructure, managing Terraform state, creating VPCs, configuring IAM roles/policies, deploying databases, or troubleshooting Terraform/AWS issues.
---

# Terraform AWS Infrastructure Management

## Overview

Complete guide for managing AWS infrastructure as code using Terraform. This skill provides production-ready patterns for VPC networking, IAM security, state management, and common AWS resources with Terraform 1.11+ features and AWS Provider 6.x.

**Keywords**: Terraform, AWS, infrastructure as code, IaC, VPC, IAM, S3 backend, state locking, modules, EC2, RDS, EKS, security groups, CloudWatch

**Terraform Version**: 1.11+ (with S3 native locking)
**AWS Provider**: 6.x

## When to Use This Skill

- Provisioning AWS infrastructure with Terraform
- Setting up VPC networking with public/private subnets
- Configuring IAM roles, policies, and permissions
- Managing Terraform state with S3 backend
- Deploying databases (RDS, Aurora)
- Creating EKS-ready VPC configurations
- Troubleshooting Terraform plan/apply failures
- Migrating from DynamoDB to S3 native locking
- Importing existing AWS resources into Terraform

## Quick Start

### Basic AWS Provider Configuration

```hcl
terraform {
  required_version = ">= 1.11.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state-bucket"
    key    = "production/terraform.tfstate"
    region = "us-east-1"

    # Native S3 locking (Terraform 1.11+)
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}
```

### Variables Configuration

```hcl
variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "project_name" {
  description = "Project name for resource naming and tagging"
  type        = string
}
```

## Common Resource Patterns

### VPC with Public and Private Subnets

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = var.environment != "production"  # Cost optimization for non-prod

  enable_dns_hostnames = true
  enable_dns_support   = true

  # VPC Flow Logs
  enable_flow_log                      = true
  create_flow_log_cloudwatch_iam_role  = true
  create_flow_log_cloudwatch_log_group = true

  tags = {
    Environment = var.environment
  }
}
```

### S3 Bucket with Encryption and Versioning

```hcl
resource "aws_s3_bucket" "app_data" {
  bucket = "${var.project_name}-app-data-${var.environment}"

  tags = {
    Name        = "${var.project_name}-app-data"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

### IAM Role for EC2 with SSM Access

```hcl
# IAM role for EC2 instances
resource "aws_iam_role" "ec2_app_role" {
  name = "${var.project_name}-ec2-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach AWS managed policy for SSM
resource "aws_iam_role_policy_attachment" "ec2_ssm" {
  role       = aws_iam_role.ec2_app_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Custom policy for S3 access
resource "aws_iam_role_policy" "ec2_s3_access" {
  name = "${var.project_name}-ec2-s3-access"
  role = aws_iam_role.ec2_app_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.app_data.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.app_data.arn
      }
    ]
  })
}

# Instance profile for EC2
resource "aws_iam_instance_profile" "ec2_app_profile" {
  name = "${var.project_name}-ec2-app-profile"
  role = aws_iam_role.ec2_app_role.name
}
```

### RDS PostgreSQL Database

```hcl
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group for RDS database"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description     = "PostgreSQL from VPC"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    cidr_blocks     = [module.vpc.vpc_cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-db-${var.environment}"
  engine         = "postgres"
  engine_version = "16.3"

  instance_class    = var.environment == "production" ? "db.t3.medium" : "db.t3.micro"
  allocated_storage = var.environment == "production" ? 100 : 20
  storage_type      = "gp3"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password  # Use AWS Secrets Manager in production!

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = var.environment == "production" ? 30 : 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  deletion_protection = var.environment == "production"
  skip_final_snapshot = var.environment != "production"
  final_snapshot_identifier = var.environment == "production" ? "${var.project_name}-db-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}" : null

  tags = {
    Name        = "${var.project_name}-db"
    Environment = var.environment
  }
}
```

## State Management

### S3 Backend with Native Locking (Terraform 1.11+)

**Recommended approach** - No DynamoDB required!

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state-bucket"
    key    = "production/terraform.tfstate"
    region = "us-east-1"

    # Enable S3 native locking (Terraform 1.11+)
    use_lockfile = true

    # Encryption
    encrypt = true

    # Optional: Use KMS for encryption
    # kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/abcd1234-..."
  }
}
```

### Legacy: S3 + DynamoDB Locking

**For Terraform < 1.11:**

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

See [references/state-management.md](references/state-management.md) for complete state management patterns.

## Module Usage Patterns

### Using Community Modules

```hcl
# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project_name}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  enable_vpn_gateway = false
}

# EKS Module
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${var.project_name}-eks"
  cluster_version = "1.30"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    main = {
      min_size     = 2
      max_size     = 10
      desired_size = 3

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
    }
  }
}
```

### Creating Custom Modules

```
modules/
└── application/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

```hcl
# Using custom module
module "application" {
  source = "./modules/application"

  name        = "${var.project_name}-app"
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnets
}
```

## Common Workflows

### Initialize Terraform

```bash
# Initialize backend and download providers
terraform init

# Migrate state to new backend
terraform init -migrate-state

# Reconfigure backend
terraform init -reconfigure
```

### Plan and Apply Changes

```bash
# See what will change
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Auto-approve (use with caution!)
terraform apply -auto-approve

# Target specific resource
terraform apply -target=aws_instance.web
```

### Import Existing Resources

```bash
# Import VPC
terraform import aws_vpc.main vpc-12345678

# Import S3 bucket
terraform import aws_s3_bucket.app_data my-bucket-name

# Import RDS instance
terraform import aws_db_instance.main my-db-instance
```

### Workspace Management

```bash
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new staging

# Switch workspace
terraform workspace select production

# Show current workspace
terraform workspace show
```

## Detailed Documentation

For comprehensive guides on specific topics:

- **VPC Networking**: [references/vpc-networking.md](references/vpc-networking.md)
  - VPC module configuration
  - Public/private/intra subnets
  - NAT Gateway patterns
  - VPC endpoints
  - Security groups and NACLs
  - EKS-ready VPC setup

- **IAM Security**: [references/iam-security.md](references/iam-security.md)
  - IAM roles and policies
  - Assume role policies
  - Service-linked roles
  - Cross-account access
  - Permission boundaries
  - Policy best practices

- **State Management**: [references/state-management.md](references/state-management.md)
  - S3 backend configuration
  - Native locking vs DynamoDB
  - State encryption
  - Workspace strategies
  - Import and migration
  - State manipulation

## Common Issues and Solutions

| Issue | Cause | Fix |
|-------|-------|-----|
| State lock timeout | Orphaned lock file | `terraform force-unlock <lock-id>` |
| Provider version conflict | Incompatible versions | Update `required_providers` block |
| Cycle in resource dependencies | Circular reference | Use `depends_on` or split resources |
| Resource already exists | Resource created outside Terraform | Use `terraform import` |
| Insufficient permissions | Missing IAM permissions | Add required IAM policies |
| State drift detected | Manual changes in AWS | Review with `terraform plan`, then apply or import |

## Best Practices

### Resource Naming

```hcl
# Use consistent naming pattern
resource "aws_instance" "web" {
  # Format: {project}-{resource}-{environment}
  tags = {
    Name = "${var.project_name}-web-${var.environment}"
  }
}
```

### Environment-Specific Configuration

```hcl
# Use conditionals for environment differences
resource "aws_db_instance" "main" {
  instance_class = var.environment == "production" ? "db.r5.large" : "db.t3.micro"

  backup_retention_period = var.environment == "production" ? 30 : 7
  deletion_protection     = var.environment == "production"
}
```

### Sensitive Data Management

```hcl
# Never hardcode secrets!
variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

# Use AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "production/db/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

### Default Tags

```hcl
provider "aws" {
  region = var.aws_region

  # All resources get these tags automatically
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
      CostCenter  = var.cost_center
    }
  }
}
```

## Quick Reference Commands

```bash
# Initialization
terraform init                    # Initialize working directory
terraform init -upgrade           # Upgrade providers to latest version

# Planning
terraform plan                    # Show execution plan
terraform plan -out=tfplan        # Save plan to file
terraform plan -destroy           # Plan resource destruction

# Applying
terraform apply                   # Apply changes
terraform apply tfplan            # Apply saved plan
terraform destroy                 # Destroy all resources

# State Management
terraform state list              # List resources in state
terraform state show <resource>   # Show resource details
terraform state rm <resource>     # Remove resource from state
terraform state mv <src> <dest>   # Move/rename resource in state

# Validation
terraform fmt                     # Format HCL files
terraform fmt -recursive          # Format all .tf files
terraform validate                # Validate configuration
terraform validate -json          # JSON output for CI/CD

# Outputs
terraform output                  # Show all outputs
terraform output <name>           # Show specific output
terraform output -json            # JSON output

# Workspaces
terraform workspace list          # List workspaces
terraform workspace new <name>    # Create workspace
terraform workspace select <name> # Switch workspace
terraform workspace delete <name> # Delete workspace
```

## Production Deployment Checklist

- [ ] S3 backend configured with encryption
- [ ] State locking enabled (native S3 or DynamoDB)
- [ ] Remote state shared among team members
- [ ] Provider versions pinned in `required_providers`
- [ ] Variables defined with validation rules
- [ ] Sensitive variables marked as `sensitive = true`
- [ ] Secrets stored in AWS Secrets Manager (not hardcoded)
- [ ] Default tags configured on provider
- [ ] Resource naming follows consistent pattern
- [ ] VPC using private subnets for sensitive resources
- [ ] Security groups follow least privilege principle
- [ ] IAM roles using principle of least privilege
- [ ] CloudWatch logging enabled for critical resources
- [ ] Backup and retention policies configured
- [ ] `terraform fmt` and `terraform validate` pass
- [ ] State file stored in version-controlled S3 bucket
- [ ] `.terraform/` and `*.tfstate` in `.gitignore`

---

**Terraform Version**: 1.11+
**AWS Provider**: 6.x
**Best Practices**: Following AWS Well-Architected Framework
**Last Updated**: November 2025
