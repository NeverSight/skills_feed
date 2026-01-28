---
name: infranodus-orchestrator
description: Orchestrates complex knowledge graph analysis workflows using InfraNodus MCP tools integrated with hierarchical-reasoning, knowledge-graph, and obsidian-markdown skills. Use when tasks involve text network analysis, content gap detection, research question generation, SEO optimization, comparative text analysis, or Google search intelligence requiring multi-step analytical workflows with local documentation.
---

# InfraNodus Orchestrator

## Overview

The InfraNodus Orchestrator is a meta-cognitive skill that intelligently coordinates cloud-based graph analytics (via InfraNodus MCP tools) with local knowledge management skills to enable sophisticated research, content analysis, and knowledge discovery workflows. It bridges the gap between powerful cloud-based text network analysis and local knowledge preservation through adaptive workflow routing.

**Core Philosophy**: InfraNodus provides world-class graph analytics and gap detection in the cloud, while local skills (hierarchical-reasoning, knowledge-graph, obsidian-markdown) handle strategic planning, local storage, and documentation. The orchestrator seamlessly integrates both worlds.

## When to Use This Skill

Use this skill when tasks involve:

- **Knowledge graph generation** from text with topical clustering and gap analysis
- **Research question generation** based on structural gaps in discourse
- **Content gap analysis** to identify missing connections and underexplored topics
- **SEO optimization** through search demand-supply gap analysis
- **Comparative text analysis** finding overlaps and differences between documents
- **Google search intelligence** analyzing search results and related queries
- **Topic development** with latent topic identification and conceptual bridge building
- **Iterative research workflows** requiring strategic planning + analytics + documentation

**Trigger Keywords**: knowledge graph, content gaps, research questions, topical clusters, InfraNodus, gap analysis, SEO optimization, comparative analysis, search intelligence, topic development

## Core Capabilities

### 1. Adaptive Workflow Routing

Automatically analyzes user requests to select the optimal workflow pattern based on task complexity, content type, and analytical requirements.

**Routing Decision Framework:**

```yaml
Simple Graph Generation (confidence 0.90+):
  - Single text input, basic analysis request
  - Direct: mcp__infranodus__generate_knowledge_graph

Deep Research & Gap Analysis (confidence 0.85+):
  - Complex analysis requiring gaps + research questions
  - Workflow Pattern 1 (see below)

SEO Content Optimization (confidence 0.85+):
  - Contains SEO/optimization keywords
  - Workflow Pattern 2 (see below)

Comparative Text Analysis (confidence 0.80+):
  - Multiple texts requiring comparison
  - Workflow Pattern 3 (see below)

Iterative Topic Development (confidence 0.75+):
  - Requires topic refinement and development
  - Workflow Pattern 4 (see below)

Google Search Intelligence (confidence 0.85+):
  - Search analysis keywords present
  - Workflow Pattern 5 (see below)
```

**Confidence Calculation Factors:**
- Keyword presence and frequency (30%)
- Task complexity assessment (25%)
- Artifact type requirements (20%)
- Integration needs (15%)
- User history patterns (10%)

### 2. Five Canonical Workflow Patterns

The orchestrator implements five battle-tested workflow patterns for complex analytical tasks:

#### Pattern 1: Deep Research & Gap Analysis

**Purpose**: Comprehensive knowledge exploration with strategic decomposition, gap detection, and research question generation.

**Trigger Conditions**:
- `complexity_score > 0.7`
- `requires_gaps = true`
- `artifact_type = analysis`
- Keywords: "research", "gaps", "analysis", "comprehensive", "explore"

**Workflow Sequence**:

```yaml
1. hierarchical-reasoning:
   purpose: Strategic decomposition of research topic
   input: user_request
   output: strategic_insights (context boundaries, key themes, scope definition)

2. mcp__infranodus__generate_knowledge_graph:
   purpose: Generate text network graph with topical clusters
   input: user_text + strategic_context
   parameters:
     modifyAnalyzedText: "detectEntities"  # Better entity recognition
     includeStatements: false  # Optimize response size
   output: graph_structure + topical_clusters

3. mcp__infranodus__generate_content_gaps:
   purpose: Identify missing connections and structural gaps
   input: analyzed_text
   output: content_gaps (underexplored areas, missing connections)

4. mcp__infranodus__generate_research_questions:
   purpose: Create investigation prompts from gaps
   input: analyzed_text
   parameters:
     useSeveralGaps: true  # Multiple question sets
     gapDepth: 0  # Primary gaps
   output: research_questions

5. knowledge-graph:
   purpose: Convert InfraNodus output to local graph representation
   input: graph_structure + entities + relationships
   output: local_graph.json (with provenance and confidence scores)

6. obsidian-markdown:
   purpose: Document findings with research questions as MOC
   input:
     content: research_questions + content_gaps + topical_clusters
     template: research-moc-template
     frontmatter:
       tags: [research, knowledge-graph, infranodus]
       clusters: topical_cluster_names
       gaps: content_gap_identifiers
   output: research_documentation.md
```

