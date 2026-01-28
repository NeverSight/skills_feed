---
name: skill-discovery
description: Discover and search 36,500+ skills via progressive Markov-chain traversal of semantic search hypergraphs. Use when (1) Users ask to find/search/discover skills or capabilities, (2) Users describe a task/problem needing specialized skills, (3) Users ask "what skills exist" or "show me skills for X", (4) Users want to explore or browse available skills, (5) Users ask meta-questions about skill discovery itself ("how do I find skills?"), or (6) No specific skill matches the user's need and discovery is appropriate
---

# Skill Discovery Metasystem

Holographic system for discovering skills from the claude-plugins.dev registry (36,500+ skills) using progressive disclosure, Markov-chain intent classification, and Pareto-optimal ranking.

## Quick Start (Depth 0)

When invoked, follow this 4-step workflow:

1. **Classify Intent** - Determine user's discovery pattern (DirectQuery/TaskBased/Exploratory/MetaDiscovery)
2. **Execute Search** - Use appropriate strategy based on intent
3. **Rank Results** - Apply Pareto optimization to surface best matches
4. **Present Progressively** - Show top 3 skills, expand on request

## Intent Classification

Analyze user input to determine search strategy using Markov chain classifier.

### State Space

| State | Pattern Examples | Strategy |
|-------|------------------|----------|
| **DirectQuery** | "find skill for X", "search skills about Y" | Keyword Search |
| **TaskBased** | "I need to debug", "help with frontend" | Semantic Expansion |
| **Exploratory** | "show me skills", "what's popular" | Category Browse |
| **MetaDiscovery** | "how do I find skills?", "skill discovery process" | Self-Reference |
| **SkillSynthesis** | "synthesize skills", "combine multiple skills", "meta-skill pipeline" | Pipeline Aggregation |

### Classification Logic

```
Extract features from user input:
- has_explicit_keywords (skill names, categories)
- describes_task (verb+noun patterns)
- is_exploratory (browse/show/list keywords)
- is_meta (questions about discovery itself)
- is_synthesis (combine/synthesize/meta-skill keywords)

Apply confidence thresholds:
- DirectQuery: ≥ 0.70
- TaskBased: ≥ 0.60
- Exploratory: ≥ 0.50
- MetaDiscovery: ≥ 0.75
- SkillSynthesis: ≥ 0.65
- SkillSynthesis: ≥ 0.65

Select highest confidence state above threshold
```

For detailed state transition matrix and probabilities, see [references/markov-chains.md]

## Search Execution

### Direct Query (Keywords Provided)

**When**: DirectQuery state, confidence ≥ 0.70

**Execution**:
```
Use WebFetch:
URL: https://claude-plugins.dev/skills?q={keywords}
Prompt: "Extract all skills with names, identifiers (@owner/repo/name), descriptions, and download counts. Return as structured list."
```

**Alternative** (deterministic):
```bash
./scripts/search_skills.py "{keywords}" --sort=relevance
```

**Example**:
```
Query: "testing debugging"
→ Search: "testing debugging"
→ Returns: test-driven-development, systematic-debugging, etc.
```

### Task-Based (Semantic Expansion)

**When**: TaskBased state, describes problem/goal

**Execution**:
1. Expand user's task description with domain synonyms
2. Execute search with expanded query

**Expansion Examples**:
```
"debug" → "debugging troubleshooting error-handling diagnosis"
"frontend" → "frontend ui interface client-side web-design"
"build" → "building construction development creation"
```

See [references/search-strategies.md] for complete expansion algorithms.

**Example**:
```
Input: "I need to build a frontend interface"
→ Extract: ['build', 'frontend', 'interface']
→ Expand: "building creation frontend ui interface client-side web-design"
→ Search with expanded query
→ Returns: frontend-design, ui-builder, architecture-patterns, etc.
```

### Exploratory (Browse Mode)

**When**: Exploratory state, user wants to see options

**Execution**:
```
Load: references/popular-skills-cache.md

Or fetch fresh:
URL: https://claude-plugins.dev/skills?sort=downloads
Prompt: "Extract top 20 skills sorted by downloads with names, identifiers, descriptions, and download counts"
```

