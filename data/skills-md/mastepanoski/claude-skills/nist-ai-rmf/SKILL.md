---
name: nist-ai-rmf
description: AI risk assessment using NIST AI RMF 1.0 framework. Evaluate AI systems across 4 core functions (Govern, Map, Measure, Manage) for trustworthy and responsible AI deployment.
---

# NIST AI Risk Management Framework (AI RMF 1.0)

This skill enables AI agents to perform a comprehensive **AI risk assessment** using the **NIST AI Risk Management Framework (AI RMF 1.0)**, published January 2023 by the National Institute of Standards and Technology.

The AI RMF is a voluntary, technology- and sector-agnostic framework designed to help organizations manage risks associated with AI systems throughout their lifecycle. It promotes trustworthy AI development by addressing risks that affect individuals, organizations, and society.

Use this skill to identify, assess, and manage AI risks; establish governance structures; ensure trustworthy AI characteristics; and align with international AI risk management best practices.

Combine with "ISO 42001 AI Governance" for comprehensive compliance coverage or "OWASP LLM Top 10" for security-focused assessment.

## When to Use This Skill

Invoke this skill when:
- Assessing risks of AI systems before deployment
- Establishing AI governance and accountability structures
- Evaluating trustworthiness of AI products and services
- Preparing for regulatory compliance (EU AI Act, state AI laws)
- Conducting periodic AI risk reviews
- Evaluating third-party AI tools and vendors
- Building organizational AI risk management programs
- Documenting AI system risks for stakeholders

## Inputs Required

When executing this assessment, gather:

- **ai_system_description**: Description of the AI system (purpose, capabilities, deployment context, users, data sources) [REQUIRED]
- **system_lifecycle_stage**: Current stage (design, development, deployment, monitoring, decommissioning) [OPTIONAL, defaults to deployment]
- **organization_context**: Organization size, industry, risk tolerance, regulatory environment [OPTIONAL]
- **existing_controls**: Current risk management processes or controls in place [OPTIONAL]
- **specific_concerns**: Known risks, incidents, or areas of focus [OPTIONAL]
- **stakeholders**: Key stakeholders and affected communities [OPTIONAL]

## Trustworthy AI Characteristics

The AI RMF identifies seven characteristics of trustworthy AI that serve as evaluation criteria across all functions:

1. **Valid and Reliable**: System performs as intended with consistent results
2. **Safe**: System does not endanger human life, health, property, or the environment
3. **Secure and Resilient**: System withstands adverse events and recovers gracefully
4. **Accountable and Transparent**: Information about the system is available to stakeholders
5. **Explainable and Interpretable**: Mechanisms and outputs can be understood
6. **Privacy-Enhanced**: Human autonomy and data rights are protected
7. **Fair with Harmful Bias Managed**: System does not produce discriminatory outcomes

---

## The 4 Core Functions

The AI RMF Core is composed of four functions, each broken into categories and subcategories:

### GOVERN Function

Establishes organizational policies, processes, and accountability for AI risk management. GOVERN is cross-cutting and applies across all other functions.

#### GOVERN 1: Policies and Processes
*Policies, processes, procedures, and practices across the organization related to the mapping, measuring, and managing of AI risks are in place, transparent, and implemented effectively.*

- **GOVERN 1.1**: Legal and regulatory requirements involving AI are understood, managed, and documented
- **GOVERN 1.2**: Trustworthy AI characteristics integrated into organizational policies, processes, and practices
- **GOVERN 1.3**: Processes to determine needed risk management activity levels based on organizational risk tolerance
- **GOVERN 1.4**: Risk management process and outcomes established through transparent policies, procedures, and controls
- **GOVERN 1.5**: Ongoing monitoring and periodic review of risk management process with clear roles and responsibilities
- **GOVERN 1.6**: Mechanisms to inventory AI systems resourced by organizational risk priorities
- **GOVERN 1.7**: Processes for decommissioning and phasing out AI systems safely

#### GOVERN 2: Accountability Structures
*Accountability structures ensure appropriate teams and individuals are empowered, responsible, and trained for AI risk management.*

- **GOVERN 2.1**: Roles, responsibilities, and communication lines documented and clear
- **GOVERN 2.2**: Personnel receive AI risk management training
- **GOVERN 2.3**: Executive leadership takes responsibility for AI decisions

#### GOVERN 3: Workforce Diversity and Inclusion
*Workforce diversity, equity, inclusion, and accessibility processes are prioritized in AI risk management.*

