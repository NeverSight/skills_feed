---
name: x-ai-topic-selector
description: Fetches tweets from Twitter List, scores them using data metrics and AI analysis, and generates topic recommendation reports for content creators.
commands:
  - name: /select-topics
    description: Generate topic report from Twitter List, Home, or Bookmarks (interactive guided flow)
---

## ⚠️ 默认行为 (Default Behavior)

**重要**: 当用户直接调用 `/x-ai-topic-selector` 而不指定子命令时，Agent **必须自动启动** `/select-topics` 的完整交互流程。

### 交互模式要求

- ✅ **必须使用**: `question()` 工具 + `options` 数组（生成**可点击的选项按钮**）
- ❌ **禁止使用**: 文本提示 + 等待用户输入（如"请输入..."、"直接回复选项编号"等）

**所有参数收集必须通过 `question()` 工具的选项选择完成**，用户只需点击选项，无需手动输入文本（除非是自由格式输入，如 API Key、URL 等特殊情况）。

---

# X AI Topic Selector

自动从 X (Twitter) 抓取推文，通过多维评分（数据指标 + AI 分析）生成选题推荐报告。

![alt text](architecture.svg)

## 命令

### `/select-topics`

运行选题工具。

**使用方式**: 直接调用 `/select-topics`，Agent 将通过交互式引导收集参数。
**功能说明**:
- **扫描模式 (Lists/Home)**: 支持按分类筛选、多维评分、精选推荐。
- **书签模式 (Bookmarks)**: 自动提取全部书签内容，进入 AI 深度分析模式（无过滤，保留全部）。

---

## 配置持久化

配置文件路径: `~/.x-topic-selector/config.json`

Agent 在执行前**必须检查**此文件是否存在：
1. 如果存在，读取并解析 JSON
2. 在 Step 1 后询问用户是否使用已保存配置
3. 执行完成后保存当前配置到此文件

**配置文件结构**:
```json
{
  "sourceType": "list|home|bookmarks",
  "listUrls": ["https://x.com/i/lists/xxx"],
  "scoreMode": "data-only|ai-only",
  "aiProvider": "auto|gemini|openai",
  "geminiApiKey": "",
  "topicCategory": "all",
  "maxTweets": 200,
  "topN": 10,
  "lastUsed": "2025-02-01T12:00:00Z"
}
```

---

## 参数回填规则

为了提升交互体验，当 `config.json` 存在时，Agent 应遵循以下回填规则：

1. **单选类**: 在对应的选项 `label` 后添加 `(上次选择)` 标记。
2. **自定义数值**: 如果上次使用的是自定义数值（不在预设选项中），应动态添加一个新选项。
3. **API Key**: 如果已保存且用户选择 AI 模式，自动复用，无需再次输入。
4. **列表 URL**: 在 `question` 文本中包含 `📌 上次使用: <value>`，并在 `options` 中将该值作为第一个选项提供。

---

## 交互流程

当用户触发 `/select-topics` 命令后，Agent **必须按以下步骤**使用 `question()` 工具引导用户：

### Step 0: 检查已保存配置

**必须执行**: Agent 先检查 `~/.x-topic-selector/config.json` 是否存在

```bash
cat ~/.x-topic-selector/config.json 2>/dev/null || echo "NO_CONFIG"
```

如果配置存在，进入 Step 0b；否则跳到 Step 1。

### Step 0b: 询问是否使用已保存配置

如果检测到已保存配置，使用 `question()` 询问：

```
question({
  questions: [{
    header: "使用已保存配置",
    question: "检测到上次使用的配置：\n\n• 内容来源: ${config.sourceType || 'list'}\n• 列表 URL: ${config.listUrls.join(', ')}\n• 评分模式: ${config.sourceType === 'bookmarks' ? 'AI 全量分析 (书签模式自动应用)' : (config.scoreMode === 'ai-only' ? 'AI 分析' : '数据分析')}\n• 扫描数量: ${config.maxTweets}\n• 推荐数量: ${config.sourceType === 'bookmarks' ? '全量提取' : config.topN}\n\n请选择操作：",
    options: [
      { label: "使用上次配置直接运行 (Recommended)", description: "使用所有已保存的参数立即开始" },
      { label: "重新配置全部", description: "从头开始配置所有参数" }
    ]
  }]
})
```