**Expected Outcomes**:
- Strategic understanding of topic landscape
- Topical clusters with main themes identified
- Specific content gaps documented
- Actionable research questions generated
- Local knowledge graph preserved
- Comprehensive Obsidian documentation

#### Pattern 2: SEO Content Optimization

**Purpose**: Analyze content for search optimization by comparing against search results and user queries to identify opportunities.

**Trigger Conditions**:
- `contains_seo_keywords = true`
- `requires_optimization = true`
- Keywords: "SEO", "optimize", "search", "ranking", "content strategy", "keywords"

**Workflow Sequence**:

```yaml
1. mcp__infranodus__generate_topical_clusters:
   purpose: Extract topic groups and keyword clusters from content
   input: content_text
   output: topical_clusters (main themes, keyword groups)

2. mcp__infranodus__generate_seo_report:
   purpose: Comprehensive SEO analysis with gap detection
   input: content_text
   parameters:
     importLanguage: "EN"  # Adjust based on content
     importCountry: "US"   # Adjust based on target market
   output: seo_report (6-stage progress tracking)
   note: Long-running operation with progress notifications

3. mcp__infranodus__search_queries_vs_search_results:
   purpose: Identify search demand-supply gaps
   input: target_queries
   parameters:
     queries: [derived from topical clusters]
     importLanguage: "EN"
     importCountry: "US"
   output: demand_supply_gaps

4. hierarchical-reasoning:
   purpose: Strategic content recommendations
   input:
     context: seo_report + demand_supply_gaps + topical_clusters
     problem: "Synthesize SEO optimization strategy"
   output: strategic_recommendations

5. obsidian-markdown:
   purpose: Create SEO strategy document
   input:
     content: strategic_recommendations + seo_report
     template: seo-strategy-template
     frontmatter:
       tags: [seo, content-strategy, optimization]
       target_keywords: identified_keywords
       gaps: opportunity_areas
   output: seo_strategy.md
```

**Expected Outcomes**:
- Topical cluster analysis of existing content
- Comprehensive SEO gap report
- Search demand-supply gap identification
- Strategic optimization recommendations
- Actionable SEO strategy document

#### Pattern 3: Comparative Text Analysis

**Purpose**: Find similarities and differences between multiple texts for synthesis and strategic insights.

**Trigger Conditions**:
- `multiple_texts = true`
- `requires_comparison = true`
- Keywords: "compare", "difference", "similarity", "overlap", "contrast"

**Workflow Sequence**:

```yaml
1. mcp__infranodus__overlap_between_texts:
   purpose: Find shared concepts and common themes
   input:
     contexts: [
       {text: text1, modifyAnalyzedText: "detectEntities"},
       {text: text2, modifyAnalyzedText: "detectEntities"},
       ...
     ]
   parameters:
     includeGraph: true  # Get structural overlap
   output: overlap_graph (shared concepts, common relationships)

2. mcp__infranodus__difference_between_texts:
   purpose: Identify unique content in target text vs references
   input:
     contexts: [
       {text: target_text},  # First text is analyzed for missing parts
       {text: reference_text1},
       {text: reference_text2},
       ...
     ]
   output: difference_graph (unique content, missing elements)

3. knowledge-graph:
   purpose: Synthesize comparative graph
   input:
     overlap_entities: from overlap_graph
     difference_entities: from difference_graph
   operations:
     - Merge overlap + difference graphs
     - Tag entities with source attribution
     - Calculate comparative metrics
   output: comparative_graph.json

4. obsidian-markdown:
   purpose: Document comparison with visual diagrams
   input:
     content: comparative_insights
     diagrams:
       - type: mermaid_venn
         data: overlap visualization
       - type: mermaid_graph
         data: difference relationships
     template: comparison-template
     frontmatter:
       tags: [comparison, analysis, synthesis]
       compared_texts: text_identifiers
   output: comparative_analysis.md
```

**Expected Outcomes**:
- Overlap graph showing shared concepts
- Difference graph highlighting unique content
- Synthesized comparative knowledge graph
- Visual diagrams (Venn diagrams, relationship graphs)
- Comprehensive comparison documentation

#### Pattern 4: Iterative Topic Development

**Purpose**: Develop underexplored topics and build conceptual bridges to broader discourse.

**Trigger Conditions**:
- `requires_iteration = true`
- `complexity_score > 0.6`
- Keywords: "develop", "iterate", "refine", "expand", "deepen", "elaborate"