- **GOVERN 3.1**: Decision-making informed by diverse team (demographics, disciplines, expertise)
- **GOVERN 3.2**: Policies define roles for human-AI configurations and oversight

#### GOVERN 4: Risk Culture
*Organizational teams are committed to a culture that considers and communicates AI risk.*

- **GOVERN 4.1**: Policies foster critical thinking and safety-first mindset
- **GOVERN 4.2**: Teams document and communicate risks and impacts broadly
- **GOVERN 4.3**: Practices enable AI testing, incident identification, and information sharing

#### GOVERN 5: Stakeholder Engagement
*Processes are in place for robust engagement with relevant AI actors.*

- **GOVERN 5.1**: Policies collect, consider, and integrate external feedback on impacts
- **GOVERN 5.2**: Mechanisms regularly incorporate adjudicated feedback into system design

#### GOVERN 6: Third-Party Risk
*Policies and procedures address AI risks from third-party software, data, and supply chain.*

- **GOVERN 6.1**: Policies address risks from third-party entities including IP infringement
- **GOVERN 6.2**: Contingency processes handle failures in high-risk third-party systems

---

### MAP Function

Identifies and contextualizes AI system risks within the operational environment.

#### MAP 1: Context Established
*Context is established and understood.*

- **MAP 1.1**: Intended purposes, beneficial uses, laws, norms, and deployment settings documented
- **MAP 1.2**: Interdisciplinary AI actors with demographic diversity participate and documented
- **MAP 1.3**: Organization's mission and goals for AI technology understood and documented
- **MAP 1.4**: Business value or context clearly defined or re-evaluated
- **MAP 1.5**: Organizational risk tolerances determined and documented
- **MAP 1.6**: System requirements elicited with socio-technical considerations

#### MAP 2: System Categorization
*Categorization of the AI system is performed.*

- **MAP 2.1**: Specific tasks and methods defined (classifiers, generative models, recommenders)
- **MAP 2.2**: System knowledge limits and human oversight documented
- **MAP 2.3**: Scientific integrity and TEVV considerations identified

#### MAP 3: Capabilities and Costs
*AI capabilities, targeted usage, goals, expected benefits, and costs are understood.*

- **MAP 3.1**: Potential benefits of intended functionality examined and documented
- **MAP 3.2**: Potential costs (monetary and non-monetary) from AI errors documented
- **MAP 3.3**: Targeted application scope specified based on capability
- **MAP 3.4**: Operator and practitioner proficiency assessed
- **MAP 3.5**: Human oversight processes defined and documented

#### MAP 4: Component Risks
*Risks and benefits are mapped for all components including third-party.*

- **MAP 4.1**: Approaches for mapping technology and legal risks documented
- **MAP 4.2**: Internal risk controls for components identified and documented

#### MAP 5: Impact Characterization
*Impacts to individuals, groups, communities, organizations, and society are characterized.*

- **MAP 5.1**: Likelihood and magnitude of impacts (beneficial and harmful) documented
- **MAP 5.2**: Practices for regular engagement with relevant AI actors documented

---

### MEASURE Function

Employs tools, techniques, and methodologies to assess, benchmark, and monitor AI risk.

#### MEASURE 1: Methods and Metrics
*Appropriate methods and metrics are identified and applied.*

- **MEASURE 1.1**: Approaches and metrics selected starting with most significant risks
- **MEASURE 1.2**: Appropriateness of metrics regularly assessed and updated
- **MEASURE 1.3**: Internal experts or independent assessors involved in assessments

#### MEASURE 2: Trustworthiness Evaluation
*AI systems are evaluated for trustworthy characteristics.*

- **MEASURE 2.1**: Test sets, metrics, and tool details documented during TEVV
- **MEASURE 2.2**: Evaluations with human subjects meet requirements and represent relevant populations
- **MEASURE 2.3**: Performance or assurance criteria measured and demonstrated
- **MEASURE 2.4**: Functionality and behavior monitored in production
- **MEASURE 2.5**: System demonstrated valid and reliable with generalizability limitations documented
- **MEASURE 2.6**: System regularly evaluated for safety risks with residual risk within tolerance
- **MEASURE 2.7**: Security and resilience evaluated and documented
- **MEASURE 2.8**: Transparency and accountability risks examined
- **MEASURE 2.9**: AI model explained, validated, and output interpreted within context
- **MEASURE 2.10**: Privacy risk examined and documented
- **MEASURE 2.11**: Fairness and bias evaluated with results documented
- **MEASURE 2.12**: Environmental impact and sustainability assessed
- **MEASURE 2.13**: Effectiveness of TEVV metrics evaluated

