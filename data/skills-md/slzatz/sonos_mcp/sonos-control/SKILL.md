---
name: sonos-control
description: Control Sonos speakers through MCP tools - search and play music, manage queue and playlists, adjust volume. Use when users request music playback, mention artists/songs/albums, want to control Sonos speakers, manage playlists, or ask about what's playing.
---

# Sonos Control

## Overview

This skill provides comprehensive control over Sonos speaker systems through MCP tools. Use it to search for and play music, manage playback queues and playlists, control volume, and switch between speakers. The skill handles both simple requests ("play some Neil Young") and complex multi-step workflows ("create a mix of 5 tracks from these artists").

## Core Principle: Multi-Step Workflows

Most music requests require multiple tool calls in sequence. Execute workflows automatically without asking permission at each step - just complete the workflow and confirm the result.

**Critical Rule:** Search results are ephemeral. After using `search_for_track` or `search_for_album`, immediately select and add desired tracks/albums to the queue before executing another search, as each new search clears previous results.

## Available MCP Tools

### Speaker Management
- `sonos:get_master_speaker` - Get current active speaker name
- `sonos:set_master_speaker` - Switch to a different speaker (e.g., "Bedroom", "Kitchen")

### Search and Selection
- `sonos:search_for_track` - Search by track title, artist, album (e.g., "Heart of Gold Neil Young")
- `sonos:search_for_album` - Search by album title and artist (e.g., "Harvest Neil Young")
- `sonos:add_track_to_queue` - Add track from search results by position (1-based)
- `sonos:add_album_to_queue` - Add album from search results by position (1-based)

### Queue Management
- `sonos:list_queue` - View all queued tracks
- `sonos:clear_queue` - Remove all tracks from queue
- `sonos:remove_from_queue` - Remove a track from the queue by position (1-based)
- `sonos:play_from_queue` - Play track at specific queue position (1-based)

### Playback Control
- `sonos:current_track` - Get information about currently playing track
- `sonos:play_pause` - Toggle play/pause
- `sonos:next_track` - Skip to next track

### Volume Control
- `sonos:turn_volume` - Adjust volume by 10 ("louder" or "quieter")
- `sonos:set_volume` - Set absolute volume (0-100)
- `sonos:mute` - Mute or unmute (True/False)

### Playlist Management

**Terminology:**
- **"playlist"** or **"local playlist"** = Playlists stored locally on the filesystem (`~/.sonos/playlists/`)
- **"native Sonos playlist"** = Playlists stored on the Sonos system (accessible from Sonos mobile app)

**Local Playlist Tools:**
- `sonos:list_playlists` - Display all local playlists
- `sonos:list_playlist_tracks` - Show tracks in a specific local playlist
- `sonos:add_to_playlist_from_queue` - Add queue track to local playlist by position
- `sonos:add_to_playlist_from_search` - Add search result to local playlist by position
- `sonos:add_playlist_to_queue` - Load entire local playlist into queue (optionally shuffled with shuffle=True)
- `sonos:remove_track_from_playlist` - Remove track from local playlist by position

**Native Sonos Playlist Tools:**
- `sonos:list_native_sonos_playlists` - Display all native Sonos playlists
- `sonos:create_native_sonos_playlist_from_local(local_playlist, native_playlist_name=None)` - Convert a local playlist to a native Sonos playlist
  - Checks for naming conflicts and reports if native playlist already exists
  - Temporarily uses queue but restores original queue contents
  - Makes playlist accessible from Sonos mobile app and other Sonos controllers

## Basic Workflow: Play a Track or Album

To play a specific track or album:

1. **Search** - Use `sonos:search_for_track` or `sonos:search_for_album`
2. **Select** - Use `sonos:add_track_to_queue` or `sonos:add_album_to_queue` with position number
3. **Find Position** - Use `sonos:list_queue` to see where track(s) were added
4. **Play** - Use `sonos:play_from_queue` with the position from step 3
5. **Verify** - Use `sonos:current_track` to confirm correct track is playing

**Example:** User says "play Like a Hurricane by Neil Young"
```
1. sonos:search_for_track "Like a Hurricane Neil Young"
2. sonos:add_track_to_queue 1  (select best match)
3. sonos:list_queue  (find it was added at position 15)
4. sonos:play_from_queue 15
5. sonos:current_track  (confirm)
```

## Advanced Workflows

### Creating Custom Mixes

To build a custom mix from multiple artists:

1. **For each artist:** Execute search → select → add cycle
2. **Between searches:** Ensure previous track is added to queue before next search
3. **Play first track** when all selections complete
4. **Verify** the queue contains all desired tracks

