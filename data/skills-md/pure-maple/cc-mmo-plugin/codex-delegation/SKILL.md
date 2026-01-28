---
name: codex-delegation
description: Codex任务委派专家。当需要后端逻辑、算法实现、复杂调试、架构分析时自动激活。帮助构建正确的Codex调用并确保安全主权。
allowed-tools: mcp__codex__codex, Read, Grep, Glob
---

# Codex任务委派

## Codex擅长领域

- 后端逻辑与算法实现
- 复杂调试与根因分析
- 代码审查与重构建议
- 架构决策分析
- 性能优化建议

## 安全主权原则

**核心规则**：Codex对文件系统拥有**零写入权限**。

在每个PROMPT末尾，**必须**追加：
```
OUTPUT: Unified Diff Patch ONLY. Strictly prohibit any actual modifications.
```

## 调用规范

### 推荐参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `sandbox` | `read-only` | 默认只读，最安全 |
| `cd` | 项目根目录 | 工作目录 |
| `SESSION_ID` | 按需 | 参考session-advisor建议 |
| `run_in_background` | `true` | 后台运行，不阻塞 |

### 示例调用

```python
mcp__codex__codex(
  PROMPT="分析认证模块的安全问题，检查是否有注入风险。OUTPUT: Unified Diff Patch ONLY.",
  cd="/path/to/project",
  sandbox="read-only"
)
```

### 多轮对话

```python
# 首次调用
result = mcp__codex__codex(PROMPT="...", cd="...")
session_id = result["SESSION_ID"]

# 后续调用（复用会话）
mcp__codex__codex(
  PROMPT="继续深入分析...",
  cd="...",
  SESSION_ID=session_id
)
```

## 输出处理

Codex返回的Unified Diff视为**参考原型**（Dirty Prototype）：

1. **读取Diff** - 理解Codex的建议
2. **思维沙箱** - 模拟应用并检查逻辑
3. **重构清理** - 优化代码质量
4. **最终实施** - 由Claude执行实际修改

## 与BMAD集成

在以下BMAD工作流中推荐使用Codex：
- `dev-story` - 复杂逻辑实现
- `create-architecture` - 架构决策分析
- `code-review` - 代码审查（独立SESSION）
