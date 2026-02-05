---
# ═══════════════════════════════════════════════════════════════════════════
# SKILL: Emerging Technologies
# Version: 2.0.0 | Updated: 2025-01
# ═══════════════════════════════════════════════════════════════════════════
name: emerging-tech
description: Emerging technologies (prompt engineering, AI agents, red teaming) and leadership roles (product manager, engineering manager, DevRel).

# ACTIVATION TRIGGERS
triggers:
  - prompt engineering
  - ai-agents
  - leadership
  - pm
  - product manager
  - engineering manager
  - devrel
  - llm
  - red teaming

# SKILL PARAMETERS
parameters:
  focus:
    type: string
    enum: [emerging-tech, leadership]
    required: true
  specific_area:
    type: string
    required: false

# OUTPUT SPECIFICATION
outputs:
  learning_path:
    type: array
  skills_required:
    type: array
  timeline:
    type: string

# RELIABILITY
retry:
  max_attempts: 3
  backoff: exponential

# OBSERVABILITY
observability:
  log_level: info

level: advanced
prerequisites:
  - industry-experience

sasmp_version: "1.3.0"
bonded_agent: 01-core-paths
bond_type: PRIMARY_BOND
---

# Emerging Technologies Skill

## Quick Reference

| Technology | Timeline | Demand | Entry Point |
|-----------|----------|--------|-------------|
| **Prompt Engineering** | 2-4 wk | Very High | Any developer |
| **AI Agents** | 4-6 wk | Very High | Python developer |
| **AI Red Teaming** | 6-8 wk | High | Security background |
| **Product Management** | 3-6 mo | High | Any engineer |
| **Engineering Management** | 3-6 mo | High | Senior engineer |

---

## Emerging Tech Paths

### Prompt Engineering
```
[1] Basic Prompting (3-5 days)
 │  └─ Clear instructions, context
 │
 ▼
[2] Few-shot Learning (3-5 days)
 │  └─ Examples, patterns
 │
 ▼
[3] Chain-of-Thought (3-5 days)
 │  └─ Step-by-step reasoning
 │
 ▼
[4] Structured Output (3-5 days)
 │  └─ JSON, schemas, validation
 │
 ▼
[5] Optimization (ongoing)
    └─ Evaluation, iteration
```

**Key Techniques:**
| Technique | Description | Use When |
|-----------|-------------|----------|
| Zero-shot | Direct instruction | Simple tasks |
| Few-shot | Examples provided | Pattern matching |
| CoT | Step-by-step | Complex reasoning |
| Role-based | Persona assignment | Expert behavior |
| Structured | Format constraints | Integration |

---

### AI Agents (2025 Hot Skill)
```
[1] LLM Fundamentals (1 wk)
 │  └─ Tokens, embeddings, context
 │
 ▼
[2] Tool Calling (1 wk)
 │  └─ Function definitions, execution
 │
 ▼
[3] Agent Architecture (2 wk)
 │  └─ Perceive-Reason-Act loop
 │
 ▼
[4] Error Handling (1 wk)
 │  └─ Retries, fallbacks, guardrails
 │
 ▼
[5] Production Deploy (ongoing)
    └─ Monitoring, evaluation
```

**Agent Architecture:**
```
┌─────────────────────────────────────────┐
│            AGENTIC LOOP                  │
├─────────────────────────────────────────┤
│  1. PERCEIVE: Observe, gather context   │
│         │                                │
│         ▼                                │
│  2. REASON: LLM decides next action     │
│         │                                │
│         ▼                                │
│  3. ACT: Execute tools/APIs             │
│         │                                │
│         ▼                                │
│  4. REFLECT: Evaluate, update strategy  │
│         │                                │
│         └─► Loop until goal or max      │
└─────────────────────────────────────────┘
```

**Design Patterns (Anthropic 2025):**
| Pattern | Description | Best For |
|---------|-------------|----------|
| Prompt Chaining | Sequential fixed steps | Predictable workflows |
| Routing | Classify and dispatch | Multi-domain tasks |
| Parallelization | Concurrent subtasks | Speed optimization |
| Orchestrator-Workers | Central delegation | Complex decomposition |
| Evaluator-Optimizer | Generate + critique | Quality-critical |

---

