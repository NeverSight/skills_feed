---
name: best-practices
description: Use when architecting OCI solutions, migrating from AWS/Azure, designing multi-AD deployments, or avoiding common OCI anti-patterns. Covers VCN sizing mistakes, Cloud Guard gotchas, free tier specifics, OCI terminology confusion, and multi-AD patterns.
license: MIT
metadata:
  author: alexander-cedergren
  version: "2.0.0"
---

# OCI Best Practices - Expert Knowledge

## 🏗️ Use OCI Landing Zone Terraform Modules

**Don't reinvent the wheel.** Use [oracle-terraform-modules/landing-zone](https://github.com/oracle-terraform-modules/terraform-oci-landing-zones) for OCI architecture.

**Landing Zone solves:**
- ❌ Bad Practice #1: Generic compartments (Landing Zone provides hierarchical Network/Security/Workloads structure)
- ❌ Bad Practice #2: Administrator for daily ops (Landing Zone enforces least-privilege IAM policies)
- ❌ Bad Practice #4: Poor network segmentation (Landing Zone implements hub-spoke topology with security zones)
- ❌ Bad Practice #8: Creating your own Terraform modules (Landing Zone provides battle-tested, Oracle-maintained, CIS-certified modules)

**This skill provides**: OCI-specific anti-patterns, architecture patterns, and operational knowledge for resources deployed WITHIN a Landing Zone.

---

## ⚠️ OCI CLI/API Knowledge Gap

**You don't know OCI CLI commands or OCI API structure.**

Your training data has limited and outdated knowledge of:
- OCI CLI syntax and parameters (updates monthly)
- OCI API endpoints and request/response formats
- OCI service-specific commands and flags
- Latest OCI features, limits, and regional availability
- CIS Benchmark requirements for OCI

**When OCI operations are needed:**
1. Use exact CLI commands from skill references
2. Do NOT guess OCI CLI syntax or parameters
3. Do NOT assume API endpoint structures
4. Reference landing-zones skill for Terraform modules

**What you DO know:**
- General cloud architecture concepts
- Security principles and compliance frameworks
- Multi-tier application design patterns

This skill bridges the gap by providing current OCI-specific patterns and anti-patterns.

---

You are an OCI architecture expert. This skill provides knowledge Claude lacks: OCI-specific anti-patterns, free tier specifics, terminology gotchas, multi-AD patterns, and differences from AWS/Azure/GCP.

## NEVER Do This

❌ **NEVER use /24 or smaller VCN CIDR (cannot expand)**
```
# WRONG - VCN too small, cannot expand later (OCI limitation)
oci network vcn create --cidr-block "10.0.0.0/24"
# Only 256 IPs total, exhausted quickly

# WRONG - copying AWS habit (/16 VPC default)
# OCI supports larger: /16 to /30

# RIGHT - start with /16, plan for growth
oci network vcn create --cidr-block "10.0.0.0/16"
# 65,536 IPs, room for 256 /24 subnets

# CRITICAL: OCI VCNs CANNOT be resized after creation
# Must create new VCN and migrate if too small
```

**Migration cost**: Recreating VCN = hours of downtime, IP changes, security rule updates

❌ **NEVER use AD-specific subnets (breaks multi-AD HA)**
```
# WRONG - subnet tied to single AD
oci network subnet create \
  --vcn-id <vcn-ocid> \
  --cidr-block "10.0.1.0/24" \
  --availability-domain "fMgC:US-ASHBURN-AD-1"  # AD-specific!

# Problem: Can't launch instances in other ADs, no HA

# RIGHT - regional subnet (works in all ADs)
oci network subnet create \
  --vcn-id <vcn-ocid> \
  --cidr-block "10.0.1.0/24"
  # No --availability-domain flag = regional
  # Instances can be in any AD in region
```

**Gotcha**: Some old OCI guides show AD-specific subnets (deprecated pattern)

❌ **NEVER confuse Security Lists vs NSGs (different use cases)**
```
OCI has TWO network security mechanisms:

Security Lists (stateful, subnet-level):
- Applied to ALL resources in subnet
- Use for: Broad rules (internet egress, DNS)
- Limit: 5 per subnet
- Changes: Affect all instances in subnet

Network Security Groups (NSG, resource-level):
- Applied to specific resources
- Use for: Granular rules (app tier → DB tier)
- Limit: 5 per resource, 120 rules per NSG
- Changes: Affect only tagged resources

# WRONG - using Security Lists for app-specific rules
Security List: Allow app-tier → database (applies to ENTIRE subnet)

# RIGHT - use NSG for app-tier resources
NSG "app-tier": Allow egress to NSG "db-tier" on port 1521
# Only instances in app-tier NSG can reach DB
```

