---
name: console-frontend-review
description: Reviews React/TypeScript code for the depot console web application with focus on real-time rover teleoperation, state management, WebSocket communication, and 3D visualization. Use when reviewing console frontend changes, debugging teleop UI issues, optimizing rendering performance, validating WebSocket protocols, checking React Three Fiber implementations, or evaluating state management patterns. Covers Zustand store architecture, binary protocol encoding, input handling, page visibility safety, memory management, and 360-degree video streaming.
allowed-tools: Read, Grep, Glob, Bash(npm:test), Bash(npm:build), Bash(npm:lint)
---

# Depot Console Frontend Code Review Skill

This skill provides comprehensive code review for the depot console React/TypeScript web application used for fleet operations and rover teleoperation.

## Overview

The depot console is a React 19 web application providing real-time control and monitoring of BVR rovers. It features 3D visualization, WebSocket-based teleop, and 360° video streaming.

**Technology Stack:**
- **Framework**: React 19 with Vite
- **Language**: TypeScript (strict mode)
- **State**: Zustand (single store)
- **Styling**: Tailwind CSS v4
- **3D**: React Three Fiber + drei
- **UI Components**: Radix UI primitives
- **Routing**: React Router v7
- **Build**: Vite with ESM

**Architecture:**
```
depot/console/
├── src/
│   ├── main.tsx              # Entry point
│   ├── App.tsx               # Router setup
│   ├── store.ts              # Zustand global state (single source of truth)
│   ├── components/           # React components
│   │   ├── scene/            # React Three Fiber 3D components
│   │   ├── teleop/           # Teleoperation UI panels
│   │   └── ui/               # Radix UI + CVA primitives
│   ├── views/                # Page-level components
│   ├── hooks/                # Custom React hooks
│   │   ├── useRoverConnection.ts   # WebSocket teleop
│   │   ├── useVideoStream.ts       # 360 video stream
│   │   ├── useGamepad.ts           # Gamepad input polling
│   │   ├── useKeyboard.ts          # Keyboard input handling
│   │   └── useDiscovery.ts         # Rover discovery service
│   └── lib/
│       ├── types.ts          # TypeScript type definitions
│       ├── protocol.ts       # Binary protocol codec
│       └── utils.ts          # Utility functions
```

**Critical Files:**
- Store: `depot/console/src/store.ts` (~400 lines)
- Types: `depot/console/src/lib/types.ts` (~300 lines)
- Protocol: `depot/console/src/lib/protocol.ts` (~200 lines)
- Rover connection: `depot/console/src/hooks/useRoverConnection.ts` (~250 lines)
- Video stream: `depot/console/src/hooks/useVideoStream.ts` (~150 lines)
- 3D scene: `depot/console/src/components/scene/Scene.tsx` (~200 lines)

## State Management Review (Zustand)

### Store Architecture

**Location**: `depot/console/src/store.ts`

**Key Points to Review:**
- [ ] Single store created with `create<ConsoleState>()`
- [ ] State organized into logical domains (fleet, connection, telemetry, input, camera, video)
- [ ] Immutable updates (no direct state mutation)
- [ ] Partial updates via `set()` with object spread
- [ ] No Redux-style actions (direct setter methods)

**Store Domains:**

1. **Fleet Management**:
   - `rovers: RoverInfo[]` - List of discovered rovers
   - `selectedRoverId: string | null` - Currently selected rover
   - `selectRover(id)` - Select rover and update addresses

