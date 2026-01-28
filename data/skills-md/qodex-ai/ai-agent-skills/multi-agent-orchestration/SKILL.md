---
name: multi-agent-orchestration
description: Design and coordinate multi-agent systems where specialized agents work together to solve complex problems. Covers agent communication, task delegation, workflow orchestration, and result aggregation. Use when building coordinated agent teams, complex workflows, or systems requiring specialized expertise across domains.
---

# Multi-Agent Orchestration

Design and orchestrate sophisticated multi-agent systems where specialized agents collaborate to solve complex problems, combining different expertise and perspectives.

## Quick Start

Get started with multi-agent implementations in the examples and utilities:

- **Examples**: See [`examples/`](examples/) directory for complete implementations:
  - [`orchestration_patterns.py`](examples/orchestration_patterns.py) - Sequential, parallel, hierarchical, and consensus orchestration
  - [`framework_implementations.py`](examples/framework_implementations.py) - Templates for CrewAI, AutoGen, LangGraph, and Swarm

- **Utilities**: See [`scripts/`](scripts/) directory for helper modules:
  - [`agent_communication.py`](scripts/agent_communication.py) - Message broker, shared memory, and communication protocols
  - [`workflow_management.py`](scripts/workflow_management.py) - Workflow execution, optimization, and monitoring
  - [`benchmarking.py`](scripts/benchmarking.py) - Team performance and agent effectiveness metrics

## Overview

Multi-agent systems decompose complex problems into specialized sub-tasks, assigning each to an agent with relevant expertise, then coordinating their work toward a unified goal.

### When Multi-Agent Systems Shine

- **Complex Workflows**: Tasks requiring multiple specialized roles
- **Domain-Specific Expertise**: Finance, legal, HR, engineering need different knowledge
- **Parallel Processing**: Multiple agents work on different aspects simultaneously
- **Collaborative Reasoning**: Agents debate, refine, and improve solutions
- **Resilience**: Failures in one agent don't break the entire system
- **Scalability**: Easy to add new specialized agents

### Architecture Overview

```
User Request
    ↓
Orchestrator
    ├→ Agent 1 (Specialist) → Task 1
    ├→ Agent 2 (Specialist) → Task 2
    ├→ Agent 3 (Specialist) → Task 3
    ↓
Result Aggregator
    ↓
Final Response
```

## Core Concepts

### Agent Definition

An agent is defined by:
- **Role**: What responsibility does it have? (e.g., "Financial Analyst")
- **Goal**: What should it accomplish? (e.g., "Analyze financial risks")
- **Expertise**: What knowledge/tools does it have?
- **Tools**: What capabilities can it access?
- **Context**: What information does it need to work effectively?

### Orchestration Patterns

#### 1. Sequential Orchestration
- Agents work one after another
- Each agent uses output from previous agent
- **Use Case**: Steps must follow order (research → analysis → writing)

#### 2. Parallel Orchestration
- Multiple agents work simultaneously
- Results aggregated at the end
- **Use Case**: Independent tasks (analyze competitors, market, users)

#### 3. Hierarchical Orchestration
- Senior agent delegates to junior agents
- Manager coordinates flow
- **Use Case**: Large projects with oversight

#### 4. Consensus-Based Orchestration
- Multiple agents analyze problem
- Debate and refine ideas
- Vote or reach consensus
- **Use Case**: Complex decisions needing multiple perspectives

#### 5. Tool-Mediated Orchestration
- Agents use shared tools/databases
- Minimal direct communication
- **Use Case**: Large systems, indirect coordination

## Multi-Agent Team Examples

### Finance Team

```
Coordinator Agent
    ├→ Market Analyst Agent
    │   ├ Tools: Market data API, financial news
    │   └ Task: Analyze market conditions
    ├→ Financial Analyst Agent
    │   ├ Tools: Financial statements, ratio calculations
    │   └ Task: Analyze company financials
    ├→ Risk Manager Agent
    │   ├ Tools: Risk models, scenario analysis
    │   └ Task: Assess investment risks
    └→ Report Writer Agent
        ├ Tools: Document generation
        └ Task: Synthesize findings into report
```

### Legal Team

```
Case Manager Agent (Coordinator)
    ├→ Contract Analyzer Agent
    │   └ Task: Review contract terms
    ├→ Precedent Research Agent
    │   └ Task: Find relevant case law
    ├→ Risk Assessor Agent
    │   └ Task: Identify legal risks
    └→ Document Drafter Agent
        └ Task: Prepare legal documents
```

### Customer Support Team

```
Support Coordinator
    ├→ Issue Classifier Agent
    │   └ Task: Categorize customer issue
    ├→ Knowledge Base Agent
    │   └ Task: Find relevant documentation
    ├→ Escalation Agent
    │   └ Task: Determine if human escalation needed
    └→ Solution Synthesizer Agent
        └ Task: Prepare comprehensive response
```

## Implementation Frameworks

### 1. CrewAI

**Best For**: Teams with clear roles and hierarchical structure

