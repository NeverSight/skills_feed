---
name: dedsiddd-dotnet-coding
description: 用于在 DedsiDDD + .NET 项目中，按统一约定生成 DDD/CQRS 常见代码骨架（领域模型、DTO、EF Core 映射、仓储、Commands、Queries、Controller）。
---

## 范围与目标
本 Skill 用于在 DedsiDDD + .NET 项目中生成可编译、可落地的代码骨架。

**冲突优先级**：本 SKILL 约定 > 现有仓库约定 > 一般 DDD/CQRS 习惯。

## 交互协议（强制）

- 信息不足先问（见"澄清问题清单"）
- 改造代码给"最小补丁"
- 按文件分组输出
- 占位符 `[Project]`/`[Entity]`/`[DbContext]` 必须替换为实际命名
- 依赖方向不可破坏

## 输入与输出

### 澄清问题清单
1. 模块边界：实体属于哪个模块？命名空间与目录？
2. 路由风格：Controller 使用 action route 还是资源路由？
3. 聚合信息：实体单/复数名、主键类型（默认 string/ULID）、是否聚合根
4. 字段清单：字段名/类型/必填/长度/默认值/enum/值对象
5. 关系与集合：一对多/多对多、集合唯一性约束、更新策略（增量 vs Clear+Add）
6. 数据库映射：表名、Schema、索引/唯一约束、是否软删
7. API 契约：需要哪些端点（Get/Paged/Create/Update/Delete/Export）
8. 返回结构：是否有统一的 ApiResponse/Result 包装？

### 缺省策略
- 主键：默认 `string`，生成方式 `Ulid.NewUlid().ToString()`
- 分页：使用 `DedsiPagedRequestDto`
- 更新集合：默认 Clear + Add
- 导出组件：仅当仓库已存在 MiniExcel 时提供落地代码

### 交付标准
- 明确的文件清单与落点（Domain/Infrastructure/UseCase/HttpApi）
- 每个文件的代码模板或最小变更补丁
- 所有公开入口包含 `CancellationToken` 并透传到 EF Core/仓储
- 分页查询顺序：筛选 → Count → 排序 →（非导出则分页）→ 投影 → ToList
- Controller 能编译并能调用 Query/Mediator；Command/Query 返回类型与 Controller 对齐

## 项目结构

### 架构分层
- **领域**（`src/[Project].Domain`）：核心领域对象、常量、领域模块
- **基础设施**（`src/[Project].Infrastructure`）：EF Core 持久化、DbContext、实体映射、仓储
- **用例**（`src/[Project].UseCase`）：CQRS 命令/查询与编排
- **HttpApi**（`src/[Project].HttpApi`）：暴露控制器
- **宿主**（`host/[Project].Host`）：ASP.NET Core Web 宿主

### 依赖关系
```
[Project].Host → [Project].HttpApi → [Project].UseCase → [Project].Domain
                                        ↓
                           [Project].Infrastructure → [Project].Domain
```

### 存放位置速查

| 生成块 | 放置项目 | 目录 | 典型文件 |
| --- | --- | --- | --- |
| 领域模型 | `src/[Project].Domain` | `[Entities]/` | `[Entity].cs` |
| DTO | `src/[Project].UseCase` | `[Entities]/Dtos/` | `[Entity]Dto.cs` / `[Entity]CreateUpdateDto.cs` |
| DbContext | `src/[Project].Infrastructure` | `EntityFrameworkCore/` | `[Project]DbContext.cs` |
| EF Core 映射 | `src/[Project].Infrastructure` | `EntityFrameworkCore/EntityConfigurations/` | `[Entity]Configuration.cs` |
| 仓储 | `src/[Project].Infrastructure` | `Repositories/` | `[Entity]Repository.cs` |
| Commands | `src/[Project].UseCase` | `[Entities]/CommandHandlers/` | `Create[Entity]CommandHandler.cs` |
| Queries | `src/[Project].UseCase` | `[Entities]/Queries/` | `[Entity]Query.cs` / `[Entity]PagedQuery.cs` |
| Controller | `src/[Project].HttpApi` | 随项目现有组织 | `[Entity]Controller.cs` |

