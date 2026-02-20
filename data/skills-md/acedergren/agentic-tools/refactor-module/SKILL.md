---
name: refactor-module
version: 3.0.0
license: MIT
description: |
  Terraform module extraction decision framework. Use when: (1) deciding whether to
  create module vs keep inline, (2) determining module boundaries, (3) avoiding
  over-abstraction, (4) handling state migration.

  NOT a Terraform tutorial. Focuses on the refactoring decision (when to modularize,
  when to keep inline) and anti-patterns that create module sprawl.

  Triggers: terraform module, refactor terraform, module boundaries, when to create
  module, terraform abstraction, module sprawl, state migration.
metadata:
  copyright: Copyright IBM Corp. 2026
  version: "0.0.1"
---

# Terraform Module Refactoring - Decision Expert

**Assumption**: You know Terraform syntax. This covers when to modularize vs keep inline.

---

## Before Refactoring to Module: Strategic Assessment

**Ask yourself these questions BEFORE extracting a module:**

### 1. Duplication Pain Analysis
- **How many usages?**: 1-2 usages → Keep inline (wait for third), 3+ → Module candidate
- **How identical?**: <50% same config → Use locals, >80% same → Module makes sense
- **Change frequency**: Changes weekly → DON'T modularize (unstable API), Quarterly+ → Module safe
- **Scope of changes**: Entire resource → Module, Just variables → Locals sufficient

