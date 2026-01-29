---
name: reachy-mini
description: |
  Complete SDK for controlling Reachy Mini robot - head movement, antennas, camera, audio, motion recording/playback.
  Covers architecture (daemon/client), deployment modes (USB, wireless, simulation, on-Pi), and app distribution.
  Also includes advanced application patterns: MovementManager, layered motion, audio-reactive movement, face tracking,
  LLM tool systems, and OpenAI realtime integration.
  Use when: (1) Writing code to control Reachy Mini, (2) Moving the robot head or antennas, (3) Accessing camera/video,
  (4) Playing/recording audio, (5) Recording or playing back motions, (6) Looking at points in image or world space,
  (7) Understanding robot capabilities, (8) Connecting to real or simulated robot, (9) Building conversational AI apps,
  (10) Integrating with LLMs/OpenAI, (11) Deploying apps to robot, (12) Any robotics task with Reachy Mini.
---

# Reachy Mini SDK

## Quick Start

```python
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
import numpy as np

with ReachyMini() as robot:
    robot.wake_up()

    # Move head
    pose = create_head_pose(x=0, y=0, z=0, roll=0, pitch=10, yaw=20, degrees=True)
    robot.goto_target(head=pose, antennas=[0.3, -0.3], duration=1.0)

    # Get camera frame
    frame = robot.media.get_frame()  # Returns BGR numpy array

    robot.goto_sleep()
```

## Connection Options

```python
# Local USB connection (default)
ReachyMini()

# Network discovery
ReachyMini(localhost_only=False)

# Simulation mode
ReachyMini(use_sim=True)

# Auto-spawn daemon
ReachyMini(spawn_daemon=True)

# Full options
ReachyMini(
    robot_name="reachy_mini",       # Robot identifier
    localhost_only=True,            # True=local daemon, False=network discovery
    spawn_daemon=False,             # Auto-spawn daemon process
    use_sim=False,                  # Use MuJoCo simulation
    timeout=5.0,                    # Connection timeout (seconds)
    automatic_body_yaw=True,        # Auto body yaw in IK
    log_level="INFO",               # "DEBUG", "INFO", "WARNING", "ERROR"
    media_backend="default"         # "default", "gstreamer", "webrtc", "no_media"
)
```

## Head & Antenna Control

### Creating Poses

```python
from reachy_mini.utils import create_head_pose

# By position and rotation (degrees by default)
pose = create_head_pose(x=0, y=0, z=0, roll=0, pitch=15, yaw=-10, degrees=True)

# In radians
pose = create_head_pose(pitch=0.26, yaw=-0.17, degrees=False)

# Position in millimeters
pose = create_head_pose(x=50, y=0, z=30, mm=True)
```

### Moving the Robot

```python
from reachy_mini.motion.goto_move import InterpolationTechnique

# Immediate position (no interpolation)
robot.set_target(head=pose, antennas=[0.5, -0.5], body_yaw=0.1)

# Smooth motion with duration
robot.goto_target(
    head=pose,
    antennas=[0.5, -0.5],  # [right, left] in radians
    duration=1.0,
    method=InterpolationTechnique.MIN_JERK,
    body_yaw=0.0
)
```

**Interpolation methods:**
- `LINEAR` - Linear interpolation
- `MIN_JERK` - Default, smoothest motion
- `EASE_IN_OUT` - Smooth start and end
- `CARTOON` - Exaggerated animation style

### Look-At Functions

```python
# Look at pixel coordinates in camera image
robot.look_at_image(u=320, v=240, duration=0.5)

# Look at 3D world point (meters from robot origin)
robot.look_at_world(x=0.5, y=0.1, z=0.3, duration=0.5)

# Get pose without moving
pose = robot.look_at_image(u=320, v=240, perform_movement=False)
```

### Antenna Values

Antennas are `[right_angle, left_angle]` in **radians**:
- `0.0` = antennas down/closed
- Positive = antennas up/open
- Typical range: `-0.5` to `1.0` radians

## State Queries

```python
# Current head pose (4x4 matrix)
pose = robot.get_current_head_pose()

# Joint positions
head_joints, antenna_joints = robot.get_current_joint_positions()
# head_joints: 7 values (body_rotation + 6 stewart platform)
# antenna_joints: 2 values [right, left]

# Antenna positions only
antennas = robot.get_present_antenna_joint_positions()  # [right, left]
```

## Motor Control

```python
# Enable/disable all motors
robot.enable_motors()
robot.disable_motors()

# Specific motors
robot.enable_motors(ids=["right_antenna", "left_antenna"])
robot.disable_motors(ids=["body_rotation"])
```

**Motor IDs:** `"body_rotation"`, `"stewart_1"` through `"stewart_6"`, `"right_antenna"`, `"left_antenna"`

