---
name: package-filter
description: Run commands in specific workspace packages using pnpm filters. Use to execute commands in specific packages within the monorepo.
---

# Package Filter Skill

Run commands in specific workspace packages using pnpm filters.

## Usage

Execute commands in specific packages within the monorepo.

## Common Filters

- `@cartridge/controller` - Main SDK package
- `@cartridge/keychain` - Keychain UI application
- `@cartridge/connector` - Connector package
- `@cartridge/profile` - Profile application

## Examples

```bash
# Run tests in specific package
pnpm --filter @cartridge/keychain test

# Build specific package
pnpm --filter @cartridge/controller build

# Run dev server for keychain only
pnpm --filter @cartridge/keychain dev

# Install dependency to specific package
pnpm --filter @cartridge/controller add <package-name>
```

## Steps

1. Identify target package
2. Use `pnpm --filter <package-name> <command>`
3. Verify command execution in correct package

## Notes

- Workspace dependencies automatically linked
- Filter by package name (with @scope) not directory path
- Use `pnpm -r` for recursive commands across all packages
