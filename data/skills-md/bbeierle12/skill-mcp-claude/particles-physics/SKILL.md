---
name: particles-physics
description: Physics simulation for particle systems—forces (gravity, wind, drag), attractors/repulsors, velocity fields, turbulence, and collision. Use when particles need realistic or artistic motion, swarm behavior, or field-based animation.
---

# Particle Physics

Apply forces, fields, and constraints to create dynamic particle motion.

## Quick Start

```tsx
// Simple gravity + velocity
useFrame((_, delta) => {
  for (let i = 0; i < count; i++) {
    // Apply gravity
    velocities[i * 3 + 1] -= 9.8 * delta;
    
    // Update position
    positions[i * 3] += velocities[i * 3] * delta;
    positions[i * 3 + 1] += velocities[i * 3 + 1] * delta;
    positions[i * 3 + 2] += velocities[i * 3 + 2] * delta;
  }
  geometry.attributes.position.needsUpdate = true;
});
```

## Force Types

### Gravity (Constant Force)

```tsx
function applyGravity(
  velocities: Float32Array,
  count: number,
  gravity: THREE.Vector3,
  delta: number
) {
  for (let i = 0; i < count; i++) {
    velocities[i * 3] += gravity.x * delta;
    velocities[i * 3 + 1] += gravity.y * delta;
    velocities[i * 3 + 2] += gravity.z * delta;
  }
}

// Usage
const gravity = new THREE.Vector3(0, -9.8, 0);
applyGravity(velocities, count, gravity, delta);
```

### Wind (Directional + Noise)

```tsx
function applyWind(
  velocities: Float32Array,
  positions: Float32Array,
  count: number,
  direction: THREE.Vector3,
  strength: number,
  turbulence: number,
  time: number,
  delta: number
) {
  for (let i = 0; i < count; i++) {
    const x = positions[i * 3];
    const y = positions[i * 3 + 1];
    const z = positions[i * 3 + 2];
    
    // Base wind
    let wx = direction.x * strength;
    let wy = direction.y * strength;
    let wz = direction.z * strength;
    
    // Add turbulence (using simple noise approximation)
    const noise = Math.sin(x * 0.5 + time) * Math.cos(z * 0.5 + time);
    wx += noise * turbulence;
    wy += Math.sin(y * 0.3 + time * 1.3) * turbulence * 0.5;
    wz += Math.cos(x * 0.4 + time * 0.7) * turbulence;
    
    velocities[i * 3] += wx * delta;
    velocities[i * 3 + 1] += wy * delta;
    velocities[i * 3 + 2] += wz * delta;
  }
}
```

### Drag (Velocity Damping)

```tsx
function applyDrag(
  velocities: Float32Array,
  count: number,
  drag: number,  // 0-1, higher = more drag
  delta: number
) {
  const factor = 1 - drag * delta;
  
  for (let i = 0; i < count; i++) {
    velocities[i * 3] *= factor;
    velocities[i * 3 + 1] *= factor;
    velocities[i * 3 + 2] *= factor;
  }
}

// Quadratic drag (more realistic)
function applyQuadraticDrag(
  velocities: Float32Array,
  count: number,
  coefficient: number,
  delta: number
) {
  for (let i = 0; i < count; i++) {
    const vx = velocities[i * 3];
    const vy = velocities[i * 3 + 1];
    const vz = velocities[i * 3 + 2];
    
    const speed = Math.sqrt(vx * vx + vy * vy + vz * vz);
    if (speed > 0) {
      const dragForce = coefficient * speed * speed;
      const factor = Math.max(0, 1 - (dragForce * delta) / speed);
      
      velocities[i * 3] *= factor;
      velocities[i * 3 + 1] *= factor;
      velocities[i * 3 + 2] *= factor;
    }
  }
}
```

## Attractors & Repulsors

### Point Attractor

