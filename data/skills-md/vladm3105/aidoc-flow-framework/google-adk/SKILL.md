---
title: "google-adk: Develop agentic software and multi-agent systems using Google ADK in Python"
name: google-adk
description: Develop agentic software and multi-agent systems using Google ADK in Python
tags:
  - sdd-workflow
  - shared-architecture
  - domain-specific
custom_fields:
  layer: null
  artifact_type: null
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: domain-specific
  upstream_artifacts: []
  downstream_artifacts: []
---

# Google Agent Development Kit (ADK) Skill

## Purpose

Provide specialized guidance for developing agentic applications and multi-agent systems using Google's Agent Development Kit (ADK). Enable AI assistants to design agents, build tools, orchestrate multi-agent workflows, implement memory/state management, and deploy agent-based applications following code-first development patterns.

## When to Use This Skill

Invoke this skill when:

- Building conversational AI agents with tool integration
- Creating multi-agent orchestration systems
- Developing workflow agents (sequential, parallel, iterative)
- Implementing custom tools for agents
- Designing agent architectures for complex tasks
- Deploying agent applications to production
- Evaluating agent performance and behavior
- Implementing human-in-the-loop patterns

Do NOT use this skill for:

- Generic Python development (use Python-specific skills)
- Simple REST API development (ADK is for agentic systems)
- Frontend development (ADK is backend agent framework)
- Direct LLM API usage without agent orchestration (use LLM provider SDKs)
- Non-Python agent frameworks (LangChain, CrewAI, AutoGPT - different patterns)

## Core ADK Concepts

### Platform Architecture

**Framework Philosophy:**
- **Code-first approach** - Define agents in Python code (not YAML/JSON configs)
- **Model-agnostic** - Optimized for Gemini but supports other LLMs
- **Composable** - Build complex systems from simple agent primitives
- **Observable** - Built-in integration with tracing and monitoring tools

**Supported Languages:**
- **Python** (primary, most mature) - `google-adk` package
- **Go** (available) - `adk-go` repository
- **Java** (available) - `adk-java` repository

**Runtime Environment:**
- Python 3.9+ required
- Agent Engine for deployment (containerized execution)
- Web UI for development/testing (Angular + FastAPI)
- CLI for evaluation and deployment operations

### Agent Types and Hierarchy

**1. LlmAgent** (Dynamic, model-driven)

*Use for:*
- Conversational interfaces
- Decision-making with uncertainty
- Natural language understanding
- Creative tasks (content generation)
- Contextual reasoning

*Characteristics:*
- Uses LLM for decision-making
- Non-deterministic execution
- Tool selection driven by model
- Handles ambiguous inputs

**2. Workflow Agents** (Deterministic, programmatic)

*Sequential Agent:*
- Executes tools in fixed order
- Use for: Multi-step processes with dependencies
- Example: Data pipeline (fetch → transform → load)

*Parallel Agent:*
- Executes multiple tools concurrently
- Use for: Independent operations requiring aggregation
- Example: Multi-source data gathering

*Loop Agent:*
- Repeats execution until condition met
- Use for: Iterative refinement, convergence tasks
- Example: Generator-critic pattern

**3. Custom Agents** (User-defined logic)

*Use for:*
- Domain-specific orchestration
- Complex state machines
- Integration with existing systems
- Specialized execution patterns

**Agent Composition:**
- Agents can contain sub-agents (hierarchical)
- Parent agent coordinates child agents
- Supports multi-level nesting

### Tool Ecosystem

**Tool Categories:**

1. **Built-in Tools**:
   - **Search** - Web search via Google Search API
   - **Code Execution** - Python code interpreter (sandboxed)
   - **Google Cloud tools** - Vertex AI, BigQuery, Cloud Storage

2. **Custom Function Tools**:
   - Python functions wrapped as tools
   - Automatic schema generation from type hints
   - Supports async functions

3. **OpenAPI Tools**:
   - Auto-generate from OpenAPI/Swagger specs
   - HTTP-based service integration

4. **MCP (Model Context Protocol) Tools**:
   - Integration with MCP servers
   - Cross-framework tool sharing

**Tool Attributes:**
- **Name** - Unique identifier
- **Description** - Natural language explanation for LLM
- **Parameters** - JSON schema defining inputs
- **Function** - Execution logic
- **Confirmation** - Optional human-in-the-loop approval

