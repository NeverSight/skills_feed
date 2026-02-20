---
name: proximity-reader
description: >
  Comprehensive iOS development skill for Apple's ProximityReader framework.
  Covers Tap to Pay on iPhone (payment card reading), loyalty card (VAS) integration,
  Store and Forward mode, the Verifier API (mobile document / ID reading), and
  merchant discovery UI. Use this skill whenever the user mentions ProximityReader,
  Tap to Pay on iPhone, contactless payments on iPhone, NFC payment reading,
  loyalty card reading from Wallet, VAS requests, mobile driver's license verification,
  ID verification on iPhone, MobileDocumentReader, PaymentCardReader,
  PaymentCardReaderSession, or any related topic. Also trigger when the user wants
  to build a point-of-sale (POS) app, accept contactless payments without hardware,
  or read digital wallet passes on iPhone.
---

# ProximityReader iOS Development Skill

Build contactless payment, loyalty, and ID verification features using Apple's ProximityReader framework on iPhone — no additional hardware required.

## When to Use This Skill

- Integrating **Tap to Pay on iPhone** (contactless payment acceptance)
- Reading **loyalty cards / VAS passes** from Apple Wallet
- Implementing **Store and Forward** for offline payment scenarios
- Building **ID verification** with the Verifier API (mobile driver's licenses, national IDs)
- Showing **merchant education UI** via `ProximityReaderDiscovery`
- Debugging `PaymentCardReaderError` or `MobileDocumentReaderError`

## Framework Overview

**ProximityReader** (iOS 15.4+, iPadOS 15.4+, Mac Catalyst 15.4+) enables an iPhone to act as a contactless reader for:

| Domain | Key Classes | Min iOS |
|--------|-------------|---------|
| Payments | `PaymentCardReader`, `PaymentCardReaderSession` | 15.4 |
| Loyalty (VAS) | `VASRequest`, `VASReadResult` | 15.4 |
| Store & Forward | `StoreAndForwardPaymentCardReaderSession`, `PaymentCardReaderStore` | 17.0+ |
| ID Verification | `MobileDocumentReader`, `MobileDocumentReaderSession` | 17.0+ |
| Merchant Discovery | `ProximityReaderDiscovery` | 18.0+ |

## Prerequisites & Entitlements

Before writing any code, ensure:

1. **Entitlement**: Request the Tap to Pay on iPhone entitlement from Apple via your developer account. Without it, the framework won't function.
2. **Payment Service Provider (PSP)**: You must coordinate with a Level 3 certified PSP (e.g. Stripe, Adyen, Square, Windcave). The PSP provides the **reader token** (JWT) required to initialize the reader.
3. **Device**: iPhone XS or later. No additional NFC hardware needed.
4. **Xcode**: Add the `com.apple.developer.proximity-reader.payment.acceptance` entitlement to your app's entitlements file.

For the Verifier API (ID reading), a separate entitlement and server-side reader token generation is required. Read `references/verifier-api.md` for details.

## Architecture at a Glance

```
┌─────────────────────────────────────────────────┐
│                   Your App                       │
├──────────┬──────────┬───────────┬───────────────┤
│ Payment  │ Loyalty  │ Store &   │  ID           │
│ Flow     │ (VAS)    │ Forward   │  Verification │
├──────────┴──────────┴───────────┴───────────────┤
│              ProximityReader Framework           │
├─────────────────────────────────────────────────┤
│         Secure Element / NFC Hardware            │
└─────────────────────────────────────────────────┘
```

## Quick Reference: Common Patterns

### 1. Payment Card Reading (Tap to Pay)

```swift
import ProximityReader

// 1. Create and configure the reader
let reader = PaymentCardReader()

// 2. Obtain token from your PSP
let token = PaymentCardReader.Token(rawValue: pspProvidedJWT)

// 3. Link the merchant account (first use only)
if try await !reader.isAccountLinked(using: token) {
    try await reader.linkAccount(using: token)
}

// 4. Create a session and prepare
let session = try await PaymentCardReaderSession(reader: reader, token: token)
try await session.prepare()

// 5. Read a payment card
let request = PaymentCardTransactionRequest(
    amount: Decimal(29.99),
    currencyCode: "USD",
    type: .purchase
)

let result: PaymentCardReadResult = try await session.readPaymentCard(request)
// Send result.paymentCardData to your PSP for processing
```

### 2. Loyalty Card (VAS) Reading

```swift
// Can be combined with payment or standalone
let vasRequest = VASRequest(
    merchantIdentifier: "pass.com.example.loyalty",
    localizedDescription: "Example Loyalty Program"
)

// Read loyalty card alongside payment
let result = try await session.readPaymentCard(
    request,
    vasRequest: vasRequest
)

// Access loyalty data
if let vasResult = result.vasReadResult {
    // Process loyalty identifiers
}
```

### 3. Store and Forward (Offline)

```swift
let sfSession = try await StoreAndForwardPaymentCardReaderSession(
    reader: reader,
    token: token
)
try await sfSession.prepare()

// Transactions are stored locally
let result = try await sfSession.readPaymentCard(request)

// Later, when online: retrieve and send batches
let store = PaymentCardReaderStore()
let batches: [StoreAndForwardBatch] = try await store.allBatches()

for batch in batches {
    // Send batch.data to PSP
    // On success, delete the batch
    try await store.delete(using: batch.deletionToken)
}
```

### 4. Mobile Document / ID Reading (Verifier API)

Read `references/verifier-api.md` for the full setup including server-side reader token generation.

```swift
import ProximityReader

let docReader = MobileDocumentReader()
let readerToken = try await fetchReaderToken() // From your server

let session = try await MobileDocumentReaderSession(
    reader: docReader,
    readerToken: readerToken
)
try await session.prepare()

// Request a driver's license display
let displayRequest = MobileDriversLicenseDisplayRequest(
    retainedElements: [.givenName, .familyName, .portrait, .dateOfBirth, .ageOver21]
)
try await session.readDocument(displayRequest)

// Or request validated data
let dataRequest = MobileDriversLicenseDataRequest(
    retainedElements: [.givenName, .familyName, .dateOfBirth]
)
let documentResult = try await session.readDocument(dataRequest)
```

### 5. Merchant Discovery UI

```swift
// iOS 18+: Show Apple-provided merchant education
let discovery = ProximityReaderDiscovery()
try await discovery.present()
```

## Error Handling

Always wrap ProximityReader calls in do-catch. The two main error types are:

```swift
do {
    try await session.readPaymentCard(request)
} catch let error as PaymentCardReaderError {
    switch error {
    case .notAllowed:
        // Missing entitlement or not authorized
    case .unsupported:
        // Device doesn't support Tap to Pay
    case .networkError:
        // Connectivity issue
    case .invalidReaderToken:
        // Token from PSP is invalid or expired
    case .readerBusy:
        // Another read session is active
    case .backgrounded:
        // App moved to background during read — must call prepare() again
    default:
        break
    }
} catch let error as PaymentCardReaderSession.ReadError {
    switch error {
    case .cancelled:
        // Customer cancelled the tap
    case .invalidAmount:
        // Amount was negative or zero
    case .notReady:
        // prepare() was not called
    default:
        break
    }
}
```

For the Verifier API:
```swift
catch let error as MobileDocumentReaderError {
    // Handle session preparation and document request errors
}
```

## Critical Implementation Notes

- **Always call `prepare()` after the app returns to the foreground.** The reader session is invalidated when backgrounded. Safe to call multiple times.
- **Call `prepare()` after each transaction** to reset internal state for the next transaction.
- **The reader token (JWT) comes from your PSP**, not from Apple directly. Each PSP has their own token generation flow.
- **PIN entry** is supported on iOS 16.4+ for contactless cards that require it.
- **Testing**: Use `ProximityReaderStub` for simulator testing. Real NFC reads require a physical device.
- **Thread safety**: ProximityReader uses Swift concurrency (async/await). All calls should be made from the main actor or appropriate actor context.
- **Store and Forward**: Batches persist on device. Always delete after successful processing to avoid data accumulation.

## Deeper Reference Docs

For more detailed implementation guides, read these reference files:

| Reference | When to Read |
|-----------|-------------|
| `references/api-reference.md` | Full class/struct/enum listing with all properties and methods |
| `references/verifier-api.md` | Complete Verifier API setup including server-side token generation |
| `references/integration-patterns.md` | PSP integration patterns (Stripe, Adyen, Square), SwiftUI patterns, MVVM architecture |
| `references/troubleshooting.md` | Common errors, debugging tips, device compatibility |

## Code Generation Guidelines

When generating ProximityReader code:

1. Always `import ProximityReader`
2. Use Swift concurrency (async/await) — the entire API is async
3. Wrap all reader operations in do-catch with specific error handling
4. Include `prepare()` calls after foregrounding and after each transaction
5. Never hardcode PSP tokens — always fetch from server/PSP SDK
6. For SwiftUI: use `.task {}` modifier or `@MainActor` view models
7. Always check device capability before attempting to use the reader
8. Follow Apple HIG: the tap payment sheet is system-provided — don't recreate it
