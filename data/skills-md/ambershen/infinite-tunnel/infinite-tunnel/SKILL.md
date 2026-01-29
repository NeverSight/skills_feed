---
name: infinite-tunnel
description: This skill covers creating infinite tunnel effects using Three.js and GSAP
---

# Three.js Infinite Tunnel Effect Skill

## Overview
This skill covers creating infinite tunnel effects using Three.js and GSAP (GreenSock Animation Platform). An infinite tunnel creates a mesmerizing looping effect by continuously moving the camera through repeating geometric segments.

## When to Use
Use this skill when:
- You want to build an immersive, 3D scrolling experience for a gallery, portfolio, or showcase.
- The user asks for "infinite scrolling", "3D tunnel", "wormhole", or "time travel" effects.
- You need to display a large number of items (images, cards, objects) in a creative, non-grid layout.
- The project requires a high-impact, futuristic, or abstract visual style.
- You are working with `Three.js` for 3D rendering and `GSAP` for smooth animations.

## Core Concept
The infinite tunnel effect relies on a simple principle:
1. Create multiple geometric segments positioned in a line (forming the tunnel)
2. Move the camera forward through them
3. When segments pass behind the camera, teleport them to the far end
4. This creates a seamless infinite loop

## Advanced Gallery Implementation

### 1. Curve-Based Wall Placement
Instead of placing objects in a straight line, use a `CatmullRomCurve3` to create a winding path. Objects are positioned on the tunnel "walls" using tangent, normal, and binormal vectors.

```javascript
// Calculate position on curve
const pos = curve.getPointAt(t_slot);

// Calculate local coordinate frame
const tangent = curve.getTangentAt(t_slot).normalize();
const up = new THREE.Vector3(0, 1, 0);
// Handle Gimbal lock for vertical tangents
if (Math.abs(tangent.y) > 0.9) up.set(0, 0, 1);

const normal = new THREE.Vector3().crossVectors(tangent, up).normalize();
const binormal = new THREE.Vector3().crossVectors(tangent, normal).normalize();

// Offset from center to wall
const angle = (slotIndex * 137.5) * (Math.PI / 180); // Golden angle distribution
const radius = tubeRadius - 1.5;

const offset = new THREE.Vector3()
  .addScaledVector(normal, Math.cos(angle) * radius)
  .addScaledVector(binormal, Math.sin(angle) * radius);

item.group.position.copy(pos).add(offset);
item.group.lookAt(pos); // Face center
```

### 2. Recursive Raycasting for Nested Objects
When objects have children (like borders or suspension strings), simple raycasting fails. Use recursive checking and traverse up the parent chain to identify the logical "item".

```javascript
// Enable recursive search (true)
const intersects = raycaster.intersectObjects(interactables, true);

if (intersects.length > 0) {
  let hitMesh = intersects[0].object;
  // Traverse up to find the root mesh
  while (hitMesh && !interactables.includes(hitMesh)) {
      hitMesh = hitMesh.parent;
  }
  // Now hitMesh corresponds to your pool item
}
```

### 3. Detail View Transition
Seamlessly switch between "Tunnel Mode" (scrolling) and "Detail Mode" (focused view) using GSAP to animate the camera.

```javascript
function enterDetailMode(item) {
  // Calculate a target position in front of the image
  const centerPos = item.group.position.clone()
    .add(item.group.getWorldDirection(new THREE.Vector3()).multiplyScalar(2));

  gsap.to(camera.position, {
    x: centerPos.x,
    y: centerPos.y,
    z: centerPos.z,
    duration: 1.5,
    ease: "power2.inOut",
    onUpdate: () => camera.lookAt(item.group.position)
  });
}
```

### 4. Dynamic Aspect Ratio Handling
To support diverse content types (portrait/landscape) without distortion, use a unit square geometry (`1x1`) and scale the mesh based on the loaded texture's aspect ratio.

```javascript
const planeGeometry = new THREE.PlaneGeometry(1, 1);

// When texture loads:
const aspect = tex.image.width / tex.image.height;
const targetHeight = 2.0;
// Scale width proportional to aspect ratio, keep height fixed
mesh.scale.set(targetHeight * aspect, targetHeight, 1);
```

### 5. Procedural Suspension Strings
Add "hanging wires" to objects that automatically adjust to the object's scale by attaching them to the mesh's coordinate system.

