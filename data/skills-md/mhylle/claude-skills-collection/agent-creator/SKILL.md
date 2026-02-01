---
name: agent-creator
description: |
  Create composable AI agent systems in NestJS projects following the "tools all the way down" architecture. Use this skill when users want to: (1) Create new AI agents with orchestrator/planner/executor/evaluator components, (2) Build agentic systems that can call other agents as tools, (3) Implement DAG-based planning with parallel execution, (4) Add database-backed state persistence for agent runs, (5) Create custom evaluators for quality assurance. Triggers on "create agent", "build agent", "agent system", "agentic", "orchestrator", "planner/executor pattern", or NestJS AI agent requests.
context: fork
agent: Explore
---

# Agent Creator

Create composable AI agent systems in NestJS with uniform tool interfaces, DAG-based planning, and database-backed state.

## Core Concept

Every agent system exposes the same `Tool` interface as a simple tool. Callers don't know if they're calling a web search API or a complex research system. This enables arbitrary composition and nesting.

## Workflow

### 1. Gather Requirements

Ask the user:

1. **Purpose**: What should this agent accomplish?
2. **Inputs/Outputs**: What data goes in and comes out?
3. **Tools**: What capabilities does it need? (existing tools or other agents)
4. **Success Criteria**: How do we know the output is good?
5. **Evaluator Types**: What quality dimensions matter? (see [evaluators.md](references/evaluators.md))

### 2. Generate Agent Structure

Create this NestJS module structure:

```
src/agents/{agent-name}/
├── {agent-name}.module.ts           # NestJS module
├── {agent-name}.tool.ts             # Tool interface (public API)
├── services/
│   ├── orchestrator.service.ts      # Workflow coordination
│   ├── planner.service.ts           # Plan generation
│   ├── executor.service.ts          # Tool execution
│   └── state.service.ts             # State management
├── evaluators/
│   ├── evaluator.registry.ts        # Registry service
│   └── {type}.evaluator.ts          # Per evaluator type
├── tools/
│   └── tool.registry.ts             # Available tools
├── entities/                         # TypeORM entities
├── dto/                              # Input/output DTOs
├── prompts/                          # LLM prompts
├── config/
│   └── {agent-name}.config.ts
└── interfaces/
```

### 3. Implement Components

For each component, follow the patterns in:
- [architecture.md](references/architecture.md) - Core interfaces, component roles, loops
- [nestjs-patterns.md](references/nestjs-patterns.md) - NestJS service templates
- [prompts.md](references/prompts.md) - System prompts for planner/executor/evaluators
- [evaluators.md](references/evaluators.md) - Built-in evaluator types

### 4. Wire Up Module

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([...entities])],
  providers: [
    OrchestratorService,
    PlannerService,
    ExecutorService,
    StateService,
    EvaluatorRegistry,
    ...evaluators,
    ToolRegistry,
    AgentTool,
  ],
  exports: [AgentTool], // Only export the Tool interface
})
export class AgentNameModule {}
```

## Key Architecture Rules

1. **Uniform Interface**: Agent's public API is always `Tool.execute(input, context)`
2. **Planning Loop**: plan → evaluate plan → revise → repeat (max iterations)
3. **Execution Loop**: execute step → evaluate → retry with feedback → repeat
4. **DAG Plans**: Steps declare dependencies; independent steps run in parallel
5. **State Persistence**: All context, messages, plans, executions stored in PostgreSQL
6. **Composition**: Agents can use other agents as tools transparently

## Quick Reference

### Tool Interface

```typescript
interface Tool {
  id: string;
  name: string;
  description: string;
  inputSchema: JSONSchema;
  outputSchema: JSONSchema;
  execute(input: any, context?: ExecutionContext): Promise<ToolResult>;
}
```

### Plan Structure

```typescript
interface Plan {
  id: string;
  goal: string;
  success_criteria: string[];
  steps: PlanStep[];
}

interface PlanStep {
  id: string;
  description: string;
  tool_id: string;
  input: any;
  success_criteria: string[];
  evaluator_type: string;
  depends_on: string[];  // DAG dependencies
}
```

### Default Config

```typescript
export const agentConfig = {
  maxDepth: 3,
  maxPlanIterations: 3,
  maxStepRetries: 3,
  timeoutMs: 300000,
  llm: { model: 'claude-sonnet-4-20250514', maxTokens: 4096 },
};
```

## Composition Example

After creating `research-agent` and `document-generator`:

```typescript
// document-generator/tools/tool.registry.ts
@Injectable()
export class ToolRegistry {
  constructor(private readonly researchTool: ResearchTool) {
    this.register(this.researchTool);
  }
}
```

The document generator's planner can now create steps using `research-system-v1` as a tool_id.
