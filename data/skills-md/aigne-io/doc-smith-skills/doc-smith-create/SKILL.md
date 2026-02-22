---
name: doc-smith-create
description: "Generate and update structured documentation from project data sources. Supports initial generation and modifying existing documents. Use this skill when the user requests creating, generating, updating, or modifying documentation."
---

# DocSmith 文档生成

从工作区数据源生成和更新结构化文档。所有输出创建在 `.aigne/doc-smith/` workspace 中。

## 约束

以下约束在任何操作中都必须满足。

### 1. Workspace 约束

- 所有操作前 workspace 必须存在且有效（config.yaml + sources）
- workspace 有独立 git 仓库，所有 git 操作在 `.aigne/doc-smith/` 下执行
- workspace 不存在时按以下流程初始化：
  1. `mkdir -p .aigne/doc-smith/{intent,planning,docs,assets,cache}`
  2. `cd .aigne/doc-smith && git init`
  3. 创建 config.yaml（schema 见下方）
  4. 初始 commit

**config.yaml schema**：

```yaml
workspaceVersion: "1.0"
createdAt: "2025-01-13T10:00:00Z"  # ISO 8601
projectName: "my-project"
projectDesc: "项目描述"
locale: "zh"                        # 输出语言代码，初始化时必须向用户确认
projectLogo: ""
translateLanguages: []
sources:
  - type: local-path
    path: "../../"                  # 相对于 workspace
    url: ""                         # 可选: git remote URL
    branch: ""                      # 可选: 当前分支
    commit: ""                      # 可选: 当前 commit
```

**locale 确认规则**：初始化 workspace 时，若用户未明确指定语言，必须用 AskUserQuestion 确认输出语言（如 zh、en、ja），不得默认写入。

### 2. 结构约束

- `document-structure.yaml` 必须符合下方 schema
- 结构变更后必须通过 `/doc-smith-check --structure`
- 结构变更后必须重建 nav.js：`node skills/doc-smith-build/scripts/build.mjs --nav --workspace .aigne/doc-smith --output .aigne/doc-smith/dist`

**document-structure.yaml schema**：

```yaml
project:
  title: "项目名称"
  description: "项目概述"
documents:
  - title: "文档标题"
    description: "简要摘要"
    path: "/filename"               # 必须以 / 开头
    sourcePaths: ["src/main.py"]    # 源文件路径（无 workspace: 前缀）
    icon: "lucide:book-open"        # 仅顶层文档必需
    children:                       # 可选：嵌套文档
      - title: "子文档"
        description: "详细信息"
        path: "/section/nested"
        sourcePaths: ["src/utils.py"]
```

### 3. 内容约束

- 每篇文档必须有 `docs/{path}/.meta.yaml`（kind: doc, source, default）
- HTML 必须生成在 `dist/{lang}/docs/{path}.html`
- `docs/` 目录中不得残留 `.md` 文件（构建后删除）
- 所有内部链接使用文档 path 格式（如 `/overview/doc-gen`），build.mjs 自动转换为相对 HTML 路径
- 资源引用使用 `/assets/xxx` 绝对路径格式（build.mjs 自动转换为相对路径）

### 4. 人类确认约束

- 用户意图推断后必须经用户确认（使用 AskUserQuestion）
- 文档结构规划后必须经用户确认（使用 AskUserQuestion）
- 确认后若有变更需再次确认

### 5. 上下文管理约束

Task 使用后台执行模式（`run_in_background: true`），执行日志不会回流到主 agent 上下文。主 agent 通过信号文件（`.status`）获取结果。

**实践规则**：
- 主 agent 可自由读取项目源文件，不再受 Task 返回值的上下文预算限制
- 首次生成时，先通过目录结构（`ls`/`Glob`）评估项目规模，再决定结构规划方式：
  - 小项目（源文件少、预计文档 ≤ 5 篇）：主 agent 可直接读取源文件并规划结构
  - 大项目（源文件多、预计文档 > 5 篇）：将结构规划委派给 Task（见"关键流程"）

### 6. Task 分发约束

