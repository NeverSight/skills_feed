---
name: apaas-object-skill
description: Use when managing aPaaS platform data objects via the apaas-oapi-client Node SDK (client.schema.create/update/delete), or when converting relational database designs (MySQL, PostgreSQL, SQLite DDL, ER diagrams) to aPaaS objects.
---

# aPaaS 数据对象管理

管理 aPaaS 平台数据对象（表）的创建、更新、删除。通过 Node SDK 的 `client.schema.*` 接口操作。

## 前置条件

使用此 skill 前，必须确保以下环境已就绪：

1. **安装 Node.js**（>= 16）
2. **安装 SDK**：`npm install apaas-oapi-client@^0.1.37`（`schema` 模块从 0.1.37 开始提供，低版本会报 `Cannot read properties of undefined`）
3. **获取凭据**（在 aPaaS 平台的应用管理中获取）：
   - Client ID（格式：`c_` 开头，如 `c_a4dd955086ec45a882b9`）
   - Client Secret（格式：32 位十六进制，如 `a62fc785b97a4847810a4f319ccbdb5e`）
   - Namespace（必须以 `__c` 结尾，如 `package_5dc5b7__c`）

### 初始化 Client

SDK 导出结构为 `{ apaas: { Client } }`，**不是**直接导出 `Client`：

```typescript
// ESM
import { apaas } from 'apaas-oapi-client';

// CommonJS
const { apaas } = require('apaas-oapi-client');
```

构造参数为**顶层平铺**，不要嵌套在 `auth` 或其他对象下：

```typescript
// ✅ 正确
const client = new apaas.Client({
    clientId: 'c_a4dd955086ec45a882b9',
    clientSecret: 'a62fc785b97a4847810a4f319ccbdb5e',
    namespace: 'package_5dc5b7__c'
});
await client.init();

// ❌ 错误：不能解构 Client 直接用
const { Client } = require('apaas-oapi-client');  // Client is undefined

// ❌ 错误：不能嵌套在 auth 下
new apaas.Client({ auth: { clientId: '...' } });  // 鉴权失败
```

## 系统预置规则

### 系统预置对象（只读）

平台预置两张数据表，**不可修改、不可删除**：

| 对象 | 说明 |
|------|------|
| `_user` | 用户表 |
| `_department` | 部门表 |

### 系统字段识别规则

**API name 以 `_` 下划线开头的对象或字段，均为系统预置，只读不可修改/删除。**

### 默认字段

任何新建的空白对象，系统自动生成以下 5 个字段，无需手动创建：

| 字段 | 类型 | 说明 |
|------|------|------|
| `_id` | bigint | 记录唯一标识 |
| `_createdBy` | lookup | 创建人 |
| `_createdAt` | datetime | 创建时间 |
| `_updatedBy` | lookup | 最后修改人 |
| `_updatedAt` | datetime | 最后修改时间 |

**注意**：
- 不要在 `schema.create` 的 fields 中定义这些字段，会冲突报错
- 不要尝试用 `schema.update` 修改或删除这些字段
- `_user` 和 `_department` 可以作为 lookup 的 `referenced_object_api_name` 目标（如关联用户/部门）

## 核心 API

| 接口 | 用途 |
|------|------|
| `client.schema.create({ objects })` | 批量创建数据对象 |
| `client.schema.update({ objects })` | 批量更新对象（添加/修改/删除字段） |
| `client.schema.delete({ api_names })` | 批量删除数据对象 |

> **批量上限**：`schema.create / update / delete` 每次调用最多 **10 个对象**，超过时需分批调用：
>
> ```typescript
> // 通用分批执行：将 items 按 batchSize 拆分，逐批调用 fn
> async function batchExecute<T>(items: T[], batchSize: number, fn: (batch: T[]) => Promise<any>) {
>     for (let i = 0; i < items.length; i += batchSize) {
>         const batch = items.slice(i, i + batchSize);
>         const result = await fn(batch);
>         // 检查 result（见"响应验证"章节）
>     }
> }
>
> // 示例：创建 25 个空壳对象
> const allObjects = [/* ... 25 个对象定义 ... */];
> await batchExecute(allObjects, 10, (batch) => client.schema.create({ objects: batch }));
> ```

