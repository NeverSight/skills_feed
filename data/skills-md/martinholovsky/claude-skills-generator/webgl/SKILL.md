---
name: webgl
description: WebGL shaders and effects for JARVIS 3D HUD
model: sonnet
risk_level: MEDIUM
version: 1.0.0
---

# WebGL Development Skill

> **File Organization**: This skill uses split structure. See `references/` for advanced patterns and security examples.

## 1. Overview

This skill provides WebGL expertise for creating custom shaders and visual effects in the JARVIS AI Assistant HUD. It focuses on GPU-accelerated rendering with security considerations.

**Risk Level**: MEDIUM - Direct GPU access, potential for resource exhaustion, driver vulnerabilities

**Primary Use Cases**:
- Custom shaders for holographic effects
- Post-processing effects (bloom, glitch)
- Particle systems with compute shaders
- Real-time data visualization

## 2. Core Responsibilities

### 2.1 Fundamental Principles

1. **TDD First**: Write tests before implementation - test shaders, contexts, and resources
2. **Performance Aware**: Optimize GPU usage - batch draws, reuse buffers, compress textures
3. **GPU Safety**: Implement timeout mechanisms and resource limits
4. **Shader Validation**: Validate all shader inputs before compilation
5. **Context Management**: Handle context loss gracefully
6. **Performance Budgets**: Set strict limits on draw calls and triangles
7. **Fallback Strategy**: Provide non-WebGL fallbacks
8. **Memory Management**: Track and limit texture/buffer usage

## 3. Technology Stack & Versions

### 3.1 Browser Support

| Browser | WebGL 2.0 | Notes |
|---------|-----------|-------|
| Chrome | 56+ | Full support |
| Firefox | 51+ | Full support |
| Safari | 15+ | WebGL 2.0 support |
| Edge | 79+ | Chromium-based |

### 3.2 Security Considerations

```typescript
// Check WebGL support and capabilities
function getWebGLContext(canvas: HTMLCanvasElement): WebGL2RenderingContext | null {
  const gl = canvas.getContext('webgl2', {
    alpha: true,
    antialias: true,
    powerPreference: 'high-performance',
    failIfMajorPerformanceCaveat: true  // Fail if software rendering
  })

  if (!gl) {
    console.warn('WebGL 2.0 not supported')
    return null
  }

  return gl
}
```

## 4. Implementation Patterns

### 4.1 Safe Shader Compilation

```typescript
// utils/shaderUtils.ts

// ✅ Safe shader compilation with error handling
export function compileShader(
  gl: WebGL2RenderingContext,
  source: string,
  type: number
): WebGLShader | null {
  const shader = gl.createShader(type)
  if (!shader) return null

  gl.shaderSource(shader, source)
  gl.compileShader(shader)

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const error = gl.getShaderInfoLog(shader)
    console.error('Shader compilation error:', error)
    gl.deleteShader(shader)
    return null
  }

  return shader
}

// ✅ Safe program linking
export function createProgram(
  gl: WebGL2RenderingContext,
  vertexShader: WebGLShader,
  fragmentShader: WebGLShader
): WebGLProgram | null {
  const program = gl.createProgram()
  if (!program) return null

  gl.attachShader(program, vertexShader)
  gl.attachShader(program, fragmentShader)
  gl.linkProgram(program)

  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const error = gl.getProgramInfoLog(program)
    console.error('Program linking error:', error)
    gl.deleteProgram(program)
    return null
  }

  return program
}
```

### 4.2 Context Loss Handling

```typescript
// composables/useWebGL.ts
export function useWebGL(canvas: Ref<HTMLCanvasElement | null>) {
  const gl = ref<WebGL2RenderingContext | null>(null)
  const contextLost = ref(false)

  onMounted(() => {
    if (!canvas.value) return

    // ✅ Handle context loss
    canvas.value.addEventListener('webglcontextlost', (e) => {
      e.preventDefault()
      contextLost.value = true
      console.warn('WebGL context lost')
    })

    canvas.value.addEventListener('webglcontextrestored', () => {
      contextLost.value = false
      initializeGL()
      console.info('WebGL context restored')
    })

    initializeGL()
  })

  function initializeGL() {
    gl.value = getWebGLContext(canvas.value!)
    // Reinitialize all resources
  }

  return { gl, contextLost }
}
```

### 4.3 Holographic Shader

```glsl
// shaders/holographic.frag
#version 300 es
precision highp float;

uniform float uTime;
uniform vec3 uColor;
uniform float uScanlineIntensity;

in vec2 vUv;
out vec4 fragColor;

void main() {
  // Scanline effect
  float scanline = sin(vUv.y * 200.0 + uTime * 2.0) * 0.5 + 0.5;
  scanline = mix(1.0, scanline, uScanlineIntensity);

  // Edge glow
  float edge = smoothstep(0.0, 0.1, vUv.x) *
               smoothstep(1.0, 0.9, vUv.x) *
               smoothstep(0.0, 0.1, vUv.y) *
               smoothstep(1.0, 0.9, vUv.y);

  vec3 color = uColor * scanline * edge;
  float alpha = edge * 0.8;

  fragColor = vec4(color, alpha);
}
```

