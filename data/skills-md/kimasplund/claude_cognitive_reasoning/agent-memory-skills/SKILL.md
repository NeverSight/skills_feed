---
name: agent-memory-skills
description: Self-improving agent architecture using ChromaDB for continuous learning, self-evaluation, and improvement storage. Agents maintain separate memory collections for learned patterns, performance metrics, and self-assessments without modifying their static .md configuration.
license: MIT
---

# Agent Memory & Continuous Self-Improvement Skills

**Purpose**: Enable agents to learn from experience, evaluate themselves continuously, and store improvements in ChromaDB collections separate from static configuration files.

**Philosophy**: Static configuration (.md) for capabilities; dynamic memory (ChromaDB) for learned experiences.

---

## Architecture Overview

### The Dual-Layer Model

```
┌──────────────────────────────────────────────────────────┐
│ Layer 1: Static Agent Configuration (.md files)          │
│ - Core capabilities, workflows, prompt templates         │
│ - Human-designed, expert-reviewed                        │
│ - Version controlled (Git)                               │
│ - Changes: Infrequent (weeks/months)                     │
└──────────────────────────────────────────────────────────┘
                          ↓ loads at runtime
┌──────────────────────────────────────────────────────────┐
│ Layer 2: Dynamic Agent Memory (ChromaDB)                 │
│ - Learned improvements, preferences, patterns            │
│ - Self-evaluation results, performance metrics           │
│ - Agent-managed, auto-updated                            │
│ - Changes: Continuous (every task completion)            │
└──────────────────────────────────────────────────────────┘
```

### Memory Collection Structure

Each agent gets **3 ChromaDB collections**:

1. **`agent_{name}_improvements`**: Learned patterns and strategies
2. **`agent_{name}_evaluations`**: Self-assessment results
3. **`agent_{name}_performance`**: Metrics over time

---

## Collection 1: Improvements Storage

### When to Store Improvements

Store when:
- ✅ Task completed successfully with clear learning
- ✅ User feedback received (positive or negative)
- ✅ New pattern discovered (not in static config)
- ✅ Confidence score ≥ 0.7 (high confidence learning)

Don't store:
- ❌ Failed tasks without clear lessons
- ❌ Routine operations following existing patterns
- ❌ Low confidence observations (< 0.5)

### Improvement Schema

```javascript
const improvement = {
  // Document (semantic search target)
  document: `
    When user asks for "latest" information, prioritize sources from 2025
    over 2024. Use date filters: where: { year: { "$gte": 2025 } }
  `,

  // ID (unique, timestamp-based)
  id: `improvement_research_${Date.now()}`,

  // Metadata (for filtering)
  metadata: {
    agent_name: "research-specialist",
    category: "search_strategy",
    learned_from: "feedback_2025-11-18",
    confidence: 0.85,
    success_rate: null,  // Will be updated with usage
    usage_count: 0,
    created_at: "2025-11-18T15:30:00Z",
    last_used: null,
    tags: ["recency", "date_filtering", "search"]
  }
};
```

### Storage Function

```javascript
async function storeImprovement(agentName, improvement) {
  const collectionName = `agent_${agentName}_improvements`;

  // Ensure collection exists
  const collections = await mcp__chroma__list_collections();
  if (!collections.includes(collectionName)) {
    await mcp__chroma__create_collection({
      collection_name: collectionName,
      embedding_function_name: "default",
      metadata: {
        agent: agentName,
        purpose: "learned_improvements",
        created_at: new Date().toISOString()
      }
    });
  }

  // Store improvement
  await mcp__chroma__add_documents({
    collection_name: collectionName,
    documents: [improvement.document],
    ids: [improvement.id],
    metadatas: [improvement.metadata]
  });

  console.log(`✅ Stored improvement for ${agentName}: ${improvement.category}`);
}
```

### Retrieval Before Task

