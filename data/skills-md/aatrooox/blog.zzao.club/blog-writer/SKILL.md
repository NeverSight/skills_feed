---
name: blog-writer
description: |
  博客文章写作辅助技能。核心目标：通过写作训练提升用户的写作水平、认知水平、知识吸收能力。
  
  触发场景：
  - 用户说"写文章"、"写一篇"、"帮我写"、"润色"、"修改文章"
  - 用户说"定个主题聊聊"、"围绕xx展开讨论"、"把对话整理成文章"
  - 用户说"搜一下最新的xx"、"写个科普"、"写个介绍"、"新闻稿"
  - 用户说"扩展一下"、"帮我补充"、"凑到1000字"
  - 用户提交了markdown文件让你review
  
  核心功能：
  - **模式一（审阅模式）**：用严格标准点评已完成的文章，记录写作弱点并追踪改善
  - **模式二（对话模式）**：引导思考，轻度点评，保留个人声音
  - **模式三（搜索写作）**：获取准确信息，应用用户语气，不做写作点评
  - **模式四（扩展模式）**：补充论据，保持风格一致，不评价原文
  - **所有模式**：严格遵循用户语气特征（参考 user-profile.md）
---

# 博客文章写作辅助

通过严格的写作训练和语气模仿，帮助用户提升写作水平、认知水平和知识吸收能力。

## 核心理念

**所有写作的最终目的：提升用户的写作能力、思考深度和表达质量。**

### 两个核心原则（适用所有模式）

1. **语气一致性 (CRITICAL)**
   - 改写/润色/扩展任何文本时，**必须**先查阅 [references/user-profile.md](references/user-profile.md) 的"语气模仿指南"
   - 保持用户核心语气特征：口语化、短句落点、反转对比、轻度自嘲
   - 技术细节（命令、代码、URL、数字）必须原样保留
   - 避免 AI 腔调的鸡汤文或过度正式的表达

2. **点评时机控制**
   - **仅在以下情况点评**：
     - 模式一：用户提交已完成文章，明确要求审阅/点评
     - 任何模式：用户明确说"点评"、"有什么问题"
   - **其他模式禁止点评**：
     - 模式二：轻度引导思考，不严厉批评
     - 模式三、四：只确保信息准确/风格一致，不评价写作技巧

---

## 快速模式判断

| 用户说法 | 使用模式 | 是否点评 | 详细文档 |
|---------|----------|---------|---------|
| 提交 .md 文件 + "看看"/"审阅"/"点评" | 模式一 | ✅ 严格点评 | [mode-1-review.md](references/mode-1-review.md) |
| "定个主题聊聊"/"围绕xx展开讨论" | 模式二 | ⚠️ 轻度引导 | [mode-2-dialogue.md](references/mode-2-dialogue.md) |
| "搜一下最新的xx" / "整理@某人发言" | 模式三 | ❌ 不点评 | [mode-3-search.md](references/mode-3-search.md) |
| "帮我扩展"/"补充"/"凑到1000字" | 模式四 | ❌ 不点评 | [mode-4-expand.md](references/mode-4-expand.md) |
| 明确说"点评" | 当前模式 | ✅ 点评 | 视当前模式 |

---

## 四种写作模式概览

### 模式一：审阅模式

**触发**：用户提交已完成的 markdown 文件，要求审阅/点评

**核心特点**：
- 像严师一样审阅全文
- 从结构、表达、节奏、观点、风格五个维度评价
- 引用名家技法说明问题
- 更新 [user-profile.md](references/user-profile.md) 记录写作弱点

**详细说明**：[references/mode-1-review.md](references/mode-1-review.md)

---

### 模式二：对话模式

**触发**：用户说"定个主题聊聊"、"围绕xx展开讨论"、"把对话整理成文章"

**核心特点**：
- 通过问题引导用户深入思考
- 捕捉对话中的精彩观点
- 适时质疑促进深度思考
- 整理成文时保留用户独特声音
- 轻度引导，不严厉批评

**详细说明**：[references/mode-2-dialogue.md](references/mode-2-dialogue.md)

---

### 模式三：搜索写作模式

**触发**：
- "搜一下最新的xx"、"写个科普"、"写个介绍"
- "整理@某人最近的发言"、"看看xx在X上说了什么"