### 2. Team Readiness Assessment
- **Test coverage**: <50% coverage → TOO RISKY (breaking changes won't be caught)
- **State backup**: Is state in remote backend? Can we roll back if migration fails?
- **Consumer count**: 1-3 consumers → Easy to update, 10+ → Module change = 10 PRs
- **Documentation**: Does team know how to use `terraform state mv`? Need training first?

### 3. Cost/Benefit Analysis
- **Module overhead**: Versioning strategy + automated tests + migration docs + state migration risk
- **Duplication pain**: Inconsistent configs + bug fixes need 3+ PRs + compliance drift risk
- **Break-even point**: Module worth it when 4+ identical usages + stable API + compliance need
- **Time to value**: Simple module = 2 hours, Complex with state = 2 days planning + 4 hours execution

---

## Critical Decision: Module vs Inline

```
Considering creating a module?
│
├─ Pattern used once → DON'T modularize (keep inline)
│   └─ Wait for second usage
│      WHY: Premature abstraction harder to change
│
├─ Pattern used 2-3 times → MAYBE modularize
│   ├─ Identical config → Modularize
│   ├─ Similar but different → DON'T (use locals instead)
│   └─ Different teams using → DON'T (coordination overhead)
│
├─ Pattern used 4+ times → Modularize
│   └─ IF config is stable (not changing every sprint)
│      WHY: Module changes require updating all consumers
│
└─ Compliance/security requirement → Modularize
    └─ Enforce standards across teams
       WHY: Module = single source of truth for compliance
```

**The trap**: Over-modularization. Modules add indirection, versioning, testing overhead.

**Rule of thumb**: Resist creating modules until pain of duplication > pain of abstraction.

---

## Anti-Patterns

### ❌ #1: Leaky Abstractions
**Problem**: Module exposes 50 variables, just wrapping resources

```hcl
// ❌ WRONG - 1:1 variable mapping
module "vpc" {
  source = "./modules/vpc"

  cidr_block                           = var.cidr_block
  enable_dns_hostnames                 = var.enable_dns_hostnames
  enable_dns_support                   = var.enable_dns_support
  instance_tenancy                     = var.instance_tenancy
  enable_classiclink                   = var.enable_classiclink
  enable_classiclink_dns_support       = var.enable_classiclink_dns_support
  assign_generated_ipv6_cidr_block     = var.assign_generated_ipv6_cidr_block
  // ... 43 more variables
}

// WHY IT'S BAD: Not abstracting anything, just moving code
```

**Fix**: High-level interface
```hcl
// ✅ CORRECT - meaningful abstraction
module "vpc" {
  source = "./modules/vpc"

  network_config = {
    cidr           = "10.0.0.0/16"
    azs            = ["us-east-1a", "us-east-1b"]
    public_subnets = 2
    private_subnets = 2
  }

  // 4 variables instead of 50
}
```

**Test**: If module variables match resource arguments 1:1, it's not a real abstraction.

**Why this is deceptively hard to debug**: Module works perfectly—tests pass, terraform apply succeeds. The problem emerges slowly over months: every resource argument becomes a module variable (+50 variables), documentation becomes unwieldy (which of 50 variables do I actually need?), consumers still need to know AWS VPC internals to use the module (defeating abstraction purpose). Takes 3-6 months of maintenance hell—adding new AWS features requires module updates, version bumps, consumer migrations—before team realizes the module isn't abstracting anything, just adding indirection. By then, you have 10+ consumers and unwinding the module is more painful than living with it.

### ❌ #2: Premature Modularization
**Problem**: Create module after first usage, becomes wrong abstraction

```hcl
// First usage: Simple S3 bucket
resource "aws_s3_bucket" "data" {
  bucket = "company-data"
}

// Developer: "Let's make this a module!"
// Creates module with 1 user

// Second usage: Needs versioning
// Third usage: Needs replication
// Fourth usage: Needs lifecycle rules
// Fifth usage: Needs encryption

// Result: Module has 30 variables, nobody uses all of them
```

**Fix**: Wait for 2-3 real usages, then extract common pattern
```hcl
// After seeing 3 usages, common pattern emerges:
module "s3_bucket" {
  source = "./modules/s3"

  name = "company-data"
  type = "data" | "logs" | "artifacts"  // 3 known patterns

  // Module handles appropriate defaults per type
}
```

**Rule**: First time: inline. Second time: copy-paste. Third time: abstract.

**Why this is deceptively hard to debug**: First usage looks clean (simple S3 module, 3 variables). Second usage needs versioning (add 2 variables). Third needs replication (add 5 variables). Fourth needs lifecycle rules (add 8 variables). Each addition seems reasonable in isolation. After 6 months, module has 30 variables, 20 boolean feature flags, complex conditional logic. Nobody uses all features (each consumer uses 30% of variables). Every change risks breaking someone. The wrong abstraction was baked in early (before patterns emerged) and now refactoring requires coordinating 10+ teams. Takes 3-6 months of feature requests to realize the module grew wrong, but reversing it requires migrating all consumers—a 2-month project nobody has time for.

### ❌ #3: State Migration Nightmare
**Problem**: Refactor to module without planning state migration

```hcl
// Before: Inline resources
resource "aws_vpc" "main" { ... }
resource "aws_subnet" "private" { ... }

// After: Module
module "network" {
  source = "./modules/network"
}

// Result: Terraform wants to destroy old resources, create new ones
// State addresses changed: aws_vpc.main → module.network.aws_vpc.main
```

**Fix**: Move state before deploying
```bash
# Plan the move
terraform state list  # See current addresses

# Move resources into module
terraform state mv aws_vpc.main module.network.aws_vpc.main
terraform state mv aws_subnet.private module.network.aws_subnet.private

# Verify no changes
terraform plan  # Should show: No changes
```

**WARNING**: State moves are dangerous. Always backup state first:
```bash
terraform state pull > backup-$(date +%s).tfstate
```

**Why this is deceptively hard to debug**: NO ERROR MESSAGE. `terraform apply` shows plan to destroy VPC, create "new" VPC with identical config. Looks like Terraform bug or state corruption. You spend 20-30 minutes checking: Terraform version? Backend config? State file corrupted? The error is invisible—state addresses changed (aws_vpc.main → module.network.aws_vpc.main) but Terraform doesn't say "you moved code without moving state." It just says "resource doesn't exist in state, will create new one." Developers approve the plan thinking it's safe (identical config), then production VPC gets destroyed and recreated, taking down all services. The fix (state mv) is 2 minutes, but discovering that's the problem takes 20-30 minutes of debugging—and by then you may have already applied and caused an outage.

### ❌ #4: Module Version Hell
**Problem**: 20 consumers on different module versions, breaking changes

```hcl
// app1
module "vpc" { source = "git::...?ref=v1.0.0" }

// app2
module "vpc" { source = "git::...?ref=v1.2.0" }

// app3
module "vpc" { source = "git::...?ref=v2.0.0" }  // Breaking changes

// Need bugfix in v1.x but already on v2.x
// Result: Maintain 3 versions or force painful upgrades
```

**Fix**: Semantic versioning + deprecation period
```hcl
// v1.x: Stable, bug fixes only
// v2.x: New features, maintains v1 compatibility mode
// v3.x: Remove deprecated features

// v2 module supports both:
variable "legacy_mode" {
  default = false  // New consumers get new behavior
}

// Gives consumers 6 months to migrate
```

**Rule**: Breaking changes require major version + migration guide.

**Why this is deceptively hard to debug**: Version divergence happens slowly over weeks/months. App1 upgrades to v2.0 (works fine). App2 stays on v1.2 (no time to upgrade). App3 needs bugfix only in v1.x but you're maintaining v2.x now. Takes 2-3 weeks before pattern emerges: every module change requires checking "which versions need this fix?" You're backporting fixes to 3 versions, testing each, cutting multiple releases. CI builds slow down (testing v1.x, v2.x, v3.x). Documentation fragments (README has v1 vs v2 sections). Consumers report bugs fixed in v2 still present in v1—but they can't upgrade due to breaking changes. After 3-6 months you have 5 major versions to support, or you force painful migrations that break production apps.

---

## Decision Frameworks

### When to Extract Common Code

```
Have repeated Terraform code?
│
├─ Repeated data sources → Use locals (NOT module)
│   └─ data "aws_ami" { ... } appears 3 times
│      WHY: Data sources don't benefit from modules
│
├─ Repeated resource patterns → Check usage count
│   ├─ 1 usage → Keep inline
│   ├─ 2-3 usages → Use locals or workspaces
│   └─ 4+ usages → Consider module
│
└─ Compliance requirement → Module immediately
    └─ Must enforce security standards
       WHY: Module = single compliance enforcement point
```

### Module Boundaries

```
Where to draw module boundary?
│
├─ By lifecycle → Good boundary
│   └─ VPC (rarely changes) vs EC2 (often changes)
│      WHY: Separate change frequencies
│
├─ By team ownership → Good boundary
│   └─ Team A owns networking, Team B owns compute
│      WHY: Clear ownership and responsibility
│
├─ By technology → Bad boundary
│   └─ "Database module", "Compute module", "Network module"
│      WHY: Real apps need cross-cutting concerns
│
└─ By Terraform resource type → Bad boundary
    └─ aws_vpc module, aws_subnet module, aws_route_table module
       WHY: Too granular, loses cohesion
```

**Good module**: VPC + subnets + route tables + NAT gateway (cohesive networking unit)
**Bad module**: Just VPC (consumer has to wire up subnets manually)

---

## Module Design Patterns

### Pattern 1: Composition (Preferred)
```hcl
// Small, focused modules
module "vpc" { ... }
module "eks" {
  vpc_id = module.vpc.id  // Compose modules
}
module "rds" {
  subnet_ids = module.vpc.private_subnet_ids
}
```

**Benefit**: Mix and match, replace parts independently.

### Pattern 2: Monolithic (Avoid)
```hcl
// One module does everything
module "infrastructure" {
  // Creates VPC + EKS + RDS + everything
}
```

**Problem**: Can't replace just VPC, all-or-nothing.

**When monolithic is OK**: Compliance module that must enforce standards together.

---

## Refactoring Process

### Step 1: Identify Duplication (Don't Rush)
```bash
# Find repeated patterns
grep -r "resource \"aws_s3_bucket\"" .
# If 1-2 results: keep inline
# If 3+ results: analyze differences
```

### Step 2: Validate True Duplication
```bash
# Are configs actually identical?
diff app1/s3.tf app2/s3.tf

# If > 50% different: NOT true duplication
# Solution: locals or data sources, not module
```

### Step 3: Design Module Interface
```hcl
// ❌ WRONG - expose every resource argument
variable "acl" {}
variable "versioning" {}
variable "lifecycle_rules" {}
variable "replication" {}
// ... 20 more variables

// ✅ CORRECT - expose intent
variable "bucket_type" {
  type = string
  validation {
    condition = contains(["data", "logs", "artifacts"], var.bucket_type)
  }
}

// Module maps type to appropriate settings
```

### Step 4: Extract + Test
```bash
# Create module
mkdir -p modules/s3
mv s3.tf modules/s3/main.tf

# Test in isolation
cd modules/s3
terraform init
terraform plan -var bucket_type=data
```

### Step 5: Migrate State (Critical)
```bash
# Backup state
terraform state pull > backup.tfstate

# Move resources
terraform state mv aws_s3_bucket.data module.s3.aws_s3_bucket.main

# Verify
terraform plan  # Should show: No changes
```

---

## Error Recovery Procedures

### When State Migration Causes Destroy/Create Plan
**Recovery steps**:
1. **STOP**: Do NOT apply. Run `terraform state pull > emergency-backup.tfstate` immediately
2. **Diagnose**: Run `terraform state list` to see current addresses vs expected module addresses
3. **Fix state**: Run `terraform state mv` commands for each resource that moved into module
4. **Fallback**: If you already applied and destroyed resources, restore from backup: `terraform state push emergency-backup.tfstate`, then import destroyed resources: `terraform import module.network.aws_vpc.main vpc-xxxxx`

### When Module Has Too Many Variables (Leaky Abstraction)
**Recovery steps**:
1. **Audit usage**: Survey all consumers—which variables do they actually use? (Often 20% of variables)
2. **Identify patterns**: Group consumers by usage pattern (data buckets, log buckets, artifact buckets)
3. **Redesign interface**: Replace 50 variables with `bucket_type` enum + sensible defaults per type
4. **Fallback**: If redesign too risky, create `v2` module with clean interface, deprecate `v1` over 6 months

### When Premature Module Needs Different Features Per Consumer
**Recovery steps**:
1. **Count feature flags**: If >10 boolean toggles, module is wrong abstraction
2. **Split by usage**: Create separate modules per use case (simple-bucket, versioned-bucket, replicated-bucket)
3. **Migrate incrementally**: New consumers use new modules, old consumers stay on v1 (deprecate over time)
4. **Fallback**: If splitting too complex, add `advanced_config` escape hatch allowing raw HCL passthrough for edge cases

### When Multiple Module Versions Cause Maintenance Hell
**Recovery steps**:
1. **Audit versions**: Run `grep -r 'source.*?ref=' . | sort | uniq -c` to see version distribution
2. **Create migration path**: Write automated migration script (sed/awk) to update HCL from v1 → v2
3. **Coordinate upgrades**: Schedule "module upgrade week" where all teams migrate together
4. **Fallback**: If coordination impossible, use monorepo with workspace protocol (`source = "../../modules/vpc"`) to eliminate versions—all consumers use same code, breaking changes impossible

---

## When to Load Full Reference

**MANDATORY - READ ENTIRE FILE**: `references/state-migration.md` when:
- Migrating 5+ resources into module with complex dependencies
- Encountering 3+ state-related errors during migration (resource not found, duplicate)
- Setting up automated state migration for 10+ similar refactorings
- Need rollback procedures for failed state migration in production

**MANDATORY - READ ENTIRE FILE**: `references/module-testing.md` when:
- Module has 3+ consumers and needs automated testing
- Setting up CI/CD pipeline for module with 5+ test scenarios
- Implementing contract tests between module versions
- Need to test 10+ module input combinations

**Do NOT load references** for:
- Basic refactoring decisions (use Strategic Assessment section)
- Single resource state moves (use Error Recovery section above)
- Deciding whether to create module (use Critical Decision section)

---

## Resources

- **Official Docs**: https://developer.hashicorp.com/terraform/language/modules (for syntax)
- **This Skill**: When to modularize, module boundaries, anti-patterns
