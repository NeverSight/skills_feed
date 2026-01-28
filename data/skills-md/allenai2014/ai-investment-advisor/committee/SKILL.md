---
name: committee
description: 多模型投资委员会。当用户说"开会"、"投资委员会"、"多模型分析"、"让三个模型一起看看"时使用此skill。
user-invocable: true
---

# /committee - 投资委员会（数据驱动版）

让 Claude、Codex、Gemini 基于同一份客观数据独立分析，必要时交叉验证，最终提取可执行共识。

## 使用方式

- `/committee` - 召开投资委员会
- `/committee 红利ETF该怎么操作` - 针对特定问题召开
- `/committee consensus` - 汇总已有的三个模型观点

## 执行步骤（建议增强版）

### 0. 选择模式

- **简版**：一轮独立分析 → 汇总共识
- **增强版**：R1 独立分析 → R2 交叉验证 → 汇总共识
- 默认：询问用户；未指定时使用增强版

### 第一步：准备统一输入数据

1. **获取市场数据**
```bash
cd "股市信息" && python3 scripts/fetch_market_data.py
```
> 脚本已支持 `technicals`（MA/RSI/MACD/区间位置）。如太慢可在 `MODULES` 里关闭。

2. **读取上下文**
读取 `股市信息/Config/Context.md`，并补充 `Profile.md`、`Principles.md`、`Insight.md` 的风险偏好与约束

3. **确定今日决策问题**
询问用户今天想让委员会讨论什么问题

4. **生成输入文件**
将以上内容整合，保存到 `股市信息/Committee/Input/YYYY-MM-DD-Input.md`
- 使用模板：`Committee/Templates/prompt_template.md`
- **必须包含“数据质量清单”**，明确缺失字段（估值/资金/技术等）
- `fetch_market_data.py` 输出中 `holdings`/`watchlist` 的 `technicals` 与成交数据必须纳入

### 第二步：Round1 独立分析

基于输入数据，按 `Committee/Templates/opinion_template.md` 输出：
1. 市场整体判断
2. 持仓信号矩阵与操作建议（每个标的建议必须引用 >=2 个客观数据字段）
3. 风险预警
4. 回答决策问题
5. 置信度自评

保存到：
- `Committee/Opinions/Claude.md`
- `Committee/Opinions/Codex.md`
- `Committee/Opinions/Gemini.md`

### 第三步：交叉验证（增强版）

将 R1 观点互相提供给其他模型，要求：
- 只基于相同数据指出遗漏/误读/过度推断
- 允许调整：建议、信心、风险预警
- 输出 R2 修正表

保存到：
- `Committee/Opinions/Claude-R2.md`
- `Committee/Opinions/Codex-R2.md`
- `Committee/Opinions/Gemini-R2.md`

### 第四步：汇总共识

当用户表示观点都已收集完成后：

1. **读取观点文件**
优先使用 R2；没有则使用 R1

2. **逐标的对比**
- 3/3 一致 → 强共识
- 2/3 一致 → 弱共识
- 各不相同 → 分歧

3. **权重与风控规则**
- 权重 = 置信度 × 数据完整度
- 未引用客观数据的观点降权
- 任一模型高风险预警必须纳入汇总

4. **生成共识报告**
按 `Templates/consensus_template.md` 输出并保存到 `Committee/Sessions/YYYY-MM-DD.md`

### 第五步：记录待追踪建议

- 将强共识建议记录到 `股市信息/Config/Insight.md` 的“采纳记录”
- 设置状态为“待采纳”，后续用 `/trade` 验证

---

## 输出格式要求

- 统一使用 `Committee/Templates/opinion_template.md`
- **字段缺失必须标注“缺失”**，禁止自行补全
- 关键建议必须写“关键数据依据”

---

## 共识提取规则（补充）

- 若关键数据理解不一致（如 RSI/趋势读法不同），进入“分歧区”并标明数据争议
- 若数据缺口较大，原强共识降级为弱共识
- 若出现“风险红线”（如 RSI>75 且价格远高于 MA60），须提示谨慎并降低信心

---

## 模板文件位置

- 输入提示词模板：`Committee/Templates/prompt_template.md`
- 观点输出模板：`Committee/Templates/opinion_template.md`
- 共识汇总模板：`Committee/Templates/consensus_template.md`