| `client.object.listWithIterator()` | 列出所有数据对象 |
| `client.object.metadata.fields({ object_name })` | 获取对象所有字段元数据 |
| `client.object.metadata.export2markdown()` | 导出对象元数据为 Markdown |

## 创建对象（两步走，必须遵守）

**`schema.create` 会静默忽略 `fields` 参数** — 即使传了字段定义，返回 `code: 0`，但实际只创建空壳对象，字段不会被创建。

必须采用**两步走**：先 `create` 空壳，再 `update` 添加字段。

```typescript
// 步骤 1：创建空壳对象（不传 fields，或传了也会被忽略）
await client.schema.create({
    objects: [{
        api_name: 'product',
        label: { zh_cn: '产品', en_us: 'Product' },
        settings: { display_name: '_id', allow_search_fields: ['_id'], search_layout: [] }
    }]
});

// 步骤 2：用 update + operator:'add' 添加字段
await client.schema.update({
    objects: [{
        api_name: 'product',
        fields: [
            { operator: 'add', api_name: 'name',
              label: { zh_cn: '产品名称', en_us: 'Name' },
              type: { name: 'text', settings: { required: true, unique: false, case_sensitive: false, multiline: false, max_length: 200 } },
              encrypt_type: 'none' }
        ]
    }]
});
```

> 字段就位后可再次调用 `schema.update` 将 `display_name` 从 `_id` 更新为实际字段（如 `name`），注意 **不能用** `_name`。多对象场景见「三阶段创建法」。

## 更新对象

三种操作通过 `operator` 字段区分：

```typescript
await client.schema.update({
    objects: [{
        api_name: 'product',
        fields: [
            // 添加字段
            { operator: 'add', api_name: 'desc', label: { zh_cn: '描述', en_us: 'Desc' },
              type: { name: 'text', settings: { required: false, unique: false, case_sensitive: false, multiline: true, max_length: 1000 } }, encrypt_type: 'none' },
            // 修改字段（必须带完整 type，只改 label 会报错）
            { operator: 'replace', api_name: 'code',
              label: { zh_cn: '编号', en_us: 'Code' },
              type: { name: 'text', settings: { required: true, unique: true, case_sensitive: false, multiline: false, max_length: 100 } } },
            // 删除字段（只需 api_name）
            { operator: 'remove', api_name: 'desc' }
        ]
    }]
});
```

## 删除对象

```typescript
await client.schema.delete({ api_names: ['product', 'order'] });
```

## 字段类型映射（关键陷阱）

metadata 返回的类型名和 schema 接口接受的类型名**不一致**，以下类型**必须转换**（用错会报类型不识别）：

| Metadata Type | Schema Type |
|---|---|
| `number` | `float` |
| `option` | `enum` |
| `file` | `attachment` |
| `autoId` | `auto_number` |
| `mobileNumber` | `phone` |
| `avatarOrLogo` | `avatar` |
| `referenceField` | `reference_field` |

其余类型同名直接使用：`text`、`bigint`、`date`、`datetime`、`boolean`、`lookup`、`richText`、`email`、`region`、`decimal`、`multilingual`。

> 完整映射见 `references/field-schema-rules.ts` 的 `SCHEMA_TYPE_BY_METADATA_TYPE`。

## 各字段类型 settings 模板（必须遵守）

> **致命陷阱**：某些 settings 字段**看似可选实则必填**。缺失时 API 返回 `code: "0"` + `data: null`，看似成功但**字段不会被创建**。更危险的是，同一批次中一个字段缺少必填 settings，会导致**整批所有字段都静默失败**。
>
> 下表中用 ⚠️ 标记的 settings 为**必填项**，不传会导致静默失败。始终使用下方完整模板，不要省略任何字段。

