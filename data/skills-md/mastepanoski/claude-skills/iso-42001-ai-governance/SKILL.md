---
name: iso-42001-ai-governance
description: AI governance audit using ISO 42001 standard. Ensures AI systems are developed and deployed responsibly with risk management, ethics, security, transparency, and compliance best practices.
---

# ISO 42001 AI Governance Audit

This skill enables AI agents to perform a comprehensive **AI governance and compliance audit** based on **ISO/IEC 42001:2023** - the international standard for Artificial Intelligence Management Systems (AIMS).

ISO 42001 provides a framework for responsible development, deployment, and use of AI systems, addressing risks, ethics, security, transparency, and regulatory compliance.

Use this skill to ensure AI projects follow international best practices, manage risks effectively, and maintain ethical standards throughout the AI lifecycle.

Combine with security audits, code reviews, or ethical AI assessments for comprehensive AI system evaluation.

## When to Use This Skill

Invoke this skill when:
- Developing or integrating AI systems
- Ensuring AI governance and compliance
- Managing AI risks and ethical concerns
- Preparing for AI regulatory requirements (EU AI Act, etc.)
- Auditing existing AI implementations
- Establishing AI governance frameworks
- Responding to AI security or bias incidents
- Planning responsible AI deployment
- Documenting AI systems for stakeholders

## Inputs Required

When executing this audit, gather:

- **ai_system_description**: Detailed description (purpose, capabilities, data used, users affected, deployment context) [REQUIRED]
- **use_case**: Specific application (e.g., hiring tool, medical diagnosis, content moderation) [REQUIRED]
- **risk_category**: High-risk, limited-risk, or minimal-risk per EU AI Act classification [OPTIONAL but recommended]
- **existing_documentation**: Technical docs, data sheets, model cards, risk assessments [OPTIONAL]
- **stakeholders**: Who develops, deploys, uses, and is affected by the AI [OPTIONAL]
- **regulatory_context**: Applicable laws (GDPR, EU AI Act, industry regulations) [OPTIONAL]

## ISO 42001 Framework Overview

ISO 42001 is structured around **10 key clauses** plus supporting annexes:

### Core Clauses

1. **Scope** - Define AIMS boundaries
2. **Normative References** - Related standards
3. **Terms and Definitions** - AI terminology
4. **Context of Organization** - Internal/external factors
5. **Leadership** - Management commitment and roles
6. **Planning** - Objectives and risk management
7. **Support** - Resources, competence, communication
8. **Operation** - AI system lifecycle management
9. **Performance Evaluation** - Monitoring and measurement
10. **Improvement** - Continual enhancement

### Key ISO 42001 Principles

#### 1. Risk-Based Approach
- Identify, assess, and mitigate AI-specific risks
- Consider technical, ethical, legal, and social risks
- Proportionate controls based on risk level

#### 2. Ethical AI
- Fairness and non-discrimination
- Transparency and explainability
- Human oversight and control
- Privacy and data protection
- Accountability

#### 3. Lifecycle Management
- Design → Development → Deployment → Monitoring → Decommissioning
- Continuous evaluation and improvement
- Documentation throughout

#### 4. Stakeholder Engagement
- Involve affected parties
- Clear communication about AI use
- Mechanisms for feedback and redress

---

## Audit Procedure

Follow these steps systematically:

### Step 1: Context and Scope Analysis (15 minutes)

**Understand the AI System:**

1. **Define AIMS Scope** (Clause 4)
   - What AI systems are included?
   - Organizational boundaries
   - Interfaces with other systems
   - Exclusions (if any)

2. **Identify Stakeholders:**
   - **Developers**: Who builds the AI?
   - **Deployers**: Who operates it?
   - **Users**: Who interacts with it?
   - **Affected Parties**: Who is impacted by decisions?
   - **Regulators**: What oversight exists?

3. **Assess Context:**
   - Industry and domain
   - Regulatory environment (EU AI Act, GDPR, sector-specific)
   - Cultural and social considerations
   - Technical maturity and capabilities

4. **Risk Classification** (EU AI Act alignment):
   - **Unacceptable Risk**: Prohibited uses (e.g., social scoring, real-time biometric surveillance)
   - **High Risk**: Significant impact (e.g., employment, credit scoring, healthcare, law enforcement)
   - **Limited Risk**: Transparency obligations (e.g., chatbots, deepfakes)
   - **Minimal Risk**: Low impact (e.g., spam filters, recommender systems)

