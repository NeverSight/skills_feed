---
name: complex-state-management
description: Production patterns for managing complex application state in React without Redux, Zustand, or other state libraries. Includes multi-stage loading, command patterns, refs for performance, and parallel data fetching. Use when building complex UIs with interconnected states, need loading stages and progress tracking, or implementing command patterns.
---

# Complex State Management Without External Libraries

Production patterns for managing complex application state in React without Redux, Zustand, or other state libraries. Includes multi-stage loading, command patterns, refs for performance, and parallel data fetching.

## When to use this skill

- Building complex UIs with many interconnected states
- Need loading stages and progress tracking
- Implementing command patterns for centralized control
- Managing real-time updates and background operations
- Want to avoid Redux/Zustand overhead
- Building video players, editors, or multi-step flows
- Need precise performance control with refs

## Core Patterns

1. **Multi-Stage Loading States** - Track progress through complex operations
2. **Command Pattern** - Centralized playback/control commands
3. **Ref-Based Optimization** - Avoid re-renders for frequently changing values
4. **Memoized Setters** - Prevent unnecessary child re-renders
5. **Parallel State Updates** - Batch related changes together

## Implementation

### Pattern 1: Multi-Stage Loading with Progress

```typescript
'use client';

import { useState, useRef } from 'react';
import { AbortManager } from '@/lib/promise-utils';

type PageState = 'IDLE' | 'ANALYZING_NEW' | 'LOADING_CACHED' | 'ERROR';
type LoadingStage = 'fetching' | 'understanding' | 'generating' | 'processing' | null;

export function ComplexPage() {
  // Page state machine
  const [pageState, setPageState] = useState<PageState>('IDLE');
  const [loadingStage, setLoadingStage] = useState<LoadingStage>(null);
  const [error, setError] = useState<string>('');

  // Progress tracking
  const [generationStartTime, setGenerationStartTime] = useState<number | null>(null);
  const [processingStartTime, setProcessingStartTime] = useState<number | null>(null);

  // Cleanup manager
  const abortManager = useRef(new AbortManager());

  const handleAnalyze = async () => {
    try {
      // Stage 1: Fetching
      setPageState('ANALYZING_NEW');
      setLoadingStage('fetching');

      const controller1 = abortManager.current.createController('fetch', 30000);
      const data = await fetch('/api/data', { signal: controller1.signal })
        .then(r => r.json());

      // Stage 2: Understanding
      setLoadingStage('understanding');

      // Stage 3: Generating
      setLoadingStage('generating');
      setGenerationStartTime(Date.now());

      const controller2 = abortManager.current.createController('generate', 60000);
      const analysis = await fetch('/api/analyze', {
        signal: controller2.signal,
        method: 'POST',
        body: JSON.stringify(data)
      }).then(r => r.json());

      // Stage 4: Processing
      setLoadingStage('processing');
      setProcessingStartTime(Date.now());

      // Process results...

      setPageState('IDLE');
      setLoadingStage(null);
      setGenerationStartTime(null);

    } catch (error) {
      setPageState('ERROR');
      setError(error.message);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => abortManager.current.cleanup();
  }, []);

  return (
    <div>
      {loadingStage && (
        <LoadingIndicator
          stage={loadingStage}
          elapsedTime={generationStartTime ? Date.now() - generationStartTime : 0}
        />
      )}
    </div>
  );
}
```

### Pattern 2: Command Pattern for Centralized Control

