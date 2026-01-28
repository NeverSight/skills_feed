---
name: cache_patterns
router_kit: FullStackKit
description: Instruction set for enabling and operating the Spring Cache abstraction in Spring Boot when implementing application-level caching for performance-sensitive workloads.
allowed-tools: Read, Write, Bash
category: backend
tags: [architecture, automation, best practices, cache patterns, cache-managers, cacheable, caching, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, performance, productivity, programming, project management, quality assurance, refactoring, software engineering, spring-boot, standards, testing, utilities, version control, workflow]
version: 1.1.0
metadata:
  skillport:
    category: auto-healed
    tags:
      - cache_patterns
      - cache_patterns
---

# Spring Boot Cache Abstraction

## Overview

Spring Boot ships with a cache abstraction that wraps expensive service calls
behind annotation-driven caches. This abstraction supports multiple cache
providers (ConcurrentMap, Caffeine, Redis, Ehcache, JCache) without changing
business code. The skill provides a concise workflow for enabling caching,
managing cache lifecycles, and validating behavior in Spring Boot 3.5+ services.

## When to Use

- Add `@Cacheable`, `@CachePut`, or `@CacheEvict` to Spring Boot service methods.
- Configure Caffeine, Redis, or JCache cache managers for Spring Boot.
- Diagnose cache invalidation, eviction scheduling, or cache key issues.
- Expose cache management endpoints or scheduled eviction routines.

Use trigger phrases such as **"implement service caching"**, **"configure
CaffeineCacheManager"**, **"evict caches on update"**, or **"test Spring cache
behavior"** to load this skill.

## Prerequisites

- Java 17+ project based on Spring Boot 3.5.x (records encouraged for DTOs).
- Dependency `spring-boot-starter-cache`; add provider-specific starters as
  needed (`spring-boot-starter-data-redis`, `caffeine`, `ehcache`, etc.).
- Constructor-injected services that expose deterministic method signatures.
- Observability stack (Actuator, Micrometer) when operating caches in
  production.

## Quick Start

1. **Add dependencies**

   ```xml
   <!-- Maven -->
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-cache</artifactId>
   </dependency>
   <dependency> <!-- Optional: Caffeine -->
       <groupId>com.github.ben-manes.caffeine</groupId>
       <artifactId>caffeine</artifactId>
   </dependency>
   ```

   ```gradle
   implementation "org.springframework.boot:spring-boot-starter-cache"
   implementation "com.github.ben-manes.caffeine:caffeine"
   ```

2. **Enable caching**

   ```java
   @Configuration
   @EnableCaching
   class CacheConfig {
       @Bean
       CacheManager cacheManager() {
           return new CaffeineCacheManager("users", "orders");
       }
   }
   ```

3. **Annotate service methods**

   ```java
   @Service
   @CacheConfig(cacheNames = "users")
   class UserService {

       @Cacheable(key = "#id", unless = "#result == null")
       User findUser(Long id) { ... }

       @CachePut(key = "#user.id")
       User refreshUser(User user) { ... }

       @CacheEvict(key = "#id", beforeInvocation = false)
       void deleteUser(Long id) { ... }
   }
   ```

4. **Verify behavior**
   - Run focused unit tests that call cached methods twice and assert repository
     invocations.
   - Inspect Actuator `cache` endpoint (if enabled) for hit/miss counters.

## 🔄 Workflow

