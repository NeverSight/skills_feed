---
name: install-flutter-from-git
description: Install Flutter SDK via git clone and configure for all platforms
---

# Install Flutter from Git

This skill guides you through installing the Flutter SDK using `git clone` and setting up the environment for Web, Mobile, and Desktop development.

## 1. Prerequisites (All Platforms)

Ensure you have the following installed:
- **Git**: [Install Git](https://git-scm.com/downloads)
- **Curl/Unzip** (macOS/Linux usually have these; Windows usually needs Git Bash or similar)

## 2. Install Flutter SDK

### macOS / Linux
Open your terminal and run the following commands to clone the stable branch of the Flutter SDK.

```bash
# Create a directory for development (e.g., ~/development)
mkdir -p ~/development
cd ~/development

# Clone the Flutter SDK
git clone https://github.com/flutter/flutter.git -b stable
```

### Windows
Open PowerShell or Command Prompt.

```powershell
# Create a directory for development (e.g., C:\src)
mkdir C:\src
cd C:\src

# Clone the Flutter SDK
git clone https://github.com/flutter/flutter.git -b stable
```

## 3. Add Flutter to PATH

To run `flutter` commands from any terminal, you must add the SDK's `bin` directory to your PATH.

### macOS (Zsh) / Linux (Bash/Zsh)
1.  Open your shell configuration file (e.g., `~/.zshrc`, `~/.bashrc`, or `~/.zshenv`).
2.  Add the following line (replace `~/development/flutter` with your actual path):

    ```bash
    export PATH="$PATH:$HOME/development/flutter/bin"
    ```
3.  Refresh your current terminal:
    ```bash
    source ~/.zshrc  # or ~/.bashrc
    ```

### Windows
1.  Press `Win + S`, type "env", and select **Edit the system environment variables**.
2.  Click **Environment Variables**.
3.  Under **User variables**, select **Path** and click **Edit**.
4.  Click **New** and add the full path to `flutter\bin` (e.g., `C:\src\flutter\bin`).
5.  Click **OK** on all windows.
6.  Restart your terminal/PowerShell.

## 4. Verify Installation

Run the following command to check for missing dependencies:

```bash
flutter doctor
```

## 5. Platform Setup

### Web (Chrome)
1.  **Install Chrome**: Ensure Google Chrome is installed.
2.  **Enable Web Support** (usually enabled by default):
    ```bash
    flutter config --enable-web
    ```
3.  **Verify**: Run `flutter devices` to see "Chrome" listed.

### Mobile (iOS & Android)

#### iOS (macOS only)
1.  **Install Xcode**: Download from the Mac App Store.
2.  **Configure Command Line Tools**:
    ```bash
    sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
    sudo xcodebuild -runFirstLaunch
    ```
3.  **Install CocoaPods** (for dependency management):
    ```bash
    sudo gem install cocoapods
    ```
4.  **Simulator**: Open via `open -a Simulator`.

#### Android (All Operating Systems)
1.  **Install Android Studio**: [Download here](https://developer.android.com/studio).
2.  **Install SDK Components**:
    - Open Android Studio -> SDK Manager.
    - Install **Android SDK Platform-Tools**.
    - Install **Android SDK Command-line Tools (latest)**.
3.  **Accept Licenses**:
    ```bash
    flutter doctor --android-licenses
    ```
    (Press `y` to accept all licences).
4.  **Emulator**: Create a device in AVD Manager.

### Desktop (macOS, Windows, Linux)

#### macOS Desktop
1.  **Install Xcode**: (Same as iOS steps above).
2.  **Enable macOS**:
    ```bash
    flutter config --enable-macos-desktop
    ```

#### Windows Desktop
1.  **Install Visual Studio** (not VS Code): [Download VS Community](https://visualstudio.microsoft.com/downloads/).
2.  **Workloads**: When installing, select **Desktop development with C++**.
3.  **Enable Windows**:
    ```bash
    flutter config --enable-windows-desktop
    ```

#### Linux Desktop
1.  **Install Dependencies** (Ubuntu/Debian example):
    ```bash
    sudo apt-get update
    sudo apt-get install clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev
    ```
2.  **Enable Linux**:
    ```bash
    flutter config --enable-linux-desktop
    ```

## 6. Final Check

Run `flutter doctor` again to ensure all desired platforms have checkmarks.

```bash
flutter doctor -v
```