---

### Step 2: Leadership and Governance Evaluation (20 minutes)

#### Clause 5: Leadership

**5.1 Leadership and Commitment**

**Evaluate:**
- [ ] Top management demonstrates commitment to AIMS
- [ ] AI governance policy established
- [ ] Resources allocated for responsible AI
- [ ] AI risks integrated into strategic planning

**Questions:**
- Is there executive-level accountability for AI?
- Who owns AI governance?
- Are AI principles documented and communicated?

**Findings:**
- ✅ Good: [Examples of strong leadership]
- ❌ Gaps: [Missing elements]

---

**5.2 AI Policy**

**Evaluate:**
- [ ] Documented AI policy exists
- [ ] Covers ethical principles
- [ ] Addresses risk management
- [ ] Defines roles and responsibilities
- [ ] Communicated to stakeholders
- [ ] Regularly reviewed and updated

**Required Policy Elements:**
1. **Purpose and Scope**: What AI systems are covered
2. **Ethical Principles**: Fairness, transparency, accountability
3. **Risk Management**: How risks are identified and mitigated
4. **Human Oversight**: Mechanisms for human control
5. **Data Governance**: Data quality, privacy, security
6. **Compliance**: Legal and regulatory obligations
7. **Incident Response**: How AI failures are handled
8. **Continuous Improvement**: Review and update processes

**Assessment:**
- Policy Score: [0-10]
- Completeness: [Comprehensive/Partial/Missing]
- Implementation: [Enforced/Documented only/Not followed]

---

**5.3 Organizational Roles and Responsibilities**

**Evaluate:**
- [ ] AI governance roles defined (e.g., AI Ethics Officer, Data Protection Officer)
- [ ] Clear accountability for AI decisions
- [ ] Cross-functional AI governance team
- [ ] Competencies and training requirements specified

**Key Roles to Define:**
- **AI Product Owner**: Responsible for AI system outcomes
- **AI Ethics Committee**: Oversees ethical compliance
- **Data Governance Lead**: Ensures data quality and privacy
- **Security Lead**: Manages AI security risks
- **Legal/Compliance Officer**: Ensures regulatory compliance
- **Human Oversight Designate**: Maintains meaningful human control

**Gap Analysis:**
- Defined: [Roles present]
- Missing: [Roles needed]
- Unclear: [Ambiguous responsibilities]

---

### Step 3: Planning and Risk Management (30 minutes)

#### Clause 6: Planning

**6.1 Actions to Address Risks and Opportunities**

**ISO 42001 Risk Categories:**

1. **Technical Risks**
   - Model accuracy and reliability
   - Robustness to adversarial attacks
   - Data quality and bias
   - System failures and errors
   - Integration issues
   - Scalability and performance

2. **Ethical Risks**
   - Discrimination and bias
   - Lack of fairness
   - Privacy violations
   - Lack of transparency
   - Autonomy and human dignity impacts

3. **Legal and Compliance Risks**
   - Regulatory non-compliance (GDPR, EU AI Act)
   - Intellectual property issues
   - Liability for AI decisions
   - Contractual obligations

4. **Operational Risks**
   - Dependency on AI vendors
   - Skills and competency gaps
   - Change management failures
   - Inadequate monitoring

5. **Reputational Risks**
   - Public trust erosion
   - Media scrutiny
   - Stakeholder backlash
   - Brand damage from AI failures

**Risk Assessment Process:**

For each identified risk:

```markdown
## Risk: [Name]

**Category**: Technical / Ethical / Legal / Operational / Reputational
**Likelihood**: Low / Medium / High
**Impact**: Low / Medium / High / Critical
**Risk Level**: [Likelihood × Impact]

**Description**: [What could go wrong]
**Affected Stakeholders**: [Who is impacted]
**Existing Controls**: [Current mitigations]
**Residual Risk**: [Risk after controls]

**Treatment Plan**:
- [ ] Accept (if low risk)
- [ ] Mitigate (reduce likelihood/impact)
- [ ] Transfer (insurance, contracts)
- [ ] Avoid (don't deploy feature)

**Mitigation Actions**:
1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

**Owner**: [Who is responsible]
**Timeline**: [When to implement]
**Review Date**: [When to reassess]
```

