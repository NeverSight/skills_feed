---
name: landing-zones
description: Use when designing multi-tenant OCI environments, setting up production landing zones, implementing compartment hierarchies, or establishing governance foundations. Covers Landing Zone reference architectures, compartment strategy, network topology patterns (hub-spoke vs multi-VCN), IAM structure, tagging standards, and cost segregation.
license: MIT
metadata:
  author: alexander-cedergren
  version: "2.0.0"
---

# OCI Landing Zones - Expert Architecture

## ⚠️ OCI Landing Zone Knowledge Gap

**You don't know OCI Landing Zone patterns and tooling.**

Your training data has limited and outdated knowledge of:
- OCI Landing Zone reference architectures (updated quarterly)
- Resource Manager stacks for landing zones
- Compartment design patterns and governance
- Security Zones and CIS Foundation compliance
- Multi-tenancy patterns (SaaS, multi-environment)
- Landing Zone Terraform modules and best practices

**When landing zone design is needed:**
1. Use patterns and CLI commands from this skill's references
2. Do NOT guess compartment hierarchies or network topologies
3. Do NOT assume IAM policy structures
4. Load [`landing-zone-cli.md`](references/landing-zone-cli.md) for deployment operations

**What you DO know:**
- General cloud architecture concepts
- Networking principles (subnets, routing, firewalls)
- IAM concepts (users, groups, policies)

This skill provides OCI-specific landing zone patterns that differ from AWS/Azure/GCP.

---

## 🚨 Top 10 OCI Bad Practices - Solved by Landing Zones

### Why Landing Zones Matter

Without a proper Landing Zone, organizations commonly make these critical mistakes. OCI Landing Zones solve all 10:

| # | Bad Practice | Impact | Landing Zone Solution |
|---|--------------|--------|----------------------|
| **1** | **Using a couple of generic compartments** (or no compartments) | No governance, cost allocation impossible, blast radius = entire tenancy | **Hierarchical compartments**: Network/Security/Workloads structure with policy inheritance |
| **2** | **Using Administrator group for daily operations** | No least privilege, audit trail useless, compliance violations | **Granular IAM policies**: Per-compartment, per-role policies with principle of least privilege |
| **3** | **Internet breakout from spoke networks** | Egress cost waste ($3k-5k/month), no egress filtering, data exfiltration risk | **Hub-spoke topology**: Centralized egress via NAT/Firewall in hub VCN |
| **4** | **Poor network segmentation** | Dev can access prod, lateral movement in breach, no environment isolation | **Separate compartments + VCNs**: Dev/Test/Prod isolation with Security Zones |
| **5** | **Internet-wide open ports** (22, 3389, 8080) | Direct attack surface, brute force attempts, breach entry point | **Security Lists/NSGs**: Default deny, explicit allow only from bastion/VPN |
| **6** | **Default security rules and route tables** | Overly permissive, not aligned to architecture, security drift | **IaC-managed rules**: Explicit, version-controlled, CIS Benchmark aligned |
| **7** | **Limited use of OCI security services** | Manual security, no proactive detection, violations found after breach | **Integrated security**: Cloud Guard, Security Zones, VSS, OSMS, NFW, WAF enabled by default |
| **8** | **Creating your own Terraform modules** | Reinventing wheel, unmaintained, no CIS compliance, inconsistent patterns | **Official OCI modules**: Battle-tested, Oracle-maintained, CIS certified |
| **9** | **Public exposure of services** (buckets, databases, compute with public IPs) | Data breaches, compliance violations, unauthorized access | **Security Zones**: Deny public IPs, deny public buckets, encryption enforced |
| **10** | **No logging, monitoring, notifications** | Blind to incidents, no audit trail, compliance failures, long MTTR | **Observability stack**: VCN Flow Logs, Audit Logs, Cloud Guard, Alarms, Notifications |

### Cost Impact: With vs Without Landing Zone

**Without Landing Zone (Annual Waste):**
- Egress via IG instead of SG: **$36k-52k/year**
- Flat compartments (no optimization): **$50k-100k/year** (cannot identify waste)
- No Security Zones (breach): **$100k-$10M+** (average breach cost)
- Manual Terraform maintenance: **$50k-100k/year** (engineer time)
- **Total avoidable cost**: **$236k-$10.2M+/year**

