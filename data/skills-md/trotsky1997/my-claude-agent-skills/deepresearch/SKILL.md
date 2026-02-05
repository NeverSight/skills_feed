---
name: deepresearch
description: Comprehensive DeepResearch methodology for conducting rigorous, traceable research projects with quality gates, structured analysis, and decision-ready deliverables. Use when (1) Conducting deep research projects requiring evidence-based analysis, (2) Managing research progress with quality gates and artifacts, (3) Producing research reports with traceable sources and structured reasoning, (4) Applying OSINT verification techniques, (5) Using structured analytic techniques (ACH, Key Assumptions Check, Red Team), (6) Expressing uncertainty and confidence in research findings, (7) Ensuring research deliverables meet intelligence tradecraft standards (ICD 203/206/208)
metadata:
  short-description: DeepResearch methodology with quality gates and structured analysis

---

# DeepResearch Methodology

A comprehensive methodology for conducting rigorous, traceable research projects that produce decision-ready deliverables with evidence-based analysis, structured reasoning, and quality gates.

## Core Principles

1. **Artifact-driven progress**: Research is organized into 5 stages, each producing required deliverables
2. **Quality gates**: Each stage has explicit quality criteria that must be met before proceeding
3. **Traceable evidence**: Every claim must be traceable to sources with proper citation
4. **Structured analysis**: Use structured analytic techniques to mitigate bias and improve rigor
5. **Uncertainty expression**: Clearly distinguish facts, judgments, and speculation with likelihood and confidence
6. **Decision-ready outputs**: Deliverables are structured for immediate use by decision-makers

## Recommended Tools

### Cursor IDE Browser (cursor-ide-browser)

The **cursor-ide-browser** MCP server is highly recommended for DeepResearch projects. It enables browser automation directly within Cursor IDE, making information collection, verification, and OSINT work more efficient and traceable.

**Key Use Cases**:

1. **Information Collection (Stage 3)**:
   - Navigate to official sources, company websites, regulatory filings
   - Capture screenshots with timestamps for audit trail
   - Extract structured data from web pages
   - Archive web pages before they change or disappear

2. **OSINT Verification (Stage 4)**:
   - Reverse image search on multiple platforms (Google Images, TinEye, Yandex)
   - Verify social media posts and UGC authenticity
   - Check geolocation using map services
   - Capture verification evidence (screenshots, page snapshots)

3. **Source Archiving**:
   - Take full-page screenshots of key sources
   - Capture page snapshots with accessibility tree for later analysis
   - Document page state at time of access (for reproducibility)

4. **Cross-Platform Verification**:
   - Navigate between multiple sources to verify consistency
   - Check multiple language versions of same content
   - Verify across different platforms (official site, news, social media)

**Best Practices**:
- Always capture screenshots/snapshots when accessing sources (for audit trail)
- Use browser navigation to verify links are still active
- Take snapshots before archiving (captures full page state)
- Use browser console to check for dynamic content or hidden information

**Integration with Workflow**:
- **collection-strategist**: Use browser to access and archive sources during collection
- **verification-expert**: Use browser for reverse image search, geolocation verification, UGC checking
- **evidence-librarian**: Use browser to verify citations and capture source snapshots

See [OSINT_VERIFICATION.md](references/OSINT_VERIFICATION.md) for detailed browser-based verification techniques.

## Research Stages

### Stage A: Task Contract (0→1)
**Deliverables:**
- Task Contract: Goal, audience, time window, scope, non-goals, deliverable format
- KIQs (Key Intelligence Questions): 3-7 must-answer questions
- Success criteria: Definition of "good enough" and "unobtainable"

**Quality Gate 1:** Research questions are answerable, falsifiable, with clear time windows. Non-goals are explicit. KIQs ≤ 7 and actionable.

### Stage B: Decomposition & Planning (1→Plan)
**Deliverables:**
- Issue tree / Hypothesis set (MECE decomposition + initial hypotheses)
- Collection plan: Source map, retrieval routes, priorities, verification strategy
- Risk log: Data gaps, timeliness, compliance boundaries, conflicting evidence expectations

**Quality Gate 2:** Issue tree is MECE. Each sub-question has evidence requirements and source routes. Cross-validation design exists (at least two complementary source types).

### Stage C: Collection & Registration (Plan→Evidence)
**Deliverables:**
- Source Register: Type, time, reliability, bias risk, usable scope for each source
- Evidence Table: Claim→Evidence→Strength→Conflict→Notes
- Collection log: Query strings, timestamps, exclusion reasons (for reproducibility and audit)

**Quality Gate 3:** Key claims coverage reaches threshold (e.g., 70% of core claims have usable evidence). Evidence is from traceable sources with timestamps/versions. Conflicts are explicitly recorded.

### Stage D: Analysis & Convergence (Evidence→Judgment)
**Deliverables:**
- Structured analysis workbook: ACH/Key Assumptions Check/Red Team (at least 1-2 techniques)
- Key Judgments (3-7): Each with likelihood + confidence + evidence anchors
- Alternative explanations and flip conditions: What would change my mind / signposts

**Quality Gate 4:** At least 1 alternative explanation exists and is evaluated. Key assumptions are explicit. Most vulnerable assumption is identified. Confidence matches evidence strength.

### Stage E: Delivery & Review (Judgment→Product)
**Deliverables:**
- Deliverable (brief/memo/table/appendices package)
- QA checklist record: Fact-checking, traceable citations, consistent uncertainty expression
- Follow-up actions: Gap list, next collection suggestions, monitoring indicators

**Quality Gate 5:** Key Judgments are conclusion-first, clear language, audience-appropriate. Each judgment has traceable citations. Uncertainty is expressed consistently. Inference is distinguished from fact.

## Quick Start Workflow

> **⚠️ MANDATORY FIRST STEP**: Before starting any DeepResearch project, create `AGENTS.md` in project root using `@cursor-agents-md`. This file defines project-specific instructions that all research work must follow.