2. **Connection State**:
   - `roverAddress: string` - WebSocket teleop address (ws://localhost:4850)
   - `videoAddress: string` - WebSocket video address (ws://localhost:4851)
   - `connected: boolean` - Connection status
   - `latencyMs: number` - Round-trip latency

3. **Telemetry** (Real-time Rover State):
   - `mode: Mode` - Operational mode (Idle, Teleop, etc.)
   - `pose: Pose` - Position (x, y, theta)
   - `velocity: Twist` - Current velocity
   - `power: PowerStatus` - Battery voltage, current
   - `temperatures: TempStatus` - Motor and controller temps

4. **Input**:
   - `input: GamepadInput` - Normalized gamepad/keyboard input
   - `inputSource: InputSource` - "gamepad" | "keyboard" | "none"

5. **Camera**:
   - `cameraMode: CameraMode` - ThirdPerson, FirstPerson, FreeLook
   - `cameraSettings` - FOV, distance, offset

6. **Video**:
   - `videoFrame: string | null` - Blob URL for current frame
   - `videoConnected: boolean`
   - `videoFps: number`

**Example Pattern:**
```typescript
// Good: Zustand store with domain slices
export const useConsoleStore = create<ConsoleState>((set) => ({
  // Fleet state
  rovers: [],
  selectedRoverId: null,
  selectRover: (id: string) =>
    set((state) => {
      const rover = state.rovers.find((r) => r.id === id);
      return {
        selectedRoverId: id,
        roverAddress: rover ? `ws://${rover.hostname}:4850` : state.roverAddress,
        videoAddress: rover ? `ws://${rover.hostname}:4851` : state.videoAddress,
      };
    }),

  // Telemetry state
  mode: Mode.Disabled,
  pose: { x: 0, y: 0, theta: 0 },
  updateTelemetry: (telemetry: Partial<Telemetry>) =>
    set((state) => ({
      ...state,
      ...telemetry, // Partial merge
    })),

  // Connection state
  connected: false,
  setConnected: (connected: boolean) => set({ connected }),
}));
```

**Red Flags:**
- Direct state mutation (`state.rovers.push(...)`)
- Missing immutability in updates
- No TypeScript types for state shape
- Large monolithic state (should be split into domains)
- Computed values stored in state (should be derived)

**See**: [Zustand Best Practices](https://docs.pmnd.rs/zustand/guides/practice-with-no-store-actions)

### State Consumption in Components

**Key Points to Review:**
- [ ] Use `useConsoleStore()` hook to access state
- [ ] Selector functions for performance (only re-render on relevant changes)
- [ ] No prop drilling (state accessed directly from store)

**Example Pattern:**
```typescript
// Good: Selector for specific state slice
function TelemetryPanel() {
  const { mode, pose, velocity } = useConsoleStore((state) => ({
    mode: state.mode,
    pose: state.pose,
    velocity: state.velocity,
  }));

  return (
    <div>
      <div>Mode: {ModeLabels[mode]}</div>
      <div>Position: ({pose.x.toFixed(2)}, {pose.y.toFixed(2)})</div>
      <div>Velocity: {velocity.linear.toFixed(2)} m/s</div>
    </div>
  );
}

// Bad: Selecting entire state (re-renders on any state change)
const state = useConsoleStore();  // ❌ Don't do this
```

## TypeScript Patterns Review

### Type Definitions

**Location**: `depot/console/src/lib/types.ts`

**Key Points to Review:**
- [ ] Enums defined with `as const` pattern
- [ ] Type aliases derived from enum keys
- [ ] Interfaces for object shapes (not types)
- [ ] No `any` types (use `unknown` or proper types)
- [ ] Strict null checks enabled

**Example Pattern:**
```typescript
// Good: Const enum with type alias
export const Mode = {
  Disabled: 0,
  Idle: 1,
  Teleop: 2,
  Autonomous: 3,
  EStop: 4,
  Fault: 5,
} as const;

export type Mode = (typeof Mode)[keyof typeof Mode];

// Good: Label map for UI display
export const ModeLabels: Record<Mode, string> = {
  [Mode.Disabled]: "Disabled",
  [Mode.Idle]: "Idle",
  [Mode.Teleop]: "Teleop",
  [Mode.Autonomous]: "Autonomous",
  [Mode.EStop]: "E-Stop",
  [Mode.Fault]: "Fault",
};

// Good: Interface for objects
export interface Telemetry {
  mode: Mode;
  pose: Pose;
  velocity: Twist;
  power: PowerStatus;
  temperatures: TempStatus;
}