**Example Risks:**

**Risk 1: Algorithmic Bias in Hiring AI**
- Category: Ethical, Legal
- Likelihood: High (historical bias in training data)
- Impact: Critical (discrimination, legal liability)
- Risk Level: **CRITICAL**
- Mitigation:
  - Bias testing on protected attributes
  - Diverse training data
  - Regular fairness audits
  - Human review of decisions
  - Transparent criteria documentation

**Risk 2: Data Poisoning Attack**
- Category: Technical, Security
- Likelihood: Medium (if public data sources)
- Impact: High (model corruption)
- Risk Level: **HIGH**
- Mitigation:
  - Data validation and sanitization
  - Anomaly detection
  - Provenance tracking
  - Regular model retraining
  - Adversarial testing

---

**6.2 AI Objectives and Planning to Achieve Them**

**Evaluate:**
- [ ] Measurable AI objectives defined
- [ ] Aligned with organizational goals
- [ ] Consider stakeholder needs
- [ ] Include ethical and safety criteria
- [ ] Resources and timelines allocated
- [ ] Performance indicators established

**SMART AI Objectives Example:**
- "Achieve 95% accuracy while maintaining <5% false positive rate across all demographic groups by Q4"
- "Reduce bias disparity in loan approvals to <2% between groups by 2026"
- "Maintain 100% compliance with GDPR data subject rights"

---

### Step 4: Support and Resources (20 minutes)

#### Clause 7: Support

**7.1 Resources**

**Evaluate:**
- [ ] Adequate computational resources (GPUs, cloud infrastructure)
- [ ] Sufficient budget for responsible AI practices
- [ ] Access to diverse, quality training data
- [ ] Tools for AI monitoring and testing
- [ ] Expertise and personnel available

**Resource Assessment:**
- Compute: [Adequate/Limited/Insufficient]
- Budget: [Well-funded/Constrained/Underfunded]
- Data: [High-quality/Adequate/Poor]
- Tools: [State-of-art/Basic/Lacking]
- People: [Expert team/Learning/Understaffed]

---

**7.2 Competence**

**Evaluate:**
- [ ] AI/ML expertise available
- [ ] Understanding of ethical AI principles
- [ ] Knowledge of relevant regulations
- [ ] Data science and engineering skills
- [ ] Domain expertise for use case
- [ ] Ongoing training and development

**Competency Gaps:**
- Technical: [Gaps identified]
- Ethical: [Training needed]
- Legal: [Compliance knowledge]
- Domain: [Subject matter expertise]

**Training Plan:**
- Who needs training: [Roles]
- Topics: [Areas to cover]
- Format: [Workshops, courses, certifications]
- Timeline: [When to complete]

---

**7.3 Awareness**

**Evaluate:**
- [ ] Staff aware of AI policy
- [ ] Understanding of responsible AI principles
- [ ] Know how to report AI concerns
- [ ] Aware of their role in AI governance

**Communication Channels:**
- Internal documentation
- Training sessions
- Regular updates
- Incident reporting mechanisms

---

**7.4 Communication**

**Evaluate:**
- [ ] Stakeholder communication plan exists
- [ ] Transparency about AI use
- [ ] Clear explanation of AI decisions (where required)
- [ ] Feedback mechanisms for affected parties
- [ ] Public disclosure appropriate to risk level

**Communication Requirements by Risk Level:**

**High-Risk AI:**
- Public disclosure of AI use
- Detailed explanation of how system works
- Rights and remedies for affected individuals
- Contact for questions and complaints

**Limited-Risk AI:**
- Notification of AI interaction (e.g., chatbot disclosure)
- Basic information about system purpose

**Minimal-Risk AI:**
- Standard privacy notices
- Optional transparency information

---

**7.5 Documented Information**

**Evaluate:**
- [ ] AI system documentation maintained
- [ ] Model cards or datasheets created
- [ ] Risk assessments documented
- [ ] Audit trails for decisions
- [ ] Version control for models and data
- [ ] Retention policies defined

**Required Documentation (ISO 42001):**

1. **AI Policy and Procedures**
2. **Risk Assessments and Treatment Plans**
3. **AI System Descriptions** (Model Cards)
   - Purpose and intended use
   - Training data sources and characteristics
   - Model architecture and hyperparameters
   - Performance metrics
   - Known limitations and biases
   - Monitoring and maintenance procedures

