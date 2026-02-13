---
name: session-management
description: "Expert session decisions for iOS/tvOS: token storage security levels, refresh flow architectures, multi-session handling strategies, and logout cleanup requirements. Use when implementing authentication, debugging token issues, or designing session architecture. Trigger keywords: session, authentication, token, Keychain, refresh token, access token, JWT, OAuth2, logout, session expiration, KeychainHelper, SecItemAdd, kSecAttrAccessible"
version: "3.0.0"
---

# Session Management — Expert Decisions

Expert decision frameworks for session management choices. Claude knows Keychain basics and OAuth concepts — this skill provides judgment calls for security levels, refresh strategies, and cleanup requirements.

---

## Decision Trees

### Token Storage Strategy

```
Where should you store authentication tokens?
├─ Access token (short-lived, <1hr)
│  └─ Keychain with kSecAttrAccessibleAfterFirstUnlock
│     Available after first unlock, survives restart
│
├─ Refresh token (long-lived)
│  └─ Keychain with kSecAttrAccessibleWhenUnlockedThisDeviceOnly
│     More secure, device-bound, requires unlock
│
├─ Session ID (server-side session)
│  └─ Keychain with kSecAttrAccessibleAfterFirstUnlock
│     Needs to work for background refreshes
│
├─ Temporary auth code (OAuth flow)
│  └─ Memory only (no persistence)
│     Used once, discarded immediately
│
└─ Remember me preference
   └─ UserDefaults (not sensitive)
      Just a boolean, not a credential
```

**The trap**: Storing tokens in UserDefaults. It's unencrypted, backed up to iCloud, and readable by jailbroken devices.

### Token Refresh Architecture

```
How should you handle token refresh?
├─ Simple app, few API calls
│  └─ Refresh on 401 response
│     Reactive: refresh when expired
│
├─ Frequent API calls
│  └─ Proactive refresh before expiration
│     Schedule refresh 5 min before exp
│
├─ Real-time features (WebSocket)
│  └─ Background refresh + reconnect
│     Maintain connection continuity
│
├─ Offline-first app
│  └─ Longer token lifetime + retry queue
│     Queue requests when offline
│
└─ High-security app
   └─ Short tokens + frequent refresh
      Minimize exposure window
```

### Multi-Session Architecture

```
How many sessions does your app support?
├─ Single device, single account
│  └─ Simple SessionManager singleton
│     Replace tokens on new login
│
├─ Single device, multiple accounts (switching)
│  └─ Account-keyed Keychain storage
│     Keychain items per account ID
│     Active account pointer
│
├─ Multiple devices, single account
│  └─ Server-side session management
│     Device tokens registered with server
│     Remote logout capability
│
└─ Multiple devices, multiple accounts
   └─ Full session registry
      Server tracks all device-account pairs
      Cross-device session visibility
```

### Logout Cleanup Scope

```
What needs clearing on logout?
├─ Always clear
│  └─ Tokens (Keychain)
│  └─ User object (memory)
│  └─ Authenticated state
│
├─ Usually clear
│  └─ URL cache (cached API responses)
│  └─ HTTP cookies
│  └─ User preferences tied to account
│
├─ Consider clearing
│  └─ Downloaded files (if user-specific)
│  └─ Core Data (if user-specific)
│  └─ Image cache (if contains private content)
│
└─ Usually keep
   └─ App preferences (theme, language)
   └─ Onboarding completion state
   └─ Device registration
```

---

## NEVER Do

### Token Storage

**NEVER** store tokens in UserDefaults:
```swift
// ❌ Unencrypted, backed up, exposed on jailbreak
UserDefaults.standard.set(accessToken, forKey: "accessToken")
UserDefaults.standard.set(refreshToken, forKey: "refreshToken")

// ✅ Use Keychain
try KeychainHelper.shared.save(accessToken, service: "auth", account: "accessToken")
try KeychainHelper.shared.save(refreshToken, service: "auth", account: "refreshToken")
```

**NEVER** log or print tokens:
```swift
// ❌ Tokens in console logs — security disaster
print("Token: \(accessToken)")
Logger.debug("Refresh token: \(refreshToken)")

// ✅ Log safely
Logger.debug("Token refreshed successfully")  // No token content
Logger.debug("Token length: \(accessToken.count)")  // Metadata only
```

**NEVER** hardcode secrets:
```swift
// ❌ Secrets in binary — extractable
let clientSecret = "abc123xyz789"
let apiKey = "sk-live-xxxxx"

// ✅ Use environment or server
// Fetch from server during OAuth flow
// Or use Info.plist with .gitignore for dev keys
let clientId = Bundle.main.infoDictionary?["CLIENT_ID"] as? String
```

### Token Refresh