// Good: Discriminated union for input source
export type InputSource = "gamepad" | "keyboard" | "none";
```

**Red Flags:**
- String enums instead of numeric (breaks binary protocol)
- `type` used for objects (use `interface`)
- Missing null checks
- `any` types
- Duplicate type definitions

### Component Props

**Key Points to Review:**
- [ ] Props interfaces defined with `interface` keyword
- [ ] Optional props use `?` operator
- [ ] Destructured in function parameters
- [ ] Children typed with `React.ReactNode`

**Example Pattern:**
```typescript
// Good: Props interface
interface TelemetryPanelProps {
  className?: string;
  showAdvanced?: boolean;
}

export function TelemetryPanel({ className, showAdvanced = false }: TelemetryPanelProps) {
  // ...
}
```

## WebSocket Communication Review

### Binary Protocol Implementation

**Location**: `depot/console/src/lib/protocol.ts`

**Message Types:**
- Commands (Console → Rover): `0x01-0x0F`
- Telemetry (Rover → Console): `0x10-0x1F`
- Video (Rover → Console): `0x20-0x2F`

**Key Points to Review:**
- [ ] Binary encoding uses `DataView` with little-endian
- [ ] Message type byte at offset 0
- [ ] Payload follows type byte
- [ ] Bounds checking before reading
- [ ] No string encoding in critical path (use binary for performance)

**Command Encoding:**
```typescript
// Good: Binary command encoding
export function encodeTwist(twist: Twist): ArrayBuffer {
  const buffer = new ArrayBuffer(25);  // 1 + 3*8 bytes
  const view = new DataView(buffer);

  view.setUint8(0, MSG_TWIST);                    // Message type
  view.setFloat64(1, twist.linear, true);          // Little-endian f64
  view.setFloat64(9, twist.angular, true);
  view.setUint8(17, twist.boost ? 1 : 0);

  return buffer;
}

