---
name: dify_creator
description: 通过多轮对话引导用户确定需求，参考现有 Dify 案例，生成可直接导入 Dify 的工作流 DSL YAML 配置
license: CC BY-NC-SA 4.0
author: 沐然
---

# Dify 工作流生成器 (dify_creator)

通过多轮对话引导用户明确需求，**参考 `organized_dsl/` 目录中的现有案例**，生成符合对应 Dify 版本规范的 DSL YAML 文件，可直接导入 Dify 使用。

> ⚠️ **重要：搜索文件前必须先切换到技能目录！**
>
> ```bash
> cd "c:\Users\14429\.claude\skills\dify_creator"
> ```
>
> 然后再搜索 `organized_dsl/INDEX.md`和 `organized_dsl/**/*.yml`

## 核心能力

- **智能对话引导**：通过提问帮助用户梳理需求，避免遗漏关键信息
- **案例参考定位**：基于 INDEX.md 索引，自动匹配相似 Dify 案例
- **工作流结构设计**：分析需求后给出流程结构，与用户确认
- **完整 DSL 生成**：参考 DSL 节点指南，生成符合规范的完整 YAML 配置

## 使用场景

- 创建智能客服对话流程
- 构建 RAG 知识库问答系统
- 设计音视频处理工作流
- 开发代码生成和文档处理工具
- 搭建多模型协作的复杂流程

---

## 工作流程总览

```
用户需求 → 案例定位 → 流程设计 → 用户确认 → DSL生成 → 交付
```

### 核心步骤

| 步骤 | 名称 | 输出 |
|------|------|------|
| Step 1 | 收集需求 | 需求文档 |
| Step 2 | 案例定位 | 参考案例列表 |
| Step 3 | 流程设计 | 流程结构图 |
| Step 4 | 用户确认 | 确认反馈 |
| Step 5 | DSL生成 | 完整YAML文件 |

---

## Step 1：收集用户需求

首先向用户询问基础信息，明确工作流的目标和功能。

### 1.1 基础信息收集

```markdown
请告诉我关于你要创建的 Dify 工作流的基本信息：

1. **工作流名称**（英文，使用连字符，如：document-processor）
2. **一句话描述**：这个工作流做什么？
3. **应用类型**：
   - workflow：批处理任务，单轮执行
   - advanced-chat：高级聊天模式，支持多轮对话
   - chatflow：对话式应用，简单多轮交互
4. **目标用户**：谁会使用这个工作流？
```

### 1.2 功能需求收集

根据用户选择的应用类型，深入询问功能需求：

**通用问题：**

```markdown
5. **输入方式**：用户如何提供输入？
   - 文本输入（短文本/长文本）
   - 文件上传（图片/PDF/音视频/文档）
   - 混合输入

6. **核心处理**：工作流需要执行哪些处理步骤？
   - 数据预处理 → 核心处理 → 结果输出
   - 请尽可能描述每个步骤

7. **输出形式**：最终返回什么结果？
   - 文本回复
   - 结构化数据（JSON/Markdown表格）
   - 文件（图片/PDF/音频）
   - 混合输出
```

**根据功能类型补充：**

| 功能类型 | 补充问题 |
|---------|---------|
| **RAG问答** | 知识库来源？检索策略（关键词/向量）？召回数量？是否需要重排序？ |
| **音视频处理** | 音频提取？语音识别（ASR）？内容总结？字幕生成？ |
| **文档处理** | PDF解析？内容提取？格式转换？OCR识别？ |
| **图像生成** | 文生图？图生图？风格迁移？是否需要多图组合？ |
| **数据处理** | 数据来源（API/数据库/文件）？分析维度？图表类型？ |
| **工具调用** | 使用哪些工具/插件？调用频率？是否需要MCP？ |
| **多模型协作** | 调用哪些模型？分工是什么？模型间如何传递信息？ |

### 1.3 模型和工具配置

