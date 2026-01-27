---
name: auto-claude-optimization
description: Auto-Claude performance optimization and cost management. Use when optimizing token usage, reducing API costs, improving build speed, or tuning agent performance.
version: 1.0.0
auto-claude-version: 2.7.2
---

# Auto-Claude Optimization

Performance tuning, cost reduction, and efficiency improvements.

## Performance Overview

### Key Metrics

| Metric | Impact | Optimization |
|--------|--------|--------------|
| API latency | Build speed | Model selection, caching |
| Token usage | Cost | Prompt efficiency, context limits |
| Memory queries | Speed | Embedding model, index tuning |
| Build iterations | Time | Spec quality, QA settings |

## Model Optimization

### Model Selection

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| claude-opus-4-5-20251101 | Slow | High | Best | Complex features |
| claude-sonnet-4-5-20250929 | Fast | Medium | Good | Standard features |

```bash
# Override model in .env
AUTO_BUILD_MODEL=claude-sonnet-4-5-20250929
```

### Extended Thinking Tokens

Configure thinking budget per agent:

| Agent | Default | Recommended |
|-------|---------|-------------|
| Spec creation | 16000 | Keep default for quality |
| Planning | 5000 | Reduce to 3000 for speed |
| Coding | 0 | Keep disabled |
| QA Review | 10000 | Reduce to 5000 for speed |

```python
# In agent configuration
max_thinking_tokens=5000  # or None to disable
```

## Token Optimization

### Reduce Context Size

1. **Smaller spec files**
   ```bash
   # Keep specs concise
   # Bad: 5000 word spec
   # Good: 500 word spec with clear criteria
   ```

2. **Limit codebase scanning**
   ```python
   # In context/builder.py
   MAX_CONTEXT_FILES = 50  # Reduce from 100
   ```

3. **Use targeted searches**
   ```bash
   # Instead of full codebase scan
   # Focus on relevant directories
   ```

### Efficient Prompts

Optimize system prompts in `apps/backend/prompts/`:

```markdown
<!-- Bad: Verbose -->
You are an expert software developer who specializes in building
high-quality, production-ready applications. You have extensive
experience with many programming languages and frameworks...

<!-- Good: Concise -->
Expert full-stack developer. Build production-quality code.
Follow existing patterns. Test thoroughly.
```

### Memory Optimization

```bash
# Use efficient embedding model
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Or offline with smaller model
OLLAMA_EMBEDDING_MODEL=all-minilm
OLLAMA_EMBEDDING_DIM=384
```

## Speed Optimization

### Parallel Execution

```bash
# Enable more parallel agents (default: 4)
MAX_PARALLEL_AGENTS=8
```

### Reduce QA Iterations

```bash
# Limit QA loop iterations
MAX_QA_ITERATIONS=10  # Default: 50

# Skip QA for quick iterations
python run.py --spec 001 --skip-qa
```

### Faster Spec Creation

```bash
# Force simple complexity for quick tasks
python spec_runner.py --task "Fix typo" --complexity simple

# Skip research phase
SKIP_RESEARCH_PHASE=true python spec_runner.py --task "..."
```

### API Timeout Tuning

```bash
# Reduce timeout for faster failure detection
API_TIMEOUT_MS=120000  # 2 minutes (default: 10 minutes)
```

## Cost Management

### Monitor Token Usage

```bash
# Enable cost tracking
ENABLE_COST_TRACKING=true

# View usage report
python usage_report.py --spec 001
```

### Cost Reduction Strategies

1. **Use cheaper models for simple tasks**
   ```bash
   # For simple specs
   AUTO_BUILD_MODEL=claude-sonnet-4-5-20250929 python spec_runner.py --task "..."
   ```

2. **Limit context window**
   ```bash
   MAX_CONTEXT_TOKENS=50000  # Reduce from 100000
   ```

3. **Batch similar tasks**
   ```bash
   # Create specs together, run together
   python spec_runner.py --task "Add feature A"
   python spec_runner.py --task "Add feature B"
   python run.py --spec 001
   python run.py --spec 002
   ```

4. **Use local models for memory**
   ```bash
   # Ollama for memory (free)
   GRAPHITI_LLM_PROVIDER=ollama
   GRAPHITI_EMBEDDER_PROVIDER=ollama
   ```

### Cost Estimation

