---
name: go-create-cache
description: Generate Go cache implementations following GO modular architechture conventions. Use when creating cache layers in internal/modules/<module>/cache/ - user state caching, session caching, rate limiting data, temporary data storage, or any domain cache that uses Redis for fast data access with TTL support.
---

# Go Create Cache

Generate cache files for Go backend using Redis.

## Two-File Pattern

Every cache requires two files:

1. **Port interface**: `internal/modules/<module>/ports/<cache_name>_cache.go`
2. **Cache implementation**: `internal/modules/<module>/cache/<cache_name>_cache.go`

### Port File Layout Order

1. Interface definition (`XxxCache` — no suffix)

### Cache File Layout Order

1. Constants (cache key prefix, TTL)
2. Implementation struct (`XxxCache`)
3. Compile-time interface assertion
4. Constructor (`NewXxxCache`)
5. Methods (`Set`, `Get`, `Delete`, etc.)
6. Helper methods (`buildKey`, etc.)

## Port Interface Structure

**Location**: `internal/modules/<module>/ports/<cache_name>_cache.go`

```go
package ports

type UserActivatedCache interface {
	Set(userID uint64) error
	Get(userID uint64) (bool, error)
	Delete(userID uint64) error
}
```

## Cache Implementation Structure

**Location**: `internal/modules/<module>/cache/<cache_name>_cache.go`

```go
package cache

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/cristiano-pacheco/bricks/pkg/redis"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
)

const (
	cacheKeyPrefix = "entity_name:"
	cacheTTLMin    = 23 * time.Hour
	cacheTTLMax    = 25 * time.Hour
)

type EntityCache struct {
	redisClient redis.UniversalClient
}

var _ ports.EntityCache = (*EntityCache)(nil)

func NewEntityCache(redisClient redis.UniversalClient) *EntityCache {
	return &EntityCache{
		redisClient: redisClient,
	}
}

func (c *EntityCache) Set(id uint64) error {
	key := c.buildKey(id)
	ctx := context.Background()

	ttl := c.calculateTTL()
	return c.redisClient.Set(ctx, key, "1", ttl).Err()
}

func (c *EntityCache) calculateTTL() time.Duration {
	min := cacheTTLMin.Milliseconds()
	max := cacheTTLMax.Milliseconds()
	randomMs := min + rand.Int63n(max-min+1)
	return time.Duration(randomMs) * time.Millisecond
}

func (c *EntityCache) Get(id uint64) (bool, error) {
	key := c.buildKey(id)
	ctx := context.Background()

	result := c.redisClient.Get(ctx, key)
	if err := result.Err(); err != nil {
		if errors.Is(err, redisClient.Nil) {
			return false, nil // Key does not exist
		}
		return false, err
	}

	return true, nil
}

func (c *EntityCache) Delete(id uint64) error {
	key := c.buildKey(id)
	ctx := context.Background()

	return c.redisClient.Del(ctx, key).Err()
}

func (c *EntityCache) buildKey(id uint64) string {
	return fmt.Sprintf("%s%d", cacheKeyPrefix, id)
}
```

## Cache Variants

### Boolean flag cache (Set/Get/Delete)

Use when caching simple existence or state flags.

Port (`ports/user_activated_cache.go`):

```go
type UserActivatedCache interface {
	Set(userID uint64) error
	Get(userID uint64) (bool, error)
	Delete(userID uint64) error
}
```

Implementation notes:
- Store `"1"` as value for true state
- Return `false, nil` when key doesn't exist (not an error)
- Use `errors.Is(err, redisClient.Nil)` to detect missing keys

### Value cache (Set/Get/Delete with data)

Use when caching structured data or strings.

Port (`ports/session_cache.go`):

```go
type SessionCache interface {
	Set(sessionID string, data SessionData) error
	Get(sessionID string) (*SessionData, error)
	Delete(sessionID string) error
}
```

Implementation notes:
- Serialize data with `json.Marshal` before storing
- Deserialize with `json.Unmarshal` when retrieving
- Return `nil, nil` when key doesn't exist (not an error)
- TTL is internal to the cache implementation with randomized range to prevent cache stampede

## Redis Client Usage

The cache uses `redis.UniversalClient` directly from the Bricks Redis package (`github.com/cristiano-pacheco/bricks/pkg/redis`).

Common operations:
- `Set(ctx, key, value, ttl)` - Store value with TTL
- `Get(ctx, key)` - Retrieve value
- `Del(ctx, key)` - Delete key
- `Exists(ctx, key)` - Check if key exists
- `Incr(ctx, key)` - Increment counter
- `Expire(ctx, key, ttl)` - Set TTL on existing key

## Key Building

Always use a helper method to build cache keys consistently:

