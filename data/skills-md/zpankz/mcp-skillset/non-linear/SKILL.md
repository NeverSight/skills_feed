---
name: non-linear
description: Uncertainty-aware non-linear reasoning system with recursive subagent orchestration. Triggers for complex reasoning, research, multi-domain synthesis, or when explicit commands `/nlr`, `/reason`, `/think-deep` are used. Integrates think skill (reasoning), agent-core skill (acting), and MCP tools (infranodus, exa, scholar-gateway) in recursive think→act→observe loops. Uses coding sandbox for execution validation and maintains deliberate noisiness via NoisyGraph scaffold. Supports `/compact` mode for abbreviated outputs and `/semantic` mode for rich exploration.
---

# Non-Linear Reasoning

Execute uncertainty-aware reasoning through recursive think→act→observe loops using Anthropic's orchestrator-worker pattern with effort scaling.

## Quick Reference

| Need | Go To |
|------|-------|
| Research orchestration | [references/RESEARCH-ORCHESTRATION.md](references/RESEARCH-ORCHESTRATION.md) |
| Subagent patterns | [references/SUBAGENTS.md](references/SUBAGENTS.md) |
| MCP integration | [references/MCP-INTEGRATION.md](references/MCP-INTEGRATION.md) |
| State persistence | [references/STATE-PERSISTENCE.md](references/STATE-PERSISTENCE.md) |
| NoisyGraph schema | [references/NOISY-GRAPH.md](references/NOISY-GRAPH.md) |
| Sandbox execution | [references/SANDBOX.md](references/SANDBOX.md) |

## Triggers

| Trigger | Mode | Effort Level |
|---------|------|--------------|
| `/nlr`, `/reason`, `/think-deep` | Full | Adaptive (1-10 subagents) |
| `/compact` | Abbreviated | Minimal (1-3 subagents) |
| `/semantic` | Exploratory | Maximum (5-10 subagents) |
| `/research [topic]` | Research | Full orchestrator-worker |
| Complex query auto-detect | Adaptive | Score-based scaling |

## Architecture: Orchestrator-Worker Pattern

Based on Anthropic's multi-agent research system architecture:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      LEAD RESEARCHER (Orchestrator)                  │
│  • Analyzes query complexity → determines effort level              │
│  • Develops research strategy → saves to Memory                      │
│  • Spawns specialized subagents → coordinates parallel execution     │
│  • Synthesizes findings → handles citation attribution               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│   │  MAPPER     │  │  SKEPTIC    │  │  SEARCHER   │    ...         │
│   │  SUBAGENT   │  │  SUBAGENT   │  │  SUBAGENT   │                │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                │
│          │                │                │                        │
│          └────────────────┴────────────────┘                        │
│                           │                                         │
│                   ┌───────▼───────┐                                 │
│                   │    MEMORY     │  (State persistence)            │
│                   │  checkpoint   │                                 │
│                   └───────────────┘                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Effort Scaling (Anthropic Pattern)

Query complexity determines subagent allocation:

| Complexity | Subagents | Tool Calls | Use Case |
|------------|-----------|------------|----------|
| Simple | 1 | 3-10 | Single fact-finding |
| Moderate | 2-4 | 10-30 | Multi-source synthesis |
| Complex | 5-10 | 30-100+ | Deep research, comparison |

### Complexity Classification

```python
def classify_effort(query: str, context: dict) -> EffortLevel:
    score = 0
    
    # Domain complexity
    domains = detect_domains(query)  # medical, legal, technical, etc.
    score += len(domains) * 2
    
    # Reasoning indicators
    if any(w in query.lower() for w in ['compare', 'analyze', 'synthesize']):
        score += 3
    if any(w in query.lower() for w in ['mechanism', 'pathway', 'causation']):
        score += 4
    
    # Stakes multiplier (medical/legal = high stakes)
    if 'medical' in domains or 'legal' in domains:
        score *= 1.5
    
    # Novelty (requires verification)
    if requires_current_information(query):
        score += 2
    
    return EffortLevel.from_score(score)
    # < 4: SIMPLE, 4-8: MODERATE, > 8: COMPLEX
```

## Core Workflow

### Phase 1: Initialize Lead Researcher

```python
# Extended thinking for strategy development
thoughtbox({
    thought: """
    LEAD RESEARCHER INITIALIZATION
    Query: {query}
    
    Strategy Development:
    1. Complexity assessment: {classify_effort(query)}
    2. Domain identification: {detect_domains(query)}
    3. Subagent allocation: {determine_subagents(effort_level)}
    4. Research plan: {develop_plan(query, context)}
    """,
    thoughtNumber: 1,
    totalThoughts: effort_level.max_iterations,
    nextThoughtNeeded: True,
    includeGuide: True
})

# Save plan to memory for context overflow recovery
checkpoint_state({
    "plan": research_plan,
    "subagents": allocated_subagents,
    "iteration": 0
})
```

