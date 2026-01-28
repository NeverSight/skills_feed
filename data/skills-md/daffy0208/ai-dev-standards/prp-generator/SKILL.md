---
name: PRP Generator
description: Guides creation of Product Requirements Prompts (PRPs) - comprehensive requirement documents that serve as the foundation for AI-assisted development
version: 1.0.0
category: requirements
triggers:
  - 'prp-generator'
  - 'prp generator'
  - 'product requirements prompt'
  - 'create prp'
  - 'generate requirements'
dependencies:
  required_mcps: []
  required_tools: []
  required_integrations: []
---

# PRP Generator (Product Requirements Prompt)

## Overview

The PRP Generator helps you create comprehensive Product Requirements Prompts - structured documents that capture everything needed to build a product feature or system. PRPs are optimized for AI-assisted development, providing clear requirements that both humans and AI can understand.

**Core Purpose:** Transform vague ideas into actionable, complete requirements.

## When to Use This Skill

Use PRP Generator when:

- Starting a new product or major feature
- Requirements are unclear or scattered
- Need to communicate requirements to development team
- Using AI assistants for implementation
- Transitioning from discovery to development
- Onboarding new team members to a project

## Key Capabilities

- Structure requirements into 12 standardized sections
- Identify project complexity pattern (A, B, C)
- Extract user stories in Jobs-to-be-Done format
- Define success criteria and metrics
- Document functional and non-functional requirements
- Capture constraints, risks, and assumptions
- Clarify what's in and out of scope

## Workflow

### The 12-Section PRP Structure

A complete PRP contains these 12 sections:

1. **Project Overview**
2. **Problem Statement**
3. **Success Criteria**
4. **User Stories (Jobs-to-be-Done)**
5. **Functional Requirements**
6. **Non-Functional Requirements**
7. **Technical Constraints**
8. **Data Requirements**
9. **UI/UX Requirements**
10. **Risks & Assumptions**
11. **Out of Scope**
12. **Open Questions**

Let's dive into each:

---

### 1. Project Overview

**Purpose:** High-level context and pattern classification

**What to Include:**

- Project name and one-sentence description
- Pattern classification (A, B, or C)
- Timeline estimate
- Target users
- Business context

**Example:**

```
Project: Customer Support Chatbot
Pattern: C (AI-Native System)
Timeline: 10-12 weeks
Users: Customer support agents + end customers
Context: Reduce support ticket volume by 40% while maintaining customer satisfaction
```

---

### 2. Problem Statement

**Purpose:** Clearly define the problem being solved

**Template:**

```
[User type] faces [problem] when [situation].
This causes [negative outcome].
We know this because [evidence].
```

**Example:**

```
Customer support agents face long response times when customers ask common questions about billing, account setup, and feature usage. This causes customer frustration and agent burnout handling repetitive inquiries.

We know this because:
- 60% of tickets are "How do I..." questions
- Average response time is 4 hours
- Agent surveys show 70% of time spent on repetitive questions
- NPS dropped from 45 to 38 in past 6 months
```

---

### 3. Success Criteria

**Purpose:** Define measurable outcomes

**Structure:**

- Primary metric (North Star)
- Secondary metrics
- Minimum success thresholds

**Example:**

```
Primary Metric:
- Reduce support ticket volume by 40% within 3 months of launch

Secondary Metrics:
- 80% of common questions answered by AI without escalation
- <2 second response time for AI answers
- >4.0/5.0 user satisfaction rating with AI responses
- 50% reduction in agent time spent on common questions

Minimum Success:
- 30% ticket reduction + 4.0/5.0 satisfaction
```

---

### 4. User Stories (Jobs-to-be-Done)

**Purpose:** Capture user needs in job-to-be-done format

**Template:**

```
When [situation], I want to [action], so I can [outcome].
```

**Example:**

```
Customer Stories:
1. When I have a billing question, I want instant answers, so I can resolve issues without waiting.
2. When I'm setting up my account, I want step-by-step guidance, so I don't get stuck.
3. When I need to reset my password, I want a simple self-service flow, so I don't need to contact support.

Agent Stories:
1. When a complex issue arrives, I want context from the AI conversation, so I can help efficiently.
2. When training new agents, I want the AI to handle basics, so I can focus on teaching advanced topics.
3. When customers escalate, I want conversation history, so I don't ask redundant questions.
```