**处理逻辑**:
- "使用上次配置直接运行" → 跳到 Step 3 执行
- "重新配置全部" → 从 Step 1 开始完整流程

### Step 1: 欢迎 + 登录提示

首先显示欢迎信息和重要提示：

```
📊 X AI 选题助手
由公众号「懂点儿AI」开发维护，如有问题或建议欢迎关注公众号反馈。

在开始之前，请确保：
✅ 已安装 Google Chrome 浏览器
✅ 已在 Chrome 中登录您的 X (Twitter) 账号

首次运行时，脚本会打开 Chrome 窗口，请在窗口中完成登录（登录状态会被保存）。
```

### Step 2: 一次性收集所有参数

**核心设计**: 将所有参数放在单次 `question()` 调用中。

使用 `question()` 工具一次性询问所有参数：

```
question({
  questions: [
    // Q1: 内容来源
    {
      header: "内容来源",
      question: "请选择要扫描的内容来源",
      options: [
        { label: `X 列表 (List)${config?.sourceType === 'list' ? ' (上次选择)' : ''}`, description: "扫描指定的 Twitter 列表，选择后需要输入列表 URL" },
        { label: `推荐 (For You)${config?.sourceType === 'home' ? ' (上次选择)' : ''}`, description: "扫描 X 推荐的内容" },
        { label: `书签 (Bookmarks)${config?.sourceType === 'bookmarks' ? ' (上次选择)' : ''}`, description: "扫描你收藏的推文（自动进入 AI 深度分析模式，全量提取）" }
      ]
    },
    // Q2: 评分模式 (仅非书签模式)
    {
      header: "评分模式",
      question: "请选择选题评分模式 (书签模式下自动使用 AI 分析)",
      options: [
        { label: `数据分析模式 (Recommended)${config?.scoreMode === 'data-only' ? ' (上次选择)' : ''}`, description: "基于互动数据评分，无需 API Key" },
        { label: `AI 分析模式${config?.scoreMode === 'ai-only' ? ' (上次选择)' : ''}`, description: "基于 AI 内容分析，需要 Gemini API Key" }
      ]
    },
    // Q2b: AI 服务商 (仅 AI 分析模式或书签模式)
    {
      header: "AI 服务商",
      question: "请选择 AI 分析使用的服务商（书签模式同样适用）",
      options: [
        { label: `自动检测 (Recommended)${config?.aiProvider === 'auto' || !config?.aiProvider ? ' (上次选择)' : ''}`, description: "按优先级自动选择：Gemini → OpenAI 兼容接口" },
        { label: `Gemini${config?.aiProvider === 'gemini' ? ' (上次选择)' : ''}`, description: "使用 Google Gemini API（需要 GEMINI_API_KEY）" },
        { label: `OpenAI 兼容${config?.aiProvider === 'openai' ? ' (上次选择)' : ''}`, description: "使用 OpenAI 兼容接口（需要 OPENAI_API_KEY + OPENAI_MODEL）如 DeepSeek" }
      ]
    },
    // Q3: 选题范围 (仅非书签模式)
    {
      header: "选题范围",
      question: "请选择要关注的选题范围 (书签模式下将分析全部内容)",
      options: [
        { label: `不限 (Recommended)${config?.topicCategory === 'all' ? ' (上次选择)' : ''}`, description: "显示所有类型的选题" },
        { label: `AI 工具/产品发布${config?.topicCategory === 'ai-tools' ? ' (上次选择)' : ''}`, description: "新工具、新功能、产品更新" },
        { label: `行业新闻/动态${config?.topicCategory === 'industry-news' ? ' (上次选择)' : ''}`, description: "公司动态、融资、并购等" },
        { label: `技术突破/论文${config?.topicCategory === 'tech-breakthroughs' ? ' (上次选择)' : ''}`, description: "新研究、技术创新" },
        { label: `教程/实用技巧${config?.topicCategory === 'tutorials' ? ' (上次选择)' : ''}`, description: "使用指南、最佳实践" },
        { label: `争议/讨论话题${config?.topicCategory === 'controversial' ? ' (上次选择)' : ''}`, description: "行业争论、热点讨论" }
      ]
    },
    // Q4: 扫描数量
    {
      header: "扫描数量",
      question: "请选择要扫描的推文数量",
      options: [
        { label: `100 条${config?.maxTweets === 100 ? ' (上次选择)' : ''}`, description: "快速扫描" },
        { label: `200 条 (Recommended)${config?.maxTweets === 200 ? ' (上次选择)' : ''}`, description: "标准扫描" },
        { label: `500 条${config?.maxTweets === 500 ? ' (上次选择)' : ''}`, description: "深度扫描" }
      ]
    },
    // Q5: 推荐条数 (仅非书签模式)
    {
      header: "推荐条数",
      question: "请选择要推荐的选题数量 (书签模式下将提取全部)",
      options: [
        { label: `5 条${config?.topN === 5 ? ' (上次选择)' : ''}`, description: "精选推荐" },
        { label: `10 条 (Recommended)${config?.topN === 10 ? ' (上次选择)' : ''}`, description: "标准推荐" },
        { label: `20 条${config?.topN === 20 ? ' (上次选择)' : ''}`, description: "扩展推荐" }
      ]
    }
  ]
})
```