1. **Create AGENTS.md** (MANDATORY):
   ```
   @cursor-agents-md Create an AGENTS.md file for this DeepResearch project
   ```
   - Must include project-specific research guidelines
   - Must include reminder to read `cursor-agents-md` before updates
   - Must be in project root directory

2. **Create Task Contract**: Define research question, KIQs, scope, and success criteria
3. **Build Issue Tree**: MECE decomposition with initial hypotheses
4. **Develop Collection Plan**: Source map with cross-validation strategy
5. **Collect & Register**: Build Source Register and Evidence Table as you collect
6. **Analyze**: Apply structured analytic techniques (see [STRUCTURED_ANALYSIS.md](references/STRUCTURED_ANALYSIS.md))
7. **Synthesize**: Generate Key Judgments with likelihood and confidence
8. **Deliver**: Create deliverable following [REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md) and run [QA_CHECKLIST.md](references/QA_CHECKLIST.md)

## Evidence-Chain Production Line (12-Stage Workflow)

The complete workflow from problem to usable conclusions, with subagent assignments:

### Stage 0: Task Contract Definition
**Subagent**: `research-lead`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Decision-maker's vague question | Define decision goal, boundaries, time window, success criteria | Task Contract v1 | Does "falsifiable judgment" exist? |

> **⚠️ MANDATORY PREREQUISITE**: Before starting Stage 0, ensure `AGENTS.md` exists in project root. If not, create it using `@cursor-agents-md`.

**Checklist**:
- [ ] **AGENTS.md exists** (created using `@cursor-agents-md`)
- [ ] Research question is falsifiable and testable
- [ ] Non-goals are explicit
- [ ] Time window defined
- [ ] Success criteria clear
- [ ] Deliverable format specified

**Handoff to**: `methodologist` (for KIQ decomposition)

---

### Stage 1: KIQ & Claim Draft
**Subagents**: `research-lead` + `methodologist`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Task Contract | Break into KIQs; form initial Key Claims | Claim Tree v1 | Do "falsifiable" claims exist? |

**Collaboration**:
- `research-lead`: Defines KIQs and priority
- `methodologist`: Ensures claims are falsifiable, suggests hypothesis structure

**Handoff to**: `collection-strategist` (for source map design)

**Checklist**:
- [ ] KIQs ≤ 7
- [ ] Each KIQ has corresponding claims
- [ ] Claims are falsifiable
- [ ] Priority order established

---

### Stage 2: Source Map Design
**Subagent**: `collection-strategist`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Claim Tree | Design source type combinations for each claim | Source Map | Each claim has ≥2 independent source types? |

**Handoff to**: Collectors (Stage 3) + `verification-expert` (for verification strategy)

**Checklist**:
- [ ] Each claim mapped to ≥2 source types
- [ ] Cross-validation design exists
- [ ] Retrieval routes specified
- [ ] Archiving strategy defined
- [ ] Language variants considered

---

### Stage 3: Collection & Archiving
**Subagents**: `collection-strategist` + Collectors

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Source Map | Search, download, archive, tag | Evidence Pool | Is it auditable? Are original copies available? |

**Collaboration**:
- `collection-strategist`: Monitors coverage, adjusts strategy
- Collectors: Execute retrieval, archive materials

**Recommended Tool**: Use **cursor-ide-browser** to:
- Navigate to sources and capture screenshots/snapshots immediately
- Archive web pages before they change or disappear
- Verify links are still active
- Extract structured data from web pages

**Handoff to**: `verification-expert` (Stage 4)

**Checklist**:
- [ ] Original sources archived
- [ ] Screenshots/snapshots captured (browser evidence)
- [ ] Timestamps recorded
- [ ] Archive links created
- [ ] Metadata captured
- [ ] Coverage threshold met (e.g., 70% of core claims)

---

### Stage 4: OSINT Verification
**Subagent**: `verification-expert`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Evidence Pool | Deception removal, time-geography consistency check | Verified Evidence | Does it pass "falsify first" test? |

**Recommended Tool**: Use **cursor-ide-browser** to:
- Perform reverse image/video search across multiple platforms
- Verify geolocation using map services (Google Maps/Earth)
- Check social media accounts and capture snapshots
- Verify chronolocation using weather/timezone services
- Capture verification evidence (screenshots, snapshots) at each step

**Handoff to**: `evidence-librarian` (Stage 5)

**Checklist**:
- [ ] UGC verified (source, time, location, originality)
- [ ] Images/videos geolocated (if applicable)
- [ ] Chronolocation verified
- [ ] Consistency checks passed
- [ ] Verification log complete
- [ ] Browser-captured evidence included (screenshots, snapshots)

---

### Stage 5: Evidence Registration
**Subagent**: `evidence-librarian`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Verified Evidence | Build Claim–Evidence Table | Evidence Register | Does each key judgment have evidence? |

**Handoff to**: `methodologist` (Stage 6) + `quant-analyst` (for data consistency)

**Checklist**:
- [ ] Source Register complete
- [ ] Evidence Table built
- [ ] Each claim linked to evidence
- [ ] Conflicts explicitly recorded
- [ ] Citations traceable

---

### Stage 6: Structured Reasoning
**Subagent**: `methodologist`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Evidence Register | ACH, hypothesis competition, discriminating evidence | Hypothesis Matrix | Do competing worlds exist? |

**Collaboration**:
- May consult `domain-expert` for mechanism plausibility
- May consult `quant-analyst` for data consistency

**Handoff to**: `quant-analyst` (Stage 7) + `devils-advocate` (Stage 8)

**Checklist**:
- [ ] ACH matrix complete
- [ ] At least 2 competing hypotheses
- [ ] Discriminating evidence identified
- [ ] Key assumptions checked
- [ ] Alternative explanations evaluated

---

### Stage 7: Data Consistency & Sensitivity
**Subagent**: `quant-analyst`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Hypothesis Matrix | Metric unification, sensitivity analysis | Consistency Pack | Are conclusions sensitive to assumptions? |

**Handoff to**: `devils-advocate` (Stage 8) + `domain-expert` (Stage 9)