### Phase 2: Spawn Subagents with Task Descriptions

Each subagent receives detailed instructions to prevent duplication:

```python
SUBAGENT_TEMPLATES = {
    "mapper": {
        "objective": "Extract entities, relationships, and structural gaps from {domain}",
        "output_format": {
            "entities": [{"label": str, "confidence": float, "evidence": list}],
            "relationships": [{"source": str, "target": str, "type": str}],
            "gaps": [{"description": str, "suggested_placeholder": str}]
        },
        "tool_guidance": "Use infranodus for graph analysis, exa for current info",
        "boundaries": "Focus on {domain} only. Do not search {excluded_domains}",
        "context": "{relevant_prior_findings}"
    },
    "skeptic": {
        "objective": "Challenge assumptions and quantify uncertainty for {topic}",
        "output_format": {
            "challenged_claims": [{"claim": str, "concern": str, "confidence_adjustment": float}],
            "missing_falsifiers": [str],
            "noise_budget_status": {"current": float, "target": float}
        },
        "tool_guidance": "Use Scholar Gateway for peer-reviewed counterevidence",
        "boundaries": "Only challenge claims with confidence > 0.7",
        "context": "{current_graph_state}"
    },
    "searcher": {
        "objective": "Gather evidence on {specific_question}",
        "output_format": {
            "findings": [{"fact": str, "source": str, "confidence": float}],
            "gaps_discovered": [str]
        },
        "tool_guidance": "Prioritize: Scholar Gateway > exa > web_search",
        "boundaries": "Max 5 tool calls. Return condensed findings only.",
        "context": "{search_focus_areas}"
    }
}

async def spawn_subagent(template_name: str, params: dict) -> SubagentResult:
    template = SUBAGENT_TEMPLATES[template_name]
    
    # Inject NoisyGraph reasoning framework
    system_prompt = f"""
    ## Subagent: {template_name}
    
    You are operating within the NoisyGraph reasoning framework.
    
    OBJECTIVE: {template['objective'].format(**params)}
    
    OUTPUT FORMAT: Return JSON matching:
    {json.dumps(template['output_format'], indent=2)}
    
    TOOL GUIDANCE: {template['tool_guidance']}
    
    BOUNDARIES: {template['boundaries'].format(**params)}
    
    UNCERTAINTY REQUIREMENTS:
    - Rate confidence 0-1 for each finding
    - Explicitly note assumptions
    - Flag low-confidence elements (≤0.5) for noise budget
    
    CONTEXT: {template['context'].format(**params)}
    """
    
    # Use extended thinking for reasoning trace
    result = await execute_with_thinking(system_prompt, params['query'])
    
    return parse_subagent_result(result, template['output_format'])
```

### Phase 3: Parallel Subagent Execution

```python
async def execute_subagents_parallel(
    subagent_configs: list[dict],
    scaffold: NoisyGraphScaffold
) -> list[SubagentResult]:
    """Execute subagents in parallel with isolated contexts."""
    
    # Emit spawn events
    for config in subagent_configs:
        await event_bus.publish({
            'type': 'nlr.subagent.spawned',
            'payload': {'agent_id': config['id'], 'type': config['type']}
        })
    
    # Parallel execution
    results = await asyncio.gather(*[
        spawn_subagent(config['type'], config['params'])
        for config in subagent_configs
    ], return_exceptions=True)
    
    # Handle failures gracefully
    valid_results = []
    for config, result in zip(subagent_configs, results):
        if isinstance(result, Exception):
            scaffold.self_correction.issues_found.append(
                f"Subagent {config['id']} failed: {result}"
            )
        else:
            valid_results.append(result)
    
    return valid_results
```

### Phase 4: NoisyGraph Integration

Build uncertainty-aware knowledge graph from subagent findings:

```python
def integrate_subagent_findings(
    scaffold: NoisyGraphScaffold,
    results: list[SubagentResult]
) -> None:
    """Integrate subagent findings into NoisyGraph scaffold."""
    
    for result in results:
        # Add entities as nodes
        for entity in result.get('entities', []):
            add_node(scaffold,
                label=entity['label'],
                description=entity.get('why_relevant', ''),
                node_type=infer_node_type(entity),
                confidence=entity['confidence'],
                evidence=entity.get('evidence', [])
            )
        
        # Add relationships as edges
        for rel in result.get('relationships', []):
            add_edge(scaffold,
                source_id=get_node_id(rel['source']),
                target_id=get_node_id(rel['target']),
                edge_type=EdgeType(rel['type']),
                description=rel.get('description', ''),
                strength=rel.get('strength', 0.5)
            )
        
        # Process gaps into placeholders
        for gap in result.get('gaps', []):
            add_placeholder(scaffold, gap)
        
        # Apply skeptic challenges
        for challenge in result.get('challenged_claims', []):
            apply_confidence_adjustment(scaffold, challenge)
```

