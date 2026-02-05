---
name: morphism-mapper
description: Category Theory Morphism Mapper v2.6 - 基于范畴论的跨领域结构映射工具，将 Domain A 的问题结构映射到远域 Domain B，借助 B 领域的成熟定理生成非共识创新方案。当用户需要解决复杂问题、寻找创新思路、突破思维定势、进行跨学科类比、或新增/扩展领域知识时使用。支持基础四阶段流程（提取范畴骨架→选择异构域→执行结构映射→拉回合成提案）、高级按需挂载模块（Yoneda Probe、Natural Transformation、Adjoint Balancer、Limits/Colimits）、以及领域知识管理（新增自定义领域、升级领域版本）。触发关键词包括"看不穿商业模式"、"环境变了需要转型"、"方案如何落地"、"多领域交叉验证"、"增加易经思想领域"、"升级领域知识"等。
---

# Category Theory Morphism Mapper v2.6

基于范畴论的函子映射逻辑，将 Domain A 的问题结构映射到远域 Domain B，借助 B 领域的成熟定理生成创新方案。

**版本**: v2.6  
**更新日期**: 2025-02  
**领域数量**: 27个内置领域（24个原有 + 3个新增）  
**领域版本**: V2（100基本基石 + 14 Objects + 14 Morphisms + 18 Theorems）

## 核心原理

1. **Object Preservation**: 识别 Domain A 核心实体
2. **Morphism Preservation**: 识别实体间动态关系
3. **Composition Consistency**: 映射结果可拉回并保持逻辑闭环

## 使用模式

### 模式一：快捷命令（问题求解）

- `/morphism-extract "问题描述"` - 提取范畴骨架
- `/morphism-domains` - 列出可用 Domain B
- `/morphism-map <domain>` - 执行到指定领域的映射
- `/morphism-synthesize` - 拉回合成生成提案
- `/morphism-config` - 配置和扩展

### 模式二：对话引导（问题求解）

直接描述问题，自动进入四阶段流程：
1. Category Extraction - 提取范畴骨架
2. Domain Selection - 推荐 Domain B
3. Functorial Mapping - 执行结构映射
4. Pull-back & Synthesis - 生成提案

### 模式三：领域知识管理（新增功能 v2.5）

**新增领域**：
- `/morphism-add-domain "领域名称"` - 基于V2标准创建新领域
- `/morphism-add-domain "易经思想"` - 示例：增加易经思想领域
- `/morphism-add-domain "中医"` - 示例：增加中医领域
- `/morphism-list-domains` - 查看所有领域（包括自定义）

**快捷用法示例**：
- `"morphism-mapper技能增加易经思想领域"` → 自动创建易经思想领域文件
- `"增加中医领域到morphism-mapper"` → 自动创建中医领域文件
- `"新增领域：孙子兵法"` → 自动创建孙子兵法领域文件

## 内置领域清单（v2.5 - 27个领域）

### 物理学与复杂性科学
- `quantum_mechanics` - 量子力学（叠加态、不确定性、纠缠）
- `thermodynamics` - 热力学（能量、熵、耗散结构）
- `information_theory` - 信息论（熵、信道容量、噪声）
- `complexity_science` - 复杂性科学（涌现、混沌、自组织）

### 生命科学与认知
- `evolutionary_biology` - 进化生物学（选择、适应、关键创新）
- `ecology` - 生态学（种群、共生、生态位）
- `immunology` - 免疫学（识别、记忆、耐受）
- `neuroscience` - 神经科学（神经可塑性、预测编码）
- `zhuangzi` - 庄子哲学（变化、尺度、相对性）

### 系统与控制
- `control_systems` - 控制系统（反馈、调节、稳定）
- `distributed_systems` - 分布式系统（一致性、共识、分区容错）
- `network_theory` - 网络理论（节点、连接、传播）

### 数学与运筹
- `game_theory` - 博弈论（策略、均衡、信号）
- `operations_research` - 运筹学（优化、约束、排队）
- `second_order_thinking` - 二阶思维（反馈延迟、意外后果）