### Memory and State Management

**Session Management:**
- Agent maintains conversation history
- Automatic context window management
- Configurable history retention

**State Persistence:**
- Custom state objects per agent
- Serialization support (JSON, pickle)
- Database integration for long-term storage

**Context Caching:**
- Reduces token usage for repeated context
- Automatic cache invalidation
- Configurable cache TTL

## Agent Development Methodology

### Planning Phase

**Step 1: Define Agent Purpose**
- Primary objective (single responsibility)
- Input/output format
- Success criteria
- Failure modes

**Step 2: Identify Required Tools**

Decision criteria:
- Use **built-in tools** when available (Search, Code Execution)
- Create **custom functions** for simple operations (<100 lines)
- Use **OpenAPI tools** for existing REST APIs
- Use **MCP tools** for cross-framework compatibility

**Step 3: Select Agent Type**

```
START: What's the agent's decision pattern?
  │
  ├─> Requires natural language reasoning? ─Yes─> LlmAgent ★
  │
  ├─> Fixed sequence of steps?
  │   └─> Sequential Workflow Agent ★
  │
  ├─> Independent parallel operations?
  │   └─> Parallel Workflow Agent ★
  │
  ├─> Iterative refinement needed?
  │   └─> Loop Workflow Agent ★
  │
  └─> Custom orchestration logic?
      └─> Custom Agent ★
```

**Step 4: Design Multi-Agent Architecture** (if needed)

Patterns:
- **Coordinator/Dispatcher** - Central agent routes to specialists
- **Sequential Pipeline** - Output of Agent A → Input of Agent B
- **Parallel Fan-Out/Gather** - Distribute work, aggregate results
- **Hierarchical Decomposition** - Break complex task into subtasks

### Implementation Phase

**Agent Implementation Examples:**

[See Code Examples: examples/google_adk_agent_implementation.py]

Key agent patterns demonstrated:
- **LlmAgent** - `create_weather_assistant()` - Conversational agent with custom tools
- **SequentialAgent** - `create_data_pipeline()` - Ordered execution (fetch → transform → save)
- **ParallelAgent** - `create_market_researcher()` - Concurrent tool execution
- **LoopAgent** - `create_content_generator()` - Iterative refinement with break conditions
- **Session Management** - `create_stateful_session()` - Multi-turn conversation with history

### Testing Phase

**Web UI Testing:**

```bash
# Start API server
adk api_server --port 8000

# Start web UI (separate terminal)
cd adk-web
npm install
npm start
# Access: http://localhost:4200
```

**Programmatic Testing:**

```python
# Unit test for agent
def test_weather_agent():
    agent = create_weather_agent()
    response = agent.run("Weather in NYC?")
    assert "weather" in response.content.lower()
    assert response.success is True

# Integration test with mock tools
def test_pipeline_agent():
    agent = create_pipeline_agent(mock_tools=True)
    result = agent.run({"input": "test_data"})
    assert result["status"] == "completed"
```

**Evaluation Framework:**

```python
from google.adk.evaluation import evaluate_agent

# Criteria-based evaluation
results = evaluate_agent(
    agent=my_agent,
    test_cases=[
        {"input": "What's 2+2?", "expected_output": "4"},
        {"input": "Explain quantum computing", "criteria": "mentions_qubits"}
    ],
    evaluator_model="gemini-2.0-flash"
)

print(f"Pass rate: {results.pass_rate}")
print(f"Average score: {results.avg_score}")
```

## Tool Development

[See Code Examples: examples/google_adk_tools_example.py]

### Custom Function Tools

Examples demonstrated:
- **Basic Function Tool** - `calculate_tax()` - Simple tool with type hints
- **Async Tool** - `fetch_user_data()` - Asynchronous API calls
- **HITL Confirmation** - `send_email()`, `delete_user_account()` - Human approval required
- **Input Validation** - `send_email_tool()` - Email format validation and sanitization
- **Retry Logic** - `fetch_external_data()` - Automatic retry with exponential backoff
- **Rate Limiting** - `call_external_api()` - Decorator-based rate limiting
- **Error Handling** - `fetch_stock_price()` - Graceful degradation on failures

### OpenAPI Tools

**Integration Pattern:**
- Load tools from OpenAPI spec URL
- Optional tool filtering for specific operations
- Automatic schema generation from spec
[See: `create_api_agent()` in examples/google_adk_tools_example.py]

