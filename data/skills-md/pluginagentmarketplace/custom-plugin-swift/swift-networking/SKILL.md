---
name: swift-networking
description: Handle networking in Swift - URLSession, async/await, Codable, API clients, error handling
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 04-swift-data
bond_type: PRIMARY_BOND
---

# Swift Networking Skill

Modern networking patterns for Swift applications using URLSession, async/await, and type-safe API clients.

## Prerequisites

- iOS 15+ / macOS 12+ (for async/await)
- Understanding of HTTP fundamentals
- Familiarity with Codable protocol

## Parameters

```yaml
parameters:
  base_url:
    type: string
    required: true
    description: API base URL
  timeout:
    type: number
    default: 30
    description: Request timeout in seconds
  retry_enabled:
    type: boolean
    default: true
  max_retries:
    type: number
    default: 3
  auth_type:
    type: string
    enum: [none, bearer, api_key, basic]
    default: bearer
```

## Topics Covered

### URLSession Configuration
| Configuration | Use Case |
|---------------|----------|
| `.default` | Standard caching, credentials |
| `.ephemeral` | No persistent storage |
| `.background` | Large transfers, app suspended |

### HTTP Methods
| Method | Purpose | Body |
|--------|---------|------|
| GET | Retrieve resource | No |
| POST | Create resource | Yes |
| PUT | Replace resource | Yes |
| PATCH | Partial update | Yes |
| DELETE | Remove resource | Optional |

### Response Handling
| Status Code | Meaning | Action |
|-------------|---------|--------|
| 200-299 | Success | Parse response |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Refresh token / re-auth |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource missing |
| 429 | Rate Limited | Backoff and retry |
| 500-599 | Server Error | Retry with backoff |

## Code Examples

### Type-Safe API Client
```swift
import Foundation

// MARK: - Protocol Definitions

protocol APIEndpoint {
    associatedtype Response: Decodable
    var path: String { get }
    var method: HTTPMethod { get }
    var headers: [String: String] { get }
    var queryItems: [URLQueryItem]? { get }
    var body: Encodable? { get }
}

extension APIEndpoint {
    var headers: [String: String] { [:] }
    var queryItems: [URLQueryItem]? { nil }
    var body: Encodable? { nil }
}

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case patch = "PATCH"
    case delete = "DELETE"
}

// MARK: - API Client

actor APIClient {
    private let session: URLSession
    private let baseURL: URL
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder
    private var authToken: String?

    init(baseURL: URL, configuration: URLSessionConfiguration = .default) {
        self.baseURL = baseURL
        self.session = URLSession(configuration: configuration)
        self.decoder = JSONDecoder()
        self.decoder.dateDecodingStrategy = .iso8601
        self.decoder.keyDecodingStrategy = .convertFromSnakeCase
        self.encoder = JSONEncoder()
        self.encoder.dateEncodingStrategy = .iso8601
        self.encoder.keyEncodingStrategy = .convertToSnakeCase
    }

    func setAuthToken(_ token: String?) {
        self.authToken = token
    }

    func request<E: APIEndpoint>(_ endpoint: E) async throws -> E.Response {
        let request = try buildRequest(for: endpoint)
        let (data, response) = try await session.data(for: request)

        try validateResponse(response, data: data)

        do {
            return try decoder.decode(E.Response.self, from: data)
        } catch {
            throw APIError.decodingError(error, data: data)
        }
    }

    private func buildRequest<E: APIEndpoint>(for endpoint: E) throws -> URLRequest {
        var components = URLComponents(url: baseURL.appendingPathComponent(endpoint.path), resolvingAgainstBaseURL: true)!
        components.queryItems = endpoint.queryItems

        guard let url = components.url else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        if let token = authToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        endpoint.headers.forEach { request.setValue($1, forHTTPHeaderField: $0) }

        if let body = endpoint.body {
            request.httpBody = try encoder.encode(AnyEncodable(body))
        }

        return request
    }

    private func validateResponse(_ response: URLResponse, data: Data) throws {
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        switch httpResponse.statusCode {
        case 200..<300:
            return
        case 401:
            throw APIError.unauthorized
        case 403:
            throw APIError.forbidden
        case 404:
            throw APIError.notFound
        case 429:
            throw APIError.rateLimited
        case 400..<500:
            throw APIError.clientError(statusCode: httpResponse.statusCode, data: data)
        case 500..<600:
            throw APIError.serverError(statusCode: httpResponse.statusCode)
        default:
            throw APIError.unknown(statusCode: httpResponse.statusCode)
        }
    }
}

// MARK: - Error Types

enum APIError: LocalizedError {
    case invalidURL
    case invalidResponse
    case unauthorized
    case forbidden
    case notFound
    case rateLimited
    case clientError(statusCode: Int, data: Data)
    case serverError(statusCode: Int)
    case decodingError(Error, data: Data)
    case unknown(statusCode: Int)

    var errorDescription: String? {
        switch self {
        case .invalidURL: return "Invalid URL"
        case .invalidResponse: return "Invalid response"
        case .unauthorized: return "Authentication required"
        case .forbidden: return "Access denied"
        case .notFound: return "Resource not found"
        case .rateLimited: return "Rate limit exceeded"
        case .clientError(let code, _): return "Client error: \(code)"
        case .serverError(let code): return "Server error: \(code)"
        case .decodingError(let error, _): return "Decoding failed: \(error)"
        case .unknown(let code): return "Unknown error: \(code)"
        }
    }

    var isRetryable: Bool {
        switch self {
        case .rateLimited, .serverError: return true
        default: return false
        }
    }
}
```