```go
func (c *EntityCache) buildKey(id uint64) string {
	return fmt.Sprintf("%s%d", cacheKeyPrefix, id)
}
```

For string IDs:

```go
func (c *EntityCache) buildKey(id string) string {
	return fmt.Sprintf("%s%s", cacheKeyPrefix, id)
}
```

For composite keys:

```go
func (c *EntityCache) buildKey(userID uint64, resourceID string) string {
	return fmt.Sprintf("%s%d:%s", cacheKeyPrefix, userID, resourceID)
}
```

## TTL Configuration

Define TTL as a range at the package level to prevent cache stampede (multiple entries expiring simultaneously):

```go
const (
	cacheKeyPrefix    = "entity_name:"
	cacheTTLMin       = 12 * time.Hour  // Minimum TTL
	cacheTTLMax       = 24 * time.Hour  // Maximum TTL
)
```

Use a helper function to calculate randomized TTL:

```go
import (
	"math/rand"
	"time"
)

func (c *EntityCache) calculateTTL() time.Duration {
	min := cacheTTLMin.Milliseconds()
	max := cacheTTLMax.Milliseconds()
	randomMs := min + rand.Int63n(max-min+1)
	return time.Duration(randomMs) * time.Millisecond
}
```

Common TTL ranges:
- Short-lived: `4-6 minutes` - Rate limits, OTP codes
- Session data: `50-70 minutes` - User sessions
- Daily data: `12-25 hours` - User activation status, daily metrics
- Weekly data: `6.5-7.5 days` - Weekly aggregations

**Why randomized TTL?** When many cache entries are created at the same time (e.g., during traffic spikes), they would all expire simultaneously, causing a "thundering herd" to the database. Randomizing TTL spreads out expirations over time.

## Error Handling

### Missing Key vs Error

Distinguish between "key not found" (normal) and actual errors:

```go
result := client.Get(ctx, key)
if err := result.Err(); err != nil {
	if errors.Is(err, redisClient.Nil) {
		return false, nil // Key doesn't exist - not an error
	}
	return false, err // Actual error
}
```


## Context Usage

Use `context.Background()` for cache operations unless you have a specific context:

```go
ctx := context.Background()
```

For operations called from handlers/use cases, accept context as parameter:

```go
func (c *EntityCache) Set(ctx context.Context, id uint64) error {
	key := c.buildKey(id)
	// Use provided ctx
	return c.redisClient.Set(ctx, key, "1", cacheTTL).Err()
}
```

## Naming

- Port interface: `XxxCache` (in `ports` package, no suffix)
- Implementation struct: `XxxCache` (in `cache` package, same name — disambiguated by package)
- Constructor: `NewXxxCache`, returns a pointer of the struct implementation
- Constants: `cacheKeyPrefix` and `cacheTTL` (lowercase, package-level)

## Fx Wiring

Add to `internal/modules/<module>/module.go`:

```go
fx.Provide(
	fx.Annotate(
		cache.NewXxxCache,
		fx.As(new(ports.XxxCache)),
	),
),
```

## Dependencies

Caches depend on:

- `redis.UniversalClient` from `"github.com/cristiano-pacheco/bricks/pkg/redis"` — Redis operations interface

## Example 1: Boolean Flag Cache (User Activation)

Port interface (`ports/user_activated_cache.go`):

```go
package ports

type UserActivatedCache interface {
	Set(userID uint64) error
	Get(userID uint64) (bool, error)
	Delete(userID uint64) error
}
```

Implementation (`cache/user_activated_cache.go`):

```go
package cache

import (
	"context"
	"errors"
	"fmt"
	"strconv"
	"time"

	"github.com/cristiano-pacheco/bricks/pkg/redis"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/ports"
)

const (
	cacheKeyPrefix = "user_activated:"
	cacheTTLMin    = 23 * time.Hour
	cacheTTLMax    = 25 * time.Hour
)

type UserActivatedCache struct {
	redisClient redis.UniversalClient
}

var _ ports.UserActivatedCache = (*UserActivatedCache)(nil)

func NewUserActivatedCache(redisClient redis.UniversalClient) *UserActivatedCache {
	return &UserActivatedCache{
		redisClient: redisClient,
	}
}

func (c *UserActivatedCache) Set(userID uint64) error {
	key := c.buildKey(userID)
	ctx := context.Background()

	ttl := c.calculateTTL()
	return c.redisClient.Set(ctx, key, "1", ttl).Err()
}

func (c *UserActivatedCache) calculateTTL() time.Duration {
	min := cacheTTLMin.Milliseconds()
	max := cacheTTLMax.Milliseconds()
	randomMs := min + rand.Int63n(max-min+1)
	return time.Duration(randomMs) * time.Millisecond
}

func (c *UserActivatedCache) Get(userID uint64) (bool, error) {
	key := c.buildKey(userID)
	ctx := context.Background()

	result := c.redisClient.Get(ctx, key)
	if err := result.Err(); err != nil {
		if errors.Is(err, redisClient.Nil) {
			return false, nil
		}
		return false, err
	}

	return true, nil
}

func (c *UserActivatedCache) Delete(userID uint64) error {
	key := c.buildKey(userID)
	ctx := context.Background()

	return c.redisClient.Del(ctx, key).Err()
}

func (c *UserActivatedCache) buildKey(userID uint64) string {
	return fmt.Sprintf("%s%s", cacheKeyPrefix, strconv.FormatUint(userID, 10))
}
```

