---
name: langchain-use
description: LangChain 1.0 使用指南。提供 Agent、Tool、Memory、Middleware 等核心概念的快速参考。当用户需要创建 AI Agent、集成 LangChain、或解决 LangChain 相关问题时激活。
---

# LangChain Use Skill

LangChain 是构建 LLM 驱动的智能体和应用程序的开源框架。

## 安装

使用 uv 安装 LangChain（推荐，需要 Python 3.10+）：

```bash
# 安装核心包
uv add langchain

# 安装模型提供商集成
uv add langchain-anthropic  # Anthropic/Claude
uv add langchain-openai     # OpenAI
```

## 快速参考

### 核心工作流程

```
用户查询 -> create_agent() -> ReAct 循环 -> Tool 调用 -> 返回结果
```

### 创建 Agent

详见 [Agent 基础](references/agents/agent-basics.md)

```python
from langchain.agents import create_agent

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# 运行 agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

### 定义 Tool

详见 [Tool 基础](references/tools/tool-basics.md)

```python
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"
```

### 访问 Runtime Context

使用 `ToolRuntime` 访问 state、context、store：

```python
from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass

@dataclass
class Context:
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user location based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"
```

### 管理 Memory

详见 [短期记忆](references/memory/short-term-memory.md)
详见 [长期记忆](references/memory/long-term-memory.md)

```python
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model,
    tools,
    checkpointer=InMemorySaver(),  # 短期记忆
)

# 使用 thread_id 维护会话
config = {"configurable": {"thread_id": "1"}}
agent.invoke({"messages": [...]}, config)
```

### 添加 Middleware

详见 [中间件概述](references/middleware/middleware-overview.md)

```python
from langchain.agents.middleware import before_model, after_model

@before_model
def trim_messages(state, runtime):
    # 消息修剪逻辑
    return None
```

## 进阶主题

| 主题 | 文档 | 说明 |
|------|------|------|
| Streaming | [Streaming](references/advanced/streaming.md) | 实时输出流式更新 |
| Structured Output | [结构化输出](references/advanced/structured-output.md) | Pydantic/dataclass 输出格式 |
| Runtime | [Runtime](references/advanced/runtime.md) | ToolRuntime 和上下文访问 |
| Guardrails | [安全护栏](references/advanced/guardrails.md) | PII 检测、内容过滤 |
| MCP | [MCP](references/advanced/mcp.md) | Model Context Protocol 集成 |

## 集成主题

| 主题 | 文档 | 说明 |
|------|------|------|
| Models | [模型](references/integration/models.md) | 多提供商模型初始化 |
| Messages | [消息](references/integration/messages.md) | 消息类型和内容块 |
| Retrieval | [检索](references/integration/retrieval.md) | RAG 和知识库构建 |

## 关键概念

### Agent (智能体)
LangChain 1.0 的核心抽象，基于 LangGraph 构建。使用 `create_agent()` 创建。

### Tool (工具)
使用 `@tool` 装饰器定义。可选 ToolRuntime 访问状态、上下文和存储。

### Memory (记忆)
- **Checkpointer**: 短期会话记忆 (InMemorySaver, PostgresSaver)
- **Store**: 长期持久化存储 (InMemoryStore)

### Middleware (中间件)
装饰器风格的扩展机制：
- `@before_model` - 模型调用前处理
- `@after_model` - 模型调用后处理
- `@wrap_tool_call` - 工具调用包装
- `@dynamic_prompt` - 动态系统提示

## 常见模式

### 基础 Agent
```python
from langchain.agents import create_agent

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[my_tool],
    system_prompt="You are helpful.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "hello"}]}
)
```

### 带记忆的 Agent（会话持久化）
```python
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[my_tool],
    checkpointer=InMemorySaver(),
)

# 使用 thread_id 标识会话
config = {"configurable": {"thread_id": "1"}}
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Bob"}]},
    config
)
agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config
)
```

### 生产环境 Memory（使用数据库）
```python
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()  # 自动创建表
    agent = create_agent(
        model="claude-sonnet-4-5-20250929",
        tools=[my_tool],
        checkpointer=checkpointer,
    )
```

### 带上下文的 Agent（Runtime Context）
```python
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

@dataclass
class Context:
    user_id: str

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Get user information."""
    user_id = runtime.context.user_id
    return f"User ID: {user_id}"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_user_info],
    context_schema=Context,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "get my info"}]},
    context=Context(user_id="user_123")
)
```

### 带结构化输出的 Agent
```python
from dataclasses import dataclass
from langchain.agents.structured_output import ToolStrategy

@dataclass
class Response:
    answer: str
    confidence: float

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[my_tool],
    response_format=ToolStrategy(Response),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is 2+2?"}]}
)
print(result['structured_response'])
# Response(answer="4", confidence=1.0)
```

### 完整示例（生产级 Agent）
```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy

@dataclass
class Context:
    user_id: str

@dataclass
class ResponseFormat:
    answer: str
    confidence: float | None = None

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Sunny in {city}"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Get user's location."""
    return "San Francisco" if runtime.context.user_id == "1" else "Unknown"

# 配置模型
model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature=0.5,
    max_tokens=1000
)

# 创建 agent
agent = create_agent(
    model=model,
    system_prompt="You are a weather assistant.",
    tools=[get_weather, get_user_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=InMemorySaver(),
)

# 运行 agent
config = {"configurable": {"thread_id": "1"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather?"}]},
    config=config,
    context=Context(user_id="1")
)
```

## 资源链接

- [核心概念](references/core-concepts/overview.md) - LangChain 概述
- [快速开始](references/core-concepts/quickstart.md) - 10行代码创建 Agent
- [官方文档](https://python.langchain.com)
- [API 参考](https://reference.langchain.com/python)