| Schema Type | 完整 settings 模板 |
|---|---|
| `text` | `{ required: false, unique: false, case_sensitive: false,` ⚠️ `multiline: false, max_length: 255 }` |
| `float` | `{ required: false, unique: false, display_as_percentage: false, decimal_places_number: 2 }` |
| `bigint` | `{ required: false, unique: false }` |
| `date` / `datetime` | `{ required: false }` |
| `enum` | `{ required: false, multiple: false, option_source: "custom", options: [{label, api_name, color, active}] }` |
| `boolean` | `{ default_value: true, description_if_true: {zh_cn, en_us}, description_if_false: {zh_cn, en_us} }` |
| `lookup` | `{ required: false, multiple: false, referenced_object_api_name: "target" }` |
| `reference_field` | `{ current_lookup_field_api_name: "...", target_reference_field_api_name: "..." }` |
| `attachment` | `{ required: false, any_type: true, max_uploaded_num: 10, mime_types: [] }` |
| `auto_number` | `{` ⚠️ `generation_method: "random", digits: 1, prefix: "", suffix: "", start_at: "1" }` |
| `richText` | `{ required: false, max_length: 1000 }` |
| `phone` | `{ required: false, unique: false }` |
| `avatar` | `{ display_style: "square" }` |
| `email` | `{ required: false, unique: false }` |
| `region` | `{ required: false, multiple: false, has_level_strict: true, strict_level: 4 }` |
| `decimal` | `{ required: false, unique: false, display_as_percentage: false, decimal_places: 2 }` |
| `multilingual` | `{ required: false, unique: false, case_sensitive: false,` ⚠️ `multiline: false, max_length: 1000 }` |

**已确认的必填 settings**（缺失 = 静默失败）：
- **`text` / `multilingual`**：`multiline` 必须显式传 `true` 或 `false`
- **`auto_number`**：`generation_method` 必须传（如 `"random"`）

**enum 选项颜色**：`blue, cyan, green, yellow, orange, red, magenta, purple, blueMagenta, grey`

## 从关系型数据库设计转换为 aPaaS 对象

用户提供的数据模型文档可能基于 MySQL、PostgreSQL、SQLite 等关系型数据库设计。以下规则指导如何将其转换为 aPaaS 平台的对象和字段。

**转换完成后，必须先生成转换确认表呈现给用户确认，再执行创建操作。**

### SQL 列类型 → aPaaS 字段类型

| SQL 类型 | aPaaS Schema Type | settings 要点 | 转换说明 |
|---|---|---|---|
| `VARCHAR(n)` / `CHAR(n)` | `text` | `multiline: false, max_length: n` | n > 255 时建议确认是否需要多行 |
| `TEXT` / `LONGTEXT` / `MEDIUMTEXT` | `text` | `multiline: true, max_length: 100000` | 大文本映射为多行文本 |
| `INT` / `INTEGER` / `BIGINT` / `SERIAL` | `bigint` | `required: false, unique: false` | aPaaS 无 int/bigint 区分，统一用 bigint |
| `FLOAT` / `DOUBLE` / `REAL` | `float` | `decimal_places_number: 2` | 按需调整小数位 |
| `DECIMAL(p,s)` / `NUMERIC(p,s)` | `decimal` | `decimal_places: s` | s 映射为 `decimal_places` |
| `DATE` | `date` | `required: false` | 直接映射 |
| `DATETIME` / `TIMESTAMP` | `datetime` | `required: false` | 统一映射为 datetime |
| `BOOLEAN` / `TINYINT(1)` / `BIT` | `boolean` | `default_value: true/false` | 注意转换 DEFAULT 值 |
| `ENUM('a','b','c')` | `enum` | 每个枚举值转为 `options` 数组项 | 见下方枚举转换规则 |
| `JSON`（存富文本） | `richText` | `max_length: 1000` | 仅当 JSON 用于富文本时 |
| `BLOB` / `BINARY` / `VARBINARY` | `attachment` | `any_type: true` | 二进制文件类的列 |