#### MEASURE 3: Risk Tracking
*Mechanisms for tracking identified AI risks over time are in place.*

- **MEASURE 3.1**: Approaches track existing, unanticipated, and emergent risks
- **MEASURE 3.2**: Risk tracking considered for settings where assessment is difficult
- **MEASURE 3.3**: Feedback processes for end users to report problems and appeal outcomes

#### MEASURE 4: Measurement Efficacy
*Feedback about efficacy of measurement is gathered and assessed.*

- **MEASURE 4.1**: Measurement approaches informed by domain experts and end users
- **MEASURE 4.2**: Results validated for consistency with intended performance
- **MEASURE 4.3**: Measurable performance improvements or declines identified

---

### MANAGE Function

Allocates resources to mapped and measured risks on a regular basis.

#### MANAGE 1: Risk Prioritization
*AI risks based on assessments are prioritized, responded to, and managed.*

- **MANAGE 1.1**: Determination made whether AI system achieves intended purposes
- **MANAGE 1.2**: Treatment of risks prioritized based on impact, likelihood, and resources
- **MANAGE 1.3**: Responses to high-priority risks developed (mitigate, transfer, avoid, accept)
- **MANAGE 1.4**: Negative residual risks documented for downstream users

#### MANAGE 2: Benefit Maximization
*Strategies to maximize AI benefits and minimize negative impacts are planned and documented.*

- **MANAGE 2.1**: Resources to manage risks considered alongside non-AI alternatives
- **MANAGE 2.2**: Mechanisms to sustain value of deployed systems
- **MANAGE 2.3**: Procedures to respond to and recover from unknown risks
- **MANAGE 2.4**: Mechanisms to supersede, disengage, or deactivate inconsistent systems

#### MANAGE 3: Third-Party Risk Management
*AI risks and benefits from third-party entities are managed.*

- **MANAGE 3.1**: Third-party risks regularly monitored with controls applied
- **MANAGE 3.2**: Pre-trained models monitored as part of regular maintenance

#### MANAGE 4: Communication and Monitoring
*Risk treatments and communication plans are documented and monitored.*

- **MANAGE 4.1**: Post-deployment monitoring plans with user input, appeal, and decommissioning mechanisms
- **MANAGE 4.2**: Continual improvement activities integrated into updates
- **MANAGE 4.3**: Incidents communicated to relevant actors; tracking and recovery documented

---

## Audit Procedure

Follow these steps systematically:

### Step 1: System Understanding (15 minutes)

1. **Review AI system:**
   - Analyze `ai_system_description` and `system_lifecycle_stage`
   - Identify system type (classifier, generative, recommender, autonomous, etc.)
   - Document data sources, models, and deployment environment
   - Note stakeholders and affected communities

2. **Understand context:**
   - Review `organization_context` and regulatory environment
   - Identify applicable laws and standards
   - Note risk tolerance and existing controls

3. **Define scope:**
   - Determine which functions and categories to assess
   - Prioritize based on lifecycle stage and concerns

### Step 2: GOVERN Assessment (20 minutes)

Evaluate organizational governance:

- [ ] **G1**: Are AI risk policies in place and transparent?
- [ ] **G1.1**: Legal/regulatory requirements understood and documented?
- [ ] **G1.2**: Trustworthy AI characteristics in organizational policies?
- [ ] **G1.5**: Monitoring and review processes planned?
- [ ] **G1.6**: AI system inventory maintained?
- [ ] **G2**: Accountability structures defined?
- [ ] **G2.1**: Roles and responsibilities clear?
- [ ] **G2.3**: Executive leadership accountable?
- [ ] **G3.1**: Diverse team informing decisions?
- [ ] **G4**: Risk culture fostered?
- [ ] **G5**: Stakeholder engagement processes in place?
- [ ] **G6**: Third-party risks addressed?

### Step 3: MAP Assessment (20 minutes)

Evaluate risk identification and context:

- [ ] **M1.1**: Intended purposes and deployment context documented?
- [ ] **M1.5**: Risk tolerances determined?
- [ ] **M2.1**: AI tasks and methods defined?
- [ ] **M2.2**: Knowledge limits and human oversight documented?
- [ ] **M3.1**: Benefits examined and documented?
- [ ] **M3.2**: Costs from AI errors documented?
- [ ] **M3.5**: Human oversight processes defined?
- [ ] **M4.1**: Component risks mapped?
- [ ] **M5.1**: Impact likelihood and magnitude documented?

