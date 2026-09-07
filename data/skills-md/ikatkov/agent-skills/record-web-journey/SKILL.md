---
name: record-web-journey
description: Record a web journey as evidence on the browser host - a WebM video, a screenshot after every click and page load with a red marker at the click point, and a steps.md log. Works two ways - an agent drives the browser itself through agent-browser over CDP, or a human clicks through a Playwright-launched window while the script records. Use when asked to "record a web journey", "record the flow", "capture a user flow", "show me what you clicked", or when a walkthrough needs screenshots and video as proof.
---

# Record a web journey

Produces `<out>/<NAME>-<timestamp>/` with `steps.md`, `screenshots/NNN-<kind>-<label>.png`, and
`videos/*.webm`. `steps.md` keeps typed values and query strings omitted.

Run the recorder and browser driver on the same host. Save the artifacts directly on that
host: a browser running in a VM writes to the VM, and a browser running locally writes to the
local machine. Leave the completed folder in place for later review and report its absolute
path.

Set `SKILL_DIR` to the absolute directory containing this `SKILL.md`, then use the bundled
recorder through its absolute path:

```bash
SKILL_DIR="/absolute/path/to/record-web-journey"
RECORDER="$SKILL_DIR/scripts/record-flow.mjs"
AB="$SKILL_DIR/scripts/node_modules/.bin/agent-browser"
```

Re-establish `SKILL_DIR`, `RECORDER`, `AB`, the retained CDP port, and `DISPLAY` when applicable
at the start of each separate shell call; agent harness shells may be independent.

## Setup (once per browser host)

```bash
"$SKILL_DIR/scripts/setup.sh"
"$AB" skills get core
```

Installs agent-browser and Playwright next to the recorder, adds Playwright's ffmpeg helper for
video, and adds Chromium when Google Chrome is absent. Prefer `--chrome` when Google Chrome
exists: it looks like a normal browser to sign-in pages.

## Agent-driven recording (you drive)

Parse the request into: start URL, recording NAME, and the steps to perform.

1. Check the host. `pgrep -a Xvnc` or `echo $DISPLAY` tells you whether a desktop exists; if
   it does, `export DISPLAY=<it>` in every shell call and the human can watch live. Without a
   display add `--headless`. Check `df -h /dev/shm`; remount to 2G if it is 64M or Chrome
   renderers crash. On shared hosts, inspect active `agent-browser` processes, choose a unique
   session, and close only that named session at completion.
2. From the workspace being recorded, choose an absolute output directory on this host and
   an available local CDP port. Start the recorder in a dedicated long-lived terminal or
   harness process session and keep that session running:

   ```bash
   OUT="$PWD/.context/flow-recordings"
   PORT="$(node -e 'const s=require("node:net").createServer();s.listen(0,"127.0.0.1",()=>{console.log(s.address().port);s.close()})')"
   BROWSER_ARGS=()
   if command -v google-chrome >/dev/null || { [[ "$(uname -s)" == Darwin ]] && [[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; }; then
     BROWSER_ARGS=(--chrome)
   fi
   printf 'CDP port: %s\n' "$PORT"
   node "$RECORDER" "https://app.example.com/" --name "journey-name" "${BROWSER_ARGS[@]}" --cdp "$PORT" --out "$OUT"
   ```

   Retain the printed port and absolute recording directory across shell calls. Pass
   `--profile <dir>` for a signed-in journey (see
   `references/auth-and-bot-checks.md`).
3. Attach agent-browser to that Chrome with a unique session name and drive as usual:

   ```bash
   "$AB" --session "rec-journey-name" --cdp "$PORT" snapshot -i -u
   "$AB" --session "rec-journey-name" --cdp "$PORT" click @e5
   ```

   Every command uses both `--session` and `--cdp`. Continue from the start URL loaded by the
   recorder, and use `open` when a requested step calls for direct navigation.
4. Pace like a person: about a second between actions, `wait --load networkidle` after
   navigations. Each screenshot is taken 250 ms after the click, so back-to-back clicks blur
   which screenshot belongs to which step.
5. For anything below the fold: `scrollintoview @ref`, then `wait 1000`, then `click @ref`.
   Sites with `scroll-behavior: smooth` animate the scroll; explicit settling keeps click
   coordinates aligned with the target and avoids the mid-animation coordinate read verified
   on claude.ai. Drive clicks through fresh, visible refs from `snapshot -i`. A visually hidden
   1x1 input records as "(no visible target)", so select the visible label or control that
   represents it.
6. Finish through `<recordingDir>/STOP`, wait for "Saved N visual steps" in the recorder
   session, then close the named agent-browser session. This sequence finalizes the WebM
   before handoff.

   ```bash
   touch "/absolute/recording/directory/STOP"
   ```

   Resume or wait on the recorder's long-lived session until it prints `Saved N visual steps`,
   then close the named driver session:

   ```bash
   "$AB" --session "rec-journey-name" close
   ```
7. Complete `steps.md` on the browser host with one short observation under each step: visible
   copy, relevant responses from `agent-browser network requests`, and any result that differs
   from the expected flow. Leave the artifact folder there. Report its absolute path, the step
   count, the observed outcome, and anything that blocked a requested step.

## Human-driven recording (a person drives)

```bash
node "$RECORDER" https://app.example.com/ -name "F06" --chrome --profile .context/chrome-profile
```

The person uses the window normally and presses Enter in the terminal when done. The resulting
folder stays under the selected output directory on that machine for later review.

## Flags

| Flag | Meaning |
| --- | --- |
| `-name "<NAME>"` | Folder prefix, e.g. `F06-custom-mcp-<timestamp>` |
| `--chrome` | Use installed Google Chrome (recommended when present) |
| `--profile <dir>` | Reuse a Chrome user-data dir so sign-ins survive between recordings |
| `--cdp <port>` | Expose CDP so an agent can attach with `agent-browser --cdp <port>` |
| `--headless` | No window; video and screenshots still produced |
| `--out <dir>` | Parent directory, default `.context/flow-recordings` |
| `--viewport WxH` | Viewport and video size, default `1440x900` |
| `--sign-in` | With `--profile`: open plain Chrome to pass a bot check or sign in, then quit |

Ending signals: Enter (TTY), `STOP` file, browser close, SIGTERM. Enter or `STOP` gives
Playwright the clean finalization path.