```markdown
8. **大模型选择**：
   - 模型提供商：OpenAI / Anthropic / 国内模型（硅基流动/通义千问/零一万物等）
   - 模型名称：如 gpt-4o, deepseek-V3, qwen-max
   - 参数设置：temperature（创意度 0-1）、max_tokens 等

9. **工具/插件**：
   - 内置工具：代码执行、知识检索、HTTP请求、TTS等
   - 第三方插件：PDF处理、数据库连接等
   - MCP服务：是否需要集成外部MCP工具？

10. **知识库（可选）**：
    - 是否需要接入知识库？
    - 知识库ID和名称
    - 检索策略配置
```

### 1.4 流程控制询问

```markdown
11. **流程分支**：是否有条件分支？（是/否）
    - 如果是，分支条件是什么？（例如：根据用户意图分类走不同处理路径）
12. **循环处理**：是否需要迭代处理批量数据？（是/否）
    - 例如：批量处理多个文件、对列表中每项进行处理
13. **会话状态**：是否需要保存会话状态？（是/否）
    - 例如：记录用户偏好、跨轮次变量传递
14. **错误处理**：失败时如何处理？
    - 终止流程并报错
    - 继续执行其他分支
    - 返回默认结果
```

---

## Step 2：案例定位（基于 INDEX.md）

根据收集的需求，在 `organized_dsl/INDEX.md` 中定位相似案例。

### 2.0 搜索路径配置

```markdown
⚠️ **关键步骤：搜索前必须先切换到技能目录！**

**第一步：切换到技能目录（必须执行）**
```bash
cd "c:\Users\14429\.claude\skills\dify_creator"
```

**第二步：搜索 DSL 文件**
- 搜索 `organized_dsl/**/*.yml`（在技能目录下搜索）

**第三步：搜索索引文件**
- 搜索 `organized_dsl/INDEX.md`
- 搜索 `organized_dsl/Dify_DSL_节点完整参考指南.md`

**错误做法：**
- ❌ 直接搜索 `**/*.yml`（当前目录可能不对）
- ❌ 搜索 `**/organized_dsl/**/*.yml`（路径重复）
- ❌ 搜索 `**/*.yaml`（文件是 .yml 不是 .yaml）
- ❌ 在其他目录下搜索 `organized_dsl/**/*.yml`（会找不到）

**正确做法：**
1. 先执行 `cd "c:\Users\14429\.claude\skills\dify_creator"`
2. 再搜索 `organized_dsl/**/*.yml`
3. 再搜索 `organized_dsl/INDEX.md`
```

### 2.1 读取 INDEX.md 索引

首先读取索引文件了解案例分类：

```markdown
1. 搜索并读取 `organized_dsl/INDEX.md`
2. 根据用户需求的功能类型，定位相关分类目录
3. 在对应目录中搜索相似功能的 DSL 案例（使用 `organized_dsl/**/*.yml`）
```

### 2.2 分类定位

根据功能类型查找对应目录：

```markdown
根据你的需求，我定位到以下相关分类：

| 分类 | 目录路径 |
|------|----------|
| 内容创作 | `01_内容生成与创作/` |
| 图像生成 | `02_图像生成与设计/` |
| 视频生成 | `03_视频生成/` |
| 数据分析 | `04_数据分析与可视化/` |
| 文档处理 | `05_文档处理与OCR/` |
| 知识库RAG | `06_知识库与RAG/` |
| Agent工具 | `07_Agent与工具调用/` |
| 教育学习 | `08_教育与学习/` |
| 商业办公 | `09_商业与办公/` |
| 多媒体处理 | `10_多媒体处理/` |
| 代码开发 | `11_代码与开发/` |
| 创意娱乐 | `12_创意与娱乐/` |
```

### 2.3 复杂度匹配

根据节点数量匹配复杂度：

| 复杂度 | 节点数 | 适用场景 |
|--------|--------|----------|
| 简单 | 3-5个 | 单一功能，线性流程 |
| 中等 | 6-15个 | 多步骤处理，有分支 |
| 复杂 | 16+个 | 多模块协作，循环处理 |

