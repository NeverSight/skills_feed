---
name: orchestrator
description: Meta-skill orchestrating 7 atomic skills into unified workflows for intelligent development
version: 1.0.0
triggers:
  - multi-skill coordination
  - composite workflow
  - cross-tool integration
  - intelligent task routing
  - unified code discovery
  - AI module development
  - agent orchestration
dependencies:
  - bd@0.28.0
  - bv@0.1.0
  - mcp_agent_mail@0.1.0
  - osgrep@0.4.15
  - leann@0.14.0
  - dspy-code@2.6.0
  - agents-md@1.0.0
author: architect
integration: claude-code
---

# Orchestrator - Meta-Skill for Unified Development

## Overview

The **Orchestrator** is a meta-skill that integrates 7 atomic skills into coherent composite workflows. It addresses the critical integration gaps identified through red-team validation and provides a unified framework for intelligent development.

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ORCHESTRATOR                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                     Composite Workflows                            │    │
│   ├───────────────────┬────────────────────┬──────────────────────────┤    │
│   │ Task Intelligence │  Code Discovery    │   AI Development         │    │
│   │   (bd→bv→mail)    │ (osgrep↔leann)     │  (dspy+all)              │    │
│   └───────────────────┴────────────────────┴──────────────────────────┘    │
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                     Integration Layer                              │    │
│   ├─────────────────┬─────────────────┬───────────────────────────────┤    │
│   │  Shared Types   │   Event Bridge  │      State Manager            │    │
│   │ (UnifiedTask,   │  (EventBus,     │   (caches, workflows,         │    │
│   │  UnifiedAgent,  │   EventRouter,  │    metrics, snapshots)        │    │
│   │  SearchResult)  │   Adapters)     │                               │    │
│   └─────────────────┴─────────────────┴───────────────────────────────┘    │
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                      Atomic Skills                                 │    │
│   ├────────┬────────┬────────────────┬─────────┬────────┬─────────────┤    │
│   │   bd   │   bv   │ mcp_agent_mail │ osgrep  │ leann  │  dspy-code  │    │
│   │(tasks) │(graph) │   (comms)      │(search) │ (RAG)  │   (AI)      │    │
│   └────────┴────────┴────────────────┴─────────┴────────┴─────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## When to Use This Skill

### Activate Orchestrator when:

1. **Multi-skill coordination needed**
   - Task requires 2+ atomic skills
   - Cross-skill data flow required
   - Need unified result format

2. **Composite workflows**
   - Sprint planning with intelligent assignment
   - Code exploration with task linking
   - AI module development with integration

3. **Integration scenarios**
   - bd tasks need bv metrics
   - osgrep results should update leann index
   - mcp_agent_mail reservations should link to bd tasks

4. **Event-driven automation**
   - React to task state changes
   - Propagate search results
   - Coordinate agent activities

### DO NOT use Orchestrator when:

- Single skill suffices (use atomic skill directly)
- Simple queries without cross-skill needs
- Performance-critical single operations

## Core Components

### 1. Shared Types (`types/shared.ts`)

Unified type definitions bridging all skills:

```typescript
// Bridges bd.assignee (string) and mcp_agent_mail.Agent (object)
interface UnifiedAgent {
  id: string;
  capabilities?: string[];
  status?: AgentStatus;
  bdAssigneeFormat: string;  // "@claude" format
  mcpAgentId: string;        // Full agent ID
}

// Bridges bd.Issue + bv metrics + mcp_agent_mail context
interface UnifiedTask {
  id: string;
  title: string;
  state: TaskState;
  assignee?: UnifiedAgent;
  metrics?: TaskGraphMetrics;  // FROM bv
  threadId?: string;           // FROM mcp_agent_mail
  reservations?: FileReservation[];
}

// Bridges osgrep.SearchResult and leann.ScoredItem
interface UnifiedSearchResult {
  path: string;
  score: number;
  scoreBreakdown?: {
    semantic: number;   // osgrep vector
    lexical: number;    // BM25
    rag: number;        // leann
    fusion: number;     // RRF
  };
  source: 'osgrep' | 'leann' | 'hybrid';
}
```