```python
# Gravity compensation (requires Placo kinematics)
robot.enable_gravity_compensation()
robot.disable_gravity_compensation()
```

## Behaviors

```python
robot.wake_up()     # Wake animation + sound
robot.goto_sleep()  # Sleep position + sound
```

## Camera

```python
# Get frame (BGR numpy array, or None if unavailable)
frame = robot.media.get_frame()

# Camera properties
width, height = robot.media.camera.resolution
fps = robot.media.camera.framerate
K = robot.media.camera.K  # 3x3 intrinsic matrix
D = robot.media.camera.D  # Distortion coefficients

# Change resolution
from reachy_mini.media.camera.camera_constants import CameraResolution
robot.media.camera.set_resolution(CameraResolution.R1920x1080at30fps)
```

**Common resolutions:** `R1280x720at30fps`, `R1280x720at60fps`, `R1920x1080at30fps`, `R1920x1080at60fps`, `R3840x2160at30fps`

## Audio

```python
# Play sound file
robot.media.play_sound("wake_up.wav")

# Record audio
robot.media.start_recording()
sample = robot.media.get_audio_sample()  # numpy array
robot.media.stop_recording()

# Stream audio output
robot.media.start_playing()
robot.media.push_audio_sample(audio_data)
robot.media.stop_playing()

# Audio specs
sample_rate = robot.media.get_input_audio_samplerate()  # 16000 Hz
channels = robot.media.get_input_channels()  # 2

# Direction of Arrival (ReSpeaker only)
angle, valid = robot.media.get_DoA()  # angle in radians (0=left, pi/2=front, pi=right)
```

## Motion Recording & Playback

### Recording

```python
robot.start_recording()
# ... perform motions manually or via code ...
recorded_data = robot.stop_recording()
# Returns list of dicts with timestamps, poses, joint positions
```

### Playing Recorded Moves

```python
from reachy_mini.motion.recorded_move import RecordedMoves

# Load move library from HuggingFace
moves = RecordedMoves("pollen-robotics/reachy-mini-dances-library")

# List available moves
print(moves.list_moves())

# Play a move
move = moves.get("dance_name")
robot.play_move(move, initial_goto_duration=1.0, sound=True)

# Async playback
await robot.async_play_move(move)
```

## Kinematics

Three engines available:

| Engine | Install | Speed | Features |
|--------|---------|-------|----------|
| AnalyticalKinematics | Default | Fast | Always available |
| PlacoKinematics | `pip install reachy_mini[placo_kinematics]` | Medium | Collision checking, gravity compensation |
| NNKinematics | `pip install reachy_mini[nn_kinematics]` | Very fast | Neural network based |

```python
# Direct kinematics access
from reachy_mini.kinematics.analytical import AnalyticalKinematics

kin = AnalyticalKinematics()
joint_angles = kin.ik(pose, body_yaw=0.0)  # Inverse kinematics: pose -> joints
pose = kin.fk(joint_angles)                 # Forward kinematics: joints -> pose
```

## Simulation

```python
# Start with simulation
robot = ReachyMini(use_sim=True)

# Or via daemon CLI
# reachy-mini-daemon --sim
```

## Common Patterns

### Face Tracking
```python
# Detect face, get center coordinates (u, v)
robot.look_at_image(u=face_center_x, v=face_center_y, duration=0.3)
```

### Expressive Movements
```python
# Happy - antennas up
robot.goto_target(antennas=[0.8, 0.8], duration=0.3)

# Sad - antennas down
robot.goto_target(antennas=[-0.3, -0.3], duration=0.5)

# Curious tilt
pose = create_head_pose(roll=15, pitch=10, degrees=True)
robot.goto_target(head=pose, duration=0.4)
```

### Idle Animation Loop
```python
import time
while True:
    robot.goto_target(head=create_head_pose(yaw=10, degrees=True), duration=2.0)
    time.sleep(2.0)
    robot.goto_target(head=create_head_pose(yaw=-10, degrees=True), duration=2.0)
    time.sleep(2.0)
```

## Reference Documentation

- **[Architecture & Deployment](references/architecture.md)** - Daemon/client split, deployment modes (USB, wireless, simulation), running code, app distribution
- **[API Reference](references/api_reference.md)** - Complete method signatures, all parameters and return types
- **[Motion Reference](references/motion_reference.md)** - Interpolation details, Move classes, GotoMove, RecordedMove
- **[Media Reference](references/media_reference.md)** - All camera resolutions, audio specs, backend options
- **[Application Patterns](references/application_patterns.md)** - Advanced patterns: MovementManager, layered motion, audio-reactive movement, face tracking, LLM tool systems, OpenAI realtime integration
