---
name: synchronization-algorithms
version: "2.0.0"
description: |
  Network synchronization, lag compensation, client prediction, and state
  consistency for responsive multiplayer games.
sasmp_version: "1.3.0"
bonded_agent: 05-networking-multiplayer
bond_type: PRIMARY_BOND

parameters:
  - name: technique
    type: string
    required: false
    validation:
      enum: [prediction, interpolation, reconciliation, rollback, lockstep]
  - name: game_type
    type: string
    required: false
    validation:
      enum: [fps, fighting, rts, mmo, racing]

retry_policy:
  enabled: true
  max_attempts: 5
  backoff: exponential
  jitter: true

observability:
  log_events: [start, complete, error, desync]
  metrics: [prediction_error_ms, rollback_count, resync_frequency]
---

# Multiplayer Synchronization

## Synchronization Techniques

```
┌─────────────────────────────────────────────────────────────┐
│                    SYNC TECHNIQUES OVERVIEW                  │
├─────────────────────────────────────────────────────────────┤
│  CLIENT PREDICTION:                                          │
│  → Execute input locally before server confirms             │
│  → Feels responsive, requires reconciliation               │
│  Best for: FPS, action games                                │
├─────────────────────────────────────────────────────────────┤
│  INTERPOLATION:                                              │
│  → Display positions between known states                   │
│  → Smooth visuals, adds latency                            │
│  Best for: Other players, NPCs                              │
├─────────────────────────────────────────────────────────────┤
│  ROLLBACK NETCODE:                                           │
│  → Rewind game state on correction                          │
│  → Re-simulate with corrected data                          │
│  Best for: Fighting games, precise timing                   │
├─────────────────────────────────────────────────────────────┤
│  LOCKSTEP:                                                   │
│  → All clients advance together                             │
│  → Deterministic, waits for slowest                        │
│  Best for: RTS, turn-based                                  │
└─────────────────────────────────────────────────────────────┘
```

## Client Prediction & Reconciliation

```
PREDICTION FLOW:
┌─────────────────────────────────────────────────────────────┐
│  Frame N:                                                    │
│  1. Capture input                                           │
│  2. Predict result locally (immediate response)            │
│  3. Store input + predicted state                          │
│  4. Send input to server                                   │
│                                                              │
│  Frame N+RTT:                                                │
│  5. Receive server state for Frame N                       │
│  6. Compare with stored prediction                         │
│  7. If mismatch: RECONCILE                                 │
│     a. Snap to server state                                │
│     b. Re-apply all inputs since Frame N                   │
│     c. Smooth correction to avoid visual pop               │
└─────────────────────────────────────────────────────────────┘
```

```csharp
// ✅ Production-Ready: Prediction Buffer
public class PredictionBuffer
{
    private const int BUFFER_SIZE = 128;
    private readonly PredictionEntry[] _buffer = new PredictionEntry[BUFFER_SIZE];

    public void Store(uint tick, InputPayload input, PlayerState predictedState)
    {
        int index = (int)(tick % BUFFER_SIZE);
        _buffer[index] = new PredictionEntry
        {
            Tick = tick,
            Input = input,
            PredictedState = predictedState
        };
    }

    public void Reconcile(uint serverTick, PlayerState serverState)
    {
        int index = (int)(serverTick % BUFFER_SIZE);
        var entry = _buffer[index];

        if (entry.Tick != serverTick) return; // Stale data

        float error = Vector3.Distance(entry.PredictedState.Position, serverState.Position);
        if (error < 0.01f) return; // Within tolerance

        // Misprediction detected - reconcile
        PlayerState currentState = serverState;

        // Re-simulate all inputs since server tick
        for (uint t = serverTick + 1; t <= CurrentTick; t++)
        {
            int idx = (int)(t % BUFFER_SIZE);
            if (_buffer[idx].Tick == t)
            {
                currentState = SimulateInput(currentState, _buffer[idx].Input);
            }
        }

        // Apply corrected state (with smoothing)
        ApplyCorrectedState(currentState);
    }
}
```

## Interpolation

```
INTERPOLATION BUFFER:
┌─────────────────────────────────────────────────────────────┐
│  RECEIVE: [State T-100ms] [State T-50ms] [State T-now]     │
│                                                              │
│  RENDER: Display interpolated position between T-100ms      │
│          and T-50ms based on current render time           │
│                                                              │
│  WHY: Always have two states to interpolate between        │
│       (render behind real-time by buffer amount)           │
│                                                              │
│  BUFFER SIZE:                                                │
│  • Too small: Choppy when packets delayed                  │
│  • Too large: Everything feels delayed                     │
│  • Typical: 100-200ms for other players                    │
└─────────────────────────────────────────────────────────────┘
```

## Rollback Netcode

```
ROLLBACK FLOW (Fighting Games):
┌─────────────────────────────────────────────────────────────┐
│  1. Execute frame with predicted opponent input             │
│  2. Store complete game state snapshot                      │
│  3. When actual input arrives:                              │
│     a. If matches prediction: continue                      │
│     b. If mismatch:                                         │
│        - Load snapshot from that frame                     │
│        - Re-simulate all frames with correct input         │
│        - "Rollback" visual to corrected state              │
│  4. Hide rollbacks with animation tricks                   │
└─────────────────────────────────────────────────────────────┘

ROLLBACK LIMITS:
• Max rollback: 7-8 frames (~116ms at 60fps)
• Beyond: Game stutters or desyncs
• Input delay trade-off: 0-3 frames pre-delay
```

## Lockstep Synchronization

```
LOCKSTEP (RTS Games):
┌─────────────────────────────────────────────────────────────┐
│  Frame 0: All clients send inputs                           │
│           Wait for all inputs                               │
│           Execute deterministically                         │
│                                                              │
│  Frame 1: Repeat                                            │
│                                                              │
│  REQUIREMENTS:                                               │
│  • Deterministic simulation (fixed-point math)             │
│  • Synchronized RNG seeds                                   │
│  • Identical execution order                               │
│                                                              │
│  PROS: Minimal bandwidth (only inputs)                      │
│  CONS: Latency = slowest player, input delay               │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Troubleshooting

```
┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Visible rubber-banding                             │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Increase interpolation buffer                             │
│ → Smooth reconciliation (lerp, not snap)                    │
│ → Add visual damping                                        │
│ → Check for consistent tick rate                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Clients desyncing                                  │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Use fixed-point math                                      │
│ → Sync random number seeds                                  │
│ → Periodic full-state resync                                │
│ → Add state hash verification                               │
│ → Check floating-point determinism                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Too many rollbacks (fighting games)                │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Add input delay frames (1-3)                              │
│ → Better input prediction                                   │
│ → Limit max rollback frames                                 │
│ → Disconnect players with bad connections                   │
└─────────────────────────────────────────────────────────────┘
```

## Technique Selection

| Game Type | Primary | Secondary | Latency Budget |
|-----------|---------|-----------|----------------|
| FPS | Prediction | Interpolation | 50-100ms |
| Fighting | Rollback | Input delay | 50-80ms |
| RTS | Lockstep | - | 200-500ms |
| MMO | Interpolation | Prediction | 100-200ms |
| Racing | Prediction | Extrapolation | 50-100ms |

---

**Use this skill**: When building multiplayer systems, optimizing netcode, or fixing desync issues.