### 最小交付清单
1. Domain：`[Entity].cs`
2. Infrastructure：`[Project]DbContext.cs` 增加 `DbSet<[Entity]>`、`[Entity]Configuration.cs`、`[Entity]Repository.cs`
3. UseCase：DTO、Command/Query
4. HttpApi：Controller + Requests（推荐）

## 通用约定

- **占位符**：`[Entity]` / `[Project]` / `[DbContext]` 按实际业务替换
- **文件聚合原则**：Command/Handler 同文件；Query 接口/实现同文件；Repository 接口/实现同文件
- **Enum 约束**：所有 `enum` 必须显式赋值，第一个业务值从 `1` 开始
- **CancellationToken**：所有公开 API/Query/Command 必须接收并透传到 EF Core/仓储
- **XML 注释**：Controller、Query 接口/实现、DTO 必须有 XML 注释；实现类可用 `/// <inheritdoc />`

## 推荐工作流

1. 澄清边界与不变式
2. 写领域模型（Domain）
3. 定义 DTO（Contract）
4. 配置 EF Core（DbContext + EntityConfiguration）
5. 生成仓储（Repository）
6. 实现 Commands（写侧）
7. 实现 Queries（读侧）
8. 实现 Controller（API 层）
9. 一致性检查

---

## 生成领域模型

### 规则
- 聚合根继承 `DedsiAggregateRoot<string>`
- 必须包含 `protected` 无参构造函数（供 ORM）
- 属性使用 `private set`
- 状态变更通过聚合根方法：`Change+属性名`、`Add+元素名`、`Remove+元素名`、`Clear+集合名`
- 入参校验：字符串 `Check.NotNullOrWhiteSpace`，引用类型 `Check.NotNull`，枚举值合法性检查
- 幂等性：新旧值相同直接返回
- 维护不变式：不满足时抛 `BusinessException`

### 模板
```csharp
using Volo.Abp;
using Dedsi.Ddd.Domain.Entities;

/// <summary>
/// [Entity]
/// </summary>
public class [Entity] : DedsiAggregateRoot<string>
{
    protected [Entity]() { }

    public [Entity](string id, string requiredField)
        : base(id)
    {
        ChangeRequiredField(requiredField);
        CreationTime = DateTime.Now;
    }

    public DateTime CreationTime { get; private set; }

    /// <summary>
    /// 中文注释
    /// </summary>
    public string RequiredField { get; private set; }

    public void ChangeRequiredField(string value)
    {
        RequiredField = Check.NotNullOrWhiteSpace(value, nameof(RequiredField));
    }

    public ICollection<[Child]> Children { get; private set; } = [];

    public void AddChild([Child] child)
    {
        Children.Add(Check.NotNull(child, nameof([Child])));
    }

    public void ClearChildren()
    {
        Children.Clear();
    }
}

/// <summary>
/// [Entity]
/// </summary>
public class [Child]
{
    public string [Entity]Id { get; private set; }

    protected [Child]() { }

    public [Child](string id, string requiredField)
        : base(id)
    {
        ChangeRequiredField(requiredField);
    }

    /// <summary>
    /// 中文注释
    /// </summary>
    public string RequiredField { get; private set; }

    public void ChangeRequiredField(string value)
    {
        RequiredField = Check.NotNullOrWhiteSpace(value, nameof(value));
    }
}
```

---

## 生成 DTO

### 规则
- 展示 DTO：`[Entity]Dto`，使用 `public get; set;`
- 创建/更新 DTO：`[Entity]CreateUpdateDto`，使用 `public get; set;`
- 每个字段/属性必须有 XML 注释
- DTO 不直接暴露领域对象类型（为集合/复杂对象单独定义 DTO）