---

### 5. Functional Requirements

**Purpose:** What the system must do

**Categories:**

- Core features (P0 - must have)
- Important features (P1 - should have)
- Nice-to-have (P2 - could have)

**Example:**

```
P0 (Core - MVP):
- FR-001: System answers common questions from knowledge base
- FR-002: System escalates to human when confidence is low (<70%)
- FR-003: Agents can see full conversation history
- FR-004: System tracks conversation satisfaction ratings

P1 (Important - Post-MVP):
- FR-005: System learns from agent corrections
- FR-006: System handles multi-turn conversations with context
- FR-007: Agents can override AI suggestions

P2 (Nice-to-have - Future):
- FR-008: System proactively suggests help articles
- FR-009: System detects frustrated customers
- FR-010: Multi-language support
```

---

### 6. Non-Functional Requirements

**Purpose:** How the system should perform

**Categories:**

- Performance
- Security
- Scalability
- Reliability
- Usability

**Example:**

```
Performance:
- NFR-001: Response time <2 seconds for 95th percentile
- NFR-002: Handle 100 concurrent conversations
- NFR-003: Knowledge base search <500ms

Security:
- NFR-004: Customer data encrypted at rest and in transit
- NFR-005: SOC2 Type II compliance
- NFR-006: Role-based access control (RBAC)
- NFR-007: Audit logs for all AI responses

Scalability:
- NFR-008: Support 10,000 conversations/day at launch
- NFR-009: Scale to 100,000 conversations/day within 6 months

Reliability:
- NFR-010: 99.9% uptime SLA
- NFR-011: Graceful degradation if AI service unavailable

Usability:
- NFR-012: Agents can use with <10 minutes training
- NFR-013: WCAG 2.1 AA accessibility compliance
```

---

### 7. Technical Constraints

**Purpose:** Technology limitations and requirements

**What to Include:**

- Existing systems to integrate with
- Technology stack requirements
- Infrastructure constraints
- Budget limitations
- Timeline constraints

**Example:**

```
Integrations:
- Must integrate with existing Zendesk system
- Must use company SSO (Okta)
- Must log to existing Datadog monitoring

Technology Stack:
- Backend: Python (existing team expertise)
- LLM: OpenAI GPT-4 (approved vendor)
- Vector DB: Pinecone or Weaviate (to be decided)
- Frontend: React (existing stack)

Infrastructure:
- Deploy on existing AWS infrastructure
- Use existing CI/CD pipelines (GitHub Actions)

Budget:
- OpenAI API budget: $5,000/month maximum
- Infrastructure: $2,000/month maximum

Timeline:
- MVP must launch within 10 weeks
- Full feature set within 16 weeks
```

---

### 8. Data Requirements

**Purpose:** What data is needed and how it's managed

**Structure:**

- Data sources
- Data models
- Data privacy
- Data retention

**Example:**

```
Data Sources:
- Knowledge base articles (500+ articles in Notion)
- Historical support tickets (Zendesk, 2 years)
- Product documentation (GitHub docs)
- FAQ pages (company website)

Data Models:
- Conversations: id, customer_id, agent_id, messages[], status, satisfaction_rating
- Messages: id, sender, text, timestamp, ai_confidence
- Knowledge: id, title, content, embeddings, category, last_updated

Data Privacy:
- PII must be redacted before AI processing
- Conversation data retained for 90 days
- Analytics data aggregated and anonymized
- GDPR right-to-delete compliance

Data Security:
- Encrypt customer data at rest (AES-256)
- Encrypt in transit (TLS 1.3)
- Role-based access to conversation data
```

---

### 9. UI/UX Requirements

**Purpose:** How users interact with the system

**What to Include:**

- User flows
- Interface requirements
- Design constraints
- Accessibility needs

**Example:**

```
Customer Interface:
- Chat widget in bottom-right corner
- Typing indicators and response time estimates
- Clear "Talk to a human" button always visible
- Conversation history accessible for 30 days

Agent Interface:
- Side panel showing AI suggestions
- One-click "Accept AI answer" button
- Edit AI answer before sending
- Flag incorrect responses for retraining
- Dashboard showing AI performance metrics

User Flows:
1. Customer asks question → AI retrieves answer → Displays with confidence
2. Low confidence → Auto-escalate to agent → Agent sees full context
3. Agent corrects AI → System logs for improvement

Design Constraints:
- Match existing brand colors
- Mobile-responsive design
- WCAG 2.1 AA compliant
- Support keyboard navigation
```

