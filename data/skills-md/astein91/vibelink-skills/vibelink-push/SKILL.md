---
name: vibelink-push
description: Share your current project via Vibelink. Analyzes your project, creates metadata, zips it up (excluding node_modules, .git, etc.), and uploads to vibelink.to. Returns a shareable link anyone can open in Claude Code.
---

# /vibelink-push

Share the current project via Vibelink.

## What this skill does

1. Analyzes the project to detect name, description, and technologies
2. Detects if this is a remix of another vibelink project
3. Starts the dev server (if applicable)
4. Takes a screenshot of the running app (if browser tools available)
5. Creates or updates `vibelink.json` metadata
6. Zips the project (excluding node_modules, .git, etc.)
7. Uploads to vibelink.to
8. Returns the shareable link

## Instructions

When the user runs `/vibelink-push`, follow these steps:

### Step 1: Analyze the project

Look for these files to understand the project:
- `package.json` - for name, description, dependencies
- `README.md` - for description
- `vibelink.json` - existing metadata (if any)
- Source files - to detect technologies

Detect technologies by looking at:
- Dependencies in package.json (React, Vue, Svelte, etc.)
- File extensions (.ts, .tsx, .py, .rs, etc.)
- Config files (tailwind.config.js, vite.config.ts, etc.)

### Step 2: Check for existing vibelink.json and detect remixes

Check if `vibelink.json` exists and examine it:

**Case A: No vibelink.json exists**
- This is a new project
- Generate a new projectId
- Ask user for name, description, author

**Case B: vibelink.json exists with NO `forkedFrom` field**
- This is the original project being updated
- Keep the same projectId
- Update metadata if needed

**Case C: vibelink.json exists WITH a `forkedFrom` field, but same author**
- This is the user's own remix being updated
- Keep the same projectId
- Update metadata if needed