### 模板
```csharp
/// <summary>
/// [Entity]Dto
/// </summary>
public class [Entity]Dto
{
    /// <summary>
    /// 标识
    /// </summary>
    public string Id { get; set; }

    /// <summary>
    /// 创建时间
    /// </summary>
    public DateTime CreationTime { get; set; }

    /// <summary>
    /// 必填字段
    /// </summary>
    public string RequiredField { get; set; }

    /// <summary>
    /// 可空字段
    /// </summary>
    public string? OptionalField { get; set; }

    /// <summary>
    /// 列表字段
    /// </summary>
    public IEnumerable<[Child]Dto> Children { get; set; } = [];
}

/// <summary>
/// [Entity]CreateUpdateDto
/// </summary>
public class [Entity]CreateUpdateDto
{
    /// <summary>
    /// 必填字段
    /// </summary>
    public string RequiredField { get; set; }

    /// <summary>
    /// 可空字段
    /// </summary>
    public string? OptionalField { get; set; }

    /// <summary>
    /// 列表字段
    /// </summary>
    public IEnumerable<[Child]CreateUpdateDto> Children { get; set; } = [];
}

/// <summary>
/// [Entity]PagedInputDto
/// </summary>
public class [Entity]PagedInputDto : DedsiPagedRequestDto
{
    /// <summary>
    /// 关键字
    /// </summary>
    public string? Keyword { get; set; }
}

/// <summary>
/// [Entity]PagedRowDto
/// </summary>
public class [Entity]PagedRowDto
{
    /// <summary>
    /// 主键
    /// </summary>
    public string Id { get; set; } = default!;

    /// <summary>
    /// 示例字段
    /// </summary>
    public string? Example { get; set; }
}

/// <summary>
/// [Entity]PagedResultDto
/// </summary>
public class [Entity]PagedResultDto : DedsiPagedResultDto<[Entity]PagedRowDto>;
```

---

## 配置数据库

### DbContext 规则
- 命名：聚合根复数形式（例如 `Risks`）
- 类型：`DbSet<聚合根>`
- 位置：`I[Project]DbContext` / `[Project]DbContext`
- 标注：`[ConnectionStringName([Project]DomainConsts.ConnectionStringName)]`
- 接口：`I[Project]DbContext : IDedsiEfCoreDbContext`
- 实现：`[Project]DbContext : DedsiEfCoreDbContext<[Project]DbContext>, I[Project]DbContext`
- OnModelCreating：空值校验 → `ApplyConfigurationsFromAssembly` → `base.OnModelCreating`

### EntityConfiguration 规则
- 每个实体一个配置类：`[Entity]Configuration`，放在 `EntityFrameworkCore/EntityConfigurations`
- `internal class`，实现 `IEntityTypeConfiguration<[EntityName]>`

### 模板
```csharp
// DbContext
using Dedsi.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Volo.Abp.Data;

namespace [Project].Infrastructure.EntityFrameworkCore;

[ConnectionStringName([Project]DomainConsts.ConnectionStringName)]
public interface I[Project]DbContext : IDedsiEfCoreDbContext
{
    DbSet<[Entity]> [Entities] { get; }
}

[ConnectionStringName([Project]DomainConsts.ConnectionStringName)]
public class [Project]DbContext(DbContextOptions<[Project]DbContext> options)
    : DedsiEfCoreDbContext<[Project]DbContext>(options), I[Project]DbContext
{
    public DbSet<[Entity]> [Entities] { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        ArgumentNullException.ThrowIfNull(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(typeof([Project]DbContext).Assembly);
        base.OnModelCreating(modelBuilder);
    }
}

// EntityConfiguration
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace [Project].Infrastructure.EntityFrameworkCore.EntityConfigurations;

internal class [Entity]Configuration : IEntityTypeConfiguration<[Entity]>
{
    public void Configure(EntityTypeBuilder<[Entity]> builder)
    {
        builder.ToTable("[Entities]", [Project]DomainConsts.DbSchemaName);
        builder.HasKey(e => e.Id);

        builder.Property(e => e.RequiredField)
            .IsRequired()
            .HasMaxLength(128);
    }
}
```

