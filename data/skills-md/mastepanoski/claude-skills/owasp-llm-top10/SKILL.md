---
name: owasp-llm-top10
description: Security audit for LLM and GenAI applications using OWASP Top 10 for LLM Apps 2025. Assess prompt injection, data leakage, supply chain, and 7 more critical vulnerabilities.
---

# OWASP Top 10 for LLM Applications Security Audit

This skill enables AI agents to perform a comprehensive **security assessment** of Large Language Model (LLM) and Generative AI applications using the **OWASP Top 10 for LLM Applications 2025**, published by the OWASP GenAI Security Project.

The OWASP Top 10 for LLM Applications identifies the most critical security risks in systems that integrate large language models, covering vulnerabilities from prompt injection to unbounded resource consumption. This is the authoritative industry standard for LLM application security.

Use this skill to identify security vulnerabilities, assess risk exposure, prioritize remediation, and establish secure development practices for AI-powered applications.

Combine with "NIST AI RMF" for comprehensive risk management or "ISO 42001 AI Governance" for governance compliance.

## When to Use This Skill

Invoke this skill when:
- Auditing security of LLM-powered applications before deployment
- Reviewing GenAI integrations for security vulnerabilities
- Assessing RAG (Retrieval-Augmented Generation) systems
- Evaluating chatbot or AI assistant security
- Conducting penetration testing of AI features
- Building secure AI application architectures
- Reviewing third-party AI API integrations
- Preparing for security compliance reviews
- Responding to AI-related security incidents

## Inputs Required

When executing this audit, gather:

- **application_description**: Description of the AI application (purpose, LLM used, architecture, features, user base) [REQUIRED]
- **architecture_details**: System architecture (APIs, databases, vector stores, plugins, integrations) [OPTIONAL but recommended]
- **llm_provider**: LLM provider and model (OpenAI GPT-4, Anthropic Claude, self-hosted, etc.) [OPTIONAL]
- **deployment_context**: Deployment environment (cloud, on-premise, hybrid, edge) [OPTIONAL]
- **data_sensitivity**: Types of data processed (PII, financial, health, proprietary) [OPTIONAL]
- **existing_controls**: Current security measures (auth, rate limiting, content filtering) [OPTIONAL]
- **specific_concerns**: Known vulnerabilities or areas of focus [OPTIONAL]

---

## The OWASP Top 10 for LLM Applications (2025)

### LLM01: Prompt Injection

**Severity**: Critical

**Description**: Attackers manipulate LLM operations through crafted inputs, either directly or indirectly, to bypass intended functionality, access unauthorized data, or trigger unintended actions.

**Attack Vectors:**
- **Direct injection**: Malicious user prompts containing override commands
- **Indirect injection**: Hidden instructions in external content (web pages, documents, emails) processed by the LLM
- **Jailbreaks**: Techniques to bypass safety constraints and content policies

**Impact:**
- Unauthorized data access and exfiltration
- Bypass of content safety filters
- Manipulation of downstream system actions
- Social engineering of users through manipulated outputs

**Assessment Checklist:**
- [ ] Input sanitization and validation implemented
- [ ] System prompts separated from user inputs with clear delimiters
- [ ] Least privilege applied to LLM backend access
- [ ] Output validation before downstream actions
- [ ] Human-in-the-loop for critical operations
- [ ] Adversarial testing conducted with known injection techniques
- [ ] Content filtering layers applied pre- and post-LLM

**Mitigation Strategies:**
1. Enforce privilege controls on LLM backend access
2. Segregate external content from user prompts
3. Maintain human oversight for critical functions
4. Implement input/output validation pipelines
5. Conduct regular adversarial testing

---

### LLM02: Sensitive Information Disclosure

**Severity**: Critical

**Description**: LLMs inadvertently expose confidential data including PII, proprietary algorithms, credentials, intellectual property, or internal system information through their outputs.

**Attack Vectors:**
- Crafted prompts designed to extract training data
- Legitimate queries that trigger memorized sensitive content
- Model outputs revealing internal system architecture
- Embedding leakage from vector databases