### MCP Tool Integration

**Integration Pattern:**
- Connect to MCP server endpoint
- Import tools for cross-framework compatibility
[See: `create_mcp_agent()` in examples/google_adk_tools_example.py]

## Multi-Agent Orchestration

[See Code Examples: examples/google_adk_multi_agent.py]

### Multi-Agent Patterns

**Pattern 1: Coordinator/Dispatcher** (Complexity: 4)
- **Use case:** Route user requests to specialized agents
- **Function:** `create_coordinator_system()` - Weather + Finance specialists

**Pattern 2: Sequential Pipeline** (Complexity: 3)
- **Use case:** Multi-stage processing with dependencies
- **Function:** `create_content_pipeline()` - Research → Write → Edit

**Pattern 3: Parallel Fan-Out/Gather** (Complexity: 4)
- **Use case:** Aggregate results from multiple sources
- **Function:** `create_market_analysis_system()` - Technical + Fundamental + Sentiment analysis

**Pattern 4: Hierarchical Decomposition** (Complexity: 5)
- **Use case:** Break complex tasks into manageable subtasks
- **Function:** `create_project_management_system()` - Multi-level agent hierarchy

**Pattern 5: Generator-Critic Loop** (Complexity: 4)
- **Use case:** Iterative refinement with feedback
- **Function:** `create_quality_content_system()` - Generate → Critique → Refine

**Pattern 6: Human-in-the-Loop (HITL)** (Complexity: 3)
- **Use case:** Critical decisions require human approval
- **Function:** `create_account_management_agent()` - Confirmation before deletion

**Pattern 7: State Management**
- **Use case:** Persistent user context across sessions
- **Class:** `StatefulAgent` - In-memory state storage with history

**Pattern 8: Database Persistence**
- **Use case:** Long-term state storage
- **Functions:** `save_state()`, `load_state()` - PostgreSQL-backed persistence

## Memory and State Management

[See Code Examples: examples/google_adk_multi_agent.py - State Management section]

### Session Management

**Basic Session Pattern:**
- Multi-turn conversation with history retention
- Automatic context window management
- Configurable history limits

[See: `create_stateful_session()` in examples/google_adk_agent_implementation.py]

### State Persistence

**Custom State Object:**
- In-memory state storage per user
- Dataclass-based state modeling
- Conversation history tracking

[See: `StatefulAgent` class in examples/google_adk_multi_agent.py]

**Database Persistence:**
- Long-term state storage with SQLAlchemy
- JSON-serialized state data
- PostgreSQL/MySQL support

[See: `save_state()`, `load_state()` functions in examples/google_adk_multi_agent.py]

## Deployment Options

[See Code Examples: examples/google_adk_deployment.py]

### Agent Engine (Managed Service)

**Deployment Commands:**
```bash
pip install google-adk[cli]
adk auth login
adk deploy --agent-file agent.py --agent-name my_agent --project-id my-gcp-project --region us-central1
```

[See: `create_production_agent()` for configuration example]

### Cloud Run Deployment

**Components:**
- FastAPI server with agent endpoints
- Dockerfile for containerization
- Health check and error handling
- Environment configuration

[See: FastAPI app implementation, Dockerfile reference, deployment commands in examples/google_adk_deployment.py]

### Docker Containerization

**Self-Hosted Options:**
- Docker Compose with Redis
- Single container deployment
- Environment variable configuration

[See: docker-compose.yml reference, deployment commands in examples/google_adk_deployment.py]

### Resource Requirements

| Agent Complexity | CPU | RAM | Concurrent Requests |
|------------------|-----|-----|---------------------|
| Simple LlmAgent | 1 core | 512MB | 10 |
| Workflow Agent | 2 cores | 1GB | 20 |
| Multi-Agent (3-5 agents) | 4 cores | 2GB | 10 |
| Complex Multi-Agent (>5) | 8 cores | 4GB | 5 |

## Evaluation and Testing

[See Code Examples: examples/google_adk_deployment.py - Evaluation endpoint]

### Criteria-Based Evaluation

**Pattern:**
- Define custom evaluation criteria (accuracy, helpfulness, etc.)
- Run test cases against agent
- Analyze pass rate and scores

[See: `evaluate_agent_endpoint()` in examples/google_adk_deployment.py]

### User Simulation Evaluation