---

## 生成仓储

### 规则
- 接口：`I[Entity]Repository : IDedsiCqrsRepository<[Entity], KeyType>`
- 实现：`[Entity]Repository : DedsiDddEfCoreRepository<DbContext, [Entity], KeyType>`
- 接口和实现必须在同一个文件中
- 构造函数注入 `IDbContextProvider<DbContext>`

### 模板
```csharp
using Dedsi.Ddd.Domain.Repositories;
using Dedsi.EntityFrameworkCore.Repositories;
using Volo.Abp.EntityFrameworkCore;
using [Project].Infrastructure.EntityFrameworkCore;

namespace [Project].Infrastructure.Repositories;

/// <summary>
/// [Entity] 仓储
/// </summary>
public interface I[Entity]Repository : IDedsiCqrsRepository<[Entity], string>;

/// <summary>
/// [Entity] 仓储
/// </summary>
public class [Entity]Repository(IDbContextProvider<[Project]DbContext> dbContextProvider)
    : DedsiDddEfCoreRepository<[Project]DbContext, [Entity], string>(dbContextProvider), I[Entity]Repository;
```

---

## 生成命令 (Commands)

### 规则
- Create/Update/Delete 拆分为三个独立文件
- Command 与 Handler 必须在同文件
- 继承 `DedsiCommandHandler<Command, Result>`
- 全链路透传 `CancellationToken`

### 模板
```csharp
// Create
using Dedsi.Ddd.CQRS.CommandHandlers;
using Dedsi.Ddd.CQRS.Commands;

/// <summary>
/// 创建 [Entity] 命令
/// </summary>
public record Create[Entity]Command([Entity]CreateUpdateDto Dto) : DedsiCommand<string>;

/// <summary>
/// 创建 [Entity] 命令处理器
/// </summary>
public class Create[Entity]CommandHandler(I[Entity]Repository repository)
    : DedsiCommandHandler<Create[Entity]Command, string>
{
    public override async Task<string> Handle(Create[Entity]Command command, CancellationToken cancellationToken)
    {
        var domainId = Ulid.NewUlid().ToString();
        var domain = new [Entity](domainId, command.Dto.RequiredField);
        await repository.InsertAsync(domain, autoSave: true, cancellationToken);
        return domainId;
    }
}

/// <summary>
/// 更新 [Entity] 命令
/// </summary>
public record Update[Entity]Command(string Id, [Entity]CreateUpdateDto Dto) : DedsiCommand<bool>;

/// <summary>
/// 更新 [Entity] 命令处理器
/// </summary>
public class Update[Entity]CommandHandler(I[Entity]Repository repository)
    : DedsiCommandHandler<Update[Entity]Command, bool>
{
    public override async Task<bool> Handle(Update[Entity]Command command, CancellationToken cancellationToken)
    {
        var domain = await repository.GetAsync(e => e.Id == command.Id, true, cancellationToken);
        domain.ChangeRequiredField(command.Dto.RequiredField);
        await repository.UpdateAsync(domain, autoSave: true, cancellationToken);
        return true;
    }
}

// Delete
/// <summary>
/// 删除 [Entity] 命令
/// </summary>
public record Delete[Entity]Command(string Id) : DedsiCommand<bool>;

/// <summary>
/// 删除 [Entity] 命令处理器
/// </summary>
public class Delete[Entity]CommandHandler(I[Entity]Repository repository)
    : DedsiCommandHandler<Delete[Entity]Command, bool>
{
    public override async Task<bool> Handle(Delete[Entity]Command command, CancellationToken cancellationToken)
    {
        var domain = await repository.GetAsync(command.Id, true, cancellationToken);

        await repository.DeleteAsync(domain, true, cancellationToken);

        return true;
    }
}
```

