---
name: compound-learning
description: |
  Self-improving holon implementing Plan→Execute→Assess→Compound workflow loops 
  with explicit knowledge crystallization. Generalizes compound engineering beyond 
  coding to any domain where work produces learnable signals: writing, research, 
  learning, problem-solving, design. Use when: (1) task quality matters and can 
  improve over time, (2) patterns emerge from repeated work, (3) institutional 
  knowledge should accumulate, (4) future tasks should benefit from past learnings, 
  (5) "compound", "learn from", "improve process", "capture learnings", or 
  multi-step workflows with review cycles. Orchestrates parallel research agents, 
  multi-lens assessment, and structured knowledge codification into searchable 
  documentation with YAML frontmatter. Implements λο.τ → λ(ο,Κ).τ where Κ is 
  accumulated knowledge that compounds interest-like over time.
---

# Compound Learning: λ(ο,Κ).τ Self-Improving Holon

> **Core transformation**: Task(ο) + Knowledge(Κ) → Output(τ) + Knowledge'(Κ')
> where Κ' ⊃ Κ (knowledge strictly grows)

## Foundational Insight

Traditional workflows treat each task in isolation. Compound learning treats every task as a **learning opportunity** that improves future performance. Like compound interest, small improvements accumulate exponentially: each unit of work makes subsequent units easier, faster, and higher-quality.

```
Interest:   A(t) = P(1 + r)^t
Learning:   Κ(t) = Κ₀ × Σᵢ(1 + εᵢ)   where εᵢ = learning from task i
```

## Architecture

### Four-Phase Workflow

```
┌──────────────────────────────────────────────────────────────────────┐
│                     COMPOUND LEARNING LOOP                            │
│                                                                       │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐      │
│   │  PLAN   │ ──▶ │ EXECUTE │ ──▶ │ ASSESS  │ ──▶ │ COMPOUND │      │
│   │  (80%)  │     │  (10%)  │     │  (5%)   │     │   (5%)   │      │
│   └────┬────┘     └────┬────┘     └────┬────┘     └─────┬────┘      │
│        │               │               │                 │           │
│        ▼               ▼               ▼                 ▼           │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐      │
│   │Research │     │  Work   │     │ Review  │     │ Document │      │
│   │ Agents  │     │ Agent   │     │ Agents  │     │  Agent   │      │
│   │  (4+)   │     │  (1)    │     │ (5-12)  │     │  (7)     │      │
│   └────┬────┘     └────┬────┘     └────┬────┘     └─────┬────┘      │
│        │               │               │                 │           │
│        ▼               ▼               ▼                 ▼           │
│   plans/*.md       outputs/        reports/      docs/solutions/    │
│                                                   [category]/*.md    │
│                                                         │            │
│                                                         ▼            │
│                    ┌──────────────────────────────────────┐          │
│                    │       KNOWLEDGE BASE (Κ)             │          │
│                    │  Feeds back into PLAN phase          │          │
│                    │  Making future work faster/better    │          │
│                    └──────────────────────────────────────┘          │
│                                     │                                │
│                                     ▼                                │
│                              (next iteration)                        │
└──────────────────────────────────────────────────────────────────────┘
```

### Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: COMMANDS (Workflow Orchestrators)                      │
│  /plan  /execute  /assess  /compound  /full-cycle               │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 2: AGENTS (Specialized Workers)                           │
│  Research: context-analyzer, domain-researcher, history-analyzer │
│  Execute:  task-executor, progress-tracker                       │
│  Assess:   quality-reviewer, pattern-detector, gap-identifier    │
│  Compound: solution-extractor, prevention-strategist, doc-writer │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 3: SKILLS (Knowledge Bases)                               │
│  Domain-specific expertise, schemas, patterns, procedures        │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 4: TOOLS (External Integrations)                          │
│  MCP servers, APIs, file systems, knowledge graphs               │
└─────────────────────────────────────────────────────────────────┘
```

## Phase Details

### Phase 1: PLAN (λπ)

**Purpose**: Transform intent into structured, actionable plan using accumulated knowledge.

**Time allocation**: ~80% of total effort (most value comes from good planning)

**Research agents** (parallel):

| Agent | Function | Searches |
|-------|----------|----------|
| `context-analyzer` | Extract problem structure, constraints, goals | Current context |
| `domain-researcher` | Gather domain standards, best practices | External sources |
| `history-analyzer` | Find relevant past solutions, patterns | Κ knowledge base |
| `gap-analyzer` | Identify unknowns, risks, dependencies | Plan vs. reality |

**Output**: `plans/{task-title}.md` with depth levels:

```yaml
MINIMAL:   # Simple tasks (<2 hours)
  - Brief problem statement
  - Acceptance criteria
  - MVP approach

