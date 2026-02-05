---
name: ros-bridge
version: 2.0.0
description: |
  Full robotics stack for AI agents. Connect to any ROS robot via rosbridge, control motors,
  read sensors, run vision models, explore autonomously, coordinate swarms, and expose as
  A2A agent with optional X402 payments. Complete robot-to-agent pipeline.
homepage: https://github.com/QUSD-ai/ros-bridge-skill
metadata:
  emoji: "🤖"
  category: robotics
  tags: ["ros", "robotics", "hardware", "rosbridge", "jetson", "ugv", "lidar", "a2a", "x402"]
---

# 🤖 ROS Bridge Skill

**Complete robot-to-agent pipeline.** Connect any ROS robot to AI agents with full control.

## What's Included

| Module | Description |
|--------|-------------|
| `rosbridge-client` | WebSocket client for rosbridge |
| `ros-tools` | VoltAgent tools: move, turn, stop, lidar |
| `vision-tools` | Camera capture, 9 CV detection modes |
| `sensor-tools` | Lidar, IMU, sensor fusion, pose estimation |
| `exploration-tools` | Mapping, frontier detection, path planning |
| `swarm-tools` | Multi-robot coordination, task allocation |
| `hardware-tools` | LED control, OLED display, gimbal |
| `robot-agent` | A2A agent factory for robot discovery |
| `x402-wrapper` | Paid robot API (charge per call) |

---

## Quick Start

### 1. Connect to Robot

```typescript
import { RosbridgeClient } from './rosbridge-client';

const robot = new RosbridgeClient('192.168.1.100', 9090);
await robot.connect();
```

### 2. Basic Control

```typescript
// Move forward 0.5 m/s for 2 seconds
robot.publish('/cmd_vel', 'geometry_msgs/Twist', {
  linear: { x: 0.5, y: 0, z: 0 },
  angular: { x: 0, y: 0, z: 0 }
});

// Turn left at 0.3 rad/s
robot.publish('/cmd_vel', 'geometry_msgs/Twist', {
  linear: { x: 0, y: 0, z: 0 },
  angular: { x: 0, y: 0, z: 0.3 }
});

// Stop
robot.publish('/cmd_vel', 'geometry_msgs/Twist', {
  linear: { x: 0, y: 0, z: 0 },
  angular: { x: 0, y: 0, z: 0 }
});
```

### 3. Read Sensors

```typescript
// Subscribe to LIDAR
robot.subscribe('/scan', 'sensor_msgs/LaserScan', (data) => {
  const minDistance = Math.min(...data.ranges.filter(r => r > 0));
  console.log(`Closest obstacle: ${minDistance.toFixed(2)}m`);
});

// Subscribe to odometry
robot.subscribe('/odom', 'nav_msgs/Odometry', (data) => {
  console.log(`Position: x=${data.pose.pose.position.x}, y=${data.pose.pose.position.y}`);
});

// Subscribe to IMU
robot.subscribe('/imu/data', 'sensor_msgs/Imu', (data) => {
  console.log(`Orientation: ${JSON.stringify(data.orientation)}`);
});
```

---

## VoltAgent Integration

Turn ROS tools into LLM-callable functions:

```typescript
import { Agent } from '@voltagent/core';
import { rosTools, initializeROS } from './ros-tools';
import { visionTools } from './tools/vision';
import { sensorTools } from './tools/sensors';
import { explorationTools } from './tools/exploration';

// Connect to robot
initializeROS('ws://192.168.1.100:9090');

// Create embodied agent
const agent = new Agent({
  name: 'ugv-rover-01',
  instructions: `You control a physical UGV robot. You can move, turn, stop,
    read sensors, capture images, and explore autonomously.`,
  llm: anthropic('claude-sonnet-4-20250514'),
  tools: [
    ...rosTools,      // move_forward, turn, stop, read_lidar
    ...visionTools,   // capture_image, detect_objects, detect_faces
    ...sensorTools,   // get_multi_sensor_scan, detect_obstacles_360
    ...explorationTools, // update_map, detect_frontiers, find_safe_path
  ],
});

// Chat with robot
const response = await agent.chat('Move forward slowly and tell me what you see');
```

### Available Tools (20+)

**Movement:**
- `move_forward(speed, duration)` — Move at m/s for seconds
- `turn(angular_velocity, duration)` — Rotate at rad/s
- `stop()` — Emergency stop

