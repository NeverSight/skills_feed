---
name: kelly-position
description: 使用Kelly公式科学计算投资仓位大小。当用户询问仓位、资金分配、position sizing或Kelly公式时使用。支持完整Kelly、分数Kelly和组合优化。
version: 1.0.0
author: InvestIntel AI Team
tags:
  - position-sizing
  - kelly-criterion
  - risk-management
  - portfolio-optimization
---

# Kelly仓位计算

使用Kelly公式计算最优投资仓位,平衡长期增长与风险控制。

## 核心公式

**完整Kelly**: `f* = (bp - q) / b`
- `b` = 盈亏比 (平均盈利/平均亏损)
- `p` = 胜率, `q` = 败率 (1-p)
- `f*` = 最优仓位比例

**简化Kelly**: `f = μ / σ²` (基于期望收益μ和方差σ²)

## 实践建议

1. **分数Kelly**: 使用1/4或1/2 Kelly降低波动
2. **仓位上限**: 单只股票≤25%(Munger原则)
3. **最小仓位**: Kelly<2%时不建仓
4. **组合管理**: 多只股票时需归一化总仓位

## 使用方式

当用户提供胜率和盈亏比时,计算完整Kelly并应用1/4分数:

```rust
let kelly = (b * p - (1.0 - p)) / b;
let safe_kelly = (kelly * 0.25).min(0.25).max(0.0);
```

## 输出内容

- Kelly最优仓位
- 推荐仓位(1/4或1/2 Kelly)
- 风险等级评估
- 仓位限制说明
- 建议理由

## 工具和详细文档

- 📁 [详细计算方法](./detailed-calculation.md)
- 📁 [Rust实现参考](./reference-implementation.md)
- 🔧 [kelly_calculator.py](./scripts/kelly_calculator.py) - 命令行工具
