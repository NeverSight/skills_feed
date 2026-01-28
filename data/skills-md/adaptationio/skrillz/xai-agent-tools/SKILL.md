---
name: xai-agent-tools
description: xAI Agent Tools API for autonomous tool calling with X search, web search, and code execution. Use when building agents that need real-time data access and autonomous task execution.
version: 1.0.0
---

# xAI Agent Tools API

Server-side agentic tool calling that enables Grok to autonomously search, analyze, and execute code.

## Overview

The Agent Tools API manages the entire reasoning and tool-execution loop on the server side, unlike traditional tool-calling where clients must handle each invocation.

**Available Tools:**
- `x_search` - Search Twitter/X posts
- `web_search` - Real-time web search
- `code_execution` - Python sandbox
- `document_search` - Search uploaded documents

## Quick Start

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# Agent with automatic tool use
response = client.chat.completions.create(
    model="grok-4-1-fast",
    messages=[{
        "role": "user",
        "content": "Search X for Tesla news, then search the web for Tesla stock price, and calculate the sentiment score"
    }]
)
print(response.choices[0].message.content)
```

## Tool Configurations

### X Search Tool
```python
x_search_config = {
    "type": "x_search",
    "x_search": {
        "enabled": True,
        "allowed_x_handles": ["elonmusk", "Tesla"],  # Max 10
        "excluded_x_handles": [],  # Cannot use with allowed
        "date_range": {
            "start": "2025-12-01",  # ISO8601
            "end": "2025-12-05"
        },
        "include_media": True  # Analyze images/videos
    }
}
```

### Web Search Tool
```python
web_search_config = {
    "type": "web_search",
    "web_search": {
        "enabled": True,
        "search_depth": "comprehensive",  # or "quick"
        "include_domains": ["reuters.com", "bloomberg.com"],
        "exclude_domains": ["spam.com"]
    }
}
```

### Code Execution Tool
```python
code_execution_config = {
    "type": "code_execution",
    "code_execution": {
        "enabled": True,
        "language": "python",
        "timeout": 30  # seconds
    }
}
```

## Agent Patterns

### Research Agent
```python
def research_agent(query: str) -> str:
    """Agent that searches both X and web for comprehensive research."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""You are a research agent. For the query: "{query}"

            1. Search X for real-time social discussion
            2. Search the web for news and analysis
            3. Synthesize findings into a comprehensive report

            Include:
            - Key findings from X
            - Key findings from web
            - Sentiment analysis
            - Recommendations"""
        }]
    )
    return response.choices[0].message.content
```

### Analysis Agent
```python
def analysis_agent(data: str, analysis_type: str) -> str:
    """Agent that uses code execution for analysis."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze this data using Python:

            Data: {data}
            Analysis type: {analysis_type}

            Use code execution to:
            1. Parse the data
            2. Perform statistical analysis
            3. Generate insights
            4. Create visualizations if helpful

            Return the analysis results."""
        }]
    )
    return response.choices[0].message.content
```

### Financial Agent
```python
def financial_agent(ticker: str) -> str:
    """Comprehensive financial analysis agent."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""You are a financial analyst agent. Analyze ${ticker}:

            1. Search X for:
               - Retail sentiment
               - Influencer opinions
               - Breaking news

            2. Search web for:
               - Recent news articles
               - Analyst ratings
               - Earnings reports

            3. Use code execution to:
               - Calculate sentiment score
               - Analyze mention velocity
               - Generate summary statistics

            Return a comprehensive investment report with:
            - Overall sentiment
            - Key catalysts
            - Risk factors
            - Trading recommendation"""
        }]
    )
    return response.choices[0].message.content
```

### Multi-Step Agent
```python
def multi_step_agent(objective: str) -> str:
    """Agent that breaks down and executes complex tasks."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Objective: {objective}

            You have access to:
            - X search (real-time social data)
            - Web search (news and information)
            - Code execution (Python analysis)

            Process:
            1. Break down the objective into steps
            2. Execute each step using appropriate tools
            3. Synthesize results
            4. Provide actionable insights

            Think step by step and use tools as needed."""
        }]
    )
    return response.choices[0].message.content
```

## Tool Cost Management

| Tool | Cost per 1,000 calls |
|------|---------------------|
| X Search | $5.00 |
| Web Search | $5.00 |
| Code Execution | $5.00 |
| Document Search | $2.50 |

### Cost-Optimized Agent
```python
def cost_optimized_agent(query: str, max_tool_calls: int = 3) -> str:
    """Agent with tool call limits for cost control."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Query: {query}

            IMPORTANT: Minimize tool usage. You have a budget of {max_tool_calls} tool calls.
            - Only use tools when essential
            - Combine related searches
            - Prefer single comprehensive searches

            Provide the best answer within this constraint."""
        }]
    )
    return response.choices[0].message.content
```

## Error Handling

```python
def robust_agent(query: str) -> dict:
    """Agent with comprehensive error handling."""
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast",
            messages=[{"role": "user", "content": query}],
            timeout=60
        )

        return {
            "success": True,
            "result": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
```

## Streaming Responses

```python
def streaming_agent(query: str):
    """Agent with streaming output."""
    stream = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{"role": "user", "content": query}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
```

## Conversation Context

```python
class ConversationalAgent:
    """Agent that maintains conversation history."""

    def __init__(self):
        self.messages = []

    def add_system_prompt(self, prompt: str):
        self.messages.append({"role": "system", "content": prompt})

    def chat(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="grok-4-1-fast",
            messages=self.messages
        )

        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

# Usage
agent = ConversationalAgent()
agent.add_system_prompt("You are a financial analyst with access to X and web search.")
print(agent.chat("What's the sentiment on AAPL?"))
print(agent.chat("Compare that to MSFT"))
```

## Best Practices

1. **Use grok-4-1-fast** - Optimized for tool calling
2. **Be specific** - Clear instructions reduce unnecessary tool calls
3. **Set limits** - Control costs with tool call budgets
4. **Handle errors** - Tools can fail, plan for it
5. **Stream for UX** - Use streaming for long responses
6. **Cache results** - Don't repeat identical searches

## Model Selection for Agents

| Model | Tool Calling | Speed | Cost |
|-------|--------------|-------|------|
| grok-4-1-fast | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| grok-4 | ⭐⭐ | ⭐ | ⭐ |
| grok-3-fast | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

## Related Skills
- `xai-x-search` - X search details
- `xai-sentiment` - Sentiment analysis
- `xai-stock-sentiment` - Stock analysis

## References
- [Agent Tools API](https://x.ai/news/grok-4-1-fast/)
- [Tools Overview](https://docs.x.ai/docs/guides/tools/overview)
- [Function Calling](https://docs.x.ai/docs/guides/function-calling)