```javascript
const stringPoints = [
  new THREE.Vector3(-0.5, 0.5, 0), // Top-left of 1x1 plane
  new THREE.Vector3(-0.5, 5.0, 0), // Up into the ceiling
  new THREE.Vector3(0.5, 0.5, 0),  // Top-right
  new THREE.Vector3(0.5, 5.0, 0)
];
const strings = new THREE.LineSegments(...);
mesh.add(strings); // Add as child so it scales with the image
```

## Basic Implementation Pattern

### Setup
```javascript
import * as THREE from 'three';
import { gsap } from 'gsap';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

camera.position.z = 5;
```

### Creating Tunnel Segments
```javascript
const segments = [];
const segmentSpacing = 2;
const numSegments = 50;

for (let i = 0; i < numSegments; i++) {
  const geometry = new THREE.TorusGeometry(3, 0.1, 16, 32);
  const material = new THREE.MeshBasicMaterial({ 
    color: new THREE.Color(`hsl(${i * 7}, 70%, 50%)`),
    wireframe: true 
  });
  const segment = new THREE.Mesh(geometry, material);
  segment.position.z = -i * segmentSpacing;
  segment.userData.initialZ = segment.position.z;
  segments.push(segment);
  scene.add(segment);
}
```

### Infinite Loop Logic
```javascript
const tunnelLength = numSegments * segmentSpacing;

gsap.to(camera.position, {
  z: -tunnelLength,
  duration: 20,
  ease: 'none',
  repeat: -1,
  onUpdate: () => {
    segments.forEach(segment => {
      // When segment is behind camera, move it to the front
      if (segment.position.z > camera.position.z + 10) {
        segment.position.z -= tunnelLength;
      }
    });
  }
});
```

## Best Practices

### 1. Performance Optimization
**Use InstancedMesh for many identical segments:**
```javascript
const geometry = new THREE.TorusGeometry(3, 0.1, 16, 32);
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const count = 100;
const instancedMesh = new THREE.InstancedMesh(geometry, material, count);

const dummy = new THREE.Object3D();
for (let i = 0; i < count; i++) {
  dummy.position.z = -i * segmentSpacing;
  dummy.updateMatrix();
  instancedMesh.setMatrixAt(i, dummy.matrix);
}
instancedMesh.instanceMatrix.needsUpdate = true;
scene.add(instancedMesh);
```

**Optimize geometry:**
- Use lower polygon counts for distant segments
- Share geometries and materials between segments
- Use `BufferGeometry` instead of regular geometry

### 2. Segment Positioning
**Calculate tunnel length carefully:**
```javascript
const segmentSpacing = 2;
const numSegments = 50;
const tunnelLength = numSegments * segmentSpacing;

// Ensure enough segments to fill view + buffer
const fov = 75;
const aspectRatio = window.innerWidth / window.innerHeight;
const minSegments = Math.ceil(tunnelLength / segmentSpacing) + 5; // +5 buffer
```

**Proper wrapping logic:**
```javascript
// Option 1: Simple wraparound
if (segment.position.z > camera.position.z + wrapDistance) {
  segment.position.z -= tunnelLength;
}

// Option 2: Modulo approach (smoother)
const relativeZ = segment.position.z - camera.position.z;
if (relativeZ > wrapDistance) {
  segment.position.z = camera.position.z - tunnelLength + (relativeZ % tunnelLength);
}
```

### 3. Animation Timing
**Use GSAP effectively:**
```javascript
// Constant speed tunnel
gsap.to(camera.position, {
  z: -tunnelLength,
  duration: 20,
  ease: 'none',  // Linear motion
  repeat: -1,
  repeatDelay: 0
});

// Variable speed with easing
const tl = gsap.timeline({ repeat: -1 });
tl.to(camera.position, { z: -50, duration: 5, ease: 'power1.inOut' })
  .to(camera.position, { z: -100, duration: 3, ease: 'power2.in' });
```

### 4. Visual Enhancements
**Color gradients:**
```javascript
segments.forEach((segment, i) => {
  const hue = (i * 10 + Date.now() * 0.05) % 360;
  segment.material.color.setHSL(hue / 360, 0.7, 0.5);
});
```