```javascript
async function retrieveRelevantImprovements(agentName, taskDescription, limit = 5) {
  const collectionName = `agent_${agentName}_improvements`;

  try {
    const results = await mcp__chroma__query_documents({
      collection_name: collectionName,
      query_texts: [taskDescription],
      n_results: limit,
      where: {
        "$and": [
          { "confidence": { "$gte": 0.7 } },  // High confidence only
          { "success_rate": { "$gte": 0.6 } }  // Or null (new, untested)
        ]
      },
      include: ["documents", "metadatas", "distances"]
    });

    // Filter by relevance (distance < 0.4)
    const relevant = results.ids[0]
      .map((id, idx) => ({
        id: id,
        improvement: results.documents[0][idx],
        metadata: results.metadatas[0][idx],
        relevance: 1 - results.distances[0][idx]
      }))
      .filter(item => item.relevance > 0.6);

    return relevant;
  } catch (error) {
    console.log(`No improvements found for ${agentName} (collection may not exist yet)`);
    return [];
  }
}
```

---

## Collection 2: Self-Evaluation Storage

### Continuous Self-Evaluation Pattern

After **every task**, agents run self-evaluation:

```javascript
async function selfEvaluate(agentName, taskContext, taskResult) {
  const evaluation = {
    // What was the task?
    task_description: taskContext.description,
    task_type: taskContext.type,  // "research", "code", "debug", etc.

    // How did I perform?
    success: taskResult.success,  // true/false
    quality_score: taskResult.quality,  // 0-100
    time_taken_ms: taskResult.duration,
    tokens_used: taskResult.tokens,

    // What went well?
    strengths: identifyStrengths(taskResult),
    // What went poorly?
    weaknesses: identifyWeaknesses(taskResult),

    // What did I learn?
    insights: extractInsights(taskResult),

    // Metadata
    timestamp: new Date().toISOString(),
    context: taskContext.additionalContext
  };

  // Store evaluation
  await storeEvaluation(agentName, evaluation);

  // If strong learning → store as improvement
  if (evaluation.insights.length > 0 && evaluation.quality_score >= 70) {
    for (const insight of evaluation.insights) {
      await storeImprovement(agentName, {
        document: insight.description,
        id: `improvement_${agentName}_${Date.now()}`,
        metadata: {
          agent_name: agentName,
          category: insight.category,
          learned_from: `task_${evaluation.timestamp}`,
          confidence: insight.confidence,
          created_at: evaluation.timestamp
        }
      });
    }
  }

  return evaluation;
}

function identifyStrengths(taskResult) {
  const strengths = [];

  if (taskResult.time_taken_ms < taskResult.expected_duration) {
    strengths.push("Completed faster than expected");
  }

  if (taskResult.validation_passed) {
    strengths.push("All validations passed");
  }

  if (taskResult.user_feedback?.positive) {
    strengths.push(taskResult.user_feedback.comment);
  }

  return strengths;
}

function identifyWeaknesses(taskResult) {
  const weaknesses = [];

  if (taskResult.errors.length > 0) {
    weaknesses.push(`Encountered ${taskResult.errors.length} errors`);
  }

  if (taskResult.retries > 0) {
    weaknesses.push(`Required ${taskResult.retries} retries`);
  }

  if (taskResult.user_feedback?.negative) {
    weaknesses.push(taskResult.user_feedback.comment);
  }

  return weaknesses;
}

function extractInsights(taskResult) {
  const insights = [];

  // Example: Learned a new error handling pattern
  if (taskResult.errors.some(e => e.type === "ConnectionTimeout") && taskResult.success) {
    insights.push({
      description: "When encountering ConnectionTimeout, retry with exponential backoff (3 attempts)",
      category: "error_handling",
      confidence: 0.8
    });
  }

  // Example: Discovered optimal parameter
  if (taskResult.optimization_found) {
    insights.push({
      description: taskResult.optimization_found.description,
      category: "optimization",
      confidence: 0.9
    });
  }

  return insights;
}
```

### Evaluation Storage

