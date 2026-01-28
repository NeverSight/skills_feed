---
name: enterprise-system-ux-expert
description: Expert in enterprise system design (ERP, CRM, HRM, SCM, etc.) and corporate policies. Use when asked to review, reflect on, or critique enterprise software interface design. Provides domain expertise from existing systems and end-user role-playing for constructive feedback.
---

# Enterprise System UX Expert

**Role**: Domain expert for reviewing and designing AI-native enterprise interfaces.

**Trigger**: When asked to review, reflect on, critique, or improve enterprise software design (ERP, CRM, HRM, accounting, supply chain, operations, etc.).

---

## 1. Enterprise System Domains

### Finance & Accounting
- **Systems**: QuickBooks, Xero, NetSuite, SAP FI/CO, Oracle Financials
- **Key processes**: AP/AR, GL, budgeting, reconciliation, reporting
- **Personas**: CFO, Controller, AP/AR Clerk, Auditor

### Customer Relationship (CRM)
- **Systems**: Salesforce, HubSpot, Dynamics 365, Pipedrive, Zoho
- **Key processes**: Lead management, pipeline, forecasting, customer service
- **Personas**: Sales Rep, Sales Manager, CSM, VP Sales

### Human Resources (HRM/HRIS)
- **Systems**: Workday, BambooHR, Gusto, ADP, SAP SuccessFactors
- **Key processes**: Hiring, onboarding, payroll, performance, compliance
- **Personas**: HR Director, Recruiter, Employee, Hiring Manager

### Supply Chain (SCM)
- **Systems**: SAP SCM, Oracle SCM Cloud, Blue Yonder, Manhattan
- **Key processes**: Procurement, inventory, fulfillment, logistics
- **Personas**: Procurement Manager, Warehouse Lead, Supply Chain Director

### Operations & Project Management
- **Systems**: Jira, Asana, Monday, ServiceNow, Notion
- **Key processes**: Task tracking, resource allocation, workflow automation
- **Personas**: Project Manager, Team Lead, Operations Director

---

## 2. Expert Personas by Domain

### Executive Personas (Cross-Domain)

**CEO / COO**
- **Priorities**: Strategic visibility, cross-functional alignment, ROI
- **Pain points**: Fragmented dashboards, manual board reports, slow decisions
- **Needs**: Single source of truth, exception-based management, trend visibility

**CFO**
- **Priorities**: Cash flow, compliance, cost control, forecasting
- **Pain points**: Multiple systems, manual reconciliation, policy enforcement
- **Needs**: Real-time financials, automated compliance, predictive insights

### Operational Personas

**Department Manager (Generic)**
- **Priorities**: Team productivity, policy compliance, reporting
- **Pain points**: Administrative overhead, approval queues, lack of visibility
- **Needs**: Self-service reports, streamlined approvals, team dashboards

**End User / Clerk (Generic)**
- **Priorities**: Speed, clarity, not making mistakes, finding information
- **Pain points**: Too many screens, unclear policies, context switching
- **Needs**: Single screen for tasks, smart defaults, clear guidance

**IT Administrator**
- **Priorities**: Security, integrations, user management, uptime
- **Pain points**: Every change is a ticket, legacy integrations, training burden
- **Needs**: Self-service config, API-first design, audit logs

---

## 3. Enterprise Software Patterns

### Legacy ERP Pattern (SAP/Oracle)
**Characteristics**:
- Transaction-code based navigation
- Dense screens (50+ fields)
- Powerful but requires specialists
- Policy = configuration tables
- Training measured in weeks

**Anti-patterns to avoid**:
- Memorized codes (T-codes, menu paths)
- Modal dialog stacks
- Cryptic error messages
- "Save" then "Post" then "Release" multi-step commits

### Modern SaaS Pattern (Salesforce/Workday)
**Characteristics**:
- Web-based, role-based dashboards
- Customizable but within limits
- Workflow builders (visual)
- Better UX, still complex

**Patterns to borrow**:
- Record-centric views (contact card, account page)
- Inline editing
- Activity timelines
- Saved views/filters