**Impact:**
- Privacy violations and regulatory non-compliance (GDPR, CCPA)
- Intellectual property theft
- Credential exposure enabling further attacks
- Reputational damage

**Assessment Checklist:**
- [ ] PII and sensitive data removed from training/fine-tuning data
- [ ] Data masking and tokenization in logs and outputs
- [ ] System instructions forbidding sensitive disclosures
- [ ] Output filtering for known sensitive patterns (SSN, credit cards, API keys)
- [ ] Model access restricted to necessary information via middleware
- [ ] User education against pasting confidential content
- [ ] Output monitoring for anomalous data exposure

**Mitigation Strategies:**
1. Sanitize training data to remove sensitive information
2. Implement data loss prevention (DLP) on outputs
3. Apply access controls limiting model's data reach
4. Monitor outputs for sensitive data patterns
5. Use differential privacy techniques in training

---

### LLM03: Supply Chain Vulnerabilities

**Severity**: High

**Description**: Compromised third-party components (models, datasets, libraries, plugins) introduce security risks including malware, backdoors, or biased behavior.

**Attack Vectors:**
- Malicious pre-trained models from public repositories
- Poisoned datasets with embedded triggers
- Vulnerable ML libraries and dependencies
- Compromised plugins with unauthorized access
- Trojanized fine-tuning adapters

**Impact:**
- System compromise and data theft
- Backdoor access to production systems
- Model corruption affecting all users
- Legal liability from unlicensed content

**Assessment Checklist:**
- [ ] Models sourced from verified, reputable providers
- [ ] Digital signatures and checksums verified
- [ ] Model files scanned for suspicious code (picklescan, etc.)
- [ ] Third-party models deployed in sandboxed environments
- [ ] Dependencies regularly updated and audited
- [ ] Plugin permissions restricted with allowlists
- [ ] Complete inventory of all models and components maintained
- [ ] SBOM (Software Bill of Materials) maintained for AI components

**Mitigation Strategies:**
1. Source models only from trusted, verified providers
2. Scan model files for malicious code before deployment
3. Sandbox third-party models with restricted permissions
4. Maintain updated dependency inventory
5. Implement model signing and integrity verification

---

### LLM04: Data and Model Poisoning

**Severity**: High

**Description**: Attackers manipulate training or fine-tuning data to introduce vulnerabilities, backdoors, or biases that compromise model security and reliability.

**Attack Vectors:**
- Crafted training examples with hidden trigger phrases
- Poisoned web-scraped content absorbed during training
- Direct tampering with model weights or parameters
- Malicious fine-tuning data
- Subtle label manipulation or data anomalies

**Impact:**
- Biased or degraded model outputs
- Trigger-activated backdoors in production
- Erosion of model trustworthiness
- Long-term hidden threats difficult to detect

**Assessment Checklist:**
- [ ] Training data validated, cleaned, and audited
- [ ] Data provenance tracked and documented
- [ ] Rate limiting and moderation for crowdsourced data
- [ ] Differential privacy techniques applied
- [ ] Models tested with known trigger phrases before deployment
- [ ] Deployed models monitored for behavioral drift
- [ ] Model file checksums verified against known-good states

**Mitigation Strategies:**
1. Validate and clean all training data sources
2. Implement data provenance tracking
3. Apply differential privacy to limit individual data influence
4. Test with adversarial inputs before deployment
5. Monitor production models for unexpected behavior

---

### LLM05: Improper Output Handling

**Severity**: High

**Description**: Applications blindly execute or render LLM outputs without validation, enabling code injection, XSS, SQL injection, SSRF, and other attacks.

**Attack Vectors:**
- Unescaped HTML/JavaScript in outputs (XSS)
- Model-generated shell commands executed without sanitization
- SQL queries constructed from model output
- Unsanitized API calls based on AI suggestions
- Direct execution via eval() or exec()

**Impact:**
- Remote code execution
- Session hijacking
- Database manipulation
- Privilege escalation
- Full system compromise

**Assessment Checklist:**
- [ ] All LLM output treated as untrusted input
- [ ] Strict output schema validation enforced (JSON, formats)
- [ ] Output sanitized and escaped based on context (HTML, SQL, shell)
- [ ] Parameterized queries used instead of raw SQL
- [ ] Allowlists for acceptable output patterns
- [ ] Generated code executed in sandboxed environments
- [ ] Human approval required for high-impact actions
- [ ] Rendering libraries with built-in escaping used

