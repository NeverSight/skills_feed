---
name: robotframework-appium-skill
description: Guide AI agents in creating AppiumLibrary tests for iOS and Android native apps, hybrid apps, and mobile browsers. Load when asked about mobile testing, Appium, or mobile app automation.
---

# AppiumLibrary Skill for Robot Framework

## Quick Reference

AppiumLibrary enables mobile app testing on iOS and Android using Appium automation.

## Installation

```bash
# Install the library
pip install robotframework-appiumlibrary

# Install Appium server (requires Node.js)
npm install -g appium

# Install platform drivers
appium driver install uiautomator2    # Android
appium driver install xcuitest        # iOS
```

## Appium Server

Appium server must be running before tests:

```bash
appium                    # Start with defaults
appium server             # Alternative
appium --port 4724        # Custom port
```

Default URL: `http://127.0.0.1:4723`

## Library Import

```robotframework
*** Settings ***
Library    AppiumLibrary
```

## Android Quick Start

### Open Android App

```robotframework
Open Application    http://127.0.0.1:4723
...    platformName=Android
...    platformVersion=13
...    deviceName=emulator-5554
...    automationName=UiAutomator2
...    app=${CURDIR}/app.apk
```

### Android Locators (Priority Order)

```robotframework
# 1. accessibility_id (RECOMMENDED - stable)
Click Element    accessibility_id=login_button

# 2. id (resource-id)
Click Element    id=com.example:id/login_button
Click Element    id=login_button                    # Short form if unique

# 3. xpath
Click Element    xpath=//android.widget.Button[@text='Login']

# 4. android UIAutomator2 selector
Click Element    android=new UiSelector().text("Login")

# 5. class name
Click Element    class=android.widget.Button
```

## iOS Quick Start

### Open iOS App

```robotframework
Open Application    http://127.0.0.1:4723
...    platformName=iOS
...    platformVersion=17.0
...    deviceName=iPhone 15
...    automationName=XCUITest
...    app=${CURDIR}/MyApp.app
...    udid=auto                                    # For real devices
```

### iOS Locators (Priority Order)

```robotframework
# 1. accessibility_id (RECOMMENDED - stable)
Click Element    accessibility_id=loginButton

# 2. name
Click Element    name=Login

# 3. ios predicate string
Click Element    ios=type == 'XCUIElementTypeButton' AND name == 'Login'

# 4. ios class chain (fast) - NOTE: use chain= prefix for class chains
Click Element    chain=**/XCUIElementTypeButton[`name == 'Login'`]

# 5. xpath
Click Element    xpath=//XCUIElementTypeButton[@name='Login']

# 6. class name
Click Element    class=XCUIElementTypeButton
```

## Essential Keywords

### Element Interaction

```robotframework
Click Element           locator
Click Text              visible_text
Input Text              locator    text_to_enter
Clear Text              locator
Tap                     locator    duration=0:00:01    # Long press (replaces removed Long Press)
```

### Getting Element Content

```robotframework
${text}=    Get Text              locator
${attr}=    Get Element Attribute    locator    attribute_name
${count}=   Get Matching Xpath Count    //android.widget.Button
```

### Waits

```robotframework
Wait Until Element Is Visible       locator    timeout=10s
Wait Until Page Contains            text       timeout=10s
Wait Until Page Contains Element    locator    timeout=10s
```

### Verification

```robotframework
Element Should Be Visible       locator
Element Should Be Enabled       locator
Page Should Contain Text        expected_text
Page Should Contain Element     locator
Element Text Should Be          locator    expected_text
```

### Screenshots

```robotframework
Capture Page Screenshot    filename.png
Capture Page Screenshot    ${OUTPUT_DIR}/screenshots/screen.png
```

## Get Page Source (View Hierarchy)

Useful for finding locators and debugging:

```robotframework
${source}=    Get Source
Log    ${source}
```

## Basic Gestures

```robotframework
# Scroll (locator is the element to scroll to/within)
Scroll Down    locator
Scroll Up      locator

# Swipe (start_x, start_y, end_x, end_y, duration as timedelta)
Swipe    start_x=500    start_y=1500    end_x=500    end_y=500    duration=0:00:01    # Swipe up

# Long press (use Tap with duration; Long Press was removed in v3.2.0)
Tap    locator    duration=0:00:02

# Tap at coordinates
Tap With Positions    500    800
```

## Android Scroll to Element (UIAutomator2)

```robotframework
# Automatically scrolls to find element!
Click Element    android=new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Settings"))
```

