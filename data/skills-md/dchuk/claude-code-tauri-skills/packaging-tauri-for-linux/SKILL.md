---
name: packaging-tauri-for-linux
description: Guides users through packaging Tauri v2 applications for Linux distributions including AppImage, Debian (.deb), RPM, Flatpak, Snap, and AUR submission.
---

# Packaging Tauri Applications for Linux

## Critical Build Requirement

**glibc Compatibility**: Build on the oldest base system you intend to support (e.g., Ubuntu 18.04 rather than 22.04). Use Docker or GitHub Actions for reproducible builds.

## Format Overview

| Format | Use Case | Auto-Update | Installation |
|--------|----------|-------------|--------------|
| AppImage | Universal, portable | Manual | Run directly |
| Debian | Debian/Ubuntu | Via repos | `dpkg -i` |
| RPM | Fedora/RHEL/openSUSE | Via repos | `rpm -i` |
| Flatpak | Sandboxed, Flathub | Built-in | `flatpak install` |
| Snap | Ubuntu Store | Built-in | `snap install` |
| AUR | Arch Linux | Via helpers | `makepkg -si` |

---

## AppImage

Self-contained executable bundles requiring no installation.

```json
{
  "bundle": {
    "linux": {
      "appimage": {
        "bundleMediaFramework": true,
        "files": { "/usr/share/README.md": "../README.md" }
      }
    }
  }
}
```

| Option | Description |
|--------|-------------|
| `bundleMediaFramework` | Include GStreamer (increases size, licensing concerns with `ugly` plugins) |
| `files` | Additional files (paths must start with `/usr/`) |

```bash
npm run tauri build -- --bundles appimage
```

**ARM**: No cross-compilation support. Use GitHub `ubuntu-22.04-arm` runners.

---

## Debian Packages (.deb)

```json
{
  "bundle": {
    "linux": {
      "deb": {
        "depends": ["libssl3", "libasound2"],
        "files": { "/usr/share/doc/myapp/README": "../README.md" },
        "section": "utils",
        "priority": "optional"
      }
    }
  }
}
```

Default dependencies: `libwebkit2gtk-4.1-0`, `libgtk-3-0`, `libappindicator3-1` (if tray used).

```bash
npm run tauri build -- --bundles deb
```

### ARM Cross-Compilation

```bash
# ARM64
rustup target add aarch64-unknown-linux-gnu
sudo apt install gcc-aarch64-linux-gnu
```

`.cargo/config.toml`:
```toml
[target.aarch64-unknown-linux-gnu]
linker = "aarch64-linux-gnu-gcc"
```

```bash
PKG_CONFIG_SYSROOT_DIR=/usr/aarch64-linux-gnu cargo tauri build --target aarch64-unknown-linux-gnu
```

---

## RPM Packages

```json
{
  "bundle": {
    "linux": {
      "rpm": {
        "depends": ["openssl"],
        "conflicts": ["oldapp"],
        "obsoletes": ["legacyapp < 2.0"],
        "provides": ["myapp-bin"],
        "license": "MIT",
        "preInstallScript": "scripts/pre-install.sh",
        "postInstallScript": "scripts/post-install.sh"
      }
    }
  }
}
```

Scripts receive: `1` (install), `2` (upgrade), `0` (uninstall).

```bash
npm run tauri build -- --bundles rpm
```

### Signing

```bash
gpg --gen-key && gpg --export-secret-keys --armor > private.key
export TAURI_SIGNING_RPM_KEY=$(cat private.key)
export TAURI_SIGNING_RPM_KEY_PASSPHRASE="passphrase"
```

### Debug Commands

```bash
rpm -qip pkg.rpm   # Info
rpm -qlp pkg.rpm   # Files
rpm -qp --scripts pkg.rpm  # Scripts
rpm -Kv pkg.rpm    # Verify signature
```

---

## Flatpak

### Prerequisites

```bash
sudo apt install flatpak flatpak-builder  # Ubuntu/Debian
flatpak install flathub org.gnome.Platform//46 org.gnome.Sdk//46
```

### Manifest (flatpak-builder.yaml)

```yaml
id: com.example.myapp
runtime: org.gnome.Platform
runtime-version: '46'
sdk: org.gnome.Sdk
command: myapp

finish-args:
  - --socket=wayland
  - --socket=fallback-x11
  - --device=dri
  - --share=ipc
  - --share=network
  - --talk-name=org.kde.StatusNotifierWatcher
  - --filesystem=xdg-run/tray-icon:create

modules:
  - name: binary
    buildsystem: simple
    sources:
      - type: file
        path: flatpak.metainfo.xml
      - type: file
        url: https://github.com/user/repo/releases/download/v1.0.0/myapp_1.0.0_amd64.deb
        sha256: <hash>
        only-arches: [x86_64]
    build-commands:
      - mkdir deb-extract && ar -x *.deb --output deb-extract
      - tar -C deb-extract -xf deb-extract/data.tar.gz
      - install -Dm755 deb-extract/usr/bin/myapp /app/bin/myapp
      - sed -i 's/^Icon=.*/Icon=com.example.myapp/' deb-extract/usr/share/applications/myapp.desktop
      - install -Dm644 deb-extract/usr/share/applications/myapp.desktop /app/share/applications/com.example.myapp.desktop
      - install -Dm644 deb-extract/usr/share/icons/hicolor/128x128/apps/myapp.png /app/share/icons/hicolor/128x128/apps/com.example.myapp.png
      - install -Dm644 flatpak.metainfo.xml /app/share/metainfo/com.example.myapp.metainfo.xml
```

