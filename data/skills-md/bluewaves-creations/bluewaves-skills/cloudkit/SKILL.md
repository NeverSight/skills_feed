---
name: cloudkit
description: CloudKit framework for iCloud data storage, sync, and sharing. Covers CKContainer, CKDatabase, CKRecord, CKQuery, subscriptions, CKShare, and UICloudSharingController. Use when user asks about CloudKit, CKRecord, CKDatabase, iCloud public database, CloudKit subscriptions, CKShare, sharing records, or UICloudSharingController.
allowed-tools: Bash, Read, Write, Edit
---

# CloudKit Framework

Comprehensive guide to CloudKit for direct iCloud data storage, synchronization, subscriptions, and multi-user sharing.

## Prerequisites

- iOS 10+ (iOS 26 recommended)
- Xcode 26+
- iCloud capability with CloudKit enabled
- Active Apple Developer account with admin permissions

---

## CloudKit Architecture

### CKContainer

The container is the top-level encapsulation of your app's CloudKit data:

```swift
import CloudKit

// Default container (from entitlements)
let container = CKContainer.default()

// Custom container identifier
let customContainer = CKContainer(identifier: "iCloud.com.yourcompany.yourapp")

// Access container properties
let containerID = container.containerIdentifier
```

### CKDatabase Types

Each container has three databases with different visibility:

```swift
// Private database - user's own data (requires sign-in)
let privateDB = container.privateCloudDatabase

// Public database - visible to all users (read without sign-in)
let publicDB = container.publicCloudDatabase

// Shared database - data shared with this user by others
let sharedDB = container.sharedCloudDatabase
```

**Database Scope Summary:**

| Database | Read | Write | Sign-in Required |
|----------|------|-------|------------------|
| Private | Owner only | Owner only | Yes |
| Public | Everyone | Signed-in users | Read: No, Write: Yes |
| Shared | Participants | Participants with permission | Yes |

### CKRecordZone

Zones partition records within a database:

```swift
// Default zone (always exists)
let defaultZone = CKRecordZone.default()

// Custom zone for advanced sync features
let customZone = CKRecordZone(zoneName: "MyCustomZone")

// Create custom zone
privateDB.save(customZone) { zone, error in
    if let error = error {
        print("Zone creation failed: \(error)")
        return
    }
    print("Zone created: \(zone?.zoneID.zoneName ?? "")")
}
```

**When to use custom zones:**
- Enable atomic commits across multiple records
- Track changes with change tokens for efficient sync
- Share entire zones with other users
- Support custom zone subscriptions

---

## CKRecord Basics

### Creating Records

```swift
// Create a record with a type name
let noteRecord = CKRecord(recordType: "Note")
noteRecord["title"] = "Meeting Notes"
noteRecord["content"] = "Discuss Q4 goals"
noteRecord["createdAt"] = Date()
noteRecord["isPinned"] = false

// Create with explicit ID
let recordID = CKRecord.ID(recordName: "unique-note-123")
let noteWithID = CKRecord(recordType: "Note", recordID: recordID)

// Create in custom zone
let zoneID = CKRecordZone.ID(zoneName: "NotesZone", ownerName: CKCurrentUserDefaultName)
let zonedRecordID = CKRecord.ID(recordName: "note-456", zoneID: zoneID)
let zonedNote = CKRecord(recordType: "Note", recordID: zonedRecordID)
```

### Supported Field Types

```swift
let record = CKRecord(recordType: "MediaItem")

// Basic types
record["title"] = "Sunset Photo" as String
record["viewCount"] = 42 as Int
record["rating"] = 4.5 as Double
record["isPublished"] = true as Bool

// Date
record["createdAt"] = Date()

// Data (up to 1MB inline, use CKAsset for larger)
record["thumbnail"] = Data()

// Location
record["location"] = CLLocation(latitude: 37.7749, longitude: -122.4194)

// Asset (for large files)
let fileURL = URL(fileURLWithPath: "/path/to/image.jpg")
record["photo"] = CKAsset(fileURL: fileURL)

// Reference to another record
let albumID = CKRecord.ID(recordName: "album-123")
record["album"] = CKRecord.Reference(recordID: albumID, action: .deleteSelf)

// Arrays
record["tags"] = ["nature", "sunset", "photography"] as [String]
```