### AI Red Teaming
```
[1] LLM Security Basics (1-2 wk)
 │  └─ Attack surfaces, vulnerabilities
 │
 ▼
[2] Adversarial Prompting (2 wk)
 │  └─ Jailbreaks, prompt injection
 │
 ▼
[3] Bias Testing (2 wk)
 │  └─ Demographic probes, fairness
 │
 ▼
[4] Safety Evaluation (2 wk)
    └─ Guardrails, alignment testing
```

**Techniques:**
| Category | Method | Goal |
|----------|--------|------|
| Jailbreaking | Bypass safety | Test guardrails |
| Prompt Injection | Hidden instructions | Test input handling |
| Bias Testing | Demographic probes | Find unfair outputs |
| Adversarial | Edge cases | Find failure modes |

---

## Leadership Paths

### Product Management
**Timeline:** 3-6 months transition

**Core Responsibilities:**
1. Vision & Strategy
2. User Research
3. Feature Prioritization
4. Roadmapping
5. Success Metrics

**Key Skills:**
| Skill | Why Important |
|-------|---------------|
| Communication | Align stakeholders |
| Data Analysis | Evidence-based decisions |
| User Empathy | Build right features |
| Prioritization | Focus on impact |
| Technical Literacy | Credibility with eng |

**Frameworks:**
- Prioritization: RICE, MoSCoW, Kano
- Discovery: Jobs-to-be-Done, Design Sprints
- Metrics: AARRR, North Star

---

### Engineering Management
**Timeline:** 3-6 months transition

**Responsibilities:**
1. Hire & develop engineers
2. 1:1s and feedback
3. Remove blockers
4. Set goals and vision
5. Team culture and health

**Key Skills:**
| Skill | Why Important |
|-------|---------------|
| Delegation | Scale yourself |
| Feedback | Grow your team |
| Strategic Thinking | Long-term planning |
| Emotional Intelligence | Handle people issues |
| Technical Literacy | Maintain credibility |

**Common Challenges:**
- Letting go of coding
- Difficult conversations
- Managing former peers
- Up vs down management

---

### Developer Relations
**Timeline:** 2-3 months transition

**Responsibilities:**
1. Community engagement
2. Content creation
3. Developer advocacy
4. Feedback gathering
5. Trust building

**Content Types:**
| Type | Platform | Effort |
|------|----------|--------|
| Blog posts | Dev.to | Medium |
| Tutorials | Docs | Medium |
| Videos | YouTube | High |
| Talks | Conferences | High |
| Examples | GitHub | Low |

---

## Career Transitions

| From | To | Difficulty | Key Bridge |
|------|----|-----------:|------------|
| Dev → PM | Medium | Product sense + communication |
| Dev → EM | Medium | Leadership + people skills |
| Dev → DevRel | Low | Communication + community |
| Dev → Architect | Medium | System design + strategy |

### Leadership Ladder
```
Individual Contributor (0-2 yr)
         │
         ▼
Lead / Senior (2-5 yr)
         │
         ▼
Manager (5+ yr)
         │
    ┌────┴────┐
    ▼         ▼
IC Track   Management Track
(Staff,    (Director,
Principal) VP, CTO)
```

---

## Troubleshooting

```
Want to transition to PM?
├─► Build product sense: analyze products you use
├─► Get experience: side projects, internal transfers
├─► Learn frameworks: RICE, user research
└─► Network: talk to PMs, understand their day

Want to become a manager?
├─► Start mentoring: lead projects, help juniors
├─► Build soft skills: communication, feedback
├─► Understand: you're not coding anymore
└─► Talk to: your manager about the path

AI agent not working?
├─► Tool definitions clear? → Improve docs
├─► Context window full? → Summarize
├─► Looping forever? → Add max iterations
└─► Wrong tools called? → Improve routing
```

---

## Common Failure Modes

| Symptom | Root Cause | Recovery |
|---------|------------|----------|
| PM rejected by eng | Too many requirements | Fewer, clearer asks |
| Team not performing | Micromanaging | Delegate more |
| Agent loops forever | No exit condition | Max iterations |
| Community not engaging | Wrong content | Ask what they need |

---

## Next Actions

Specify your interest area (emerging tech or leadership) for detailed guidance.
