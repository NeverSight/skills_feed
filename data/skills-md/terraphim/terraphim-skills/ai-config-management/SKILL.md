---
name: ai-config-management
description: >
  Produce formal specifications for AI-enabled Configuration Management (CM) systems
  that operationalise Context Engineering principles. Use when tasked with: (1) creating
  CM specifications for AI-enabled programs, (2) defining semantic governance models for
  AI artefacts, (3) designing drift detection frameworks for prompts/models/domains,
  (4) specifying stage-gate control logic with semantic validation, (5) building
  traceability models across AI lifecycle stages, (6) defining change control for
  prompt and model evolution, (7) architecting AI agent roles for configuration
  governance, or (8) any configuration control task involving probabilistic AI behaviour,
  evolving prompts, shifting domain definitions, or artefact proliferation.
license: Apache-2.0
---

# AI-Enabled Configuration Management Specification

## Workflow

Producing an AI-enabled CM specification follows this sequence:

1. **Scope the system** -- Identify operational context, enterprise constraints, AI maturity level
2. **Define the governance model** -- Authority structure, RACI/RASIC, escalation paths
3. **Specify functional requirements** -- See [functional-requirements.md](references/functional-requirements.md)
4. **Define AI agent architecture** -- See [ai-agents.md](references/ai-agents.md)
5. **Map control surfaces and baselines** -- See [control-surfaces.md](references/control-surfaces.md)
6. **Design drift detection framework** -- See [drift-detection.md](references/drift-detection.md)
7. **Establish metrics and health indicators** -- See [metrics.md](references/metrics.md)
8. **Compose the deliverable** -- See [deliverable-structure.md](references/deliverable-structure.md) for required sections and format

## Core Principles

Treat context as a **controlled architectural variable**, not an ambient condition.

- AI augments human authority; it does not replace it
- Entropy is reduced through semantic baselining, reconciliation protocols, and gated progression
- Progression halts when semantic integrity is violated
- Operational mechanisms, not philosophical descriptions

## Operating Constraints

The CM system addresses environments characterised by:

- Probabilistic AI behaviour with non-deterministic outputs
- Evolving prompts, model versions, and training data
- Shifting domain definitions under commercial pressure
- Artefact proliferation across lifecycle stages
- Multiple stakeholder interpretation layers

Explicit threats the specification must counter:

| Threat | Mechanism |
|--------|-----------|
| Context entropy | Semantic baselining + reconciliation |
| Semantic drift | Terminology stability index + drift alerts |
| Unmanaged scope expansion | Baseline freeze + formal change control |
| Informal commitments bypassing governance | Decision container governance + traceability |
| Artefact inconsistency | Cross-artefact consistency engine + contradiction detection |

## Deliverable Structure

The specification output must contain these sections (see [deliverable-structure.md](references/deliverable-structure.md) for full detail):

1. Executive Overview
2. System Architecture (textual description)
3. Formal Requirements (numbered, FR-xxx / NFR-xxx)
4. Workflow Narratives
5. Data Model Schema (conceptual)
6. Governance Matrix (RACI/RASIC)
7. Risk Register
8. Implementation Phases

Use formal systems engineering language. Avoid generic project management phrasing. Align terminology with configuration control, semantic governance, and systems architecture.

## ZDP Integration (Optional)

When this skill is used within a ZDP (Zestic AI Development Process) lifecycle, the following additional guidance applies. **This section can be ignored for standalone usage.**

### ZDP Context

AI-enabled CM specification maps to the ZDP **Design** stage as a governance artefact produced alongside the Architecture Document. The CM specification's lifecycle stages align directly with ZDP's 6D model (Discovery through Drive). CM gate definitions (FR-C01-C05) should reference ZDP gate types (PFA, LCO, LCA, IOC, FOC, CLR) when producing specifications for ZDP-governed programs.

### Additional Guidance

When producing CM specifications within a ZDP lifecycle:
- Map CM control surface baselines (control-surfaces.md) to ZDP stage-gate boundaries
- Reference ZDP artefact types in the artefact classification schema (FR-B01): PVVH, business scenarios, domain model, design brief, prompt specs align to control surfaces 1-10
- Integrate epistemic status classification from perspective-investigation into gate readiness assessments (FR-C01-C04): gate checklist items should carry Known/Sufficient, Partially Known, Contested, Underdetermined, or Out-of-Scope status
- Reference the Responsible AI Risk Register (from `/responsible-ai`) as input to Risk Register section (Section 7 of deliverable)
- Align drift monitoring categories (drift-detection.md) with ZDP Drive stage monitoring requirements

### Cross-References

If available, coordinate outputs with:
- `/architecture` -- CM specification complements the Architecture Document
- `/responsible-ai` -- AI-specific risks feed into CM risk register
- `/perspective-investigation` -- epistemic status classification for gate items
- `/mlops-monitoring` -- operational drift monitoring complements CM drift specification
- `/requirements-traceability` -- CM traceability requirements (FR-H) align with traceability matrix production

## Reference Navigation

| Need | Reference File |
|------|---------------|
| Functional capabilities (A through I) | [functional-requirements.md](references/functional-requirements.md) |
| AI agent roles, inputs, outputs, authority | [ai-agents.md](references/ai-agents.md) |
| Control surfaces, baselines, freeze logic | [control-surfaces.md](references/control-surfaces.md) |
| Drift detection framework | [drift-detection.md](references/drift-detection.md) |
| Metrics and health indicators | [metrics.md](references/metrics.md) |
| Full deliverable structure and format | [deliverable-structure.md](references/deliverable-structure.md) |
| Governance templates (RACI, risk register) | [governance-templates.md](references/governance-templates.md) |

Load only the reference files relevant to the current task. For a full specification, read all. For targeted work (e.g., only drift detection), read only the applicable file.
