---
name: remote-bash
description: Execute bash commands against any public GitHub repository without cloning it locally. Use when the user needs to explore, search, or analyze external repos, check dependency source code, or investigate implementation details in third-party code.
---

# remote-bash

Execute bash commands against any public GitHub repository without cloning it to the local machine.

```bash
npx remote-bash <target> [options] -- <command>
```

## Target formats

| Format | Example | Behavior |
|--------|---------|----------|
| `owner/repo` | `vercel/next.js` | Target the default branch |
| `package-name` | `zod` | Reads version from local lockfile, resolves to repo + exact SHA |

## Options

| Option | Description |
|--------|-------------|
| `-ref <branch\|commit>` | Target a specific branch or commit SHA |
| `-v <version>` | Target a specific version/tag |

## Examples

```bash
# check how next.js exports its cache APIs
npx remote-bash vercel/next.js -- cat packages/next/cache.d.ts

# find all ZodIssueCode types in zod (uses your lockfile version)
npx remote-bash zod -- grep "ZodIssueCode" packages/zod/src/v3/ZodError.ts

# explore three.js module structure
npx remote-bash mrdoob/three.js -- ls src/

# search for cacheLife usage across next.js canary branch
npx remote-bash vercel/next.js -ref canary -- grep -rn "cacheLife" --include="*.ts"

# check a specific three.js release
npx remote-bash mrdoob/three.js -v r150 -- cat src/Three.js
```

## Key Benefits

- **No local clone**: Runs in the cloud, nothing downloaded to your machine
- **Lockfile-aware**: Package names resolve to the exact version you have installed
- **Version pinning**: Explore different branches, commits, or tags with `-ref` and `-v`
