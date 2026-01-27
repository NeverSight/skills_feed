---
name: terraform-engineer
description: Infrastructure as Code (IaC) expert using Terraform/OpenTofu, HCL, and modern state management.
---

# Terraform Engineer

## Purpose

Provides Infrastructure as Code expertise specializing in Terraform and OpenTofu for cloud provisioning. Designs modular, scalable infrastructure with proper state management, remote backends, and GitOps-driven automation pipelines.

## When to Use

- Provisioning new cloud infrastructure (VPCs, EKS, RDS)
- Refactoring monolithic Terraform code into reusable modules
- Implementing "GitOps" for infrastructure (Atlantis/TFC)
- Managing remote state, locking, and backend configuration
- Writing custom providers or complex HCL logic (loops, conditionals)
- Migrating/importing existing manual infrastructure into Terraform

## Examples

### Example 1: Multi-Cloud Landing Zone

**Scenario:** Building a secure, compliant multi-cloud landing zone.

**Implementation:**
1. Created reusable modules for VPC, IAM, security groups
2. Implemented remote state with S3 backend and DynamoDB locking
3. Added variable validation and preconditions
4. Implemented cost estimation and budget alerts
5. Set up Terraform Cloud for state management

**Results:**
- Infrastructure provisioning reduced from weeks to hours
- 100% consistency across environments
- Security compliance automated
- 40% reduction in cloud costs through optimization

### Example 2: Kubernetes Platform with EKS

**Scenario:** Building a production-ready Kubernetes platform.

**Implementation:**
1. Created EKS module with managed node groups
2. Implemented RBAC and service accounts
3. Added network policies and security groups
4. Configured secrets management with Vault integration
5. Set up monitoring and observability

**Results:**
- Platform deployment in under 30 minutes
- Zero configuration drift
- Built-in security controls
- Clear upgrade path for K8s versions

### Example 3: Legacy Infrastructure Migration

**Scenario:** Importing manually provisioned infrastructure into Terraform.

**Implementation:**
1. Used terraform import for existing resources
2. Created corresponding Terraform configurations
3. Implemented state mv for resource reorganization
4. Verified no changes during import
5. Established Terraform as source of truth

**Results:**
- 200+ resources migrated to Terraform
- Infrastructure now version controlled
- Enables infrastructure as code workflows
- Improved audit and compliance

## Best Practices

### State Management

- **Remote Backend**: Always use remote state (S3, GCS, Terraform Cloud)
- **State Locking**: Prevent concurrent modifications
- **State Isolation**: Separate state for environments
- **Backup**: Enable state versioning

### Module Development

- **Single Responsibility**: Each module does one thing well
- **Version Pinning**: Lock module versions
- **Documentation**: Document inputs, outputs, behavior
- **Testing**: Test modules before publishing

### Code Quality

- **Formatting**: Use terraform fmt consistently
- **Validation**: Run terraform validate
- **Linting**: Use tflint for provider-specific issues
- **Security Scanning**: Use tfsec/checkov

### Collaboration

- **Code Review**: All changes reviewed before merge
- **Workspace Strategy**: Use workspaces for environment isolation
- **Variable Management**: Use variable files, not hardcoding
- **Output Documentation**: Document important outputs

---
---

## 2. Decision Framework

### State Management Strategy

| Scale | Strategy | Backend |
|-------|----------|---------|
| **Individual** | Local State | `local` (Not recommended for prod) |
| **Small Team** | Remote State + Locking | `s3` + DynamoDB (AWS) / `azurerm` (Azure) |
| **Enterprise** | Managed State + Runs | **Terraform Cloud** / **spacelift** / **env0** |
| **GitOps** | PR-driven Runs | **Atlantis** (Self-hosted) |

### Module Architecture

```
What are you building?
│
├─ **Root Module** (The "Glue")
│  ├─ `main.tf`: Instantiates child modules
│  ├─ `providers.tf`: Provider config
│  └─ `backend.tf`: State config
│
├─ **Child Modules** (Reusable)
│  ├─ **Resource Modules**: Wraps single resource (e.g., `s3-secure-bucket`)
│  │  └─ Enforces tagging, encryption, logging defaults.
│  │
│  └─ **Infrastructure Modules**: Logical group (e.g., `vpc-with-peering`)
│     └─ Combines VPC, Subnets, Route Tables, NAT Gateways.
│
└─ **Composition** (Terragrunt/Workspaces)
   ├─ `prod/`
   ├─ `stage/`
   └─ `dev/`
```

### Terraform vs. The World

| Tool | Approach | Best For |
|------|----------|----------|
| **Terraform** | HCL (Declarative) | Industry standard, massive ecosystem. |
| **Pulumi** | General Purpose Lang (TS/Py) | Devs who hate HCL, dynamic logic. |
| **Crossplane** | K8s Custom Resources | Control planes, self-service platforms. |
| **CloudFormation** | YAML/JSON | AWS purists (drift detection is native). |

**Red Flags → Escalate to `security-engineer`:**
- Hardcoded AWS keys in `provider` block
- State files stored in git (`terraform.tfstate`)
- Security Groups allowing `0.0.0.0/0` on SSH/RDP
- S3 buckets public by default

---
---

## 3. Core Workflows

### Workflow 1: Production AWS VPC (Modular)

**Goal:** Create a 3-tier VPC network using the community module.

**Steps:**

