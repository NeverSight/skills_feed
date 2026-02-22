---
name: cloudkit
description: Apple CloudKit framework for iOS/macOS/watchOS/tvOS development. Use for iCloud data persistence, multi-device sync, CKSyncEngine implementation, CKContainer/CKDatabase/CKRecord operations, conflict resolution, error handling, subscriptions, and CloudKit best practices. Triggers on CloudKit questions, iCloud sync implementation, CKRecord CRUD, zone management, or cross-device data synchronization in Swift/SwiftUI apps.
---

# CloudKit Framework Skill

CloudKit is Apple's framework for iCloud data persistence with up to **1PB public storage** and automatic cross-device sync.

## Code Review Checklist

When reviewing CloudKit code, verify:

- [ ] Account status checked before private/shared database operations
- [ ] Custom zones used (not default zone) for production data
- [ ] All CloudKit errors handled with `retryAfterSeconds` respected
- [ ] `serverRecordChanged` conflicts handled with proper merge logic
- [ ] `CKErrorPartialFailure` parsed for individual record errors
- [ ] Batch operations used (`CKModifyRecordsOperation`) not individual saves
- [ ] Large binary data stored as `CKAsset` (records have 1MB limit)
- [ ] Record keys type-safe (enums) not string literals
- [ ] UI updates dispatched to main thread from callbacks
- [ ] `CKAccountChangedNotification` observed for account switches
- [ ] Subscriptions have unique IDs to prevent duplicates
- [ ] CKShare uses custom zone (sharing requires custom zones)
- [ ] CKSyncEngine state token cached on every `.stateUpdate` event
- [ ] Schema deployed to production before App Store release

### Review Output Format

Report issues as: `[FILE:LINE] ISSUE_TITLE`

Examples:
- `[SyncManager.swift:45] Missing CKSyncEngine state token persistence`
- `[DataStore.swift:89] Unhandled serverRecordChanged conflict`
- `[CloudKit.swift:156] Individual saves instead of batch operation`

## Quick Start

```swift
import CloudKit

// Initialize container and database
let container = CKContainer.default()  // or CKContainer(identifier: "iCloud.your.bundle.id")
let privateDB = container.privateCloudDatabase
let publicDB = container.publicCloudDatabase
let sharedDB = container.sharedCloudDatabase
```

## Core Architecture

| Component | Purpose |
|-----------|---------|
| **CKContainer** | Top-level entry point (1 per app typically) |
| **CKDatabase** | Storage layer (private/public/shared) |
| **CKRecordZone** | Logical grouping of records in private DB |
| **CKRecord** | Single data item (like a dictionary) |
| **CKRecord.ID** | Unique identifier (recordName + zoneID) |
| **CKAsset** | Binary data (images, files) |
| **CKReference** | Relationships between records |
| **CKSubscription** | Push notification triggers |

## CKSyncEngine (iOS 17+) — Recommended Approach

CKSyncEngine dramatically simplifies sync. See [references/cksyncengine.md](references/cksyncengine.md) for complete implementation guide.

### Minimal Setup

```swift
import CloudKit

class SyncManager: CKSyncEngineDelegate {
    private var engine: CKSyncEngine!
    private let container = CKContainer(identifier: "iCloud.your.bundle.id")
    
    init() {
        let config = CKSyncEngine.Configuration(
            database: container.privateCloudDatabase,
            stateSerialization: loadCachedState(),  // nil if first launch
            delegate: self
        )
        engine = CKSyncEngine(config)
    }
    
    // MARK: - Delegate Methods
    
    func handleEvent(_ event: CKSyncEngine.Event, syncEngine: CKSyncEngine) async {
        switch event {
        case .stateUpdate(let update):
            // CRITICAL: Always cache the state token
            saveCachedState(update.stateSerialization)
            
        case .accountChange(let change):
            handleAccountChange(change)
            
        case .fetchedRecordZoneChanges(let changes):
            // Server → Local: Process incoming data
            for modification in changes.modifications {
                saveLocally(modification.record)
            }
            for deletion in changes.deletions {
                deleteLocally(deletion.recordID)
            }
            
        case .sentRecordZoneChanges(let sent):
            // Confirm successful uploads, handle failures
            for failure in sent.failedRecordSaves {
                handleSaveFailure(failure)
            }
            
        default: break
        }
    }
    
    func nextRecordZoneChangeBatch(_ context: CKSyncEngine.SendChangesContext, 
                                    syncEngine: CKSyncEngine) async -> CKSyncEngine.RecordZoneChangeBatch? {
        // Local → Server: Provide records to upload
        let pending = syncEngine.state.pendingRecordZoneChanges.filter { 
            context.options.scope.contains($0) 
        }
        return await CKSyncEngine.RecordZoneChangeBatch(pendingChanges: pending) { recordID in
            return getLocalRecord(for: recordID)
        }
    }
    
    // MARK: - Queue Changes
    
    func queueSave(_ record: CKRecord) {
        engine.state.add(pendingRecordZoneChanges: [.saveRecord(record.recordID)])
    }
    
    func queueDelete(_ recordID: CKRecord.ID) {
        engine.state.add(pendingRecordZoneChanges: [.deleteRecord(recordID)])
    }
}
```