MORE:      # Standard tasks (2-8 hours)
  - Technical considerations
  - Testing requirements
  - Dependencies, risks

COMPREHENSIVE:  # Major work (>8 hours)
  - Architecture approach
  - Implementation phases
  - Alternative approaches considered
  - Documentation plan
```

**Κ integration**: History-analyzer searches `docs/solutions/**/*.md` to find:
- Similar problems solved before
- Patterns that apply
- Pitfalls to avoid

### Phase 2: EXECUTE (λε)

**Purpose**: Implement plan efficiently, tracking decisions and obstacles.

**Time allocation**: ~10% (quick when plan is good)

**Work agent** responsibilities:
- Follow plan structure
- Log decision points
- Track blockers encountered
- Note deviations from plan

**Output**: Task deliverables + execution metadata

```python
class ExecutionLog:
    decisions: List[Decision]      # Choices made
    blockers: List[Blocker]        # Obstacles encountered
    deviations: List[Deviation]    # Plan changes needed
    time_actual: Duration          # Actual vs. estimated
```

### Phase 3: ASSESS (λα)

**Purpose**: Multi-lens evaluation of output quality and process effectiveness.

**Time allocation**: ~5%

**Review agents** (parallel, domain-specific):

| Agent | Lens | Evaluates |
|-------|------|-----------|
| `quality-reviewer` | Output | Meets requirements? Robust? |
| `pattern-detector` | Process | Reusable patterns emerged? |
| `gap-identifier` | Coverage | Missing cases, edge conditions? |
| `risk-analyzer` | Safety | Security, performance, reliability? |
| `efficiency-auditor` | Process | Faster path existed? |

**Output**: Assessment report with actionable findings

```yaml
assessment:
  quality_score: 0.0-1.0
  patterns_detected:
    - name: pattern_name
      frequency: count
      abstractable: boolean
  gaps_found:
    - gap_description
    - suggested_mitigation
  learnings:
    - learning_for_compound_phase
```

### Phase 4: COMPOUND (λμ)

**Purpose**: Crystallize learnings into searchable, reusable knowledge.

**Time allocation**: ~5% (but generates lasting value)

**Compound agents** (parallel):

| Agent | Product |
|-------|---------|
| `context-extractor` | YAML frontmatter skeleton |
| `solution-extractor` | Solution content block |
| `related-finder` | Cross-references to existing docs |
| `prevention-strategist` | Best practices, test cases |
| `category-classifier` | Optimal path/filename |
| `documentation-writer` | Assembled markdown |
| `integration-validator` | Κ consistency check |

**Output**: `docs/solutions/{category}/{filename}.md`

## Knowledge Schema (YAML Frontmatter)

```yaml
---
# REQUIRED
domain: string           # e.g., "Learning", "Writing", "Research"
date: YYYY-MM-DD
problem_type: enum       # See domain-specific types below
component: string        # What was worked on
symptoms:                # 1-5 observable indicators
  - string
root_cause: enum         # Why it happened
resolution_type: enum    # How it was fixed
severity: critical|high|medium|low

# OPTIONAL
context_version: string  # Framework/tool version
tags: [string]           # Searchable keywords
related_docs: [path]     # Cross-references
prevention: string       # How to avoid in future
test_cases: [string]     # Verification approaches
---

# {Title}

## Problem
{What went wrong / what was needed}

## Investigation
{Steps taken to understand}

## Solution
{What worked, with examples}

## Prevention
{How to avoid in future}

