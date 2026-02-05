---
name: firebase-app-hosting
description: Guide for configuring, deploying, and troubleshooting Firebase App Hosting with Next.js and other frameworks. Use when setting up apphosting.yaml, debugging build/deploy errors, managing environment variables, configuring Cloud Run settings, or adapting projects for App Hosting production environment.
---

# Firebase App Hosting Configuration Guide

This skill provides comprehensive guidance for working with Firebase App Hosting - a modern hosting solution for dynamic web apps with built-in GitHub integration, Cloud Run backend, and Cloud CDN caching.

## When to Use This Skill

Use this skill when:
- Setting up or configuring `apphosting.yaml` for the first time
- Debugging build or deployment failures
- Encountering errors that work in dev but fail in production
- Configuring environment variables and secrets
- Adjusting Cloud Run service settings (CPU, memory, concurrency)
- Converting dependencies between `dependencies` and `devDependencies`
- Optimizing app for App Hosting production environment

## Quick Start Checklist

Before deploying to Firebase App Hosting:

1. **Project Requirements**
   - Firebase project with Blaze (pay-as-you-go) plan
   - GitHub repository connected to Firebase
   - Next.js 13.5.x+ or Angular 18.2.x+ (or community-supported framework)
   - Next.js 15.x is now in active support (as of 2025)
   - Node.js 20+

2. **Essential Files**
   - `apphosting.yaml` in project root
   - `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml` (lock file required)
   - Valid `package.json` with correct dependency classifications

3. **Initial Setup**
   ```bash
   # Initialize apphosting.yaml
   firebase init apphosting
   
   # Create backend
   firebase apphosting:backends:create --project PROJECT_ID
   ```

## Core Configuration Workflow

### Step 1: Create apphosting.yaml

Start with the basic structure. See `assets/apphosting.yaml.template` for a complete working example.

**Minimal configuration:**
```yaml
runConfig:
  cpu: 1
  memoryMiB: 512
  minInstances: 0
  maxInstances: 10

env:
  - variable: NODE_ENV
    value: production
```

**Key sections:**
- `runConfig` - Cloud Run service settings (CPU, memory, scaling)
- `env` - Environment variables and secrets
- `scripts` - Optional build/run command overrides
- `outputFiles` - Optional deploy optimization

For detailed configuration options, see `references/apphosting-yaml-reference.md`.

### Step 2: Configure Environment Variables

**Rules for environment variables:**

1. **Build-time vs Runtime availability:**
   ```yaml
   env:
     # Available in both build and runtime (default)
     - variable: NEXT_PUBLIC_API_URL
       value: https://api.example.com
     
     # Build-time only
     - variable: NEXT_TELEMETRY_DISABLED
       value: "1"
       availability:
         - BUILD
     
     # Runtime only (server-side secrets)
     - variable: DATABASE_URL
       secret: database-url-secret
       availability:
         - RUNTIME
   ```

2. **Next.js public variables:**
   - Prefix with `NEXT_PUBLIC_` for browser access
   - These must be available at BUILD time to be embedded

3. **Secrets management:**
   - Store sensitive data in Cloud Secret Manager
   - Reference secrets in apphosting.yaml (safe for source control)
   - Never set secrets with BUILD availability - this can cause runtime initialization errors

**Common mistake to avoid:**
```yaml
# ❌ WRONG - Admin SDK credentials at BUILD time causes errors
- variable: FIREBASE_PRIVATE_KEY
  value: "..."
  availability:
    - BUILD
    - RUNTIME

# ✅ CORRECT - Admin SDK credentials at RUNTIME only
- variable: FIREBASE_PRIVATE_KEY
  value: "..."
  availability:
    - RUNTIME
```

### Step 3: Validate package.json Dependencies

**Critical distinction:**
- `dependencies` - Required at runtime in production
- `devDependencies` - Only needed during development/build

**Common issues:**

1. **Build tools in wrong section:**
   ```json
   {
     "dependencies": {
       "next": "15.5.6",        // ✅ Needed at runtime
       "react": "^19",          // ✅ Needed at runtime
       "typescript": "^5"       // ❌ Should be devDependency
     },
     "devDependencies": {
       "@types/node": "^20",    // ✅ Build-time only
       "eslint": "^9"           // ✅ Build-time only
     }
   }
   ```

2. **Missing runtime dependencies:**
   If a package is used in production code, it must be in `dependencies`:
   ```json
   {
     "dependencies": {
       "firebase-admin": "^12",     // ✅ Used in API routes
       "stripe": "^14"              // ✅ Used server-side
     }
   }
   ```

For detailed guidance, see `references/package-json-guide.md`.

### Step 4: Deploy and Monitor

```bash
# Push to live branch triggers automatic deployment
git push origin main

# Or manually create rollout
firebase apphosting:rollouts:create BACKEND_ID --project PROJECT_ID

# Monitor deployment
firebase apphosting:backends:get BACKEND_ID --project PROJECT_ID
```

## Common Production Issues

### Issue 1: "Module not found" in Production

**Symptom:** Works locally, fails in App Hosting with module import errors.

**Causes:**
1. Package in `devDependencies` but needed at runtime
2. Missing lock file
3. Case-sensitive imports (Linux production vs case-insensitive dev)

