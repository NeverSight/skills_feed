---
name: carplay
description: CarPlay framework for iOS in-car applications
version: 1.0
---

# CarPlay Skill

## When to Use This Skill

Use this skill when:
- Developing CarPlay apps for iOS
- Building audio, podcast, or music apps for CarPlay
- Creating navigation apps with turn-by-turn guidance
- Implementing communication apps (messaging, VoIP)
- Building parking, EV charging, or food ordering apps
- Working with CPTemplate, CPInterfaceController, or any CarPlay APIs

## Description
Complete CarPlay framework documentation covering audio, communication, navigation, parking, EV charging, and food ordering integrations. Includes all templates (CPListTemplate, CPMapTemplate, CPGridTemplate, etc.), UI elements, and navigation APIs.

## Quick Reference

### Core Components

### Api Reference
- `CPInterfaceController`
- `CPWindow`
- `CarPlay`

### Communication
- `CPContact`
- `CPMessageListItem`

### Getting Started
- `CPSessionConfiguration`
- `CPTemplateApplicationScene`
- `CPTemplateApplicationSceneDelegate`

### Navigation
- `CPManeuver`
- `CPNavigationSession`
- `CPRouteChoice`
- `CPTrip`

### Poi
- `CPPointOfInterest`

### Templates
- `CPActionSheetTemplate`
- `CPAlertTemplate`
- `CPContactTemplate`
- `CPGridTemplate`
- `CPInformationTemplate`
- `CPListTemplate`
- `CPMapTemplate`
- `CPNowPlayingTemplate`
- `CPPointOfInterestTemplate`
- `CPSearchTemplate`
- `CPTabBarTemplate`
- `CPTemplate`
- `CPVoiceControlTemplate`

### Ui Elements
- `CPAlertAction`
- `CPBarButton`
- `CPButton`
- `CPGridButton`
- `CPInformationItem`
- `CPListImageRowItem`
- `CPListItem`
- `CPListSection`
- `CPTextButton`

### Dashboard (iOS 13.4+)
- `CPDashboardButton`
- `CPDashboardController`
- `CPTemplateApplicationDashboardScene`
- `CPTemplateApplicationDashboardSceneDelegate`

### Instrument Cluster (iOS 15.4+)
- `CPInstrumentClusterController`
- `CPTemplateApplicationInstrumentClusterScene`
- `CPTemplateApplicationInstrumentClusterSceneDelegate`


## Key Concepts

### Platform Support
- iOS 12.0+ (Core CarPlay)
- iOS 13.4+ (Dashboard scenes)
- iOS 14.0+ (Tab Bar, POI, Now Playing)
- iOS 15.4+ (Instrument Cluster)
- iOS 17.4+ (CPRouteInformation)
- iPadOS 12.0+
- Mac Catalyst 13.1+

### CarPlay App Categories

**⚠️ Important:** CarPlay apps require entitlements from Apple. You must request and receive approval for your specific app category before your app can connect to CarPlay.

CarPlay supports apps in the following categories (each requires a separate entitlement):

- **Audio & Podcasts**: Music, podcasts, audiobooks, and radio apps
  - Entitlement: `com.apple.developer.carplay-audio`
  - Requirements: Audio playback, Now Playing integration

- **Communication**: Messaging and VoIP calling apps
  - Entitlement: `com.apple.developer.carplay-communication`
  - Requirements: CallKit integration, Siri integration

- **Navigation**: Turn-by-turn navigation and maps
  - Entitlement: `com.apple.developer.carplay-maps`
  - Requirements: Real-time navigation, route guidance

- **Parking**: Finding and paying for parking
  - Entitlement: `com.apple.developer.carplay-parking`
  - Requirements: Location services, parking availability

- **EV Charging**: Locating and managing electric vehicle charging
  - Entitlement: `com.apple.developer.carplay-charging`
  - Requirements: Charging station data, availability status