---

## 生成查询 (Queries)

### 规则
- 接口与实现同文件
- 查询注入 DbContext 接口
- 分页查询必须 `AsNoTracking()`
- 固定顺序：筛选 → Count → 排序 →（非导出则分页）→ 投影 → ToList
- `id` 入参必须用于谓词
- Query 接口/实现/方法必须有 XML 注释

### 模板

#### 分页查询
```csharp
using Dedsi.Ddd.Application.Contracts.Dtos;
using Dedsi.Ddd.Domain.Queries;
using Microsoft.EntityFrameworkCore;
using Volo.Abp.Linq;

/// <summary>
/// [Entity] 分页查询
/// </summary>
/// <param name="[Project]DbContext"></param>
public class [Entity]PagedQuery(I[Project]DbContext [Project]DbContext) : IDedsiQuery
{
    /// <summary>
    /// [Entity] 分页条件查询
    /// </summary>
    /// <param name="input"></param>
    /// <param name="cancellationToken"></param>
    /// <returns></returns>
    public async Task<[Entity]PagedResultDto> PagedQueryAsync([Entity]PagedInputDto input, CancellationToken cancellationToken)
    {
        var query = [Project]DbContext
            .[Entities]
            .AsNoTracking()
            .WhereIf(!string.IsNullOrWhiteSpace(input.Keyword), e => e.RequiredField.Contains(input.Keyword!));

        var totalCount = await query.CountAsync(cancellationToken);

        query = query.OrderByDescending(e => e.CreationTime);
        if (!input.IsExport)
        {
            query = query.PageBy(input.GetSkipCount(), input.PageSize);
        }

        var items = await query
            .Select(e => new [Entity]PagedRowDto { Id = e.Id, Example = e.RequiredField })
            .ToListAsync(cancellationToken);

        return new [Entity]PagedResultDto { TotalCount = totalCount, Items = items };
    }
}
```

#### 单个查询
```csharp
using Dedsi.Ddd.Domain.Queries;

/// <summary>
/// [Entity] 查询
/// </summary>
/// <param name="dbContext"></param>
/// <param name="repository"></param>
public class [Entity]Query(
I[Project]DbContext [Project]DbContext,
I[Entity]Repository [Entity]Repository) : IDedsiQuery
{

    /// <summary>
    /// 获取详情
    /// </summary>
    /// <param name="id"></param>
    /// <param name="cancellationToken"></param>
    /// <returns></returns>
    public async Task<[Entity]Dto> GetAsync(string id, CancellationToken cancellationToken)
    {
        var domain = await [Entity]Repository.GetAsync(e => e.Id == id, true, cancellationToken);
        return new [Entity]Dto
        {
            Id = domain.Id,
            CreationTime = domain.CreationTime,
            RequiredField = domain.RequiredField,
            OptionalField = domain.OptionalField,
            Children = domain.Children.Select(c => new [Child]Dto { /* 字段映射 */ })
        };
    }
}
```

---

## 生成控制器 (Controller)

### 规则
- 继承项目基础控制器
- 注入 `I[Entity]Query`、`I[Entity]PagedQuery`、`IDedsiMediator`
- `CancellationToken` 使用 `HttpContext.RequestAborted`
- 路由风格跟随仓库现有 Controller
- Update Body 使用 `CreateUpdateDto`（写入契约），不使用 `Dto`（展示契约）
- 导出：仅当仓库已引用 MiniExcel 时落地代码

### Request 模型（推荐）
```csharp
/// <summary>
/// 创建请求对象
/// </summary>
public record Create[Entity]Request([Entity]CreateUpdateDto [Entity]);

/// <summary>
/// 修改请求对象
/// </summary>
public record Update[Entity]Request([Entity]CreateUpdateDto [Entity]);
```