**Checklist**:
- [ ] Metrics unified
- [ ] Consistency checks passed
- [ ] Sensitivity analysis complete
- [ ] Error ranges specified
- [ ] Timeline closed (if applicable)

---

### Stage 8: Counter-World Attack
**Subagent**: `devils-advocate`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Consistency Pack | Construct counter-worlds, Kill Points | Adversarial Review | Do single-point failures exist? |

**Key Activities**:
1. Construct 2-4 counterfactual worlds
2. Identify Kill Points (evidence that if falsified, conclusion fails)
3. Create Fragility Map (which judgments sensitive to which assumptions)
4. Write Adversarial Review Memo
5. Design Decision-Failure Simulation

**Checklist**:
- [ ] At least 2 counterfactual worlds
- [ ] Kill points identified
- [ ] Fragility map complete
- [ ] Adversarial review challenges main conclusion
- [ ] Failure scenarios designed

**Handoff to**: `domain-expert` (Stage 9) + `methodologist` (if re-analysis needed)

---

### Stage 9: Domain Mechanism Validation
**Subagent**: `domain-expert`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Adversarial Review | Mechanism plausibility check | Mechanism Memo | Does it violate industry common sense? |

**Handoff to**: `editor` (Stage 10)

**Checklist**:
- [ ] Mechanisms are plausible
- [ ] Industry patterns respected
- [ ] Anomalies flagged
- [ ] Context provided
- [ ] Common sense boundaries checked

---

### Stage 10: Conclusion Packaging
**Subagent**: `editor`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Mechanism Memo | Pyramid structure, risk grading | Draft Report | Can conclusions be grasped in 3 minutes? |

**Key Activities**:
1. Structure: Conclusion-first pyramid
2. Language: Precise uncertainty expression
3. Format: Scannable, forwardable
4. Risk narrative: Clear and actionable

**Handoff to**: `qa-gatekeeper` (Stage 11)

**Checklist**:
- [ ] Conclusion-first structure
- [ ] Key Judgments clear
- [ ] Uncertainty expressed consistently
- [ ] 3-minute grasp test passed
- [ ] Evidence anchors present

---

### Stage 11: QA Gate
**Subagent**: `qa-gatekeeper`

| Input | Actions | Output | Gate |
|-------|---------|--------|------|
| Draft Report | Method audit, compliance check | Go / No-Go | Is release permitted? |

**Key Activities**:
1. Tradecraft QA (all 8 dimensions from rubric)
2. Compliance check (ethics, privacy, permissions)
3. Risk assessment
4. Final Go/No-Go decision

**Checklist**:
- [ ] All quality gates passed
- [ ] Compliance verified
- [ ] Ethics boundaries respected
- [ ] Risk acceptable
- [ ] Ready for delivery

**If No-Go**: Return to appropriate stage with specific feedback

## Key Resources

### Templates & Checklists
- **[PROJECT_MANAGEMENT.md](references/PROJECT_MANAGEMENT.md)**: Complete project management template with all stages, gates, and tracking tables
- **[REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md)**: Standard report template with all required sections
- **[QA_CHECKLIST.md](references/QA_CHECKLIST.md)**: Pre-delivery quality assurance checklist

### Methodology Guides
- **[STRUCTURED_ANALYSIS.md](references/STRUCTURED_ANALYSIS.md)**: Structured analytic techniques (ACH, Key Assumptions Check, Red Team, etc.)
- **[OSINT_VERIFICATION.md](references/OSINT_VERIFICATION.md)**: OSINT verification techniques for UGC, images, videos, geolocation
- **[UNCERTAINTY_EXPRESSION.md](references/UNCERTAINTY_EXPRESSION.md)**: How to express likelihood, confidence, and distinguish facts/judgments/speculation

### Quality Standards
- **[RUBRIC.md](references/RUBRIC.md)**: Evaluation rubric with 8 dimensions and scoring criteria
- **[ETHICS_GUARDRAILS.md](references/ETHICS_GUARDRAILS.md)**: Compliance and ethics boundaries

### Team & Subagents System
All subagent system documentation is integrated into this SKILL.md file. See sections:
- **Subagents System Setup**: Initialization and setup instructions
- **Evidence-Chain Production Line**: Complete 12-stage workflow with subagent assignments
- **Weekly Research Rituals**: Fixed weekly ceremonies
- **Subagent Role Definitions**: Detailed role descriptions for all 10 subagents

## Evidence & Citation Standards

### Source Register Minimum Fields
- Type (official/company/media/academic/UGC/database)
- Provenance (who produced, when, version)
- Access path (how obtained/paid/scraped)
- Bias risks (stakeholder interests, propaganda tendency, method limitations)
- Reliability (High/Medium/Low + rationale)
- Use limits (what it can prove)

### Evidence Table Structure
- Claim (falsifiable assertion)
- Evidence (citation + summary)
- Supports/Contradicts (which hypothesis)
- Strength (Strong/Medium/Weak: based on method and independence)
- Alternative explanations
- Notes (gaps, next verification steps)

### Citation Requirements
- Each Key Judgment: At least 2 independent sources (or 1 primary authoritative + explanation why sufficient)
- Each key number/timeline node: Must be traceable to original source or clear derivation chain
- Conflicting evidence: Must be explicitly presented with explanation of choice and remaining uncertainty

## Structured Analytic Techniques

Select technique based on problem type:
- **Causal attribution / Who did it** → ACH + prioritize disconfirming evidence
- **Future prediction / Risk** → Scenario planning + indicator framework
- **Strong consensus** → Devil's Advocacy / Team A-Team B
- **Unstable key premises** → Key Assumptions Check
- **Adversary intent/behavior** → Red Team (avoid mirror imaging)

See [STRUCTURED_ANALYSIS.md](references/STRUCTURED_ANALYSIS.md) for detailed procedures.

## Uncertainty Expression

### Three Categories (Kent)
- **Fact**: Observable, verifiable with high certainty
- **Judgment/Estimate**: Evidence sufficient but still probabilistic
- **Inference/Speculation**: Limited evidence, more logic-based

### Probability Words (5-tier)
- Almost impossible
- Unlikely
- Possible
- Likely
- Almost certain