- **Food Ordering**: Quick service food ordering
  - Entitlement: `com.apple.developer.carplay-quick-food`
  - Requirements: Menu browsing, order placement

**How to request entitlements:**
1. Visit https://developer.apple.com/contact/carplay/
2. Describe your app's functionality and category
3. Wait for Apple's review and approval (typically 1-2 weeks)
4. Add the approved entitlement to your Xcode project

### Template-Based UI
CarPlay uses a template-based system where Apple provides the UI components and you provide the content. This ensures:
- Driver-safe interfaces optimized for in-car use
- Consistent user experience across all CarPlay apps
- Automatic adaptation to different vehicle displays

## Usage Guidelines

1. **Use appropriate templates** for your app category
2. **Keep content simple** - limit items and text for driver safety
3. **Provide large, clear images** for better visibility
4. **Handle connection/disconnection** gracefully
5. **Test in CarPlay Simulator** before testing in vehicle
6. **Follow distraction guidelines** - no video, animations, or ads while driving

### Testing with CarPlay Simulator

The CarPlay Simulator in Xcode allows you to test your app without a physical vehicle:

**Setup:**
1. Open your CarPlay app project in Xcode
2. Select an iOS Simulator as your run destination
3. In the Simulator menu: **I/O > External Displays > CarPlay**
4. A CarPlay display window will appear alongside the iOS simulator

**Simulator Features:**
- Test all CarPlay templates and UI elements
- Simulate day/night modes (automatic based on system dark mode)
- Test different screen sizes and aspect ratios
- Simulate Siri interactions and voice commands
- Test connection/disconnection scenarios
- Debug layout issues before vehicle testing

**Limitations:**
- Cannot test actual vehicle integration
- Limited testing of physical controls (knobs, touchscreens)
- Some vehicle-specific features unavailable
- Audio routing may differ from actual vehicles

**Best Practice:** Always test in the simulator first, then verify in a physical vehicle or CarPlay-compatible head unit before release.

## Navigation

See the `references/` directory for detailed API documentation organized by category:
- `references/api_reference.md` - Api Reference
- `references/communication.md` - Communication
- `references/dashboard.md` - Dashboard and Instrument Cluster
- `references/getting_started.md` - Getting Started
- `references/navigation.md` - Navigation
- `references/poi.md` - Poi
- `references/templates.md` - Templates
- `references/ui_elements.md` - Ui Elements


## Best Practices

- **Scene Management**: Implement `CPTemplateApplicationSceneDelegate` to handle CarPlay connection
- **Template Limits**: Respect maximum item counts (CPListTemplate: 12 sections, CPGridTemplate: 8 buttons)
- **Image Sizes**: Follow recommended image sizes for templates and UI elements
- **Dynamic Updates**: Use update methods (`updateSections`, `updateButtons`) to refresh content
- **Navigation Hierarchy**: Use push/pop for navigation, present for modals
- **Error Handling**: Gracefully handle failures and provide user feedback

## Common Patterns

### Basic List Template
```swift
// Create list items
let item1 = CPListItem(text: "Song Title", detailText: "Artist Name")
item1.handler = { item, completion in
    // Handle selection
    completion()
}

// Create section and template
let section = CPListSection(items: [item1, item2])
let listTemplate = CPListTemplate(title: "My Playlist", sections: [section])

// Set as root
interfaceController.setRootTemplate(listTemplate, animated: true)
```

### Navigation with Map Template
```swift
// Create map template
let mapTemplate = CPMapTemplate()
mapTemplate.mapDelegate = self

// Show trip preview
let trip = CPTrip(/* route data */)
mapTemplate.showTripPreviews([trip], textConfiguration: nil)

// Start navigation
let navigationSession = mapTemplate.startNavigationSession(for: trip)
navigationSession.upcomingManeuvers = [maneuver1, maneuver2]
```

