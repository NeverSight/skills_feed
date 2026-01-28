---
name: prompt-design
description: |
  基于 Anthropic 官方准则的提示词设计、优化和质量检查工具。适用场景：
  (1) 创建新提示词 - 用户说"帮我创建/设计一个XXX提示词"
  (2) 优化现有提示词 - 用户说"优化/改进这个提示词"
  (3) 检查提示词质量 - 用户说"检查/审查这个提示词"
  (4) 理解提示词结构 - 用户询问"如何设计提示词"或"提示词最佳实践"
---

# Prompt Design Skill

基于 [Anthropic Prompt Library](https://docs.anthropic.com/en/prompt-library/library) 官方准则的提示词设计助手。

## 核心工作流

### 创建新提示词

1. **确定类型** - 识别任务场景（编程/文档/创意/教育/学术）
2. **选择模板** - 参考 [templates.md](references/templates.md) 选择对应模板
3. **填充内容** - 按模板结构填写各标签内容
4. **质量检查** - 使用 [quality-checklist.md](references/quality-checklist.md) 验证
5. **输出提示词** - 交付完整的 System Prompt + User Prompt

### 优化现有提示词

1. **诊断问题** - 识别输出质量问题（幻觉/格式混乱/逻辑不清）
2. **对照准则** - 检查是否符合下方 XML 标签规范
3. **应用模板** - 重构为标准结构
4. **增强机制** - 添加 CoT/引用验证/XML 标签等

## XML 标签规范

Claude 在训练中使用了 XML 标签，推荐使用以下结构：

### 核心结构标签

| 标签 | 用途 | 关键要求 |
|------|------|----------|
| `<role>` | 角色定义 | 明确身份、专业背景 |
| `<task>` | 任务声明 | 使用 "Your task is to..." |
| `<thinking>` | 内部推理 | **必须标注"不直接输出给用户"** |
| `<instructions>` | 操作指令 | 包含步骤 + **格式选择逻辑** |
| `<output_format>` | 输出格式 | **仅通用规范，禁止多模板并列** |
| `<constraints>` | 约束条件 | 使用肯定式指令 |

### 标签职责分离原则

**核心规则：** 多场景提示词中，格式选择逻辑放 `<instructions>`，`<output_format>` 只写通用规范。

```
❌ 错误：output_format 并列多种格式
<output_format>
【分析类】**分析过程：** [...]
---
【事实类】**回答：** [...]
</output_format>

✅ 正确：格式选择在 instructions
<instructions>
X. **格式选择**：根据问题类型：
   - 分析类：使用 "**分析过程**" + "**结论**"
   - 事实类：使用 "**回答**" + "**来源**"
</instructions>
<output_format>
使用 Markdown 格式，对比数据用表格
</output_format>
```

### 内容包装标签

| 标签 | 用途 |
|------|------|
| `<document>` | 包裹参考文档 |
| `<code>` | 包裹代码片段 |
| `<example>` | Few-Shot 示例 |
| `<context>` | 背景信息 |

### 高级推理标签

| 标签 | 用途 |
|------|------|
| `<scratchpad>` | 中间计算/推理步骤 |
| `<reasoning>` | 结构化逻辑推导 |
| `<verification>` | 结果自检 |

## 设计准则

### 1. 肯定式优于否定式

```
❌ "Don't make up information"
✅ "Only use information from the provided document. If uncertain, say 'I don't know'"
```

### 2. 思维链引导

复杂任务添加逐步思考：

```
Think step by step before providing your final answer.
First, analyze the problem. Then, consider possible approaches. Finally, provide your solution.
```

### 3. System vs Human Prompt 分工

| 类型 | 内容 |
|------|------|
| **System** | 角色定义、全局约束、工具定义 |
| **Human** | 具体任务、输入数据、特定要求 |

## 场景特定要点

| 场景 | 关键要素 |
|------|----------|
| **编程类** | `<code>` 标签 + 注释要求 + 错误处理 |
| **文档类** | `<document>` 标签 + 格式化输出 |
| **学术类** | ReAct 验证 + CoT + LaTeX 公式 |
| **引用类** | 仅使用提供文档 + 引用来源 + 置信度 |

## 详细参考

- **完整模板**: [references/templates.md](references/templates.md)
- **质量检查清单**: [references/quality-checklist.md](references/quality-checklist.md)
