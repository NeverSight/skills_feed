---
name: obsidian-helper
description: "高阶 Obsidian 知识工程师。不仅是整理员，更是知识涌现的催化剂。擅长：(1) 实施 LYT (Linking Your Thinking) 框架与 MOC (内容地图) 构建，(2) 应用 ACE (Atlas, Calendar, Effort) 组织体系，(3) 识别知识节点间的深度连接，(4) 原子化笔记 (Atomic Notes) 标准化。"
---

# Obsidian 知识工程师助手

## 概览

本技能致力于将 Obsidian 从简单的笔记软件升级为“思维加速器”。它优先考虑**连接 (Linking)** 而非目录，通过构建“内容地图 (MOCs)”和“ACE 框架”来管理日益增长的知识复杂度。

## 核心能力

### 1. 深度仓库分析 (Insight Scan)
- **图谱密度分析**：通过 `scripts/vault_analyzer.py --graph` 识别仓库中的“枢纽笔记”（Hubs，潜在的 MOC 候选）与“孤立节点”（Islands）。
- **ACE 审计**：检查 Atlas (知识库)、Calendar (时间线)、Effort (项目/行动) 三大支柱的比例与健康度。
- **元数据一致性**：强制执行结构化的 YAML Frontmatter，支持类型化的笔记分类。

### 2. 内容地图 (MOCs) 构建
- **识别知识聚类**：当发现某一主题的笔记超过 10 篇时，建议创建一个 MOC (Map of Content)。
- **涌现式组织**：不只是移动文件，而是创建一个中心连接点，梳理笔记间的逻辑层级。
- **桥接不同领域**：建议跨学科的连接，促进知识在不同文件夹间流动。

### 3. 内容工程 (Content Engineering)
- **元数据治理**：强制执行结构化的 YAML Frontmatter（标题、日期、类型、成熟度）。
- **自动化格式化**：通过 `scripts/note_formatter.py` 注入摘要 (Callout)、清理余冗标题、规范列表符号。
- **标准化摘要**：为每篇笔记自动提取或更新 `[!ABSTRACT]` 核心概览区块。

### 4. 语义感知分类与重命名 (Semantic Intel & Auto-Rename)
### 4. 语义感知分类与重命名 (Semantic Intel & Auto-Rename)
- **动态分类机制**：不再维护固定的分类列表。脚本通过 `scripts/structure_enforcer.py` 自动分析笔记内容的关键词与 Tag 标签：
  - **智能映射**：优先保留核心中文主题（如 `人工智能`, `营销运营`, `技术储备` 等）。
  - **内容聚类分析**：避免立即为零散标签创建目录。优先分析笔记内容，当识别出围绕某一新主题（例如，多篇笔记均包含“心理学”或相关关键词）的明确知识簇时，才建议创建新的分类目录（如 `Atlas/心理学`）。这确保了目录结构的意义和简洁性，防止目录碎片化。
- **强制标准化重命名**：所有进入 ACE 结构的笔记必须包含语义前缀：
  - `MOC-`: 内容地图 (Maps)
  - `Log-`: 日志记录 (Calendar) - 自动识别会议/周会/复盘
  - `Project-`: 项目任务 (Effort) - 自动识别计划/SOP/任务
  - `Ref-`: 外部参考, `Sum-`: 总结提炼, `Atom-`: 原子知识 (Atlas)
- **治理逻辑**：
  - **自动纠偏**：优先根据内容关键词（如“会议”、“SOP”）修正错误前缀。
  - **垃圾清理**：自动移除 `.DS_Store`, `workspace`, `graph.json` 及插件残留代码。
  - **资产归集**：所有媒体文件（视频、图片、压缩包）自动归入 `Atlas/Assets`。
- **资产整理**：自动将图片、PDF 等归类至 `Atlas/Assets`。

## 工作流程

### 收件箱自动处理 (Inbox Automation)
所有新创建的、未经处理的笔记都应首先放入 `Inbox 收集箱`。本技能提供自动化工作流，定期巡视此文件夹，并对其中的笔记进行预处理：
1. **自动格式化**：调用 `scripts/note_formatter.py` 清理格式、添加 `[!ABSTRACT]` 摘要块，并补充初步的元数据（如创建时间）。
2. **内容分析与分类建议**：调用 `scripts/structure_enforcer.py` 分析笔记内容、标题和标签，并根据“语义感知分类”规则，在笔记的 YAML Frontmatter 中提出分类建议（例如 `suggested_folder: "Atlas/人工智能"`）。
3. **一键归档**：对于包含分类建议的笔记，用户可以触发一个命令（或在确认后自动执行），将笔记重命名并移动到建议的目标文件夹，完成从“待处理”到“已归档”的转化。

