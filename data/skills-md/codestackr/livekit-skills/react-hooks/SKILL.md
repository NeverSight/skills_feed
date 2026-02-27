---
name: react-hooks
description: Build custom React UIs with LiveKit hooks from @livekit/components-react. Use this skill when you need low-level control over agent state, participants, tracks, chat, and data channels. For pre-built UI components, use the livekit-agents-ui skill instead.
---

# LiveKit React Hooks

Build custom React UIs for realtime audio/video applications with LiveKit hooks.

## LiveKit MCP server tools

This skill works alongside the LiveKit MCP server, which provides direct access to the latest LiveKit documentation, code examples, and changelogs. Use these tools when you need up-to-date information that may have changed since this skill was created.

**Available MCP tools:**
- `docs_search` - Search the LiveKit docs site
- `get_pages` - Fetch specific documentation pages by path
- `get_changelog` - Get recent releases and updates for LiveKit packages
- `code_search` - Search LiveKit repositories for code examples
- `get_python_agent_example` - Browse 100+ Python agent examples

**When to use MCP tools:**
- You need the latest API documentation or feature updates
- You're looking for recent examples or code patterns
- You want to check if a feature has been added in recent releases
- The local references don't cover a specific topic

**When to use local references:**
- You need quick access to core concepts covered in this skill
- You're working offline or want faster access to common patterns
- The information in the references is sufficient for your needs

Use MCP tools and local references together for the best experience.

## Scope

This skill covers **hooks only** from `@livekit/components-react`. These hooks provide low-level access to LiveKit room state, participants, tracks, and agent data for building fully custom UIs.

**Important: For agent applications, do NOT use UI components from `@livekit/components-react`.** All UI components should come from the **livekit-agents-ui** skill, which provides shadcn-based components:
- `AgentSessionProvider` - Session wrapper with audio rendering
- `AgentControlBar` - Media controls
- `AgentAudioVisualizerBar/Grid/Radial` - Audio visualizers
- `AgentChatTranscript` - Chat display
- And more

Use hooks from this skill only when you need custom behavior that the Agents UI components don't provide. The Agents UI components use these hooks internally.

## References

Consult these resources as needed:

- ./references/livekit-overview.md -- LiveKit ecosystem overview and how these skills work together
- ./references/participant-hooks.md -- Hooks for accessing participant data and state
- ./references/track-hooks.md -- Hooks for working with audio/video tracks
- ./references/room-hooks.md -- Hooks for room connection and state
- ./references/session-hooks.md -- Hooks for managed agent sessions (useSession, useSessionMessages)
- ./references/agent-hooks.md -- Hooks for voice AI agent integration
- ./references/data-hooks.md -- Hooks for chat and data channels

## Installation

```bash
npm install @livekit/components-react livekit-client
```

## Quick start

### Using hooks with AgentSessionProvider (standard approach)

For agent apps, use `AgentSessionProvider` from the **livekit-agents-ui** skill for the session provider. The `useSession` hook from this package is **required** to create the session for `AgentSessionProvider`.

**Required hook**: Use `useSession` to create the session object:

```tsx
import { useRef, useEffect } from 'react';
import { useSession } from '@livekit/components-react';
import { TokenSource, TokenSourceConfigurable } from 'livekit-client';
import { AgentSessionProvider } from '@/components/agents-ui/agent-session-provider';

function App() {
  const tokenSource: TokenSourceConfigurable = useRef(
    TokenSource.endpoint('/api/token')
  ).current;

  // Create session using useSession hook (required for AgentSessionProvider)
  const session = useSession(tokenSource, { agentName: 'your-agent' });

  useEffect(() => {
    session.start();
    return () => session.end();
  }, []);

  return (
    <AgentSessionProvider session={session}>
      <MyAgentUI />
    </AgentSessionProvider>
  );
}
```

**Additional hook for agent state**: Use `useVoiceAssistant` to access agent state, audio tracks, and transcriptions:

```tsx
import { useVoiceAssistant } from '@livekit/components-react';

// This component must be inside an AgentSessionProvider
function CustomAgentStatus() {
  const { state, audioTrack, agentTranscriptions } = useVoiceAssistant();

  return (
    <div>
      <p>Agent state: {state}</p>
      {agentTranscriptions.map((t) => (
        <p key={t.id}>{t.text}</p>
      ))}
    </div>
  );
}
```

See the **livekit-agents-ui** skill for full component documentation.

### Custom microphone toggle