4. **Data Governance Documentation**
   - Data inventories
   - Data quality assessments
   - Privacy impact assessments (PIAs)
   - Data lineage and provenance

5. **Testing and Validation Records**
   - Accuracy, fairness, robustness tests
   - Adversarial testing results
   - Edge case analysis
   - Ongoing monitoring logs

6. **Incident Reports and Resolutions**
7. **Training Records** (personnel competence)
8. **Audit and Review Reports**

**Documentation Maturity:**
- Level 5: Comprehensive, up-to-date, accessible
- Level 4: Good coverage, some gaps
- Level 3: Basic docs, outdated areas
- Level 2: Minimal, incomplete
- Level 1: Little to no documentation

---

### Step 5: Operation - AI Lifecycle Management (40 minutes)

#### Clause 8: Operation

**8.1 Operational Planning and Control**

ISO 42001 requires managing AI through its entire lifecycle:

**AI Lifecycle Stages:**

```
Design → Development → Validation → Deployment → Monitoring → Maintenance → Decommissioning
```

---

**STAGE 1: Design and Requirements**

**Evaluate:**
- [ ] Clear problem definition and success criteria
- [ ] Stakeholder needs assessed
- [ ] Ethical considerations identified early
- [ ] Regulatory requirements mapped
- [ ] Feasibility and impact analysis conducted
- [ ] Alternatives to AI considered

**Questions:**
- Is AI the right solution, or could simpler approaches work?
- What could go wrong?
- Who is affected and how?
- What data is needed and available?
- What are the ethical red lines?

**Red Flags:**
- Using AI for high-stakes decisions without justification
- No clear success metrics
- Ignoring stakeholder concerns
- Insufficient data or biased data sources

---

**STAGE 2: Data Management**

**Evaluate:**
- [ ] Data quality assessed (accuracy, completeness, timeliness)
- [ ] Bias and representativeness analyzed
- [ ] Data sources documented and verified
- [ ] Privacy and consent requirements met
- [ ] Data security and access controls
- [ ] Data minimization principles applied

**Data Quality Dimensions:**
1. **Accuracy**: Correct and error-free
2. **Completeness**: No missing values in critical fields
3. **Consistency**: Uniform across sources
4. **Timeliness**: Up-to-date and relevant
5. **Representativeness**: Reflects target population
6. **Fairness**: Balanced across demographic groups

**Bias Detection:**
- [ ] Underrepresentation of groups
- [ ] Historical bias in labels
- [ ] Proxy discrimination (e.g., zip code for race)
- [ ] Sampling bias
- [ ] Measurement bias

**Privacy Compliance (GDPR/ISO 42001):**
- [ ] Lawful basis for processing (consent, legitimate interest, etc.)
- [ ] Data subject rights supported (access, deletion, portability)
- [ ] Privacy by design principles
- [ ] Data Protection Impact Assessment (DPIA) if high-risk
- [ ] Data Processing Agreements (DPAs) with vendors

---

**STAGE 3: Model Development**

**Evaluate:**
- [ ] Appropriate algorithm selection
- [ ] Explainability requirements considered
- [ ] Fairness constraints incorporated
- [ ] Robustness testing planned
- [ ] Version control for code and models
- [ ] Reproducibility ensured

**Model Development Best Practices:**

1. **Baseline Establishment**
   - Simple model first (logistic regression, decision tree)
   - Benchmark against human performance
   - Justify complexity increase

2. **Fairness Considerations**
   - Define fairness metrics (demographic parity, equalized odds, etc.)
   - Test across protected attributes
   - Trade-offs between accuracy and fairness documented

3. **Explainability**
   - Use interpretable models when possible
   - Apply XAI techniques (SHAP, LIME) for black-box models
   - Document feature importance
   - Provide example-based explanations

4. **Adversarial Robustness**
   - Test against adversarial examples
   - Implement input validation
   - Monitor for distribution shift

5. **Reproducibility**
   - Random seeds set
   - Hyperparameters logged
   - Environment documented (dependencies, versions)
   - Training data snapshots preserved

---

**STAGE 4: Validation and Testing**