// Bad: JSON encoding (too slow for 100Hz)
const json = JSON.stringify({ type: "twist", ...twist }); // ❌ Inefficient
```

**Telemetry Decoding:**
```typescript
// Good: Binary telemetry decoding with bounds check
export function decodeTelemetry(data: ArrayBuffer): Telemetry {
  if (data.byteLength < 90) {
    throw new Error(`Telemetry frame too short: ${data.byteLength} bytes`);
  }

  const view = new DataView(data);
  const type = view.getUint8(0);

  if (type !== MSG_TELEMETRY) {
    throw new Error(`Invalid message type: ${type}`);
  }

  return {
    mode: view.getUint8(1),
    pose: {
      x: view.getFloat64(2, true),
      y: view.getFloat64(10, true),
      theta: view.getFloat32(18, true),
    },
    velocity: {
      linear: view.getFloat32(22, true),
      angular: view.getFloat32(26, true),
      boost: view.getUint8(30) !== 0,
    },
    // ... more fields
  };
}
```

**See**: [websocket-protocols.md](websocket-protocols.md) for complete protocol reference.

### WebSocket Connection Management

**Location**: `depot/console/src/hooks/useRoverConnection.ts`

**Key Points to Review:**
- [ ] WebSocket created with `new WebSocket(url)`
- [ ] Event listeners: `onopen`, `onmessage`, `onclose`, `onerror`
- [ ] Binary type set to `"arraybuffer"`
- [ ] Auto-reconnect with exponential backoff
- [ ] Cleanup on unmount (close socket)
- [ ] Error handling doesn't crash app

**Example Pattern:**
```typescript
// Good: WebSocket with cleanup
export function useRoverConnection() {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const address = useConsoleStore((state) => state.roverAddress);

  useEffect(() => {
    const socket = new WebSocket(address);
    socket.binaryType = "arraybuffer";  // Critical for binary protocol

    socket.onopen = () => {
      console.log("Connected to rover");
      useConsoleStore.getState().setConnected(true);
    };

    socket.onmessage = (event: MessageEvent) => {
      const telemetry = decodeTelemetry(event.data);
      useConsoleStore.getState().updateTelemetry(telemetry);
    };

    socket.onclose = () => {
      console.log("Disconnected from rover");
      useConsoleStore.getState().setConnected(false);
      // Reconnect after 3s
      setTimeout(() => setWs(null), 3000);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    setWs(socket);

    // Cleanup on unmount
    return () => {
      socket.close();
    };
  }, [address]);

  return { ws };
}
```

**Red Flags:**
- No `binaryType = "arraybuffer"` (defaults to Blob, slower)
- Missing cleanup (memory leak)
- No reconnection logic
- Errors thrown instead of logged
- No timeout handling

### Command Transmission

**Key Points to Review:**
- [ ] Commands sent at appropriate rate (100Hz for twist)
- [ ] Heartbeat sent periodically (10Hz)
- [ ] No commands sent when disconnected
- [ ] Binary encoding used (not JSON)

**Example Pattern:**
```typescript
// Good: Command sending at 100Hz
useEffect(() => {
  if (!ws || !connected) return;

  const interval = setInterval(() => {
    const input = useConsoleStore.getState().input;
    const twist = { linear: input.linear, angular: input.angular, boost: input.boost };
    const buffer = encodeTwist(twist);
    ws.send(buffer);
  }, 10);  // 100Hz = 10ms period

  return () => clearInterval(interval);
}, [ws, connected]);

// Good: Heartbeat at 10Hz
useEffect(() => {
  if (!ws || !connected) return;

  const interval = setInterval(() => {
    const buffer = encodeHeartbeat();
    ws.send(buffer);
  }, 100);  // 10Hz = 100ms period

  return () => clearInterval(interval);
}, [ws, connected]);
```

## Safety Features Review

### Page Visibility Tracking

**Purpose**: Stop sending motor commands when tab loses focus (user switches tabs).

**Key Points to Review:**
- [ ] `document.visibilityState` monitored
- [ ] Commands stopped when `hidden`
- [ ] Input cleared when tab not visible
- [ ] Warning shown to user

**Example Pattern:**
```typescript
// Good: Page visibility tracking
useEffect(() => {
  const handleVisibilityChange = () => {
    if (document.hidden) {
      // Stop all commands
      useConsoleStore.getState().setInput({
        linear: 0,
        angular: 0,
        boost: false,
      });
      useConsoleStore.getState().setInputSource("none");
      console.warn("Tab hidden, stopping commands");
    }
  };

  document.addEventListener("visibilitychange", handleVisibilityChange);
  return () => document.removeEventListener("visibilitychange", handleVisibilityChange);
}, []);
```

**Red Flags:**
- No visibility tracking (rover continues moving when tab hidden)
- Commands sent regardless of focus state

### E-Stop Button

**Key Points to Review:**
- [ ] Prominent e-stop button in UI
- [ ] Sends e-stop command immediately on click
- [ ] Visual feedback (overlay, color change)
- [ ] Keyboard shortcut (e.g., Space bar)

**Example Pattern:**
```typescript
// Good: E-Stop button
function EStopButton() {
  const { ws } = useRoverConnection();

  const handleEStop = () => {
    if (!ws) return;
    const buffer = encodeEStop();
    ws.send(buffer);
    // Visual feedback
    useConsoleStore.getState().addToast({
      title: "E-Stop Activated",
      variant: "destructive",
    });
  };

  return (
    <Button
      variant="destructive"
      size="lg"
      onClick={handleEStop}
      className="fixed top-4 right-4 z-50"
    >
      <AlertTriangle className="mr-2" />
      E-STOP
    </Button>
  );
}
```

## Input Handling Review

### Gamepad Input

**Location**: `depot/console/src/hooks/useGamepad.ts`

**Key Points to Review:**
- [ ] Polling via `requestAnimationFrame` (not event-based)
- [ ] Dead zone applied (e.g., 0.1 threshold)
- [ ] Axes normalized to [-1, 1]
- [ ] Button state tracked
- [ ] Cleanup on unmount

**Example Pattern:**
```typescript
// Good: Gamepad polling with deadzone
export function useGamepad() {
  const [input, setInput] = useState<GamepadInput>({ linear: 0, angular: 0, boost: false });

  useEffect(() => {
    let frameId: number;

    const poll = () => {
      const gamepads = navigator.getGamepads();
      const gamepad = gamepads[0];

      if (gamepad) {
        const DEADZONE = 0.1;

        // Left stick Y (inverted): linear
        let linear = -gamepad.axes[1];
        if (Math.abs(linear) < DEADZONE) linear = 0;

        // Right stick X: angular
        let angular = gamepad.axes[2];
        if (Math.abs(angular) < DEADZONE) angular = 0;

        // Button 0 (A): boost
        const boost = gamepad.buttons[0].pressed;

        setInput({ linear, angular, boost });
        useConsoleStore.getState().setInputSource("gamepad");
      }

      frameId = requestAnimationFrame(poll);
    };

    frameId = requestAnimationFrame(poll);
    return () => cancelAnimationFrame(frameId);
  }, []);

  return input;
}
```

**Red Flags:**
- Event-based (gamepad API doesn't support events reliably)
- No dead zone (jittery input)
- Axes not normalized
- Missing cleanup

### Keyboard Input

**Location**: `depot/console/src/hooks/useKeyboard.ts`

**Key Points to Review:**
- [ ] Global listeners on `document` or `window`
- [ ] Key state tracked in `Set` or object
- [ ] Input normalized to [-1, 1]
- [ ] Cleanup removes listeners
- [ ] Doesn't interfere with text inputs

**Example Pattern:**
```typescript
// Good: Keyboard input with state tracking
export function useKeyboard() {
  const [keys, setKeys] = useState<Set<string>>(new Set());

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't capture if typing in input
      if (e.target instanceof HTMLInputElement) return;

      setKeys((prev) => new Set(prev).add(e.code));
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      setKeys((prev) => {
        const next = new Set(prev);
        next.delete(e.code);
        return next;
      });
    };

    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("keyup", handleKeyUp);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  // Convert keys to input
  const input = useMemo(() => {
    let linear = 0;
    let angular = 0;

    if (keys.has("KeyW")) linear += 1;
    if (keys.has("KeyS")) linear -= 1;
    if (keys.has("KeyA")) angular += 1;
    if (keys.has("KeyD")) angular -= 1;

    return { linear, angular, boost: keys.has("ShiftLeft") };
  }, [keys]);

  if (input.linear !== 0 || input.angular !== 0) {
    useConsoleStore.getState().setInputSource("keyboard");
  }

  return input;
}
```

## 3D Visualization Review (React Three Fiber)

### Scene Setup

**Location**: `depot/console/src/components/scene/Scene.tsx`

**Key Points to Review:**
- [ ] `<Canvas>` wraps all Three.js components
- [ ] Camera FOV reasonable (60-75°)
- [ ] Lighting includes ambient + directional
- [ ] Shadows enabled if needed
- [ ] Performance monitoring (`<Perf>` in dev)

**Example Pattern:**
```typescript
// Good: Canvas setup with lighting
export function Scene() {
  return (
    <Canvas shadows camera={{ fov: 60, position: [0, 5, 10] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} castShadow />
      <RoverModel />
      <Ground />
      <EquirectangularSky />
      <CameraController />
    </Canvas>
  );
}
```

### Rover Model Animation

**Key Points to Review:**
- [ ] Position interpolated with `lerp` (smooth motion)
- [ ] Angle interpolation handles wraparound (0° ↔ 360°)
- [ ] Delta time used for frame-rate independence
- [ ] Model updates on telemetry change

**Example Pattern:**
```typescript
// Good: Smooth position interpolation
function RoverModel() {
  const pose = useConsoleStore((state) => state.pose);
  const ref = useRef<THREE.Group>(null);

  useFrame((state, delta) => {
    if (!ref.current) return;

    // Lerp position
    ref.current.position.x = THREE.MathUtils.lerp(ref.current.position.x, pose.x, delta * 10);
    ref.current.position.z = THREE.MathUtils.lerp(ref.current.position.z, -pose.y, delta * 10);

    // Lerp rotation (handle wraparound)
    const targetRot = -pose.theta;
    const currentRot = ref.current.rotation.y;
    const diff = ((targetRot - currentRot + Math.PI) % (2 * Math.PI)) - Math.PI;
    ref.current.rotation.y += diff * delta * 10;
  });

  return (
    <group ref={ref}>
      {/* Rover geometry */}
    </group>
  );
}
```

**Red Flags:**
- Direct assignment (no interpolation, jumpy motion)
- No wraparound handling for angles
- Fixed delta (not frame-rate independent)

### Memory Management

**Key Points to Review:**
- [ ] Textures disposed on unmount
- [ ] Geometries disposed when not needed
- [ ] Materials disposed when not needed
- [ ] Blob URLs revoked with `URL.revokeObjectURL()`

**Example Pattern:**
```typescript
// Good: Texture cleanup
useEffect(() => {
  if (!videoFrame) return;

  const texture = new THREE.TextureLoader().load(videoFrame);

  return () => {
    texture.dispose();  // Free GPU memory
    URL.revokeObjectURL(videoFrame);  // Free blob URL
  };
}, [videoFrame]);
```

**See**: [performance.md](performance.md) for optimization strategies.

## Component Patterns Review

### File Naming

**Convention**: PascalCase for components, camelCase for hooks/utils.

**Key Points to Review:**
- [ ] Components: `TelemetryPanel.tsx`, `RoverModel.tsx`
- [ ] Hooks: `useGamepad.ts`, `useRoverConnection.ts`
- [ ] Utils: `utils.ts`, `protocol.ts`
- [ ] All TypeScript (`.ts` or `.tsx`)

### Component Structure

**Key Points to Review:**
- [ ] Functional components (not class components)
- [ ] Props destructured in parameters
- [ ] Hooks at top of function (before any conditional)
- [ ] Event handlers defined inside component
- [ ] Return JSX with semantic HTML

**Example Pattern:**
```typescript
// Good: Component structure
interface TelemetryPanelProps {
  className?: string;
}

export function TelemetryPanel({ className }: TelemetryPanelProps) {
  // 1. Zustand store access
  const { mode, pose, velocity } = useConsoleStore((state) => ({
    mode: state.mode,
    pose: state.pose,
    velocity: state.velocity,
  }));

  // 2. Local state
  const [expanded, setExpanded] = useState(false);

  // 3. Effects
  useEffect(() => {
    // Side effects
  }, []);

  // 4. Event handlers
  const handleToggle = () => setExpanded(!expanded);

  // 5. Render
  return (
    <Card className={cn("p-4", className)}>
      <h2>Telemetry</h2>
      <div>Mode: {ModeLabels[mode]}</div>
      <div>Position: ({pose.x.toFixed(2)}, {pose.y.toFixed(2)})</div>
      <Button onClick={handleToggle}>Toggle</Button>
    </Card>
  );
}
```

## Testing and Linting

### ESLint Configuration

**Key Points to Review:**
- [ ] TypeScript ESLint rules enabled
- [ ] React hooks rules enforced
- [ ] No `any` types allowed
- [ ] Unused vars detected
- [ ] Import order enforced

**Run linting:**
```bash
npm run lint
```

### Type Checking

**Key Points to Review:**
- [ ] No TypeScript errors: `npm run build`
- [ ] Strict mode enabled in `tsconfig.json`
- [ ] All imports have types

### Build Verification

**Key Points to Review:**
- [ ] Vite build succeeds: `npm run build`
- [ ] Bundle size reasonable (<1MB for main chunk)
- [ ] No console errors in production build

## References and Additional Resources

For more detailed information, see:
- [websocket-protocols.md](websocket-protocols.md) - Binary protocol encoding/decoding
- [performance.md](performance.md) - React rendering optimization and memory management
- [CLAUDE.md](/Users/cam/Developer/muni/CLAUDE.md) - Project-wide conventions

## Quick Review Commands

```bash
# Lint code
npm run lint

# Type check and build
npm run build

# Dev server with hot-reload
npm run dev

# Run tests (if configured)
npm run test
```
