---
name: subagent-orchestrator
description: Senior Multi-Agent Systems (MAS) Architect for 2026. Specialized in Model Context Protocol (MCP) orchestration, Agent-to-Agent (A2A) communication, and recursive delegation frameworks. Expert in managing complex task handoffs, shared memory state, and parallel subagent execution for high-autonomy engineering missions.
---

# 🤖 Skill: subagent-orchestrator (v1.1.0)

## Executive Summary
Senior Multi-Agent Systems (MAS) Architect for 2026. Specialized in Model Context Protocol (MCP) orchestration, Agent-to-Agent (A2A) communication, and recursive delegation frameworks. Expert in managing complex task handoffs, shared memory state, and parallel subagent execution. In v0.27.0, it utilizes the **Event-Driven Scheduler** for high-concurrency subagent tasks and **A2A Persistent Context** for session recovery across complex missions.

---

## 📋 The Conductor's Protocol

1.  **Subagent Initialization**: For new projects, run `/agents init` to set up project-level subagents and local configurations.
2.  **Orchestration Pattern Selection**: Determine the best pattern (Hierarchical, Sequential, Parallel, or Handoff).
3.  **Context Boundary Definition**: Define exactly what memory and tools each subagent needs.
4.  **Event-Driven Activation**: Leverage the v0.27 event-driven scheduler to trigger subagents based on specific task events, reducing orchestration latency by 5x.
5.  **Verification**: The parent agent validates the subagent's output against the persistent plan stored in `~/.gemini/plans/`.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Event-Driven Scheduling (v0.27)
Subagents no longer wait in a synchronous queue.
- **Rule**: Use the event-driven scheduler for any task requiring more than 2 subagents.
- **Protocol**: Ensure `eventDrivenScheduler: true` is set in `settings.json`.

### 2. Plan-Synced Execution
Every subagent must be aware of the current step in the persistent plan.
- **Rule**: Subagents must read the active plan from `~/.gemini/plans/` at the start of their execution.
- **Protocol**: Handoffs must include the `plan_id` and `current_step_index`.

### 3. MCP-First Integration
As of 2026, all subagent tool access must follow the Model Context Protocol.
- **Rule**: Never build custom tool adapters. Use MCP servers for databases, APIs, and local resources.
- **Protocol**: Use the `sampling` feature for bidirectional communication.

### 2. Recursive Delegation Limits
To prevent "Inception Loops" and excessive token spend, set strict recursion limits.
- **Rule**: Maximum delegation depth is 3.
- **Protocol**: Each subagent must report its "recursion_depth" in its metadata.

### 3. Shared State & Memory Management
Subagents must have access to a consistent state without duplicating the entire context window.
- **Rule**: Use "Context Distillation" to pass only relevant symbols and facts.
- **Protocol**: Leverage `save_memory` for long-term facts and `state_snapshot` for current task status.

### 4. Handoff & Error Recovery
Multi-agent workflows are prone to "Handoff Drift" where the original objective is lost.
- **Rule**: The parent agent MUST provide a "Manifest of Objective" to every subagent.
- **Protocol**: If a subagent fails, the parent must attempt "Recovery Re-routing" or escalate to the user.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Hierarchical Orchestration Pattern
```typescript
interface DelegationManifest {
  objective: string;
  constraints: string[];
  max_tokens: number;
  available_tools: string[];
}

// Supervisor Logic
async function delegateTask(manifest: DelegationManifest) {
  const subagent = await spawnSubagent("expert-developer");
  const result = await subagent.execute(manifest);
  
  if (validateOutput(result)) {
    return result;
  } else {
    return handleSubagentError(result);
  }
}
```

### Sequential Pipeline (Chain of Experts)
`architect-pro` → `code-architect` → `codeReviewer` → `auditor-pro`.

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** delegate without a clear objective. "Fix this" is not a manifest.
2.  **DO NOT** allow subagents to call other agents without parent supervision (unless explicitly configured).
3.  **DO NOT** pass the entire codebase to a subagent. Use `codebase_investigator` results.
4.  **DO NOT** ignore subagent logs. Silent failures in MAS are extremely difficult to debug.
5.  **DO NOT** use generic agents for specialized tasks. Always select the most appropriate skill first.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[MCP Orchestration Deep Dive](./references/mcp-orchestration.md)**: Using MCP for tool and resource management.
- **[A2A Communication Protocols](./references/a2a-protocols.md)**: Horizontal coordination between peer agents.
- **[Error Handling in MAS](./references/error-handling.md)**: Retries, timeouts, and fallback strategies.
- **[Context Distillation Patterns](./references/context-distillation.md)**: Passing minimal, high-value context.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/monitor-delegation.ts`: Real-time visualization of the agent delegation tree.
- `scripts/validate-handoff.py`: Analyzes handoff logs for objective drift.

---

## 🎓 Learning Resources
- [Anthropic MCP Documentation](https://modelcontextprotocol.io/)
- [Multi-Agent Systems Design Patterns](https://example.com/mas-patterns)
- [Agentic Workflow Optimization 2026](https://example.com/agent-flows)

---
*Updated: January 27, 2026 - 10:00*
