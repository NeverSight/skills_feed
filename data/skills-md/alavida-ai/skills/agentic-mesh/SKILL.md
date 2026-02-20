---
name: agentic-mesh
description: "Reference guide for the Agentic Mesh framework (Falconer, O'Reilly 2025). Covers agent architecture, mesh platform design, trust frameworks, operating models, and implementation roadmaps. Use when: discussing agentic mesh concepts, designing agent ecosystems, planning mesh infrastructure, referencing agent patterns (communication, role, organizational), understanding trust/security/governance for agents, building agent factories, or implementing the Agonda methodology. Triggers: agentic mesh, agent architecture, agent ecosystem, mesh platform, trust framework, agent factory, agent fleet, agentic quantum, microagent, agent registry, agent lifecycle, agent patterns, mesh governance, agent operations"
---

# Agentic Mesh

Reference skill for the Agentic Mesh book (Falconer, O'Reilly 2025). Provides the theoretical and architectural foundation for building agent ecosystems.

## Core Definitions

- **Agentic Mesh**: Interconnected ecosystem for agent discovery, collaboration, interaction, and transactions. Inherits from service mesh (APIs) and data mesh (data products).
- **Agent**: LLM-powered program that independently makes decisions, plans iteratively, and executes complex tasks. Distinguished from workflows by autonomous reasoning and nondeterministic execution.
- **Agentic Quantum**: Smallest meaningful unit = LLM (brain) + tools (limbs) + execution framework, containerized as a microagent.

## Architecture at a Glance

### Agent Anatomy (4 components)
| Component | Role |
|-----------|------|
| **Brain (LLM)** | Reasoning, planning, language — stateless, multimodal |
| **Memory** | Native / short-term / long-term / episodic / procedural / semantic |
| **Context Engineering** | Hot/warm/cold cache tiers, RAG, compression, slotting |
| **Tools** | Sensors + actuators, MCP protocol, tool chaining |

### Agent Types (4)
| Type | Behavior |
|------|----------|
| **Task-oriented** | Clear objective, execute plan, return result |
| **Goal-oriented** | Collaborative problem-solving, dynamic planning, shared workspace |
| **Simulation** | Virtual models, emergent behavior analysis |
| **Observer** | Continuous monitoring, event-driven, pub/sub |

### Mesh Platform (6 components)
Registry, Monitor, Interactions Server, Marketplace, Workbenches (Consumer/Creator/Trust/Operator), Proxy

### Agent Lifecycle
`Draft` -> `Registered` -> `Published` -> `Certified` -> `Updated` -> `Deprecated` -> `Retired`

## Key Frameworks

### Seven-Layer Trust Framework
| Layer | Domain |
|-------|--------|
| L1 | Identity & Authentication (cryptographic, mTLS) |
| L2 | Authorization & Access Control (RBAC/ABAC, OAuth2) |
| L3 | Purpose & Policies (data contracts, constraints) |
| L4 | Explainability (task plans, tool selection logic) |
| L5 | Observability & Traceability (logs, correlation, monitoring) |
| L6 | Certification & Compliance (evaluation, stress testing) |
| L7 | Governance & Lifecycle (bodies, ownership, escalation) |

### Reliability Solution
- **Problem**: Combinatorial explosion — 0.99^1000 = 0.004% accuracy
- **Solution**: Task decomposition -> task independence -> specialization -> deterministic execution

### Patterns Catalog
- **Communication (6)**: Interaction, Delegation, Conversation, Attention, Broadcast, Listener
- **Role (6)**: Planner, Orchestrator, Executor, Observer, Judge, Enforcer
- **Organizational (8)**: Singleton, Team, Organization, Swarm, Ecosystem, Legal Entity, Federation, Supply Chain
- **Messaging (7)**: Request-response, Async, Event-driven, Message queue, Streaming, Actor model, Shared workspaces

## Operating Model (5 Pillars)
Structure (people + agents) | Process (lifecycle + governance) | Technology (registry, observability) | Policy (autonomy tiers, guardrails) | Metrics (value + safety)

### Scaling Units
Agent (person) -> Fleet (team) -> Ecosystem (organization) -> Supply chain (economy)

## Implementation Roadmap (5 Workstreams)
1. Strategic foundations (vision -> MVP)
2. Technology (build -> industrialize -> secure -> model ops)
3. Agent & fleet factories (frameworks -> DevSecOps -> factories)
4. Organization (operating model -> change management -> training)
5. Governance (agent governance -> fleet governance)

## Reference Files

Detailed concept files — read the specific file when deeper context is needed:

| File | Covers | When to read |
|------|--------|-------------|
| [foundations.md](references/foundations.md) | Core definitions, mesh vision, enterprise requirements, scale predictions | Defining what agentic mesh is, why it matters |
| [agents-landscape.md](references/agents-landscape.md) | AI history, workflows vs agents, evolution stages | Comparing agents to workflows, understanding agent evolution |
| [agent-basics.md](references/agent-basics.md) | Planning, execution, tools, memory, learning, collaboration | Understanding how individual agents work |
| [agent-architecture.md](references/agent-architecture.md) | Principles, components, types, all pattern catalogs, state management | Designing agents, choosing patterns |
| [enterprise-agents.md](references/enterprise-agents.md) | Microagents, reliability, explainability, discovery, AgentOps, testing | Building production-grade agents |
| [ecosystem-ux.md](references/ecosystem-ux.md) | Fleets, mesh components, lifecycle, marketplace, workbenches | Designing the mesh platform and UX |
| [registry-interaction.md](references/registry-interaction.md) | Registry data model, conversations, interactions, events, super-contexts | Building registry and communication infrastructure |
| [security-governance.md](references/security-governance.md) | Seven-layer trust, zero-trust, prompt injection, certification | Implementing security and governance |
| [operations-factory.md](references/operations-factory.md) | Operating model, team roles, fleet structures, agent factory, SDLC | Setting up operations and agent factories |
| [practical-roadmap.md](references/practical-roadmap.md) | Five workstreams, technology stack, dependencies, scale progression | Planning implementation |

### Original Chapters

Full book source material lives in `references/chapters/`. The concept files above are curated summaries — go to chapters for verbatim detail.

| Chapter | File |
|---------|------|
| Foreword | `references/chapters/00-foreword.md` |
| Preface | `references/chapters/01-preface.md` |
| Part I intro | `references/chapters/02-part-i-defining-the-essentials.md` |
| Ch01: Understanding Agentic Mesh | `references/chapters/03-ch01-understanding-agentic-mesh.md` |
| Ch02: Agentic Past, Present & Future | `references/chapters/04-ch02-agentic-past-present-future.md` |
| Ch03: Agents vs AI Workflow | `references/chapters/05-ch03-agents-versus-ai-workflow.md` |
| Ch04: Agent Basics | `references/chapters/06-ch04-agent-basics.md` |
| Part II intro | `references/chapters/07-part-ii-defining-agent-ecosystem.md` |
| Ch05: Agent Architecture | `references/chapters/08-ch05-agent-architecture.md` |
| Ch06: Enterprise-Grade Agents | `references/chapters/09-ch06-enterprise-grade-agents.md` |
| Ch07: Agentic Mesh Ecosystem | `references/chapters/10-ch07-agentic-mesh-ecosystem.md` |
| Ch08: Agentic Mesh UX | `references/chapters/11-ch08-agentic-mesh-ux.md` |
| Ch09: Agentic Mesh Registry | `references/chapters/12-ch09-agentic-mesh-registry.md` |
| Ch10: Interaction Management | `references/chapters/13-ch10-interaction-management.md` |
| Ch11: Security Considerations | `references/chapters/14-ch11-security-considerations.md` |
| Ch12: Trust Framework & Governance | `references/chapters/15-ch12-trust-framework-governance.md` |
| Part III intro | `references/chapters/16-part-iii-building-your-agentic-mesh.md` |
| Ch13: Operating Model & Team Structure | `references/chapters/17-ch13-operating-model-team-structure.md` |
| Ch14: Agent Factory | `references/chapters/18-ch14-agent-factory.md` |
| Ch15: Practical Roadmap | `references/chapters/19-ch15-practical-roadmap.md` |
