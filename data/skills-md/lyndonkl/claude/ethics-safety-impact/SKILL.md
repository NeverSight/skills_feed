---
name: ethics-safety-impact
description: Use when decisions could affect groups differently and need to anticipate harms/benefits, assess fairness and safety concerns, identify vulnerable populations, propose risk mitigations, define monitoring metrics, or when user mentions ethical review, impact assessment, differential harm, safety analysis, vulnerable groups, bias audit, or responsible AI/tech.
---
# Ethics, Safety & Impact Assessment

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Ethics, Safety & Impact Assessment provides a structured framework for identifying potential harms, benefits, and differential impacts before launching features, implementing policies, or making decisions that affect people. This skill guides you through stakeholder identification, harm/benefit analysis, fairness evaluation, risk mitigation design, and ongoing monitoring to ensure responsible and equitable outcomes.

## When to Use

Use this skill when:

- **Product launches**: New features, algorithm changes, UI redesigns that affect user experience or outcomes
- **Policy decisions**: Terms of service updates, content moderation rules, data usage policies, pricing changes
- **Data & AI systems**: Training models, deploying algorithms, using sensitive data, automated decision-making
- **Platform changes**: Recommendation systems, search ranking, feed algorithms, matching/routing logic
- **Access & inclusion**: Features affecting accessibility, vulnerable populations, underrepresented groups, global markets
- **Safety-critical systems**: Health, finance, transportation, security applications where errors have serious consequences
- **High-stakes decisions**: Hiring, lending, admissions, criminal justice, insurance where outcomes significantly affect lives
- **Content & communication**: Moderation policies, fact-checking systems, content ranking, amplification rules

Trigger phrases: "ethical review", "impact assessment", "who might be harmed", "differential impact", "vulnerable populations", "bias audit", "fairness check", "safety analysis", "responsible AI", "unintended consequences"

## What Is It?

Ethics, Safety & Impact Assessment is a proactive evaluation framework that systematically examines:
- **Who** is affected (stakeholder mapping, vulnerable groups)
- **What** could go wrong (harm scenarios, failure modes)
- **Why** it matters (severity, likelihood, distribution of impacts)
- **How** to mitigate (design changes, safeguards, monitoring)
- **When** to escalate (triggers, thresholds, review processes)

**Core ethical principles:**
- **Fairness**: Equal treatment, non-discrimination, equitable outcomes across groups
- **Autonomy**: User choice, informed consent, control over data and experience
- **Beneficence**: Maximize benefits, design for positive impact
- **Non-maleficence**: Minimize harms, "do no harm" as baseline
- **Transparency**: Explain decisions, disclose limitations, build trust
- **Accountability**: Clear ownership, redress mechanisms, audit trails
- **Privacy**: Data protection, confidentiality, purpose limitation
- **Justice**: Equitable distribution of benefits and burdens, address historical inequities

**Quick example:**

**Scenario**: Launching credit scoring algorithm for loan approvals

**Ethical impact assessment**:

1. **Stakeholders affected**: Loan applicants (diverse demographics), lenders, society (economic mobility)

2. **Potential harms**:
   - **Disparate impact**: Algorithm trained on historical data may perpetuate bias against protected groups (race, gender, age)
   - **Opacity**: Applicants denied loans without explanation, cannot contest decision
   - **Feedback loops**: Denying loans to disadvantaged groups → lack of credit history → continued denials
   - **Economic harm**: Incorrect denials prevent wealth building, perpetuate poverty

3. **Vulnerable groups**: Racial minorities historically discriminated in lending, immigrants with thin credit files, young adults, people in poverty

4. **Mitigations**:
   - **Fairness audit**: Test for disparate impact across protected classes, equalized odds
   - **Explainability**: Provide reason codes (top 3 factors), allow appeals
   - **Alternative data**: Include rent, utility payments to expand access
   - **Human review**: Flag edge cases for manual review, override capability
   - **Regular monitoring**: Track approval rates by demographic, quarterly bias audits

5. **Monitoring & escalation**:
   - **Metrics**: Approval rate parity (within 10% across groups), false positive/negative rates, appeal overturn rate
   - **Triggers**: If disparate impact >20%, escalate to ethics committee
   - **Review**: Quarterly fairness audits, annual independent assessment

