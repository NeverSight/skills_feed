---
name: cleanddd-dotnet-coding
description: 在 CleanDDD 项目中落地已建模的需求（聚合/命令/查询/API 端点（Endpoints）/事件/仓储/配置/测试）的编码指南；用于编写或修改业务功能、端点与数据访问时
---

## 使用时机
- 在本仓库编写/修改业务功能、命令、查询、端点、集成事件、仓储、实体配置或相关测试时加载。

## 前置输入

- 建模设计：已完成 CleanDDD 需求分析与建模，获得聚合、命令、查询、事件等设计文档。

## 开始前快速检查
- 是否已有 cleanddd-modeling 的聚合/命令/事件/API 端点（Endpoints）清单，缺失先补齐。
- 确认聚合边界与不变式；命名统一 PascalCase，枚举固定拼写。
- 约定：命令处理器不显式 SaveChanges；跨聚合交互用领域事件/集成事件，禁直接跨聚合更新。

## 通用原则
- 优先用主构造函数，所有 IO/仓储/EF 调用使用 async/await 并传递 CancellationToken。
- 严格分层：Web → Infrastructure → Domain；聚合与实体发布领域事件，命令处理器不显式 SaveChanges。
- 强类型 ID 由 EF 值生成器提供；构造函数不设置 ID，直接使用类型实例，避免 .Value。
- 业务异常使用 KnownException；FastEndpoints 用特性配置，不使用 Configure()；IMediator 构造注入，使用 Send.OkAsync/CreatedAsync/NoContentAsync 与 .AsResponseData()。

## 推荐工作流
1) 聚合与实体 → 2) 领域事件 → 3) 仓储与实体配置 → 4) 命令+验证器+处理器 → 5) 查询+验证器+处理器 → 6) API 端点（Endpoints） → 7) 领域事件处理器 → 8) 集成事件/转换器/处理器 → 9) 测试。

