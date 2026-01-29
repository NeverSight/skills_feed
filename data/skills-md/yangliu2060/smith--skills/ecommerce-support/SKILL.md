---
name: ecommerce-support
description: AI电商客服助手，支持订单查询、商品推荐、工单处理，可使用Playwright MCP自动操作电商后台查询真实订单状态。
---

# 电商客服助手

AI 驱动的电商客服机器人，自动识别客户意图，处理订单查询、商品推荐、投诉工单等场景。

## 触发条件

当用户说以下内容时启动此技能：
- "客服回复"
- "处理客户问题"
- "订单查询"
- "ecommerce support"
- "帮我回复客户"
- "生成客服话术"

## 依赖的 MCP 服务

| MCP | 用途 | 必需 |
|-----|------|------|
| **playwright** | 自动登录电商后台查询订单 | 可选 |
| **supabase** | 存储订单/工单数据 | 可选 |
| **memory** | 保持对话上下文 | 可选 |

## 工作流程

```
┌─────────────────────┐
│   客户消息输入       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   AI 意图识别       │
│   分析客户需求       │
└──────────┬──────────┘
           │
     ┌─────┼─────┬──────────┐
     │     │     │          │
     ▼     ▼     ▼          ▼
┌───────┐┌───────┐┌───────┐┌───────┐
│订单   ││商品   ││投诉   ││常见   │
│查询   ││推荐   ││工单   ││问答   │
└───┬───┘└───┬───┘└───┬───┘└───┬───┘
    │        │        │        │
    ▼        ▼        ▼        ▼
┌───────┐┌───────┐┌───────┐┌───────┐
│Playwright│ AI   ││创建   ││知识库 │
│查后台  ││分析   ││工单   ││匹配   │
└───┬───┘└───┬───┘└───┬───┘└───┬───┘
    │        │        │        │
    └────────┴────────┴────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  生成客服回复    │
         │  保存对话记录    │
         └─────────────────┘
```

## 执行步骤

### 步骤 1：接收客户消息

**输入格式**：
```
用户: 帮我回复这个客户：
"你好，我的订单123456怎么还没发货？已经3天了！"
```

或批量处理：
```
用户: 处理这些客服消息 [消息列表/文件]
```

### 步骤 2：AI 意图识别

**意图分类**：

| 意图 | 关键词 | 处理方式 |
|------|--------|---------|
| 订单查询 | 订单、发货、物流、到哪了 | 查询订单状态 |
| 退款退货 | 退款、退货、换货、不想要了 | 创建退货工单 |
| 商品咨询 | 有货吗、尺码、颜色、推荐 | 商品推荐 |
| 投诉建议 | 投诉、差评、不满意、垃圾 | 创建投诉工单 |
| 优惠活动 | 优惠券、满减、活动、便宜 | 活动信息 |
| 售后问题 | 坏了、质量问题、维修 | 创建售后工单 |
| 闲聊其他 | 你好、谢谢、在吗 | 常规回复 |

**意图识别提示词**：
```
分析以下客户消息的意图：

【客户消息】
{message}

【输出格式】
{
  "intent": "order_query|refund|product_inquiry|complaint|promotion|after_sale|chat",
  "confidence": 0.95,
  "entities": {
    "order_id": "123456",
    "product_name": "",
    "emotion": "negative|neutral|positive"
  },
  "urgency": "high|medium|low"
}
```

### 步骤 3：订单查询处理

#### 方式 A：使用 Playwright MCP 查询真实订单

**适用场景**：需要查询电商后台真实订单状态

```javascript
// Playwright MCP 操作步骤

1. 打开电商后台
   browser_navigate({ url: "https://seller.taobao.com" })
   // 或其他电商平台后台

2. 检查登录状态
   - 如未登录，提示用户先登录
   - 保存登录状态供后续使用

3. 进入订单管理
   browser_click({ element: "订单管理" })

4. 搜索订单号
   browser_type({
     element: "订单搜索框",
     text: "{order_id}"
   })
   browser_click({ element: "搜索" })

5. 获取订单状态
   browser_snapshot() // 截图获取订单信息

6. 解析订单状态
   - 订单状态（待发货/已发货/已签收）
   - 物流信息
   - 预计到达时间
```

**支持的电商平台**：
- 淘宝/天猫卖家中心
- 京东商家后台
- 拼多多商家版
- Shopify Admin
- 有赞商家后台

#### 方式 B：模拟订单数据

**适用场景**：演示或无后台访问权限

```json
{
  "order_id": "123456",
  "status": "shipped",
  "status_text": "已发货，运输中",
  "logistics": {
    "company": "顺丰速运",
    "tracking_no": "SF1234567890",
    "last_update": "2025-12-28 15:30",
    "location": "深圳转运中心"
  },
  "estimated_delivery": "2025-12-30"
}
```

### 步骤 4：商品推荐处理

**推荐逻辑**：
```
1. 解析客户需求（品类、价格区间、偏好）
2. 匹配商品库/搜索商品
3. 生成推荐话术

【推荐话术模板】
亲，根据您的需求，为您推荐以下商品：

1️⃣ **{商品名1}** - ¥{价格}
   {商品亮点}

2️⃣ **{商品名2}** - ¥{价格}
   {商品亮点}

您看哪款更合适呢？有任何问题随时问我～
```

#### 使用 Playwright 获取商品信息

```javascript
// 从电商平台获取商品详情

1. 打开商品页面
   browser_navigate({ url: "{product_url}" })

2. 获取商品信息
   browser_snapshot()

3. 解析信息
   - 商品名称
   - 价格
   - 库存状态
   - 规格参数
```

### 步骤 5：工单处理

