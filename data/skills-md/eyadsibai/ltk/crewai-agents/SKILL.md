---
name: crewai-agents
description: Use when "CrewAI", "multi-agent systems", "agent orchestration", "AI crews", or asking about "autonomous agents", "agent collaboration", "role-based agents", "agent workflows", "AI team coordination"
version: 1.0.0
---

<!-- Adapted from: AI-research-SKILLs/14-agents/crewai -->

# CrewAI Multi-Agent Orchestration

Build teams of autonomous AI agents that collaborate on complex tasks.

## When to Use

- Building multi-agent systems with specialized roles
- Need autonomous collaboration between agents
- Want role-based task delegation (researcher, writer, analyst)
- Require sequential or hierarchical process execution
- Building production workflows with memory and observability

## Quick Start

```bash
pip install crewai
pip install 'crewai[tools]'  # With 50+ built-in tools
```

### Simple Crew

```python
from crewai import Agent, Task, Crew, Process

# Define agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Discover cutting-edge developments in AI",
    backstory="You are an expert analyst with a keen eye for trends.",
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear, engaging content about technical topics",
    backstory="You excel at explaining complex concepts.",
    verbose=True
)

# Define tasks
research_task = Task(
    description="Research the latest developments in {topic}. Find 5 key trends.",
    expected_output="A detailed report with 5 bullet points.",
    agent=researcher
)

write_task = Task(
    description="Write a blog post based on the research findings.",
    expected_output="A 500-word blog post in markdown format.",
    agent=writer,
    context=[research_task]  # Uses research output
)

# Create and run crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff(inputs={"topic": "AI Agents"})
print(result.raw)
```

## Process Types

### Sequential

Tasks execute in order:

```python
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential  # Task 1 -> Task 2 -> Task 3
)
```

### Hierarchical

Auto-creates a manager agent that delegates:

```python
crew = Crew(
    agents=[researcher, writer, analyst],
    tasks=[research_task, write_task, analyze_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o"
)
```

## Using Tools

```python
from crewai_tools import (
    SerperDevTool,       # Web search
    ScrapeWebsiteTool,   # Web scraping
    FileReadTool,        # Read files
    PDFSearchTool,       # Search PDFs
)

researcher = Agent(
    role="Researcher",
    goal="Find accurate information",
    backstory="Expert at finding data online.",
    tools=[SerperDevTool(), ScrapeWebsiteTool()]
)
```

### Custom Tools

```python
from crewai.tools import BaseTool

class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = "Performs mathematical calculations."

    def _run(self, expression: str) -> str:
        try:
            return f"Result: {eval(expression)}"
        except Exception as e:
            return f"Error: {str(e)}"
```

## YAML Configuration

### agents.yaml

```yaml
researcher:
  role: "{topic} Senior Data Researcher"
  goal: "Uncover cutting-edge developments in {topic}"
  backstory: >
    You're a seasoned researcher with a knack for uncovering
    the latest developments in {topic}.

reporting_analyst:
  role: "Reporting Analyst"
  goal: "Create detailed reports based on research data"
  backstory: >
    You're a meticulous analyst who transforms raw data into
    actionable insights.
```

### tasks.yaml

```yaml
research_task:
  description: >
    Conduct thorough research about {topic}.
    Find the most relevant information for {year}.
  expected_output: >
    A list with 10 bullet points of the most relevant
    information about {topic}.
  agent: researcher

reporting_task:
  description: >
    Review the research and create a comprehensive report.
  expected_output: >
    A detailed report in markdown format.
  agent: reporting_analyst
  output_file: report.md
```

## Memory System

```python
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    memory=True,  # Enable memory
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)
```

## LLM Providers

```python
from crewai import LLM

llm = LLM(model="gpt-4o")  # OpenAI
llm = LLM(model="claude-sonnet-4-5-20250929")  # Anthropic
llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")  # Local

agent = Agent(role="Analyst", goal="Analyze data", llm=llm)
```

## Best Practices

1. **Clear roles** - Each agent should have a distinct specialty
2. **YAML config** - Better organization for larger projects
3. **Enable memory** - Improves context across tasks
4. **Set max_iter** - Prevent infinite loops (default 15)
5. **Limit tools** - 3-5 tools per agent max
6. **Rate limiting** - Set max_rpm to avoid API limits

## Common Issues

**Agent stuck in loop:**

```python
agent = Agent(
    role="...",
    max_iter=10,
    max_rpm=5
)
```

**Task not using context:**

```python
task2 = Task(
    description="...",
    context=[task1],  # Explicitly pass context
    agent=writer
)
```

## vs Alternatives

| Feature | CrewAI | LangChain | LangGraph |
|---------|--------|-----------|-----------|
| Best for | Multi-agent teams | General LLM apps | Stateful workflows |
| Learning curve | Low | Medium | Higher |
| Agent paradigm | Role-based | Tool-based | Graph-based |

## Resources

- GitHub: <https://github.com/crewAIInc/crewAI>
- Docs: <https://docs.crewai.com>
- Tools: <https://github.com/crewAIInc/crewAI-tools>
