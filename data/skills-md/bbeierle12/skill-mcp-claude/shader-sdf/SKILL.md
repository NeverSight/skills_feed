---
name: shader-sdf
description: Signed Distance Functions (SDFs) in GLSL—2D/3D shape primitives, boolean operations (union, intersection, subtraction), smooth blending, repetition, and raymarching fundamentals. Use when creating procedural shapes, text effects, smooth morphing, or raymarched 3D scenes.
---

# Shader SDFs

Signed Distance Functions return the distance from a point to a shape's surface. Negative = inside, positive = outside, zero = on surface.

## Quick Start

```glsl
// 2D circle SDF
float sdCircle(vec2 p, float r) {
  return length(p) - r;
}

// Usage
float d = sdCircle(uv - 0.5, 0.3);

// Render
vec3 color = d < 0.0 ? vec3(1.0) : vec3(0.0);           // Hard edge
vec3 color = vec3(smoothstep(0.01, 0.0, d));            // Soft edge
vec3 color = vec3(smoothstep(0.02, 0.0, abs(d)));       // Outline
```

## 2D Primitives

### Circle

```glsl
float sdCircle(vec2 p, float r) {
  return length(p) - r;
}
```

### Box

```glsl
float sdBox(vec2 p, vec2 b) {
  vec2 d = abs(p) - b;
  return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}
```

### Rounded Box

```glsl
float sdRoundedBox(vec2 p, vec2 b, float r) {
  vec2 d = abs(p) - b + r;
  return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0) - r;
}
```

### Line Segment

```glsl
float sdSegment(vec2 p, vec2 a, vec2 b) {
  vec2 pa = p - a;
  vec2 ba = b - a;
  float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
  return length(pa - ba * h);
}
```

### Triangle

```glsl
float sdTriangle(vec2 p, vec2 p0, vec2 p1, vec2 p2) {
  vec2 e0 = p1 - p0, e1 = p2 - p1, e2 = p0 - p2;
  vec2 v0 = p - p0, v1 = p - p1, v2 = p - p2;
  vec2 pq0 = v0 - e0 * clamp(dot(v0, e0) / dot(e0, e0), 0.0, 1.0);
  vec2 pq1 = v1 - e1 * clamp(dot(v1, e1) / dot(e1, e1), 0.0, 1.0);
  vec2 pq2 = v2 - e2 * clamp(dot(v2, e2) / dot(e2, e2), 0.0, 1.0);
  float s = sign(e0.x * e2.y - e0.y * e2.x);
  vec2 d = min(min(
    vec2(dot(pq0, pq0), s * (v0.x * e0.y - v0.y * e0.x)),
    vec2(dot(pq1, pq1), s * (v1.x * e1.y - v1.y * e1.x))),
    vec2(dot(pq2, pq2), s * (v2.x * e2.y - v2.y * e2.x)));
  return -sqrt(d.x) * sign(d.y);
}
```

### Ring

```glsl
float sdRing(vec2 p, float r, float thickness) {
  return abs(length(p) - r) - thickness;
}
```

### Polygon (N-sided)

```glsl
float sdPolygon(vec2 p, float r, int n) {
  float a = atan(p.x, p.y) + 3.141592;
  float s = 6.283185 / float(n);
  return cos(floor(0.5 + a / s) * s - a) * length(p) - r;
}
```

### Star

```glsl
float sdStar(vec2 p, float r, int n, float m) {
  float an = 3.141592 / float(n);
  float en = 3.141592 / m;
  vec2 acs = vec2(cos(an), sin(an));
  vec2 ecs = vec2(cos(en), sin(en));
  
  float bn = mod(atan(p.x, p.y), 2.0 * an) - an;
  p = length(p) * vec2(cos(bn), abs(sin(bn)));
  p -= r * acs;
  p += ecs * clamp(-dot(p, ecs), 0.0, r * acs.y / ecs.y);
  
  return length(p) * sign(p.x);
}
```

## 3D Primitives

### Sphere

```glsl
float sdSphere(vec3 p, float r) {
  return length(p) - r;
}
```

### Box