### 4.4 Resource Management

```typescript
// utils/resourceManager.ts
export class WebGLResourceManager {
  private textures: Set<WebGLTexture> = new Set()
  private buffers: Set<WebGLBuffer> = new Set()
  private programs: Set<WebGLProgram> = new Set()

  private textureMemory = 0
  private readonly MAX_TEXTURE_MEMORY = 256 * 1024 * 1024  // 256MB

  constructor(private gl: WebGL2RenderingContext) {}

  createTexture(width: number, height: number): WebGLTexture | null {
    const size = width * height * 4  // RGBA

    // ✅ Enforce memory limits
    if (this.textureMemory + size > this.MAX_TEXTURE_MEMORY) {
      console.error('Texture memory limit exceeded')
      return null
    }

    const texture = this.gl.createTexture()
    if (texture) {
      this.textures.add(texture)
      this.textureMemory += size
    }
    return texture
  }

  dispose(): void {
    this.textures.forEach(t => this.gl.deleteTexture(t))
    this.buffers.forEach(b => this.gl.deleteBuffer(b))
    this.programs.forEach(p => this.gl.deleteProgram(p))
    this.textureMemory = 0
  }
}
```

### 4.5 Uniform Validation

```typescript
// ✅ Type-safe uniform setting
export function setUniforms(
  gl: WebGL2RenderingContext,
  program: WebGLProgram,
  uniforms: Record<string, number | number[] | Float32Array>
): void {
  for (const [name, value] of Object.entries(uniforms)) {
    const location = gl.getUniformLocation(program, name)
    if (!location) {
      console.warn(`Uniform '${name}' not found`)
      continue
    }

    if (typeof value === 'number') {
      gl.uniform1f(location, value)
    } else if (Array.isArray(value)) {
      switch (value.length) {
        case 2: gl.uniform2fv(location, value); break
        case 3: gl.uniform3fv(location, value); break
        case 4: gl.uniform4fv(location, value); break
        case 16: gl.uniformMatrix4fv(location, false, value); break
      }
    }
  }
}
```

## 5. Implementation Workflow (TDD)

### 5.1 Step-by-Step Process

1. **Write failing test** -> 2. **Implement minimum** -> 3. **Refactor** -> 4. **Verify**

```typescript
// Step 1: tests/webgl/shaderCompilation.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { compileShader } from '@/utils/shaderUtils'

describe('WebGL Shader Compilation', () => {
  let gl: WebGL2RenderingContext

  beforeEach(() => {
    gl = document.createElement('canvas').getContext('webgl2')!
  })

  it('should compile valid shader', () => {
    const source = `#version 300 es
      in vec4 aPosition;
      void main() { gl_Position = aPosition; }`
    expect(compileShader(gl, source, gl.VERTEX_SHADER)).not.toBeNull()
  })

  it('should return null for invalid shader', () => {
    expect(compileShader(gl, 'invalid', gl.FRAGMENT_SHADER)).toBeNull()
  })
})

// Step 2-3: Implement and refactor (see section 4.1)
// Step 4: npm test && npm run typecheck && npm run build
```

### 5.2 Testing Context and Resources

```typescript
describe('WebGL Context', () => {
  it('should handle context loss', async () => {
    const { gl, contextLost } = useWebGL(ref(canvas))
    gl.value?.getExtension('WEBGL_lose_context')?.loseContext()
    await nextTick()
    expect(contextLost.value).toBe(true)
  })
})

describe('Resource Manager', () => {
  it('should enforce memory limits', () => {
    const manager = new WebGLResourceManager(gl)
    expect(manager.createTexture(1024, 1024)).not.toBeNull()
    expect(manager.createTexture(16384, 16384)).toBeNull() // Exceeds limit
  })
})
```

## 6. Performance Patterns

### 6.1 Buffer Reuse

```typescript
// Bad - Creates new buffer every frame
const buffer = gl.createBuffer()
gl.bufferData(gl.ARRAY_BUFFER, data, gl.DYNAMIC_DRAW)
gl.deleteBuffer(buffer)

// Good - Reuse buffer, update only data
gl.bufferSubData(gl.ARRAY_BUFFER, 0, data)  // Update existing buffer
```

### 6.2 Draw Call Batching

```typescript
// Bad - One draw call per object
objects.forEach(obj => {
  gl.useProgram(obj.program)
  gl.drawElements(...)
})

// Good - Batch by material/shader
const batches = groupByMaterial(objects)
batches.forEach(batch => {
  gl.useProgram(batch.program)
  batch.objects.forEach(obj => gl.drawElements(...))
})
```