## Context Switching (Hybrid Apps)

```robotframework
# Check current context
${context}=    Get Current Context
Log    Current: ${context}

# List all contexts
@{contexts}=    Get Contexts
Log Many    @{contexts}

# Switch to webview
Switch To Context    WEBVIEW_com.example.app

# Switch back to native
Switch To Context    NATIVE_APP
```

## Mobile Browser Testing

### Android Chrome

```robotframework
Open Application    http://127.0.0.1:4723
...    platformName=Android
...    deviceName=emulator-5554
...    automationName=UiAutomator2
...    browserName=Chrome

Go To Url    https://example.com
Input Text    id=username    admin
Click Element    css=button[type='submit']
```

### iOS Safari

```robotframework
Open Application    http://127.0.0.1:4723
...    platformName=iOS
...    deviceName=iPhone 15
...    automationName=XCUITest
...    browserName=Safari

Go To Url    https://example.com
```

## Session Management

```robotframework
# Close app and end session
Close Application

# Background/foreground
Background Application    5    # Background for 5 seconds

# NOTE: Quit Application was removed in v3.0.0 - use Close Application instead
# NOTE: Reset Application was removed in v3.2.0 - use Close Application + Open Application instead
```

## W3C Capabilities Format (Appium 2.x)

Appium 2.x uses W3C capabilities with the `appium:` vendor prefix for non-standard capabilities:

```robotframework
Open Application    http://127.0.0.1:4723
...    platformName=Android
...    appium:automationName=UiAutomator2
...    appium:app=/path/to/app.apk
...    appium:deviceName=emulator-5554
...    appium:autoGrantPermissions=true
```

Only `platformName` is standard W3C. All other Appium-specific capabilities need the `appium:` prefix.
AppiumLibrary will typically add the prefix automatically, but explicitly using it is recommended for clarity.

## Cloud Testing (BrowserStack / Sauce Labs)

### BrowserStack

```robotframework
Open Application    http://hub-cloud.browserstack.com/wd/hub
...    platformName=Android
...    appium:deviceName=Google Pixel 7
...    appium:platformVersion=13.0
...    appium:app=bs://your_app_hash
...    bstack:options={"userName": "${BS_USERNAME}", "accessKey": "${BS_ACCESS_KEY}"}
```

### Sauce Labs

```robotframework
Open Application    https://ondemand.us-west-1.saucelabs.com:443/wd/hub
...    platformName=iOS
...    appium:deviceName=iPhone 14
...    appium:platformVersion=16
...    appium:app=storage:filename=MyApp.ipa
...    sauce:options={"username": "${SAUCE_USERNAME}", "accessKey": "${SAUCE_ACCESS_KEY}"}
```

## Removed Keywords and Alternatives

Several keywords were removed in AppiumLibrary v3.x:

| Removed Keyword | Version Removed | Alternative |
|-----------------|-----------------|-------------|
| `Long Press` | v3.2.0 | `Tap    locator    duration=0:00:01` |
| `Click A Point` | v3.0.0 | `Tap With Positions    x    y` |
| `Zoom` | v3.2.0 | Use W3C Actions via Execute Script |
| `Pinch` | v3.0.0 | Use W3C Actions via Execute Script |
| `Reset Application` | v3.2.0 | `Close Application` then `Open Application` |
| `Quit Application` | v3.0.0 | `Close Application` |
| `Background App` | v3.0.0 | `Background Application` |
| `Get Window Size` | N/A | `Get Window Width` / `Get Window Height` |

### W3C Actions for Zoom/Pinch

Zoom and Pinch gestures require W3C Actions in AppiumLibrary v3.x. These can be performed
using multi-touch sequences via the Appium driver directly if needed:

```robotframework
# Example: Use Execute Script to perform pinch/zoom via driver
Execute Script    mobile: pinchOpen    {"elementId": "${element_id}", "percent": 0.75}
```

## When to Load Additional References

Reference files for deeper guidance (planned):

<!-- Note: Reference files listed below are planned for future addition -->
| Need | Reference File |
|------|----------------|
| Android locator strategies | `references/locators-android.md` |
| iOS locator strategies | `references/locators-ios.md` |
| Device capabilities setup | `references/device-capabilities.md` |
| Gestures and scrolling | `references/gestures-touch.md` |
| iOS-specific features | `references/ios-specific.md` |
| Android-specific features | `references/android-specific.md` |
| Complete keyword list | `references/keywords-reference.md` |
| Common issues and solutions | `references/troubleshooting.md` |