**Workflow Sequence**:

```yaml
1. mcp__infranodus__generate_knowledge_graph:
   purpose: Generate initial topic graph
   input: initial_content
   parameters:
     modifyAnalyzedText: "detectEntities"
   output: initial_graph

2. mcp__infranodus__develop_latent_topics:
   purpose: Identify underdeveloped topics requiring expansion
   input: analyzed_text
   parameters:
     modelToUse: "gpt-4o"  # High-quality analysis
   output: latent_topics (underdeveloped areas, expansion opportunities)

3. mcp__infranodus__develop_conceptual_bridges:
   purpose: Connect topic to broader discourse
   input: analyzed_text
   parameters:
     modelToUse: "gpt-4o"
   output: conceptual_bridges (connection opportunities, discourse links)

4. mcp__infranodus__develop_text_tool:
   purpose: Comprehensive development workflow with progress tracking
   input: analyzed_text
   parameters:
     modelToUse: "gpt-4o"
     useSeveralGaps: true
     extendedIdeationMode: false  # Questions first, ideas if needed
   output:
     - research_questions
     - latent_topics_analysis
     - content_gaps
   note: Multi-step workflow with progress tracking

5. hierarchical-reasoning:
   purpose: Validate and refine insights
   input:
     context: latent_topics + conceptual_bridges + research_questions
     problem: "Synthesize coherent topic development strategy"
   output: refined_development_strategy

6. obsidian-markdown:
   purpose: Create refined topic documentation
   input:
     content: refined_development_strategy + latent_topics + bridges
     template: topic-development-template
     frontmatter:
       tags: [topic-development, research, iteration]
       latent_topics: identified_topics
       bridges: conceptual_connections
   output: topic_development.md
```

**Expected Outcomes**:
- Initial knowledge graph of topic
- Identified latent/underdeveloped topics
- Conceptual bridges to broader discourse
- Comprehensive research questions
- Strategic development recommendations
- Refined topic documentation

#### Pattern 5: Google Search Intelligence

**Purpose**: Analyze search landscape to understand topical trends, user queries, and content opportunities.

**Trigger Conditions**:
- `contains_search_keywords = true`
- `requires_search_analysis = true`
- Keywords: "Google", "search", "queries", "trends", "SERP", "search results"

**Workflow Sequence**:

```yaml
1. mcp__infranodus__analyze_google_search_results:
   purpose: Analyze search results landscape
   input:
     queries: target_search_queries
   parameters:
     importLanguage: "EN"
     importCountry: "US"
     showGraphOnly: true  # Focus on graph structure
   output: search_results_graph (topical clusters from results)

2. mcp__infranodus__analyze_related_search_queries:
   purpose: Extract topical clusters from related searches
   input:
     queries: target_search_queries
   parameters:
     importLanguage: "EN"
     importCountry: "US"
     keywordsSource: "related"  # or "adwords" for broader range
     showGraphOnly: true
   output: related_queries_graph (query clustering, search patterns)

3. knowledge-graph:
   purpose: Create local graph of search insights
   input:
     search_entities: from search_results_graph
     query_entities: from related_queries_graph
   operations:
     - Merge search + query graphs
     - Identify high-opportunity topics
     - Calculate search intent clusters
   output: search_intelligence_graph.json

4. obsidian-markdown:
   purpose: Document search intelligence findings
   input:
     content: search_insights + topical_clusters + opportunities
     diagrams:
       - type: mermaid_graph
         data: search landscape visualization
       - type: table
         data: keyword opportunities matrix
     template: search-intelligence-template
     frontmatter:
       tags: [search-intelligence, seo, research]
       queries: analyzed_queries
       clusters: topical_clusters
   output: search_intelligence.md
```

**Expected Outcomes**:
- Search results topical graph
- Related queries cluster analysis
- Search intent identification
- Content opportunity matrix
- Local search intelligence graph
- Comprehensive search documentation

### 3. Integration with Existing Skills

The orchestrator seamlessly integrates with four existing skills:

#### knowledge-orchestrator Integration

The InfraNodus orchestrator operates as a **specialized meta-layer** above the knowledge-orchestrator:

**Delegation Pattern**:
```yaml
InfraNodus-specific tasks:
  - InfraNodus orchestrator handles directly
  - Uses InfraNodus MCP tools + coordinates with other skills

Standard knowledge management:
  - Delegate to knowledge-orchestrator
  - Let knowledge-orchestrator route to obsidian-markdown, knowledge-graph, etc.

Mixed workflows:
  - InfraNodus orchestrator coordinates high-level workflow
  - Delegates specific sub-tasks to knowledge-orchestrator
```