### 经济与社会
- `behavioral_economics` - 行为经济学（认知偏差、损失厌恶）
- `social_capital` - 社会资本（网络、信任、结构洞）
- `incentive_design` - 激励机制设计（动机、委托代理）
- `linguistics` - 语言学（符号、意义、隐喻）

### 战略与创新
- `military_strategy` - 军事战略（机动、后勤、OODA）
- `innovation_theory` - 创新理论（颠覆性、S曲线、网络效应）
- `kaizen` - 精益/持续改善（浪费消除、PDCA、现场）
- `antifragility` - 反脆弱性（凸性、选择权、杠铃策略）
- `mythology` - 神话学/原型（英雄之旅、阈限、阴影）

### ⭐ 新增领域（v2.5）
- `anthropology` - 人类学（文化、田野调查、参与观察）
- `religious_studies` - 宗教学（神圣与世俗、仪式、象征）
- `mao_zedong_thought` - 毛泽东思想（实践论、矛盾论、持久战）

### 自定义领域
- `custom/*` - 用户添加的自定义领域

## 执行协议

### Phase 0: Context Anchoring (隐式执行) ⚓

在开始任何推演前，必须先建立 **User Profile (C_user)**。若用户未提供以下信息，在执行 Phase 1 前先反问用户，或根据对话历史进行 Zero-shot 侧写。

**用户画像三要素**：
- **Identity**: 用户是谁？（高管/创业者/学生/独立开发者/研究员/投资者）
- **Resources**: 手里有什么牌？（资金/技术栈/团队规模/核心数据/时间/人脉）
- **Constraints**: 绝对不能触碰的底线？（合规/成本上限/时间窗口/伦理边界/物理定律）

**用户画像推断 Zero-shot 模板**：
当用户未明确提供画像时，根据以下维度进行 Zero-shot 侧写：

```
Identity Signals:
- 用词风格（"团队"vs"我"、"融资"vs"收入"、"战略"vs"功能"）
- 问题复杂度（组织级/产品级/个人级）
- 时间视角（季度/年度/五年规划）

Resource Inference:
- 资金规模（暗示："试错成本"→充裕；"预算有限"→紧张）
- 团队规模（"跨部门"→大组织；"全栈"→小团队）
- 技术债务（"重构"vs"重写"vs"渐进式"）

Constraint Detection:
- 显性约束（用户直接声明的限制）
- 隐性约束（行业默认、物理规律、伦理边界）
- 软约束（可协商vs不可协商）
```

**不同用户类型的典型约束示例表**：

| 用户类型 | 典型 Resources | 常见 Constraints | 映射风险提示 |
|----------|----------------|------------------|--------------|
| 科技高管 | 预算/团队/品牌 | 监管/股东/政治 | 避免"颠覆式"建议，侧重"渐进式创新" |
| 创业者 | 时间/股权/愿景 | 现金流/生存/信任 | 避免"需要3年数据"建议，侧重"快速验证" |
| 独立开发者 | 技能/精力/热情 | 时间/资金/健康 | 避免"组建团队"建议，侧重"杠杆工具" |
| 产品经理 | 用户数据/团队 | OKR/资源/政治 | 避免"推翻重做"建议，侧重"A/B测试" |
| 投资者 | 资金/信息/人脉 | 流动性/合规/声誉 | 避免"亲自下场"建议，侧重"生态位判断" |
| 学生/研究者 | 时间/好奇心 | 经验/资源/权威 | 避免"需要资源"建议，侧重"认知框架" |

**Context Injection 规则与示例**：
1. **明确画像注入**：将 Constraints 硬编码到映射逻辑中
   ```
   输入: "如何扩大市场份额"
   用户: 上市公司高管
   注入: 映射时自动过滤"价格战""灰色地推"等违规策略
   ```