### Phase 5: Self-Correction with Extended Thinking

```python
async def self_correct_with_reasoning(scaffold: NoisyGraphScaffold) -> None:
    """Run self-correction with explicit reasoning trace."""
    
    await thoughtbox({
        'thought': f"""
        SELF-CORRECTION PHASE
        
        Current State:
        - Nodes: {len(scaffold.graph.nodes)}
        - Edges: {len(scaffold.graph.edges)}
        - Topology ratio: {len(scaffold.graph.edges)/len(scaffold.graph.nodes):.2f}
        
        Checklist Evaluation:
        1. Duplicate labels: {check_duplicates(scaffold)}
        2. Dangling edges: {check_edge_integrity(scaffold)}
        3. Noise budget: {check_noise_budget(scaffold)}
        4. Falsifiability: {check_falsifiability(scaffold)}
        5. Topology target: {check_topology(scaffold)}
        
        Issues Found: {scaffold.self_correction.issues_found}
        
        Corrective Actions:
        {generate_corrective_actions(scaffold)}
        """,
        'thoughtNumber': scaffold.meta.iteration + 1,
        'totalThoughts': scaffold.meta.iteration_limit,
        'nextThoughtNeeded': True
    })
    
    # Apply corrections
    apply_corrections(scaffold)
```

### Phase 6: State Checkpoint

```python
def checkpoint_state(scaffold: NoisyGraphScaffold, checkpoint_id: str) -> None:
    """Save state for context overflow recovery."""
    
    checkpoint = {
        "id": checkpoint_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "meta": scaffold.meta.__dict__,
        "graph_summary": {
            "node_count": len(scaffold.graph.nodes),
            "edge_count": len(scaffold.graph.edges),
            "topology_ratio": len(scaffold.graph.edges) / max(1, len(scaffold.graph.nodes)),
            "noise_ratio": calculate_noise_ratio(scaffold)
        },
        "key_findings": extract_key_findings(scaffold),
        "open_gaps": [g for g in scaffold.core.implied_relationships_and_gaps if not g.get('resolved')],
        "next_actions": scaffold.meta.get('next_actions', [])
    }
    
    # Save to filesystem for persistence
    save_checkpoint(checkpoint, f"/home/claude/nlr_checkpoints/{checkpoint_id}.json")
```

### Phase 7: Synthesis with Citation

```python
async def synthesize_findings(scaffold: NoisyGraphScaffold) -> SynthesisResult:
    """Final synthesis with proper citation attribution."""
    
    # Use extended thinking for synthesis
    synthesis = await thoughtbox({
        'thought': f"""
        FINAL SYNTHESIS
        
        Research Question: {scaffold.meta.topic}
        
        Key Findings (by confidence):
        {format_findings_by_confidence(scaffold)}
        
        Structural Analysis:
        - Central concepts: {identify_hubs(scaffold)}
        - Knowledge gaps: {identify_gaps(scaffold)}
        - Contradictions: {identify_contradictions(scaffold)}
        
        Uncertainty Summary:
        - High confidence (>0.8): {count_high_confidence(scaffold)} elements
        - Low confidence (≤0.5): {count_low_confidence(scaffold)} elements
        - Noise budget: {check_noise_budget(scaffold)}
        
        SYNTHESIS:
        [Integrate findings into coherent narrative with explicit uncertainty markers]
        
        RECOMMENDATIONS:
        [Identify areas requiring further research]
        """,
        'thoughtNumber': scaffold.meta.iteration,
        'totalThoughts': scaffold.meta.iteration,
        'nextThoughtNeeded': False,
        'includeGuide': True
    })
    
    # Process citations
    cited_synthesis = process_citations(synthesis, scaffold.graph.nodes)
    
    return SynthesisResult(
        synthesis=cited_synthesis,
        confidence=calculate_overall_confidence(scaffold),
        graph=scaffold.graph,
        uncertainties=extract_key_uncertainties(scaffold),
        recommendations=extract_recommendations(synthesis),
        trace=build_execution_trace(scaffold)
    )
```

## Mode Selection

### /compact Mode

Output format: `[NLR:i{iter}/{max}|n{nodes}|e{edges}|r{ratio}|c{conf}]`