**Case D: vibelink.json exists and project is in ~/vibelinks/ directory**
- This was downloaded from vibelink - it's a remix!
- MUST generate a NEW projectId (never overwrite someone else's project)
- Set `forkedFrom` to the original projectId
- Ask user: "This looks like a remix of {originalName}. What do you want to call your version?"
- Suggest a name like "{originalName} Remix" or let them choose

### Step 3: Check for existing project ID

**For NEW projects:**
- Do NOT generate a project ID - the server will generate one
- The server returns the generated ID in the response

**For UPDATES (when vibelink.json already has a projectId and you have a saved token):**
- Use the existing projectId from vibelink.json
- Include the saved author token

### Step 4: Try to capture a preview screenshot

If browser automation tools (mcp__claude-in-chrome__*) are available:

1. Detect the dev server command and port from package.json scripts or common patterns
2. Start the dev server in the background
3. Wait for it to be ready (check if port is listening)
4. Navigate to localhost:{port} using mcp__claude-in-chrome__navigate
5. Take a screenshot using mcp__claude-in-chrome__computer with action: "screenshot"
6. Save the screenshot to `./vibelink-preview.png`
7. Stop the dev server

If browser tools are not available or the app can't be started, skip this step.

### Step 5: Create the zip

Create a zip file excluding:
- `node_modules/`
- `.git/`
- `dist/`
- `build/`
- `.next/`
- `__pycache__/`
- `*.pyc`
- `.env` (but include `.env.example` if it exists)
- `.DS_Store`
- `vibelink-upload.zip` (previous upload)

Use: `zip -r vibelink-upload.zip . -x "node_modules/*" -x ".git/*" ...`

### Step 6: Upload to vibelink.to

**Determine if this is a NEW project or UPDATE:**

Check if vibelink.json has a `projectId` AND you have a saved token in `~/.vibelink-tokens/{projectId}`:
- If BOTH exist: this is an UPDATE
- Otherwise: this is a NEW project

**Upload the project using curl:**

For NEW projects (server generates the ID):
```bash
curl -X POST https://vibelink.to/upload \
  -F "metadata=@vibelink.json" \
  -F "zip=@vibelink-upload.zip" \
  -F "preview=@vibelink-preview.png"  # only if preview exists
```

For UPDATES (include projectId and authorToken):
```bash
curl -X POST https://vibelink.to/upload \
  -F "projectId={projectId}" \
  -F "authorToken={token}" \
  -F "metadata=@vibelink.json" \
  -F "zip=@vibelink-upload.zip" \
  -F "preview=@vibelink-preview.png"  # only if preview exists
```

**Handle the response:**

The response JSON includes:
- `projectId`: The project's ID (server-generated for new projects)
- `url`: The shareable URL
- `isUpdate`: Whether this was an update
- `authorToken`: (Only for new projects) Save this!

On success (200):
1. Parse the JSON response to get the `projectId`
2. If response contains `authorToken`:
   - Create tokens directory: `mkdir -p ~/.vibelink-tokens`
   - Save token: `echo "{token}" > ~/.vibelink-tokens/{projectId}`
   - Update vibelink.json with the server-generated `projectId`
3. Display the shareable link

Error responses:
- 403 Forbidden: Invalid or missing author token for update
- 404 Not Found: Trying to update a project that doesn't exist
- 413 Payload Too Large: Project exceeds 100MB limit
- 429 Rate Limited: Exceeded 100MB/hour upload limit

**On successful upload, display:**

For NEW projects:
```
✅ Uploaded to Vibelink!

Project: {name}
{Remixed from: {originalName} - if applicable}

🔗 https://vibelink.to/{projectId}

Share this link - anyone can open it in Claude Code!

🔑 Your author token has been saved to ~/.vibelink-tokens/{projectId}
   You'll need this token to update your project later.
```

For UPDATES:
```
✅ Updated on Vibelink!

Project: {name}

🔗 https://vibelink.to/{projectId}
```

### Step 7: Clean up

Optionally remove the zip file after successful upload (keep vibelink.json).

## Example vibelink.json - New project

```json
{
  "name": "Weather Dashboard",
  "description": "A real-time weather dashboard with beautiful visualizations",
  "author": "alexstein",
  "projectId": "weather-dashboard-x7k2",
  "technologies": ["React", "TypeScript", "Tailwind CSS", "OpenWeather API"],
  "preview": {
    "type": "image",
    "src": "./vibelink-preview.png"
  }
}
```

## Example vibelink.json - Remix

```json
{
  "name": "Weather Dashboard Dark Mode",
  "description": "Added dark mode and hourly forecasts to the weather dashboard",
  "author": "friendname",
  "projectId": "weather-dashboard-dark-k9p2",
  "forkedFrom": "weather-dashboard-x7k2",
  "technologies": ["React", "TypeScript", "Tailwind CSS", "OpenWeather API"],
  "preview": {
    "type": "image",
    "src": "./vibelink-preview.png"
  }
}
```

## Important notes

- Always ask for confirmation before uploading
- Don't include sensitive files (.env, credentials, etc.)
- NEVER overwrite someone else's project - always create a new ID for remixes
- If the project is in ~/vibelinks/, it was downloaded and is definitely a remix
- Give credit by setting `forkedFrom` when remixing
- Author tokens are stored in `~/.vibelink-tokens/` - these are needed to update projects
- If you lose your author token, you cannot update that project (create a new one instead)

## Limits

**Per-project size limit: 100MB**

Vibelink is for small vibe-coded projects, not large repositories.

After creating the zip, check its size:
```bash
du -h vibelink-upload.zip
```

- **Under 100MB**: Good to go!
- **Over 100MB**: Stop and warn the user. Suggest:
  - Make sure node_modules, .git, dist, build are excluded
  - Remove large assets (videos, large images)
  - Consider if this project is too big for vibelink

**Rate limit: 100MB per hour per user**

Users can upload up to 100MB total per hour. If rate limited, they'll need to wait before uploading more.