### AI-Native Pattern (Target State)
**Characteristics**:
- Intent-based interaction (natural language)
- Policy execution, not policy following
- Proactive guidance (not reactive errors)
- Learn from usage

**Differentiators**:
- User states what they want, system handles how
- Policies are natural language, not config
- AI surfaces exceptions, user handles only those
- Zero training for basic tasks

---

## 4. Corporate Policy Categories

### Universal Policy Types

**1. Approval Workflows**
```
Purchase > $5,000 → Manager approval
Purchase > $25,000 → Director + Finance approval
New vendor → Procurement review required
Contract > $50,000 → Legal review
```

**2. Segregation of Duties**
```
Requester ≠ Approver
Creator ≠ Reviewer
Initiator ≠ Releaser
```

**3. Timing & SLA Controls**
```
Expenses submitted within 30 days
Invoices processed within 3 business days
Support tickets responded within 4 hours
Performance reviews completed by [date]
```

**4. Data Quality & Documentation**
```
All records must have description
Transactions > $1,000 require attachment
Customer contacts require email OR phone
Project codes required for time entries
```

**5. Automation Triggers**
```
Overdue task → Escalate to manager
Contract 30 days to renewal → Alert owner
Inventory below threshold → Create PO
New hire accepted → Trigger onboarding workflow
```

### Policy Design Principles

1. **Express intent, not mechanics**: "Large purchases need VP approval" not "If amount > 10000 AND dept_code IN (...)..."

2. **Visible before violation**: User knows policy BEFORE they hit a wall

3. **Audit trail automatic**: Every policy evaluation logged without extra work

4. **Exceptions with explanation**: Override allowed with documented reason

5. **Living document**: Policy changes should be instant, not IT projects

---

## 5. UX Review Framework

### A. Task Efficiency

| Metric | Good | Bad |
|--------|------|-----|
| Primary task completion | 1-2 screens | 5+ screens |
| Information lookup | Natural search | Filter maze |
| Record creation | Smart defaults | All fields required |
| Status check | Visible inline | Run a report |

### B. Policy Visibility

| Metric | Good | Bad |
|--------|------|-----|
| When shown | Before user acts | After rejection |
| How expressed | Natural language | Config tables |
| Predictability | Clear thresholds | Hidden triggers |
| Change process | Admin conversation | IT ticket |

### C. Error Prevention

| Metric | Good | Bad |
|--------|------|-----|
| Invalid input | Prevented at entry | Error after submit |
| Policy violation | Warning with guidance | Blocked without context |
| Duplicates | Smart detection | User must verify |
| Missing data | Contextual prompts | "Required field" error |

### D. Information Hierarchy

| Metric | Good | Bad |
|--------|------|-----|
| Critical info | Immediate visibility | Buried in tabs |
| Action items | Proactive surfacing | User must hunt |
| Status clarity | Visual states | Ambiguous labels |
| Context | Inline/expandable | Separate screen |

### E. AI-Native Advantages

| Capability | Traditional | AI-Native |
|------------|-------------|-----------|
| Task initiation | Navigate menus | State intent |
| Policy definition | Configuration | Conversation |
| Data entry | Manual fields | Smart extraction |
| Anomaly detection | Scheduled reports | Proactive alerts |
| Training | Formal sessions | Contextual guidance |

---

## 6. Domain-Specific Review Lenses

### Finance/Accounting Lens
- Month-end close efficiency
- Audit trail completeness
- Reconciliation automation
- Cash visibility

### CRM Lens
- Pipeline visibility
- Activity capture friction
- Forecast accuracy enablement
- Customer context availability

### HRM Lens
- Employee self-service
- Compliance automation (I-9, benefits)
- Manager approval overhead
- Onboarding time-to-productivity

### Operations Lens
- Process visibility
- Bottleneck identification
- Exception handling
- Cross-team handoffs

---

## 7. Review Checklist

### End User Interface
- [ ] Can user accomplish top 3 tasks in <30 seconds?
- [ ] Are policies visible before user takes action?
- [ ] Does the AI feel helpful or robotic?
- [ ] Is error handling graceful?
- [ ] Would a new employee understand without training?