### Tab Bar Template
```swift
// Create root templates for each tab
let musicTab = CPListTemplate(title: "Music", sections: [musicSection])
musicTab.tabTitle = "Music"
musicTab.tabImage = UIImage(systemName: "music.note")

let podcastsTab = CPListTemplate(title: "Podcasts", sections: [podcastSection])
podcastsTab.tabTitle = "Podcasts"
podcastsTab.tabImage = UIImage(systemName: "mic")

// Create tab bar
let tabBarTemplate = CPTabBarTemplate(templates: [musicTab, podcastsTab])
interfaceController.setRootTemplate(tabBarTemplate, animated: false)
```

### Now Playing Template
```swift
// Configure Now Playing buttons
let playButton = CPNowPlayingPlaybackRateButton()
let skipButton = CPNowPlayingSkipButton(handler: { _ in
    // Skip to next track
})

CPNowPlayingTemplate.shared.updateNowPlayingButtons([playButton, skipButton])
CPNowPlayingTemplate.shared.isUpNextButtonEnabled = true
```

### Sports Mode for Live Events (iOS 18.4+)
```swift
// Create team logos
let homeTeamLogo = CPNowPlayingSportsTeamLogo(teamLogo: UIImage(named: "home_logo")!)
let awayTeamLogo = CPNowPlayingSportsTeamLogo(teamInitials: "VIS")

// Create teams with scores and possession
let homeTeam = CPNowPlayingSportsTeam(
    name: "Home Team",
    logo: homeTeamLogo,
    teamStandings: "1st Place",
    eventScore: "21",
    possessionIndicator: .solid,  // Home team has possession
    favorite: true
)

let awayTeam = CPNowPlayingSportsTeam(
    name: "Away Team",
    logo: awayTeamLogo,
    teamStandings: "2nd Place",
    eventScore: "17",
    possessionIndicator: nil,  // No possession
    favorite: false
)

// Create game clock (counting down from 15:00)
let gameClock = CPNowPlayingSportsClock(
    timeRemaining: 15 * 60,  // 15 minutes in seconds
    paused: false
)

// Create event status with status text and clock
let eventStatus = CPNowPlayingSportsEventStatus(
    eventStatusText: ["3rd Quarter", "4th Down", "Goal Line"],
    eventStatusImage: UIImage(named: "field_position"),
    eventClock: gameClock
)

// Create sports mode
let sportsMode = CPNowPlayingModeSports(
    leftTeam: homeTeam,
    rightTeam: awayTeam,
    eventStatus: eventStatus,
    backgroundArtwork: UIImage(named: "stadium_background")
)

// Set as active now playing mode
CPNowPlayingTemplate.shared.nowPlayingMode = sportsMode

// Update clock during game (e.g., every second)
Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
    // Update time remaining
    let newClock = CPNowPlayingSportsClock(
        timeRemaining: getCurrentGameTime(),
        paused: isGamePaused()
    )

    // Update event status with new clock
    let updatedStatus = CPNowPlayingSportsEventStatus(
        eventStatusText: eventStatus.eventStatusText,
        eventStatusImage: eventStatus.eventStatusImage,
        eventClock: newClock
    )

    // Refresh sports mode
    let updatedMode = CPNowPlayingModeSports(
        leftTeam: homeTeam,
        rightTeam: awayTeam,
        eventStatus: updatedStatus,
        backgroundArtwork: sportsMode.backgroundArtwork
    )

    CPNowPlayingTemplate.shared.nowPlayingMode = updatedMode
}
```

### Navigation with Maneuvers
```swift
// Create maneuvers for turn-by-turn guidance
let maneuver = CPManeuver()
maneuver.instructionVariants = ["Turn right onto Main Street"]
maneuver.symbolImage = UIImage(named: "turn-right")
maneuver.initialTravelEstimates = CPTravelEstimates(
    distanceRemaining: Measurement(value: 500, unit: UnitLength.meters),
    timeRemaining: 60
)

// Add lane guidance
let lane1 = CPLane(angles: [.left, .straight])
lane1.status = .recommended
let lane2 = CPLane(angles: [.straight, .right])
lane2.status = .preferred
maneuver.linkedLaneGuidance = CPLaneGuidance(lanes: [lane1, lane2], instructionVariants: ["Use right lane"])

// Add maneuver to navigation session
navigationSession.upcomingManeuvers = [maneuver]
```

