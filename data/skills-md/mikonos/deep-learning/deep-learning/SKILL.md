---
name: deep-learning
description: 全能深度阅读工具（All-in-One Deep Reading）。适用于书/长文/研报/论文的深度消化。Use when 用户要深度消化一本书/长文/研报/论文并构建知识网络、产出结构笔记与原子笔记。融合 Mortimer Adler（结构）、Feynman（解释）、Luhmann（网络）、Pragmatist（工具化）、Critics（辩论）；强制 High Fidelity 案例保留与 Actionable 工具提取。关键词：深度阅读、结构笔记、deep learning、卢曼。
---

# 深度阅读 (Deep Reading)

> **核心理念**：不仅要理解世界（Understand），还要改变世界（Act）。
> **适用范围**：Book, Long-form Article, Research Report, Academic Paper.

## 专家座席 (The Council)

1.  **Mortimer Adler** (The Architect): 负责结构化，提取核心命题和逻辑树。
2.  **The Pragmatist** (The Engineer): 负责工具化，提取可执行的 SOP、模板和清单。
3.  **Richard Feynman** (The Teacher): 负责解释力，确保概念去魅，用人话讲清楚。
4.  **Niklas Luhmann** (The Librarian): 负责连接性，确保知识入网，有机生长。
5.  **The Critics** (The Stress Testers): Musk, Socrates, Munger 负责压力测试和辩论。

---

## 核心法则 (The Iron Rules)

1.  **Always Deep**: 无论输入长短，默认按最高规格处理（结构+工具+辩论）。
2.  **Case Fidelity (案例保真)**:
    *   **有原文/书在手**：禁止概括性改写；原子笔记中涉及案例、研究处须保留**具体数字、作者/机构、时间线、原话**（可标页码）。
    *   **无原文、仅摘要或记忆**：在笔记中标注 `来源: 本书/摘要，未核对原文`；保留能确定的专有名词与结论，**禁止编造细节**；Feynman 验收时标「案例保真：部分（无原文）」。
3.  **No Vague Verbs (模糊词禁令)**: 禁止使用 "优化"、"加强"、"适当" 等虚词。必须转化为**具体动作**或**量化指标**。
4.  **Metadata Mandatory (元数据强制)**: 所有笔记必须包含 YAML Frontmatter (type, tags, links)。**禁止省略**。

---

## 存储规则 (Storage Rules)

1.  **默认位置**: `05_每日记录 (Daily)/YYYY/MM/DD`
    *   获取当前日期 (YYYY, MM, DD)，若日期文件夹不存在则创建；创建本次任务文件夹。
    *   **任务文件夹命名规范**: 任务文件夹默认 `[标题]_结构笔记.md`。
    *   **结构笔记命名规范**: 结构笔记默认 `YYYYMMDD_00_[标题]_结构笔记.md`。

2.  **结构笔记接入** (二选一，见 Phase 6):
    *   **方式 A**：若目标索引有 `## Inbox`，在 Inbox 下追加本书入口（如 `- [[本书结构笔记]] — 书名，YYYYMMDD`）。
    *   **方式 B**：若目标索引无 Inbox，则新建 Inbox章节

3.  **索引笔记入网** (见 Phase 2.5)：将新建索引笔记挂载到已存在索引，并移动到 `03_索引/` 下合适文件夹；具体 Inbox/入口写法见 Phase 2.5。

---

## 工作流程 (The Workflow)

**执行顺序**：Phase 0 → 1 → 2 → 2.5 → 3 → 4 → 5 → 6 → **6.5（流程执行审查，强制）**，不可跳步；Phase 2.5 须在 Phase 2 完成后立即执行；Phase 6.5 须在 Phase 6 完成后立即执行。

### Phase 0: Pre-game Plan (准备)
在开始 Phase 1 前产出执行计划；落盘为 `YYYYMMDD_01_[书名]_执行计划.md`（与结构笔记同目录），并在 task.md 的 Preparation 下链接该文件。

