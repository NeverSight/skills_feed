---
name: database-expert
description: 专注于数据库建模、TypeORM 实体定义、迁移管理与 SQL 优化。
version: 1.0.0
author: GitHub Copilot
---

# Database Expert Skill (数据库专家技能)

## 核心能力 (Core Capabilities)

-   **模型设计**: 设计符合第三范式的数据库 Schema。
-   **TypeORM 实体**: 编写标准的 TypeORM 实体类，正确配置 `@Entity`, `@Column`, `@PrimaryGeneratedColumn` 等装饰器。
-   **关系映射**: 处理 OneToOne, OneToMany, ManyToMany 关系，并配置适当的 Cascade 和 JoinColumn。
-   **性能优化**: 识别并添加必要的索引 (Indices)，优化慢查询。
-   **数据迁移**: 维护数据库结构变更，确保生产环境平滑升级。

## 指令 (Instructions)

1.  **优先建模**: 在开发后端 API 前，必须先通过该技能检查或更新数据库实体。
2.  **强制命名**: 数据库字段使用 `snake_case`，实体属性使用 `camelCase`，表名遵循项目约定的复数形式。
3.  **约束完整性**: 必须为关键字段定义 `nullable: false`, `unique: true` 等约束。
4.  **安全注入**: 严禁在代码中直接拼接字符串构建 SQL，始终使用 TypeORM 的 QueryBuilder 或 Repository API。

## 使用示例 (Usage Example)

输入: "为博客添加分类功能。"
动作: 在 `server/database/entities/` 中创建 `Category.ts` 实体，并建立与 `Post` 的多对一关系。