**Best practice**: Security Lists for baseline (internet, DNS), NSGs for application-specific rules

❌ **NEVER assume single-AD deployment is acceptable (no SLA)**
```
OCI Availability Domains (ADs):
- 3 ADs per region (most regions)
- Isolated fault domains
- <1ms latency between ADs

# WRONG - all resources in single AD
All instances in AD-1 → AD failure = complete outage

# RIGHT - distribute across ADs
Production instances: AD-1, AD-2, AD-3
Load balancer: Automatically multi-AD
Database: Autonomous (auto 3-AD) or RAC (2+ nodes)

SLA impact:
Single-AD: NO SLA (OCI doesn't guarantee)
Multi-AD: 99.95% SLA
```

**Critical**: Oracle **refuses** SLA claims for single-AD deployments in regions with 3 ADs

❌ **NEVER hardcode AD names (tenant-specific)**
```
# WRONG - AD names are tenant-specific, not portable
availability_domain = "fMgC:US-ASHBURN-AD-1"  # Only works in YOUR tenancy!

# Another tenant's AD name for same physical AD:
availability_domain = "xYzA:US-ASHBURN-AD-1"  # Different prefix!

# RIGHT - query AD names dynamically
data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

resource "oci_core_instance" "web" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
}
```

**Why**: OCI generates unique AD prefixes per tenant for security isolation

❌ **NEVER enable Cloud Guard auto-remediation without testing**
```
Cloud Guard = OCI threat detection + auto-response

# DANGER - auto-remediation can break production
Detector: "Public bucket detected"
Auto-remediation: Make bucket private → breaks public website!

Detector: "Security list allows 0.0.0.0/0"
Auto-remediation: Remove rule → breaks internet access!

# SAFER approach:
1. Enable detectors (read-only mode first)
2. Review findings for 1-2 weeks
3. Tune responders to avoid false positives
4. Enable auto-remediation for trusted patterns only
```

**Gotcha**: Cloud Guard enabled by default in some tenancies, can auto-break things

❌ **NEVER assume you need Oracle Linux (common misconception)**
```
OCI supports:
✓ Oracle Linux (free, optimized)
✓ Ubuntu, CentOS, Rocky Linux (free)
✓ Windows Server (BYOL or license-included)
✓ Custom images (import your own)

# WRONG assumption: "OCI = must use Oracle Linux"
Reality: Any Linux works, Ubuntu has larger community

# Cost: Oracle Linux is FREE (no license cost)
# But if team knows Ubuntu → use Ubuntu
```

**Marketing confusion**: Oracle pushes Oracle Linux, but it's not required

## OCI Always-Free Tier (Exact Limits)

**Generous permanent free tier** (no credit card trial, no expiration):

### Compute
- **2 AMD VMs**: VM.Standard.E2.1.Micro (1/8 OCPU, 1 GB RAM each)
- **4 Arm OCPUs**: VM.Standard.A1.Flex (allocate as 1×4 OCPU or 4×1 OCPU)
  - Up to 24 GB total RAM (6 GB per OCPU)
  - **Example**: Run 4× 1OCPU/6GB Arm instances free forever

### Database
- **2 Autonomous Databases**: 1 OCPU each, 20 GB storage per ADB
  - Can be ATP or ADW
  - **Limit**: 2 total per tenancy across all regions

### Storage
- **Block volumes**: 200 GB total (2× 100 GB boot volumes + custom)
- **Object storage**: 10 GB Standard tier
- **Archive storage**: 10 GB Archive tier
- **Block volume backups**: 10 GB

### Networking
- **Load balancer**: 1 flexible LB, 10 Mbps bandwidth
- **VCN**: 2 VCNs per region (free, no OCID cost)
- **Public IPv4**: 1 reserved public IP free per region

### Observability
- **Monitoring**: 1 billion data points ingested
- **Logging**: 10 GB ingested per month
- **Notifications**: 1 million emails per month