**特殊语义识别**（根据列名或注释推断更精确的类型）：

| 列名模式 | 推断 aPaaS 类型 | 判断依据 |
|---|---|---|
| `email` / `*_email` / `mail` | `email` | 列名含 email/mail |
| `phone` / `mobile` / `tel` / `*_phone` | `phone` | 列名含 phone/mobile/tel |
| `avatar` / `logo` / `profile_image` | `avatar` | 列名含 avatar/logo |
| `auto_number` / `serial_no` / `*_code`（自增编号类） | `auto_number` | 列名暗示自增编号且有 AUTO_INCREMENT 或 SERIAL |
| `region` / `province` / `city` / `address` | `region` | 列名含地区信息 |

> **注意**：语义识别是启发式的，转换后必须让用户确认。当无法确定时，默认映射为 `text`。

### SQL 约束 → aPaaS 字段 settings

| SQL 约束 | aPaaS settings | 说明 |
|---|---|---|
| `NOT NULL` | `required: true` | 非空约束 |
| `UNIQUE` | `unique: true` | 唯一约束 |
| `DEFAULT value` | `default_value: value`（boolean）| 仅 boolean 类型支持默认值 |
| `PRIMARY KEY` (`id`) | 不转换 | aPaaS 自动生成 `_id`，忽略用户的主键列 |
| `AUTO_INCREMENT` | 通常忽略 | `_id` 自动处理；如果是业务编号列，用 `auto_number` |
| `CHECK` | 不直接支持 | 需要在应用层实现或告知用户 aPaaS 不支持 |
| `INDEX` | 不转换 | aPaaS 自动管理索引 |

### 外键与关联关系 → lookup / reference_field

这是转换中**最关键**的部分。关系型数据库用外键表达关联，aPaaS 用 lookup 和 reference_field。

| 关系型设计 | aPaaS 转换 | 示例 |
|---|---|---|
| **外键列**（`order.customer_id REFERENCES customer(id)`） | 在 order 上创建 `lookup` 字段，`referenced_object_api_name: 'customer'` | `customer_id INT FK` → lookup |
| **一对多**（一个 customer 有多个 order） | 多的一方（order）加 `lookup`（`multiple: false`）指向一的一方 | 标准 lookup |
| **多对多**（中间表 `student_course(student_id, course_id)`） | **消除中间表**，在任一方加 `lookup`（`multiple: true`）指向另一方 | 中间表不创建为 aPaaS 对象 |
| **自关联**（`employee.manager_id REFERENCES employee(id)`） | 同一对象上创建 lookup 指向自身 | `referenced_object_api_name` 指向自己 |
| **外键 + 需要显示关联对象的字段**（如订单列表要显示客户名称） | 先建 lookup，再建 `reference_field` 引用目标对象的字段 | lookup + reference_field 组合 |

**中间表识别规则**：
- 表只有两个外键列（+ 可能的 id 和时间戳）
- 表名是两个实体名的组合（如 `student_course`、`user_role`、`tag_article`）
- 没有独立的业务字段

遇到中间表时：
1. **不要**创建为 aPaaS 对象
2. 在关系的某一方创建 `lookup`（`multiple: true`）指向另一方
3. 选择哪一方加 lookup 时，优先选择业务上"主动关联"的一方（如学生选课 → 在 student 上加 lookup 指向 course）
4. 如果中间表有额外业务字段（如 `score`、`enrolled_at`），则**必须保留为独立对象**，两端各用一个 lookup

### SQL ENUM → aPaaS enum 转换规则

```sql
-- SQL 定义
status ENUM('draft', 'published', 'archived') NOT NULL DEFAULT 'draft'
```

转换为：

