---
name: model-hierarchy
description: >
  Cost-optimize AI agent operations by routing tasks to appropriate models based on complexity.
  Use this skill when: (1) deciding which model to use for a task, (2) spawning sub-agents,
  (3) considering cost efficiency, (4) the current model feels like overkill for the task.
  Triggers: "model routing", "cost optimization", "which model", "too expensive", "spawn agent".

---

# Model Hierarchy

Route tasks to the cheapest model that can handle them. Most agent work is routine.

## Core Principle

**80% of agent tasks are janitorial.** File reads, status checks, formatting, simple Q&A. These don't need expensive models. Reserve premium models for problems that actually require deep reasoning.

## Model Tiers

### Tier 1: Cheap ($0.10-0.50/M tokens)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| DeepSeek V3 | $0.14 | $0.28 | General routine work |
| GPT-4o-mini | $0.15 | $0.60 | Quick responses |
| Claude Haiku | $0.25 | $1.25 | Fast tool use |
| Gemini Flash | $0.075 | $0.30 | High volume |
| GLM 5 (Zhipu) | (OpenRouter Z.AI) | (OpenRouter Z.AI) | Routine + moderate text; 200K context; **text-only** — do not use for image/vision |
| Kimi K2.5 (Moonshot) | $0.45 | $2.25 | Routine + moderate; 262K context; **multimodal (text + image + video)** |

**Text-only models (e.g. GLM 5):** Do not use for any task that requires image input or vision — no photo analysis, screenshots, image-generation tools, or document/chart vision. Route to a vision-capable model (e.g. Kimi K2.5, GPT-4o, Gemini, Claude with vision, GLM-4.5V/4.6V).

**Vision-capable Tier 1/2 (e.g. Kimi K2.5):** Use for routine or moderate tasks that may involve images — screenshots, photo analysis, docs, image-generation orchestration — without moving to premium vision models.

### Tier 2: Mid ($1-5/M tokens)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| Claude Sonnet | $3.00 | $15.00 | Balanced performance |
| GPT-4o | $2.50 | $10.00 | Multimodal tasks |
| Gemini Pro | $1.25 | $5.00 | Long context |

### Tier 3: Premium ($10-75/M tokens)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| Claude Opus | $15.00 | $75.00 | Complex reasoning |
| GPT-4.5 | $75.00 | $150.00 | Frontier tasks |
| o1 | $15.00 | $60.00 | Multi-step reasoning |
| o3-mini | $1.10 | $4.40 | Reasoning on budget |

*Prices as of Feb 2026. Check provider docs for current rates.*

## Task Classification

Before executing any task, classify it:

### ROUTINE → Use Tier 1

**Requires image/vision** → Do not assign to text-only models (GLM 5, etc.). Use a vision-capable model from Tier 1/2 or 3 (e.g. Kimi K2.5, GPT-4o, Gemini, Claude, GLM-4.5V).

Characteristics:
- Single-step operations
- Clear, unambiguous instructions
- No judgment required
- Deterministic output expected

Examples:
- File read/write operations
- Status checks and health monitoring
- Simple lookups (time, weather, definitions)
- Formatting and restructuring text
- List operations (filter, sort, transform)
- API calls with known parameters
- Heartbeat and cron tasks
- URL fetching and basic parsing

### MODERATE → Use Tier 2

Characteristics:
- Multi-step but well-defined
- Some synthesis required
- Standard patterns apply
- Quality matters but isn't critical

Examples:
- Code generation (standard patterns)
- Summarization and synthesis
- Draft writing (emails, docs, messages)
- Data analysis and transformation
- Multi-file operations
- Tool orchestration
- Code review (non-security)
- Search and research tasks

### COMPLEX → Use Tier 3

Characteristics:
- Novel problem solving required
- Multiple valid approaches
- Nuanced judgment calls
- High stakes or irreversible
- Previous attempts failed

Examples:
- Multi-step debugging
- Architecture and design decisions
- Security-sensitive code review
- Tasks where cheaper model already failed
- Ambiguous requirements needing interpretation
- Long-context reasoning (>50K tokens)
- Creative work requiring originality
- Adversarial or edge-case handling

## Decision Algorithm

```
function selectModel(task):
    # Rule 1: Vision override (Tier 1/2 includes text-only models)
    if task.requiresImageInput or task.requiresVision:
        return VISION_CAPABLE_MODEL  # e.g. Kimi K2.5, GPT-4o, Gemini, Claude; do not use GLM 5 or other text-only
    
    # Rule 2: Escalation override
    if task.previousAttemptFailed:
        return nextTierUp(task.previousModel)
    
    # Rule 3: Explicit complexity signals
    if task.hasSignal("debug", "architect", "design", "security"):
        return TIER_3
    
    if task.hasSignal("write", "code", "summarize", "analyze"):
        return TIER_2
    
    # Rule 4: Default classification
    complexity = classifyTask(task)
    
    if complexity == ROUTINE:
        return TIER_1
    elif complexity == MODERATE:
        return TIER_2
    else:
        return TIER_3
```