### Confidence Levels
- **High**: Multiple independent sources, consistent, high-quality methods
- **Medium**: Some independent verification, partial consistency
- **Low**: Single source, high uncertainty, limited verification

Each Key Judgment must include: Likelihood (probability word) + Confidence (High/Medium/Low) + Why (evidence and method rationale)

See [UNCERTAINTY_EXPRESSION.md](references/UNCERTAINTY_EXPRESSION.md) for detailed guidance.

## Common Failure Modes

### Scope Creep
**Symptom**: Delivery date approaching but questions multiplying, conclusions becoming vague
**Solution**: Force return to Task Contract. New questions must answer:
1. Will not doing it affect the decision?
2. Is there an evidence path? If unobtainable, move to "future work", not current scope

### Last-Minute Citation & Verification
**Symptom**: Report finished but evidence doesn't match/links broken/inconsistent metrics
**Solution**: Front-load citation and evidence registration:
- Register sources during collection (Source Register)
- Pull evidence from Evidence Table when writing conclusions (not from memory)

## Project Rhythm (1-2 week research)

- **Day 1**: Task Contract + Issue tree + Collection plan (Gate 1/2)
- **Day 2-4**: Collection + registration + initial Evidence Table (daily Gate 3)
- **Day 5**: Structured analysis (ACH/Key Assumptions Check) + initial Key Judgments (Gate 4)
- **Day 6**: Fill gaps, handle conflicts, update confidence
- **Day 7**: Deliverable writing + Red Team + QA (Gate 5)

## Daily Standup (10 minutes)
- What new "usable evidence" was added yesterday (not "what was read")
- What hypothesis/gap will be verified today
- Blockers: Can't get data? Conflicting evidence? Scope change?

## Tradecraft Review (every 2-3 days)
- Are claims covered? Are conflicts recorded?
- Is there a tendency toward "feeling-based convergence"?
- Does collection strategy need adjustment (change source types, languages, timeline)?

## Red Team / Devil's Advocate (24 hours before delivery)
- What is the most vulnerable point of your conclusion?
- Which evidence is weakest? What if it's wrong?
- Have you "missed alternative explanations"?

## Weekly Research Rituals

Fixed weekly ceremonies that support the evidence-chain production line:

### Ritual Overview

| Ritual | Frequency | Duration | Participants | Purpose |
|--------|-----------|----------|--------------|---------|
| Claim Review | Weekly | 30 min | research-lead, methodologist | Prevent scope drift |
| Kill Point Review | Weekly | 30 min | devils-advocate, research-lead | Identify single-point failures |
| Conflict Evidence Stand-up | Weekly | 15 min | evidence-librarian, all | Make conflicting evidence explicit |
| Devil's Day | Bi-weekly | 2 hours | devils-advocate, all | Counter-world attack session |
| QA Pre-Gate | Before delivery | 1 hour | qa-gatekeeper, editor | Pre-release failure simulation |

---

### 1. Claim Review (Monday, 30 min)
**Participants**: `research-lead` (facilitator), `methodologist`  
**Optional**: `collection-strategist`, `domain-expert`

**Agenda**:

1. **Review Current Claims** (10 min)
   - List all active claims from Claim Tree
   - Check: Are they still falsifiable?
   - Check: Do they still answer KIQs?

2. **Scope Check** (10 min)
   - Compare claims to Task Contract
   - Identify scope drift
   - Decide: Keep, modify, or remove claims

3. **Priority Update** (10 min)
   - Re-rank claims by decision impact
   - Identify which claims need evidence first
   - Update collection priorities

**Outputs**:
- Updated Claim Tree
- Priority Matrix
- Scope Change Log (if any)

**Success Criteria**:
- [ ] All claims traceable to KIQs
- [ ] No scope drift beyond Task Contract
- [ ] Priorities reflect decision needs

---

### 2. Kill Point Review (Wednesday, 30 min)
**Participants**: `devils-advocate` (facilitator), `research-lead`, `methodologist`, `evidence-librarian`

**Agenda**:

1. **Identify Kill Points** (15 min)
   - Review current Key Judgments
   - For each judgment: What evidence, if falsified, would kill it?
   - List all Kill Points

2. **Assess Fragility** (10 min)
   - Which judgments have single-point failures?
   - Which assumptions are most vulnerable?
   - Create Fragility Map

3. **Action Plan** (5 min)
   - Which Kill Points need additional evidence?
   - Which need re-verification?
   - Assign follow-up tasks

**Outputs**:
- Kill-Point List (updated)
- Fragility Map
- Action Items

**Success Criteria**:
- [ ] All Key Judgments have identified Kill Points
- [ ] Single-point failures flagged
- [ ] Action plan for strengthening weak points

---

### 3. Conflict Evidence Stand-up (Friday, 15 min)
**Participants**: `evidence-librarian` (facilitator), all subagents (brief check-in)

**Agenda**:

1. **New Conflicts** (5 min)
   - `evidence-librarian` reports new conflicting evidence
   - Brief description: What conflicts, why

2. **Status Update** (5 min)
   - Each subagent: Any conflicts discovered in their work?
   - Quick round: "I found X conflicting with Y"

3. **Next Steps** (5 min)
   - Which conflicts need investigation?
   - Assign to appropriate subagent
   - Update Conflict Evidence Log

**Outputs**:
- Updated Conflict Evidence Log
- Action Items for conflict resolution

**Success Criteria**:
- [ ] All conflicts explicitly recorded
- [ ] No conflicts "hidden" or ignored
- [ ] Action plan for each conflict

---

### 4. Devil's Day (Bi-weekly, 2 hours)
**Participants**: `devils-advocate` (facilitator), all subagents (full participation)

**Agenda**:

1. **Current State Review** (20 min)
   - `research-lead`: Current Key Judgments
   - `methodologist`: Current hypothesis status
   - `evidence-librarian`: Evidence summary

2. **Counter-World Construction** (40 min)
   - `devils-advocate` presents 2-3 alternative explanations
   - Group discussion: Can these worlds explain the evidence?
   - Identify what evidence would distinguish worlds

