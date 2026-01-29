---
name: dolphindb
description: DolphinDB 时序数据库完整技术文档与最佳实践。包含1490个技术文档 + 3份官方白皮书。涵盖数据库设计、流计算、量化回测、函数查询等全场景。
version: 2.0.0
source: https://docs.dolphindb.cn + Official Whitepapers
author: Optimized by Skill Creator
tags:
  - database
  - time-series
  - streaming
  - quantitative-trading
  - backtesting
  - dolphindb
---

# DolphinDB 完整技术文档与实战指南

**版本**: 2.0.0 (优化版)  
**文档数量**: 1490 个技术文档 + 3 份官方白皮书  
**DolphinDB版本**: 3.00.4  
**更新时间**: 2026-01-22  
**文档来源**: https://docs.dolphindb.cn  

---

## 📚 核心资源概览

### 🎯 官方白皮书（深度最佳实践）

提供生产级架构设计和完整工作流程指南：

1. **[数据库白皮书](references/whitepapers/database.md)** (1073行)
   - DolphinDB 核心架构与分布式设计
   - TSDB vs OLAP 存储引擎详解
   - 分区策略、高可用、备份恢复
   - SQL优化与库内计算
   - **适用场景**: 系统架构设计、性能优化、生产部署

2. **[流数据白皮书](references/whitepapers/streaming.md)** (2279行)
   - 流计算框架与发布订阅机制
   - 7大流计算引擎详解
   - 流批一体架构与历史回放
   - 金融与物联网场景应用
   - **适用场景**: 实时计算、CEP、流式ETL

3. **[中高频回测白皮书](references/whitepapers/backtest.md)** (2205行)
   - 完整回测系统架构
   - 数据回放与模拟撮合引擎
   - DolphinScript/Python/C++ 策略开发
   - 量化策略实战案例
   - **适用场景**: 量化回测、算法交易、策略研发

### 📖 在线技术文档（1490篇）

按功能领域分类的完整API参考和操作指南：

| 分类 | 文档数量 | 说明 |
|------|---------|------|
| 函数参考/其他函数 | 1171 | 系统函数、网络函数等 |
| 其他 | 97 | 其他技术文档 |
| 函数参考/统计函数 | 61 | 相关性、协方差、标准差等统计指标 |
| 函数参考/数学函数 | 42 | 基础数学运算、三角函数、对数等 |
| 函数参考/SQL函数 | 41 | 查询、关联、聚合等SQL操作 |
| 函数参考/时间序列函数 | 26 | 日期时间处理、时序窗口计算 |
| 流数据处理 | 22 | 流表、订阅、流计算引擎 |
| 数据库核心 | 13 | 存储引擎、分区、事务、高可用 |
| 部署与配置 | 9 | 集群部署、参数配置 |
| 函数参考/字符串函数 | 5 | 字符串操作、正则表达式 |
| API与连接器 | 1 | Python、Java、C++ API |
| 运维管理 | 1 | 监控、备份、权限管理 |
| 教程与示例 | 1 | 快速入门、场景案例 |

**完整文档索引**: 详见 [CATALOG.md](CATALOG.md)

---

## 🚀 常见问题快速导航

### 新手入门
- **如何快速上手DolphinDB？** → [关于 DolphinDB](references/doc_1201.md)
- **如何部署集群？** → [分布式架构](references/doc_6249.md)
- **如何选择存储引擎？** → 查阅 [数据库白皮书](references/whitepapers/database.md) 第3-4章

### 数据库设计
- **如何选择分区策略？** → [数据分区](references/doc_9485.md) + [数据库白皮书](references/whitepapers/database.md)
- **TSDB vs OLAP 如何选择？** → [TSDB存储引擎](references/doc_6240.md) 和 [OLAP存储引擎](references/doc_7837.md)
- **如何优化查询性能？** → [数据库白皮书](references/whitepapers/database.md) 第5章

### 流计算开发
- **如何实现实时计算？** → [流数据白皮书](references/whitepapers/streaming.md)
- **流计算引擎有哪些？** → [流数据白皮书](references/whitepapers/streaming.md) 第3章
- **如何实现流批一体？** → [流数据白皮书](references/whitepapers/streaming.md) 第4章

### 量化回测
- **如何搭建回测系统？** → [回测白皮书](references/whitepapers/backtest.md)
- **如何实现模拟撮合？** → [回测白皮书](references/whitepapers/backtest.md) 第3章
- **如何进行中高频回测？** → [回测白皮书](references/whitepapers/backtest.md) 第4-7章

