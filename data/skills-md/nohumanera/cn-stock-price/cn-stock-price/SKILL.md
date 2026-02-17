---
name: cn-stock-price
description: check stock price
---

# 股票价格查询工具

一个简单的中国A股实时股票价格查询脚本。

## 功能

- 查询实时股票价格
- 支持单只或多只股票同时查询
- 提供默认股票列表（主要指数+个股）

## Example

```bash
# 查询默认股票列表
python ./scripts/check.py
# 查询指定股票（支持多只）
python ./scripts/check.py sh600519
python ./scripts/check.py sh600036 sz002352
```

## Dependencies

- requests
