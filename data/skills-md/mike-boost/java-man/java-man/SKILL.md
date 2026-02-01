---
name: java-man
description: "Ops-grade, evidence-backed profiling for Java projects (business flows + integrations + Kubernetes readiness). Produces PROJECT_PROFILE.md + DEPLOYMENT_RUNBOOK.md. Tool-agnostic, zero-hallucination."
---

# java-man — Ops-grade Java Project Profiling (Commercial Deliverable)

## Profile (Tool-Agnostic)

- Audience: Ops/SRE (cross-team readable)
- Priorities: business flows → integrations → Kubernetes/operations
- Baselines: absorb `java-architect` (architecture) and `java-reviewer` (Java quality signals)

## Mission

Produce a commercial-grade, product-level report that treats the Java codebase as data. Focus on business and logic first, then operations. Generate exactly two Markdown deliverables in English: `PROJECT_PROFILE.md` and `DEPLOYMENT_RUNBOOK.md`.

## Mandatory Skill Absorption (Unify, Do Not Fragment)

Perform both absorptions before repo analysis, then operate as a single cohesive skill:

1. **Absorb `java-architect`** (architecture baseline)
    - Prefer skill registry; if unavailable, read `~/.agents/skills/java-architect/SKILL.md`.
    - Summarize into an **Architecture Baseline** section: required steps, outputs, terminology.
2. **Absorb `java-reviewer`** (Java quality signals)
    - Prefer skill registry; if unavailable, read `~/.cursor/skills/java-reviewer/SKILL.md`.
    - Use only for **non-test code** and **as reference**; do not override business/ops priorities.
      If either skill is inaccessible, mark **Unknown (skill not accessible)** in the final report’s Unknowns section and continue with repository evidence only.

## Strict Facts Policy (No Imagination)

- Do not assume anything. If not found, mark **Unknown (Not Found in Repo)** and state what was searched.
- If plausible but not proven, label **Hypothesis (Evidence-based)** and include the evidence chain.
- If evidence is weak or indirect, label **Unverified** and do not treat as fact.
- Never assume this is a microservice; determine type (service/batch/worker/library/module) from evidence or mark Unknown.
- Treat **test code as reference only**; never assert business behavior based solely on tests.

## Evidence Anchors (Required)

For every non-trivial claim, attach at least one Evidence Anchor:

- `path/to/File.java` + `ClassName#methodName`, or
- <=10 lines excerpt + file path.
  If none exists, state `Unknown (Not Found in Repo)` and mention what was searched.

## Analysis Workflow (Progressive Disclosure; Tool-Agnostic)

1. **Surface Scan (Repo Map & Tech Stack)**
    - Identify modules, build tool(s), Java version, frameworks, dependency management.
    - Output a tech-stack map/tree and module structure with evidence.
2. **Runtime Identity**
    - Find entrypoints: `main`, `SpringBootApplication`, CLI, jobs, workers.
    - Determine runtime type (service/batch/worker/library) with evidence.
3. **Business Capability Extraction**
    - Derive capabilities from non-test controllers/handlers/jobs/listeners.
    - Identify inputs/outputs and side effects (DB writes, external calls).
4. **System Interactions (Integration Matrix)**
    - Detect outbound/inbound integrations: REST/gRPC/messaging/DB/cache/files.
    - Record protocol, auth, endpoints/topics, timeouts/retries if evidenced.
5. **Critical Business Flows (3–5)**
    - Trace end-to-end call chains with evidence.
    - Include data read/write, transaction boundaries, external calls.
6. **Configuration & Environment Model**
    - Identify config sources, precedence, required keys, secrets handling.
    - Build a config inventory table (key → meaning → default → required → usage).
7. **Kubernetes & Ops Readiness**
    - Derive ports, probes, graceful shutdown, resource hints, dependencies.
    - If missing, provide blueprint placeholders marked **Unknown**.
8. **Observability & SLO-Relevant Paths**
    - Identify logging/metrics/tracing and SLO-relevant paths (latency, DB usage, external calls, queue lag) if evidenced.
9. **Report Assembly**
    - Produce the two required documents with tables, diagrams, checklists, and explicit Unknowns.

## Testing Policy (Reference Only)

Only provide:

- Test types present (unit/integration/e2e) and layout
- High-level behaviors they appear to test
- Evidence of skipped/disabled tests
- Whether CI invokes tests (if evidenced), else Unknown
  Do not claim tests are correct or representative.

## Required Outputs (Exactly Two Markdown Docs)

- Create an output directory in the working directory named: `analyze-report-YYYY-MM-DD` (use current date).
- Write the two files inside that directory:
    - `PROJECT_PROFILE.md`
    - `DEPLOYMENT_RUNBOOK.md`
      If file creation is not possible, print the two documents with clear headings.

## Document A: PROJECT_PROFILE.md (Fixed Sections)

1. **Cover** (project/service name, report version, date, scope, audience)
2. **Executive Summary** (role, integration snapshot, top 10 findings, readiness score, top 5 actions)
3. **Reader Guide** (Ops/SRE, Integration/Platform, Developers)
4. **Repository Map & Service Identity**
5. **Functional Role & Capabilities**
6. **System Context & Interactions** (integration matrix + contract surfaces)
7. **Critical Business Flows** (3–5, with sequence diagrams)
8. **Configuration Model & Environment Mapping**
9. **Data Layer (Ops-focused only)**
10. **Deployment & Kubernetes Readiness**
11. **Observability & Operability**
12. **Testing Overview (Reference Only)**
13. **Risks, Unknowns, and Deployment Readiness**
14. **Verification Checklist** (must be filled; no empty evidence unless Unknown)