**Mitigation Strategies:**
1. Never trust LLM output; validate and sanitize everything
2. Enforce strict output schemas
3. Use parameterized queries and safe ORM methods
4. Sandbox all code execution
5. Require human approval for privileged operations

---

### LLM06: Excessive Agency

**Severity**: High

**Description**: AI agents possess excessive permissions and autonomous capabilities, enabling significant harm through compromised prompts, hallucinations, or malicious manipulation.

**Attack Vectors:**
- Prompt injection exploiting overly permissioned agents
- Hallucinations triggering unintended high-impact actions
- Confused deputy attacks using AI's elevated privileges
- Malicious plugins with excessive access
- Unrestricted system control (email, API, database)

**Impact:**
- Unauthorized data transmission
- Destructive actions (deletion, modification)
- Financial loss through unauthorized transactions
- Service disruptions
- Automated attack amplification

**Assessment Checklist:**
- [ ] Principle of least privilege applied to all AI capabilities
- [ ] Granular permissions with limited-scope OAuth tokens
- [ ] Functionality compartmentalized across narrow-scope agents
- [ ] High-risk actions restricted (deletion, transfers, device control)
- [ ] Explicit user approval for significant operations
- [ ] Rate limiting on AI actions and API calls
- [ ] Comprehensive audit logs of all agent activities
- [ ] Monitoring with alerts for anomalous behavior

**Mitigation Strategies:**
1. Grant only essential capabilities (least privilege)
2. Compartmentalize agent functionality
3. Require human approval for high-impact operations
4. Implement comprehensive audit logging
5. Set up real-time monitoring and anomaly detection

---

### LLM07: System Prompt Leakage

**Severity**: Medium

**Description**: System instructions intended to guide AI behavior are exposed to users or attackers, revealing internal logic, security controls, or sensitive configurations.

**Attack Vectors:**
- Prompt injection requesting instruction disclosure
- Sophisticated probing asking to repeat conversation context
- Tokenization quirks causing unintended disclosure
- Reverse-engineering through behavioral observation
- Model unintentionally echoing system prompts

**Impact:**
- Security logic exposure enabling bypass attacks
- Credential compromise if secrets embedded in prompts
- Internal system knowledge revelation
- Facilitation of more targeted attacks

**Assessment Checklist:**
- [ ] No passwords, API keys, or secrets in system prompts
- [ ] Prompts treated as public information
- [ ] Models configured to refuse revealing system messages
- [ ] Clear message role delimiters (system/user/assistant)
- [ ] Security policies enforced at application level, not prompt level
- [ ] Output monitoring for prompt leakage patterns
- [ ] Regular testing with known extraction techniques

**Mitigation Strategies:**
1. Never embed sensitive data in system prompts
2. Implement application-level security enforcement
3. Configure models to refuse prompt disclosure
4. Monitor outputs for leakage patterns
5. Use structured message formats with role delimiters

---

### LLM08: Vector and Embedding Weaknesses

**Severity**: Medium

**Description**: Vulnerabilities in vector databases and embedding-based retrieval systems (RAG) allow poisoning, injection, or unauthorized access to stored data.

**Attack Vectors:**
- Poisoned embeddings retrieved during RAG operations
- Direct injection of malicious vectors into stores
- Retrieval of sensitive data from improperly secured databases
- Metadata-based attacks exploiting insufficient filtering
- Similarity-based retrieval returning harmful content

**Impact:**
- Output manipulation through poisoned context
- Sensitive data leakage from vector stores
- Misinformation injection
- Compromised RAG system integrity

**Assessment Checklist:**
- [ ] Data validated and sanitized before vectorization
- [ ] Access controls on vector store insertion and modification
- [ ] Metadata filtering restricts retrieval to appropriate categories
- [ ] Monitoring for suspicious bulk insertions
- [ ] Similarity thresholds ensuring relevant retrieval
- [ ] Sensitive and public vector stores separated
- [ ] Embedding source provenance tracked
- [ ] Anomaly detection for unusual retrieval patterns

