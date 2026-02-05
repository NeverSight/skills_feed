---
name: clean-build
description: Clean all build artifacts and rebuild from scratch. Use when experiencing stale build artifacts, Turbo cache issues, mysterious build failures, or after dependency updates.
---

# Clean Build Skill

Clean all build artifacts and rebuild from scratch.

## Usage

Use when experiencing:
- Stale build artifacts
- Turbo cache issues
- Mysterious build failures
- After dependency updates

## Steps

1. Run `pnpm clean` to remove build artifacts and prune store
2. Reinstall dependencies with `pnpm i`
3. Run `pnpm build` to rebuild all packages
4. Verify build success
5. Optional: Run tests to ensure everything works

## Notes

- Turbo uses aggressive caching - clean build resolves most cache issues
- WASM dependencies (controller-wasm, session-wasm) rebuilt automatically
- GraphQL codegen runs automatically during keychain build
