---
name: model-patterns
description: "Expert model design decisions for iOS/tvOS: when DTO separation adds value vs overkill, validation strategy selection, immutability trade-offs, and custom Codable decoder design. Use when designing data models, implementing API contracts, or debugging decoding failures. Trigger keywords: Codable, DTO, domain model, CodingKeys, custom decoder, validation, immutable, struct, mapping, JSON decoding"
version: "3.0.0"
---

# Model Patterns — Expert Decisions

Expert decision frameworks for model design choices. Claude knows Codable syntax — this skill provides judgment calls for when to separate DTOs, validation strategies, and immutability trade-offs.

---

## Decision Trees

### DTO vs Single Model

```
Does API response match your domain needs?
├─ YES (1:1 mapping)
│  └─ Is API contract stable?
│     ├─ YES → Single Codable model is fine
│     └─ NO → DTO protects against API changes
│
├─ NO (needs transformation)
│  └─ DTO + Domain model
│     DTO: matches API exactly
│     Domain: matches app needs
│
└─ Multiple APIs for same domain concept?
   └─ Separate DTOs per API
      Single domain model aggregates
```

**The trap**: DTO for everything. If your API matches your domain and is stable, a single Codable struct is simpler. Add DTO layer when it solves a real problem.

### Validation Strategy Selection

```
When should validation happen?
├─ External data (API, user input)
│  └─ Validate at boundary (init or factory)
│     Fail fast with clear errors
│
├─ Internal data (already validated)
│  └─ Trust it (no re-validation)
│     Validation at boundary is sufficient
│
└─ Critical invariants (money, permissions)
   └─ Type-level enforcement
      Email type, not String
      Money type, not Double
```

### Struct vs Class Decision

```
What are your requirements?
├─ Simple data container
│  └─ Struct (value semantics)
│     Passed by copy, immutable by default
│
├─ Shared mutable state needed?
│  └─ Really? Reconsider design
│     └─ If truly needed → Class with @Observable
│
├─ Identity matters (same instance)?
│  └─ Class (reference semantics)
│     But consider if ID equality suffices
│
└─ Inheritance needed?
   └─ Class (but prefer composition)
```

### Custom Decoder Complexity

```
How much custom decoding?
├─ Just key mapping (snake_case → camelCase)
│  └─ Use keyDecodingStrategy
│     decoder.keyDecodingStrategy = .convertFromSnakeCase
│
├─ Few fields need transformation
│  └─ Custom init(from decoder:)
│     Transform specific fields only
│
├─ Complex nested structure flattening
│  └─ Custom init(from decoder:) with nested containers
│     Or intermediate DTO + mapping
│
└─ Polymorphic decoding (type field determines struct)
   └─ Type-discriminated enum with associated values
      Or AnyDecodable wrapper
```

---

## NEVER Do

### DTO Design

**NEVER** make DTOs mutable:
```swift
// ❌ DTO can be modified after decoding
struct UserDTO: Codable {
    var id: String
    var name: String  // var allows mutation
}

// ✅ DTOs are immutable snapshots of API response
struct UserDTO: Codable {
    let id: String
    let name: String  // let enforces immutability
}
```

**NEVER** add business logic to DTOs:
```swift
// ❌ DTO has behavior
struct UserDTO: Codable {
    let id: String
    let firstName: String
    let lastName: String

    func sendWelcomeEmail() { ... }  // Business logic in DTO!

    var isAdmin: Bool {
        roles.contains("admin")  // Business rule in DTO
    }
}

// ✅ DTO is pure data; logic in domain model or service
struct UserDTO: Codable {
    let id: String
    let firstName: String
    let lastName: String
}

struct User {
    let id: String
    let fullName: String
    let isAdmin: Bool

    init(from dto: UserDTO, roles: [String]) {
        // Mapping and business logic here
    }
}
```

