---
name: grpc-integration-patterns
description: "gRPC integration patterns for ABP microservices including service implementation, client generation, multi-tenancy, and error handling. Use when: (1) implementing inter-service communication, (2) creating gRPC service endpoints, (3) consuming gRPC clients in AppServices, (4) designing high-performance APIs."
layer: 3
tech_stack: [dotnet, csharp, abp, grpc]
topics: [grpc, protobuf, service-communication, streaming, interceptors]
depends_on: [abp-framework-patterns]
complements: []
keywords: [gRPC, Protobuf, proto, GrpcChannel, ServerServiceDefinition, Interceptor]
---

# gRPC Integration Patterns

Master gRPC integration for high-performance inter-service communication in ABP Framework microservices architectures.

## When to Use This Skill

- Building inter-service communication in microservices
- Implementing high-performance APIs with streaming
- Creating gRPC service endpoints alongside REST APIs
- Consuming gRPC clients in application services
- Handling multi-tenancy in gRPC context
- Designing real-time communication with bidirectional streaming

## Why gRPC?

| Feature | REST | gRPC |
|---------|------|------|
| Protocol | HTTP/1.1 JSON | HTTP/2 Protobuf |
| Performance | Good | Excellent (10x faster) |
| Contract | OpenAPI (optional) | Required (Protobuf) |
| Streaming | Limited | Full support |
| Code Gen | Optional | Built-in |
| Best for | Public APIs | Internal microservices |

## Project Setup

### 1. NuGet Packages

```xml
<!-- In your gRPC host project -->
<ItemGroup>
  <PackageReference Include="Grpc.AspNetCore" Version="2.60.0" />
  <PackageReference Include="Grpc.Tools" Version="2.60.0" PrivateAssets="All" />
</ItemGroup>

<!-- For client projects -->
<ItemGroup>
  <PackageReference Include="Grpc.Net.Client" Version="2.60.0" />
  <PackageReference Include="Google.Protobuf" Version="3.25.2" />
</ItemGroup>
```

### 2. Protobuf Definitions

```protobuf
// Protos/license_plate.proto
syntax = "proto3";

option csharp_namespace = "MyApp.Shared.Grpc";

package licenseplate;

// Service definition
service LicensePlateService {
  // Unary RPC
  rpc GetTenantIdByLPNumber (LicensePlateRequest) returns (LicensePlateResponse);

  // Server streaming
  rpc GetLicensePlates (GetLicensePlatesRequest) returns (stream LicensePlateDto);

  // Client streaming
  rpc ReceiveLicensePlates (stream ReceiveLicensePlateRequest) returns (ReceiveLicensePlateResponse);

  // Bidirectional streaming
  rpc SyncLicensePlates (stream LicensePlateSyncRequest) returns (stream LicensePlateSyncResponse);
}

// Messages
message LicensePlateRequest {
  string lp_number = 1;
}

message LicensePlateResponse {
  string tenant_id = 1;
  bool found = 2;
}

message GetLicensePlatesRequest {
  string tenant_id = 1;
  string project_code = 2;
  int32 page_size = 3;
  int32 page_number = 4;
}

message LicensePlateDto {
  string id = 1;
  string license_plate_number = 2;
  string project_code = 3;
  string tag_mac = 4;
  double length = 5;
  double width = 6;
  double height = 7;
  double weight = 8;
  string created_at = 9;
}

message ReceiveLicensePlateRequest {
  string from_tenant_id = 1;
  string to_tenant_id = 2;
  repeated LicensePlateInput license_plates = 3;
}

message LicensePlateInput {
  string license_plate_number = 1;
  string project_code = 2;
  string tag_mac = 3;
  string sku_id = 4;
  double length = 5;
  double width = 6;
  double height = 7;
  double weight = 8;
}

message ReceiveLicensePlateResponse {
  bool is_success = 1;
  repeated ReceiveLicensePlateError errors = 2;
}

message ReceiveLicensePlateError {
  string error = 1;
  string field = 2;
  int32 row_number = 3;
}
```

### 3. Project File Configuration