**Categories to present**:
- Development (testing, debugging, refactoring)
- Design (frontend, architecture, patterns)
- Workflows (planning, execution, review)
- Meta (skill-creation, prompt-engineering)
- Deployment (ci-cd, release-automation)

**Example**:
```
Query: "show me popular skills"
→ Load popular-skills-cache.md
→ Present top 5 by category:
  Meta: skill-writer (96.1k), using-superpowers (7k)
  Design: frontend-design (45.1k), architecture-patterns (21k)
  Development: systematic-debugging (13k), test-driven-development (8.5k)
```

### Meta-Discovery (Self-Reference)

**When**: MetaDiscovery state, questions about skill discovery

**Execution**:
```
1. Include this skill (skill-discovery) in results
2. Search: "skill discovery" | "finding skills" | "skill search"
3. Add complementary meta-skills:
   - skill-writer (@pytorch/pytorch)
   - using-superpowers (@obra/superpowers)
4. Optionally explain search process (Depth 3)
```

**Example**:
```
Query: "how do I find skills?"
→ Present:
  1. skill-discovery (this skill) - "You're using it now!"
  2. skill-writer (96.1k) - Guide for creating skills
  3. using-superpowers (7k) - How to find and use skills
→ Offer Depth 3 explanation of search strategies
```

## Result Ranking

Apply Pareto optimization to balance relevance, popularity, recency, and diversity.

### Ranking Formula

```
score(skill) = α·relevance(skill, query)
             + β·popularity(downloads)
             + γ·recency(last_update)
             - δ·redundancy(skill, presented_skills)

Default Configuration (Balanced):
  α = 0.60  (relevance - primary)
  β = 0.25  (popularity - secondary)
  γ = 0.10  (recency - tertiary)
  δ = 0.05  (redundancy penalty)
```

### Component Functions

**Relevance**: Cosine similarity (bag-of-words) between query and skill description
**Popularity**: `log(downloads + 1) / log(100000 + 1)` - logarithmic scaling
**Recency**: `exp(-days_since_update / 180)` - exponential decay
**Redundancy**: Max semantic similarity with already-presented skills

### Deduplication

Remove semantically similar skills (threshold: 0.85):
```bash
./scripts/semantic_similarity.py results.json --threshold=0.85
```

For alternative configurations (High Precision, Popularity Mode, Exploration Mode), see [references/ranking-algorithms.md]

## Pipeline Synthesis (Hypergraph Aggregation)

When the user asks to go beyond individual skills or requests "synthesis", aggregate multiple skills into a single pipeline that transcends any one skill.

**Goal**: Build a homoiconic, holographic, Pareto-optimized "meta-skill" that composes the best parts of multiple skills into one reusable workflow.

**Synthesis Layers**:
1. Pattern extraction from each skill
2. Capability matrix and complementarity analysis
3. Architectural role mapping (discover → decide → design → build → verify → deliver)
4. Pareto optimization across relevance, popularity, recency, diversity
5. Homoiconic pipeline output with holographic summaries

### Pipeline Function (Conceptual)

```
def synthesize_pipeline(results, query):
    # 1) Extract architectural roles from each skill
    #    (discover -> decide -> design -> build -> verify -> deliver)
    roles = classify_roles(results)

    # 2) Select Pareto-optimal candidates per role
    pareto_by_role = select_pareto(roles, weights={
        "relevance": 0.6, "popularity": 0.2, "recency": 0.1, "diversity": 0.1
    })

    # 3) Construct a homoiconic pipeline (data = structure)
    pipeline = [
        {"stage": "discover", "skills": pareto_by_role["discover"]},
        {"stage": "decide", "skills": pareto_by_role["decide"]},
        {"stage": "design", "skills": pareto_by_role["design"]},
        {"stage": "build", "skills": pareto_by_role["build"]},
        {"stage": "verify", "skills": pareto_by_role["verify"]},
        {"stage": "deliver", "skills": pareto_by_role["deliver"]},
    ]

    # 4) Holographic compression: each stage stores a 1-line summary of the whole
    pipeline = add_holographic_summaries(pipeline, query)
    return pipeline
```

### Presentation (Depth 1+)