### Attributed Instructions with Images
```swift
// Create attributed instruction with embedded image
let instruction = NSMutableAttributedString(string: "Turn right on Apple Park Way")

// Attach an image icon
let image = UIImage(systemName: "arrow.turn.up.right")!
let attachment = NSTextAttachment(image: image)
let imageString = NSAttributedString(attachment: attachment)
instruction.append(NSAttributedString(string: " "))
instruction.append(imageString)

// Create maneuver with attributed instruction
let maneuver = CPManeuver()
maneuver.attributedInstructionVariants = [instruction]

// Also set dashboard-specific attributed instructions
let dashboardInstruction = NSMutableAttributedString(string: "Turn Right ")
let dashboardImage = UIImage(systemName: "arrow.turn.up.right.circle.fill")!
let dashboardAttachment = NSTextAttachment(image: dashboardImage)
dashboardInstruction.append(NSAttributedString(attachment: dashboardAttachment))
dashboardInstruction.append(NSAttributedString(string: " Apple Park Way"))

maneuver.dashboardAttributedInstructionVariants = [dashboardInstruction]

// Set symbol image for main display
maneuver.symbolImage = UIImage(named: "turn-right")

// Add to navigation session
navigationSession.upcomingManeuvers = [maneuver]
```

### Route Selection
```swift
// Create route choices for trip preview
let fastRoute = CPRouteChoice(
    summaryVariants: ["Via Highway - 25 min"],
    additionalInformationVariants: ["Fastest route"],
    selectionSummaryVariants: ["Take the highway"]
)

let scenicRoute = CPRouteChoice(
    summaryVariants: ["Via Scenic Road - 35 min"],
    additionalInformationVariants: ["No tolls"],
    selectionSummaryVariants: ["Take the scenic route"]
)

let trip = CPTrip(
    origin: originMapItem,
    destination: destinationMapItem,
    routeChoices: [fastRoute, scenicRoute]
)

mapTemplate.showTripPreviews([trip], textConfiguration: nil)
```

### Dashboard Integration (iOS 13.4+)
```swift
// Configure dashboard scene delegate
func templateApplicationDashboardScene(
    _ dashboardScene: CPTemplateApplicationDashboardScene,
    didConnect dashboardController: CPDashboardController,
    to window: UIWindow
) {
    // Create dashboard shortcut buttons
    let homeButton = CPDashboardButton(
        titleVariants: ["Home"],
        subtitleVariants: ["123 Main St"],
        image: UIImage(systemName: "house.fill")!
    ) { button in
        // Navigate to home
    }

    let workButton = CPDashboardButton(
        titleVariants: ["Work"],
        subtitleVariants: ["456 Office Blvd"],
        image: UIImage(systemName: "building.2.fill")!
    ) { button in
        // Navigate to work
    }

    // Set dashboard shortcut buttons
    dashboardController.shortcutButtons = [homeButton, workButton]
}
```

### Instrument Cluster Integration (iOS 15.4+)
```swift
// Configure instrument cluster scene delegate
func templateApplicationInstrumentClusterScene(
    _ instrumentClusterScene: CPTemplateApplicationInstrumentClusterScene,
    didConnect instrumentClusterController: CPInstrumentClusterController
) {
    // Configure instrument cluster display
    instrumentClusterController.inactiveDescriptionVariants = [
        "No active navigation"
    ]

    // Set compass display
    instrumentClusterController.compassSetting = .automatic

    // Update with route information (iOS 17.4+)
    let routeInfo = CPRouteInformation(
        maneuvers: upcomingManeuvers,
        laneGuidances: lanGuidances,
        currentManeuvers: [currentManeuver],
        currentLaneGuidance: currentLaneGuidance,
        trip: currentTrip,
        maneuverTravelEstimates: travelEstimates
    )

    // Display on instrument cluster
    instrumentClusterController.compassSetting = .showAlways
}
```