### 2. Event Bridge (`events/bridge.ts`)

Cross-skill event propagation:

```typescript
// Event types spanning all skills
type EventType =
  | 'task.created' | 'task.assigned' | 'task.completed'  // bd
  | 'metrics.calculated' | 'critical_path.changed'       // bv
  | 'message.sent' | 'reservation.created'               // mcp_agent_mail
  | 'search.completed' | 'index.updated'                 // osgrep/leann
  | 'module.compiled' | 'optimization.completed'         // dspy-code
  | 'workflow.started' | 'workflow.completed';           // orchestrator

// Default routes (auto-configured)
// bd → bv: Task changes trigger metric recalculation
// bd → mcp_agent_mail: Assignments trigger notifications
// bv → bd: Critical path changes update priorities
// osgrep → leann: Search results can update index
```

### 3. State Manager (`state/manager.ts`)

Centralized state with caching:

```typescript
interface OrchestratorState {
  workflows: Map<string, WorkflowExecutionState>;
  taskCache: Map<string, UnifiedTask>;
  searchCache: Map<string, UnifiedSearchResult[]>;
  agentCache: Map<string, UnifiedAgent>;
  eventLog: OrchestratorEvent[];
  metrics: OrchestratorMetrics;
}
```

### 4. Workflow Engine (`workflows/engine.ts`)

Composite workflow execution:

```typescript
const result = await workflowEngine.execute(
  taskIntelligencePipeline,
  {
    taskTitle: 'Implement auth',
    taskPriority: 'high',
    dependencies: [],
  }
);
// Executes: bd.create → bv.analyze → bv.recommend → mcp_agent_mail.send → bd.assign
```

## Composite Workflows

### 1. Task Intelligence Pipeline

**Skills**: bd → bv → mcp_agent_mail

Creates tasks, analyzes dependencies, routes to optimal agents.

```bash
# Trigger: New task with dependencies
# Flow:
# 1. bd: Create task with dependencies
# 2. bv: Calculate PageRank, critical path, blocker score
# 3. bv: Recommend optimal agent based on metrics
# 4. mcp_agent_mail: Notify agent, create file reservations
# 5. bd: Update task with assignment and metrics
```

**Use cases**:
- Sprint planning automation
- Bottleneck detection and response
- Critical path optimization

### 2. Code Discovery Pipeline

**Skills**: osgrep ↔ leann

Unified semantic search with hybrid ranking.

```bash
# Trigger: Conceptual code search
# Flow:
# 1. leann: Check RAG cache
# 2. [parallel] osgrep: Semantic search | leann: RAG search
# 3. orchestrator: RRF fusion of results
# 4. leann: Update cache
# 5. osgrep: Warm index for found paths
```

**Use cases**:
- Conceptual code exploration
- Architecture understanding
- Cross-project pattern finding

### 3. AI Development Pipeline

**Skills**: dspy-code + all

End-to-end DSPy module development.

```bash
# Trigger: AI module development task
# Flow:
# 1. bd: Create AI task
# 2. [parallel] osgrep: Find similar modules | leann: Find training patterns
# 3. dspy-code: Define signature, select predictor
# 4. dspy-code: Implement and optimize module
# 5. bd: Update task with metrics
# 6. mcp_agent_mail: Notify stakeholders
# 7. leann: Index new module
```

**Use cases**:
- QA module development
- Code review automation
- GEPA prompt optimization

## Quick Start

### 1. Initialize Orchestrator

```typescript
import { eventBus, eventRouter, stateManager, workflowEngine } from './orchestrator';

// Event routing is auto-configured
// State manager starts with empty caches
// Workflow engine ready to execute
```

### 2. Execute Composite Workflow