### Reference Actions

```swift
// Delete this record if parent is deleted
CKRecord.Reference(recordID: parentID, action: .deleteSelf)

// No automatic action
CKRecord.Reference(recordID: parentID, action: .none)
```

### Saving Records

```swift
// Simple save
privateDB.save(noteRecord) { savedRecord, error in
    if let error = error {
        print("Save failed: \(error)")
        return
    }
    print("Saved record: \(savedRecord?.recordID.recordName ?? "")")
}

// Async/await (iOS 15+)
func saveNote(_ record: CKRecord) async throws -> CKRecord {
    return try await privateDB.save(record)
}
```

### Fetching by ID

```swift
let recordID = CKRecord.ID(recordName: "note-123")

// Callback-based
privateDB.fetch(withRecordID: recordID) { record, error in
    if let error = error {
        print("Fetch failed: \(error)")
        return
    }
    if let note = record {
        print("Title: \(note["title"] ?? "")")
    }
}

// Async/await
func fetchNote(id: String) async throws -> CKRecord {
    let recordID = CKRecord.ID(recordName: id)
    return try await privateDB.record(for: recordID)
}
```

### Deleting Records

```swift
privateDB.delete(withRecordID: recordID) { deletedID, error in
    if let error = error {
        print("Delete failed: \(error)")
        return
    }
    print("Deleted: \(deletedID?.recordName ?? "")")
}
```

---

## CKQuery and Fetching

### Basic Query with Predicate

```swift
// Fetch all notes
let allNotesPredicate = NSPredicate(value: true)
let allNotesQuery = CKQuery(recordType: "Note", predicate: allNotesPredicate)

// Fetch pinned notes
let pinnedPredicate = NSPredicate(format: "isPinned == %@", NSNumber(value: true))
let pinnedQuery = CKQuery(recordType: "Note", predicate: pinnedPredicate)

// String contains (case-insensitive)
let searchPredicate = NSPredicate(format: "title CONTAINS[cd] %@", "meeting")
let searchQuery = CKQuery(recordType: "Note", predicate: searchPredicate)

// Date comparison
let recentPredicate = NSPredicate(format: "createdAt > %@", Date().addingTimeInterval(-86400) as NSDate)
let recentQuery = CKQuery(recordType: "Note", predicate: recentPredicate)

// Reference match
let albumRef = CKRecord.Reference(recordID: albumID, action: .none)
let albumPredicate = NSPredicate(format: "album == %@", albumRef)
```

### Sorting Results

```swift
let query = CKQuery(recordType: "Note", predicate: NSPredicate(value: true))

// Single sort
query.sortDescriptors = [NSSortDescriptor(key: "createdAt", ascending: false)]

// Multiple sorts
query.sortDescriptors = [
    NSSortDescriptor(key: "isPinned", ascending: false),
    NSSortDescriptor(key: "createdAt", ascending: false)
]
```

### CKQueryOperation for Pagination

```swift
func fetchNotes(cursor: CKQueryOperation.Cursor? = nil) {
    let operation: CKQueryOperation

    if let cursor = cursor {
        operation = CKQueryOperation(cursor: cursor)
    } else {
        let query = CKQuery(recordType: "Note", predicate: NSPredicate(value: true))
        query.sortDescriptors = [NSSortDescriptor(key: "createdAt", ascending: false)]
        operation = CKQueryOperation(query: query)
    }

    operation.resultsLimit = 50

    var fetchedRecords: [CKRecord] = []

    operation.recordMatchedBlock = { recordID, result in
        switch result {
        case .success(let record):
            fetchedRecords.append(record)
        case .failure(let error):
            print("Record fetch error: \(error)")
        }
    }

    operation.queryResultBlock = { result in
        switch result {
        case .success(let cursor):
            print("Fetched \(fetchedRecords.count) records")
            if let cursor = cursor {
                // More results available - fetch next page
                self.fetchNotes(cursor: cursor)
            }
        case .failure(let error):
            print("Query failed: \(error)")
        }
    }

    privateDB.add(operation)
}
```

### Fetching Specific Fields Only

```swift
let operation = CKQueryOperation(query: query)
operation.desiredKeys = ["title", "createdAt"]  // Only fetch these fields
```

---

## Batch Operations

### CKModifyRecordsOperation