**Mitigation Strategies:**
1. Validate data before storing in vector databases
2. Implement strict access controls on vector operations
3. Use metadata filtering and similarity thresholds
4. Separate sensitive and public data stores
5. Monitor for anomalous patterns

---

### LLM09: Misinformation

**Severity**: Medium

**Description**: LLMs generate plausible but false information (hallucinations/confabulations) that users may trust and act upon, causing harm.

**Attack Vectors:**
- Fabricated facts presented authoritatively
- Fake citations or references that don't exist
- Invented case law, medical advice, or technical solutions
- Adversarial prompts designed to trigger hallucinations
- Confident incorrect reasoning

**Impact:**
- Harmful decisions based on false information
- Legal liability from incorrect advice
- Erosion of trust in AI systems
- Regulatory violations in compliance contexts
- Reputational damage

**Assessment Checklist:**
- [ ] Confidence scores or uncertainty indicators provided
- [ ] Fact-checking against reliable databases implemented
- [ ] Citations with verifiable sources required for sensitive domains
- [ ] RAG grounding responses in validated data
- [ ] System instructions encourage admitting uncertainty
- [ ] Human review for critical outputs
- [ ] Model limitations clearly communicated to users

**Mitigation Strategies:**
1. Implement retrieval-augmented generation (RAG) for grounding
2. Provide confidence indicators to users
3. Require verifiable citations for critical domains
4. Add human review for high-stakes outputs
5. Clearly communicate model limitations

---

### LLM10: Unbounded Consumption

**Severity**: Medium

**Description**: Uncontrolled LLM usage causes denial-of-service, system crashes, or excessive operational costs through resource exhaustion.

**Attack Vectors:**
- Flood of queries overwhelming API endpoints
- Extremely long or recursive prompts consuming resources
- Infinite loops through recursive prompt injection
- Distributed attacks with massive input volumes
- Cascading failures through connected systems

**Impact:**
- Service unavailability for legitimate users
- Financial loss from excessive token usage
- System crashes and performance degradation
- Infrastructure damage

**Assessment Checklist:**
- [ ] Rate limiting per user, IP, and API key
- [ ] Maximum token limits for requests and daily usage
- [ ] Resource consumption monitoring with alerting
- [ ] Request timeouts preventing hung operations
- [ ] Per-user quotas with cost implications
- [ ] Cost monitoring with automated budget alerts
- [ ] Load balancing across infrastructure
- [ ] Auto-scaling with cost-aware limits

**Mitigation Strategies:**
1. Implement rate limiting at multiple levels
2. Set token and cost limits per user/session
3. Monitor resource consumption with alerts
4. Use request timeouts and queue management
5. Design auto-scaling with cost guardrails

---

## Audit Procedure

### Step 1: Application Understanding (15 minutes)

1. **System inventory:**
   - Document LLM provider, model version, and configuration
   - Map application architecture (APIs, databases, vector stores)
   - Identify all data flows to and from the LLM
   - List plugins, tools, and integrations

2. **Threat modeling:**
   - Identify attack surfaces (user inputs, APIs, data sources)
   - Determine data sensitivity classification
   - Map trust boundaries between components
   - Identify privileged operations the LLM can trigger

### Step 2: Vulnerability Assessment (40-60 minutes)

For each of the 10 vulnerabilities, assess:

#### Prompt Injection (LLM01) - 10 min
- [ ] Test with known injection techniques (direct and indirect)
- [ ] Attempt to override system instructions
- [ ] Test with malicious content in external data sources
- [ ] Verify input validation and sanitization

#### Sensitive Information Disclosure (LLM02) - 5 min
- [ ] Attempt to extract training data
- [ ] Test for PII leakage in outputs
- [ ] Check for credential or API key exposure
- [ ] Verify output filtering effectiveness

#### Supply Chain (LLM03) - 5 min
- [ ] Review model provenance and source
- [ ] Check dependency versions and vulnerability status
- [ ] Verify plugin and integration security
- [ ] Review SBOM completeness