**NEVER** expose DTOs to UI layer:
```swift
// ❌ View depends on API contract
struct UserView: View {
    let user: UserDTO  // If API changes, UI breaks

    var body: some View {
        Text(user.first_name)  // Snake_case in UI!
    }
}

// ✅ View uses domain model
struct UserView: View {
    let user: User  // Stable domain model

    var body: some View {
        Text(user.fullName)  // Clean API
    }
}
```

### Codable Implementation

**NEVER** force-unwrap in custom decoders:
```swift
// ❌ Crashes on unexpected data
init(from decoder: Decoder) throws {
    let container = try decoder.container(keyedBy: CodingKeys.self)
    let urlString = try container.decode(String.self, forKey: .imageURL)
    imageURL = URL(string: urlString)!  // Crashes if invalid URL!
}

// ✅ Handle invalid data gracefully
init(from decoder: Decoder) throws {
    let container = try decoder.container(keyedBy: CodingKeys.self)
    let urlString = try container.decode(String.self, forKey: .imageURL)
    guard let url = URL(string: urlString) else {
        throw DecodingError.dataCorrupted(
            .init(codingPath: [CodingKeys.imageURL],
                  debugDescription: "Invalid URL: \(urlString)")
        )
    }
    imageURL = url
}
```

**NEVER** silently default invalid data:
```swift
// ❌ Hides data problems
init(from decoder: Decoder) throws {
    let container = try decoder.container(keyedBy: CodingKeys.self)
    // Silently uses 0 for invalid price — masks bugs!
    price = (try? container.decode(Double.self, forKey: .price)) ?? 0.0
}

// ✅ Fail or default with logging
init(from decoder: Decoder) throws {
    let container = try decoder.container(keyedBy: CodingKeys.self)
    do {
        price = try container.decode(Double.self, forKey: .price)
    } catch {
        Logger.api.warning("Invalid price, defaulting to 0: \(error)")
        price = 0.0  // Intentional default, logged
    }
}
```

**NEVER** use String for typed values:
```swift
// ❌ No type safety
struct User: Codable {
    let email: String  // Any string allowed
    let status: String  // "active", "inactive"... or typo?
}

// ✅ Type-safe wrappers
struct Email {
    let value: String
    init?(_ value: String) {
        guard value.contains("@") else { return nil }
        self.value = value
    }
}

enum UserStatus: String, Codable {
    case active, inactive, suspended
}

struct User {
    let email: Email
    let status: UserStatus
}
```

### Validation

**NEVER** validate in multiple places:
```swift
// ❌ Validation scattered
func saveUser(_ user: User) {
    guard user.email.contains("@") else { return }  // Duplicate!
    // ...
}

func displayUser(_ user: User) {
    guard user.email.contains("@") else { return }  // Duplicate!
    // ...
}

// ✅ Validate once at creation
struct User {
    let email: Email  // Email type guarantees validity

    init(email: String) throws {
        guard let validEmail = Email(email) else {
            throw ValidationError.invalidEmail
        }
        self.email = validEmail
        // All downstream code trusts email is valid
    }
}
```

**NEVER** throw generic errors from validation:
```swift
// ❌ Caller can't determine what's wrong
init(name: String, email: String, age: Int) throws {
    guard !name.isEmpty else { throw NSError(domain: "error", code: -1) }
    guard email.contains("@") else { throw NSError(domain: "error", code: -1) }
    // Same error for different problems!
}

// ✅ Specific validation errors
enum ValidationError: LocalizedError {
    case emptyName
    case invalidEmail(String)
    case ageOutOfRange(Int)

    var errorDescription: String? {
        switch self {
        case .emptyName: return "Name cannot be empty"
        case .invalidEmail(let email): return "Invalid email: \(email)"
        case .ageOutOfRange(let age): return "Age \(age) is out of valid range"
        }
    }
}
```

---

## Essential Patterns

### DTO with Domain Mapping

