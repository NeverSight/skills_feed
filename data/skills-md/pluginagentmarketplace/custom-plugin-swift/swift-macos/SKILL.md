---
name: swift-macos
description: Build macOS applications - AppKit, windows, menus, system integration, distribution
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 05-swift-macos
bond_type: PRIMARY_BOND
---

# Swift macOS Skill

Native macOS application development with AppKit, system integration, and distribution.

## Prerequisites

- Xcode 15+ on macOS Sonoma+
- Apple Developer account (for distribution)
- Understanding of AppKit fundamentals

## Parameters

```yaml
parameters:
  distribution_method:
    type: string
    enum: [app_store, developer_id, none]
    default: developer_id
  sandbox_enabled:
    type: boolean
    default: true
  min_macos_version:
    type: string
    default: "13.0"
  app_type:
    type: string
    enum: [document_based, single_window, menu_bar, agent]
    default: single_window
```

## Topics Covered

### AppKit Components
| Component | Purpose |
|-----------|---------|
| NSWindow | Window management |
| NSViewController | View controller |
| NSView | Base view class |
| NSMenu | Menu bar and context menus |
| NSStatusItem | Menu bar icon |
| NSAlert | Dialog boxes |

### Window Types
| Type | Use Case |
|------|----------|
| NSWindow | Standard window |
| NSPanel | Utility/floating window |
| NSPopover | Attached popover |
| NSSavePanel/NSOpenPanel | File dialogs |

### Distribution Methods
| Method | Requirements |
|--------|--------------|
| Mac App Store | Sandbox, App Review |
| Developer ID | Notarization |
| Direct | None (Gatekeeper blocks) |

## Code Examples

### Menu Bar Application
```swift
import AppKit
import SwiftUI

@main
struct MenuBarApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        Settings {
            SettingsView()
        }
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem!
    private var popover: NSPopover!

    func applicationDidFinishLaunching(_ notification: Notification) {
        setupStatusItem()
        setupPopover()

        // Hide dock icon for menu bar only app
        NSApp.setActivationPolicy(.accessory)
    }

    private func setupStatusItem() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)

        if let button = statusItem.button {
            button.image = NSImage(systemSymbolName: "star.fill", accessibilityDescription: "App")
            button.action = #selector(togglePopover)
        }
    }

    private func setupPopover() {
        popover = NSPopover()
        popover.contentSize = NSSize(width: 300, height: 400)
        popover.behavior = .transient
        popover.contentViewController = NSHostingController(rootView: PopoverView())
    }

    @objc private func togglePopover() {
        guard let button = statusItem.button else { return }

        if popover.isShown {
            popover.performClose(nil)
        } else {
            popover.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
            popover.contentViewController?.view.window?.makeKey()
        }
    }
}

struct PopoverView: View {
    @Environment(\.openSettings) private var openSettings

    var body: some View {
        VStack(spacing: 16) {
            Text("Menu Bar App")
                .font(.headline)

            Button("Settings") {
                openSettings()
            }

            Button("Quit") {
                NSApp.terminate(nil)
            }
        }
        .padding()
    }
}
```

### NSDocument-Based App
```swift
import AppKit

final class Document: NSDocument {
    var content: String = ""

    override class var autosavesInPlace: Bool { true }

    override func makeWindowControllers() {
        let contentVC = ContentViewController(document: self)
        let window = NSWindow(contentViewController: contentVC)
        window.setContentSize(NSSize(width: 800, height: 600))

        let windowController = NSWindowController(window: window)
        addWindowController(windowController)
    }

    override func data(ofType typeName: String) throws -> Data {
        guard let data = content.data(using: .utf8) else {
            throw NSError(domain: NSOSStatusErrorDomain, code: writErr)
        }
        return data
    }

    override func read(from data: Data, ofType typeName: String) throws {
        guard let content = String(data: data, encoding: .utf8) else {
            throw NSError(domain: NSOSStatusErrorDomain, code: readErr)
        }
        self.content = content
    }
}

final class ContentViewController: NSViewController {
    private let document: Document

    init(document: Document) {
        self.document = document
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) not implemented")
    }

    override func loadView() {
        let scrollView = NSScrollView()
        let textView = NSTextView()

        textView.isEditable = true
        textView.isRichText = false
        textView.font = .monospacedSystemFont(ofSize: 13, weight: .regular)
        textView.string = document.content

        scrollView.documentView = textView
        scrollView.hasVerticalScroller = true

        view = scrollView
    }
}
```

