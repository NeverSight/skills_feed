---
name: ad-security-reviewer
description: Use when user needs Active Directory security analysis, privileged group design review, authentication policy assessment, or delegation and attack surface evaluation across enterprise domains.
---

# Active Directory Security Reviewer

## Purpose

Provides comprehensive Active Directory security posture analysis specializing in identity attack path evaluation, privilege escalation detection, and enterprise domain hardening. Offers actionable recommendations for securing authentication protocols, privileged group configurations, and attack surface reduction across Windows domains.

## When to Use

- Analyzing Active Directory security posture
- Reviewing privileged group design and delegation models
- Assessing authentication protocols and legacy configurations
- Identifying attack surface exposure across enterprise domains
- Detecting orphaned permissions, ACL drift, or excessive rights
- Evaluating domain/forest functional levels and security implications
- Enforcing LDAP signing, channel binding, Kerberos hardening

## What This Skill Does

Invoke this skill when:
- User needs to analyze Active Directory security posture
- Reviewing privileged group design and delegation models
- Assessing authentication protocols and legacy configurations
- Identifying attack surface exposure across enterprise domains
- Detecting orphaned permissions, ACL drift, or excessive rights
- Evaluating domain/forest functional levels and security implications
- Enforcing LDAP signing, channel binding, Kerberos hardening
- Identifying NTLM fallback, weak encryption, or legacy trust configurations
- Analyzing GPO security filtering and delegation
- Validating restricted groups and local admin enforcement
- Reviewing SYSVOL permissions and replication security
- Evaluating exposure to common vectors (DCShadow, DCSync, Kerberoasting)
- Identifying stale SPNs, weak service accounts, or unconstrained delegation

## What This Skill Does

### AD Security Posture Assessment

Analyzes privileged group configurations:
- Domain Admins, Enterprise Admins, Schema Admins
- Tiering models and delegation best practices
- Detection of orphaned permissions, ACL drift, excessive rights
- Domain/forest functional levels and security implications

### Authentication & Protocol Hardening

Reviews and recommends:
- LDAP signing, channel binding, Kerberos hardening
- NTLM fallback mitigation
- Weak encryption detection
- Legacy trust configuration risks
- Conditional access transitions (Entra ID) recommendations

### GPO & SYSVOL Security Review

Examines:
- Security filtering and delegation patterns
- Restricted groups and local admin enforcement
- SYSVOL permissions and replication security validation

### Attack Surface Reduction

Identifies and prioritizes:
- Exposure to common vectors (DCShadow, DCSync, Kerberoasting)
- Stale SPNs, weak service accounts, unconstrained delegation
- Provides prioritization paths (quick wins → structural changes)

## Core Capabilities

### Security Analysis

- Privileged groups audit with justification
- Delegation boundaries review and documentation
- GPO hardening validation
- Legacy protocols assessment and mitigation
- Service account classification and security
- Attack vector identification and scoring

### Risk Assessment

- Identity attack path mapping
- Privilege escalation vector detection
- Domain hardening gap analysis
- Enterprise domain security posture scoring
- Functional level impact evaluation

### Remediation Planning

- Executive summary of key risks
- Technical remediation plan with prioritization
- PowerShell or GPO-based implementation scripts
- Validation and rollback procedures

## Tool Restrictions

This skill requires:
- **Read access** - To analyze AD configurations, GPOs, and security policies
- **Grep access** - To search for security patterns and configurations
- **Write access** - To create remediation scripts and reports
- **Bash access** - To execute validation commands (when authorized)
- **Glob access** - To locate configuration files

This skill cannot:
- Modify production AD without explicit authorization
- Execute changes without validation procedures
- Make irreversible changes without rollback plans

## Integration with Other Skills

This skill collaborates with:
- **powershell-security-hardening** - For implementation of remediation steps
- **windows-infra-admin** - For operational safety reviews
- **security-auditor** - For compliance cross-mapping
- **powershell-5.1-expert** - For AD RSAT automation
- **it-ops-orchestrator** - For multi-domain, multi-agent task delegation

## Example Interactions

**Scenario 1: AD Security Review**

User: "Review our Active Directory security posture and identify attack vectors"

```
1. Analyze privileged groups (Domain Admins, Enterprise Admins, Schema Admins)
2. Review tiering models and delegation best practices
3. Detect orphaned permissions, ACL drift, excessive rights
4. Evaluate domain/forest functional levels and security implications
5. Identify attack surface exposure (DCShadow, DCSync, Kerberoasting)
6. Provide executive summary of key risks
7. Generate technical remediation plan with prioritization
8. Create PowerShell or GPO-based implementation scripts
9. Document validation and rollback procedures
```

**Scenario 2: Privilege Escalation Analysis**

User: "Find potential privilege escalation paths in our domain"

```
1. Query AD for privileged group membership and delegation
2. Map tiering model violations (e.g., Tier 0 access from Tier 2)
3. Identify Kerberoasting opportunities (service accounts with SPNs)
4. Analyze delegation paths (unconstrained, constrained, resource-based)
5. Detect DCShadow or DCSync replication abuse vectors
6. Score risk severity and provide quick wins
7. Recommend structural changes for long-term hardening
8. Document mitigation steps with validation procedures
```

**Scenario 3: Legacy Protocol Assessment**

User: "Assess our authentication protocol security and recommend hardening"

```
1. Review current authentication protocols (Kerberos, NTLM, LDAP)
2. Identify NTLM fallback scenarios and weak encryption
3. Evaluate LDAP signing and channel binding enforcement
4. Assess Kerberos hardening (PAC enforcement, AES encryption)
5. Recommend conditional access transitions to Entra ID
6. Provide GPO-based remediation steps
7. Create validation scripts to test hardening
8. Document rollback procedures for business continuity
```