```javascript
async function storeEvaluation(agentName, evaluation) {
  const collectionName = `agent_${agentName}_evaluations`;

  await mcp__chroma__add_documents({
    collection_name: collectionName,
    documents: [
      `Task: ${evaluation.task_description}. Result: ${evaluation.success ? 'Success' : 'Failure'}. ` +
      `Quality: ${evaluation.quality_score}/100. Insights: ${evaluation.insights.map(i => i.description).join('; ')}`
    ],
    ids: [`eval_${Date.now()}`],
    metadatas: [{
      agent_name: agentName,
      task_type: evaluation.task_type,
      success: evaluation.success,
      quality_score: evaluation.quality_score,
      time_taken_ms: evaluation.time_taken_ms,
      tokens_used: evaluation.tokens_used,
      strengths_count: evaluation.strengths.length,
      weaknesses_count: evaluation.weaknesses.length,
      insights_count: evaluation.insights.length,
      timestamp: evaluation.timestamp
    }]
  });
}
```

---

## Collection 3: Performance Metrics

### Aggregate Performance Tracking

```javascript
async function trackPerformanceMetrics(agentName) {
  const collectionName = `agent_${agentName}_evaluations`;

  // Retrieve last 100 evaluations
  const recentEvals = await mcp__chroma__get_documents({
    collection_name: collectionName,
    limit: 100,
    include: ["metadatas"],
    where: {
      "timestamp": { "$gte": thirtyDaysAgo() }
    }
  });

  const metrics = {
    agent_name: agentName,
    period: "30_days",

    // Success metrics
    total_tasks: recentEvals.metadatas.length,
    successful_tasks: recentEvals.metadatas.filter(m => m.success).length,
    success_rate: 0,

    // Quality metrics
    avg_quality: average(recentEvals.metadatas.map(m => m.quality_score)),
    quality_trend: calculateTrend(recentEvals.metadatas, 'quality_score'),

    // Efficiency metrics
    avg_time_ms: average(recentEvals.metadatas.map(m => m.time_taken_ms)),
    avg_tokens: average(recentEvals.metadatas.map(m => m.tokens_used)),

    // Learning metrics
    total_insights: sum(recentEvals.metadatas.map(m => m.insights_count)),
    improvements_stored: await countImprovements(agentName, thirtyDaysAgo()),

    // Trend
    improving: false,  // Will calculate
    timestamp: new Date().toISOString()
  };

  metrics.success_rate = metrics.successful_tasks / metrics.total_tasks;

  // Is agent improving over time?
  metrics.improving = metrics.quality_trend > 0 && metrics.success_rate > 0.7;

  // Store aggregated metrics
  const perfCollection = `agent_${agentName}_performance`;
  await mcp__chroma__add_documents({
    collection_name: perfCollection,
    documents: [
      `Performance snapshot: ${metrics.success_rate * 100}% success, ` +
      `quality ${metrics.avg_quality}/100, ${metrics.improvements_stored} improvements`
    ],
    ids: [`perf_${Date.now()}`],
    metadatas: [metrics]
  });

  return metrics;
}

function calculateTrend(evaluations, metric) {
  if (evaluations.length < 2) return 0;

  const recent = evaluations.slice(0, Math.floor(evaluations.length / 2));
  const older = evaluations.slice(Math.floor(evaluations.length / 2));

  const recentAvg = average(recent.map(e => e[metric]));
  const olderAvg = average(older.map(e => e[metric]));

  return recentAvg - olderAvg;  // Positive = improving
}
```

---

## Complete Workflow: Agent with Memory

### At Agent Initialization

```javascript
async function initializeAgentMemory(agentName) {
  // Load static configuration from .md file
  const staticConfig = await loadAgentConfig(`/agents/${agentName}.md`);

  // Load dynamic improvements from ChromaDB
  const improvements = await retrieveAllImprovements(agentName);

  // Combine static + dynamic
  return {
    ...staticConfig,
    learned_improvements: improvements,
    memory_enabled: true
  };
}
```