## Behavioral Rules

### For Main Session

1. **Default to Tier 2** for interactive work
2. **Suggest downgrade** when doing routine work: "This is routine - I can handle this on a cheaper model or spawn a sub-agent."
3. **Request upgrade** when stuck: "This needs more reasoning power. Switching to [premium model]."

### For Sub-Agents

1. **Default to Tier 1** unless task is clearly moderate+
2. **Batch similar tasks** to amortize overhead
3. **Report failures** back to parent for escalation

### For Automated Tasks

1. **Heartbeats/monitoring** → Always Tier 1
2. **Scheduled reports** → Tier 1 or 2 based on complexity
3. **Alert responses** → Start Tier 2, escalate if needed

## Communication Patterns

When suggesting model changes, use clear language:

**Downgrade suggestion:**
> "This looks like routine file work. Want me to spawn a sub-agent on DeepSeek for this? Same result, fraction of the cost."

**Upgrade request:**
> "I'm hitting the limits of what I can figure out here. This needs Opus-level reasoning. Switching up."

**Explaining hierarchy:**
> "I'm running the heavy analysis on Sonnet while sub-agents fetch the data on DeepSeek. Keeps costs down without sacrificing quality where it matters."

## Cost Impact

Assuming 100K tokens/day average usage:

| Strategy | Monthly Cost | Notes |
|----------|--------------|-------|
| Pure Opus | ~$225 | Maximum capability, maximum spend |
| Pure Sonnet | ~$45 | Good default for most work |
| Pure DeepSeek | ~$8 | Cheap but limited on hard problems |
| **Hierarchy (80/15/5)** | **~$19** | Best of all worlds |

The 80/15/5 split:
- 80% routine tasks on Tier 1 (~$6)
- 15% moderate tasks on Tier 2 (~$7)
- 5% complex tasks on Tier 3 (~$6)

**Result: 10x cost reduction vs pure premium, with equivalent quality on complex tasks.**

## Integration Examples

### OpenClaw

```yaml
# config.yml - set default model
model: anthropic/claude-sonnet-4

# In session, switch models
/model opus  # upgrade for complex task
/model deepseek  # downgrade for routine

# Spawn sub-agent on cheap model
sessions_spawn:
  task: "Fetch and parse these 50 URLs"
  model: deepseek
```

**OpenRouter (Tier 1 with vision or text-only):**

```yaml
# Tier 1 with vision — Kimi K2.5 (multimodal)
model: openrouter/moonshotai/kimi-k2.5
# Heartbeats, cron, image-involving tasks: K2.5 handles text and vision.

# Tier 1 text-only — GLM 5 (no vision)
# model: openrouter/z-ai/glm-5  # exact ID TBD on OpenRouter Z.AI
# Routine text-only only; for image tasks use Kimi K2.5 or another vision-capable model.
```

### Claude Code

```
# In CLAUDE.md or project instructions
When spawning background agents, use claude-3-haiku for:
- File operations
- Simple searches  
- Status checks

Reserve claude-sonnet-4 for:
- Code generation
- Analysis tasks
```

### General Agent Systems

```python
def get_model_for_task(task_description: str) -> str:
    routine_signals = ['read', 'fetch', 'check', 'list', 'format', 'status']
    complex_signals = ['debug', 'architect', 'design', 'security', 'why']
    
    desc_lower = task_description.lower()
    
    if any(signal in desc_lower for signal in complex_signals):
        return "claude-opus-4"
    elif any(signal in desc_lower for signal in routine_signals):
        return "deepseek-v3"
    else:
        return "claude-sonnet-4"
```

## Anti-Patterns

**DON'T:**
- Run heartbeats on Opus
- Use premium models for file I/O
- Keep expensive model when task is clearly routine
- Spawn sub-agents on premium models by default
- Use GLM 5 (or any text-only Tier 1/2 model) for image/vision tasks — e.g. photo analysis, screenshot understanding, image-generation skills, or any tool that takes image input

**DO:**
- Start mid-tier, adjust based on task
- Spawn helpers on cheapest viable model
- Escalate explicitly when stuck
- Track cost per task type to optimize further

## Extending This Skill

To customize for your use case:

1. **Adjust tier definitions** based on your provider/budget
2. **Add domain-specific signals** to classification rules
3. **Track actual complexity** vs predicted to improve heuristics
4. **Set budget alerts** to catch runaway premium usage