## CRUD Operations (Direct API)

For non-CKSyncEngine apps or public database. See [references/crud-operations.md](references/crud-operations.md).

```swift
// CREATE
let record = CKRecord(recordType: "Note")
record["title"] = "My Note"
record["content"] = "Hello CloudKit"
let saved = try await database.save(record)

// READ
let recordID = CKRecord.ID(recordName: "unique-id")
let fetched = try await database.record(for: recordID)

// UPDATE
fetched["content"] = "Updated content"
let updated = try await database.save(fetched)

// DELETE
try await database.deleteRecord(withID: recordID)

// QUERY
let predicate = NSPredicate(format: "title BEGINSWITH %@", "My")
let query = CKQuery(recordType: "Note", predicate: predicate)
let (results, _) = try await database.records(matching: query)
```

## Error Handling

See [references/error-handling.md](references/error-handling.md) for complete error codes.

```swift
do {
    try await database.save(record)
} catch let error as CKError {
    switch error.code {
    case .serverRecordChanged:
        // Conflict! Resolve using serverRecord
        let serverRecord = error.serverRecord
        resolveConflict(local: record, server: serverRecord)
        
    case .networkFailure, .networkUnavailable, .serviceUnavailable:
        // Transient - retry with backoff
        let retryAfter = error.retryAfterSeconds ?? 30
        scheduleRetry(after: retryAfter)
        
    case .quotaExceeded:
        // User out of iCloud storage
        notifyUserStorageFull()
        
    case .notAuthenticated:
        // User not signed into iCloud
        promptiCloudSignIn()
        
    case .limitExceeded:
        // Too many records - split into batches of 400
        splitAndRetry(records)
        
    default:
        log("CloudKit error: \(error.localizedDescription)")
    }
}
```

## Conflict Resolution

```swift
func resolveConflict(local: CKRecord, server: CKRecord?) -> CKRecord {
    guard let server = server else { return local }
    
    // Strategy 1: Server wins (safest)
    return server
    
    // Strategy 2: Last writer wins (by modificationDate)
    // return server.modificationDate! > local.modificationDate! ? server : local
    
    // Strategy 3: Field-level merge
    // let merged = CKRecord(recordType: local.recordType, recordID: local.recordID)
    // merged["title"] = local["title"]  // Keep local title
    // merged["content"] = server["content"]  // Keep server content
    // return merged
    
    // Strategy 4: Edit count (increment counter on each edit)
    // let localCount = local["editCount"] as? Int ?? 0
    // let serverCount = server["editCount"] as? Int ?? 0
    // return localCount > serverCount ? local : server
}
```

## Record Zones

Private database supports custom zones with change tracking:

```swift
let zoneID = CKRecordZone.ID(zoneName: "MyAppZone", ownerName: CKCurrentUserDefaultName)
let zone = CKRecordZone(zoneID: zoneID)

// Create zone
try await database.save(zone)

// Create record in zone
let recordID = CKRecord.ID(recordName: UUID().uuidString, zoneID: zoneID)
let record = CKRecord(recordType: "Note", recordID: recordID)

// Delete zone (deletes ALL records in it)
try await database.deleteRecordZone(withID: zoneID)
```

## Subscriptions & Push Notifications