## Workflow

Copy this checklist and track your progress:

```
Ethics & Safety Assessment Progress:
- [ ] Step 1: Map stakeholders and identify vulnerable groups
- [ ] Step 2: Analyze potential harms and benefits
- [ ] Step 3: Assess fairness and differential impacts
- [ ] Step 4: Evaluate severity and likelihood
- [ ] Step 5: Design mitigations and safeguards
- [ ] Step 6: Define monitoring and escalation protocols
```

**Step 1: Map stakeholders and identify vulnerable groups**

Identify all affected parties (direct users, indirect, society). Prioritize vulnerable populations most at risk. See [resources/template.md](resources/template.md#stakeholder-mapping-template) for stakeholder analysis framework.

**Step 2: Analyze potential harms and benefits**

Brainstorm what could go wrong (harms) and what value is created (benefits) for each stakeholder group. See [resources/template.md](resources/template.md#harm-benefit-analysis-template) for structured analysis.

**Step 3: Assess fairness and differential impacts**

Evaluate whether outcomes, treatment, or access differ across groups. Check for disparate impact. See [resources/methodology.md](resources/methodology.md#fairness-metrics) for fairness criteria and measurement.

**Step 4: Evaluate severity and likelihood**

Score each harm on severity (1-5) and likelihood (1-5), prioritize high-risk combinations. See [resources/template.md](resources/template.md#risk-matrix-template) for prioritization framework.

**Step 5: Design mitigations and safeguards**

For high-priority harms, propose design changes, policy safeguards, oversight mechanisms. See [resources/methodology.md](resources/methodology.md#mitigation-strategies) for intervention types.

**Step 6: Define monitoring and escalation protocols**

Set metrics, thresholds, review cadence, escalation triggers. Validate using [resources/evaluators/rubric_ethics_safety_impact.json](resources/evaluators/rubric_ethics_safety_impact.json). **Minimum standard**: Average score ≥ 3.5.

## Common Patterns

**Pattern 1: Algorithm Fairness Audit**
- **Stakeholders**: Users receiving algorithmic decisions (hiring, lending, content ranking), protected groups
- **Harms**: Disparate impact (bias against protected classes), feedback loops amplifying inequality, opacity preventing accountability
- **Assessment**: Test for demographic parity, equalized odds, calibration across groups; analyze training data for historical bias
- **Mitigations**: Debiasing techniques, fairness constraints, explainability, human review for edge cases, regular audits
- **Monitoring**: Disparate impact ratio, false positive/negative rates by group, user appeals and overturn rates

**Pattern 2: Data Privacy & Consent**
- **Stakeholders**: Data subjects (users whose data is collected), vulnerable groups (children, marginalized communities)
- **Harms**: Privacy violations, surveillance, data breaches, lack of informed consent, secondary use without permission, re-identification risk
- **Assessment**: Map data flows (collection → storage → use → sharing), identify sensitive attributes (PII, health, location), consent adequacy
- **Mitigations**: Data minimization (collect only necessary), anonymization/differential privacy, granular consent, user data controls (export, delete), encryption
- **Monitoring**: Breach incidents, data access logs, consent withdrawal rates, user data requests (GDPR, CCPA)

**Pattern 3: Content Moderation & Free Expression**
- **Stakeholders**: Content creators, viewers, vulnerable groups (targets of harassment), society (information integrity)
- **Harms**: Over-moderation (silencing legitimate speech, especially marginalized voices), under-moderation (allowing harm, harassment, misinformation), inconsistent enforcement
- **Assessment**: Analyze moderation error rates (false positives/negatives), differential enforcement across groups, cultural context sensitivity
- **Mitigations**: Clear policies with examples, appeals process, human review, diverse moderators, cultural context training, transparency reports
- **Monitoring**: Moderation volume and error rates by category, appeal overturn rates, disparate enforcement across languages/regions

**Pattern 4: Accessibility & Inclusive Design**
- **Stakeholders**: Users with disabilities (visual, auditory, motor, cognitive), elderly, low-literacy, low-bandwidth users
- **Harms**: Exclusion (cannot use product), degraded experience, safety risks (cannot access critical features), digital divide
- **Assessment**: WCAG compliance audit, assistive technology testing, user research with diverse abilities, cross-cultural usability
- **Mitigations**: Accessible design (WCAG AA/AAA), alt text, keyboard navigation, screen reader support, low-bandwidth mode, multi-language, plain language
- **Monitoring**: Accessibility test coverage, user feedback from disability communities, task completion rates across abilities

**Pattern 5: Safety-Critical Systems**
- **Stakeholders**: End users (patients, drivers, operators), vulnerable groups (children, elderly, compromised health), public safety
- **Harms**: Physical harm (injury, death), psychological harm (trauma), property damage, cascade failures affecting many
- **Assessment**: Failure mode analysis (FMEA), fault tree analysis, worst-case scenarios, edge cases that break assumptions
- **Mitigations**: Redundancy, fail-safes, human oversight, rigorous testing (stress, chaos, adversarial), incident response plans, staged rollouts
- **Monitoring**: Error rates, near-miss incidents, safety metrics (accidents, adverse events), user-reported issues, compliance audits

## Guardrails

**Critical requirements:**

1. **Identify vulnerable groups explicitly**: Not all stakeholders are equally at risk. Prioritize: children, elderly, people with disabilities, marginalized/discriminated groups, low-income, low-literacy, geographically isolated, politically targeted. If none identified, you're probably missing them.

2. **Consider second-order and long-term effects**: First-order obvious harms are just the start. Look for: feedback loops (harm → disadvantage → more harm), normalization (practice becomes standard), precedent (enables worse future behavior), accumulation (small harms compound over time). Ask "what happens next?"

3. **Assess differential impact, not just average**: Feature may help average user but harm specific groups. Metrics: disparate impact (outcome differences across groups >20% = red flag), intersectionality (combinations of identities may face unique harms), distributive justice (who gets benefits vs. burdens?).

4. **Design mitigations before launch, not after harm**: Reactive fixes are too late for those already harmed. Proactive: Build safeguards into design, test with diverse users, staged rollout with monitoring, kill switches, pre-commit to audits. "Move fast and break things" is unethical for systems affecting people's lives.

5. **Provide transparency and recourse**: People affected have right to know and contest. Minimum: Explain decisions (what factors, why outcome), Appeal mechanism (human review, overturn if wrong), Redress (compensate harm), Audit trails (investigate complaints). Opacity is often a sign of hidden bias or risk.

6. **Monitor outcomes, not just intentions**: Good intentions don't prevent harm. Measure actual impacts: outcome disparities by group, user-reported harms, error rates and their distribution, unintended consequences. Set thresholds that trigger review/shutdown.

7. **Establish clear accountability and escalation**: Assign ownership. Define: Who reviews ethics risks before launch? Who monitors post-launch? What triggers escalation? Who can halt harmful features? Document decisions and rationale for later review.

8. **Respect autonomy and consent**: Users deserve: Informed choice (understand what they're agreeing to, in plain language), Meaningful alternatives (consent not coerced), Control (opt out, delete data, configure settings), Purpose limitation (data used only for stated purpose). Children and vulnerable groups need extra protections.

**Common pitfalls:**

- ❌ **Assuming "we treat everyone the same" = fairness**: Equal treatment of unequal groups perpetuates inequality. Fairness often requires differential treatment.
- ❌ **Optimization without constraints**: Maximizing engagement/revenue unconstrained leads to amplifying outrage, addiction, polarization. Set ethical boundaries.
- ❌ **Moving fast and apologizing later**: For safety/ethics, prevention > apology. Harms to vulnerable groups are not acceptable experiments.
- ❌ **Privacy theater**: Requiring consent without explaining risks, or making consent mandatory for service, is not meaningful consent.
- ❌ **Sampling bias in testing**: Testing only on employees (young, educated, English-speaking) misses how diverse users experience harm.
- ❌ **Ethics washing**: Performative statements without material changes. Impact assessments must change decisions, not just document them.

## Quick Reference

**Key resources:**

- **[resources/template.md](resources/template.md)**: Stakeholder mapping, harm/benefit analysis, risk matrix, mitigation planning, monitoring framework
- **[resources/methodology.md](resources/methodology.md)**: Fairness metrics, privacy analysis, safety assessment, bias detection, participatory design
- **[resources/evaluators/rubric_ethics_safety_impact.json](resources/evaluators/rubric_ethics_safety_impact.json)**: Quality criteria for stakeholder analysis, harm identification, mitigation design, monitoring

**Stakeholder Priorities:**

High-risk groups to always consider:
- Children (<18, especially <13)
- People with disabilities (visual, auditory, motor, cognitive)
- Racial/ethnic minorities, especially historically discriminated groups
- Low-income, unhoused, financially precarious
- LGBTQ+, especially in hostile jurisdictions
- Elderly (>65), especially digitally less-skilled
- Non-English speakers, low-literacy
- Political dissidents, activists, journalists in repressive contexts
- Refugees, immigrants, undocumented
- Mentally ill, cognitively impaired

**Harm Categories:**

- **Physical**: Injury, death, health deterioration
- **Psychological**: Trauma, stress, anxiety, depression, addiction
- **Economic**: Lost income, debt, poverty, exclusion from opportunity
- **Social**: Discrimination, harassment, ostracism, loss of relationships
- **Autonomy**: Coercion, manipulation, loss of control, dignity violation
- **Privacy**: Surveillance, exposure, data breach, re-identification
- **Reputational**: Stigma, defamation, loss of standing
- **Epistemic**: Misinformation, loss of knowledge access, filter bubbles
- **Political**: Disenfranchisement, censorship, targeted repression

**Fairness Definitions** (choose appropriate for context):

- **Demographic parity**: Outcome rates equal across groups (e.g., 40% approval rate for all)
- **Equalized odds**: False positive and false negative rates equal across groups
- **Equal opportunity**: True positive rate equal across groups (equal access to benefit)
- **Calibration**: Predicted probabilities match observed frequencies for all groups
- **Individual fairness**: Similar individuals treated similarly (Lipschitz condition)
- **Counterfactual fairness**: Outcome same if sensitive attribute (race, gender) were different

**Mitigation Strategies:**

- **Prevent**: Design change eliminates harm (e.g., don't collect sensitive data)
- **Reduce**: Decrease likelihood or severity (e.g., rate limiting, friction for risky actions)
- **Detect**: Monitor and alert when harm occurs (e.g., bias dashboard, anomaly detection)
- **Respond**: Process to address harm when found (e.g., appeals, human review, compensation)
- **Safeguard**: Redundancy, fail-safes, circuit breakers for critical failures
- **Transparency**: Explain, educate, build understanding and trust
- **Empower**: Give users control, choice, ability to opt out or customize

**Monitoring Metrics:**

- **Outcome disparities**: Measure by protected class (approval rates, error rates, treatment quality)
- **Error distribution**: False positives/negatives, who bears burden?
- **User complaints**: Volume, categories, resolution rates, disparities
- **Engagement/retention**: Differences across groups (are some excluded?)
- **Safety incidents**: Volume, severity, affected populations
- **Consent/opt-outs**: How many decline? Demographics of decliners?

**Escalation Triggers:**

- Disparate impact >20% without justification
- Safety incidents causing serious harm (injury, death)
- Vulnerable group disproportionately affected (>2× harm rate)
- User complaints spike (>2× baseline)
- Press/regulator attention
- Internal ethics concerns raised

**When to escalate beyond this skill:**

- Legal compliance required (GDPR, ADA, Civil Rights Act, industry regulations)
- Life-or-death safety-critical system (medical, transportation)
- Children or vulnerable populations primary users
- High controversy or political salience
- Novel ethical terrain (new technology, no precedent)
→ Consult: Legal counsel, ethics board, domain experts, affected communities, regulators

**Inputs required:**

- **Feature or decision** (what is being proposed? what changes?)
- **Affected groups** (who is impacted? direct and indirect?)
- **Context** (what problem does this solve? why now?)

**Outputs produced:**

- `ethics-safety-impact.md`: Stakeholder analysis, harm/benefit assessment, fairness evaluation, risk prioritization, mitigation plan, monitoring framework, escalation protocol