### Always-Free Gotchas

**CRITICAL limits often missed**:
```
# Gotcha 1: 2 ADB limit is TENANCY-wide, not per region
Can have: 1 ATP in Phoenix + 1 ADW in Ashburn = 2 (limit reached)
Cannot: Add 3rd ADB in any region

# Gotcha 2: Arm instances must be VM.Standard.A1.Flex only
Cannot: Use newer A2 shapes (paid only)

# Gotcha 3: Free tier != trial credits
Free tier: Permanent, no expiration
Trial: $300 credit for 30 days (separate)

# Gotcha 4: Stopped ADB counts toward 2 ADB limit
To free slot: Must DELETE ADB, not just STOP
```

## OCI Terminology vs AWS/Azure

Migrating from AWS/Azure? **Terminology traps**:

| OCI Term | AWS Equivalent | Azure Equivalent |
|----------|---------------|------------------|
| **VCN** | VPC | Virtual Network |
| **Subnet** | Subnet | Subnet |
| **Security List** | VPC Security Group | NSG (network-level) |
| **NSG** | Security Group | Application Security Group |
| **DRG** | Virtual Private Gateway | VPN Gateway |
| **Compartment** | Resource Group / OU | Resource Group |
| **Tenancy** | Account | Subscription |
| **Region** | Region | Region |
| **AD (Availability Domain)** | Availability Zone | Availability Zone |
| **Fault Domain** | (within AZ) | Availability Set |
| **Dynamic Group** | IAM Role (for instances) | Managed Identity |
| **Instance Principal** | EC2 Instance Profile | Managed Identity |
| **OCIR** | ECR | Container Registry |
| **OKE** | EKS | AKS |

**Critical difference**: OCI has **both** Security Lists (subnet) **and** NSGs (resource). AWS only has Security Groups (resource-level).

## Multi-AD Architecture Patterns

**OCI multi-AD specifics**:

### AD Distribution Strategy

```
OCI Regions with 3 ADs (most regions):
- US: Phoenix, Ashburn
- UK: London
- DE: Frankfurt
- AU: Sydney, Melbourne

Pattern: Distribute instances across all 3 ADs

AD-1: Web tier (2 instances) + DB primary
AD-2: Web tier (2 instances) + DB standby
AD-3: Web tier (2 instances) + DB standby

Load Balancer: Automatically spans ADs
```

**Gotcha**: Some shapes only available in specific ADs (check first)

```bash
# Check shape availability by AD
oci compute shape list \
  --compartment-id <ocid> \
  --availability-domain "fMgC:US-ASHBURN-AD-1"
```

### Fault Domain Additional Layer

Within each AD, OCI has **Fault Domains** (FD):
- 3 FDs per AD
- Separate power, cooling, network
- <1ms latency within AD

```
Best practice: Spread instances across ADs AND FDs

AD-1:
  FD-1: Web instance 1
  FD-2: Web instance 2
  FD-3: Web instance 3

AD-2:
  FD-1: Web instance 4
  (repeat pattern)

Protection:
- AD failure: 2 ADs survive (66% capacity)
- FD failure: Only 1 instance affected (16% capacity)
```

**When to use FDs**: Only for extra-critical apps (adds complexity)

## Compartment Strategy Best Practices

**Compartment hierarchy** (OCI-specific IAM boundary):

```
Root Compartment (tenancy)
│
├─ SharedServices (networking, security)
│  ├─ Network (VCNs, DRGs)
│  └─ Security (Vault, KMS, Cloud Guard)
│
├─ Production
│  ├─ App1
│  │  ├─ Compute
│  │  ├─ Database
│  │  └─ Storage
│  └─ App2
│
├─ NonProduction
│  ├─ Development
│  ├─ Testing
│  └─ Staging
│
└─ Sandbox (developers, auto-cleanup)
```

**Key principles**:
1. **Billing separation**: Compartment tags enable cost reporting by environment
2. **IAM boundaries**: Policies scoped to compartments (least privilege)
3. **Quota isolation**: Separate limits per compartment
4. **Lifecycle**: Delete entire compartment = deletes all resources inside

**Anti-pattern**: Flat structure with no hierarchy (AWS account-per-env habit)

## Cost Optimization OCI-Specific

### Flex Shape Savings (Unique to OCI)