```swift
func saveMultipleRecords(_ records: [CKRecord]) {
    let operation = CKModifyRecordsOperation(
        recordsToSave: records,
        recordIDsToDelete: nil
    )

    // Per-record progress
    operation.perRecordProgressBlock = { record, progress in
        print("Upload progress for \(record.recordID.recordName): \(progress)")
    }

    // Per-record result
    operation.perRecordSaveBlock = { recordID, result in
        switch result {
        case .success(let record):
            print("Saved: \(record.recordID.recordName)")
        case .failure(let error):
            print("Failed to save \(recordID.recordName): \(error)")
        }
    }

    // Overall completion
    operation.modifyRecordsResultBlock = { result in
        switch result {
        case .success:
            print("Batch save completed")
        case .failure(let error):
            print("Batch operation failed: \(error)")
        }
    }

    // Save policy
    operation.savePolicy = .changedKeys  // Only upload changed fields

    // Atomic commit (requires custom zone)
    operation.isAtomic = true

    privateDB.add(operation)
}
```

### Save Policies

```swift
// Only save fields that changed since last fetch
operation.savePolicy = .changedKeys

// Save all fields (overwrites server values)
operation.savePolicy = .allKeys

// Fail if record has changed on server
operation.savePolicy = .ifServerRecordUnchanged
```

### Batch Delete

```swift
func deleteRecords(_ recordIDs: [CKRecord.ID]) {
    let operation = CKModifyRecordsOperation(
        recordsToSave: nil,
        recordIDsToDelete: recordIDs
    )

    operation.perRecordDeleteBlock = { recordID, result in
        switch result {
        case .success:
            print("Deleted: \(recordID.recordName)")
        case .failure(let error):
            print("Delete failed: \(error)")
        }
    }

    privateDB.add(operation)
}
```

---

## Subscriptions and Notifications

### Query Subscription

Subscribe to changes matching a predicate:

```swift
func subscribeToNewNotes() {
    let predicate = NSPredicate(format: "isPinned == %@", NSNumber(value: true))

    let subscription = CKQuerySubscription(
        recordType: "Note",
        predicate: predicate,
        subscriptionID: "pinned-notes-subscription",
        options: [.firesOnRecordCreation, .firesOnRecordUpdate, .firesOnRecordDeletion]
    )

    let notification = CKSubscription.NotificationInfo()
    notification.shouldSendContentAvailable = true  // Silent push
    notification.alertBody = "A pinned note was updated"
    notification.soundName = "default"

    subscription.notificationInfo = notification

    privateDB.save(subscription) { subscription, error in
        if let error = error {
            print("Subscription failed: \(error)")
            return
        }
        print("Subscribed to pinned notes")
    }
}
```

### Database Subscription

Subscribe to all changes in a database:

```swift
func subscribeToDatabaseChanges() {
    let subscription = CKDatabaseSubscription(subscriptionID: "private-db-changes")

    let notification = CKSubscription.NotificationInfo()
    notification.shouldSendContentAvailable = true

    subscription.notificationInfo = notification

    privateDB.save(subscription) { subscription, error in
        if let error = error {
            print("Database subscription failed: \(error)")
            return
        }
        print("Subscribed to all private database changes")
    }
}
```

### Record Zone Subscription

Subscribe to changes in a specific zone:

```swift
func subscribeToZoneChanges(zoneID: CKRecordZone.ID) {
    let subscription = CKRecordZoneSubscription(
        zoneID: zoneID,
        subscriptionID: "zone-\(zoneID.zoneName)-changes"
    )

    let notification = CKSubscription.NotificationInfo()
    notification.shouldSendContentAvailable = true

    subscription.notificationInfo = notification

    privateDB.save(subscription) { subscription, error in
        if let error = error {
            print("Zone subscription failed: \(error)")
            return
        }
        print("Subscribed to zone: \(zoneID.zoneName)")
    }
}
```

### Processing Push Notifications

In your App Delegate:

```swift
func application(_ application: UIApplication,
                 didReceiveRemoteNotification userInfo: [AnyHashable: Any],
                 fetchCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void) {

    let notification = CKNotification(fromRemoteNotificationDictionary: userInfo)

    switch notification?.notificationType {
    case .query:
        if let queryNotification = notification as? CKQueryNotification {
            let recordID = queryNotification.recordID
            print("Record changed: \(recordID?.recordName ?? "")")
        }
    case .database:
        print("Database changed - fetch changes")
        fetchDatabaseChanges()
    case .recordZone:
        if let zoneNotification = notification as? CKRecordZoneNotification {
            print("Zone changed: \(zoneNotification.recordZoneID?.zoneName ?? "")")
        }
    default:
        break
    }

    completionHandler(.newData)
}
```

---

## Record Zones and Change Tokens

### Creating a Custom Zone

```swift
func createNotesZone() async throws {
    let zoneID = CKRecordZone.ID(zoneName: "NotesZone", ownerName: CKCurrentUserDefaultName)
    let zone = CKRecordZone(zoneID: zoneID)

    _ = try await privateDB.save(zone)
    print("Notes zone created")
}
```

### Fetching Zone Changes with Tokens

```swift
class CloudKitSync {
    var zoneChangeToken: CKServerChangeToken?

    func fetchZoneChanges(zoneID: CKRecordZone.ID) {
        let configuration = CKFetchRecordZoneChangesOperation.ZoneConfiguration()
        configuration.previousServerChangeToken = zoneChangeToken

        let operation = CKFetchRecordZoneChangesOperation(
            recordZoneIDs: [zoneID],
            configurationsByRecordZoneID: [zoneID: configuration]
        )

        operation.recordWasChangedBlock = { recordID, result in
            switch result {
            case .success(let record):
                print("Changed: \(record.recordType) - \(recordID.recordName)")
                // Update local cache
            case .failure(let error):
                print("Record change error: \(error)")
            }
        }

        operation.recordWithIDWasDeletedBlock = { recordID, recordType in
            print("Deleted: \(recordType) - \(recordID.recordName)")
            // Remove from local cache
        }

        operation.recordZoneChangeTokensUpdatedBlock = { zoneID, token, _ in
            // Save token for next fetch
            self.zoneChangeToken = token
        }

        operation.recordZoneFetchResultBlock = { zoneID, result in
            switch result {
            case .success((let token, _)):
                self.zoneChangeToken = token
                print("Zone sync complete")
            case .failure(let error):
                print("Zone fetch failed: \(error)")
            }
        }

        privateDB.add(operation)
    }
}
```

---

## Sharing with CKShare

### Record Hierarchy Sharing

Share a specific record and its children:

```swift
func shareAlbum(_ album: CKRecord) async throws -> CKShare {
    // Create share for the root record
    let share = CKShare(rootRecord: album)

    // Configure share metadata
    share[CKShare.SystemFieldKey.title] = album["name"]
    if let coverData = album["coverImage"] as? Data {
        share[CKShare.SystemFieldKey.thumbnailImageData] = coverData
    }
    share[CKShare.SystemFieldKey.shareType] = "com.yourapp.album"

    // Set permissions
    share.publicPermission = .none  // Private share (invite only)

    // Save share and root record together
    let operation = CKModifyRecordsOperation(
        recordsToSave: [album, share],
        recordIDsToDelete: nil
    )

    return try await withCheckedThrowingContinuation { continuation in
        operation.modifyRecordsResultBlock = { result in
            switch result {
            case .success:
                continuation.resume(returning: share)
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }
        privateDB.add(operation)
    }
}
```

### Record Zone Sharing

Share an entire zone:

```swift
func shareZone(_ zoneID: CKRecordZone.ID) async throws -> CKShare {
    let share = CKShare(recordZoneID: zoneID)

    share[CKShare.SystemFieldKey.title] = "Shared Notes"
    share.publicPermission = .none

    let operation = CKModifyRecordsOperation(
        recordsToSave: [share],
        recordIDsToDelete: nil
    )

    return try await withCheckedThrowingContinuation { continuation in
        operation.modifyRecordsResultBlock = { result in
            switch result {
            case .success:
                continuation.resume(returning: share)
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }
        privateDB.add(operation)
    }
}
```

### Detecting Zone-Wide Share

```swift
func isZoneWideShare(_ metadata: CKShare.Metadata) -> Bool {
    return metadata.share.recordID.recordName == CKRecordNameZoneWideShare
}
```

### Share Permissions

