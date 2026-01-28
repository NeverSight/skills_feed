---
name: jimmer-orm
description: Jimmer ORM 开发助手，帮助编写实体映射代码和 DSL 查询语句。适用于：(1) 定义或修改 Jimmer 实体（使用 @Entity 注解的 interface）；(2) 编写 Jimmer DSL 查询代码；(3) 配置实体关联关系（@ManyToOne, @OneToMany, @ManyToMany）；(4) 使用动态谓词、动态表连接或隐式子查询；(5) 编辑包含 Jimmer 相关代码的 Java/Kotlin 文件。
---

## 核心概念

### 实体定义特点

- 使用 **interface** 定义实体，而非 class
- 实体是**动态对象**和**不可变对象**
- 只有 getter，没有 setter
- 由 KSP (Kotlin) 或 AnnotationProcessor (Java) 编译时生成实现
- 属性未设置 ≠ 属性为 null

### DSL 查询特点

- 强类型 SQL DSL，提供编译时安全保证
- 动态谓词：根据参数决定是否添加 SQL 条件
- 动态表连接：未使用的连接自动忽略，冲突连接自动合并
- 隐式子查询：基于集合关联创建子查询，自动生成父子关联条件

## 语言选择

Jimmer 为 Kotlin 提供了特化的 API 风格

- **实体映射：** 参考 `references/entity-mapping.md`
- **DSL 查询：** 参考 `references/dsl-queries.md`
- **实体模板：** 参考 `assets/EntityTemplate.kt`

## 关键注解速查

- `@Entity` - 标记实体类型
- `@Id` - 标记主键
- `@GeneratedValue` - 主键生成策略
- `@Key` - 业务键
- `@ManyToOne` / `@OneToMany` / `@ManyToMany` / `@OneToOne` - 关联映射
- `@JoinColumn` - 自定义外键列名
- `@JoinTable` - 自定义中间表
- `@Column` - 自定义列名（仅用于非关联字段）
- `@Table` - 自定义表名
- `?` (Kotlin) - 标记可空属性

## 命名约定

- 实体名 → 表名：`BookStore` → `BOOK_STORE`
- 属性名 → 列名：`firstName` → `FIRST_NAME`
- 多对一外键：`store` → `STORE_ID`

## 工作流程

1. **定义实体时：**
   - 使用 interface 而非 class
   - 根据项目语言参考对应的实体模板和映射文档
   - 参考 `assets/EntityTemplate.kt` 和 `references/entity-mapping.md`
   - 参考 `references/dto.md` 完成 DTO 定义

2. **编写查询时：**
   - 优先使用动态谓词（Kotlin: `ilike?`/`between?`）
   - 使用动态表连接处理关联查询
   - 使用隐式子查询处理集合关联
   - 根据项目语言参考对应的 DSL 查询文档
   - 参考 `references/dsl-queries.md`

3. **遇到问题时：**
   - 检查实体是否使用 interface 定义
   - 检查关联映射的 `mappedBy` 配置
   - 检查动态谓词的参数是否正确
   - 确认表连接路径是否正确
