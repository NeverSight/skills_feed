---
name: misttrack-skills
description: 使用 MistTrack OpenAPI 进行加密货币地址风险分析、AML 合规检测和交易追踪。MistTrack 是由 SlowMist 开发的反洗钱追踪工具，支持 BTC、ETH、TRX、BNB 等主流链上地址与交易的风险评分、标签查询、交易调查等功能。
---

# MistTrack OpenAPI 技能

## 概述

MistTrack 是由 [SlowMist](https://www.slowmist.com/en/) 开发的加密货币反洗钱（AML）追踪工具，专注于打击加密货币洗钱活动。

- 收录超过 **4 亿个**地址（涵盖主要交易平台的各类钱包）
- 提供 **50 万条**威胁情报地址
- 标记超过 **9000 万个**与恶意活动相关的地址

## API 基本信息

### Base URL
```
https://openapi.misttrack.io
```

### 认证方式
所有请求均需在 Query Parameter 中传入 `api_key`（GET 请求）或 Request Body（POST 请求）。

### 通用响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | Boolean | 请求是否成功 |
| `msg` | String | 失败时的错误信息 |
| `data` | Dictionary | 响应数据 |

### 速率限制（Rate Limits）

| 套餐 | 速率 | 每日限额 |
|------|------|----------|
| Standard | 1 次/秒/key | 10,000 次/天/key |
| Compliance | 5 次/秒/key | 50,000 次/天/key |
| Enterprise | 无限制 | 无限制 |

超出限制时返回：
```json
{"success": false, "msg": "ExceededDailyRateLimit", "retry_after": 12345}
{"success": false, "msg": "ExceededRateLimit", "retry_after": 1}
```

---

## 常见错误码

| HTTP 状态码 | 原因 | 解决方案 |
|------------|------|----------|
| 402 | MistTrack 订阅已过期 | 登录并续订 |
| 429 | 请求速度过快 | 参考速率限制指南控制请求频率 |
| 500 | 服务端错误 | 稍后重试 |

### 错误消息（`msg` 字段）

| `msg` 值 | 说明 |
|----------|------|
| `ExceededRateLimit` | 超过每秒速率限制 |
| `ExceededDailyRateLimit` | 超过每日速率限制 |
| `InvalidApiKey` | API Key 无效 |
| `UnsupportedToken` | 不支持的代币 |
| `InvalidAddress` | 无效地址 |
| `PageNotFound` | 页面未找到 |
| `ExpiredPlan` | 套餐已过期 |
| `TaskNotFound` | 任务不存在（需先创建） |
| `UnsupportedAddressType` | 不支持的地址类型（如热钱包地址） |

---

## 多链支持

MistTrack 支持以下区块链及代币：

- **Bitcoin**: BTC
- **Ethereum**: ETH, USDT-ERC20, USDC-ERC20, WETH-ERC20, PEPE-ERC20, SHIB-ERC20, DAI-ERC20 等
- **TRON**: TRX, USDT-TRC20, USDC-TRC20, USDD-TRC20
- **BNB Smart Chain**: BNB, USDT-BEP20, BUSD-BEP20, ETH-BEP20 等
- **Polygon**: POL-Polygon, USDT-Polygon, USDC-Polygon, WETH-Polygon 等
- **Arbitrum One**: ETH-Arbitrum, USDT-Arbitrum, USDC-Arbitrum 等
- **OP Mainnet**: ETH-Optimism, USDT-Optimism, USDC-Optimism 等
- **Base**: ETH-Base, USDC-Base, USDT-Base 等
- **Avalanche**: AVAX-Avalanche, USDT-Avalanche, USDC-Avalanche 等
- **zkSync Era**: ETH-zkSync, ZK-zkSync, USDT-zkSync, USDC-zkSync
- **Toncoin**: TON, USDT-TON
- **Solana**: SOL, USDT-Solana, USDC-Solana, Bonk-Solana 等
- **Litecoin**: LTC
- **Dogecoin**: DOGE
- **Bitcoin Cash**: BCH
- **Merlin Chain**: BTC-Merlin
- **HashKey Chain**: HSK
- **Sui**: SUI, wUSDT-SUI, USDC-SUI
- **IoTeX**: IOTX

完整代币列表请调用 `/v1/status` 接口获取。

---

## API 端点列表

### 1. 获取 API 状态 (`v1/status`)

**功能**：返回 API 状态及支持的代币列表。

```
GET https://openapi.misttrack.io/v1/status
```

**请求参数**：无

**响应示例**：
```json
{
  "success": true,
  "msg": "",
  "data": {
    "support_api": ["status", "address_labels", "risk_score", "transactions_investigation", "address_overview", "address_action", "address_trace"],
    "support_coin": ["ETH", "USDT-ERC20", "BTC", "TRX", "USDT-TRC20", "..."]
  }
}
```

---

### 2. 获取地址标签 (`v1/address_labels`)

**功能**：返回指定地址的标签列表，包括实体名称、地址类型、链上标签、链下标签等。

```
GET https://openapi.misttrack.io/v1/address_labels?coin=ETH&address={address}&api_key={api_key}
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coin` | string | ✅ | 查询的代币（如 ETH、BTC、TRX） |
| `address` | string | ✅ | 查询的地址 |
| `api_key` | string | ✅ | API 密钥 |

**响应字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `label_list` | list | 地址标签列表，包含实体名称（如 Coinbase、Binance）、地址类型（deposit/hot/cold wallet）、链上标签（ENS、MEV Bots、DeFi Whales）、链下标签（MetaMask Wallet User、Twitter handle） |
| `label_type` | string | 地址类型分类：`exchange`（中心化交易所、支付平台）/ `defi`（DeFi 项目、跨链桥）/ `mixer`（混币器或无 KYC 即时兑换）/ `nft`（NFT 市场）/ 空字符串（未分类） |

**响应示例**：
```json
{
  "success": true,
  "msg": "",
  "data": {
    "label_list": ["Binance", "hot"],
    "label_type": "exchange"
  }
}
```

---

### 3. 获取地址概览 (`v1/address_overview`)

**功能**：返回指定地址的余额及统计数据。

```
GET https://openapi.misttrack.io/v1/address_overview?coin=ETH&address={address}&api_key={api_key}
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coin` | string | ✅ | 查询的代币 |
| `address` | string | ✅ | 查询的地址 |
| `api_key` | string | ✅ | API 密钥 |

**响应字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `balance` | float(4) | 地址余额 |
| `txs_count` | int | 总交易数 |
| `first_seen` | int | 首次交易时间（Unix 时间戳） |
| `last_seen` | int | 最近交易时间（Unix 时间戳） |
| `total_received` | float(4) | 总接收金额 |
| `total_spent` | float(4) | 总支出金额 |
| `received_txs_count` | int | 接收交易总数 |
| `spent_txs_count` | int | 发出交易总数 |

**响应示例**：
```json
{
  "success": true,
  "msg": "",
  "data": {
    "balance": 49.8305,
    "txs_count": 1231,
    "first_seen": 1441800674,
    "last_seen": 1670971955,
    "total_received": 916204.8697,
    "total_spent": 916151.0499,
    "received_txs_count": 1018,
    "spent_txs_count": 213
  }
}
```

---

### 4. 获取风险评分 - 同步模式 (`v2/risk_score`)

**功能**：返回指定地址或交易哈希的 AML 风险评分及风险详情（KYT/KYA）。

> ⚠️ **注意**：风险评分基于地址的所有相关交易计算，因此同一地址下所有代币会获得相同的评分。

```
GET https://openapi.misttrack.io/v2/risk_score?coin=ETH&address={address}&api_key={api_key}
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coin` | string | ✅ | 查询的代币 |
| `address` | string | 与 txid 二选一 | 查询的地址 |
| `txid` | string | 与 address 二选一 | 查询的交易哈希 |
| `api_key` | string | ✅ | API 密钥 |

> `address` 和 `txid` 只传其中一个，不能同时传。

**响应字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `score` | int | 风险评分，范围 3~100 |
| `hacking_event` | string | 相关安全事件名称 |
| `detail_list` | list | 风险描述列表 |
| `risk_level` | string | 风险级别：Low / Moderate / High / Severe |
| `risk_detail` | list | 风险评分计算详情 |
| `risk_report_url` | string | MistTrack AML 风险报告 PDF 链接 |

**`risk_detail` 子字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `entity` | string | 风险实体名称（如 garantex.io） |
| `risk_type` | string | 风险类型：`sanctioned_entity` / `illicit_activity` / `mixer` / `gambling` / `risk_exchange` / `bridge` |
| `exposure_type` | string | 暴露类型：`direct`（直接） / `indirect`（间接） |
| `hop_num` | int | 到风险实体的跳数（≥1） |
| `volume` | float | 与风险实体的交易总额（USD） |
| `percent` | float | 占总交易额的百分比 |

#### 风险描述（`detail_list` 可能的值）

| 描述 | 含义 |
|------|------|
| Malicious Address | 直接参与恶意事件的地址（如 DeFi 攻击者、黑客、被制裁地址） |
| Suspected Malicious Address | 与恶意事件相关的地址 |
| High-risk Tag Address | 高风险实体地址（如混币器、某些嵌套交易所） |
| Medium-risk Tag Address | 中风险实体地址（如赌博平台、无 KYC 交易所） |
| Mixer | 混币器地址（如 Tornado Cash） |
| Sanctioned Entity | 被制裁实体地址（如 garantex） |
| Risk Exchange | 无 KYC 要求的交易所 |
| Gambling | 赌博平台地址 |
| Involved Theft Activity | 参与盗窃事件的地址 |
| Involved Ransom Activity | 参与勒索事件的地址 |
| Involved Phishing Activity | 参与钓鱼事件的地址 |
| Involved Illicit Activity | 参与非法活动的地址（如洗钱） |
| Interact With Malicious Address | 与恶意地址有交互 |
| Interact With Suspected Malicious Address | 与疑似恶意地址有交互 |
| Interact With High-risk Tag Address | 与高风险地址有交互 |
| Interact With Medium-risk Tag Addresses | 与中风险地址有交互 |

#### 风险级别指南

| 风险级别 | 分数范围 | 建议操作 |
|----------|----------|----------|
| **Severe** | 91~100 | 禁止提现和交易，立即上报地址 |
| **High** | 71~90 | 高度监控，通过 MistTrack AML 平台或 OpenAPI 进行交易分析 |
| **Moderate** | 31~70 | 需要适度监管 |
| **Low** | 0~30 | 最低监管要求 |

**响应示例**：
```json
{
  "success": true,
  "msg": "",
  "data": {
    "score": 35,
    "hacking_event": "",
    "detail_list": ["Involved Illicit Activity", "Interact With High-risk Tag Address"],
    "risk_level": "Moderate",
    "risk_detail": [
      {
        "entity": "huionepay",
        "risk_type": "sanctioned_entity",
        "volume": 6700352.55,
        "hop_num": 2,
        "exposure_type": "indirect",
        "percent": 3.419
      }
    ],
    "risk_report_url": "https://light.misttrack.io/riskReport/0x..."
  }
}
```

---

### 5. 获取风险评分 - 异步模式 (`v2/risk_score_create_task` & `v2/risk_score_query_task`)

**功能**：以异步方式获取地址或交易的风险评分（适用于大批量查询场景）。

#### 5.1 创建任务 (`v2/risk_score_create_task`)

```
POST https://openapi.misttrack.io/v2/risk_score_create_task
Content-Type: application/json
```

**请求 Body**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coin` | string | ✅ | 查询的代币 |
| `address` | string | 与 txid 二选一 | 查询的地址 |
| `txid` | string | 与 address 二选一 | 查询的交易哈希 |
| `api_key` | string | ✅ | API 密钥 |

**cURL 示例**：
```bash
curl --location 'https://openapi.misttrack.io/v2/risk_score_create_task' \
  --header 'Content-Type: application/json' \
  --data '{
    "address": "TNXoiAJ3dct8Fjg4M9fkLFh9S2v9TXc32G",
    "coin": "TRX",
    "api_key": "YourApiKey"
  }'