1.  **Dependency Definition (`versions.tf`)**
    ```hcl
    terraform {
      required_version = ">= 1.5.0"
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 5.0"
        }
      }
    }
    ```

2.  **Implementation (`main.tf`)**
    ```hcl
    module "vpc" {
      source = "terraform-aws-modules/vpc/aws"
      version = "5.5.1"

      name = "prod-vpc"
      cidr = "10.0.0.0/16"

      azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
      private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
      public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

      enable_nat_gateway = true
      single_nat_gateway = false # High Availability
      enable_vpn_gateway = false

      tags = {
        Environment = "Production"
        Terraform   = "true"
      }
    }
    ```

3.  **Outputs (`outputs.tf`)**
    ```hcl
    output "vpc_id" {
      description = "The ID of the VPC"
      value       = module.vpc.vpc_id
    }
    ```

---
---

### Workflow 3: Importing Existing Infrastructure

**Goal:** Bring a manually created EC2 instance under Terraform control.

**Steps:**

1.  **Identify Resource ID**
    -   AWS Console → EC2 → Instance ID: `i-0123456789abcdef0`

2.  **Write Terraform Code**
    ```hcl
    resource "aws_instance" "legacy_server" {
      ami           = "ami-0c55b159cbfafe1f0"
      instance_type = "t2.micro"
      # Fill in other known details...
    }
    ```

3.  **Run Import**
    ```bash
    terraform import aws_instance.legacy_server i-0123456789abcdef0
    ```
    *(Or use `import` block in TF 1.5+)*
    ```hcl
    import {
      to = aws_instance.legacy_server
      id = "i-0123456789abcdef0"
    }
    ```

4.  **Reconcile**
    -   Run `terraform plan`.
    -   Update code to match the state until "No changes" is reported.

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Monolithic State File

**What it looks like:**
-   One `main.tf` controlling VPC, Database, EKS, and 50 Microservices.
-   `terraform plan` takes 10 minutes.

**Why it fails:**
-   **Blast Radius:** One error breaks everything.
-   **Performance:** API rate limits (AWS Throttling).
-   **Locking:** Dev A blocks Dev B.

**Correct approach:**
-   **Split State:** Separate `network`, `data`, `app-cluster`.
-   Use `terraform_remote_state` data source to read outputs from other layers.

### ❌ Anti-Pattern 2: Hardcoding Environments

**What it looks like:**
-   `vpc-prod.tf`, `vpc-dev.tf` files with duplicated code.

**Why it fails:**
-   Drift between environments.
-   Double maintenance.

**Correct approach:**
-   **Workspaces:** Use `terraform workspace` with `var.environment`.
-   **Tfvars:** `prod.tfvars` vs `dev.tfvars`.
-   **Modules:** Reuse the same logic, pass different variables.

### ❌ Anti-Pattern 3: Ignoring `.gitignore`

**What it looks like:**
-   Committing `.terraform/` directory (plugins).
-   Committing `terraform.tfvars` (secrets).

**Why it fails:**
-   Repo bloat.
-   Security leak.

**Correct approach:**
-   Standard `.gitignore` for Terraform:
    ```
    .terraform/
    *.tfstate
    *.tfstate.backup
    *.tfvars
    .terraform.lock.hcl (Commit this one!)
    ```

---
---

## 7. Quality Checklist

**Code Quality:**
-   [ ] **Formatting:** Run `terraform fmt -recursive`.
-   [ ] **Validation:** Run `terraform validate`.
-   [ ] **Linting:** Run `tflint` for provider-specific issues.
-   [ ] **Docs:** Generate README using `terraform-docs`.

**Security:**
-   [ ] **Secrets:** No plain text secrets (Use KMS/Vault/Secrets Manager).
-   [ ] **Encryption:** `encrypted = true` on all storage (EBS, S3, RDS).
-   [ ] **Public Access:** Locked down (S3 Block Public Access).

**Reliability:**
-   [ ] **State:** Remote backend configured with locking.
-   [ ] **Versions:** Provider and Terraform versions pinned (e.g., `~> 5.0`).
-   [ ] **Cleanup:** `destroy` provisioners tested (or protection enabled for DBs).

## Anti-Patterns

### State Management Anti-Patterns

- **Local State**: Using local state files - always use remote backends
- **State Drift**: Manual changes outside Terraform - use only Terraform for changes
- **State Lock Contention**: No state locking - implement proper locking
- **State Corruption**: Editing state files manually - never manually edit state

### Module Anti-Patterns

- **Monolithic Modules**: Large, unwieldy modules - split into focused modules
- **Hardcoded Values**: Using values instead of variables - parameterize everything
- **Module Version Chaos**: No version pinning - pin module versions
- **Deep Module Nesting**: Over-nested module structures - keep module hierarchy flat

### Resource Anti-Patterns

- **Resource Spam**: Many small resources instead of patterns - use resource grouping
- **Lifecycle Lock**: Resources that can't update - avoid create_before_destroy conflicts
- **Ignored Changes**: Overusing ignore_changes - understand and manage changes
- **Sensitive Data Exposure**: Plain text secrets in state - use sensitive flag

### Code Organization Anti-Patterns

- **Flat Structure**: No directory organization - use modular structure
- **Duplication**: Repeated code blocks - use modules and for_each
- **No Formatting**: Unformatted HCL code - use terraform fmt
- **Missing Documentation**: undocumented modules - document all inputs/outputs
