---
name: service-best-practice
description: 帮助开发者根据项目指南编写 Services，以 tRPC + Service + DAO 架构的最佳实践。提供 Service 结构、依赖注入、错误处理、代码示例、模板、样板代码生成和最佳实践验证的指导。在创建或重构代码库中的 Service 文件时使用。
---

# Service 最佳实践

## 概述

在 code-arena 项目中，Service 层负责业务逻辑处理、数据转换和外部 API 集成。本技能提供编写 Service 的规范和最佳实践指导，确保代码的可维护性、可测试性和一致性。

## 项目数据流

前端 React 组件 → tRPC 客户端 → tRPC 路由器 → Service → DAO → Drizzle DB → PostgreSQL

## 核心规范

### 1. 文件结构

- 位置：`apps/web/src/services/`
- 命名：`{feature}Service.ts`
- 导出：`export const {Feature}Service = { ... }`

### 2. 依赖注入（强制）

Service 不得直接导入 `db`，必须通过 DAO 依赖注入。

### 3. 方法签名

- 驼峰命名
- 返回 Promise 类型
- 使用 Zod 验证输入

### 4. 错误处理

使用自定义错误类，记录日志，抛出适当错误。

### 5. 事务管理

Service 可发起 `db.transaction()`，DAO 接收可选 `tx` 参数。

## 使用指南

当创建或重构 Service 文件时：

1. 遵循依赖注入模式
2. 使用 Zod 验证输入
3. 通过 DAO 处理数据库操作
4. 实现适当错误处理和日志
5. 编写测试用例

## 详细参考

完整的最佳实践指南请参阅 [service-best-practice-guide.md](references/service-best-practice-guide.md)，包含代码示例、模板和高级用法。

## 资源

- [service-best-practice-guide.md](references/service-best-practice-guide.md)：完整的 Service 编写指南