### 6.3 Texture Compression

```typescript
// Bad - Always uncompressed RGBA
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image)

// Good - Use compressed formats when available
const ext = gl.getExtension('WEBGL_compressed_texture_s3tc')
if (ext) gl.compressedTexImage2D(gl.TEXTURE_2D, 0, ext.COMPRESSED_RGBA_S3TC_DXT5_EXT, ...)
```

### 6.4 Instanced Rendering

```typescript
// Bad - Individual draw calls for particles
particles.forEach(p => {
  gl.uniform3fv(uPosition, p.position)
  gl.drawArrays(gl.TRIANGLES, 0, 6)
})

// Good - Single instanced draw call
gl.drawArraysInstanced(gl.TRIANGLES, 0, 6, particles.length)
```

### 6.5 VAO Usage

```typescript
// Bad - Rebind attributes every frame
gl.enableVertexAttribArray(0)
gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0)

// Good - Use VAO to store attribute state
const vao = gl.createVertexArray()
gl.bindVertexArray(vao)
// Set up once, then just bind VAO for rendering
```

## 7. Security Standards

### 7.1 Known Vulnerabilities

| CVE | Severity | Description | Mitigation |
|-----|----------|-------------|------------|
| CVE-2024-11691 | HIGH | Apple M series memory corruption | Update browser, OS patches |
| CVE-2023-1531 | HIGH | Chrome use-after-free | Update Chrome |

### 7.2 OWASP Top 10 Coverage

| OWASP Category | Risk | Mitigation |
|----------------|------|------------|
| A06 Vulnerable Components | HIGH | Keep browsers updated |
| A10 SSRF | LOW | Context isolation by browser |

### 7.3 GPU Resource Protection

```typescript
// ✅ Implement resource limits
const LIMITS = {
  maxDrawCalls: 100,
  maxTriangles: 1_000_000,
  maxTextures: 32,
  maxTextureSize: 4096
}

function checkLimits(stats: RenderStats): boolean {
  if (stats.drawCalls > LIMITS.maxDrawCalls) {
    console.error('Draw call limit exceeded')
    return false
  }
  if (stats.triangles > LIMITS.maxTriangles) {
    console.error('Triangle limit exceeded')
    return false
  }
  return true
}
```

## 8. Common Mistakes & Anti-Patterns

### 8.1 Critical Security Anti-Patterns

#### Never: Skip Context Loss Handling

```typescript
// ❌ DANGEROUS - App crashes on context loss
const gl = canvas.getContext('webgl2')
// No context loss handler!

// ✅ SECURE - Handle gracefully
canvas.addEventListener('webglcontextlost', handleLoss)
canvas.addEventListener('webglcontextrestored', handleRestore)
```

#### Never: Unlimited Resource Allocation

```typescript
// ❌ DANGEROUS - GPU memory exhaustion
for (let i = 0; i < userCount; i++) {
  textures.push(gl.createTexture())
}

// ✅ SECURE - Enforce limits
if (textureCount < MAX_TEXTURES) {
  textures.push(gl.createTexture())
}
```

### 8.2 Performance Anti-Patterns

#### Avoid: Excessive State Changes

```typescript
// ❌ BAD - Unbatched draw calls
objects.forEach(obj => {
  gl.useProgram(obj.program)
  gl.bindTexture(gl.TEXTURE_2D, obj.texture)
  gl.drawElements(...)
})

// ✅ GOOD - Batch by material
batches.forEach(batch => {
  gl.useProgram(batch.program)
  gl.bindTexture(gl.TEXTURE_2D, batch.texture)
  batch.objects.forEach(obj => gl.drawElements(...))
})
```

## 9. Pre-Implementation Checklist

### Phase 1: Before Writing Code
- [ ] Write failing tests for shaders, context, and resources
- [ ] Define performance budgets (draw calls <100, memory <256MB)
- [ ] Identify required WebGL extensions

### Phase 2: During Implementation
- [ ] Context loss handling with recovery
- [ ] Resource limits and memory tracking
- [ ] Shader validation before compilation
- [ ] Use VAOs, batch draws, reuse buffers
- [ ] Instanced rendering for particles

### Phase 3: Before Committing
- [ ] Tests pass: `npm test -- --run tests/webgl/`
- [ ] Type check: `npm run typecheck`
- [ ] Build: `npm run build`
- [ ] Performance verified (draws, memory)
- [ ] Fallback for no WebGL tested

## 10. Summary

WebGL provides GPU-accelerated graphics for JARVIS HUD. Key principles: handle context loss, enforce resource limits, validate shaders, track memory, batch draw calls, minimize state changes.

**Remember**: WebGL bypasses browser sandboxing - always protect against resource exhaustion.
**References**: `references/advanced-patterns.md`, `references/security-examples.md`