```swift
// Public permission (anyone with link)
share.publicPermission = .none           // Invite only
share.publicPermission = .readOnly       // Anyone can read
share.publicPermission = .readWrite      // Anyone can read/write

// Participant permissions
let participant = share.participants.first
participant?.permission = .readOnly
participant?.permission = .readWrite
```

### Adding Participants Programmatically

```swift
func addParticipant(email: String, to share: CKShare) async throws {
    let lookupInfo = CKUserIdentity.LookupInfo(emailAddress: email)

    let fetchOp = CKFetchShareParticipantsOperation(userIdentityLookupInfos: [lookupInfo])

    var participant: CKShare.Participant?

    fetchOp.perShareParticipantResultBlock = { lookupInfo, result in
        switch result {
        case .success(let p):
            participant = p
            participant?.permission = .readWrite
        case .failure(let error):
            print("Failed to fetch participant: \(error)")
        }
    }

    try await withCheckedThrowingContinuation { (continuation: CheckedContinuation<Void, Error>) in
        fetchOp.fetchShareParticipantsResultBlock = { result in
            switch result {
            case .success:
                if let participant = participant {
                    share.addParticipant(participant)
                }
                continuation.resume()
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }
        CKContainer.default().add(fetchOp)
    }
}
```

---

## UICloudSharingController

### Info.plist Requirement

Add to your Info.plist:

```xml
<key>CKSharingSupported</key>
<true/>
```

### Presenting for New Share

```swift
class SharingViewController: UIViewController, UICloudSharingControllerDelegate {
    var recordToShare: CKRecord?

    @IBAction func shareButtonTapped(_ sender: UIBarButtonItem) {
        guard let record = recordToShare else { return }

        let sharingController = UICloudSharingController { controller, completion in
            self.createShare(for: record, completion: completion)
        }

        sharingController.delegate = self

        // REQUIRED for iPad - set popover source
        if let popover = sharingController.popoverPresentationController {
            popover.barButtonItem = sender
        }

        present(sharingController, animated: true)
    }

    private func createShare(for record: CKRecord,
                            completion: @escaping (CKShare?, CKContainer?, Error?) -> Void) {
        let share = CKShare(rootRecord: record)
        share[CKShare.SystemFieldKey.title] = record["title"]

        let operation = CKModifyRecordsOperation(
            recordsToSave: [record, share],
            recordIDsToDelete: nil
        )

        operation.modifyRecordsResultBlock = { result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    completion(share, CKContainer.default(), nil)
                case .failure(let error):
                    completion(nil, nil, error)
                }
            }
        }

        CKContainer.default().privateCloudDatabase.add(operation)
    }

    // MARK: - UICloudSharingControllerDelegate

    func cloudSharingController(_ csc: UICloudSharingController,
                               failedToSaveShareWithError error: Error) {
        print("Failed to save share: \(error)")
    }

    func itemTitle(for csc: UICloudSharingController) -> String? {
        return recordToShare?["title"] as? String
    }

    func itemThumbnailData(for csc: UICloudSharingController) -> Data? {
        return recordToShare?["thumbnailData"] as? Data
    }
}
```

### Managing Existing Share

```swift
func manageShare(_ share: CKShare) {
    let sharingController = UICloudSharingController(
        share: share,
        container: CKContainer.default()
    )

    sharingController.delegate = self

    // Always set popover source for iPad
    if let popover = sharingController.popoverPresentationController {
        popover.sourceView = view
        popover.sourceRect = CGRect(x: view.bounds.midX, y: view.bounds.midY, width: 0, height: 0)
    }

    present(sharingController, animated: true)
}
```

### Configuring Available Permissions

```swift
let sharingController = UICloudSharingController(share: share, container: container)

// Allow only specific options
sharingController.availablePermissions = [
    .allowPublic,      // Allow "Anyone with link" option
    .allowPrivate,     // Allow "Only invited people" option
    .allowReadOnly,    // Allow read-only permission
    .allowReadWrite    // Allow read/write permission
]
```

---

## Share Operations

### Fetching Share Metadata

```swift
func fetchShareMetadata(from url: URL) async throws -> CKShare.Metadata {
    let operation = CKFetchShareMetadataOperation(shareURLs: [url])

    return try await withCheckedThrowingContinuation { continuation in
        var fetchedMetadata: CKShare.Metadata?

        operation.perShareMetadataResultBlock = { url, result in
            switch result {
            case .success(let metadata):
                fetchedMetadata = metadata
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }

        operation.fetchShareMetadataResultBlock = { result in
            switch result {
            case .success:
                if let metadata = fetchedMetadata {
                    continuation.resume(returning: metadata)
                }
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }

        CKContainer.default().add(operation)
    }
}
```

