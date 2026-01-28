---
name: system-design-patterns
description: "System design patterns for scalability, reliability, and performance. Use when: (1) designing distributed systems, (2) planning for scale, (3) making architecture decisions, (4) evaluating trade-offs."
layer: 2
tech_stack: [agnostic, dotnet, distributed-systems]
topics: [scalability, reliability, performance, architecture, trade-offs]
depends_on: []
complements: [technical-design-patterns, api-design-principles]
keywords: [Scalability, CAP, ACID, BASE, LoadBalancing, Caching, Sharding, Replication]
---

# System Design Patterns

Design scalable, reliable, and performant systems with proven patterns.

## When to Use

- Designing new systems or features
- Evaluating architecture trade-offs
- Planning for scale
- Improving system reliability
- Making infrastructure decisions

## Core Principles

### CAP Theorem

| Property | Meaning | Trade-off |
|----------|---------|-----------|
| **C**onsistency | All nodes see the same data | Higher latency |
| **A**vailability | System responds to every request | May return stale data |
| **P**artition Tolerance | System works despite network failures | Must sacrifice C or A |

**Choose 2:**
- CP: Banking, inventory (consistency critical)
- AP: Social media, caching (availability critical)
- CA: Single-node systems only (no network partitions)

### ACID vs BASE

| ACID (Traditional RDBMS) | BASE (Distributed) |
|--------------------------|-------------------|
| Atomicity | Basically Available |
| Consistency | Soft state |
| Isolation | Eventually consistent |
| Durability | |

## Scalability Patterns

### Horizontal vs Vertical Scaling

```
Vertical Scaling (Scale Up)          Horizontal Scaling (Scale Out)
┌─────────────────────────┐         ┌──────┐ ┌──────┐ ┌──────┐
│                         │         │      │ │      │ │      │
│     Bigger Server       │    vs   │Server│ │Server│ │Server│
│                         │         │      │ │      │ │      │
│ More CPU, RAM, Storage  │         │      │ │      │ │      │
└─────────────────────────┘         └──────┘ └──────┘ └──────┘

Pros:                               Pros:
- Simple to implement               - Near-infinite scale
- No code changes                   - Fault tolerant
- Lower operational complexity      - Cost effective at scale

Cons:                               Cons:
- Hardware limits                   - Distributed complexity
- Single point of failure           - Data consistency challenges
- Expensive at scale                - More operational overhead
```

### Load Balancing Strategies

```csharp
// Strategy selection based on use case

public enum LoadBalancingStrategy
{
    // Simple, stateless services
    RoundRobin,

    // Varying server capacities
    WeightedRoundRobin,

    // Session affinity needed
    IpHash,

    // Optimal resource utilization
    LeastConnections,

    // Latency-sensitive applications
    LeastResponseTime,

    // Geographic distribution
    GeographicBased
}
```

| Strategy | Use Case | Trade-off |
|----------|----------|-----------|
| Round Robin | Stateless, homogeneous | No health awareness |
| Weighted | Different server sizes | Manual configuration |
| IP Hash | Session stickiness | Uneven distribution |
| Least Connections | Long-lived connections | Overhead tracking |
| Geographic | Global users | Complexity |

### Database Scaling

#### Read Replicas

```
┌─────────────────────────────────────────────────────┐
│                    Application                       │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐           ┌─────────────────┐
│  Primary DB   │──────────►│  Read Replica 1 │
│  (Writes)     │    Async  ├─────────────────┤
│               │──────────►│  Read Replica 2 │
└───────────────┘    Repl   └─────────────────┘
                                    ▲
                                    │
                              Read Queries
```

```csharp
// Read/Write splitting in ABP
public class PatientAppService : ApplicationService
{
    private readonly IReadOnlyRepository<Patient, Guid> _readRepository;
    private readonly IRepository<Patient, Guid> _writeRepository;

    // Reads go to replicas
    public async Task<PatientDto> GetAsync(Guid id)
    {
        var patient = await _readRepository.GetAsync(id);
        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    // Writes go to primary
    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        var patient = new Patient(GuidGenerator.Create(), input.Name);
        await _writeRepository.InsertAsync(patient);
        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }
}
```

