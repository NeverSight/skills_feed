---
name: deliberation-debate-red-teaming
description: Use when testing plans or decisions for blind spots, need adversarial review before launch, validating strategy against worst-case scenarios, building consensus through structured debate, identifying attack vectors or vulnerabilities, user mentions "play devil's advocate", "what could go wrong", "challenge our assumptions", "stress test this", "red team", or when groupthink or confirmation bias may be hiding risks.
---

# Deliberation, Debate & Red Teaming

## What Is It?

Deliberation-debate-red-teaming is a structured adversarial process where you intentionally challenge plans, designs, or decisions from multiple critical perspectives to surface blind spots, hidden assumptions, and vulnerabilities before they cause real damage.

**Quick example:**

**Proposal:** "Launch new feature to all users next week"

**Red team critiques:**
- **Security:** "No penetration testing done, could expose user data"
- **Operations:** "No runbook for rollback, deployment on Friday risks weekend outage"
- **Customer:** "Feature breaks existing workflow for power users (20% of revenue)"
- **Legal:** "GDPR consent flow unclear, could trigger regulatory investigation"

**Result:** Delay launch 2 weeks, address security/legal/ops gaps, add feature flag for gradual rollout

## Workflow

Copy this checklist and track your progress:

```
Deliberation & Red Teaming Progress:
- [ ] Step 1: Define the proposal and stakes
- [ ] Step 2: Assign adversarial roles
- [ ] Step 3: Generate critiques and challenges
- [ ] Step 4: Synthesize findings and prioritize risks
- [ ] Step 5: Recommend mitigations and revisions
```

**Step 1: Define the proposal and stakes**

