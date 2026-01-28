---
name: swift-core-data
description: Persist data with Core Data - models, contexts, fetch requests, migrations, SwiftData
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 04-swift-data
bond_type: PRIMARY_BOND
---

# Swift Core Data Skill

Data persistence framework knowledge for Core Data and SwiftData in Apple platforms.

## Prerequisites

- Xcode 15+ installed
- Understanding of object graphs
- Basic SQL concepts helpful

## Parameters

```yaml
parameters:
  framework:
    type: string
    enum: [core_data, swift_data]
    default: swift_data
    description: Persistence framework
  cloudkit_sync:
    type: boolean
    default: false
  lightweight_migration:
    type: boolean
    default: true
  store_type:
    type: string
    enum: [sqlite, in_memory, binary]
    default: sqlite
```

## Topics Covered

### Core Data vs SwiftData
| Feature | Core Data | SwiftData |
|---------|-----------|-----------|
| Min iOS | 3.0+ | 17.0+ |
| Definition | .xcdatamodeld | @Model macro |
| Threading | Manual (contexts) | Actor-based |
| Fetch | NSFetchRequest | #Predicate |
| Learning Curve | Steep | Gentle |

### Core Data Stack
| Component | Purpose |
|-----------|---------|
| NSPersistentContainer | Encapsulates stack |
| NSManagedObjectContext | Working area for objects |
| NSManagedObjectModel | Schema definition |
| NSPersistentStoreCoordinator | Store management |

### SwiftData Components
| Component | Purpose |
|-----------|---------|
| ModelContainer | Schema + store |
| ModelContext | Working area |
| @Model | Entity macro |
| @Query | Fetch in SwiftUI |

## Code Examples

### SwiftData (iOS 17+)
```swift
import SwiftData

// MARK: - Model Definition

@Model
final class Task {
    var title: String
    var notes: String
    var dueDate: Date?
    var isCompleted: Bool
    var priority: Priority
    var createdAt: Date

    @Relationship(deleteRule: .cascade, inverse: \Subtask.parentTask)
    var subtasks: [Subtask] = []

    @Relationship(inverse: \Tag.tasks)
    var tags: [Tag] = []

    init(title: String, notes: String = "", dueDate: Date? = nil, priority: Priority = .medium) {
        self.title = title
        self.notes = notes
        self.dueDate = dueDate
        self.isCompleted = false
        self.priority = priority
        self.createdAt = Date()
    }
}

@Model
final class Subtask {
    var title: String
    var isCompleted: Bool
    var parentTask: Task?

    init(title: String, parentTask: Task? = nil) {
        self.title = title
        self.isCompleted = false
        self.parentTask = parentTask
    }
}

@Model
final class Tag {
    @Attribute(.unique) var name: String
    var color: String
    var tasks: [Task] = []

    init(name: String, color: String = "#007AFF") {
        self.name = name
        self.color = color
    }
}

enum Priority: String, Codable, CaseIterable {
    case low, medium, high, urgent
}

// MARK: - Container Setup

@main
struct TaskApp: App {
    let container: ModelContainer

    init() {
        let schema = Schema([Task.self, Subtask.self, Tag.self])
        let config = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false,
            cloudKitDatabase: .none
        )

        do {
            container = try ModelContainer(for: schema, configurations: config)
        } catch {
            fatalError("Failed to create ModelContainer: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}

// MARK: - SwiftUI Integration

struct TaskListView: View {
    @Environment(\.modelContext) private var context
    @Query(sort: \Task.dueDate) private var tasks: [Task]

    var body: some View {
        List {
            ForEach(tasks) { task in
                TaskRow(task: task)
            }
            .onDelete(perform: deleteTasks)
        }
    }

    private func deleteTasks(at offsets: IndexSet) {
        for index in offsets {
            context.delete(tasks[index])
        }
    }
}

// Query with predicate
struct IncompleteTasks: View {
    @Query(filter: #Predicate<Task> { !$0.isCompleted },
           sort: [SortDescriptor(\Task.priority, order: .reverse)])
    private var tasks: [Task]

    var body: some View {
        List(tasks) { task in
            Text(task.title)
        }
    }
}
```