## Document B: DEPLOYMENT_RUNBOOK.md (Fixed Sections)

1. **Dependencies & Connectivity** (include how to verify)
2. **Build & Package** (evidence-backed)
3. **Configuration & Secrets** (required keys + references)
4. **Local Run (Minimal)** (evidence-backed or Unknown)
5. **Kubernetes Deployment Steps** (assets if present; otherwise blueprint with placeholders)
6. **Post‑deploy Validation** (smoke tests + health checks)
7. **Troubleshooting Playbook (Top 10)** (symptom → causes → checks → fixes)
8. **Rollback Strategy** (asset-based; otherwise generic guidance labeled as such)
9. **Operational Checklists** (Go‑live / Day‑2)
10. **Monitoring Suggestions** (tied to critical flows; evidence-backed)

## Presentation Requirements

- Write for Ops/SRE, cross-team readable.
- Use progressive disclosure: start high-level, then go deeper.
- Use tables for integration matrix, config inventory, endpoints, dependencies.
- Use Mermaid diagrams for visualization.
- Make Unknowns explicit and traceable to missing evidence.

## Bundled References (Templates)

Use these files to keep output consistent and report-grade:

- `references/integration-matrix.md`
- `references/config-inventory.md`
- `references/mermaid-diagrams.md`
- `references/readiness-score.md`
- `references/report-outline.md`

## Diagrams (Mandatory)

- At least 2 Mermaid diagrams:
    - Component diagram (service + external dependencies)
    - Module dependency diagram (if multi-module)
- Sequence diagram for each critical business flow.

## Production Readiness Score (0–100)

- Provide a score breakdown with explicit evidence for each sub-score.
- If evidence is missing, score that dimension low and explain why.

## Internal Multi‑pass Method (Silent)

PASS 0: Absorb `java-architect` and `java-reviewer` baselines.  
PASS 1: Scan repo structure, detect modules/build/configs/entrypoints.  
PASS 2: Identify integrations and create integration matrix; draft diagrams.  
PASS 3: Trace 3–5 critical flows end-to-end with evidence.  
PASS 4: Extract K8s/deployment signals: ports, health endpoints, env vars, dependencies.  
PASS 5: Summarize tests at high level and CI invocation if evidenced.  
PASS 6: Self-verify against checklist; re-scan missing areas until completed or marked Unknown.  
PASS 7: Produce final docs with no contradictions and explicit Unknowns.

## Self‑Verification Checklist (Must Include in Final Report)

- [ ] Absorb java-architect baseline OR mark Unknown (not accessible).
- [ ] Absorb java-reviewer baseline OR mark Unknown (not accessible).
- [ ] Identify build tool(s) and Java version with evidence.
- [ ] Identify runtime type (service/batch/lib/worker) with evidence.
- [ ] Locate entrypoints (main classes / SpringBootApplication / jobs) with evidence.
- [ ] Map configuration model & precedence with evidence (or Unknown).
- [ ] Build an integration matrix with evidence anchors for each partner.
- [ ] Produce at least 2 Mermaid diagrams (component + module dependency).
- [ ] Identify 3–5 critical business flows and provide sequence diagrams (or Unknown with reason).
- [ ] List API endpoints grouped by controller with evidence (or Unknown).
- [ ] Document messaging/async OR state “Not Found in Repo” with proof.
- [ ] Document minimal data layer essentials & migrations with evidence (or Unknown).
- [ ] Derive K8s deployment needs (ports, probes, env vars, dependencies) with evidence (or Unknown).
- [ ] Summarize tests (reference only) + CI invocation evidence (or Unknown).
- [ ] Provide ops runbook with troubleshooting + rollback guidance.
- [ ] Verification checklist table: no empty evidence fields unless Status=Unknown.

## Style & Focus

- English only.
- Business/logic first, operations second, testing last.
- Use tables for inventories and matrices.
- Make Unknowns explicit and traceable to missing evidence.

## Focus Control (Prevent Drift / Keep It High-Signal)

Use these rules to avoid over-detailing and stay aligned with business/ops priorities:

- **Always start from business capability and critical flows**; do not start from utilities or low-level code.
- **Prefer boundary evidence**: controllers/handlers/jobs/listeners, integration clients, repositories, config entrypoints.
- **De‑prioritize internals**: helpers, DTO mappers, internal utils, minor refactors, stylistic patterns.
- **Cap detail depth**: for each section, include only evidence that changes ops decisions or explains a critical flow.
- **If unsure relevance**: label as “Ancillary” and keep to 1–2 lines, or omit.

## Evidence Weighting (What Counts as “Important”)

Rank evidence by operational impact:

1. **System boundaries** (ingress/egress, auth, protocols)
2. **Business‑critical flows** (money movement, core transactions, lifecycle events)
3. **Data ownership & persistence** (writes, migrations, schema changes)
4. **Runtime & deploy** (ports, probes, shutdown, env vars)
5. **Observability signals** (logs/metrics/trace hooks)
6. **Quality signals** (from `java-reviewer`, non-test only)

Only surface lower‑rank items if higher‑rank items are complete.

## Depth Limits (Anti‑Noise)

- Max 3–5 critical flows; if fewer, explain why.
- Integration matrix: top external dependencies first; internal-only libs summarized.
- Endpoints: group by controller; do not list every endpoint if it doesn’t affect ops.
- Tests: reference-only summary; never deep dive into test logic.

## Version

0.6