```tsx
import { useTrackToggle } from '@livekit/components-react';
import { Track } from 'livekit-client';

// Use this inside an AgentSessionProvider for custom toggle behavior
function CustomMicrophoneButton() {
  const { enabled, toggle, pending } = useTrackToggle({
    source: Track.Source.Microphone,
  });

  return (
    <button onClick={() => toggle()} disabled={pending}>
      {enabled ? 'Mute' : 'Unmute'}
    </button>
  );
}
```

### Fully custom approach: useSession + SessionProvider (not recommended)

> **Note**: This pattern uses UI components from `@livekit/components-react` directly. For agent applications, use `AgentSessionProvider` from livekit-agents-ui instead, which wraps these components and provides a better developer experience.

For fully custom implementations without Agents UI components, you can use `useSession` with `SessionProvider` and `RoomAudioRenderer` directly. This gives you complete control but requires more manual setup.

Use this pattern only when you cannot use `AgentSessionProvider` from Agents UI:

```tsx
import { useEffect, useRef } from 'react';
import { useSession, useAgent, SessionProvider, RoomAudioRenderer } from '@livekit/components-react';
import { TokenSource, TokenSourceConfigurable } from 'livekit-client';

function AgentApp() {
  // Use useRef to prevent recreating TokenSource on each render
  const tokenSource: TokenSourceConfigurable = useRef(
    TokenSource.sandboxTokenServer('your-sandbox-id')
  ).current;

  const session = useSession(tokenSource, {
    agentName: 'your-agent-name',
  });
  const agent = useAgent(session);

  // Auto-start session with cleanup
  useEffect(() => {
    session.start();
    return () => {
      session.end();
    };
  }, []);

  return (
    <SessionProvider session={session}>
      <RoomAudioRenderer />
      <div>
        <p>Connection: {session.connectionState}</p>
        <p>Agent: {agent.state}</p>
      </div>
    </SessionProvider>
  );
}
```

For production, use `TokenSource.endpoint()` instead of the sandbox:

```tsx
const tokenSource: TokenSourceConfigurable = useRef(
  TokenSource.endpoint('/api/token')
).current;

const session = useSession(tokenSource, {
  roomName: 'my-room',
  participantIdentity: 'user-123',
  participantName: 'John',
  agentName: 'my-agent',
});
```

## Hook categories

### Participant hooks

Access participant data and state:

- `useParticipants()` - All participants (local + remote)
- `useLocalParticipant()` - Local participant with media state
- `useRemoteParticipants()` - All remote participants
- `useRemoteParticipant(identity)` - Specific remote participant
- `useParticipantInfo()` - Identity, name, metadata
- `useParticipantAttributes()` - Participant attributes

### Track hooks

Work with audio/video tracks:

- `useTracks(sources)` - Array of track references
- `useParticipantTracks(sources, identity)` - Tracks for specific participant
- `useTrackToggle({ source })` - Toggle mic/camera/screen
- `useIsMuted(trackRef)` - Check if track is muted
- `useIsSpeaking(participant)` - Check if participant is speaking
- `useTrackVolume(track)` - Audio volume level

### Room hooks

Room connection and state:

- `useConnectionState()` - Room connection state
- `useRoomInfo()` - Room name and metadata
- `useLiveKitRoom(props)` - Create and manage room instance
- `useIsRecording()` - Check if room is being recorded
- `useMediaDeviceSelect({ kind })` - Select audio/video devices

### Session hooks (beta)

For session management (required for `AgentSessionProvider`):

- `useSession(tokenSource, options)` - Create and manage agent session with connection lifecycle. Required for `AgentSessionProvider`.
- `useSessionMessages(session)` - Combined chat and transcription messages

### Agent hooks (beta)

Voice AI agent integration:

- `useVoiceAssistant()` - Primary hook for agent state, tracks, and transcriptions. Works inside `AgentSessionProvider`.
- `useAgent(session)` - Full agent state with lifecycle helpers. Requires session from `useSession`.

### Data hooks

Chat and data channels:

- `useChat()` - Send/receive chat messages
- `useDataChannel(topic)` - Low-level data messaging
- `useTextStream(topic)` - Subscribe to text streams (beta)
- `useTranscriptions()` - Get transcription data (beta)
- `useEvents(instance, event, handler)` - Subscribe to typed events from session/agent

## Context requirement

Most hooks require a room context. For agent applications, there are two approaches:

### Option 1: useSession + AgentSessionProvider (standard)

Use `useSession` to create a session, then pass it to `AgentSessionProvider` from livekit-agents-ui. The `AgentSessionProvider` wraps `SessionProvider` and includes `RoomAudioRenderer` for audio playback. Hooks like `useVoiceAssistant`, `useTrackToggle`, `useChat`, and others work automatically inside this provider.

