---
name: mcp-data-gateway
description: 统一查询股票、加密货币等金融数据。支持Yahoo Finance、Alpha Vantage、Tushare、Binance等多个数据源。当用户需要市场数据、行情、财务数据时使用。
version: 1.0.0
author: InvestIntel AI Team
tags:
  - market-data
  - data-gateway
  - financial-data
  - crypto-data
  - api-integration
---

# MCP数据网关

统一访问多个金融数据源,提供一致的查询接口。

## 支持的数据源

| 数据源 | 类型 | 覆盖范围 |
|--------|------|----------|
| **Yahoo Finance** | 股票、ETF、指数 | 全球市场 |
| **Alpha Vantage** | 股票、外汇、加密货币 | 美股为主 |
| **Tushare** | A股、港股、中概股 | 中国市场 |
| **Binance** | 加密货币 | 主要币种 |

## 查询功能

### 实时行情
- 股价、涨跌幅、成交量
- 实时报价、日内高低
- 52周高低

### 历史数据
- 历史K线(日/周/月)
- 历史分红、拆股
- 财务报表数据

### 财务数据
- 收入、盈利、ROE
- 资产负债表
- 现金流量表

## 使用方式

优先使用默认数据源,自动失败转移:

```rust
// 获取报价
let quote = gateway.get_quote("AAPL").await?;

// 获取财务数据
let fundamental = gateway.get_fundamental("AAPL").await?;

// 获取历史K线
let history = gateway.get_history("AAPL", Period::Daily, 1).await?;
```

## 数据源选择策略

1. 美股: Yahoo Finance → Alpha Vantage
2. A股: Tushare → Yahoo Finance
3. 加密货币: Binance → Yahoo Finance

## 工具和详细文档

- 📁 [API接口文档](./api-reference.md)
- 📁 [数据源配置](./data-sources.md)
- 📁 [Rust实现参考](./reference-implementation.md)
- 🔧 [data_gateway.py](./scripts/data_gateway.py) - 命令行工具
