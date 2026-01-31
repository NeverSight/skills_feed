---
name: fullstack-dev
description: Full-stack development context for coordinating changes across contracts and frontend. Use this skill when changes span both backend contracts and frontend code, requiring synchronized updates across the stack.
---

# Full-Stack Development

Context for coordinating changes across contracts, frontend, and shared packages.

## When This Skill Activates

- Changes spanning contracts AND frontend
- SDK or shared type updates
- Deployment artifact synchronization
- ABI changes affecting frontend
- End-to-end feature implementation

## Scope

- Smart contracts (Solidity, Anchor)
- Frontend applications (React, Next.js)
- Shared SDKs and type packages
- Deployment configurations

## Key Practices

1. **Coordinate changes** across contracts and frontend
2. **Update SDK** when contract interfaces change
3. Run **both** contract tests AND frontend build
4. Sync deployment artifacts after contract changes

## Configuration Guidelines

- Use config files for all UI text and constants
- Never hardcode strings in components
- Validate configs before build

## File Naming & Versioning

- **Canonical Names Only**: Use `Market.sol`, NOT `MarketV10.sol`
- **Single Active Version**: Never keep `V1.ts` and `V2.ts` side-by-side
- **Archiving**: Move old code to `archive/` or trust Git history

## Common Workflows

### After Contract Changes

```bash
# Build and test contracts
forge build && forge test

# Sync ABIs to frontend
./sync-deployments.sh  # or equivalent

# Rebuild frontend
cd apps/web && npm run build
```

### After Frontend Changes

```bash
cd apps/web
npm run build
npm run dev
```

### Full Build

```bash
pnpm install
pnpm build
```

## Key Integration Points

- **SDK package** - ABIs exported from contracts
- **Deployment configs** - Contract addresses per chain
- **Shared types** - TypeScript types matching contract structs

## Sync Checklist

After contract changes:
- [ ] ABIs regenerated
- [ ] Frontend config updated
- [ ] Types regenerated
- [ ] Frontend builds successfully
- [ ] E2E tests pass

## Related Skills

- `solidity-dev` - Contract development, gas optimization, security scanning
- `frontend-dev` - UI implementation and styling