```

**响应字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `has_result` | bool | 是否已有缓存结果 |
| `scanned_ts` | int | 任务结果生成时间戳 |

- **Cache Miss**（`has_result: false`）：等待 1-10 秒后调用 `v2/risk_score_query_task`
- **Cache Hit**（`has_result: true`）：立即调用 `v2/risk_score_query_task`

#### 5.2 查询任务结果 (`v2/risk_score_query_task`)

> ⚠️ 此接口**无速率限制**。

```
GET https://openapi.misttrack.io/v2/risk_score_query_task?coin=ETH&address={address}&api_key={api_key}
```

**请求参数**：与创建任务接口相同。

**响应**：
- 任务未完成：`{"success": true, "msg": "TaskUnderRunning"}`
- 任务完成：与同步 `v2/risk_score` 响应结构相同（含 score、risk_level、detail_list、risk_detail）

---

### 6. 交易调查 (`v1/transactions_investigation`)

**功能**：返回指定地址的交易调查结果，包含转入/转出交易列表及关联地址信息。

```
GET https://openapi.misttrack.io/v1/transactions_investigation?coin=ETH&address={address}&api_key={api_key}
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coin` | string | ✅ | 查询的代币 |
| `address` | string | ✅ | 查询的地址 |
| `api_key` | string | ✅ | API 密钥 |
| `start_timestamp` | int | ❌ | 开始时间戳（默认为 0） |
| `end_timestamp` | int | ❌ | 结束时间戳（默认为当前时间） |
| `type` | string | ❌ | 查询类型：`in`、`out`、`all`（默认 `all`） |
| `page` | int | ❌ | 页码（默认为 1） |

**响应字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `in` | list | 转入交易列表 |
| `out` | list | 转出交易列表 |
| `page` | int | 当前页码 |
| `total_pages` | int | 总页数 |
| `transactions_on_page` | int | 当前页交易数量（最多 1000 条） |

**交易条目子字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `address` | string | 与查询地址有转账关系的地址 |
| `type` | int | 地址类型：1=EOA/BTC地址，2=恶意地址，3=实体标签地址，4=合约地址 |
| `tx_hash_list` | list | 相关交易哈希列表 |
| `amount` | float(4) | 总转账金额 |
| `label` | string | 地址标签详情 |

**响应示例**：
```json
{
  "success": true,
  "msg": "",
  "data": {
    "out": [
      {
        "address": "0xd90e2f925da726b50c4ed8d0fb90ad053324f31b",
        "tx_hash_list": ["0x48c2601b..."],
        "amount": 743,
        "type": 3,
        "label": "Tornado.Cash: Router"
      }
    ],
    "in": [...],
    "page": 1,
    "total_pages": 1,
    "transactions_on_page": 36
  }
}
```

---

### 7. 地址行为分析 (`v1/address_action`)

**功能**：返回指定地址的交易行为分析结果（适合以饼图方式展示）。

```
GET https://openapi.misttrack.io/v1/address_action?coin=ETH&address={address}&api_key={api_key}
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coin` | string | ✅ | 查询的代币 |
| `address` | string | ✅ | 查询的地址 |
| `api_key` | string | ✅ | API 密钥 |

**响应字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `received_txs` | list | 转入交易行为分析结果列表 |
| `spent_txs` | list | 转出交易行为分析结果列表 |

**行为条目子字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `action` | string | 行为类型（如 DEX、Exchange、Mixer、Transfer、Swap） |
| `count` | int | 该类型交易数量 |
| `proportion` | float | 占比（百分比） |

**响应示例**：
```json
{
  "success": true,
  "msg": "",
  "action_dic": {
    "received_txs": [
      {"action": "DEX", "count": 7, "proportion": 70.0},
      {"action": "Mixer", "count": 1, "proportion": 10.0},
      {"action": "Exchange", "count": 1, "proportion": 10.0},
      {"action": "Swap", "count": 1, "proportion": 10.0}
    ],
    "spent_txs": [
      {"action": "Exchange", "count": 15, "proportion": 57.69},
      {"action": "DEX", "count": 2, "proportion": 7.69},
      {"action": "Transfer", "count": 9, "proportion": 34.62}
    ]
  }
}
```

---

### 8. 地址画像 / 地址追踪 (`v1/address_trace`)

**功能**：追踪地址与哪些平台有过交互（交易所、混币器、DeFi 协议、NFT 平台），识别相关恶意事件，并提供地址附加信息（使用的钱包、ENS 名称、关联 Twitter 账号）。

```
GET https://openapi.misttrack.io/v1/address_trace?coin=ETH&address={address}&api_key={api_key}
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coin` | string | ✅ | 查询的代币 |
| `address` | string | ✅ | 查询的地址 |
| `api_key` | string | ✅ | API 密钥 |

**响应字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `first_address` | string | Gas 费用的来源钱包地址或其标签 |
| `use_platform` | dict | 交互平台信息，包含 `exchange`（交易所）、`dex`（DEX）、`mixer`（混币器）、`nft`（NFT 平台） |
| `malicious_event` | dict | 恶意事件信息，包含 `phishing`（钓鱼）、`ransom`（勒索）、`stealing`（盗窃）、`laundering`（洗钱） |
| `relation_info` | dict | 关联信息，包含 `wallet`（关联钱包）、`ens`（ENS 名称）、`twitter`（Twitter 账号） |

**响应示例**：
```json
{
  "success": true,
  "msg": "",
  "data": {
    "first_address": "sideshift.ai",
    "use_platform": {
      "exchange": {"count": 1, "exchange_list": ["Binance"]},
      "dex": {"count": 3, "dex_list": ["Uniswap", "SushiSwap", "Multichain"]},
      "mixer": {"count": 2, "mixer_list": ["Tornado.Cash", "sideshift.ai"]},
      "nft": {"count": 0, "nft_list": []}
    },
    "malicious_event": {
      "phishing": {"count": 0, "phishing_list": []},
      "ransom": {"count": 0, "ransom_list": []},
      "stealing": {"count": 5, "stealing_list": ["MMFinance Exploiter"]},
      "laundering": {"count": 0, "laundering_list": []}
    },
    "relation_info": {
      "wallet": {"count": 0, "wallet_list": []},
      "ens": {"count": 2, "ens_list": ["destruction.eth", "poma.eth"]},
      "twitter": {"count": 1, "twitter_list": ["@destructioneth"]}
    }
  }
}
```

---

### 9. 地址交易对手分析 (`v1/address_counterparty`)

**功能**：返回指定地址的交易对手分析结果（适合以饼图方式展示）。

> ⚠️ **注意**：此接口不支持分析热钱包地址，会返回 `UnsupportedAddressType` 错误。

```
GET https://openapi.misttrack.io/v1/address_counterparty?coin=ETH&address={address}&api_key={api_key}
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coin` | string | ✅ | 查询的代币 |
| `address` | string | ✅ | 查询的地址 |
| `api_key` | string | ✅ | API 密钥 |

**响应字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `address_counterparty_list` | list | 交易对手列表 |

**交易对手条目子字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 实体名称（如 Uniswap、Tornado.Cash、Binance） |
| `amount` | float | 总交易金额（USD） |
| `percent` | float | 占比（百分比） |

**响应示例**：
```json
{
  "success": true,
  "msg": "",
  "address_counterparty_list": [
    {"name": "Uniswap", "amount": 4496524.699, "percent": 49.678},
    {"name": "Tornado.Cash", "amount": 2377637.58, "percent": 26.268},
    {"name": "Binance", "amount": 302.008, "percent": 0.003}
  ]
}
```

---

## 使用示例

### 场景 1：快速地址风险检测（KYT）

当需要对提币/充值地址进行快速 AML 检查时：

1. 调用 `v2/risk_score` 获取风险评分
2. 根据 `risk_level` 决策：
   - `Severe` (91-100)：拒绝交易并上报
   - `High` (71-90)：需人工复核
   - `Moderate` (31-70)：适度监控
   - `Low` (0-30)：正常放行

### 场景 2：批量异步风险检测

当需要批量检测大量地址时使用异步模式：

1. 循环调用 `POST v2/risk_score_create_task` 创建任务
2. 等待 1-10 秒（如 `has_result: false`）
3. 调用 `GET v2/risk_score_query_task` 轮询结果（无速率限制）

### 场景 3：地址完整画像调查

对可疑地址进行全面调查时，建议依次调用：

1. `v1/address_labels` → 了解地址实体身份
2. `v1/address_overview` → 了解地址活跃度和资产规模
3. `v2/risk_score` → 获取 AML 风险评分
4. `v1/address_trace` → 了解地址平台交互历史及关联信息
5. `v1/transactions_investigation` → 深入分析具体交易流向
6. `v1/address_counterparty` → 分析主要交易对手构成

---

## 示例脚本

参考 `scripts/` 目录中的示例脚本：

- `risk_check.py` - 单地址风险评分检查
- `batch_risk_check.py` - 批量异步风险评分
- `address_investigation.py` - 地址完整调查

---

## 与 Bitget Wallet Skill 集成 — 转账地址安全检测

> **适用场景**：当 Agent 同时加载了 [bitget-wallet-skill](https://github.com/bitget-wallet-ai-lab/bitget-wallet-skill) 和 misttrack-skills 时，在执行任何**转账 / Swap** 操作前，必须自动调用本技能对**目标地址（recipient / to-address）** 进行 AML 风险检测。

### 为什么需要地址级安全检测？

bitget-wallet-skill 的 Pre-Trade Workflow 已覆盖**代币安全**（蜜罐、税率、流动性），但未检测**收款方地址**的 AML 风险。向被制裁地址、混币器出金地址或黑客钱包转账可能导致：

- 资产被链上追踪机构标记
- 触犯 OFAC 制裁合规要求
- 资金被交易所冻结（如目标是洗钱中转地址）

misttrack-skills 专门填补这一缺口。

---

### 链代码映射表

将 bitget-wallet-skill 的 `chain` 参数映射为 MistTrack `coin` 参数：

| bitget-wallet-skill chain | MistTrack coin | 说明 |
|--------------------------|---------------|------|
| `eth` | `ETH` | Ethereum 原生代币 |
| `sol` | `SOL` | Solana 原生代币 |
| `bnb` | `BNB` | BNB Chain 原生代币 |
| `trx` | `TRX` | TRON 原生代币 |
| `base` | `ETH-Base` | Base 链 ETH |
| `arbitrum` | `ETH-Arbitrum` | Arbitrum 链 ETH |
| `optimism` | `ETH-Optimism` | OP Mainnet ETH |
| `matic` | `POL-Polygon` | Polygon 链原生代币 |
| `ton` | `TON` | TON 链原生代币 |
| `suinet` | `SUI` | Sui 链原生代币 |

> **稳定币注意**：若转账代币为 USDT/USDC（非原生代币），MistTrack 风险评分**对地址是全局计算的**（与代币无关），因此使用原生代币的 coin 参数查询即可。

---

### 决策逻辑

| MistTrack 风险等级 | 分数范围 | Agent 决策 | 操作 |
|-----------------|----------|-----------|------|
| **Low** | 0–30 | ✅ ALLOW | 静默通过，正常继续转账流程 |
| **Moderate** | 31–70 | ⚠️ WARN | 向用户展示风险摘要，请求二次确认后方可继续 |
| **High** | 71–90 | ⚠️ WARN | 向用户展示详细风险报告，强烈建议取消，需明确二次确认 |
| **Severe** | 91–100 | ❌ BLOCK | 拒绝执行转账，告知用户目标地址存在严重风险 |

> **特例 — 已认证白名单地址**：若 `v1/address_labels` 返回的 `label_type` 为 `exchange`（如 Binance、Coinbase 充值地址），且 `risk_level` 为 Low 或 Moderate，可直接 ALLOW，无需二次确认。

---

### Agent 集成工作流

Agent 在执行 `swap-calldata` 或任何转账指令**之前**，自动执行以下步骤（对用户透明，不中断流程）：

```
转账安全检测流程（Agent 后台自动执行）：