### Before Task Execution

```javascript
async function executeTaskWithMemory(agentName, task) {
  // Step 1: Retrieve relevant past learnings
  const relevantImprovements = await retrieveRelevantImprovements(
    agentName,
    task.description,
    5  // top 5 improvements
  );

  console.log(`📚 Retrieved ${relevantImprovements.length} relevant improvements`);

  // Step 2: Execute task with improvements as context
  const taskResult = await executeTask(task, {
    improvements: relevantImprovements.map(i => i.improvement)
  });

  // Step 3: Self-evaluate
  const evaluation = await selfEvaluate(agentName, task, taskResult);

  // Step 4: Update improvement usage stats
  for (const improvement of relevantImprovements) {
    await updateImprovementUsage(agentName, improvement.id, taskResult.success);
  }

  // Step 5: Track performance (daily)
  if (shouldRunDailyMetrics()) {
    await trackPerformanceMetrics(agentName);
  }

  return taskResult;
}
```

### Update Improvement Statistics

```javascript
async function updateImprovementUsage(agentName, improvementId, wasSuccessful) {
  const collectionName = `agent_${agentName}_improvements`;

  // Get current improvement
  const current = await mcp__chroma__get_documents({
    collection_name: collectionName,
    ids: [improvementId]
  });

  const metadata = current.metadatas[0];

  // Update statistics
  const newUsageCount = (metadata.usage_count || 0) + 1;
  const successCount = (metadata.success_count || 0) + (wasSuccessful ? 1 : 0);
  const newSuccessRate = successCount / newUsageCount;

  // Update metadata
  await mcp__chroma__update_documents({
    collection_name: collectionName,
    ids: [improvementId],
    metadatas: [{
      ...metadata,
      usage_count: newUsageCount,
      success_count: successCount,
      success_rate: newSuccessRate,
      last_used: new Date().toISOString()
    }]
  });

  // If improvement consistently fails (< 40% success after 10+ uses), mark as deprecated
  if (newUsageCount >= 10 && newSuccessRate < 0.4) {
    console.log(`⚠️ Improvement ${improvementId} has low success rate (${newSuccessRate}), marking deprecated`);

    await mcp__chroma__update_documents({
      collection_name: collectionName,
      ids: [improvementId],
      metadatas: [{
        ...metadata,
        deprecated: true,
        deprecated_reason: "Low success rate after extensive usage"
      }]
    });
  }
}
```

---

## Continuous Evaluation Schedule

### Evaluation Frequency

- **After every task**: Store evaluation (lightweight)
- **Daily**: Calculate performance metrics (aggregation)
- **Weekly**: Review top/bottom improvements, identify trends
- **Monthly**: Archive old evaluations, clean up deprecated improvements

### Scheduled Maintenance

```javascript
async function dailyAgentMaintenance(agentName) {
  console.log(`🔧 Running daily maintenance for ${agentName}...`);

  // 1. Track performance metrics
  const metrics = await trackPerformanceMetrics(agentName);

  // 2. Identify underperforming improvements
  const deprecatedCount = await deprecateFailingImprovements(agentName);

  // 3. Promote high-performing improvements (boost confidence)
  const promotedCount = await promoteSuccessfulImprovements(agentName);

  console.log(`
    Metrics: ${metrics.success_rate * 100}% success, quality ${metrics.avg_quality}/100
    Deprecated: ${deprecatedCount} low-performing improvements
    Promoted: ${promotedCount} high-performing improvements
  `);
}

async function deprecateFailingImprovements(agentName) {
  const collectionName = `agent_${agentName}_improvements`;

  const allImprovements = await mcp__chroma__get_documents({
    collection_name: collectionName,
    where: {
      "$and": [
        { "usage_count": { "$gte": 10 } },
        { "success_rate": { "$lt": 0.4 } },
        { "deprecated": { "$ne": true } }
      ]
    }
  });

  for (const id of allImprovements.ids) {
    await mcp__chroma__update_documents({
      collection_name: collectionName,
      ids: [id],
      metadatas: [{
        ...allImprovements.metadatas[id],
        deprecated: true
      }]
    });
  }

  return allImprovements.ids.length;
}

async function promoteSuccessfulImprovements(agentName) {
  const collectionName = `agent_${agentName}_improvements`;

  const highPerformers = await mcp__chroma__get_documents({
    collection_name: collectionName,
    where: {
      "$and": [
        { "usage_count": { "$gte": 20 } },
        { "success_rate": { "$gte": 0.85 } }
      ]
    }
  });

  for (const [idx, id] of highPerformers.ids.entries()) {
    const metadata = highPerformers.metadatas[idx];

    await mcp__chroma__update_documents({
      collection_name: collectionName,
      ids: [id],
      metadatas: [{
        ...metadata,
        confidence: Math.min(0.95, metadata.confidence + 0.05),  // Boost confidence (max 0.95)
        promoted: true
      }]
    });
  }

  return highPerformers.ids.length;
}
```

