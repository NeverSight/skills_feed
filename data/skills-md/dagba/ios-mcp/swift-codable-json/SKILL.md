---
name: swift-codable-json
description: Use when implementing JSON encoding/decoding with Codable, handling API responses, encountering decoding errors, managing date formats, mapping snake_case to camelCase, or dealing with nested/inconsistent JSON structures
---

# Swift Codable for JSON Parsing

## Overview

**Codable provides type-safe JSON parsing but strict typing means any mismatch crashes decoding.** One date strategy per decoder, CodingKeys for every naming mismatch, custom decoders for nested structures.

**Core principle:** Design for API reality (not ideal JSON), fail gracefully with error handling, use optionals for unreliable data.

## Basic Patterns

### Pattern 1: Simple Mapping

```swift
// JSON: {"id": 123, "name": "Alice", "email": "alice@example.com"}

struct User: Codable {
    let id: Int
    let name: String
    let email: String
}

// Usage:
let data = jsonString.data(using: .utf8)!
let user = try JSONDecoder().decode(User.self, from: data)
```

**Auto-synthesis works when:**
- Property names match JSON keys exactly
- All types match (String → String, Int → Int)
- All required properties present in JSON

### Pattern 2: CodingKeys for Name Mapping

**Problem:** API uses snake_case, Swift uses camelCase.

```swift
// JSON: {"user_id": 123, "first_name": "Alice", "created_at": "2026-01-15"}

struct User: Codable {
    let userID: Int
    let firstName: String
    let createdAt: String

    enum CodingKeys: String, CodingKey {
        case userID = "user_id"
        case firstName = "first_name"
        case createdAt = "created_at"
    }
}
```

**Rule:** Every property must appear in CodingKeys, even if name matches.

```swift
// ❌ WRONG: Compiler error (missing properties in CodingKeys)
enum CodingKeys: String, CodingKey {
    case userID = "user_id"  // Missing firstName and createdAt
}

// ✅ CORRECT: All properties listed
enum CodingKeys: String, CodingKey {
    case userID = "user_id"
    case firstName = "first_name"
    case createdAt = "created_at"
}
```

## Date Handling

### Problem: Multiple Date Formats in Same Response

**CRITICAL:** JSONDecoder supports ONE date strategy at a time.

```swift
// JSON with mixed formats:
{
    "created": "2026-01-15T10:30:00Z",      // ISO8601
    "published": "15/01/2026",              // Custom format
    "timestamp": 1705316400                  // Unix timestamp
}

// ❌ WRONG: Can't set multiple strategies
let decoder = JSONDecoder()
decoder.dateDecodingStrategy = .iso8601  // Only applies to ONE field
```

### Solution 1: Custom Date Decoding

```swift
struct Article: Decodable {
    let created: Date
    let published: Date
    let timestamp: Date

    enum CodingKeys: String, CodingKey {
        case created, published, timestamp
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)

        // ISO8601 format
        let iso8601Formatter = ISO8601DateFormatter()
        let createdString = try container.decode(String.self, forKey: .created)
        guard let createdDate = iso8601Formatter.date(from: createdString) else {
            throw DecodingError.dataCorruptedError(forKey: .created, in: container, debugDescription: "Invalid ISO8601 date")
        }
        self.created = createdDate

        // Custom format
        let customFormatter = DateFormatter()
        customFormatter.dateFormat = "dd/MM/yyyy"
        let publishedString = try container.decode(String.self, forKey: .published)
        guard let publishedDate = customFormatter.date(from: publishedString) else {
            throw DecodingError.dataCorruptedError(forKey: .published, in: container, debugDescription: "Invalid date format")
        }
        self.published = publishedDate

        // Unix timestamp
        let timestampValue = try container.decode(TimeInterval.self, forKey: .timestamp)
        self.timestamp = Date(timeIntervalSince1970: timestampValue)
    }
}
```

### Solution 2: Dedicated Date Types

```swift
struct Article: Codable {
    let created: String  // Keep as String, parse when needed
    let published: String
    let timestamp: TimeInterval

    var createdDate: Date? {
        ISO8601DateFormatter().date(from: created)
    }

    var publishedDate: Date? {
        let formatter = DateFormatter()
        formatter.dateFormat = "dd/MM/yyyy"
        return formatter.date(from: published)
    }

    var timestampDate: Date {
        Date(timeIntervalSince1970: timestamp)
    }
}
```

**Trade-off:** Less type-safe at decode time, but more flexible.

## Nested JSON Flattening

### Problem: Nested JSON Structure, Flat Swift Model

```swift
// API response:
{
    "user": {
        "id": 123,
        "profile": {
            "name": "Alice",
            "avatar_url": "https://..."
        }
    },
    "settings": {
        "notifications": true
    }
}

// Want: Flat Swift model
struct User {
    let id: Int
    let name: String
    let avatarURL: String
    let notifications: Bool
}
```

