---
name: pub-package-explorer
description: Find and read source code for Dart or Flutter package dependencies installed in a project. Use when asked to inspect code from a package on pub.dev, trace implementation details in dependencies, or locate package files from package names by resolving `.dart_tool/package_config.json`.
---

# Pub Package Explorer

Use this workflow to read source code for a dependency package in a Dart or Flutter project.

## Resolve a Package Source Path

1. Confirm the project contains `.dart_tool/package_config.json`.
2. Read the package entry from `packages[]` by `name`.
3. Extract:
- `rootUri` (package root, usually in pub cache)
- `packageUri` (usually `lib/`)
4. Build source path as `rootUri + packageUri`.
5. Convert `file://` URI to a filesystem path before reading files.

Use this command pattern:

```bash
PACKAGE="analyzer"
CONFIG=".dart_tool/package_config.json"

SOURCE_URI="$(jq -r --arg pkg "$PACKAGE" '
  .packages[]
  | select(.name == $pkg)
  | (.rootUri + (if (.rootUri | endswith("/")) then "" else "/" end) + .packageUri)
' "$CONFIG")"
```

Convert the URI to a local path:

```bash
SOURCE_PATH="$(printf '%s\n' "$SOURCE_URI" | sed 's#^file://##')"
```

Then inspect source files under that directory (`rg`, `ls`, `cat`).

## Useful Variants

- Return only the package root:

```bash
jq -r --arg pkg "$PACKAGE" '
  .packages[]
  | select(.name == $pkg)
  | .rootUri
' .dart_tool/package_config.json
```

- Return both root and package URI:

```bash
jq -r --arg pkg "$PACKAGE" '
  .packages[]
  | select(.name == $pkg)
  | "\(.rootUri)\t\(.packageUri)"
' .dart_tool/package_config.json
```

## Verification and Error Handling

- If no package matches, stop and report that the package is not in `package_config.json`.
- If `.dart_tool/package_config.json` is missing, run dependency resolution first (`dart pub get` or `flutter pub get`) and retry.
- Prefer reading from `rootUri + packageUri` because package APIs are exposed from that subpath, not always from the package root.