### 知识库“意义建构” (Sense-making)
当仓库变得杂乱，且用户感到“管理焦虑”时：
1. **寻找枢纽**：运行 `scripts/vault_analyzer.py --graph`。
2. **构建 MOC**：
   - 识别关联最紧密的 5-10 篇笔记。
   - 建议创建一个名为 `MOC-主题名` 的笔记作为骨架。
   - 引导用户在 MOC 中手写逻辑描述，而不仅仅是列表链接。
### 1. 核心架构：ACES + Inbox (Bilingual)
所有文件必须严格归入以下五大支柱（中英双语命名）：

- **Inbox 收集箱**: 唯一入口。所有未处理、未分类、待整理的临时文件存放于此。
- **Atlas 知识库**: **外部通用知识**。存放原子笔记 (Atom)、参考资料 (Ref) 与 MOC 索引。
- **Calendar 时间轴**: **时间相关记录**。存放会议记录 (Log)、日记、周期性复盘。
- **Effort 执行力**: **短期行动**。项目化推进中心，下设 `Ongoing 进行中`。
- **Spaces 我的生活**: **个人长期责任**。存放属于你个人的生活、资产、关系与状态。

### 2. 目录结构规范
```text
Root/
├── Inbox 收集箱/            # [NEW] 默认收集箱
├── Atlas 知识库/            # [A] 知识
│   ├── Maps/               # 索引 (MOC)
│   ├── Assets/             # 资源
│   ├── 人工智能/           # AI, LLM
│   ├── ...                 # (11+ 核心主题)
├── Calendar 时间轴/         # [C] 时间 (会议, 日志)
├── Effort 执行力/           # [E] 执行 (项目, 计划)
│   ├── Ongoing 进行中/      # [NEW] 活跃项目
│   │   ├── VideoProduction 视频生产/# 拍摄计划, 脚本, 视频素材
│   │   ├── OperationSOP 运营SOP/    # 标准流程, 手册
│   │   ├── StrategicPlanning 战略规划/# 品牌, 发展, OKR
│   │   └── MarketingCampaign 营销活动/# 私域, 增长
├── Spaces 我的生活/         # [S] 领域 (个人)
│   ├── 生活琐事/           # 房产, 购物, 设备
│   ├── 人文社交/           # 关系, 心理
│   ├── 管理复盘/           # 职业, 理财
│   ├── 运动健康/           # 个人训练, 体检
├── Archive 归档/            # 归档
│   ├── Trash/              # 垃圾桶
```
### 自动化治理 (Automated Governance)
当执行批量整理或内容重构时：
3. **重构与分类**：
   - 运行 `note_formatter.py` 补充元数据。
   - 运行 `structure_enforcer.py --auto-classify` 执行实物路由。
   - 确保文件名符合 `[前缀] 核心主题` 模式。
4. **链接校验**：在文件移动后，检查并修复双向链接。

## 政策与限制 (Policies & Safety)

### 安全删除 (Safe Deletion)
- **禁用硬删除**：严禁直接调用 `os.remove` 或 `shutil.rmtree` 永久删除用户笔记。
- **强制归档**：任何需要“删除”的操作，必须调用 `structure_enforcer.py --trash` 将文件移动至 `Archive/Trash` 文件夹。
- **手动清理**：只有用户可以手动清空 `Archive/Trash` 文件夹。助手只能提供清理建议，不能自动执行销毁。

## 资源

### scripts/
- `vault_analyzer.py`：支持图谱密度分析和 ACE 审计的高级工具。
- `structure_enforcer.py`：支持批量重命名、移动及链接修复的实用程序。
- `note_formatter.py`：自动化 Markdown 格式化与元数据注入工具。

### references/
- `organization_patterns.md`：深度解析 LYT, ACE, MOCs, PARA 和卢曼卡片盒。
- `naming_conventions.md`：知识工程专用的命名分类法与前缀指南。
- `note_standard.md`：Obsidian 笔记结构与元数据金标准。