### Solution: Nested CodingKeys

```swift
struct User: Decodable {
    let id: Int
    let name: String
    let avatarURL: String
    let notifications: Bool

    enum CodingKeys: String, CodingKey {
        case user, settings
    }

    enum UserKeys: String, CodingKey {
        case id, profile
    }

    enum ProfileKeys: String, CodingKey {
        case name
        case avatarURL = "avatar_url"
    }

    enum SettingsKeys: String, CodingKey {
        case notifications
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)

        // Navigate to user.id
        let userContainer = try container.nestedContainer(keyedBy: UserKeys.self, forKey: .user)
        id = try userContainer.decode(Int.self, forKey: .id)

        // Navigate to user.profile.name and user.profile.avatar_url
        let profileContainer = try userContainer.nestedContainer(keyedBy: ProfileKeys.self, forKey: .profile)
        name = try profileContainer.decode(String.self, forKey: .name)
        avatarURL = try profileContainer.decode(String.self, forKey: .avatarURL)

        // Navigate to settings.notifications
        let settingsContainer = try container.nestedContainer(keyedBy: SettingsKeys.self, forKey: .settings)
        notifications = try settingsContainer.decode(Bool.self, forKey: .notifications)
    }
}
```

## Optional vs Required Fields

### Pattern: Handle Unreliable Data

```swift
// API sometimes omits fields or sends null

// ❌ WRONG: Crashes when field missing
struct User: Codable {
    let id: Int
    let name: String
    let email: String  // Crashes if null or missing
}

// ✅ CORRECT: Optional for unreliable fields
struct User: Codable {
    let id: Int
    let name: String
    let email: String?  // nil if null or missing
}

// ✅ BETTER: Default values for missing fields
struct User: Codable {
    let id: Int
    let name: String
    let email: String?
    let isVerified: Bool

    enum CodingKeys: String, CodingKey {
        case id, name, email
        case isVerified = "is_verified"
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(Int.self, forKey: .id)
        name = try container.decode(String.self, forKey: .name)
        email = try container.decodeIfPresent(String.self, forKey: .email)
        isVerified = try container.decodeIfPresent(Bool.self, forKey: .isVerified) ?? false
    }
}
```

**Rule:** Use `decodeIfPresent()` for optional fields, provide defaults where appropriate.

## Error Handling

### Pattern: Graceful Failure with Diagnostics

```swift
// ❌ WRONG: Silent failure or crash
let user = try! JSONDecoder().decode(User.self, from: data)

// ✅ CORRECT: Informative error handling
do {
    let user = try JSONDecoder().decode(User.self, from: data)
    return user
} catch let DecodingError.keyNotFound(key, context) {
    print("Missing key: \(key.stringValue)")
    print("Context: \(context.debugDescription)")
    print("CodingPath: \(context.codingPath)")
    return nil
} catch let DecodingError.typeMismatch(type, context) {
    print("Type mismatch for type: \(type)")
    print("Context: \(context.debugDescription)")
    print("CodingPath: \(context.codingPath)")
    return nil
} catch let DecodingError.valueNotFound(type, context) {
    print("Value not found for type: \(type)")
    print("Context: \(context.debugDescription)")
    return nil
} catch {
    print("Decoding error: \(error)")
    return nil
}
```

**Production Pattern:**

```swift
enum NetworkError: LocalizedError {
    case decodingFailed(reason: String)

    var errorDescription: String? {
        switch self {
        case .decodingFailed(let reason):
            return "Failed to decode response: \(reason)"
        }
    }
}

func decodeUser(from data: Data) throws -> User {
    do {
        return try JSONDecoder().decode(User.self, from: data)
    } catch let DecodingError.keyNotFound(key, context) {
        throw NetworkError.decodingFailed(
            reason: "Missing key '\(key.stringValue)' at \(context.codingPath.map(\.stringValue).joined(separator: "."))"
        )
    } catch let DecodingError.typeMismatch(_, context) {
        throw NetworkError.decodingFailed(
            reason: "Type mismatch at \(context.codingPath.map(\.stringValue).joined(separator: "."))"
        )
    } catch {
        throw NetworkError.decodingFailed(reason: error.localizedDescription)
    }
}
```

## Performance Optimization

### Pattern: Background Decoding for Large JSON

```swift
// ❌ WRONG: Blocks main thread with 10MB JSON
let users = try JSONDecoder().decode([User].self, from: largeData)
updateUI(with: users)

// ✅ CORRECT: Background decoding
Task.detached {
    let users = try JSONDecoder().decode([User].self, from: largeData)
    await MainActor.run {
        updateUI(with: users)
    }
}
```

