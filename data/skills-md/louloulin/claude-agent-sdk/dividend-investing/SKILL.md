---
name: dividend-investing
description: 分析股息投资机会,评估股息安全性、增长潜力和收益率。当用户询问股息、分红、红利投资或股息率时使用。支持快速筛选、深度分析和组合优化。
version: 1.0.0
author: InvestIntel AI Team
tags:
  - dividend-investing
  - income-investing
  - yield-analysis
  - passive-income
---

# 股息投资分析

评估股息投资机会,平衡当前收益与未来增长。

## 核心指标

1. **股息率** - 年度股息/股价
2. **股息支付率** - 股息/盈利 (建议<70%)
3. **股息增长** - 连续增长年数
4. **自由现金流覆盖率** - FCF/股息 (建议>1.2)

## 分析步骤

1. 计算当前股息率
2. 评估支付安全性(支付率、FCF覆盖)
3. 检查增长历史(连续年数、CAGR)
4. 评估可持续性(行业、护城河)
5. 计算综合得分

## 评分标准 (0-100分)

- **收益率** (0-25分): >6%优秀,4-6%良好,2-4%一般
- **安全性** (0-35分): 支付率<50%优秀,<70%良好
- **增长性** (0-25分): 连续>10年优秀,>5年良好
- **可持续性** (0-15分): 护城河评分

## 风险提示

- ⚠️ 高股息率可能暗示经营困难
- ⚠️ 检查股息是否来自借款
- ⚠️ 周期行业股息不稳定

## 工具和详细文档

- 📁 [详细分析框架](./detailed-analysis.md)
- 📁 [股息筛选标准](./screening-criteria.md)
- 📁 [Rust实现参考](./reference-implementation.md)
- 🔧 [dividend_analyzer.py](./scripts/dividend_analyzer.py) - 股息分析工具
