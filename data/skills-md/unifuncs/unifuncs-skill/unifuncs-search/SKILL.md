---
name: unifuncs-search
description: 使用 UniFuncs API 进行实时网络搜索，支持全球和中国地域，获取最新网络内容和新闻。当用户需要搜索、查找、联网获取信息时使用。
argument-hint: [搜索关键词]
allowed-tools: Bash(python*:*)
---

# UniFuncs 实时搜索 Skill

快速的实时搜索服务，支持全球和中国地域搜索。

## 首次使用配置

1. 前往 https://unifuncs.com/account 获取 API Key
2. 设置环境变量：`export UNIFUNCS_API_KEY="sk-your-api-key"`

## 使用方法

```bash
python3 scripts/search.py "搜索关键词"

# 查看所有参数
python3 scripts/search.py --help
```