**路由逻辑**:
- **如果用户选择 "书签 (Bookmarks)"**: 仅收集 "扫描数量"。自动设置 `scoreMode = ai-only`，忽略选题范围和推荐条数（全量提取）。
- **如果用户选择 "X 列表" 或 "推荐"**: 执行完整参数收集流程。

**AI 服务商路由逻辑**:
- **如果用户选择 "自动检测"**: 不传 `--ai-provider` 参数，脚本自动按优先级检测可用的 API Key。
- **如果用户选择 "Gemini"**: 传 `--ai-provider gemini`。
- **如果用户选择 "OpenAI 兼容"**: 传 `--ai-provider openai`。
- **如果用户选择 "数据分析模式" 且非书签来源**: AI 服务商选择可忽略（不使用 AI）。

#### A. 已移除书签模式独立流程 (已合并到 Step 2)

Step 2 现在一次性收集所有参数。如果 Source = Bookmarks，脚本会自动忽略评分模式和推荐条数等参数。

#### B. 扫描过滤模式流程 (已合并到 Step 2)

### Step 2b: 条件性补充收集

根据 Step 2 的选择结果，可能需要补充收集以下信息：

#### 如果选择了 "X 列表 (List)"

需要继续询问列表 URL：

```
question({
  questions: [{
    header: "X 列表 URL",
    question: "请输入要扫描的 X 列表 URL 地址（支持多个，用逗号分隔）\n\n示例格式：https://x.com/i/lists/1234567890\n\n💡 推荐尝试使用「AI 精选」列表，可获取高质量 AI 领域内容。${config?.listUrls?.[0] ? `\n\n📌 上次使用: ${config.listUrls.join(', ')}` : ''}",
    options: [
      ...(config?.listUrls?.[0] ? [{ label: config.listUrls.join(', '), description: "复用上次输入的 URL" }] : []),
      { label: "https://x.com/i/lists/2021198996157710621", description: "「AI 精选」推荐列表 — 优质 AI 内容源" }
    ]
  }]
})
```

#### 如果进入了 "书签模式" 或选择了 "AI 分析模式"

**根据用户选择的 AI 服务商**，检查对应的 API Key 和环境变量：

##### 如果用户选择 "Gemini" 或 "自动检测"

**必须检查** Gemini API Key：

```
question({
  questions: [{
    header: "Gemini API Key",
    question: "书签模式和 AI 模式需要 Gemini API Key\n\n获取方式：访问 https://aistudio.google.com/apikey 创建 API Key${config?.geminiApiKey ? '\n\n📌 检测到已保存的 API Key，可直接复用' : ''}",
    options: config?.geminiApiKey ? [{ label: "使用已保存的 API Key", description: "复用上次保存的 Gemini API Key" }] : []
  }]
})
```

