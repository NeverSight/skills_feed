---
name: run-codex
description: 向助手发出协助请求，适用于代码审核、逻辑推理、科学与哲学思考、深度分析、策略制定、市场分析等任务场景。
---

# 功能简介

通过 MCP 工具向一位外部助手发出协助请求，请对方在一个上下文干净的、运行时隔离的、独立环境中，执行代码审核、逻辑推理、科学与哲学思考、深度分析、策略制定、市场分析等任务。

## 使用方法

使用 `mcp__plugin_headless-knight_runCLI__codex` 工具来向助手发出请求，可传入参数包括：
- `prompt`: string，从上下文整理出的完整的任务描述，必填参数
- `systemPrompt`: string，从上下文整理出的需要该助手遵守的系统提示词，用于约束他的行为，可选
- `workDir`: string，工作目录，默认为当前目录，可选
- `model`: string，指定使用哪个模型，取值为"gpt-5.1-codex"、"gpt-5.1"、"gpt-5-mini"、"gpt-5-nano"或"o3"等 OpenAI 的 GPT 系列模型的代号，可选，默认为 gpt-5.1-codex
- `env`: object，自定义环境变量，键值对，可选

## 模型选择

- o3: 适用于复杂的科学、数学、逻辑推理、哲学思考、策略分析与制定等任务与问题
- gpt 5/5.1 系列: 适用于代码审核、重构方案制定、BUG 分析、数学科学与哲学问题的深度思考等任务与问题，根据任务或问题的难度调整使用原版、mini 版还是 nano 版，codex 版更专注于代码审核

## 相关环境变量

如果不另外设置，则自动使用当前对话上下文中的配置
- `OPENAI_API_KEY`: Codex CLI 的 API_Key
- `HTTP_PROXY`: HTTP 代理地址
- `HTTPS_PROXY`: HTTPS 代理地址
- `ALL_PROXY`: 默认代理地址
- `OPENAI_CODEX_COMMAND`: Codex 命令行地址或名称（确保在 PATH 中包含了路径）
- `NODE_ENV`: 环境参数，比如 "development"
