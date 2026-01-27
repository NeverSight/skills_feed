---
name: compliance-auditor
description: Specialized auditor for SOC2, HIPAA, GDPR, and regulatory compliance frameworks across industries
---

# Compliance Auditor Skill

## Purpose

Provides regulatory compliance auditing expertise specializing in SOC2, HIPAA, GDPR, and industry-specific compliance frameworks. Conducts gap analysis, evidence collection, control assessments, and remediation guidance to ensure organizations meet regulatory requirements and security standards.

## When to Use

- Conducting SOC 2 Type I & II audits
- Ensuring HIPAA compliance for healthcare systems
- Implementing GDPR data privacy requirements
- Preparing for PCI DSS assessments
- Mapping compliance requirements to organizational controls
- Performing gap analysis and remediation planning

## Overview
Expert in regulatory compliance auditing, specializing in SOC2, HIPAA, GDPR, and industry-specific compliance frameworks with gap analysis and remediation guidance.

## Compliance Frameworks

### Financial & Business Compliance
- **SOC 2 Type I & II** - Service Organization Control reporting
- **SOX** - Sarbanes-Oxley Act compliance
- **PCI DSS** - Payment Card Industry Data Security Standard
- **GLBA** - Gramm-Leach-Bliley Act

### Healthcare Compliance
- **HIPAA** - Health Insurance Portability and Accountability Act
- **HITECH** - Health Information Technology for Economic and Clinical Health
- **HITECH** - Omnibus Rule provisions
- **21 CFR Part 11** - Electronic signatures and records

### Data Privacy & Protection
- **GDPR** - General Data Protection Regulation (EU)
- **CCPA/CPRA** - California Consumer Privacy Act/Privacy Rights Act
- **PIPEDA** - Personal Information Protection and Electronic Documents Act
- **LGPD** - Lei Geral de Proteção de Dados (Brazil)

### Industry-Specific Standards
- **ISO 27001** - Information Security Management
- **ISO 27701** - Privacy Information Management
- **NIST Cybersecurity Framework** - Critical infrastructure
- **CMMC** - Cybersecurity Maturity Model Certification

## Core Audit Competencies

### Evidence Collection & Analysis
```bash
# Example patterns for compliance evidence
grep -r "audit" config/ --include="*.json" --include="*.yml" --include="*.properties"
grep -r "access" policies/ --include="*.md" --include="*.txt" --include="*.doc"
grep -r "retention" procedures/ --include="*.md" --include="*.pdf"
```

### Control Assessment
- Design effectiveness evaluation
- Operating effectiveness testing
- Control gap identification
- Remediation timeline development
- Continuous monitoring implementation

### Documentation Review
- Policy and procedure analysis
- Evidence collection validation
- Risk assessment methodology review
- Incident response documentation
- Third-party assessment reports

## Audit Methodology

### Planning & Scoping
- Compliance requirement mapping
- Risk-based approach development
- Sampling methodology design
- Stakeholder interviews
- Documentation requests

### Fieldwork Execution
- Control testing procedures
- Evidence collection protocols
- Process walk-throughs
- System configuration reviews
- Staff competency validation

### Reporting & Findings
- Gap analysis documentation
- Risk rating assignments
- Remediation recommendations
- Implementation roadmaps
- Executive summary preparation

## Specific Compliance Areas

### SOC 2 Trust Services Criteria
- **Security** - System protection against unauthorized access
- **Availability** - System availability for operation and use
- **Processing Integrity** - System processing completeness and accuracy
- **Confidentiality** - Information protection from unauthorized disclosure
- **Privacy** - Personal information collection and use controls

### HIPAA Administrative Safeguards
- Security officer designation
- Workforce security procedures
- Information access management
- Security awareness and training
- Security incident procedures

### GDPR Data Protection Requirements
- Lawfulness of processing
- Purpose limitation principles
- Data minimization practices
- Accuracy maintenance procedures
- Storage limitation implementations

## Audit Scenarios

### Cloud Service Provider Assessment
- AWS/Azure/GCP security configurations
- Multi-tenancy isolation controls
- Data encryption verification
- Service provider due diligence
- Subprocessor management

### Software Development Lifecycle
- Secure coding practices
- Change management procedures
- Code review processes
- Security testing integration
- DevSecOps pipeline compliance

### Third-Party Risk Management
- Vendor assessment procedures
- Contract compliance verification
- Service level agreement monitoring
- Data processing agreement review
- Supply chain security validation

## Deliverables

### Compliance Reports
- Comprehensive audit findings
- Gap analysis with remediation plans
- Control effectiveness ratings
- Risk mitigation strategies
- Compliance dashboard development

## Skill-Specific Scripts and References

### Available Compliance Auditor Scripts
Located in `scripts/` directory:

- **check_gdpr.py** - GDPR compliance checking (data minimization, consent, right to erasure)
- **validate_hipaa.py** - HIPAA validation (PHI protection, audit controls)
- **collect_soc2_evidence.py** - SOC 2 evidence collection (Security, Availability, Processing Integrity, Confidentiality, Privacy)
- **scan_pci_dss.py** - PCI DSS scanning (cardholder data, encryption standards)
- **validate_nist.py** - NIST controls validation (CSF, SP 800-53)
- **assess_iso27001.py** - ISO 27001 assessment (ISMS controls)
- **generate_report.py** - Compliance report generation

### Available Compliance Auditor References
Located in `references/` directory:

- **gdpr_requirements.md** - GDPR requirements and compliance checks
- **hipaa_guidelines.md** - HIPAA guidelines and controls
- **soc2_controls.md** - SOC 2 Type 2 examination criteria and controls
- **pci_dss_standard.md** - PCI DSS v4.0 requirements and compliance checklist
- **nist_controls.md** - NIST Cybersecurity Framework and SP 800-53 controls
- **iso27001_mapping.md** - ISO 27001 control mapping and implementation guidance

### Script Usage Examples

```bash
# GDPR compliance check
python3 scripts/check_gdpr.py . --config config/compliance.yaml --output gdpr_report.json

# HIPAA validation
python3 scripts/validate_hipaa.py . --format text

# SOC 2 evidence collection
python3 scripts/collect_soc2_evidence.py . --framework SOC2_Type2 --output soc2_evidence/

# PCI DSS scanning
python3 scripts/scan_pci_dss.py . --scan_level full

# NIST controls validation
python3 scripts/validate_nist.py . --framework CSF

# ISO 27001 assessment
python3 scripts/assess_iso27001.py . --controls annex_a --output iso_report.md

# Generate compliance report
python3 scripts/generate_report.py --evidence evidence/ --compliance SOC2 --output compliance_report.md
```

### Configuration Files

Create `config/compliance.yaml` for script configuration:

```yaml
compliance_auditing:
  audit_scope: '.'
  frameworks: ['SOC2', 'GDPR', 'HIPAA', 'PCI_DSS', 'ISO27001', 'NIST']
  
  check_gdpr:
    data_minimization: true
    consent_management: true
    right_to_erasure: true
    data_portability: true
    
  validate_hipaa:
    phi_protection: true
    audit_controls: true
    administrative_safeguards: true
    physical_safeguards: true
    technical_safeguards: true
    
  collect_soc2_evidence:
    trust_services_criteria: ['security', 'availability', 'processing_integrity', 'confidentiality', 'privacy']
    common_criteria: true
    
  scan_pci_dss:
    scan_level: 'full'
    cardholder_data_scope: true
    encryption_standards: true
    
  validate_nist:
    framework: 'CSF'
    control_baselines: ['low', 'moderate', 'high']
    
  assess_iso27001:
    controls: 'annex_a'
    isms_controls: true
    
  generate_report:
    report_format: 'markdown'
    include_recommendations: true
    include_roadmap: true
```

### Policy & Procedure Templates
- Security policy frameworks
- Incident response procedures
- Data classification guidelines
- Access management policies
- Business continuity plans

### Training Materials
- Compliance awareness programs
- Role-specific security training
- Incident response tabletop exercises
- Privacy best practices guides
- Regulatory change management

## Continuous Compliance
- Automated compliance monitoring
- Regulatory change tracking
- Control effectiveness testing
- Risk assessment updates
- Compliance management systems integration

## Industry Expertise
- Healthcare providers and payers
- Financial services institutions
- SaaS and technology companies
- Government contractors
- Educational institutions

## Examples

### Example 1: SOC 2 Type II Preparation for SaaS Startup

**Scenario:** A growing SaaS company preparing for their first SOC 2 Type II audit needs to implement controls and collect evidence for the Security and Availability trust services criteria.

**Audit Preparation Approach:**
1. **Gap Analysis**: Compared current practices against SOC 2 trust services criteria
2. **Control Implementation**: Deployed access management, encryption, and monitoring controls
3. **Evidence Collection**: Automated collection of logs, configurations, and access reviews
4. **Remediation**: Addressed 23 gaps identified in initial assessment

**Key Controls Implemented:**
- Multi-factor authentication for all system access
- Automated log retention and security monitoring
- Encrypted data at rest and in transit (TLS 1.3, AES-256)
- Incident response procedures with documented evidence
- Vendor management program with security assessments

**Audit Result**: Passed with 2 minor observations (no material findings)

### Example 2: HIPAA Compliance for Healthcare Application

**Scenario:** A healthcare technology company needs to ensure their patient portal meets HIPAA requirements for PHI protection.

**Compliance Assessment:**
1. **PHI Inventory**: Mapped all locations where PHI is stored, processed, or transmitted
2. **Technical Controls**: Evaluated encryption, access controls, and audit logging
3. **Administrative Safeguards**: Reviewed policies, procedures, and workforce training
4. **Business Associate Agreements**: Audited all third-party relationships

