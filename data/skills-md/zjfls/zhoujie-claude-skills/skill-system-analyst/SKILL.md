---
name: skill-system-analyst
description: 系统/代码库架构分析与技术文档编排（mindmap 驱动，分章节 append/render），生成可视化（Mermaid）且注意 XSS 安全的深度报告。
---

# Skill: System Analyst (Mindmap-Driven)

用“先制图（全局地图），再下潜（逐叶节点深挖）”的方式，生成**细致、结构化、可视化**的系统分析文档。你不是一次性写完，而是像写书一样：**分解 → 计划 → 分章执行 → 校验 → 汇总**。

## 适用场景
- 接手陌生代码库，需要快速但不粗糙地建立系统认知
- 架构评审/技术尽调：关注边界、权衡、风险、演进路径
- 需要产出可分享的分析报告（HTML + Mermaid + mindmap）

## 输出标准（深度门槛）
每个“章节”至少包含：
- **范围与职责**：这个模块解决什么问题，不解决什么
- **关键证据**：具体到文件路径、关键函数/类、关键配置项
- **数据/控制流**：至少 1 张 Mermaid（组件图/时序图/数据流图择一）
- **关键权衡**：为什么这样设计（trade-offs），替代方案是什么
- **风险分级**：安全/可靠性/性能/可维护性风险（高/中/低），并给出修复建议

默认以中文输出（除非用户要求英文）。

## 核心规则
1. **必须编排**：禁止“一口气写完整报告”；必须用 `doc-generator.js` 分章节追加。
2. **必须可追溯**：关键结论要落到“文件 + 入口 + 证据”，禁止空泛描述。
3. **必须可视化**：每个重要章节都要有 Mermaid，或明确引用全局 mindmap 的节点。
4. **必须安全**：输出 HTML 中展示代码/用户输入时必须转义（例如 `&lt;script&gt;`）。

## 工具约定（在 Codex CLI 中）
优先用可复现的命令提取证据：`ls`、`rg -n`、`sed -n`、`git log`、`git blame` 等。

## 工作流（系统性执行）

### Phase 0：需求澄清（先问清楚再开始）
在动手扫描前，先确认：
- 分析目标：架构总览 / 安全审计 / 性能瓶颈 / 可维护性 / 上线风险
- 受众：开发/架构/管理层（决定术语密度与建议形式）
- 产出范围：需要覆盖哪些模块/路径，是否要包含改进方案与优先级

### Phase 1：Cartography（全局制图 + 计划）
1. **全局扫描**：找入口（main/server/app）、路由、任务调度、配置、依赖、数据存储、外部集成点。
2. **构建 mindmap**（Markdown 列表，≥3 层）：覆盖 Server / DB / Async / View / Security / Config / Observability。
3. **把 mindmap 转成执行计划**：把每个重要叶节点映射为“章节列表”（章节名要可读、可检索）。
4. **初始化会话**：在项目根目录生成 `metadata.json`，并用本 skill 的生成器初始化会话：
   - 生成器路径：本 skill 目录的 `lib/doc-generator.js`（即 `SKILL.md` 所在目录下的 `lib/`）。
   - 命令：
     ```bash
     node <skill_dir>/lib/doc-generator.js init metadata.json
     ```
   - `metadata.json` 必须包含 `mindmap_markdown`；建议包含 `related_files`（入口文件、关键配置、DB schema 等）。

### Phase 2：Deep Dive Loop（逐章深挖，保持深度）
对“章节列表”逐个执行，直到覆盖关键叶节点：
1. **选定章节**：一次只做一个章节，避免上下文发散。
2. **定向取证**：只读这个章节相关的文件集（必要时扩展），并记录“入口/出口/调用链/数据结构”。
3. **产出章节 JSON**：写 `section.json`，字段：
   - `heading`: 章节标题（与 mindmap 节点一致）
   - `content`: HTML 字符串（包含转义后的代码片段与 Mermaid）
4. **追加**：
   ```bash
   node <skill_dir>/lib/doc-generator.js append <session_id> section.json
   ```
5. **更新进度**：每追加一个章节，回写当前完成度（已覆盖哪些节点、还缺哪些风险点）。

### Phase 3：Final Assembly（汇总 + 质量校验）
1. **渲染**：
   ```bash
   node <skill_dir>/lib/doc-generator.js render <session_id>
   ```
2. **质量校验**：确认 HTML 可打开、Mermaid 可渲染、代码与用户输入已转义、章节结构完整。
3. **交付摘要**：给出 1 页级别的“系统概览 + 风险清单 + 建议路线图（按优先级）”。

## 章节内容模板（建议）
章节 `content` 至少按以下结构组织（HTML）：
- `<h3>职责与边界</h3>`
- `<h3>关键组件与接口</h3>`（含文件/函数证据）
- `<h3>关键流程</h3>`（Mermaid）
- `<h3>权衡与替代方案</h3>`
- `<h3>风险与改进建议</h3>`（分级 + 具体行动项）