**Example:** User says "play a mix of Springsteen, Jackson Browne, and Patty Griffin"
```
1. sonos:search_for_track "Born to Run Springsteen"
2. sonos:add_track_to_queue 1
3. sonos:search_for_track "Running on Empty Jackson Browne"
4. sonos:add_track_to_queue 1
5. sonos:search_for_track "Let Him Fly Patty Griffin"
6. sonos:add_track_to_queue 1
7. sonos:list_queue (verify all added)
8. sonos:play_from_queue 1 (start first track)
```

### Finding Live Performances

To find live tracks or albums:

1. **Include "live" or "unplugged" in search queries**
2. **Look for venue names** in search results: "Massey Hall", "Nashville", "The Troubadour", "Red Rocks", "The Fillmore", "The Ryman"
3. **Check album titles** for indicators: "Live at", "Unplugged", "In Concert"

**Example:** User says "play 5 live tracks from Patty Griffin"
```
1. sonos:search_for_track "Patty Griffin live"
2. Review results for venue names or "live" indicators
3. sonos:add_track_to_queue 1
4. sonos:add_track_to_queue 3
5. sonos:add_track_to_queue 5
6. sonos:add_track_to_queue 7
7. sonos:add_track_to_queue 9
8. sonos:play_from_queue 1
```

### Multi-Room Control

To play music in a specific room:

1. **Switch speaker first** - Use `sonos:set_master_speaker` with room name
2. **Verify switch** - Check response confirms speaker change
3. **Continue with normal workflow** - Search, add, play as usual

**Example:** User says "play some Neil Young in the bedroom"
```
1. sonos:set_master_speaker "Bedroom"
2. sonos:search_for_track "Neil Young"
3. sonos:add_track_to_queue 1
4. sonos:play_from_queue 1
```

## Playlist Workflows

### Adding Tracks to Playlists

**From queue:**
1. Use `sonos:list_queue` to find track position
2. Use `sonos:add_to_playlist_from_queue` with playlist name and position

**From search:**
1. Use `sonos:search_for_track` to find track
2. Use `sonos:add_to_playlist_from_search` with playlist name and position

**Example:** User says "add the current track to my Chill Vibes playlist"
```
1. sonos:current_track (get what's playing)
2. sonos:list_queue (find its position)
3. sonos:add_to_playlist_from_queue "Chill Vibes" <position>
```

### Copying Entire Queue to New Playlist

To save the current queue as a new playlist (useful for preserving a curated queue):

1. Use `sonos:list_queue` to see all tracks and count them
2. For each track position (1 through N), use `sonos:add_to_playlist_from_queue` with the new playlist name
3. The first call creates the new playlist; subsequent calls append tracks
4. Optionally verify with `sonos:list_playlist_tracks`

**Important:** When removing multiple tracks from a queue or playlist, always remove from highest position to lowest to avoid position shifts affecting remaining targets.

**Example:** User says "save everything in the queue as playlist20250119"
```
1. sonos:list_queue (count 59 tracks)
2. sonos:add_to_playlist_from_queue "playlist20250119" 1
3. sonos:add_to_playlist_from_queue "playlist20250119" 2
... (continue for all 59 positions)
60. sonos:list_playlist_tracks "playlist20250119" (verify)
```

**Note:** For large queues (50+ tracks), execute all additions in sequence without requesting permission at each step, following the "Multi-Step Workflows" principle.

## Selecting Multiple Tracks from One Artist

When a user requests N tracks from an artist without specific guidance:

### Default Strategy (No Prior Context)
1. **Mix popular and quality tracks** - Include 1-2 well-known hits, rest can be deep cuts
2. **Album variety** - Spread selections across 2-3 different albums when possible
3. **Career representation** - For established artists, vary across different periods
4. **Mood consistency** - Ensure tracks flow well together in sequence

### Contextual Adjustments
- **If user mentions "favorites"** - Prioritize most-streamed/canonical tracks
- **If user says "best of"** - Focus on greatest hits and popular tracks
- **If user mentions specific album** - Select all tracks from that album
- **If user says "variety" or "mix"** - Maximize album and style diversity

### When to Ask for Clarification
Only ask if the request is genuinely ambiguous:
- ✗ Don't ask: "play 3 Vienna Teng songs" (use default strategy)
- ✓ Do ask: "play Neil Young songs" when user has requested both acoustic and electric in past
- ✓ Do ask: "play some Beatles" (too many eras/styles to assume)