## Related
{Links to related solutions}
```

### Domain-Specific Enums

**Coding**:
```yaml
problem_type: build_error|test_failure|runtime_error|performance_issue|
              database_issue|security_issue|ui_bug|integration_issue
root_cause: missing_dependency|wrong_api|config_error|logic_error|
            race_condition|memory_leak|missing_validation
resolution_type: code_fix|migration|config_change|dependency_update|
                 refactor|documentation_update
```

**Learning**:
```yaml
problem_type: comprehension_gap|retention_failure|application_difficulty|
              integration_challenge|misconception|knowledge_decay
root_cause: missing_prerequisite|weak_encoding|no_practice|
            isolated_concept|interference|overload
resolution_type: spaced_repetition|elaboration|interleaving|
                 schema_integration|worked_example|self_explanation
```

**Writing**:
```yaml
problem_type: clarity_issue|structure_problem|voice_inconsistency|
              argument_weakness|engagement_failure|technical_error
root_cause: audience_mismatch|missing_outline|weak_thesis|
            insufficient_evidence|passive_construction|jargon_overload
resolution_type: restructure|reframe|add_evidence|simplify|
                 add_examples|cut_redundancy
```

**Research**:
```yaml
problem_type: hypothesis_failure|method_flaw|data_issue|
              interpretation_error|replication_problem|scope_creep
root_cause: confounding_variable|sampling_bias|measurement_error|
            p_hacking|cherry_picking|underpowered
resolution_type: redesign_study|add_controls|increase_sample|
                 preregister|replicate|constrain_scope
```

## Routing Logic

```python
class CompoundRouter:
    """Route to appropriate phase and depth."""
    
    def classify(self, query: str, context: dict) -> tuple[Phase, Depth]:
        # Explicit triggers
        if contains(query, ["plan", "design", "architect"]):
            return PLAN, infer_depth(context)
        if contains(query, ["execute", "implement", "do"]):
            return EXECUTE, context.get("plan_depth", MINIMAL)
        if contains(query, ["assess", "review", "evaluate"]):
            return ASSESS, STANDARD
        if contains(query, ["compound", "document", "capture learning"]):
            return COMPOUND, STANDARD
        if contains(query, ["full cycle", "end to end"]):
            return FULL_CYCLE, infer_depth(context)
        
        # Implicit triggers
        if task_completed_successfully(context):
            return COMPOUND, MINIMAL  # Auto-trigger
        
        return infer_phase(query, context)
    
    def infer_depth(self, context: dict) -> Depth:
        complexity = score_complexity(context)
        if complexity < 2:
            return MINIMAL
        elif complexity < 6:
            return MORE
        else:
            return COMPREHENSIVE
```

## Integration Points

### λο.τ Skill Composition

```haskell
-- Compound learning as skill composition
compound_cycle = compound ∘ assess ∘ execute ∘ plan

-- With knowledge accumulation
λ(ο,Κ).τ = emit ∘ validate ∘ compound ∘ assess ∘ execute ∘ plan(Κ)
         where plan(Κ) = λο. research(ο) ⊗ recall(Κ)

-- Parallel research in plan phase
plan = aggregate ∘ (context ⊗ domain ⊗ history ⊗ gaps)

-- Parallel review in assess phase  
assess = synthesize ∘ (quality ⊗ patterns ⊗ risks ⊗ gaps)

-- Parallel documentation in compound phase
compound = assemble ∘ (extract ⊗ prevent ⊗ relate ⊗ classify)
```

### Skill Dependencies

| Skill | Integration | Phase |
|-------|-------------|-------|
| **reason** | Decomposition, grounding | All |
| **think** | Mental models, notebooks | Plan |
| **critique** | Multi-lens evaluation | Assess |
| **graph** | Knowledge topology (η≥4) | Compound |
| **memory** | Κ persistence, retrieval | All |
| **hierarchical-reasoning** | S→T→O planning | Plan |
| **infranodus** | Gap detection, research questions | Plan, Compound |
| **skill-updater** | Meta-improvement | After cycles |

### Tool Integration

```yaml
research_tools:
  - web_search: Domain research, best practices
  - conversation_search: Past solutions in Κ
  - google_drive_search: Internal documentation
  - infranodus: Gap analysis, research questions