| Operation | Estimated Tokens | Cost (Opus) | Cost (Sonnet) |
|-----------|-----------------|-------------|---------------|
| Simple spec | 10k | ~$0.30 | ~$0.06 |
| Standard spec | 50k | ~$1.50 | ~$0.30 |
| Complex spec | 200k | ~$6.00 | ~$1.20 |
| Build (simple) | 50k | ~$1.50 | ~$0.30 |
| Build (standard) | 200k | ~$6.00 | ~$1.20 |
| Build (complex) | 500k | ~$15.00 | ~$3.00 |

## Memory System Optimization

### Embedding Performance

```bash
# Faster embeddings
OPENAI_EMBEDDING_MODEL=text-embedding-3-small  # 1536 dim, fast

# Higher quality (slower)
OPENAI_EMBEDDING_MODEL=text-embedding-3-large  # 3072 dim

# Offline (fastest, free)
OLLAMA_EMBEDDING_MODEL=all-minilm
OLLAMA_EMBEDDING_DIM=384
```

### Query Optimization

```python
# Limit search results
memory.search("query", limit=10)  # Instead of 100

# Use semantic caching
ENABLE_MEMORY_CACHE=true
```

### Database Maintenance

```bash
# Compact database periodically
python -c "from integrations.graphiti.memory import compact_database; compact_database()"

# Clear old episodes
python query_memory.py --cleanup --older-than 30d
```

## Build Efficiency

### Spec Quality = Build Speed

High-quality specs reduce iterations:

```markdown
# Good spec (fewer iterations)
## Acceptance Criteria
- [ ] User can log in with email/password
- [ ] Invalid credentials show error message
- [ ] Successful login redirects to /dashboard
- [ ] Session persists for 24 hours

# Bad spec (more iterations)
## Acceptance Criteria
- [ ] Login works
```

### Subtask Granularity

Optimal subtask size:
- **Too large**: Agent gets stuck, needs recovery
- **Too small**: Overhead per subtask
- **Optimal**: 30-60 minutes of work each

### Parallel Work

Let agents spawn subagents for parallel execution:

```
Main Coder
├── Subagent 1: Frontend (parallel)
├── Subagent 2: Backend (parallel)
└── Subagent 3: Tests (parallel)
```

## Environment Tuning

### Optimal .env Configuration

```bash
# Performance-focused configuration
AUTO_BUILD_MODEL=claude-sonnet-4-5-20250929
API_TIMEOUT_MS=180000
MAX_PARALLEL_AGENTS=6

# Memory optimization
GRAPHITI_LLM_PROVIDER=ollama
GRAPHITI_EMBEDDER_PROVIDER=ollama
OLLAMA_LLM_MODEL=llama3.2:3b
OLLAMA_EMBEDDING_MODEL=all-minilm
OLLAMA_EMBEDDING_DIM=384

# Reduce verbosity
DEBUG=false
ENABLE_FANCY_UI=false
```

### Resource Limits

```bash
# Limit Python memory
export PYTHONMALLOC=malloc

# Set max file descriptors
ulimit -n 4096
```

## Benchmarking

### Measure Build Time

```bash
# Time a build
time python run.py --spec 001

# Compare models
time AUTO_BUILD_MODEL=claude-opus-4-5-20251101 python run.py --spec 001
time AUTO_BUILD_MODEL=claude-sonnet-4-5-20250929 python run.py --spec 001
```

### Profile Memory Usage

```bash
# Monitor memory
watch -n 1 'ps aux | grep python | head -5'

# Profile script
python -m cProfile -o profile.stats run.py --spec 001
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"
```

## Quick Wins

### Immediate Optimizations

1. **Switch to Sonnet for most tasks**
   ```bash
   AUTO_BUILD_MODEL=claude-sonnet-4-5-20250929
   ```

2. **Use Ollama for memory**
   ```bash
   GRAPHITI_LLM_PROVIDER=ollama
   GRAPHITI_EMBEDDER_PROVIDER=ollama
   ```

3. **Skip QA for prototypes**
   ```bash
   python run.py --spec 001 --skip-qa
   ```

4. **Force simple complexity for small tasks**
   ```bash
   python spec_runner.py --task "..." --complexity simple
   ```

### Medium-Term Improvements

1. Optimize prompts in `apps/backend/prompts/`
2. Configure project-specific security allowlist
3. Set up memory caching
4. Tune parallel agent count

### Long-Term Strategies

1. Self-hosted LLM for memory (Ollama)
2. Caching layer for common operations
3. Incremental context building
4. Project-specific prompt optimization

## Related Skills

- **auto-claude-memory**: Memory configuration
- **auto-claude-build**: Build process
- **auto-claude-troubleshooting**: Debugging