```swift
// DTO: Exact API contract
struct UserDTO: Codable {
    let id: String
    let first_name: String
    let last_name: String
    let email: String
    let avatar_url: String?
    let created_at: String
    let is_verified: Bool
}

// Domain: App's representation
struct User: Identifiable {
    let id: String
    let fullName: String
    let email: Email
    let avatarURL: URL?
    let createdAt: Date
    let isVerified: Bool

    var initials: String {
        fullName.split(separator: " ")
            .compactMap { $0.first }
            .map(String.init)
            .joined()
    }
}

// Mapping extension
extension User {
    init(from dto: UserDTO) throws {
        self.id = dto.id
        self.fullName = "\(dto.first_name) \(dto.last_name)"

        guard let email = Email(dto.email) else {
            throw MappingError.invalidEmail(dto.email)
        }
        self.email = email

        self.avatarURL = dto.avatar_url.flatMap(URL.init)
        self.createdAt = ISO8601DateFormatter().date(from: dto.created_at) ?? Date()
        self.isVerified = dto.is_verified
    }
}
```

### Type-Safe Wrapper Pattern

```swift
struct Email: Codable, Hashable {
    let value: String

    init?(_ value: String) {
        let regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i
        guard value.wholeMatch(of: regex) != nil else { return nil }
        self.value = value
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        let rawValue = try container.decode(String.self)
        guard let email = Email(rawValue) else {
            throw DecodingError.dataCorrupted(
                .init(codingPath: container.codingPath,
                      debugDescription: "Invalid email: \(rawValue)")
            )
        }
        self = email
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        try container.encode(value)
    }
}

// Usage: compiler enforces email validity
func sendEmail(to: Email) { ... }  // Can't pass arbitrary String
```

### Polymorphic Decoding

```swift
enum MediaItem: Codable {
    case image(ImageMedia)
    case video(VideoMedia)
    case document(DocumentMedia)

    private enum CodingKeys: String, CodingKey {
        case type
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        let type = try container.decode(String.self, forKey: .type)

        switch type {
        case "image":
            self = .image(try ImageMedia(from: decoder))
        case "video":
            self = .video(try VideoMedia(from: decoder))
        case "document":
            self = .document(try DocumentMedia(from: decoder))
        default:
            throw DecodingError.dataCorrupted(
                .init(codingPath: [CodingKeys.type],
                      debugDescription: "Unknown media type: \(type)")
            )
        }
    }

    func encode(to encoder: Encoder) throws {
        switch self {
        case .image(let media): try media.encode(to: encoder)
        case .video(let media): try media.encode(to: encoder)
        case .document(let media): try media.encode(to: encoder)
        }
    }
}
```

---

## Quick Reference

### When to Use DTO Separation

| Scenario | Use DTO? |
|----------|----------|
| API matches domain exactly | No |
| API likely to change | Yes |
| Need transformation (flatten, combine) | Yes |
| Multiple APIs for same concept | Yes |
| Single stable internal API | No |

### Validation Strategy by Layer

| Layer | Validation Type |
|-------|-----------------|
| API boundary (DTO init) | Structure validity |
| Domain model init | Business rules |
| Type wrappers | Format enforcement |
| UI | Already validated |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| `var` in DTO | Mutable snapshot | Use `let` |
| Business logic in DTO | Wrong layer | Move to domain model |
| DTO in View | Coupling | Map to domain model |
| Force-unwrap in decoder | Crash risk | Throw or optional |
| String for typed values | No safety | Type wrappers |
| Same validation in multiple places | DRY violation | Validate at creation |
| Generic validation errors | Poor UX | Specific error cases |

### Decoder Strategy Selection

| Need | Solution |
|------|----------|
| snake_case → camelCase | `keyDecodingStrategy` |
| Custom date format | `dateDecodingStrategy` |
| Single field transformation | Custom `init(from:)` |
| Nested structure flattening | Nested containers |
| Type-discriminated union | Enum with associated values |