> **Kaynak:** [Spring Boot Caching Guide](https://spring.io/guides/gs/caching/) & [Caffeine Cache Best Practices](https://github.com/ben-manes/caffeine/wiki/Best-Practices)

### Aşama 1: Strategy & Provider Selection
- [ ] **Identifying Hot Paths**: En çok beklenen ve nadir değişen veri okuma (I/O) noktalarını belirle.
- [ ] **Provider Selection**: Bellek içi (Caffeine) veya dağıtık (Redis) cache seçimine karar ver.
- [ ] **Key Design**: SpEL kullanarak benzersiz ve tahmin edilebilir cache key strategy'si oluştur.

### Aşama 2: Annotation Implementation
- [ ] **@Cacheable**: Veriyi cache'e yaz we sonraki çağrılarda oradan oku.
- [ ] **@CachePut**: Veri güncellendiğinde cache'i de yenile.
- [ ] **@CacheEvict**: Silme işlemlerinde veya belirli periyotlarda cache'i temizle (`allEntries=true` opsiyonunu değerlendir).

### Aşama 3: LifeCycle & Monitoring
- [ ] **TTL/Eviction**: Veri tazeliği (TTL) ve temizleme (Eviction) politikalarını (LRU/LFU) konfigüre et.
- [ ] **Actuator Audit**: `cache` endpoint'i üzerinden hit/miss oranlarını izle.
- [ ] **Integration Testing**: `@SpringBootTest` ile cache izolasyonunu ve tutarlılığını test et.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Transactional işlemler sırasında cache tutarlılığı (Data drift) bozuluyor mu? |
| 2 | "Cache-aside" veya "ReadOnly" stratejisi doğru uygulandı mı? |
| 3 | Çoklu instance yapısında "Cache Stampede" riski önlendi mi? |

---
*Cache Patterns v2.0 - With Workflow*

## Advanced Options

- Integrate JCache annotations when interoperating with providers that favor
  JSR-107 (`@CacheResult`, `@CacheRemove`). Avoid mixing with Spring annotations
  on the same method.
- Cache reactive return types (`Mono`, `Flux`) or `CompletableFuture` values.
  Spring stores resolved values and resubscribes on hits; consider TTL alignment
  with publisher semantics.
- Apply HTTP caching headers using `CacheControl` when exposing cached responses
  via REST.

## Examples

- Load [`references/cache-examples.md`](references/cache-examples.md) for
  progressive scenarios (basic product cache, conditional caching, multilevel
  eviction, Redis integration).
- Load [`references/cache-core-reference.md`](references/cache-core-reference.md)
  for annotation matrices, configuration tables, and property samples.

## References

- [`references/spring-framework-cache-docs.md`](references/spring-framework-cache-docs.md):
  curated excerpts from the Spring Framework Reference Guide (official).
- [`references/spring-cache-doc-snippet.md`](references/spring-cache-doc-snippet.md):
  narrative overview extracted from Spring documentation.
- [`references/cache-core-reference.md`](references/cache-core-reference.md):
  annotation parameters, dependency matrices, property catalogs.
- [`references/cache-examples.md`](references/cache-examples.md):
  end-to-end examples with tests.

## Best Practices

- Prefer constructor injection and immutable DTOs for cache entries.
- Separate cache names per aggregate (`users`, `orders`) to simplify eviction.
- Log cache hits/misses only at debug to avoid noise; push metrics via Micrometer.
- Tune TTLs based on data staleness tolerance; document rationale in code.
- Guard caches that store PII or credentials with encryption or avoid caching.
- Align cache eviction with transactional boundaries to prevent dirty reads.

## Constraints and Warnings

- Avoid caching mutable entities that depend on open persistence contexts.
- Do not mix Spring cache annotations with JCache annotations on the same
  method.
- Ensure multi-level caches (e.g. Caffeine + Redis) maintain consistency; prefer
  publish/subscribe invalidation channels.
- Validate serialization compatibility when caching across service instances.
- Monitor memory footprint to prevent OOM when using in-memory stores.

## Related Skills

- [`skills/spring-boot/spring-boot-rest-api-standards`](../spring-boot-rest-api-standards/SKILL.md)
- [`skills/spring-boot/spring-boot-test-patterns`](../spring-boot-test-patterns/SKILL.md)
- [`skills/junit-test/unit-test-caching`](../../junit-test/unit-test-caching/SKILL.md)