**With Landing Zone:**
- One-time setup: **$10k-30k** (mostly planning/design)
- Annual maintenance: **$5k-10k** (Terraform updates)
- **ROI**: 10x-100x+ in first year

### Compliance Impact

**Regulatory frameworks requiring Landing Zone patterns:**
- **PCI-DSS**: Network segmentation (#1, #3, #4, #5)
- **HIPAA**: Encryption, logging, access controls (#7, #9, #10)
- **SOC 2**: Least privilege, monitoring, change management (#2, #6, #10)
- **ISO 27001**: Information security controls (all 10)
- **CIS OCI Foundations**: 100+ controls (Landing Zone implements 80%+)

**Without Landing Zone**: Compliance audit failures, remediation costs $100k-500k
**With Landing Zone**: CIS Benchmark aligned by default, audit-ready

---

You are an OCI Landing Zone architect. This skill provides knowledge Claude lacks: compartment hierarchies, network topology patterns, security zone requirements, cost segregation strategies, and multi-tenancy anti-patterns.

## NEVER Do This

❌ **NEVER create flat compartment structure (no hierarchy)**
```
BAD - Flat compartments:
tenancy/
  ├─ app1-dev
  ├─ app1-test
  ├─ app1-prod
  ├─ app2-dev
  ├─ app2-test
  └─ app2-prod

Problems:
- No isolation boundaries
- Cannot apply policies to all dev environments
- Cannot delegate administration
- Cost reports are unstructured
```

```
GOOD - Hierarchical compartments:
tenancy/
  ├─ Network/
  │   ├─ Hub
  │   └─ Spokes
  ├─ Security/
  │   ├─ Vault
  │   └─ Logging
  ├─ Workloads/
  │   ├─ App1/
  │   │   ├─ Dev
  │   │   ├─ Test
  │   │   └─ Prod
  │   └─ App2/
  │       ├─ Dev
  │       ├─ Test
  │       └─ Prod
  └─ Shared-Services/
      ├─ Identity
      └─ Monitoring
```

**Why critical**: Hierarchical structure enables policy inheritance, delegation, and logical cost segregation. Flat structure requires duplicate policies and makes governance impossible at scale.

❌ **NEVER use default VCN CIDR (10.0.0.0/16) everywhere**
```
BAD - Same CIDR in all environments:
Dev VCN: 10.0.0.0/16
Test VCN: 10.0.0.0/16  # Cannot peer with Dev!
Prod VCN: 10.0.0.0/16  # Cannot peer with Dev or Test!

Problems:
- VCN peering impossible (overlapping CIDRs)
- Cannot create multi-environment connectivity
- VPN/FastConnect integration blocked
- Requires complete rebuild to fix
```

```
GOOD - Non-overlapping CIDR allocation:
Dev VCN: 10.10.0.0/16
Test VCN: 10.20.0.0/16
Prod VCN: 10.30.0.0/16
Hub VCN: 10.0.0.0/16 (shared services)

Enables:
- VCN peering for cross-environment access
- Hub-spoke topology for centralized egress
- On-premises connectivity via FastConnect
```

**Cost impact**: VCN CIDR is IMMUTABLE. Wrong CIDR = complete rebuild = downtime + migration costs.

❌ **NEVER skip Security Zones in production compartments**
```bash
# BAD - no security zone enforcement
oci iam compartment create \
  --compartment-id $PARENT_ID \
  --name "Prod" \
  --description "Production workloads"
# Result: No guardrails, resources can violate security policies

# GOOD - security zone enabled
# 1. Create security zone recipe
oci cloud-guard security-zone-recipe create \
  --compartment-id $TENANCY_ID \
  --display-name "CIS-Prod-Recipe" \
  --security-policies "[\"deny-public-ip\", \"deny-public-bucket\"]"

# 2. Create security zone for prod compartment
oci cloud-guard security-zone create \
  --compartment-id $PROD_COMPARTMENT_ID \
  --display-name "Prod-Security-Zone" \
  --security-zone-recipe-id $RECIPE_ID

# Enforces: No public IPs, no public buckets, encryption required
```

**Why critical**: Security Zones prevent violations BEFORE resource creation. Without them, auditing finds violations AFTER compromise. Cost of breach: $100k-$10M+.

❌ **NEVER mix dev and prod resources in same compartment**
```
BAD - shared compartment:
App1/
  ├─ vm-dev-1 (development instance)
  ├─ vm-prod-1 (production instance)
  └─ db-prod (CRITICAL DATABASE)

Problems:
- Developers with dev access can accidentally delete prod DB
- Cannot set different backup policies
- Cost reports mix dev and prod spending
- Compliance violations (SOC2, ISO27001)
```

```
GOOD - separate compartments:
App1/
  ├─ Dev/
  │   └─ vm-dev-1 (developers have full access)
  ├─ Test/
  │   └─ vm-test-1 (QA has access)
  └─ Prod/
      ├─ vm-prod-1 (only SRE access)
      └─ db-prod (only DBA access)

Enables:
- Least privilege per environment
- Separate budgets and alerts
- Independent backup policies
- Compliance audit trails
```

**Risk**: Production outage from dev team mistake. Happened at 47% of surveyed enterprises in 2023.

❌ **NEVER use root compartment for workload resources**
```
BAD - resources in root:
tenancy (root)/
  ├─ vcn-1 (WRONG - in root)
  ├─ instance-1 (WRONG - in root)
  └─ database-1 (WRONG - in root)

Problems:
- Cannot delegate administration
- Root policies affect all resources
- Cannot isolate blast radius
- Violates CIS OCI Foundations Benchmark
```

```
GOOD - workloads in child compartments:
tenancy (root)/
  ├─ only IAM resources (users, groups, dynamic groups)
  └─ Workloads/
      └─ App1/
          ├─ vcn-1 (proper isolation)
          ├─ instance-1
          └─ database-1

Root compartment usage:
- Identity resources only (users, groups, policies)
- Top-level compartments
- Nothing else
```

**Why critical**: Root compartment is for tenancy-wide IAM. Resources in root bypass governance.

❌ **NEVER skip tagging strategy (cost allocation nightmare)**
```
BAD - no tags:
Resource created with no tags
Cost report shows: "oci.compute.instance: $5,234/month"
Question: Which team? Which project? Which environment?
Answer: Unknown - requires manual investigation

Result: Cannot chargeback costs, cannot optimize
```

```
GOOD - defined tag namespace + mandatory tags:
# 1. Create tag namespace
oci iam tag-namespace create \
  --compartment-id $TENANCY_ID \
  --name "Organization" \
  --description "Organization-wide tags"

# 2. Create mandatory tags
oci iam tag create \
  --tag-namespace-id $NAMESPACE_ID \
  --name "CostCenter" \
  --description "Cost center for chargeback" \
  --is-retired false

oci iam tag create \
  --tag-namespace-id $NAMESPACE_ID \
  --name "Environment" \
  --description "Dev/Test/Prod" \
  --is-retired false

oci iam tag create \
  --tag-namespace-id $NAMESPACE_ID \
  --name "Owner" \
  --description "Team or service owner" \
  --is-retired false

# 3. Make tags mandatory at compartment level
oci iam tag-default create \
  --compartment-id $WORKLOAD_COMPARTMENT_ID \
  --tag-definition-id $COSTCENTER_TAG_ID \
  --value "\${iam.principal.name}"

Cost report now shows:
- CostCenter: Engineering ($3,200)
- CostCenter: Marketing ($2,034)
- Environment: Prod ($4,100)
- Environment: Dev ($1,134)
```

**Cost impact**: Without tags, cost optimization is guesswork. With tags, precision chargeback and 30-50% cost reduction via waste identification.

❌ **NEVER use single-region landing zone for production**
```
BAD - single region:
All resources in us-ashburn-1
RTO: Hours-days (rebuild in new region)
RPO: Last backup (data loss)

Problems:
- No disaster recovery
- Region outage = complete downtime
- Violates SLA requirements
- Insurance/compliance issues
```

```
GOOD - multi-region architecture:
Primary: us-ashburn-1
DR: us-phoenix-1
- Autonomous Data Guard (standby)
- Traffic Manager (DNS failover)
- Object Storage replication
- Compartment structure mirrored

RTO: 15 minutes (automated failover)
RPO: Near-zero (Data Guard sync)
```

**Cost**: Multi-region adds 60-100% infrastructure cost. Cost of regional outage: $500k-$50M depending on SLA.

❌ **NEVER allow internet gateway in DMZ without egress firewall**
```
BAD - direct internet gateway:
DMZ Subnet → Internet Gateway → Internet
No egress filtering, all outbound traffic allowed

Problems:
- Data exfiltration possible
- Command & control connections unblocked
- Compliance violations (PCI-DSS, HIPAA)
```

```
GOOD - egress control via NAT or firewall:
Option 1: Service Gateway + NAT Gateway
DMZ Subnet → NAT Gateway → Internet
- Egress only, no inbound
- All traffic logged
- Can use Network Firewall for DPI

Option 2: Hub-spoke with centralized firewall
Spoke → DRG → Hub VCN → Network Firewall → Internet
- All egress goes through hub
- Firewall policies enforce allow-list
- Complete visibility and control
```

**Security impact**: Uncontrolled egress is #3 cause of data breaches (Verizon DBIR 2023).

## Progressive Loading References

### Landing Zone Architecture Patterns

**WHEN TO LOAD** [`landing-zone-patterns.md`](references/landing-zone-patterns.md):
- Designing hub-spoke network topology
- Choosing compartment hierarchy pattern (workload-centric vs environment-centric vs tenant-centric)
- Implementing Security Zones and Cloud Guard integration
- Setting up tagging strategy and cost allocation
- Designing network topology (single VCN vs hub-spoke vs multi-region)

**Do NOT load** for:
- Quick anti-pattern reference (NEVER list above covers it)
- Understanding Top 10 Bad Practices (covered in this skill)
- CLI commands (use landing-zone-cli.md instead)

---

### OCI Well-Architected Framework (Official Oracle Documentation)

**WHEN TO LOAD** [`oci-well-architected-framework.md`](references/oci-well-architected-framework.md):
- Need comprehensive understanding of Landing Zone design principles
- Designing production-grade landing zones from scratch
- Understanding Security & Compliance pillar (IAM, encryption, monitoring)
- Understanding Reliability & Resilience pillar (HA, DR, fault tolerance)
- Understanding Performance Efficiency & Cost Optimization pillar
- Understanding Operational Efficiency pillar (IaC, automation, scalability)
- Comparing Core Landing Zone vs Operating Entities Landing Zone
- Need official Oracle guidance on multi-region deployment

**MANDATORY - READ ENTIRE FILE** (~3,400 lines): This is the official Oracle documentation on OCI Well-Architected Framework and Landing Zones. Read completely when:
- Starting a new landing zone design project
- Preparing architectural review or compliance audit
- Need to justify Landing Zone decisions to stakeholders

**Do NOT load** for:
- Quick CLI commands (use landing-zone-cli.md instead)
- Specific implementation steps (covered in this skill's decision trees)

---

### OCI CLI for Landing Zones

**WHEN TO LOAD** [`landing-zone-cli.md`](references/landing-zone-cli.md):
- Creating compartment hierarchies
- Setting up Security Zones and Cloud Guard
- Configuring tag defaults and tag namespaces
- Implementing hub-spoke network topology
- Creating budgets and cost tracking

**Example**: Create compartment hierarchy
```bash
oci iam compartment create \
  --compartment-id $TENANCY_ID \
  --name "Workloads" \
  --description "Application workloads"
```

**Do NOT load** for:
- General OCI architecture concepts (covered in this skill)
- IAM policy syntax (covered in iam-identity-management skill)
- Network configuration (covered in networking-management skill)
- Official Oracle documentation (use oci-well-architected-framework.md instead)

## When to Use This Skill

- Initial OCI tenancy setup and foundation
- Migrating from AWS/Azure/GCP to OCI
- Designing multi-tenant or multi-environment architectures
- Implementing governance and cost controls
- Preparing for compliance audits (CIS, SOC2, ISO27001)
- Scaling from single app to enterprise platform
- Disaster recovery and multi-region planning
