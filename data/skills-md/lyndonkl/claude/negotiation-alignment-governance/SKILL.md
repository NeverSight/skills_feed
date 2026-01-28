---
name: negotiation-alignment-governance
description: Use when stakeholders need aligned working agreements, resolving decision authority ambiguity, navigating cross-functional conflicts, establishing governance frameworks (RACI/DACI/RAPID), negotiating resource allocation, defining escalation paths, creating team norms, mediating trade-off disputes, or when user mentions stakeholder alignment, decision rights, working agreements, conflict resolution, governance model, or consensus building.
---

# Negotiation Alignment Governance

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Create explicit stakeholder alignment through negotiated working agreements, clear decision rights, and conflict resolution protocols—transforming ambiguity and tension into shared understanding and actionable governance.

## When to Use

**Decision Authority Ambiguity:**
- Multiple stakeholders believe they have final say
- Unclear who should be consulted vs informed
- Decisions blocked because no one owns them
- Frequent "I thought you were doing that" moments

**Cross-Functional Conflict:**
- Departments optimizing for different goals
- Resource contention between teams
- Trade-off disputes (quality vs speed, innovation vs stability)
- Scope disagreements between stakeholders

**Alignment Needs:**
- New team forming and needs working agreements
- Org restructure creating unclear boundaries
- Cross-functional initiative requiring coordination
- Partnership or joint venture needing governance

**Negotiation Scenarios:**
- Competing priorities requiring resolution
- Stakeholder expectations needing alignment
- SLAs and commitments to negotiate
- Risk tolerance differences to reconcile

## What Is It

Negotiation-alignment-governance creates explicit agreements on:

**1. Decision Rights (Who Decides):**
- RACI: Responsible, Accountable, Consulted, Informed
- DACI: Driver, Approver, Contributors, Informed
- RAPID: Recommend, Agree, Perform, Input, Decide
- Consent-based frameworks

**2. Working Agreements (How We Work):**
- Communication norms (sync vs async, response times)
- Meeting protocols (agendas, decision methods)
- Quality standards and definition of done
- Escalation paths and conflict resolution

**3. Conflict Resolution (When We Disagree):**
- Structured dialogue formats
- Mediation protocols
- Disagree-and-commit mechanisms
- Escalation criteria

**Example:**
Product wants to ship fast, Engineering wants quality. Instead of endless debates:
- **Decision rights:** Product owns feature scope (DACI: Approver), Engineering owns quality bar (veto on production issues)
- **Working agreement:** Weekly trade-off discussion with data (bug rate, tech debt, customer complaints)
- **Conflict resolution:** If blocked, escalate to VP with joint recommendation and decision criteria

## Workflow

Copy this checklist and track your progress:

```
Negotiation Alignment Governance Progress:
- [ ] Step 1: Map stakeholders and tensions
- [ ] Step 2: Choose governance approach
- [ ] Step 3: Facilitate alignment
- [ ] Step 4: Document agreements
- [ ] Step 5: Establish monitoring
```

**Step 1: Map stakeholders and tensions**

