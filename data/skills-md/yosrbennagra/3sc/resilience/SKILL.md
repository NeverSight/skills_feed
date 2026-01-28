---
name: resilience
description: Resilience patterns for the 3SC widget host. Covers retry policies, circuit breakers, timeouts, fallbacks, and graceful degradation for external dependencies.
---

# Resilience

## Overview

Desktop applications must handle failures gracefully - network issues, database locks, external service outages. This skill covers patterns for building resilient features.

## Definition of Done (DoD)

- [ ] External API calls have retry policies with exponential backoff
- [ ] Database operations handle transient failures (SQLITE_BUSY)
- [ ] Network operations have reasonable timeouts
- [ ] Failed operations provide user feedback
- [ ] Critical paths have fallback strategies
- [ ] Circuit breaker prevents cascade failures

## Resilience Patterns

### 1. Retry with Exponential Backoff

```csharp
public class RetryPolicy
{
    private static readonly Random Jitter = new();
    
    public static async Task<T> ExecuteAsync<T>(
        Func<CancellationToken, Task<T>> operation,
        int maxRetries = 3,
        TimeSpan? initialDelay = null,
        CancellationToken cancellationToken = default)
    {
        var delay = initialDelay ?? TimeSpan.FromMilliseconds(200);
        Exception? lastException = null;
        
        for (int attempt = 0; attempt <= maxRetries; attempt++)
        {
            try
            {
                return await operation(cancellationToken).ConfigureAwait(false);
            }
            catch (Exception ex) when (IsTransient(ex) && attempt < maxRetries)
            {
                lastException = ex;
                Log.Warning(ex, "Transient failure on attempt {Attempt}/{MaxRetries}", 
                    attempt + 1, maxRetries + 1);
                
                // Exponential backoff with jitter
                var jitteredDelay = delay + TimeSpan.FromMilliseconds(Jitter.Next(0, 100));
                await Task.Delay(jitteredDelay, cancellationToken).ConfigureAwait(false);
                delay *= 2;  // Double for next attempt
            }
        }
        
        throw lastException!;
    }
    
    private static bool IsTransient(Exception ex) => ex switch
    {
        HttpRequestException => true,
        TimeoutException => true,
        TaskCanceledException => false,  // User cancellation
        Microsoft.Data.Sqlite.SqliteException sqEx => 
            sqEx.SqliteErrorCode == 5,   // SQLITE_BUSY
        _ => false
    };
}
```

### 2. Circuit Breaker

Prevents repeated calls to failing services:

```csharp
public class CircuitBreaker
{
    private readonly int _failureThreshold;
    private readonly TimeSpan _resetTimeout;
    private readonly object _lock = new();
    
    private int _failureCount;
    private CircuitState _state = CircuitState.Closed;
    private DateTimeOffset _lastFailureTime;
    
    public CircuitBreaker(int failureThreshold = 5, TimeSpan? resetTimeout = null)
    {
        _failureThreshold = failureThreshold;
        _resetTimeout = resetTimeout ?? TimeSpan.FromMinutes(1);
    }
    
    public async Task<T> ExecuteAsync<T>(Func<Task<T>> operation, Func<T>? fallback = null)
    {
        lock (_lock)
        {
            if (_state == CircuitState.Open)
            {
                if (DateTimeOffset.UtcNow - _lastFailureTime >= _resetTimeout)
                {
                    _state = CircuitState.HalfOpen;
                    Log.Information("Circuit breaker entering half-open state");
                }
                else
                {
                    Log.Warning("Circuit breaker is open, using fallback");
                    if (fallback != null) return fallback();
                    throw new CircuitBreakerOpenException();
                }
            }
        }
        
        try
        {
            var result = await operation().ConfigureAwait(false);
            
            lock (_lock)
            {
                _failureCount = 0;
                _state = CircuitState.Closed;
            }
            
            return result;
        }
        catch (Exception ex)
        {
            lock (_lock)
            {
                _failureCount++;
                _lastFailureTime = DateTimeOffset.UtcNow;
                
                if (_failureCount >= _failureThreshold)
                {
                    _state = CircuitState.Open;
                    Log.Warning("Circuit breaker opened after {Count} failures", _failureCount);
                }
            }
            
            if (fallback != null) return fallback();
            throw;
        }
    }
    
    public CircuitState State => _state;
}

public enum CircuitState { Closed, Open, HalfOpen }

public class CircuitBreakerOpenException : Exception
{
    public CircuitBreakerOpenException() 
        : base("Circuit breaker is open. Service is temporarily unavailable.") { }
}
```