---

### 10. Risks & Assumptions

**Purpose:** Identify potential blockers and dependencies

**Structure:**

- Risks with mitigation plans
- Assumptions to validate
- Dependencies on external factors

**Example:**

```
Risks:
1. AI hallucination risk
   - Mitigation: Confidence thresholds, human review for low confidence

2. Knowledge base quality risk
   - Mitigation: Content audit before launch, SME review of top 100 articles

3. User adoption risk (agents don't trust AI)
   - Mitigation: Gradual rollout, agent training, show accuracy metrics

4. API cost overruns
   - Mitigation: Aggressive caching, token limits, usage monitoring

Assumptions:
1. Customers will accept AI responses (validate with beta test)
2. Knowledge base is accurate and up-to-date (audit required)
3. 80% of questions can be answered with existing knowledge
4. OpenAI API latency is acceptable (<2s)

Dependencies:
1. Access to Zendesk API (need approval from IT)
2. Knowledge base export from Notion
3. OpenAI API quota increase (currently limited)
4. Agent availability for training and feedback
```

---

### 11. Out of Scope

**Purpose:** Explicitly state what WON'T be built

**Why Important:** Prevents scope creep and sets expectations

**Example:**

```
Out of Scope for MVP:
- Voice/phone support integration (post-MVP)
- Multi-language support (Phase 2)
- Integration with CRM system (future)
- Custom AI model training (using OpenAI)
- Mobile app (web only initially)
- Proactive outreach (reactive support only)
- Sentiment analysis dashboard (future analytics)
- Agent performance scoring (v2 feature)

Explicitly NOT Building:
- Custom LLM training (too expensive)
- Real-time translation (complexity vs. value)
- Video call integration (different project)
```

---

### 12. Open Questions

**Purpose:** Document unknowns that need answers

**Structure:**

- Question
- Who can answer
- When answer needed by
- Impact if not answered

**Example:**

```
Open Questions:

Q1: What's acceptable AI error rate for customers?
- Who: Product Manager + Customer Success lead
- Deadline: Week 2 (before architecture finalized)
- Impact: Determines confidence thresholds and escalation flow

Q2: Can we access historical conversation sentiment data?
- Who: Data team
- Deadline: Week 3 (before training data collection)
- Impact: Improves AI tone matching

Q3: What's our Zendesk API rate limit?
- Who: IT/Infrastructure
- Deadline: Week 1 (critical for architecture)
- Impact: May need caching strategy

Q4: Do we have budget for Pinecone or need open-source vector DB?
- Who: Engineering Manager
- Deadline: Week 2 (affects tech stack)
- Impact: Pinecone is easier, open-source is cheaper but more work

Q5: Are agents allowed to edit AI-generated responses?
- Who: Legal/Compliance
- Deadline: Week 4 (before feature development)
- Impact: Affects agent interface design
```

---

## Examples

### Example 1: Simple Feature (Pattern A)

**Project:** Add CSV export to user dashboard

```markdown
# PRP: CSV Export Feature

## 1. Project Overview

Pattern A (Simple Feature)
Timeline: 2-3 days
Add CSV export button to user dashboard

## 2. Problem Statement

Users need to export data for offline analysis. Currently they must manually copy-paste.

## 3. Success Criteria

- 80% of users who click export get successful download
- <5s export time for typical dataset (1000 rows)

## 4. User Stories

When viewing my data, I want to click "Export CSV", so I can analyze it in Excel.

## 5. Functional Requirements

FR-001: Export button in dashboard toolbar
FR-002: Exports all visible columns
FR-003: Respects current filters
FR-004: Filename includes timestamp

## 6-12. [Abbreviated for Pattern A]
```

---

### Example 2: New Product (Pattern B)

_See customer support chatbot example throughout sections above_

---

### Example 3: AI-Native System (Pattern C)

**Project:** Multi-Agent Research Assistant