```typescript
{
    operator: 'add',
    api_name: 'status',
    label: { zh_cn: '状态', en_us: 'Status' },
    type: {
        name: 'enum',
        settings: {
            required: true,    // 来自 NOT NULL
            multiple: false,
            option_source: 'custom',
            options: [
                { label: { zh_cn: '草稿', en_us: 'Draft' }, api_name: 'draft', color: 'grey', active: true },
                { label: { zh_cn: '已发布', en_us: 'Published' }, api_name: 'published', color: 'green', active: true },
                { label: { zh_cn: '已归档', en_us: 'Archived' }, api_name: 'archived', color: 'blue', active: true }
            ]
        }
    },
    encrypt_type: 'none'
}
```

**注意**：
- SQL 的 ENUM 值直接作为 `api_name`（需合法：小写字母、数字、下划线）
- `label` 的中文需要根据语义翻译，无法机械转换，转换时用英文作为占位、中文标注"待确认"
- 颜色按顺序从 `enum 选项颜色`（见 settings 模板章节）中轮询分配

### 转换工作流（必须遵守）

拿到用户的数据库设计文档（SQL DDL、ER 图描述、表格等）后，按以下流程执行：

**第一步：解析与识别**

1. 提取所有表（→ aPaaS 对象）和列（→ aPaaS 字段）
2. 识别主键列 → 忽略（aPaaS 用 `_id`）
3. 识别外键列 → 标记为 lookup 候选
4. 识别中间表 → 标记为"消除"或"保留"
5. 识别 ENUM 列 → 提取枚举值列表
6. 对每个列按「SQL 列类型映射表」和「语义识别规则」确定 aPaaS 类型

**第二步：生成转换确认表**

以 Markdown 表格形式呈现给用户，**必须等待用户确认后才能执行创建**：

```markdown
## 转换结果确认

### 对象列表
| SQL 表名 | aPaaS 对象 api_name | 标签(zh_cn) | 处理方式 |
|---|---|---|---|
| customer | customer | 客户 | 创建 |
| order | order | 订单 | 创建 |
| order_item | order_item | 订单明细 | 创建 |
| customer_tag | — | — | ⚠️ 识别为中间表，不创建（在 customer 上加 tags lookup） |

### 字段转换明细
| 对象 | SQL 列 | SQL 类型 | → aPaaS 类型 | api_name | 说明 |
|---|---|---|---|---|---|
| customer | id | INT PK | — | — | 忽略（用系统 _id） |
| customer | name | VARCHAR(100) NOT NULL | text | name | required: true, max_length: 100 |
| customer | email | VARCHAR(200) | email | email | 语义识别为 email 类型 |
| customer | status | ENUM('active','inactive') | enum | status | 2 个选项 |
| order | customer_id | INT FK→customer | lookup | customer | 关联客户 |
| order | total | DECIMAL(10,2) | decimal | total | decimal_places: 2 |

### 需要确认的项
- [ ] customer.email: 推断为 `email` 类型，是否正确？还是保持 `text`？
- [ ] customer_tag 识别为中间表，是否正确？如果该表有额外业务字段请告知
- [ ] enum 选项的中文标签是否准确？

请确认或修改后，我将按照三阶段创建法执行。
```

**第三步：用户确认后执行**

用户确认后，按「多对象依赖分析与分阶段创建」章节的流程执行（1a 空壳 → 1b 基础字段 → 2 lookup → 3 reference_field）。

### 不可转换的 SQL 特性

以下 SQL 特性在 aPaaS 中无直接对应，需告知用户：

| SQL 特性 | aPaaS 处理方式 |
|---|---|
| 存储过程 / 触发器 | 不支持，需用应用逻辑实现 |
| 视图（VIEW） | 不支持，忽略 |
| 复合主键 | 不支持，aPaaS 用 `_id` 单列主键 |
| 复合唯一约束（多列联合） | 不支持单字段级 `unique` 无法表达联合唯一 |
| CHECK 约束 | 不直接支持，需在应用层校验 |
| 分区表 | 不支持，忽略 |
| 自定义函数 / 计算列 | 不支持 |

遇到这些特性时，在转换确认表中标注"⚠️ 不支持"并给出替代建议（如果有的话）。