```typescript
// Define command types
export type PlaybackCommandType = 'SEEK' | 'PLAY_TOPIC' | 'PLAY_SEGMENT' | 'PLAY' | 'PAUSE' | 'PLAY_ALL';

export interface PlaybackCommand {
  type: PlaybackCommandType;
  time?: number;
  topic?: Topic;
  segment?: Segment;
  autoPlay?: boolean;
}

// Parent component
export function VideoAnalysisPage() {
  const [playbackCommand, setPlaybackCommand] = useState<PlaybackCommand | null>(null);

  const handleTopicClick = (topic: Topic) => {
    setPlaybackCommand({
      type: 'PLAY_TOPIC',
      topic,
      autoPlay: true
    });
  };

  const handleSeek = (time: number) => {
    setPlaybackCommand({
      type: 'SEEK',
      time
    });
  };

  return (
    <div>
      <VideoPlayer
        command={playbackCommand}
        onCommandExecuted={() => setPlaybackCommand(null)}
      />

      <TopicsList
        topics={topics}
        onTopicClick={handleTopicClick}
      />
    </div>
  );
}

// Child component
export function VideoPlayer({
  command,
  onCommandExecuted
}: {
  command: PlaybackCommand | null;
  onCommandExecuted: () => void;
}) {
  const playerRef = useRef<YouTubePlayer>(null);

  useEffect(() => {
    if (!command || !playerRef.current) return;

    switch (command.type) {
      case 'SEEK':
        playerRef.current.seekTo(command.time!);
        break;

      case 'PLAY_TOPIC':
        playerRef.current.seekTo(command.topic!.startTime);
        if (command.autoPlay) {
          playerRef.current.playVideo();
        }
        break;

      case 'PLAY':
        playerRef.current.playVideo();
        break;

      case 'PAUSE':
        playerRef.current.pauseVideo();
        break;
    }

    onCommandExecuted();
  }, [command]);

  return <div ref={playerRef} />;
}
```

### Pattern 3: Refs for Performance-Critical State

```typescript
export function HighPerformanceComponent() {
  // Use state for UI updates
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null);

  // Use refs for frequently changing values that don't need re-renders
  const selectedThemeRef = useRef<string | null>(null);
  const nextRequestIdRef = useRef(0);
  const activeRequestIdRef = useRef<number | null>(null);
  const pendingRequestsRef = useRef(new Map<string, number>());

  const handleThemeChange = async (theme: string) => {
    // Generate unique request ID
    const requestId = nextRequestIdRef.current++;

    // Cancel previous request for this theme
    const existingRequestId = pendingRequestsRef.current.get(theme);
    if (existingRequestId !== undefined && existingRequestId === activeRequestIdRef.current) {
      return; // Request already in progress
    }

    // Store request ID
    pendingRequestsRef.current.set(theme, requestId);
    activeRequestIdRef.current = requestId;
    selectedThemeRef.current = theme;

    // Update UI
    setSelectedTheme(theme);

    // Fetch data
    const data = await fetchThemeData(theme);

    // Check if this request is still relevant
    if (activeRequestIdRef.current === requestId) {
      // Process data...
    }
  };

  return <div>...</div>;
}
```

### Pattern 4: Memoized Setters for Child Components

```typescript
export function ParentWithManyChildren() {
  const [playAllIndex, setPlayAllIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  // Memoize setters to prevent child re-renders
  const memoizedSetPlayAllIndex = useCallback((value: number | ((prev: number) => number)) => {
    setPlayAllIndex(value);
  }, []);

  const memoizedSetIsPlaying = useCallback((value: boolean) => {
    setIsPlaying(value);
  }, []);

  return (
    <>
      {/* Child won't re-render when other state changes */}
      <PlaybackControls
        index={playAllIndex}
        setIndex={memoizedSetPlayAllIndex}
        isPlaying={isPlaying}
        setIsPlaying={memoizedSetIsPlaying}
      />
    </>
  );
}
```

### Pattern 5: Parallel State Updates

```typescript
export function DataFetchingPage() {
  const [data1, setData1] = useState(null);
  const [data2, setData2] = useState(null);
  const [data3, setData3] = useState(null);

  useEffect(() => {
    const fetchAll = async () => {
      // Fetch in parallel
      const [result1, result2, result3] = await Promise.allSettled([
        fetch('/api/data1').then(r => r.json()),
        fetch('/api/data2').then(r => r.json()),
        fetch('/api/data3').then(r => r.json())
      ]);

      // Batch state updates to trigger single re-render
      React.startTransition(() => {
        if (result1.status === 'fulfilled') setData1(result1.value);
        if (result2.status === 'fulfilled') setData2(result2.value);
        if (result3.status === 'fulfilled') setData3(result3.value);
      });
    };

    fetchAll();
  }, []);

  return <div>...</div>;
}
```

### Pattern 6: Custom Hooks for Complex Logic

```typescript
// Custom hook for elapsed time
export function useElapsedTimer(startTime: number | null) {
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    if (!startTime) {
      setElapsedTime(0);
      return;
    }

    const interval = setInterval(() => {
      setElapsedTime(Date.now() - startTime);
    }, 1000);

    return () => clearInterval(interval);
  }, [startTime]);

  return elapsedTime;
}

// Usage
const generationStartTime = useState<number | null>(null);
const elapsedTime = useElapsedTimer(generationStartTime);

console.log(`Generating for ${Math.floor(elapsedTime / 1000)}s`);
```

