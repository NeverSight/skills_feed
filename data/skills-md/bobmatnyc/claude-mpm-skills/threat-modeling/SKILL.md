---
name: threat-modeling
description: "Threat modeling workflow for software systems: scope, data flow diagrams, STRIDE analysis, risk scoring, and turning mitigations into backlog and tests"
version: 1.0.0
category: universal
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Run a lightweight threat modeling workshop (STRIDE) and turn risks into concrete mitigations, tests, and PR checks"
    when_to_use: "When designing new features, reviewing architecture changes, handling sensitive data, or hardening auth/payment/multi-tenant flows"
    quick_start: "1. Define scope/assets 2. Draw data flows + trust boundaries 3. STRIDE per element 4. Score + prioritize 5. Track mitigations + tests"
  token_estimate:
    entry: 150
    full: 8000
context_limit: 900
tags:
  - security
  - threat-modeling
  - stride
  - architecture
  - risk
requires_tools: []
---

# Threat Modeling (STRIDE)

## Outputs (Definition of Done)

Produce a data flow diagram, a threat register, and a mitigation plan that becomes tickets and tests.

## Load Next (References)

- `references/stride-workshop.md` — step-by-step workshop agenda + DFD guidance
- `references/common-threats-and-mitigations.md` — threat catalog with mitigations
- `references/templates.md` — copy/paste templates for docs and tickets
