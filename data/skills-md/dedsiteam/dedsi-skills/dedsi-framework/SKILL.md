---
name: dedsi-framework
description: 基于 DedsiFramework.md 的信息，提供 Dedsi Framework（ABP 扩展框架）的模块速查、接入步骤、常见用法与问题定位建议。
---

## 范围与目标

本 Skill 用于：
- 快速解释 Dedsi Framework 各类库的职责与核心类型（按模块）。
- 指导在 ABP 项目中如何引用/DependsOn/配置这些模块。
- 给出 CQRS、Repository、异常处理、ORM（EF Core/SqlSugar）、CAP、FastEndpoints 的典型用法与落地检查清单。

不在范围内：
- 推断/编造 Dedsi Framework 未在文档中描述的 API 行为与参数。
- 输出与现有项目约定冲突的强绑定代码（若仓库已有实现，以仓库为准）。

信息来源：工作区根目录 [DedsiFramework.md](../DedsiFramework.md)。

## 快速目录
- [模块速查](#模块速查)
- [ABP 接入清单](#abp-接入清单)
- [常用使用场景](#常用使用场景)
- [排错与对齐](#排错与对齐)

---

## 模块速查

> 下列内容是对文档中各类库与类型的“可检索速记”。当你需要定位“这个类型属于哪个库/应该在哪里用”时，优先从这里开始。

### 1) Dedsi.AspNetCore
**定位**：ASP.NET Core 扩展与中间件，增强 Web API 基础能力。

**核心类型**
- `DedsiAspNetCoreModule`：模块定义文件，配置依赖。
- `DedsiControllerBase`：控制器基类（继承 `AbpControllerBase`）。
  - 提供 `FileByExcel`、`FileByPdf` 便捷导出。
- `Middlewares/DedsiGlobalExceptionHandler`：全局异常处理中间件。
  - 可选：当你需要将错误响应统一为 `DedsiErrorData`（非 ABP 默认格式）时启用。
  - 捕获异常并统一返回 `DedsiErrorData` JSON。
  - 自动处理 `UserFriendlyException`、`BusinessException` 并提取错误码。
- `DedsiErrorData`：可选的错误响应结构封装（用于替代/兼容 ABP 默认错误响应）。
- `DedsiErrorMessage`：错误信息模型（Message、Code、ServiceTime）。

### 2) Dedsi.Ddd.Domain
**定位**：领域层基础扩展；增强审计、仓储、查询标记接口。

**核心类型**
- `DedsiDddDomainModule`：模块定义。
- `DedsiDddDomainConsts`：领域常量（例如默认 DB Schema）。
- 审计接口（扩展创建审计，含创建人姓名）
  - `Auditing/Contracts/IDedsiCreationAuditedObject`
  - `Auditing/Contracts/IDedsiMayHaveCreator`
  - `Auditing/Contracts/IHasCreationName`
- 查询标记
  - `Queries/IDedsiQuery`：标记接口，继承 `ITransientDependency`。
- 仓储接口
  - `Repositories/IDedsiCqrsRepository`：面向 CQRS 的仓储接口（Insert/Update/Delete 等）。
  - `Repositories/IDedsiRepository`：增强通用仓储接口。
    - `GetQueryableNoTrackingAsync`（无追踪查询）
    - `GetPagedListAsync`（分页查询）
    - `DeleteManyAsync`（批量删除）
    - `ExecuteSqlAsync`（执行原生 SQL）

### 3) Dedsi.Ddd.Domain.Shared
**定位**：领域共享项目（枚举、常量、共享对象）。

**核心类型**
- `DedsiDddDomainSharedModule`

### 4) Dedsi.Ddd.Application.Contracts
**定位**：应用服务契约层（DTO 与服务接口）。

**核心类型**
- `DedsiDddApplicationContractsModule`
- DTO
  - `Dtos/DedsiPagedRequestDto`：分页请求基类（PageIndex、PageSize、IsExport）。
  - `Dtos/DedsiPagedResultDto`：分页结果基类。
- `Services/IDedsiApplicationService`：应用服务基类接口。

### 5) Dedsi.Ddd.Application
**定位**：应用服务层基础实现。

**核心类型**
- `DedsiDddApplicationModule`
- `Services/DedsiApplicationService`：继承 ABP `ApplicationService` 并实现 `IDedsiApplicationService`。

### 6) Dedsi.Ddd.CQRS
**定位**：CQRS 核心库；集成 MediatR；提供命令/事件记录能力。

**核心类型**
- `DedsiDddCqrsModule`
- `DedsiDddCqrsConsts`

**命令/事件记录（Recorders）**
- `CommandEventRecorder`：记录实体。
- `CqrsCeRecorder`：记录服务实现（调用 Repository 保存）。
- `ICqrsCeRecorder`：记录服务接口。
- `ICommandEventRecorderRepository`：记录仓储接口。
- `LocalCommandEventRecorderRepository`：本地记录仓储实现（开发/日志）。

**命令处理（Handlers）**
- `DedsiCommandHandler`：命令处理器基类（注入 Logger、CurrentUser 等常用服务）。
- `IDedsiCommandHandler`

**命令（Commands）**
- `DedsiCommand`：命令基类（含 `CommandId`）。
- `DedsiCommandId`：命令 ID 值对象。
- `IDedsiCommand`

**事件总线（EventBus）**
- `DedsiEvent`、`DedsiEventId`、`IDedsiEvent`
- `DedsiLocalEventBus`：自定义本地事件总线；重写 `PublishAsync` 以自动记录事件日志。

**中介者（Mediators）**
- `DedsiMediator`：封装 MediatR；发送命令前后自动记录日志。
- `IDedsiMediator`

### 7) Dedsi.EntityFrameworkCore
**定位**：EF Core 集成；实现 Dedsi.Ddd.Domain 的仓储接口；并提供 Dapper 集成。

**核心类型**
- `DedsiEntityFrameworkCoreModule`
- DbContext
  - `EntityFrameworkCore/DedsiEfCoreDbContext`
  - `EntityFrameworkCore/IDedsiEfCoreDbContext`
- `PropertySetters/DedsiAuditPropertySetter`：自动填充 `CreatorName`。
- 查询基类
  - `Queries/DedsiDapperQuery`
  - `Queries/DedsiEfCoreQuery`：提供 `GetNoTrackingQueryableAsync`。
- 仓储实现
  - `Repositories/DedsiDddEfCoreRepository`：`IDedsiCqrsRepository` 的 EF Core 实现。
  - `Repositories/DedsiEfCoreRepository`：`IDedsiRepository` 的 EF Core 实现（分页、批量删除等）。

### 8) Dedsi.SqlSugar
**定位**：SqlSugar ORM 集成；提供另一种数据访问方式。

**核心类型**
- `DedsiSqlSugarModule`
- `Extensions/DedsiSqlSugarExtensions`：在模块配置中注册 SqlSugar（SqlServer、MySql）。
- `Queries/DedsiSqlSugarQuery`：基于 SqlSugar 的查询基类，实现 `IDedsiQuery`。

### 9) Dedsi.Core
**定位**：核心模块（最基础定义）。
- `DedsiCoreModule`

### 10) Dedsi.CAP
**定位**：集成 DotNetCore.CAP，处理分布式事务与消息队列。
- `DedsiCapModule`

### 11) Dedsi.FastEndpoints
**定位**：集成 FastEndpoints，提供轻量级 API 端点开发方式。
- `DedsiFastEndpointsModule`

### 12) Dedsi.CleanArchitecture.*（Domain/HttpApi/Infrastructure）
**定位**：更像是整洁架构（Clean Architecture）模板/示例结构，不一定属于框架“核心能力”。

**核心类型**
- `Dedsi.CleanArchitecture.Domain`
  - `DedsiCleanArchitectureDomainModule`
  - `DedsiCleanArchitectureDomainConsts`
- `Dedsi.CleanArchitecture.HttpApi`
  - `DedsiCleanArchitectureHttpApiModule`
- `Dedsi.CleanArchitecture.Infrastructure`
  - `DedsiCleanArchitectureInfrastructureModule`

---

## ABP 接入清单

> 目标：把 Dedsi Framework 当作 ABP 模块集合接入。不同项目的模块装配点可能在 Host / HttpApi / Application 等层；以你的解决方案分层为准。

### 1) 选择你需要的模块
- Web API（异常处理/导出）→ `Dedsi.AspNetCore`
- DDD 基础（审计接口/仓储接口/查询标记）→ `Dedsi.Ddd.Domain` + `Dedsi.Ddd.Domain.Shared`
- 应用服务 → `Dedsi.Ddd.Application.Contracts` + `Dedsi.Ddd.Application`
- CQRS（MediatR + 记录）→ `Dedsi.Ddd.CQRS`
- EF Core 仓储实现 + Dapper Query → `Dedsi.EntityFrameworkCore`
- SqlSugar Query → `Dedsi.SqlSugar`
- 分布式事务/消息 → `Dedsi.CAP`
- FastEndpoints → `Dedsi.FastEndpoints`

### 2) 在 ABP Module 上声明 DependsOn（模板）
> 具体模块类名来自文档；实际命名空间/包引用以你的项目引用为准。

```csharp
using Volo.Abp.Modularity;

[DependsOn(
    typeof(DedsiAspNetCoreModule),
    typeof(DedsiDddDomainModule),
    typeof(DedsiDddDomainSharedModule),
    typeof(DedsiDddApplicationContractsModule),
    typeof(DedsiDddApplicationModule),
    typeof(DedsiDddCqrsModule),
    typeof(DedsiEntityFrameworkCoreModule)
)]
public class YourProjectModule : AbpModule;

// 如果需要可编译示例，使用：
// public class YourProjectModule : AbpModule
// {
// }
```

### 3) 异常/错误响应策略（推荐）
- **优先**使用 ABP 默认异常处理与错误响应（项目的既有格式为准）。
- **可选**：如果前端/调用方必须使用 `DedsiErrorData` 作为统一错误契约，再启用 `DedsiGlobalExceptionHandler`。
- 注意：`DedsiGlobalExceptionHandler` 属于“替换/包裹默认输出”的中间件，注册顺序可能改变最终返回格式；若项目已有 ABP 统一错误返回约定，优先保持一致。

### 4) 审计（CreatorName）启用检查（EF Core）
- 若你使用 EF Core 集成：确认 `DedsiAuditPropertySetter` 生效。
- 期望行为：实体实现/包含 `CreatorName` 时，在创建时自动填充。

---

## 常用使用场景

### 场景 A：统一 API 错误返回（优先 ABP）
**目标**：错误响应格式与项目 ABP 约定保持一致；仅在需要时切换到 `DedsiErrorData`。

落地策略（二选一）：
- **推荐：ABP 默认错误响应**
  - 保持 ABP 的异常处理与错误返回，不额外接管格式。
  - 业务层使用 `BusinessException` / `UserFriendlyException` 表达可预期错误（并携带错误码/消息）。
- **可选：DedsiErrorData 错误响应**
  - 仅当调用方明确要求 `DedsiErrorData` 契约时，在 Host 管线启用 `DedsiGlobalExceptionHandler`。
  - 启用后预期：异常统一返回 `DedsiErrorData` JSON（Message/Code/ServiceTime）。

### 场景 B：Controller 导出文件
**目标**：快速导出 Excel/PDF。

落地步骤：
- Controller 继承 `DedsiControllerBase`。
- 调用 `FileByExcel` / `FileByPdf`（参数与具体生成逻辑以框架实现为准）。

### 场景 C：CQRS + 自动记录（命令/事件）
**目标**：命令与事件在发送/发布时自动记录。

要点：
- 发命令：优先使用 `DedsiMediator`（而非直接使用 MediatR 的默认接口），以便“发送前后自动记录”。
- 发事件：使用 `DedsiLocalEventBus` 发布事件，以便 `PublishAsync` 自动记录事件日志。
- 记录落地：通过 `ICqrsCeRecorder` + `ICommandEventRecorderRepository`（可选本地实现 `LocalCommandEventRecorderRepository`）。

### 场景 D：Repository/Query 的统一抽象
**目标**：读写分离与通用数据访问能力统一。

策略建议：
- 写侧（命令）使用 `IDedsiCqrsRepository` / 其 EF Core 实现 `DedsiDddEfCoreRepository`。
- 读侧（查询）使用 `IDedsiQuery` 标记，并选择：
  - EF Core：继承/使用 `DedsiEfCoreQuery` 获取无追踪 IQueryable（`GetNoTrackingQueryableAsync`）。
  - Dapper：使用 `DedsiDapperQuery`。
  - SqlSugar：使用 `DedsiSqlSugarQuery`。

### 场景 E：分页/批量操作/原生 SQL
**目标**：在通用仓储上统一分页、批量删除、执行 SQL。

要点：
- 使用 `IDedsiRepository`（或其实现 `DedsiEfCoreRepository`）提供：
  - `GetPagedListAsync`
  - `DeleteManyAsync`
  - `ExecuteSqlAsync`

---

## 排错与对齐

### 1) “不知道该引用哪个库”
- 先查“模块速查”定位类型所在模块。
- 再检查你的项目是否引用了对应 NuGet 包/项目引用，以及 ABP `DependsOn` 是否添加。

### 2) “异常没有变成 DedsiErrorData”
先确认你到底期望哪一种格式：
- 若**期望 ABP 默认错误响应**：不要启用（或移除）`DedsiGlobalExceptionHandler`；并检查是否有自定义中间件/过滤器接管了异常输出。
- 若**期望 DedsiErrorData**：检查 `DedsiGlobalExceptionHandler` 是否注册、顺序是否在路由/终结点之前；并检查业务层是否抛出了 `BusinessException` / `UserFriendlyException`（便于错误码提取）。

### 3) “CreatorName 没有自动填充”
- 仅在 EF Core 集成链路下，检查 `DedsiAuditPropertySetter` 是否启用。
- 检查实体是否实现了文档提到的创建审计相关接口或包含 `CreatorName` 字段。

### 4) “CQRS 记录没有落库/没有输出”
- 发命令是否通过 `DedsiMediator`，发事件是否通过 `DedsiLocalEventBus`。
- `ICqrsCeRecorder` 与 `ICommandEventRecorderRepository` 是否有实现并完成 DI 注册。
- 开发期可先切换到 `LocalCommandEventRecorderRepository` 验证记录链路（如果项目允许）。

---

## 交付物
- 本 Skill 仅用于解释/指导 Dedsi Framework 使用；如需我基于你具体仓库生成/调整实际代码（模块装配、管线注册、CQRS 示例等），请提供对应项目结构或让我检索解决方案目录。