**Evaluate:**
- [ ] Comprehensive test suite executed
- [ ] Performance across subgroups validated
- [ ] Fairness metrics measured
- [ ] Robustness testing (adversarial, edge cases)
- [ ] Safety and security testing
- [ ] User acceptance testing (UAT)
- [ ] Independent validation (if high-risk)

**Testing Checklist:**

**Performance Testing:**
- [ ] Accuracy on test set
- [ ] Precision, recall, F1-score
- [ ] Performance by demographic group
- [ ] Performance on edge cases
- [ ] Calibration (confidence vs. accuracy)

**Fairness Testing:**
- [ ] Demographic parity (equal acceptance rates)
- [ ] Equalized odds (equal false positive/negative rates)
- [ ] Predictive parity (equal precision)
- [ ] Individual fairness (similar individuals treated similarly)

**Robustness Testing:**
- [ ] Adversarial examples resistance
- [ ] Input perturbation sensitivity
- [ ] Out-of-distribution detection
- [ ] Stress testing (high load, edge cases)

**Safety Testing:**
- [ ] Failure mode analysis
- [ ] Fallback mechanisms tested
- [ ] Human override tested
- [ ] Emergency stop procedures

**Security Testing:**
- [ ] Model extraction attacks
- [ ] Data poisoning resistance
- [ ] Backdoor detection
- [ ] Privacy leakage testing (membership inference)

**Validation Outcome:**
- Pass: [Meets all criteria]
- Conditional: [Meets most, some improvements needed]
- Fail: [Major gaps, do not deploy]

---

**STAGE 5: Deployment**

**Evaluate:**
- [ ] Phased rollout plan (pilot → limited → full)
- [ ] Monitoring infrastructure in place
- [ ] Human oversight mechanisms established
- [ ] Incident response plan ready
- [ ] User training and communication completed
- [ ] Rollback plan prepared

**Deployment Best Practices:**

1. **Pilot Testing**
   - Small user group
   - Controlled environment
   - Close monitoring
   - Rapid feedback loops

2. **Gradual Rollout**
   - Canary deployment (1% → 10% → 50% → 100%)
   - A/B testing against baseline
   - Monitor for unexpected impacts

3. **Human-in-the-Loop**
   - Human review of high-stakes decisions
   - Override capabilities
   - Escalation procedures
   - Audit sampling

4. **Communication**
   - Notify affected users
   - Provide transparency (AI disclosure)
   - Explain rights and remedies
   - Offer feedback channels

**Deployment Checklist:**
- [ ] Infrastructure ready (compute, storage, APIs)
- [ ] Monitoring dashboards configured
- [ ] Alerting thresholds set
- [ ] Incident response team trained
- [ ] Legal and compliance approval obtained
- [ ] Stakeholder communication sent
- [ ] Documentation updated

---

**STAGE 6: Monitoring and Maintenance**

**Evaluate:**
- [ ] Continuous performance monitoring
- [ ] Drift detection (data and model)
- [ ] Fairness monitoring over time
- [ ] User feedback collection
- [ ] Incident tracking and resolution
- [ ] Regular model retraining
- [ ] Audit trails maintained

**Monitoring Framework:**

**1. Performance Monitoring**
- Accuracy, precision, recall (daily/weekly)
- Latency and throughput
- Error rates and types
- Service availability (uptime)

**2. Fairness Monitoring**
- Outcome disparities across groups (weekly/monthly)
- False positive/negative rates by demographics
- User satisfaction by group
- Complaint rates

**3. Data Drift Detection**
- Input distribution changes
- Feature importance shifts
- Anomaly detection
- Trigger for retraining

**4. Model Drift Detection**
- Prediction distribution changes
- Confidence score patterns
- A/B test against updated models

**5. Safety Monitoring**
- Near-miss incidents
- Human override frequency
- Fallback activations
- Edge case occurrences

**Alert Triggers:**
- Accuracy drops > 5%
- Fairness disparity exceeds threshold
- Data drift detected
- Error rate spike
- Security anomalies
- User complaints increase

**Maintenance Schedule:**
- **Daily**: Dashboard review, alert triage
- **Weekly**: Performance deep-dive, fairness check
- **Monthly**: Model health assessment, incident review
- **Quarterly**: Comprehensive audit, retraining evaluation
- **Annually**: Full ISO 42001 compliance review

---

