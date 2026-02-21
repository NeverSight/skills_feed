---
name: android-data-persistence
description: "Android data persistence standards with Room as primary local storage and custom API backends for cloud sync. Covers SharedPreferences, DataStore, Room (entities, DAOs, relations, migrations), file storage, offline-first architecture, and repository pattern for API-backed sync. Use when implementing any data storage, caching, or sync feature in Android apps."
---

# Android Data Persistence

## Overview

Our apps use **Room** for local persistence and **custom REST API backends** for cloud data. This skill covers every storage method and when to use each.

Android 10+ required.

**Architecture:** Offline-first with API sync via Repository pattern.

**Backend Environments:** APIs run on Windows dev (MySQL 8.4.7), Ubuntu staging (MySQL 8.x), Debian production (MySQL 8.x). Use Gradle build flavors for environment-specific base URLs. All backends use `utf8mb4_unicode_ci` collation.

**Icon Policy:** If any UI code is included, use custom PNG icons and maintain `PROJECT_ICONS.md` (see `android-custom-icons`).

**Report Table Policy:** If persistence examples include report UIs that can exceed 25 rows, use table layouts (see `android-report-tables`).

```
UI (Compose) → ViewModel → Repository → Room (local) + API (remote)
```

## Storage Decision Guide

| Need                        | Solution                      | Complexity  |
| --------------------------- | ----------------------------- | ----------- |
| App settings, flags, tokens | DataStore / SharedPreferences | Very Low    |
| Structured data (offline)   | Room                          | Medium      |
| Large files (images, docs)  | Internal/External files       | Low         |
| Cloud-synced data           | Room + API backend            | Medium-High |
| Real-time shared data       | API with polling/WebSocket    | High        |
| Cached API responses        | Room as cache layer           | Medium      |

### Quick Decision

```
"I need to store..."
├── Settings/tokens/flags → DataStore (Preferences)
├── A single file → Internal storage
├── Structured local data → Room
├── Data from our API → Room cache + Repository sync
└── User-generated media → Internal files + API upload
```

## Quick Reference

| Topic                 | Reference File                    | When to Use                                    |
| --------------------- | --------------------------------- | ---------------------------------------------- |
| **Room Essentials**   | `references/room-essentials.md`   | Entities, DAOs, Database setup, TypeConverters |
| **Room Advanced**     | `references/room-advanced.md`     | Relations, migrations, testing, performance    |
| **Local Storage**     | `references/local-storage.md`     | DataStore, SharedPreferences, file I/O         |
| **API Sync Patterns** | `references/api-sync-patterns.md` | Offline-first, Repository, cache strategies    |

## Room: The Primary Local Database

Room is our **standard** for all structured local data. It provides compile-time SQL verification, lifecycle-aware queries, and clean integration with ViewModels.

### Three Core Components

```
@Entity       → Defines a database table (data class)
@Dao          → Defines operations (interface)
@Database     → Connects entities and DAOs (abstract class)
```

### Entity (Table Definition)

```kotlin
@Entity(tableName = "products")
data class ProductEntity(
    @PrimaryKey
    @ColumnInfo(name = "product_id")
    val productId: String,

    @ColumnInfo(name = "name")
    val name: String,

    @ColumnInfo(name = "price")
    val price: Double,

    @ColumnInfo(name = "category_id")
    val categoryId: String,

    @ColumnInfo(name = "last_synced")
    val lastSynced: Long = System.currentTimeMillis()
)
```

### DAO (Data Access)

```kotlin
@Dao
interface ProductDao {
    @Query("SELECT * FROM products ORDER BY name ASC")
    fun getAllProducts(): Flow<List<ProductEntity>>

    @Query("SELECT * FROM products WHERE product_id = :id")
    suspend fun getById(id: String): ProductEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(products: List<ProductEntity>)

    @Update
    suspend fun update(product: ProductEntity)

    @Delete
    suspend fun delete(product: ProductEntity)

    @Query("DELETE FROM products")
    suspend fun deleteAll()
}
```

### Database

```kotlin
@Database(
    entities = [ProductEntity::class, CategoryEntity::class],
    version = 1,
    exportSchema = true
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun productDao(): ProductDao
    abstract fun categoryDao(): CategoryDao
}
```

