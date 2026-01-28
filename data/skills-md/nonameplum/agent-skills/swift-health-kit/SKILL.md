---
name: swift-health-kit
description: Apple HealthKit framework for health and fitness data. Use for reading/writing health samples, workout data, authorization flows, observer queries, background delivery, clinical records, activity rings, and integrating with the Health app across iPhone, Apple Watch, iPad, and visionOS.
---

# HealthKit

## What to open

- Use `Articles/healtkit.md` for complete HealthKit documentation (188 pages consolidated).
- Search within the file by section URLs or keywords like `HKHealthStore`, `HKQuantitySample`, `HKWorkout`, `HKObserverQuery`.

## Document structure

The documentation file is organized by Apple documentation URLs as section headers. Key sections:

| Line | Topic |
|------|-------|
| ~11 | Framework overview |
| ~115 | About the HealthKit framework (architecture) |
| ~246 | Setting up HealthKit (entitlements, Info.plist) |
| ~357 | Authorizing access to health data |
| ~517 | Protecting user privacy |
| ~586 | Saving data to HealthKit |
| ~673 | Reading data from HealthKit (queries) |
| ~760 | HKHealthStore API reference |
| ~968 | Creating a Mobility Health App (sample project) |
| ~1025 | Data types (type identifiers) |
| ~1614 | Samples (HKSample, quantity, category, correlations) |
| ~1871 | Queries (sample, anchored, statistics, observer) |
| ~2146 | Visualizing State of Mind in visionOS |
| ~2203 | Logging symptoms associated with a medication |
| ~2278 | Workouts and activity rings |
| ~2449 | HKError and error handling |
| ~3152 | Executing observer queries |
| ~4778 | Background delivery (HKUpdateFrequency) |
| ~5974 | HKObjectType and subclasses |
| ~7264 | HKSampleType reference |

## Setup checklist

1. Add HealthKit capability in Xcode (enable Clinical Health Records only if needed).
2. Add `NSHealthShareUsageDescription` and `NSHealthUpdateUsageDescription` to Info.plist.
3. Check `HKHealthStore.isHealthDataAvailable()` before any HealthKit calls.
4. Create a single `HKHealthStore` instance and retain it for the app's lifetime.
5. Request authorization with `requestAuthorization(toShare:read:)` before reading or writing.

## Common workflows

### Reading data

1. Create the appropriate `HKSampleType` or `HKQuantityType`.
2. Build a query descriptor (e.g., `HKSampleQueryDescriptor`, `HKStatisticsQueryDescriptor`).
3. Execute the query against `HKHealthStore`.
4. Handle results on a background queue; dispatch to main for UI updates.

### Saving data

1. Create an `HKQuantitySample`, `HKCategorySample`, or `HKCorrelation`.
2. Use matching units for the data type (e.g., `.count()` for steps, `.meter()` for distance).
3. Call `healthStore.save(_:withCompletion:)`.
4. Check `authorizationStatus(for:)` before saving to catch permission issues early.

### Background delivery

1. Enable Background Modes in Xcode (Background fetch).
2. Call `enableBackgroundDelivery(for:frequency:withCompletion:)` for each data type.
3. Register an `HKObserverQuery` with an update handler.
4. When woken, call `healthStore.execute(_:)` to re-run the query.

### Workouts

1. Create an `HKWorkoutConfiguration` with activity type and location.
2. Start a workout session on Apple Watch with `HKWorkoutSession`.
3. Use `HKLiveWorkoutBuilder` to collect real-time samples.
4. End the session and save the workout with `endCollection(withEnd:completion:)`.

## Key types

| Type | Purpose |
|------|---------|
| `HKHealthStore` | Central access point; authorization, queries, saving |
| `HKQuantitySample` | Numeric health data (steps, heart rate, weight) |
| `HKCategorySample` | Enumerated data (sleep analysis, menstrual flow) |
| `HKCorrelation` | Composite samples (food, blood pressure) |
| `HKWorkout` | Fitness activity with duration, energy, distance |
| `HKObserverQuery` | Long-running query for store changes |
| `HKAnchoredObjectQueryDescriptor` | Track additions/deletions since last anchor |
| `HKStatisticsQueryDescriptor` | Aggregate calculations (sum, avg, min, max) |
| `HKStatisticsCollectionQueryDescriptor` | Time-bucketed statistics for charts |

## Privacy and authorization

- HealthKit uses fine-grained authorization per data type.
- Apps cannot detect if read permission was denied; queries simply return no data.
- Use `authorizationStatus(for:)` to check write permission before saving.
- Guest User sessions on visionOS restrict mutations; handle `errorNotPermissibleForGuestUserMode`.
- Never use HealthKit data for advertising or sell it to third parties.

## Platform availability

- **iPhone/Apple Watch/visionOS**: Full HealthKit store with sync.
- **iPadOS 17+**: Has its own HealthKit store.
- **iPadOS 16 and earlier / macOS 13+**: Framework available but `isHealthDataAvailable()` returns `false`.
- Use `earliestPermittedSampleDate()` on Apple Watch to find oldest available data.

## Error handling

Check for these common `HKError.Code` values:

- `errorHealthDataUnavailable` – Device doesn't support HealthKit.
- `errorHealthDataRestricted` – Enterprise or parental restrictions.
- `errorAuthorizationNotDetermined` – Authorization not yet requested.
- `errorAuthorizationDenied` – User denied write permission.
- `errorNotPermissibleForGuestUserMode` – Vision Pro guest session restriction.
- `errorRequiredAuthorizationDenied` – Required clinical record types denied.

## SwiftUI integration

Use the `HealthKitUI` framework for SwiftUI authorization:

```swift
import HealthKitUI

.healthDataAccessRequest(
    store: healthStore,
    shareTypes: allTypes,
    readTypes: allTypes,
    trigger: trigger
) { result in
    // Handle authorization result
}
```

## Reminders

- HealthKit store is thread-safe; samples are immutable.
- Avoid samples longer than 24 hours; many types have duration limits.
- Correlations store contained samples internally—don't save them separately.
- Use `HKDeletedObject` via anchored queries to detect deletions.
- For workout heart rate zones, use `HKWorkoutActivity` and route samples.Message Łukasz Śliwiński.p-ia4_client--huddle-workspace-in-sidebar {
				--huddlesWorkspaceHeight: 0px;
			}
		Open in split viewHow was the audio and video?
