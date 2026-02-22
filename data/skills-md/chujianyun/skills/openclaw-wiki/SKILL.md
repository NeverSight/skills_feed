---
name: openclaw-wiki
description: OpenClaw 官方文档知识库，一个多渠道 AI Agent 网关。当用户询问 OpenClaw 相关问题（如安装、配置、Gateway、WhatsApp/Telegram/Discord 等渠道连接、Sessions、Tools、Skills、Pi Agent、故障排查等）时使用此 skill。
---

# OpenClaw Wiki

OpenClaw 官方文档知识库，提供多渠道 AI Agent 网关的使用指南和技术参考。

## 使用方式

1. 首先查阅 [INDEX.md](INDEX.md) 获取文档索引和内容概览
2. 根据用户问题定位相关文档
3. 使用 Read 工具读取对应的 docs/ 目录下的文档
4. 如文档信息不足，再考虑联网搜索补充

## 文档结构

```
docs/
├── index.md              # 项目首页和概述
├── start/                # 快速开始、入门向导、安装设置
├── concepts/             # 核心概念：Agent、Session、Memory、Models
├── gateway/              # Gateway 配置、安全、远程访问、故障排查
├── channels/             # 渠道配置：WhatsApp、Telegram、Discord、iMessage 等
├── tools/                # 工具：Browser、Skills、Subagents、Exec
├── install/              # 安装指南：Docker、Node、macOS、Linux
├── providers/            # 模型提供商：Anthropic、OpenAI、Ollama 等
├── nodes/                # 移动节点：iOS、Android
├── cli/                  # CLI 命令参考
├── web/                  # Web Control UI
├── help/                 # 帮助和故障排查
├── security/             # 安全配置
├── plugins/              # 插件开发
├── automation/           # 自动化配置
└── zh-CN/                # 中文文档
```

## 常见问题分类

| 问题类型 | 参考文档 |
|---------|---------|
| 什么是 OpenClaw | docs/index.md |
| 快速开始/安装 | docs/start/getting-started.md, docs/start/quickstart.md |
| 入门向导 | docs/start/wizard.md, docs/start/onboarding.md |
| Gateway 配置 | docs/gateway/configuration.md, docs/gateway/configuration-reference.md |
| WhatsApp 连接 | docs/channels/whatsapp.md |
| Telegram 连接 | docs/channels/telegram.md |
| Discord 连接 | docs/channels/discord.md |
| iMessage 连接 | docs/channels/imessage.md |
| 群组消息 | docs/channels/groups.md, docs/channels/group-messages.md |
| Agent 概念 | docs/concepts/agent.md, docs/concepts/agent-loop.md |
| Session 管理 | docs/concepts/session.md, docs/concepts/session-tool.md |
| Memory 功能 | docs/concepts/memory.md |
| 模型配置 | docs/concepts/models.md, docs/concepts/model-providers.md |
| 多 Agent 路由 | docs/concepts/multi-agent.md |
| Browser 工具 | docs/tools/browser.md |
| Skills 配置 | docs/tools/skills.md, docs/tools/creating-skills.md |
| Subagents | docs/tools/subagents.md |
| 命令执行 | docs/tools/exec.md, docs/tools/exec-approvals.md |
| Docker 安装 | docs/install/docker.md |
| 远程访问 | docs/gateway/remote.md, docs/gateway/tailscale.md |
| 安全配置 | docs/gateway/sandboxing.md, docs/gateway/authentication.md |
| 故障排查 | docs/gateway/troubleshooting.md, docs/help/ |
| CLI 命令 | docs/cli/ |
| Pi Agent | docs/pi.md |