### Hilt Module for Database

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        )
        .addMigrations(MIGRATION_1_2)
        .build()
    }

    @Provides
    fun provideProductDao(database: AppDatabase): ProductDao = database.productDao()
}
```

## Repository Pattern (Room + API)

The Repository is the **single source of truth** for data:

```kotlin
class ProductRepository @Inject constructor(
    private val productDao: ProductDao,
    private val apiService: ProductApiService
) {
    // Local data as Flow (always fresh from Room)
    fun getProducts(): Flow<List<Product>> =
        productDao.getAllProducts().map { entities ->
            entities.map { it.toDomain() }
        }

    // Sync: fetch from API, save to Room
    suspend fun refreshProducts(): Result<Unit> {
        return try {
            val response = apiService.getProducts()
            productDao.insertAll(response.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // Create: save locally + push to API
    suspend fun createProduct(product: Product): Result<Product> {
        return try {
            val response = apiService.createProduct(product.toDto())
            val entity = response.toEntity()
            productDao.insertAll(listOf(entity))
            Result.success(entity.toDomain())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

## ViewModel Integration

```kotlin
@HiltViewModel
class ProductViewModel @Inject constructor(
    private val repository: ProductRepository
) : ViewModel() {

    val products = repository.getProducts()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    private val _isRefreshing = MutableStateFlow(false)
    val isRefreshing = _isRefreshing.asStateFlow()

    fun refresh() {
        viewModelScope.launch {
            _isRefreshing.value = true
            repository.refreshProducts()
            _isRefreshing.value = false
        }
    }
}
```

## DataStore (Settings & Preferences)

**Prefer DataStore over SharedPreferences** for new code:

```kotlin
// Define keys
object PrefsKeys {
    val DARK_MODE = booleanPreferencesKey("dark_mode")
    val AUTH_TOKEN = stringPreferencesKey("auth_token")
    val SORT_ORDER = stringPreferencesKey("sort_order")
}

// Read
val darkMode: Flow<Boolean> = context.dataStore.data.map { prefs ->
    prefs[PrefsKeys.DARK_MODE] ?: false
}

// Write
suspend fun setDarkMode(enabled: Boolean) {
    context.dataStore.edit { prefs ->
        prefs[PrefsKeys.DARK_MODE] = enabled
    }
}
```

## TypeConverters (Custom Column Types)

```kotlin
class Converters {
    @TypeConverter
    fun fromTimestamp(value: Long?): Date? = value?.let { Date(it) }

    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? = date?.time

    @TypeConverter
    fun fromStringList(value: String?): List<String> =
        value?.split(",") ?: emptyList()

    @TypeConverter
    fun toStringList(list: List<String>): String = list.joinToString(",")
}
```

## Migrations

Always provide migration paths when changing schema:

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE products ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1")
    }
}

// Register in database builder
Room.databaseBuilder(context, AppDatabase::class.java, "app_database")
    .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
    .build()
```

**Never use `fallbackToDestructiveMigration()` in production.**

## Data Layer Mapping

Always separate API DTOs, Room entities, and domain models:

```kotlin
// API DTO (what the server sends)
data class ProductDto(val id: String, val name: String, val price: Double)

// Room Entity (what's stored locally)
@Entity(tableName = "products")
data class ProductEntity(
    @PrimaryKey val productId: String,
    val name: String,
    val price: Double,
    val lastSynced: Long
)

// Domain Model (what the UI uses)
data class Product(val id: String, val name: String, val price: Double)

// Mappers
fun ProductDto.toEntity() = ProductEntity(id, name, price, System.currentTimeMillis())
fun ProductEntity.toDomain() = Product(productId, name, price)
fun Product.toDto() = ProductDto(id, name, price)
```

## Patterns & Anti-Patterns

### DO

- Use Room for all structured local data
- Use DataStore for key-value preferences (not SharedPreferences)
- Use Repository pattern as single source of truth
- Separate DTOs, entities, and domain models
- Return `Flow` from DAOs for reactive UI updates
- Provide proper migrations for schema changes
- Use `onConflict = REPLACE` for API-synced data
- Export Room schema for migration testing

### DON'T

- Access DAOs directly from ViewModels (use Repository)
- Store large blobs in Room (use file storage)
- Use `fallbackToDestructiveMigration()` in production
- Mix network calls with database operations outside Repository
- Store sensitive data unencrypted (use EncryptedSharedPreferences)
- Skip the entity-to-domain mapping (couples UI to database schema)
- Run Room queries on the main thread

## Integration with Other Skills

```
android-development → Architecture (MVVM, Clean, Hilt DI)
      |
android-data-persistence → Storage, Room, API sync (THIS SKILL)
      |
jetpack-compose-ui → Display data in beautiful UI
      |
android-tdd → Test DAOs, Repositories, ViewModels
```

**Key integrations:**

- **android-development**: Follows Clean Architecture layers
- **android-tdd**: Room in-memory DB testing, MockWebServer for API tests
- **api-error-handling**: Error patterns for API sync failures

## References

- **Room Guide**: developer.android.com/training/data-storage/room
- **DataStore**: developer.android.com/topic/libraries/architecture/datastore
- **Architecture Samples**: github.com/android/architecture-samples