**STAGE 7: Decommissioning**

**Evaluate:**
- [ ] Decommissioning criteria defined
- [ ] Data retention/deletion policies
- [ ] User migration plan (if replacement system)
- [ ] Impact assessment of discontinuation
- [ ] Archival and documentation
- [ ] Lessons learned captured

**Decommissioning Triggers:**
- End of useful life
- Better alternative available
- Regulatory prohibition
- Unacceptable risk identified
- Business need eliminated

**Decommissioning Process:**
1. Stakeholder notification (advance warning)
2. Gradual phase-out
3. Data handling (delete, anonymize, or archive)
4. Model archival (for audits)
5. Post-mortem analysis
6. Knowledge transfer

---

### Step 6: Performance Evaluation (20 minutes)

#### Clause 9: Performance Evaluation

**9.1 Monitoring, Measurement, Analysis, and Evaluation**

**Key Performance Indicators (KPIs):**

**Technical KPIs:**
- Model accuracy/performance metrics
- System uptime and reliability
- Response time and latency
- Resource utilization

**Ethical KPIs:**
- Fairness metrics (disparity ratios)
- Transparency compliance (disclosure rates)
- Human oversight utilization (review rates)
- User trust and satisfaction scores

**Governance KPIs:**
- Incident response time
- Audit compliance rate
- Training completion rates
- Documentation currency (% up-to-date)

**Business KPIs:**
- User adoption rate
- ROI and cost savings
- Productivity improvements
- Risk mitigation effectiveness

**Dashboard Requirements:**
- Real-time performance metrics
- Fairness indicators
- Alert status
- Incident log
- Trend analysis

---

**9.2 Internal Audit**

**Evaluate:**
- [ ] Internal audit program established
- [ ] Audit schedule defined (at least annually)
- [ ] Independent auditors (not system developers)
- [ ] Audit findings documented
- [ ] Corrective actions tracked

**Audit Scope:**
- Compliance with ISO 42001 requirements
- Effectiveness of risk controls
- Documentation completeness
- Adherence to AI policy
- Incident management effectiveness

**Audit Frequency:**
- **High-Risk AI**: Quarterly
- **Limited-Risk AI**: Bi-annually
- **Minimal-Risk AI**: Annually

---

**9.3 Management Review**

**Evaluate:**
- [ ] Periodic management reviews conducted
- [ ] Review covers AIMS performance
- [ ] Decisions documented
- [ ] Resources allocated for improvements
- [ ] Stakeholder feedback considered

**Review Agenda:**
1. Audit findings and status
2. Performance against objectives
3. Risks and opportunities
4. Incident summary and lessons learned
5. Regulatory changes
6. Resource needs
7. Improvement initiatives

**Review Frequency:** At least annually, or after significant incidents

---

### Step 7: Improvement (15 minutes)

#### Clause 10: Improvement

**10.1 Nonconformity and Corrective Action**

**Evaluate:**
- [ ] Process for identifying nonconformities
- [ ] Root cause analysis conducted
- [ ] Corrective actions implemented
- [ ] Effectiveness verified
- [ ] AIMS updated to prevent recurrence

**Example Nonconformities:**
- Fairness threshold breached
- Undocumented model change
- Training data bias discovered
- Incident response delayed
- Audit finding not addressed

**Corrective Action Process:**
1. Identify nonconformity
2. Immediate containment (stop harm)
3. Root cause analysis (5 Whys, Fishbone)
4. Corrective action plan
5. Implementation
6. Verification of effectiveness
7. Documentation and communication

---

**10.2 Continual Improvement**

**Evaluate:**
- [ ] Process for ongoing improvement
- [ ] Lessons learned captured
- [ ] Best practices shared
- [ ] Innovation encouraged
- [ ] Benchmarking against industry

**Improvement Opportunities:**
- New techniques for bias mitigation
- Enhanced explainability methods
- Automation of monitoring
- Better stakeholder engagement
- Process efficiency gains

**Improvement Cycle:**
```
Plan → Do → Check → Act (PDCA)
```

Apply continuously to AI systems and governance processes.

---

## Complete ISO 42001 Audit Report