### Step 4: MEASURE Assessment (25 minutes)

Evaluate risk measurement and monitoring:

- [ ] **ME1.1**: Risk metrics selected and applied?
- [ ] **ME2.3**: Performance criteria measured?
- [ ] **ME2.4**: Production behavior monitored?
- [ ] **ME2.5**: Validity and reliability demonstrated?
- [ ] **ME2.6**: Safety risks evaluated?
- [ ] **ME2.7**: Security and resilience evaluated?
- [ ] **ME2.9**: Model explainability documented?
- [ ] **ME2.10**: Privacy risk examined?
- [ ] **ME2.11**: Fairness and bias evaluated?
- [ ] **ME3.1**: Risk tracking in place?
- [ ] **ME3.3**: User feedback mechanisms established?

### Step 5: MANAGE Assessment (20 minutes)

Evaluate risk response and treatment:

- [ ] **MA1.1**: System achieves intended purposes?
- [ ] **MA1.2**: Risk treatment prioritized?
- [ ] **MA1.3**: Response plans for high-priority risks?
- [ ] **MA2.1**: Non-AI alternatives considered?
- [ ] **MA2.3**: Unknown risk response procedures?
- [ ] **MA2.4**: Deactivation mechanisms in place?
- [ ] **MA3.1**: Third-party risks monitored?
- [ ] **MA4.1**: Post-deployment monitoring implemented?
- [ ] **MA4.3**: Incident communication and recovery documented?

### Step 6: Report Generation (20 minutes)

Compile assessment findings with ratings and recommendations.

---

## Output Format

Generate a comprehensive NIST AI RMF assessment report:

```markdown
# NIST AI RMF Assessment Report

**AI System**: [Name/Description]
**Organization**: [Name]
**Date**: [Date]
**Lifecycle Stage**: [Design/Development/Deployment/Monitoring]
**Evaluator**: [AI Agent or Human]
**AI RMF Version**: 1.0 (January 2023)

---

## Executive Summary

### Overall Risk Profile: [Low / Medium / High / Critical]

**System Type**: [Classifier / Generative / Recommender / Autonomous / Other]
**Deployment Context**: [Internal / Customer-facing / Public / Critical infrastructure]
**Regulatory Applicability**: [EU AI Act risk level, state laws, sector regulations]

### Key Findings
- **Total Issues**: [X]
  - Critical: [X] (immediate action required)
  - High: [X] (action required within 30 days)
  - Medium: [X] (action required within 90 days)
  - Low: [X] (improvements recommended)

### Trustworthiness Summary
| Characteristic | Status | Rating |
|---|---|---|
| Valid & Reliable | [Status] | [1-5] |
| Safe | [Status] | [1-5] |
| Secure & Resilient | [Status] | [1-5] |
| Accountable & Transparent | [Status] | [1-5] |
| Explainable & Interpretable | [Status] | [1-5] |
| Privacy-Enhanced | [Status] | [1-5] |
| Fair (Bias Managed) | [Status] | [1-5] |

---

## GOVERN Function Assessment

### GOVERN 1: Policies and Processes
**Rating**: [Not Implemented / Partial / Substantial / Full]

**Findings:**
- [Finding 1 with evidence]
- [Finding 2 with evidence]

**Gaps:**
- [ ] [Gap description]

**Recommendations:**
- [Recommendation with priority]

### GOVERN 2: Accountability Structures
**Rating**: [Not Implemented / Partial / Substantial / Full]

[Continue for all GOVERN categories...]

---

## MAP Function Assessment

### MAP 1: Context Established
**Rating**: [Not Implemented / Partial / Substantial / Full]

**Findings:**
- [Findings with evidence]

**Gaps:**
- [ ] [Gap description]

**Recommendations:**
- [Recommendation with priority]

[Continue for all MAP categories...]

---

## MEASURE Function Assessment

### MEASURE 1: Methods and Metrics
**Rating**: [Not Implemented / Partial / Substantial / Full]

**Findings:**
- [Findings with evidence]

**Gaps:**
- [ ] [Gap description]

**Recommendations:**
- [Recommendation with priority]

[Continue for all MEASURE categories...]

---

## MANAGE Function Assessment

### MANAGE 1: Risk Prioritization
**Rating**: [Not Implemented / Partial / Substantial / Full]

**Findings:**
- [Findings with evidence]

**Gaps:**
- [ ] [Gap description]

**Recommendations:**
- [Recommendation with priority]

[Continue for all MANAGE categories...]

---

## Risk Register

| ID | Risk Description | Function | Likelihood | Impact | Priority | Mitigation |
|---|---|---|---|---|---|---|
| R1 | [Description] | [G/M/ME/MA] | [L/M/H] | [L/M/H] | [P0-P3] | [Strategy] |
| R2 | [Description] | [G/M/ME/MA] | [L/M/H] | [L/M/H] | [P0-P3] | [Strategy] |

---

## Remediation Roadmap

### Phase 1: Critical (0-30 days)
1. [Action item with owner and deadline]
2. [Action item with owner and deadline]

### Phase 2: High Priority (30-90 days)
1. [Action item with owner and deadline]

### Phase 3: Medium Priority (90-180 days)
1. [Action item with owner and deadline]

### Phase 4: Continuous Improvement
1. [Ongoing practices]

---

## Compliance Alignment

### Regulatory Mapping
| Regulation | Relevant AI RMF Functions | Status |
|---|---|---|
| EU AI Act | GOVERN, MAP, MEASURE | [Status] |
| NIST CSF 2.0 | GOVERN, MANAGE | [Status] |
| State AI Laws | GOVERN, MAP | [Status] |
| Sector Regulations | [Relevant functions] | [Status] |

---

## Next Steps

### Immediate Actions
1. [ ] Address critical findings
2. [ ] Assign risk owners
3. [ ] Establish monitoring cadence

### Short-term (1-3 months)
1. [ ] Implement Phase 1 remediation
2. [ ] Establish governance structure
3. [ ] Train personnel on AI RMF

### Long-term (3-12 months)
1. [ ] Complete all remediation phases
2. [ ] Conduct follow-up assessment
3. [ ] Integrate into organizational risk management

---

## Resources

- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook)
- [NIST AI RMF Generative AI Profile](https://airc.nist.gov/Docs/1)
- [NIST Trustworthy AI Resource Center](https://airc.nist.gov/)

---

**Assessment Version**: 1.0
**Date**: [Date]
```

