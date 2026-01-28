---
name: networking-servers
version: "2.0.0"
description: |
  Multiplayer systems, netcode, game servers, synchronization, and anti-cheat.
  Build scalable, responsive multiplayer experiences.
sasmp_version: "1.3.0"
bonded_agent: 05-networking-multiplayer
bond_type: PRIMARY_BOND

parameters:
  - name: architecture
    type: string
    required: false
    validation:
      enum: [client_server, p2p, hybrid, dedicated]
  - name: framework
    type: string
    required: false
    validation:
      enum: [photon, mirror, netcode, fishnet, custom]

retry_policy:
  enabled: true
  max_attempts: 5
  backoff: exponential
  jitter: true

observability:
  log_events: [start, complete, error, reconnect]
  metrics: [latency_ms, packet_loss, bandwidth_kbps, player_count]
---

# Networking & Game Servers

## Network Architecture

```
CLIENT-SERVER (AUTHORITATIVE):
┌─────────────────────────────────────────────────────────────┐
│                   DEDICATED SERVER                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • Authoritative game state                          │   │
│  │  • Physics simulation                                │   │
│  │  • Hit validation                                    │   │
│  │  • Anti-cheat checks                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│       ↑↓              ↑↓              ↑↓              ↑↓    │
│   [Client A]    [Client B]    [Client C]    [Client D]     │
│   └─ Prediction  └─ Prediction  └─ Prediction  └─ Prediction│
└─────────────────────────────────────────────────────────────┘
```

## Netcode Implementation

### Client Prediction with Reconciliation

```csharp
// ✅ Production-Ready: Prediction + Reconciliation System
public class NetworkedMovement : NetworkBehaviour
{
    private struct InputPayload
    {
        public uint Tick;
        public uint Sequence;
        public Vector2 MoveInput;
        public bool Jump;
    }

    private Queue<InputPayload> _pendingInputs = new();
    private CircularBuffer<PlayerState> _stateHistory;
    private uint _inputSequence;

    private void Update()
    {
        if (!IsOwner) return;

        // Capture input
        var input = new InputPayload
        {
            Tick = NetworkManager.ServerTime.Tick,
            Sequence = _inputSequence++,
            MoveInput = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical")),
            Jump = Input.GetButtonDown("Jump")
        };

        // Predict locally (immediate response)
        ApplyInput(input);

        // Store for reconciliation
        _pendingInputs.Enqueue(input);
        _stateHistory.Add(GetCurrentState());

        // Send to server
        SendInputServerRpc(input);
    }

    [ClientRpc]
    private void ReconcileClientRpc(uint ackedSequence, PlayerState serverState)
    {
        if (!IsOwner) return;

        // Remove acknowledged inputs
        while (_pendingInputs.Count > 0 && _pendingInputs.Peek().Sequence <= ackedSequence)
            _pendingInputs.Dequeue();

        // Check for prediction error
        var predictedState = _stateHistory.Get(ackedSequence);
        if (Vector3.Distance(predictedState.Position, serverState.Position) > 0.01f)
        {
            // Reconcile: reset to server state, replay pending inputs
            SetState(serverState);
            foreach (var input in _pendingInputs)
                ApplyInput(input);
        }
    }
}
```

### Lag Compensation

```csharp
// ✅ Production-Ready: Server-Side Rewind
public class LagCompensation : NetworkBehaviour
{
    private const int HISTORY_SIZE = 128;
    private const float MAX_REWIND_MS = 200f;

    private CircularBuffer<PositionSnapshot>[] _playerHistory;

    [ServerRpc]
    public void RequestHitValidationServerRpc(uint shooterClientId,
        Vector3 shootOrigin, Vector3 shootDirection, uint targetClientId)
    {
        // Get shooter's RTT
        float rtt = NetworkManager.ConnectedClients[shooterClientId].RTT;
        float rewindTime = Mathf.Min(rtt / 2f + 50f, MAX_REWIND_MS);

        // Get target's position at that time
        var targetPastPosition = GetPositionAtTime(targetClientId,
            Time.time - (rewindTime / 1000f));

        // Perform hit check at rewound position
        if (Physics.Raycast(shootOrigin, shootDirection, out var hit))
        {
            if (Vector3.Distance(hit.point, targetPastPosition) < 1f)
            {
                // Valid hit - apply damage
                ApplyDamage(targetClientId, 25);
            }
        }
    }
}
```

## Server Architecture

```
SCALABLE SERVER ARCHITECTURE:
┌─────────────────────────────────────────────────────────────┐
│  LOAD BALANCER (Global)                                      │
│         ↓                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  MATCHMAKING SERVICE                                  │   │
│  │  • Player queuing                                     │   │
│  │  • Skill-based matching                               │   │
│  │  • Session creation                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│         ↓                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  GAME SERVERS (Auto-scaled)                          │   │
│  │  [US-East] [US-West] [EU] [Asia]                     │   │
│  │  Each region: 10-1000 instances                       │   │
│  └─────────────────────────────────────────────────────┘   │
│         ↓                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  DATABASE CLUSTER                                     │   │
│  │  • Player profiles                                    │   │
│  │  • Match history                                      │   │
│  │  • Leaderboards                                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Bandwidth Optimization

| Technique | Savings | Implementation |
|-----------|---------|----------------|
| Delta Compression | 60-80% | Only send changed values |
| Quantization | 50-70% | Float → fixed-point |
| Bit Packing | 30-50% | Custom serialization |
| Interest Management | 70-90% | Only send relevant data |
| Priority Queue | Variable | Less important = less often |

## Anti-Cheat Strategies

```
ANTI-CHEAT LAYERS:
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: Server Authority                                   │
│  → All game state validated on server                       │
│  → Never trust client                                       │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: Sanity Checks                                      │
│  → Movement speed limits                                    │
│  → Action rate limits                                       │
│  → Position validation                                      │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: Statistical Detection                              │
│  → Inhuman accuracy patterns                                │
│  → Impossible reaction times                                │
│  → Abnormal session metrics                                 │
├─────────────────────────────────────────────────────────────┤
│  LAYER 4: Client-Side (Optional)                             │
│  → Memory scanning (EAC, BattlEye)                          │
│  → Process monitoring                                       │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Troubleshooting

```
┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Players rubber-banding / teleporting               │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Increase interpolation buffer                             │
│ → Add jitter buffer for packets                             │
│ → Smooth corrections (lerp, not snap)                       │
│ → Check prediction code determinism                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Desyncs between clients                            │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Use fixed-point math                                      │
│ → Sync random seeds                                         │
│ → Periodic full-state resync                                │
│ → State hash comparison                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: High bandwidth usage                               │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Implement delta compression                               │
│ → Reduce tick rate for non-critical data                    │
│ → Use interest management                                   │
│ → Quantize position/rotation values                         │
└─────────────────────────────────────────────────────────────┘
```

## Framework Comparison

| Framework | Best For | Max Players | Learning Curve |
|-----------|----------|-------------|----------------|
| Photon | Quick start | 16-32 | Easy |
| Mirror | Open source | 100+ | Medium |
| Netcode for GO | Unity official | 100+ | Medium |
| FishNet | Performance | 200+ | Medium |
| Custom | Full control | Unlimited | Hard |

---

**Use this skill**: When building multiplayer, designing servers, or implementing anti-cheat.