### 高级功能
- **如何实现高可用？** → [高可用](references/doc_3934.md)
- **如何进行数据备份？** → [数据库白皮书](references/whitepapers/database.md) 第6章
- **如何管理权限？** → [数据库白皮书](references/whitepapers/database.md) 第6.4节

---

## 📝 常用代码示例

### 1. 创建TSDB存储引擎的分区表

```dolphindb
// 组合分区: VALUE(日期) + HASH(股票代码)
db_date = database("", VALUE, 2024.01.01..2024.12.31)
db_sym = database("", HASH, [SYMBOL, 10])
db = database("dfs://stock_data", COMPO, [db_date, db_sym])

// TSDB引擎，支持排序列和去重
schemaTable = table(
    1:0,
    `trade_time`symbol`price`volume,
    [TIMESTAMP, SYMBOL, DOUBLE, LONG]
)

pt = db.createPartitionedTable(
    table=schemaTable,
    tableName="stock_tick",
    partitionColumns=`trade_date`symbol,
    sortColumns=`symbol`trade_time,  // 排序键
    keepDuplicates=LAST,  // 去重策略
    engine="TSDB"
)
```

### 2. 创建OLAP存储引擎的分区表

```dolphindb
// OLAP引擎适合追加式写入和批量分析
db = database("dfs://stock_analysis", VALUE, 2024.01M..2024.12M)

schemaTable = table(
    1:0,
    `trade_date`symbol`open`high`low`close`volume,
    [DATE, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, LONG]
)

pt = db.createPartitionedTable(
    table=schemaTable,
    tableName="daily_kline",
    partitionColumns=`trade_date,
    engine="OLAP"
)
```

### 3. 流计算 - 实时K线合成

```dolphindb
// 1. 创建流表
share streamTable(1:0, `time`sym`price`vol, [TIMESTAMP, SYMBOL, DOUBLE, INT]) as tickStream
share streamTable(1:0, `time`sym`open`high`low`close`volume, 
                  [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, LONG]) as klineStream

// 2. 创建时序聚合引擎
tsEngine = createTimeSeriesEngine(
    name="kline_1min",
    windowSize=60000,  // 1分钟窗口
    step=60000,
    metrics=<[first(price), max(price), min(price), last(price), sum(vol)]>,
    dummyTable=tickStream,
    outputTable=klineStream,
    timeColumn=`time,
    keyColumn=`sym
)

// 3. 订阅流表
subscribeTable(tableName="tickStream", actionName="kline", handler=append!{tsEngine})