```
Fixed shapes (legacy):
VM.Standard2.4: 4 OCPUs, 60 GB RAM, $218/month

Flex shapes (right-size RAM independently):
VM.Standard.E4.Flex: 4 OCPUs, 16 GB RAM, $109/month (50% savings)

Flex advantage: Pay only for RAM you need
- 1 OCPU = 1-64 GB RAM configurable
- Most apps don't need 15GB per OCPU (fixed ratio)
```

**Migration**: Replace fixed shapes with Flex for 30-50% savings

### Arm Instance Savings (Generous Free Tier)

```
AMD instance: VM.Standard.E4.Flex (1 OCPU) = $0.03/hr
Arm instance: VM.Standard.A1.Flex (1 OCPU) = $0.01/hr (67% cheaper)

Always-Free Arm: 4 OCPUs free forever!

Use case: Web servers, CI/CD runners, dev environments
Limitation: ARM64 only (not all apps compatible)
```

**Gotcha**: Free tier is A1 shapes only, newer A2 shapes are paid

### Storage Tiering (Exact Prices)

| Tier | Cost/GB/Month | Use Case | Retrieval |
|------|--------------|----------|-----------|
| **Standard** | $0.0255 | Active data, frequent access | Instant, free |
| **Infrequent Access** | $0.0125 (51% off) | Backups, logs (accessed monthly) | Instant, $0.01/GB |
| **Archive** | $0.0024 (91% off) | Compliance, long-term retention | 1 hour, $0.01/GB |

**Lifecycle policy example**:
```
Day 0-30: Standard ($0.0255/GB/mo)
Day 31-90: Infrequent ($0.0125/GB/mo)
Day 91+: Archive ($0.0024/GB/mo)

1 TB data for 1 year:
Without tiering: $0.0255 × 1000 × 12 = $306/year
With tiering: $0.0255 × 1000 × 1 + $0.0125 × 1000 × 2 + $0.0024 × 1000 × 9 = $72/year
Savings: $234/year (76%)
```

## Security Zones (OCI-Unique)

**OCI Security Zones** = Infrastructure-level policy enforcement:

```
Security Zone enforces:
✓ All storage encrypted
✓ No public buckets
✓ No internet gateways in VCN
✓ All databases private endpoint only
✓ Cloud Guard enabled

Enforcement: API rejects violating requests (preventive, not detective)

Example:
oci os bucket create --public-access-type ObjectRead
→ FAILS if compartment is in Security Zone

Use case: Production, PCI-DSS, healthcare (mandatory controls)
```

**Gotcha**: Security Zones can break existing automation (test in dev first)

## Progressive Loading References

### OCI Well-Architected Checklist

**WHEN TO LOAD** [`oci-well-architected-checklist.md`](references/oci-well-architected-checklist.md):
- Running compliance checks against OCI tenancy
- Preparing for CIS OCI Foundations Benchmark audit
- Implementing automated security scanning
- Creating remediation scripts for common findings
- Setting up monitoring for drift detection

**Do NOT load** for:
- Quick anti-pattern reference (NEVER list above covers it)
- Architecture decisions (covered in this skill)
- Understanding OCI terminology (tables above)

### Official Oracle Documentation Sources

**Primary References** (50+ official sources scraped):
- [Well-Architected Framework for OCI](https://docs.oracle.com/en/solutions/oci-best-practices/)
- [OCI Architecture Center](https://docs.oracle.com/en/solutions/)
- [CIS OCI Foundations Benchmark](https://www.cisecurity.org/benchmark/oracle_cloud)
- [Security Best Practices](https://docs.oracle.com/en-us/iaas/Content/Security/Reference/security_best_practices.htm)
- [Compartment Design](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.htm)
- [Network Architecture Patterns](https://docs.oracle.com/en/solutions/oci-best-practices/)

**Note**: All anti-patterns, terminology mappings, and Always-Free limits in this skill are derived from official Oracle documentation and A-Team Oracle blog

---

## When to Use This Skill

- Architecture design: Multi-AD patterns, compartment strategy, VCN sizing
- Migration from AWS/Azure: Terminology mapping, anti-pattern avoidance
- Cost optimization: Free tier planning, Flex shapes, storage tiering
- Security: Cloud Guard tuning, Security Zones, NSG vs Security Lists
- Production readiness: SLA requirements, HA patterns, fault tolerance