```tsx
function applyAttractor(
  velocities: Float32Array,
  positions: Float32Array,
  count: number,
  attractorPos: THREE.Vector3,
  strength: number,  // Positive = attract, negative = repel
  delta: number
) {
  for (let i = 0; i < count; i++) {
    const dx = attractorPos.x - positions[i * 3];
    const dy = attractorPos.y - positions[i * 3 + 1];
    const dz = attractorPos.z - positions[i * 3 + 2];
    
    const distSq = dx * dx + dy * dy + dz * dz;
    const dist = Math.sqrt(distSq);
    
    if (dist > 0.1) {  // Avoid division by zero
      // Inverse square falloff
      const force = strength / distSq;
      
      velocities[i * 3] += (dx / dist) * force * delta;
      velocities[i * 3 + 1] += (dy / dist) * force * delta;
      velocities[i * 3 + 2] += (dz / dist) * force * delta;
    }
  }
}
```

### Orbit Attractor

```tsx
function applyOrbitAttractor(
  velocities: Float32Array,
  positions: Float32Array,
  count: number,
  center: THREE.Vector3,
  orbitStrength: number,
  pullStrength: number,
  delta: number
) {
  for (let i = 0; i < count; i++) {
    const dx = positions[i * 3] - center.x;
    const dy = positions[i * 3 + 1] - center.y;
    const dz = positions[i * 3 + 2] - center.z;
    
    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
    
    if (dist > 0.1) {
      // Tangential force (orbit)
      const tx = -dz / dist;
      const tz = dx / dist;
      
      velocities[i * 3] += tx * orbitStrength * delta;
      velocities[i * 3 + 2] += tz * orbitStrength * delta;
      
      // Radial force (pull toward center)
      velocities[i * 3] -= (dx / dist) * pullStrength * delta;
      velocities[i * 3 + 1] -= (dy / dist) * pullStrength * delta;
      velocities[i * 3 + 2] -= (dz / dist) * pullStrength * delta;
    }
  }
}
```

### Multiple Attractors

```tsx
interface Attractor {
  position: THREE.Vector3;
  strength: number;
  radius: number;  // Influence radius
}

function applyAttractors(
  velocities: Float32Array,
  positions: Float32Array,
  count: number,
  attractors: Attractor[],
  delta: number
) {
  for (let i = 0; i < count; i++) {
    const px = positions[i * 3];
    const py = positions[i * 3 + 1];
    const pz = positions[i * 3 + 2];
    
    for (const attractor of attractors) {
      const dx = attractor.position.x - px;
      const dy = attractor.position.y - py;
      const dz = attractor.position.z - pz;
      
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
      
      if (dist > 0.1 && dist < attractor.radius) {
        // Smooth falloff within radius
        const falloff = 1 - dist / attractor.radius;
        const force = attractor.strength * falloff * falloff;
        
        velocities[i * 3] += (dx / dist) * force * delta;
        velocities[i * 3 + 1] += (dy / dist) * force * delta;
        velocities[i * 3 + 2] += (dz / dist) * force * delta;
      }
    }
  }
}
```

## Velocity Fields

### Curl Noise Field

```tsx
// In shader (GPU)
vec3 curlNoise(vec3 p) {
  const float e = 0.1;
  
  vec3 dx = vec3(e, 0.0, 0.0);
  vec3 dy = vec3(0.0, e, 0.0);
  vec3 dz = vec3(0.0, 0.0, e);
  
  float n1 = snoise(p + dy) - snoise(p - dy);
  float n2 = snoise(p + dz) - snoise(p - dz);
  float n3 = snoise(p + dx) - snoise(p - dx);
  float n4 = snoise(p + dz) - snoise(p - dz);
  float n5 = snoise(p + dx) - snoise(p - dx);
  float n6 = snoise(p + dy) - snoise(p - dy);
  
  return normalize(vec3(n1 - n2, n3 - n4, n5 - n6));
}

// Usage in vertex shader
vec3 velocity = curlNoise(position * 0.5 + uTime * 0.1);
position += velocity * delta;
```

### Flow Field (2D/3D Grid)

