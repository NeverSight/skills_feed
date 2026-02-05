---
name: port-manager
description: Helper for agents to check ports before starting dev servers and avoid unnecessary restarts
---

# port-manager

A helper skill for agents to intelligently manage ports when starting development servers. Avoid unnecessary restarts by checking if the server is already running.

## When to use

ALWAYS refer to this skill when the user asks to:
- start the dev server / development server
- run the dev server / development server
- start the server / run the server
- start the app / run the app
- execute npm run dev / pnpm dev / yarn dev
- execute npm run start / pnpm start / yarn start
- execute vite / next dev / nuxt dev
- 개발서버 실행 / 개발 서버 시작
- 서버 시작 / 실행

Also refer when:
- About to execute any command that binds to a port
- Encountering "port already in use" error

## Instructions

### Before Starting Dev Server

When the user asks to start a dev server, ALWAYS check the port first:

1. **Identify the project's port**
   - Check package.json scripts (dev, start)
   - Check framework config files (vite.config, next.config, etc.)
   - Common ports: Next.js 3000, Vite 5173, CRA 3000, Django 8000, Rails 3000

2. **Check if the port is already occupied**
   ```bash
   lsof -i :<port>
   ```

3. **Handle the result**

   If port is **FREE**:
   - Start the dev server
   - Confirm success with URL (e.g., "✓ Server running at http://localhost:3000")

   If port is occupied by **SAME PROJECT**:
   - Skip starting, inform user: "✓ [Project] dev server is already running at http://localhost:3000"
   - Do NOT start another instance

   If port is occupied by **DIFFERENT PROCESS**:
   - Ask user: "⚠️ Port 3000 is occupied by [process details]. Options:
     1. Kill it and start [project] server
     2. Skip and keep existing
     What would you prefer?"

## Platform Notes

**macOS/Linux/WSL:**
- Check port: `lsof -i :<port>`
- Kill process: `kill -9 <PID>`

**Windows native:**
- Check port: `netstat -ano | findstr :<port>`
- Kill process: `taskkill /PID <PID> /F`