### 3. Timeout Policy

```csharp
public static class TimeoutPolicy
{
    public static async Task<T> ExecuteAsync<T>(
        Func<CancellationToken, Task<T>> operation,
        TimeSpan timeout,
        CancellationToken cancellationToken = default)
    {
        using var cts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        cts.CancelAfter(timeout);
        
        try
        {
            return await operation(cts.Token).ConfigureAwait(false);
        }
        catch (OperationCanceledException) when (!cancellationToken.IsCancellationRequested)
        {
            throw new TimeoutException($"Operation timed out after {timeout.TotalSeconds}s");
        }
    }
}
```

### 4. Fallback Strategy

```csharp
public class FallbackPolicy<T>
{
    private readonly Func<Task<T>> _primaryOperation;
    private readonly Func<Exception, Task<T>> _fallbackOperation;
    private readonly Func<T>? _cachedFallback;
    
    public FallbackPolicy(
        Func<Task<T>> primary,
        Func<Exception, Task<T>>? fallback = null,
        Func<T>? cached = null)
    {
        _primaryOperation = primary;
        _fallbackOperation = fallback ?? (_ => Task.FromResult(default(T)!));
        _cachedFallback = cached;
    }
    
    public async Task<T> ExecuteAsync()
    {
        try
        {
            return await _primaryOperation().ConfigureAwait(false);
        }
        catch (Exception ex)
        {
            Log.Warning(ex, "Primary operation failed, trying fallback");
            
            try
            {
                return await _fallbackOperation(ex).ConfigureAwait(false);
            }
            catch (Exception fallbackEx)
            {
                Log.Error(fallbackEx, "Fallback operation also failed");
                
                if (_cachedFallback != null)
                {
                    Log.Information("Using cached fallback value");
                    return _cachedFallback();
                }
                
                throw;
            }
        }
    }
}
```

## Database Resilience

### SQLite Busy Handling

```csharp
public class ResilientDbContext : AppDbContext
{
    private const int MaxRetries = 3;
    private static readonly TimeSpan InitialDelay = TimeSpan.FromMilliseconds(50);
    
    public override async Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        return await RetryPolicy.ExecuteAsync(
            async token => await base.SaveChangesAsync(token),
            maxRetries: MaxRetries,
            initialDelay: InitialDelay,
            cancellationToken: ct);
    }
}
```

### Connection Pooling

```csharp
// In ServiceLocator - use factory pattern
private readonly Lazy<IDbContextFactory<AppDbContext>> _dbContextFactory;

// Create context per operation
public async Task DoWorkAsync()
{
    await using var context = _dbContextFactory.Value.CreateDbContext();
    // Use context...
}
```

## Network Resilience

### HTTP Client Configuration

```csharp
public class ResilientHttpClientFactory
{
    private static readonly CircuitBreaker _circuitBreaker = new(failureThreshold: 5);
    
    public static HttpClient Create(TimeSpan? timeout = null)
    {
        var handler = new SocketsHttpHandler
        {
            PooledConnectionLifetime = TimeSpan.FromMinutes(2),
            PooledConnectionIdleTimeout = TimeSpan.FromMinutes(1),
            ConnectTimeout = TimeSpan.FromSeconds(10),
        };
        
        return new HttpClient(handler)
        {
            Timeout = timeout ?? TimeSpan.FromSeconds(30)
        };
    }
    
    public static async Task<HttpResponseMessage> SendWithResilienceAsync(
        HttpClient client,
        HttpRequestMessage request,
        CancellationToken ct = default)
    {
        return await _circuitBreaker.ExecuteAsync(async () =>
        {
            return await RetryPolicy.ExecuteAsync(
                async token =>
                {
                    var response = await client.SendAsync(request, token);
                    response.EnsureSuccessStatusCode();
                    return response;
                },
                maxRetries: 3,
                cancellationToken: ct);
        });
    }
}
```

