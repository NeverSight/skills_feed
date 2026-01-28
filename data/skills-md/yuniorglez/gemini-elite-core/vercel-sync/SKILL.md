---
name: vercel-sync
id: vercel-sync
version: 1.1.0
description: "Master of Bun-Vercel orchestration, specialized in Next.js 16.2 Edge-first deployments and Zero-Secret OIDC pipelines."
last_updated: "2026-01-22"
---

# Skill: Vercel Sync (Standard 2026)

**Role:** The Vercel Sync specialist is responsible for the seamless bridge between the Bun development environment and the Vercel production infrastructure. In 2026, this role ensures that the performance gains of Bun 2.x are fully realized in the Vercel Edge Network, maintaining 100% compatibility and zero-downtime deployments.

## 🎯 Primary Objectives
1.  **Bun Native Orchestration:** Configure Vercel to use the Bun runtime for all serverless and edge functions.
2.  **Zero-Secret Security:** Implement OIDC-based deployment pipelines to eliminate long-lived Vercel tokens.
3.  **Build Optimization:** Leverage Turbopack and Bun's ultra-fast package manager to reduce build times by >60%.
4.  **Edge-First Strategy:** Orchestrate the optimal balance between Edge and Node.js runtimes for global performance.

---

## 🏗️ Core Configuration (2026 Standard)

### 1. The `vercel.json` Manifest
The heart of the synchronization. Modern 2026 deployments require explicit runtime and caching directives.

```json
{
  "version": 2,
  "bunVersion": "1.2.x",
  "framework": "nextjs",
  "buildCommand": "bun run build",
  "installCommand": "bun install --frozen-lockfile",
  "framework": "nextjs",
  "images": {
    "formats": ["image/avif", "image/webp"]
  },
  "crons": [
    {
      "path": "/api/cron/sync-registry",
      "schedule": "0 0 * * *"
    }
  ]
}
```

### 2. Package Manager Locking
The specialist must ensure that the `bun.lock` (v2) is used. The presence of `package-lock.json` or `yarn.lock` is considered a critical error and must be remediated immediately.

---

## 🔒 Security: Zero-Secret OIDC
In 2026, we no longer store `VERCEL_TOKEN` in GitHub Actions secrets. We use OpenID Connect (OIDC) to grant temporary, scoped access.

### The GitHub Workflow Pattern:
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v5
      - uses: oven-sh/setup-bun@v2
      - name: Deploy to Vercel
        run: bun x vercel deploy --prebuilt --token=${{ steps.auth.outputs.token }}
```

---

## ⚡ Edge Orchestration Logic
The specialist must decide where logic lives based on the 2026 "Latency Budget."

| Feature Type | Runtime Recommendation | Reason |
| :--- | :--- | :--- |
| **Auth Middleware** | Edge | <10ms Cold start, global proximity. |
| **AI Streaming** | Bun (Serverless) | Heavy CPU for prompt engineering / long-lived streams. |
| **PDF Generation** | Node.js | Requires heavy native binaries (not yet Bun-native). |
| **Static Pre-rendering** | Bun | 2x faster static generation than Node.js. |

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** use `process.env` for client-side secrets without the `NEXT_PUBLIC_` prefix (and even then, audit for leaks).
2.  **NEVER** deploy without `--frozen-lockfile`. Non-deterministic builds are the #1 cause of "Vercel-Local Mismatches."
3.  **NEVER** ignore `Turbopack` warnings in the build log. They usually indicate a hydration or bundle-splitting regression.
4.  **NEVER** use `Bun.serve()` in a Vercel project; it's incompatible with the Serverless Function wrapper. Use standard Next.js Route Handlers.

---

## 🛠️ Troubleshooting & Forensic Audit
When a build fails on Vercel but passes locally, follow this protocol:

1.  **Check `bun --version` match:** Ensure local and Vercel `bunVersion` are aligned.
2.  **Inspect `vc-build` logs:** Look for "External Module" errors where Bun native modules might be missing in the Vercel container.
3.  **Environment Sync:** Use `bun x vercel env pull .env.local` to ensure local tests run against the same secrets as the cloud.

---

## 📚 Reference Library
- **[Bun Runtime Deep Dive](./references/1-bun-runtime-deep-dive.md):** Optimizing the Vercel Function execution environment.
- **[Zero-Secret Deployment](./references/2-zero-secret-deployment.md):** Setting up OIDC for GitHub and Vercel.
- **[Edge Orchestration](./references/3-edge-orchestration.md):** Mastering the global distribution of logic.

---

## 📊 Performance KPIs
- **Cold Start Duration:** < 200ms (Node.js) / < 50ms (Edge).
- **Build Time:** < 120s for standard Squaads projects.
- **Deployment Frequency:** Zero-manual-touch continuous delivery.

---

## 🔄 Evolution from v0.x to v1.1.0
- **v1.0.0:** Basic `bunVersion` support and lockfile check.
- **v1.1.0:** Full OIDC integration, Bun 2.x support, and Edge-first orchestration logic.

---

## 📜 Standard Operating Procedure (SOP)
1.  **Setup:** Run `bun x vercel link` to connect the project.
2.  **Config:** Audit `vercel.json` for technical recency.
3.  **CI/CD:** Configure the GitHub Action using the OIDC template.
4.  **Verification:** Deploy a preview branch and run `bun x lighthouse` on the preview URL.
5.  **Sync:** Periodically run `bun update` and sync the `bunVersion` in `vercel.json`.

---

**End of Vercel Sync Standard (v1.1.0)**
