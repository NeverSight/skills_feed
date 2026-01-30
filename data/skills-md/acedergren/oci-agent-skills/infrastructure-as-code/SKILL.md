---
name: infrastructure-as-code
description: Use when writing Terraform for OCI, troubleshooting provider errors, managing state files, or implementing Resource Manager stacks. Covers terraform-provider-oci gotchas, resource lifecycle anti-patterns, state management mistakes, authentication issues, and OCI Landing Zones.
license: MIT
metadata:
  author: alexander-cedergren
  version: "2.0.0"
---

# OCI Infrastructure as Code - Expert Knowledge

## 🏗️ IMPORTANT: Use OCI Landing Zone Terraform Modules

### Do NOT Reinvent the Wheel

**❌ WRONG Approach:**
```hcl
# Writing Terraform from scratch for every resource
resource "oci_identity_compartment" "prod" { ... }
resource "oci_core_vcn" "main" { ... }
resource "oci_identity_policy" "policies" { ... }
# Result: Unmaintainable, inconsistent, no governance
```

**✅ RIGHT Approach: Use Official OCI Landing Zone Terraform Modules**

```hcl
# Use official OCI Landing Zone modules
module "landing_zone" {
  source  = "oracle-terraform-modules/landing-zone/oci"
  version = "~> 2.0"

  # Infrastructure configuration
  compartments_configuration = { ... }
  network_configuration = { ... }
  security_configuration = { ... }
}
```

**Why Use Landing Zone Modules:**
- ✅ **Battle-tested**: Thousands of OCI customers
- ✅ **Compliant**: CIS OCI Foundations Benchmark aligned
- ✅ **Maintained**: Oracle updates for API changes
- ✅ **Comprehensive**: Includes IAM, networking, security, logging
- ✅ **Reusable**: Consistent patterns across environments