3. **Adversarial Attack** (40 min)
   - `devils-advocate` attacks evidence chain
   - Each subagent defends their work
   - Identify weaknesses and gaps

4. **Action Plan** (20 min)
   - What needs re-verification?
   - What evidence is missing?
   - Update Fragility Map and Kill Points

**Outputs**:
- Adversarial Review Memo
- Updated Kill-Point List
- Re-verification Plan
- Updated Fragility Map

**Success Criteria**:
- [ ] At least 2 counterfactual worlds constructed
- [ ] Evidence chain weaknesses identified
- [ ] Action plan for strengthening conclusions

**Rules**:
- `devils-advocate` must be systematic, not emotional
- All participants must engage, not just listen
- Focus on structure, not personalities

---

### 5. QA Pre-Gate (Before delivery, 1 hour)
**Participants**: `qa-gatekeeper` (facilitator), `editor`, `research-lead`, optional `devils-advocate`

**Agenda**:

1. **Pre-Flight Check** (15 min)
   - `editor`: Deliverable status
   - `research-lead`: Key Judgments summary
   - `qa-gatekeeper`: QA checklist preview

2. **Rubric Review** (30 min)
   - Go through 8-dimension rubric
   - Score each dimension (1-5)
   - Identify any dimensions ≤2 (must fix)

3. **Failure Simulation** (10 min)
   - `qa-gatekeeper`: "What if this is wrong?"
   - Identify worst-case scenarios
   - Check: Are risks acceptable?

4. **Go/No-Go Decision** (5 min)
   - `qa-gatekeeper`: Final decision
   - If Go: Approval for delivery
   - If No-Go: Specific feedback and return stage

**Outputs**:
- QA Report
- Rubric Scores
- Go/No-Go Decision
- Action Items (if No-Go)

**Success Criteria**:
- [ ] All dimensions ≥3 (ideally ≥4)
- [ ] No critical issues
- [ ] Risks acceptable
- [ ] Ready for delivery

---

### Ritual Integration with Workflow

**Weekly Schedule Example**:

- **Monday**: Morning: Claim Review (30 min); Rest of day: Normal workflow
- **Wednesday**: Morning: Kill Point Review (30 min); Rest of day: Normal workflow
- **Friday**: Morning: Conflict Evidence Stand-up (15 min); Afternoon (bi-weekly): Devil's Day (2 hours)
- **Before Delivery**: 24-48 hours: QA Pre-Gate (1 hour)

**Ritual Outputs Feed Workflow**:
- **Claim Review** → Updates Stage 1 (KIQ & Claim Draft)
- **Kill Point Review** → Updates Stage 8 (Counter-World Attack)
- **Conflict Evidence Stand-up** → Updates Stage 5 (Evidence Registration)
- **Devil's Day** → May trigger return to Stage 6 (Structured Reasoning) or Stage 2 (Source Map)
- **QA Pre-Gate** → Final check before Stage 11 (QA Gate)

**Adapting Rituals**:
- **Smaller teams**: Combine roles, reduce frequency
- **Tighter timelines**: Shorten durations, focus on critical rituals
- **Larger teams**: Add sub-rituals, more detailed agendas

**Common Pitfalls**:
1. **Skipping rituals**: "We don't have time" → Leads to scope drift, missed conflicts
2. **Rituals become formalities**: No real engagement → No value
3. **Wrong participants**: Missing key roles → Incomplete reviews
4. **No follow-up**: Rituals identify issues but no action → Problems persist

**Solution**: Treat rituals as **essential quality gates**, not optional meetings.

---

## Subagents System Setup

### Initializing Subagents in Your Workspace

To use the DeepResearch subagents system, you need to copy the subagent definitions from the skill to your workspace:

**Source**: `@deepresearch/subagents/.cursor/agents/`  
**Destination**: Your workspace `.cursor/agents/` directory

### Setup Steps

> **⚠️ MANDATORY FIRST STEP**: Before initializing subagents, you **MUST** create an `AGENTS.md` file in your project root using the `cursor-agents-md` skill. This file defines project-specific instructions for all DeepResearch work.

1. **Create AGENTS.md** (MANDATORY):
   ```
   @cursor-agents-md Create an AGENTS.md file for this DeepResearch project
   ```
   
   The AGENTS.md file must include:
   - Project-specific research guidelines
   - Code style and documentation standards (if applicable)
   - File structure and organization rules
   - Boundaries and constraints
   - **Important**: Add a reminder to read `cursor-agents-md` skill before updating AGENTS.md
   
   **Required content in AGENTS.md**:
   ```markdown
   > **⚠️ Important:** You must read `cursor-agents-md` skills every time before write or update this `AGENTS.md`.
   
   # DeepResearch Project Instructions
   
   [Project-specific guidelines for DeepResearch work]
   ```