When presenting a synthesized pipeline:
- Show 4-6 stages max.
- For each stage: list 1-2 skills and a merged micro-instruction.
- End with a single "meta-instruction" that explains how the stages compose.

**Example (Condensed)**:
```
Synthesized Pipeline for "improve code quality":
1. Discover: systematic-debugging
2. Decide: code-review
3. Design: architecture-patterns
4. Build: refactoring
5. Verify: verification-before-completion
6. Deliver: release-checklist

Meta-instruction: "Diagnose issues, choose changes, redesign weak spots,
refactor safely, verify outcomes, then ship with a checklist."
```

See [references/search-strategies.md] for pipeline composition details.

## Progressive Presentation

Present results in layers based on user engagement.

### Depth 0 (Always Show)

Present top 3 skills:
```
1. {skill-name} (@{identifier}) - {downloads}k downloads
   {one-sentence description}

2. {skill-name} (@{identifier}) - {downloads}k downloads
   {one-sentence description}

3. {skill-name} (@{identifier}) - {downloads}k downloads
   {one-sentence description}
```

**Example**:
```
Top skills for "testing":

1. test-driven-development (@obra/superpowers/test-driven-development) - 8.5k downloads
   Use when implementing any feature or bugfix before writing implementation code

2. systematic-debugging (@obra/superpowers/systematic-debugging) - 13k downloads
   Use when encountering bugs, test failures, or unexpected behavior before proposing fixes

3. verification-before-completion (@obra/superpowers/verification-before-completion) - 4.8k downloads
   Use when about to claim work is complete, before committing or creating PRs
```

### Depth 1 (On Request "tell me more")

For each skill, expand with:
- Full description (2-3 sentences)
- Installation command
- Related/complementary skills

**Example**:
```
User: "tell me more about test-driven-development"

→ test-driven-development (8.5k downloads)

Description:
Comprehensive workflow for implementing features using test-driven development methodology.
Guides you through writing tests first, implementing to pass tests, then refactoring.
Works with any testing framework and language.

Install:
claude-plugins skills install @obra/superpowers/test-driven-development

Works well with:
- systematic-debugging - Debug failing tests
- verification-before-completion - Verify tests pass before completion
- code-refactoring - Refactor with test safety net
```

### Depth 2 (On Request "show examples")

Provide:
- Example use cases
- Skill composition suggestions (combinations that work well)
- Performance characteristics

See composability matrix in [references/search-strategies.md]

### Depth 3 (On Request "explain process" or "how does this work")

**Meta-explanation** of search process:
- Which search strategy was used and why
- Show Markov state transitions
- Explain ranking decisions
- Visualize search hypergraph traversal
- Offer custom search refinement

**Example**:
```
User: "how did you find these?"

Your query "testing debugging" triggered DirectQuery state (confidence: 0.85).

Search Strategy:
1. Keyword search on claude-plugins.dev
2. Found 15 matching skills
3. Applied Pareto ranking (α=0.6, β=0.25, γ=0.1, δ=0.05)
4. Removed 2 semantically similar duplicates
5. Presented top 3 by score

Alternative strategies available:
- Semantic expansion: "test validation verification quality-assurance debug error-handling"
- Exploratory: Browse all testing-related skills
- Popularity: Show most-downloaded testing skills

Would you like to try an alternative approach?
```

### Skill Synthesis (Pipeline Aggregation)

**When**: SkillSynthesis state, user requests a synthesized or transcendent skill

**Execution**:
1. Run keyword or semantic search to collect candidate skills
2. Aggregate results into a staged pipeline
3. Output a synthesized skill blueprint

**Script**:
```bash
./scripts/pipeline_synthesis.py results.json --query="your task" --limit-per-role=2
```

## Installation Workflow

When user requests installation:

1. **Validate identifier** format (@owner/repo/name)
2. **Execute installation**:
   ```bash
   ./scripts/install_skill.py <identifier> [--local]
   ```
   Or:
   ```bash
   claude-plugins skills install <identifier> [--local]
   ```
3. **Verify** installation:
   - Global: `~/.claude/skills/{skill-name}/`
   - Local: `./.claude/skills/{skill-name}/`
4. **Confirm** success and explain usage