### Grid Template
```swift
// Create grid buttons with icons
let homeButton = CPGridButton(
    titleVariants: ["Home"],
    image: UIImage(systemName: "house.fill")!
) { button in
    // Navigate to home
}

let workButton = CPGridButton(
    titleVariants: ["Work"],
    image: UIImage(systemName: "building.2.fill")!
) { button in
    // Navigate to work
}

let favoritesButton = CPGridButton(
    titleVariants: ["Favorites"],
    image: UIImage(systemName: "star.fill")!
) { button in
    // Show favorites
}

// Create grid template with up to 8 buttons
let gridTemplate = CPGridTemplate(
    title: "Quick Actions",
    gridButtons: [homeButton, workButton, favoritesButton]
)

interfaceController.setRootTemplate(gridTemplate, animated: true)

// Update buttons dynamically
let newButtons = [homeButton, workButton, favoritesButton, newButton]
gridTemplate.updateGridButtons(newButtons)
```

### Search Template
```swift
// Create search template
let searchTemplate = CPSearchTemplate()
searchTemplate.delegate = self

// Set as root
interfaceController.setRootTemplate(searchTemplate, animated: true)

// Implement CPSearchTemplateDelegate
func searchTemplate(
    _ searchTemplate: CPSearchTemplate,
    updatedSearchText searchText: String,
    completionHandler: @escaping ([CPListItem]) -> Void
) {
    // Perform search
    let results = performSearch(query: searchText)

    // Convert to list items
    let listItems = results.map { result in
        let item = CPListItem(text: result.name, detailText: result.address)
        item.handler = { item, completion in
            // Handle selection
            self.showResultDetails(result)
            completion()
        }
        return item
    }

    // Return results
    completionHandler(listItems)
}

func searchTemplateSearchButtonPressed(_ searchTemplate: CPSearchTemplate) {
    // User tapped search button
    print("Search initiated")
}
```

### Point of Interest Template
```swift
// Create points of interest
let poi1 = CPPointOfInterest(
    location: MKMapItem(placemark: MKPlacemark(coordinate: coordinate1)),
    title: "Apple Park",
    subtitle: "1 Apple Park Way",
    summary: "Apple headquarters",
    detailTitle: "Visitor Center",
    detailSubtitle: "Open 9 AM - 5 PM",
    detailSummary: "Tours available",
    pinImage: UIImage(systemName: "applelogo")
)

let poi2 = CPPointOfInterest(
    location: MKMapItem(placemark: MKPlacemark(coordinate: coordinate2)),
    title: "Golden Gate Bridge",
    subtitle: "San Francisco",
    summary: "Iconic landmark",
    detailTitle: "Vista Point",
    detailSubtitle: "Always Open",
    detailSummary: "Great views",
    pinImage: UIImage(systemName: "bridge")
)

// Create POI template
let poiTemplate = CPPointOfInterestTemplate(
    title: "Nearby Attractions",
    pointsOfInterest: [poi1, poi2],
    selectedIndex: 0
)

poiTemplate.pointOfInterestDelegate = self

// Implement delegate
func pointOfInterestTemplate(
    _ template: CPPointOfInterestTemplate,
    didSelectPointOfInterest poi: CPPointOfInterest
) {
    // User selected a POI
    print("Selected: \(poi.title)")

    // Show navigation options
    showNavigationOptions(for: poi)
}

func pointOfInterestTemplate(
    _ template: CPPointOfInterestTemplate,
    didChangeMapRegion region: MKCoordinateRegion
) {
    // Map region changed (user panned/zoomed)
    fetchNearbyPOIs(in: region)
}
```