```typescript
import { taskIntelligencePipeline } from './workflows/task-intelligence';

const result = await workflowEngine.execute(
  taskIntelligencePipeline,
  {
    taskTitle: 'Implement user authentication',
    taskDescription: 'Add JWT-based auth with refresh tokens',
    taskPriority: 'high',
    dependencies: ['setup-database'],
    agentPool: ['@claude', '@backend-team'],
  }
);

if (result.ok) {
  console.log('Task created:', result.value.createdTaskId);
  console.log('Assigned to:', result.value.optimalAgent);
  console.log('Metrics:', result.value.taskMetrics);
}
```

### 3. Subscribe to Events

```typescript
// React to task assignments
eventBus.subscribe('task.assigned', async (event) => {
  const { task, agent } = event.payload;
  console.log(`${task.title} assigned to ${agent.id}`);

  // Find related code
  const code = await codeDiscoveryPipeline.execute({
    searchQuery: task.description,
  });

  // Link files to task
  await bd.update(task.id, { files: code.value.unifiedResults.map(r => r.path) });
});

// React to critical path changes
eventBus.subscribe('critical_path.changed', async (event) => {
  const { paths } = event.payload;
  console.log('Critical path updated:', paths);

  // Re-prioritize tasks on critical path
  for (const taskId of paths) {
    await bd.update(taskId, { priority: 'critical' });
  }
});
```

### 4. Use Unified Types

```typescript
import { toUnifiedAgent, fromOsgrepResult, fromLeannResult } from './types/shared';

// Convert bd assignee to unified agent
const agent = toUnifiedAgent('@claude');
// { id: 'claude', bdAssigneeFormat: '@claude', mcpAgentId: 'claude' }

// Convert osgrep result to unified format
const osgrepResult = { path: 'auth.ts', score: 0.89, snippet: '...' };
const unified = fromOsgrepResult(osgrepResult);
// { path: 'auth.ts', score: 0.89, source: 'osgrep', scoreBreakdown: {...} }
```

## Integration Patterns

### Pattern 1: Task-Driven Code Discovery

```typescript
// When task is created, find related code
eventBus.subscribe('task.created', async (event) => {
  const task = event.payload as UnifiedTask;

  const code = await workflowEngine.execute(codeDiscoveryPipeline, {
    searchQuery: `${task.title} ${task.description}`,
    maxResults: 10,
  });

  const relatedFiles = code.value.unifiedResults
    .filter(r => r.score > 0.6)
    .map(r => r.path);

  // Update task with related files
  await bd.update(task.id, { files: relatedFiles });

  // Reserve files for assignee
  if (task.assignee) {
    await mcp_agent_mail.reserve({
      agentId: task.assignee.mcpAgentId,
      files: relatedFiles,
      taskId: task.id, // NOW LINKED
    });
  }
});
```

### Pattern 2: Metrics-Driven Prioritization

```typescript
// When metrics are calculated, update task priority
eventBus.subscribe('metrics.calculated', async (event) => {
  const { taskId, metrics } = event.payload;

  // High blocker score = high priority
  if (metrics.blockerScore > 0.7) {
    await bd.update(taskId, { priority: 'critical' });

    // Notify assignee
    const task = stateManager.getTask(taskId);
    if (task?.assignee) {
      await mcp_agent_mail.send({
        to: task.assignee.mcpAgentId,
        subject: `URGENT: ${task.title} is blocking others`,
        body: `Blocker score: ${metrics.blockerScore}. Please prioritize.`,
      });
    }
  }
});
```

### Pattern 3: AI-Assisted Task Completion

```typescript
// When AI module is optimized, update task
eventBus.subscribe('optimization.completed', async (event) => {
  const { moduleId, metrics } = event.payload;

  // Find linked task
  const tasks = stateManager.getTasksByState('in_progress')
    .filter(t => t.metadata?.moduleId === moduleId);

  for (const task of tasks) {
    // Update task with results
    await bd.update(task.id, {
      metadata: { ...task.metadata, optimizationMetrics: metrics },
    });

    // Transition to review
    await bd.transition(task.id, 'review');

    // Notify for review
    await mcp_agent_mail.broadcast({
      channel: 'ai-reviews',
      subject: `AI Module Ready: ${task.title}`,
      body: `Optimization complete. Metrics: ${JSON.stringify(metrics)}`,
    });
  }
});
```