## 多对象依赖分析与分阶段创建（核心策略）

当一个应用有多张数据表且互相关联时，**不能一次性创建带 lookup 的完整对象**。

### 问题：循环依赖

```
订单(order) --lookup--> 客户(customer)
客户(customer) --lookup--> 订单(order)   // 互相引用，谁先创建？
```

lookup 字段要求目标对象已存在，互相引用时直接创建必然失败。

### 解决：三阶段创建法

**阶段 1a — 创建空壳对象**：所有对象只建壳子，不传 fields（传了也会被忽略）。`display_name` 暂时指向 `_id`。

```typescript
// 阶段 1a：创建所有空壳
await client.schema.create({
    objects: [
        { api_name: 'customer', label: { zh_cn: '客户', en_us: 'Customer' },
          settings: { display_name: '_id' } },
        { api_name: 'order', label: { zh_cn: '订单', en_us: 'Order' },
          settings: { display_name: '_id' } }
    ]
});
```

**阶段 1b — 添加基础字段**：用 `schema.update` + `operator: 'add'` 给每个对象补上基础字段（text, bigint, decimal, enum 等不依赖其他对象的字段）。

```typescript
// 阶段 1b：补基础字段
await client.schema.update({
    objects: [
        { api_name: 'customer', fields: [
            { operator: 'add', api_name: 'name', label: { zh_cn: '客户名', en_us: 'Name' },
              type: { name: 'text', settings: { required: true, unique: false, case_sensitive: false, multiline: false, max_length: 200 } }, encrypt_type: 'none' }
        ]},
        { api_name: 'order', fields: [
            { operator: 'add', api_name: 'order_no', label: { zh_cn: '订单号', en_us: 'Order No' },
              type: { name: 'text', settings: { required: true, unique: true, case_sensitive: false, multiline: false, max_length: 50 } }, encrypt_type: 'none' }
        ]}
    ]
});
```

**阶段 2 — 补充 lookup 字段**：所有对象已存在，用 `schema.update` + `operator: 'add'` 给每个对象补上 lookup 字段。

```typescript
// 阶段 2：所有对象已存在，补 lookup
await client.schema.update({
    objects: [
        {
            api_name: 'order',
            fields: [
                { operator: 'add', api_name: 'customer', label: { zh_cn: '客户', en_us: 'Customer' },
                  type: { name: 'lookup', settings: { required: false, multiple: false, referenced_object_api_name: 'customer' } },
                  encrypt_type: 'none' }
            ]
        },
        {
            api_name: 'customer',
            fields: [
                { operator: 'add', api_name: 'latest_order', label: { zh_cn: '最近订单', en_us: 'Latest Order' },
                  type: { name: 'lookup', settings: { required: false, multiple: false, referenced_object_api_name: 'order' } },
                  encrypt_type: 'none' }
            ]
        }
    ]
});
```

**阶段 3 — 补充 reference_field**：lookup 就位后，添加引用字段。

```typescript
// 阶段 3：lookup 就位后，补 reference_field
await client.schema.update({
    objects: [{
        api_name: 'order',
        fields: [
            { operator: 'add', api_name: 'customer_name', label: { zh_cn: '客户名称', en_us: 'Customer Name' },
              type: { name: 'reference_field', settings: {
                  current_lookup_field_api_name: 'customer',
                  target_reference_field_api_name: 'name'
              } }, encrypt_type: 'none' }
        ]
    }]
});
```

### 依赖分析流程

拿到需求后，按此流程分析：

1. **列出所有对象和字段**，标记哪些字段是 lookup / lookup_multi / reference_field
2. **画出依赖关系**：lookup 的 `referenced_object_api_name` 指向谁
3. **分类到各阶段**：
   - 阶段 1a：`schema.create` 创建所有空壳对象（不传 fields）
   - 阶段 1b：`schema.update` 添加基础字段（text, bigint, float, date, datetime, enum, boolean, attachment, auto_number, richText, phone, avatar, email, region, decimal, multilingual）
   - 阶段 2：`schema.update` 添加 lookup / lookup_multi
   - 阶段 3：`schema.update` 添加 reference_field