确保包含：
1.  **TODO List** (≥6 项)：如全书论证骨架、关键概念、论证链、框架提取、方法提取、案例核实、批判性审查、入网连接。
2.  **Context**：读取意图（我要解决什么问题？）。

### Phase 1: Overview & Structure (概览与骨架)
**Agent**: Mortimer Adler

1.  **任务**: 创建结构笔记；产出须符合 `templates/structure_note_template.md`，含核心命题与逻辑支撑链。
2.  **说明**: 强制调用 `structure-note` skill

### Phase 2: Index Design (索引设计)
**Agent**: Niklas Luhmann
> "不要问它属于哪个分类，问它和谁对话。"

1.  **任务**: 为本书创建索引笔记；产出须符合本书 `templates/index_note_template.md`，含关键词与多入口。
2.  **说明**: 强制调用 `index-note` skill；

### Phase 2.5: 索引笔记入网 (Index Note Onboarding)
**Agent**: Niklas Luhmann

索引笔记创建完成后立即执行；确保新索引被知识网络接纳且物理归位。

1.  **挂载到已存在索引**：在 `03_索引/` 下选定一个（或多个）与本书主题相关的**已存在索引**，在其中添加入口指向本索引笔记（如 `## Inbox` 下追加 `- [[本索引笔记名]] — 书名/主题，YYYYMMDD`，或在该索引的「主题结构/子索引」板块添加）。确保双向链接：本索引笔记底部也链回该父索引。
2.  **移动到索引目录**：将本索引笔记文件从当前任务目录（如 `05_每日记录/...`）**移动**到 `03_索引 (Index)/` 下合适位置：
    *   使用 `file-organize` skill 评估：根目录（与现有 Hub 并列）或某主题子文件夹（如 `某主题相关/`）。
    *   移动后父索引中的 `[[本索引笔记名]]` 仍有效（仅文件名，不依赖路径）。
3.  **（多索引挂载检查延后至 Phase 6）**：本索引**内提到的笔记**还可挂到哪些其他索引，在 Phase 6 统一检查并添加入口。

### Phase 3: Recursive Growth (递归生长)
**Agent**: Luhmann & Feynman
> 核心创新：边创建边发现 (Luhmann Scan)。

**流程**:
1.  **Round 1 (骨架)**: 从结构笔记出发，创建所有显式链接的 **Atomic Note (概念)**。
2.  **Luhmann Scan (每张必做)**：见 `references/luhmann_scan.md`。三项——前置依赖、潜在连接、**方法论发现**（若概念附带可执行 how → 记入 task，Phase 4 创建详细的 Method Note）。在 task.md 中每张卡记录格式：`前置 → Round 2: [[A]]. 连接 → Round 3: [[B]]. 方法论 → [[方法名]] (Phase 4).`
3.  **Round 2 (血肉)**: 创建发现的新笔记，继续 Luhmann Scan。
4.  **Round 3+ (边缘)**: 直到完成或超出范围。

**Atomic Note 规范**:
*   **模板**: `templates/atomic_note_template.md`
*   **聚焦**: 定义 (Definition)、机制 (Mechanism)、语境 (Context)。
*   **验收**: 费曼测试 (外行能听懂)。

### Phase 4: Methodology Consolidation (方法论整理)
**Agent**: The Pragmatist

将 Phase 3 发现的方法论创建为 Method Note。

**Method Note 规范** (*高优先级*):
1.  **模板**: `templates/method_note_template.md`
2.  **聚焦**: 可执行步骤 (SOP)、模板 (Template)、检查清单 (Checklist)。
3.  **约束**:
    *   **No Vague Verbs**: 无模糊动词。
    *   **Mechanism & Leverage**: 为什么有效？
    *   **MVE**: 下一步最小可行性实验。

### Phase 5: Final Review (终极审视)
**Agent**: Richard Feynman

用 Feynman 标准审视整个知识网络：
1.  **去魅检验**: 术语是否已"翻译"为日常语言？
2.  **比喻检验**: 复杂概念是否有恰当比喻？
3.  **逻辑检验**: 论证链是否有断裂？
4.  **拓扑检验**: 是否形成了"意外的惊喜"连接？