1. 提取目标地址（swap --to-address 或用户指定的收款地址）
2. 识别链类型（通过上方映射表 chain → coin）
3. 调用风险评分脚本：
   python3 scripts/transfer_security_check.py --address <to_address> --chain <chain_code>

4. 读取 exit code 和 JSON 输出，按决策逻辑处理：
   - exit 0 (ALLOW)  → 静默继续，在最终确认摘要中显示 "✅ 收款地址安全"
   - exit 1 (WARN)   → 暂停，向用户显示风险摘要，等待用户明确确认
   - exit 2 (BLOCK)  → 终止流程，向用户说明原因，建议放弃转账
   - exit 3 (ERROR)  → API 不可用，显示 "⚠️ 地址安全检测失败（原因：...）"，由用户决定是否继续
```

#### 集成到 bitget-wallet-skill Pre-Trade Workflow

在原有 bitget-wallet-skill 的 Pre-Trade Workflow 基础上，插入第 0 步：

```
0. transfer-security  → 检测收款地址 AML 风险（新增，使用 misttrack-skills）
1. security           → 检查代币安全（honeypot、tax）
2. token-info         → 获取价格、市值
3. liquidity          → 检查池深度
4. swap-quote         → 获取报价和路由
```

---

### 调用示例

#### 基础调用（推荐 Agent 使用）

```bash
# ETH 链地址检测
python3 scripts/transfer_security_check.py \
  --address 0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b \
  --chain eth