### Selection Transparency
In your response, briefly mention your selection reasoning:
- "I've added 3 tracks mixing popular hits and album favorites..."
- "Here are 3 tracks spanning her early and recent work..."
### Playing Playlists

To play a saved playlist:
1. Use `sonos:add_playlist_to_queue` to load all tracks (optionally with shuffle=True)
2. Use `sonos:play_from_queue 1` to start playing

**Example:** User says "play my favorites playlist"
```
1. sonos:add_playlist_to_queue "favorites"
2. sonos:play_from_queue 1
```

**Example:** User says "play my workout playlist in random order"
```
1. sonos:add_playlist_to_queue "workout" shuffle=True
2. sonos:play_from_queue 1
```

### Converting Local Playlists to Native Sonos Playlists

To make a local playlist accessible in the Sonos mobile app and other Sonos controllers:

1. **Check for conflicts** - Use `sonos:list_native_sonos_playlists` to see if the name already exists
2. **Convert** - Use `sonos:create_native_sonos_playlist_from_local` with the local playlist name
3. **Optionally specify different name** - Pass `native_playlist_name` parameter if desired
4. **Verify** - Use `sonos:list_native_sonos_playlists` to confirm creation

**Example:** User says "create a native Sonos playlist from my favorites playlist"
```
1. sonos:list_native_sonos_playlists (check if "favorites" already exists)
2. sonos:create_native_sonos_playlist_from_local "favorites"
3. sonos:list_native_sonos_playlists (verify it was created)
```

**Example:** User says "make a Sonos playlist called favorites_backup from my favorites playlist"
```
1. sonos:create_native_sonos_playlist_from_local "favorites" native_playlist_name="favorites_backup"
2. sonos:list_native_sonos_playlists (verify)
```

**Important Notes:**
- The conversion temporarily uses the queue but restores it automatically
- If a native playlist with that name already exists, you'll get an error with a clear message
- Ask the user if they want to use a different name or if they want you to proceed differently
- Local and native playlists are independent - changes to one don't affect the other

## Common Request Patterns

### Simple Requests
- "What's playing?" → `sonos:current_track`
- "Show me the queue" → `sonos:list_queue`
- "Turn it up" → `sonos:turn_volume "louder"`
- "Set volume to 50" → `sonos:set_volume 50`
- "Mute" → `sonos:mute True`
- "Next song" → `sonos:next_track`
- "Pause" → `sonos:play_pause`
- "What playlists do I have?" → `sonos:list_playlists`
- "Show my native Sonos playlists" → `sonos:list_native_sonos_playlists`

### Complex Requests
- "Play [specific track]" → Execute Basic Workflow
- "Play [number] tracks by [artist]" → Execute Advanced Workflow with multiple searches
- "Create a mix of [artists]" → Execute Custom Mix Workflow
- "Play some [artist] in [room]" → Execute Multi-Room Workflow
- "Add [track] to [playlist]" → Execute Playlist Workflow
- "Play [playlist] shuffled/randomized/in random order" → Use `add_playlist_to_queue` with shuffle=True
- "Create a native Sonos playlist from [local playlist]" → Execute Converting Local Playlists Workflow
- "Make [local playlist] available in the Sonos app" → Execute Converting Local Playlists Workflow

## Response Guidelines

### After Completing Workflows

Provide natural, music-focused responses:
- Confirm what's playing
- Share relevant context (album, year, interesting facts)
- Explain selection reasoning for custom mixes
- Mention notable aspects (live performance, rare version, etc.)

### When Making Selections

Use music knowledge to select best matches:
- Prefer original studio versions unless user requests otherwise
- For "live" requests, prioritize well-known live albums
- For deep cuts, select lesser-known but high-quality tracks
- Consider chronology and artist periods when building mixes

### Handling Ambiguity

If search results are unclear:
- Make best judgment based on context
- Select most popular/canonical version
- Only ask for clarification if results are completely ambiguous
- Provide reasoning for selection in response

## Error Handling

### Search Returns No Results
- Try simplified search (fewer keywords)
- Suggest alternative artist/track names
- Offer to search for similar artists or tracks
- Consult `references/search_tips.md` for search strategies

### Queue Issues
- If queue is full, suggest clearing old tracks
- If position is invalid, list queue to find correct position

### Playback Issues
- Verify track is in queue using `sonos:list_queue`
- Confirm correct speaker using `sonos:get_master_speaker`
- Check current status with `sonos:current_track`

## Additional Resources

For detailed search strategies, artist name variations, and mix-building tips, reference the bundled file:
- `references/search_tips.md` - Comprehensive guide for effective music searches