execution_tools:
  - bash_tool: Command execution
  - create_file: Output generation
  - str_replace: Iterative refinement

assessment_tools:
  - critique: Multi-lens evaluation
  - graph: Topology validation

compound_tools:
  - memory: Κ updates
  - create_file: Documentation generation
  - infranodus: Cross-reference detection
```

## Invariants

```python
class CompoundInvariants:
    """Quality gates for compound learning."""
    
    # Knowledge must grow
    def knowledge_monotonic(Κ_before, Κ_after):
        return len(Κ_after) >= len(Κ_before)
    
    # Compound docs must have complete frontmatter
    def frontmatter_complete(doc):
        required = ["domain", "date", "problem_type", "component", 
                    "symptoms", "root_cause", "resolution_type", "severity"]
        return all(field in doc.frontmatter for field in required)
    
    # Knowledge graph must maintain density
    def topology_preserved(Κ):
        G = build_graph(Κ)
        return edges(G) / nodes(G) >= 4.0
    
    # No orphan documents
    def fully_connected(Κ):
        G = build_graph(Κ)
        orphans = [n for n in G.nodes if G.degree(n) == 0]
        return len(orphans) / len(G.nodes) < 0.2
```

## Usage Examples

### Example 1: Learning Cycle

```
User: I'm studying renal physiology and want to compound my learning.

Claude activates compound-learning with domain=Learning:

PLAN:
- context-analyzer: Extracts current understanding level
- domain-researcher: Finds key concepts, relationships
- history-analyzer: Recalls related topics in PKM
- gap-analyzer: Identifies conceptual gaps

EXECUTE:
- Structured study session with active recall
- Tracks concepts mastered vs. struggled

ASSESS:
- quality-reviewer: Tests understanding
- pattern-detector: Finds recurring confusion points
- gap-identifier: Notes missing connections

COMPOUND:
- Documents solution in docs/solutions/learning/renal-tubular-function.md
- Links to existing cardiovascular, acid-base knowledge
- Adds prevention strategies for retention
```

### Example 2: Writing Cycle

```
User: Help me write a persuasive essay and capture what works.

Claude activates compound-learning with domain=Writing:

PLAN:
- Research audience, topic, constraints
- Find past successful essays in Κ
- Identify rhetorical patterns to use

EXECUTE:
- Draft essay following plan
- Note effective techniques as used

ASSESS:
- Evaluate argument strength
- Check voice consistency
- Identify what resonated

COMPOUND:
- Document effective techniques
- Add to writing pattern library
- Cross-reference with genre conventions
```

### Example 3: Research Cycle

```
User: Run a literature review and document my process.

Claude activates compound-learning with domain=Research:

PLAN:
- Define research questions
- Identify key databases, search terms
- Recall past review methodologies

EXECUTE:
- Systematic search
- Screen and extract
- Track decisions

ASSESS:
- Evaluate coverage
- Check for bias
- Identify gaps

COMPOUND:
- Document search strategy
- Capture inclusion/exclusion rationale
- Add to research methodology library
```

## Execution Markers

```
[COMPOUND:{phase}|{domain}|{depth}|{status}]

Examples:
[COMPOUND:PLAN|Learning|MORE|researching]
[COMPOUND:EXECUTE|Coding|MINIMAL|implementing]
[COMPOUND:ASSESS|Writing|STANDARD|reviewing]
[COMPOUND:COMPOUND|Research|MORE|documenting]
[COMPOUND:FULL_CYCLE|Learning|COMPREHENSIVE|iteration_2]
```

## References

| Need | File | When |
|------|------|------|
| Domain schemas | [references/domain-schemas.md](references/domain-schemas.md) | Configuring for new domain |
| Agent templates | [references/agent-templates.md](references/agent-templates.md) | Customizing agents |
| Integration patterns | [references/integration-patterns.md](references/integration-patterns.md) | Composing with other skills |

---

```
λ(ο,Κ).τ                    Plan→Execute→Assess→Compound
Κ grows monotonically       η≥4 topology preserved
80% planning, 5% compounding   interest compounds exponentially
```