### 2.4 输出参考案例列表

```markdown
找到以下与你需求相关的参考案例：

### 📂 案例1：[案例名称]
- **位置**：`目录路径/文件名.yml`
- **复杂度**：简单/中等/复杂
- **节点数**：X个
- **主要节点**：start → llm → answer
- **参考价值**：节点结构、Prompt模板、流程设计

### 📂 案例2：[案例名称]
...

请确认：
- 是否需要查看更多相似案例？
- 哪些案例的结构最符合你的需求？
```

### 2.5 读取并分析参考案例

选定参考案例后，读取 DSL 文件进行分析：

```markdown
我已读取参考案例，以下是关键配置提取：

**节点结构：**
```
[开始节点]
  ↓
[LLM节点] - 模型: xxx, Prompt: xxx
  ↓
[工具节点] - 工具: xxx
  ↓
[输出节点]
```

**关键配置参考：**
- LLM prompt模板：...
- 变量传递方式：...
- 条件分支逻辑：...
```

---

## Step 3：工作流结构设计

根据需求分析和参考案例，设计工作流结构。

### 3.1 设计原则

1. **KISS原则**：保持简单，避免过度设计
2. **模块化**：将复杂流程拆分为可复用的步骤
3. **清晰变量**：使用有意义的变量名，便于追踪

### 3.2 输出流程结构图

```markdown
根据你的需求，我设计了以下工作流结构：

## 📊 流程结构图

```
┌─────────────┐
│   开始节点   │  输入：{{input_var}}
└──────┬──────┘
       ↓
┌─────────────┐
│  预处理节点  │  功能：数据清洗/格式转换
└──────┬──────┘
       ↓
┌─────────────┐
│   核心处理   │  功能：LLM调用/工具执行
│   (分支判断) │  条件：{{condition}}
└──────┬──────┘
   ┌────┴────┐
   ↓         ↓
┌──────┐  ┌──────┐
│分支A │  │分支B │
└────┬─┘  └────┬─┘
   │          │
   └────┬─────┘
        ↓
┌─────────────┐
│   结果处理   │  功能：格式化/聚合
└──────┬──────┘
       ↓
┌─────────────┐
│   输出节点   │  输出：{{output_var}}
└─────────────┘
```

## 📋 节点列表

| 序号 | 节点名称 | 节点类型 | 功能描述 | 输入变量 | 输出变量 |
|------|---------|---------|---------|---------|---------|
| 1 | 开始 | start | 接收用户输入 | - | user_input |
| 2 | 预处理 | code | 数据清洗 | user_input | clean_data |
| 3 | LLM处理 | llm | 生成内容 | clean_data | llm_result |
| 4 | 条件判断 | if-else | 分支处理 | llm_result | branch |
| 5 | 输出 | answer | 返回结果 | final_result | - |

## 📝 关键配置

**LLM配置：**
- 模型：xxx
- Prompt模板：xxx

**变量传递：**
- 上游输出 → 下游输入
```

---

## Step 4：用户确认（⚠️ 必须步骤）

**警告：未获得用户明确确认前，禁止生成 DSL！**

向用户展示结构设计，必须获取以下确认后才能继续：

### 4.1 确认内容

```markdown
## 工作流结构确认 ⚠️

在生成 DSL 文件之前，请确认以下设计：

### ✅ 流程结构
- 节点数量：X 个
- 流程分支：X 条
- 循环处理：X 处

### ✅ 节点配置
1. [节点1]：确认配置 ✓
2. [节点2]：需要调整 →
3. [节点3]：确认配置 ✓

### ✅ 待确认事项
1. 模型选择是否正确？
2. Prompt模板是否需要调整？
3. 分支条件是否合理？
4. 输出格式是否满足需求？

**请回复「确认」或「继续」以生成 DSL，或提供修改意见。**
```

### 4.2 确认检查清单