2. **Create workspace agents directory** (if it doesn't exist):
   ```
   mkdir -p .cursor/agents
   ```

2. **Copy subagent definitions** from the skill:
   - Copy all `.md` files from `@deepresearch/subagents/.cursor/agents/` to your workspace `.cursor/agents/`
   - Required files:
     - `research-lead.md`
     - `collection-strategist.md`
     - `verification-expert.md`
     - `evidence-librarian.md`
     - `methodologist.md`
     - `quant-analyst.md`
     - `domain-expert.md`
     - `editor.md`
     - `qa-gatekeeper.md`
     - `devils-advocate.md`

3. **Verify Cursor settings**:
   - Ensure Cursor is in Nightly mode (Settings > Cursor Settings > Beta > Nightly)
   - Subagents feature should be enabled (Settings > Cursor Settings > Subagents)

4. **Test subagent invocation**:
   ```
   @research-lead Create a Task Contract for researching [topic]
   ```

### Subagent Roles

| Subagent | Role | Key Responsibility |
|----------|------|-------------------|
| `research-lead` | Research Lead | Task Contract, Priority, Final Judgments |
| `collection-strategist` | Collection Strategist | Source Map Design, Retrieval Routes |
| `verification-expert` | OSINT Verification Expert | Truth Testing, Evidence Chain |
| `evidence-librarian` | Evidence Librarian | Source Register, Evidence Table |
| `methodologist` | Analytic Methodologist | Structured Analysis, Hypothesis Competition |
| `quant-analyst` | Data Analyst | Data Consistency, Sensitivity Analysis |
| `domain-expert` | Domain Expert | Mechanism Validation, Plausibility Check |
| `editor` | Editor/Storyliner | Decision Packaging, Report Writing |
| `qa-gatekeeper` | QA/Ethics Gatekeeper | Quality Gates, Compliance Check |
| `devils-advocate` | Devil's Advocate | Adversarial Review, Counter-Hypotheses |

### Using Subagents

Invoke subagents using the Task tool in Cursor:

```
@research-lead Create a Task Contract for researching [topic]
@collection-strategist Design a Source Map for these claims: [claims]
@verification-expert Verify this image: [image URL]
@evidence-librarian Register this evidence: [evidence details]
@methodologist Apply ACH to these hypotheses: [hypotheses]
@quant-analyst Check consistency of these numbers: [numbers]
@domain-expert Validate this mechanism: [mechanism description]
@editor Package this research into a report: [research content]
@qa-gatekeeper Perform QA on this report: [report]
@devils-advocate Challenge this conclusion: [conclusion]
```

### Subagent Workflow Integration

Each subagent is assigned to specific workflow stages:
- **Stage 0-1**: `research-lead` + `methodologist`
- **Stage 2-3**: `collection-strategist`
- **Stage 4**: `verification-expert`
- **Stage 5**: `evidence-librarian`
- **Stage 6**: `methodologist`
- **Stage 7**: `quant-analyst`
- **Stage 8**: `devils-advocate`
- **Stage 9**: `domain-expert`
- **Stage 10**: `editor`
- **Stage 11**: `qa-gatekeeper`

See "Evidence-Chain Production Line" section above for detailed stage-by-stage SOP and "Weekly Research Rituals" section for weekly ceremony procedures.

### Complete Subagent Initialization Guide

#### Prerequisites

> **⚠️ MANDATORY FIRST STEP**: Before initializing subagents, you **MUST** create an `AGENTS.md` file in your project root using the `cursor-agents-md` skill.

**Step 0: Create AGENTS.md** (MANDATORY):

1. **Invoke cursor-agents-md skill**:
   ```
   @cursor-agents-md Create an AGENTS.md file for this DeepResearch project
   ```

2. **Required content in AGENTS.md**:
   ```markdown
   > **⚠️ Important:** You must read `cursor-agents-md` skills every time before write or update this `AGENTS.md`.
   
   # DeepResearch Project Instructions
   
   ## Project Overview
   [Describe your research project]
   
   ## Research Guidelines
   [Project-specific research guidelines]
   
   ## File Structure
   [How research files should be organized]
   
   ## Boundaries
   [What should never be done]
   ```

3. **Verify AGENTS.md exists**:
   ```bash
   ls AGENTS.md  # Should exist in project root
   ```

**Why this is mandatory**: AGENTS.md provides project-specific context that all subagents need to work effectively. Without it, subagents lack project-specific guidelines and may make incorrect assumptions.

#### Copying Subagent Files

**Option 1: Manual Copy (Recommended)**

1. **Locate the skill's subagent directory**:
   - Path: `@deepresearch/subagents/.cursor/agents/`
   - Or: `[skill-install-path]/deepresearch/subagents/.cursor/agents/`

2. **Create workspace agents directory** (if it doesn't exist):
   ```bash
   mkdir -p .cursor/agents
   ```

3. **Copy all subagent files**:
   ```bash
   # Windows (PowerShell)
   Copy-Item "@deepresearch/subagents/.cursor/agents/*.md" -Destination ".cursor/agents/" -Exclude "README.md"
   
   # Linux/Mac
   cp @deepresearch/subagents/.cursor/agents/*.md .cursor/agents/ --exclude README.md
   ```

4. **Required files to copy**:
   - `research-lead.md`
   - `collection-strategist.md`
   - `verification-expert.md`
   - `evidence-librarian.md`
   - `methodologist.md`
   - `quant-analyst.md`
   - `domain-expert.md`
   - `editor.md`
   - `qa-gatekeeper.md`
   - `devils-advocate.md`

**Option 2: Using Cursor's File Operations**

1. Open Cursor IDE
2. Navigate to `@deepresearch/subagents/.cursor/agents/`
3. Select all `.md` files (except `README.md`)
4. Copy to your workspace `.cursor/agents/` directory

#### Verification

After copying, verify the setup:

1. **Check AGENTS.md exists** (MANDATORY):
   ```bash
   ls AGENTS.md  # Must exist in project root
   ```

2. **Check files exist**:
   ```bash
   ls .cursor/agents/*.md
   ```

3. **Test subagent invocation**:
   ```
   @research-lead Create a Task Contract for researching [your topic]
   ```

4. **Verify Cursor settings**:
   - Settings > Cursor Settings > Beta > Nightly (enabled)
   - Settings > Cursor Settings > Subagents (should show your subagents)

#### Troubleshooting

**Subagents not appearing**:
- Check Cursor version: Must be Nightly build
- Check file location: Must be in `.cursor/agents/` in workspace root
- Check file format: Each file must have valid YAML frontmatter
- Restart Cursor: After copying files, restart Cursor IDE

**Subagent not responding**:
- Check file name: Must match subagent name exactly (e.g., `research-lead.md`)
- Check YAML frontmatter: Must have `name`, `description`, `model` fields
- Check file encoding: Must be UTF-8

#### File Structure

After initialization, your workspace should have:

```
your-workspace/
├── AGENTS.md (project instructions - MANDATORY)
├── .cursor/
│   └── agents/
│       ├── research-lead.md
│       ├── collection-strategist.md
│       ├── verification-expert.md
│       ├── evidence-librarian.md
│       ├── methodologist.md
│       ├── quant-analyst.md
│       ├── domain-expert.md
│       ├── editor.md
│       ├── qa-gatekeeper.md
│       └── devils-advocate.md
└── [your project files]
```

#### Customization

After copying, you can customize subagents for your specific needs:

1. **Edit subagent files** in `.cursor/agents/`
2. **Modify descriptions** to match your workflow
3. **Add project-specific instructions** to system prompts
4. **Restart Cursor** to load changes

**Note**: Customizations are local to your workspace and won't affect the skill definition.

#### Updating Subagents

When the skill is updated:

1. **Compare versions**: Check if skill subagents have changed
2. **Backup customizations**: Save your custom changes
3. **Re-copy files**: Copy updated files from skill
4. **Re-apply customizations**: Merge your custom changes back

### Detailed Subagent Role Definitions

#### 1. research-lead (Research Lead / Owner)

**Core Responsibilities**:
- Define Task Contract: research question, boundaries, time window, deliverable format, success criteria
- Set priorities and rhythm: prioritize KIQs that most impact decisions
- Make final judgments: Key Judgments, confidence levels, risk narrative

**Mental Model**:
- **"Decision-backward"**: Ask "what will readers decide" first, then determine what to research
- **"Claim-first"**: Write research as falsifiable claims, not topic summaries
- **"Stop rules"**: Define what evidence is sufficient, when to stop

**Key Outputs**: Task Contract v1, Claim Tree v1, Key Judgments (final), Priority Matrix

**Quality Gates**: Research question is falsifiable and testable; Non-goals are explicit; KIQs ≤ 7 and actionable; Success criteria defined

**Common Pitfalls**: Unclear goals leading to scope creep; Premature convergence using intuition over evidence

---

#### 2. collection-strategist (Collection Strategist / Source Map Designer)

**Core Responsibilities**:
- Create Source Map: source type combinations for each sub-question (official/academic/industry/primary data/media/UGC)
- Design retrieval routes: keywords, language variants, exclusion terms, archiving strategy
- Control costs: prioritize "most discriminating" information

**Mental Model**:
- **"Source type complementarity"**: Each key judgment has at least 2 independent source types for cross-validation
- **"High signal first"**: Get high-credibility/auditable primary materials first, then supplement with secondary
- **"Coverage thinking"**: Focus on claims coverage, not link count

**Key Outputs**: Source Map, Collection Plan, Retrieval Route Specifications, Archiving Strategy

**Quality Gates**: Each claim has ≥2 independent source types; Cross-validation design exists; Archiving strategy defined

**Common Pitfalls**: Single-source dependency (only news/only company PR); No archiving leading to non-auditable results

---

#### 3. verification-expert (OSINT Verification Expert / Truth Tester)

**Core Responsibilities**:
- Verify UGC, event materials, images, videos: source/location/time/editing traces/reuse
- Output auditable evidence chains: coordinates, screenshot comparisons, exclusion rationale, timelines

**Mental Model**:
- **"Falsify first, then verify"**: Try to prove it's fake first (reused old images, out-of-context, fake accounts)
- **"Chain inference"**: Only advance to "auditable" degree at each step, no jumps
- **"Consistency constraints"**: Time, geography, physical details must be mutually consistent

**Key Outputs**: Verified Evidence Pool, Geolocation Reports, Chronolocation Analysis, Verification Log

**Quality Gates**: Passes "falsify first" test; Evidence chain is auditable; Consistency checks passed

**Common Pitfalls**: Only giving conclusions without chain; Treating "looks like" as evidence

---

#### 4. evidence-librarian (Evidence Librarian / Sourcing & Traceability)

**Core Responsibilities**:
- Source Register (source registry), Evidence Table (claim-evidence table)
- Citation standards: each key judgment traceable to sources (with version/timestamp/location)
- Conflict evidence management: conflict points, methods, bias risks, why chosen

**Mental Model**:
- **"Audit perspective"**: Assume someone will verify line by line, can you reproduce?
- **"Claim-evidence alignment"**: Each key sentence points to evidence; without evidence, downgrade to hypothesis
- **"Conflicts don't disappear"**: Conflicting evidence is an asset, must be explicitly presented

**Key Outputs**: Source Register, Evidence Table, Citation Index, Conflict Evidence Log

**Quality Gates**: Each key judgment has traceable citations; Evidence Table is complete; Conflicts are explicitly recorded

**Common Pitfalls**: Citations stack links but don't correspond to claims; Adding citations on last day causing full rework

---

#### 5. methodologist (Analytic Methodologist / Reasoning Engineer)

**Core Responsibilities**:
- Select and facilitate structured analysis: ACH, Key Assumptions Check, Red Team, scenario planning, indicator framework
- Make reasoning process "replayable": why this explanation is better, what are key discriminating evidence

**Mental Model**:
- **"Competing explanations"**: Default at least 2 sets of hypotheses explaining the world in parallel
- **"Maximize discrimination"**: Prioritize evidence that best distinguishes hypotheses, not most evidence
- **"Bias immunity"**: Design processes to counter confirmation bias, premature convergence, mirror imaging

**Key Outputs**: ACH Matrix, Hypothesis Analysis, Key Assumptions Check, Alternative Explanations

**Quality Gates**: At least 2 competing hypotheses exist; Discriminating evidence identified; Bias mitigation techniques applied

**Common Pitfalls**: Only writing narrative; Not doing alternative explanations; Writing logical deductions as fact statements

---

#### 6. quant-analyst (Data Analyst / Numbers & Consistency)

**Core Responsibilities**:
- Data cleaning, metric unification, comparable system building (e.g., market size, share, financial metrics)
- Sensitivity analysis/scenario analysis: how sensitive conclusions are to assumption changes
- Consistency checks: do numbers conflict, are timelines closed

**Mental Model**:
- **"Metrics before numbers"**: Unify definitions first, then discuss conclusions
- **"Range and error"**: Output intervals, confidence and error sources
- **"Explainable modeling"**: Models reveal driving factors, not "calculate a precise number"

**Key Outputs**: Consistency Report, Sensitivity Analysis, Data Cleaning Log, Metric Unification Guide

**Quality Gates**: Metrics are unified; Consistency checks passed; Sensitivity analysis complete

**Common Pitfalls**: Using precise numbers to mask uncertainty; Ignoring metric differences leading to wrong comparisons

---

#### 7. domain-expert (Domain Expert / Context & Plausibility)

**Core Responsibilities**:
- Provide "industry common sense boundaries": which conclusions cannot hold in reality (common mechanisms, regulation, business logic)
- Guide evidence priorities: which sources/indicators are more critical in this domain
- Help team identify "seemingly reasonable but mechanistically wrong" inferences

**Mental Model**:
- **"Mechanism testing"**: Not just "is there evidence", but "does it make sense mechanistically"
- **"Anomaly identification"**: When seeing signals violating industry patterns, trigger re-verification

**Key Outputs**: Mechanism Memo, Plausibility Assessment, Industry Context Guide, Anomaly Flag List

**Quality Gates**: Mechanisms are plausible; Industry patterns respected; Anomalies flagged and investigated

**Common Pitfalls**: Authority suppressing evidence (deciding by experience); Writing domain language that's unreadable

---

#### 8. editor (Editor / Storyliner / Decision Packaging)

**Core Responsibilities**:
- Package research into usable deliverables: conclusion-first, clear hierarchy, scannable, forwardable
- Control language quality: qualifiers, risk warnings, consistent uncertainty expression
- "Reader experience": readers can grasp key judgments in 3 minutes, understand basis in 10 minutes

**Mental Model**:
- **"Reader bandwidth"**: Information density designed for decision-maker's time
- **"Conclusion-reason-evidence pyramid"**: Each layer stands independently
- **"Semantic precision"**: Treat "possible/likely/almost certain" as engineering specs, not rhetoric

**Key Outputs**: Draft Report, Executive Summary, Key Judgments Section, Risk Narrative

**Quality Gates**: Conclusion-first structure; 3-minute grasp test passed; Uncertainty expressed consistently

**Common Pitfalls**: Treating process as output; Sacrificing rigor for fluency (mixing facts/judgments)

---

#### 9. qa-gatekeeper (QA / Risk & Ethics / Gatekeeper)

**Core Responsibilities**:
- Tradecraft QA: objectivity, source transparency, alternative explanations, uncertainty, logical consistency
- Compliance and ethics boundaries: privacy, permissions, gray data, misinformation risk
- Failure plans: how to downgrade delivery when evidence insufficient, how to declare gaps

**Mental Model**:
- **"Prevent disasters before adding points"**: Research's most expensive cost is wrong conclusions causing decision losses
- **"Gatekeeper not debater"**: Doesn't make conclusions for you, but ensures you're qualified to make conclusions
- **"Revocability"**: Any conclusion must allow future updates with new evidence

**Key Outputs**: QA Report, Go/No-Go Decision, Compliance Checklist, Risk Assessment

**Quality Gates**: All quality gates passed; Compliance verified; Ethics boundaries respected

**Common Pitfalls**: QA intervenes too late; Treating compliance as formal review rather than part of research method

---

#### 10. devils-advocate (Devil's Advocate / Systematic Dissenter)

**Core Responsibilities**:
- Construct counterfactual worlds: 2-4 "completely different but still self-consistent" world versions for current main conclusion
- Attack evidence chain: identify single-point failures, sensitivity points, unverifiable reasoning steps
- Trigger critical re-verification: specify "Kill Points" where if evidence is falsified, entire conclusion must restart
- Failure simulation: design 3-5 "research failure decision disaster" scenarios

**Mental Model**:
- **"Adversarial intelligence assumption"**: Assume you're seeing selectively exposed information, systematically manipulated
- **"Disconfirming evidence priority"**: A conclusion doesn't need more supporting evidence, it needs disconfirming attempts that still can't kill it
- **"Failure backward"**: Ask "three years later, where is this project most likely to fail on which assumption"
- **"Single-point failure sensitivity"**: Particularly dislikes key judgments supported by only one piece of evidence

**Key Outputs**: Counter-Hypothesis Brief, Kill-Point List, Fragility Map, Adversarial Review Memo, Decision-Failure Simulation

**Quality Gates**: At least 2 counterfactual worlds constructed; Kill points identified; Fragility map complete; Adversarial review challenges main conclusion

**Common Pitfalls**: Anyone temporarily playing opposition → becomes polite objection without attack power; Only questioning views, not evidence chain → only hits surface, not structure; Only raising doubts, not proposing alternative worlds → cannot drive re-verification

---

### Parallel Processing & Iteration Details

**Parallel Processing Opportunities**:
- **Stage 4 (Verification) + Stage 5 (Evidence Registration)**: As evidence is verified, librarian can start registering
- **Stage 6 (Structured Reasoning) + Stage 7 (Data Consistency)**: Can run in parallel, then reconcile
- **Stage 8 (Devil's Advocate) + Stage 9 (Domain Expert)**: Can run in parallel, then reconcile

**Common Iteration Loops**:
- **Stage 6 → Stage 2**: If evidence insufficient, return to collection
- **Stage 8 → Stage 6**: If Kill Points identified, may need re-analysis
- **Stage 11 → Stage 10**: If QA fails, return to editor
- **Stage 11 → Any Stage**: If major issues found, return to appropriate stage

**Handoff Protocols**: Each handoff should include output artifacts, status summary, known issues, and next steps.

**Quality Gate Escalation**: If a gate fails: Minor issue → Fix within stage; Moderate issue → Return to previous stage; Major issue → Return to Stage 0 (Task Contract) or Stage 1 (KIQ)

### Small Team Adaptation

For small teams (1-3 people), one person can wear multiple hats:

- **Solo Researcher**: research-lead + methodologist + editor
- **Two-Person Team**: 
  - Person A: research-lead + collection-strategist + evidence-librarian
  - Person B: methodologist + verification-expert + editor + qa-gatekeeper
- **Three-Person Team**: Distribute roles more evenly

**Key Principle**: Even if one person does multiple roles, **the functions should not be skipped**. The mental models and quality gates still apply.