**注意**: 如果 `config.geminiApiKey` 已存在，跳过此步骤，直接使用已保存的 Key。

##### 如果用户选择 "OpenAI 兼容"

**必须检查** OpenAI 相关环境变量：
- `OPENAI_API_KEY`（必需）— OpenAI 兼容接口的 API Key
- `OPENAI_API_BASE`（可选）— 自定义 API 端点（如 DeepSeek: `https://api.deepseek.com/v1`）
- `OPENAI_MODEL`（必需）— 模型名称（如 `deepseek-chat`、`gpt-4o`）

```
question({
  questions: [{
    header: "OpenAI API Key",
    question: "OpenAI 兼容模式需要设置环境变量：\n\n• OPENAI_API_KEY（必需）\n• OPENAI_MODEL（必需，如 deepseek-chat）\n• OPENAI_API_BASE（可选，自定义端点）\n\n请确认环境变量已设置，或在此输入 OPENAI_API_KEY",
    options: [
      { label: "环境变量已设置", description: "已通过 export 设置 OPENAI_API_KEY 和 OPENAI_MODEL" }
    ]
  }]
})
```

**注意**: 模型选择（`OPENAI_MODEL`）仅通过环境变量配置，不在交互流程中询问。

##### 如果用户选择 "自动检测"

Agent 按以下优先级检查可用的 API Key：
1. 检查 `GEMINI_API_KEY` 环境变量或 `config.geminiApiKey`
2. 检查 `OPENAI_API_KEY` 环境变量
3. 如果都不可用，提示用户配置至少一个

### Step 3: 执行脚本

收集完所有参数后，Agent 构建并执行命令：

```bash
# 确保输出目录存在
mkdir -p ./output

# 设置环境变量（根据 AI 服务商选择）
export GEMINI_API_KEY="用户提供的key"          # Gemini 或自动检测模式
# export OPENAI_API_KEY="用户提供的key"        # OpenAI 兼容模式
# export OPENAI_MODEL="deepseek-chat"          # OpenAI 兼容模式（必需）
# export OPENAI_API_BASE="https://api.deepseek.com/v1"  # OpenAI 兼容模式（可选）

# 执行脚本 (Source = List/Home)
bun run ${SKILL_DIR}/scripts/x-topic-selector.ts \
  "URL" \
  --score-mode <mode> \
  --ai-provider <provider> \
  --max-tweets <count> \
  --topic-category <category> \
  --top-n <n> \
  --output ./output/topic-report-{timestamp}.md

# 执行脚本 (Source = Bookmarks)
bun run ${SKILL_DIR}/scripts/x-topic-selector.ts \
  "https://x.com/i/bookmarks" \
  --digest \
  --ai-provider <provider> \
  --max-tweets <count> \
  --output ./output/topic-report-{timestamp}.md
```

### Step 3b: 保存配置

执行成功后，**必须保存配置**以便下次复用：

```bash
cat > ~/.x-topic-selector/config.json << 'EOF'
{
  "sourceType": "list|home|bookmarks",
  "listUrls": ["URL"],
  "scoreMode": "data-only|ai-only",
  "geminiApiKey": "KEY",
  "topicCategory": "all",
  "maxTweets": count,
  "topN": n,
  "lastUsed": "ISO_TIMESTAMP"
}
EOF
```

### Step 4: 结果展示

执行完成后，向用户展示结果。对于**书签模式**，展示内容包含：
- 📁 日报文件路径
- 📝 今日看点预览
- 🏆 必读 Top 3 标题
- 💡 选题思路数量

---

## 脚本目录
... (内容同前)

## 参数映射
... (内容同前)

## 环境要求
... (内容同前)

## Thread 自动展开
... (内容同前)

## 故障排除
... (内容同前)

---

## 脚本目录

**重要**: 所有脚本位于此 skill 的 `scripts/` 子目录。

**Agent 执行说明**:
1. 确定此 SKILL.md 文件的目录路径为 `SKILL_DIR`
2. 脚本路径 = `${SKILL_DIR}/scripts/<script-name>.ts`
3. 将本文档中所有 `${SKILL_DIR}` 替换为实际路径