### Retry Logic with Exponential Backoff
```swift
extension APIClient {
    func requestWithRetry<E: APIEndpoint>(
        _ endpoint: E,
        maxRetries: Int = 3,
        initialDelay: Duration = .seconds(1)
    ) async throws -> E.Response {
        var lastError: Error?
        var delay = initialDelay

        for attempt in 0..<maxRetries {
            do {
                return try await request(endpoint)
            } catch let error as APIError where error.isRetryable {
                lastError = error
                if attempt < maxRetries - 1 {
                    try await Task.sleep(for: delay)
                    delay *= 2 // Exponential backoff
                }
            } catch {
                throw error // Non-retryable error
            }
        }

        throw lastError ?? APIError.unknown(statusCode: 0)
    }
}
```

### Concrete Endpoint Example
```swift
enum ProductsAPI {
    struct GetProducts: APIEndpoint {
        typealias Response = [Product]
        let path = "/products"
        let method = HTTPMethod.get
        var queryItems: [URLQueryItem]? {
            [URLQueryItem(name: "page", value: "\(page)")]
        }

        let page: Int
    }

    struct CreateProduct: APIEndpoint {
        typealias Response = Product
        let path = "/products"
        let method = HTTPMethod.post
        var body: Encodable? { request }

        let request: CreateProductRequest
    }

    struct DeleteProduct: APIEndpoint {
        typealias Response = EmptyResponse
        var path: String { "/products/\(id)" }
        let method = HTTPMethod.delete

        let id: String
    }
}

struct EmptyResponse: Decodable {}

// Usage
let client = APIClient(baseURL: URL(string: "https://api.example.com")!)
await client.setAuthToken("your-token")

let products = try await client.request(ProductsAPI.GetProducts(page: 1))
let newProduct = try await client.request(ProductsAPI.CreateProduct(request: .init(name: "Widget")))
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "The certificate is not trusted" | SSL pinning or self-signed | Configure ATS or add certificate |
| "keyNotFound" | JSON key mismatch | Check CodingKeys, use keyDecodingStrategy |
| Request timeout | Network or server slow | Increase timeout, add retry |
| Memory spike on download | Not streaming | Use URLSession download task |

### Debug Tips
```swift
// Log request/response
extension URLRequest {
    func log() {
        print("➡️ \(httpMethod ?? "?") \(url?.absoluteString ?? "?")")
        if let body = httpBody, let str = String(data: body, encoding: .utf8) {
            print("Body: \(str)")
        }
    }
}

// Pretty print JSON for debugging
extension Data {
    var prettyJSON: String {
        guard let object = try? JSONSerialization.jsonObject(with: self),
              let data = try? JSONSerialization.data(withJSONObject: object, options: .prettyPrinted),
              let string = String(data: data, encoding: .utf8) else {
            return String(data: self, encoding: .utf8) ?? "Invalid data"
        }
        return string
    }
}
```

## Validation Rules

```yaml
validation:
  - rule: use_async_await
    severity: info
    check: Prefer async/await over completion handlers
  - rule: handle_all_errors
    severity: error
    check: All network calls must have error handling
  - rule: no_hardcoded_urls
    severity: warning
    check: URLs should be configurable, not hardcoded
```

## Usage

```
Skill("swift-networking")
```

## Related Skills

- `swift-concurrency` - Async patterns
- `swift-core-data` - Caching responses
- `swift-testing` - Mocking network calls
