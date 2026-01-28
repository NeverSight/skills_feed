---
name: knowledge-orchestrator
description: Intelligently coordinates obsidian-markdown, hierarchical-reasoning, and knowledge-graph skills through automatic skill selection, context-aware routing, and hybrid MCP integration. Use when tasks involve knowledge base construction, research synthesis, documentation generation, or learning workflows that could benefit from multi-skill composition. Activates automatically to evaluate whether specialized skills should handle the request.
---

# Knowledge Orchestrator

## Overview

The Knowledge Orchestrator is a meta-cognitive skill that automatically analyzes user requests and intelligently routes them to the most appropriate specialized skill(s): obsidian-markdown, hierarchical-reasoning, or knowledge-graph. It operates as a transparent cognitive layer that enhances task execution through:

- **Automatic skill selection** based on semantic task analysis
- **Context-aware routing** using confidence-weighted decision logic
- **Workflow composition** for complex multi-skill tasks
- **Hybrid MCP integration** that enriches context before delegation
- **Quality validation** ensuring outputs meet standards

The orchestrator eliminates the need for manual skill selection while enabling sophisticated multi-skill workflows that produce higher-quality outputs than individual skills alone.

## Core Philosophy

The orchestrator operates at a **meta-tactical level**—above individual skill tactics but below user-facing strategy—serving as an intelligent dispatcher rather than a monolithic controller. It preserves skill autonomy (skills can still be invoked directly) while adding adaptive coordination that emerges from task analysis rather than rigid rules.

## Core Capabilities

### 1. Semantic Task Analysis

Extracts multi-dimensional features from user requests to enable intelligent routing:

**Feature Dimensions:**
- **Content Type**: code, structured_data, prose, mixed
- **Artifact Type**: file, knowledge, analysis, visualization
- **Complexity Score**: 0.0-1.0 based on decomposition needs, domain breadth, abstraction level
- **Creation Signals**: creates_md_file, requires_extraction, requires_decomposition
- **Domain Signals**: obsidian_keywords, reasoning_keywords, graph_keywords

**Example Analysis:**
```
User: "Create a comprehensive note about neural networks with entity relationships"

Analysis:
  content_type: prose
  artifact_type: file + knowledge
  complexity_score: 0.75 (multi-step, requires structure)
  creates_md_file: true (keyword "note")
  requires_extraction: true (keyword "entity relationships")
  obsidian_signals: 1 ("note")
  graph_signals: 2 ("entity", "relationships")

Selection: Multi-skill workflow (research→structure→document pattern)
```

**Keyword Catalogs:**
- **Obsidian**: vault, wikilink, dataview, frontmatter, callout, note, .md, mermaid, templater
- **Reasoning**: analyze, strategic, tactical, decompose, converge, multi-level, planning
- **Graph**: entities, relationships, extract, ontology, schema, knowledge graph, mapping

### 2. Skill Selection

Maps task features to skill(s) using confidence-weighted decision logic with priority tiers:

**Confidence Thresholds:**
- **0.90-1.0**: Execute immediately (high confidence)
- **0.70-0.89**: Execute with notification about selection reasoning
- **0.50-0.69**: Present options to user for confirmation
- **<0.50**: Ask user to specify skill or provide more context

**Decision Priority Order:**

1. **Explicit Triggers (0.90-1.0 confidence)**
   - Creates .md file → obsidian-markdown (0.95)
   - Contains 3+ Obsidian keywords → obsidian-markdown (0.92)
   - Requires extraction + non-code content → knowledge-graph (0.90)
   - Contains 2+ graph keywords → knowledge-graph (0.88)
   - Complexity > 0.7 + requires decomposition → hierarchical-reasoning (0.90)
   - Contains 3+ reasoning keywords → hierarchical-reasoning (0.88)

2. **Implicit Triggers (0.70-0.89 confidence)**
   - Artifact type = knowledge (no explicit extraction) → knowledge-graph (0.75)
   - Complexity > 0.5 + artifact = analysis → hierarchical-reasoning (0.72)
   - Artifact = file + content = prose → obsidian-markdown (0.70)