Task 类型：
- **结构规划** Task（按需）：当项目较大时，委派 Task 分析源文件生成 `document-structure.yaml` 草稿
- **内容生成** Task：按"并行生成文档内容"中的 prompt 模板分发，每篇文档一个 Task

分发规则：
- **所有内容生成 Task 必须使用 `run_in_background: true`**，避免执行日志回流到主 agent 上下文
- 文档数量 ≤ 5 时并行执行，> 5 时分批（每批 ≤ 5 个），前一批完成后再启动下一批
- 内容生成前先执行媒体资源扫描：`Glob: **/*.{png,jpg,jpeg,gif,svg,mp4,webp}`（排除 .aigne/ 和 node_modules/），将结果作为 mediaFiles 传递给每个 Task

信号文件机制：
- 每个 Task 完成时在 `.aigne/doc-smith/cache/task-status/` 写入 `{slug}.status` 文件
- slug 规则：docPath 去除 `/` 前缀后以 `-` 替换 `/`（如 `/api/overview` → `api-overview`）
- 状态文件内容为 1 行摘要（如 `/overview: 成功 | HTML ✓ | .meta.yaml ✓`）
- 主 agent 通过轮询 `.status` 文件判断 Task 是否完成（见"批次执行流程"）

### 7. 完成约束

- `/doc-smith-check --structure` 通过
- `/doc-smith-check --content` 通过
- `dist/` 目录包含所有文档的 HTML
- `nav.js` 包含所有文档条目
- 自动 git commit（在 `.aigne/doc-smith/` 目录下）

## 统一入口

| 场景 | 判断条件 | 行为 |
|------|---------|------|
| 首次生成 | `docs/` 不存在或用户明确要求 | 完整流程：意图 → 结构 → 生成 |
| 修改已有文档 | `docs/` 已存在 | AI 理解修改请求，直接修改，满足约束即可 |

修改场景不需要 changeset/PATCH 机制。用户用自然语言描述修改需求，AI 执行并满足约束。

## 用户意图

文件：`.aigne/doc-smith/intent/user-intent.md`

基于项目 README 和目录结构（`ls`/`Glob`）推断目标用户、使用场景、文档侧重点。生成后用 AskUserQuestion 确认。

```markdown
# 用户意图

## 目标用户
[主要受众是谁]

## 使用场景
- [场景 1]
- [场景 2]

## 文档侧重点
本文档采用**[文档类型]**的形式：
- [侧重点 1]
- [侧重点 2]
```

## 结构规划原则

- 规划必须依据用户意图，只规划明确需要的文档
- 扁平优于嵌套，有疑虑时选择更简单的结构
- 拆分条件：4+ 章节、内容独立、无重复、可独立查阅
- 不拆分：内容单薄、顺序步骤、存在重复
- 结构规划后用 AskUserQuestion 确认，展示文档总数、层次、每个文档的标题和描述

## 内容组织原则

- 导航链接只能链接已生成的文档（使用 path 格式），不链接工作目录文件
- 文档开头：前置条件、父主题
- 文档结尾：相关主题、下一步、子文档
- 有子文档的概览文档：简写（150-300 行），每个子主题 2-4 段 + 引导链接
- 无子文档的详细文档：详写（300-500 行），完整展开

## 关键流程

### 结构规划

主 agent 生成 `user-intent.md` 并经用户确认后，根据项目规模选择结构规划方式：

- **小项目**：主 agent 直接读取源文件，分析后生成 `document-structure.yaml`
- **大项目**：委派 Task 分析源文件并生成 `document-structure.yaml` 草稿，Task 返回文件路径 + 结构摘要（≤ 10 行）

生成后用 AskUserQuestion 向用户确认，展示文档总数、层次、每个文档的标题和描述。

### 生成 nav.js（结构确认后、内容生成前）

```bash
node skills/doc-smith-build/scripts/build.mjs \
  --nav --workspace .aigne/doc-smith --output .aigne/doc-smith/dist
```

### 并行生成文档内容

每篇文档使用单独的 Task tool 生成（≤ 5 篇并行，> 5 篇分批）。**必须使用 `run_in_background: true` 分发 Task**。必须使用以下模板构造 Task prompt，不得自行概括 content.md 内容：