4. **始终用此流程**，即使没有循环依赖也不要尝试在 `create` 中传 fields

### 删除顺序（逆向）

删除时必须反向操作：

1. **先删 reference_field**（依赖 lookup）
2. **再删 lookup / lookup_multi**（依赖目标对象）
3. **最后删对象本身**

### 删除所有对象（完整工作流）

清理环境或重建数据模型时，需要删除应用内所有自定义对象。流程如下：

```typescript
// 步骤 1：获取所有自定义对象（_ 开头为系统预置，不可删除）
const allObjects = await client.object.listWithIterator();
const customObjects = allObjects.items.filter(o => !o.apiName.startsWith('_'));
if (customObjects.length === 0) return;

// 步骤 2：收集依赖字段
const fieldsByType: Record<string, { object: string; field: string }[]> = { referenceField: [], lookup: [] };
for (const obj of customObjects) {
    const result = await client.object.metadata.fields({ object_name: obj.apiName });
    for (const field of result.data?.fields || []) {
        if (field.apiName.startsWith('_')) continue;
        const typeName = field.type?.name || field.type;
        if (typeName === 'referenceField' || typeName === 'lookup') {
            fieldsByType[typeName].push({ object: obj.apiName, field: field.apiName });
        }
    }
}

// 步骤 3：按依赖顺序删字段（reference_field → lookup）
for (const typeName of ['referenceField', 'lookup']) {
    const items = fieldsByType[typeName];
    if (items.length === 0) continue;
    const grouped: Record<string, { operator: 'remove'; api_name: string }[]> = {};
    for (const { object, field } of items) {
        (grouped[object] ??= []).push({ operator: 'remove', api_name: field });
    }
    await client.schema.update({
        objects: Object.entries(grouped).map(([api_name, fields]) => ({ api_name, fields }))
    });
}

// 步骤 4：删除所有对象
await client.schema.delete({ api_names: customObjects.map(o => o.apiName) });
```

> 删除后建议用 `verifyObjects()` 或 `client.object.listWithIterator()` 确认清理干净。

### 约束速记

- `reference_field` 只能引用 `multiple: false` 的 lookup
- `lookup_multi`（`multiple: true`）**不能**作为 reference_field 的引导字段
- 同一批 `schema.update` 中，add 的执行顺序不保证，不要在同一批里 add lookup 又 add 依赖它的 reference_field

## 失败恢复与幂等重跑

多阶段创建过程中，任意阶段都可能失败。以下是各阶段失败后的状态和恢复策略：

### 各阶段失败后的状态

| 失败点 | 已完成的状态 | 恢复策略 |
|--------|-------------|---------|
| 阶段 1a 失败 | 部分空壳对象可能已创建 | 重跑 1a，已存在的对象会报 `k_ec_000015`（含 "exist"），安全忽略 |
| 阶段 1b 失败 | 空壳对象存在，部分字段可能已添加 | 重跑 1b，已存在的字段会报错，可通过先查询 metadata 跳过已有字段 |
| 阶段 2 失败 | 基础字段已就位，部分 lookup 可能已添加 | 同上，查询后跳过已有 lookup |
| 阶段 3 失败 | lookup 已就位，部分 reference_field 可能已添加 | 同上，查询后跳过已有 reference_field |

### 幂等重跑模式

```typescript
// 查询已有字段，跳过已存在的
async function addFieldsIdempotent(objectName: string, fieldsToAdd: any[]) {
    const existing = await client.object.metadata.fields({ object_name: objectName });
    const existingNames = new Set(
        (existing.data?.fields || []).map((f: any) => f.apiName)
    );
    const newFields = fieldsToAdd.filter(f => !existingNames.has(f.api_name));
    if (newFields.length === 0) {
        console.log(`  [SKIP] ${objectName}: 所有字段已存在`);
        return;
    }
    const result = await client.schema.update({
        objects: [{ api_name: objectName, fields: newFields }]
    });
    checkResponse(result, `addFields(${objectName})`);
}
```

