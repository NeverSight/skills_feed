---
name: letta-development-guide
description: Comprehensive guide for developing Letta agents, including architecture selection, memory design, model selection, and tool configuration. Use when building or troubleshooting Letta agents.
license: MIT
---

# Letta Development Guide

Comprehensive guide for designing and building effective Letta agents with appropriate architectures, memory configurations, model selection, and tool setups.

## When to Use This Skill

Use this skill when:
- Starting a new Letta agent project
- Choosing between agent architectures (letta_v1_agent vs memgpt_v2_agent)
- Designing memory block structure and architecture
- Selecting appropriate models for your use case
- Planning tool configurations
- Optimizing memory management and performance
- Implementing shared memory between agents
- Debugging memory-related issues

## Quick Start Guide

### Minimal Working Example

```python
from letta_client import Letta

client = Letta()
agent = client.agents.create(
    name="my-assistant",
    model="openai/gpt-4o",
    embedding="openai/text-embedding-3-small",
    memory_blocks=[
        {"label": "persona", "value": "You are a helpful assistant."},
        {"label": "human", "value": "The user's name and preferences."},
    ],
)

# Send a message
response = client.agents.messages.create(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.messages[-1].content)
```

### 1. Architecture Selection

**Use letta_v1_agent when:**
- Building new agents (recommended default)
- Need compatibility with reasoning models (GPT-4o, Claude Sonnet 4)
- Want simpler system prompts and direct message generation

**Use memgpt_v2_agent when:**
- Maintaining legacy agents
- Require specific tool patterns not yet supported in v1

For detailed comparison, see `references/architectures.md`.

### 2. Memory Architecture Design

Memory is the foundation of effective agents. Letta provides three memory types:

**Core Memory (in-context):**
- Always accessible in agent's context window
- Use for: current state, active context, frequently referenced information
- Limit: Keep total core memory under 80% of context window

**Archival Memory (out-of-context):**
- Semantic search over vector database
- Use for: historical records, large knowledge bases, past interactions
- Access: Agent must explicitly call archival_memory_search
- Note: NOT automatically populated from context overflow

**Conversation History:**
- Past messages from current conversation
- Retrieved via conversation_search tool
- Use for: referencing earlier discussion, tracking conversation flow

See `references/memory-architecture.md` for detailed guidance.

### 3. Memory Block Design

**Core principle:** One block per distinct functional unit.

**Essential blocks:**
- `persona`: Agent identity, behavioral guidelines, capabilities
- `human`: User information, preferences, context

**Add domain-specific blocks based on use case:**
- Customer support: `company_policies`, `product_knowledge`, `customer`
- Coding assistant: `project_context`, `coding_standards`, `current_task`
- Personal assistant: `schedule`, `preferences`, `contacts`

**Memory block guidelines:**
- Keep blocks focused and purpose-specific
- Use clear, instructional descriptions
- Monitor size limits (typically 2000-5000 characters per block)
- Design for append operations when sharing memory between agents

See `references/memory-patterns.md` for domain examples and `references/description-patterns.md` for writing effective descriptions.

### 4. Model Selection

Match model capabilities to agent requirements:

**For production agents:**
- GPT-4o or Claude Sonnet 4 for complex reasoning
- GPT-4o-mini for cost-efficient general tasks
- Claude Haiku 3.5 for fast, lightweight operations
- Gemini 2.0 Flash for balanced speed/capability

**Avoid for production:**
- Small Ollama models (<7B parameters) - poor tool calling
- Models without reliable function calling support

See `references/model-recommendations.md` for detailed guidance.

### 5. Tool Configuration

**Start minimal:** Attach only tools the agent will actively use.

**Common starting points:**
- **Memory tools** (memory_insert, memory_replace, memory_rethink): Core for most agents
- **File system tools**: Auto-attached when folders are connected
- **Custom tools**: For domain-specific operations (databases, APIs, etc.)

**Tool Rules:** Use to enforce sequencing when needed (e.g., "always call search before answer")

Consult `references/tool-patterns.md` for common configurations.

## Advanced Topics

### Memory Size Management