### Pattern 7: Theme-Based Dynamic Content

```typescript
export function ThemeBasedContent() {
  const [baseTopics, setBaseTopics] = useState<Topic[]>([]);
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null);
  const [themeTopicsMap, setThemeTopicsMap] = useState<Record<string, Topic[]>>({});
  const [usedTopicKeys, setUsedTopicKeys] = useState<Set<string>>(new Set());

  // Display topics based on selected theme
  const displayedTopics = selectedTheme
    ? (themeTopicsMap[selectedTheme] || [])
    : baseTopics;

  const handleThemeSelect = async (theme: string) => {
    setSelectedTheme(theme);

    // Check cache first
    if (themeTopicsMap[theme]) {
      return; // Already loaded
    }

    // Fetch theme-specific topics
    const newTopics = await fetch('/api/topics', {
      method: 'POST',
      body: JSON.stringify({
        theme,
        excludeKeys: Array.from(usedTopicKeys)
      })
    }).then(r => r.json());

    // Update cache and used keys
    setThemeTopicsMap(prev => ({
      ...prev,
      [theme]: newTopics
    }));

    setUsedTopicKeys(prev => {
      const newSet = new Set(prev);
      newTopics.forEach(t => newSet.add(t.key));
      return newSet;
    });
  };

  return (
    <div>
      <ThemeSelector onSelect={handleThemeSelect} />
      <TopicsList topics={displayedTopics} />
    </div>
  );
}
```

## Best Practices

1. **Use refs for non-UI state** - Don't trigger re-renders unnecessarily
2. **Batch related state updates** - Use startTransition or update together
3. **Memoize callbacks** - Prevent child component re-renders
4. **Clean up on unmount** - Always cleanup timers, subscriptions, AbortControllers
5. **Use state machines** - Explicit states prevent invalid state combinations
6. **Separate concerns** - Loading state, data state, UI state
7. **Cache when possible** - Avoid re-fetching with Map/Set caches

## Common Pitfalls

1. **Too many useState calls** - Group related state into objects
2. **Not cleaning up** - Memory leaks from timers/subscriptions
3. **Passing non-memoized callbacks** - Causes unnecessary re-renders
4. **Using state for everything** - Use refs for non-UI values
5. **Not batching updates** - Multiple state updates = multiple renders
6. **Forgetting dependencies** - useEffect/useCallback need correct deps
7. **Mutating state** - Always create new objects/arrays

## Performance Optimization

```typescript
// ❌ Bad: Multiple re-renders
function Component() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);
  const [c, setC] = useState(0);

  const update = () => {
    setA(1); // Re-render 1
    setB(2); // Re-render 2
    setC(3); // Re-render 3
  };
}

// ✅ Good: Single re-render
function Component() {
  const [state, setState] = useState({ a: 0, b: 0, c: 0 });

  const update = () => {
    setState({ a: 1, b: 2, c: 3 }); // Re-render 1
  };
}

// ✅ Better: Use startTransition for non-urgent updates
function Component() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);
  const [c, setC] = useState(0);

  const update = () => {
    startTransition(() => {
      setA(1);
      setB(2);
      setC(3);
    });
  };
}
```

## Testing

```typescript
import { renderHook, act } from '@testing/library/react';

test('useElapsedTimer increments over time', () => {
  jest.useFakeTimers();

  const { result } = renderHook(() => useElapsedTimer(Date.now()));

  expect(result.current).toBe(0);

  act(() => {
    jest.advanceTimersByTime(5000);
  });

  expect(result.current).toBeGreaterThanOrEqual(5000);
});
```

## Next Steps

1. Extract common patterns into custom hooks
2. Add state persistence with localStorage
3. Implement undo/redo with state history
4. Add state debugging with DevTools
5. Create state machines with XState if needed
6. Profile render performance with React DevTools

## Related Skills

- **Resilient Async Operations** - Manage async state safely
- **Type-Safe Form Validation** - Validate state updates
- **Advanced Text Search** - Complex search state management

---

Built from production state management in [TLDW](https://github.com/vishalsachdev/tldw) video analysis UI