### Information Template
```swift
// Create information items
let addressItem = CPInformationItem(
    title: "Address",
    detail: "1 Apple Park Way, Cupertino, CA"
)

let hoursItem = CPInformationItem(
    title: "Hours",
    detail: "9:00 AM - 9:00 PM"
)

let phoneItem = CPInformationItem(
    title: "Phone",
    detail: "(408) 996-1010"
)

// Create action buttons
let callButton = CPTextButton(text: "Call", textStyle: .normal) { button in
    // Make phone call
    makePhoneCall()
}

let directionsButton = CPTextButton(text: "Directions", textStyle: .confirm) { button in
    // Start navigation
    startNavigation()
}

// Create information template
let infoTemplate = CPInformationTemplate(
    title: "Apple Store",
    layout: .leading,  // or .twoColumn
    items: [addressItem, hoursItem, phoneItem],
    actions: [callButton, directionsButton]
)

interfaceController.pushTemplate(infoTemplate, animated: true)
```

### Action Sheet Template
```swift
// Create actions for action sheet
let confirmAction = CPAlertAction(title: "Confirm", style: .default) { action in
    // User confirmed
    self.performAction()
}

let cancelAction = CPAlertAction(title: "Cancel", style: .cancel) { action in
    // User cancelled
    print("Action cancelled")
}

let destructiveAction = CPAlertAction(title: "Delete", style: .destructive) { action in
    // User chose destructive action
    self.deleteItem()
}

// Create action sheet
let actionSheet = CPActionSheetTemplate(
    title: "Choose Action",
    message: "What would you like to do?",
    actions: [confirmAction, destructiveAction, cancelAction]
)

// Present modally
interfaceController.presentTemplate(actionSheet, animated: true, completion: nil)
```

### Alert Template
```swift
// Create alert actions
let okAction = CPAlertAction(title: "OK", style: .default) { action in
    // User tapped OK
    print("User acknowledged")
}

let retryAction = CPAlertAction(title: "Retry", style: .default) { action in
    // User wants to retry
    self.retryOperation()
}

let cancelAction = CPAlertAction(title: "Cancel", style: .cancel) { action in
    // User cancelled
}

// Create alert with multiple title variants for different screen sizes
let alert = CPAlertTemplate(
    titleVariants: [
        "Connection Lost",
        "Lost Connection",
        "No Network"
    ],
    actions: [retryAction, cancelAction]
)

// Present alert
interfaceController.presentTemplate(alert, animated: true, completion: nil)

// Auto-dismiss after 5 seconds
DispatchQueue.main.asyncAfter(deadline: .now() + 5) {
    interfaceController.dismissTemplate(animated: true, completion: nil)
}
```

### Voice Control Template
```swift
// Create voice control states
let listeningState = CPVoiceControlState(
    identifier: "listening",
    titleVariants: ["Listening...", "Say a command"],
    image: UIImage(systemName: "waveform")!,
    repeats: true
)

let processingState = CPVoiceControlState(
    identifier: "processing",
    titleVariants: ["Processing...", "Working on it"],
    image: UIImage(systemName: "gear")!,
    repeats: false
)

let successState = CPVoiceControlState(
    identifier: "success",
    titleVariants: ["Done!", "Complete"],
    image: UIImage(systemName: "checkmark.circle.fill")!,
    repeats: false
)

// Create voice control template
let voiceTemplate = CPVoiceControlTemplate(
    voiceControlStates: [listeningState, processingState, successState]
)

// Present voice control
interfaceController.presentTemplate(voiceTemplate, animated: true) {
    // Start listening
    self.startVoiceRecognition()
}

// Update state based on recognition progress
voiceTemplate.activateVoiceControlState(withIdentifier: "processing")

// Show success when done
voiceTemplate.activateVoiceControlState(withIdentifier: "success")

// Dismiss after completion
DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
    interfaceController.dismissTemplate(animated: true, completion: nil)
}
```

