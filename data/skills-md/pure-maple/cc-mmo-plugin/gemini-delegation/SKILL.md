---
name: gemini-delegation
description: Gemini任务委派专家。当需要前端UI/UX、样式设计、React/Vue组件、CSS优化时自动激活。帮助构建正确的Gemini调用。
allowed-tools: mcp__gemini__gemini, Read, Grep, Glob
---

# Gemini任务委派

## Gemini擅长领域

- 前端UI/UX设计
- React/Vue/Svelte组件
- CSS/Tailwind样式
- 响应式布局
- 动画与交互效果
- 视觉一致性审查

## 注意事项

⚠️ **Gemini上下文限制**：< 32k tokens

⚠️ **后端逻辑**：Gemini对后端逻辑理解有缺陷，其相关建议需客观审视

## 安全主权原则

与Codex相同，在PROMPT末尾追加：
```
OUTPUT: Unified Diff Patch ONLY. Strictly prohibit any actual modifications.
```

## 调用规范

### 推荐参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `sandbox` | `true` | 启用沙箱模式 |
| `cd` | 项目根目录 | 工作目录 |
| `SESSION_ID` | 按需 | 参考session-advisor建议 |

### 示例调用

```python
mcp__gemini__gemini(
  PROMPT="优化登录表单的用户体验，添加输入验证反馈动画。OUTPUT: Unified Diff Patch ONLY.",
  cd="/path/to/project",
  sandbox=True
)
```

## 输出处理

Gemini返回的样式/组件代码视为**视觉基准**：

1. **审视设计** - 确认符合项目风格
2. **验证兼容** - 检查与现有组件的兼容性
3. **重构优化** - 按项目规范调整
4. **最终实施** - 由Claude执行修改

## 与BMAD集成

在以下BMAD工作流中推荐使用Gemini：
- `create-ux-design` - UX设计讨论
- `dev-story` - 前端组件实现
- `code-review` - UI/UX审查（独立SESSION）

## Gemini vs Codex选择

| 任务类型 | 推荐模型 |
|----------|----------|
| 后端API逻辑 | Codex |
| React组件样式 | Gemini |
| 数据库查询优化 | Codex |
| 动画效果实现 | Gemini |
| 算法实现 | Codex |
| 响应式布局 | Gemini |