Fx wiring (`module.go`):

```go
fx.Provide(
	fx.Annotate(
		cache.NewUserActivatedCache,
		fx.As(new(ports.UserActivatedCache)),
	),
),
```

## Example 2: JSON Data Cache (User Session)

DTO (`dto/user_session_dto.go`):

```go
package dto

import "time"

type UserSessionData struct {
	UserID       uint64    `json:"user_id"`
	Email        string    `json:"email"`
	Name         string    `json:"name"`
	Roles        []string  `json:"roles"`
	LastActivity time.Time `json:"last_activity"`
	IPAddress    string    `json:"ip_address"`
}
```

Port interface (`ports/user_session_cache.go`):

```go
package ports

import (
	"time"

	"github.com/cristiano-pacheco/pingo/internal/modules/identity/dto"
)

type UserSessionCache interface {
	Set(sessionID string, data dto.UserSessionData) error
	Get(sessionID string) (*dto.UserSessionData, error)
	Delete(sessionID string) error
	Exists(sessionID string) (bool, error)
}
```

Implementation (`cache/user_session_cache.go`):

```go
package cache

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"github.com/cristiano-pacheco/bricks/pkg/redis"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/dto"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/ports"
)

const (
	sessionCacheKeyPrefix = "user_session:"
	sessionCacheTTLMin    = 50 * time.Minute
	sessionCacheTTLMax    = 70 * time.Minute
)

type UserSessionCache struct {
	redisClient redis.UniversalClient
}

var _ ports.UserSessionCache = (*UserSessionCache)(nil)

func NewUserSessionCache(redisClient redis.UniversalClient) *UserSessionCache {
	return &UserSessionCache{
		redisClient: redisClient,
	}
}

func (c *UserSessionCache) Set(sessionID string, data dto.UserSessionData) error {
	key := c.buildKey(sessionID)
	ctx := context.Background()

	jsonData, err := json.Marshal(data)
	if err != nil {
		return fmt.Errorf("failed to marshal session data: %w", err)
	}

	ttl := c.calculateTTL()
	return c.redisClient.Set(ctx, key, jsonData, ttl).Err()
}

func (c *UserSessionCache) calculateTTL() time.Duration {
	min := sessionCacheTTLMin.Milliseconds()
	max := sessionCacheTTLMax.Milliseconds()
	randomMs := min + rand.Int63n(max-min+1)
	return time.Duration(randomMs) * time.Millisecond
}

func (c *UserSessionCache) Get(sessionID string) (*dto.UserSessionData, error) {
	key := c.buildKey(sessionID)
	ctx := context.Background()

	result := c.redisClient.Get(ctx, key)
	if err := result.Err(); err != nil {
		if errors.Is(err, redisClient.Nil) {
			return nil, nil
		}
		return nil, err
	}

	jsonData, err := result.Bytes()
	if err != nil {
		return nil, fmt.Errorf("failed to get bytes: %w", err)
	}

	var data dto.UserSessionData
	if err := json.Unmarshal(jsonData, &data); err != nil {
		return nil, fmt.Errorf("failed to unmarshal session data: %w", err)
	}

	return &data, nil
}

func (c *UserSessionCache) Delete(sessionID string) error {
	key := c.buildKey(sessionID)
	ctx := context.Background()

	return c.redisClient.Del(ctx, key).Err()
}

func (c *UserSessionCache) Exists(sessionID string) (bool, error) {
	key := c.buildKey(sessionID)
	ctx := context.Background()

	result := c.redisClient.Exists(ctx, key)
	if err := result.Err(); err != nil {
		return false, err
	}

	return result.Val() > 0, nil
}

func (c *UserSessionCache) buildKey(sessionID string) string {
	return fmt.Sprintf("%s%s", sessionCacheKeyPrefix, sessionID)
}
```

Fx wiring (`module.go`):

```go
fx.Provide(
	fx.Annotate(
		cache.NewUserSessionCache,
		fx.As(new(ports.UserSessionCache)),
	),
),
```

## Example 3: Protobuf Data Cache (User Profile)