**NEVER** retry refresh infinitely:
```swift
// ❌ Infinite loop if refresh token is invalid
func refreshToken() async throws {
    do {
        let response = try await API.refresh(token: refreshToken)
        storeTokens(response)
    } catch {
        try await refreshToken()  // Recursive retry — infinite loop!
    }
}

// ✅ Limited retries with backoff, then logout
func refreshToken(attempt: Int = 0) async throws {
    guard attempt < 3 else {
        await MainActor.run { logout() }
        throw SessionError.refreshFailed
    }

    do {
        let response = try await API.refresh(token: refreshToken)
        storeTokens(response)
    } catch {
        try await Task.sleep(nanoseconds: UInt64(pow(2.0, Double(attempt))) * 1_000_000_000)
        try await refreshToken(attempt: attempt + 1)
    }
}
```

**NEVER** refresh on every request:
```swift
// ❌ Unnecessary API calls
func makeRequest(_ endpoint: Endpoint) async throws -> Data {
    try await refreshAccessToken()  // Refresh EVERY request!
    return try await performRequest(endpoint)
}

// ✅ Refresh only when needed (expired or 401)
func makeRequest(_ endpoint: Endpoint) async throws -> Data {
    if isTokenExpired() {
        try await refreshAccessToken()
    }

    let (data, response) = try await performRequest(endpoint)

    if (response as? HTTPURLResponse)?.statusCode == 401 {
        try await refreshAccessToken()
        return try await performRequest(endpoint).0
    }

    return data
}
```

### Logout

**NEVER** forget to clear sensitive data:
```swift
// ❌ Partial cleanup — tokens still accessible
func logout() {
    currentUser = nil
    isAuthenticated = false
    // Forgot to clear Keychain tokens!
}

// ✅ Complete cleanup
func logout() {
    // Clear tokens
    KeychainHelper.shared.deleteAll(service: keychainService)

    // Clear memory
    currentUser = nil
    isAuthenticated = false

    // Clear caches
    URLCache.shared.removeAllCachedResponses()

    // Clear cookies
    HTTPCookieStorage.shared.removeCookies(since: .distantPast)

    // Clear UserDefaults user data
    let userKeys = ["userId", "userEmail", "userPreferences"]
    userKeys.forEach { UserDefaults.standard.removeObject(forKey: $0) }
}
```

**NEVER** leave background tasks running after logout:
```swift
// ❌ Background refresh continues for logged-out user
func logout() {
    clearTokens()
    currentUser = nil
    // Background refresh timer still running!
}

// ✅ Cancel all background work
func logout() {
    // Cancel scheduled tasks
    sessionRefreshTask?.cancel()
    sessionRefreshTask = nil

    // Cancel any pending requests
    URLSession.shared.getAllTasks { tasks in
        tasks.forEach { $0.cancel() }
    }

    // Clear data
    clearTokens()
    currentUser = nil
}
```

### Keychain Security

**NEVER** use wrong accessibility level:
```swift
// ❌ Too permissive — accessible even when locked
kSecAttrAccessibleAlways  // Deprecated and insecure!
kSecAttrAccessibleAlwaysThisDeviceOnly  // Still too permissive

// ✅ Appropriate accessibility
// For tokens that need background access:
kSecAttrAccessibleAfterFirstUnlock

// For highly sensitive data (biometric):
kSecAttrAccessibleWhenUnlockedThisDeviceOnly
```

**NEVER** ignore Keychain errors:
```swift
// ❌ Silent failure — user appears logged out
func getToken() -> String? {
    let query = [...]
    var result: AnyObject?
    SecItemCopyMatching(query as CFDictionary, &result)  // Ignoring status!
    return result as? String
}

// ✅ Handle errors properly
func getToken() throws -> String? {
    let query = [...]
    var result: AnyObject?
    let status = SecItemCopyMatching(query as CFDictionary, &result)

    switch status {
    case errSecSuccess:
        guard let data = result as? Data,
              let token = String(data: data, encoding: .utf8) else {
            throw KeychainError.invalidData
        }
        return token
    case errSecItemNotFound:
        return nil  // No token stored
    default:
        throw KeychainError.unableToRetrieve(status: status)
    }
}
```

---

## Essential Patterns

### Secure SessionManager

```swift
@MainActor
final class SessionManager: ObservableObject {
    static let shared = SessionManager()

    @Published private(set) var isAuthenticated = false
    @Published private(set) var currentUser: User?

    private let keychainService = "com.app.auth"
    private var refreshTask: Task<Void, Never>?

    private init() {
        restoreSession()
    }

    // MARK: - Authentication

    func login(email: String, password: String) async throws {
        let response = try await AuthAPI.login(email: email, password: password)
        try storeTokens(access: response.accessToken, refresh: response.refreshToken)
        currentUser = response.user
        isAuthenticated = true
        scheduleTokenRefresh()
    }

    func logout() {
        // Cancel background work
        refreshTask?.cancel()
        refreshTask = nil

        // Clear Keychain
        KeychainHelper.shared.deleteAll(service: keychainService)

        // Clear state
        currentUser = nil
        isAuthenticated = false

        // Clear caches
        URLCache.shared.removeAllCachedResponses()
        HTTPCookieStorage.shared.removeCookies(since: .distantPast)
    }

    // MARK: - Token Management

    func getAccessToken() -> String? {
        KeychainHelper.shared.read(service: keychainService, account: "accessToken")
    }

    func refreshAccessToken() async throws {
        guard let refreshToken = KeychainHelper.shared.read(
            service: keychainService, account: "refreshToken"
        ) else {
            throw SessionError.noRefreshToken
        }

        let response = try await AuthAPI.refresh(token: refreshToken)
        try storeTokens(access: response.accessToken, refresh: response.refreshToken)
    }

    // MARK: - Private

    private func storeTokens(access: String, refresh: String) throws {
        try KeychainHelper.shared.save(access, service: keychainService, account: "accessToken")
        try KeychainHelper.shared.save(refresh, service: keychainService, account: "refreshToken")
    }

    private func restoreSession() {
        guard let _ = getAccessToken() else { return }
        isAuthenticated = true
        Task { try? await loadUserProfile() }
    }

    private func scheduleTokenRefresh() {
        refreshTask?.cancel()

        refreshTask = Task {
            while !Task.isCancelled {
                // Refresh 5 minutes before expiration
                try? await Task.sleep(nanoseconds: 55 * 60 * 1_000_000_000)  // 55 min
                guard !Task.isCancelled else { return }

                do {
                    try await refreshAccessToken()
                } catch {
                    await MainActor.run { logout() }
                    return
                }
            }
        }
    }
}
```

