---
name: data
description: Room ORM, SQLite, SharedPreferences, DataStore, encryption.
version: "2.0.0"
sasmp_version: "1.3.0"

# Agent Binding
bonded_agent: 04-data-management
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: Data persistence & storage

# Parameter Validation
parameters:
  storage_type:
    type: string
    enum: [room, datastore, preferences, encrypted]
    required: false
  operation:
    type: string
    enum: [create, read, update, delete, migrate]
    required: false

# Retry Configuration
retry:
  max_attempts: 2
  backoff: exponential
  on_failure: suggest_transaction_rollback

# Observability
logging:
  level: info
  include: [query, storage_type, security_level]
---

# Data Persistence Skill

## Quick Start

### Room Entity & DAO
```kotlin
@Entity
data class User(@PrimaryKey val id: Int, val name: String)

@Dao
interface UserDao {
    @Query("SELECT * FROM User")
    suspend fun getAllUsers(): List<User>
    
    @Insert
    suspend fun insert(user: User)
}
```

### EncryptedSharedPreferences
```kotlin
val prefs = EncryptedSharedPreferences.create(context, "secret",
    MasterKey.Builder(context).setKeyScheme(AES256_GCM).build(),
    AES256_SIV, AES256_GCM)

prefs.edit { putString("token", value) }
```

### DataStore
```kotlin
val dataStore = context.createDataStore("settings")
val preferences = dataStore.data.map { it[KEY] ?: "" }
```

## Key Concepts

### Room Advantages
- Type-safe queries
- Compile-time checks
- Suspend/Flow support
- Migration management

### SharedPreferences
- Simple key-value store
- Use Encrypted version for sensitive data
- Limited to small data

### DataStore
- Modern SharedPreferences
- Coroutine-native
- Type-safe
- ACID transactions

## Best Practices

✅ Use Room for complex data
✅ Encrypt sensitive data
✅ Implement proper migrations
✅ Handle database errors
✅ Test database operations

## Resources

- [Room Documentation](https://developer.android.com/training/data-storage/room)
- [DataStore Guide](https://developer.android.com/topic/libraries/architecture/datastore)
