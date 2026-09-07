---
name: analyze-agent-codebase
description: "Use when analyzing an LLM-agent repository, agent harness, single-agent runtime, multi-agent system, agent framework, or mature open-source agent project to understand or present its system design, runtime behavior, context/state handling, tools, permissions, memory, RAG, events, artifacts, observability, evals, coordination model, Mermaid architecture diagrams, or plain-language HTML architecture report."
---

# Analyze Agent Codebase

## Core Principle

Analyze how the project turns an open-ended user task into controlled, recoverable, auditable system behavior. Do not explain the repository as files. Explain the agent system as a runtime.

The final user-facing deliverable is one polished static HTML report:

`agent-codebase-analysis/agent-architecture-analysis.html`

Use any intermediate evidence files only as private scratch. Do not ask the user to read `inventory.json`, raw file maps, or temporary markdown drafts.

## Workflow

1. Resolve the project root or repository source from the user's request.
2. Run the read-only evidence finder only to locate high-signal files:

```bash
python path/to/this/skill/scripts/repo_inventory.py /path/to/repo --out agent-codebase-analysis/.analysis-work
```

3. Read `agent-codebase-analysis/.analysis-work/inventory.json` only to choose evidence files. Never summarize raw inventory statistics.
4. Load `references/agent-design-taxonomy.md` and `references/report-template.md` before writing. Use them as the analysis and final HTML structure.
5. Load `references/interview-explanation-guide.md` before writing. Use it to make explanations plain-language, interview-ready, and focused on design reasoning rather than code names.
6. Read selectively: product docs, entrypoints, harness/runtime loop, state/context, prompt assembly, model adapters, tool registry/execution, permissions/sandboxing, memory/RAG, artifacts, events/streaming, persistence/replay, observability/evals, and multi-agent coordination code if present.
7. Generate project-specific Mermaid diagrams during analysis, then embed them into the final HTML:
   - Mermaid diagrams are mandatory, not optional.
   - Include Mermaid diagram source for every major diagram, even if compiled SVG is also embedded.
   - Prefer compiling Mermaid to inline SVG with an available local Mermaid renderer such as `mmdc`.
   - If no renderer is available, embed `<div class="mermaid">...</div>` blocks and include Mermaid initialization in the HTML so the diagrams render in a browser.
   - Make every diagram zoomable with an inline modal/lightbox, expandable panel, or equivalent self-contained HTML interaction.
   - Split overly complex diagrams into smaller diagrams instead of shrinking text until it is unreadable.
   - Do not leave a separate `architecture-visuals.md` as the primary deliverable.
8. Write only the final user-facing report:
   - `agent-codebase-analysis/agent-architecture-analysis.html`

## Required Analysis Frame

### 0. System Task Boundary

Start by identifying the product contract:

- What job does the agent system perform for the user?
- What enters the system and what final artifact, answer, action, or state change leaves it?
- Who decides success or failure?
- Is it a chat assistant, coding agent, browser agent, research agent, workflow agent, platform runtime, or agent framework?
- Where is the main complexity: context, tools, safety, long-running work, collaboration, deployment, or evaluation?

### 1. Harness: How Behavior Is Constrained

Treat the harness as the core research object. Explain how it makes the agent more than "LLM plus tools".

Cover the project-specific design for:

- Entry protocol: CLI, API, UI, chat surface, IDE, queue, gateway, SDK, or webhook.
- Runtime loop: ReAct loop, graph, workflow, planner/executor, router, queue worker, or framework-managed loop.
- State machine: running, planning, tool_calling, waiting_approval, failed, cancelled, completed, or project-specific equivalents.
- Context management: what enters the prompt, what stays hidden runtime state, how history, memory, RAG, tool results, and artifacts are compressed, ranked, or excluded.
- Tool system: registration, discovery, filtering, authorization, execution, timeout, retry, observation format, and side-effect boundaries.
- Model abstraction: provider selection, tool calling, streaming, structured output, fallback, reasoning modes, and capability normalization.
- Artifact model: plans, files, code diffs, browser state, search results, traces, reports, generated assets, and who can read/write them.
- Event protocol: model deltas, tool calls, tool results, approvals, errors, progress, checkpoints, and UI stream events.
- Control plane versus execution plane: scheduling, permissions, audit, and policy versus actual model/tool/browser/sandbox execution.
- Human intervention: approval gates, manual edits, plan changes, escalation, and final acceptance.
- Persistence and replay: sessions, checkpoints, prompts, tool calls, outputs, errors, artifacts, and whether a run can be searched or audited.
- Safety boundary: filesystem, terminal, network, database, browser, third-party APIs, secrets, and sandbox policy.
- Observability and evaluation: traces, logs, cost, latency, success rate, failure taxonomy, evals, regression tests, and human takeover records.

