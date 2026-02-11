---
name: miniqmt-skills
description: XtQuant (迅投量化) API 文档 - 用于量化交易的 Python API，包括行情数据获取、交易执行、策略回测等功能
---

# XtQuant (迅投量化) 技能文档

XtQuant 是基于迅投 MiniQMT 的完善 Python 策略运行框架，提供量化交易所需的行情和交易 API 接口。

## 何时使用此技能

在以下场景中应该使用此技能：

### 量化交易开发
- 开发 A 股量化交易策略
- 实现自动化交易系统
- 构建回测框架
- 编写交易信号生成逻辑

### 行情数据处理
- 获取历史 K 线数据（日线、分钟线等）
- 订阅实时行情推送
- 下载财务数据和板块信息
- 处理分笔成交数据

### 交易执行
- 程序化下单（限价单、市价单等）
- 批量撤单操作
- 查询账户资产、持仓、委托
- 接收交易回报推送

### 问题排查
- 调试 XtQuant 连接问题
- 解决数据订阅失败
- 处理交易接口报错
- 优化策略性能

## 核心概念

### 两大核心模块

**xtdata - 行情数据模块**
- 提供历史和实时的 K 线、分笔数据
- 财务数据、合约基础信息
- 板块和行业分类信息
- 需要先启动 MiniQMT 客户端

**xttrader - 交易执行模块**
- 报单、撤单操作
- 查询资产、委托、成交、持仓
- 接收资金、委托、成交等主推消息
- 支持回调机制处理交易事件

### 运行环境要求
- Python 版本：3.6 - 3.12（64位）
- 必须先启动 MiniQMT 客户端
- 通过 session_id 区分不同策略会话

## 快速参考

### 1. 行情数据获取（基础模式）

从官方文档提取的完整示例：

```python
from xtquant import xtdata
import time

# 设定标的列表和周期
code_list = ["000001.SZ"]
period = "1d"

# 下载历史行情数据到本地
for code in code_list:
    xtdata.download_history_data(code, period=period, incrementally=True)

# 下载财务和板块数据
xtdata.download_financial_data(code_list)
xtdata.download_sector_data()

# 读取本地历史行情
history_data = xtdata.get_market_data_ex([], code_list, period=period, count=-1)
print(history_data)
```

**说明**：XtQuant 的数据以压缩形式存储在本地，使用前需要先下载。

### 2. 实时行情订阅（回调模式）

```python
from xtquant import xtdata

code_list = ["000001.SZ"]
period = "1d"

# 定义回调函数
def on_data(data):
    code_list = list(data.keys())
    kline = xtdata.get_market_data_ex([], code_list, period=period)
    print(kline)

# 订阅行情并设置回调
for code in code_list:
    xtdata.subscribe_quote(code, period=period, count=-1, callback=on_data)

# 阻塞程序以持续接收回调
xtdata.run()
```

**说明**：使用回调模式时，必须调用 `xtdata.run()` 阻塞程序，否则程序会直接退出。

### 3. 交易模块初始化与下单

从官方文档提取的交易示例：

```python
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant

# 定义交易回调类
class MyXtQuantTraderCallback(XtQuantTraderCallback):
    def on_stock_order(self, order):
        """委托回报推送"""
        print("委托回报:", order.stock_code, order.order_status)

    def on_stock_trade(self, trade):
        """成交变动推送"""
        print("成交回报:", trade.stock_code, trade.order_id)

    def on_order_error(self, order_error):
        """委托失败推送"""
        print("委托失败:", order_error.error_msg)

# 初始化交易客户端
path = 'D:\\迅投极速交易终端\\userdata_mini'  # MiniQMT 安装路径
session_id = 123456  # 会话编号，不同策略使用不同编号
xt_trader = XtQuantTrader(path, session_id)

# 创建账号对象
acc = StockAccount('1000000365')  # 替换为实际账号

# 注册回调
callback = MyXtQuantTraderCallback()
xt_trader.register_callback(callback)

# 启动交易线程并连接
xt_trader.start()
connect_result = xt_trader.connect()  # 返回0表示成功
subscribe_result = xt_trader.subscribe(acc)  # 订阅交易推送

# 下单示例
stock_code = '600000.SH'
order_id = xt_trader.order_stock(
    acc,
    stock_code,
    xtconstant.STOCK_BUY,  # 买入
    200,  # 数量
    xtconstant.FIX_PRICE,  # 限价单
    10.5  # 价格
)
print(f"下单成功，订单号: {order_id}")
```

**说明**：交易前必须先启动 MiniQMT 客户端并登录账号。

### 4. 连接VIP服务器（高级功能）

从官方文档提取的VIP服务器连接示例：

```python
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata

# 设置token（从投研用户中心获取）
xtdc.set_token('这里输入你的token')

# 设置VIP服务器连接池
addr_list = [
    '115.231.218.73:55310',
    '115.231.218.79:55310',
    '42.228.16.211:55300',
    '42.228.16.210:55300'
]
xtdc.set_allow_optmize_address(addr_list)

# 开启K线全推功能（VIP功能）
xtdc.set_kline_mirror_enabled(True)

# 初始化并监听端口
xtdc.init()
port = xtdc.listen(port=58621)  # 指定固定端口
xtdata.connect(port=port)

print('连接成功')
xtdata.run()
```

**说明**：VIP服务器提供更快的行情推送和更多的数据服务，需要从投研用户中心获取token。

### 5. 指定端口避免冲突