# Solana 链地址检测
python3 scripts/transfer_security_check.py \
  --address 5tzFkiKscXHK5B17AoKFdroMRCEVGvSqtPkRSLzprFwN \
  --chain sol

# JSON 输出（便于 Agent 解析）
python3 scripts/transfer_security_check.py \
  --address 0x28C6c06298d514Db089934071355E5743bf21d60 \
  --chain eth --json
```

#### JSON 输出格式

```json
{
  "decision": "ALLOW",
  "score": 15,
  "risk_level": "Low",
  "detail_list": [],
  "label_type": "exchange",
  "label_list": ["Binance", "hot"],
  "risk_report_url": "https://light.misttrack.io/riskReport/0x...",
  "address": "0x28C6c06298d514Db089934071355E5743bf21d60",
  "coin": "ETH",
  "chain": "eth"
}
```

#### WARN 场景示例输出（展示给用户）

```
⚠️  收款地址安全警告
────────────────────────────────────
地址：    0xABCD...1234
链：      ETH
风险评分：55 (Moderate)
风险描述：Interact With High-risk Tag Address, Involved Illicit Activity
风险报告：https://light.misttrack.io/riskReport/0xABCD...

建议：该地址存在中等风险，请确认收款方身份后再继续。
是否仍要继续转账？[yes/no]
```

---

### API 不可用时的降级策略

| 场景 | 原因 | 处理方式 |
|------|------|---------|
| `MISTTRACK_API_KEY` 未设置 | 未配置 | exit 3，警告用户前往设置 |
| `InvalidApiKey` | Key 无效或过期 | exit 3，提示检查 Key |
| `ExceededDailyRateLimit` | 超出每日限额 | exit 3，提示次日重试或升级套餐 |
| 网络超时 | 网络问题 | exit 3，重试 1 次后放弃 |

> **重要**：任何 exit 3 情况下，Agent 必须明确告知用户「地址安全检测失败，无法验证收款地址风险」，并让用户决定是否继续。**不得静默忽略检测失败**。

---

## 与 Trust Wallet Skills 集成 — 转账地址安全检测

> **适用场景**：当 Agent 同时加载了 [tw-agent-skills](https://github.com/trustwallet/tw-agent-skills)（`wallet-core` 或 `trust-web3-provider`）和 misttrack-skills 时，在生成任何含收款地址的代码之前，必须自动调用本技能进行 AML 风险检测。

### Trust Wallet Skills 的转账场景

Trust Wallet skills 是**开发者库**（非命令行工具），收款地址通过代码字段传入：

| 技能 | 场景 | 收款地址字段 |
|------|------|------------|
| **wallet-core** | Swift/Kotlin/TS 签名交易 | `toAddress`（ETH/BTC/Cosmos `sendCoinsMessage`） |
| **trust-web3-provider** | EthereumProvider handler | `eth_sendTransaction.to` |
| **trust-web3-provider** | TonProvider | `ton_sendTransaction.to` |
| **trust-web3-provider** | BitcoinProvider | `signPSBT` outputs 中的目标地址 |
| **trust-web3-provider** | TronProvider | `sign(transaction)` 的目标地址字段 |

### CoinType → MistTrack coin 映射表

| wallet-core CoinType | `--chain` 参数 | MistTrack coin |
|----------------------|--------------|---------------|
| `.ethereum` | `eth` | `ETH` |
| `.bitcoin` | `bitcoin` / `btc` | `BTC` |
| `.solana` | `solana` / `sol` | `SOL` |
| `.smartChain` | `smartchain` / `bsc` | `BNB` |
| `.tron` | `tron` / `trx` | `TRX` |
| `.polygon` | `polygon` / `matic` | `POL-Polygon` |
| `.ton` | `ton` / `tonchain` | `TON` |
| `.cosmos` | `cosmos` / `atom` | ⛔ 不支持，exit 3 |
| `.aptos` | `aptos` | ⛔ 不支持，exit 3 |

> **trust-web3-provider 链映射**：`EthereumProvider` chainId `0x1`→`eth`，`0x38`→`bnb`，`0x89`→`polygon`，`0xa`→`optimism`，`0xa4b1`→`arbitrum`，`0x2105`→`base`。

### Agent 触发规则

Agent 在以下任意时刻**应自动调用安全检测**：

#### wallet-core 场景
当 Agent 生成含 `toAddress` 的签名代码片段时，在给出代码前先检查该地址：

```bash
# 示例：用户请求为 Bitcoin 地址生成签名，先检查目标地址
python3 scripts/transfer_security_check.py \
  --address 1MityqAKBEKHPkBpwDCqPMBNbYPxbNbKzr \
  --chain bitcoin --json