```swift
// Subscribe to zone changes (private DB)
let subscription = CKRecordZoneSubscription(zoneID: zoneID)
let notificationInfo = CKSubscription.NotificationInfo()
notificationInfo.shouldSendContentAvailable = true  // Silent push
subscription.notificationInfo = notificationInfo
try await database.save(subscription)

// Subscribe to query (public DB)
let predicate = NSPredicate(format: "category == %@", "important")
let querySubscription = CKQuerySubscription(
    recordType: "Note",
    predicate: predicate,
    options: [.firesOnRecordCreation, .firesOnRecordUpdate]
)
```

## Assets (Binary Data)

```swift
// Save image
let imageURL = FileManager.default.temporaryDirectory.appendingPathComponent("photo.jpg")
imageData.write(to: imageURL)
let asset = CKAsset(fileURL: imageURL)
record["photo"] = asset
try await database.save(record)

// Load image
if let asset = record["photo"] as? CKAsset, let url = asset.fileURL {
    let data = try Data(contentsOf: url)
    let image = UIImage(data: data)
}
```

## Sharing (CloudKit Sharing)

```swift
// Create share
let share = CKShare(rootRecord: record)
share.publicPermission = .readOnly
share[CKShare.SystemFieldKey.title] = "Shared Document"

// Save both
let operation = CKModifyRecordsOperation(recordsToSave: [record, share])
try await database.add(operation)

// Present sharing UI
let sharingController = UICloudSharingController(share: share, container: container)
present(sharingController, animated: true)
```

## Project Setup Checklist

1. **Apple Developer Program** membership required
2. **Xcode Signing & Capabilities**:
   - Add iCloud capability
   - Check CloudKit
   - Create/select container (e.g., `iCloud.com.yourcompany.appname`)
   - Background Modes → Remote notifications
3. **Container cannot be deleted** — name carefully
4. **Info.plist** (for background fetch):
   ```xml
   <key>UIBackgroundModes</key>
   <array>
       <string>remote-notification</string>
   </array>
   ```

## CloudKit Dashboard

Access at: https://icloud.developer.apple.com

- View/edit records, zones, subscriptions
- Monitor usage and quotas
- Deploy schema to production
- **Development vs Production** environments are separate

## Best Practices

1. **Always cache CKSyncEngine state token** — or sync breaks
2. **Batch operations to 400 records max** — avoid `limitExceeded`
3. **Store CKRecord metadata locally** — for conflict resolution
4. **Use encrypted fields for sensitive data** — `record.encryptedValues["key"]`
5. **Handle all error cases** — especially transient errors with retry
6. **Test on physical devices** — simulator has limitations
7. **Don't use enums in synced data** — use strings instead (forward compatibility)
8. **Keep change tokens after fetches** — commit only after local save succeeds

## References

### Implementation Guides
- [CKSyncEngine Guide](references/cksyncengine.md) — Complete implementation walkthrough (iOS 17+)
- [CRUD Operations](references/crud-operations.md) — Direct database operations, queries, assets
- [Operations Reference](references/operations.md) — All CKOperation classes, batching, pagination
- [Subscriptions & Notifications](references/subscriptions-notifications.md) — Push notifications, real-time sync

### Features
- [Sharing](references/sharing.md) — CKShare, UICloudSharingController, zone sharing
- [User Discovery](references/user-discovery.md) — CKUserIdentity, finding users, discoverability
- [Privacy & Security](references/privacy-security.md) — Encryption, access controls, GDPR compliance

### Reference
- [API Reference](references/api-reference.md) — Complete class/method listing for all CloudKit APIs
- [Error Handling](references/error-handling.md) — All CKError codes and retry strategies
- [Schema Design](references/schema-design.md) — Versioning, references, encryption, migrations
- [Troubleshooting](references/troubleshooting.md) — Common issues, debugging, CloudKit Dashboard

## External Resources

- [Apple Sample: CKSyncEngine](https://github.com/apple/sample-cloudkit-sync-engine)
- [Apple Sample: Zone Sharing](https://github.com/apple/sample-cloudkit-zonesharing)
- [Apple CloudKit Documentation](https://developer.apple.com/documentation/cloudkit)
- [CloudKit Dashboard](https://icloud.developer.apple.com)
- [WWDC Videos](https://developer.apple.com/videos/frameworks/cloudkit)