2. **模糊画像标注**：生成提案时标注适用场景
   ```
   【方案 A】⚠️ 适用性标注：需要 6 个月预算周期，适合资源充足组织
   【方案 B】✓ 适用性标注：可 2 周内验证，适合资源受限场景
   ```

3. **典型场景示例**：
   | 用户类型 | 典型输入 | 错误建议 ❌ | 正确建议 ✅ |
   |----------|----------|-------------|-------------|
   | 马斯克型 | "如何制造火箭" | "先小规模试错" | "从第一性原理拆解材料成本" |
   | 独立开发者 | "如何获得用户" | "建立销售团队" | "构建产品驱动增长机制" |
   | 初创公司 | "如何对抗巨头" | "正面竞争" | "寻找非对称优势点位" |
   | 传统行业 | "如何数字化转型" | "全面上云" | "从数据孤岛打通开始" |

4. **动态约束检测**：若用户反对某类建议，将其加入永久 Constraints 清单

---

### Phase 1: Category Extraction

将用户输入拆解为：
- **Objects (O_a)**: 核心实体
- **Morphisms (M_a)**: 实体间动态关系
- **Identity & Composition**: 维持现状的机制

### Phase 2: Domain Selection

基于 O_a 和 M_a 的拓扑结构，从 references/ 中选择逻辑距离远但结构相似的 Domain B。

**知识引用原则 (Grounding Mechanism)**：

1. **优先索引**：首先检索 `references/` 目录下的 V2 标准库。

2. **外部验证**：若选用库外领域，或库内信息不足，**必须**调用搜索工具验证该定理的真实性：
   - Who proposed it?（谁提出的？）
   - Which book/paper?（哪本书/论文？）
   - Is it widely accepted?（是否被广泛接受？）

3. **幻觉阻断**：**禁止**捏造定理名称。如果找不到适配定理，宁可报告：
   > "当前知识库中无适配定理，建议：①扩展领域知识 ②重构问题结构 ③使用 koan_break 模块"

4. **引文标注**：每个使用的定理必须标注来源：
   - 内置领域：`[来源: thermodynamics_v2.md / Theorem 7]`
   - 外部验证：`[来源: Smith (2019), Nature; 已验证]`

**领域选择策略（Entropy Injection）**：

1. **距离优先**：优先选择 Semantic Distance (语义距离) > 0.7 的领域
   - 语义距离计算：`distance = 1 - similarity(O_a, Domain_B_Objects)`
   - 高距离示例：金融问题 → 菌群生态 (距离≈0.85)
   - 低距离示例：商业问题 → 博弈论 (距离≈0.3) - 避免连续使用

2. **反重复**：检查对话历史，**禁止**连续两次使用同一个 Domain B
   - 追踪 `last_domain_b` 变量
   - 若用户再次询问相似问题，强制切换 Domain B

3. **意外性奖励**：如果能从以下非理科领域找到同构，优先权 +1：
   - `mythology` - 神话学/原型
   - `anthropology` - 人类学
   - `zhuangzi` - 庄子哲学
   - `religious_studies` - 宗教学
   - 其他人文领域

4. **熵值衰减**：若某领域在过去 10 次映射中被使用超过 3 次，其选择权重下降 50%

**V2领域结构**：
每个领域文件包含以下标准化结构：
- **Fundamentals**: 100基本基石（导语 + 18哲学观 + 22核心原则 + 28思维模型 + 22方法论 + 10避坑指南）
- **Core Objects**: 14个核心对象（含定义、本质、关联）
- **Core Morphisms**: 14个核心态射（含定义、涉及、动态）
- **Theorems**: 18个定理/模式（含内容、Applicable_Structure、Mapping_Hint、Case_Study）

### Phase 3: Functorial Mapping

建立映射函数 F: A -> B：
- F(O_a) = O_b
- F(M_a) = M_b
- 在 Domain B 中寻找已证实的定理

**关键：Mapping_Hint 的具体可操作性**

每个定理的 Mapping_Hint 遵循以下格式：
> "当 Domain A 面临[具体情境]时，识别[具体结构]，通过[具体方法]实现[具体目标]"

