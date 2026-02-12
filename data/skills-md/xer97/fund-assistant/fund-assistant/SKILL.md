---
name: fund-assistant
description: |
  基金投资助手。查询基金实时估值、净值、涨跌幅；搜索基金（按名称或代码）；
  管理投资组合（添加/删除持仓、记录交易、计算收益）；查看大盘指数、资金流向、北向资金；
  导入导出持仓数据。支持多用户数据隔离。
  触发词：基金、净值、估值、持仓、收益、定投、行情、北向资金、沪深300
---

# 基金投资助手

## 脚本命令

### 基金 API（scripts/fund_api.py）

```bash
python scripts/fund_api.py query 001618,000001   # 查询实时估值
python scripts/fund_api.py search 白酒           # 搜索基金
python scripts/fund_api.py detail 001618         # 基金详情
python scripts/fund_api.py history 001618 y      # 历史净值 (y/3y/6y/n/3n/5n)
python scripts/fund_api.py position 001618       # 持仓明细
python scripts/fund_api.py manager 001618        # 基金经理
python scripts/fund_api.py index                 # 大盘指数
python scripts/fund_api.py flow                  # 资金流向
python scripts/fund_api.py north                 # 北向资金
```

### 持仓管理（scripts/portfolio.py）

```bash
python scripts/portfolio.py init                 # 初始化数据目录
python scripts/portfolio.py list                 # 查看持仓
python scripts/portfolio.py add 001618 1000 1.5  # 添加持仓（代码 份额 成本）
python scripts/portfolio.py update 001618 shares=1500  # 更新持仓
python scripts/portfolio.py remove 001618        # 删除持仓
python scripts/portfolio.py user 老婆            # 切换用户
python scripts/portfolio.py users                # 列出所有用户
python scripts/portfolio.py export portfolio.json  # 导出持仓
python scripts/portfolio.py import portfolio.json  # 导入持仓
```

## 数据存储

位置：`.fund-assistant/users/{用户名}/portfolio.json`（项目本地目录）

```json
{"funds": [{"code": "001618", "name": "天弘中证食品饮料", "shares": 1000, "cost": 1.5}]}
```

详细结构：[references/storage.md](references/storage.md)

## 收益计算

```javascript
// 当日预估收益（今天赚/亏多少）
dailyGains = (gsz - nav) * shares;
dailyGainsRate = gszzl;  // 直接用API返回的涨跌幅

// 持仓总收益（从买入到现在总共赚/亏多少）
costGains = (gsz - cost) * shares;
costGainsRate = ((gsz - cost) / cost) * 100;
```

**重要区分：**
- **当日收益** = (估算净值 - 昨日净值) × 份额 → 今天赚了多少
- **持仓收益** = (估算净值 - 成本价) × 份额 → 总共赚了多少

**字段说明：**
- `nav`: 昨日净值（已公布）
- `gsz`: 估算净值（盘中实时）
- `gszzl`: 估算涨跌幅（%）
- `gztime`: 估值更新时间
- `cost`: 用户买入成本价

## 操作流程

| 用户意图 | 执行步骤 |
|----------|----------|
| 查询基金 | `fund_api.py query {代码}` → 解析 JSON 输出 |
| 添加持仓 | `portfolio.py add {代码} {份额} {成本}` |
| 查看持仓收益 | `portfolio.py list` → `fund_api.py query {代码列表}` → 计算收益 |
| 切换用户 | `portfolio.py user {用户名}` |
| 查看行情 | `fund_api.py index` |

## API 响应字段

详见 [references/api.md](references/api.md)

## 注意事项

1. 首次使用需运行 `portfolio.py init` 初始化数据目录
2. 实时估值使用天天基金接口 `http://fundgz.1234567.com.cn/js/{code}.js`
3. 交易时段：9:30-11:30, 13:00-15:00（排除节假日）
4. QDII基金估值可能延迟，部分新发基金无估值数据
