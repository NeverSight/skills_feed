---
name: technical-analysis
description: 对股票K线数据进行技术分析，计算MA/MACD/RSI等指标，判断趋势和买卖信号。触发场景：(1) "分析一下茅台的技术面" (2) "看看这只股票能不能买" (3) "技术分析 600519" (4) 需要判断股票趋势、买卖点时使用。需要先用 data-collect 获取数据
---

# 技术分析

基于 K 线数据进行完整技术分析，输出趋势判断和买卖信号。

## 执行

```bash
python scripts/analyze.py <股票代码> --date YYYY-MM-DD

# 示例
python scripts/analyze.py 600519 --date 2025-01-01
```

## 输入（必需）

需要先运行 `data-collect`，并确保 `--date` 一致。

```
output/<股票代码>/<日期>/data.json
```

## 数据流

```
读取: output/<股票代码>/<日期>/data.json
输出: output/<股票代码>/<日期>/analysis.json
```

## 输出（稳定字段）

- `trend`：趋势状态、强度、是否偏多
- `bias`：乖离率与安全性判断
- `macd`：MACD 状态与信号
- `volume`：量能状态
- `signal`：动作建议、评分、理由与风险

## 核心交易理念

1. **严进策略** - 乖离率 > 5% 坚决不买
2. **趋势交易** - MA5 > MA10 > MA20 多头排列
3. **买点偏好** - 缩量回踩 MA5/MA10 支撑

## 输出

```json
{
  "trend": {"status": "多头排列", "strength": 75, "is_bullish": true},
  "bias": {"ma5": 0.30, "status": "安全"},
  "macd": {"status": "GOLDEN_CROSS", "signal": "金叉，趋势向上"},
  "volume": {"status": "SHRINK_VOLUME_DOWN", "trend": "缩量回调"},
  "signal": {"action": "买入", "score": 72, "reasons": [...], "risks": [...]}
}
```

## 评分标准

| 分数 | 信号 |
|------|------|
| 75+ | 强烈买入 |
| 60-74 | 买入 |
| 45-59 | 持有 |
| 30-44 | 观望 |
| <30 | 卖出 |

详细指标说明见 [references/indicators.md](references/indicators.md)

## 失败处理

- 找不到 `data.json`：先运行 `data-collect`（同一个 `--date`）
- `data.json` 字段缺失/为空：检查 `data-collect` 是否拉取成功；必要时扩大 `--days`
- 指标无法计算（样本不足）：尝试提高 `data-collect --days`（例如 120/240）