```python
from xtquant import xtdatacenter as xtdc

xtdc.set_token("你的token")
xtdc.init(False)  # 不自动初始化
port = 58601  # 自定义端口
xtdc.listen(port=port)
print(f"服务启动，开放端口：{port}")
```

**说明**：当58609默认端口被占用时，可以指定自定义端口。

## 常见问题与解决方案

### 问题1：导入xtquant库失败

**错误信息**：`NO module named 'xtquant.IPythonAPiClient'`

**解决方案**：
- 确认使用的是64位 Python 3.6-3.12 版本
- 检查 xtquant 库是否正确安装
- 如果出现 PermissionError，说明存在文件权限问题

### 问题2：连接失败返回-1

**原因**：同一个 session 的两次 Python 进程 connect 之间必须超过3秒

**解决方案**：
- 等待至少3秒后再次连接
- 或者使用不同的 session_id

### 问题3：端口58609被占用

**错误信息**：执行 xtdatacenter.init 时提示监听58609端口失败

**解决方案**：
```python
# 方法1：指定自定义端口
xtdc.init(False)
port = xtdc.listen(port=58601)

# 方法2：关闭所有Python程序或重启电脑
```

### 问题4：委托备注字段被截断

**问题描述**：查询委托的投资备注只有前半部分

**原因**：极简客户端的 order_remark 字段最大24个英文字符（一个中文占3个），超出部分会被丢弃

**解决方案**：控制备注长度，或使用大QMT（无长度限制）

## 参考文档说明

本技能包含以下参考文档，使用 `view` 命令查看详细内容：

### api.md - API完整文档
**来源**：官方文档
**置信度**：中等
**内容**：5个页面，包含：

- **完整实例**：行情订阅、交易下单的完整代码示例
- **XtData模块**：行情数据获取的详细API说明
- **XtTrader模块**：交易执行的详细API说明
- **常见问题**：实际使用中的问题和解决方案

**适用场景**：
- 查找具体API的参数说明
- 学习完整的代码实现模式
- 解决开发中遇到的具体问题

### getting_started.md - 快速入门
**来源**：官方文档
**置信度**：中等
**内容**：2个页面，包含：

- XtQuant 能提供的服务概述
- 运行依赖环境说明
- XtQuant 运行逻辑介绍
- xtdata 和 xttrader 两大模块简介

**适用场景**：
- 初次接触 XtQuant
- 了解整体架构和设计理念
- 确认环境配置要求

## 使用指南

### 初学者入门路径

**第一步：环境准备**
1. 安装64位 Python 3.6-3.12
2. 下载并安装 MiniQMT 客户端
3. 安装 xtquant 库：`pip install xtquant`

**第二步：学习基础**
1. 阅读 `getting_started.md` 了解整体架构
2. 运行"快速参考"中的示例1（行情数据获取）
3. 理解数据下载和读取的流程

**第三步：实践进阶**
1. 尝试实时行情订阅（示例2）
2. 学习回调机制的使用
3. 查看 `api.md` 中的完整实例

### 中级用户进阶

**行情数据处理**
- 掌握多周期数据获取（1m, 5m, 1d等）
- 学习财务数据和板块数据的使用
- 实现数据缓存和增量更新策略

**交易策略开发**
- 理解交易回调机制（on_stock_order, on_stock_trade）
- 实现风险控制逻辑
- 处理委托失败和撤单场景

**性能优化**
- 使用异步查询接口（query_stock_orders_async）
- 合理设置订阅范围避免数据过载
- 控制session数量避免文件堆积

### 高级用户最佳实践

**VIP服务器使用**
- 配置VIP服务器连接池
- 开启K线全推功能获取全市场数据
- 优化网络连接和数据传输

**多账户管理**
- 使用不同session_id管理多个策略
- 实现账户间的资金调度
- 处理沪港通、深港通等特殊账户类型

**生产环境部署**
- 实现断线重连机制
- 添加日志记录和监控
- 设置异常告警和自动恢复

## 重要提示

### 使用前必读

1. **MiniQMT客户端必须先启动**
   - 所有 xtdata 和 xttrader 功能都依赖 MiniQMT 客户端
   - 确保客户端已登录并连接到行情服务器

2. **数据下载机制**
   - XtQuant 的历史数据以压缩形式存储在本地
   - 使用前必须先调用 download_* 接口下载数据
   - 订阅的实时数据会自动保存，无需重复下载

3. **回调函数注意事项**
   - 使用回调模式时必须调用 `xtdata.run()` 或 `xttrader.run()` 阻塞程序
   - 回调函数中不要执行耗时操作，避免阻塞数据接收
   - 推荐在回调中使用异步查询接口

4. **Session管理**
   - 不同策略使用不同的 session_id
   - 同一 session 的两次连接间隔必须超过3秒
   - 控制 session 范围避免产生大量 down_queue 文件

5. **风险提示**
   - 本文档中的策略示例仅供参考学习
   - 实盘交易前请充分测试
   - 交易有风险，投资需谨慎

## 技能来源

本技能文档基于以下来源自动生成：

- **官方文档**：迅投知识库 (dict.thinktrader.net)
- **抓取页面数**：7个页面
- **文档分类**：入门指南、API文档、完整示例、常见问题
- **生成时间**：2026年1月

## 相关资源

- **官方网站**：http://www.thinktrader.net
- **投研用户中心**：https://xuntou.net/#/userInfo（获取VIP token）
- **迅投学院**：https://www.xuntou.net/plugin.php?id=keke_video_base
- **技术支持**：参考官方文档的常见问题部分
