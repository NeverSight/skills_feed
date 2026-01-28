---
name: pattern-deploy
description: Deploy patterns and test with CLI
user-invocable: false
---

# Deploy Phase

Use `Skill("ct")` for comprehensive ct CLI documentation.

## Read First
- `docs/development/LOCAL_DEV_SERVERS.md` - Local dev setup
- `docs/common/workflows/development.md` - Workflow commands

## Find Identity Key
```bash
ls -la *.key 2>/dev/null || ls -la ~/.claude/*.key 2>/dev/null || find . -name "*.key" -maxdepth 2 2>/dev/null
```

## Commands

**Check syntax without deploying:**
```bash
deno task ct check pattern.tsx --no-run
```

**Deploy new pattern:**
```bash
deno task ct charm new packages/patterns/[name]/main.tsx --identity PATH_TO_KEY
```

**Inspect charm state:**
```bash
deno task ct charm inspect
```

**Update deployed pattern:**
```bash
deno task ct charm setsrc packages/patterns/[name]/main.tsx
```

**Test handler via CLI:**
```bash
deno task ct charm call handlerName --charm CHARM_ID
```

## Get Help
```bash
deno task ct --help
deno task ct charm --help
```

## Done When
- Charm deploys without errors
- State inspects correctly
- Handlers respond to CLI calls