### MetaInfo (flatpak.metainfo.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>com.example.myapp</id>
  <name>My App</name>
  <summary>Short description</summary>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>MIT</project_license>
  <description><p>Longer description.</p></description>
  <launchable type="desktop-id">com.example.myapp.desktop</launchable>
  <url type="homepage">https://example.com</url>
  <releases><release version="1.0.0" date="2025-01-01"/></releases>
</component>
```

### Build and Test

```bash
flatpak-builder --force-clean --user --install flatpak flatpak-builder.yaml
flatpak run com.example.myapp
```

### Tray Icon Fix

```rust
TrayIconBuilder::new()
    .icon(app.default_window_icon().unwrap().clone())
    .temp_dir_path(app.path().app_cache_dir().unwrap())
    .build().unwrap();
```

### Flathub Submission

1. Fork https://github.com/flathub/flathub
2. Create branch from `new-pr`, add manifest
3. Open PR, address feedback, receive repo access

---

## Snap Packages

### Prerequisites

```bash
sudo apt install snapd
sudo snap install core22
sudo snap install snapcraft --classic
```

Register app at https://snapcraft.io

### snapcraft.yaml

```yaml
name: myapp
base: core22
version: '1.0.0'
summary: Short description (max 79 chars)
description: Longer description.
grade: stable
confinement: strict

layout:
  /usr/lib/x86_64-linux-gnu/webkit2gtk-4.1:
    bind: $SNAP/usr/lib/x86_64-linux-gnu/webkit2gtk-4.1

apps:
  myapp:
    command: usr/bin/myapp
    desktop: usr/share/applications/myapp.desktop
    extensions: [gnome]
    plugs: [home, network, audio-playback, desktop, wayland, x11, opengl]

parts:
  myapp:
    plugin: nil
    source: .
    build-packages: [nodejs, npm, curl, libwebkit2gtk-4.1-dev, libssl-dev, libayatana-appindicator3-dev]
    stage-packages: [libwebkit2gtk-4.1-0, libayatana-appindicator3-1]
    override-build: |
      curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
      . "$HOME/.cargo/env"
      npm install && npm run tauri build -- --bundles deb
      mkdir -p deb-extract && ar -x src-tauri/target/release/bundle/deb/*.deb --output deb-extract
      tar -C deb-extract -xf deb-extract/data.tar.gz
      cp -r deb-extract/usr $SNAPCRAFT_PART_INSTALL/
```

### Build and Publish

```bash
sudo snapcraft
snap run myapp
snapcraft login && snapcraft upload --release=stable myapp_1.0.0_amd64.snap
```

---

## AUR (Arch User Repository)

### Setup

```bash
# Create account at https://aur.archlinux.org, configure SSH
git clone ssh://aur@aur.archlinux.org/myapp.git
```

### PKGBUILD (Binary)

```bash
pkgname=myapp
pkgver=1.0.0
pkgrel=1
pkgdesc="Description"
arch=('x86_64' 'aarch64')
url="https://github.com/user/myapp"
license=('MIT')
depends=('cairo' 'desktop-file-utils' 'gdk-pixbuf2' 'glib2' 'gtk3' 'hicolor-icon-theme' 'libsoup' 'pango' 'webkit2gtk-4.1')
source_x86_64=("$pkgname-$pkgver.deb::https://github.com/user/myapp/releases/download/v$pkgver/myapp_${pkgver}_amd64.deb")
sha256sums_x86_64=('SKIP')

package() { tar -xf data.tar.gz -C "$pkgdir"; }
```

### PKGBUILD (Source)

```bash
pkgname=myapp
pkgver=1.0.0
pkgrel=1
pkgdesc="Description"
arch=('x86_64')
url="https://github.com/user/myapp"
license=('MIT')
makedepends=('cargo' 'nodejs' 'npm' 'webkit2gtk-4.1' 'base-devel' 'openssl' 'libappindicator-gtk3')
depends=('cairo' 'desktop-file-utils' 'gdk-pixbuf2' 'glib2' 'gtk3' 'hicolor-icon-theme' 'libsoup' 'pango' 'webkit2gtk-4.1')
source=("$pkgname-$pkgver.tar.gz::https://github.com/user/myapp/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() { cd "$pkgname-$pkgver" && npm install && npm run tauri build -- --bundles deb; }
package() { cd "$pkgname-$pkgver" && tar -xf src-tauri/target/release/bundle/deb/*.deb && tar -xf data.tar.gz -C "$pkgdir"; }
```

### Install Script (myapp.install)

```bash
post_install() { update-desktop-database -q; gtk-update-icon-cache -q -t -f usr/share/icons/hicolor; }
post_upgrade() { post_install; }
post_remove() { post_install; }
```

### Submit

```bash
makepkg --printsrcinfo > .SRCINFO
makepkg -si  # Test
git add PKGBUILD .SRCINFO myapp.install && git commit -m "myapp 1.0.0" && git push
```

---

## Environment Variables

GUI apps don't inherit `$PATH`. Use `fix-path-env-rs`:

```toml
[dependencies]
fix-path-env = "0.1"
```

```rust
fn main() {
    fix_path_env::fix();
    tauri::Builder::default().run(tauri::generate_context!()).expect("error");
}
```

---

## GitHub Actions Example

```yaml
name: Build Linux
on: [push]
jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt update && sudo apt install -y libwebkit2gtk-4.1-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - uses: dtolnay/rust-action@stable
      - run: npm install && npm run tauri build -- --bundles deb,rpm,appimage
      - uses: actions/upload-artifact@v4
        with:
          name: linux-bundles
          path: src-tauri/target/release/bundle/**/*
```