```tsx
class FlowField {
  private field: THREE.Vector3[];
  private resolution: number;
  private size: number;
  
  constructor(resolution: number, size: number) {
    this.resolution = resolution;
    this.size = size;
    this.field = [];
    
    for (let i = 0; i < resolution ** 3; i++) {
      this.field.push(new THREE.Vector3());
    }
  }
  
  // Generate field from noise
  generate(time: number, scale: number) {
    for (let x = 0; x < this.resolution; x++) {
      for (let y = 0; y < this.resolution; y++) {
        for (let z = 0; z < this.resolution; z++) {
          const index = x + y * this.resolution + z * this.resolution * this.resolution;
          
          // Use noise to generate flow direction
          const wx = x / this.resolution * scale;
          const wy = y / this.resolution * scale;
          const wz = z / this.resolution * scale;
          
          const angle1 = noise3D(wx, wy, wz + time) * Math.PI * 2;
          const angle2 = noise3D(wx + 100, wy, wz + time) * Math.PI * 2;
          
          this.field[index].set(
            Math.cos(angle1) * Math.cos(angle2),
            Math.sin(angle2),
            Math.sin(angle1) * Math.cos(angle2)
          );
        }
      }
    }
  }
  
  // Sample field at position
  sample(position: THREE.Vector3): THREE.Vector3 {
    const halfSize = this.size / 2;
    
    const x = Math.floor(((position.x + halfSize) / this.size) * this.resolution);
    const y = Math.floor(((position.y + halfSize) / this.size) * this.resolution);
    const z = Math.floor(((position.z + halfSize) / this.size) * this.resolution);
    
    const cx = Math.max(0, Math.min(this.resolution - 1, x));
    const cy = Math.max(0, Math.min(this.resolution - 1, y));
    const cz = Math.max(0, Math.min(this.resolution - 1, z));
    
    const index = cx + cy * this.resolution + cz * this.resolution * this.resolution;
    return this.field[index];
  }
}
```

### Vortex Field

```tsx
function applyVortex(
  velocities: Float32Array,
  positions: Float32Array,
  count: number,
  center: THREE.Vector3,
  axis: THREE.Vector3,  // Normalized
  strength: number,
  falloff: number,
  delta: number
) {
  for (let i = 0; i < count; i++) {
    const dx = positions[i * 3] - center.x;
    const dy = positions[i * 3 + 1] - center.y;
    const dz = positions[i * 3 + 2] - center.z;
    
    // Project onto plane perpendicular to axis
    const dot = dx * axis.x + dy * axis.y + dz * axis.z;
    const px = dx - dot * axis.x;
    const py = dy - dot * axis.y;
    const pz = dz - dot * axis.z;
    
    const dist = Math.sqrt(px * px + py * py + pz * pz);
    
    if (dist > 0.1) {
      // Tangent direction (cross product with axis)
      const tx = axis.y * pz - axis.z * py;
      const ty = axis.z * px - axis.x * pz;
      const tz = axis.x * py - axis.y * px;
      
      const tLen = Math.sqrt(tx * tx + ty * ty + tz * tz);
      const force = strength * Math.exp(-dist * falloff);
      
      velocities[i * 3] += (tx / tLen) * force * delta;
      velocities[i * 3 + 1] += (ty / tLen) * force * delta;
      velocities[i * 3 + 2] += (tz / tLen) * force * delta;
    }
  }
}
```

## Turbulence

### Simplex-Based Turbulence

```glsl
// GPU turbulence in vertex shader
vec3 turbulence(vec3 p, float time, float scale, int octaves) {
  vec3 result = vec3(0.0);
  float amplitude = 1.0;
  float frequency = scale;
  
  for (int i = 0; i < octaves; i++) {
    vec3 samplePos = p * frequency + time;
    result.x += snoise(samplePos) * amplitude;
    result.y += snoise(samplePos + vec3(100.0)) * amplitude;
    result.z += snoise(samplePos + vec3(200.0)) * amplitude;
    
    frequency *= 2.0;
    amplitude *= 0.5;
  }
  
  return result;
}
```

### CPU Turbulence

```tsx
function applyTurbulence(
  velocities: Float32Array,
  positions: Float32Array,
  count: number,
  strength: number,
  scale: number,
  time: number,
  delta: number
) {
  for (let i = 0; i < count; i++) {
    const x = positions[i * 3] * scale;
    const y = positions[i * 3 + 1] * scale;
    const z = positions[i * 3 + 2] * scale;
    
    // Simple noise approximation
    const nx = Math.sin(x + time) * Math.cos(z + time * 0.7);
    const ny = Math.sin(y + time * 1.3) * Math.cos(x + time * 0.5);
    const nz = Math.sin(z + time * 0.9) * Math.cos(y + time * 1.1);
    
    velocities[i * 3] += nx * strength * delta;
    velocities[i * 3 + 1] += ny * strength * delta;
    velocities[i * 3 + 2] += nz * strength * delta;
  }
}
```

