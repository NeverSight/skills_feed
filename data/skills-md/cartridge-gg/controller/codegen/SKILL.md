---
name: codegen
description: Regenerate GraphQL types from API schema. Use when API schema has changed, GraphQL queries/mutations added or modified, or type errors in API calls.
---

# GraphQL Codegen Skill

Regenerate GraphQL types from API schema.

## Usage

Run when:
- API schema has changed
- GraphQL queries/mutations added or modified
- Type errors in API calls

## Steps

1. Run `pnpm --filter @cartridge/keychain codegen`
2. Verify generated types in `packages/keychain/src/utils/api/graphql.ts`
3. Check for any TypeScript errors in files using the API
4. Run `pnpm test` to ensure tests still pass

## Configuration

- Schema source: https://api.cartridge.gg/query
- Config: `packages/keychain/src/utils/api/codegen.yaml`
- Auto-runs during build process

## Notes

- Codegen is also triggered automatically during `pnpm build`
- Generated files should not be manually edited
- Commit generated changes with schema updates
