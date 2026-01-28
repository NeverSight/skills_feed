---
name: kotlin-patterns
description: Kotlin/Spring Boot patterns for Orca service - use when implementing backend features, writing services, repositories, or controllers
---

# Kotlin Patterns for Orca

## Entity Pattern

```kotlin
data class EntityName(
    val id: UUID,
    val name: String,
    val createdAt: Instant,
    val updatedAt: Instant?
)
```

## Service Pattern

```kotlin
@Service
class EntityNameService(
    private val repository: EntityNameRepository,
    private val relatedService: RelatedService
) {
    @Transactional(propagation = Propagation.NEVER)
    fun create(request: CreateRequest): Pair<EntityResponse, Boolean> {
        // Check exists, validate, create
        // Return Pair for idempotent operations
    }

    fun findById(id: UUID): EntityName? =
        repository.findById(id)

    fun findAll(): List<EntityName> =
        repository.findAll()
}
```

## Repository Pattern (JOOQ)

```kotlin
@Repository
class EntityNameRepository(
    private val dsl: DSLContext
) {
    fun findById(id: UUID): EntityName? =
        dsl.selectFrom(ENTITY_NAME)
            .where(ENTITY_NAME.ID.eq(id))
            .fetchOne()
            ?.toEntity()

    fun findAll(): List<EntityName> =
        dsl.selectFrom(ENTITY_NAME)
            .fetch()
            .map { it.toEntity() }

    fun save(entity: EntityName): EntityName =
        dsl.insertInto(ENTITY_NAME)
            .set(ENTITY_NAME.ID, entity.id)
            .set(ENTITY_NAME.NAME, entity.name)
            .set(ENTITY_NAME.CREATED_AT, entity.createdAt)
            .returning()
            .fetchOne()!!
            .toEntity()

    private fun EntityNameRecord.toEntity() = EntityName(
        id = id,
        name = name,
        createdAt = createdAt,
        updatedAt = updatedAt
    )
}
```

## Controller Pattern

```kotlin
@RestController
class EntityNameController(
    private val service: EntityNameService
) : EntityNameApi {

    override fun create(request: CreateRequest): ResponseEntity<EntityResponse> {
        val (result, isNew) = service.create(request)
        return if (isNew) ResponseEntity.status(201).body(result)
        else ResponseEntity.ok(result)
    }

    override fun getById(id: UUID): ResponseEntity<EntityResponse> {
        val entity = service.findById(id)
            ?: throw ResourceNotFoundRestException("EntityName", id)
        return ResponseEntity.ok(entity.toResponse())
    }
}
```

## API Interface Pattern

```kotlin
@Tag(name = "Entity Name")
interface EntityNameApi {

    @Operation(summary = "Create entity")
    @PostMapping("/api/v1/entities")
    fun create(@RequestBody @Valid request: CreateRequest): ResponseEntity<EntityResponse>

    @Operation(summary = "Get entity by ID")
    @GetMapping("/api/v1/entities/{id}")
    fun getById(@PathVariable id: UUID): ResponseEntity<EntityResponse>
}
```

## DTO Pattern

```kotlin
data class CreateRequest(
    @field:NotBlank
    val name: String,

    @field:Size(max = 255)
    val description: String?
)

data class EntityResponse(
    val id: UUID,
    val name: String,
    val description: String?,
    val createdAt: Instant
)
```

## Exception Pattern

```kotlin
// Use typed exceptions
throw ResourceNotFoundRestException("EntityName", id)
throw ValidationRestException("Name cannot be empty")
throw ConflictRestException("Entity already exists")
```

## Null Safety Guidelines

- Use `?.let{}` for optional operations
- Use `when` for exhaustive matching
- Avoid `!!` - use `.single()`, `.firstOrNull()` instead
- Return `Pair<Result, Boolean>` for idempotent operations