### Accepting a Share

```swift
func acceptShare(_ metadata: CKShare.Metadata) async throws {
    let operation = CKAcceptSharesOperation(shareMetadatas: [metadata])

    try await withCheckedThrowingContinuation { (continuation: CheckedContinuation<Void, Error>) in
        operation.perShareResultBlock = { metadata, result in
            switch result {
            case .success(let share):
                print("Accepted share: \(share.recordID.recordName)")
            case .failure(let error):
                print("Failed to accept: \(error)")
            }
        }

        operation.acceptSharesResultBlock = { result in
            switch result {
            case .success:
                continuation.resume()
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }

        CKContainer.default().add(operation)
    }
}
```

### Processing Share in App Delegate

```swift
// Scene-based apps (iOS 13+)
class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    func windowScene(_ windowScene: UIWindowScene,
                    userDidAcceptCloudKitShareWith cloudKitShareMetadata: CKShare.Metadata) {
        Task {
            do {
                try await acceptShare(cloudKitShareMetadata)
                // Navigate to shared content
            } catch {
                print("Failed to accept share: \(error)")
            }
        }
    }
}

// Non-scene apps
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(_ application: UIApplication,
                    userDidAcceptCloudKitShareWith cloudKitShareMetadata: CKShare.Metadata) {
        Task {
            try? await acceptShare(cloudKitShareMetadata)
        }
    }
}
```

---

## SwiftData + CloudKit Integration

### Basic SwiftData with CloudKit

SwiftData can use CloudKit automatically:

```swift
let config = ModelConfiguration(cloudKitDatabase: .automatic)
let container = try ModelContainer(for: Note.self, configurations: config)
```

### Initializing CloudKit Schema for SwiftData

Before releasing to production, initialize the CloudKit schema:

```swift
@main
struct MyApp: App {
    let container: ModelContainer

    init() {
        let config = ModelConfiguration()

        do {
            #if DEBUG
            try autoreleasepool {
                let desc = NSPersistentStoreDescription(url: config.url)
                let opts = NSPersistentCloudKitContainerOptions(
                    containerIdentifier: "iCloud.com.yourcompany.yourapp"
                )
                desc.cloudKitContainerOptions = opts
                desc.shouldAddStoreAsynchronously = false

                if let mom = NSManagedObjectModel.makeManagedObjectModel(
                    for: [Note.self, Tag.self]
                ) {
                    let container = NSPersistentCloudKitContainer(
                        name: "MyApp",
                        managedObjectModel: mom
                    )
                    container.persistentStoreDescriptions = [desc]
                    container.loadPersistentStores { _, error in
                        if let error = error {
                            fatalError(error.localizedDescription)
                        }
                    }
                    try container.initializeCloudKitSchema()
                    if let store = container.persistentStoreCoordinator.persistentStores.first {
                        try container.persistentStoreCoordinator.remove(store)
                    }
                }
            }
            #endif

            container = try ModelContainer(for: Note.self, Tag.self, configurations: config)
        } catch {
            fatalError("Failed to configure SwiftData: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}
```

### Specifying CloudKit Container

```swift
// Use specific CloudKit container
let config = ModelConfiguration(
    cloudKitDatabase: .private("iCloud.com.yourcompany.yourapp")
)

// Disable CloudKit sync entirely
let localConfig = ModelConfiguration(cloudKitDatabase: .none)
```

### Schema Compatibility Requirements

For SwiftData models to sync via CloudKit:

```swift
@Model
class Note {
    // All relationships must be optional
    var folder: Folder?
    var tags: [Tag]?

    // No unique constraints
    // @Attribute(.unique) var id: String  // NOT SUPPORTED

    // No deny delete rules
    // @Relationship(deleteRule: .deny)    // NOT SUPPORTED

    var title: String = ""
    var content: String = ""

    init(title: String = "") {
        self.title = title
    }
}
```

---

## Error Handling

### Common CloudKit Errors