Ask user for the plan/decision to evaluate (specific proposal, not vague idea), stakes (what happens if this fails), current confidence level (how certain are they), and deadline (when must decision be made). Understanding stakes helps calibrate critique intensity. See [Scoping Questions](#scoping-questions).

**Step 2: Assign adversarial roles**

Identify critical perspectives that could expose blind spots. Choose 3-5 roles based on proposal type (security, legal, operations, customer, competitor, etc.). Each role has different incentives and concerns. See [Adversarial Role Types](#adversarial-role-types) and [resources/template.md](resources/template.md) for role assignment guidance.

**Step 3: Generate critiques and challenges**

For each role, generate specific critiques: What could go wrong? What assumptions are questionable? What edge cases break this? Be adversarial but realistic (steelman, not strawman arguments). For advanced critique techniques → See [resources/methodology.md](resources/methodology.md) for red team attack patterns.

**Step 4: Synthesize findings and prioritize risks**

Collect all critiques, identify themes (security gaps, operational risks, customer impact, etc.), assess severity and likelihood for each risk. Distinguish between showstoppers (must fix) and acceptable risks (monitor/mitigate). See [Risk Prioritization](#risk-prioritization).

**Step 5: Recommend mitigations and revisions**

For each critical risk, propose concrete mitigation (change the plan, add safeguards, gather more data, or accept risk with monitoring). Present revised proposal incorporating fixes. See [Mitigation Patterns](#mitigation-patterns) for common approaches.

## Scoping Questions

**To define the proposal:**
- What exactly are we evaluating? (Be specific: "launch feature X to cohort Y on date Z")
- What's the goal? (Why do this?)
- Who made this proposal? (Understanding bias helps)

**To understand stakes:**
- What happens if this succeeds? (Upside)
- What happens if this fails? (Downside, worst case)
- Is this reversible? (Can we roll back if wrong?)
- What's the cost of delay? (Opportunity cost of waiting)

**To calibrate critique:**
- How confident is the team? (0-100%)
- What analysis has been done already?
- What concerns have been raised internally?
- When do we need to decide? (Time pressure affects rigor)

## Adversarial Role Types

Choose 3-5 roles that are most likely to expose blind spots for this specific proposal:

### External Adversary Roles

**Competitor:**
- "How would our competitor exploit this decision?"
- "What gives them an opening in the market?"
- Useful for: Strategy, product launches, pricing decisions

**Malicious Actor (Security):**
- "How would an attacker compromise this?"
- "What's the weakest link in the chain?"
- Useful for: Security architecture, data handling, access controls

**Regulator/Auditor:**
- "Does this violate any laws, regulations, or compliance requirements?"
- "What documentation is missing for audit trail?"
- Useful for: Privacy, financial, healthcare, legal matters

**Investigative Journalist:**
- "What looks bad if this becomes public?"
- "What are we hiding or not disclosing?"
- Useful for: PR-sensitive decisions, ethics, transparency

### Internal Stakeholder Roles

**Operations/SRE:**
- "Will this break production? Can we maintain it?"
- "What's the runbook for when this fails at 2am?"
- Useful for: Technical changes, deployments, infrastructure

**Customer/User:**
- "Does this actually solve my problem or create new friction?"
- "Am I being asked to change behavior? Why should I?"
- Useful for: Product features, UX changes, pricing

**Finance/Budget:**
- "What are the hidden costs? TCO over 3 years?"
- "Is ROI realistic or based on optimistic assumptions?"
- Useful for: Investments, vendor selection, resource allocation

**Legal/Compliance:**
- "What liability does this create?"
- "Are contracts/terms clear? What disputes could arise?"
- Useful for: Partnerships, licensing, data usage

**Engineering/Technical:**
- "Is this technically feasible? What's the technical debt?"
- "What are we underestimating in complexity?"
- Useful for: Architecture decisions, technology choices, timelines

### Devil's Advocate Roles

**Pessimist:**
- "What's the worst-case scenario?"
- "Murphy's Law: What can go wrong will go wrong"
- Useful for: Risk assessment, contingency planning

**Contrarian:**
- "What if the opposite is true?"
- "Challenge every assumption: What if market research is wrong?"
- Useful for: Validating assumptions, testing consensus

**Long-term Thinker:**
- "What are second-order effects in 1-3 years?"
- "Are we solving today's problem and creating tomorrow's crisis?"
- Useful for: Strategic decisions, architectural choices

## Risk Prioritization

After generating critiques, prioritize by severity and likelihood:

### Severity Scale

**Critical (5):** Catastrophic failure (data breach, regulatory fine, business shutdown)
**High (4):** Major damage (significant revenue loss, customer exodus, reputation hit)
**Medium (3):** Moderate impact (delays, budget overrun, customer complaints)
**Low (2):** Minor inconvenience (edge case bugs, small inefficiency)
**Trivial (1):** Negligible (cosmetic issues, minor UX friction)

### Likelihood Scale

**Very Likely (5):** >80% chance if we proceed
**Likely (4):** 50-80% chance
**Possible (3):** 20-50% chance
**Unlikely (2):** 5-20% chance
**Rare (1):** <5% chance

### Risk Score = Severity × Likelihood

**Showstoppers (score ≥ 15):** Must address before proceeding
**High Priority (score 10-14):** Should address, or have strong mitigation plan
**Monitor (score 5-9):** Accept risk but have contingency
**Accept (score < 5):** Acknowledge and move on

### Risk Matrix

| Severity ↓ / Likelihood → | Rare (1) | Unlikely (2) | Possible (3) | Likely (4) | Very Likely (5) |
|---------------------------|----------|--------------|--------------|------------|-----------------|
| **Critical (5)** | 5 (Monitor) | 10 (High Priority) | 15 (SHOWSTOPPER) | 20 (SHOWSTOPPER) | 25 (SHOWSTOPPER) |
| **High (4)** | 4 (Accept) | 8 (Monitor) | 12 (High Priority) | 16 (SHOWSTOPPER) | 20 (SHOWSTOPPER) |
| **Medium (3)** | 3 (Accept) | 6 (Monitor) | 9 (Monitor) | 12 (High Priority) | 15 (SHOWSTOPPER) |
| **Low (2)** | 2 (Accept) | 4 (Accept) | 6 (Monitor) | 8 (Monitor) | 10 (High Priority) |
| **Trivial (1)** | 1 (Accept) | 2 (Accept) | 3 (Accept) | 4 (Accept) | 5 (Monitor) |

## Mitigation Patterns

For each identified risk, choose mitigation approach:

**1. Revise the Proposal (Change Plan)**
- Fix the flaw in design/approach
- Example: Security risk → Add authentication layer before launch

**2. Add Safeguards (Reduce Likelihood)**
- Implement controls to prevent risk
- Example: Operations risk → Add automated rollback, feature flags

**3. Reduce Blast Radius (Reduce Severity)**
- Limit scope or impact if failure occurs
- Example: Customer risk → Gradual rollout to 5% of users first

**4. Contingency Planning (Prepare for Failure)**
- Have plan B ready
- Example: Vendor risk → Identify backup supplier in advance

**5. Gather More Data (Reduce Uncertainty)**
- Research, prototype, or test before committing
- Example: Assumption risk → Run A/B test to validate hypothesis

**6. Accept and Monitor (Informed Risk)**
- Acknowledge risk, set up alerts/metrics to detect if it manifests
- Example: Low-probability edge case → Monitor error rates, have fix ready

**7. Delay/Cancel (Avoid Risk Entirely)**
- If risk is too high and can't be mitigated, don't proceed
- Example: Showstopper legal risk → Delay until legal review complete

## When NOT to Use This Skill

**Skip red teaming if:**
- Decision is trivial/low-stakes (not worth the overhead)
- Time-critical emergency (no time for deliberation, must act now)
- Already thoroughly vetted (extensive prior review, red team would be redundant)
- No reasonable alternatives (one viable path, red team can't change outcome)
- Pure research/exploration (not committing to anything, failure is cheap)

**Use instead:**
- Trivial decision → Just decide, move on
- Emergency → Act immediately, retrospective later
- Already vetted → Proceed with monitoring
- No alternatives → Focus on execution planning

## Quick Reference

**Process:**
1. Define proposal and stakes → Set scope
2. Assign adversarial roles → Choose 3-5 critical perspectives
3. Generate critiques → What could go wrong from each role?
4. Prioritize risks → Severity × Likelihood matrix
5. Recommend mitigations → Revise, safeguard, contingency, accept, or cancel

**Common adversarial roles:**
- Competitor, Malicious Actor, Regulator, Operations, Customer, Finance, Legal, Engineer, Pessimist, Contrarian, Long-term Thinker

**Risk prioritization:**
- Showstoppers (≥15): Must fix
- High Priority (10-14): Should address
- Monitor (5-9): Accept with contingency
- Accept (<5): Acknowledge

**Resources:**
- [resources/template.md](resources/template.md) - Structured red team process with role templates
- [resources/methodology.md](resources/methodology.md) - Advanced techniques (attack trees, pre-mortem, wargaming)
- [resources/evaluators/rubric_deliberation_debate_red_teaming.json](resources/evaluators/rubric_deliberation_debate_red_teaming.json) - Quality checklist

**Deliverable:** `deliberation-debate-red-teaming.md` with critiques, risk assessment, and mitigation recommendations
