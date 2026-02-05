---
name: logs
description: View Vercel deployment logs. Use when the user says "show logs", "check logs", "vercel logs", or "what went wrong with the deployment".
---

# Vercel Logs

## List Deployments

```bash
vercel ls
```

## View Logs

```bash
vercel logs <deployment-url>
```

**Follow logs in real-time:**
```bash
vercel logs <deployment-url> --follow
```

## Analyze

- Look for errors or warnings
- Check for failed function invocations
- Identify build failures