### 部分成功的处理

`schema.update` 可能在一批 10 个对象中只有部分成功。通过 `data.items[].status.code` 逐项检查，只重跑失败的对象：

```typescript
const result = await client.schema.update({ objects: batch });
const failed = (result.data?.items || [])
    .filter((item: any) => item.status?.code !== '0')
    .map((item: any) => item.api_name);
if (failed.length > 0) {
    console.warn(`部分失败: ${failed.join(', ')}，可针对这些对象重跑`);
}
```

## 常见错误与对策

| 错误 | 原因 | 修复 |
|---|---|---|
| **`update` 返回 `code: "0"` + `data: null`** | **⚠️ 静默失败**：字段 settings 缺少必填项（如 text 缺 `multiline`，auto_number 缺 `generation_method`），或同一批次中某个字段有此问题导致整批失败 | **始终使用 settings 模板中的完整字段**。检查方法：成功时返回 `data.items`，返回 `data: null` 即为失败 |
| `invalid generation_method value` | auto_number 字段未传 `generation_method` | 必须传 `generation_method: "random"` |
| `k_ec_000015 field type is required` | `replace` 时只传了 label 没传 type | replace 必须带完整 type（name + settings） |
| `k_ec_000015` + 含 "exist" | 对象已存在，重复创建 | 先查询是否存在，或安全忽略此错误 |
| `create` 返回成功但字段为空 | `schema.create` 静默忽略 fields | **必须用两步走**：先 create 空壳，再 update 添加字段 |
| 创建字段类型不识别 | 用了 metadata type（如 `number`） | 用 schema type（`float`） |
| `display_name` 报错 | 使用了 `_name`，或指向不存在的字段 | 创建空壳时先用 `_id`，字段就位后再更新 |
| lookup 创建失败 | 目标对象不存在 | 先创建目标对象 |
| reference_field 创建失败 | 引导 lookup 不存在或是 multi | 先创建 `multiple: false` 的 lookup |
| reference_field `field not found` | lookup 刚创建，系统索引延迟；或目标字段类型不支持引用（如 `avatar`） | 批量迁移时对 reference_field 失败做容错（打印错误但不中断），必要时加延迟重试 |

## 响应验证

每次 API 调用后必须检查**三层状态**：

1. **`result.code !== '0'`** — 请求级错误（参数格式问题）
2. **`result.code === '0' && result.data === null`** — ⚠️ **静默失败**（最危险：看起来成功，但字段未创建。原因：settings 缺必填项）
3. **`result.data.items[].status.code !== '0'`** — 单个对象级错误

> 上述三层检查已封装在 `scripts/run.ts` 的 `checkResponse(result, context)` 函数中，直接调用即可。

## 创建后验证

创建/更新对象后，调用 `scripts/run.ts` 的 `verifyObjects(['product', ...])` 验证：自动检查对象是否存在、列出自定义字段及类型、导出 Markdown 供人工审查。

## 执行脚本与目录结构

```bash
npm install && cp scripts/.env.example scripts/.env  # 填入凭据后执行：
npx ts-node scripts/run.ts
```

`scripts/run.ts` 自动加载凭据、初始化 client，内置工具函数：`checkResponse()`（三层响应验证）、`batchExecute()`（自动分批）、`verifyObjects()`（字段级验证）。

```
apaas-object-skill/
  SKILL.md                          # 主文档（Claude 读取此文件）
  references/
    FIELD_SCHEMA_RULES.md           # 字段类型映射与规则（人读版）
    field-schema-rules.ts           # 字段类型映射与规则（机器可读版，含 SQL 转换规则）
  scripts/
    run.ts                          # 执行脚本（凭据加载、client 初始化、工具函数）
    .env.example                    # 凭据配置模板
```