**Pattern:**
- Simulate user interactions with defined goals
- Track goal completion rate
- Measure average turns to completion

[See documentation for UserSimulator examples]

## Best Practices

[See Code Examples: examples/google_adk_tools_example.py - Tool Design Best Practices section]

### Agent Instruction Writing

**Effective Patterns:**
- Clear role and responsibilities
- Structured format with constraints
- Specific tool usage guidance
- Example interactions

[See: GOOD vs BAD examples at end of examples/google_adk_tools_example.py]

### Tool Design Principles

**Key Principles:**
1. **Single Responsibility** - One clear purpose per tool
2. **Descriptive Naming** - Clear action and object naming
3. **Type Hints** - Complete type annotations for all parameters

[See: Tool design examples at end of examples/google_adk_tools_example.py]

### Error Handling

**Strategies:**
- **Graceful Degradation** - Return error messages instead of raising exceptions
- **Retry Logic** - Automatic retry with exponential backoff
- **Input Validation** - Validate and sanitize all inputs

[See: `fetch_stock_price()`, `fetch_external_data()`, `send_email_tool()` in examples/google_adk_tools_example.py]

### Security and Safety

**Implementation:**
- **Input Validation** - Email format validation, length limits
- **Rate Limiting** - Decorator-based request throttling
- **Sanitization** - Remove dangerous HTML/script content

[See: `send_email_tool()`, `rate_limit()` decorator in examples/google_adk_tools_example.py]

### Performance Optimization

**Async Tools:**
- Automatic parallel execution for async functions
- Improved throughput for I/O-bound operations

[See: `fetch_price()`, `create_portfolio_analyzer()` in examples/google_adk_tools_example.py]

## Quality Gates

### Definition of Done: Agents

An agent is production-ready when:

1. **Functionality:**
   - ✓ Agent completes primary objective on test cases
   - ✓ Tool execution succeeds with valid inputs
   - ✓ Error handling covers expected failure modes
   - ✓ Multi-turn conversations maintain context

2. **Performance:**
   - ✓ Response time <5 seconds for simple queries
   - ✓ Response time <30 seconds for complex workflows
   - ✓ Evaluation pass rate ≥80% on criteria
   - ✓ Resource usage within deployment limits

3. **Safety:**
   - ✓ Input validation on all tools
   - ✓ High-risk actions require confirmation (HITL)
   - ✓ No hardcoded credentials or API keys
   - ✓ Rate limiting on external API calls

4. **Observability:**
   - ✓ Logging configured for debugging
   - ✓ Tracing enabled for multi-agent workflows
   - ✓ Evaluation metrics tracked
   - ✓ Error alerts configured

5. **Documentation:**
   - ✓ Agent purpose and capabilities documented
   - ✓ Tool descriptions clear and accurate
   - ✓ Example usage provided
   - ✓ Known limitations documented

### Definition of Done: Tools

A tool is production-ready when:

1. **Interface:**
   - ✓ Function has type hints for all parameters
   - ✓ Docstring explains purpose, args, returns
   - ✓ Parameter descriptions guide LLM selection
   - ✓ Return values are JSON-serializable

2. **Reliability:**
   - ✓ Error handling with informative messages
   - ✓ Input validation prevents invalid operations
   - ✓ Timeout configured for long-running operations
   - ✓ Retry logic for transient failures

3. **Testing:**
   - ✓ Unit tests cover success cases
   - ✓ Unit tests cover error cases
   - ✓ Integration tests with agent execution
   - ✓ Performance benchmarks for expensive operations

## Error Handling Guide

### Common Issues and Resolutions

**Issue: Agent doesn't call the right tool**
- **Cause:** Tool description unclear or ambiguous
- **Resolution:**
  ```python
  # BAD: Vague description
  def process(data):
      """Process data."""  # Too generic

  # GOOD: Specific description
  def validate_email_format(email: str) -> bool:
      """Check if email address matches valid format (user@domain.com).

      Use this tool ONLY to validate email syntax, not to verify
      if email exists or is deliverable."""
  ```

**Issue: Agent loops indefinitely**
- **Cause:** No termination condition in Loop Agent
- **Resolution:**
  ```python
  # Add max_iterations and explicit break condition
  agent = LoopAgent(
      tools=[...],
      max_iterations=10,  # Hard limit
      break_condition=lambda result: result.get("completed", False)
  )
  ```

