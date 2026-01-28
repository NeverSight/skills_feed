---
name: preview
description: Start local development server for previewing the site.
allowed-tools: Bash
---

# Start Preview Server

Start the Next.js development server for local preview.

## Steps
1. Check if dependencies are installed:
   ```bash
   [ -d "node_modules" ] || pnpm install
   ```

2. Check if port 3000 is available:
   ```bash
   lsof -i :3000 | grep LISTEN
   ```

3. Start development server:
   ```bash
   pnpm dev
   ```

4. Report the URL: http://localhost:3000

## If Port 3000 is Busy
Suggest alternative:
```bash
pnpm dev -- -p 3001
```

Or kill existing process (with user confirmation):
```bash
kill $(lsof -t -i:3000)
pnpm dev
```

## Docker Alternative
If Docker is preferred:
```bash
docker compose up
```
Server will be available at http://localhost:3000