```xml
<!-- Add to .csproj -->
<ItemGroup>
  <Protobuf Include="Protos\*.proto" GrpcServices="Server" />
</ItemGroup>

<!-- For client project -->
<ItemGroup>
  <Protobuf Include="Protos\*.proto" GrpcServices="Client" />
</ItemGroup>
```

## gRPC Service Implementation

### 1. Basic Service Implementation

```csharp
// Application/GrpcServices/LicensePlateGrpcService.cs
public class LicensePlateGrpcService : LicensePlateService.LicensePlateServiceBase
{
    private readonly CommonDependencies<LicensePlateGrpcService> _common;
    private readonly IRepository<LicensePlate, Guid> _licensePlateRepository;
    private readonly IRepository<Project, Guid> _projectRepository;

    public LicensePlateGrpcService(
        CommonDependencies<LicensePlateGrpcService> common,
        IRepository<LicensePlate, Guid> licensePlateRepository,
        IRepository<Project, Guid> projectRepository)
    {
        _common = common;
        _licensePlateRepository = licensePlateRepository;
        _projectRepository = projectRepository;
    }

    public override async Task<LicensePlateResponse> GetTenantIdByLPNumber(
        LicensePlateRequest request,
        ServerCallContext context)
    {
        _common.Logger.LogInformation(
            "[{Service}] GetTenantIdByLPNumber - Started - LP: {LpNumber}",
            nameof(LicensePlateGrpcService), request.LpNumber);

        try
        {
            // Disable tenant filter for cross-tenant lookup
            using (_common.DataFilter.Disable<IMultiTenant>())
            {
                var licensePlate = await _licensePlateRepository
                    .FirstOrDefaultAsync(lp =>
                        lp.LicensePlateNumber == request.LpNumber &&
                        !lp.ShippedOut);

                var response = new LicensePlateResponse
                {
                    Found = licensePlate != null,
                    TenantId = licensePlate?.TenantId?.ToString() ?? string.Empty
                };

                _common.Logger.LogInformation(
                    "[{Service}] GetTenantIdByLPNumber - Completed - Found: {Found}",
                    nameof(LicensePlateGrpcService), response.Found);

                return response;
            }
        }
        catch (Exception ex)
        {
            _common.Logger.LogError(ex,
                "[{Service}] GetTenantIdByLPNumber - Failed - LP: {LpNumber}",
                nameof(LicensePlateGrpcService), request.LpNumber);

            throw new RpcException(new Status(StatusCode.Internal, ex.Message));
        }
    }
}
```

### 2. Server Streaming

```csharp
public override async Task GetLicensePlates(
    GetLicensePlatesRequest request,
    IServerStreamWriter<LicensePlateDto> responseStream,
    ServerCallContext context)
{
    _common.Logger.LogInformation(
        "[{Service}] GetLicensePlates - Started - TenantId: {TenantId}",
        nameof(LicensePlateGrpcService), request.TenantId);

    var tenantId = Guid.Parse(request.TenantId);

    using (_common.CurrentTenant.Change(tenantId))
    {
        var query = await _licensePlateRepository.GetQueryableAsync();

        var licensePlates = query
            .WhereIf(!string.IsNullOrEmpty(request.ProjectCode),
                lp => lp.Project.ProjectCode == request.ProjectCode)
            .Skip(request.PageNumber * request.PageSize)
            .Take(request.PageSize);

        foreach (var lp in licensePlates)
        {
            // Check for cancellation
            if (context.CancellationToken.IsCancellationRequested)
            {
                _common.Logger.LogWarning(
                    "[{Service}] GetLicensePlates - Cancelled by client",
                    nameof(LicensePlateGrpcService));
                break;
            }

            await responseStream.WriteAsync(new LicensePlateDto
            {
                Id = lp.Id.ToString(),
                LicensePlateNumber = lp.LicensePlateNumber,
                ProjectCode = lp.Project?.ProjectCode ?? string.Empty,
                TagMac = lp.Tag?.TagMac ?? string.Empty,
                Length = (double)lp.Length,
                Width = (double)lp.Width,
                Height = (double)lp.Height,
                Weight = (double)lp.Weight,
                CreatedAt = lp.CreationTime.ToString("O")
            });
        }
    }

    _common.Logger.LogInformation(
        "[{Service}] GetLicensePlates - Completed",
        nameof(LicensePlateGrpcService));
}
```