**Example Decision Logic**:
```
User: "Create a comprehensive note about AI with entity relationships"
→ knowledge-orchestrator handles (standard knowledge base construction)

User: "Analyze this text for content gaps and generate research questions"
→ InfraNodus orchestrator handles (InfraNodus-specific gap analysis)

User: "Analyze gaps in my AI notes and create refined documentation"
→ InfraNodus orchestrator coordinates InfraNodus analysis
→ Delegates documentation to knowledge-orchestrator
```

#### hierarchical-reasoning Integration

**Role**: Strategic planning and decomposition BEFORE cloud-based analysis

**Integration Points**:
- **Pre-analysis**: Decompose complex topics before InfraNodus processing
- **Post-analysis**: Validate InfraNodus insights and synthesize recommendations
- **Quality control**: Assess coherence and completeness of extracted knowledge

**Example Usage**:
```yaml
Pattern 1 Step 1:
  skill: hierarchical-reasoning
  input: "Analyze distributed systems architecture"
  output:
    strategic: "Core themes: consistency, availability, partition tolerance"
    tactical: "Sub-topics: consensus algorithms, replication, data partitioning"
    operational: "Specific concepts to extract: Paxos, Raft, CAP theorem"

  → This output guides InfraNodus analysis in Step 2
```

#### knowledge-graph Integration

**Role**: Local preservation of InfraNodus cloud analytics

**Integration Points**:
- **Format conversion**: InfraNodus graph → local JSON graph format
- **Provenance tracking**: Add source attribution and timestamps
- **Confidence scoring**: Map InfraNodus metrics to local confidence scores
- **Storage**: Persist graphs locally for long-term knowledge management

**Transformation Mapping**:
```yaml
InfraNodus Output → Local Knowledge Graph:

  nodes (concepts):
    - Extract from InfraNodus topical clusters
    - Create entity objects with:
      id: normalized_concept_name
      type: "Concept" or domain-specific type
      name: concept label
      confidence: derived from InfraNodus centrality
      provenance:
        source: "InfraNodus"
        graph_name: original_graph_identifier
        extraction_date: ISO timestamp
      properties:
        cluster: topical_cluster_membership
        centrality: node importance score

  edges (relationships):
    - Extract from InfraNodus co-occurrence connections
    - Create relationship objects with:
      source: entity_id_1
      target: entity_id_2
      type: "RELATED_TO" or "CO_OCCURS_WITH"
      confidence: derived from edge weight
      properties:
        weight: co-occurrence strength
        context: semantic relationship type
```

#### obsidian-markdown Integration

**Role**: Documentation and knowledge preservation

**Integration Points**:
- **Research documentation**: Create MOCs from research questions and gaps
- **SEO strategy docs**: Format SEO reports as actionable strategy notes
- **Comparison reports**: Visualize comparative analysis with Mermaid diagrams
- **Topic development**: Document iterative refinement process

**Template Usage**:
```yaml
research-moc-template:
  frontmatter:
    tags: [research, knowledge-graph, infranodus]
    clusters: ${topical_clusters}
    gaps: ${identified_gaps}
    date: ${timestamp}
  structure:
    - h1: Topic Overview
    - h2: Topical Clusters (from InfraNodus)
    - h2: Content Gaps (callout: warning)
    - h2: Research Questions (task list)
    - h2: Key Concepts (wikilinks to entities)
    - h2: Visual Map (Mermaid graph from InfraNodus)

seo-strategy-template:
  frontmatter:
    tags: [seo, content-strategy, optimization]
    target_keywords: ${keywords}
    opportunities: ${gaps}
  structure:
    - h1: SEO Strategy
    - h2: Current Topical Clusters
    - h2: Search Demand-Supply Gaps (table)
    - h2: Optimization Recommendations
    - h2: Content Opportunities (prioritized list)
    - h2: Implementation Roadmap
```

### 4. InfraNodus MCP Tools Reference

The orchestrator uses 21+ InfraNodus MCP tools. Key tools organized by category:

#### Core Analysis Tools

**generate_knowledge_graph**
```yaml
purpose: Convert text into visual knowledge graphs
parameters:
  text: string (required) - Source material
  includeStatements: boolean - Retain original excerpts
  modifyAnalyzedText: "none" | "detectEntities" | "extractEntitiesOnly"
output: graph structure + topical clusters + main concepts
best_practice: Use detectEntities for cleaner graph structures
```

**analyze_existing_graph_by_name**
```yaml
purpose: Retrieve and analyze previously saved InfraNodus graphs
parameters:
  graphName: string (required) - Graph identifier
  includeStatements: boolean - Include source statements
  includeGraphSummary: boolean - Add structural overview
output: graph analysis + topical clusters + optional summary
use_case: Iterate on previously created graphs
```