---

## Agent Memory Dashboard

### Performance Summary

```javascript
async function getAgentMemoryDashboard(agentName) {
  const dashboard = {
    agent: agentName,
    timestamp: new Date().toISOString(),

    // Improvements
    total_improvements: await countDocuments(`agent_${agentName}_improvements`),
    active_improvements: await countDocuments(`agent_${agentName}_improvements`, {
      "deprecated": { "$ne": true }
    }),
    deprecated_improvements: await countDocuments(`agent_${agentName}_improvements`, {
      "deprecated": true
    }),

    // Evaluations
    total_evaluations: await countDocuments(`agent_${agentName}_evaluations`),
    recent_success_rate: await calculateRecentSuccessRate(agentName, 30),  // Last 30 days

    // Performance
    latest_metrics: await getLatestMetrics(agentName),

    // Top improvements (by success rate)
    top_improvements: await getTopImprovements(agentName, 5),

    // Learning rate
    improvements_last_7_days: await countDocuments(`agent_${agentName}_improvements`, {
      "created_at": { "$gte": sevenDaysAgo() }
    })
  };

  return dashboard;
}
```

---

## Global vs Project Memory Scopes

### Dual-Scope Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Global Memory (~/.claude/chroma_data)                   │
│ - Cross-project patterns that apply everywhere          │
│ - Reusable learnings (search strategies, code quality)  │
│ - Collections: agent_{name}_improvements                │
│ - Persists: Forever (user's institutional knowledge)    │
└─────────────────────────────────────────────────────────┘
                         ↓ query both
┌─────────────────────────────────────────────────────────┐
│ Project Memory (.claude/chroma_data)                    │
│ - Project-specific patterns (this codebase's style)     │
│ - Domain knowledge (this API, this architecture)        │
│ - Collections: agent_{name}_project_{hash}_improvements │
│ - Persists: Project lifetime                            │
└─────────────────────────────────────────────────────────┘
```

### Memory Scope Selection

```javascript
function selectMemoryScope(insight) {
  // Global: Universal patterns
  if (insight.category in ['search_strategy', 'error_handling', 'code_quality',
                           'testing_patterns', 'documentation_style']) {
    return 'global';
  }

  // Project: Codebase-specific patterns
  if (insight.category in ['naming_conventions', 'architecture_patterns',
                           'api_usage', 'domain_terminology']) {
    return 'project';
  }

  // Default: Store in both if uncertain
  return 'both';
}

async function storeWithScope(agentName, improvement, scope = 'global') {
  const globalCollection = `agent_${agentName}_improvements`;
  const projectCollection = `agent_${agentName}_project_${getProjectHash()}_improvements`;

  if (scope === 'global' || scope === 'both') {
    await storeImprovement(globalCollection, improvement);
  }
  if (scope === 'project' || scope === 'both') {
    await storeImprovement(projectCollection, improvement);
  }
}

async function retrieveWithScope(agentName, taskDescription) {
  const globalResults = await retrieveRelevantImprovements(
    `agent_${agentName}_improvements`, taskDescription, 3
  );
  const projectResults = await retrieveRelevantImprovements(
    `agent_${agentName}_project_${getProjectHash()}_improvements`, taskDescription, 3
  );

  // Merge and deduplicate, project-specific takes priority
  return mergeImprovements(projectResults, globalResults);
}
```

---

## Slim Agent Integration Template

Agents should reference this skill instead of duplicating memory code:

```markdown
## Memory Configuration (uses agent-memory-skills)

**Collections**:
- Global: `agent_{name}_improvements`, `agent_{name}_evaluations`, `agent_{name}_performance`
- Project: `agent_{name}_project_{hash}_improvements` (if project-specific learning)

**Quality Criteria** (agent-specific):
- [criterion_1]: weight X%
- [criterion_2]: weight Y%
- [criterion_3]: weight Z%

**Insight Categories** (agent-specific):
- [category_1]: Description of when this applies
- [category_2]: Description of when this applies

**Memory Workflow**:
1. **Phase 0.5 (Before Task)**: Retrieve relevant improvements
   - Call: `retrieveWithScope(agentName, taskDescription)`
   - Apply retrieved patterns to current task

2. **Phase N.5 (After Task)**: Self-evaluate and store
   - Assess quality using agent-specific criteria
   - Extract insights with agent-specific categories
   - Store improvements if quality ≥ 70
   - Update usage statistics for retrieved improvements
```

### Example: Slim Code-Finder Memory Section

```markdown
## Memory Configuration (uses agent-memory-skills)

**Collections**: `agent_code_finder_improvements`, `agent_code_finder_evaluations`

**Quality Criteria**:
- Result accuracy: 30%
- Search confidence: 25%
- Strategy completeness: 20%
- Search efficiency: 15%
- Coverage assessment: 10%

**Insight Categories**:
- `search_strategy`: Effective search patterns for code types
- `file_patterns`: File naming/location patterns that work
- `naming_conventions`: Casing and naming variants that help
- `query_optimization`: Query formulations that improve results

**Memory Workflow**:
- Phase 0.5: Retrieve search strategy improvements before search
- Phase 4.5: Evaluate search quality, store effective patterns
```

---

## Memory Consolidation Integration

Individual agent memories benefit from periodic consolidation by the **memory-consolidation-agent**. This section describes how agents interact with the consolidation system.

### Consolidation-Ready Metadata

When storing improvements, include metadata that enables consolidation:

```javascript
const improvementMetadata = {
  // Standard fields
  agent_name: agentName,
  category: insight.category,
  confidence: insight.confidence,
  created_at: timestamp,
  usage_count: 0,
  success_rate: null,

  // Consolidation-ready fields
  cross_validated: false,           // Set true when validated across agents
  source: 'self',                   // 'self' | 'system_principles' | 'transferred'
  original_id: null,                // If transferred from another agent
  consolidation_eligible: true,     // Can be used for schema formation
  context_tags: ['domain', 'tech'], // Help consolidation group related patterns
  deprecated: false,
  deprecated_reason: null
};
```

### Receiving Transferred Knowledge

Agents may receive improvements from the consolidation system. Handle these appropriately:

```javascript
async function retrieveWithTransfers(agentName, taskDescription) {
  const results = await mcp__chroma__query_documents({
    collection_name: `agent_${agentName}_improvements`,
    query_texts: [taskDescription],
    n_results: 10,
    where: { "deprecated": { "$ne": true } }
  });

  // Prioritize cross-validated and transferred improvements
  return results.ids[0]
    .map((id, idx) => ({
      id: id,
      improvement: results.documents[0][idx],
      metadata: results.metadatas[0][idx],
      relevance: 1 - results.distances[0][idx],
      // Boost score for cross-validated patterns
      priority: results.metadatas[0][idx].cross_validated ? 1.2 : 1.0
    }))
    .filter(item => item.relevance > 0.6)
    .sort((a, b) => (b.relevance * b.priority) - (a.relevance * a.priority));
}
```

### Consolidation Hooks

Agents should expose these hooks for the consolidation system:

```javascript
// Hook: Get all improvements for consolidation analysis
async function getConsolidatableImprovements(agentName) {
  return await mcp__chroma__get_documents({
    collection_name: `agent_${agentName}_improvements`,
    where: { "consolidation_eligible": true, "deprecated": { "$ne": true } },
    include: ["documents", "metadatas"]
  });
}

// Hook: Mark improvement as cross-validated
async function markCrossValidated(agentName, improvementId, validatingAgents) {
  const current = await mcp__chroma__get_documents({
    collection_name: `agent_${agentName}_improvements`,
    ids: [improvementId]
  });

  await mcp__chroma__update_documents({
    collection_name: `agent_${agentName}_improvements`,
    ids: [improvementId],
    metadatas: [{
      ...current.metadatas[0],
      cross_validated: true,
      validating_agents: validatingAgents.join(','),
      cross_validated_at: new Date().toISOString()
    }]
  });
}

// Hook: Receive transferred principle from consolidation
async function receiveTransferredPrinciple(agentName, principle, sourceMetadata) {
  await mcp__chroma__add_documents({
    collection_name: `agent_${agentName}_improvements`,
    documents: [principle],
    ids: [`transferred_${sourceMetadata.original_id}_${Date.now()}`],
    metadatas: [{
      agent_name: agentName,
      category: sourceMetadata.category,
      confidence: sourceMetadata.confidence * 0.9,  // Discount for transfer
      source: 'system_principles',
      original_id: sourceMetadata.original_id,
      cross_validated: true,
      transferred_at: new Date().toISOString(),
      usage_count: 0,
      success_rate: null,
      consolidation_eligible: false  // Don't re-consolidate transferred items
    }]
  });
}
```

### Consolidation Schedule

| Frequency | What Happens | Agent Impact |
|-----------|--------------|--------------|
| **Daily** | Conflict scan, anomaly detection | Flagged conflicts may need review |
| **Weekly** | Schema formation, knowledge transfer | May receive new transferred principles |
| **Monthly** | Full optimization, cleanup | Old improvements may be archived |

---

## Success Criteria

Agent memory system is working when:

- ✅ **Improvements Stored**: Agent learns from each task (10+ improvements/week)
- ✅ **Relevant Retrieval**: Retrieved improvements match current task (>80% relevance)
- ✅ **Success Rate Tracking**: Improvements update usage stats correctly
- ✅ **Performance Improving**: Quality trend positive over 30 days
- ✅ **Self-Evaluation**: Runs after every task completion
- ✅ **Deprecation Works**: Low-performing improvements marked deprecated
- ✅ **Promotion Works**: High-performing improvements boosted
- ✅ **No .md Modifications**: Static config unchanged, memory in ChromaDB

---

## Comparison: .md vs ChromaDB

| Requirement | Modify .md Files | ChromaDB Memory |
|-------------|-----------------|-----------------|
| Store learning | ❌ Manual editing | ✅ Automatic |
| Concurrent access | ❌ Race conditions | ✅ Safe |
| Semantic search | ❌ Keyword only | ✅ Vector similarity |
| Success tracking | ❌ Manual | ✅ Automatic stats |
| Rollback | ⚠️ Git history | ✅ Query by timestamp |
| A/B testing | ❌ Destructive | ✅ Clone collections |
| Human review | ✅ Git diffs | ⚠️ Export needed |
| Version control | ✅ Native | ⚠️ Manual |

**Recommendation**: Use **ChromaDB for dynamic memory**, **.md for static config**

---

**Version**: 1.0
**Created**: 2025-11-18
**Purpose**: Enable continuous agent self-improvement with ChromaDB memory
**Dependencies**: chromadb-integration-skills
**Applicable To**: All agents (research, development, trading, legal, etc.)