// 4. 插入数据测试
insert into tickStream values(2024.01.01T09:30:00.000, `600000, 10.5, 1000)
```

### 4. 中高频回测完整流程

```dolphindb
// 1. 清理环境
try{ unsubscribeTable(tableName="replayStream", actionName="backtest") }catch(ex){}
try{ dropStreamEngine("backtestEngine") }catch(ex){}

// 2. 创建回放流表
share streamTable(1:0, `time`sym`price`vol, [TIMESTAMP, SYMBOL, DOUBLE, INT]) as replayStream

// 3. 创建回测引擎（需要加载回测插件）
loadPlugin("/path/to/backtest_plugin.so")
backtestEngine = createBacktestEngine(
    name="my_strategy",
    initialCapital=10000000,
    commission=0.0003
)

// 4. 订阅回放数据
subscribeTable(tableName="replayStream", actionName="backtest", handler=backtestEngine)

// 5. 数据回放
histData = loadTable("dfs://stock_data", "stock_tick")
ds = replayDS(sqlObj=<select * from histData where trade_date=2024.01.01>, 
              dateColumn=`trade_date, 
              timeColumn=`trade_time)
replay(inputTables=ds, outputTables=replayStream, dateColumn=`trade_date, 
       timeColumn=`trade_time, replayRate=1000)

// 6. 获取回测结果
backtestEngine.getPositions()  // 持仓
backtestEngine.getOrders()     // 订单
backtestEngine.getTrades()     // 成交
backtestEngine.getMetrics()    // 绩效指标
```

### 5. 高级SQL示例

```dolphindb
// Context By - 组内窗口计算
select 
    trade_date, symbol, close,
    movingAvg(close, 5) as ma5,
    movingAvg(close, 20) as ma20
from loadTable("dfs://stock", "daily")
context by symbol

// Pivot By - 数据透视
select close 
from loadTable("dfs://stock", "daily")
where symbol in `600000`600001`600002
pivot by trade_date, symbol

// Asof Join - 时序非精确关联
select * 
from tick_data aj snapshot_data 
on tick_data.time = snapshot_data.time and tick_data.symbol = snapshot_data.symbol
```

---

## 💡 最佳实践工作流

### 1. 数据库设计流程

```
需求分析 → 存储引擎选择 → 分区策略设计 → 性能测试 → 生产部署
    ↓            ↓              ↓             ↓          ↓
  数据特征    TSDB/OLAP    COMPO分区      压力测试    高可用配置
```

**决策要点**:
- **高频写入 + 点查** → TSDB引擎 + sortColumns
- **批量分析** → OLAP引擎
- **时序数据** → VALUE(日期) + HASH(Symbol) 组合分区
- **查询优化** → 合理使用分区裁剪、并行计算

**参考文档**: [数据库白皮书](references/whitepapers/database.md) 第2-4章

### 2. 流计算开发流程

```
数据源接入 → 流表设计 → 引擎选择 → 订阅处理 → 结果输出
    ↓           ↓          ↓          ↓         ↓
  Kafka等   streamTable  7种引擎  subscribeTable  入库/推送
```

**引擎选择**:
- **滑动窗口聚合** (K线合成) → TimeSeriesEngine
- **横截面计算** (全市场排名) → CrossSectionalEngine  
- **复杂状态逻辑** (多因子计算) → ReactiveStateEngine
- **异常检测** → AnomalyDetectionEngine

**参考文档**: [流数据白皮书](references/whitepapers/streaming.md) 第3章

### 3. 量化回测完整流程

```
数据准备 → 历史回放 → 模拟撮合 → 策略执行 → 绩效分析
   ↓         ↓          ↓          ↓         ↓
 分区表    replay    Exchange   BacktestEngine  Sharpe/回撤
```

**核心技术点**:
- 使用 `replay` 或 `replayDS` 严格按时序回放
- `createExchange` 实现"价格优先、时间优先"撮合
- 支持逐笔、快照、分钟频等多种数据源
- C++插件可提升10倍以上性能

**参考文档**: [回测白皮书](references/whitepapers/backtest.md) 完整内容

---

## 🔍 如何使用本Skill

### 按场景查找

1. **我是新手，想快速上手**
   - 先阅读: [关于 DolphinDB](references/doc_1201.md)
   - 然后看: [数据库白皮书](references/whitepapers/database.md) 第1章

2. **我要设计生产数据库**
   - 必读: [数据库白皮书](references/whitepapers/database.md) 第2-6章
   - 参考: [数据分区](references/doc_9485.md)、[高可用](references/doc_3934.md)

3. **我要开发实时计算应用**
   - 必读: [流数据白皮书](references/whitepapers/streaming.md) 全文
   - 速查: 本文档中的"流计算代码示例"

4. **我要搭建量化回测系统**
   - 必读: [回测白皮书](references/whitepapers/backtest.md) 全文
   - 实战: 白皮书第5-7章策略案例

5. **我要查特定函数用法**
   - 使用: [CATALOG.md](CATALOG.md) 按分类查找
   - 或在 `references/` 目录搜索关键词

### 按角色查找

| 角色 | 推荐阅读路径 |
|------|-------------|
| **架构师** | 数据库白皮书 → 分布式架构 → 高可用方案 |
| **DBA** | 数据库白皮书 → 运维章节 → 备份恢复 |
| **后端开发** | 流数据白皮书 → API文档 → 代码示例 |
| **量化研究员** | 回测白皮书 → 策略开发 → 绩效分析 |
| **数据分析师** | SQL函数参考 → Context By → Pivot By |

---

## 📊 版本信息

- **Skill版本**: 2.0.0 (相比1.x版本的改进)
  - ✅ 新增完整文档索引 (CATALOG.md)
  - ✅ 新增常见问题快速导航
  - ✅ 新增5大类代码示例
  - ✅ 优化文档分类 (14个细分类别)
  - ✅ 明确DolphinDB版本对应关系
  
- **DolphinDB版本**: 3.00.4
- **文档同步时间**: 2026-01-20
- **维护策略**: 季度更新 / 重大版本发布时同步

---

## 🔗 相关资源

- **官网**: https://www.dolphindb.com
- **文档中心**: https://docs.dolphindb.cn
- **社区论坛**: https://community.dolphindb.com
- **GitHub**: https://github.com/dolphindb

---

**Generated by Skill Creator v2.0** | 优化时间: 2026-01-22