### Phase 6: Network Review (入网审视)
**Agent**: Niklas Luhmann

1.  **检查**: 确认每张笔记（非结构父子）至少有 2 条双向链接。
2.  **入网**: 在 `03_索引/` 下相关索引中完成接入——`## Inbox` 无则新建 Inbox；结构笔记与原子笔记按关键词/主题入对应索引。必要时调用 `index-note` 模式三（内容入网）执行单篇/批量入网。
3.  **多索引挂载检查**: 针对**本索引内提到的笔记**（本索引关键词区、主题结构区所链接的笔记），逐条评估是否还应挂载到 `03_索引/` 下**其他**索引（不同查找意图）；若某笔记也是其他主题的优质入口，则在对应索引中添加入口，实现多入口可达。输出简要清单：`[[笔记A]] → 已入 索引_X；建议补充入 索引_Y（理由）`。

### Phase 6.5: 流程执行审查（强制）

**Phase 6 完成后必须执行**。调用 **workflow-audit** skill，以德明+葛文德视角对本流程执行完成度逐项核对与系统闭环检查：

1. **审查对象**：本 skill（deep-learning）；**产出**：本次任务目录（执行计划、结构笔记、索引、原子笔记、task.md 等）。
2. **产出**：落盘审查报告（`YYYYMMDD_[任务名]_流程审查报告_德明与葛文德视角.md`），含逐项清单、系统闭环、DoD 勾选、多索引挂载清单；对审查中标为 ❌ 的项**必须补执行**，直至 DoD 全部通过。
3. **workflow-audit 主文件**：`.cursor/skills/workflow-audit/SKILL.md`；报告模板：`workflow-audit/references/audit_report_template.md`。

> 不可跳过。未通过流程执行审查并补全漏项，则本流程视为未完成。

---

## 任务追踪 (Task Tracking)

在 `task.md` 中维护进度：

```markdown
# Preparation
- [ ] Pre-game Plan Created (≥6 项 TODO + Context；对话内区块或落盘文件)

# Structure & Index
- [ ] Structure Note Created (Adler)
- [ ] Index Note Created (Luhmann)
- [ ] Index Note Onboarding (Phase 2.5): 挂载到已存在索引 + 移动到 03_索引 文件夹

# Extraction Loop (Phase 3)
- [ ] [[笔记A (Concept)]] + Luhmann Scan
- [ ] [[笔记B (Concept)]] + Luhmann Scan

# Methodology (Phase 4)
- [ ] [[工具A (Method)]] (SOP/Checklist/MVE)

# Review (Phase 5 & 6)
- [ ] Feynman Check (De-jargon check)
- [ ] Network Check (2+ Links per note；索引入网：Inbox 或关键词条目；多索引挂载检查)

# Workflow Audit (Phase 6.5，强制)
- [ ] 调用 **workflow-audit** 做流程执行审查（德明+葛文德视角），产出审查报告并对 ❌ 项补执行，直至 DoD 全部通过
```

---

## 质量验收清单 (Definition of Done)

- [ ] **Phase 0**: 执行计划已产出（≥6 项 TODO + Context）。
- [ ] **Overview**: 5个问题回答清晰，费曼测试通过。
- [ ] **Fidelity**: 有原文时案例含数字/专有名词/原话；无原文时已标注来源限制且未编造细节。
- [ ] **Actionability**: Method Note 包含无模糊词的步骤 + 可复制模板。
- [ ] **Network**: 所有笔记双向可达 (≥2 links)；已在 03_索引 相关索引入网（Inbox 或关键词条目）；本索引已挂载到已存在索引并位于 03_索引 下；多索引挂载检查已完成。
- [ ] **Insight**: 产生了新的连接或意外发现。
- [ ] **流程执行审查**：Phase 6.5 已执行，workflow-audit 已产出审查报告，且所有 ❌ 项已补执行、DoD 全部通过。