**generate_content_gaps**
```yaml
purpose: Identify missing connections and underexplored areas
parameters:
  text: string (required) - Material for gap analysis
output: content gaps + missing connections + structural holes
best_practice: Chain after generate_knowledge_graph
```

#### Advanced Analysis Tools

**generate_topical_clusters**
```yaml
purpose: Extract topic groups and keyword clusters
parameters:
  text: string (required)
output: topic groups + keyword clusters + themes
use_case: Content organization, SEO topic identification
```

**generate_research_questions**
```yaml
purpose: Create investigation prompts based on gaps
parameters:
  text: string (required)
  useSeveralGaps: boolean - Multiple question sets
  gapDepth: number - Gap hierarchy level (0 = primary)
  modelToUse: "gpt-4o" | "gpt-4o-mini" | others
output: research questions + gap analysis
best_practice: Use after gap detection for focused questions
```

**generate_research_ideas**
```yaml
purpose: Generate innovative ideas from content gaps
parameters:
  text: string (required)
  useSeveralGaps: boolean
  gapDepth: number
  modelToUse: string
output: research ideas + innovation opportunities
use_case: Ideation and exploration phase
```

**develop_text_tool**
```yaml
purpose: Comprehensive workflow with progress tracking
parameters:
  text: string (required)
  useSeveralGaps: boolean
  extendedIdeationMode: boolean - Ideas instead of questions
  modelToUse: string
output: research questions + latent topics + gaps
note: Multi-step workflow with 6+ progress checkpoints
```

#### SEO & Search Tools

**generate_seo_report**
```yaml
purpose: Comprehensive SEO optimization analysis
parameters:
  text: string (required) - Content to optimize
  importLanguage: "EN" | "DE" | "FR" | others
  importCountry: "US" | "GB" | "DE" | others
output: SEO gaps + optimization recommendations
note: Long-running with 6-stage progress tracking
```

**analyze_google_search_results**
```yaml
purpose: Analyze search results landscape
parameters:
  queries: array of strings (required)
  importLanguage: string
  importCountry: string
  showGraphOnly: boolean - Omit raw results
output: topical clusters from search results
use_case: Search landscape analysis
```

**analyze_related_search_queries**
```yaml
purpose: Extract topical clusters from related searches
parameters:
  queries: array of strings (required)
  keywordsSource: "related" | "adwords"
  importLanguage: string
  importCountry: string
  showGraphOnly: boolean
output: query clusters + search patterns
best_practice: Use "related" for focused, "adwords" for broad
```

**search_queries_vs_search_results**
```yaml
purpose: Find search demand-supply gaps
parameters:
  queries: array of strings (required)
  importLanguage: string
  importCountry: string
output: keyword combinations users search but don't find
use_case: Content opportunity identification
```

#### Comparative Analysis Tools

**overlap_between_texts**
```yaml
purpose: Find similarities across multiple documents
parameters:
  contexts: array of {text, modifyAnalyzedText}
  includeGraph: boolean - Include structural data
output: overlap graph + shared concepts
use_case: Finding common themes across documents
```

**difference_between_texts**
```yaml
purpose: Identify unique content in target vs references
parameters:
  contexts: array - FIRST is target, rest are references
  includeGraph: boolean
output: difference graph + unique content
best_practice: Order matters - first text is analyzed for gaps
```

#### Topic Development Tools

**develop_latent_topics**
```yaml
purpose: Identify underdeveloped topics
parameters:
  text: string (required)
  modelToUse: string
output: latent topics + development opportunities
use_case: Topic expansion and elaboration
```

**develop_conceptual_bridges**
```yaml
purpose: Connect content to broader discourse
parameters:
  text: string (required)
  modelToUse: string
output: conceptual bridges + discourse connections
use_case: Linking specialized topics to general knowledge
```

#### Graph Management Tools

**create_knowledge_graph**
```yaml
purpose: Generate and SAVE graph to InfraNodus account
parameters:
  graphName: string (required) - Unique identifier
  text: string (required)
  modifyAnalyzedText: string
output: saved graph + name + link for future use
best_practice: Use descriptive names for easy retrieval
```

**search** and **fetch**
```yaml
search:
  purpose: Find concepts in existing InfraNodus graphs
  parameters:
    query: string (required)
    contextNames: array - Graph names to search (empty = all)
  output: matching concepts + graph locations

fetch:
  purpose: Retrieve specific search result details
  parameters:
    id: string (required) - Format: username:graph:query
  output: detailed result information
```

### 5. Workflow Decision Logic

The orchestrator uses sophisticated decision logic to select workflows:

#### Task Feature Extraction