3. **Workflow Detection**
   - Multiple candidates → check workflow pattern library
   - Match found → route to workflow coordinator

4. **Tiebreaker Logic**
   - Single candidate → execute that skill
   - Multiple candidates without workflow → select highest confidence
   - Zero candidates → ask user for clarification

**Decision Tree Reference:** See `references/decision_logic.md` for complete rules and examples

### 3. Workflow Coordination

Composes multi-skill workflows for complex tasks using canonical patterns:

**Pattern 1: Research → Structure → Document**
```yaml
description: "Complex topic research → structured documentation"
trigger_conditions:
  - complexity_score > 0.7
  - artifact_type == file
  - requires_decomposition == true

sequence:
  1. hierarchical-reasoning:
     purpose: "Strategic decomposition of topic"
     input: user_request
     output: strategic_insights

  2. knowledge-graph:
     purpose: "Extract entities/relationships from insights"
     input: strategic_insights.operational_output
     output: knowledge_structure

  3. obsidian-markdown:
     purpose: "Format as Obsidian note"
     input:
       content: knowledge_structure
       template: moc-template
       frontmatter:
         tags: knowledge_structure.entity_types
         related: knowledge_structure.entity_names
     output: final_note
```

**Pattern 2: Extract → Validate → Format**
```yaml
description: "Process unstructured text → validated knowledge → Obsidian note"
trigger_conditions:
  - artifact_type == file
  - requires_extraction == true
  - content_type == prose

sequence:
  1. knowledge-graph:
     purpose: "Extract entities and relationships"
     input: user_request.source_text
     output: raw_graph

  2. hierarchical-reasoning:
     purpose: "Validate graph coherence and completeness"
     input:
       problem: "Assess quality of extracted knowledge graph"
       context: raw_graph
     output: validation_assessment

  3. obsidian-markdown:
     purpose: "Create structured note with wikilinks"
     input:
       entities: raw_graph.entities
       relationships: raw_graph.relationships
       template: note-template
     output: final_note
```

**Pattern 3: Analyze → Graph → Visualize**
```yaml
description: "Complex system analysis → knowledge graph → visualization"
trigger_conditions:
  - complexity_score > 0.6
  - requires_decomposition == true
  - requires_extraction == true

sequence:
  1. hierarchical-reasoning:
     purpose: "Decompose system into components"
     input: user_request
     output: system_decomposition

  2. knowledge-graph:
     purpose: "Map components as graph"
     input: system_decomposition
     output: system_graph

  3. obsidian-markdown:
     purpose: "Visualize with Mermaid diagram"
     input:
       graph: system_graph
       diagram_type: mermaid_graph
       template: note-template
     output: visual_doc
```

**Workflow Pattern Reference:** See `references/workflow_patterns.md` for additional patterns and customization

### 4. Context Enrichment

Gathers relevant context via MCP tools before skill delegation using a hybrid approach:

**Obsidian-Markdown Enrichment:**
- Analyze vault conventions (if accessible)
- Select appropriate template based on note type
- Load relevant reference documentation
- Gather example notes of similar type

**Hierarchical-Reasoning Enrichment:**
- Identify constraints from task features
- Define success criteria based on complexity/domain
- Set convergence parameters (thresholds, cycle counts)
- Gather domain-specific examples

**Knowledge-Graph Enrichment:**
- Load domain ontology (core_ontology.md or coding_domain.md)
- Search for similar extraction examples
- Set confidence thresholds based on complexity
- Retrieve relevant schemas

**MCP Integration Reference:** See `references/mcp_integration.md` for tool usage patterns

### 5. Output Validation

Ensures skill outputs meet quality standards before returning to user:

**Obsidian-Markdown Validation:**
- Valid YAML frontmatter present
- Wikilinks used for internal notes (not markdown links)
- Callout syntax correct
- Tables properly formatted
- Code blocks have language tags

**Hierarchical-Reasoning Validation:**
- Convergence score ≥ 0.85
- All three levels present (strategic, tactical, operational)
- Average confidence ≥ 0.7
- Reasoning trace available if requested