**Issue: "Tool execution failed" errors**
- **Cause:** Tool raises unhandled exception
- **Resolution:**
  ```python
  def robust_tool(param: str) -> str:
      try:
          result = risky_operation(param)
          return f"Success: {result}"
      except SpecificError as e:
          return f"Operation failed: {e.message}"
      except Exception as e:
          logger.error(f"Unexpected error in robust_tool: {e}")
          return "Temporary service error, please try again"
  ```

**Issue: Agent response is too slow**
- **Cause:** Sequential tool calls when parallelization possible
- **Resolution:**
  ```python
  # Use Parallel Agent or async tools
  agent = ParallelAgent(
      tools=[tool1, tool2, tool3]  # Execute concurrently
  )
  ```

**Issue: Context limit exceeded**
- **Cause:** Conversation history too long
- **Resolution:**
  ```python
  session = Session(
      agent=my_agent,
      max_history_turns=10,  # Limit history
      context_window_tokens=30000  # Set explicit limit
  )
  ```

**Issue: Deployment fails on Cloud Run**
- **Cause:** Missing dependencies or environment variables
- **Resolution:**
  ```bash
  # Ensure requirements.txt is complete
  pip freeze > requirements.txt

  # Set required environment variables
  gcloud run deploy my-agent \
    --set-env-vars GOOGLE_API_KEY=your_key,AGENT_CONFIG=prod
  ```

### Debugging Strategies

**1. Enable verbose logging:**

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("google.adk")
logger.setLevel(logging.DEBUG)
```

**2. Test tools independently:**

```python
# Test tool without agent
tool = Tool.from_function(my_function)
result = my_function("test_input")
print(f"Tool output: {result}")
```

**3. Use web UI for interactive debugging:**

```bash
adk api_server --debug
# Access UI at http://localhost:4200
# View tool calls, agent reasoning, response generation
```

**4. Inspect agent execution trace:**

```python
response = agent.run("test query", return_trace=True)
print(response.trace)  # Shows all tool calls and decisions
```

## Complexity Ratings

| Task | Rating | Description |
|------|--------|-------------|
| Simple LlmAgent with tools | 2 | Basic conversational agent |
| Sequential Workflow Agent | 2 | Fixed-order tool execution |
| Parallel Workflow Agent | 3 | Concurrent operations |
| Loop Workflow Agent | 3 | Iterative refinement |
| Custom Agent | 3 | User-defined orchestration |
| Coordinator/Dispatcher (2-3 agents) | 4 | Multi-agent routing |
| Sequential Pipeline (3+ agents) | 4 | Chained agent execution |
| Hierarchical Multi-Agent (>5 agents) | 5 | Complex nested architecture |
| Custom tool development | 2 | Python function wrapper |
| OpenAPI tool integration | 2 | Auto-generated from spec |
| MCP tool integration | 3 | Cross-framework tools |
| Deployment to Agent Engine | 2 | Managed deployment |
| Self-hosted Docker deployment | 3 | Container orchestration |
| Advanced evaluation framework | 4 | Custom criteria and simulation |

## References

### Official Documentation
- **Main docs:** https://google.github.io/adk-docs/
- **Python SDK:** https://github.com/google/adk-python
- **Examples:** https://github.com/google/adk-samples
- **Web UI:** https://github.com/google/adk-web

### Python SDK Resources
- **Installation:** `pip install google-adk`
- **API Reference:** https://google.github.io/adk-docs/api/python/
- **Quickstart Guide:** https://google.github.io/adk-docs/quickstart/

### Additional Languages
- **Go SDK:** https://github.com/google/adk-go
- **Java SDK:** https://github.com/google/adk-java

### Community Resources
- **GitHub Discussions:** https://github.com/google/adk-python/discussions
- **Issue Tracker:** https://github.com/google/adk-python/issues

### Related Skills
- For workflow automation: Use `n8n` skill
- For API design: Use `api-design-architect` skill
- For cloud deployment: Use `cloud-devops-expert` skill
- For Python development: Use Python-specific skills
- For LLM integration: Use model provider SDKs (OpenAI, Anthropic, etc.)

---

**Version:** 1.0.0
**Last Updated:** 2025-11-13
**Complexity Rating:** 3 (Moderate - requires agent architecture knowledge)
**Estimated Learning Time:** 10-15 hours for proficiency
