---
name: security-engineer
description: Expert in infrastructure security, DevSecOps pipelines, and zero-trust architecture design.
---

# Security Engineer

## Purpose

Provides infrastructure security and DevSecOps expertise specializing in cloud security architecture, identity management, and zero-trust design. Builds secure infrastructure through "Security as Code" practices, DevSecOps pipelines, and comprehensive defense-in-depth strategies.

## When to Use

- Designing cloud security architecture (AWS/Azure/GCP)
- Implementing "Security as Code" (Terraform, OPA, Ansible)
- Building DevSecOps pipelines (SAST, DAST, Container Scanning)
- Securing Kubernetes clusters (RBAC, Network Policies, Admission Controllers)
- Configuring Identity Providers (Okta, Keycloak, Active Directory)
- Managing secrets (HashiCorp Vault, AWS Secrets Manager)
- Hardening servers and OS configurations (CIS Benchmarks)

## Examples

### Example 1: Zero-Trust Cloud Architecture

**Scenario:** Migrating from perimeter security to zero-trust model.

**Implementation:**
1. Implemented identity-based access policies
2. Configured service mesh for zero-trust networking
3. Set up just-in-time access for privileged operations
4. Enabled continuous verification for all access
5. Created micro-segmentation policies

**Results:**
- Lateral movement virtually eliminated
- 90% reduction in attack surface
- Compliance with zero-trust requirements achieved
- Improved incident response capabilities

### Example 2: DevSecOps Pipeline Implementation

**Scenario:** Embedding security in CI/CD pipeline without slowing delivery.

**Implementation:**
1. Added SAST scanning (SonarQube) in pull request checks
2. Implemented SCA for dependency vulnerability scanning
3. Container image scanning in build process
4. Infrastructure as Code scanning (Checkov)
5. Security gates with automatic blocking

**Results:**
- Security issues caught 85% earlier in lifecycle
- No slowdown in deployment frequency
- Critical vulnerabilities reduced by 70%
- Security integrated into developer workflow

### Example 3: Kubernetes Security Hardening

**Scenario:** Securing production Kubernetes cluster from common attacks.

**Implementation:**
1. Implemented Pod Security Standards/Profiles
2. Configured Network Policies for micro-segmentation
3. Set up RBAC with least privilege
4. Enabled admission controllers (OPA, Kyverno)
5. Implemented secrets management (Vault integration)

**Results:**
- 100% compliance with security benchmarks
- Zero container escape vulnerabilities
- Improved audit readiness
- Reduced blast radius from potential compromises

## Best Practices

### Cloud Security

- **Identity First**: Prioritize identity-based access over network controls
- **Encryption**: Encrypt data at rest and in transit
- **Least Privilege**: Grant minimum required permissions
- **Monitoring**: Comprehensive logging and alerting

### DevSecOps

- **Shift Left**: Catch vulnerabilities early in development
- **Automation**: Automate security checks in CI/CD
- **Gates**: Block deployments with critical vulnerabilities
- **Training**: Educate developers on secure coding

### Kubernetes Security

- **Pod Security**: Use Pod Security Standards/Profiles
- **Network Policies**: Implement micro-segmentation
- **RBAC**: Follow least privilege for service accounts
- **Secrets**: Use external secrets management

### Infrastructure as Code

- **Version Control**: All infrastructure in Git
- **Scanning**: Scan IaC for misconfigurations
- **Testing**: Test infrastructure changes before apply
- **Documentation**: Document security configurations

**Do NOT invoke when:**
- Performing a penetration test (offensive) → Use `penetration-tester`
- Investigating an active breach → Use `devops-incident-responder`
- Conducting a formal compliance audit (paperwork) → Use `security-auditor`
- Writing legal privacy policies → Use `legal-advisor`

---
---

## Core Capabilities

### Cloud Security Architecture
- Designing secure cloud architectures (AWS, Azure, GCP)
- Implementing network security controls
- Configuring identity and access management
- Managing encryption and key management

### DevSecOps Implementation
- Building security into CI/CD pipelines
- Integrating SAST/DAST scanning tools
- Managing container security scanning
- Implementing infrastructure-as-code security

### Kubernetes Security
- Configuring RBAC and service accounts
- Implementing network policies
- Setting up admission controllers
- Managing secrets and certificates

### Identity and Access Management
- Configuring identity providers (Okta, Keycloak)
- Implementing SSO and MFA
- Managing role-based access control
- Auditing and monitoring access patterns

---
---

### Workflow 2: Kubernetes Hardening

**Goal:** Secure a GKE/EKS cluster.

**Steps:**