### 3. Client Streaming (Bulk Receive)

```csharp
public override async Task<ReceiveLicensePlateResponse> ReceiveLicensePlates(
    IAsyncStreamReader<ReceiveLicensePlateRequest> requestStream,
    ServerCallContext context)
{
    _common.Logger.LogInformation(
        "[{Service}] ReceiveLicensePlates - Started",
        nameof(LicensePlateGrpcService));

    var allLicensePlates = new List<LicensePlateInput>();
    var errors = new List<ReceiveLicensePlateError>();
    Guid? fromTenantId = null;
    Guid? toTenantId = null;

    // Read all incoming messages
    await foreach (var request in requestStream.ReadAllAsync(context.CancellationToken))
    {
        fromTenantId ??= Guid.Parse(request.FromTenantId);
        toTenantId ??= Guid.Parse(request.ToTenantId);

        allLicensePlates.AddRange(request.LicensePlates);
    }

    if (!toTenantId.HasValue || !allLicensePlates.Any())
    {
        return new ReceiveLicensePlateResponse
        {
            IsSuccess = false,
            Errors = { new ReceiveLicensePlateError { Error = "No data received" } }
        };
    }

    // Process in target tenant context
    using (_common.DataFilter.Disable<IMultiTenant>())
    {
        try
        {
            // Validate and create license plates
            var result = await ProcessLicensePlatesAsync(
                allLicensePlates,
                fromTenantId.Value,
                toTenantId.Value);

            return result;
        }
        catch (Exception ex)
        {
            _common.Logger.LogError(ex,
                "[{Service}] ReceiveLicensePlates - Failed",
                nameof(LicensePlateGrpcService));

            return new ReceiveLicensePlateResponse
            {
                IsSuccess = false,
                Errors = { new ReceiveLicensePlateError { Error = ex.Message } }
            };
        }
    }
}
```

### 4. Bidirectional Streaming

```csharp
public override async Task SyncLicensePlates(
    IAsyncStreamReader<LicensePlateSyncRequest> requestStream,
    IServerStreamWriter<LicensePlateSyncResponse> responseStream,
    ServerCallContext context)
{
    _common.Logger.LogInformation(
        "[{Service}] SyncLicensePlates - Started",
        nameof(LicensePlateGrpcService));

    await foreach (var request in requestStream.ReadAllAsync(context.CancellationToken))
    {
        try
        {
            // Process each request and immediately respond
            var result = await ProcessSyncRequestAsync(request);

            await responseStream.WriteAsync(new LicensePlateSyncResponse
            {
                RequestId = request.RequestId,
                IsSuccess = true,
                Message = $"Processed {request.LicensePlateNumber}"
            });
        }
        catch (Exception ex)
        {
            await responseStream.WriteAsync(new LicensePlateSyncResponse
            {
                RequestId = request.RequestId,
                IsSuccess = false,
                Message = ex.Message
            });
        }
    }
}
```

## gRPC Client Implementation

### 1. Client Factory Registration

```csharp
// Module configuration
public override void ConfigureServices(ServiceConfigurationContext context)
{
    var configuration = context.Services.GetConfiguration();

    // Register gRPC client
    context.Services.AddGrpcClient<LicensePlateService.LicensePlateServiceClient>(options =>
    {
        options.Address = new Uri(configuration["GrpcServices:InboundService"]);
    })
    .ConfigurePrimaryHttpMessageHandler(() =>
    {
        var handler = new HttpClientHandler();

        // For development/testing - skip certificate validation
        if (context.Services.GetHostingEnvironment().IsDevelopment())
        {
            handler.ServerCertificateCustomValidationCallback =
                HttpClientHandler.DangerousAcceptAnyServerCertificateValidator;
        }

        return handler;
    })
    .AddInterceptor<ClientLoggingInterceptor>();
}
```