**Critical Findings and Remediation:**
- Unencrypted database backups → Implemented TDE and encrypted backup storage
- Excessive user access → Deployed role-based access control (RBAC)
- Missing audit logs → Integrated CloudTrail and database audit logging
- Outdated BAA with vendor → Negotiated updated BAA with current requirements

**Outcome**: Achieved full HIPAA compliance within 90 days

### Example 3: GDPR Data Privacy Implementation

**Scenario:** An e-commerce company expanding to EU markets needs to implement GDPR compliance for customer data processing.

**Privacy Implementation:**
1. **Data Mapping**: Documented all personal data flows across the organization
2. **Consent Management**: Implemented cookie consent and preference management
3. **Data Subject Rights**: Built automated processes for access, deletion, and portability requests
4. **Data Retention**: Defined and implemented retention schedules

**Implementation Components:**
- Privacy-by-design architecture review
- Consent management platform integration
- Data subject request (DSR) automation workflow
- International data transfer mechanisms (Standard Contractual Clauses)
- Privacy impact assessment (PIA) process

**Measurable Outcomes:**
- Consent capture rate: 98% (up from 45%)
- DSR response time: 5 days average (regulatory requirement: 30 days)
- Data breach notification process tested quarterly
- Privacy training completion: 100% of employees

## Best Practices

### Audit Preparation

- **Start Early**: Begin compliance efforts 6-12 months before audit
- **Gap Analysis First**: Understand where you stand before planning remediation
- **Phased Approach**: Address highest-risk gaps first
- **Evidence Automation**: Collect evidence continuously, not just before audit
- **Management Buy-In**: Ensure leadership understands compliance requirements

### Control Framework

- **Risk-Based Controls**: Implement controls based on risk assessment findings
- **Defense in Depth**: Multiple layers of controls for critical areas
- **Least Privilege**: Grant minimum access required for each role
- **Change Management**: Document and review all control changes
- **Continuous Monitoring**: Implement automated control effectiveness testing

### Documentation Excellence

- **Clear Policies**: Write policies that are understandable and actionable
- **Procedure Documentation**: Detail how policies are implemented operationally
- **Evidence Artifacts**: Maintain comprehensive evidence of control operation
- **Traceability**: Link controls to requirements and risks
- **Version Control**: Track policy changes over time

### Third-Party Management

- **Due Diligence**: Assess security posture before engagement
- **Contract Requirements**: Include security requirements in contracts
- **Ongoing Monitoring**: Reassess vendors periodically
- **Incident Coordination**: Establish breach notification procedures
- **Exit Planning**: Define data handling at relationship end

### Regulatory Updates

- **Track Changes**: Monitor regulatory developments in your industry
- **Impact Assessment**: Evaluate how changes affect current compliance
- **Proactive Adaptation**: Update controls before enforcement deadlines
- **Industry Collaboration**: Participate in industry compliance groups
- **Expert Consultation**: Engage specialists for complex requirements

## Anti-Patterns

### Audit Process Anti-Patterns

- **Checkbox Compliance**: Treating compliance as a form-filling exercise - focus on actual security outcomes
- **Point-in-Time Snapshots**: Assessing controls only at audit time - implement continuous compliance monitoring
- **Evidence Fabrication**: Creating evidence rather than demonstrating real controls - build genuine compliance programs
- **Scope Shrinking**: Minimizing audit scope to reduce findings - address root causes instead of hiding problems

### Control Implementation Anti-Patterns

- **Paper Controls**: Policies that exist only in documentation - implement technical enforcement mechanisms
- **Over-Complex Controls**: Controls so complex they cannot be operationalized - balance security with operability
- **Control Redundancy**: Implementing overlapping controls without coordination - map and rationalize control portfolio
- **Control Gaps**: Leaving security domains uncovered - maintain comprehensive control coverage

### Evidence Collection Anti-Patterns

- **Last Minute Rush**: Collecting evidence only when auditors arrive - automate continuous evidence collection
- **Incomplete Evidence**: Providing partial evidence that raises more questions - ensure comprehensive documentation
- **Outdated Evidence**: Using evidence from outdated systems or processes - maintain current evidence artifacts
- **Inaccessible Evidence**: Evidence that cannot be located or produced - organize and index evidence systematically

### Remediation Anti-Patterns

- **Temporary Fixes**: Applying bandages instead of solving root causes - implement permanent solutions
- **Finding Chasing**: Prioritizing based on audit severity rather than risk - assess actual risk impact
- **Remediation Debt**: Accumulating findings without resolution - maintain remediation backlog with timelines
- **Siloed Remediation**: Fixing findings in isolation without systemic improvement - identify patterns and prevent recurrence
