---
name: offline-sync
description: Expert in data persistence, local-first architectures, and synchronization strategies for Capacitor/Android applications.
---

# Offline-First & Data Sync Specialist Skill

This skill enables the assistant to design and implement a robust synchronization system to solve the "No Offline Queue" issue (P0).

## Knowledge Areas

### 1. Local Storage (Native)
- **Room Database:** Implementing a local SQLite storage on the Android side to buffer location updates.
- **Data Entities:** Defining schema for `OfflineLocation` that matches the Supabase `registros_reten` structure.

### 2. Synchronization Strategies
- **Background Sync:** Using `WorkManager` for reliable data upload when connectivity returns.
- **Conflict Resolution:** Simple timestamp-based resolution for location data.
- **Batched Uploads:** Strategies for sending multiple records in a single HTTP request to Supabase to save battery.

### 3. Connection Monitoring
- **Network State:** Reacting to connectivity changes on both the Web (React) and Native (Java) sides.
- **Failover Logic:** Gracefully switching between direct-to-Supabase and local-first modes.

### 4. Data Integrity
- **De-duplication:** Ensuring the same location point isn't sent twice.
- **Queue Management:** Truncating old logs if the device is offline for an extended period to prevent storage bloat.

## Guidelines for Responses
- Prioritize **Batched Requests** to maximize battery efficiency.
- Always include **Error Handling** for network failures in sync logic.
- Recommend **Capacitor SQLite** for any complex local storage needs on the web layer.
- Ensure **Data Retention** is respected (deleting synced records).