**Knowledge-Graph Validation:**
- Minimum entity count (≥3 for meaningful graphs)
- Minimum relationship count (≥2 for connectivity)
- Provenance coverage (all entities have source attribution)
- Confidence scores present
- No broken references

**Quality Thresholds:**
- Overall quality score ≥ 0.6 to pass validation
- If validation fails, trigger refinement or notify user
- Issues reported with actionable remediation steps

**Validation Reference:** See `references/validation_criteria.md` for complete checklists

## Integration Points

The orchestrator bridges outputs between skills through automatic transformations:

**Knowledge Graph → Obsidian**
- Entities → `[[wikilinks]]` with proper formatting
- Relationships → Mermaid diagram syntax
- Confidence scores → Frontmatter metadata
- Provenance → Source attribution in frontmatter

**Hierarchical Reasoning → Knowledge Graph**
- Strategic insights → Extraction focus areas
- Operational details → Entity candidates
- Tactical structure → Relationship organization
- Convergence metrics → Validation criteria

**Hierarchical Reasoning → Obsidian**
- Strategic level → H2 headings
- Tactical level → H3 headings
- Operational level → H4 headings / detailed content
- Confidence scores → Callout annotations

**Integration Reference:** See `references/integration_mappings.md` for transformation specifications

## Usage Patterns

### Automatic Activation (Recommended)

The orchestrator evaluates every request to determine if specialized skills should handle it:

```
User: "Create a note about microservices architecture with key concepts and relationships"

Orchestrator Analysis:
✓ Detected: creates_md_file (keyword "note")
✓ Detected: requires_extraction (keywords "concepts", "relationships")
✓ Complexity score: 0.75 (multi-step analysis + structure + formatting)
✓ Pattern match: Research → Structure → Document

Execution:
1. [hierarchical-reasoning] Decompose microservices architecture
2. [knowledge-graph] Extract entities (concepts, patterns, technologies)
3. [obsidian-markdown] Format as MOC with wikilinks + mermaid diagram

Result: Comprehensive Obsidian note with strategic insights, linked entities, and visual architecture diagram
```

### Manual Override

Users can explicitly request specific skills or bypass orchestrator:

```
User: "Use hierarchical-reasoning only to analyze this problem"
→ Orchestrator delegates directly to hierarchical-reasoning without workflow composition

User: "Don't use the orchestrator, just create a simple markdown note"
→ Orchestrator deactivates, standard markdown creation proceeds
```

### Debugging Mode

Request orchestrator to explain its decision-making:

```
User: "Explain why you selected those skills"
→ Orchestrator outputs:
   • Task features extracted
   • Confidence scores calculated
   • Decision logic applied
   • Workflow pattern matched (if multi-skill)
```

## Configuration

The orchestrator supports optional configuration tuning:

**Confidence Thresholds** (adjust selection sensitivity):
```yaml
execute_immediately: 0.90  # High confidence threshold
execute_with_note: 0.70    # Medium confidence threshold
ask_user: 0.50             # Low confidence threshold
```

**Workflow Detection** (enable/disable pattern matching):
```yaml
workflow_patterns_enabled: true
custom_patterns_path: /path/to/custom/patterns.yaml
```

**Context Enrichment** (control MCP usage):
```yaml
mcp_enrichment: hybrid  # Options: hybrid, full, minimal, none
max_enrichment_tools: 3
```

**Validation Strictness** (adjust quality requirements):
```yaml
quality_threshold: 0.6  # Minimum score to pass (0.0-1.0)
strict_mode: false      # Require all checks to pass
```

## Advanced Features

### Learning from Patterns

The orchestrator can adapt based on user preferences:

- Track which skills user manually selects after seeing orchestrator suggestions
- Adjust confidence weights for future similar tasks
- Learn user-specific workflow preferences

### Recursive Refinement

If validation fails or quality is low:

1. Analyze what went wrong (missing info, low confidence, structural issues)
2. Determine if re-running with enriched context would help
3. Optionally loop workflow with additional constraints