这是 V2 版本的核心质量特征。

### Phase 4: Pull-back & Synthesis

将 Domain B 的定理逆映射回 Domain A，生成具体可执行的方案。

### Phase 4.1: Commutativity Check (逻辑验算) ⚠️

**【强制执行】** 在生成【推演提案】前，必须验证映射的**逆运算合理性**：

#### 验证步骤

1. **正向路径验证**：A(问题) → B(定理) → A'(方案)
   - 确认 F(O_a) = O_b 的对象映射保持语义
   - 确认 F(M_a) = M_b 的关系映射保持动态

2. **逆向路径验证**：如果直接在 A 中执行该方案，是否违反 A 的基础公理？
   - **法律公理**：方案是否违反法律法规？
   - **物理公理**：方案是否违反物理定律？
   - **伦理公理**：方案是否违反伦理底线？
   - **经济公理**：方案是否违反经济规律？

3. **结构守恒检查**：Morphsim 是否被篡改？
   - 检查映射是否保持了原结构的本质
   - **非法映射示例**：
     - B 中的"捕食"映射回 A 变成了"恶性竞争"
     - 如果 A 是合作生态，则此映射非法，需丢弃
   - **合法映射示例**：
     - B 中的"共生"映射回 A 仍然是"互利共赢"
     - 结构一致，映射有效

#### 失败处理

若 Commutativity Check 失败：
1. 标记该映射路径为"结构不兼容"
2. 返回 Phase 2 重新选择 Domain B
3. 或触发 `koan_break` 模块进行问题重构

#### 检查清单

- [ ] 正向映射逻辑清晰
- [ ] 逆向验证无公理冲突
- [ ] 结构保持未被篡改
- [ ] 方案在 A 域中可执行

## 新增领域工作流程（v2.5 新增）

当用户请求"增加XX领域"时：

### Step 1: 需求理解
- 确认领域名称和核心关注点
- 识别该领域的关键学者/著作
- 确定 Structural_Primitives（5-10个核心概念）

### Step 2: 生成领域文件
按照 V2 标准格式创建领域文件：

```markdown
# Domain: [领域名称]
# Source: [关键学者《著作》, ...]
# Structural_Primitives: [核心概念列表]

## Fundamentals (100 基本基石)

### 导语
[100-150字，点破该领域最核心矛盾，冷峻简练宗师口吻]

### 一、哲学观 (18条)
[编号1-18，每条≤20字，有力简练，无常识]
...

### 二、核心原则 (22条)
[编号19-40，每条≤20字]
...

### 三、思维模型 (28条)
[编号41-68，每条≤20字]
...

### 四、关键方法论 (22条)
[编号69-90，每条≤20字]
...

### 五、避坑指南 (10条)
[编号91-100，每条≤20字]
...

## Core Objects (14个)
- **[Object 1]**: [定义]
  - *本质*: [一句话本质]
  - *关联*: [关联对象]
...

## Core Morphisms (14个)
- **[Morphism 1]**: [定义]
  - *涉及*: [涉及对象]
  - *动态*: [动态描述]
...

## Theorems / Patterns (18个)

### 1. [定理名称]
**内容**: [定理详细描述]

**Applicable_Structure**: [适用结构]

**Mapping_Hint**: [具体可操作："当Domain A...时，识别...，通过...实现..."]

**Case_Study**: [案例研究]
...

## Tags
[标签列表]
```

### Step 3: 质量标准验证
- [ ] 100条完整，每条≤20字
- [ ] 导语点破核心矛盾
- [ ] Objects共14个
- [ ] Morphisms共14个
- [ ] Theorems共18个
- [ ] 每个Theorem有完整4字段
- [ ] Mapping_Hint具体可操作

### Step 4: 保存到 custom/ 目录
- 保存为 `references/custom/[domain_name]_v2.md`
- 更新领域索引

## Refinement Loop（按需挂载高级模块）

