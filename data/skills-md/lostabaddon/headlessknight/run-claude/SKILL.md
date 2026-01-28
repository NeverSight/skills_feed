---
name: run-claude
description: 向助手发出协助请求，适用于需要在隔离的独立环境中执行复杂编程任务、任务规划、文稿撰写的场景。
---

# 功能简介

通过 MCP 工具向一位外部助手发出协助请求，请对方在一个上下文干净的、运行时隔离的、独立环境中，完成复杂编程任务、任务规划、文章撰写、编曲等任务。

## 使用方法

使用 `mcp__plugin_headless-knight_runCLI__claude` 工具来向助手发出请求，可传入参数包括：
- `prompt`: string，从上下文整理出的完整的任务描述，必填参数
- `systemPrompt`: string，从上下文整理出的需要该助手遵守的系统提示词，用于约束他的行为，可选
- `workDir`: string，工作目录，默认为当前目录，可选
- `model`: string，指定使用哪个模型，取值为"sonnet"、"haiku"或"opus"之一，可选，默认为 sonnet
- `env`: object，自定义环境变量，键值对，可选

## 模型选择

- opus: 适用于复杂材料的分析、深度推理，或者复杂任务的规划拆解，或者法律文书等需要极高准去度的专业文书的写作
- sonnet: 适用于复杂编程任务，文章（包括小说、讲稿、剧本、营销文案、商业文档等）撰写、编曲等
- haiku: 适合发挥创意的艺术创作工作

## 相关环境变量

如果不另外设置，则自动使用当前对话上下文中的配置
- `ANTHROPIC_API_KEY`: Claude Code 的 API_Key
- `HTTP_PROXY`: HTTP 代理地址
- `HTTPS_PROXY`: HTTPS 代理地址
- `ALL_PROXY`: 默认代理地址
- `CODE_ENVCLAUDE_CODE_COMMAND`: Claude 命令行地址或名称（确保在 PATH 中包含了路径），或者 ClaudeCodeRouter 地址或名称（比如 "ccr code"）
- `NODE_ENV`: 环境参数，比如 "development"