## 目录结构
- Domain：src/ProjectName.Domain/（AggregatesModel/{Aggregate}Aggregate，DomainEvents）。
- Infrastructure：src/ProjectName.Infrastructure/（Repositories，EntityConfigurations，ApplicationDbContext）。
- Web：src/ProjectName.Web/Application/（Commands，Queries，DomainEventHandlers，IntegrationEvents，IntegrationEventConverters，IntegrationEventHandlers）；Endpoints。
- Tests：test/* 对应各层。

## 统一命名与放置约定
- 命名风格：全部使用 PascalCase；record/class/接口按 .NET 惯例；事件使用过去式。
- 强类型 ID：命名为 {Entity}Id，定义为 `public partial record`，与实体/聚合同文件。
- 文件命名：
    - 命令：{Action}{Entity}Command.cs；同文件包含验证器与处理器。
    - 查询：{Action}{Entity}Query.cs；同文件包含响应/DTO、验证器与处理器。
    - 端点：{Action}{Entity}Endpoint.cs；每文件一个端点。
    - 仓储：{Aggregate}Repository.cs；同文件放接口与实现。
    - 实体配置：{Entity}EntityTypeConfiguration.cs。
    - 领域事件：{Aggregate}DomainEvents.cs；可包含该聚合的多个事件。
    - 集成事件：{Entity}{Action}IntegrationEvent.cs。
    - 集成事件转换器：{Entity}{Action}IntegrationEventConverter.cs。
    - 集成事件处理器：{IntegrationEvent}HandlerFor{Action}.cs。
    - 领域事件处理器：{DomainEvent}DomainEventHandlerFor{Action}.cs。
    - DbContext：ApplicationDbContext.cs。
- 放置目录：
    - 聚合/实体/领域事件：src/ProjectName.Domain/AggregatesModel/{Aggregate}Aggregate 与 src/ProjectName.Domain/DomainEvents。
    - 仓储与配置：src/ProjectName.Infrastructure/Repositories 与 src/ProjectName.Infrastructure/EntityConfigurations。
    - 应用层：src/ProjectName.Web/Application/{Commands|Queries|DomainEventHandlers|IntegrationEvents|IntegrationEventConverters|IntegrationEventHandlers}。
    - 端点：src/ProjectName.Web/Endpoints/{Module}/。
- 单文件合并约定：命令/查询将验证器、处理器与响应（如有）合并至同一文件；仓储接口与实现同文件；其余类型一类一文件。

## 聚合
- 命名规则：聚合根无需 “Aggregate” 后缀；子实体遵循实体命名。
- 目录：src/ProjectName.Domain/AggregatesModel/{Aggregate}Aggregate。
- 文件名：{Entity}.cs（与 `{Entity}Id` 同文件）。
- 实现要点：
    - 聚合根继承 Entity<TId> + IAggregateRoot，protected 无参构造。
    - 属性 private set，默认值显式设置；包含 Deleted 与 RowVersion。
    - 状态变更时使用 this.AddDomainEvent() 发布领域事件。
    - 强类型 ID 实现 IGuidStronglyTypedId（优先）或 IInt64StronglyTypedId，由 EF 值生成器生成。
    - 子实体继承 Entity<TId> + IEntity，并提供无参构造。

示例：User 聚合根与强类型 ID
```csharp
namespace ProjectName.Domain.AggregatesModel.UserAggregate;

public partial record UserId : IGuidStronglyTypedId;

public class User : Entity<UserId>, IAggregateRoot
{
    protected User() { }

    public User(string name, string email)
    {
        Name = name;
        Email = email;
        this.AddDomainEvent(new UserCreatedDomainEvent(this));
    }

    public string Name { get; private set; } = string.Empty;
    public string Email { get; private set; } = string.Empty;
    public Deleted Deleted { get; private set; } = new();
    public RowVersion RowVersion { get; private set; } = new(0);

    public void ChangeEmail(string email)
    {
        Email = email;
        this.AddDomainEvent(new UserEmailChangedDomainEvent(this));
    }
}
```

## 领域事件
- 命名规则：{Entity}{Action}DomainEvent（过去式），使用 record，类型实现 IDomainEvent。
- 目录：src/ProjectName.Domain/DomainEvents。
- 文件名：{Aggregate}DomainEvents.cs（同聚合的多个事件可合并）。
- 实现要点：仅作为载体，不含业务逻辑。

示例：User 领域事件
```csharp
namespace ProjectName.Domain.DomainEvents;

public record UserCreatedDomainEvent(User User) : IDomainEvent;
public record UserEmailChangedDomainEvent(User User) : IDomainEvent;
```

## 命令
- 命名规则：命令 record 为 {Action}{Entity}Command；返回类型使用 ICommand<TResponse>，无返回使用 ICommand。
- 目录：src/ProjectName.Web/Application/Commands/{Module}s。
- 文件名：{Action}{Entity}Command.cs（同文件包含验证器与处理器）。
- 实现要点：
    - 处理器实现 ICommandHandler（或泛型版本）。
    - 使用仓储读取/持久化聚合；全异步并传递 CancellationToken。
    - 使用 KnownException 表达业务异常；不手动调用 SaveChanges/UpdateAsync。

示例：创建用户命令
```csharp
using ProjectName.Domain.AggregatesModel.UserAggregate;

namespace ProjectName.Web.Application.Commands.Users;

public record CreateUserCommand(string Name, string Email) : ICommand<UserId>;

public class CreateUserCommandValidator : AbstractValidator<CreateUserCommand>
{
    public CreateUserCommandValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(50);
        RuleFor(x => x.Email).NotEmpty().EmailAddress().MaximumLength(100);
    }
}

public class CreateUserCommandHandler(IUserRepository userRepository)
    : ICommandHandler<CreateUserCommand, UserId>
{
    public async Task<UserId> Handle(CreateUserCommand command, CancellationToken cancellationToken)
    {
        if (await userRepository.EmailExistsAsync(command.Email, cancellationToken))
            throw new KnownException("邮箱已存在");

        var user = new User(command.Name, command.Email);
        await userRepository.AddAsync(user, cancellationToken);
        return user.Id;
    }
}
```

## 查询
- 命名规则：{Action}{Entity}Query；返回 IQuery<T> 或 IPagedQuery<T>。
- 目录：src/ProjectName.Web/Application/Queries/{Module}s。
- 文件名：{Action}{Entity}Query.cs（同文件包含响应/DTO、验证器与处理器）。
- 实现要点：
    - 处理器实现 IQueryHandler；直接使用 ApplicationDbContext 查询。
    - 全异步并传递 CancellationToken；使用投影、WhereIf/OrderByIf/ToPagedDataAsync。
    - 分页使用 PagedData<T>，提供默认排序。
    - 禁用仓储与跨聚合 Join；无副作用。
    - 输出类型可为 {Entity}Response 或 DTO。

示例：查询用户
```csharp
using ProjectName.Domain.AggregatesModel.UserAggregate;
using ProjectName.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace ProjectName.Web.Application.Queries.Users;

public record GetUserQuery(UserId UserId) : IQuery<UserDto>;

public class GetUserQueryValidator : AbstractValidator<GetUserQuery>
{
    public GetUserQueryValidator()
    {
        RuleFor(x => x.UserId).NotEmpty();
    }
}

public class GetUserQueryHandler(ApplicationDbContext context)
    : IQueryHandler<GetUserQuery, UserDto>
{
    public async Task<UserDto> Handle(GetUserQuery request, CancellationToken cancellationToken)
    {
        return await context.Users
            .Where(x => x.Id == request.UserId)
            .Select(x => new UserDto(x.Id, x.Name, x.Email))
            .FirstOrDefaultAsync(cancellationToken)
            ?? throw new KnownException($"未找到用户，UserId = {request.UserId}");
    }
}

public record UserDto(UserId Id, string Name, string Email);
```

## API 端点（Endpoints）
- 命名规则：{Action}{Entity}Endpoint；请求/响应为 {Action}{Entity}Request/{Action}{Entity}Response（不使用 DTO）。
- 目录：src/ProjectName.Web/Endpoints/{Module}。
- 文件名：{Action}{Entity}Endpoint.cs（每文件一个端点）。
- 实现要点：
    - 使用属性路由/权限（[HttpPost]/[AllowAnonymous]/[Tags]）。
    - HandleAsync 通过 mediator 发送命令/查询；Send.OkAsync/CreatedAsync/NoContentAsync + .AsResponseData()。
    - 请求/响应可直接使用强类型 ID，避免解包 .Value；不使用 Configure()。

示例：创建用户 API 端点（Endpoint）
```csharp
using ProjectName.Domain.AggregatesModel.UserAggregate;
using ProjectName.Web.Application.Commands.Users;
using Microsoft.AspNetCore.Authorization;

namespace ProjectName.Web.Endpoints.Users;

public record CreateUserRequest(string Name, string Email);
public record CreateUserResponse(UserId UserId);

[Tags("Users")]
[HttpPost("/api/users")]
[AllowAnonymous]
public class CreateUserEndpoint(IMediator mediator)
    : Endpoint<CreateUserRequest, ResponseData<CreateUserResponse>>
{
    public override async Task HandleAsync(CreateUserRequest req, CancellationToken ct)
    {
        var id = await mediator.Send(new CreateUserCommand(req.Name, req.Email), ct);
        await Send.OkAsync(new CreateUserResponse(id).AsResponseData(), ct);
    }
}
```

## 领域事件处理器
- 命名规则：{DomainEvent}DomainEventHandlerFor{Action}。
- 目录：src/ProjectName.Web/Application/DomainEventHandlers。
- 文件名：{Name}.cs（每文件一个处理器）。
- 实现要点：
    - 实现 IDomainEventHandler<T>，方法签名 Handle(TEvent, CancellationToken)。
    - 通过 mediator 发送命令驱动聚合，不直接改 Db；遵守事务/取消。
    - 主构造函数注入依赖。

示例：领域事件处理器触发命令
```csharp
using ProjectName.Domain.DomainEvents;
using ProjectName.Web.Application.Commands.Users;

namespace ProjectName.Web.Application.DomainEventHandlers;

public class UserCreatedDomainEventHandlerForSendWelcome(IMediator mediator)
    : IDomainEventHandler<UserCreatedDomainEvent>
{
    public async Task Handle(UserCreatedDomainEvent domainEvent, CancellationToken cancellationToken)
    {
        var command = new SendWelcomeEmailCommand(domainEvent.User.Id, domainEvent.User.Email, domainEvent.User.Name);
        await mediator.Send(command, cancellationToken);
    }
}
```

## 仓储
- 命名规则：接口 I{Aggregate}Repository；实现 {Aggregate}Repository。
- 目录：src/ProjectName.Infrastructure/Repositories。
- 文件名：{Aggregate}Repository.cs（接口与实现同文件）。
- 实现要点：
    - 接口继承 IRepository<TEntity, TKey>；实现继承 RepositoryBase<TEntity, TKey, ApplicationDbContext>。
    - DbContext 属性访问 DbSet；优先使用基类默认方法，避免重复实现。
    - 由框架自动完成依赖注入注册。

示例：用户仓储
```csharp
using ProjectName.Domain.AggregatesModel.UserAggregate;

namespace ProjectName.Infrastructure.Repositories;

public interface IUserRepository : IRepository<User, UserId>
{
    Task<bool> EmailExistsAsync(string email, CancellationToken cancellationToken = default);
}

public class UserRepository(ApplicationDbContext context)
    : RepositoryBase<User, UserId, ApplicationDbContext>(context), IUserRepository
{
    public async Task<bool> EmailExistsAsync(string email, CancellationToken cancellationToken = default)
    {
        return await DbContext.Users.AnyAsync(x => x.Email == email, cancellationToken);
    }
}
```

## 实体配置
- 命名规则：{Entity}EntityTypeConfiguration。
- 目录：src/ProjectName.Infrastructure/EntityConfigurations。
- 文件名：{Entity}EntityTypeConfiguration.cs。
- 实现要点：
    - 实现 IEntityTypeConfiguration<T>。
    - 必须配置主键；字符串列设置 MaxLength；必填列 IsRequired；字段添加 HasComment 注释；按需要添加索引。
    - 强类型 ID：IGuidStronglyTypedId → UseGuidVersion7ValueGenerator；IInt64StronglyTypedId → UseSnowFlakeValueGenerator；RowVersion 无需配置；不要自定义转换器。

示例：用户实体配置
```csharp
using ProjectName.Domain.AggregatesModel.UserAggregate;

namespace ProjectName.Infrastructure.EntityConfigurations;

public class UserEntityTypeConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("Users");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Id)
            .UseGuidVersion7ValueGenerator()
            .HasComment("用户标识");

        builder.Property(x => x.Name)
            .IsRequired()
            .HasMaxLength(50)
            .HasComment("用户姓名");

        builder.Property(x => x.Email)
            .IsRequired()
            .HasMaxLength(100)
            .HasComment("用户邮箱");

        builder.HasIndex(x => x.Email).IsUnique();
    }
}
```

## DbContext
- 命名规则：ApplicationDbContext。
- 目录：src/ProjectName.Infrastructure。
- 文件名：ApplicationDbContext.cs。
- 实现要点：
    - 添加聚合 DbSet 属性（`public DbSet<T> Name => Set<T>();`）。
    - 通过 ApplyConfigurationsFromAssembly 自动应用实体配置。

示例：DbSet 注册
```csharp
using ProjectName.Domain.AggregatesModel.UserAggregate;

namespace ProjectName.Infrastructure;

public partial class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options, IMediator mediator)
    : AppDbContextBase(options, mediator)
{
    public DbSet<User> Users => Set<User>();
}
```

## 集成事件
- 命名规则：{Entity}{Action}IntegrationEvent（record）。
- 目录：src/ProjectName.Web/Application/IntegrationEvents。
- 文件名：{Entity}{Action}IntegrationEvent.cs。
- 实现要点：不可变；不直接引用聚合实例，避免敏感信息；复杂类型同文件使用 record。

示例：用户创建集成事件
```csharp
using ProjectName.Domain.AggregatesModel.UserAggregate;

namespace ProjectName.Web.Application.IntegrationEvents;

public record UserCreatedIntegrationEvent(UserId UserId, string Name, string Email, DateTime CreatedTime);
```

## 集成事件转换器
- 命名规则：{Entity}{Action}IntegrationEventConverter。
- 目录：src/ProjectName.Web/Application/IntegrationEventConverters。
- 文件名：{Entity}{Action}IntegrationEventConverter.cs。
- 实现要点：实现 IIntegrationEventConverter<TDomainEvent, TIntegrationEvent>，将领域事件映射为集成事件；使用 record。

示例：领域事件到集成事件
```csharp
using ProjectName.Domain.DomainEvents;
using ProjectName.Web.Application.IntegrationEvents;

namespace ProjectName.Web.Application.IntegrationEventConverters;

public class UserCreatedIntegrationEventConverter
    : IIntegrationEventConverter<UserCreatedDomainEvent, UserCreatedIntegrationEvent>
{
    public UserCreatedIntegrationEvent Convert(UserCreatedDomainEvent domainEvent)
    {
        var user = domainEvent.User;
        return new UserCreatedIntegrationEvent(user.Id, user.Name, user.Email, DateTime.UtcNow);
    }
}
```

## 集成事件处理器
- 命名规则：{IntegrationEvent}HandlerFor{Action}。
- 目录：src/ProjectName.Web/Application/IntegrationEventHandlers。
- 文件名：{Name}.cs（每文件一个处理器）。
- 实现要点：实现 IIntegrationEventHandler<T>，在 HandleAsync 中通过命令驱动聚合，不直接修改 Db；主构造函数注入依赖。

示例：处理集成事件
```csharp
using ProjectName.Web.Application.Commands.Users;
using ProjectName.Web.Application.IntegrationEvents;

namespace ProjectName.Web.Application.IntegrationEventHandlers;

public class UserCreatedIntegrationEventHandlerForSendWelcomeEmail(
    ILogger<UserCreatedIntegrationEventHandlerForSendWelcomeEmail> logger,
    IMediator mediator)
    : IIntegrationEventHandler<UserCreatedIntegrationEvent>
{
    public async Task HandleAsync(UserCreatedIntegrationEvent integrationEvent, CancellationToken cancellationToken)
    {
        logger.LogInformation("发送欢迎邮件：{UserId}", integrationEvent.UserId);
        var command = new SendWelcomeEmailCommand(integrationEvent.UserId, integrationEvent.Email, integrationEvent.Name);
        await mediator.Send(command, cancellationToken);
    }
}
```

## 单元测试
- 命名规则：{Method}_{Scenario}_{Expected}。
- 目录：test/ProjectName.{Layer}.Tests/。
- 文件名：{Entity}Tests.cs（或按模块拆分）。
- 实现要点：
    - 采用 AAA 模式；单测单场景；覆盖正常/异常、领域事件、状态/不变量、边界。
    - 使用 Theory/InlineData；强类型 ID 直接 new 比较；时间采用相对比较（>= 等）。
    - 使用 GetDomainEvents() 校验事件类型与数量；可用工厂/Builder 生成测试数据。

## 提交前自检
- 命令/查询/处理器均为 async，传递 CancellationToken；未出现 SaveChanges/UpdateAsync 手动调用。
- 领域事件发布完整，处理器不直接跨聚合改数据；集成事件无聚合引用，包含必要审计信息。
- API 端点仅调用 mediator；请求/响应与强类型 ID 不解包 .Value；路由/标签/鉴权正确。查询输出允许使用 Response 或 DTO。
- EF 配置包含主键、长度、必填、注释；强类型 ID 使用标准值生成器。

示例：聚合单测
```csharp
public class UserTests
{
    [Fact]
    public void Constructor_ShouldRaiseCreatedEvent()
    {
        var user = new User("Alice", "alice@example.com");

        Assert.Equal("Alice", user.Name);
        Assert.Single(user.GetDomainEvents());
        Assert.IsType<UserCreatedDomainEvent>(user.GetDomainEvents().First());
    }

    [Fact]
    public void ChangeEmail_ShouldRaiseChangedEvent()
    {
        var user = new User("Bob", "old@example.com");
        user.ClearDomainEvents();

        user.ChangeEmail("new@example.com");

        Assert.Equal("new@example.com", user.Email);
        Assert.IsType<UserEmailChangedDomainEvent>(user.GetDomainEvents().Single());
    }
}
```

## KnownException 参考
```csharp
if (Paid) throw new KnownException("Order has been paid");
var order = await orderRepository.GetAsync(request.OrderId, cancellationToken)
             ?? throw new KnownException($"未找到订单，OrderId = {request.OrderId}");
order.OrderPaid();
```

## 常用 using 提示
- Web 全局：global using FluentValidation; MediatR; NetCorePal.Extensions.Primitives; FastEndpoints; NetCorePal.Extensions.Dto; NetCorePal.Extensions.Domain。
- Infrastructure 全局：global using Microsoft.EntityFrameworkCore; Microsoft.EntityFrameworkCore.Metadata.Builders; NetCorePal.Extensions.Primitives。
- Domain 全局：global using NetCorePal.Extensions.Domain; NetCorePal.Extensions.Primitives。
- Tests 全局：global using Xunit; NetCorePal.Extensions.Primitives。
- 额外：查询处理器需引用聚合命名空间与 Infrastructure；实体配置需引用对应聚合；端点需引用聚合、命令、查询命名空间。
