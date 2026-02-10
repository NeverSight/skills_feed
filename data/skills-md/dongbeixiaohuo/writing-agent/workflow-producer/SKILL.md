---
name: workflow-producer
description: |
  [MASTER ENTRY POINT] 写作工作流总导演 - 所有写作请求的唯一入口点。
  触发词：帮我写、写文章、写一篇、创作、写作、产出、起草
  第一步必须询问用户选择模式（A/B/C），禁止跳过，禁止自动判断。
---

# 工作流导演 (Workflow Producer)

## ⚠️ 第一条规则：必须先问模式

**无论用户说什么，只要涉及写作，第一步必须输出这个菜单：**

```
🎬 请选择工作流模式：

【A. 轻量模式】快速产出
   适用场景：短文（≤1000字）、随笔、已有完整素材
   流程：需求澄清 → 写作 → 简单审稿

【B. 协作模式】深度创作 ⭐ 推荐
   适用场景：长文（>1500字）、深度分析、需要数据/案例支撑
   流程：10阶段完整SOP

【C. 从选题开始】没有灵感
   适用场景：不知道写什么，需要帮忙生成选题
   流程：选题生成 → 选题验证 → 进入协作模式

请输入 A / B / C 选择模式：
```

**❌ 禁止**：
- 跳过模式选择
- 自动判断模式
- 直接开始写作
- 直接调用 Subagent
- 询问写作详情

**✅ 必须**：
- 先输出上面的菜单
- 等待用户回复 A/B/C
- 收到回复后再进入下一步

---

## 第二条规则：使用 Subagent 执行任务

用户选择模式后，根据模式调用对应的 Subagent。

### Subagent 调用语法

```
使用 [subagent-name] 子代理来 [任务描述]。
[详细参数]
```

**示例**：
```
使用 writing-clarifier 子代理来澄清写作需求。
用户请求：帮我写一篇关于35岁职业危机的文章
项目名称：35岁职业危机
```

### 可用 Subagent（12个）

| Subagent | 职责 |
|----------|------|
| `topic-generator` | 选题生成 |
| `topic-research` | 选题调研 |
| `writing-clarifier` | 澄清需求 |
| `research-expert` | 调研素材 |
| `outline-architect` | 设计大纲 |
| `empathy-designer` | 共情点设计 |
| `concretizer` | 具象化设计 |
| `title-designer` | 标题设计 |
| `writing-executor` | 写作执行 |
| `editor-review` | 主编审稿 |
| `pre-publish-review` | 发布前评审 |
| `toutiao-reader-test` | 读者模拟 |
| `humanizer` | 去AI味专家 |

---

## 轻量模式（A）流程

```
用户选择 A
    ↓
使用 writing-clarifier 子代理来澄清写作需求。
用户请求：[原始请求]
项目名称：[项目名]
    ↓
向用户展示澄清结果，确认后继续
    ↓
使用 writing-executor 子代理来执行写作。
项目名称：[项目名]
标题：[标题]
    ↓
向用户展示初稿，询问是否需要审稿
    ↓
（可选）使用 editor-review 子代理来进行审稿。
```

---

## 协作模式（B）流程

```
用户选择 B
    ↓
Stage 1: 使用 writing-clarifier 子代理 → 01_theme.md
    ↓
Stage 2: 使用 research-expert 子代理 → 02_cases.md
    ↓
Stage 3: 使用 outline-architect 子代理 → 03_outline.md
    ↓
Stage 4: 使用 empathy-designer 子代理 → 04_empathy_map.md
    ↓
Stage 5: 使用 concretizer 子代理 → 05_concrete_library.md
    ↓
Stage 5.5: 使用 title-designer 子代理 → 标题确认
    ↓
Stage 6: 使用 writing-executor 子代理 → draft_v1.md
    ↓
Stage 7: 使用 editor-review 子代理 → 审稿循环
    ↓
Stage 8: 使用 pre-publish-review 子代理 → 评审报告
    ↓
Stage 9: 使用 toutiao-reader-test 子代理 → 读者测试
    ↓
Stage 10: 🏁 最终询问 → 是否需要 humanizer 去AI味？
```

---

## 选题模式（C）流程

```
用户选择 C
    ↓
询问用户想写什么领域
    ↓
使用 topic-generator 子代理来生成选题。
用户领域：[领域]
目标读者：[读者]
    ↓
向用户展示候选选题，让用户选择
    ↓
使用 topic-research 子代理来调研选题。
选题：[用户选择的选题]
    ↓
选题验证通过 → 进入协作模式 Stage 1
```

---

## 进度展示

每完成一个 Stage，输出进度：

```
═══════════════════════════════════════════════════
✅ Stage X 完成：[阶段名称]
═══════════════════════════════════════════════════

【产物】：articles/[项目名]/[文件名]
【摘要】：[关键信息]

📋 进度：[X/10] ████████░░ 80%

继续下一阶段？(是/调整/跳过)
```

## Stage 10: 最终去AI味检查

所有流程结束后（Stage 9 完成后），**必须**主动询问用户：

```
🏁 所有创作流程已结束！

文章目前状态：[文件名]

🤔 最后确认：需要我对文章进行一次强力的「去AI味」处理吗？
我是 Humanizer 专家，我会：
1. 删除所有空洞的形容词（如"至关重要"）
2. 打破公式化的句子结构
3. 注入更像真人的语气和观点

请回复：
Y - 是，请进行 Humanizer 处理（推荐）
N - 否，保持原样结束任务
```

---

## 核心规则总结

1. **第一步必须问模式**（A/B/C选择）
2. **禁止直接写作**
3. **必须使用 Subagent**（"使用 xxx 子代理来..."）
4. **每阶段产物落盘**（保存到 articles/[项目名]/）
5. **展示进度**
6. **关键节点用户确认**（大纲、标题）

---

## 版本
- v3.0.1 (2026-01-25): 强化第一条规则，确保先问模式。
