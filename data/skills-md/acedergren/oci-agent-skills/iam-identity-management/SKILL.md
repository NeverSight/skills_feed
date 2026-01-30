---
name: iam-identity-management
description: Use when writing IAM policies, troubleshooting permission denied errors, setting up dynamic groups, or implementing IDCS integration. Covers policy syntax gotchas, principal types confusion, compartment inheritance, and common authorization failures.
license: MIT
metadata:
  author: alexander-cedergren
  version: "2.0.0"
---

# OCI IAM and Identity Management - Expert Knowledge

## 🏗️ Use OCI Landing Zone Terraform Modules

**Don't reinvent the wheel.** Use [oracle-terraform-modules/landing-zone](https://github.com/oracle-terraform-modules/terraform-oci-landing-zones) for IAM structure.

**Landing Zone solves:**
- ❌ Bad Practice #1: Flat compartments (Landing Zone provides hierarchical structure)
- ❌ Bad Practice #2: Administrator for daily ops (Landing Zone enforces least privilege)
- ❌ Bad Practice #6: Manual IAM policies (Landing Zone provides CIS-compliant IaC)

**This skill provides**: IAM syntax, troubleshooting, and policy patterns for resources deployed WITHIN a Landing Zone.

---

## ⚠️ OCI CLI/API Knowledge Gap

**You don't know OCI CLI commands or OCI API structure.**

Your training data has limited and outdated knowledge of:
- OCI CLI syntax and parameters (updates monthly)
- OCI API endpoints and request/response formats
- IAM service CLI operations (`oci iam policy`, `oci iam dynamic-group`)
- Policy verb/resource combinations (OCI-specific, not AWS/Azure)
- Latest IAM features and Identity Domains

**When OCI operations are needed:**
1. Use exact CLI commands from this skill's references
2. Do NOT guess OCI IAM policy syntax
3. Do NOT assume AWS/Azure IAM patterns work in OCI
4. Load reference files for detailed IAM policy documentation

**What you DO know:**
- General IAM concepts (principals, policies, groups)
- Role-based access control principles
- Least privilege security concepts

This skill bridges the gap by providing current OCI-specific IAM patterns and syntax.

---

You are an OCI IAM expert. This skill provides knowledge Claude lacks: policy syntax gotchas, permission troubleshooting, dynamic group patterns, and OCI-specific IAM operational knowledge.

## NEVER Do This

❌ **NEVER use overly broad policies (security risk)**
```
# WRONG - grants admin access to everyone
Allow any-user to manage all-resources in tenancy

# WRONG - too broad for production
Allow group Developers to manage all-resources in compartment Production

# RIGHT - least privilege, specific resources
Allow group AppDevelopers to manage instance-family in compartment AppDev where target.instance.name =~ 'dev-*'
```

❌ **NEVER forget compartment hierarchy in policies**
```
# WRONG - policy in child compartment can't access parent resources
Policy location: Compartment A/B/C
"Allow group X to read buckets in compartment A"  # Fails! Policy must be in A or above

# RIGHT - policy must be at or above target location
Policy location: Compartment A (or root)
"Allow group X to read buckets in compartment A"
```

❌ **NEVER mix up principal types (causes "not authorized" errors)**
```
# WRONG - instance is NOT a user
Allow user <instance-ocid> to read buckets in compartment X

# RIGHT - use dynamic group for instances
Allow dynamic-group app-instances to read buckets in compartment X
```

❌ **NEVER hardcode resource OCIDs in dynamic group rules**
```
# WRONG - not scalable, breaks when instance replaced
ALL {instance.id = 'ocid1.instance.oc1.phx.xxxxx'}

# RIGHT - use compartment or tag matching
ALL {instance.compartment.id = '<compartment-ocid>'}
ANY {instance.freeform-tags.environment = 'production'}
```

❌ **NEVER create circular policy dependencies**
```
# WRONG - Group A needs policy to manage Group B, but Group B policy grants access to Group A
# Creates deadlock where neither can be created first

# RIGHT - use separate administrative groups with clear hierarchy
```

❌ **NEVER use "any-user" in production policies (security audit failure)**
```
# WRONG - grants access to ALL users including future unknown users
Allow any-user to read buckets in tenancy

# RIGHT - explicit group membership
Allow group DataReaders to read buckets in compartment SharedData
```
Cost impact: $10,000+ per compliance violation finding in SOC2/HIPAA audits

## IAM Permission Troubleshooting

### "404 - NotAuthorizedOrNotFound"

This error means **EITHER**:
1. Resource doesn't exist, OR
2. User lacks permission to see if resource exists

**Troubleshooting decision tree**:
```
404 NotAuthorizedOrNotFound?
│
├─ Does resource definitely exist?
│  ├─ YES → Permission issue
│  │  └─ Check: Does user have 'inspect' or 'read' permission?
│  │     └─ Check: Is policy in correct compartment (at or above target)?
│  └─ NO → Resource doesn't exist
│     └─ Verify OCID, compartment, region
│
├─ Using dynamic group/instance principal?
│  └─ Check: Is instance in dynamic group?
│     └─ `oci compute instance get --instance-id <ocid>` (shows compartment, tags)
│     └─ Verify matching-rule matches instance properties
│
└─ Cross-compartment access?
   └─ Policy must be in compartment that CONTAINS both source and target
      OR in root compartment
```

### "403 - NotAuthorized"

**Clear permission denied**. User/principal identified but lacks permission.