#### Database Sharding

```
┌─────────────────────────────────────────────────────────────┐
│                     Shard Router                            │
│         (Routes queries based on shard key)                 │
└────────────┬──────────────┬──────────────┬─────────────────┘
             │              │              │
             ▼              ▼              ▼
      ┌───────────┐  ┌───────────┐  ┌───────────┐
      │  Shard 1  │  │  Shard 2  │  │  Shard 3  │
      │  A - H    │  │  I - P    │  │  Q - Z    │
      │ (Users)   │  │ (Users)   │  │ (Users)   │
      └───────────┘  └───────────┘  └───────────┘
```

| Sharding Strategy | Pros | Cons |
|-------------------|------|------|
| Range-based | Simple, range queries work | Hotspots possible |
| Hash-based | Even distribution | Range queries need scatter-gather |
| Directory-based | Flexible | Lookup overhead, SPOF |
| Geographic | Data locality | Cross-region queries slow |

## Caching Patterns

### Cache-Aside (Lazy Loading)

```csharp
public class PatientService
{
    private readonly IDistributedCache _cache;
    private readonly IPatientRepository _repository;

    public async Task<PatientDto> GetAsync(Guid id)
    {
        var cacheKey = $"patient:{id}";

        // 1. Check cache
        var cached = await _cache.GetStringAsync(cacheKey);
        if (cached != null)
        {
            return JsonSerializer.Deserialize<PatientDto>(cached);
        }

        // 2. Cache miss - load from DB
        var patient = await _repository.GetAsync(id);
        var dto = ObjectMapper.Map<Patient, PatientDto>(patient);

        // 3. Populate cache
        await _cache.SetStringAsync(
            cacheKey,
            JsonSerializer.Serialize(dto),
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
            });

        return dto;
    }

    public async Task UpdateAsync(Guid id, UpdatePatientDto input)
    {
        // Update database
        var patient = await _repository.GetAsync(id);
        patient.Update(input.Name, input.Email);
        await _repository.UpdateAsync(patient);

        // Invalidate cache
        await _cache.RemoveAsync($"patient:{id}");
    }
}
```

### Write-Through Cache

```csharp
public async Task<PatientDto> CreateAsync(CreatePatientDto input)
{
    // 1. Write to database
    var patient = new Patient(GuidGenerator.Create(), input.Name);
    await _repository.InsertAsync(patient);

    // 2. Write to cache synchronously
    var dto = ObjectMapper.Map<Patient, PatientDto>(patient);
    await _cache.SetStringAsync(
        $"patient:{patient.Id}",
        JsonSerializer.Serialize(dto),
        new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
        });

    return dto;
}
```

### Cache Strategies Comparison

| Pattern | Consistency | Performance | Use Case |
|---------|-------------|-------------|----------|
| Cache-Aside | Eventual | Read-heavy | User profiles |
| Write-Through | Strong | Write + Read | Financial data |
| Write-Behind | Eventual | Write-heavy | Analytics, logs |
| Read-Through | Eventual | Read-heavy | Reference data |

## Reliability Patterns

### Circuit Breaker

```csharp
// Using Polly
public class ExternalServiceClient
{
    private readonly HttpClient _client;
    private readonly AsyncCircuitBreakerPolicy _circuitBreaker;

    public ExternalServiceClient(HttpClient client)
    {
        _client = client;
        _circuitBreaker = Policy
            .Handle<HttpRequestException>()
            .CircuitBreakerAsync(
                exceptionsAllowedBeforeBreaking: 5,
                durationOfBreak: TimeSpan.FromSeconds(30),
                onBreak: (ex, duration) =>
                    Log.Warning("Circuit opened for {Duration}s", duration.TotalSeconds),
                onReset: () =>
                    Log.Information("Circuit closed"),
                onHalfOpen: () =>
                    Log.Information("Circuit half-open, testing...")
            );
    }

    public async Task<T> GetAsync<T>(string endpoint)
    {
        return await _circuitBreaker.ExecuteAsync(async () =>
        {
            var response = await _client.GetAsync(endpoint);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<T>();
        });
    }
}
```

