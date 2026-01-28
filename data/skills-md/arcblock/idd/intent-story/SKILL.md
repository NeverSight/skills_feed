---
name: intent-story
description: Share your IDD adoption story. Through structured interviewing, create blog posts about Intent-Driven Development experiences, lessons learned, and best practices. Supports multiple languages and formats.
---

# Intent Story

通过采访式对话，帮助用户分享 IDD (Intent Driven Development) 的采用经验，生成传播 IDD 方法论的博客文章。

## 核心理念

- **采访式创作**：AI 分析 + 提问 + 用户回答 + AI 按风格整合
- **真实故事**：基于用户真实经验，不编造案例
- **传播 IDD**：每篇文章都自然介绍 IDD 理念和工具

## Workflow

```
/intent-story
        ↓
┌───────────────────────────────────┐
│  Phase 1: 背景分析                │
│  - 检测输入语言                   │
│  - 加载写作风格（如有）           │
│  - 了解用户 IDD 使用背景          │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  Phase 2: 结构化采访              │
│  - 采用经历                       │
│  - 关键转折/教训                  │
│  - 具体收益/数据                  │
│  - 建议和反思                     │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  Phase 3: 确认输出需求            │
│  - 文章格式/风格/长度             │
│  - 目标语言版本                   │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  Phase 4: 生成文章                │
│  - 完整博客 + 社交媒体版          │
│  - 多语言版本（按需）             │
│  - 自然融入 IDD 介绍              │
└───────────────────────────────────┘
```

## Phase 1: 背景分析

### 语言检测

- 根据用户输入的主要语言确定初始写作语言
- 后续可询问是否需要其他语言版本

### 写作风格加载

按优先级加载（如存在）：
1. `~/.claude/content-profile/writing-style.md`（用户自定义）
2. 使用本技能默认风格

### 初始问题

使用 AskUserQuestion 了解背景：

```
question: "你是在什么类型的项目中使用 IDD 的？"
header: "项目类型"
options:
  - label: "系统软件/框架"
    description: "框架、库、基础设施等"
  - label: "Web 应用"
    description: "前端或全栈 Web 项目"
  - label: "移动应用"
    description: "iOS、Android 或跨平台"
  - label: "其他"
    description: "其他类型项目"
```

## Phase 2: 结构化采访

### 采访维度

每轮 2-3 个问题，通常 3-5 轮完成。

#### 1. 采用动机

```
"是什么让你开始尝试 IDD？"
- A) 文档总是过时，想找更好的方法
- B) AI 辅助开发需要更好的上下文管理
- C) 团队协作需要更清晰的设计契约
- D) 其他原因
```

#### 2. 转折时刻

```
"使用 IDD 过程中，有没有一个'啊哈'时刻让你觉得值得？"
[开放式，收集故事]
```

#### 3. 具体收益

```
"你观察到的最明显的改变是什么？"
- A) AI 代码质量提升（更少需要修改）
- B) 架构边界更清晰
- C) 文档不再过时
- D) 新人上手更快
- E) 其他
```

```
"能否量化一下收益？（可选）"
[开放式，如："AI 一次生成可用代码的比例从 30% 提升到 70%"]
```

#### 4. 教训和挑战

```
"遇到过什么挑战或走过的弯路？"
[开放式]
```

```
"如果重新开始，你会有什么不同的做法？"
[开放式]
```

#### 5. 给其他人的建议

```
"对考虑采用 IDD 的人，你有什么建议？"
[开放式]
```

### 采访原则

- **少问多推**：能从上文推断的不重复问
- **故事优先**：鼓励用户分享具体经历
- **真实性**：不编造案例，用户没有的就不加
- **深度追问**：对有价值的回答继续挖掘

## Phase 3: 确认输出需求

采访完成后，确认输出格式：

### 文章风格