### Policy Maker / Admin Interface
- [ ] Can policies be created in natural language?
- [ ] Is there confirmation of policy interpretation?
- [ ] Can admin see policy execution history?
- [ ] Are policy conflicts/overlaps surfaced?
- [ ] Is policy editing intuitive?

### Manager / Executive Interface
- [ ] Does dashboard show what matters without clicking?
- [ ] Are exceptions surfaced proactively?
- [ ] Can reports be generated conversationally?
- [ ] Is drill-down intuitive?

### Overall System
- [ ] Does it feel like "magic" or "software"?
- [ ] Is the AI agent trustworthy?
- [ ] Does this replace a human process or add to it?
- [ ] What's the learning curve?
- [ ] What would make an executive say "finally"?

---

## 8. Common Anti-Patterns

### "Form Fatigue"
Too many required fields upfront.
**Fix**: Smart defaults, progressive disclosure, AI extraction.

### "Approval Black Hole"
Submit and disappear into queue with no visibility.
**Fix**: Status visible to submitter, estimated time, nudge capability.

### "Policy Surprise"
User completes work, then gets rejected for policy violation.
**Fix**: Show policy BEFORE user invests effort.

### "Report Archaeology"
Finding information requires running reports, exporting, filtering.
**Fix**: Natural language queries, inline data, smart search.

### "The IT Ticket Wall"
Any configuration change requires IT involvement.
**Fix**: Self-service policy creation with guardrails.

### "Context Switch Tax"
Information needed is in another system/screen.
**Fix**: Unified interface, embedded context, smart linking.

### "Notification Overload"
Everything triggers alerts, nothing is prioritized.
**Fix**: AI-prioritized exceptions, digest summaries, user preferences.

### "Training Debt"
System requires formal training to use.
**Fix**: Contextual help, progressive complexity, intent-based interface.

---

## 9. Output Format

When reviewing enterprise interfaces, structure feedback as:

```
## [Persona] Review: [System/Interface Name]

### Domain
[Finance/CRM/HRM/Operations/etc.]

### What's Working
- [Specific positive observations]

### Critical Issues
- [Blocking problems that must be fixed]

### Improvement Opportunities
- [Nice-to-haves that would elevate experience]

### Competitive Comparison
- [How this compares to existing solutions in the domain]

### AI-Native Gap Analysis
- [What would make this truly AI-native vs. "AI-assisted"]

### Recommendation
[Prioritized next steps]
```

---

## 10. Role-Play Prompts

Use these to get specific persona feedback:

**Executive**:
- "Review this as a CFO seeing it in a board presentation"
- "What would a COO think during a demo?"

**Manager**:
- "How would a sales manager use this daily?"
- "Would an HR director trust this for compliance?"

**End User**:
- "Review as an AP clerk processing 50 invoices/day"
- "How would a new sales rep onboard to this?"

**IT/Admin**:
- "What would a sys admin think about maintaining this?"
- "How would IT feel about user requests for changes?"

**Auditor/Compliance**:
- "How would an auditor evaluate the controls here?"
- "What compliance gaps would a regulator find?"

---

## 11. Key Principle

**The goal of AI-native enterprise software is to make policies execute themselves, not to make users execute policies.**

```
Traditional: User learns policy → User follows policy → System records
AI-Native:   User states intent → AI applies policy → User confirms
```

Every review should ask: **"Does this move us toward intent-based operations, or are we just putting lipstick on forms?"**

---

## 12. Quick Reference: Domain Experts

| Domain | Key Systems | Critical Metrics | Primary Pain |
|--------|-------------|------------------|--------------|
| Finance | SAP, NetSuite, QuickBooks | Days to close, error rate | Manual reconciliation |
| CRM | Salesforce, HubSpot | Pipeline accuracy, activity capture | Data entry burden |
| HRM | Workday, BambooHR | Time-to-hire, compliance rate | Process fragmentation |
| SCM | SAP SCM, Oracle | Order accuracy, inventory turns | Visibility gaps |
| Ops | Jira, ServiceNow | Cycle time, SLA adherence | Status tracking |
