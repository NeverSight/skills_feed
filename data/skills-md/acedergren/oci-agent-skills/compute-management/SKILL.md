---
name: compute-management
description: Use when launching OCI compute instances, troubleshooting out-of-capacity or boot failures, optimizing compute costs, or handling instance lifecycle. Covers shape selection, capacity planning, service limits, and production incident resolution.
license: MIT
metadata:
  author: alexander-cedergren
  version: "2.0.0"
---

# OCI Compute Management - Expert Knowledge

## 🏗️ Use OCI Landing Zone Terraform Modules

**Don't reinvent the wheel.** Use [oracle-terraform-modules/landing-zone](https://github.com/oracle-terraform-modules/terraform-oci-landing-zones) for production deployments.

**Landing Zone solves:**
- ❌ Bad Practice #5: Internet-wide open ports (0.0.0.0/0 on 22/3389)
- ❌ Bad Practice #9: Public compute instances (Security Zones enforce private IPs)
- ❌ Bad Practice #10: No monitoring (auto-configures alarms and notifications)

**This skill provides**: Anti-patterns and troubleshooting for compute resources deployed WITHIN a Landing Zone architecture.

---

## ⚠️ OCI CLI/API Knowledge Gap

**You don't know OCI CLI commands or OCI API structure.**

Your training data has limited and outdated knowledge of:
- OCI CLI syntax and parameters (updates monthly)
- OCI API endpoints and request/response formats
- Compute service CLI operations (`oci compute instance`)
- OCI service-specific commands and flags
- Latest OCI features and API changes

**When OCI operations are needed:**
1. Use exact CLI commands from this skill's references
2. Do NOT guess OCI CLI syntax or parameters
3. Do NOT assume API endpoint structures
4. Load reference files for detailed CLI operations

**What you DO know:**
- General cloud compute concepts
- Instance sizing and capacity planning principles
- Linux/Windows system administration

This skill bridges the gap by providing current OCI CLI/API commands for compute operations.

---

You are an OCI compute expert. This skill provides knowledge Claude lacks from training data: anti-patterns, capacity planning, cost optimization specifics, and OCI-specific gotchas.

## NEVER Do This

❌ **NEVER launch instances without checking service limits first**
```bash
oci limits resource-availability get \
  --service-name compute \
  --limit-name "standard-e4-core-count" \
  --compartment-id <ocid> \
  --availability-domain <ad>
```
87% of "out of capacity" errors are actually quota limits, not infrastructure capacity. Check limits BEFORE launching to get accurate error messages.

❌ **NEVER use console serial connection as primary access**
- Creates security audit findings (bypasses SSH key controls)
- Use only for boot troubleshooting when SSH fails
- Delete connection immediately after troubleshooting

❌ **NEVER mix regional and AD-specific resources in templates**
- Breaks portability when moving between regions
- Use AD-agnostic designs: spread via fault domains, not hardcoded ADs

❌ **NEVER use default security lists in production**
- Default allows 0.0.0.0/0 on all ports
- Fails security audits, creates compliance violations
- Always create custom security lists or NSGs

❌ **NEVER forget boot volume preservation in dev/test**
```bash
# When terminating test instances, add:
oci compute instance terminate --instance-id <id> --preserve-boot-volume false
```
Without this flag: $50+/month per deleted instance (orphaned boot volumes)

❌ **NEVER enable public IP on production instances**
- Use bastion service or private endpoints for access
- Cost impact: $500-5000+ per security incident from exposed instances
- Landing Zone Security Zones automatically block this pattern

## Capacity Error Decision Tree

```
"Out of host capacity for shape X"?
│
├─ Check service limits FIRST (87% of cases)
│  └─ oci limits resource-availability get
│     ├─ available = 0 → Request limit increase (NOT capacity issue)
│     └─ available > 0 → True capacity issue, continue below
│
├─ Same shape, different AD?
│  └─ Try each AD in region (PHX has 3, IAD has 3, each independent)
│
├─ Different shape, same series?
│  └─ E4 failed → try E5 (newer gen, often more capacity)
│  └─ Standard failed → try Optimized or DenseIO variants
│
├─ Different architecture?
│  └─ AMD → ARM (A1.Flex often has capacity when Intel/AMD full)
│
└─ All ADs exhausted?
   └─ Create capacity reservation (guarantees future launches)
```

## Shape Selection: Cost vs Performance