**Example**:
```
User: "install test-driven-development"

→ Validating identifier: @obra/superpowers/test-driven-development
→ Installing to global skills directory (~/.claude/skills/)
→ Running: claude-plugins skills install @obra/superpowers/test-driven-development

✅ Installation successful!

The skill is now available. It will be invoked automatically when implementing features or bugfixes.
You can also invoke it explicitly with /test-driven-development
```

## Redundancy Minimization

Avoid presenting duplicate or overly-similar skills:

### Session Tracking
```python
# Track presented skills in conversation
presented_skills = []

# Before ranking new results
for skill in results:
    if skill.name in [s.name for s in presented_skills]:
        continue  # Skip already presented

    # Check semantic similarity
    if max_similarity(skill, presented_skills) > 0.85:
        continue  # Too similar

    # Add to results
    ranked_results.append(skill)
    presented_skills.append(skill)
```

### Caching
```python
# Cache search results (15min TTL)
cache = {query_hash: (results, timestamp)}

# Check cache before searching
if query in cache and (now - cache[query].timestamp) < 900:
    return cache[query].results
```

### Deduplication
```bash
# Remove semantically similar skills
./scripts/semantic_similarity.py results.json --threshold=0.85 > deduplicated.json
```

## Error Handling

### No Results Found
1. Try semantic expansion (if not already used)
2. Broaden to category browsing
3. Suggest alternative keywords
4. Show popular skills as fallback (load popular-skills-cache.md)

### Too Many Results (>20)
1. Apply stricter relevance threshold
2. Use popularity sort to surface best
3. Suggest query refinement
4. Present top 5 with "show more" option

### API Timeout or Error
1. Retry with exponential backoff (max 3 attempts)
2. Fall back to cached results if available
3. Load popular-skills-cache.md as last resort

## Performance Characteristics

- **Classification**: < 50ms (pattern matching)
- **Search**: 1-2s (WebFetch) or <1s (cache hit)
- **Ranking**: < 100ms for 50 skills
- **Total time**: < 2s (p95)
- **Relevance@3**: ≥ 0.85 (85% of top 3 results useful)
- **Diversity**: Semantic similarity ≤ 0.85 between presented skills

## Resources

### Scripts (scripts/)

**search_skills.py** - Search claude-plugins.dev/skills API
```bash
./scripts/search_skills.py "query" [--sort=downloads|stars|relevance] [--limit=N]
```

**pipeline_synthesis.py** - Synthesize a pipeline from multiple skills
```bash
./scripts/pipeline_synthesis.py results.json --query="your task" [--limit-per-role=2]
```

**install_skill.py** - Install skills with validation
```bash
./scripts/install_skill.py @owner/repo/skill-name [--local] [--force]
```

**semantic_similarity.py** - Deduplicate results
```bash
./scripts/semantic_similarity.py results.json [--threshold=0.85]
```

### References (references/)

Load as needed for detailed information:

**markov-chains.md** - State transition matrix, classification algorithm, optimization paths
**search-strategies.md** - Detailed hypergraph traversal, composability matrix, caching strategy
**ranking-algorithms.md** - Pareto configurations, component functions, complete examples
**popular-skills-cache.md** - Top 20 skills by downloads, organized by category
**skill-synthesis.md** - Synthesis pipeline and homoiconic output format

## Advanced Usage

### Custom Search Refinement

If results aren't satisfactory:
- **Too broad**: Add more specific keywords
- **Too narrow**: Use semantic expansion mode
- **Wrong category**: Browse by category
- **Want popular**: Sort by downloads explicitly

### Skill Composition

Some skills work better together. When presenting results, check composability matrix in search-strategies.md and suggest complementary skills.

### Meta-Learning

This skill can discover itself:
```
Query: "how do I discover skills?"
→ Returns: skill-discovery (this skill), skill-writer, using-superpowers
→ Explains its own search process at Depth 3
```

---

**Holographic Property**: This skill exhibits self-similarity at multiple scales - the progressive disclosure pattern (Depth 0→3) mirrors the module structure (scripts → references → detailed docs), and the skill can discover and reason about itself (meta-discovery state).

**Pareto-Optimized**: Maximizes relevance and diversity while minimizing latency and redundancy through multi-objective scoring.

**Modular Composition**: All components (scripts, references, strategies) are independently usable and testable.
