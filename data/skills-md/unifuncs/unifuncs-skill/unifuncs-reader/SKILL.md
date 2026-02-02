---
name: unifuncs-reader
description: 使用 UniFuncs API 读取网页、PDF、Word 等文档内容，支持 AI 内容提取。当用户需要阅读、抓取、提取网页或文档内容时使用。
argument-hint: [URL]
allowed-tools: Bash(python*:*)
---

# UniFuncs 网页阅读 Skill

读取网页、PDF、Word 等文档内容，支持 AI 内容提取。

## 首次使用配置

1. 前往 https://unifuncs.com/account 获取 API Key
2. 设置环境变量：`export UNIFUNCS_API_KEY="sk-your-api-key"`

## 使用方法

```bash
python3 scripts/read.py "https://example.com"

# 查看所有参数
python3 scripts/read.py --help
```