**Rotation patterns:**
```javascript
segments.forEach((segment, i) => {
  segment.rotation.z += 0.01 * (1 + i * 0.01);
  // Or synchronized rotation
  segment.rotation.z = (Date.now() * 0.001 + i * 0.1) % (Math.PI * 2);
});
```

**Scaling effects:**
```javascript
const scaleOscillation = Math.sin(Date.now() * 0.001 + i * 0.5) * 0.2 + 1;
segment.scale.set(scaleOscillation, scaleOscillation, 1);
```

## Common Patterns

### Pattern 1: Wireframe Tunnel
```javascript
const geometry = new THREE.TorusGeometry(3, 0.1, 16, 32);
const material = new THREE.MeshBasicMaterial({ 
  wireframe: true,
  color: 0x00ffff
});
```

### Pattern 2: Glowing Tunnel
```javascript
const material = new THREE.MeshBasicMaterial({ 
  color: 0xff00ff,
  transparent: true,
  opacity: 0.8,
  blending: THREE.AdditiveBlending
});

// Add point lights
segments.forEach(segment => {
  const light = new THREE.PointLight(0xff00ff, 2, 10);
  light.position.copy(segment.position);
  scene.add(light);
});
```

### Pattern 3: Mixed Geometry Tunnel
```javascript
const geometries = [
  new THREE.TorusGeometry(3, 0.1, 16, 32),
  new THREE.RingGeometry(2, 3, 32),
  new THREE.OctahedronGeometry(2),
  new THREE.BoxGeometry(4, 4, 0.2)
];

segments.forEach((segment, i) => {
  segment.geometry = geometries[i % geometries.length];
});
```

### Pattern 4: Particle Tunnel
```javascript
const particleCount = 5000;
const geometry = new THREE.BufferGeometry();
const positions = new Float32Array(particleCount * 3);
const colors = new Float32Array(particleCount * 3);

for (let i = 0; i < particleCount; i++) {
  const angle = Math.random() * Math.PI * 2;
  const radius = 2 + Math.random() * 2;
  positions[i * 3] = Math.cos(angle) * radius;
  positions[i * 3 + 1] = Math.sin(angle) * radius;
  positions[i * 3 + 2] = -Math.random() * tunnelLength;
  
  colors[i * 3] = Math.random();
  colors[i * 3 + 1] = Math.random();
  colors[i * 3 + 2] = 1;
}

geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

const material = new THREE.PointsMaterial({ 
  size: 0.1, 
  vertexColors: true,
  blending: THREE.AdditiveBlending
});
const particles = new THREE.Points(geometry, material);
scene.add(particles);
```

## Advanced Techniques

### Camera Controls with GSAP
```javascript
// Turbulence effect
gsap.to(camera.rotation, {
  x: '+=0.1',
  y: '+=0.05',
  duration: 2,
  yoyo: true,
  repeat: -1,
  ease: 'sine.inOut'
});

// Banking on turns
gsap.to(camera.rotation, {
  z: 0.3,
  duration: 1,
  ease: 'power2.inOut',
  onComplete: () => {
    gsap.to(camera.rotation, { z: 0, duration: 1 });
  }
});
```

### Post-Processing Effects
```javascript
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass';

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));

const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,  // strength
  0.4,  // radius
  0.85  // threshold
);
composer.addPass(bloomPass);

// In animation loop, use composer instead of renderer
composer.render();
```

### Shader-Based Tunnels
```javascript
const vertexShader = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const fragmentShader = `
  uniform float time;
  varying vec2 vUv;
  
  void main() {
    vec2 center = vUv - 0.5;
    float dist = length(center);
    float pulse = sin(dist * 10.0 - time * 2.0) * 0.5 + 0.5;
    vec3 color = vec3(pulse, 0.5, 1.0 - pulse);
    gl_FragColor = vec4(color, 1.0);
  }
`;

const material = new THREE.ShaderMaterial({
  vertexShader,
  fragmentShader,
  uniforms: { time: { value: 0 } }
});
```

## Troubleshooting

### Problem: Segments visible popping in/out
**Solution:** Increase buffer segments and adjust wrap distance
```javascript
const visibleDistance = 15; // Distance where segments are visible
const wrapDistance = visibleDistance + 5; // Add buffer
```

