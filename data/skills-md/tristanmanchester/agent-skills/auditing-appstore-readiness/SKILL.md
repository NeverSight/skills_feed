---
name: auditing-appstore-readiness
description: Audit an iOS app repo (Swift/Xcode or React Native/Expo) for App Store compliance and release readiness; output a pass/warn/fail report and publish checklist.
metadata: {"openclaw":{"emoji":"🧾","requires":{"bins":["git"]}}}
---

# App Store Readiness Audit

This skill reviews an app repository and produces a release readiness report for iOS **App Store** / **TestFlight** submission.

It supports:
- Native iOS (Swift/Obj‑C, Xcode project/workspace)
- React Native (bare)
- Expo (managed or prebuild)

## Quick start (recommended)

Run the read‑only audit script from the repo root:

{ "tool": "exec", "command": "node {baseDir}/scripts/audit.mjs --repo . --format md" }

If you want JSON output as well:

{ "tool": "exec", "command": "node {baseDir}/scripts/audit.mjs --repo . --format md --json audit.json" }

If the repo is a monorepo, point at the app directory:

{ "tool": "exec", "command": "node {baseDir}/scripts/audit.mjs --repo apps/mobile --format md" }

## Output contract

Always return:
- Overall verdict: **PASS** / **WARN** / **FAIL**
- Detected project flavour and key identifiers (bundle id, version, build)
- A list of checks with evidence and remediation steps
- A **Publish checklist** the developer can tick off

Use: [references/report-template.md](references/report-template.md)

## Safety rules (don’t break the repo)

Default to **read‑only** commands. Do not run commands that modify the workspace unless:
- the user explicitly asks, **or**
- the fix is trivial and clearly desired (then explain what will change first)

Examples of mutating commands:
- dependency installs (`npm i`, `yarn`, `pnpm i`, `pod install`)
- config generation (`expo prebuild`)
- signing automation (`fastlane match`)
- archiving (`xcodebuild archive`, `eas build`) — creates artefacts and may require signing

If you must run a mutating command, label it clearly as **MUTATING** before running.

## Main workflow

### 1) Identify the repo and project flavour

Prefer scripted detection (`audit.mjs`). If doing manually:

- Expo likely: `package.json` contains `expo` and `app.json` / `app.config.*` exists
- React Native (bare): `package.json` contains `react-native` and `ios/` exists
- Native iOS: `*.xcodeproj` or `*.xcworkspace` exists

If multiple apps exist, pick the one matching the user’s intent; otherwise pick the directory with:
- a single `ios/<AppName>/Info.plist`, and
- exactly one `.xcodeproj` or `.xcworkspace` near the root.

### 2) Run static compliance checks (works everywhere)

Run these checks even without Xcode:

- Repo hygiene: clean git status; obvious secrets not committed
- iOS identifiers: bundle id, version, build number
- App icons: includes an App Store (1024×1024) icon
- Launch screen present
- Privacy & permissions:
  - Privacy manifest present (`PrivacyInfo.xcprivacy`) or explicitly accounted for
  - Permission usage strings present when relevant (camera, location, tracking, etc.)
  - Avoid broad ATS exemptions (`NSAllowsArbitraryLoads`)
- Third‑party SDK hygiene: licences, privacy manifests, tracking disclosures
- Store listing basics: privacy policy URL exists somewhere in repo/docs; support/contact info

The script outputs PASS/WARN/FAIL for these.

### 3) Run build‑accuracy checks (macOS + Xcode, optional but high confidence)

Only if you have **Xcode** available (local macOS gateway or a paired macOS node).

Recommended sequence (creates build artefacts):

1) Show Xcode + SDK versions:
{ "tool": "exec", "command": "xcodebuild -version" }

2) List schemes (project/workspace as detected):
{ "tool": "exec", "command": "xcodebuild -list -json -workspace <path>.xcworkspace" }
or
{ "tool": "exec", "command": "xcodebuild -list -json -project <path>.xcodeproj" }

3) Release build for simulator (fast, avoids signing):
{ "tool": "exec", "command": "xcodebuild -workspace <...> -scheme <...> -configuration Release -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 15' build" }

4) If you need a distribution artefact (**MUTATING / signing**):
- Prefer Fastlane if already configured
- Otherwise `xcodebuild archive` + `xcodebuild -exportArchive`

If build checks aren’t possible, the report must explicitly say so and keep the verdict at **WARN** (unless there are definite FAIL items).

### 4) Produce the final readiness report

- Use [references/report-template.md](references/report-template.md)
- Include a “Go / No‑Go” recommendation:
  - **FAIL** → must fix before submitting
  - **WARN** → submission may work, but risk areas remain
  - **PASS** → ready to submit; remaining items are administrative

## Manual checks the agent cannot fully verify

Always include these as a final checklist section (even if automated checks pass):

- App Store Connect metadata: screenshots, description, keywords, age rating, pricing, categories
- Privacy Nutrition Labels match actual behaviour
- Export compliance (encryption) answers are correct
- Content/IP rights: licences, third‑party assets, trademarks
- Account / regional requirements (e.g. EU trader status if applicable)
- In‑app purchases / subscriptions configured if used

See: [references/manual-checklist.md](references/manual-checklist.md)

## When the user asks “make it compliant”

Switch to fix mode:
1) Identify failing items that can be fixed safely in‑repo (Info.plist strings, `PrivacyInfo.xcprivacy` template, ATS exceptions tightening, etc.)
2) Propose minimal patches and apply with `apply_patch`
3) Re‑run `audit.mjs` and update the report

## Quick search

- Permissions mapping: [references/permissions-map.md](references/permissions-map.md)
- Expo‑specific checks: [references/expo.md](references/expo.md)
- React Native iOS checks: [references/react-native.md](references/react-native.md)
- Native iOS checks: [references/native-ios.md](references/native-ios.md)
