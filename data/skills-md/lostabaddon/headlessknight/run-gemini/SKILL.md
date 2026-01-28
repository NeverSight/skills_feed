---
name: run-gemini
description: 向助手发出协助请求，适用于长文阅读理解、网络搜索、网页读取、文章翻译、网页与前端界面制作等任务场景。
---

# 功能简介

通过 MCP 工具向一位外部助手发出协助请求，请对方在一个上下文干净的、运行时隔离的、独立环境中，执行网络搜索、网页读取、长文本的阅读理解以及全文翻译等任务。

## 使用方法

使用 `mcp__plugin_headless-knight_runCLI__gemini` 工具来向助手发出请求，可传入参数包括：
- `prompt`: string，从上下文整理出的完整的任务描述，必填参数
- `systemPrompt`: string，从上下文整理出的需要该助手遵守的系统提示词，用于约束他的行为，可选
- `workDir`: string，工作目录，默认为当前目录，可选
- `model`: string，指定使用哪个模型，取值为"gemini-3-pro-preview"、"gemini-2.5-flash"或"gemini-2.5-flash-lite"等模型的代号，可选，默认为 gemini-2.5-flash
- `env`: object，自定义环境变量，键值对，可选

## 模型选择

- gemini-3-pro-preview: 擅长超长文档的阅读理解、文献整理与汇总、中长篇小说的修改与撰写、全文翻译、网页与前端界面制作等任务的执行
- gemini-2.5-flash: 擅长网络搜索、长文档的阅读理解、创意写作、翻译审查与修订，等等
- gemini-2.5-flash-lite: 适用于极快速反应与头脑风暴

## 相关环境变量

如果不另外设置，则自动使用当前对话上下文中的配置
- `GEMINI_API_KEY`: Codex CLI 的 API_Key
- `HTTP_PROXY`: HTTP 代理地址
- `HTTPS_PROXY`: HTTPS 代理地址
- `ALL_PROXY`: 默认代理地址
- `GEMINI_CLI_COMMAND`: Codex 命令行地址或名称（确保在 PATH 中包含了路径）
- `NODE_ENV`: 环境参数，比如 "development"