```markdown
# PRP: Multi-Agent Research Assistant

## 1. Project Overview

Pattern C (AI-Native System)
Timeline: 14-16 weeks
Multi-agent system with specialized agents for research, synthesis, and fact-checking

## 2. Problem Statement

Researchers spend 60% of their time finding and synthesizing papers instead of analysis. Current tools return overwhelming results without quality filtering.

## 3. Success Criteria

Primary: Reduce research time from 8 hours to 2 hours per topic
Secondary:

- 90% accuracy in paper relevance
- 85% user satisfaction
- <30s for initial results
- 5+ papers synthesized per query

## 4. User Stories

- When I enter a research topic, I want a synthesized summary with sources, so I can quickly understand the landscape
- When results are vague, I want follow-up questions suggested, so I can refine my search
- When I find a relevant paper, I want related papers suggested, so I can explore deeper

## 5. Functional Requirements (AI-specific)

FR-001: Search agent queries multiple academic databases
FR-002: Filter agent scores paper relevance (0-100)
FR-003: Synthesis agent creates 500-word summary
FR-004: Fact-check agent validates key claims
FR-005: Orchestrator coordinates agents and resolves conflicts

## 6. Non-Functional Requirements (AI-specific)

NFR-001: Agent coordination latency <5s
NFR-002: RAG retrieval accuracy >90%
NFR-003: Handle 50 concurrent research sessions
NFR-004: LLM token budget: $10/research session maximum

## 7. Technical Constraints (AI-specific)

- LLM: GPT-4 for synthesis, GPT-3.5 for filtering
- Vector DB: Pinecone (1M vectors)
- Agent framework: LangChain or CrewAI
- Academic APIs: Semantic Scholar, arXiv

## 8. Data Requirements (AI-specific)

- Paper embeddings: title + abstract + keywords
- Citation network graph for related papers
- User research history for personalization
- Fact-check database with verified claims

## 9-12. [Complete as per structure]
```

---

## Best Practices

### 1. Start with Problem, Not Solution

Write problem statement before functional requirements. Understand "why" before "what".

### 2. Make Success Criteria Measurable

Bad: "Improve user experience"
Good: "Increase task completion rate from 60% to 85%"

### 3. Use Jobs-to-be-Done Format

Captures user intent, not just feature requests.

### 4. Be Explicit About Out of Scope

Prevents future arguments about "I thought we were building X".

### 5. Document All Open Questions

Don't hide unknowns. Make them visible and track resolution.

### 6. Update PRP as You Learn

PRPs evolve. Update when you discover new information.

### 7. Review with Stakeholders

Validate PRP with:

- Product Manager (business requirements)
- Engineering Lead (technical feasibility)
- Designer (UX requirements)
- Security (compliance requirements)

---

## Common Pitfalls

### 1. Writing Solutions Instead of Requirements

**Antipattern:** "Use React with Redux for state management"
**Better:** "System must handle real-time updates across multiple views"

### 2. Vague Success Criteria

**Antipattern:** "Users should be happy"
**Better:** "NPS score >50, task completion rate >80%"

### 3. Missing Non-Functional Requirements

**Antipattern:** Only listing features
**Better:** Include performance, security, scalability

### 4. Assuming Knowledge

**Antipattern:** "Obviously we need authentication"
**Better:** Explicitly state all requirements

### 5. Mixing Pattern Complexity

**Antipattern:** Pattern A with Pattern C orchestration
**Better:** Match PRP depth to pattern complexity

---

## Related Skills

- **framework-orchestrator** - Uses PRP to determine pattern and sequence
- **product-strategist** - Validates problem before PRP creation
- **user-researcher** - Provides user insights for PRP
- **bmad-method** - Business model informs technical requirements
- **security-architect** - Security requirements section
- **api-designer** - Technical constraints section

---

## Deliverables

A complete PRP document containing:

1. All 12 sections filled out
2. Pattern classification (A, B, or C)
3. Reviewed by key stakeholders
4. Open questions tracked with owners and deadlines
5. Version controlled (update as you learn)

---

## Success Metrics

You've created a good PRP when:

- Developers can build from it without constant clarification
- Stakeholders agree on scope and success criteria
- Risks and assumptions are surfaced early
- Out of scope is crystal clear
- Open questions have owners and deadlines
- Pattern complexity matches project reality

---

**Remember:** A good PRP is the difference between organized development and chaotic scope creep. Invest time upfront to save weeks later.