**Sensors:**
- `read_lidar()` — 8-direction obstacle scan
- `get_multi_sensor_scan()` — Combined LIDAR + camera + IMU
- `detect_obstacles_360()` — Full danger/safe zone map
- `estimate_robot_pose()` — Position + orientation + velocity

**Vision (9 CV Modes):**
- `capture_image()` — Raw camera frame
- `detect_objects()` — YOLO object detection
- `detect_faces()` — Face detection
- `detect_qr_codes()` — QR/barcode scanning
- `detect_color(target_color)` — Color blob tracking
- `detect_lines()` — Line following
- `get_depth_map()` — Depth estimation

**Exploration:**
- `update_map()` — Build occupancy grid
- `detect_frontiers()` — Find unexplored boundaries
- `find_safe_path(goal)` — A* path planning
- `goto(x, y)` — Navigate to coordinate

**Hardware:**
- `set_led(color)` — Control status LEDs
- `set_display(lines)` — Write to OLED
- `set_gimbal(pan, tilt)` — Control camera angle
- `play_sound(name)` — Audio feedback

**Swarm:**
- `broadcast_position()` — Share pose with swarm
- `request_assistance(task)` — Ask nearby robots for help
- `coordinate_formation(formation)` — Move in formation

---

## A2A Agent (Discoverable Robot)

Expose your robot as an A2A agent other agents can find and use:

```typescript
import { createRobotAgent } from './robot-agent';

const agent = createRobotAgent({
  name: 'warehouse-bot-01',
  rosUrl: 'ws://192.168.1.100:9090',
  port: 3001,
  capabilities: ['move', 'scan', 'capture', 'explore'],
});

await agent.start();

// Now discoverable at:
// http://192.168.1.100:3001/.well-known/agent.json
```

Other agents can now:
```typescript
import { A2AClient } from 'nanda-ts';

const robot = new A2AClient('http://192.168.1.100:3001');
await robot.sendTask({ message: 'Move to the loading dock' });
```

---

## X402 Paid Robot Services

Charge other agents for robot API calls:

```typescript
import { createX402RobotServer } from './x402-wrapper';

const server = createX402RobotServer({
  rosUrl: 'ws://192.168.1.100:9090',
  port: 3002,
  escrowAddress: '0x...',
  pricing: {
    move: 0.01,        // 1¢ per movement
    scan: 0.005,       // 0.5¢ per scan
    capture: 0.02,     // 2¢ per image
    explore: 0.10,     // 10¢ per exploration task
  }
});

await server.start();
```

Buyers automatically pay via HTTP 402:
```typescript
const scan = await x402Client.fetch('http://robot:3002/api/scan');
// Paid 0.005 USDC, received LIDAR data
```

---

## Supported Robots

Works with any ROS1/ROS2 robot running rosbridge:

| Robot | Tested | Notes |
|-------|--------|-------|
| Waveshare UGV Rover | ✅ | Full support |
| Waveshare UGV Beast | ✅ | Full support + arm |
| TurtleBot 3/4 | ✅ | Navigation stack |
| Clearpath Jackal | ✅ | Outdoor capable |
| Custom ROS robot | ✅ | Any rosbridge setup |

---

## Prerequisites

1. **Robot with ROS** — ROS1 Noetic or ROS2 Humble+
2. **Rosbridge** — `rosbridge_websocket` running
3. **Network access** — Agent can reach `ws://ROBOT_IP:9090`

```bash
# On robot (ROS2)
ros2 launch rosbridge_server rosbridge_websocket_launch.xml

# On robot (ROS1)
roslaunch rosbridge_server rosbridge_websocket.launch
```

---

## Example: Autonomous Exploration

```typescript
const agent = new Agent({
  name: 'explorer-01',
  instructions: `Explore unknown areas. Use LIDAR to avoid obstacles.
    Build a map as you go. Report interesting findings.`,
  tools: [...rosTools, ...sensorTools, ...explorationTools],
});

// Start autonomous exploration
await agent.chat('Explore this room and map it. Avoid obstacles.');

// Agent will:
// 1. Read LIDAR to detect obstacles
// 2. Find frontiers (unexplored areas)
// 3. Plan path to nearest frontier
// 4. Navigate while avoiding obstacles
// 5. Update map with new data
// 6. Repeat until room is mapped
```

---

## Links

- [rosbridge_suite](http://wiki.ros.org/rosbridge_suite)
- [VoltAgent](https://voltagent.dev)
- [QUSD Hardware Skills](https://github.com/QUSD-ai/hardware-skills)
- [X402 Payments](https://github.com/QUSD-ai/x402-payments)
