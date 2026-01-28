---
name: iac-automation
description: Terraform, Pulumi, CloudFormation, and infrastructure as code for data platforms
sasmp_version: "1.3.0"
bonded_agent: 03-devops-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 100
prerequisites: [cloud-platforms, git-version-control]
unlocks: [cicd-pipelines, containerization]
---

# Infrastructure as Code

Production infrastructure automation with Terraform, Pulumi, and cloud-native IaC patterns.

## Quick Start

```hcl
# Terraform - AWS Data Lake Infrastructure
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "terraform-state-prod"
    key    = "data-lake/terraform.tfstate"
    region = "us-east-1"
  }
}

# Data Lake S3 Bucket
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake-${var.environment}"

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Glue Catalog Database
resource "aws_glue_catalog_database" "analytics" {
  name = "analytics_${var.environment}"
}

# Output
output "data_lake_bucket" {
  value = aws_s3_bucket.data_lake.bucket
}
```

## Core Concepts

### 1. Terraform Modules

```hcl
# modules/data-pipeline/main.tf
variable "pipeline_name" {
  type        = string
  description = "Name of the data pipeline"
}

variable "schedule" {
  type    = string
  default = "cron(0 2 * * ? *)"
}

resource "aws_glue_job" "etl" {
  name     = var.pipeline_name
  role_arn = aws_iam_role.glue.arn

  command {
    script_location = "s3://${var.scripts_bucket}/jobs/${var.pipeline_name}.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"        = "python"
    "--enable-metrics"      = "true"
    "--enable-spark-ui"     = "true"
  }

  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2
}

resource "aws_glue_trigger" "scheduled" {
  name     = "${var.pipeline_name}-trigger"
  schedule = var.schedule
  type     = "SCHEDULED"

  actions {
    job_name = aws_glue_job.etl.name
  }
}

# Usage
module "customer_pipeline" {
  source        = "./modules/data-pipeline"
  pipeline_name = "customer-etl"
  schedule      = "cron(0 3 * * ? *)"
}
```

### 2. State Management

```hcl
# Remote state configuration
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "env/prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# State locking with DynamoDB
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

# Import existing resources
# terraform import aws_s3_bucket.existing bucket-name

# Move resources between states
# terraform state mv module.old.resource module.new.resource
```

### 3. Pulumi (Python)

```python
import pulumi
import pulumi_aws as aws

# Configuration
config = pulumi.Config()
environment = config.require("environment")

# S3 Data Lake
data_lake = aws.s3.Bucket(
    "data-lake",
    bucket=f"company-data-lake-{environment}",
    versioning=aws.s3.BucketVersioningArgs(enabled=True),
    tags={"Environment": environment, "ManagedBy": "pulumi"}
)

# Glue Database
analytics_db = aws.glue.CatalogDatabase(
    "analytics",
    name=f"analytics_{environment}"
)

# Lambda for data processing
data_processor = aws.lambda_.Function(
    "data-processor",
    runtime="python3.11",
    handler="handler.main",
    role=lambda_role.arn,
    code=pulumi.FileArchive("./lambda"),
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={"BUCKET": data_lake.bucket}
    )
)

# Export outputs
pulumi.export("bucket_name", data_lake.bucket)
pulumi.export("database_name", analytics_db.name)
```

### 4. Environment Management

```hcl
# environments/prod/main.tf
module "data_platform" {
  source = "../../modules/data-platform"

  environment         = "prod"
  vpc_cidr           = "10.0.0.0/16"
  instance_type      = "r5.2xlarge"
  min_capacity       = 2
  max_capacity       = 10

  tags = {
    Environment = "prod"
    CostCenter  = "data-engineering"
  }
}

# Workspace-based environments
# terraform workspace new prod
# terraform workspace select prod

locals {
  env_config = {
    dev = {
      instance_type = "t3.medium"
      min_nodes     = 1
    }
    prod = {
      instance_type = "r5.xlarge"
      min_nodes     = 3
    }
  }
  config = local.env_config[terraform.workspace]
}
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **Terraform** | IaC standard | 1.7+ |
| **Pulumi** | IaC with Python | 3.100+ |
| **CloudFormation** | AWS native | Latest |
| **Terragrunt** | Terraform wrapper | 0.55+ |
| **tfsec** | Security scanning | 1.28+ |
| **Checkov** | Policy as code | 3.2+ |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **State Lock** | Can't apply | Previous run crashed | `terraform force-unlock` |
| **Drift** | Plan shows changes | Manual changes | Import or recreate |
| **Cycle Error** | Dependency cycle | Circular references | Refactor dependencies |
| **Provider Error** | Auth failed | Wrong credentials | Check AWS profile |

## Best Practices

```hcl
# ✅ DO: Use variables with validation
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# ✅ DO: Tag all resources
default_tags {
  tags = {
    ManagedBy   = "terraform"
    Environment = var.environment
  }
}

# ✅ DO: Use data sources for existing resources
data "aws_vpc" "existing" {
  id = var.vpc_id
}

# ❌ DON'T: Hard-code values
# ❌ DON'T: Store state locally in production
# ❌ DON'T: Skip plan review before apply
```

## Resources

- [Terraform Docs](https://developer.hashicorp.com/terraform)
- [Pulumi Docs](https://www.pulumi.com/docs/)
- [AWS CDK](https://docs.aws.amazon.com/cdk/)

---

**Skill Certification Checklist:**
- [ ] Can write Terraform modules
- [ ] Can manage remote state
- [ ] Can use workspaces for environments
- [ ] Can implement security best practices
- [ ] Can automate with CI/CD