### Sandboxing with Security-Scoped Bookmarks
```swift
final class SandboxedFileAccess {
    private static let bookmarksKey = "securityScopedBookmarks"

    static func requestAccess(to url: URL) throws -> URL {
        let bookmark = try url.bookmarkData(
            options: .withSecurityScope,
            includingResourceValuesForKeys: nil,
            relativeTo: nil
        )

        var bookmarks = UserDefaults.standard.dictionary(forKey: bookmarksKey) as? [String: Data] ?? [:]
        bookmarks[url.path] = bookmark
        UserDefaults.standard.set(bookmarks, forKey: bookmarksKey)

        return url
    }

    static func accessBookmarkedURL(_ path: String) throws -> URL {
        guard let bookmarks = UserDefaults.standard.dictionary(forKey: bookmarksKey) as? [String: Data],
              let bookmarkData = bookmarks[path] else {
            throw SandboxError.noBookmark
        }

        var isStale = false
        let url = try URL(
            resolvingBookmarkData: bookmarkData,
            options: .withSecurityScope,
            relativeTo: nil,
            bookmarkDataIsStale: &isStale
        )

        if isStale {
            _ = try requestAccess(to: url)
        }

        return url
    }

    static func withAccess<T>(to url: URL, perform: (URL) throws -> T) throws -> T {
        guard url.startAccessingSecurityScopedResource() else {
            throw SandboxError.accessDenied
        }
        defer { url.stopAccessingSecurityScopedResource() }
        return try perform(url)
    }
}

enum SandboxError: Error {
    case noBookmark
    case accessDenied
}
```

### Notarization Script
```bash
#!/bin/bash
set -e

APP_PATH="$1"
DEVELOPER_ID="Developer ID Application: Your Name (TEAMID)"
KEYCHAIN_PROFILE="notary-profile"

echo "Signing..."
codesign --force --options runtime --sign "$DEVELOPER_ID" \
    --deep --strict "$APP_PATH"

echo "Creating ZIP..."
ditto -c -k --keepParent "$APP_PATH" "app.zip"

echo "Submitting for notarization..."
xcrun notarytool submit "app.zip" \
    --keychain-profile "$KEYCHAIN_PROFILE" \
    --wait

echo "Stapling..."
xcrun stapler staple "$APP_PATH"

echo "Verifying..."
spctl --assess --type execute --verbose=2 "$APP_PATH"

echo "Done!"
rm "app.zip"
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "App is damaged" | Not notarized | Notarize before distribution |
| Sandbox violation | Missing entitlement | Add required entitlement |
| Window not appearing | Wrong activation policy | Check NSApp.activationPolicy |
| Menu not responding | Missing target/action | Verify menu item connections |
| Sparkle updates fail | Code signing issue | Add exception entitlement |

### Debug Tips
```bash
# Check code signing
codesign -dv --verbose=4 App.app

# Check entitlements
codesign -d --entitlements :- App.app

# Check notarization
spctl --assess --type execute App.app

# View sandbox violations
log show --predicate 'subsystem == "com.apple.sandbox"' --last 1h
```

## Validation Rules

```yaml
validation:
  - rule: hardened_runtime
    severity: error
    check: Enable hardened runtime for notarization
  - rule: sandbox_entitlements
    severity: warning
    check: Only request necessary sandbox entitlements
  - rule: code_signing
    severity: error
    check: Sign with Developer ID for distribution
```

## Usage

```
Skill("swift-macos")
```

## Related Skills

- `swift-swiftui` - SwiftUI on macOS
- `swift-architecture` - App architecture
- `swift-testing` - Testing macOS apps