## Offline-First Pattern

```csharp
public class OfflineFirstService<T>
{
    private readonly IRepository<T> _localRepository;
    private readonly IRemoteApi<T> _remoteApi;
    private readonly ISyncQueue _syncQueue;
    
    public async Task<IReadOnlyList<T>> GetAllAsync(CancellationToken ct)
    {
        // Always return local data immediately
        var localData = await _localRepository.GetAllAsync(ct);
        
        // Try to sync in background
        _ = TrySyncAsync(ct);
        
        return localData;
    }
    
    private async Task TrySyncAsync(CancellationToken ct)
    {
        try
        {
            var remoteData = await TimeoutPolicy.ExecuteAsync(
                token => _remoteApi.FetchAllAsync(token),
                timeout: TimeSpan.FromSeconds(10),
                cancellationToken: ct);
                
            await _localRepository.UpsertManyAsync(remoteData, ct);
        }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            Log.Warning(ex, "Background sync failed, will retry later");
            // Queue for later retry
        }
    }
}
```

## Graceful Degradation

### Feature Flags for Degraded Mode

```csharp
public class FeatureAvailability
{
    private static readonly ConcurrentDictionary<string, bool> _features = new();
    
    public static bool IsAvailable(string feature) => 
        _features.GetOrAdd(feature, _ => true);
    
    public static void Disable(string feature)
    {
        _features[feature] = false;
        Log.Warning("Feature {Feature} has been disabled", feature);
    }
    
    public static void Enable(string feature)
    {
        _features[feature] = true;
        Log.Information("Feature {Feature} has been enabled", feature);
    }
}

// Usage in ViewModel
public async Task SyncWithCloudAsync()
{
    if (!FeatureAvailability.IsAvailable("cloud-sync"))
    {
        ShowMessage("Cloud sync is temporarily unavailable");
        return;
    }
    
    try
    {
        await _syncService.SyncAsync();
    }
    catch (CircuitBreakerOpenException)
    {
        FeatureAvailability.Disable("cloud-sync");
        ShowMessage("Cloud sync disabled due to connectivity issues");
    }
}
```

## Monitoring Resilience

```csharp
public static class ResilienceMetrics
{
    private static int _retryCount;
    private static int _circuitBreakerTrips;
    private static int _fallbackUsed;
    
    public static void RecordRetry() => Interlocked.Increment(ref _retryCount);
    public static void RecordCircuitBreakerTrip() => Interlocked.Increment(ref _circuitBreakerTrips);
    public static void RecordFallback() => Interlocked.Increment(ref _fallbackUsed);
    
    public static (int Retries, int CircuitBreakerTrips, int Fallbacks) GetMetrics() =>
        (_retryCount, _circuitBreakerTrips, _fallbackUsed);
}
```

## Best Practices

| Practice | Reason |
|----------|--------|
| Set timeouts on all external calls | Prevent indefinite hangs |
| Use exponential backoff | Reduce load on failing services |
| Add jitter to retries | Prevent thundering herd |
| Log retry attempts | Aid debugging |
| Provide fallback UI | Keep app usable during failures |
| Monitor failure rates | Detect degradation early |

## References

- [Polly Library](https://github.com/App-vNext/Polly) - Consider for complex scenarios
- [Release It! by Michael Nygard](https://pragprog.com/titles/mnee2/release-it-second-edition/)
- [Circuit Breaker Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
