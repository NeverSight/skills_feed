---
name: dao-best-practices
description: 用于规范化DAO文件，确保遵循Drizzle ORM最佳实践，包括文件结构、方法命名、类型安全和性能优化。当需要重构或创建DAO文件以符合项目标准时使用。
---

# DAO规范化技能

此技能帮助规范化DAO文件，使其符合项目的最佳实践。

## 使用说明

1. 识别需要规范化的DAO文件，通常位于 `apps/web/src/db/models/daos/`。

2. 阅读参考指南：[DAO最佳实践指南](references/dao-best-practices.md) 以了解规范。
3. 代码示例：[DAO代码参考](references/template-dao.ts) 作为参考
4. 使用脚本检查文件：[检查DAO脚本](scripts/check-dao.js) （如果可用）。

5. 重构文件以匹配指南中的模式。

## 核心规范

- 文件结构：文件名与表名一致，导出为对象。
- 方法：使用驼峰命名，标准CRUD方法。
- 类型安全：使用Drizzle类型推断。
- 性能：使用分页、联表查询等。

如果需要更多细节，请阅读参考文件。
