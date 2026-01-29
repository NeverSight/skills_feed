---
name: skills-guide
description: Comprehensive guide for discovering, understanding, and installing Claude Code skills from skills.sh marketplace. Use this skill when users want to (1) browse or search skills.sh for recommendations, (2) get skill recommendations by role (developer, marketer, designer, product manager), (3) understand how a specific installed skill works by reading and explaining its SKILL.md, (4) learn the anatomy and structure of skills, or (5) find and install skills that match their specific workflow needs. This is NOT for creating new skills (use skill-creator instead).
---

# Skills 完整指南

帮助用户理解、查找和创建 Claude Code Skills。

## 快速问答

**什么是 Skills？**
Skills 是扩展 Claude 能力的模块化包。可以理解为"专家知识包"——给 Claude 注入特定领域的工作流、专业知识和工具。

**在哪找 Skills？**
[skills.sh](https://skills.sh) - 开放的 Skills 目录，按安装量排行。

**怎么安装？**
```bash
npx skills add <owner/repo> --yes
```

**Skills 装在哪？**
`~/.agents/skills/` - 每个 skill 一个文件夹，里面有 SKILL.md 文件。

## 帮用户找 Skill

当用户描述需求时，按这个流程执行：

1. **明确需求** - 具体要做什么任务？什么领域？
2. **搜索 skills.sh** - 用 WebFetch 访问 https://skills.sh 查找相关 skills
3. **评估选项** - 看安装量（越高越靠谱）、读描述
4. **推荐并解释** - 说明这个 skill 做什么、为什么适合
5. **安装** - 如果用户同意，执行 `npx skills add <owner/repo> --yes`

### 热门推荐速查

**开发者：**
- `vercel-labs/agent-skills` → React/Next.js 最佳实践（37k+ 安装）
- `anthropics/skills` → 官方文档处理（PDF、Word、PPT、Excel）
- `expo/skills` → 移动应用开发

**产品/运营/市场：**
- `coreyhaines31/marketingskills` → 23个营销skills（文案、定价、SEO、广告）

**内容创作者（中文友好）：**
- `jimliu/baoyu-skills` → 幻灯片、配图、小红书图片（宝玉老师出品）

## 解读已安装的 Skill

当用户想了解某个 skill 时：

1. 读取 SKILL.md：`~/.agents/skills/<skill名>/SKILL.md`
2. 解释：触发条件、核心能力、包含的资源
3. 举例说明什么时候用、怎么用

## 创建 Skill

详细指南见 [references/creating-skills.md](references/creating-skills.md)

**快速概览：**
1. Skill 是一个文件夹，必须有 SKILL.md
2. SKILL.md 有 YAML 头（name、description）+ Markdown 正文
3. 可选：`scripts/`、`references/`、`assets/` 文件夹放资源
4. 发布：推到 GitHub，用户就能 `npx skills add <你的仓库>` 安装

**关键原则**：`description` 字段最重要——它决定 skill 什么时候被触发。要把使用场景写清楚。

## 深入了解

需要详细信息时，读取参考文件：

- **[references/skills-anatomy.md](references/skills-anatomy.md)** - Skills 技术结构详解
- **[references/creating-skills.md](references/creating-skills.md)** - 从零创建 skill 的完整指南
- **[references/top-skills.md](references/top-skills.md)** - 按角色和场景分类的热门推荐