Identify all stakeholders, their interests and concerns, current tensions or conflicts, and decision points needing clarity. See [Common Patterns](#common-patterns) for typical stakeholder configurations.

**Step 2: Choose governance approach**

For straightforward cases with clear stakeholders → Use [resources/template.md](resources/template.md) for RACI/DACI and working agreement structures. For complex cases with multiple conflicts or nested decisions → Study [resources/methodology.md](resources/methodology.md) for negotiation techniques, conflict mediation, and advanced governance patterns.

**Step 3: Facilitate alignment**

Create `negotiation-alignment-governance.md` with: stakeholder map, decision rights matrix (RACI/DACI/RAPID), working agreements (communication, quality, processes), conflict resolution protocols, and escalation paths. Facilitate structured dialogue to negotiate and reach consensus. See [resources/methodology.md](resources/methodology.md) for facilitation techniques.

**Step 4: Document agreements**

Self-assess using [resources/evaluators/rubric_negotiation_alignment_governance.json](resources/evaluators/rubric_negotiation_alignment_governance.json). Check: decision rights are unambiguous, all key stakeholders covered, agreements are specific and actionable, conflict protocols are clear, escalation paths defined. Minimum standard: Average score ≥ 3.5.

**Step 5: Establish monitoring**

Set up regular reviews of governance effectiveness (quarterly), define triggers for updating agreements, establish metrics for decision velocity and conflict resolution, and create feedback mechanisms for stakeholders.

## Common Patterns

### Decision Rights Frameworks

**RACI (Most Common):**
- **R**esponsible: Does the work
- **A**ccountable: Owns the outcome (only ONE person)
- **C**onsulted: Provides input before decision
- **I**nformed: Notified after decision
- Use for: Process mapping, task allocation

**DACI (Better for Decisions):**
- **D**river: Runs the process, gathers input
- **A**pprover: Makes the final decision (only ONE)
- **C**ontributors: Provide input, must be consulted
- **I**nformed: Notified of decision
- Use for: Strategic decisions, product choices

**RAPID (Best for Complex Decisions):**
- **R**ecommend: Propose the decision
- **A**gree: Must agree (veto power)
- **P**erform: Execute the decision
- **I**nput: Consulted for expertise
- **D**ecide: Final authority
- Use for: Major strategic choices with compliance/legal concerns

**Advice Process (Distributed Authority):**
- Anyone can make decision after seeking advice from:
  - Those who will be affected
  - Those with expertise
- Decision-maker is accountable
- Use for: Empowered teams, flat organizations

### Typical Stakeholder Conflicts

**Product vs Engineering:**
- Conflict: Feature scope vs technical quality
- Resolution: Product owns "what" (feature priority), Engineering owns "how" and quality bar
- Escalation: Joint recommendation with data to VP

**Business vs Legal/Compliance:**
- Conflict: Speed to market vs risk mitigation
- Resolution: Business owns opportunity decision, Legal has veto on unacceptable risk
- Escalation: Risk committee with quantified trade-offs

**Centralized vs Decentralized Teams:**
- Conflict: Standards vs autonomy
- Resolution: Central team sets minimum viable standards, teams choose beyond that
- Escalation: Architecture review board for exceptions

### Working Agreement Templates

**Communication Norms:**
- Synchronous (meetings): For collaboration, negotiation, brainstorming
- Asynchronous (docs, Slack): For updates, approvals, information sharing
- Response time expectations: Urgent (<2h), Normal (<24h), FYI (no response needed)
- Meeting defaults: Agenda required, decisions documented, async-first when possible

**Decision-Making Norms:**
- Reversible decisions: Use consent (no objections) for speed
- Irreversible decisions: Use consensus or explicit DACI
- Time-box decisions: If no consensus in N discussions, escalate with options
- Document decisions: ADRs for architecture, decision logs for product

**Conflict Resolution Norms:**
- Direct dialogue first (1:1 between parties)
- Mediation second (neutral third party facilitates)
- Escalation third (manager/leader decides with input)
- Disagree-and-commit: Once decided, all commit to execution

## Guardrails

**Decision Rights:**
- Only ONE person/role is "Accountable" or "Approver"
- Avoid "everyone is consulted" (decision paralysis)
- Consulted ≠ consensus—input gathered, then decider decides
- Define scope: What decisions does this cover?

**Working Agreements:**
- Make agreements specific and observable (not "communicate well" but "respond to Slack in 24h")
- Include both positive behaviors and boundaries
- Revisit quarterly—agreements expire without review
- Get explicit consent from all parties

**Conflict Resolution:**
- Assume good intent—conflicts are about goals/constraints, not character
- Focus on interests (why) not positions (what)
- Use objective criteria when possible (data, benchmarks, principles)
- Separate people from problem

**Facilitation:**
- Remain neutral if mediating (don't take sides)
- Ensure psychological safety (no retribution for honesty)
- Make implicit tensions explicit (name the elephant)
- Don't force consensus—sometimes need to escalate

**Red Flags:**
- Too many decision-makers (slows everything)
- Shadow governance (real decisions made elsewhere)
- Agreements without accountability (no consequences)
- Conflict avoidance (swept under rug, not resolved)

## Quick Reference

**Resources:**
- `resources/template.md` - RACI/DACI/RAPID templates, working agreement structures, conflict resolution protocols
- `resources/methodology.md` - Negotiation techniques (principled negotiation, BATNA analysis), conflict mediation, facilitation patterns, governance design for complex scenarios
- `resources/evaluators/rubric_negotiation_alignment_governance.json` - Quality criteria

**Output:** `negotiation-alignment-governance.md` with stakeholder map, decision rights matrix, working agreements, conflict protocols, escalation paths

**Success Criteria:**
- Decision rights unambiguous (one Accountable/Approver per decision)
- All key stakeholders covered in framework
- Agreements specific and actionable (observable behaviors)
- Conflict resolution protocol clear with escalation path
- Regular review cadence established
- Score ≥ 3.5 on rubric

**Quick Decisions:**
- **Clear stakeholders, simple decisions?** → RACI or DACI template
- **Complex multi-party negotiation?** → Use methodology for principled negotiation
- **Active conflict?** → Start with mediation techniques from methodology
- **Distributed team?** → Consider advice process over hierarchical approval

**Common Mistakes:**
1. Multiple "Accountable" roles (diffuses responsibility)
2. Everyone consulted (decision paralysis)
3. Vague agreements ("communicate better" vs "respond in 24h")
4. No review/update cycle (agreements decay)
5. Shadow governance (official RACI ignored, real decisions made informally)
6. Forcing consensus (sometimes need to disagree-and-commit)

**Key Insight:**
Explicit governance reduces coordination costs over time. Initial investment in alignment pays dividends through faster decisions, less rework, and lower conflict.