基础四阶段流程完成后，根据情况自动或手动挂载以下模块：

| 模块 | 触发条件 | 功能 |
|------|----------|------|
| `yoneda_probe` | 信息不透明/模糊 | 通过关系网反推对象本质 |
| `natural_transformation` | 环境变化/策略失效/视角冲突 | 平滑迁移策略逻辑 |
| `monad_risk_container` | 【强制执行】输出前 | 风险识别与标注（法律/成本/信任） |
| `adjoint_balancer` | 【强制执行】输出前 | 可行性校验与优化 |
| `limits_colimits` | 多域交叉验证后 | 提取跨域元逻辑 |
| `kan_extension` | 需要扩展/泛化/尺度变换 | 最优扩展与泛化构造 |
| `koan_break` | 逻辑悖论/无解/所有Domain B映射失败 | 禅宗式打断，重构问题本身 |

### 触发映射速查

| 用户话术关键词 | 潜在困境 | 挂载模块 |
|----------------|----------|----------|
| "环境变了"、"风向调了" | 结构性失效 | Natural Transformation |
| "看不穿"、"查不到"、"黑盒" | 信息不对称 | Yoneda Probe |
| "合规吗"、"有风险吗"、"合法吗" | 风险识别需求 | Monad Risk Container |
| "太难了"、"没资源"、"怎么落地" | 复杂度超载 | Adjoint Balancer |
| "这几个领域有什么共同点？" | 缺乏通用底层 | Limits/Colimits |
| "如何扩展"、"能否泛化"、"放大/缩小" | 尺度变换需求 | Kan Extension |
| "圆的方"、"无解"、"走不通" | 逻辑悖论/范畴错误 | Koan Break |
| 遍历所有Domain B均无法映射 | 结构不匹配 | Koan Break |
| "增加XX领域"、"新增领域" | 扩展知识库 | 新增领域工作流 |

### 自动触发规则

**⚠️ 触发词边界说明**: 不同模块的触发词有明确的语义边界，避免冲突

- **Yoneda Probe**: 当 Domain A 中关键对象属性缺失 >30% 时
  - 关键词: "看不穿"、"查不到"、"黑盒"、"信息不足"

- **Natural Transformation**: 当用户输入包含**时间/状态变化**相关词汇时
  - 关键词: "环境变了"、"风向调了"、"策略失效"、"视角冲突"、"颗粒度"
  - **语义边界**: 处理的是"从 A 状态平滑过渡到 B 状态"，不是空间扩展

- **Monad Risk Container**: 每次生成【推演提案】前自动执行（在 Phase 4.1 之后，adjoint_balancer 之前）
  - 关键词: "合规吗"、"风险"、"合法吗"、"可以吗"
  - **作用**: 自动识别方案的 [🛡️ 法律熵] [💸 隐性债] [❤️ 信任能] 风险

- **Adjoint Balancer**: 每次生成【推演提案】前自动执行

- **Limits/Colimits**: 当使用 3+ 个 Domain B 或用户要求"交叉验证"时

- **Kan Extension**: 当用户输入包含**空间/规模复制**相关词汇时 ⭐
  - 关键词: "复制到XX市场"、"如何规模化"、"下沉市场"、"推广到全国"、"从1到N"、"泛化"
  - **语义边界**: 处理的是"把已验证的模式 S 复制到新的空间 C"，不是时间变化
  - **与 NT 的区别**: 
    - NT: "业务从 A 模式转型到 B 模式"（时间维度，替换）
    - Kan: "把 A 模式的成功复制到 B 市场"（空间维度，扩展）

- **Koan Break**: 当遍历所有 Domain B 均无法映射、或 Phase 4.1 Commutativity Check 连续失败 3 次、或用户问题存在逻辑悖论时

- **新增领域工作流**: 当用户输入包含"增加"、"新增"、"添加"、"扩展" + "领域"时（注意：这里的"扩展"指的是扩展知识库，不是业务扩展）