### Skill Extensibility

The orchestrator can be extended to coordinate additional skills:

1. Add new skill to task analyzer keyword catalog
2. Define trigger conditions and confidence scoring
3. Map integration points (how skill outputs transform to other skill inputs)
4. Add validation criteria for new skill's outputs

See `references/extending_orchestrator.md` for extension guide

## Resources

This skill includes comprehensive reference documentation:

### references/

- **decision_logic.md** - Complete decision rules, examples, and edge cases
- **workflow_patterns.md** - Canonical patterns with customization options
- **integration_mappings.md** - Transformation specifications between skills
- **validation_criteria.md** - Quality checklists for each skill
- **mcp_integration.md** - MCP tool usage patterns and best practices
- **extending_orchestrator.md** - Guide for adding new skills to orchestration

### scripts/

- **task_classifier.py** - Standalone task feature extraction utility
- **skill_selector.py** - Test skill selection logic on sample inputs
- **validate_workflow.py** - Validate custom workflow pattern definitions

## Skill Interaction Examples

### Example 1: Knowledge Base Construction

```
User: "Help me build a knowledge base about distributed systems"

Orchestrator:
  Task Analysis: complexity=0.85, artifact=knowledge+file, requires_decomposition=true
  Selection: Multi-skill workflow (Research → Structure → Document)

Execution:
  1. Hierarchical-reasoning decomposes distributed systems into strategic themes
  2. Knowledge-graph extracts key entities (CAP theorem, consensus algorithms, etc.)
  3. Obsidian-markdown creates MOC with wikilinks and concept map

Output: Structured Obsidian vault entry with linked concepts and visual diagrams
```

### Example 2: Research Synthesis

```
User: "Analyze this research paper and create a structured summary"

Orchestrator:
  Task Analysis: complexity=0.70, artifact=file, requires_extraction=true
  Selection: Multi-skill workflow (Extract → Validate → Format)

Execution:
  1. Knowledge-graph extracts authors, methods, findings, citations
  2. Hierarchical-reasoning validates coherence and completeness
  3. Obsidian-markdown formats with proper citations and structure

Output: Well-structured note with extracted entities, validated insights, proper formatting
```

### Example 3: Learning Workflow

```
User: "I'm learning about GraphQL - help me organize what I'm learning"

Orchestrator:
  Task Analysis: complexity=0.60, artifact=file, domain=technical_learning
  Selection: Single skill with enhancement (obsidian-markdown + light graph extraction)

Execution:
  1. Identify GraphQL concepts to track
  2. Create learning note template with progress tracking
  3. Suggest related concept links

Output: Learning-optimized note with concept relationships and tracking structure
```

## Best Practices

1. **Trust automatic selection** - The orchestrator analyzes task features systematically
2. **Provide context** - More detail in requests → better skill selection and context enrichment
3. **Use explain mode** - When selection seems wrong, ask orchestrator to explain reasoning
4. **Extend thoughtfully** - Only add new skills when they provide unique capabilities
5. **Validate outputs** - Review quality scores and validation results for critical work
6. **Iterate patterns** - Custom workflow patterns can be added for domain-specific needs

## Limitations

- **Learning curve**: Understanding orchestrator decision logic takes time
- **Overhead**: Task analysis adds token usage (offset by better skill selection)
- **Skill dependency**: Requires obsidian-markdown, hierarchical-reasoning, knowledge-graph skills
- **Context limits**: Very large workflows may approach context window constraints
- **Manual better sometimes**: Simple tasks may not benefit from orchestration

## When Not to Use

- **Simple single-skill tasks**: "Fix this typo" doesn't need orchestration
- **Explicit skill preference**: User states "only use X skill"
- **Time-critical tasks**: Analysis overhead may not be worthwhile
- **Highly specialized domains**: Custom skills may be more appropriate than orchestration

---

**Core Philosophy**: The orchestrator emerges sophisticated capabilities from simple skill coordination, enabling workflows greater than the sum of their parts while preserving the autonomy and specialization that makes individual skills valuable.
