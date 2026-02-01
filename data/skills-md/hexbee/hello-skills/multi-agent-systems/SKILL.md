---
name: multi-agent-systems
description: "Design and implement multi-agent LLM architectures using the orchestrator-subagent pattern. Use when: (1) Deciding whether to use multi-agent vs single-agent systems, (2) Implementing context isolation for high-volume operations, (3) Parallelizing independent research tasks, (4) Creating specialized agents with focused tool sets, (5) Building verification subagents for quality assurance, or (6) Analyzing context-centric decomposition boundaries."
---

# Multi-Agent Systems

## When to Use Multi-Agent Architectures

Multi-agent systems introduce overhead. Every additional agent represents another potential point of failure, another set of prompts to maintain, and another source of unexpected behavior.

**Multi-agent systems use 3-10x more tokens than single-agent approaches** due to:
- Duplicating context across agents
- Coordination messages between agents
- Summarizing results for handoffs

### Start with a Single Agent

A well-designed single agent with appropriate tools can accomplish far more than expected. Use single agent when:
- Tasks are sequential and context-dependent
- Tool count is under 15-20
- No clear benefit from parallelization

### Three Cases Where Multi-Agent Excels

1. **Context pollution** - Subtasks generate >1000 tokens but most info is irrelevant to main task
2. **Parallelization** - Tasks can run independently and explore larger search space
3. **Specialization** - Different tasks need different tools, prompts, or domain expertise

## Decision Framework

### Context Protection Pattern

Use when subtasks generate large context but only summary is needed for main task.

**Example: Customer Support**
```python
class OrderLookupAgent:
    def lookup_order(self, order_id: str) -> dict:
        messages = [{"role": "user", "content": f"Get essential details for order {order_id}"}]
        response = client.messages.create(
            model="claude-sonnet-4-5", max_tokens=1024,
            messages=messages, tools=[get_order_details_tool]
        )
        return extract_summary(response)  # Returns 50-100 tokens, not 2000+

class SupportAgent:
    def handle_issue(self, user_message: str):
        if needs_order_info(user_message):
            order_id = extract_order_id(user_message)
            order_summary = OrderLookupAgent().lookup_order(order_id)
            context = f"Order {order_id}: {order_summary['status']}, purchased {order_summary['date']}"
        # Main agent gets clean context
```

**Best when:**
- Subtask generates >1000 tokens, most irrelevant
- Subtast is well-defined with clear extraction criteria
- Lookup/retrieval operations need filtering before use

### Parallelization Pattern

Use when exploring larger search space or independent research facets.

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def research_topic(query: str) -> dict:
    facets = await lead_agent.decompose_query(query)
    tasks = [research_subagent(facet) for facet in facets]
    results = await asyncio.gather(*tasks)
    return await lead_agent.synthesize(results)

async def research_subagent(facet: str) -> dict:
    messages = [{"role": "user", "content": f"Research: {facet}"}]
    response = await client.messages.create(
        model="claude-sonnet-4-5", max_tokens=4096,
        messages=messages, tools=[web_search, read_document]
    )
    return extract_findings(response)
```

**Benefit:** Thoroughness, not speed. Covers more ground at higher token cost.

### Specialization Patterns

#### Tool Set Specialization

Split by domain when agent has 20+ tools, shows domain confusion, or degraded performance.

**Signs you need specialization:**
1. Quantity: 20+ tools
2. Domain confusion: Tools span unrelated domains
3. Degraded performance: New tools hurt existing tasks

#### System Prompt Specialization

Different tasks require conflicting behavioral modes:
- Customer support: empathetic, patient
- Code review: precise, critical
- Compliance: rigid rule-following
- Brainstorming: creative flexibility

#### Domain Expertise Specialization

Deep domain context that would overwhelm a generalist:
- Legal analysis: case law, regulatory frameworks
- Medical research: clinical trial methodology

### Multi-Platform Integration Example

```python
class CRMAgent:
    system_prompt = """You are a CRM specialist. You manage contacts,
    opportunities, and account records. Always verify record ownership
    before updates and maintain data integrity across related records."""
    tools = [crm_get_contacts, crm_create_opportunity]  # 8-10 CRM tools

class MarketingAgent:
    system_prompt = """You are a marketing automation specialist. You
    manage campaigns, lead scoring, and email sequences."""
    tools = [marketing_get_campaigns, marketing_create_lead]  # 8-10 tools

class OrchestratorAgent:
    def execute(self, user_request: str):
        response = client.messages.create(
            model="claude-sonnet-4-5", max_tokens=1024,
            system="""Route to appropriate specialist:
    - CRM: Contacts, opportunities, accounts, sales pipeline
    - Marketing: Campaigns, lead nurturing, email sequences""",
            messages=[{"role": "user", "content": user_request}],
            tools=[delegate_to_crm, delegate_to_marketing]
        )
        return response
```

## Context-Centric Decomposition

**Problem-centric (counterproductive):** Split by work type (writer, tester, reviewer) - creates coordination overhead, context loss at handoffs.

**Context-centric (effective):** Agent handling a feature also handles its tests - already has necessary context.

### Effective Boundaries
- Independent research paths
- Separate components with clean API contracts
- Blackbox verification

### Problematic Boundaries
- Sequential phases of same work
- Tightly coupled components
- Work requiring shared state

## Verification Subagent Pattern

Dedicated agent for testing/validating main agent's work. Succeeds because verification requires minimal context transfer.

```python
class CodingAgent:
    def implement_feature(self, requirements: str) -> dict:
        response = client.messages.create(
            model="claude-sonnet-4-5", max_tokens=4096,
            messages=[{"role": "user", "content": f"Implement: {requirements}"}],
            tools=[read_file, write_file, list_directory]
        )
        return {"code": response.content, "files_changed": extract_files(response)}

class VerificationAgent:
    def verify_implementation(self, requirements: str, files_changed: list) -> dict:
        messages = [{"role": "user", "content": f"""
Requirements: {requirements}
Files changed: {files_changed}

Run the complete test suite and verify:
1. All existing tests pass
2. New functionality works as specified
3. No obvious errors or security issues

You MUST run: pytest --verbose
Only mark as PASSED if ALL tests pass with no failures.
"""}]
        response = client.messages.create(
            model="claude-sonnet-4-5", max_tokens=4096,
            messages=messages, tools=[run_tests, execute_code, read_file]
        )
        return {"passed": extract_pass_fail(response), "issues": extract_issues(response)}
```

### Mitigate "Early Victory Problem"

Verifier marks passing without thorough testing. Prevention:

- **Concrete criteria:** "Run full test suite" not "make sure it works"
- **Comprehensive checks:** Test multiple scenarios and edge cases
- **Negative tests:** Confirm inputs that should fail do fail
- **Explicit instructions:** "You MUST run the complete test suite"

## Moving Forward Checklist

Before adding multi-agent complexity:

1. [ ] Genuine constraints exist (context limits, parallelization, specialization need)
2. [ ] Decomposition follows context, not problem type
3. [ ] Clear verification points where subagents can validate

**Start with simplest approach that works. Add complexity only when evidence supports it.**

## References

- [Building multi-agent systems: when and how to use them](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
