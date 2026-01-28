---
name: session-advisor
description: 多模型协作的SESSION管理顾问。当调用Codex或Gemini前，自动提供SESSION复用/新开建议。当用户讨论多模型协作、SESSION管理、上下文隔离时使用。
---

# SESSION管理顾问

## 核心原则

SESSION_ID管理采用**灵活建议**而非**强制规定**的方式。

## 何时建议新开SESSION？

以下场景**推荐**（非强制）新开SESSION：

- 🔍 **审计/Review** - 需要独立客观视角，避免先入为主
- 🔀 **方向分叉** - 同一问题想探索不同解法
- 🧹 **上下文过长** - 感觉模型"记混"了之前讨论
- ⚡ **并行任务** - 多个worktree同时开发
- 🎯 **职责切换** - 从后端逻辑切到UI设计

## 何时建议复用SESSION？

以下场景**适合**复用现有SESSION：

- 🔧 **迭代修复** - 基于上一轮反馈继续优化
- 🔗 **上下文依赖** - 需要模型理解之前的决策背景
- 📝 **连续讨论** - 围绕同一技术问题深入探讨

## 判断提示

在调用Codex/Gemini前，思考：

> "如果这个模型'记得'之前的讨论，会**帮助**还是**干扰**？"

| 答案 | 建议 |
|------|------|
| 帮助 | 复用SESSION（传入 `--SESSION_ID`） |
| 干扰 | 新开SESSION（不传 `SESSION_ID`） |
| 不确定 | 默认新开（更安全） |

## 同一Story多会话

一个Story可以有多个独立会话，例如：
- 主线实现会话
- 备选方案探索会话
- 独立code-review会话

不需要强制统一SESSION_ID格式。

详细指南见 [session-management.md](../guides/session-management.md)
