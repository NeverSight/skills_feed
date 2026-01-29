---
name: demo
description: |
  Automatically generate screen recordings with AI narration to demonstrate PR changes.
  Use this skill when you need to create a demo video showing UI changes from a pull request.
  Triggers: /demo, demo video, PR demo, screen recording, show changes, demonstrate PR
---

# /demo - PR Demo Video Generator

Generate screen recordings with AI narration to demonstrate your PR changes.

## How to Execute /demo

Follow these steps in order. You (Claude) generate the test and narration directly - no templates needed.

### Step 1: Check Prerequisites

```bash
npx tsx lib/cli.ts check-prereqs
```

Returns JSON with status for:
- `devServer`: Whether the dev server is responding
- `ffmpeg`: Whether ffmpeg is installed (needed for video composition)
- `elevenLabsKey`: Whether ELEVEN_LABS_API_KEY is set (optional, for narration)

If `devServer` is false, ask the user to start their dev server first.

### Step 2: Analyze the Diff

```bash
npx tsx lib/cli.ts analyze-diff --staged
```

Or for specific commits:
```bash
npx tsx lib/cli.ts analyze-diff --commits=HEAD~3..HEAD
```

Returns JSON with:
- `uiRelevant`: Whether changes affect UI
- `suggestedRoute`: Route to navigate to
- `changedComponents`: Component names that changed
- `suggestedActions`: What to demonstrate

If `uiRelevant` is false, inform the user and stop.

### Step 3: Discover Playwright Setup (For Monorepos)

For monorepos or projects with non-root Playwright configs:
```
Glob("**/playwright.config.ts")
```

Note the paths for Step 5.

### Step 4: Generate Playwright Test (YOU WRITE THIS)

Based on the analysis, write a Playwright test that demonstrates the UI changes.

**Use vanilla Playwright only** - import from `@playwright/test`, not custom fixtures.

Save to `temp/demo-recording.spec.ts`:

```typescript
import { test } from "@playwright/test";

test("demo: updated modal copy", async ({ page }) => {
  await page.goto("http://localhost:3000/home");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(1500);

  await page.click('[data-testid="add-repo-button"]');
  await page.waitForTimeout(800);

  await page.waitForSelector('[role="dialog"]');
  await page.waitForTimeout(3000); // Let viewers see the changes
});
```

Guidelines:
- Navigate to the affected route
- Include realistic timing with `page.waitForTimeout()` (1-3 seconds between actions)
- Use robust selectors: data-testid > ARIA roles > text content

### Step 5: Generate Narration Script (YOU WRITE THIS)

Write natural narration as a JSON array. Save to `temp/narration-script.json`:

```json
[
  { "text": "This pull request updates the copy in our add repository modal.", "startTimeMs": 0 },
  { "text": "Let me show you - I'll click the add button here.", "startTimeMs": 2500 },
  { "text": "And here's the modal with our updated messaging.", "startTimeMs": 5500 }
]
```

Guidelines:
- Brief intro explaining the PR changes
- Commentary synced to test actions
- Conversational tone
- ~150 words per minute for timing

### Step 6: Run the Recording

```bash
npx tsx lib/cli.ts cleanup
npx tsx lib/cli.ts record temp/demo-recording.spec.ts
```

For monorepos, pass discovered config:
```bash
npx tsx lib/cli.ts record temp/demo-recording.spec.ts --config=apps/web/playwright.config.ts --test-dir=apps/web/tests
```

Look for `videoPath` in the JSON output under `--- RESULT ---`.

### Step 7: Generate Narration Audio (Optional)

If `ELEVEN_LABS_API_KEY` is set:
```bash
npx tsx lib/cli.ts narrate temp/narration-script.json
```

Look for `audioPath` in the JSON output.

### Step 8: Composite Final Video

```bash
npx tsx lib/cli.ts composite <video-path> [audio-path]
```

Example:
```bash
npx tsx lib/cli.ts composite temp/test-results/video.webm temp/narration.mp3
```

Or without audio:
```bash
npx tsx lib/cli.ts composite temp/test-results/video.webm
```

Look for `outputPath` - this is the final MP4 in `output/`.

---

## Configuration

Edit `config.json` in the skill directory:

```json
{
  "baseUrl": "http://localhost:3000",
  "voiceId": "21m00Tcm4TlvDq8ikWAM",
  "videoDimensions": { "width": 1280, "height": 720 },
  "outputDir": "output",
  "tempDir": "temp",
  "recordingTimeout": 60000
}
```

### ElevenLabs Voice IDs

- `21m00Tcm4TlvDq8ikWAM` - Rachel (default, conversational)
- `EXAVITQu4vr4xnSDxMaL` - Bella (warm, friendly)
- `ErXwobaYiN019PkySvjV` - Antoni (professional)

---

## Troubleshooting

### "Dev server not responding"
Start your dev server: `pnpm dev` or `npm run dev`

### "ffmpeg not found"
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`
- Windows: `choco install ffmpeg`

### "ElevenLabs API error"
Check your API key: `echo $ELEVEN_LABS_API_KEY`
Video will work without it (just no narration).

### Video file not found
Check `temp/playwright-output.log` for errors.

---

## MCP Server (Advanced)

For tighter Claude integration, an MCP server is available with typed tools:

```bash
pnpm run mcp-server
```

Tools: `demo_check_prerequisites`, `demo_analyze_changes`, `demo_discover_test_environment`, `demo_save_test_file`, `demo_save_narration_script`, `demo_record_video`, `demo_generate_audio`, `demo_composite_final_video`, `demo_cleanup`

Configure in your MCP settings to use these instead of CLI commands.