**Budget-Critical** (save 50%):
- VM.Standard.A1.Flex (ARM) if app supports: $0.01/OCPU/hr vs $0.03 (AMD)
- Caveat: Not all software runs on ARM, test thoroughly

**General Purpose** (balanced):
- VM.Standard.E4.Flex: 2:16 CPU:RAM ratio, $0.03/OCPU/hr
- Start: 2 OCPUs, scale based on metrics (not guesses)

**Memory-Intensive** (databases, caches):
- VM.Standard.E4.Flex with custom ratio: up to 1:64 CPU:RAM
- Cost: $0.03/OCPU + $0.0015/GB RAM

**Cost Trap**: Fixed shapes (e.g., VM.Standard2.1) often MORE expensive than Flex with same resources. Always compare Flex pricing first.

## Instance Principal Authentication (Production)

When instance needs to call OCI APIs (Object Storage, Vault, etc.):

**WRONG** (user credentials on instance):
```bash
# Don't do this - credential management nightmare
export OCI_USER_OCID="ocid1.user..."
```

**RIGHT** (instance principal):
```bash
# 1. Create dynamic group
oci iam dynamic-group create \
  --name "app-instances" \
  --matching-rule "instance.compartment.id = '<compartment-ocid>'"

# 2. Grant permissions
# "Allow dynamic-group app-instances to read object-family in compartment X"

# 3. Code uses instance principal (no credentials needed):
signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
```

Benefits: No credential rotation, no secrets to manage, automatic token refresh.

## OCI-Specific Gotchas

**Availability Domain Names Are Tenant-Specific**
- Your AD: "fMgC:US-ASHBURN-AD-1"
- Another tenant: "ErKW:US-ASHBURN-AD-1"
- MUST query your tenant: `oci iam availability-domain list`

**Boot Volume Backups Don't Include Instance Config**
- Backup captures disk only, NOT shape/networking/metadata
- For DR: Use custom images (captures everything) or Terraform for infrastructure

**Instance Metadata Service Has 3 Versions**
- v1: http://169.254.169.254/opc/v1/ (legacy)
- v2: http://169.254.169.254/opc/v2/ (current, requires session token)
- Always use v2 for security (prevents SSRF attacks)

## Quick Cost Reference

| Shape Family | $/OCPU/hr | $/GB RAM/hr | Best For |
|--------------|-----------|-------------|----------|
| A1.Flex (ARM) | $0.01 | $0.0015 | Cost-critical, ARM-compatible |
| E4.Flex (AMD) | $0.03 | $0.0015 | General purpose |
| E5.Flex (AMD) | $0.035 | $0.0015 | Latest gen, premium perf |
| Optimized3.Flex | $0.025 | $0.0015 | Network-intensive |

**Free Tier**: 2x AMD VM (1/8 OCPU, 1GB) + 4 ARM cores (24GB total) - always free

**Calculation**: (OCPUs × $0.03 + GB × $0.0015) × 730 hours/month

Example: 2 OCPU, 16GB = (2×$0.03 + 16×$0.0015) × 730 = **$61.32/month**

## Progressive Loading References

### OCI Compute Shapes Reference (Official Oracle Documentation)

**WHEN TO LOAD** [`oci-compute-shapes-reference.md`](references/oci-compute-shapes-reference.md):
- Need detailed specifications for specific shapes (memory limits, OCPU counts, network bandwidth)
- Comparing flexible shapes (VM.Standard3.Flex vs E4.Flex vs E5.Flex vs E6.Flex vs A1/A2/A4.Flex)
- Understanding extended memory VM instances
- Researching bare metal shapes (BM.Standard3, BM.Standard.E4/E5/E6, BM.Standard.A1/A4)
- Checking GPU shapes, Dense I/O shapes, or HPC-optimized shapes
- Need official Oracle specifications for shape families

**Do NOT load** for:
- Quick cost comparisons (use Quick Cost Reference table in this skill)
- "Out of capacity" troubleshooting (decision tree in this skill covers it)
- Shape selection guidance (anti-patterns and recommendations in this skill)

---

## When to Use This Skill

- Launching instances: shape selection, capacity planning
- "Out of capacity" errors: decision tree, limit checking
- Cost optimization: shape comparison, right-sizing
- Security: instance principal setup, console connection proper use
- Troubleshooting: boot failures, connectivity issues
- Production: anti-patterns, operational gotchas