```yaml
Extract from user request:

  content_type:
    - single_text: One document/passage
    - multiple_texts: 2+ documents for comparison
    - search_queries: Google search terms
    - existing_graph: Reference to saved InfraNodus graph

  analysis_requirements:
    - basic_graph: Simple graph generation
    - gap_detection: Identify content gaps
    - research_questions: Generate investigation prompts
    - seo_optimization: Search optimization needs
    - topic_development: Expand/refine topics
    - comparative_analysis: Compare multiple texts

  complexity_score: 0.0-1.0
    factors:
      - Number of analysis steps required (0-0.3)
      - Integration needs across skills (0-0.3)
      - Strategic planning requirements (0-0.2)
      - Documentation complexity (0-0.2)

  keyword_signals:
    infranodus_specific: ["InfraNodus", "topical cluster", "content gap", "research question"]
    seo_keywords: ["SEO", "optimize", "search", "ranking", "keywords"]
    comparison_keywords: ["compare", "difference", "overlap", "similarity"]
    development_keywords: ["develop", "refine", "expand", "iterate"]
    search_keywords: ["Google", "search results", "queries", "SERP"]
```

#### Confidence Calculation

```yaml
Calculate confidence for each pattern:

  pattern_score = (
    keyword_match_score * 0.30 +
    complexity_alignment * 0.25 +
    artifact_type_match * 0.20 +
    integration_needs_match * 0.15 +
    user_history_factor * 0.10
  )

  Execute if pattern_score >= threshold:
    0.90+: Execute immediately (high confidence)
    0.70-0.89: Execute with explanation
    0.50-0.69: Present options to user
    < 0.50: Ask for clarification
```

#### Multi-Pattern Detection

```yaml
If multiple patterns score >= 0.70:

  check_workflow_composition:
    - Pattern 1 + Pattern 4: Research → Topic Development
    - Pattern 2 + Pattern 5: SEO → Search Intelligence
    - Pattern 3 + Pattern 1: Comparison → Deep Analysis

  if composition_makes_sense:
    execute_composed_workflow()
  else:
    select_highest_confidence_pattern()
```

### 6. Best Practices

#### Parameter Optimization

**modifyAnalyzedText Selection**:
```yaml
"detectEntities":
  - Use for cleaner graph structures
  - Better entity recognition
  - Recommended for most workflows

"extractEntitiesOnly":
  - Use for ontology creation
  - Pure entity extraction
  - Specialized use cases

"none":
  - Default processing
  - Preserves all word-level detail
```

**includeStatements Usage**:
```yaml
false (recommended):
  - Reduces response size
  - Faster processing
  - Use when source attribution not critical

true:
  - Includes original text excerpts
  - Enables provenance tracking
  - Use for academic/research work requiring citations
```

**Model Selection** (for AI-enhanced tools):
```yaml
"gpt-4o":
  - Highest quality analysis
  - Best for critical research questions
  - Use for strategic work

"gpt-4o-mini":
  - Faster processing
  - Good for iterative workflows
  - Cost-effective for exploration
```

#### Tool Chaining Strategy

**Optimal Chains**:
```yaml
Research Workflow:
  generate_knowledge_graph →
  generate_content_gaps →
  generate_research_questions

SEO Workflow:
  generate_topical_clusters →
  generate_seo_report →
  search_queries_vs_search_results

Topic Development:
  generate_knowledge_graph →
  develop_latent_topics →
  develop_conceptual_bridges
```

**Avoid Anti-Patterns**:
- ❌ Running gap detection without prior graph generation
- ❌ Using seo_report without topical cluster analysis
- ❌ Comparing texts without entity detection enabled
- ❌ Creating research questions from graphs without gap analysis

#### Progress Tracking

Long-running tools (seo_report, develop_text_tool) emit progress notifications:

```yaml
Progress Checkpoints:
  1. "Initializing analysis..." (0%)
  2. "Gathering search data..." (20%)
  3. "Analyzing topical structure..." (40%)
  4. "Detecting content gaps..." (60%)
  5. "Generating insights..." (80%)
  6. "Finalizing report..." (100%)

Best Practice:
  - Inform user when starting long operations
  - Show progress updates as they arrive
  - Provide estimated completion time if available
```

### 7. Error Handling & Troubleshooting

#### Common Issues

**Issue**: InfraNodus quota exhausted
```yaml
Error: API quota exceeded
Solution:
  - First 70 requests are quota-free
  - After exhaustion, requires API credentials
  - For Smithery integration, credentials auto-managed
  - For local deployment, configure INFRANODUS_API_KEY
```

**Issue**: Graph generation fails with large texts
```yaml
Error: Text too large or timeout
Solution:
  1. Use hierarchical-reasoning to chunk strategically
  2. Process in segments
  3. Merge resulting graphs using knowledge-graph skill
  4. Alternative: Use graph creation for persistent storage
```