**Rule:** Decode > 1MB JSON on background thread.

### Pattern: Streaming for Very Large Files

```swift
// For multi-megabyte JSON files
func decodeInChunks(from fileURL: URL) throws -> [User] {
    let stream = InputStream(url: fileURL)!
    stream.open()
    defer { stream.close() }

    // Use JSONSerialization to read incrementally
    var users: [User] = []
    // Process in chunks to avoid loading entire file
    return users
}
```

## Common Mistakes

| Mistake | Reality | Fix |
|---------|---------|-----|
| "All fields required" | APIs change, fields disappear. App crashes. | Use optionals for unreliable fields |
| "One CodingKeys entry per renamed field" | Must list ALL properties if using CodingKeys | List every property, even non-renamed |
| "decoder.dateDecodingStrategy handles all dates" | Only ONE strategy per decoder | Custom init(from:) for mixed formats |
| "try! is fine for trusted APIs" | APIs break. App crashes in production. | Always use do-catch with informative errors |
| "Type mismatch errors are obvious" | CodingPath can be nested 5 levels deep | Log context.codingPath for diagnosis |
| "String → Int will auto-convert" | Strict types. "123" ≠ 123 in Codable | Match API types exactly or use custom decoding |

## Quick Reference

**CodingKeys:**
```swift
enum CodingKeys: String, CodingKey {
    case userID = "user_id"  // Map names
    case name                 // Keep same
}
```

**Nested containers:**
```swift
let outer = try decoder.container(keyedBy: OuterKeys.self)
let inner = try outer.nestedContainer(keyedBy: InnerKeys.self, forKey: .nested)
let value = try inner.decode(String.self, forKey: .value)
```

**Optional decoding:**
```swift
let value = try container.decodeIfPresent(String.self, forKey: .optional) ?? "default"
```

**Custom dates:**
```swift
init(from decoder: Decoder) throws {
    let container = try decoder.container(keyedBy: CodingKeys.self)
    let dateString = try container.decode(String.self, forKey: .date)
    let formatter = DateFormatter()
    formatter.dateFormat = "yyyy-MM-dd"
    date = formatter.date(from: dateString)!
}
```

## Advanced Patterns

### Polymorphic Decoding

```swift
// JSON with type field:
{
    "type": "image",
    "url": "https://..."
}
// OR
{
    "type": "video",
    "duration": 120
}

enum Media: Decodable {
    case image(url: String)
    case video(duration: Int)

    enum CodingKeys: String, CodingKey {
        case type, url, duration
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        let type = try container.decode(String.self, forKey: .type)

        switch type {
        case "image":
            let url = try container.decode(String.self, forKey: .url)
            self = .image(url: url)
        case "video":
            let duration = try container.decode(Int.self, forKey: .duration)
            self = .video(duration: duration)
        default:
            throw DecodingError.dataCorruptedError(
                forKey: .type,
                in: container,
                debugDescription: "Unknown media type: \(type)"
            )
        }
    }
}
```

### Lossy Array Decoding

**Problem:** Array with 1000 items, 3 are malformed. Want to decode 997, skip 3.

```swift
struct LossyArray<Element: Decodable>: Decodable {
    let elements: [Element]

    init(from decoder: Decoder) throws {
        var container = try decoder.unkeyedContainer()
        var elements: [Element] = []

        while !container.isAtEnd {
            do {
                let element = try container.decode(Element.self)
                elements.append(element)
            } catch {
                // Skip malformed element, continue
                _ = try? container.decode(FailableDecodable.self)
            }
        }
        self.elements = elements
    }
}

private struct FailableDecodable: Decodable {}

// Usage:
let response = try JSONDecoder().decode(LossyArray<User>.self, from: data)
print("Decoded \(response.elements.count) valid users")
```

## Red Flags - STOP and Reconsider

- Using `try!` for API decoding → Add proper error handling
- All fields non-optional → Make unreliable fields optional
- Type mismatch error with no context → Log context.codingPath
- Single date strategy for mixed formats → Custom init(from:)
- Decoding multi-MB JSON on main thread → Background Task
- "keyNotFound" in production → Field is optional in API, make it optional in Swift
- CodingKeys missing properties → List ALL properties

## Real-World Impact

**Before:** App crashes for 5% of users when API adds nullable `middleName` field (strict non-optional String).

**After:** `var middleName: String?` Optional field. Zero crashes.

---

**Before:** 10-second freeze decoding 8MB user feed JSON on main thread.

**After:** Background Task decoding. UI responsive, feed loads in 2 seconds.

---

**Before:** "typeMismatch" error in logs with no details. Hours debugging.

**After:** Log `context.codingPath` → "items.3.metadata.tags". Found malformed tag in 4th item immediately.