**When approaching character limits:**
1. **Split by topic:** `customer_profile` → `customer_business`, `customer_preferences`
2. **Split by time:** `interaction_history` → `recent_interactions`, archive older to archival memory
3. **Archive historical data:** Move old information to archival memory
4. **Consolidate with memory_rethink:** Summarize and rewrite block

See `references/size-management.md` for strategies.

### Concurrency Patterns

When multiple agents share memory blocks or an agent processes concurrent requests:

**Safest operations:**
- `memory_insert`: Append-only, minimal race conditions
- Database uses PostgreSQL row-level locking

**Risk of race conditions:**
- `memory_replace`: Target string may change before write
- `memory_rethink`: Last-writer-wins, no merge

**Best practices:**
- Design for append operations when possible
- Use memory_insert for concurrent writes
- Reserve memory_rethink for single-agent exclusive access

Consult `references/concurrency.md` for detailed patterns.

## Validation Checklist

Before finalizing your agent design:

**Architecture:**
- [ ] Does the architecture match the model's capabilities?
- [ ] Is the model appropriate for expected workload and latency requirements?

**Memory:**
- [ ] Is core memory total under 80% of context window?
- [ ] Is each block focused on one functional area?
- [ ] Are descriptions clear about when to read/write?
- [ ] Have you planned for size growth and overflow?
- [ ] If multi-agent, are concurrency patterns considered?

**Tools:**
- [ ] Are tools necessary and properly configured?
- [ ] Are memory blocks granular enough for effective updates?

## Common Antipatterns

**Too few memory blocks:**
```yaml
# Bad: Everything in one block
agent_memory: "Agent is helpful. User is John..."
```
Split into focused blocks instead.

**Too many memory blocks:**
Creating 10+ blocks when 3-4 would suffice. Start minimal, expand as needed.

**Poor descriptions:**
```yaml
# Bad
data: "Contains data"
```
Provide actionable guidance instead. See `references/description-patterns.md`.

**Ignoring size limits:**
Letting blocks grow indefinitely until they hit limits. Monitor and manage proactively.

## Implementation Steps

### 1. Design Phase
- Choose architecture based on requirements
- Design memory block structure
- Select appropriate model
- Plan tool configuration

### 2. Creation Phase (SDK)

**Python:**
```python
from letta_client import Letta

client = Letta()  # Uses LETTA_API_KEY env var

# Create agent with custom memory blocks
agent = client.agents.create(
    name="my-agent",
    model="openai/gpt-4o",  # or "anthropic/claude-sonnet-4-20250514"
    embedding="openai/text-embedding-3-small",
    memory_blocks=[
        {"label": "persona", "value": "You are a helpful assistant..."},
        {"label": "human", "value": "User preferences and context..."},
        {"label": "project", "value": "Current project details..."},
    ],
    description="Agent for helping with X",
)
print(f"Created agent: {agent.id}")
```

**TypeScript:**
```typescript
import Letta from "letta-client";

const client = new Letta();

const agent = await client.agents.create({
  name: "my-agent",
  model: "openai/gpt-4o",
  embedding: "openai/text-embedding-3-small",
  memoryBlocks: [
    { label: "persona", value: "You are a helpful assistant..." },
    { label: "human", value: "User preferences and context..." },
    { label: "project", value: "Current project details..." },
  ],
  description: "Agent for helping with X",
});
console.log(`Created agent: ${agent.id}`);
```

**Note:** Letta Code CLI (`letta` command) creates agents interactively. Use `letta --new-agent` to start fresh, then `/rename` and `/description` to configure.

### 3. Testing Phase
- Test with representative queries
- Monitor memory tool usage patterns
- Verify tool calling behavior

### 4. Iteration Phase
- Refine memory block structure based on actual usage
- Optimize system instructions
- Adjust tool configurations

## References

For detailed information on specific topics, consult the reference materials:

- `references/architectures.md` - Architecture comparison and selection
- `references/memory-architecture.md` - Memory types and when to use them
- `references/memory-patterns.md` - Domain-specific memory block examples
- `references/description-patterns.md` - Writing effective block descriptions
- `references/size-management.md` - Managing memory block size limits
- `references/concurrency.md` - Multi-agent memory sharing patterns
- `references/model-recommendations.md` - Model selection guidance
- `references/tool-patterns.md` - Common tool configurations