### Problem: Jerky animation
**Solution:** Use `ease: 'none'` for constant speed and ensure consistent frame rate
```javascript
gsap.ticker.fps(60); // Lock to 60fps
gsap.to(camera.position, { 
  z: -tunnelLength, 
  duration: 20, 
  ease: 'none' 
});
```

### Problem: Performance issues
**Solutions:**
- Use InstancedMesh for identical segments
- Reduce polygon count on geometries
- Implement frustum culling
- Use simpler materials (MeshBasicMaterial vs MeshStandardMaterial)
- Limit the number of segments in view

### Problem: Gaps between segments
**Solution:** Ensure proper segment spacing calculation
```javascript
const geometry = new THREE.TorusGeometry(3, 0.1, 16, 32);
const boundingBox = new THREE.Box3().setFromObject(new THREE.Mesh(geometry));
const segmentDepth = boundingBox.max.z - boundingBox.min.z;
const segmentSpacing = segmentDepth * 0.9; // Slight overlap
```

## Complete Working Example
```javascript
import * as THREE from 'three';
import { gsap } from 'gsap';

// Setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);
scene.fog = new THREE.Fog(0x000000, 1, 50);

const camera = new THREE.PerspectiveCamera(
  75, 
  window.innerWidth / window.innerHeight, 
  0.1, 
  1000
);
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Tunnel creation
const segments = [];
const segmentSpacing = 2;
const numSegments = 50;
const tunnelLength = numSegments * segmentSpacing;

for (let i = 0; i < numSegments; i++) {
  const geometry = new THREE.TorusGeometry(3, 0.1, 16, 32);
  const material = new THREE.MeshBasicMaterial({ 
    color: new THREE.Color(`hsl(${i * 7}, 70%, 50%)`),
    wireframe: true 
  });
  const segment = new THREE.Mesh(geometry, material);
  segment.position.z = -i * segmentSpacing;
  segments.push(segment);
  scene.add(segment);
}

// Animation
gsap.to(camera.position, {
  z: -tunnelLength,
  duration: 20,
  ease: 'none',
  repeat: -1,
  onUpdate: () => {
    segments.forEach(segment => {
      if (segment.position.z > camera.position.z + 10) {
        segment.position.z -= tunnelLength;
      }
    });
  }
});

// Render loop
function animate() {
  requestAnimationFrame(animate);
  
  segments.forEach((segment, i) => {
    segment.rotation.z += 0.01 * (1 + i * 0.01);
  });
  
  renderer.render(scene, camera);
}

animate();

// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

### Pattern 5: Scroll-Controlled Tunnel
Replace auto-movement with smooth scroll interaction.

```javascript
const state = {
  zPos: 0,
  targetZ: 0
};

// Listen for scroll events
window.addEventListener('wheel', (e) => {
  // Normalize scroll delta
  const delta = Math.sign(e.deltaY) * Math.min(Math.abs(e.deltaY), 10);
  // Scroll down (positive delta) moves forward (negative Z)
  state.targetZ -= delta * 0.5;
});

function animate() {
  // Smoothly interpolate current position to target
  state.zPos += (state.targetZ - state.zPos) * 0.1;
  camera.position.z = state.zPos;
  
  // Update infinite loop logic (same as basic pattern)
  segments.forEach(segment => {
    if (segment.position.z > camera.position.z + 10) {
      segment.position.z -= tunnelLength;
    }
  });
  
  renderer.render(scene, camera);
}
```

## Tips & Tricks

1. **Start simple**: Begin with basic shapes and add complexity gradually
2. **Layer effects**: Combine multiple tunnel layers with different speeds for depth
3. **Audio reactivity**: Sync segment colors/sizes to audio frequencies
4. **Interactive tunnels**: Use mouse position to influence camera rotation
5. **Texture mapping**: Apply textures to segments for richer visuals
6. **Blend modes**: Use THREE.AdditiveBlending for glowing neon effects
7. **Camera shake**: Add subtle GSAP animations to camera for dynamic feel
8. **Fog**: Use THREE.Fog to hide distant segment pop-in

## Resources

- Three.js Documentation: https://threejs.org/docs/
- GSAP Documentation: https://greensock.com/docs/
- Three.js Examples: https://threejs.org/examples/
- WebGL Fundamentals: https://webglfundamentals.org/