### 2. Using gRPC Client in AppService

```csharp
public class WarehouseTransferAppService : ApplicationService
{
    private readonly LicensePlateService.LicensePlateServiceClient _licensePlateClient;
    private readonly ILogger<WarehouseTransferAppService> _logger;

    public WarehouseTransferAppService(
        LicensePlateService.LicensePlateServiceClient licensePlateClient,
        ILogger<WarehouseTransferAppService> logger)
    {
        _licensePlateClient = licensePlateClient;
        _logger = logger;
    }

    public async Task<Guid?> GetTenantByLicensePlateAsync(string lpNumber)
    {
        _logger.LogInformation(
            "[{Service}] GetTenantByLicensePlate - Calling gRPC - LP: {LpNumber}",
            nameof(WarehouseTransferAppService), lpNumber);

        try
        {
            var response = await _licensePlateClient.GetTenantIdByLPNumberAsync(
                new LicensePlateRequest { LpNumber = lpNumber });

            if (!response.Found)
            {
                _logger.LogWarning("License plate not found: {LpNumber}", lpNumber);
                return null;
            }

            return Guid.Parse(response.TenantId);
        }
        catch (RpcException ex)
        {
            _logger.LogError(ex,
                "gRPC call failed for license plate: {LpNumber}", lpNumber);
            throw new UserFriendlyException(
                $"Failed to lookup license plate: {ex.Status.Detail}");
        }
    }

    public async Task TransferLicensePlatesAsync(
        Guid fromTenantId,
        Guid toTenantId,
        List<TransferLicensePlateDto> licensePlates)
    {
        _logger.LogInformation(
            "[{Service}] TransferLicensePlates - Started - Count: {Count}",
            nameof(WarehouseTransferAppService), licensePlates.Count);

        var request = new ReceiveLicensePlateRequest
        {
            FromTenantId = fromTenantId.ToString(),
            ToTenantId = toTenantId.ToString()
        };

        request.LicensePlates.AddRange(licensePlates.Select(lp => new LicensePlateInput
        {
            LicensePlateNumber = lp.LicensePlateNumber,
            ProjectCode = lp.ProjectCode,
            TagMac = lp.TagMac,
            SkuId = lp.SkuId.ToString(),
            Length = (double)lp.Length,
            Width = (double)lp.Width,
            Height = (double)lp.Height,
            Weight = (double)lp.Weight
        }));

        var response = await _licensePlateClient.ReceiveLicensePlatesAsync(request);

        if (!response.IsSuccess)
        {
            var errors = string.Join(", ", response.Errors.Select(e => e.Error));
            throw new UserFriendlyException($"Transfer failed: {errors}");
        }

        _logger.LogInformation(
            "[{Service}] TransferLicensePlates - Completed",
            nameof(WarehouseTransferAppService));
    }
}
```

### 3. Streaming Client

```csharp
public async Task<List<LicensePlateDto>> GetLicensePlatesStreamAsync(
    Guid tenantId,
    string projectCode,
    CancellationToken cancellationToken = default)
{
    var results = new List<LicensePlateDto>();

    using var call = _licensePlateClient.GetLicensePlates(
        new GetLicensePlatesRequest
        {
            TenantId = tenantId.ToString(),
            ProjectCode = projectCode
        });

    await foreach (var lp in call.ResponseStream.ReadAllAsync(cancellationToken))
    {
        results.Add(new LicensePlateDto
        {
            Id = Guid.Parse(lp.Id),
            LicensePlateNumber = lp.LicensePlateNumber,
            ProjectCode = lp.ProjectCode
        });
    }

    return results;
}
```

## Interceptors

### 1. Client Logging Interceptor