```python
from crewai import Agent, Task, Crew

# Define agents
analyst = Agent(
    role="Financial Analyst",
    goal="Analyze financial data and provide insights",
    backstory="Expert in financial markets with 10+ years experience"
)

researcher = Agent(
    role="Market Researcher",
    goal="Research market trends and competition",
    backstory="Data-driven researcher specializing in market analysis"
)

# Define tasks
analysis_task = Task(
    description="Analyze Q3 financial results for {company}",
    agent=analyst,
    tools=[financial_tool, data_tool]
)

research_task = Task(
    description="Research competitive landscape in {market}",
    agent=researcher,
    tools=[web_search_tool, industry_data_tool]
)

# Create crew and execute
crew = Crew(
    agents=[analyst, researcher],
    tasks=[analysis_task, research_task],
    process=Process.sequential
)

result = crew.kickoff(inputs={"company": "TechCorp", "market": "AI"})
```

### 2. AutoGen (Microsoft)

**Best For**: Complex multi-turn conversations and negotiations

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Define agents
analyst = AssistantAgent(
    name="analyst",
    system_message="You are a financial analyst..."
)

researcher = AssistantAgent(
    name="researcher",
    system_message="You are a market researcher..."
)

# Create group chat
groupchat = GroupChat(
    agents=[analyst, researcher],
    messages=[],
    max_round=10,
    speaker_selection_method="auto"
)

# Manage group conversation
manager = GroupChatManager(groupchat=groupchat)

# User proxy to initiate conversation
user = UserProxyAgent(name="user")

# Have conversation
user.initiate_chat(
    manager,
    message="Analyze if Company X should invest in Y market"
)
```

### 3. LangGraph

**Best For**: Complex workflows with state management

```python
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import create_agent_executor

# Define state
class AgentState:
    research_findings: str
    analysis: str
    recommendations: str

# Create graph
graph = StateGraph(AgentState)

# Add nodes for each agent
graph.add_node("researcher", research_agent)
graph.add_node("analyst", analyst_agent)
graph.add_node("writer", writer_agent)

# Define edges (workflow)
graph.add_edge("researcher", "analyst")
graph.add_edge("analyst", "writer")

# Set entry/exit points
graph.set_entry_point("researcher")
graph.set_finish_point("writer")

# Compile and run
workflow = graph.compile()
result = workflow.invoke({"topic": "AI trends"})
```

### 4. OpenAI Swarm

**Best For**: Simple agent handoffs and conversational workflows

```python
from swarm import Agent, Swarm

# Define agents
triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine which specialist to route the customer to"
)

billing_agent = Agent(
    name="Billing Specialist",
    instructions="Handle billing and payment questions"
)

technical_agent = Agent(
    name="Technical Support",
    instructions="Handle technical issues"
)

# Define handoff functions
def route_to_billing(reason: str):
    return billing_agent

def route_to_technical(reason: str):
    return technical_agent

# Add tools to triage agent
triage_agent.functions = [route_to_billing, route_to_technical]

# Execute swarm
client = Swarm()
response = client.run(
    agent=triage_agent,
    messages=[{"role": "user", "content": "I have a billing question"}]
)
```

## Orchestration Patterns

### Pattern 1: Sequential Task Chain

Agents execute tasks in sequence, each building on previous results:

```python
# Task 1: Research
research_output = research_agent.work("Analyze AI market trends")

# Task 2: Analysis (uses research output)
analysis = analyst_agent.work(f"Analyze these findings: {research_output}")

# Task 3: Report (uses analysis)
report = writer_agent.work(f"Write report on: {analysis}")
```

**When to Use**: Steps have dependencies, each builds on previous

### Pattern 2: Parallel Execution

Multiple agents work simultaneously, results combined:

```python
import asyncio

async def parallel_teams():
    # All agents work in parallel
    market_task = market_agent.work_async("Analyze market")
    technical_task = tech_agent.work_async("Analyze technology")
    user_task = user_agent.work_async("Analyze user needs")

    # Wait for all to complete
    market_results, tech_results, user_results = await asyncio.gather(
        market_task, technical_task, user_task
    )

    # Synthesize results
    return synthesize(market_results, tech_results, user_results)
```

**When to Use**: Independent analyses, need quick results, want diversity

### Pattern 3: Hierarchical Structure

Manager agent coordinates specialists:

```python
manager_agent.orchestrate({
    "market_analysis": {
        "agents": [competitor_analyst, trend_analyst],
        "task": "Comprehensive market analysis"
    },
    "technical_evaluation": {
        "agents": [architecture_agent, security_agent],
        "task": "Technical feasibility assessment"
    },
    "synthesis": {
        "agents": [strategy_agent],
        "task": "Create strategic recommendations"
    }
})
```

**When to Use**: Clear hierarchy, different teams, complex coordination

### Pattern 4: Debate & Consensus

Multiple agents discuss and reach consensus:

```python
agents = [bull_agent, bear_agent, neutral_agent]
question = "Should we invest in this startup?"