```markdown
# ISO 42001 AI Governance Audit Report

**AI System**: [Name]
**Organization**: [Name]
**Date**: [Date]
**Auditor**: [AI Agent]
**Standard**: ISO/IEC 42001:2023

---

## Executive Summary

### Compliance Status

**Overall Conformance**: [Conformant / Partially Conformant / Non-Conformant]

**Conformance by Clause:**

| Clause | Title | Status | Score | Critical Gaps |
|--------|-------|--------|-------|---------------|
| 4 | Context | ✅ / ⚠️ / ❌ | [X]/10 | [List] |
| 5 | Leadership | ✅ / ⚠️ / ❌ | [X]/10 | [List] |
| 6 | Planning | ✅ / ⚠️ / ❌ | [X]/10 | [List] |
| 7 | Support | ✅ / ⚠️ / ❌ | [X]/10 | [List] |
| 8 | Operation | ✅ / ⚠️ / ❌ | [X]/10 | [List] |
| 9 | Evaluation | ✅ / ⚠️ / ❌ | [X]/10 | [List] |
| 10 | Improvement | ✅ / ⚠️ / ❌ | [X]/10 | [List] |

**Overall Score**: [X]/100

### Risk Classification

**AI System Risk Level**: High / Limited / Minimal / Unacceptable

**Justification**: [Based on EU AI Act criteria and impact assessment]

### Top 5 Critical Findings

1. **[Finding]** - Clause [X] - Severity: Critical
   - Risk: [Description]
   - Impact: [Consequences]
   - Recommendation: [Immediate action]

2. **[Finding]** - Clause [X] - Severity: High
   [Continue...]

### Positive Highlights

- ✅ [Strength 1]
- ✅ [Strength 2]
- ✅ [Strength 3]

---

## Detailed Findings

[Full analysis by clause with evidence, gaps, and recommendations]

---

## Risk Assessment Summary

### Critical Risks Identified

**Risk 1: [Name]**
- **Category**: Ethical / Technical / Legal / Operational
- **Likelihood**: High
- **Impact**: Critical
- **Risk Level**: CRITICAL
- **Current Controls**: [Insufficient]
- **Required Actions**: [List]
- **Owner**: [Responsible party]
- **Deadline**: [Date]

[Continue for all critical and high risks...]

---

## Compliance Roadmap

### Phase 1: Critical Compliance (0-3 months)

**Objective**: Address critical gaps and establish baseline compliance

**Actions:**
1. [Action 1] - Owner: [Name] - Due: [Date]
2. [Action 2] - Owner: [Name] - Due: [Date]
3. [Action 3] - Owner: [Name] - Due: [Date]

**Success Criteria**: [Measurable outcomes]

**Investment**: [Time, resources, budget]

---

### Phase 2: Enhanced Governance (3-6 months)

**Objective**: Strengthen AI governance and risk management

**Actions:**
[List...]

---

### Phase 3: Maturity and Optimization (6-12 months)

**Objective**: Achieve full conformance and continual improvement

**Actions:**
[List...]

---

## Documentation Requirements

### Missing Documentation

- [ ] AI Policy Document
- [ ] Risk Assessment Register
- [ ] Model Cards for all AI systems
- [ ] Data Governance Procedures
- [ ] Incident Response Plan
- [ ] Training Records
- [ ] Audit Reports

**Priority**: Create within [timeframe]

---

## Recommendations by Stakeholder

### For Leadership

1. Establish AI Ethics Committee
2. Allocate budget for responsible AI
3. Mandate ISO 42001 compliance

### For AI Teams

1. Implement fairness testing in CI/CD
2. Create model cards for all systems
3. Conduct bias audits quarterly

### For Legal/Compliance

1. Monitor regulatory developments (EU AI Act)
2. Update privacy policies for AI use
3. Establish DPIA process for high-risk AI

### For Operations

1. Deploy monitoring infrastructure
2. Implement human oversight mechanisms
3. Create incident response runbooks

---

## Next Steps

1. **Immediate (Week 1)**
   - [ ] Present findings to leadership
   - [ ] Prioritize critical actions
   - [ ] Assign ownership

2. **Short-term (Month 1)**
   - [ ] Address critical risks
   - [ ] Start documentation efforts
   - [ ] Initiate training program

3. **Medium-term (Months 2-6)**
   - [ ] Implement AIMS processes
   - [ ] Conduct follow-up audit
   - [ ] Achieve partial conformance

4. **Long-term (Months 6-12)**
   - [ ] Full ISO 42001 conformance
   - [ ] Consider third-party certification
   - [ ] Continual improvement program

---

## Appendices

### A. ISO 42001 Checklist
[Detailed requirement-by-requirement checklist]

### B. Risk Register
[Complete risk inventory with assessments]

### C. Glossary
[AI and ISO terminology]

### D. References
- ISO/IEC 42001:2023
- EU AI Act
- NIST AI Risk Management Framework
- [Industry-specific standards]

---

**Report Version**: 1.0
**Confidentiality**: [Internal / Confidential / Public]
```

