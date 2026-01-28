---
name: pnpm-dependency-analysis
description: Analyze package usage, resolved versions, direct/transitive dependencies, workspace interdependencies, and blast radius in pnpm monorepos. Perfect for Dependabot PR triage, upgrades, security reviews, and version conflict debugging.
---

# pnpm Dependency Analysis Skill (Fusion Framework)

Helps answer:
- Where is `PACKAGE` used (direct & transitive)?
- What real versions are resolved across workspaces?
- Which workspaces depend on each other (forward/reverse graph)?
- What's the blast radius / risk level for an upgrade or patch?

All commands run from the **root** of the repository.
Replace `PACKAGE` with the real name (e.g., `lodash`, `zod`, `@tanstack/react-query`, `eslint`).

## 1. Core: Where is this package used?

### Direct usages only (fastest & cleanest)

```bash
pnpm why PACKAGE --recursive --depth=0
```

Shows only workspaces that list `PACKAGE` in `dependencies`, `devDependencies`, `peerDependencies`, or `optionalDependencies`.

### Full dependency tree (transitive paths)

```bash
pnpm why PACKAGE --recursive --long
```

Shows how `PACKAGE` gets pulled in indirectly through other dependencies.

### Resolved versions per workspace (critical for upgrades)

```bash
pnpm why PACKAGE --recursive --json \
  | jq -r '.[] | "\(.workspace)\t→ \(.version)\t\(.dependencyType // "unknown")\t\(.from // "-")"'
```

**Why this matters:**
- See all versions resolved across workspaces (handles overrides, workspace:*, catalog)
- Identify version inconsistencies or conflicts
- Understand if workspace protocol controls the version

## 2. Workspace → Workspace Dependency Graph

### Which workspaces depend on each other (direct only)

```bash
pnpm recursive list --depth=0 --json --only-projects \
  | jq 'to_entries[]
      | {from: .key, to: (.value.dependencies // {} | keys + (.value.devDependencies // {} | keys) + (.value.peerDependencies // {} | keys))}
      | select(.to | length > 0)'
```

Shows the project-level dependency structure (e.g., which @equinor/fusion-framework-* packages depend on others).

### Generate Mermaid-compatible edges (paste into GitHub PR/comments)

```bash
pnpm -r exec -- jq -r 'select(.dependencies != null or .devDependencies != null or .peerDependencies != null)
  | .name as $self
  | (.dependencies // {} | keys) + (.devDependencies // {} | keys) + (.peerDependencies // {} | keys)
  | .[] as $dep
  | "\($self) --> \($dep)"' | sort | uniq
```

Example Mermaid output (copy the edges into a code block with ` ```mermaid `):
```
graph LR
  @equinor/fusion-framework-cli --> @equinor/fusion-framework-utils
  @equinor/fusion-framework-react --> @equinor/fusion-framework-core
  @equinor/fusion-framework-react --> @equinor/fusion-framework-utils
```

Paste into GitHub issue, PR description, or [mermaid.live](https://mermaid.live) for interactive view.

## 3. One-liner investigation report

```bash
PACKAGE=some-package

echo "=== Direct usages ==="
pnpm why "$PACKAGE" --recursive --depth=0

echo -e "\n=== Resolved versions ==="
pnpm why "$PACKAGE" --recursive --json \
  | jq -r '.[] | "\(.workspace)\t→ \(.version)\t\(.dependencyType)"'

echo -e "\n=== package.json mentions ==="
grep -rl "$PACKAGE" packages/ apps/ || echo "None"

echo -e "\n=== Config/tooling mentions (eslint/vite/vitest/storybook/etc) ==="
find . -type f \( -name 'eslint.*' -o -name 'vite.*' -o -name 'vitest.*' \
  -o -name 'playwright.*' -o -name 'storybook.*' -o -name 'tsconfig*.json' \
  -o -name 'next.config.*' \) \
  -exec grep -l "$PACKAGE" {} \; | grep -vE 'node_modules|dist|build|.turbo|.cache' || echo "None"
```

Produces a clean summary of where the package appears across the monorepo.

## 4. Risk / Blast Radius Reference Table

| Indicator | Risk Level | Notes |
|-----------|-----------|-------|
| 1–2 workspaces only | Low | Limited scope |
| ≥ 6–8 workspaces | High | Widespread impact |
| Only in `devDependencies` | Lower | Unless tooling: eslint, typescript, vite, vitest, jest, rollup, playwright, storybook |
| Uses `workspace:*` or `workspace:^x.y.z` | Very Low | Controlled at workspace root |
| Many different resolved versions | Medium | May need `pnpm.overrides` or `.npmrc` resolutions |
| Hub node (many packages → it) | High | Core shared dependency |
| Deep/long chains in `pnpm why` | Medium–High | Transitive dependency risks |
| Appears in multiple config files | Medium | Tooling change affects lint/format/build |

## 5. Narrowing search with `--filter`

Scope down large investigations by focusing on specific package groups:

```bash
# Only check /packages/* (not cookbooks, etc)
pnpm why PACKAGE --recursive --filter="./packages/*"

# Only check /apps/* 
pnpm why PACKAGE --recursive --filter="./apps/*"

# Only check React packages
pnpm why PACKAGE --recursive --filter="@equinor/fusion-framework-react"
```

## Tips & Notes

- **Prerequisites**: `jq` (recommended, for JSON parsing). Built-in tools (`grep`, `find`) are used for file searches
- **Faster searches**: Install `rg` (ripgrep) to speed up searches: `brew install ripgrep` (optional, not required)
- **Mermaid visualization**: If you have many edges, ask Copilot to clean up the output or use [mermaid.live](https://mermaid.live) with an interactive filter
- **Interactive workspace graph**: `pnpm install -g pnpm-workspace-graph` → run `pnpm-workspace-graph` to open an interactive browser view
- **For Dependabot PRs**: Run this skill *before* merging to gauge impact and gather context for your review
- **Pair with other skills**: Combine with security-audit, changelog-lookup, or version-compatibility checks for full triage

## Common Dependabot Scenarios

### "Should I merge this React upgrade?"
1. Run: `pnpm why @latest/react --recursive --depth=0`
2. Check if versions are consistent across workspaces
3. Look at `packages/react/` CHANGELOG for breaking changes
4. If only in `devDependencies` or 1–2 packages, lower risk

### "Can I upgrade this shared utility?"
1. Run: `pnpm why @equinor/fusion-framework-utils --recursive`
2. Count affected workspaces
3. Check if workspace protocol is used (`workspace:*`)
4. If yes and ≤3 packages depend on it: safe
5. If no and >5 packages: run tests before merge

### "What about this obscure transitive dep?"
1. Run: `pnpm why some-obscure-package --recursive --long`
2. Look at `(.from)` field to see which package pulled it in
3. Check if it appears in only one place in the tree
4. If it's behind a single package, upgrading that package is safe

---

For questions or improvements: Refer to [pnpm docs](https://pnpm.io/cli/why) or the Fusion Framework contributing guide.