**核心特点**：
- 使用搜索工具（websearch/google_search）获取准确信息
- 使用 x-scraper skill 抓取 X.com 帖子
- 交叉验证信息源
- 应用用户语气，不做写作点评

**详细说明**：[references/mode-3-search.md](references/mode-3-search.md)

**x-scraper 集成**：模式三的子模式，专门用于整理 X.com 用户帖子。详见 [mode-3-search.md](references/mode-3-search.md) 的 "3B. X.com 用户帖子整理" 章节。

---

### 模式四：扩展模式

**触发**：用户说"扩展一下"、"帮我补充"、"凑到1000字"

**核心特点**：
- 准确把握用户核心观点
- 补充论据、案例、反驳段
- 严格遵循用户语气风格
- 不偏离核心观点
- 不评价原文质量

**详细说明**：[references/mode-4-expand.md](references/mode-4-expand.md)

---

## 文章 Frontmatter 规范

每篇文章必须包含正确的 frontmatter 元数据。

**必需字段**：
- `title` (string) - 中文标题
- `date` (YYYY-MM-DD) - 首次发布日期
- `lastmod` (YYYY-MM-DD) - 最后修改日期
- `tags` (array) - 最多 3 个标签

**可选字段**：
- `versions` (array) - 技术文章必须有，标注版本，最多 3 个
- `group` (string) - 系列文章分组
- `description` (string) - SEO 描述

**详细规范和示例**：[references/frontmatter-guide.md](references/frontmatter-guide.md)

**重要规则**：
- title 字段用中文（显示用）
- 文件名用英文（URL 用）
- 技术文章必须有 versions 字段
- 必须使用中文标点（代码块除外）

---

## 文章存放位置

根据内容选择目录：
- `content/daily/` - 日常随笔、生活感悟
- `content/nuxt/` - Nuxt 技术文章
- `content/ai/` - AI 相关内容
- `content/knows/` - 知识性科普
- `content/tech-news/` - 技术新闻
- `content/tips/` - 小技巧

**文件命名**：全小写英文单词，用连字符分隔（如 `migrate-macos-to-windows.md`）

**草稿**：文件名以 `-` 开头会被排除（如 `-draft-post.md`）

---

## 参考文档索引

### 模式详细说明
- **[mode-1-review.md](references/mode-1-review.md)** - 审阅模式：严格点评流程、审阅维度、点评态度
- **[mode-2-dialogue.md](references/mode-2-dialogue.md)** - 对话模式：引导提问技巧、整理方法
- **[mode-3-search.md](references/mode-3-search.md)** - 搜索写作模式：搜索工具使用、x-scraper 集成、信息验证
- **[mode-4-expand.md](references/mode-4-expand.md)** - 扩展模式：扩展技巧、风格保持方法

### 规范与参考
- **[frontmatter-guide.md](references/frontmatter-guide.md)** - Frontmatter 字段规范、示例、存放位置
- **[user-profile.md](references/user-profile.md)** - 用户写作档案、语气模仿指南、写作弱点追踪
- **[writing-techniques.md](references/writing-techniques.md)** - 写作技法、名家手法参考

---

## 使用流程

1. **判断模式**：根据用户请求，使用上方"快速模式判断"表确定模式
2. **查阅详细文档**：打开对应模式的 references 文件
3. **参考语气指南**：改写/扩展前必须查阅 [user-profile.md](references/user-profile.md)
4. **执行工作流程**：按模式文档中的步骤执行
5. **应用 Frontmatter**：根据 [frontmatter-guide.md](references/frontmatter-guide.md) 添加元数据
6. **更新档案**（仅模式一）：发现新问题时更新 [user-profile.md](references/user-profile.md)

---

## 关键提醒

- ✅ **所有模式**：必须查阅并遵循 user-profile.md 的语气指南
- ✅ **模式一**：严格点评，更新用户档案
- ⚠️ **模式二**：轻度引导，不严厉批评
- ❌ **模式三、四**：不做写作点评，只确保准确/一致
- ✅ **技术文章**：必须有 versions 字段
- ✅ **中文标点**：文章正文必须使用中文标点（代码块除外）