```tsx
import { useRef, useEffect } from 'react';
import { useSession, useVoiceAssistant } from '@livekit/components-react';
import { TokenSource, TokenSourceConfigurable } from 'livekit-client';
import { AgentSessionProvider } from '@/components/agents-ui/agent-session-provider';

function App() {
  const tokenSource: TokenSourceConfigurable = useRef(
    TokenSource.endpoint('/api/token')
  ).current;

  // Create session using useSession hook (required)
  const session = useSession(tokenSource, { agentName: 'your-agent' });

  useEffect(() => {
    session.start();
    return () => session.end();
  }, []);

  return (
    <AgentSessionProvider session={session}>
      {/* Hooks from @livekit/components-react work here */}
      <MyAgentComponent />
    </AgentSessionProvider>
  );
}

function MyAgentComponent() {
  // useVoiceAssistant works inside AgentSessionProvider
  const { state, audioTrack } = useVoiceAssistant();
  return <div>Agent: {state}</div>;
}
```

### Option 2: useSession + SessionProvider (not recommended)

> **Note**: This pattern uses UI components from `@livekit/components-react` directly. For agent applications, use Option 1 with `AgentSessionProvider` from livekit-agents-ui instead.

Only use this pattern if you need full manual control without using Agents UI components. You must include `RoomAudioRenderer` manually.

```tsx
import { useRef, useEffect } from 'react';
import { useSession, useAgent, SessionProvider, RoomAudioRenderer } from '@livekit/components-react';
import { TokenSource, TokenSourceConfigurable } from 'livekit-client';

function App() {
  const tokenSource: TokenSourceConfigurable = useRef(
    TokenSource.sandboxTokenServer('your-sandbox-id')
  ).current;

  const session = useSession(tokenSource, { agentName: 'your-agent' });
  const agent = useAgent(session); // Pass session explicitly when using useSession

  useEffect(() => {
    session.start();
    return () => session.end();
  }, []);

  return (
    <SessionProvider session={session}>
      <RoomAudioRenderer />
      <MyAgentComponent agent={agent} />
    </SessionProvider>
  );
}
```

## Best practices

### General

1. **Use Agents UI for standard UIs** - For most agent applications, use the pre-built components from livekit-agents-ui. Use these hooks only when you need custom behavior.
2. **Optimize with updateOnlyOn** - Many hooks accept `updateOnlyOn` to limit re-renders to specific events.
3. **Handle connection states** - Always check `useConnectionState()` before accessing room data.
4. **Memoize TokenSource** - Always use `useRef` when creating a `TokenSource` to prevent recreation on each render.

### For agent applications

5. **Use useSession with AgentSessionProvider** - For most agent apps, create a session with `useSession` and pass it to `AgentSessionProvider` from livekit-agents-ui. The `AgentSessionProvider` handles audio rendering automatically.

6. **Use useVoiceAssistant for agent state** - Inside `AgentSessionProvider`, use `useVoiceAssistant` to access agent state and transcriptions. This is simpler than `useAgent`.

```tsx
import { useVoiceAssistant } from '@livekit/components-react';

function AgentDisplay() {
  const { state, audioTrack, agentTranscriptions } = useVoiceAssistant();
  // state: "disconnected" | "connecting" | "initializing" | "listening" | "thinking" | "speaking"
}
```

7. **Handle agent states properly** - When using `useAgent`, handle all states including `'idle'`, `'pre-connect-buffering'`, and `'failed'`:

```tsx
const agent = useAgent(session);

if (agent.state === 'failed') {
  console.error('Agent failed:', agent.failureReasons);
}

if (agent.isPending) {
  // Show loading state
}
```

8. **Always use AgentSessionProvider** - Use `useSession` + `AgentSessionProvider` from livekit-agents-ui for all agent applications. This is the standard and recommended approach.

### Performance

9. **Use LiveKit's built-in hooks for media controls** - For track toggling, device selection, and similar features, use the provided hooks (`useTrackToggle`, `useMediaDeviceSelect`) rather than implementing your own. These hooks handle complex state management and have been rigorously tested.

10. **Subscribe to events with useEvents** - Instead of manually managing event listeners, use `useEvents` to subscribe to session and agent events with proper cleanup:

```tsx
useEvents(agent, AgentEvent.StateChanged, (state) => {
  console.log('Agent state:', state);
});
```

### Beta hooks

Several hooks in `@livekit/components-react` are marked as beta and may change:
- `useSession`, `useSessionMessages`
- `useAgent`, `useVoiceAssistant`
- `useTextStream`, `useTranscriptions`

Check the [LiveKit components changelog](https://github.com/livekit/components-js/releases) for updates to these hooks.