# Debate round 1
arguments = {agent: agent.argue(question) for agent in agents}

# Debate round 2 (respond to others)
counter_arguments = {
    agent: agent.respond(arguments) for agent in agents
}

# Reach consensus
consensus = mediator_agent.synthesize_consensus(counter_arguments)
```

**When to Use**: Complex decisions, need multiple perspectives, risk assessment

## Agent Communication Patterns

### 1. Direct Communication
Agents pass messages directly to each other:

```python
agent_a.send_message(agent_b, {
    "type": "request",
    "action": "analyze_document",
    "document": doc_content,
    "context": {"deadline": "urgent"}
})
```

### 2. Tool-Mediated Communication
Agents use shared tools/databases:

```python
# Agent A writes to shared memory
shared_memory.write("findings", {"market_size": "$5B", "growth": "20%"})

# Agent B reads from shared memory
findings = shared_memory.read("findings")
```

### 3. Manager-Based Communication
Central coordinator manages agent communication:

```python
manager.broadcast("update_all_agents", {
    "new_deadline": "tomorrow",
    "priority": "critical"
})
```

## Best Practices

### Agent Design
- ✓ Clear, specific role and goal
- ✓ Appropriate tools for the role
- ✓ Relevant background/expertise
- ✓ Distinct from other agents
- ✓ Reasonable scope of work

### Workflow Design
- ✓ Clear task dependencies
- ✓ Identified handoff points
- ✓ Error handling between agents
- ✓ Fallback strategies
- ✓ Performance monitoring

### Communication
- ✓ Structured message formats
- ✓ Clear context sharing
- ✓ Error propagation strategy
- ✓ Timeout handling
- ✓ Audit logging

### Orchestration
- ✓ Define process clearly (sequential, parallel, etc.)
- ✓ Set clear success criteria
- ✓ Monitor agent performance
- ✓ Implement feedback loops
- ✓ Allow human intervention points

## Common Challenges & Solutions

### Challenge: Agent Conflicts
**Solutions**:
- Clear role separation
- Explicit decision-making rules
- Consensus mechanisms
- Conflict resolution agent
- Clear authority hierarchy

### Challenge: Slow Execution
**Solutions**:
- Use parallel execution where possible
- Cache results from expensive operations
- Pre-process data
- Optimize agent logic
- Implement timeout handling

### Challenge: Poor Quality Results
**Solutions**:
- Better agent prompts/instructions
- More relevant tools
- Feedback integration
- Quality validation agents
- Result aggregation strategies

### Challenge: Complex Workflows
**Solutions**:
- Break into smaller teams
- Hierarchical structure
- Clear task definitions
- Good state management
- Documentation of workflow

## Evaluation Metrics

**Team Performance**:
- Task completion rate
- Quality of results
- Execution time
- Cost (tokens/API calls)
- Error rate

**Agent Effectiveness**:
- Task success rate
- Response quality
- Tool usage efficiency
- Communication clarity
- Collaboration score

## Advanced Techniques

### 1. Self-Organizing Teams
Agents autonomously decide roles and workflow:

```python
# Agents negotiate roles based on task
agents = [agent1, agent2, agent3]
task = "complex financial analysis"

# Agents determine best structure
negotiated_structure = self_organize(agents, task)
# Returns optimal workflow for this task
```

### 2. Adaptive Workflows
Workflow changes based on progress:

```python
# Monitor progress
if progress < expected_rate:
    # Increase resources
    workflow.add_agent(specialist_agent)
elif quality < threshold:
    # Increase validation
    workflow.insert_review_step()
```

### 3. Cross-Agent Learning
Agents learn from each other's work:

```python
# After team execution
execution_trace = crew.get_execution_trace()

# Extract learnings
learnings = extract_patterns(execution_trace)

# Update agent knowledge
for agent, learning in learnings.items():
    agent.update_knowledge(learning)
```

## Resources

### Frameworks
- **CrewAI**: https://crewai.com/
- **AutoGen**: https://microsoft.github.io/autogen/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Swarm**: https://github.com/openai/swarm

### Papers
- "Generative Agents" (Park et al.)
- "Self-Organizing Multi-Agent Systems" (research papers)

## Implementation Checklist

- [ ] Define each agent's role, goal, and expertise
- [ ] Identify available tools/capabilities for each agent
- [ ] Plan workflow (sequential, parallel, hierarchical)
- [ ] Define communication patterns
- [ ] Implement task definitions
- [ ] Set success criteria for each task
- [ ] Add error handling and fallbacks
- [ ] Implement monitoring/logging
- [ ] Test team collaboration
- [ ] Evaluate quality and performance
- [ ] Optimize based on results
- [ ] Document workflow and decisions

## Getting Started

1. **Start Small**: Begin with 2-3 agents
2. **Clear Workflow**: Document how agents interact
3. **Test Thoroughly**: Validate agent behavior individually and together
4. **Monitor Closely**: Track performance and results
5. **Iterate**: Refine based on results
6. **Scale**: Add agents and complexity as needed