### Retry with Exponential Backoff

```csharp
var retryPolicy = Policy
    .Handle<HttpRequestException>()
    .WaitAndRetryAsync(
        retryCount: 3,
        sleepDurationProvider: attempt =>
            TimeSpan.FromSeconds(Math.Pow(2, attempt)), // 2, 4, 8 seconds
        onRetry: (ex, delay, attempt, context) =>
            Log.Warning("Retry {Attempt} after {Delay}s: {Error}",
                attempt, delay.TotalSeconds, ex.Message)
    );
```

### Bulkhead Pattern

```csharp
// Isolate failures to prevent cascade
var bulkhead = Policy.BulkheadAsync(
    maxParallelization: 10,      // Max concurrent executions
    maxQueuingActions: 20,       // Max queued requests
    onBulkheadRejectedAsync: context =>
    {
        Log.Warning("Bulkhead rejected request");
        return Task.CompletedTask;
    }
);
```

## Event-Driven Architecture

### Message Queue Pattern

```
┌─────────┐    ┌─────────────┐    ┌─────────────┐
│ Service │───►│   Message   │───►│  Consumer   │
│    A    │    │    Queue    │    │  Service B  │
└─────────┘    │             │    └─────────────┘
               │  (RabbitMQ, │
               │   Kafka,    │    ┌─────────────┐
               │   Azure SB) │───►│  Consumer   │
               └─────────────┘    │  Service C  │
                                  └─────────────┘
```

### Event Sourcing

```csharp
// Store events, not state
public class PatientAggregate
{
    private readonly List<IDomainEvent> _events = new();

    public Guid Id { get; private set; }
    public string Name { get; private set; }
    public PatientStatus Status { get; private set; }

    public void Apply(PatientCreated @event)
    {
        Id = @event.PatientId;
        Name = @event.Name;
        Status = PatientStatus.Active;
        _events.Add(@event);
    }

    public void Apply(PatientNameChanged @event)
    {
        Name = @event.NewName;
        _events.Add(@event);
    }

    // Rebuild state from events
    public static PatientAggregate FromEvents(IEnumerable<IDomainEvent> events)
    {
        var patient = new PatientAggregate();
        foreach (var @event in events)
        {
            patient.Apply((dynamic)@event);
        }
        return patient;
    }
}
```

## Quick Reference: Design Trade-offs

| Decision | Option A | Option B | Consider |
|----------|----------|----------|----------|
| Storage | SQL | NoSQL | Data structure, consistency needs |
| Caching | Redis | In-memory | Distributed needs, size |
| Communication | Sync (HTTP) | Async (Queue) | Coupling, latency tolerance |
| Consistency | Strong | Eventual | Business requirements |
| Scaling | Vertical | Horizontal | Cost, complexity, limits |

## System Design Checklist

- [ ] **Requirements**: Functional + Non-functional defined
- [ ] **Scale**: Expected users, requests/sec, data volume
- [ ] **Availability**: Uptime target (99.9% = 8.76h downtime/year)
- [ ] **Latency**: P50, P95, P99 targets
- [ ] **Data**: Storage type, retention, backup strategy
- [ ] **Caching**: What to cache, invalidation strategy
- [ ] **Security**: Auth, encryption, compliance
- [ ] **Monitoring**: Metrics, logging, alerting
- [ ] **Failure modes**: What happens when X fails?
- [ ] **Cost**: Infrastructure, operational overhead

## Related Skills

- `technical-design-patterns` - Document designs
- `api-design-principles` - API architecture
- `distributed-events-advanced` - Event patterns