```
你是文档内容生成代理。请先用 Read 工具读取 {CONTENT_MD_PATH} 作为你的完整工作流程，然后严格按照其中的步骤执行。

参数：
- 文档路径：{docPath}
- workspace：{WORKSPACE_PATH}
- 可链接文档列表：{LINKABLE_DOCS}
- mediaFiles：{MEDIA_FILES}
- 用户意图摘要：{INTENT_SUMMARY}
- 状态文件路径：{STATUS_FILE_PATH}

关键工具说明：
- 使用 Skill 工具调用 /doc-smith-images 生成图片（步骤 5.5）
- 使用 Skill 工具调用 /doc-smith-check 校验文档（步骤 7）

完成检查清单（必须在写入状态文件前逐项确认）：
□ 步骤 5 图片使用：文档中已按需添加图片引用
□ 步骤 5.5 图片生成：已扫描并处理所有 /assets/{key}/images/ 引用
□ 步骤 6.5 HTML 构建：已执行 build.mjs --doc 并确认 HTML 生成
□ 步骤 7 校验：已调用 /doc-smith-check --content --path {docPath}
□ 状态文件：已将 1 行摘要写入 {STATUS_FILE_PATH}
```

**模板变量说明**：
- `{CONTENT_MD_PATH}`：`references/content.md` 的绝对路径
- `{WORKSPACE_PATH}`：`.aigne/doc-smith` 的绝对路径
- `{docPath}`：文档路径，如 `/overview`
- `{LINKABLE_DOCS}`：所有文档路径列表（从 document-structure.yaml 提取）
- `{MEDIA_FILES}`：媒体资源扫描结果
- `{INTENT_SUMMARY}`：user-intent.md 的 2-3 句话摘要
- `{STATUS_FILE_PATH}`：`.aigne/doc-smith/cache/task-status/{slug}.status`

### 批次执行流程

#### 准备阶段

分发第一个 Task 前：
1. `mkdir -p .aigne/doc-smith/cache/task-status`
2. `rm -f .aigne/doc-smith/cache/task-status/*.status`（清空旧状态）

#### 分发阶段

每个 Task 使用 `run_in_background: true` 分发。批次内所有 Task 同时启动。

#### 等待阶段

每 15 秒检查 `.status` 文件数量：

```bash
ls .aigne/doc-smith/cache/task-status/*.status 2>/dev/null | wc -l
```

- 文件数 = 当前批次文档数 → 该批次完成
- 超时：单批最多等待 10 分钟，超时后报告缺失文档
- **不要读取后台 Task 的 output_file**（可能 300K+），只读 `.status` 文件

#### 收集结果

```bash
cat .aigne/doc-smith/cache/task-status/*.status
```

每个文件 1 行，所有文档摘要汇总后通常不超过 20 行。

#### 失败处理

- `.status` 内容以"失败"开头 → 记录失败原因，不阻塞后续批次
- 超时未产生 `.status` → 标记为超时，在最终报告中提示用户重试

### AI 巡检

构建完成后，读取 `dist/` 中生成的 HTML 文件（每种语言各抽查 1-2 个页面），检查输出是否符合预期。如有问题直接修改 HTML 文件修复。

### 自动提交

```bash
cd .aigne/doc-smith && git add . && git commit -m "docsmith: xxx"
```

### 完成提示

所有文档生成并校验通过后，向用户展示生成摘要，并提示：

> 文档已生成完毕，可使用 `/doc-smith-publish` 将文档发布到线上预览。

## Workspace 目录结构

```
.aigne/doc-smith/
├── config.yaml
├── intent/user-intent.md
├── planning/document-structure.yaml
├── docs/{path}/.meta.yaml
├── dist/
│   ├── index.html
│   ├── {lang}/docs/{path}.html
│   └── assets/nav.js, docsmith.css, theme.css
├── assets/{key}/.meta.yaml, images/{lang}.png
├── glossary.yaml                  # 可选
└── cache/
    ├── translation-cache.yaml     # 发布用
    └── task-status/{slug}.status  # Task 完成信号文件
```