### Core Data (Traditional)
```swift
import CoreData

// MARK: - Core Data Stack

final class CoreDataStack {
    static let shared = CoreDataStack()

    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "DataModel")

        container.loadPersistentStores { _, error in
            if let error = error as NSError? {
                fatalError("Core Data error: \(error), \(error.userInfo)")
            }
        }

        container.viewContext.automaticallyMergesChangesFromParent = true
        container.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        return container
    }()

    var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }

    func newBackgroundContext() -> NSManagedObjectContext {
        let context = persistentContainer.newBackgroundContext()
        context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        return context
    }

    func saveContext() {
        let context = viewContext
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                let nsError = error as NSError
                print("Core Data save error: \(nsError), \(nsError.userInfo)")
            }
        }
    }
}

// MARK: - Fetch Request Helpers

extension NSManagedObjectContext {
    func fetch<T: NSManagedObject>(_ type: T.Type, predicate: NSPredicate? = nil, sortDescriptors: [NSSortDescriptor]? = nil) throws -> [T] {
        let request = T.fetchRequest()
        request.predicate = predicate
        request.sortDescriptors = sortDescriptors
        return try fetch(request) as? [T] ?? []
    }
}

// MARK: - Background Operations

extension CoreDataStack {
    func performBackgroundTask<T>(_ block: @escaping (NSManagedObjectContext) throws -> T) async throws -> T {
        try await withCheckedThrowingContinuation { continuation in
            persistentContainer.performBackgroundTask { context in
                do {
                    let result = try block(context)
                    if context.hasChanges {
                        try context.save()
                    }
                    continuation.resume(returning: result)
                } catch {
                    continuation.resume(throwing: error)
                }
            }
        }
    }

    func batchInsert<T: Encodable>(entities: [T], entityName: String) async throws {
        let context = newBackgroundContext()

        try await context.perform {
            let insertRequest = NSBatchInsertRequest(entityName: entityName, objects: entities.map { entity -> [String: Any] in
                let data = try! JSONEncoder().encode(entity)
                return try! JSONSerialization.jsonObject(with: data) as! [String: Any]
            })
            insertRequest.resultType = .count

            let result = try context.execute(insertRequest) as! NSBatchInsertResult
            print("Inserted \(result.result ?? 0) records")

            // Merge changes to view context
            NSManagedObjectContext.mergeChanges(
                fromRemoteContextSave: [NSInsertedObjectsKey: []],
                into: [self.viewContext]
            )
        }
    }
}
```

### Migration Handling
```swift
// Lightweight Migration (automatic)
let container = NSPersistentContainer(name: "DataModel")
let description = container.persistentStoreDescriptions.first
description?.setOption(true as NSNumber, forKey: NSMigratePersistentStoresAutomaticallyOption)
description?.setOption(true as NSNumber, forKey: NSInferMappingModelAutomaticallyOption)

// Custom Migration Manager
final class MigrationManager {
    func requiresMigration(at storeURL: URL, for model: NSManagedObjectModel) -> Bool {
        guard let metadata = try? NSPersistentStoreCoordinator.metadataForPersistentStore(ofType: NSSQLiteStoreType, at: storeURL) else {
            return false
        }
        return !model.isConfiguration(withName: nil, compatibleWithStoreMetadata: metadata)
    }

    func migrateStore(at storeURL: URL, to destinationModel: NSManagedObjectModel) throws {
        // Implementation for custom migration
    }
}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "The model configuration is invalid" | Schema mismatch | Delete app, check @Model |
| Context save crash | Wrong thread | Use perform/performAndWait |
| Relationship fault | Object deleted | Check for nil before access |
| Slow fetch | Missing index | Add index to frequently queried attributes |
| Migration fails | Non-trivial change | Write custom mapping model |

### Debug Tips
```bash
# Enable Core Data debug logging
# Add to scheme arguments:
-com.apple.CoreData.SQLDebug 1
-com.apple.CoreData.Logging.stderr 1

# SwiftData logging
-com.apple.SwiftData.SQLDebug 1
```

```swift
// Print fetch request SQL
let request: NSFetchRequest<Task> = Task.fetchRequest()
print(request.description)

// Check context state
print("Inserted: \(context.insertedObjects.count)")
print("Updated: \(context.updatedObjects.count)")
print("Deleted: \(context.deletedObjects.count)")
```

## Validation Rules

```yaml
validation:
  - rule: background_for_heavy_operations
    severity: error
    check: Use background context for batch operations
  - rule: main_thread_for_ui
    severity: error
    check: Only access viewContext on main thread
  - rule: index_frequently_queried
    severity: warning
    check: Add indexes to attributes used in predicates
```

## Usage

```
Skill("swift-core-data")
```

## Related Skills

- `swift-networking` - Syncing remote data
- `swift-swiftui` - @Query integration
- `swift-testing` - In-memory stores for tests
