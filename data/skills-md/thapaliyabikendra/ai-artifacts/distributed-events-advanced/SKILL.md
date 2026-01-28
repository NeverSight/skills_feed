---
name: distributed-events-advanced
description: "Advanced distributed event patterns for ABP microservices including idempotent handlers, cross-tenant events, event sourcing lite, and saga patterns. Use when: (1) implementing event handlers across services, (2) ensuring idempotent event processing, (3) cross-tenant event handling, (4) designing event-driven architectures."
layer: 3
tech_stack: [dotnet, csharp, abp]
topics: [distributed-events, event-handlers, idempotency, saga, event-sourcing, multi-tenant]
depends_on: [abp-framework-patterns]
complements: []
keywords: [IDistributedEventHandler, Eto, EventBus, Saga, Idempotent, Outbox, RabbitMQ]
---

# Distributed Events Advanced Patterns

Master advanced distributed event patterns for building resilient, scalable ABP microservices architectures.

## When to Use This Skill

- Implementing event handlers that process events from other microservices
- Building idempotent event processing to handle duplicates
- Cross-tenant event synchronization
- Designing event-driven communication patterns
- Implementing saga/choreography patterns
- Troubleshooting event delivery issues

## Core Concepts

### Event Transfer Objects (ETOs)

ETOs are the payload of distributed events. Define them in a shared library accessible by both publisher and subscriber.

```csharp
// Shared/Etos/PatientCreatedEto.cs
[EventName("patient.created")]  // Optional: explicit event name
public class PatientCreatedEto
{
    public Guid Id { get; set; }
    public Guid? TenantId { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public DateTime CreatedAt { get; set; }

    // Include correlation ID for tracing
    public string CorrelationId { get; set; }
}
```