```glsl
float sdBox(vec3 p, vec3 b) {
  vec3 q = abs(p) - b;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}
```

### Rounded Box

```glsl
float sdRoundBox(vec3 p, vec3 b, float r) {
  vec3 q = abs(p) - b;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - r;
}
```

### Cylinder

```glsl
float sdCylinder(vec3 p, float h, float r) {
  vec2 d = abs(vec2(length(p.xz), p.y)) - vec2(r, h);
  return min(max(d.x, d.y), 0.0) + length(max(d, 0.0));
}
```

### Torus

```glsl
float sdTorus(vec3 p, vec2 t) {
  vec2 q = vec2(length(p.xz) - t.x, p.y);
  return length(q) - t.y;
}
```

### Cone

```glsl
float sdCone(vec3 p, vec2 c, float h) {
  vec2 q = h * vec2(c.x / c.y, -1.0);
  vec2 w = vec2(length(p.xz), p.y);
  vec2 a = w - q * clamp(dot(w, q) / dot(q, q), 0.0, 1.0);
  vec2 b = w - q * vec2(clamp(w.x / q.x, 0.0, 1.0), 1.0);
  float k = sign(q.y);
  float d = min(dot(a, a), dot(b, b));
  float s = max(k * (w.x * q.y - w.y * q.x), k * (w.y - q.y));
  return sqrt(d) * sign(s);
}
```

### Capsule

```glsl
float sdCapsule(vec3 p, vec3 a, vec3 b, float r) {
  vec3 pa = p - a, ba = b - a;
  float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
  return length(pa - ba * h) - r;
}
```

### Plane

```glsl
float sdPlane(vec3 p, vec3 n, float h) {
  return dot(p, n) + h;
}
```

## Boolean Operations

### Union (OR)

```glsl
float opUnion(float d1, float d2) {
  return min(d1, d2);
}
```

### Intersection (AND)

```glsl
float opIntersection(float d1, float d2) {
  return max(d1, d2);
}
```

### Subtraction (NOT)

```glsl
float opSubtraction(float d1, float d2) {
  return max(-d1, d2);
}
```

### Smooth Union

```glsl
float opSmoothUnion(float d1, float d2, float k) {
  float h = clamp(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0);
  return mix(d2, d1, h) - k * h * (1.0 - h);
}
```

### Smooth Intersection

```glsl
float opSmoothIntersection(float d1, float d2, float k) {
  float h = clamp(0.5 - 0.5 * (d2 - d1) / k, 0.0, 1.0);
  return mix(d2, d1, h) + k * h * (1.0 - h);
}
```

### Smooth Subtraction

```glsl
float opSmoothSubtraction(float d1, float d2, float k) {
  float h = clamp(0.5 - 0.5 * (d2 + d1) / k, 0.0, 1.0);
  return mix(d2, -d1, h) + k * h * (1.0 - h);
}
```

## Transformations

### Translation

```glsl
// Move shape by offset
float d = sdCircle(p - offset, r);
```

### Rotation (2D)

```glsl
mat2 rot2D(float a) {
  float s = sin(a), c = cos(a);
  return mat2(c, -s, s, c);
}

// Rotate point around origin
vec2 rotatedP = rot2D(angle) * p;
float d = sdBox(rotatedP, size);
```

### Rotation (3D)

```glsl
mat3 rotateX(float a) {
  float s = sin(a), c = cos(a);
  return mat3(1, 0, 0, 0, c, -s, 0, s, c);
}

mat3 rotateY(float a) {
  float s = sin(a), c = cos(a);
  return mat3(c, 0, s, 0, 1, 0, -s, 0, c);
}

mat3 rotateZ(float a) {
  float s = sin(a), c = cos(a);
  return mat3(c, -s, 0, s, c, 0, 0, 0, 1);
}
```

### Scale

```glsl
// Scale shape
float d = sdCircle(p / scale, r) * scale;
```

### Symmetry

```glsl
// Mirror across Y axis
p.x = abs(p.x);
float d = sdCircle(p - vec2(0.3, 0.0), 0.1);
```

## Domain Operations

