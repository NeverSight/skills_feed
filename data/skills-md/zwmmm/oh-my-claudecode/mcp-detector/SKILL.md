---
name: mcp-detector
description: Automatically detect and suggest appropriate MCP tools (context7, grep_app, web_search) based on user queries. Use when queries contain documentation keywords (how to use, docs, API, guide, tutorial, 如何使用, 文档, 教程); code search keywords (example, implementation, source code, github, 例子, 示例, 实现, 源码); or latest information/bug fixing keywords (latest, 2025, 2026, new, update, fix bug, error, 最新, 更新, 修复 bug, 报错).
---

# MCP 检测器

自动识别用户查询意图并推荐合适的 MCP 工具。

## 快速检测

运行检测脚本获取工具推荐:

```bash
# 命令行参数
python scripts/detect_mcp.py "用户查询内容"

# 管道输入
echo "用户查询" | python scripts/detect_mcp.py
```

**输出格式**: JSON，包含 `matched_tools` 和 `recommendations`

## 工具说明

### context7 - 官方文档查询
- **用途**: 查找官方 API 文档、学习最佳实践、了解功能使用方法
- **工具**: `mcp__plugin_oh_context7__query-docs`
- **触发词**: how to use, API, docs, guide, tutorial, 如何使用, 文档, 教程

### grep_app - GitHub 代码搜索
- **用途**: 查找真实代码实现、学习实际使用案例、参考开源项目
- **工具**: `mcp__plugin_oh_grep_app__searchGitHub`
- **触发词**: example, implementation, source code, github, 例子, 示例, 实现, 源码

### web_search - 最新信息搜索
- **用途**: 获取最新版本信息、了解最近更新、查找 bug 解决方案
- **工具**: `mcp__plugin_oh_web_search__web_search_exa`
- **触发词**: 2025, 2026, latest, new, update, fix bug, error, 最新, 更新, 修复 bug, 报错

## 工作流程

1. **运行检测脚本** - 获取推荐工具列表
2. **分析匹配结果** - 查看匹配的关键词和理由
3. **调用匹配工具** - 直接调用推荐的 MCP 工具执行查询

## 设计原则

### KISS
- 脚本简洁高效，单一职责
- 直接输出 JSON，便于解析

### DRY
- 统一的关键词配置数据结构
- 可复用的检测逻辑

### YAGNI
- 只实现必要的关键词检测
- 基于实际需求持续优化
