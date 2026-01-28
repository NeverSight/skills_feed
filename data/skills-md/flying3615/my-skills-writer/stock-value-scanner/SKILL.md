---
name: stock-value-scanner
description: 进行股票异动，价值投资分析与趋势查询
---

# Stock Value Scanner Skill


## Description
这是一个综合性的美股分析工具。它集成了**价值投资评分**（基于 Yahoo Finance 的 P/E, ROE 等指标）、**趋势技术分析**（历史回撤、均线判断）以及**市场异动扫描**（涨跌幅榜、热门交易）。无论是寻找被低估的优质股，还是追踪市场的热点趋势，此 Skill 都能提供数据支持。

## Features
- **实时估值分析**：自动获取 P/B, P/E, PEG 等核心估值指标 (Yahoo Finance)。
- **股价趋势分析**：查看收盘价、历史高点回撤、52周范围及长期均线趋势。
- **市场异动扫描**：实时查看美股涨幅榜、跌幅榜及热门交易股。
- **质量体检**：自动检测 ROE, 净利率等质量指标，排除“垃圾股”。
- **智能打分**：基于巴菲特价值投资逻辑生成 0-6 分的综合评分。

## Usage

**前置要求**:
- 必须安装 Python 库 `yfinance`: `pip install yfinance`
- **无需** 任何 API Key。

### Example Prompts
- "分析一下 MARA 的投资价值"
- "看看 AAPL 最近的走势怎么样"
- "查询 NVDA 离历史高点还有多远"
- "看看今天美股涨幅榜"
- "最近哪些股票交易最活跃"

## Execution

### 1. 价值分析 & 评分
```bash
python3 .gemini/skills/stock-value-scanner/scripts/scanner.py [SYMBOL]
```
或批量扫描预设列表：
```bash
python3 .gemini/skills/stock-value-scanner/scripts/scanner.py --scan
```

### 2. 股价趋势查询
```bash
python3 .gemini/skills/stock-value-scanner/scripts/stock_price.py [SYMBOL]
```

### 3. 市场异动查询
```bash
python3 .gemini/skills/stock-value-scanner/scripts/market_movers.py --type [gainers|losers|active]
```

## Tips for the Agent
- **场景区分**:
  - 用户问 **“值不值得买”、“基本面”、“估值”** -> 使用 `scanner.py`。
  - 用户问 **“趋势”、“走势”、“历史高点”、“回撤”、“均线”** -> 使用 `stock_price.py`。
  - 用户问 **“涨幅榜”、“跌幅榜”、“热门”、“异动”、“大盘”** -> 使用 `market_movers.py`。
- 遇到 `ImportError: No module named 'yfinance'` 错误时，请指导用户运行 `pip install yfinance`。
- 运行结果是文本报告，直接展示给用户即可，无需过度解释。