---

## ISO 42001 Compliance Checklist

Use this quick reference for self-assessment:

### Clause 4: Context ✓

- [ ] AIMS scope defined
- [ ] Stakeholders identified
- [ ] External issues (regulatory, social) assessed
- [ ] Internal capabilities evaluated

### Clause 5: Leadership ✓

- [ ] Management commitment documented
- [ ] AI policy established
- [ ] Roles and responsibilities assigned
- [ ] AI ethics committee or similar

### Clause 6: Planning ✓

- [ ] AI objectives set
- [ ] Risk assessment conducted
- [ ] Risk treatment plans documented
- [ ] Opportunities for improvement identified

### Clause 7: Support ✓

- [ ] Resources allocated (compute, budget, people)
- [ ] Competence requirements defined
- [ ] Training provided
- [ ] Awareness program active
- [ ] Documentation maintained

### Clause 8: Operation ✓

- [ ] AI lifecycle processes defined
- [ ] Data governance implemented
- [ ] Model development standards
- [ ] Validation and testing procedures
- [ ] Deployment controls
- [ ] Monitoring systems active
- [ ] Change management process

### Clause 9: Evaluation ✓

- [ ] Performance monitoring
- [ ] Internal audits scheduled
- [ ] Management reviews conducted
- [ ] KPIs tracked

### Clause 10: Improvement ✓

- [ ] Nonconformity process
- [ ] Corrective actions
- [ ] Continual improvement culture

---

## Best Practices

1. **Start with Risk Assessment**: Prioritize based on AI risk level
2. **Document Everything**: ISO 42001 requires extensive documentation
3. **Engage Stakeholders Early**: Include affected parties in governance
4. **Use Existing Frameworks**: Leverage NIST AI RMF, EU AI Act requirements
5. **Automate Monitoring**: Build MLOps with governance built-in
6. **Train Your Team**: ISO 42001 requires competent personnel
7. **Regular Audits**: Don't wait for problems—proactive reviews
8. **Learn from Incidents**: Every issue is improvement opportunity
9. **Balance Innovation and Safety**: Responsible AI doesn't mean no AI
10. **Seek Certification**: Third-party ISO 42001 certification adds credibility

---

## Regulatory Alignment

ISO 42001 aligns with major AI regulations:

**EU AI Act:**
- Risk classification framework
- High-risk AI obligations
- Transparency requirements
- Conformity assessment

**GDPR:**
- Data protection by design
- Privacy impact assessments
- Data subject rights
- Lawful processing

**NIST AI RMF:**
- Govern, Map, Measure, Manage functions
- Risk-based approach
- Trustworthy AI characteristics

**Sector-Specific:**
- Healthcare: FDA AI/ML guidance, MDR
- Finance: Model Risk Management (SR 11-7)
- Employment: EEOC AI guidance

---

## Common Pitfalls

1. **"We'll add governance later"** - Build it in from the start
2. **Treating ISO 42001 as one-time exercise** - It's continual
3. **Documentation without implementation** - Must be operational
4. **Ignoring low-risk AI** - Even minimal-risk needs baseline governance
5. **No stakeholder engagement** - Affected parties must be involved
6. **Insufficient resources** - Responsible AI requires investment
7. **Lack of monitoring** - Deploy-and-forget is non-compliant
8. **No incident response plan** - When AI fails, you need a plan
9. **Training as checkbox** - Teams must truly understand responsible AI
10. **Copying templates without customization** - Tailor to your context

---

## Version

1.0 - Initial release based on ISO/IEC 42001:2023

---

**Remember**: ISO 42001 is about building trustworthy AI systems through systematic risk management and governance. It's not a barrier to innovation—it's a framework for responsible innovation that protects both organizations and the people affected by AI.
