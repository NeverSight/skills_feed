---
name: skill-creator
description: 创建新的 Claude Code Skill。当用户说"帮我创建一个 skill"、"把这个变成 skill"、"新建技能"时触发。
---

# Skill Creator

帮助创建有效的 Claude Code Skill。

## 触发词

- "帮我创建一个 skill"
- "把这个变成 skill"
- "新建技能"
- "/create-skill"

---

## Skill 核心概念

Skill 是模块化的能力包，用于扩展 Claude 的能力：
- **专业工作流**：多步骤的领域流程
- **工具集成**：特定文件格式或 API 的使用方法
- **领域知识**：公司特定知识、schema、业务逻辑
- **打包资源**：脚本、参考文档、资产文件

---

## Skill 目录结构

```
skill-name/
├── SKILL.md          # 必须 - 核心指令
└── 可选资源/
    ├── scripts/      # 可执行脚本（Python/Bash）
    ├── references/   # 参考文档（按需加载）
    └── assets/       # 输出资源（模板、图标）
```

---

## SKILL.md 格式

```yaml
---
name: skill-name
description: 做什么 + 什么时候触发（这是最重要的字段）
---

# Skill 标题

[指令内容]

## 触发词
- "关键词1"
- "关键词2"

## 执行步骤
1. xxx
2. xxx

## 示例
[示例用法]
```

---

## 设计原则

### 1. 简洁为王
- 上下文窗口是共享的，假设 Claude 已经很聪明
- 只添加 Claude 不知道的信息
- 用简洁示例代替冗长解释

### 2. 设置合适的自由度

| 自由度 | 何时使用 | 形式 |
|--------|---------|------|
| **高** | 多种有效方法，依赖上下文判断 | 文字说明 |
| **中** | 有推荐模式，允许一些变化 | 伪代码/脚本 |
| **低** | 操作脆弱，一致性关键 | 精确脚本 |

### 3. 渐进加载（三层）

1. **元数据**（~100词）- 始终在上下文中
2. **SKILL.md 主体**（<5k词）- skill 触发时加载
3. **附加资源** - Claude 按需加载

---

## 创建流程

### Step 1: 理解需求
- 这个 skill 要做什么？
- 用户会怎么触发它？
- 需要什么输入/输出？

### Step 2: 规划资源
- 需要脚本吗？放 `scripts/`
- 需要参考文档吗？放 `references/`
- 需要模板/资产吗？放 `assets/`

### Step 3: 创建目录
```bash
mkdir -p .claude/skills/你的skill名
```

### Step 4: 编写 SKILL.md
- frontmatter: 清晰的 name + 全面的 description
- body: 使用 skill 和资源的指令

### Step 5: 测试迭代
1. 在真实任务中使用
2. 发现问题或低效
3. 更新 SKILL.md 或资源
4. 重复

---

## 不要包含的文件

- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- 其他与 skill 功能无关的文件

---

## 存放位置

| 位置 | 作用域 |
|------|--------|
| `~/.claude/skills/` | 个人全局 |
| `项目/.claude/skills/` | 项目级，可 git 共享 |

---

## 示例：创建一个简单 skill

**用户**：帮我把"渲染公众号文章"变成 skill

**执行**：
1. 创建目录 `.claude/skills/render-article/`
2. 编写 SKILL.md
3. 测试触发词是否有效

---

*参考：[官方 Skill 仓库](https://github.com/anthropics/skills)*