```swift
func handleCloudKitError(_ error: Error) {
    guard let ckError = error as? CKError else {
        print("Unknown error: \(error)")
        return
    }

    switch ckError.code {
    case .networkFailure, .networkUnavailable:
        print("Network issue - retry later")

    case .notAuthenticated:
        print("User not signed into iCloud")

    case .quotaExceeded:
        print("iCloud storage full")

    case .serverRecordChanged:
        // Handle conflict
        if let serverRecord = ckError.userInfo[CKRecordChangedErrorServerRecordKey] as? CKRecord {
            print("Server has newer version")
            // Merge or overwrite
        }

    case .zoneNotFound:
        print("Zone doesn't exist - create it")

    case .userDeletedZone:
        print("User deleted the zone - recreate")

    case .participantMayNeedVerification:
        print("Participant needs to verify their account")

    case .alreadyShared:
        print("Record is already part of another share")

    case .partialFailure:
        // Check individual record errors
        if let partialErrors = ckError.userInfo[CKPartialErrorsByItemIDKey] as? [CKRecord.ID: Error] {
            for (recordID, recordError) in partialErrors {
                print("Error for \(recordID.recordName): \(recordError)")
            }
        }

    default:
        print("CloudKit error: \(ckError.localizedDescription)")
    }
}
```

### Retry Logic

```swift
func retryableOperation<T>(maxRetries: Int = 3,
                           operation: @escaping () async throws -> T) async throws -> T {
    var lastError: Error?

    for attempt in 1...maxRetries {
        do {
            return try await operation()
        } catch let error as CKError {
            lastError = error

            if let retryAfter = error.retryAfterSeconds {
                try await Task.sleep(nanoseconds: UInt64(retryAfter * 1_000_000_000))
            } else if error.code == .networkFailure || error.code == .serviceUnavailable {
                try await Task.sleep(nanoseconds: UInt64(pow(2.0, Double(attempt)) * 1_000_000_000))
            } else {
                throw error  // Non-retryable error
            }
        }
    }

    throw lastError ?? CKError(.internalError)
}
```

---

## Best Practices

### 1. Use Custom Zones for Private Data

```swift
// Custom zones enable:
// - Change tracking with tokens
// - Atomic transactions
// - Zone-based sharing
let zoneID = CKRecordZone.ID(zoneName: "UserData", ownerName: CKCurrentUserDefaultName)
```

### 2. Handle Errors Per-Record in Batch Operations

```swift
operation.perRecordSaveBlock = { recordID, result in
    switch result {
    case .success(let record):
        // Update local cache
    case .failure(let error):
        // Handle individual failure
    }
}
```

### 3. Use Change Tokens for Efficient Sync

```swift
// Store tokens persistently
UserDefaults.standard.set(tokenData, forKey: "zoneChangeToken")

// Use tokens to fetch only changes since last sync
configuration.previousServerChangeToken = storedToken
```

### 4. Always Set Popover Source on iPad

```swift
// REQUIRED - crashes on iPad without this
if let popover = sharingController.popoverPresentationController {
    popover.barButtonItem = sender
    // OR
    popover.sourceView = view
    popover.sourceRect = rect
}
```

### 5. Test with Multiple iCloud Accounts

- Test sharing between different accounts
- Test on devices signed out of iCloud
- Test with network disabled
- Test quota exceeded scenarios

### 6. Design for Eventual Consistency

```swift
// CloudKit syncs asynchronously - don't assume immediate consistency
// Use subscriptions for real-time updates
// Display sync status to users
```

---

## Official Resources

- [CloudKit Documentation](https://developer.apple.com/documentation/cloudkit)
- [CKShare Documentation](https://developer.apple.com/documentation/cloudkit/ckshare)
- [UICloudSharingController](https://developer.apple.com/documentation/uikit/uicloudsharingcontroller)
- [Sharing CloudKit Data with Other iCloud Users](https://developer.apple.com/documentation/cloudkit/sharing_cloudkit_data_with_other_icloud_users)
- [WWDC21: What's new in CloudKit](https://developer.apple.com/videos/play/wwdc2021/10086/)
- [WWDC22: Optimize your use of CloudKit](https://developer.apple.com/videos/play/wwdc2022/10119/)
- [WWDC23: Meet SwiftData](https://developer.apple.com/videos/play/wwdc2023/10187/)
