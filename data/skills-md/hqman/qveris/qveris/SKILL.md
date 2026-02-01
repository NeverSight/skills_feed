---
name: qveris
description: Search and execute dynamic tools via QVeris API. Use when needing to find and call external APIs/tools dynamically (weather, search, data retrieval, stock trading analysis, etc.). Requires QVERIS_API_KEY environment variable.
triggers:
  - pattern: "股票|stock|股价|股市"
    description: "Detect stock-related queries"
  - pattern: "交易|trading|买卖|成交"
    description: "Detect trading-related queries"
  - pattern: "分析|analysis|数据|指标|技术分析|基本面"
    description: "Detect analysis-related queries"
  - pattern: "市值|涨跌|收盘|开盘|市盈率|pe|pb"
    description: "Detect stock indicator queries"
auto_invoke: true
examples:
  - "Check Tesla stock price"
  - "Analyze Apple's financial data"
  - "Get Bitcoin real-time price"
  - "Show me current weather in Tokyo"
---

# QVeris Tool Search & Execution

QVeris provides dynamic tool discovery and execution - search for tools by capability, then execute them with parameters.

## Setup

Requires environment variable:
- `QVERIS_API_KEY` - Get from https://qveris.ai

## Quick Start

### Search for tools
```bash
uv run scripts/qveris_tool.py search "weather forecast API"
```

### Execute a tool
```bash
uv run scripts/qveris_tool.py execute openweathermap_current_weather --search-id <id> --params '{"city": "London", "units": "metric"}'
```

## Script Usage

```
scripts/qveris_tool.py <command> [options]

Commands:
  search <query>     Search for tools matching a capability description
  execute <tool_id>  Execute a specific tool with parameters

Options:
  --limit N          Max results for search (default: 5)
  --search-id ID     Search ID from previous search (required for execute)
  --params JSON      Tool parameters as JSON string
  --max-size N       Max response size in bytes (default: 20480)
  --json             Output raw JSON instead of formatted display
```

## Workflow

1. **Search**: Describe the capability needed (not specific parameters)
   - Good: "weather forecast API"
   - Bad: "get weather for London"

2. **Select**: Review tools by `success_rate` and `avg_execution_time`

3. **Execute**: Call tool with `tool_id`, `search_id`, and `parameters`

## Example Session

```bash
# Find weather tools
uv run scripts/qveris_tool.py search "current weather data"

# Execute with returned tool_id and search_id
uv run scripts/qveris_tool.py execute openweathermap_current_weather \
  --search-id abc123 \
  --params '{"city": "Tokyo", "units": "metric"}'
```

## Use Cases

- **Weather Data**: Get current weather, forecasts for any location
- **Stock Market**: Query stock prices, historical data, earnings calendars
- **Search**: Web search, news retrieval
- **Data APIs**: Currency exchange, geolocation, translations
- **And more**: QVeris aggregates thousands of API tools
