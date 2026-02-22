---
name: zeroth-bot
description: Zeroth Bot - 3D-printed open-source humanoid robot platform for sim-to-real and RL research. Affordable entry point for humanoid robotics.
version: 1.0.0
category: robotics-platform
author: K-Scale Labs
source: kscalelabs/zeroth-bot
license: MIT
trit: -1
trit_label: MINUS
color: "#8CC136"
verified: false
featured: false
---

# Zeroth Bot Skill

**Trit**: -1 (MINUS - specification/verification)
**Color**: #8CC136 (Lime Green)
**URI**: skill://zeroth-bot#8CC136

## Overview

Zeroth Bot (Z-Bot) is a 3D-printed open-source humanoid robot platform designed for sim-to-real research and RL experimentation. An affordable entry point for humanoid robotics.

## Specifications

```
┌────────────────────────────────────────────────────────────────┐
│                      ZEROTH BOT (Z-BOT)                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Height: ~40cm                                                 │
│  Weight: ~2kg                                                  │
│  DOF: 12 joints                                                │
│                                                                 │
│  Frame: 3D printed (PLA/PETG)                                  │
│  Actuators: Servo motors                                        │
│  Cost: ~$500 BOM                                               │
│                                                                 │
│  Ideal for:                                                     │
│  ├── Learning sim-to-real transfer                             │
│  ├── Testing RL policies at low cost                           │
│  ├── Educational robotics                                      │
│  └── Rapid prototyping                                         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Hardware BOM

| Component | Quantity | Notes |
|-----------|----------|-------|
| Servo motors | 12 | Standard hobby servos |
| 3D printed parts | Full set | STL files provided |
| MCU | 1 | ESP32 or Teensy |
| IMU | 1 | MPU6050 or similar |
| Power | 1 | 2S-3S LiPo |

## Training Pipeline

```python
from ksim.robots.zbot import ZBotConfig
from ksim import PPOTask

class ZBotWalking(PPOTask):
    robot = ZBotConfig(
        model_path="zbot.mjcf",
        servo_config={
            "kp": 50.0,
            "kd": 5.0,
            "torque_limit": 5.0,  # Smaller than K-Bot
        }
    )
    
    # Faster training due to simpler robot
    training_config = {
        "num_envs": 2048,
        "learning_rate": 5e-4,
    }
```

## GF(3) Triads

```
zeroth-bot (-1) ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
```

## Related Skills

- `kbot-humanoid` (-1): Larger flagship humanoid
- `ksim-rl` (-1): RL training library
- `kos-firmware` (+1): Firmware (kos-zbot variant)
- `urdf2mjcf` (-1): Model conversion

## Web Frontend

Z-Bot has a web-based control interface:
- Real-time telemetry visualization
- Manual joint control
- Policy deployment interface

```typescript
// From zbot-web-frontend
import { ZBotController } from '@kscale/zbot-web';

const controller = new ZBotController({
  endpoint: 'ws://zbot.local:8080',
});

await controller.connect();
await controller.setJointPositions({
  hip_pitch_l: 0.5,
  knee_l: -0.3,
});
```

## References

```bibtex
@misc{zerothbot2024,
  title={Zeroth Bot: 3D-Printed Open-Source Humanoid},
  author={K-Scale Labs},
  year={2024},
  url={https://github.com/kscalelabs/zeroth-bot}
}
```


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 2. Domain-Specific Languages

**Concepts**: DSL, wrapper, pattern-directed, embedding

### GF(3) Balanced Triad

```
zeroth-bot (−) + SDF.Ch2 (−) + [balancer] (−) = 0
```

**Skill Trit**: -1 (MINUS - verification)


### Connection Pattern

DSLs embed domain knowledge. This skill defines domain-specific operations.
