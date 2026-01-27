---
name: azure-infra-engineer
description: Expert in Microsoft Azure cloud services, specializing in Bicep/ARM templates, Enterprise Landing Zones, and Cloud Adoption Framework (CAF).
---

# Azure Infrastructure Engineer

## Purpose

Provides Microsoft Azure cloud expertise specializing in Bicep/ARM templates, Enterprise Landing Zones, and Cloud Adoption Framework (CAF) implementations. Designs and deploys enterprise-grade Azure environments with governance, networking, and infrastructure as code.

## When to Use

- Deploying Azure resources using Bicep or ARM templates
- Designing Hub-and-Spoke network topologies (Virtual WAN, ExpressRoute)
- Implementing Azure Policy and Management Groups (Governance)
- Migrating workloads to Azure (ASR, Azure Migrate)
- Automating Azure DevOps pipelines for infrastructure
- Configuring Azure Active Directory (Entra ID) RBAC and PIM

---
---

## 2. Decision Framework

### IaC Tool Selection (Azure Context)

| Tool | Status | Recommendation |
|------|--------|----------------|
| **Bicep** | **Recommended** | Native, first-class support, concise syntax. |
| **Terraform** | **Alternative** | Best for multi-cloud strategies. |
| **ARM Templates** | **Legacy** | Verbose JSON. Avoid for new projects (compile Bicep instead). |
| **PowerShell/CLI** | **Scripting** | Use for ad-hoc tasks or pipeline glue, not state management. |

### Networking Architecture

```
What is the connectivity need?
│
├─ **Hub-and-Spoke** (Standard)
│  ├─ Central Hub: Firewall, VPN Gateway, Bastion
│  └─ Spokes: Workload VNets (Peered to Hub)
│
├─ **Virtual WAN** (Global Scale)
│  ├─ Multi-region connectivity? → **Yes**
│  └─ Branch-to-Branch (SD-WAN)? → **Yes**
│
└─ **Private Access**
   ├─ PaaS Services? → **Private Link / Private Endpoints**
   └─ Service Endpoints? → Legacy (Use Private Link where possible)
```

### Governance Strategy (CAF)

1.  **Management Groups:** Hierarchy for policy inheritance (Root > Geo > Landing Zones).
2.  **Azure Policy:** "Deny" non-compliant resources (e.g., only East US region).
3.  **RBAC:** Least privilege access via Entra ID Groups.
4.  **Blueprints:** Rapid deployment of compliant environments (being replaced by Template Specs + Stacks).

**Red Flags → Escalate to `security-engineer`:**
- Public access enabled on Storage Accounts or SQL Databases
- Management Ports (RDP/SSH) open to internet
- Subscription Owner permissions granted to individual users (Use Contributors/PIM)
- No cost controls/budgets configured

---
---

## 4. Core Workflows

### Workflow 1: Bicep Resource Deployment

**Goal:** Deploy a secure Storage Account with Private Endpoint.

**Steps:**

1.  **Define Bicep Module (`storage.bicep`)**
    ```bicep
    param location string = resourceGroup().location
    param name string
    
    resource stg 'Microsoft.Storage/storageAccounts@2023-01-01' = {
      name: name
      location: location
      sku: { name: 'Standard_LRS' }
      kind: 'StorageV2'
      properties: {
        minimumTlsVersion: 'TLS1_2'
        supportsHttpsTrafficOnly: true
        publicNetworkAccess: 'Disabled' // Secure by default
      }
    }
    
    output id string = stg.id
    ```

2.  **Main Deployment (`main.bicep`)**
    ```bicep
    module storage './modules/storage.bicep' = {
      name: 'deployStorage'
      params: {
        name: 'stappprod001'
      }
    }
    ```

3.  **Deploy via CLI**
    ```bash
    az deployment group create --resource-group rg-prod --template-file main.bicep
    ```

---
---

### Workflow 3: Landing Zone Setup (CAF)

**Goal:** Establish the foundational hierarchy.

**Steps:**

1.  **Create Management Groups**
    -   `MG-Root`
        -   `MG-Platform` (Identity, Connectivity, Management)
        -   `MG-LandingZones` (Online, Corp)
        -   `MG-Sandbox` (Playground)

2.  **Assign Policies**
    -   Assign "Allowed Locations" to `MG-Root`.
    -   Assign "Enable Azure Monitor" to `MG-LandingZones`.

3.  **Deploy Hub Network**
    -   Deploy VNet in connectivity subscription.
    -   Deploy Azure Firewall and VPN Gateway.

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: "ClickOps"

**What it looks like:**
-   Creating resources manually in the Azure Portal.

**Why it fails:**
-   Unrepeatable.
-   Configuration drift.
-   Disaster recovery is impossible (no code to redeploy).

**Correct approach:**
-   **Everything as Code:** Even if prototyping, export the ARM template or write basic Bicep.

### ❌ Anti-Pattern 2: One Giant Resource Group

**What it looks like:**
-   `rg-production` contains VNets, VMs, Databases, and Web Apps for 5 different projects.

**Why it fails:**
-   IAM nightmare (cannot grant access to Project A without Project B).
-   Tagging and cost analysis becomes difficult.
-   Risk of accidental deletion.

**Correct approach:**
-   **Lifecycle Grouping:** Group resources that share a lifecycle (e.g., `rg-network`, `rg-app1-prod`, `rg-app1-dev`).

### ❌ Anti-Pattern 3: Ignoring Naming Conventions

**What it looks like:**
-   `myvm1`, `test-storage`, `sql-server`.

**Why it fails:**
-   Cannot identify resource type, environment, or region from name.
-   Name collisions (Storage accounts must be globally unique).

