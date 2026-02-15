---
name: "usability-testing"
description: "Plan, run, and synthesize usability tests and produce a Usability Test Pack (test plan, tasks/script, logistics, notes template, issue log, findings + recommendations). Use for usability test, user test, prototype test, user testing, usability study, Wizard of Oz, fake door."
---

# Usability Testing

## Scope

**Covers**
- Designing task-based usability studies tied to a specific product decision
- Testing live flows, prototypes, and “faked” implementations (fake door, Wizard of Oz)
- Running moderated sessions (remote or in-person) and capturing high-quality evidence
- Turning findings into a prioritized fix list (including high-ROI microcopy/CTA improvements)

**When to use**
- “Create a usability test plan and script for <flow>.”
- “We need to test a prototype with 5–8 users next week.”
- “Validate a value proposition before building (fake door / Wizard of Oz).”
- “Help me synthesize usability findings into a prioritized backlog.”

**When NOT to use**
- You need statistically reliable estimates or causal impact (use analytics/experimentation)
- You need open-ended discovery (“what problems do users have?”) → use `conducting-user-interviews`
- You’re working with high-risk populations or sensitive topics (medical, legal, minors) without appropriate approvals/training
- You don’t have a concrete scenario/flow to evaluate (clarify the decision first)

## Inputs

**Minimum required**
- Product + target user segment (who, context of use)
- The decision this test should inform (what will change) + timeline
- What you’re testing (flow/feature) + prototype/build link (or “recommend stimulus”)
- Platform + environment (web/mobile/desktop; remote/in-person)
- Constraints: session type, number of participants, incentives, recording policy, privacy constraints

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If still unknown, proceed with explicit assumptions and list **Open questions** that would change the plan.

## Outputs (deliverables)

Produce a **Usability Test Pack** in Markdown (in-chat; or as files if requested):

1) **Context snapshot** (decision, users, what’s being tested, constraints)
2) **Test plan** (method, prototype strategy, hypotheses/risks, success criteria)
3) **Participant plan** (criteria, recruiting channels, schedule + backups)
4) **Moderator guide + task script** (neutral tasks, probes, wrap-up)
5) **Note-taking template + issue log** (severity/impact, evidence)
6) **Synthesis readout** (findings, prioritized issues, recommendations, quick wins)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded heuristics: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (8 steps)

### 1) Frame the decision and the “why now”
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Define the decision, primary unknowns, and the minimum you need to learn to make the call.
- **Outputs:** Context snapshot + research questions/hypotheses.
- **Checks:** You can answer: “What will we do differently after this test?”

### 2) Choose the right stimulus (real vs prototype vs faked)
- **Inputs:** What’s being tested; constraints.
- **Actions:** Select the cheapest valid setup: live product, clickable prototype, fake door, Wizard of Oz, or concierge flow.
- **Outputs:** Prototype strategy + what will be real vs simulated.
- **Checks:** The setup tests the core value/behavior (not pixel perfection).

### 3) Define tasks and success criteria (keep it neutral)
- **Inputs:** User goals + scenarios.
- **Actions:** Write 5–8 realistic tasks (each with a starting state), success criteria, and key observables (hesitation, errors, workarounds).
- **Outputs:** Task list (draft) + observation plan.
- **Checks:** Tasks don’t reveal UI labels (“Click the X button”); they reflect real intent.

### 4) Pick participants + recruiting plan (include buffers)
- **Inputs:** Target segment, access to users.
- **Actions:** Set inclusion/exclusion criteria; choose channels; build a schedule with backups and slack for no-shows and busy participants.
- **Outputs:** Participant plan + recruiting copy/screener (as needed).
- **Checks:** Participants match the scenario (behavior/context), not just demographics.

### 5) Build the moderator guide + instrumentation
- **Inputs:** Task list + prototype.
- **Actions:** Create the script (intro/consent, warm-up, tasks, probes, wrap-up). Assign note-taker roles; decide what to record.
- **Outputs:** Moderator guide + notes template + issue log.
- **Checks:** The guide avoids leading questions and includes “what would you do next?” probes.

### 6) Run sessions and capture evidence (optional “reality checks”)
- **Inputs:** Guide, logistics, participants.
- **Actions:** Run sessions; capture verbatims, errors, rough time-on-task, and moments of confusion. Optionally observe comparable flows “in the wild.”
- **Outputs:** Completed notes per session + populated issue log.
- **Checks:** Every issue has at least one concrete example (quote/screenshot/time/step) attached.

### 7) Synthesize into prioritized fixes (micro wins count)
- **Inputs:** Notes + issue log.
- **Actions:** Cluster issues; label severity and frequency; connect to funnel/business impact; propose fixes (including microcopy/CTA tweaks).
- **Outputs:** Synthesis readout + prioritized recommendations/backlog.
- **Checks:** Each recommendation ties to evidence and an expected impact (directional).

### 8) Share, decide, and run the quality gate
- **Inputs:** Draft pack.
- **Actions:** Produce a shareable readout, propose next steps (design iteration, follow-up test, experiment). Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score [references/RUBRIC.md](references/RUBRIC.md).
- **Outputs:** Final Usability Test Pack + Risks/Open questions/Next steps.
- **Checks:** A stakeholder can make a “ship / fix / retest” decision asynchronously.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (Prototype test):** “Create a usability test plan + moderator guide to evaluate our new onboarding flow (web) with 6 first-time users next week.”  
Expected: full Usability Test Pack with neutral tasks, recruiting criteria, session logistics, and a synthesis structure.

**Example 2 (Wizard of Oz):** “We want to test an ‘AI auto-triage’ feature before building it. Design a Wizard of Oz usability test plan and script for 5 sessions.”  
Expected: stimulus plan defining what’s simulated, tasks focused on value, and an issue log + readout.

**Boundary example:** “Run a usability test to prove the redesign will increase retention by 10%.”  
Response: explain limits of small-n usability; recommend pairing with instrumentation/experimentation for causality and use usability to diagnose friction.