## Collision

### Plane Collision

```tsx
function collidePlane(
  positions: Float32Array,
  velocities: Float32Array,
  count: number,
  planeY: number,
  bounce: number  // 0-1
) {
  for (let i = 0; i < count; i++) {
    if (positions[i * 3 + 1] < planeY) {
      positions[i * 3 + 1] = planeY;
      velocities[i * 3 + 1] *= -bounce;
    }
  }
}
```

### Sphere Collision

```tsx
function collideSphere(
  positions: Float32Array,
  velocities: Float32Array,
  count: number,
  center: THREE.Vector3,
  radius: number,
  bounce: number,
  inside: boolean  // true = contain inside, false = repel from outside
) {
  for (let i = 0; i < count; i++) {
    const dx = positions[i * 3] - center.x;
    const dy = positions[i * 3 + 1] - center.y;
    const dz = positions[i * 3 + 2] - center.z;
    
    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
    
    const collision = inside ? dist > radius : dist < radius;
    
    if (collision && dist > 0) {
      const nx = dx / dist;
      const ny = dy / dist;
      const nz = dz / dist;
      
      // Move to surface
      const targetDist = inside ? radius : radius;
      positions[i * 3] = center.x + nx * targetDist;
      positions[i * 3 + 1] = center.y + ny * targetDist;
      positions[i * 3 + 2] = center.z + nz * targetDist;
      
      // Reflect velocity
      const dot = velocities[i * 3] * nx + velocities[i * 3 + 1] * ny + velocities[i * 3 + 2] * nz;
      velocities[i * 3] = (velocities[i * 3] - 2 * dot * nx) * bounce;
      velocities[i * 3 + 1] = (velocities[i * 3 + 1] - 2 * dot * ny) * bounce;
      velocities[i * 3 + 2] = (velocities[i * 3 + 2] - 2 * dot * nz) * bounce;
    }
  }
}
```

## Integration Methods

### Euler (Simple)

```tsx
// Fastest, least accurate
position += velocity * delta;
velocity += acceleration * delta;
```

### Verlet (Better for constraints)

```tsx
// Store previous position
const newPos = position * 2 - prevPosition + acceleration * delta * delta;
prevPosition = position;
position = newPos;
```

### RK4 (Most accurate)

```tsx
// Runge-Kutta 4th order (for high precision)
function rk4(position: number, velocity: number, acceleration: (p: number, v: number) => number, dt: number) {
  const k1v = acceleration(position, velocity);
  const k1x = velocity;
  
  const k2v = acceleration(position + k1x * dt/2, velocity + k1v * dt/2);
  const k2x = velocity + k1v * dt/2;
  
  const k3v = acceleration(position + k2x * dt/2, velocity + k2v * dt/2);
  const k3x = velocity + k2v * dt/2;
  
  const k4v = acceleration(position + k3x * dt, velocity + k3v * dt);
  const k4x = velocity + k3v * dt;
  
  return {
    position: position + (k1x + 2*k2x + 2*k3x + k4x) * dt / 6,
    velocity: velocity + (k1v + 2*k2v + 2*k3v + k4v) * dt / 6
  };
}
```

## File Structure

```
particles-physics/
├── SKILL.md
├── references/
│   ├── forces.md             # All force types
│   └── integration.md        # Integration methods comparison
└── scripts/
    ├── forces/
    │   ├── gravity.ts        # Gravity implementations
    │   ├── attractors.ts     # Point/orbit attractors
    │   └── fields.ts         # Flow/velocity fields
    └── collision/
        ├── planes.ts         # Plane collision
        └── shapes.ts         # Sphere, box collision
```

## Reference

- `references/forces.md` — Complete force implementations
- `references/integration.md` — When to use which integration method
