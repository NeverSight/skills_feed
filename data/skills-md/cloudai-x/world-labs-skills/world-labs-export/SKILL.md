---
name: world-labs-export
description: World Labs export formats - Gaussian splats, meshes, images, and engine integrations
allowed-tools:
  - Bash
  - WebFetch
---

# World Labs Export & Integration

Export generated worlds in various formats for use in game engines, 3D software, and web applications.

## Export Formats Overview

| Format            | Type           | Best For                       |
| ----------------- | -------------- | ------------------------------ |
| SPZ (2M/500K)     | Gaussian Splat | Native format, highest quality |
| PLY (2M/500K)     | Gaussian Splat | Wide compatibility             |
| Collider Mesh     | GLB            | Physics, collision             |
| High-Quality Mesh | GLB            | Rendering, modification        |
| 360 Panorama      | PNG            | Skyboxes, previews             |

## How to Export from Marble

1. Navigate to your generated world viewer
2. Open the **Download Menu**
3. Select desired format:
   - Splats (SPZ) - High resolution
   - Splats (low-res SPZ) - 500K, lighter compute
   - Splats (PLY) - High resolution, universal compatibility
   - Splats (low-res PLY) - 500K, universal
   - Collider Mesh (GLB) - Instant download
   - High-quality mesh (GLB) - Up to 1 hour processing
   - 360 Panorama

## Gaussian Splat Exports

### SPZ Format (Native)

World Labs' native Gaussian splat format, optimized for file size:

| Variant  | Splat Count | Use Case            |
| -------- | ----------- | ------------------- |
| SPZ 2M   | ~2,000,000  | Maximum quality     |
| SPZ 500K | ~500,000    | Lightweight, mobile |

**Advantages:**

- Smallest file size
- Optimized for Marble rendering
- Fast loading in supported viewers

### PLY Format (Compatible)

Standard point cloud format for broader software support:

| Variant  | Splat Count | Compatibility |
| -------- | ----------- | ------------- |
| PLY 2M   | ~2,000,000  | Universal     |
| PLY 500K | ~500,000    | Universal     |

**Advantages:**

- Wide software support
- Works with most third-party splat viewers
- No conversion needed for many tools

**Conversion Tool:**

- SPZ to PLY: <https://spz-to-ply.netlify.app/>

## Mesh Exports

### Collider Mesh (GLB)

Low-poly mesh for physics and collision:

| Property       | Specification                |
| -------------- | ---------------------------- |
| Triangle count | 100,000 - 200,000            |
| File size      | 3-4 MB                       |
| UVs            | None                         |
| Use            | Collision detection, physics |
| Download       | Instant                      |

### High-Quality Mesh (GLB)

Detailed mesh for rendering—two variants available:

| Variant       | Triangles  | Features              |
| ------------- | ---------- | --------------------- |
| Textured      | ~600,000   | Texture maps included |
| Vertex Colors | ~1,000,000 | Material flexibility  |

| Property        | Specification           |
| --------------- | ----------------------- |
| File size       | 100-200 MB              |
| Processing time | Up to 1 hour            |
| Rate limit      | 4 requests/hour         |
| Availability    | Only for worlds you own |

## Image Exports

### 360 Panorama

| Property   | Specification                       |
| ---------- | ----------------------------------- |
| Resolution | 2560 × 1280                         |
| Format     | Equirectangular PNG                 |
| Use        | Skyboxes, VR preview, presentations |

## Coordinate System

**As of December 2025**, World Labs defaults to **OpenGL convention**:

```
       -Y (down)
        │
        │
        │
        └───────→ +X (left)
       ╱
      ╱
     ↙
    -Z (forward)
```

| Axis | Direction             |
| ---- | --------------------- |
| +X   | Left                  |
| -Y   | Down                  |
| -Z   | Forward (into screen) |

**Legacy OpenCV convention** (older exports):

- +X left, +Y down, +Z forward
- To convert: Scale Y and Z axes by -1

### Conversion to Other Systems

**To Unity (Left-handed Y-up):**

```
Unity.x = WorldLabs.x
Unity.y = -WorldLabs.y
Unity.z = -WorldLabs.z
```

Scale: 1 unit = 1 meter

**To Unreal (Left-handed Z-up):**

```
Unreal.x = -WorldLabs.z * 100  // cm
Unreal.y = WorldLabs.x * 100
Unreal.z = -WorldLabs.y * 100
```

Scale: 1 unit = 1 centimeter

**To Blender (Right-handed Z-up):**

```
Blender.x = WorldLabs.x
Blender.y = -WorldLabs.z
Blender.z = -WorldLabs.y
```

Scale: 1 unit = 1 meter

## Engine Integrations

### Spark.js (Web) — Recommended

Three.js-based web viewer, native integration with World Labs:

- **URL**: <https://sparkjs.dev/>
- **Best for**: VR experiences, interactive web games, custom applications
- **Support**: Active community in World Labs Discord

### Unity

**Plugin**: aras-p UnityGaussianSplatting (Free)

| Setting         | Recommendation       |
| --------------- | -------------------- |
| Unity version   | 6.0 (for VR) or 6.1  |
| Render pipeline | URP with HDR enabled |
| Graphics API    | Vulkan (for VR)      |
| File format     | PLY 2M or SPZ 2M     |

**Notes:**

- 500K SPZ files may require conversion to PLY
- For VR (Quest 3): 500K splats perform better than 2M
- Combine multiple splat components into single component for better draw-order

### Unreal Engine

Multiple third-party plugins available:

| Plugin                   | Notes                                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| **Postshot**             | Recommended. Free version available. Requires standalone Windows app, convert SPZ to PSHT format |
| **Volinga**              | Paid. Supports depth of field, nDisplay for virtual production                                   |
| **3D Gaussians (Akiya)** | Paid. Most reliable, automatic quality splitting, nDisplay support                               |

**Note**: Convert SPZ to PLY if plugin requires it.

### Blender

Multiple third-party plugins:

| Plugin          | URL                 | Notes                                  |
| --------------- | ------------------- | -------------------------------------- |
| **KIRI Engine** | kiriengine.app      | Most maintained, verified Blender 4.2+ |
| **Reshot AI**   | github.com/ReshotAI | Better performance, straightforward    |
| **SplatForge**  | splatforge.cloud    | Most performant, separate render pass  |

### Houdini

**Plugin**: GSOPs

- **URL**: github.com/cgnomads/GSOPs
- **Compatibility**: Houdini 20.5
- **Features**: Splat animation, VDB/mesh conversion

## Format Selection Guide

| Need                | Recommended Format   |
| ------------------- | -------------------- |
| Web viewer          | SPZ 500K or PLY 500K |
| Desktop VR          | PLY 500K             |
| Archive/Quality     | SPZ 2M or PLY 2M     |
| Game engine physics | Collider Mesh GLB    |
| 3D editing          | HQ Mesh GLB + PLY    |
| Quick preview       | 360 Panorama         |
| Mobile/Quest VR     | PLY 500K             |

## Troubleshooting

| Issue                     | Solution                                        |
| ------------------------- | ----------------------------------------------- |
| Assets appear upside-down | Check coordinate system; may need Y/Z axis flip |
| Wrong scale in engine     | Unity uses meters, Unreal uses centimeters      |
| 500K SPZ not loading      | Convert to PLY using spz-to-ply.netlify.app     |
| Draw-order issues         | Combine multiple splats into single component   |

## Related Skills

- `world-labs-api` - API integration
- `world-labs-studio` - Compose and record before export
- `world-labs-chisel` - Create geometry for generation