```csharp
public class ClientLoggingInterceptor : Interceptor
{
    private readonly ILogger<ClientLoggingInterceptor> _logger;

    public ClientLoggingInterceptor(ILogger<ClientLoggingInterceptor> logger)
    {
        _logger = logger;
    }

    public override AsyncUnaryCall<TResponse> AsyncUnaryCall<TRequest, TResponse>(
        TRequest request,
        ClientInterceptorContext<TRequest, TResponse> context,
        AsyncUnaryCallContinuation<TRequest, TResponse> continuation)
    {
        var stopwatch = Stopwatch.StartNew();
        var method = context.Method.FullName;

        _logger.LogInformation(
            "[gRPC] Calling {Method} with request: {@Request}",
            method, request);

        var call = continuation(request, context);

        return new AsyncUnaryCall<TResponse>(
            HandleResponse(call.ResponseAsync, method, stopwatch),
            call.ResponseHeadersAsync,
            call.GetStatus,
            call.GetTrailers,
            call.Dispose);
    }

    private async Task<TResponse> HandleResponse<TResponse>(
        Task<TResponse> responseTask,
        string method,
        Stopwatch stopwatch)
    {
        try
        {
            var response = await responseTask;
            stopwatch.Stop();

            _logger.LogInformation(
                "[gRPC] {Method} completed in {ElapsedMs}ms",
                method, stopwatch.ElapsedMilliseconds);

            return response;
        }
        catch (RpcException ex)
        {
            stopwatch.Stop();

            _logger.LogError(
                "[gRPC] {Method} failed after {ElapsedMs}ms - Status: {Status}, Detail: {Detail}",
                method, stopwatch.ElapsedMilliseconds, ex.StatusCode, ex.Status.Detail);

            throw;
        }
    }
}
```

### 2. Server Auth Interceptor

```csharp
public class ServerAuthInterceptor : Interceptor
{
    private readonly ICurrentTenant _currentTenant;
    private readonly ICurrentUser _currentUser;

    public override async Task<TResponse> UnaryServerHandler<TRequest, TResponse>(
        TRequest request,
        ServerCallContext context,
        UnaryServerMethod<TRequest, TResponse> continuation)
    {
        // Extract tenant from metadata
        var tenantId = context.RequestHeaders
            .FirstOrDefault(h => h.Key == "x-tenant-id")?.Value;

        if (!string.IsNullOrEmpty(tenantId) && Guid.TryParse(tenantId, out var tid))
        {
            using (_currentTenant.Change(tid))
            {
                return await continuation(request, context);
            }
        }

        return await continuation(request, context);
    }
}
```

## Host Configuration

```csharp
// In HttpApi.Host module
public override void ConfigureServices(ServiceConfigurationContext context)
{
    context.Services.AddGrpc(options =>
    {
        options.EnableDetailedErrors = true;
        options.MaxReceiveMessageSize = 10 * 1024 * 1024; // 10MB
        options.MaxSendMessageSize = 10 * 1024 * 1024;
        options.Interceptors.Add<ServerAuthInterceptor>();
    });
}

public override void OnApplicationInitialization(ApplicationInitializationContext context)
{
    var app = context.GetApplicationBuilder();

    app.UseRouting();
    app.UseAuthentication();
    app.UseAuthorization();

    app.UseEndpoints(endpoints =>
    {
        endpoints.MapGrpcService<LicensePlateGrpcService>();

        // Health check endpoint
        endpoints.MapGrpcHealthChecksService();

        // REST endpoints
        endpoints.MapControllers();
    });
}
```

## Best Practices

1. **Use Protobuf for contracts** - Single source of truth for client and server
2. **Handle cancellation** - Always check `CancellationToken` in long-running operations
3. **Log comprehensively** - Log method start, completion, and errors
4. **Use interceptors** - For cross-cutting concerns (logging, auth, metrics)
5. **Batch streaming** - Use streaming for large data transfers
6. **Handle RpcException** - Map to appropriate HTTP status codes or `UserFriendlyException`
7. **Configure timeouts** - Set appropriate deadlines for all calls
8. **Use health checks** - Enable gRPC health checking service

## References

- [Protobuf Message Design](references/protobuf-design.md)
- [gRPC Error Handling](references/grpc-errors.md)

## External Resources

- gRPC for .NET: https://docs.microsoft.com/en-us/aspnet/core/grpc
- Protobuf Language Guide: https://developers.google.com/protocol-buffers/docs/proto3
