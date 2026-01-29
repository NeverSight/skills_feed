---
name: github-repo-analyzer
description: 自动分析 GitHub 仓库，获取并整理 README、文档、Issues、GitHub Actions、Releases 等所有重要信息，由 LLM 进行深度分析并生成智能 HTML 报告。
---

# GitHub 仓库分析 Skill

## 概述

这个 Skill 帮助你快速深入了解任何 GitHub 仓库。它不是简单的数据搬运，而是通过 **LLM 智能分析**，将仓库的各类信息整合、归纳、总结，生成一份真正有价值的分析报告。

---

## 核心理念

> **让 LLM 成为分析引擎，而非数据搬运工。**

与直接浏览 GitHub 页面不同，本 Skill 会：
- 🧠 **智能归纳**：从 README、Issues、Releases 中提炼关键信息
- 🔗 **关联分析**：发现信息之间的联系，识别项目的核心特征
- 📊 **健康评估**：从多个维度评价项目的状态
- ✨ **洞察提炼**：总结项目亮点、风险和上手建议

---

## 使用方式

### 输入

用户提供 GitHub 仓库的完整 URL，例如：
```
https://github.com/facebook/react
```

---

## 执行步骤

> **重要**：此 Skill 使用 `uv` 自动管理依赖和虚拟环境，无需用户手动安装任何依赖。

### 步骤 1：环境检查

首次运行时，检查 `uv` 是否可用：
```bash
uv --version
```

如果 `uv` 未安装，先安装它：
```bash
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 步骤 2：获取仓库数据

进入 Skill 目录并运行数据获取脚本：

```bash
cd .claude/skills/github-repo-analyzer
uv run scripts/fetch_repo_info.py <仓库URL>
```

脚本会自动将数据保存到 `output/{owner}_{repo}/raw_data.json`。

### 步骤 3：生成 Markdown 格式数据

**重要**：由于 Read 工具有单行 2000 字符的限制，必须先将 JSON 转换为 Markdown 格式：

```bash
uv run scripts/prepare_for_analysis.py output/{owner}_{repo}/raw_data.json
uv run scripts/generate_analysis_md.py output/{owner}_{repo}/analysis_ready.json
```

输出：`output/{owner}_{repo}/analysis_ready_for_llm.md`（可以被完整读取）

### 步骤 4：LLM 智能分析（核心）

**Claude 必须执行以下深度分析任务：**

使用 Read 工具读取 `analysis_ready_for_llm.md` 文件（完整保留所有内容），从以下维度进行分析：

| 分析维度           | 分析要点                                                              |
| ------------------ | --------------------------------------------------------------------- |
| 🎯 **项目定位**     | 这是什么类型的项目（库/框架/工具/应用）？解决什么问题？目标用户是谁？ |
| 🔧 **技术栈解析**   | 使用了哪些核心技术？整体架构是怎样的？                                |
| 📖 **快速上手指南** | 从 README 提炼：如何安装？前置条件？最简使用示例？                    |
| 🌡️ **健康度评估**   | 活跃度（最近更新时间）、社区参与度（Issue 数量和活跃度）、维护状态    |
| 🔥 **热点问题分析** | 从 Issues 中提炼：社区最关注的问题是什么？有哪些常见困惑？            |
| 📈 **版本演进**     | 从 Releases 分析：最近版本的主要更新内容？项目发展趋势？              |
| 🚀 **核心亮点**     | 这个项目最值得关注的特性是什么？与同类项目相比的优势？                |
| ⚠️ **潜在风险**     | 是否有已知的安全问题？重大 Bug？维护问题？                            |
| 📝 **贡献指南**     | 如何为这个项目做贡献？有哪些规范要求？                                |
| 💡 **使用建议**     | 适合什么场景使用？有什么需要注意的地方？                              |

### 步骤 5：生成 HTML 报告

根据分析结果，生成一份美观的 HTML 报告，保存到 `output/{owner}_{repo}/report.html`。

**报告结构要求：**

1. **仓库概览卡片** - Stars/Forks/License/语言/更新时间
2. **一句话总结** - 用最简洁的语言概括项目
3. **项目定位与技术栈** - 类型识别、技术架构
4. **快速上手** - 安装步骤、使用示例
5. **健康度仪表盘** - 可视化展示项目状态
6. **社区热点** - Issues 分析结论
7. **版本演进** - Releases 时间线
8. **亮点与风险** - 优势和需注意的地方
9. **贡献指南摘要** - 如何参与项目

**设计要求：**
- 深色模式主题
- 响应式布局
- 代码语法高亮
- 可折叠的详细内容
- 现代化 UI（渐变色、圆角、阴影）

---

## GitHub Token 配置（可选但推荐）

为提高 API 速率限制（从 60 次/小时提升到 5000 次/小时），可以配置 Token：

1. 复制 `.env.example` 为 `.env`
2. 填入你的 GitHub Personal Access Token

或者通过命令行参数传递：
```bash
uv run scripts/fetch_repo_info.py <仓库URL> --token ghp_xxx
```

---

## 输出文件

所有输出文件集中在 `output/` 目录，按仓库分目录：

```
output/
└── {owner}_{repo}/
    ├── raw_data.json                # 原始 API 数据（462KB）
    ├── analysis_ready.json          # 预处理后 JSON 数据（122KB）
    ├── analysis_ready_for_llm.md    # Markdown 格式数据（供 LLM 分析）
    └── report.html                  # 最终分析报告
```

**重要说明**：
- `analysis_ready.json` 中的长文本（README、Issue body 等）都在单行中，会被 Read 工具截断
- `analysis_ready_for_llm.md` 解决了这个问题，所有内容都可以被完整读取

---

## 注意事项

- 如果未设置 `GITHUB_TOKEN` 环境变量，API 速率限制为 60 次/小时
- 使用 Token 后速率限制提升至 5,000 次/小时
- 私有仓库需要对应的访问权限
- 此 Skill 使用 `uv` 自动管理虚拟环境，不会污染全局 Python 环境
- 输出文件统一保存在 `output/` 目录，便于管理