**Issue**: Low-quality topical clusters
```yaml
Symptom: Weak or unclear clusters
Solution:
  1. Enable detectEntities parameter
  2. Ensure text has sufficient length (>500 words recommended)
  3. Check text coherence and topic focus
  4. Consider pre-processing with hierarchical decomposition
```

**Issue**: Research questions too broad/narrow
```yaml
Symptom: Questions don't match needed depth
Solution:
  1. Adjust gapDepth parameter (0 = primary, 1+ = deeper)
  2. Use useSeveralGaps for multiple question sets
  3. Switch to generate_research_ideas for broader ideation
  4. Try extendedIdeationMode in develop_text_tool
```

#### Validation Checklist

Before finalizing workflow outputs:

```yaml
✓ InfraNodus Analysis Quality:
  - Topical clusters are meaningful and distinct
  - Content gaps are specific and actionable
  - Research questions are investigable

✓ Local Knowledge Graph:
  - All entities have confidence scores
  - Provenance includes InfraNodus source
  - Relationships properly mapped from co-occurrences

✓ Obsidian Documentation:
  - Frontmatter complete with metadata
  - Wikilinks used for concept references
  - Mermaid diagrams render correctly
  - Research questions formatted as task lists

✓ Integration Coherence:
  - hierarchical-reasoning output informed InfraNodus analysis
  - InfraNodus insights preserved in local knowledge graph
  - Documentation captures full workflow findings
```

## Usage Examples

### Example 1: Deep Research on Quantum Computing

```
User: "I want to deeply research quantum computing. Help me identify
knowledge gaps and generate research questions."

Orchestrator Analysis:
  complexity_score: 0.85 (high - requires strategic decomposition)
  requires_gaps: true
  artifact_type: analysis + documentation
  pattern_match: Pattern 1 (Deep Research & Gap Analysis)
  confidence: 0.90

Execution:
  1. hierarchical-reasoning:
     Strategic level: "Quantum computing spans hardware, algorithms, applications"
     Tactical level: "Focus areas: qubit technologies, error correction, quantum algorithms"
     Operational: "Key concepts: superposition, entanglement, quantum gates"

  2. mcp__infranodus__generate_knowledge_graph:
     Input: Quantum computing overview text
     Output: Graph with clusters: [Hardware, Algorithms, Applications, Theory]

  3. mcp__infranodus__generate_content_gaps:
     Output: Gaps between [Hardware ↔ Algorithms], [Theory ↔ Applications]

  4. mcp__infranodus__generate_research_questions:
     Output:
       - "How do error correction algorithms impact qubit hardware design?"
       - "What practical applications exist for current quantum computers?"
       - "How can quantum theory advances translate to algorithm improvements?"

  5. knowledge-graph:
     Creates local graph: quantum_computing.json
     Entities: 47 concepts, confidence avg 0.78
     Relationships: 156 co-occurrence links

  6. obsidian-markdown:
     Creates: Quantum_Computing_Research.md
     Structure: MOC with clusters, gaps highlighted, questions as tasks
     Diagrams: Mermaid graph of topical structure

Result: Comprehensive research framework with actionable questions
```

### Example 2: SEO Optimization for Blog Post

```
User: "Optimize my blog post about machine learning for SEO.
Find keyword opportunities and content gaps."

Orchestrator Analysis:
  contains_seo_keywords: true
  requires_optimization: true
  artifact_type: analysis + strategy
  pattern_match: Pattern 2 (SEO Content Optimization)
  confidence: 0.88

Execution:
  1. mcp__infranodus__generate_topical_clusters:
     Input: Blog post text
     Output: Clusters: [Neural Networks, Training Methods, Applications, Tools]

  2. mcp__infranodus__generate_seo_report:
     Progress tracking: 6 stages
     Output:
       - Current ranking potential: Medium
       - Missing topics: "model deployment", "production ML"
       - Keyword opportunities: 23 identified

  3. mcp__infranodus__search_queries_vs_search_results:
     Queries: ["machine learning tutorial", "neural network guide"]
     Output: Users search "production deployment" but results lack it

  4. hierarchical-reasoning:
     Strategic: "Focus on practitioner needs vs theoretical coverage"
     Tactical: "Add deployment section, expand tools coverage"
     Operational: "Include MLOps, Docker, cloud platforms"

  5. obsidian-markdown:
     Creates: ML_Blog_SEO_Strategy.md
     Includes: Opportunity matrix, keyword priorities, content roadmap

Result: Actionable SEO strategy with specific improvements
```

### Example 3: Comparative Analysis of Research Papers