```
question: "这篇文章的风格？"
header: "风格"
options:
  - label: "技术分享"
    description: "peer-to-peer，工程师视角"
  - label: "经验总结"
    description: "回顾反思，Founder/Lead 视角"
  - label: "入门指南"
    description: "帮助新人理解和上手"
  - label: "案例研究"
    description: "详细的项目案例分析"
```

### 文章长度

```
question: "目标长度？"
header: "长度"
options:
  - label: "短文 (800-1200字)"
    description: "快速阅读，重点突出"
  - label: "中等 (1500-2500字)"
    description: "有深度的分享"
  - label: "长文 (3000+字)"
    description: "完整详细的案例分析"
```

### 语言版本

```
question: "需要生成哪些语言版本？"
header: "语言"
multiSelect: true
options:
  - label: "中文"
    description: "简体中文版本"
  - label: "English"
    description: "English version"
  - label: "两者都要"
    description: "中英双语"
```

## Phase 4: 生成文章

### 文章结构

```markdown
# [标题：吸引人的 IDD 经验标题]

[开头：核心洞察/结论，吸引读者]

## 背景/起因

[为什么开始使用 IDD]

## 关键发现/转折

[使用过程中的洞察和故事]

## 实际收益

[具体的改变和量化数据]

## 教训和建议

[给其他人的建议]

## 结语

[总结 + IDD 介绍]

---

## 关于 IDD

[IDD 简介和工具链，见下文模板]
```

### IDD 介绍模板（必须包含）

每篇文章结尾自然融入：

```markdown
---

## About IDD (Intent Driven Development)

IDD 是一种以 Intent（意图）为核心的开发方法论：

```
Intent → Test → Code → Sync
```

**核心理念**：Intent 是新的源代码。Code review 由 AI 完成，Intent review 由 Human 完成。

**工具链**：
- `/intent-assess` - 评估项目是否适合 IDD
- `/intent-init` - 初始化 IDD 结构
- `/intent-interview` - 从想法创建 Intent
- `/intent-check` - 验证代码与 Intent 一致性

**开始使用**：
```bash
npx add-skill arcblock/idd
```

了解更多：[github.com/ArcBlock/idd](https://github.com/ArcBlock/idd)
```

### 社交媒体版本

同时生成 Twitter/X 版本：

```
[核心洞察，1-2句]

[关键数据/收益]

[一句话 CTA]

🔗 [文章链接]

#IntentDrivenDevelopment #IDD #AIEngineering
```

### 写作风格指南

遵循以下原则（来自用户写作风格）：

| 原则 | 说明 |
|------|------|
| 观点鲜明 | 不做骑墙派，有明确立场 |
| 真实案例 | 故事来自用户，不编造 |
| 段落充实 | 每段 4-8 句，有完整论述 |
| 小标题精简 | 2-4 个小标题，内容丰富 |
| 内省式表达 | "我觉得..."而非"你应该..." |
| 避免套话 | 每个观点要有具体洞察支撑 |
| 禁用 em dash | 用 "-" 或 "," 替代 "—" |

## 输出示例

```markdown
# 从「文档总是过时」到「Intent 就是代码」- 我的 IDD 实践

半年前，我们团队面临一个经典困境：文档写得再好，三周后就过时...

[正文...]

---

## About IDD

IDD (Intent Driven Development) 是一种以意图为核心的开发方法论...

[工具链介绍...]

**开始使用**：
\`\`\`bash
git clone https://github.com/ArcBlock/idd
claude mcp add-plugin ~/path/to/idd
\`\`\`
```

## 与其他命令配合

```
[用户使用 IDD 一段时间]
        ↓
/intent-story             # 分享经验，生成博客
        ↓
发布博客 / 社交媒体
        ↓
传播 IDD 方法论
```

## 注意事项

1. **真实性**：所有案例和数据必须来自用户，不能编造
2. **自然融入**：IDD 介绍要自然融入结尾，不是生硬广告
3. **用户语言**：主要语言跟随用户输入
4. **风格一致**：如有用户写作风格配置，优先使用