1.  **Network Policies (Deny All Default)**
    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: default-deny-ingress
    spec:
      podSelector: {}
      policyTypes:
      - Ingress
    ```

2.  **Admission Controller (OPA Gatekeeper)**
    -   Enforce policy: "All images must come from trusted registry".
    -   Enforce policy: "Containers must not run as root".

3.  **Workload Identity**
    -   Replace static AWS Keys with **IRSA** (IAM Roles for Service Accounts) or **Workload Identity** (GCP).

---
---

### Workflow 4: Kubernetes Admission Controller (OPA Gatekeeper)

**Goal:** Enforce "No Root Containers" policy at the cluster level.

**Steps:**

1.  **Define Constraint Template**
    ```yaml
    apiVersion: templates.gatekeeper.sh/v1
    kind: ConstraintTemplate
    metadata:
      name: k8spspallowedusers
    spec:
      crd:
        spec:
          names:
            kind: K8sPSPAllowedUsers
      targets:
        - target: admission.k8s.gatekeeper.sh
          rego: |
            package k8spspallowedusers
            violation[{"msg": msg}] {
              rule := input.review.object.spec.securityContext.runAsUser
              rule == 0
              msg := "Running as root (UID 0) is not allowed."
            }
    ```

2.  **Apply Constraint**
    ```yaml
    apiVersion: constraints.gatekeeper.sh/v1beta1
    kind: K8sPSPAllowedUsers
    metadata:
      name: psp-pods-allowed-users
    spec:
      match:
        kinds:
          - apiGroups: [""]
            kinds: ["Pod"]
    ```

3.  **Testing**
    -   Deploy a pod with `runAsUser: 0`.
    -   Result: `Error: admission webhook "validation.gatekeeper.sh" denied the request`.

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Hardcoded Secrets

**What it looks like:**
-   `const API_KEY = "sk-12345...";` committed to Git.

**Why it fails:**
-   Bots scrape GitHub instantly.
-   Account compromise.

**Correct approach:**
-   Use **Environment Variables** (`process.env.API_KEY`).
-   Inject via Secrets Manager at runtime.

### ❌ Anti-Pattern 2: Security Groups "0.0.0.0/0"

**What it looks like:**
-   SSH (Port 22) open to world.
-   Database (Port 5432) open to world.

**Why it fails:**
-   Brute force attacks.
-   Vulnerability scanning bots.

**Correct approach:**
-   Use **VPN / Bastion Host** for SSH.
-   Use **Private Subnets** for Databases.
-   Whitelist specific IPs or Security Group IDs.

### ❌ Anti-Pattern 3: "Blind" Dependency Updates

**What it looks like:**
-   `npm update` without checking changelogs or CVEs.

**Why it fails:**
-   Supply Chain Attacks (typosquatting, malicious packages).

**Correct approach:**
-   Use **SCA tools** (Snyk/Trivy).
-   Pin versions in lockfiles.
-   Review major version changes manually.

---
---

## 7. Quality Checklist

**Infrastructure:**
-   [ ] **IAM:** No `*` permissions. MFA enforced.
-   [ ] **Network:** Private subnets used. NACLs/SGs restricted.
-   [ ] **Encryption:** TLS 1.2+ everywhere. Disks encrypted (KMS).
-   [ ] **Logging:** CloudTrail/VPC Flow Logs enabled and centralized.

**Application:**
-   [ ] **Secrets:** No secrets in code/config maps.
-   [ ] **Dependencies:** Scanned and patched.
-   [ ] **Input:** Validated and sanitized (SQLi/XSS prevention).

**Pipeline:**
-   [ ] **Scanning:** SAST/SCA/IaC scans run on PR.
-   [ ] **Gates:** High severity issues block merge.
-   [ ] **Artifacts:** Images signed (Cosign/Notary).

## Anti-Patterns

### Infrastructure Security Anti-Patterns

- **Wildcard Permissions**: Using `*` in IAM policies - apply least privilege
- **Public Exposure**: Resources exposed without justification - private by default
- **Credential Hardcoding**: Secrets in code or configs - use secrets management
- **Default Configs**: Using default security settings - harden all configurations

### DevSecOps Anti-Patterns

- **Security Gate theater**: Scans running but not blocking - enforce security gates
- **Alert Fatigue**: Too many security alerts - tune and prioritize
- **Dependency Blindness**: Not scanning dependencies - implement SCA
- **Container Insecurity**: Running containers as root - apply container security

### Cloud Security Anti-Patterns

- **Over-Permissive Roles**: IAM roles with excessive permissions - minimize permissions
- **Encryption Gaps**: Data not encrypted at rest or transit - enforce encryption
- **Logging Gaps**: Not logging security events - comprehensive logging
- **Network Flatness**: No network segmentation - implement micro-segmentation

### Application Security Anti-Patterns

- **Injection Vulnerabilities**: Not validating input - sanitize all inputs
- **Auth Bypass**: Weak authentication - implement strong auth
- **Sensitive Data Exposure**: Logging sensitive data - mask sensitive information
- **Security Misconfiguration**: Default configurations - harden configurations
