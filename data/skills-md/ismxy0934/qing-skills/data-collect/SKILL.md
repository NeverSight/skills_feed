---
name: data-collect
description: 收集股票历史K线、实时行情、筹码分布数据，支持A股/港股/美股/ETF。当用户提及股票代码、获取行情数据、K线、实时报价、筹码分布、或询问茅台/AAPL等股票时使用
---

# 股票数据收集

收集指定股票的完整数据：历史K线、实时行情、筹码分布（仅A股）。

## 执行命令

```bash
python scripts/collect_stock_data.py <股票代码> [--days N] [--provider akshare|tushare] --date YYYY-MM-DD

# 示例
python scripts/collect_stock_data.py 600519 --date 2025-01-01                    # A股，60天
python scripts/collect_stock_data.py 000001 --days 90 --date 2025-01-01          # 指定90天
python scripts/collect_stock_data.py AAPL --days 30 --date 2025-01-01            # 美股30天
python scripts/collect_stock_data.py 600519 --provider tushare --date 2025-01-01 # 用户选择 tushare
```

**参数说明**：
- `--days`：获取天数（默认60天）
- `--provider`：数据源（默认 `akshare`；仅用户选择时使用 `tushare`）
- `--date`：保存文件的日期标识（必填，用于保证后续分析与决策可复现；不影响数据时间范围）

当 `--provider tushare` 时：
- 当前仅支持 **A股 K线**
- 需要设置环境变量 `TUSHARE_TOKEN`
- `realtime` 与 `chip` 字段会返回 `null`

## 市场支持

自动识别市场类型：
- **A股**：6位数字（600519, 000001）
- **港股**：5位数字（00700, 09988）
- **美股**：字母代码（AAPL, MSFT）
- **ETF**：51/52/56/58开头（512880）

详见 [markets.md](references/markets.md)

## 输出结构

```
output/<股票代码>/<日期>/data.json
```

输出包含：
- `klines`：历史K线（日期、开高低收、成交量额、涨跌幅）
- `realtime`：实时行情（价格、量比、换手率、市盈率等）
- `chip`：筹码分布（仅A股，获利比例、筹码集中度等）

完整字段说明见 [fields.md](references/fields.md)

## 失败处理

- 股票代码无效/市场不支持：检查 `markets.md` 的识别规则
- K 线数据拉取失败：脚本会自动切换数据源；如果仍失败，可能是网络/源站限制，稍后重试
- 实时行情/筹码失败：会输出警告但不阻断（K 线仍会保存）

## 错误处理

**A股数据源**：自动切换东方财富→新浪→腾讯，所有源失败才报错

**可选数据**：实时行情和筹码数据获取失败不影响K线输出（会警告）

**防封禁**：脚本自动在请求间随机休眠2-5秒

## 依赖安装

```bash
pip install akshare tushare pandas
```