**Solution:**
1. Move package to `dependencies`
2. Ensure lock file exists and is committed
3. Check import statement casing matches actual file names

### Issue 2: Environment Variable Not Available

**Symptom:** `process.env.VARIABLE_NAME` is undefined in production.

**Causes:**
1. Variable not in `apphosting.yaml`
2. Wrong `availability` setting
3. Missing `NEXT_PUBLIC_` prefix for client-side variables

**Solution:**
1. Add to `apphosting.yaml` env section
2. Set correct availability (BUILD, RUNTIME, or both)
3. Use `NEXT_PUBLIC_` prefix for browser-accessible variables

### Issue 3: Firebase Admin SDK Initialization Error

**Symptom:** "Neither apiKey nor config.authenticator" error.

**Cause:** Admin SDK credentials available at BUILD time.

**Solution:** Set credentials to RUNTIME only:
```yaml
env:
  - variable: FIREBASE_CLIENT_EMAIL
    value: "..."
    availability:
      - RUNTIME
  
  - variable: FIREBASE_PRIVATE_KEY
    value: "..."
    availability:
      - RUNTIME
```

### Issue 4: Build Succeeds but Deploy Fails

**Symptom:** Cloud Build completes, but Cloud Run deployment fails.

**Common causes:**
1. Port binding issues (App Hosting manages PORT automatically)
2. Health check failures
3. Memory/CPU limits too low

**Solution:**
1. Don't override PORT in your app
2. Increase `memoryMiB` and/or `cpu` in runConfig
3. Check Cloud Run logs for specific errors

For comprehensive troubleshooting, see `references/common-errors.md`.

## Framework-Specific Guidance

### Next.js Configuration

See `references/nextjs-specific.md` for detailed Next.js guidance including:
- Image optimization setup
- Middleware caching considerations
- Server actions configuration
- Parallel routing limitations

**Key Next.js tips:**
1. Use App Router (recommended) or Pages Router
2. Don't override default build command unless necessary
3. Image optimization requires explicit configuration
4. Middleware may affect caching

### Angular Configuration

- Angular 18.2.x+ supported
- Use Application builder
- SSR pages work with proper configuration
- Limited i18n support (check limitations)

## Advanced Configuration

### Cloud Run Service Tuning

Adjust performance and cost with `runConfig`:

```yaml
runConfig:
  # Processing power
  cpu: 2                    # 0-8 CPUs
  memoryMiB: 2048          # 128-32768 MiB
  
  # Scaling behavior
  minInstances: 0          # Minimum always-on instances
  maxInstances: 100        # Maximum instances
  concurrency: 80          # Requests per instance
```

**Memory/CPU relationship:**
- **1 vCPU**: Up to 4 GiB (4096 MiB)
- **2 vCPU**: Up to 8 GiB (8192 MiB)
- **4 vCPU**: 2 GiB to 16 GiB (minimum 2 GiB required)
- **6 vCPU**: 4 GiB to 24 GiB (minimum 4 GiB required)
- **8 vCPU**: 4 GiB to 32 GiB (minimum 4 GiB required)

**Important:** Higher memory allocations require higher CPU counts:
- Over 4 GiB → requires 2+ vCPUs
- Over 8 GiB → requires 4+ vCPUs
- Over 16 GiB → requires 6+ vCPUs
- Over 24 GiB → requires 8 vCPUs

### VPC Network Access

Connect to private resources:

```yaml
runConfig:
  vpcAccess:
    egress: PRIVATE_RANGES_ONLY
    networkInterfaces:
      - network: my-network-id
        subnetwork: my-subnetwork-id
```

### Build Command Override

Only override if framework adapters don't work:

```yaml
scripts:
  buildCommand: next build --no-lint
  runCommand: node dist/index.js
```

**Warning:** Overriding disables framework-specific optimizations.

## Resources Reference

### Templates
- `assets/apphosting.yaml.template` - Complete working configuration example

### Detailed Documentation
- `references/apphosting-yaml-reference.md` - All apphosting.yaml options
- `references/common-errors.md` - Troubleshooting guide with solutions
- `references/nextjs-specific.md` - Next.js-specific configuration
- `references/package-json-guide.md` - Dependency management guide

## Best Practices

1. **Start minimal** - Begin with basic config, add complexity as needed
2. **Test locally** - Use App Hosting emulator before deploying
   ```bash
   firebase emulators:start --only apphosting
   # Uses apphosting.emulator.yaml for local overrides
   # Your app runs with same environment variables as production
   ```
3. **Version control** - Commit apphosting.yaml (safe with secrets as references)
4. **Monitor builds** - Check Firebase console for build/deploy status
5. **Iterate carefully** - Make one change at a time when debugging
6. **Use secrets** - Store sensitive data in Cloud Secret Manager
7. **Review dependencies** - Ensure correct classification in package.json
8. **Check lock files** - Always commit your package manager's lock file

## Getting Help

If issues persist after following this guide:
1. Check `references/common-errors.md` for your specific error
2. Review Cloud Build logs in Firebase console
3. Check Cloud Run logs for runtime errors
4. Verify all dependencies are correctly classified
5. Ensure lock file is present and up to date
