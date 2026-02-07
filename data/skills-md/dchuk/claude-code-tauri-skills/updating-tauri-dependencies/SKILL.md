---
name: updating-tauri-dependencies
description: Assists users with updating Tauri dependencies including the Tauri CLI, Rust crates, JavaScript packages, and checking for outdated versions to upgrade to the latest version.
---

# Updating Tauri Dependencies

This skill provides guidance for updating Tauri dependencies across both the JavaScript and Rust ecosystems.

## Version Synchronization (Critical)

The JavaScript `@tauri-apps/api` package and Rust `tauri` crate must maintain matching minor versions. Adding new features requires upgrading both sides to ensure compatibility.

For Tauri plugins, maintain exact version parity (e.g., both `2.2.1`) for the npm package and cargo crate.

---

## Updating JavaScript Dependencies

### Using npm

Update Tauri CLI and API packages:

```bash
npm install @tauri-apps/cli@latest @tauri-apps/api@latest
```

Check for outdated packages:

```bash
npm outdated @tauri-apps/cli
npm outdated @tauri-apps/api
```

### Using yarn

Update Tauri CLI and API packages:

```bash
yarn up @tauri-apps/cli @tauri-apps/api
```

Check for outdated packages:

```bash
yarn outdated @tauri-apps/cli
yarn outdated @tauri-apps/api
```

### Using pnpm

Update Tauri CLI and API packages:

```bash
pnpm update @tauri-apps/cli @tauri-apps/api --latest
```

Check for outdated packages:

```bash
pnpm outdated @tauri-apps/cli
pnpm outdated @tauri-apps/api
```

---

## Updating Rust Dependencies

### Manual Update

1. Check the latest versions on crates.io:
   - [tauri crate versions](https://crates.io/crates/tauri/versions)
   - [tauri-build crate versions](https://crates.io/crates/tauri-build/versions)

2. Edit `src-tauri/Cargo.toml` and update the version numbers:

```toml
[build-dependencies]
tauri-build = "2.0"

[dependencies]
tauri = { version = "2.0", features = [] }
```

3. Run cargo update from the src-tauri directory:

```bash
cd src-tauri && cargo update
```

### Using cargo-edit (Automatic)

Install cargo-edit if not already installed:

```bash
cargo install cargo-edit
```

Upgrade Tauri dependencies automatically:

```bash
cd src-tauri && cargo upgrade tauri tauri-build
```

---

## Checking for Updates

### Check All Tauri Dependencies

JavaScript packages:

```bash
# npm
npm outdated | grep tauri

# yarn
yarn outdated | grep tauri

# pnpm
pnpm outdated | grep tauri
```

Rust crates:

```bash
cd src-tauri && cargo outdated | grep tauri
```

Note: `cargo outdated` requires the cargo-outdated tool:

```bash
cargo install cargo-outdated
```

---

## Updating Tauri Plugins

When updating Tauri plugins, both the npm package and Rust crate must be updated to the same version.

Example for updating a plugin (e.g., shell plugin):

### JavaScript side

```bash
# npm
npm install @tauri-apps/plugin-shell@latest

# yarn
yarn up @tauri-apps/plugin-shell

# pnpm
pnpm update @tauri-apps/plugin-shell --latest
```

### Rust side

Edit `src-tauri/Cargo.toml`:

```toml
[dependencies]
tauri-plugin-shell = "2.0"
```

Then update:

```bash
cd src-tauri && cargo update
```

---

## Complete Update Workflow

To update all Tauri dependencies in a project:

1. Update JavaScript dependencies:

```bash
# Using npm (adjust for your package manager)
npm install @tauri-apps/cli@latest @tauri-apps/api@latest
```

2. Update any Tauri plugins on the JavaScript side:

```bash
npm install @tauri-apps/plugin-shell@latest @tauri-apps/plugin-fs@latest
# Add other plugins as needed
```

3. Update Rust dependencies in `src-tauri/Cargo.toml`

4. Run cargo update:

```bash
cd src-tauri && cargo update
```

5. Rebuild the project to verify compatibility:

```bash
npm run tauri build
# or
cargo tauri build
```

---

## Troubleshooting

### Version Mismatch Errors

If you encounter version mismatch errors between JavaScript and Rust dependencies:

1. Verify both sides use matching minor versions
2. Check `package.json` for `@tauri-apps/api` version
3. Check `src-tauri/Cargo.toml` for `tauri` crate version
4. Ensure they align (e.g., both at 2.x)

### Cargo Lock Conflicts

If `Cargo.lock` has conflicts after updating:

```bash
cd src-tauri && rm Cargo.lock && cargo update
```

### Plugin Version Mismatch

For plugin version mismatches, ensure exact version parity between npm and cargo versions of the same plugin.
