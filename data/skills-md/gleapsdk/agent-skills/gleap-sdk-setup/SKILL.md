---
name: gleap-sdk-setup
description: Integrates the Gleap customer feedback SDK into projects. Detects the platform (JavaScript, iOS, Android, React Native, Flutter, Ionic Capacitor, Cordova, FlutterFlow) and guides through installation, initialization, permissions, and common API usage like user identification and event tracking. Use when adding Gleap, setting up feedback SDK, or integrating Gleap SDK.
---

# Gleap SDK Setup

Guides users through integrating the Gleap SDK into their project. Supports JavaScript, iOS, Android, React Native, Flutter, Ionic/Capacitor, Cordova, and FlutterFlow.

## Platform Detection

Detect the user's platform before proceeding. If the user explicitly states their platform, skip detection.

### Auto-Detection Priority

Check in this order (first match wins):

1. **`pubspec.yaml` exists?**
   - Contains `flutterflow` references or user mentions FlutterFlow -> **FlutterFlow** (`platform-flutterflow.md`)
   - Otherwise -> **Flutter** (`platform-flutter.md`)

2. **`package.json` exists?** Read it and check `dependencies` + `devDependencies`:
   - `react-native` present -> **React Native** (`platform-react-native.md`)
   - `@capacitor/core` or `capacitor-core` present -> **Ionic/Capacitor** (`platform-ionic-capacitor.md`)
   - `cordova` present, or `config.xml` exists with `<widget>` -> **Cordova** (`platform-cordova.md`)
   - `@angular/core` present -> **JavaScript** (Angular)
   - `react` present (without `react-native`) -> **JavaScript** (React)
   - `vue` present -> **JavaScript** (Vue)
   - `next` present -> **JavaScript** (Next.js)
   - `nuxt` present -> **JavaScript** (Nuxt)
   - Other or no framework -> **JavaScript** (generic npm)
   - Use `platform-javascript.md` for all JavaScript variants

3. **`*.xcodeproj`, `*.xcworkspace`, or `Podfile` exists?** -> **iOS** (`platform-ios.md`)

4. **`build.gradle`, `build.gradle.kts`, or `app/build.gradle` exists?** -> **Android** (`platform-android.md`)

5. **`index.html` exists (no `package.json`)?** -> **JavaScript** CDN approach (`platform-javascript.md`)

6. **Server-side web framework detected?** These all use the **JavaScript SDK** on the client side (`platform-javascript.md`):
   - `composer.json` exists (PHP / Laravel) — use CDN or npm depending on whether a JS build pipeline exists
   - `Gemfile` with `rails` (Ruby on Rails) — use CDN in layouts, or npm if Webpacker/esbuild/importmap is present
   - `requirements.txt` / `pyproject.toml` with `django` or `flask` (Python) — use CDN in base templates
   - `*.cshtml` / `*.csproj` files (.NET / ASP.NET) — use CDN in layout views
   - `pom.xml` / `build.gradle` with Spring Boot (Java) — use CDN in Thymeleaf templates
   - Any other web framework (Go, Elixir/Phoenix, etc.) — use CDN approach
   - Note: If the project also has a `package.json` with a frontend framework, step 2 already covers this.

7. **Nothing detected** -> Ask the user which platform they are targeting.

### Detection Commands

Use `Glob` to scan for key files:
- `pubspec.yaml`
- `package.json`
- `**/*.xcodeproj`
- `**/*.xcworkspace`
- `Podfile`
- `build.gradle`
- `build.gradle.kts`
- `app/build.gradle`
- `config.xml`
- `index.html`
- `composer.json`
- `Gemfile`
- `requirements.txt`
- `pyproject.toml`

If `package.json` is found, use `Read` to inspect its `dependencies` and `devDependencies` keys.

## API Key Resolution

Before asking the user for their API key, check these locations in order:

1. **User provided it in the conversation** (e.g., "add Gleap with token abc123") — use it directly
2. **`.env` file** in the project root — look for `GLEAP_API_KEY=...`
3. **Environment variable** — check if `GLEAP_API_KEY` is set via `echo $GLEAP_API_KEY`
4. **Not found** — ask the user to provide their API key (available at https://app.gleap.io under Project Settings > Security > API Key)

When a key is found or provided, offer to save it to the project's `.env` file (creating it if needed, and adding `.env` to `.gitignore` if not already there) so it's available for future use.

## Workflow

Follow these steps in order:

1. **Fetch latest SDK versions**: Run `scripts/get-latest-versions.sh` from this skill's directory. Use the returned versions in all install commands instead of hardcoded version numbers.
2. **Detect platform** using the priority rules above.
3. **Resolve API key** using the API Key Resolution steps above.
4. **Confirm with user**: State the detected platform and ask for confirmation. If the user already specified a platform, skip this step.
5. **Read platform guide**: Read the matching `platform-{name}.md` file from this skill's directory.
6. **Install SDK**: Walk the user through installing the dependency using the latest version from step 1. Run install commands when the user approves. Verify installation succeeded.
7. **Initialize SDK**: Add initialization code using the resolved API key.
8. **Configure platform**: Apply required permissions, manifest entries, or additional config from the platform guide.
9. **Verify**: Suggest building/running the project to confirm integration works.

## Post-Setup API Guidance

After setup, if the user asks about using the Gleap API, refer to the "Common API Usage" section in the relevant platform file. The most common tasks are:

- **Identify users**: Associate sessions with user data (name, email, plan, custom data)
- **Track events**: Log custom events at key points in the app
- **Custom data**: Attach contextual data to feedback tickets
- **Widget control**: Programmatically open/close the Gleap widget

Re-read the platform file's API section for the correct method signatures, as they differ between platforms.

## Important Notes

- `initialize()` must be called exactly once in the application lifecycle
- For cross-platform frameworks (React Native, Flutter, Ionic/Capacitor), both iOS and Android platform-specific configuration (permissions) is needed
- The JavaScript CDN approach works for any web context and does not require npm
- For identity verification, the user hash must be generated server-side using the project's secret key
- Custom data supports only primitive values (strings, numbers, booleans) with a max of 35 keys

## Common Troubleshooting

- **`pod install` fails**: Run `pod repo update` first, then retry
- **Gradle sync fails**: Ensure `minSdkVersion` is at least 21
- **Flutter version conflict**: Add `tools:overrideLibrary="io.gleap.gleap_sdk"` to AndroidManifest.xml
- **Widget not showing on web**: Check Content Security Policy headers allow `sdk.gleap.io`
- **Soft-reload clears widget** (Rails/Turbo): Call `Gleap.getInstance().softReInitialize()` after reload
- **Android hardware acceleration**: Do not set `android:hardwareAccelerated="false"` at application level