| 脚本 | 用途 |
|------|------|
| `scripts/x-topic-selector.ts` | 主脚本 - 抓取、评分、生成报告 |
| `scripts/ai-scorer.ts` | Gemini API 集成，AI 评分 |
| `scripts/report-generator.ts` | Markdown 报告生成 |
| `scripts/x-utils.ts` | Chrome CDP 工具函数 |

---

## 参数映射

| 交互选项 | 脚本参数 |
|----------|----------|
| 数据分析模式 | `--score-mode data-only` |
| AI 分析模式 | `--score-mode ai-only` |
| 自动检测 (AI 服务商) | (不传 `--ai-provider` 参数) |
| Gemini | `--ai-provider gemini` |
| OpenAI 兼容 | `--ai-provider openai` |
| AI 工具/产品发布 | `--topic-category ai-tools` |
| 行业新闻/动态 | `--topic-category industry-news` |
| 技术突破/论文 | `--topic-category tech-breakthroughs` |
| 教程/实用技巧 | `--topic-category tutorials` |
| 争议/讨论话题 | `--topic-category controversial` |
| 不限 | `--topic-category all` |
| 100 条 | `--max-tweets 100` |
| 200 条 | `--max-tweets 200` |
| 500 条 | `--max-tweets 500` |
| 5 条 | `--top-n 5` |
| 10 条 | `--top-n 10` |
| 20 条 | `--top-n 20` |

---

## 环境要求

- Google Chrome 或 Chromium 浏览器
- `bun` 运行时
- GEMINI_API_KEY 环境变量（Gemini 模式或自动检测模式需要）
- GEMINI_MODEL 环境变量（可选，默认 `gemini-2.0-flash`，可设置为 `gemini-1.5-pro` 等）
- OPENAI_API_KEY 环境变量（OpenAI 兼容模式需要）
- OPENAI_MODEL 环境变量（OpenAI 兼容模式必需，如 `deepseek-chat`、`gpt-4o`）
- OPENAI_API_BASE 环境变量（OpenAI 兼容模式可选，自定义 API 端点）

---

## 扩展配置 (EXTEND.md)

支持在用户项目目录下创建 `EXTEND.md` 文件进行默认配置：

```markdown
## x-ai-topic-selector

- keywords: AI,GPT,Claude,LLM,Machine Learning
- exclude: giveaway,airdrop,crypto,nft
- top-n: 10
- translate: true
```

---

## Thread 自动展开

脚本会自动检测并展开 Thread（帖子串），获取完整内容而非仅首贴。

**工作原理**：
- 对于非转发推文，脚本会导航到详情页检查是否为 Thread
- 如果是 Thread，提取同一作者的所有连续推文内容
- 多个部分用 `---` 分隔合并为一条记录

**报告显示**：
- Thread 帖子在报告中会显示 `📜 Thread (N 条)` 标识
- Thread 整体算作 1 条帖子，不重复计数
- 互动数据使用 Thread 首贴的数据

**注意事项**：
- Thread 展开会增加少量抓取时间（每条约 3 秒）
- 如果展开失败，会自动回退到仅使用首贴内容

---

## 故障排除

### "Chrome not found"
设置 `X_BROWSER_CHROME_PATH` 环境变量指向 Chrome 可执行文件路径。

### "Please log in to X"
首次运行时，脚本会打开 Chrome 窗口等待登录。请在窗口中手动登录 X 账号。

### "GEMINI_API_KEY not set"
Gemini 模式或自动检测模式需要设置 Gemini API Key，可以通过交互流程提供。

### "OPENAI_API_KEY not set" 或 "OPENAI_MODEL not set"
OpenAI 兼容模式需要设置以下环境变量：
- `export OPENAI_API_KEY="your-api-key"`
- `export OPENAI_MODEL="deepseek-chat"` （必需）
- `export OPENAI_API_BASE="https://api.deepseek.com/v1"` （可选，自定义端点）

如果使用自动检测模式（`--ai-provider` 未指定），需要至少配置 Gemini 或 OpenAI 其中之一。

### "No tweets found"
- 检查列表 URL 是否正确
- 确保已在 Chrome profile 中登录 X
- 列表可能是私有的或为空