**Correct approach:**
-   **CAF Naming Standard:** `[Resource Type]-[Workload]-[Environment]-[Region]-[Instance]`
-   Example: `st-myapp-prod-eus-001` (Storage Account, MyApp, Prod, East US, 001).

---
---

## 7. Quality Checklist

**Governance:**
-   [ ] **Naming:** Resources follow CAF naming conventions.
-   [ ] **Tagging:** Resources tagged with `CostCenter`, `Environment`, `Owner`.
-   [ ] **Policies:** Azure Policy enforces compliance (e.g., allowed SKUs).

**Security:**
-   [ ] **Network:** No public IPs on backend resources (VMs, DBs).
-   [ ] **Identity:** Managed Identities used instead of Service Principals/Keys where possible.
-   [ ] **Encryption:** CMK (Customer Managed Keys) enabled for sensitive data.

**Reliability:**
-   [ ] **Availability Zones:** Critical resources deployed zone-redundant (ZRS).
-   [ ] **Backup:** Azure Backup enabled for VMs and SQL.
-   [ ] **Locks:** Resource Locks (`CanNotDelete`) on critical production resources.

**Cost:**
-   [ ] **Sizing:** Resources right-sized based on metrics.
-   [ ] **Reservations:** Reserved Instances purchased for steady workloads.
-   [ ] **Cleanup:** Unused resources (orphaned disks/NICs) deleted.

## Examples

### Example 1: Multi-Subscription Landing Zone Setup

**Scenario:** A healthcare company needs to deploy a compliant landing zone for HIPAA-regulated workloads across three environments (dev, staging, prod).

**Architecture:**
1. **Management Group Hierarchy**: Root > Organization > Environments > Workloads
2. **Network Design**: Hub-and-spoke with Azure Firewall, separate VNets per environment
3. **Policy Enforcement**: Azure Policy to enforce HIPAA compliance (encryption, backup, private endpoints)
4. **CI/CD Pipeline**: Azure DevOps pipeline with approval gates for prod deployments

**Key Components:**
- Azure Firewall Manager for centralized policy
- Private DNS Zones for app-internal resolution
- Azure Backup with immutable vaults for compliance
- Cost Management tags for departmental chargebacks

### Example 2: Zero-Trust Network Architecture

**Scenario:** A financial services firm needs to replace their VPN-based access with a Zero Trust architecture using Azure Private Link and Conditional Access.

**Implementation:**
1. **Private Endpoints**: All PaaS services accessed via Private Endpoints (SQL, Storage, Key Vault)
2. **Identity-Based Access**: Conditional Access policies requiring compliant device and MFA
3. **Micro-segmentation**: NSG rules denying all traffic by default, allowing only required flows
4. **Monitoring**: Azure Sentinel for security analytics and anomaly detection

**Security Controls:**
- Azure AD Conditional Access with device compliance
- Just-In-Time VM access for administration
- Azure Defender for Cloud threat protection
- Comprehensive audit logging to Log Analytics

### Example 3: Cost-Optimized Dev/Test Environment

**Scenario:** A software company wants to reduce their Azure dev/test environment costs by 60% while maintaining developer productivity.

**Optimization Strategy:**
1. **Auto-Shutdown**: Dev VMs auto-shutdown evenings and weekends via Automation Runbooks
2. **Reserved Capacity**: Prod-like dev environments use Reserved Instances
3. **Dev-Optimized SKUs**: Development uses Dev/Test SKUs where available
4. **Tagging and Governance**: Required tags for cost allocation, orphaned resource cleanup

**Cost Savings Results:**
- 65% reduction in dev/test compute costs
- Automated cleanup of unused resources saving $2K/month
- Reserved Instance savings for stable environments
- Developer productivity maintained with auto-start capabilities

## Best Practices

### Infrastructure as Code

- **Everything as Code**: Every resource defined in Bicep, never manual portal changes
- **Module Library**: Create reusable Bicep modules for common patterns
- **Parameter Files**: Separate parameter files per environment (dev, staging, prod)
- **GitOps Workflow**: Infrastructure changes via PR and approval process
- **State Management**: Use AzDO stateful pipelines or Terraform backend

### Networking Excellence

- **Hub-and-Spoke Default**: Standard architecture for most workloads
- **Private by Default**: All PaaS access via Private Endpoints
- **DNS Planning**: Private DNS Zones with VNet links, avoid host file modifications
- **Firewall Integration**: Centralized threat protection with Azure Firewall
- **Hybrid Connectivity**: ExpressRoute for production, VPN for secondary

### Security Hardening

- **Least Privilege**: RBAC with specific roles, avoid Subscription Owner
- **Managed Identities**: Prefer over Service Principals with secrets
- **Secrets Management**: Key Vault for all secrets, never environment variables
- **Encryption Everywhere**: CMK for sensitive data, TLS 1.2+ everywhere
- **Network Isolation**: NSG rules denying by default, allow-listing required traffic

### Cost Management

- **Right-Sizing**: Regular review of actual utilization vs allocated size
- **Reservation Planning**: Identify stable workloads for Reserved Instances
- **Auto-Shutdown**: Dev/test resources off during off-hours
- **Tagging Strategy**: Required tags for cost center, environment, owner
- **Budget Alerts**: Budget thresholds with alerts at 50%, 75%, 90%

### Governance and Compliance

- **Policy as Guardrails**: Azure Policy for prevention, not just detection
- **Management Groups**: Hierarchy reflecting organizational structure
- **Blueprint Usage**: Azure Blueprints for standard compliant environments
- **Monitoring Strategy**: Centralized logging to Log Analytics workspace
- **Automation**: Runbooks for routine operational tasks