### Repetition (Infinite)

```glsl
float opRepeat(vec2 p, vec2 spacing) {
  vec2 q = mod(p + spacing * 0.5, spacing) - spacing * 0.5;
  return sdCircle(q, 0.1);
}
```

### Repetition (Limited)

```glsl
float opRepeatLimited(vec3 p, float spacing, vec3 count) {
  vec3 q = p - spacing * clamp(round(p / spacing), -count, count);
  return sdSphere(q, 0.1);
}
```

### Twist

```glsl
float opTwist(vec3 p, float k) {
  float c = cos(k * p.y);
  float s = sin(k * p.y);
  mat2 m = mat2(c, -s, s, c);
  vec3 q = vec3(m * p.xz, p.y);
  return sdBox(q, vec3(0.5));
}
```

### Bend

```glsl
float opBend(vec3 p, float k) {
  float c = cos(k * p.x);
  float s = sin(k * p.x);
  mat2 m = mat2(c, -s, s, c);
  vec3 q = vec3(m * p.xy, p.z);
  return sdBox(q, vec3(0.5));
}
```

### Onion (Hollow)

```glsl
float opOnion(float d, float thickness) {
  return abs(d) - thickness;
}
```

### Round

```glsl
float opRound(float d, float r) {
  return d - r;
}
```

## 2D Rendering Techniques

### Anti-aliased Edge

```glsl
float aa = fwidth(d) * 1.5;
float mask = smoothstep(aa, -aa, d);
```

### Outline

```glsl
float outline = smoothstep(thickness + aa, thickness - aa, abs(d));
```

### Glow

```glsl
float glow = exp(-d * falloff);
```

### Drop Shadow

```glsl
float shadow = smoothstep(0.0, blur, sdShape(p - shadowOffset));
```

## 3D Raymarching (Basic)

```glsl
float map(vec3 p) {
  float d = sdSphere(p, 1.0);
  d = opSmoothUnion(d, sdBox(p - vec3(1.0, 0.0, 0.0), vec3(0.5)), 0.2);
  return d;
}

vec3 calcNormal(vec3 p) {
  vec2 e = vec2(0.001, 0.0);
  return normalize(vec3(
    map(p + e.xyy) - map(p - e.xyy),
    map(p + e.yxy) - map(p - e.yxy),
    map(p + e.yyx) - map(p - e.yyx)
  ));
}

float raymarch(vec3 ro, vec3 rd) {
  float t = 0.0;
  for (int i = 0; i < 100; i++) {
    vec3 p = ro + rd * t;
    float d = map(p);
    if (d < 0.001) break;
    if (t > 100.0) break;
    t += d;
  }
  return t;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
  vec2 uv = (fragCoord - 0.5 * iResolution.xy) / iResolution.y;
  
  vec3 ro = vec3(0.0, 0.0, 3.0);  // Ray origin
  vec3 rd = normalize(vec3(uv, -1.0));  // Ray direction
  
  float t = raymarch(ro, rd);
  
  vec3 color = vec3(0.0);
  if (t < 100.0) {
    vec3 p = ro + rd * t;
    vec3 n = calcNormal(p);
    vec3 light = normalize(vec3(1.0, 1.0, 1.0));
    float diff = max(dot(n, light), 0.0);
    color = vec3(diff);
  }
  
  fragColor = vec4(color, 1.0);
}
```

## File Structure

```
shader-sdf/
├── SKILL.md
├── references/
│   ├── 2d-primitives.md      # All 2D shapes
│   ├── 3d-primitives.md      # All 3D shapes
│   └── operations.md         # All operations
└── scripts/
    ├── primitives/
    │   ├── 2d.glsl           # 2D shape functions
    │   └── 3d.glsl           # 3D shape functions
    ├── operations.glsl       # Boolean & domain ops
    └── examples/
        ├── logo.glsl         # 2D logo example
        └── raymarch.glsl     # 3D raymarching example
```

## Reference

- `references/2d-primitives.md` — Complete 2D shape library
- `references/3d-primitives.md` — Complete 3D shape library
- `references/operations.md` — All boolean and domain operations