**Official Resources:**
- [OCI Landing Zone Terraform Modules](https://github.com/oracle-terraform-modules/terraform-oci-landing-zones)
- [OCI Resource Manager Stacks](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/Tasks/deployments.htm)

**When to Write Custom Terraform** (this skill's guidance):
- Application-specific resources not covered by landing zone
- Extending landing zone modules
- Special requirements not in reference architecture

---

## ⚠️ OCI CLI/API Knowledge Gap

**You don't know OCI CLI commands or OCI API structure.**

Your training data has limited and outdated knowledge of:
- OCI Terraform provider syntax (updates frequently)
- OCI API endpoints and resource schemas
- terraform-provider-oci specific arguments and data sources
- Resource Manager stack operations
- Latest provider features and breaking changes

**When OCI operations are needed:**
1. Use exact Terraform examples from this skill's references
2. Do NOT guess OCI provider resource arguments
3. Do NOT assume AWS/Azure Terraform patterns work in OCI
4. Reference landing-zones skill for module usage

**What you DO know:**
- General Terraform concepts and HCL syntax
- State management principles
- Infrastructure as Code best practices

This skill bridges the gap by providing current OCI-specific Terraform patterns and gotchas.

---

You are an OCI Terraform expert. This skill provides knowledge Claude lacks: provider-specific gotchas, state management anti-patterns, resource lifecycle traps, and OCI-specific IaC operational knowledge.

## NEVER Do This

❌ **NEVER hardcode OCIDs in Terraform (breaks portability)**
```hcl
# WRONG - breaks when moving between regions/compartments
resource "oci_core_instance" "web" {
  compartment_id = "ocid1.compartment.oc1..aaaaaa..."  # Hardcoded!
  subnet_id      = "ocid1.subnet.oc1.phx.bbbbbb..."     # Hardcoded!
}

# RIGHT - use variables or data sources
resource "oci_core_instance" "web" {
  compartment_id = var.compartment_ocid
  subnet_id      = data.oci_core_subnet.existing.id
}
```

❌ **NEVER use `preserve_boot_volume = true` in dev/test (cost trap)**
```hcl
# WRONG - orphans boot volumes when instance destroyed ($50+/month per instance)
resource "oci_core_instance" "dev" {
  preserve_boot_volume = true  # Default behavior!
}

# RIGHT - explicit cleanup in dev/test
resource "oci_core_instance" "dev" {
  preserve_boot_volume = false
}
```

**Cost impact**: Dev team with 10 test instances × $5/volume/month = $50/month wasted on orphaned volumes

❌ **NEVER forget `lifecycle` blocks for critical resources**
```hcl
# WRONG - accidental destroy can delete production database
resource "oci_database_autonomous_database" "prod" {
  # No protection!
}

# RIGHT - prevent accidental destruction
resource "oci_database_autonomous_database" "prod" {
  lifecycle {
    prevent_destroy = true
    ignore_changes  = [defined_tags]  # Ignore tag changes from console
  }
}
```

❌ **NEVER mix regional and AD-specific resources (portability trap)**
```hcl
# WRONG - hardcoded AD breaks multi-region deployment
resource "oci_core_instance" "web" {
  availability_domain = "fMgC:US-ASHBURN-AD-1"  # Tenant-specific!
}

# RIGHT - query AD dynamically
data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

resource "oci_core_instance" "web" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
}
```

❌ **NEVER store state file in local filesystem for teams**
```hcl
# WRONG - no locking, no collaboration
terraform {
  backend "local" {}
}

# RIGHT - use OCI Object Storage with locking
terraform {
  backend "s3" {
    bucket   = "terraform-state"
    key      = "prod/terraform.tfstate"
    region   = "us-phoenix-1"
    endpoint = "https://namespace.compat.objectstorage.us-phoenix-1.oraclecloud.com"

    skip_region_validation      = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    use_path_style              = true
  }
}
```

❌ **NEVER use `count` for resources that shouldn't be replaced on reorder**
```hcl
# WRONG - reordering list recreates ALL resources
resource "oci_core_instance" "web" {
  count = length(var.instance_names)
  display_name = var.instance_names[count.index]
}

# If instance_names changes from ["web1", "web2", "web3"] to ["web0", "web1", "web2", "web3"]
# Terraform RECREATES all instances!

# RIGHT - use for_each with stable keys
resource "oci_core_instance" "web" {
  for_each = toset(var.instance_names)
  display_name = each.value
}
```

## OCI Provider Gotchas

### Authentication Hierarchy (Often Confusing)

Provider authentication precedence:
1. Explicit provider block credentials
2. `TF_VAR_*` environment variables
3. `~/.oci/config` file (DEFAULT profile)
4. Instance Principal (if `auth = "InstancePrincipal"`)

**Common mistake**: Setting environment variables but provider block overrides them silently.

### Instance Principal for Terraform on OCI Compute

```hcl
# In provider.tf
provider "oci" {
  auth   = "InstancePrincipal"
  region = var.region
}

# Dynamic group matching rule:
# "ALL {instance.compartment.id = '<compartment-ocid>'}"

# IAM policy:
# "Allow dynamic-group terraform-instances to manage all-resources in tenancy"
```

**Critical**: Instance must be in dynamic group BEFORE Terraform runs, or authentication fails with cryptic error: "authorization failed or requested resource not found"

### Resource Already Exists Errors

```
Error: 409-Conflict, Resource already exists
```

**Cause**: Resource exists in OCI but not in state file.

**Solution**:
```bash
# Import existing resource into state
terraform import oci_core_vcn.main ocid1.vcn.oc1.phx.xxxxx

# Then run plan/apply as normal
terraform plan
```

**Prevention**: Always use `terraform import` for existing infrastructure before managing with Terraform.

## State Management Anti-Patterns

### Problem: State Drift

**Symptoms**: Terraform wants to change/destroy resources that were modified outside Terraform (console, API, CLI).

**Detection**:
```bash
terraform plan  # Shows unexpected changes
terraform show  # Compare state to actual infrastructure
```

**Solutions**:

**Option 1**: Refresh state (safe)
```bash
terraform refresh  # Updates state to match reality
```

**Option 2**: Import changes (if new resources)
```bash
terraform import <resource_type>.<name> <ocid>
```

**Option 3**: Ignore changes in lifecycle
```hcl
lifecycle {
  ignore_changes = [defined_tags, freeform_tags]  # Ignore console tag edits
}
```

### Problem: State File Corruption

**Symptoms**: `terraform plan` fails with "state file corrupted" or "version mismatch"

**Recovery**:
```bash
# 1. Make backup
cp terraform.tfstate terraform.tfstate.backup

# 2. Try state repair
terraform state pull > recovered.tfstate
mv recovered.tfstate terraform.tfstate

# 3. If that fails, restore from Object Storage versioning
# Or reconstruct with imports (last resort)
```

**Prevention**: Use Object Storage backend with versioning enabled

## Resource Lifecycle Traps

### Destroy Failures (Common with Dependencies)

```
Error: Resource still in use
```

**Example**: Can't destroy VCN because subnet still exists, can't destroy subnet because instances still attached.

**Solution**:
```bash
# 1. Visualize dependencies
terraform graph | dot -Tpng > graph.png

# 2. Destroy in reverse order
terraform destroy -target=oci_core_instance.web
terraform destroy -target=oci_core_subnet.private
terraform destroy -target=oci_core_vcn.main

# Or use depends_on explicitly:
resource "oci_core_vcn" "main" {
  # ...
}

resource "oci_core_subnet" "private" {
  vcn_id = oci_core_vcn.main.id
  # depends_on is implicit via vcn_id reference
}
```

### Timeouts for Long-Running Resources

```hcl
# Database provisioning takes 15-30 minutes
resource "oci_database_autonomous_database" "prod" {
  # ... configuration ...

  timeouts {
    create = "60m"  # Default 20m often not enough
    update = "60m"
    delete = "30m"
  }
}

# Compute instance usually fast, but can timeout on capacity issues
resource "oci_core_instance" "web" {
  # ... configuration ...

  timeouts {
    create = "30m"  # Allow retries on "out of capacity"
  }
}
```

## OCI Landing Zones

**What**: Pre-built Terraform templates for enterprise OCI architectures

**Repository**: `github.com/oracle-quickstart/oci-landing-zones`

**Use when**:
- Starting new OCI tenancy (greenfield)
- Need CIS OCI Foundations Benchmark compliance
- Want security-hardened baseline
- Multi-environment (dev/test/prod) setup

**DON'T use when**:
- Brownfield (existing infrastructure) - too opinionated
- Simple single-app deployment - overkill

**Key patterns**:
- Hub-and-spoke networking
- Centralized logging/monitoring
- Security zones and bastion hosts
- IAM baseline with groups/policies

## Cost Optimization for IaC

### Use Flex Shapes (50% savings)

```hcl
# EXPENSIVE - fixed shape
resource "oci_core_instance" "web" {
  shape = "VM.Standard2.4"  # 4 OCPUs, 60GB RAM, $218/month
}

# CHEAPER - flexible shape
resource "oci_core_instance" "web" {
  shape = "VM.Standard.E4.Flex"
  shape_config {
    ocpus         = 4
    memory_in_gbs = 60
  }
  # Cost: (4 × $0.03 + 60 × $0.0015) × 730 = $153/month (30% savings)
}
```

### Tag Everything for Cost Tracking

```hcl
# Define locals for consistent tagging
locals {
  common_tags = {
    "CostCenter"  = "Engineering"
    "Environment" = var.environment
    "ManagedBy"   = "Terraform"
    "Project"     = var.project_name
  }
}

resource "oci_core_instance" "web" {
  freeform_tags = merge(
    local.common_tags,
    {
      "Component" = "WebServer"
    }
  )
}
```

**Benefit**: Cost reporting by CostCenter, Environment, Project in OCI Console

## Progressive Loading References

### OCI Terraform Patterns

**WHEN TO LOAD** [`oci-terraform-patterns.md`](references/oci-terraform-patterns.md):
- Setting up provider configuration (multi-region, auth methods)
- Resource Manager stack operations via CLI
- Common resource patterns (VCN, compute, ADB)
- State management with Object Storage backend
- Landing Zone module usage examples

**Do NOT load** for:
- Quick provider gotchas (NEVER list above)
- Understanding when to use Landing Zone (covered above)
- Lifecycle management patterns (covered above)

---

## When to Use This Skill

- Writing Terraform: provider configuration, resource dependencies, lifecycle
- State management: drift, corruption, import/export
- Troubleshooting: authentication failures, "resource already exists", destroy failures
- OCI Landing Zones: when to use, how to customize
- Cost optimization: Flex shapes, tagging strategies
- Production: prevent_destroy, ignore_changes, timeouts