### 模板
```csharp
using Dedsi.Ddd.CQRS.Mediators;
using Microsoft.AspNetCore.Mvc;
using MiniExcelLibs;
using MiniExcelLibs.OpenXml;

/// <summary>
/// [Entity]
/// </summary>
public class [Entity]Controller(
    [Entity]Query [Entity]Query,
    [Entity]PagedQuery [Entity]PagedQuery,
    IDedsiMediator dedsiMediator) : [Project]Controller
{
    /// <summary>
    /// 分页查询
    /// </summary>
    [HttpPost]
    public Task<[Entity]PagedResultDto> PagedQueryAsync([FromBody] [Entity]PagedInputDto input)
    {
        input.IsExport = false;
        return [Entity]PagedQuery.PagedQueryAsync(input, HttpContext.RequestAborted);
    }

    /// <summary>
    /// 导出 Excel
    /// </summary>
    [HttpPost("export")]
    public async Task<IActionResult> ExportExcelAsync([FromBody] [Entity]PagedInputDto input)
    {
        input.IsExport = true;
        var result = await [Entity]PagedQuery.PagedQueryAsync(input, HttpContext.RequestAborted);

        var stream = new MemoryStream();
        await stream.SaveAsAsync(result.Items, cancellationToken: HttpContext.RequestAborted);
        stream.Seek(0, SeekOrigin.Begin);

        return File(
            stream,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            $"[Entity]-{DateTime.Now:yyyyMMddHHmmss}.xlsx"
        );
    }

    /// <summary>
    /// 查询详情
    /// </summary>
    [HttpGet("{id}")]
    public Task<[Entity]Dto> GetAsync([FromRoute] string id)
        => [Entity]Query.GetAsync(id, HttpContext.RequestAborted);

    /// <summary>
    /// 创建
    /// </summary>
    [HttpPost]
    public Task<string> CreateAsync([FromBody] Create[Entity]Request request)
        => dedsiMediator.SendAsync(new Create[Entity]Command(request.[Entity]), HttpContext.RequestAborted);

    /// <summary>
    /// 修改
    /// </summary>
    [HttpPost("{id}")]
    public Task<bool> UpdateAsync([FromRoute] string id, [FromBody] Update[Entity]Request request)
        => dedsiMediator.SendAsync(new Update[Entity]Command(id, request.[Entity]), HttpContext.RequestAborted);

    /// <summary>
    /// 删除
    /// </summary>
    [HttpPost("{id}")]
    public Task<bool> DeleteAsync([FromRoute] string id)
        => dedsiMediator.SendAsync(new Delete[Entity]Command(id), HttpContext.RequestAborted);
}

/// <summary>
/// 创建请求对象
/// </summary>
public record Create[Entity]Request([Entity]CreateUpdateDto [Entity]);

/// <summary>
/// 修改请求对象
/// </summary>
public record Update[Entity]Request([Entity]CreateUpdateDto [Entity]);
```

---

## 常见坑与验收清单

### 常见坑
- Update 端点 Body 误用展示 `Dto`：必须用 `CreateUpdateDto`
- Query 忘记 `AsNoTracking()`
- 分页顺序错误：必须"筛选 → Count → 排序 →（非导出则分页）→ 投影 → ToList"
- `CancellationToken` 断链
- `id` 入参未用于谓词
- enum 未显式赋值

### 验收清单
1. 文件落点与依赖方向正确
2. Command/Handler、Query 接口/实现、Repository 接口/实现均同文件
3. Controller/Query/Command 显式接收并透传 `CancellationToken`
4. Create/Update/Delete 的返回类型与 Command 返回类型一致
5. Update/Delete 路由不冲突
6. PagedQuery 支持导出模式
7. Create/Update 的 Body 使用 `CreateUpdateDto`
8. 分页查询实现顺序正确
