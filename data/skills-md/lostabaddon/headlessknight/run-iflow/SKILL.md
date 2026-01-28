---
name: run-iflow
description: 向助手发出协助请求，适用中华文化理解、中文古文理解、中国特色作品创作、小红书与抖音的宣发文案编写、编写测试用例、信息检索等任务场景，同时也是其他专家助手的强力替补与协助，可以作为大部分认为的备选候补方案。
---

# 功能简介

通过 MCP 工具向一位外部助手发出协助请求，请对方在一个上下文干净的、运行时隔离的、独立环境中，执行中华文化理解、中文古文理解、中国特色作品创作、小红书与抖音的宣发文案编写、编写测试用例、信息检索等任务。

## 使用方法

使用 `mcp__plugin_headless-knight_runCLI__iflow` 工具来向助手发出请求，可传入参数包括：
- `prompt`: string，从上下文整理出的完整的任务描述，必填参数
- `systemPrompt`: string，从上下文整理出的需要该助手遵守的系统提示词，用于约束他的行为，可选
- `workDir`: string，工作目录，默认为当前目录，可选
- `model`: string，指定使用哪个模型，取值为"GLM-4.6"、"Qwen3-Coder-Plus"、"DeepSeek-V3.2"、"MiniMax-M2"或"Kimi-K2-0905"等模型代号，可选，默认为 MiniMax-M2
- `env`: object，自定义环境变量，键值对，可选

## 模型选择

- GLM-4.6: 擅长中文内容创作、中文市场分析、中国文化相关的教育与问答等任务
- Qwen3-Coder-Plus: 擅长阿里云用户或需要进行模型精调和私有化部署等任务
- DeepSeek-V3.2: 擅长与编程相关的任务，如代码生成、Bug 修复、代码解释、算法设计、编写单元测试等
- Kimi-K2-0905: 适用于需要处理大量文本信息的场景，如信息检索、长篇内容总结、知识库问答等
- MiniMax-M2: 适用于上述各项任务

## 相关环境变量

如果不另外设置，则自动使用当前对话上下文中的配置
- `IFLOW_API_KEY`: Codex CLI 的 API_Key
- `HTTP_PROXY`: HTTP 代理地址
- `HTTPS_PROXY`: HTTPS 代理地址
- `ALL_PROXY`: 默认代理地址
- `IFLOW_CLI_COMMAND`: Codex 命令行地址或名称（确保在 PATH 中包含了路径）
- `NODE_ENV`: 环境参数，比如 "development"
