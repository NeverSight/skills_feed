---
name: analytics-tracking
description: "搭建、改进或审计分析与追踪时使用。触发词：set up tracking、GA4、Google Analytics、转化追踪、事件追踪、UTM、tag manager、GTM、埋点方案、tracking plan。A/B 实验度量见 ab-test-setup。"
license: MIT
---

# 分析埋点

搭建可指导营销与产品决策的追踪体系。

## 前置了解

业务目标与关键转化、需回答的问题；现有工具（GA4、Mixpanel 等）与缺口；技术栈、实施与维护方、隐私与合规要求。

## 原则

- **为决策而追踪**：每个事件应对应有决策，避免虚荣指标。  
- **从问题反推**：先明确要回答什么，再定埋点。  
- **命名一致**：统一规范，事前定好并文档化。  
- **保证数据质量**：验证实现、持续监控，宁少求精。

## 事件类型

**浏览**：page_view（增强元数据）。  
**用户行为**：点击、表单、功能使用、内容互动。  
**系统**：注册完成、购买、订阅变更、报错。  
**自定义转化**：目标完成、漏斗阶段、业务里程碑。

## 命名建议

小写+下划线；具体命名（如 `cta_hero_clicked`）；语境放 properties，不塞进事件名。格式示例：`object_action`（`signup_completed`）或 `category_object_action`。

## 常用事件（示例）

**营销站**：page_view、outbound_link_clicked、scroll_depth、cta_clicked、form_started/submitted、signup_started/completed、demo_requested。  
**产品**：onboarding_step_completed、feature_used、trial_started、pricing_viewed、checkout_started、purchase_completed。  
**电商**：product_viewed、product_added_to_cart、checkout_step_completed、purchase_completed。

## GA4

Data Streams 按平台配置；开启增强衡量。使用推荐事件与预定名称。自定义事件：`gtag('event', 'signup_completed', { ... })` 或 dataLayer.push。在 Admin > Events 中标记转化、设置计数方式，必要时导入 Google Ads。

## GTM

Tags：GA4 配置 + 事件；Triggers：Page View、Click、Form Submit、自定义事件；Variables：Data Layer、JS 等。用文件夹与统一命名；每次发布写版本说明；Preview 测完再发布。

## UTM

utm_source、utm_medium、utm_campaign、utm_content、utm_term；全小写，下划线或连字符统一；具体但简洁。用表格或工具记录所有 UTM，便于复盘。

## 校验与排错

用 GA4 DebugView、GTM Preview、Tag Assistant 等。检查：触发正确、属性完整、无重复、多端一致、无 PII。常见问题：触发配置错、Tag 停用、GTM 未加载；变量/数据层/时序错误；多容器或多重触发导致重复。

## 隐私与合规

EU/UK/CA 等需 cookie 同意；避免 PII 入属性；设置留存与删除能力。GA4 Consent Mode：在获得同意前不追踪或仅部分追踪；与 CMP 集成。

## 相关技能

ab-test-setup、seo-audit、page-cro。