### 手动触发命令
- `/morphism-yoneda` - 强制启动米田探针
- `/morphism-pivot` - 强制启动策略演化分析 (Mode C)
- `/morphism-view` - 强制启动视角对齐 (Mode A)
- `/morphism-zoom` - 强制启动颗粒度缩放 (Mode B)
- `/morphism-risk` - 强制启动风险识别 (Monad Risk Container) ⭐ **v2.7 新增**
- `/morphism-monad` - 强制启动风险识别 (别名)
- `/morphism-balance` - 强制启动可行性校验
- `/morphism-limit` - 提取跨域共同核心
- `/morphism-colimit` - 整合互补洞察
- `/morphism-scale` - 强制启动尺度变换 (Kan Extension)
- `/morphism-koan` - 强制启动问题重构 (Koan Break)
- `/morphism-add-domain "领域名"` - 新增自定义领域

### 模块链式调用
支持多模块顺序执行，默认优先级：
`yoneda_probe` → `natural_transformation` → `limits_colimits` → `kan_extension` → `monad_risk_container` → `adjoint_balancer`

**逻辑解释**:
1. **Yoneda Probe**: 补全信息，明确问题结构
2. **Natural Transformation**: 处理视角对齐或环境变化
3. **Limits/Colimits**: 多域交叉验证，提取共同核心
4. **Kan Extension**: 将验证成功的局部方案扩展到全局
5. **Monad Risk Container**: 识别并标注法律/成本/信任风险 ⚠️ **v2.7 新增**
6. **Adjoint Balancer**: 最终可行性校验（强制执行）

## 输出格式

```markdown
### 【范畴骨架】- Domain A
| 类型 | 元素 | 说明 |
|------|------|------|
| Object | ... | ... |
| Morphism | ... | ... |

### 【异构域】- Domain B
**选择理由**: ...

### 【映射矩阵】
| Domain A | 映射关系 | Domain B | 同构性验证 |
|----------|----------|----------|------------|
| ... | ≅ | ... | ... |

### 【推演提案】
1. **方案标题**
   - **来源定理**: ...
   - **映射逻辑**: ...
   - **可执行方案**: ...
   - **预期效果**: ...
   - **验证方式**: ...

### 【可选模块输出】

#### 【Yoneda 拓扑画像】（若挂载 yoneda_probe）
通过关系网反推的核心对象定义...

#### 【策略演化路径】（若挂载 natural_transformation）
从旧逻辑到新逻辑的迁移桥梁...

#### 【跨域元逻辑】（若挂载 limits_colimits）
多 Domain B 的共同核心与互补整合...

#### 【风险容器检查】（强制执行 monad_risk_container）
识别并标注法律/成本/信任风险：
- [🛡️ 法律熵] 合规性检查...
- [💸 隐性债] 隐性成本识别...
- [❤️ 信任能] 信任消耗评估...

#### 【伴随解】（强制执行 adjoint_balancer）
成本-结构最优落地方标注...
```

## 约束

- 禁止泛泛类比，必须基于结构对齐
- Domain B 必须具备硬核知识底蕴
- 输出必须包含"不可直视"的洞察
- 新增领域必须符合 V2 质量标准（100基石 + 14O + 14M + 18T）

## 扩展

**自定义领域路径**: `references/custom/`

用户可添加自定义领域到 custom/ 目录，参照 V2 标准格式。

**新增领域快捷指令**：
- 直接说："增加易经思想领域"
- 直接说："morphism-mapper新增中医领域"
- 直接说："扩展领域：孙子兵法"

系统会自动：
1. 识别领域名称
2. 询问/推断关键学者和著作
3. 按照 V2 标准生成领域文件
4. 保存到 custom/ 目录

## 详细参考

- 领域知识库格式：references/_template.md
- 内置领域详情：references/*.md (V2版本，100基石+14O+14M+18T)
- V1备份：references/v1_backup/ (旧版本备份)
- 自定义领域：references/custom/ (用户添加)
- 使用示例：examples/few_shot_prompts.md