# 示例：用户构建 Ethereum 转账，先检查 toAddress
python3 scripts/transfer_security_check.py \
  --address 0xRecipient... \
  --chain eth --json
```

#### trust-web3-provider 场景
当 Agent 帮开发者实现处理 `eth_sendTransaction` / `ton_sendTransaction` 的 handler 时，在处理逻辑中插入检测点：

```bash
# Handler 收到 eth_sendTransaction，目标地址在 params.to
python3 scripts/transfer_security_check.py \
  --address <params.to> --chain eth --json

# Handler 收到 ton_sendTransaction
python3 scripts/transfer_security_check.py \
  --address <params.to> --chain ton --json
```

### 决策规则（与 Bitget Wallet 集成相同）

| exit | 决策 | Agent 行为 |
|------|------|-----------|
| 0 | ✅ ALLOW | 正常生成代码，确认摘要中添加「✅ 收款地址安全」注释 |
| 1 | ⚠️ WARN | 向用户展示风险详情，等待明确确认后再生成代码 |
| 2 | ❌ BLOCK | 拒绝生成相关代码，向用户说明风险并建议更换地址 |
| 3 | ⚠️ ERROR | 通知用户检测失败原因（API 不可用/链不支持），由用户决定是否继续 |

### 不支持的链处理

**Aptos** 和 **Cosmos/ATOM** 目前 MistTrack 尚未收录，脚本会返回 exit 3 并给出说明：

```bash
$ python3 scripts/transfer_security_check.py --address 0xabc --chain aptos --json
{
  "decision": "ERROR",
  "error": "MistTrack 暂不支持 Aptos (APT) 链地址查询。请人工核实收款方身份。"
}
# exit code: 3
```

Agent 对此类 exit 3 应向用户说明「该链暂无自动安全检测，请通过其他方式核实收款方身份」。

---

## 参考资料

- [MistTrack 官方文档](https://docs.misttrack.io/)
- [MistTrack OpenAPI 概述](https://docs.misttrack.io/openapi/overview)
- [MistTrack 控制台](https://dashboard.misttrack.io)
- [常见错误消息](https://docs.misttrack.io/support/common-error-messages)
- [Bitget Wallet Skill](https://github.com/bitget-wallet-ai-lab/bitget-wallet-skill)
- [Trust Wallet tw-agent-skills](https://github.com/trustwallet/tw-agent-skills)