---

## Scoring Guide

Use this scale for subcategory ratings:

| Rating | Description |
|---|---|
| **Not Implemented** | No evidence of activity or documentation |
| **Partial** | Some activity but inconsistent or incomplete |
| **Substantial** | Mostly implemented with minor gaps |
| **Full** | Fully implemented and regularly maintained |

Use this scale for trustworthiness characteristics:

| Score | Description |
|---|---|
| **1** | Not addressed |
| **2** | Minimally addressed |
| **3** | Partially addressed |
| **4** | Substantially addressed |
| **5** | Fully addressed and monitored |

---

## Generative AI Considerations

For generative AI systems, additionally evaluate (per NIST AI 600-1 GenAI Profile, July 2024):

- **Content provenance**: Mechanisms to track AI-generated content origin
- **Confabulation risk**: Controls for hallucinated or fabricated outputs
- **Data privacy**: Training data protections and consent
- **Environmental impact**: Computational resource consumption
- **Information security**: Prompt injection and adversarial robustness
- **Harmful content**: Filters and safeguards for toxic or dangerous outputs
- **Third-party risks**: Foundation model and API dependencies
- **Human-AI interaction**: User awareness that they are interacting with AI

---

## Best Practices

1. **Start with GOVERN**: Establish governance before mapping risks
2. **Iterate continuously**: Risk management is ongoing, not one-time
3. **Engage stakeholders**: Include diverse perspectives in assessments
4. **Document everything**: Maintain evidence for accountability
5. **Align with existing frameworks**: Integrate with NIST CSF, ISO 42001, SOC 2
6. **Tailor to context**: Adapt depth of assessment to system risk level
7. **Test in production**: Monitor deployed systems, not just pre-deployment
8. **Plan for failure**: Have incident response and decommissioning procedures
9. **Consider societal impact**: Look beyond organizational risks
10. **Stay current**: Monitor evolving AI regulations and standards

---

## Version

1.0 - Initial release (NIST AI RMF 1.0 compliant)

---

**Remember**: The NIST AI RMF is voluntary and risk-based. Not all subcategories apply to every system. Tailor the assessment depth to the system's risk profile and organizational context.