```
User: "Compare these three AI papers and find what unique
contributions each makes."

Orchestrator Analysis:
  multiple_texts: true
  requires_comparison: true
  complexity_score: 0.75
  pattern_match: Pattern 3 (Comparative Text Analysis)
  confidence: 0.83

Execution:
  1. mcp__infranodus__overlap_between_texts:
     Input: [paper1, paper2, paper3]
     Output:
       Shared concepts: [transformers, attention mechanisms, scaling laws]
       Common themes: Architecture improvements

  2. mcp__infranodus__difference_between_texts:
     Paper 1 unique: Sparse attention patterns
     Paper 2 unique: Training efficiency methods
     Paper 3 unique: Multi-modal capabilities

  3. knowledge-graph:
     Merged graph: ai_papers_comparison.json
     Tagged entities by source paper
     Calculated uniqueness scores

  4. obsidian-markdown:
     Creates: AI_Papers_Comparison.md
     Venn diagram: Shared vs unique concepts
     Graph diagram: Relationship network
     Table: Contribution matrix

Result: Clear visualization of overlaps and unique contributions
```

### Example 4: Topic Development for Content Series

```
User: "I'm writing about distributed systems. Help me identify
underdeveloped topics and expand my coverage."

Orchestrator Analysis:
  requires_iteration: true
  complexity_score: 0.72
  artifact_type: analysis + documentation
  pattern_match: Pattern 4 (Iterative Topic Development)
  confidence: 0.78

Execution:
  1. mcp__infranodus__generate_knowledge_graph:
     Input: Current distributed systems content
     Output: Clusters: [Consistency, Replication, Consensus, Partitioning]

  2. mcp__infranodus__develop_latent_topics:
     Output:
       Underdeveloped: "failure recovery patterns"
       Weak: "practical implementation examples"
       Missing: "performance tuning strategies"

  3. mcp__infranodus__develop_conceptual_bridges:
     Output:
       Bridge to microservices architecture
       Connect to cloud-native patterns
       Link to data engineering concepts

  4. mcp__infranodus__develop_text_tool:
     Research questions:
       - "How do failure recovery patterns differ across consensus algorithms?"
       - "What are practical patterns for implementing distributed transactions?"

  5. hierarchical-reasoning:
     Synthesizes: Content expansion roadmap with priorities

  6. obsidian-markdown:
     Creates: Distributed_Systems_Development.md
     Sections: Latent topics, bridges, expansion plan

Result: Strategic roadmap for content series expansion
```

## Integration with Knowledge-Orchestrator

The InfraNodus orchestrator and knowledge-orchestrator work in tandem:

**Decision Hierarchy**:
```yaml
User Request
  ↓
knowledge-orchestrator (evaluates first)
  ↓
  ├─ InfraNodus-specific? → Delegate to infranodus-orchestrator
  │   ↓
  │   infranodus-orchestrator:
  │     - Execute InfraNodus workflow
  │     - May call back to knowledge-orchestrator for sub-tasks
  │     - Coordinates: hierarchical-reasoning, knowledge-graph, obsidian-markdown
  │
  └─ Standard knowledge management? → knowledge-orchestrator handles
      ↓
      Routes to: obsidian-markdown, knowledge-graph, hierarchical-reasoning
```

**Example Delegation**:
```yaml
Request: "Create a note about AI with entity relationships"
  → knowledge-orchestrator: Standard knowledge base task
  → Routes to: obsidian-markdown + knowledge-graph
  → Result: Obsidian note with local knowledge graph

Request: "Analyze AI content for gaps and generate research questions"
  → knowledge-orchestrator: Detects InfraNodus requirement
  → Delegates to: infranodus-orchestrator
  → infranodus-orchestrator: Executes Pattern 1
  → Calls back for: obsidian documentation (via knowledge-orchestrator)
  → Result: InfraNodus gap analysis + research questions + Obsidian docs
```

## Resources

### references/

**infranodus_tools_reference.md**: Comprehensive reference for all 21+ InfraNodus MCP tools with parameter details, use cases, and examples.

**workflow_patterns_detailed.md**: Expanded workflow pattern library with additional patterns, customization options, and domain-specific adaptations.

**integration_mapping.md**: Detailed transformation specifications for integrating InfraNodus outputs with local skills (knowledge-graph, obsidian-markdown).

### scripts/

**workflow_analyzer.py**: Analyze user requests to extract task features and calculate confidence scores for workflow selection.

**graph_converter.py**: Convert InfraNodus graph format to local knowledge-graph JSON format with provenance and confidence mapping.

### assets/

**obsidian-templates/**: Collection of Obsidian markdown templates for different workflow outputs (research MOCs, SEO strategies, comparative analysis, topic development).

---

**Core Philosophy**: The InfraNodus Orchestrator bridges cloud-based graph analytics with local knowledge management, enabling sophisticated research workflows that preserve insights locally while leveraging world-class text network analysis. Strategic planning + powerful analytics + persistent documentation = comprehensive knowledge discovery.