```python
def compact_output(scaffold: NoisyGraphScaffold) -> str:
    return (
        f"[NLR:i{scaffold.meta.iteration}/{scaffold.meta.iteration_limit}|"
        f"n{len(scaffold.graph.nodes)}|"
        f"e{len(scaffold.graph.edges)}|"
        f"r{len(scaffold.graph.edges)/max(1,len(scaffold.graph.nodes)):.1f}|"
        f"c{calculate_confidence(scaffold):.2f}] "
        f"SYNTHESIS: {scaffold.synthesis[:200]}... "
        f"GAPS: {', '.join(scaffold.key_gaps[:3])}"
    )
```

### /semantic Mode

Full NoisyGraph JSON output with all subagent traces visible.

### /research Mode

Full orchestrator-worker pattern with maximum effort scaling.

## Integration Points

### Think Skill Integration

| Tool | Usage Pattern |
|------|---------------|
| `thoughtbox` | Extended reasoning with interleaved tool calls |
| `mental_models` | Framework selection per problem type |
| `notebook` | Computational validation |

### Agent-Core Integration

```typescript
const nlrConfig: SkillEventSystemConfig<'nlr'> = {
    skillName: 'nlr',
    displayName: 'NON-LINEAR-REASONING',
    groups: {
        orchestrator: defineEventGroup('orchestrator', {
            plan_created: event('plan_created'),
            effort_scaled: event('effort_scaled'),
            checkpoint_saved: event('checkpoint_saved')
        }),
        subagent: defineEventGroup('subagent', {
            spawned: event('spawned'),
            completed: event('completed'),
            failed: criticalEvent('failed')
        }),
        graph: defineEventGroup('graph', {
            node_added: event('node_added'),
            edge_added: event('edge_added'),
            self_corrected: event('self_corrected')
        }),
        synthesis: defineEventGroup('synthesis', {
            started: event('started'),
            completed: event('completed')
        })
    }
};
```

### MCP Tool Coordination

| Tool | Role in NLR |
|------|-------------|
| `infranodus:getGraphAndAdvice` | Structural gap detection, topic clustering |
| `infranodus:getGraphAndStatements` | Knowledge graph extraction |
| `exa:web_search_exa` | Current information retrieval |
| `exa:get_code_context_exa` | Technical documentation |
| `Scholar Gateway:semanticSearch` | Peer-reviewed literature |
| `atom-of-thoughts:AoT` | Deep atomic decomposition |

## Configuration

```python
NLR_CONFIG = {
    # Effort scaling
    "effort_levels": {
        "simple": {"subagents": 1, "max_tool_calls": 10, "iterations": 3},
        "moderate": {"subagents": 3, "max_tool_calls": 30, "iterations": 5},
        "complex": {"subagents": 7, "max_tool_calls": 100, "iterations": 9}
    },
    
    # NoisyGraph targets
    "noise_budget": 0.25,
    "topology_target": 4.0,
    "max_nodes": 60,
    "max_edges": 240,
    
    # Convergence
    "convergence_threshold": 0.95,
    "max_iterations": 9,
    
    # Checkpointing
    "checkpoint_interval": 3,
    "checkpoint_path": "/home/claude/nlr_checkpoints"
}
```

## Error Handling

```python
async def execute_with_recovery(scaffold: NoisyGraphScaffold) -> SynthesisResult:
    try:
        return await execute_nlr_loop(scaffold)
    except ContextOverflowError:
        # Load from checkpoint, spawn fresh subagents
        checkpoint = load_latest_checkpoint(scaffold.meta.topic)
        scaffold = restore_from_checkpoint(checkpoint)
        return await execute_nlr_loop(scaffold)
    except SubagentFailure as e:
        # Continue with remaining subagents
        scaffold.agents = [a for a in scaffold.agents if a.id != e.agent_id]
        return await execute_nlr_loop(scaffold)
    except MCPToolTimeout:
        # Graceful degradation with cached data
        return synthesize_with_partial_data(scaffold)
```

## References

- [references/RESEARCH-ORCHESTRATION.md](references/RESEARCH-ORCHESTRATION.md) - Orchestrator-worker pattern details
- [references/SUBAGENTS.md](references/SUBAGENTS.md) - Subagent specifications and task templates
- [references/STATE-PERSISTENCE.md](references/STATE-PERSISTENCE.md) - Checkpointing and recovery
- [references/MCP-INTEGRATION.md](references/MCP-INTEGRATION.md) - MCP tool coordination
- [references/NOISY-GRAPH.md](references/NOISY-GRAPH.md) - Complete NoisyGraph schema
- [references/SANDBOX.md](references/SANDBOX.md) - Code execution patterns

---

*Non-Linear Reasoning v2.0 - Orchestrator-Worker Pattern with Effort Scaling*