```markdown
生成 DSL 前必须确认以下全部项目：

- [ ] 用户明确回复「确认」或「继续」
- [ ] 所有节点配置已与用户核对
- [ ] 模型和参数已获用户认可
- [ ] 输出格式符合用户需求

**未满足上述条件，禁止跳到 Step 5！**
```

### 4.3 调整迭代

如果用户有修改意见，迭代调整直到确认：

```markdown
根据你的反馈，我进行了以下调整：

1. 修改了 LLM 节点 Prompt 模板
2. 添加了新的条件分支
3. 调整了变量传递逻辑

请再次确认。
```

---

## Step 5：生成完整 DSL（⚠️ 必须参考案例）

**生成 DSL 前必须完成以下步骤：**

1. ✅ 已切换到技能目录：`cd "c:\Users\14429\.claude\skills\dify_creator"`
2. ✅ 已在 Step 2 中读取并分析了参考案例
3. ✅ 已在 Step 4 中获得用户明确确认
4. ✅ 已读取 `organized_dsl/Dify_DSL_节点完整参考指南.md`

### 5.1 前置检查

```markdown
生成 DSL 前确认：

- [ ] 已选定参考案例文件（路径：xxx/xxx.yml）
- [ ] 已读取节点配置参考指南
- [ ] 已获得用户「确认」回复
- [ ] 所有节点配置已确定

**未完成以上步骤，禁止生成 DSL！**
```

### 5.2 生成结构

```yaml
app:
  description: '{{description}}'
  icon: '{{icon}}'
  icon_background: '{{icon_background}}'
  mode: '{{mode}}'
  name: '{{name}}'
  use_icon_as_answer_icon: false
kind: app
version: {{参考案例的版本号}}
workflow:
  conversation_variables: []
  environment_variables: []
  features:
    file_upload: {}
    # ... 其他功能配置
  graph:
    edges: []
    nodes: []
  viewport: {}
```

### 5.3 节点 ID 生成规则

- 使用时间戳+随机数作为节点 ID
- 格式：`{时间戳}{随机6位数字}`
- 示例：`1741011655068`, `1735195133945`

### 5.4 位置计算

节点在画布上的位置根据流程顺序自动计算：
- X 坐标：每增加一个节点向右移动约 300px
- Y 坐标：统一居中或根据分支调整

### 5.5 完整输出示例

```yaml
# ============================================
# Dify 工作流 DSL 文件
# 名称：xxx
# 生成时间：2026-01-03
# 参考案例：xxx.yml
# ============================================

app:
  description: '工作流描述'
  icon: 🤖
  icon_background: '#FFEAD5'
  mode: workflow
  name: xxx
kind: app
version: {{参考案例的版本号}}
workflow:
  graph:
    edges:
    # ... 连接配置
    nodes:
    # ... 节点配置
```

### ⚠️ 5.6 节点编写规则（重要！）

**每个节点都必须参考 organized_dsl 案例库中的示例格式编写！**

