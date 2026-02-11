---
name: sirikit
description: Integrate Siri voice interactions, Shortcuts, and intelligent suggestions into iOS/watchOS apps using Apple's SiriKit framework. Use when implementing Intents extensions, custom intents, Siri Shortcuts, voice phrase handling, intent resolution/confirmation/handling, IntentsUI for custom Siri interfaces, donating shortcuts, or App Intents migration. Covers system intent domains (messaging, payments, ride booking, workouts, media) and custom intent definition.
---

# SiriKit Development Skill

Empower users to interact with your app through voice, Shortcuts, and intelligent suggestions.

## Quick Start

### Add Intents Extension
1. File → New → Target → Intents Extension
2. Enable "Include UI Extension" if customizing Siri interface
3. Enable Siri capability in main app target (Signing & Capabilities)

### Minimal Intent Handler

```swift
import Intents

class IntentHandler: INExtension {
    override func handler(for intent: INIntent) -> Any {
        switch intent {
        case is OrderSoupIntent:
            return OrderSoupIntentHandler()
        default:
            return self
        }
    }
}

class OrderSoupIntentHandler: NSObject, OrderSoupIntentHandling {
    // 1. Resolve parameters
    func resolveSoup(for intent: OrderSoupIntent) async -> SoupResolutionResult {
        guard let soup = intent.soup else {
            return .needsValue()
        }
        return .success(with: soup)
    }
    
    // 2. Confirm intent
    func confirm(intent: OrderSoupIntent) async -> OrderSoupIntentResponse {
        return OrderSoupIntentResponse(code: .ready, userActivity: nil)
    }
    
    // 3. Handle intent
    func handle(intent: OrderSoupIntent) async -> OrderSoupIntentResponse {
        // Fulfill the request
        return OrderSoupIntentResponse.success(message: "Your order is confirmed!")
    }
}
```

## Intent Handling Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    User speaks to Siri                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. RESOLVE - Validate each parameter                         │
│    • Return .success(with:) if valid                        │
│    • Return .needsValue() if missing                        │
│    • Return .disambiguation(with:) for choices              │
│    • Return .unsupported() if invalid                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. CONFIRM - Final validation before execution               │
│    • Verify services are ready                              │
│    • Return .ready or appropriate failure code              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. HANDLE - Fulfill the intent                               │
│    • Execute the action                                     │
│    • Return success/failure response                        │
└─────────────────────────────────────────────────────────────┘
```

## System Intent Domains

| Domain | Use Cases | Key Intents |
|--------|-----------|-------------|
| **Messaging** | Send/search messages | `INSendMessageIntent`, `INSearchForMessagesIntent` |
| **Calling** | VoIP calls | `INStartCallIntent`, `INSearchCallHistoryIntent` |
| **Payments** | Money transfers | `INSendPaymentIntent`, `INRequestPaymentIntent` |
| **Ride Booking** | Request rides | `INRequestRideIntent`, `INGetRideStatusIntent` |
| **Workouts** | Start/end workouts | `INStartWorkoutIntent`, `INEndWorkoutIntent` |
| **Media** | Play audio/video | `INPlayMediaIntent`, `INAddMediaIntent` |
| **Photos** | Search photos | `INSearchForPhotosIntent` |
| **Lists & Notes** | Create notes/tasks | `INCreateNoteIntent`, `INAddTasksIntent` |
| **Car Commands** | Vehicle controls | `INSetCarLockStatusIntent`, `INActivateCarSignalIntent` |
| **Reservations** | Restaurant bookings | `INGetReservationDetailsIntent` |

## Custom Intents

### Define in Intent Definition File
1. Create `Intents.intentdefinition` file
2. Add new intent with VerbNoun naming (e.g., `OrderSoup`)
3. Set category matching purpose
4. Define parameters with types

### Parameter Types
- **System**: String, Integer, Boolean, Date, Person, Location, Currency
- **Custom**: Define your own types as enums or objects

## Reference Documentation

- **[Intent Handling](references/intent-handling.md)**: Resolution, confirmation, handling patterns
- **[Shortcuts](references/shortcuts.md)**: Donating, suggesting, and managing shortcuts
- **[Custom Intents](references/custom-intents.md)**: Intent definition file, parameters, responses
- **[IntentsUI](references/intents-ui.md)**: Custom Siri interface views
- **[Vocabulary](references/vocabulary.md)**: Custom terminology and phrases
- **[App Intents Migration](references/app-intents.md)**: Modern App Intents framework

## Key Configuration

### Info.plist (Intents Extension)
```xml
<key>NSExtension</key>
<dict>
    <key>NSExtensionAttributes</key>
    <dict>
        <key>IntentsSupported</key>
        <array>
            <string>OrderSoupIntent</string>
        </array>
        <key>IntentsRestrictedWhileLocked</key>
        <array>
            <string>INSendPaymentIntent</string>
        </array>
    </dict>
    <key>NSExtensionPointIdentifier</key>
    <string>com.apple.intents-service</string>
    <key>NSExtensionPrincipalClass</key>
    <string>$(PRODUCT_MODULE_NAME).IntentHandler</string>
</dict>
```

### Request Siri Authorization
```swift
import Intents

INPreferences.requestSiriAuthorization { status in
    switch status {
    case .authorized: print("Siri authorized")
    case .denied: print("Siri denied")
    case .notDetermined: print("Not determined")
    case .restricted: print("Restricted")
    @unknown default: break
    }
}
```

## Common Patterns

### Donate Shortcut After User Action
```swift
import Intents

func donateOrderShortcut(order: Order) {
    let intent = OrderSoupIntent()
    intent.soup = order.soup
    intent.quantity = order.quantity
    
    let interaction = INInteraction(intent: intent, response: nil)
    interaction.identifier = order.id.uuidString
    
    interaction.donate { error in
        if let error = error {
            print("Donation failed: \(error)")
        }
    }
}
```

### Delete Donated Shortcuts
```swift
// Delete specific
INInteraction.delete(with: [orderID.uuidString]) { error in }

// Delete all from app
INInteraction.deleteAll { error in }
```

### Handle Intent in App (when launched)
```swift
// SwiftUI
.onContinueUserActivity(NSStringFromClass(OrderSoupIntent.self)) { activity in
    if let intent = activity.interaction?.intent as? OrderSoupIntent {
        handleOrderIntent(intent)
    }
}

// UIKit SceneDelegate
func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
    if let intent = userActivity.interaction?.intent as? OrderSoupIntent {
        handleOrderIntent(intent)
    }
}
```

## Key Constraints

- **Background execution**: Extensions run briefly; launch app for long tasks
- **Shared data**: Use App Groups for data between app and extension
- **No UI in extension**: Use IntentsUI extension for custom views
- **Testing**: Wait after install for Siri to recognize new intents
- **Localization**: Provide localized `AppIntentVocabulary.plist`