### Contact Template (Communication)
```swift
// Create contact
let contact = CPContact(
    name: "John Appleseed",
    image: UIImage(named: "contact_photo")
)
contact.subtitle = "Friend"
contact.informativeText = "Last contact: Today"

// Create contact action buttons
let callButton = CPContactCallButton(handler: { button in
    // Initiate phone call
    self.makePhoneCall(to: contact)
})

let messageButton = CPContactMessageButton(phoneOrEmail: "john@example.com")

let directionsButton = CPContactDirectionsButton(handler: { button in
    // Navigate to contact's location
    self.navigateToContact(contact)
})

contact.actions = [callButton, messageButton, directionsButton]

// Create contact template
let contactTemplate = CPContactTemplate(contact: contact)

// Present contact card
interfaceController.pushTemplate(contactTemplate, animated: true)
```

### Message List Template (Communication)
```swift
// Create leading configurations (profile images)
let profileImage = UIImage(named: "profile")!
let leadingConfig = CPMessageListItemLeadingConfiguration(
    leadingItem: .image(profileImage),
    leadingImage: profileImage,
    unreadIndicator: true
)

// Create trailing configurations (timestamps/badges)
let trailingConfig = CPMessageListItemTrailingConfiguration(
    trailingItem: .image(UIImage(systemName: "chevron.right")!),
    trailingImage: UIImage(systemName: "paperclip")
)

// Create message list items
let message1 = CPMessageListItem(
    conversationIdentifier: "conv_1",
    text: "John Appleseed",
    leadingConfiguration: leadingConfig,
    trailingConfiguration: trailingConfig,
    detailText: "Hey, are you free for lunch?",
    trailingText: "12:30 PM"
)
message1.handler = { item, completion in
    // Open conversation
    self.openConversation(id: "conv_1")
    completion()
}

let message2 = CPMessageListItem(
    fullName: "Jane Smith",
    phoneOrEmailAddress: "jane@example.com",
    leadingConfiguration: CPMessageListItemLeadingConfiguration(
        leadingItem: .image(UIImage(named: "jane_photo")!),
        leadingImage: UIImage(named: "jane_photo")!,
        unreadIndicator: false
    ),
    trailingConfiguration: trailingConfig,
    detailText: "Thanks for the update!",
    trailingText: "Yesterday"
)

// Create list template with messages
let section = CPListSection(items: [message1, message2])
let listTemplate = CPListTemplate(title: "Messages", sections: [section])

interfaceController.setRootTemplate(listTemplate, animated: true)
```

### List Image Row Item
```swift
// Create images for grid display
let image1 = UIImage(named: "album_cover_1")!
let image2 = UIImage(named: "album_cover_2")!
let image3 = UIImage(named: "album_cover_3")!
let image4 = UIImage(named: "album_cover_4")!

// Create list image row item with titles
let imageRowItem = CPListImageRowItem(
    text: "Recently Played",
    images: [image1, image2, image3, image4],
    imageTitles: ["Rock Hits", "Chill Vibes", "Workout Mix", "Road Trip"]
)

// Handle image selection
imageRowItem.listImageRowHandler = { item, index, completion in
    // User selected image at index
    print("Selected image \(index)")
    self.playAlbum(at: index)
    completion()
}

// Handle row selection
imageRowItem.handler = { item, completion in
    // User tapped the entire row (not a specific image)
    self.showRecentlyPlayed()
    completion()
}

// Create list with image row
let section = CPListSection(items: [imageRowItem])
let listTemplate = CPListTemplate(title: "Music", sections: [section])

// Update images dynamically
let newImages = [image1, image2, image3, image4, image5]
imageRowItem.update(newImages)
```

## Reference Documentation

For complete API details, see the categorized documentation in the `references/` directory.