```markdown
生成工作流时，请严格遵循以下规则：

1. **先查找参考案例**
   - 搜索 `organized_dsl/**/*.yml` 找到相似功能的 DSL 文件
   - 搜索 `organized_dsl/Dify_DSL_节点完整参考指南.md` 查看节点配置说明

2. **节点结构必须完整**
   每个节点必须包含：
   - `id`: 唯一标识
   - `data.type`: 节点类型
   - `data.title`: 节点标题
   - `position`: 画布位置 {x, y}
   - `width`/`height`: 节点尺寸（可选）

3. **禁止凭空编写**
   - ❌ 不要凭记忆或想象编写节点
   - ✅ 必须复制参考案例的结构，替换关键字段

4. **特别注意事项**
   - **迭代节点**：必须包含 iteration-start 子节点和所有必要标记
   - **LLM 节点**：必须包含 model.provider、model.name、prompt_template
   - **HTTP 请求**：必须包含正确的 authorization 和 body 配置
   - **变量引用**：必须使用 `{{#节点ID.变量#}}` 格式
```

### ⚠️ 5.7 生成后强制检查（❗必须执行）

**生成 DSL 后，必须按以下步骤强制检查每个节点！**

```markdown
## DSL 生成后强制检查 ⚠️

**警告：未完成检查，禁止交付给用户！**

### 第一步：确定版本号
```yaml
version: {{参考案例的版本号}}  # ✅ 与参考案例保持一致
```

**要点：** 版本号应与所选参考案例保持一致，不是固定值。

### 第二步：遍历每个节点，逐一对照参考案例检查

**对于每个生成的节点，执行以下检查：**

1. **在参考案例中找到同类型节点**
   ```bash
   cd "c:\Users\14429\.claude\skills\dify_creator"
   rg "type: 节点类型" organized_dsl/**/*.yml | head -20
   ```

2. **读取参考案例中的节点结构**
   - 打开对应的 DSL 文件
   - 找到相同类型的节点配置

3. **逐字段对比**
   | 字段 | 参考案例 | 生成结果 | 是否正确 |
   |------|---------|---------|---------|
   | data.positionAbsolute | false | ? | |
   | data.selected | false | ? | |
   | height | 52 | ? | |
   | width | 242 | ? | |
   | ... | ... | ... | |

4. **标记差异并修正**
   - 发现任何差异，立即修正
   - 不能确定的字段，参考案例使用原值

### 第三步：边连接检查

**遍历每条边，检查以下字段：**
- [ ] `data.sourceType`: 源节点类型
- [ ] `data.targetType`: 目标节点类型
- [ ] `data.selected`: false
- [ ] `data.isInIteration`: false（迭代外）
- [ ] `type`: custom/true/false/isInIteration

### 第四步：特殊节点重点检查

| 节点类型 | 检查重点 |
|---------|---------|
| `variable-aggregator` | `output_type` + `variables` 数组（不是 outputs/formatter_template） |
| `end` | `type: end` + `outputs`（不是 type: answer） |
| `iteration` | `start_node_id` 指向 iteration-start |
| `llm` | `model.provider`, `model.name`, `prompt_template` |
| `http-request` | `authorization`, `body` 配置完整 |

### 第五步：检查报告

```markdown
## DSL 检查报告

### 节点检查结果
| 节点ID | 节点类型 | 检查状态 | 问题 |
|--------|---------|---------|------|
| xxx | start | ✅ 通过 | 无 |
| xxx | llm | ❌ 失败 | 缺少 model.provider |

### 边检查结果
| 边ID | 类型 | 检查状态 | 问题 |
|------|-----|---------|------|
| xxx | custom | ✅ 通过 | 无 |

### 最终结论
- [ ] 所有节点检查通过
- [ ] 所有边检查通过
- [ ] 无需修正，可以交付
```

**检查不通过的处理：**
1. 定位问题节点
2. 读取参考案例
3. 修正节点配置
4. 重新检查直到通过
```

---

## Dify DSL 结构规范

### 完整结构模板

```yaml
app:
  description: '应用描述'
  icon: 🤖
  icon_background: '#FFEAD5'
  mode: workflow|advanced-chat|chatflow
  name: 应用名称
  use_icon_as_answer_icon: false
kind: app
version: {{参考案例的版本号}}
workflow:
  conversation_variables: []   # 会话变量
  environment_variables: []    # 环境变量
  features:
    file_upload:               # 文件上传配置
      enabled: false
      # ... 详细配置
    opening_statement: ''      # 开场白
    retriever_resource:        # 检索资源
      enabled: true
    text_to_speech:            # TTS配置
      enabled: false
  graph:
    edges: []                  # 连线列表
    nodes: []                  # 节点列表
  viewport:                    # 视图位置
    x: 0
    y: 0
    zoom: 1
dependencies: []               # 插件依赖
```

### 节点类型说明

| 节点类型 | 用途 | 关键配置 |
|---------|------|---------|
| `start` | 开始节点 | variables（输入变量定义） |
| `llm` | 大语言模型 | model、prompt_template、vision、context |
| `answer` | **Chatflow** 直接回复 | answer（输出模板），仅用于对话式应用 |
| `knowledge-retrieval` | 知识库检索 | dataset_ids、query_variable_selector |
| `tool` | 工具调用 | provider_id、tool_name、tool_parameters |
| `code` | 代码执行 | code、code_language、outputs、variables |
| `http-request` | HTTP请求 | method、url、authorization、body |
| `if-else` | 条件分支 | cases（条件判断） |
| `template-transform` | 模板转换 | template、variables |
| `assigner` | **写入会话变量** | items、write_mode |
| `variable-aggregator` | **聚合多分支输出** | variables、output_type（不是简单整合！） |
| `iteration` | ⚠️ 循环处理 | iterator_selector、output_selector、**start_node_id（必填！）** |
| `document-extractor` | 文档提取 | variable_selector、is_array_file |
| `agent` | 智能体 | agent_parameters、agent_strategy_name |
| `end` | **Workflow** 结束节点 | outputs（输出变量），仅用于工作流 |

### 变量引用语法

```yaml
# 引用格式：{{#节点ID.输出字段#}}

# 引用开始节点的输入
{{#1742961448129.file#}}

# 引用 LLM 节点的文本输出
{{#1742965550311.text#}}

# 引用 Code 节点的自定义输出
{{#1747670104835.result#}}

# 引用会话变量
{{#conversation.status#}}

# 引用环境变量
{{#env.API_KEY#}}
```

---

## ⚠️ 迭代节点规范（关键！）

**迭代节点是 DSL 中最容易出错的部分，缺少任何一项都会导致导入失败！**

### 迭代节点完整结构

```yaml
# 1. iteration 节点 - 循环控制器
- id: '1741011600006'
  data:
    iterator_selector: ['1741011655068', 'text']  # 要遍历的数组
    output_selector: ['1741011662463', 'result']  # 输出结果
    output_type: array[object]                     # 必须格式
    start_node_id: 1741011600006start              # 必须指向 iteration-start
    title: 迭代处理
    type: iteration
  position: {x: 200, y: 100}

# 2. iteration-start 节点 - 迭代入口（必须有！）
- id: 1741011600006start
  data:
    title: 迭代开始
    type: custom-iteration-start
  parentId: '1741011600006'    # 必须指向父迭代节点
  position: {x: 200, y: 200}

# 3. 迭代内部节点 - 处理每个元素
- id: '1741011662463'
  data:
    isInIteration: true         # 必须标记在迭代内
    iteration_id: '1741011600006'  # 必须标识所属迭代
    parentId: '1741011600006'   # 必须指向父迭代
    title: 处理节点
    type: llm
  position: {x: 200, y: 300}

# 4. 迭代内部边 - 连接迭代内节点
- source: 1741011600006start
  target: '1741011662463'
  type: isInIteration           # 必须是 isInIteration
  zIndex: 1002                  # 必须的渲染层级
```

### 成功版 vs 失败版对比

| 对比项 | ✅ 成功版 | ❌ 失败版 |
|--------|------------|----------|
| 版本 | 参考案例的版本 | 版本不一致 |
| iteration-start | ✅ 有 | ❌ 缺少 |
| parentId | ✅ 有 | ❌ 缺少 |
| iteration_id | ✅ 有 | ❌ 缺少 |
| isInIteration 边 | ✅ 有 | ❌ 缺少 |
| zIndex: 1002 | ✅ 有 | ❌ 缺少 |
| output_type 格式 | `array[object]` | 错误格式 |
| start_node_id | ✅ 指向 iteration-start | ❌ 缺少 |

### ❌ 常见错误

| 问题 | 说明 |
|-----|------|
| 缺少 iteration-start | 迭代必须有专门的 start 子节点，不是"内置"的 |
| 缺少 parentId | 迭代内部节点无法识别归属哪个迭代 |
| 缺少 iteration_id | 迭代无法正确管理内部节点 |
| 缺少 zIndex: 1002 | 迭代内部边渲染层级错误 |
| output_type 格式错误 | 必须是 `array[object]` |

### 迭代边连接类型

| 类型 | 说明 | 是否用于迭代 |
|-----|------|-------------|
| `custom` | 普通连接 | ❌ 迭代外 |
| `true` | 条件为真 | ❌ |
| `false` | 条件为假 | ❌ |
| `isInIteration` | 迭代内连接 | ✅ 必须用这个 |

---

### Edge 连接类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `custom` | 普通连接 | source → target |
| `true` | 条件为真分支 | if-else → true |
| `false` | 条件为假分支 | if-else → false |
| `custom_case_id` | 自定义分支 | if-else → 自定义case_id |
| `isInIteration` | 循环内连接 | iteration内节点连接 |

---

## 使用示例

### 示例：翻译工作流

**用户需求：**
- 名称：zh-en-translator
- 功能：中译英翻译
- 类型：workflow
- 输入：中文文本
- 流程：用户输入 → LLM翻译 → 返回结果

**生成配置：**

```yaml
app:
  description: '中英文翻译工作流'
  icon: 🌐
  icon_background: '#E3F2FD'
  mode: workflow
  name: zh-en-translator
kind: app
version: {{参考案例的版本号}}
workflow:
  graph:
    edges:
    - source: '1741011655068'
      target: '1741011662463'
      type: custom
    - source: '1741011662463'
      target: llm
      type: custom
    - source: llm
      target: answer
      type: custom
    nodes:
    - data:
        title: 开始
        type: start
        variables:
        - variable: text
          type: paragraph
          label: 输入中文文本
          required: true
      id: '1741011655068'
      position: {x: 0, y: 263}
    - data:
        context:
          enabled: false
        model:
          provider: siliconflow
          name: internlm2_5-7b-chat
          mode: chat
        prompt_template:
        - role: system
          text: '请将以下中文翻译成英文，只输出翻译结果：{{#1741011655068.text#}}'
        title: LLM翻译
        type: llm
      id: llm
      position: {x: 382, y: 263}
    - data:
        answer: '{{#llm.text#}}'
        title: 翻译结果
        type: answer
      id: answer
      position: {x: 690, y: 263}
```

---

## 最佳实践

### 1. 案例复用策略

1. **先定位**：通过 INDEX.md 找到最相似的案例
2. **再分析**：阅读 DSL 文件，理解节点配置
3. **后调整**：基于参考模板进行个性化修改

### 2. 流程设计原则

1. **从简单开始**：先实现核心功能，再添加分支和循环
2. **模块化设计**：复杂流程拆分为可复用步骤
3. **清晰命名**：使用有意义的变量名

### 3. DSL 编写检查清单

- [ ] 节点 ID 唯一且格式正确
- [ ] 位置坐标合理，不重叠
- [ ] Edge 连接正确，无断链
- [ ] 变量引用格式正确
- [ ] Model/Provider 配置有效
- [ ] 输出变量名与引用一致

### 4. 测试验证建议

1. 生成后在 Dify 中导入测试
2. 检查各节点的输入输出
3. 验证条件分支逻辑
4. 测试边界情况和错误处理

---

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 需求不完整 | 提示用户补充缺失信息 |
| 流程逻辑错误 | 指出可能的循环引用或断链 |
| 节点配置错误 | 提供修正建议 |
| 变量引用无效 | 列出可用的变量选项 |
| 案例定位失败 | 扩大搜索范围或手动设计 |

---

## 参考资源

### 📂 案例目录结构

```
organized_dsl/
├── 01_内容生成与创作/
├── 02_图像生成与设计/
├── 03_视频生成/
├── 04_数据分析与可视化/
├── 05_文档处理与OCR/
├── 06_知识库与RAG/
├── 07_Agent与工具调用/
├── 08_教育与学习/
├── 09_商业与办公/
├── 10_多媒体处理/
├── 11_代码与开发/
├── 12_创意与娱乐/
├── 13_信息聚合/
├── 14_参考示例/
├── INDEX.md                    # 案例索引（搜索 organized_dsl/INDEX.md）
└── Dify_DSL_节点完整参考指南.md  # 节点配置参考（搜索 organized_dsl/Dify_DSL_节点完整参考指南.md）
```

### 📖 文档链接

- **INDEX.md**：按功能分类的案例索引
- **Dify_DSL_节点完整参考指南.md**：各节点的详细配置说明

---

## 节点自动校验与生成规则

### 版本号规则

```yaml
# ✅ 正确 - 生成时必须使用
version: {{参考案例的版本号}}

# ❌ 错误 - 禁止使用
version: {{参考案例的版本号}}
```

### 节点基础字段规则

**每个节点生成时必须包含：**

```yaml
- data:
    positionAbsolute: false      # ✅ 必须
    selected: false              # ✅ 必须
    title: "节点名称"
    type: "节点类型"
    # ... 其他字段
  height: 52
  id: '节点ID'
  position:
    x: 0
    y: 0
  width: 242
```

### Edges 字段规则

**每条边生成时必须包含：**

```yaml
- data:
    isInIteration: false         # ✅ 必须
    selected: false              # ✅ 必须
    sourceType: "源节点类型"
    targetType: "目标节点类型"
  id: "边ID"
  source: "源节点ID"
  sourceHandle: "source"
  target: "目标节点ID"
  targetHandle: "target"
  type: "custom|true|false|isInIteration"
```

### variable-aggregator 节点生成规则

```yaml
# ✅ 正确写法 - 用于聚合多分支输出
- data:
    output_type: string          # 聚合结果的输出类型
    type: variable-aggregator
    variables:                   # 聚合多分支的变量（二维数组）
    - - '分支节点ID1'             # 第一个分支的输出
      - text
    - - '分支节点ID2'             # 第二个分支的输出
      - text
  height: 211
  id: '聚合节点ID'

# ❌ 错误理解 - 不是简单的"将多个内容整合到一起"
# variable-aggregator 的真正用途：
# - 整合 IF/ELSE 条件分支的输出
# - 整合并行结构的多个输出
# - 确保无论哪个分支执行，下游都能通过统一变量引用
```

### end 节点生成规则

```yaml
# ✅ 正确写法 - Workflow 应用的结束节点
- data:
    outputs:
    - value_selector:
      - '上游节点ID'
      - text
      variable: output
    type: end                    # ✅ 使用 type: end（仅用于 Workflow）
  height: 103
  id: end
```

### answer 节点使用场景

```yaml
# ✅ 正确写法 - 仅用于 Chatflow 应用
- data:
    answer: '{{#llm.text#}}'     # 使用 answer 字段
    type: answer                 # ✅ 使用 type: answer（仅用于 Chatflow）
```

---

## DSL 生成检查清单（生成后必查）

生成 DSL 后，逐项检查：

**应用类型检查：**
- [ ] Workflow 类型使用 `type: end`，Chatflow 类型使用 `type: answer`
- [ ] Workflow 只能有唯一 End 节点
- [ ] Chatflow 支持多个 Answer 节点

**节点检查：**
- [ ] 版本号与参考案例一致
- [ ] 每个节点有 `data.positionAbsolute: false`
- [ ] 每个节点有 `data.selected: false`
- [ ] 每个节点有 `height` 和 `width`

**边检查：**
- [ ] 每条边有 `data.sourceType`
- [ ] 每条边有 `data.targetType`
- [ ] 每条边有 `data.selected: false`
- [ ] 每条边有 `data.isInIteration`（迭代外为 false）

**variable-aggregator 检查：**
- [ ] 使用 `output_type`（不是 `outputs`）
- [ ] 使用 `variables` 数组格式（不是 `formatter_template`）
- [ ] 理解用途：聚合多分支输出，不是简单整合内容

**assigner vs variable-aggregator 检查：**
- [ ] 需要写入会话变量 → 使用 `assigner`
- [ ] 需要聚合多分支输出 → 使用 `variable-aggregator`

---

*最后更新: 2026-01-03*
*参考案例数: 125+*