### Secure KeychainHelper

```swift
final class KeychainHelper {
    static let shared = KeychainHelper()
    private init() {}

    func save(_ value: String, service: String, account: String) throws {
        guard let data = value.data(using: .utf8) else {
            throw KeychainError.invalidData
        }

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlock
        ]

        // Delete existing
        SecItemDelete(query as CFDictionary)

        // Add new
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status: status)
        }
    }

    func read(service: String, account: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess,
              let data = result as? Data,
              let string = String(data: data, encoding: .utf8) else {
            return nil
        }

        return string
    }

    func delete(service: String, account: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account
        ]
        SecItemDelete(query as CFDictionary)
    }

    func deleteAll(service: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service
        ]
        SecItemDelete(query as CFDictionary)
    }
}

enum KeychainError: LocalizedError {
    case invalidData
    case saveFailed(status: OSStatus)
    case readFailed(status: OSStatus)

    var errorDescription: String? {
        switch self {
        case .invalidData: return "Invalid data format"
        case .saveFailed(let status): return "Keychain save failed: \(status)"
        case .readFailed(let status): return "Keychain read failed: \(status)"
        }
    }
}
```

### Auto-Retry Network Client

```swift
actor NetworkClient {
    private let sessionManager: SessionManager

    init(sessionManager: SessionManager = .shared) {
        self.sessionManager = sessionManager
    }

    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        var request = try endpoint.asURLRequest()

        // Add token
        if let token = await sessionManager.getAccessToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        let (data, response) = try await URLSession.shared.data(for: request)

        // Handle 401 with retry
        if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 401 {
            try await sessionManager.refreshAccessToken()

            // Retry with new token
            if let newToken = await sessionManager.getAccessToken() {
                request.setValue("Bearer \(newToken)", forHTTPHeaderField: "Authorization")
                let (retryData, _) = try await URLSession.shared.data(for: request)
                return try JSONDecoder().decode(T.self, from: retryData)
            }
        }

        return try JSONDecoder().decode(T.self, from: data)
    }
}
```

---

## Quick Reference

### Keychain Accessibility Levels

| Level | When Accessible | Use For |
|-------|-----------------|---------|
| WhenUnlocked | Device unlocked | Foreground-only tokens |
| AfterFirstUnlock | After first unlock | Background refresh tokens |
| WhenUnlockedThisDeviceOnly | Unlocked, no backup | Highly sensitive data |
| WhenPasscodeSetThisDeviceOnly | Passcode set | Biometric-protected |

### Logout Cleanup Checklist

| Data | Storage | Clear On Logout? |
|------|---------|------------------|
| Access token | Keychain | ✅ Always |
| Refresh token | Keychain | ✅ Always |
| User profile | Memory | ✅ Always |
| API cache | URLCache | ✅ Usually |
| Cookies | HTTPCookieStorage | ✅ Usually |
| User preferences | UserDefaults | ⚠️ Maybe |
| Downloaded files | FileManager | ⚠️ If user-specific |
| App settings | UserDefaults | ❌ Usually keep |

### Token Refresh Strategies

| Strategy | When to Use | Implementation |
|----------|-------------|----------------|
| On 401 | Simple apps | Retry after refresh |
| Proactive | Frequent API calls | Timer before expiration |
| Background | Real-time features | BGAppRefreshTask |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Tokens in UserDefaults | Unencrypted storage | Use Keychain |
| Logging token values | Security exposure | Log metadata only |
| Infinite refresh retry | DoS on invalid token | Limited retries + logout |
| Refresh on every request | Unnecessary API calls | Check expiration first |
| Partial logout cleanup | Data leakage | Clear all sensitive data |
| Ignoring Keychain errors | Silent failures | Handle status codes |
| kSecAttrAccessibleAlways | Too permissive | Use AfterFirstUnlock |
| Background tasks after logout | Stale operations | Cancel on logout |