Proto definition (`proto/user_profile.proto`):

```protobuf
syntax = "proto3";

package identity;

option go_package = "github.com/cristiano-pacheco/pingo/internal/modules/identity/proto";

message UserProfile {
	uint64 user_id = 1;
	string email = 2;
	string name = 3;
	repeated string roles = 4;
	int64 last_login = 5;
	string avatar_url = 6;
}
```

Port interface (`ports/user_profile_cache.go`):

```go
package ports

import (
	"time"

	"github.com/cristiano-pacheco/pingo/internal/modules/identity/proto"
)

type UserProfileCache interface {
	Set(userID uint64, profile *proto.UserProfile) error
	Get(userID uint64) (*proto.UserProfile, error)
	Delete(userID uint64) error
}
```

Implementation (`cache/user_profile_cache.go`):

```go
package cache

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/cristiano-pacheco/bricks/pkg/redis"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/ports"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/proto"
	"google.golang.org/protobuf/proto"
)

const (
	profileCacheKeyPrefix = "user_profile:"
	profileCacheTTLMin    = 12 * time.Hour
	profileCacheTTLMax    = 24 * time.Hour
)

type UserProfileCache struct {
	redisClient redis.UniversalClient
}

var _ ports.UserProfileCache = (*UserProfileCache)(nil)

func NewUserProfileCache(redisClient redis.UniversalClient) *UserProfileCache {
	return &UserProfileCache{
		redisClient: redisClient,
	}
}

func (c *UserProfileCache) Set(userID uint64, profile *proto.UserProfile) error {
	key := c.buildKey(userID)
	ctx := context.Background()

	data, err := proto.Marshal(profile)
	if err != nil {
		return fmt.Errorf("failed to marshal profile: %w", err)
	}

	ttl := c.calculateTTL()
	return c.redisClient.Set(ctx, key, data, ttl).Err()
}

func (c *UserProfileCache) calculateTTL() time.Duration {
	min := profileCacheTTLMin.Milliseconds()
	max := profileCacheTTLMax.Milliseconds()
	randomMs := min + rand.Int63n(max-min+1)
	return time.Duration(randomMs) * time.Millisecond
}

func (c *UserProfileCache) Get(userID uint64) (*proto.UserProfile, error) {
	key := c.buildKey(userID)
	ctx := context.Background()

	result := c.redisClient.Get(ctx, key)
	if err := result.Err(); err != nil {
		if errors.Is(err, redisClient.Nil) {
			return nil, nil
		}
		return nil, err
	}

	data, err := result.Bytes()
	if err != nil {
		return nil, fmt.Errorf("failed to get bytes: %w", err)
	}

	var profile proto.UserProfile
	if err := proto.Unmarshal(data, &profile); err != nil {
		return nil, fmt.Errorf("failed to unmarshal profile: %w", err)
	}

	return &profile, nil
}

func (c *UserProfileCache) Delete(userID uint64) error {
	key := c.buildKey(userID)
	ctx := context.Background()

	return c.redisClient.Del(ctx, key).Err()
}

func (c *UserProfileCache) buildKey(userID uint64) string {
	return fmt.Sprintf("%s%d", profileCacheKeyPrefix, userID)
}
```

Fx wiring (`module.go`):

```go
fx.Provide(
	fx.Annotate(
		cache.NewUserProfileCache,
		fx.As(new(ports.UserProfileCache)),
	),
),
```

## Critical Rules

1. **Two files**: Port interface in `ports/`, implementation in `cache/`
2. **Interface in ports**: Interface lives in `ports/<name>_cache.go`
3. **Interface assertion**: Add `var _ ports.XxxCache = (*XxxCache)(nil)` below the struct
4. **Constructor**: MUST return pointer `*XxxCache`
5. **Constants**: Define `cacheKeyPrefix`, `cacheTTLMin`, and `cacheTTLMax` at package level
6. **Randomized TTL**: MUST use `calculateTTL()` helper to prevent cache stampede
7. **Key builder**: Always use a `buildKey()` helper method
8. **Missing keys**: Return zero value + nil error, not an error (use `errors.Is(err, redisClient.Nil)`)
9. **Context**: Use `context.Background()` or accept `context.Context` parameter
10. **No comments**: Do not add redundant comments above methods
11. **Add detailed comment on interfaces**: Provide comprehensive comments on the port interfaces to describe their purpose and usage
12. **Redis client type**: Use `redis.UniversalClient` interface
13. **No TTL parameters**: TTL is internal to cache, never exposed in interface methods

## Workflow

1. Create port interface in `ports/<name>_cache.go`
2. Create cache implementation in `cache/<name>_cache.go`
3. Add Fx wiring to module's `module.go`
4. Run `make lint` to verify
5. Run `make nilaway` for static analysis
