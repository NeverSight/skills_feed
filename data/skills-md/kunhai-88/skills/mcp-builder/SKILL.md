---
name: mcp-builder
description: "创建高质量 MCP（Model Context Protocol）服务器的指南，使 LLM 通过精心设计的工具与外部服务交互。在构建 MCP 服务器以集成外部 API 或服务时使用，无论是 Python（FastMCP）还是 Node/TypeScript（MCP SDK）。"
license: MIT
---

# MCP 服务器开发指南

创建 MCP 服务器，使 LLM 通过精心设计的工具与外部服务交互。MCP 服务器质量以 LLM 完成真实世界任务的能力衡量。

## 高级工作流程

创建高质量 MCP 服务器涉及四个主要阶段：

### 阶段 1：深度研究与规划

**1.1 理解现代 MCP 设计**：平衡全面 API 端点覆盖与专业工作流工具。工作流工具对特定任务更便利，而全面覆盖给代理组合操作的灵活性。性能因客户端而异—某些客户端受益于组合基本工具的代码执行，而其他客户端更适合高级工作流。不确定时，优先全面 API 覆盖。  
**工具命名与可发现性**：清晰、描述性工具名帮助代理快速找到正确工具。使用一致前缀（如 `github_create_issue`、`github_list_repos`）与面向动作的命名。  
**上下文管理**：代理受益于简洁工具描述与过滤/分页结果能力。设计返回聚焦、相关数据的工具。某些客户端支持代码执行，可帮助代理高效过滤与处理数据。  
**可操作错误消息**：错误消息应通过具体建议与下一步指导代理走向解决方案。

**1.2 研究 MCP 协议文档**：从 sitemap 开始：`https://modelcontextprotocol.io/sitemap.xml`，然后获取带 `.md` 后缀的特定页面（如 `https://modelcontextprotocol.io/specification/draft.md`）。关键页面：规范概览与架构、传输机制（可流式 HTTP、stdio）、工具、资源与提示定义。

**1.3 研究框架文档**：推荐栈：TypeScript（高质量 SDK 支持与许多执行环境良好兼容性，AI 模型擅长生成 TypeScript 代码，受益于广泛使用、静态类型与良好 linting 工具）、传输：可流式 HTTP 用于远程服务器（使用无状态 JSON），stdio 用于本地服务器。  
加载框架文档：MCP 最佳实践、TypeScript SDK（从 GitHub 获取 README）、Python SDK（从 GitHub 获取 README）。

**1.4 规划实现**：理解 API（审查服务 API 文档以识别关键端点、认证要求与数据模型）、工具选择（优先全面 API 覆盖，列出要实现的端点，从最常见操作开始）。

### 阶段 2：实现

**2.1 设置项目结构**：见语言特定指南（TypeScript 指南、Python 指南）。  
**2.2 实现核心基础设施**：创建共享工具：带认证的 API 客户端、错误处理助手、响应格式化（JSON/Markdown）、分页支持。  
**2.3 实现工具**：对每个工具：输入 Schema（使用 Zod（TypeScript）或 Pydantic（Python），包含约束与清晰描述，在字段描述中添加示例）、输出 Schema（如可能定义 `outputSchema` 用于结构化数据，在工具响应中使用 `structuredContent`（TypeScript SDK 功能））、工具描述（功能简洁摘要、参数描述、返回类型 schema）、实现（I/O 操作用 async/await，带可操作消息的适当错误处理，如适用支持分页，使用现代 SDK 时返回文本内容与结构化数据）、注释（`readOnlyHint`、`destructiveHint`、`idempotentHint`、`openWorldHint`）。

### 阶段 3：审查与测试

**3.1 代码质量**：审查：无重复代码（DRY 原则）、一致错误处理、完整类型覆盖、清晰工具描述。  
**3.2 构建与测试**：TypeScript：运行 `npm run build` 验证编译，使用 MCP Inspector 测试：`npx @modelcontextprotocol/inspector`；Python：验证语法：`python -m py_compile your_server.py`，使用 MCP Inspector 测试。

### 阶段 4：创建评估

实现 MCP 服务器后，创建全面评估以测试其有效性。  
**4.1 理解评估目的**：使用评估测试 LLM 是否有效使用你的 MCP 服务器回答现实、复杂问题。  
**4.2 创建 10 个评估问题**：遵循评估指南中的流程：工具检查、内容探索、问题生成、答案验证。  
**4.3 评估要求**：确保每个问题：独立、只读、复杂（需要多次工具调用与深度探索）、现实（基于人类会关心的真实用例）、可验证（单一、清晰答案可通过字符串比较验证）、稳定（答案不会随时间改变）。  
**4.4 输出格式**：创建 XML 文件，包含问题与答案。

## 参考文件

**核心 MCP 文档**：从 sitemap 开始，然后获取特定页面；MCP 最佳实践（通用 MCP 指南，包括服务器与工具命名约定、响应格式指南、分页最佳实践、传输选择、安全与错误处理标准）。  
**SDK 文档**：Python SDK、TypeScript SDK（从 GitHub 获取 README）。  
**语言特定实现指南**：Python 实现指南（完整 Python/FastMCP 指南）、TypeScript 实现指南（完整 TypeScript 指南）。  
**评估指南**：完整评估创建指南。
