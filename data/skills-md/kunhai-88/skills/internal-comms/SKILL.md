---
name: internal-comms
description: "帮助编写各种内部沟通的资源集，使用公司喜欢的格式。Claude 应在被要求编写任何类型的内部沟通时使用此技能（状态报告、领导更新、3P 更新、公司简报、FAQ、事件报告、项目更新等）。"
license: MIT
---

# 内部沟通

编写内部沟通时使用此技能，包括：
- 3P 更新（Progress、Plans、Problems）
- 公司简报
- FAQ 回答
- 状态报告
- 领导更新
- 项目更新
- 事件报告

## 使用方式

要编写任何内部沟通：

1. **从请求中识别沟通类型**
2. **从 `examples/` 目录加载相应指南文件**：
   - `examples/3p-updates.md` — 用于 Progress/Plans/Problems 团队更新
   - `examples/company-newsletter.md` — 用于公司范围简报
   - `examples/faq-answers.md` — 用于回答常见问题
   - `examples/general-comms.md` — 用于其他不明确匹配上述之一的
3. **遵循该文件中的具体说明**，关于格式、语调与内容收集

如果沟通类型不匹配任何现有指南，询问澄清或关于所需格式的更多上下文。

## 关键词

3P updates、company newsletter、company comms、weekly update、faqs、common questions、updates、internal comms