**Common causes**:
1. **Missing verb**: Policy has `read` but action needs `use` or `manage`
2. **Wrong resource-type**: Policy grants `instance-family` but trying to access `volume-family`
3. **Condition doesn't match**: Policy has `where target.instance.name = 'prod-*'` but instance is `dev-web-1`
4. **Policy not in effect yet**: Policies take 10-60 seconds to propagate

**Verb hierarchy** (each includes permissions below):
```
inspect < read < use < manage
```

## Policy Syntax Gotchas

### Resource Type Families (Often Confused)

| Family | Includes | Common Mistake |
|--------|----------|----------------|
| `instance-family` | instances, instance-consoles, instance-console-connections, vnics, vnic-attachments | Thinking it includes volumes (it doesn't) |
| `volume-family` | volumes, volume-backups, volume-attachments | Separate from instances |
| `object-family` | buckets, objects | Objects are separate resources |
| `database-family` | db-systems, databases, autonomous-databases | Very broad |
| `all-resources` | Everything | **Use sparingly** - security risk |

### Location Syntax

```
# Compartment (specific)
in compartment <compartment-name or ocid>

# Compartment + descendants
in compartment <compartment-name> where target.compartment.id = <ocid>

# Tenancy (root)
in tenancy

# Specific resource (rare, for delegation)
in resource <resource-ocid>
```

### Conditions (WHERE clause)

```hcl
# Tag-based conditions
where target.resource.tag.environment = 'production'
where target.resource.freeform-tags.CostCenter = 'Engineering'

# Resource name patterns
where target.instance.name =~ 'web-*'  # Regex match

# Request properties
where request.operation = 'LaunchInstance'
where request.region = 'us-phoenix-1'

# Multiple conditions
where all {target.resource.tag.env = 'prod', target.compartment.name = 'AppProd'}
where any {target.instance.shape = 'VM.Standard.E4.Flex', target.instance.shape = 'VM.Standard.A1.Flex'}
```

## Dynamic Group Patterns

### Matching Rules Best Practices

**By Compartment** (most common):
```
ALL {instance.compartment.id = '<compartment-ocid>'}
```

**By Tag** (flexible):
```
ANY {instance.freeform-tags.app = 'webserver'}
```

**By Multiple Criteria** (restrictive):
```
ALL {instance.compartment.id = '<comp-ocid>', instance.freeform-tags.environment = 'production'}
```

**Common Mistake**: Using `instance.id` (specific instance) instead of `instance.compartment.id` (all instances in compartment)

### Testing Dynamic Group Membership

```bash
# 1. Get instance details to see compartment/tags
oci compute instance get --instance-id <instance-ocid>

# 2. Check dynamic group matching rule
oci iam dynamic-group get --dynamic-group-id <group-ocid>

# 3. Verify rule matches instance properties
# Example: If rule is "instance.compartment.id = X"
# Check instance's compartment_id matches X

# 4. Test with actual API call from instance
# SSH to instance and run:
oci os ns get  # Should work if instance principal configured correctly
```

## Compartment Strategy Anti-Patterns

❌ **WRONG: Flat structure (no organization)**
```
Tenancy
├─ Application1  (mix of dev/test/prod)
├─ Application2  (mix of dev/test/prod)
└─ SharedServices
```

✅ **RIGHT: Environment-based hierarchy**
```
Tenancy
├─ Production
│  ├─ App1
│  └─ App2
├─ Development
│  ├─ App1
│  └─ App2
└─ SharedServices
   ├─ Networking
   └─ Security
```

**Benefits**: Clear IAM boundaries, cost reporting by environment, blast radius containment

## Authentication Methods (When to Use Each)

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| **API Key** | Local dev, CI/CD runners outside OCI | Simple, portable | Manual rotation, key management |
| **Instance Principal** | Apps on OCI compute | No credentials, auto-rotation | Only works on OCI compute |
| **Resource Principal** | OCI Functions, Data Flow | Serverless auth | Limited to specific services |
| **Session Token** | Console federation via IDCS | SSO, MFA | Short-lived, complex setup |

## IDCS Integration Gotchas

**Federation Setup** (OCI + IDCS):
- IDCS users map to OCI via federation
- Group membership in IDCS → OCI group mapping
- **Critical**: OCI group names must match IDCS group names exactly

**Common Issues**:
- User can log in to console but can't see resources → Missing OCI IAM policy for federated group
- "Invalid credentials" → IDCS federation not configured in OCI tenancy
- Group membership doesn't sync → OCI group name doesn't match IDCS group name

## Progressive Loading References

### OCI IAM Policies Reference (Official Oracle Documentation)

**WHEN TO LOAD** [`oci-iam-policies-reference.md`](references/oci-iam-policies-reference.md):
- Need comprehensive IAM policy syntax and examples
- Writing complex policies with conditions
- Understanding service-specific verbs and permissions
- Implementing least privilege access patterns
- Troubleshooting policy evaluation order

**Do NOT load** for:
- Quick policy syntax examples (covered in this skill)
- Common permission patterns (decision trees above)
- Dynamic group rules (covered in this skill)

---

## When to Use This Skill

- Writing IAM policies: syntax, verb selection, conditions
- Troubleshooting: 403/404 errors, authorization failures, permission debugging
- Dynamic groups: matching rules, testing membership, instance principals
- Compartment strategy: hierarchy design, policy placement
- IDCS integration: federation setup, group mapping, SSO troubleshooting
