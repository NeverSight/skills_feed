---
name: bmad-security-review
description: Hardens designs and implementations with structured security reviews.
allowed-tools: ["Read", "Write", "Grep"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "threat model"
      - "security review"
      - "penetration test"
      - "secure this"
      - "hardening plan"
      - "security requirements"
      - "compliance gap"
    keywords:
      - security
      - threat-model
      - vulnerability
      - secure
      - harden
      - compliance
      - privacy
  capabilities:
    - threat-modeling
    - secure-design
    - dependency-audit
    - remediation-planning
    - compliance-checks
  prerequisites:
    - bmad-architecture-design
    - bmad-test-strategy
  outputs:
    - threat-model
    - security-gap-assessment
    - remediation-backlog
---

# BMAD Security Review Skill

## When to Invoke

Activate this skill whenever the user:
- Requests a security, privacy, or compliance review of a feature or system.
- Mentions threat modeling, secure design, risk assessment, or penetration testing.
- Asks for guidance on hardening infrastructure, APIs, data flows, or deployment pipelines.
- Needs a remediation backlog prior to launch or certification.
- Receives external audit findings that must be triaged and addressed.

Do **not** invoke when the user only needs implementation help with security stories—route those to `bmad-development-execution` once the remediation plan exists.

## Mission

Protect the product by exposing security risks early, prioritizing fixes, and embedding mitigations into the delivery plan. Deliver artifacts that downstream skills and teams can execute without ambiguity.

## Inputs Required

- Architecture decisions, diagrams, or code references (`docs/architecture.md`, repositories, infrastructure manifests).
- Current product requirements, especially data handling and auth flows.
- Any existing penetration test reports, compliance requirements, or known incidents.
- Deployment environment details (cloud provider, runtimes, integrations).

If critical context is missing, schedule discovery steps in `WORKFLOW.md` before producing findings.

## Outputs

- **Threat model** covering data flows, trust boundaries, STRIDE analysis, and mitigations using templates in `assets/`.
- **Security gap assessment** summarizing findings by severity with clear owners and due dates.
- **Remediation backlog** with prioritized user stories and acceptance criteria ready for `bmad-story-planning`.
- Optional compliance checklists (SOC2, HIPAA, GDPR) when requested.

## Process

1. Confirm prerequisites are satisfied (architecture + test strategy). Request missing artifacts.
2. Map system boundaries and data classifications. Document entry points and critical assets.
3. Run threat modeling workshops: enumerate threats via STRIDE/LINDDUN and rate likelihood × impact.
4. Review code, dependencies, and infrastructure for known vulnerabilities or misconfigurations.
5. Summarize findings with severity, evidence, and references to assets or standards violated.
6. Translate mitigations into actionable backlog items. Align with release timelines.
7. Provide launch go/no-go recommendation and residual risk statement.

## Quality Gates

- No critical/high risks without documented mitigation and owner.
- Threat model reviewed against latest architecture diagram.
- Remediation backlog linked to acceptance criteria consumable by dev/test skills.
- Compliance requirements traced to controls or follow-up activities.

## Error Handling

- If findings rely on missing context, pause and obtain evidence before finalizing reports.
- Escalate systemic issues (e.g., absence of IAM, encryption gaps) to product leadership via orchestrator.
- Document assumptions; flag when runtime verification (DAST/SAST) is required beyond conversational review.