**ETO Best Practices:**
- Include `TenantId` for multi-tenant scenarios
- Include `CorrelationId` for distributed tracing
- Use primitive types only (no navigation properties)
- Version ETOs carefully (add properties, don't remove)

## Event Handler Patterns

### 1. Basic Event Handler

```csharp
public class PatientCreatedEventHandler :
    IDistributedEventHandler<PatientCreatedEto>,
    ITransientDependency
{
    private readonly ILogger<PatientCreatedEventHandler> _logger;

    public PatientCreatedEventHandler(
        ILogger<PatientCreatedEventHandler> logger)
    {
        _logger = logger;
    }

    public async Task HandleEventAsync(PatientCreatedEto eventData)
    {
        _logger.LogInformation(
            "Processing PatientCreated event: {PatientId}",
            eventData.Id);

        // Handle the event
        await ProcessPatientAsync(eventData);
    }
}
```

### 2. Idempotent Event Handler

Handle duplicate events gracefully using idempotency keys.

```csharp
public class PatientSyncEventHandler :
    IDistributedEventHandler<PatientCreatedEto>,
    ITransientDependency
{
    private readonly IRepository<Patient, Guid> _repository;
    private readonly IRepository<ProcessedEvent, Guid> _processedEventRepository;
    private readonly ILogger<PatientSyncEventHandler> _logger;

    public async Task HandleEventAsync(PatientCreatedEto eto)
    {
        // Idempotency check using event ID or correlation ID
        var eventKey = $"PatientCreated:{eto.Id}";

        if (await _processedEventRepository.AnyAsync(x => x.EventKey == eventKey))
        {
            _logger.LogInformation(
                "Event already processed, skipping: {EventKey}", eventKey);
            return;
        }

        try
        {
            // Check if entity already exists
            var existing = await _repository.FirstOrDefaultAsync(
                x => x.ExternalId == eto.Id);

            if (existing != null)
            {
                _logger.LogInformation(
                    "Patient already exists, updating: {PatientId}", eto.Id);
                existing.SetName(eto.Name);
                await _repository.UpdateAsync(existing);
            }
            else
            {
                var patient = new Patient(
                    GuidGenerator.Create(),
                    eto.Name,
                    eto.Email)
                {
                    ExternalId = eto.Id
                };
                await _repository.InsertAsync(patient);
            }

            // Record processed event
            await _processedEventRepository.InsertAsync(new ProcessedEvent
            {
                EventKey = eventKey,
                ProcessedAt = DateTime.UtcNow
            });

            _logger.LogInformation(
                "Successfully processed PatientCreated: {PatientId}", eto.Id);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed to process PatientCreated: {PatientId}", eto.Id);
            throw; // Re-throw to trigger retry
        }
    }
}

// Entity for tracking processed events
public class ProcessedEvent : Entity<Guid>
{
    public string EventKey { get; set; }
    public DateTime ProcessedAt { get; set; }
}
```

### 3. Cross-Tenant Event Handler

Handle events that need to operate across tenant boundaries.

```csharp
public class EntitySyncEventHandler :
    IDistributedEventHandler<EntityUpdatedEto>,
    ITransientDependency
{
    private readonly IRepository<Entity, Guid> _repository;
    private readonly IDataFilter _dataFilter;
    private readonly ICurrentTenant _currentTenant;
    private readonly ILogger<EntitySyncEventHandler> _logger;

    public async Task HandleEventAsync(EntityUpdatedEto eto)
    {
        _logger.LogInformation(
            "Processing cross-tenant sync: {EntityId}, TargetTenant: {TenantId}",
            eto.Id, eto.TenantId);

        // Option 1: Disable tenant filter completely
        using (_dataFilter.Disable<IMultiTenant>())
        {
            await SyncEntityAsync(eto);
        }

        // Option 2: Switch to specific tenant context
        using (_currentTenant.Change(eto.TenantId))
        {
            await SyncEntityAsync(eto);
        }
    }

    private async Task SyncEntityAsync(EntityUpdatedEto eto)
    {
        var existing = await _repository.FirstOrDefaultAsync(
            x => x.ExternalId == eto.ExternalId);

        if (existing != null)
        {
            // Update existing
            existing.Update(eto.Name, eto.Value);
            await _repository.UpdateAsync(existing);
        }
        else
        {
            // Create new
            var entity = new Entity(
                GuidGenerator.Create(),
                eto.Name,
                eto.Value)
            {
                TenantId = eto.TenantId,
                ExternalId = eto.ExternalId
            };
            await _repository.InsertAsync(entity);
        }
    }
}
```

### 4. Handler with Business Logic Delegation

Separate handler concerns from business logic for testability.

```csharp
// Event Handler - thin, handles infrastructure concerns
public class LicensePlateAllocatedEventHandler :
    IDistributedEventHandler<LicensePlateAllocatedEto>,
    ITransientDependency
{
    private readonly ILicensePlateEventService _eventService;
    private readonly ILogger<LicensePlateAllocatedEventHandler> _logger;

    public LicensePlateAllocatedEventHandler(
        ILicensePlateEventService eventService,
        ILogger<LicensePlateAllocatedEventHandler> logger)
    {
        _eventService = eventService;
        _logger = logger;
    }

    public async Task HandleEventAsync(LicensePlateAllocatedEto eto)
    {
        try
        {
            _logger.LogInformation(
                "[{Handler}] HandleEventAsync - Started - LicensePlateId: {Id}",
                nameof(LicensePlateAllocatedEventHandler), eto.LicensePlateId);

            await _eventService.ProcessAllocationAsync(eto);

            _logger.LogInformation(
                "[{Handler}] HandleEventAsync - Completed - LicensePlateId: {Id}",
                nameof(LicensePlateAllocatedEventHandler), eto.LicensePlateId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "[{Handler}] HandleEventAsync - Failed - LicensePlateId: {Id}",
                nameof(LicensePlateAllocatedEventHandler), eto.LicensePlateId);
            throw new UserFriendlyException($"Failed to process allocation: {ex.Message}");
        }
    }
}

// Service - contains business logic, easily testable
public interface ILicensePlateEventService
{
    Task ProcessAllocationAsync(LicensePlateAllocatedEto eto);
}

public class LicensePlateEventService : ApplicationService, ILicensePlateEventService
{
    private readonly IRepository<LicensePlate, Guid> _repository;

    public async Task ProcessAllocationAsync(LicensePlateAllocatedEto eto)
    {
        var licensePlate = await _repository.GetAsync(eto.LicensePlateId);
        licensePlate.MarkAsAllocated(eto.AllocatedTo, eto.AllocatedAt);
        await _repository.UpdateAsync(licensePlate);
    }
}
```

## Publishing Events

### 1. From Application Service

```csharp
public class PatientAppService : ApplicationService, IPatientAppService
{
    private readonly IDistributedEventBus _eventBus;

    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        var patient = new Patient(GuidGenerator.Create(), input.Name, input.Email);
        await _patientRepository.InsertAsync(patient);

        // Publish event after successful creation
        await _eventBus.PublishAsync(new PatientCreatedEto
        {
            Id = patient.Id,
            TenantId = CurrentTenant.Id,
            Name = patient.Name,
            Email = patient.Email,
            CreatedAt = patient.CreationTime,
            CorrelationId = CorrelationIdAccessor.GetCorrelationId()
        });

        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }
}
```

### 2. From Domain Entity (Aggregate Root)

```csharp
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; private set; }
    public string Email { get; private set; }
    public bool IsActive { get; private set; }

    public void Activate()
    {
        if (IsActive)
        {
            throw new BusinessException("Patient is already active");
        }

        IsActive = true;

        // Domain event - published when UoW completes
        AddDistributedEvent(new PatientActivatedEto
        {
            Id = Id,
            Name = Name,
            Email = Email,
            ActivatedAt = DateTime.UtcNow
        });
    }
}
```

### 3. Outbox Pattern (Transactional Events)

Ensure events are published atomically with database changes.

```csharp
// Configure in module
public override void ConfigureServices(ServiceConfigurationContext context)
{
    Configure<AbpDistributedEventBusOptions>(options =>
    {
        options.Outbox.IsEnabled = true;  // Enable outbox
    });
}
```

## Advanced Patterns

### 1. Event Retry with Exponential Backoff

```csharp
public class ResilientEventHandler :
    IDistributedEventHandler<ImportantEventEto>,
    ITransientDependency
{
    private const int MaxRetries = 3;
    private readonly ILogger<ResilientEventHandler> _logger;

    public async Task HandleEventAsync(ImportantEventEto eto)
    {
        var retryCount = 0;
        Exception lastException = null;

        while (retryCount < MaxRetries)
        {
            try
            {
                await ProcessEventAsync(eto);
                return; // Success
            }
            catch (Exception ex) when (IsTransientError(ex))
            {
                lastException = ex;
                retryCount++;

                var delay = TimeSpan.FromSeconds(Math.Pow(2, retryCount));
                _logger.LogWarning(
                    "Retry {RetryCount}/{MaxRetries} after {Delay}s for event {EventId}",
                    retryCount, MaxRetries, delay.TotalSeconds, eto.Id);

                await Task.Delay(delay);
            }
        }

        _logger.LogError(lastException,
            "Failed to process event after {MaxRetries} retries: {EventId}",
            MaxRetries, eto.Id);
        throw lastException;
    }

    private bool IsTransientError(Exception ex) =>
        ex is DbUpdateConcurrencyException ||
        ex is TimeoutException ||
        ex is HttpRequestException;
}
```

### 2. Saga/Choreography Pattern

Coordinate multi-step processes across services.

```csharp
// Step 1: Order Service publishes OrderCreated
public class OrderAppService : ApplicationService
{
    public async Task<OrderDto> CreateAsync(CreateOrderDto input)
    {
        var order = new Order(GuidGenerator.Create(), input.CustomerId);
        await _orderRepository.InsertAsync(order);

        await _eventBus.PublishAsync(new OrderCreatedEto
        {
            OrderId = order.Id,
            CustomerId = input.CustomerId,
            Items = input.Items
        });

        return ObjectMapper.Map<Order, OrderDto>(order);
    }
}

// Step 2: Inventory Service handles OrderCreated
public class OrderCreatedHandler : IDistributedEventHandler<OrderCreatedEto>
{
    public async Task HandleEventAsync(OrderCreatedEto eto)
    {
        try
        {
            await ReserveInventoryAsync(eto.Items);

            // Publish success event
            await _eventBus.PublishAsync(new InventoryReservedEto
            {
                OrderId = eto.OrderId,
                ReservedAt = DateTime.UtcNow
            });
        }
        catch (InsufficientInventoryException ex)
        {
            // Publish failure event for compensation
            await _eventBus.PublishAsync(new InventoryReservationFailedEto
            {
                OrderId = eto.OrderId,
                Reason = ex.Message
            });
        }
    }
}

// Step 3: Order Service handles compensation
public class InventoryReservationFailedHandler :
    IDistributedEventHandler<InventoryReservationFailedEto>
{
    public async Task HandleEventAsync(InventoryReservationFailedEto eto)
    {
        var order = await _orderRepository.GetAsync(eto.OrderId);
        order.Cancel($"Inventory reservation failed: {eto.Reason}");
        await _orderRepository.UpdateAsync(order);

        // Notify customer
        await _eventBus.PublishAsync(new OrderCancelledEto
        {
            OrderId = eto.OrderId,
            Reason = eto.Reason
        });
    }
}
```

### 3. Event Aggregation

Batch multiple events for efficiency.

```csharp
public class BatchEventHandler :
    IDistributedEventHandler<ItemUpdatedEto>,
    ITransientDependency
{
    private static readonly ConcurrentDictionary<Guid, List<ItemUpdatedEto>> _batches = new();
    private static readonly SemaphoreSlim _lock = new(1, 1);

    public async Task HandleEventAsync(ItemUpdatedEto eto)
    {
        var batchKey = eto.TenantId ?? Guid.Empty;

        _batches.AddOrUpdate(
            batchKey,
            new List<ItemUpdatedEto> { eto },
            (_, list) => { list.Add(eto); return list; });

        // Process batch when threshold reached
        if (_batches[batchKey].Count >= 100)
        {
            await _lock.WaitAsync();
            try
            {
                if (_batches.TryRemove(batchKey, out var batch))
                {
                    await ProcessBatchAsync(batch);
                }
            }
            finally
            {
                _lock.Release();
            }
        }
    }
}
```

## Error Handling Patterns

### Dead Letter Queue Handling

```csharp
public class DeadLetterEventHandler :
    IDistributedEventHandler<DeadLetterEvent>,
    ITransientDependency
{
    private readonly IRepository<FailedEvent, Guid> _failedEventRepository;
    private readonly ILogger<DeadLetterEventHandler> _logger;

    public async Task HandleEventAsync(DeadLetterEvent eto)
    {
        _logger.LogWarning(
            "Event moved to dead letter queue: {EventType}, Error: {Error}",
            eto.OriginalEventType, eto.ErrorMessage);

        await _failedEventRepository.InsertAsync(new FailedEvent
        {
            EventType = eto.OriginalEventType,
            EventData = eto.OriginalEventData,
            ErrorMessage = eto.ErrorMessage,
            FailedAt = DateTime.UtcNow,
            RetryCount = eto.RetryCount
        });

        // Notify operations team
        await _notificationService.SendAlertAsync(
            "Event Processing Failed",
            $"Event {eto.OriginalEventType} failed after {eto.RetryCount} retries");
    }
}
```

## Testing Event Handlers

```csharp
public class PatientCreatedEventHandlerTests : ApplicationTestBase
{
    private readonly PatientCreatedEventHandler _handler;
    private readonly IRepository<Patient, Guid> _repository;

    [Fact]
    public async Task HandleEventAsync_CreatesPatient_WhenNotExists()
    {
        // Arrange
        var eto = new PatientCreatedEto
        {
            Id = Guid.NewGuid(),
            Name = "John Doe",
            Email = "john@example.com"
        };

        // Act
        await _handler.HandleEventAsync(eto);

        // Assert
        var patient = await _repository.FirstOrDefaultAsync(
            x => x.ExternalId == eto.Id);
        patient.ShouldNotBeNull();
        patient.Name.ShouldBe("John Doe");
    }

    [Fact]
    public async Task HandleEventAsync_UpdatesPatient_WhenExists()
    {
        // Arrange
        var existingId = Guid.NewGuid();
        await _repository.InsertAsync(new Patient(
            Guid.NewGuid(), "Old Name", "old@example.com")
        {
            ExternalId = existingId
        });

        var eto = new PatientCreatedEto
        {
            Id = existingId,
            Name = "New Name",
            Email = "new@example.com"
        };

        // Act
        await _handler.HandleEventAsync(eto);

        // Assert
        var patient = await _repository.FirstOrDefaultAsync(
            x => x.ExternalId == existingId);
        patient.Name.ShouldBe("New Name");
    }

    [Fact]
    public async Task HandleEventAsync_IsIdempotent()
    {
        // Arrange
        var eto = new PatientCreatedEto
        {
            Id = Guid.NewGuid(),
            Name = "John Doe"
        };

        // Act - process same event twice
        await _handler.HandleEventAsync(eto);
        await _handler.HandleEventAsync(eto);

        // Assert - only one patient created
        var count = await _repository.CountAsync(x => x.ExternalId == eto.Id);
        count.ShouldBe(1);
    }
}
```

## Configuration

### RabbitMQ Configuration

```csharp
public override void ConfigureServices(ServiceConfigurationContext context)
{
    var configuration = context.Services.GetConfiguration();

    Configure<AbpRabbitMqEventBusOptions>(options =>
    {
        options.ClientName = "MyService";
        options.ExchangeName = "MyApp";
    });

    Configure<AbpDistributedEventBusOptions>(options =>
    {
        options.Outbox.IsEnabled = true;
        options.Inbox.IsEnabled = true;
        options.Inbox.HandlerExecutionMaxRetryCount = 3;
    });
}
```

## References

- [Event Handler Templates](references/event-handler-templates.md)
- [Saga Pattern Examples](references/saga-patterns.md)

## External Resources

- ABP Distributed Events: https://docs.abp.io/en/abp/latest/Distributed-Event-Bus
- RabbitMQ Integration: https://docs.abp.io/en/abp/latest/Distributed-Event-Bus-RabbitMQ-Integration
