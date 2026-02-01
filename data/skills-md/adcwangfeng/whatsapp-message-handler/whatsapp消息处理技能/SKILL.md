---
name: WhatsApp消息处理技能
description: 专门处理WhatsApp多模块消息的接收和响应系统，支持文本、图片、文件等多种消息类型的处理
dependencies: 
  - node.js
  - whatsapp-web.js
---

# WhatsApp消息处理技能

## Description
专门处理WhatsApp多模块消息的接收和响应系统，支持文本、图片、文件等多种消息类型的处理。

## Capabilities
- 接收和解析各种类型的WhatsApp消息
- 多模块消息处理（文本、图片、文档、位置等）
- 智能回复生成
- 消息路由和分发
- 消息历史记录
- 错误处理和重试机制

## Usage
- 接收来自WhatsApp的消息
- 根据消息类型和内容进行处理
- 生成适当的回复
- 发送回复到WhatsApp

## Example Usage Scenarios
- **Customer Support**: 自动处理客户查询和常见问题
- **Notification System**: 发送重要通知和提醒
- **Data Collection**: 收集用户反馈和信息
- **Workflow Automation**: 自动化消息驱动的工作流程

## Example Commands
- "处理接收到的WhatsApp消息"
- "回复用户发送的文本消息"
- "转发消息到指定模块"
- "记录消息历史"

## Files
- `index.js`: 主入口文件
- `message-parser.js`: 消息解析器
- `handlers/`: 消息处理模块
- `router.js`: 消息路由器
- `response-builder.js`: 回复构建器
- `whatsapp-connector.js`: WhatsApp连接器
- `config.json`: 配置文件

## Dependencies
- Node.js >= 14.0.0
- whatsapp-web.js library
- Express.js for webhooks (if applicable)

## Configuration
The skill requires proper WhatsApp Web authentication and webhook setup.