### 2. Single-Agent: How Long Tasks Advance

If the project has one dominant agent loop, explain how it keeps a long task moving:

- How the user request becomes a goal, constraints, and plan.
- Whether planning is explicit, updated, interruptible, and resumable.
- Whether tool choice is free-form or constrained by routers, filters, policies, or gates.
- How tool failures, bad model output, context overflow, missing permissions, and partial progress are recovered.
- How short-term task state, long-term memory, project knowledge, and prior experience are separated.
- How the context budget is controlled through summarization, retrieval, trimming, or scoped artifacts.
- How the system decides the task is complete, verified, tested, or ready for human review.

### 3. Multi-Agent: Whether Coordination Is Worth It

If the project has multiple agents, analyze it as a distributed coordination system, not as "more roles".

Cover:

- Topology: supervisor-worker, router-expert, planner-executor, debate, blackboard, pipeline, swarm, or graph.
- Responsibility boundaries: each agent's input, output, permissions, tools, and completion condition.
- Shared versus isolated state: memory, context, artifacts, workspace, and conflict resolution.
- Communication protocol: natural language, structured tasks, artifacts, events, queues, or shared stores.
- Context transfer: how much the parent gives the child, and whether children return summaries, artifacts, or full traces.
- Permission model: which agents can call risky tools and who has final execution authority.
- Merge and verification: voting, adjudication, validation, deduplication, review, or tests.
- Termination: how it avoids delegation loops, waiting cycles, endless debate, and runaway cost.
- Coordination cost: token use, latency, tool amplification, error propagation, and debugging difficulty.

Only call multi-agent design useful when the task is naturally decomposable, needs specialist roles, benefits from parallel exploration, needs independent review, or has too much context for one agent. Otherwise say that a single agent plus a strong harness would be simpler.

## Project-Specific Concepts

Look for files, conventions, and domain objects that encode the project's agent identity or memory model. Explain them in plain language.

Examples:

- If both `SOUL.md` and `USER.md` exist, compare them explicitly: what information each stores, who writes them, who reads them, whether they enter prompts, how they persist, how conflicts are resolved, and why the project separates agent identity/persona from user-specific memory or preferences.
- If `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `MEMORY.md`, `PROFILE.md`, or project-specific instruction files exist, explain their role in the harness and context pipeline.
- If the project has named concepts such as sessions, threads, workspaces, skills, nodes, channels, tasks, artifacts, or memories, define them before analyzing code paths.

## RAG And Knowledge Systems

If the project includes RAG, document search, embeddings, vector search, knowledge bases, or retrieval tools, explain the mechanism as a design pipeline:

- Sources and ingestion path.
- Parsing and chunking strategy.
- Index or store construction.
- Retrieval trigger: automatic before model call, explicit tool call, router decision, or user action.
- Ranking, filtering, reranking, summarization, and context insertion.
- Citation/source handling.
- Update, invalidation, and reindexing behavior.
- Retrieval evaluation if present.

Include parameters only when they affect system behavior. Do not turn RAG analysis into per-line implementation notes.

## Final HTML Requirements

The HTML report must be self-contained, readable, and useful to a newcomer.

Required qualities:

- A sticky or clearly visible table of contents.
- If a terminology glossary exists, the table of contents must include a visible link to it, preferably `href="#terminology-glossary"`.
- An executive summary with the project thesis, agent type, main complexity, and top design lessons.
- Diagram sections placed next to the prose they explain, not dumped at the end.
- Zoomable diagrams: every Mermaid/SVG diagram must have a visible way to open it larger.
- Short "why it matters" callouts for important mechanisms.
- Evidence citations using representative files/functions/classes.
- A terminology glossary for English architecture terms and project-specific terms that may confuse newcomers.
- Plain-language glossary for project-specific concepts.
- A concise reading path with only high-leverage files.
- Unknowns and verification checks for things static reading cannot prove.
- Responsive layout that works on desktop and narrow screens.
- No raw inventory tables, byte counts, extension histograms, exhaustive file lists, per-line explanations, or implementation cloning instructions.

## Mermaid Diagram Contract

The HTML must include project-specific Mermaid framework diagrams. Do not replace them with prose.

Minimum required diagrams:

1. System boundary: user entry surfaces, harness, model providers, tools, memory/RAG, artifact store, events, persistence, and external systems.
2. Request lifecycle: user request through harness, model calls, tool/RAG/memory interaction, event/artifact updates, and final response.
3. Harness state machine: important task/run states and transitions, including error, approval, cancellation, and completion paths when present.
4. Context and memory flow: model-visible prompt context versus hidden runtime state, plus memory/RAG/artifact/tool observations.
5. Tool/action/RAG flow: tool registration, permission check, execution, observation, retry/failure, and context reinsertion.
6. Multi-agent topology or control-plane/execution-plane split when present. If absent, explicitly say why the diagram is not applicable.

Each diagram must include:

- A short title.
- A plain-language explanation of what the diagram teaches.
- The Mermaid source or compiled SVG.
- Evidence citations for the files/functions/classes that support the diagram.
- A zoom/open-larger control.

Diagram readability rules:

- Split diagrams that contain too many nodes or clusters.
- Prefer short labels inside diagrams and detailed explanation in prose.
- Keep rendered text readable; do not solve complexity by making fonts tiny.
- For dense architecture, use multiple focused diagrams: "request path", "context flow", "tool safety", and "persistence/replay" are usually more readable than one all-in-one diagram.

## Explanation Style

Explain mechanisms before citing code. Do not use class names or function names as the explanation.

Bad:

- "`AgentRunner.run` calls `ToolRegistry.execute`."

Good:

- "The runtime keeps a task record, asks the model what to do next, checks whether the next step is a tool action, sends that action through the permission layer, stores the result as an observation, and then decides whether to continue or finish. `AgentRunner.run` and `ToolRegistry.execute` are the evidence for this behavior."

For every important mechanism, answer:

- What problem does it solve?
- What goes in?
- What decision does the harness make?
- What state, context, memory, artifact, or event changes?
- What happens on failure or retry?
- Why does this design matter for reliability, safety, cost, or debugging?

Each major section must use three explanation layers:

1. Plain-language explanation for a newcomer.
2. Architecture detail covering data/state flow, decisions, failure paths, and tradeoffs.
3. Code evidence with representative files/functions/classes.

## Terminology Glossary

If the report uses English-only architecture terms, abbreviations, or project-native words, add a glossary section to the table of contents.

Choose glossary terms from four sources:

1. General agent architecture words used in the report.
2. Project-native concepts found in code or docs.
3. English-only or framework-specific phrases that would confuse newcomers.
4. Terms that frequently appear in agent architecture interviews when they are relevant to this project.

Interview-frequency terms are candidates, not a required dump. Add them only when the project actually uses the idea or when the report needs the term to explain a design tradeoff. Common candidates include: ReAct, planner-executor, agent orchestration, state management, context engineering, tool calling, function calling, tool validation, MCP, agentic RAG, GraphRAG, guardrails, human-in-the-loop, observability, evals, traces, latency, cost control, rate limits, fallback, and retry.

Explain terms briefly in the context of this project. Examples include: workspace bootstrap files, harness, runtime, context, hidden runtime state, artifact, observation, tool calling, guardrail, control plane, execution plane, checkpoint, replay, trace, handoff, RAG, vector store, and rerank.

Use restrained design: strong typography, clear spacing, readable tables, light callouts, and diagrams that fit their containers. Avoid decorative clutter.

## Resources

- `scripts/repo_inventory.py`: read-only internal evidence finder. Its output is scratch data for the agent, not a user-facing deliverable.
- `references/agent-design-taxonomy.md`: required checklist for harness, single-agent, and multi-agent analysis.
- `references/report-template.md`: required structure and HTML composition guidance.
- `references/llm-agent-patterns.md`: optional pattern cues when the runtime shape is ambiguous.
- `references/interview-explanation-guide.md`: required guide for plain-language, interview-ready explanation of agent architecture.