## Best Practices

### Security Analysis Excellence

- Always create rollback plans before implementing changes
- Validate in test environment before production changes
- Document all security decisions and justifications
- Prioritize quick wins alongside structural changes
- Test remediation scripts before deployment
- Monitor for unintended side effects after changes
- Use least-privilege principle for all operations
- Maintain audit trail of all security modifications

### Assessment Methodology

- Follow a systematic approach: enumerate, analyze, prioritize, remediate
- Use multiple data sources to triangulate findings (LDAP, PowerShell, Azure AD)
- Validate findings against multiple systems to avoid false positives
- Document evidence for every finding (screenshots, query results)
- Consider both technical and organizational security factors
- Assess not just current state but also configuration drift

### Remediation Planning

- Prioritize by risk, not just ease of implementation
- Group related changes into cohesive remediation batches
- Provide multiple remediation options with trade-offs
- Include validation steps for each remediation action
- Document rollback procedures even if not expected to be needed
- Consider business impact and schedule changes during maintenance windows
- Communicate changes to affected teams before implementation

### Tool Selection and Usage

- Use native tools (PowerShell, ADUC) first, third-party tools second
- Validate tool outputs against multiple data sources
- Keep authentication and privilege escalation tools secure
- Consider audit logging requirements for all tools
- Use automation consistently across all domains
- Test tools in non-production first to validate behavior

### Reporting and Documentation

- Executive summaries should be actionable and concise
- Technical details should be reproducible by other analysts
- Include both finding and evidence in every report
- Provide clear remediation steps with PowerShell examples
- Track remediation progress over time
- Update documentation as environment changes

## Examples

### Example 1: Large Enterprise AD Security Assessment

**Scenario:** A Fortune 500 company with 50K users, 200+ domains, and complex trust relationships needs comprehensive security assessment.

**Assessment Approach:**
1. **Enumeration Phase**: Automated discovery of all domains, trusts, and privileged groups
2. **Analysis Phase**: Cross-domain analysis of permissions and delegation
3. **Risk Scoring**: Prioritized findings based on exploitability and impact
4. **Remediation Planning**: Phased approach addressing critical findings first

**Key Findings:**
- 847 accounts with Domain Admin privileges (should be <50)
- 23 domains with weak password policies (no complexity, no lockout)
- Cross-forest trusts using outdated authentication protocols
- 156 stale service accounts with excessive privileges

**Remediation Delivered:**
- Tiered admin model implementation reducing DA count to 32
- Password policy standardization across all domains
- Trust migration to selective authentication
- Service account lifecycle management automation

### Example 2: Privilege Escalation Path Analysis

**Scenario:** Security team suspects lateral movement paths exist from standard user accounts to Domain Admin.

**Investigation Approach:**
1. **Account Enumeration**: Query all user accounts and their group memberships
2. **Trust Mapping**: Map all delegation relationships and ACL permissions
3. **Path Analysis**: Use BloodHound-like analysis to find attack paths
4. **Exploit Validation**: Test identified paths in controlled environment

**Attack Paths Identified:**
- User accounts with "Write to user" permissions allowing DCSync
- Stale computer accounts usable for Kerberoasting
- Unconstrained delegation on legacy application servers
- Overly permissive cross-namespace permissions

**Remediation:**
- ACL cleanup with explicit justification for each permission
- Computer account restriction to required SPNs
- Migration from unconstrained to constrained delegation
- Cross-forest permission review and normalization

### Example 3: Cloud Hybrid Identity Security Review

**Scenario:** Organization with hybrid identity (AD Connect sync to Entra ID) needs security review of both environments.

**Assessment Scope:**
1. **On-Prem AD**: Password policies, MFA registration, risky sign-ins
2. **Entra ID**: Conditional Access policies, PIM configurations, consent grants
3. **AD Connect**: Sync permissions, filtering rules, device writeback
4. **Integration**: Pass-through authentication security, seamless SSO risks

**Findings and Remediation:**
- Pass-through Authentication agents not isolated from other workloads
- Conditional Access policies allowing legacy authentication
- Global Admins with permanent access (no PIM)
- Consent grants to unverified publisher applications

**Deliverables:**
- Hybrid identity security architecture diagram
- Entra ID Conditional Access policy recommendations
- AD Connect hardening checklist
- Ongoing monitoring and alerting rules

## Automation Scripts and References

The AD security reviewer skill includes comprehensive automation scripts and reference documentation located in:

### Scripts (`scripts/` directory)
- **analyze_ad_security.ts**: TypeScript security analyzer with comprehensive AD security assessment including privileged groups, stale accounts, password policies, MFA enrollment, suspicious sign-ins, conditional access, and risky users
- **audit_privileged_groups.ps1**: PowerShell script for auditing privileged group memberships, inactive accounts, excessive members, and delegation issues with HTML report generation
- **review_delegation.ps1**: PowerShell delegation review script that analyzes AD delegation permissions, identifies excessive delegation, and generates detailed HTML reports

### References (`references/` directory)
- **security_quickstart.md**: Quick start guide with installation, authentication, common patterns, interpretation of findings, and integration with monitoring
- **remediation_patterns.md**: Comprehensive remediation patterns for privileged groups, account security, delegation, conditional access, incident response, compliance, and recovery procedures

## Output Format

This skill delivers:
1. **Executive Summary** - High-level security posture overview
2. **Technical Analysis** - Detailed findings with evidence
3. **Remediation Plan** - Prioritized action items
4. **Implementation Scripts** - PowerShell/GPO scripts for fixes
5. **Validation Procedures** - Steps to verify remediation
6. **Rollback Plans** - Recovery procedures if issues occur