#### Data/Model Poisoning (LLM04) - 5 min
- [ ] Review data pipeline security
- [ ] Check fine-tuning data validation
- [ ] Verify model integrity monitoring
- [ ] Test with known trigger patterns

#### Improper Output Handling (LLM05) - 10 min
- [ ] Test for XSS through LLM outputs
- [ ] Attempt SQL injection via model responses
- [ ] Check command injection possibilities
- [ ] Verify output sanitization and encoding

#### Excessive Agency (LLM06) - 5 min
- [ ] Review agent permissions and capabilities
- [ ] Test privilege boundaries
- [ ] Verify human-in-the-loop for critical actions
- [ ] Check audit logging completeness

#### System Prompt Leakage (LLM07) - 5 min
- [ ] Attempt to extract system prompts
- [ ] Check for secrets in prompts
- [ ] Verify prompt protection mechanisms

#### Vector/Embedding Weaknesses (LLM08) - 5 min
- [ ] Review vector store access controls
- [ ] Test RAG retrieval for injection
- [ ] Verify data separation and filtering

#### Misinformation (LLM09) - 5 min
- [ ] Test for hallucination in critical domains
- [ ] Verify grounding and citation mechanisms
- [ ] Check confidence indicators

#### Unbounded Consumption (LLM10) - 5 min
- [ ] Test rate limiting effectiveness
- [ ] Verify token and cost limits
- [ ] Check timeout configurations

### Step 3: Risk Scoring (15 minutes)

For each vulnerability found, score using:

**Likelihood**: How likely is exploitation?
- **High**: Known attack vectors, easy to exploit, publicly accessible
- **Medium**: Requires some skill or specific conditions
- **Low**: Difficult to exploit, limited attack surface

**Impact**: What is the potential damage?
- **Critical**: System compromise, major data breach, significant financial loss
- **High**: Unauthorized access, data exposure, service disruption
- **Medium**: Limited data exposure, partial service impact
- **Low**: Minor information disclosure, minimal impact

### Step 4: Report Generation (20 minutes)

Compile comprehensive security assessment.

---

## Output Format

Generate a comprehensive OWASP LLM security audit report:

```markdown
# OWASP LLM Top 10 Security Audit Report

**Application**: [Name]
**LLM Provider/Model**: [Provider - Model]
**Date**: [Date]
**Evaluator**: [AI Agent or Human]
**OWASP LLM Top 10 Version**: 2025

---

## Executive Summary

### Overall Security Posture: [Critical / High Risk / Medium Risk / Low Risk / Secure]

**Application Type**: [Chatbot / Agent / RAG System / Content Generator / Code Assistant / Other]
**Data Sensitivity**: [Public / Internal / Confidential / Restricted]
**User Base**: [Internal / B2B / B2C / Public]

### Critical Findings
| # | Vulnerability | Severity | Status |
|---|---|---|---|
| LLM01 | Prompt Injection | Critical | [Vulnerable / Mitigated / N/A] |
| LLM02 | Sensitive Info Disclosure | Critical | [Vulnerable / Mitigated / N/A] |
| LLM03 | Supply Chain | High | [Vulnerable / Mitigated / N/A] |
| LLM04 | Data/Model Poisoning | High | [Vulnerable / Mitigated / N/A] |
| LLM05 | Improper Output Handling | High | [Vulnerable / Mitigated / N/A] |
| LLM06 | Excessive Agency | High | [Vulnerable / Mitigated / N/A] |
| LLM07 | System Prompt Leakage | Medium | [Vulnerable / Mitigated / N/A] |
| LLM08 | Vector/Embedding Weaknesses | Medium | [Vulnerable / Mitigated / N/A] |
| LLM09 | Misinformation | Medium | [Vulnerable / Mitigated / N/A] |
| LLM10 | Unbounded Consumption | Medium | [Vulnerable / Mitigated / N/A] |

### Top 3 Critical Issues
1. [Issue] - [Impact description]
2. [Issue] - [Impact description]
3. [Issue] - [Impact description]

---

## Detailed Findings

### LLM01: Prompt Injection
**Status**: [Vulnerable / Partially Mitigated / Mitigated]
**Severity**: [Critical / High / Medium / Low]
**Likelihood**: [High / Medium / Low]

**Findings:**
1. [Finding with evidence]
2. [Finding with evidence]

**Attack Scenario:**
[Description of how this could be exploited]

**Recommendations:**
1. [Specific remediation step]
2. [Specific remediation step]

**Effort**: [Low / Medium / High]

---

[Continue for LLM02 through LLM10...]

---

## Architecture Security Review

### Data Flow Analysis
[Diagram or description of data flows with trust boundaries marked]

### Attack Surface Summary
| Surface | Risk Level | Controls |
|---|---|---|
| User Input | [Level] | [Controls] |
| API Endpoints | [Level] | [Controls] |
| Vector Store | [Level] | [Controls] |
| Plugins/Tools | [Level] | [Controls] |
| Output Rendering | [Level] | [Controls] |

---

## Remediation Roadmap

### Phase 1: Critical (0-7 days)
1. [ ] [Action item with owner]
2. [ ] [Action item with owner]

### Phase 2: High Priority (7-30 days)
1. [ ] [Action item with owner]

### Phase 3: Medium Priority (30-90 days)
1. [ ] [Action item with owner]

### Phase 4: Hardening (Ongoing)
1. [ ] [Continuous improvement practices]

---

## Security Controls Matrix

| Control | Implemented | Effective | Recommendation |
|---|---|---|---|
| Input validation | [Yes/No/Partial] | [Yes/No] | [Recommendation] |
| Output sanitization | [Yes/No/Partial] | [Yes/No] | [Recommendation] |
| Rate limiting | [Yes/No/Partial] | [Yes/No] | [Recommendation] |
| Authentication | [Yes/No/Partial] | [Yes/No] | [Recommendation] |
| Authorization | [Yes/No/Partial] | [Yes/No] | [Recommendation] |
| Logging/Monitoring | [Yes/No/Partial] | [Yes/No] | [Recommendation] |
| Content filtering | [Yes/No/Partial] | [Yes/No] | [Recommendation] |
| Human-in-the-loop | [Yes/No/Partial] | [Yes/No] | [Recommendation] |

---

## Next Steps

1. [ ] Prioritize and assign critical findings
2. [ ] Implement quick wins (input validation, rate limiting)
3. [ ] Schedule penetration testing for high-risk areas
4. [ ] Establish continuous monitoring
5. [ ] Plan follow-up audit after remediation

---

## Resources

- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [OWASP LLM AI Security & Governance Checklist](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP GitHub Repository](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications)

---

**Audit Version**: 1.0
**Date**: [Date]
```

---

## Quick Reference: Vulnerability Priority

| Priority | Vulnerabilities | Rationale |
|---|---|---|
| **P0** | LLM01 (Prompt Injection), LLM02 (Data Disclosure) | Direct exploitation, high impact |
| **P1** | LLM05 (Output Handling), LLM06 (Excessive Agency) | System compromise potential |
| **P2** | LLM03 (Supply Chain), LLM04 (Poisoning) | Harder to exploit but severe impact |
| **P3** | LLM07 (Prompt Leakage), LLM08 (Vector Weaknesses) | Enables further attacks |
| **P4** | LLM09 (Misinformation), LLM10 (Unbounded Consumption) | Operational risk |

---

## Best Practices

1. **Defense in depth**: Never rely on a single security control
2. **Zero trust for LLM output**: Treat all model output as untrusted
3. **Least privilege**: Minimize AI agent permissions and capabilities
4. **Monitor continuously**: Log and alert on anomalous AI behavior
5. **Test adversarially**: Regular red-team exercises against AI features
6. **Secure the pipeline**: Protect training data, models, and embeddings
7. **Human oversight**: Maintain human-in-the-loop for critical operations
8. **Update regularly**: Stay current with evolving attack techniques
9. **Educate users**: Train users on safe AI interaction practices
10. **Plan for incidents**: Have AI-specific incident response procedures

---

## Version

1.0 - Initial release (OWASP Top 10 for LLM Applications 2025)

---

**Remember**: LLM security is an evolving field. New attack vectors emerge regularly. This audit provides a baseline assessment; continuous monitoring and periodic re-assessment are essential for maintaining security posture.
