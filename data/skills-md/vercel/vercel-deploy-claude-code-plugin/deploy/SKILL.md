---
name: deploy
description: Deploy applications to Vercel. Use when the user says "deploy", "deploy to Vercel", "push to production", "deploy my app", or "go live".
---

# Deploy to Vercel

## Prerequisites Check

```bash
vercel --version
vercel whoami
```

If not installed: `npm install -g vercel`
If not logged in: `vercel login`

## Deployment

**Production:**
```bash
vercel --prod
```

**Preview:**
```bash
vercel
```

## After Deployment

- Display the deployment URL
- Show build status
- Mention `vercel logs <url>` for debugging if needed
