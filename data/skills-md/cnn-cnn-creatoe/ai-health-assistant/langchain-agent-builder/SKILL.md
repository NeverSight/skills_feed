---
name: langchain-agent-builder
description: 基于 LangChain 框架构建 AI Agent 机器人的技能。当用户需要创建 LangChain agent、选择 agent 框架、实现工具调用、管理对话记忆或构建复杂工作流时使用此技能。涵盖 LangGraph、CrewAI、AutoGen 等热门框架，提供最佳实践、代码模板和架构设计指导。
---

# LangChain Agent 构建 Skill

## 使用场景

当用户需要：
- 创建基于 LangChain 的 AI Agent 机器人
- 选择适合的 agent 框架和工具
- 实现工具调用和函数调用
- 管理对话记忆和上下文
- 构建复杂的工作流和状态管理
- 集成外部工具和 API
- 优化 agent 性能和响应质量

## 热门 Agent 框架推荐

### 1. LangGraph（推荐⭐⭐⭐⭐⭐）
- **GitHub**: https://github.com/langchain-ai/langgraph
- **特点**：
  - LangChain 官方状态管理框架
  - 声明式图形化工作流
  - 支持循环、分支、条件逻辑
  - 强大的状态持久化
- **适用场景**：复杂任务流程、多步骤决策、状态管理
- **优势**：与 LangChain 生态完美集成，文档完善

### 2. CrewAI（推荐⭐⭐⭐⭐⭐）
- **GitHub**: https://github.com/crewAIInc/crewAI
- **特点**：
  - 多 agent 协作框架
  - 角色分工明确（Role-based）
  - 任务流（Crews + Flows）模型
  - 丰富的工具集成
- **适用场景**：团队协作、任务分解、多 agent 协同
- **优势**：配置化强，易于扩展

### 3. AutoGen（推荐⭐⭐⭐⭐）
- **GitHub**: https://github.com/microsoft/autogen
- **特点**：
  - 微软开源多 agent 框架
  - 支持异步通信
  - 对话式协作
  - 代码执行和工具调用
- **适用场景**：对话型机器人、多 agent 交互、代码生成
- **优势**：企业级支持，功能强大

### 4. LangChain Agent Builder Templates
- **官方模板**: https://docs.langchain.com/langsmith/agent-builder-templates
- **特点**：
  - 官方预配置模板
  - 开箱即用
  - 包含系统提示词和工具集
- **适用场景**：快速原型、常见业务场景（邮件助手、日程提醒等）

### 5. LightAgent（推荐⭐⭐⭐⭐）
- **特点**：
  - 轻量级开源框架
  - 集成 Memory、Tools、Tree of Thought
  - 现代 agent 特性
- **适用场景**：快速开发、中型项目、资源受限环境

## 核心组件

### Agent 类型

#### 1. ReAct Agent
- **特点**：推理 + 行动循环
- **适用**：需要工具调用的任务
- **示例**：搜索、计算、API 调用

#### 2. Plan-and-Execute Agent
- **特点**：先规划后执行
- **适用**：复杂多步骤任务
- **示例**：数据分析、报告生成

#### 3. Conversational Agent
- **特点**：对话式交互
- **适用**：聊天机器人、客服助手
- **示例**：问答系统、对话助手

### 工具集成

#### 常用工具类型
- **搜索工具**：Google Search、DuckDuckGo
- **计算工具**：Python REPL、计算器
- **文件工具**：文件读写、文档处理
- **API 工具**：REST API、GraphQL
- **数据库工具**：SQL 查询、向量数据库

### 记忆管理

#### 记忆类型
- **对话记忆**：ConversationBufferMemory
- **摘要记忆**：ConversationSummaryMemory
- **实体记忆**：ConversationEntityMemory
- **知识图谱记忆**：ConversationKGMemory

## 开发流程

### 1. 项目初始化

```python
# 安装依赖
pip install langchain langchain-openai langgraph
# 或
pip install crewai
```

### 2. 基础 Agent 创建（LangChain）

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

# 初始化 LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 定义工具
tools = [
    Tool(
        name="search",
        func=search_function,
        description="搜索网络信息"
    )
]

# 创建 agent
agent = create_react_agent(llm, tools, prompt_template)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 运行
result = executor.invoke({"input": "查询今天的天气"})
```

### 3. LangGraph 工作流

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    next: str

def agent_node(state: AgentState):
    # Agent 逻辑
    return {"messages": [...], "next": "continue"}

def tool_node(state: AgentState):
    # 工具调用
    return {"messages": [...], "next": "agent"}

# 构建图
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge("agent", "tools")
graph.add_edge("tools", "agent")
graph.set_entry_point("agent")

app = graph.compile()
```

### 4. CrewAI 多 Agent 协作

```python
from crewai import Agent, Task, Crew

# 定义 Agent
researcher = Agent(
    role='研究员',
    goal='收集和分析信息',
    backstory='你是一个专业的研究员'
)

writer = Agent(
    role='作家',
    goal='撰写高质量内容',
    backstory='你是一个经验丰富的作家'
)

# 定义任务
research_task = Task(
    description='研究某个主题',
    agent=researcher
)

write_task = Task(
    description='基于研究结果撰写文章',
    agent=writer
)

# 创建 Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task]
)

result = crew.kickoff()
```

## 最佳实践

### 提示词设计
- **明确角色**：为 agent 定义清晰的角色和职责
- **工具描述**：详细描述工具的功能和使用场景
- **错误处理**：包含错误处理和重试机制
- **输出格式**：明确指定输出格式和结构

### 性能优化
- **工具选择**：只加载必要的工具，减少 token 消耗
- **记忆管理**：根据场景选择合适的记忆类型
- **流式输出**：使用流式响应提升用户体验
- **缓存策略**：缓存常见查询结果

### 错误处理
- **工具调用失败**：提供重试和降级方案
- **超时处理**：设置合理的超时时间
- **异常捕获**：优雅处理各种异常情况
- **日志记录**：记录关键操作和错误信息

## 推荐项目参考

### GitHub 仓库
1. **awesome-langchain-agents**
   - https://github.com/EniasCailliau/awesome-langchain-agents
   - 大量 LangChain agent 案例集合

2. **LangChain Templates**
   - https://github.com/langchain-ai/langchain/tree/master/templates
   - 官方模板和示例

3. **LangGraph Examples**
   - https://github.com/langchain-ai/langgraph/tree/main/examples
   - LangGraph 使用示例

### 学习资源
- **LangChain 官方文档**: https://docs.langchain.com
- **LangGraph 文档**: https://langchain-ai.github.io/langgraph
- **CrewAI 文档**: https://docs.crewai.com

## 注意事项

- 根据任务复杂度选择合适的框架
- 注意 token 消耗和成本控制
- 实现适当的错误处理和重试机制
- 考虑 agent 的安全性和可控性
- 定期更新依赖和框架版本
