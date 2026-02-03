---
name: capacitor-bridge
description: Specialist in Android Intents, Java-JS bridging, and External Player integration.
---

# Capacitor Bridge Skill

This skill handles the communication between the React Frontend and the Native Android layer (`TVPlayer.java`).
**Primary Goal:** Launch external players (VLC, MX Player, Vimu) correctly and handle their return results (resume position).

## 桥 API Contract

### `TVPlayer.play(options)`
Launches a single video file. **Must return a Promise that resolves only after the player closes.**

**Options:**
*   `url` (string, required): Direct link to the video stream.
*   `package` (string, optional): Specific player package name (e.g., `net.gtvbox.videoplayer`). If null, opens system chooser.
*   `title` (string): Title to display in the player.
*   `position` (number): Resume position in milliseconds.

**Java Extras (What actually gets sent):**
*   `Intent.ACTION_VIEW`
*   `return_result`: `true`
*   **Flags:** `FLAG_ACTIVITY_CLEAR_TOP`, `FLAG_ACTIVITY_SINGLE_TOP` (Crucial for preventing double rendering).

### `TVPlayer.playList(options)`
Launches a playlist (Season/Series).

**Options:**
*   `urls` (string[]): Array of video URLs.
*   `names` (string[]): Array of episode titles.
*   `startIndex` (number): Which index to start playing.
*   `position` (number): Resume position for the *started* episode.

## 📱 Supported Players & Extras

### Vimu Player (`net.gtvbox.videoplayer`)
*   **Single:** `forcename` (Title), `forcedirect` (No buffer), `startfrom` (Position).
*   **Playlist:** Uses `application/vnd.gtvbox.filelist` MIME type.
    *   `asusfilelist` (URLs)
    *   `asusnamelist` (Names)

### MX Player (`com.mxtech.videoplayer.ad` / `.pro`)
*   **Single:** `title`, `position`.
*   **Playlist:** Uses standard `video/*` with extras.
    *   `video_list` (Parcelable Uri[])
    *   `video_list.name` (String[])

### VLC (`org.videolan.vlc`)
*   **Single:** `title`, `from_start` (false).
*   **Playlist:** *Not fully supported via Intent extras, falls back to acting as single file player currently.*

## ⚠️ Critical Rules
1.  **Do NOT change `FLAG_ACTIVITY_SINGLE_TOP`.** This prevents the app from restarting or opening a second instance of the intent chooser.
2.  **RESTRICTED: `FLAG_ACTIVITY_NEW_TASK` and `FLAG_ACTIVITY_CLEAR_TOP`**. These flags are essential for correct stack manipulation between PWA and Native Player. Removing them breaks the return journey.
3.  **Lifecycle:** The promise resolves when `onActivityResult` fires (i.e., user closes the player).
    *   **Requirement:** `play()` method MUST return a Promise resolving with `{ position, duration }`.
4.  **Resume Logic:** The result object contains `{ position: number, duration: number, finished: boolean }`. You MUST save this to `localStorage` immediately.