**创建工单**：
```json
{
  "ticket_id": "TK20251229001",
  "type": "complaint",
  "customer_id": "C12345",
  "order_id": "123456",
  "description": "客户投诉物流慢",
  "priority": "high",
  "status": "open",
  "created_at": "2025-12-29T10:30:00Z"
}
```

**工单处理流程**：
1. 创建工单记录
2. 生成安抚回复
3. 通知相关人员（可用邮件MCP）
4. 跟踪处理进度

### 步骤 6：生成客服回复

**回复生成提示词**：

```
你是一位专业的电商客服，请根据以下信息生成回复：

【客户消息】
{customer_message}

【意图分析】
意图: {intent}
情绪: {emotion}
紧急度: {urgency}

【查询结果】
{query_result}

【回复要求】
1. 称呼亲切（亲/您好）
2. 先共情，再解决
3. 信息准确完整
4. 语气温和专业
5. 如有问题主动道歉
6. 结尾询问是否还有其他需要

【输出格式】
直接输出回复内容，可适当使用emoji
```

### 步骤 7：保存对话记录

```json
{
  "conversation_id": "conv_20251229_001",
  "customer_id": "C12345",
  "messages": [
    {
      "role": "customer",
      "content": "我的订单怎么还没发货？",
      "timestamp": "2025-12-29T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "亲，非常抱歉让您久等了...",
      "timestamp": "2025-12-29T10:30:05Z",
      "intent": "order_query"
    }
  ]
}
```

## 客服话术模板库

### 订单查询回复

**已发货**：
```
亲，您的订单已经发货啦！🚚

物流信息：
📦 快递公司：{company}
📝 运单号：{tracking_no}
📍 当前位置：{location}
⏰ 预计送达：{estimated_delivery}

您可以点击订单详情查看实时物流～
还有其他问题吗？
```

**未发货**：
```
亲，非常抱歉让您久等了！🙏

您的订单目前正在加紧处理中，预计{ship_date}前发出。
给您带来不便深感抱歉，我们会尽快为您安排～

如果着急，我可以帮您催一下仓库哦！
```

### 退款处理回复

```
亲，收到您的退款申请了～

我这边已经帮您提交处理：
📋 退款单号：{refund_id}
💰 退款金额：¥{amount}
⏰ 预计到账：1-3个工作日

退款会原路返回，届时请留意账户变动。
如有问题随时联系我哦！
```

### 投诉安抚回复

```
亲，真的非常抱歉给您带来了不好的体验！🙏

我完全理解您的心情，这确实是我们的问题。
我已经将您的情况反馈给主管，会尽快给您一个满意的解决方案。

为了表示歉意，这边给您申请了一张{coupon}优惠券，
希望能弥补一点点这次的不愉快。

请问您方便留一下联系电话吗？我们主管会亲自给您回电处理。
```

### 商品咨询回复

```
亲，这款商品的详细信息如下：

📦 {product_name}
💰 价格：¥{price}
📏 规格：{specs}
🎁 赠品：{gifts}
📦 库存：{stock_status}

{product_highlights}

现在下单还有{promotion}活动哦～
需要我帮您看下尺码吗？
```

## 使用示例

### 示例 1：单条消息回复

```
用户: 帮我回复："订单123456到哪了"

Claude:
1. 识别意图：订单查询
2. [可选] 使用Playwright查询后台订单状态
3. 生成回复：
   "亲，您的订单123456已经发货啦！
    快递：顺丰 SF1234567890
    当前位置：深圳转运中心
    预计明天送达～还有其他问题吗？"
```

### 示例 2：批量处理

```
用户: 批量回复这10条客户消息

Claude:
1. 逐条分析意图
2. 批量查询相关信息
3. 生成10条回复
4. 输出结果供复制使用
```

### 示例 3：接入电商后台

```
用户: 连接淘宝后台，查询订单123456的真实状态

Claude:
1. 使用Playwright打开淘宝卖家中心
2. 检查登录状态（如需登录则提示）
3. 搜索订单号
4. 截图获取订单状态
5. 解析并生成回复
```

## 电商平台后台配置

### 淘宝/天猫

```yaml
platform: taobao
login_url: https://login.taobao.com
seller_url: https://myseller.taobao.com
order_path: /home.htm#/order-manage
search_selector: "#keyword"
```

### 京东商家

```yaml
platform: jd
login_url: https://passport.jd.com
seller_url: https://shop.jd.com
order_path: /order/list
search_selector: ".search-input"
```

### Shopify

```yaml
platform: shopify
login_url: https://{store}.myshopify.com/admin
order_path: /admin/orders
search_selector: "#search-query"
```

## 数据存储

- 对话记录：`~/.claude/cache/ecommerce-support/conversations/`
- 工单记录：`~/.claude/cache/ecommerce-support/tickets/`
- 回复模板：`~/.claude/cache/ecommerce-support/templates/`

## 依赖工具

- **Claude AI**: 意图识别 + 回复生成
- **playwright MCP**: 查询电商后台订单 (可选)
- **memory MCP**: 保持对话上下文 (可选)
- **Write**: 保存对话记录

## 最佳实践

### 提升回复质量
- 先共情再解决问题
- 信息要准确完整
- 避免机械化回复
- 适当使用emoji增加亲和力

### 处理负面情绪
- 第一时间道歉
- 给出明确解决方案
- 适当补偿（优惠券等）
- 升级通道（主管回电）

### 效率提升
- 建立常见问题知识库
- 预设回复模板
- 批量处理相似问题
- 自动分类优先级

## 原始来源

改编自 n8n 模板：
- 模板ID: 7256
- 原名: AI-Powered E-commerce Customer Support Chatbot with GPT-4 & Supabase
- 链接: https://n8n.io/workflows/7256