## Configuration

```typescript
const orchestratorConfig = {
  // Event handling
  eventPropagation: true,
  maxEventLogSize: 10000,

  // Caching
  taskCacheEnabled: true,
  searchCacheMaxAge: 3600000, // 1 hour
  searchCacheMaxSize: 1000,

  // Workflows
  defaultTimeout: 30000,
  parallelExecution: true,
  transactionalWorkflows: true,

  // Metrics
  metricsEnabled: true,
  snapshotInterval: 60000, // 1 minute

  // Integration
  autoRouteEvents: true,
  linkReservationsToTasks: true, // FIX for red-team gap
};
```

## Skill Dependencies

| Skill | Version | Integration |
|-------|---------|-------------|
| bd | 0.28.0 | Task management, DAG dependencies |
| bv | 0.1.0 | Graph metrics, critical path |
| mcp_agent_mail | 0.1.0 | Notifications, reservations |
| osgrep | 0.4.15 | Semantic search, ColBERT |
| leann | 0.14.0 | RAG indexing, anchor-based |
| dspy-code | 2.6.0 | AI modules, optimization |
| agents-md | 1.0.0 | CLAUDE.md architecture |

## Red-Team Validation Fixes

This orchestrator addresses critical gaps from validation:

| Gap | Score Before | Fix | Score After |
|-----|-------------|-----|-------------|
| bd.assignee ≠ Agent | 48/100 | UnifiedAgent type | 85/100 |
| No event propagation | 48/100 | EventBus + Router | 90/100 |
| Reservations unlinked | 48/100 | taskId in reservation | 88/100 |
| osgrep/leann overlap | 72/100 | RRF fusion pipeline | 92/100 |
| No shared types | 48/100 | types/shared.ts | 90/100 |

## Directory Structure

```
orchestrator/
├── SKILL.md                    # This file
├── types/
│   └── shared.ts               # Unified type definitions
├── events/
│   └── bridge.ts               # Event bus, router, adapters
├── state/
│   └── manager.ts              # State management, caching
├── workflows/
│   ├── engine.ts               # Workflow execution engine
│   ├── task-intelligence.md    # bd → bv → mcp_agent_mail
│   ├── code-discovery.md       # osgrep ↔ leann
│   └── ai-development.md       # dspy-code + all
├── patterns/                   # Integration patterns
├── templates/                  # Workflow templates
└── scripts/                    # Utility scripts
```

## Command Reference

```bash
# Execute workflow
orchestrator execute task-intelligence --input '{"taskTitle": "..."}'

# Check state
orchestrator state tasks
orchestrator state workflows
orchestrator state metrics

# Event management
orchestrator events list
orchestrator events subscribe task.created
orchestrator events publish '{"type": "task.created", ...}'

# Cache management
orchestrator cache clear
orchestrator cache stats
```

## Metrics Tracked

| Metric | Description |
|--------|-------------|
| workflowsExecuted | Total composite workflows run |
| eventsProcessed | Cross-skill events handled |
| cacheHits/Misses | Cache efficiency |
| averageWorkflowDuration | Performance tracking |
| skillInvocations | Per-skill usage stats |

## References

- `workflows/task-intelligence.md` - Task Intelligence Pipeline
- `workflows/code-discovery.md` - Code Discovery Pipeline
- `workflows/ai-development.md` - AI Development Pipeline
- `types/shared.ts` - Type definitions
- `events/bridge.ts` - Event system
- `state/manager.ts` - State management

---

**Key Principle**: Orchestrator enables **emergent capabilities** through skill composition. Individual skills remain atomic and independent; orchestrator provides the integration layer that makes them greater than the sum of their parts.
