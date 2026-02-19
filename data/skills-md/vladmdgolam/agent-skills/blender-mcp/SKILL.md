---
name: blender-mcp
description: "Blender MCP expert for scene inspection, Python scripting, GLTF export, and material/animation extraction. Activate when: (1) using Blender MCP tools (get_scene_info, execute_python, screenshot, etc.), (2) writing Blender Python scripts for extraction or manipulation, (3) exporting scenes to GLTF/GLB for web (Three.js, R3F), (4) debugging material or texture export losses, (5) optimizing GLB files with gltf-transform, (6) using asset integrations (PolyHaven, Sketchfab, Hyper3D Rodin, Hunyuan3D). Covers critical export gotchas, material mapping survival, texture optimization pipeline, headless CLI patterns, and known failure modes."
---

# Blender MCP

## Tool Selection

Use **structured MCP tools** (`get_scene_info`, `screenshot`) for quick inspection.

Use **`execute_python`** for anything non-trivial: hierarchy traversal, material extraction, animation baking, bulk operations. It gives full `bpy` API access and avoids tool schema limitations.

Use **headless CLI** for GLTF exports — the MCP server times out on export operations.

## Health Check (Always First)

1. `get_scene_info` — verify connection (default port 9876)
2. `execute_python` with `print("ok")` — verify Python works
3. `screenshot` — verify viewport capture works

If MCP is unresponsive, check that the Blender MCP addon is enabled and the socket server is running.

## Critical Rules

### 1. MCP Server Times Out on Exports

The Blender MCP server cannot handle GLTF exports — they exceed the timeout. Always use headless CLI:

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background "scene.blend" --python-expr "
import bpy, os
export_path = 'output.glb'
os.makedirs(os.path.dirname(export_path), exist_ok=True)
bpy.ops.export_scene.gltf(
    filepath=export_path,
    export_format='GLB',
    export_apply=False,
    export_animations=True,
    export_nla_strips=True,
    export_cameras=True,
    export_lights=False,
    export_draco_mesh_compression_enable=False,
)
print(f'Size: {os.path.getsize(export_path)/1024/1024:.1f} MB')
"
```

### 2. Do NOT Apply Modifiers on Export

Set `export_apply=False`. Array modifiers (circular patterns, linear repeats) balloon file size when baked. Replicate them at runtime instead.

Example: 16 roller instances via Array modifier = ~1 MB GLB. Baked = ~56 MB GLB.

### 3. Export WITHOUT Draco First

If you plan to optimize with `gltf-transform`, export without Draco compression. Re-encoding existing Draco corrupts meshes. Apply Draco as the final step.

### 4. Procedural Textures Don't Export to GLTF

These Blender node setups are **lost** on export:

| Node Setup | What's Lost | Workaround |
|------------|-------------|------------|
| Noise Texture → roughness | Entire procedural chain | Bake to texture, or shader patch at runtime |
| Color Ramp on roughness texture | Value remapping range | Manual roughness values, or runtime remap |
| Procedural bump (Noise → Bump) | Bump detail | Bake normal map in Blender |
| Mix Shader with complex factor | Blend logic | Simplify to single BSDF before export |

**What DOES export:** flat roughness/metallic values, image textures (without Color Ramp remapping), baked normal maps, PBR texture sets (baseColor, metallicRoughness, normal).

### 5. GLTF Name Mapping

Blender names are transformed in GLTF:
- Spaces → underscores
- Dots → removed
- Trailing spaces → trailing underscore

| Blender | GLTF |
|---------|------|
| `RINGS ball L` | `RINGS_ball_L` |
| `Sphere.003` | `Sphere003` |
| `RINGS L.001` | `RINGS_L001` |
| `RINGS S ` (trailing space) | `RINGS_S_` |

Always check names in the exported GLB, not Blender, when referencing meshes in code.

### 6. Never Use gltf-transform `optimize`

The `optimize` command includes `simplify` which destroys mesh geometry. Use individual steps instead:

```bash
# Resize textures (max 1024x1024)
npx @gltf-transform/cli resize input.glb resized.glb --width 1024 --height 1024

# WebP texture compression
npx @gltf-transform/cli webp resized.glb webp.glb --quality 90

# Draco mesh compression (LAST step)
npx @gltf-transform/cli draco webp.glb output.glb
```

### 7. Quote Paths with Spaces

Blender project paths often contain spaces. Always double-quote:
```bash
/Applications/Blender.app/Contents/MacOS/Blender --background "$HOME/Downloads/blend 3/scene.blend" ...
```

## Scene Extraction Pattern

Full hierarchy with materials, transforms, and modifiers:

```python
import bpy, json

def extract_hierarchy(obj, depth=0):
    data = {
        "name": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "rotation": list(obj.rotation_euler),
        "scale": list(obj.scale),
        "visible": not obj.hide_viewport,
        "children": [],
    }
    if obj.type == 'MESH' and obj.data:
        data["vertices"] = len(obj.data.vertices)
        data["faces"] = len(obj.data.polygons)
        data["materials"] = [slot.material.name for slot in obj.material_slots if slot.material]
    if obj.type == 'LIGHT':
        data["light_type"] = obj.data.type
        data["energy"] = obj.data.energy
        data["color"] = list(obj.data.color)
        if obj.data.type == 'AREA':
            data["size"] = obj.data.size
            data["size_y"] = obj.data.size_y
    # Array modifiers (important for runtime replication)
    for mod in obj.modifiers:
        if mod.type == 'ARRAY':
            data.setdefault("modifiers", []).append({
                "type": "ARRAY",
                "count": mod.count,
                "offset_object": mod.offset_object.name if mod.offset_object else None,
            })
    for child in obj.children:
        data["children"].append(extract_hierarchy(child, depth + 1))
    return data

scene_data = {
    "name": bpy.context.scene.name,
    "fps": bpy.context.scene.render.fps,
    "frame_start": bpy.context.scene.frame_start,
    "frame_end": bpy.context.scene.frame_end,
    "objects": [],
}

for obj in bpy.context.scene.objects:
    if obj.parent is None:
        scene_data["objects"].append(extract_hierarchy(obj))

print(json.dumps(scene_data, indent=2))
```

## Material Extraction Pattern

```python
import bpy, json

def extract_materials():
    materials = []
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        info = {"name": mat.name, "nodes": []}
        for node in mat.node_tree.nodes:
            node_data = {"type": node.type, "name": node.name}
            if node.type == 'BSDF_PRINCIPLED':
                for inp in node.inputs:
                    if inp.is_linked:
                        node_data[inp.name] = "linked"
                    elif hasattr(inp, 'default_value'):
                        val = inp.default_value
                        try:
                            node_data[inp.name] = list(val)
                        except TypeError:
                            node_data[inp.name] = float(val)
            if node.type == 'TEX_IMAGE' and node.image:
                node_data["image"] = node.image.filepath
                node_data["size"] = [node.image.size[0], node.image.size[1]]
            info["nodes"].append(node_data)
        materials.append(info)
    return materials

print(json.dumps(extract_materials(), indent=2))
```

## Animation Keyframe Extraction

```python
import bpy, json

def extract_animation(obj):
    if not obj.animation_data or not obj.animation_data.action:
        return None
    tracks = []
    for fc in obj.animation_data.action.fcurves:
        keyframes = []
        for kp in fc.keyframe_points:
            keyframes.append({
                "frame": int(kp.co[0]),
                "value": float(kp.co[1]),
                "interpolation": kp.interpolation,
            })
        tracks.append({
            "data_path": fc.data_path,
            "index": fc.array_index,
            "keyframes": keyframes,
        })
    return {"object": obj.name, "tracks": tracks}

animations = []
for obj in bpy.data.objects:
    anim = extract_animation(obj)
    if anim:
        animations.append(anim)

print(json.dumps(animations, indent=2))
```

## GLTF Export Settings Reference

| Setting | Value | Why |
|---------|-------|-----|
| `export_format` | `'GLB'` | Single binary file |
| `export_apply` | `False` | Don't bake modifiers (Array, etc.) |
| `export_animations` | `True` | Include animation data |
| `export_nla_strips` | `True` | Bake NLA strips into actions |
| `export_cameras` | `True` | Include camera rigs |
| `export_lights` | `False` | Handle lights in runtime (Three.js/R3F) |
| `export_draco_mesh_compression_enable` | `False` | Apply Draco later via gltf-transform |

## Texture Optimization Pipeline

Target: smallest GLB with acceptable visual quality.

```
Blender export (no Draco) → resize (1K max) → WebP (q90) → Draco
   ~22 MB                    ~3.7 MB           ~3.7 MB      ~1 MB
```

Key insights:
- 4K textures (4096x4096) = ~89 MB GPU memory per texture. 1K = ~5.6 MB. **16x reduction**.
- PNG metallicRoughness textures compress well to WebP at quality 85-90.
- Mobile GPUs (Adreno, Mali) benefit most from texture downscaling.
- Inspect with: `npx @gltf-transform/cli inspect model.glb`

## Asset Integrations

Available through Blender MCP when configured:

| Integration | Capabilities |
|-------------|-------------|
| **PolyHaven** | Search, download, import free HDRIs, textures, and 3D models with auto material setup |
| **Sketchfab** | Search and download models (requires access token) |
| **Hyper3D Rodin** | Generate 3D models from text descriptions or reference images |
| **Hunyuan3D** | Create 3D assets from text prompts, images, or both |

## Known Errors & Workarounds

See [references/errors.md](references/errors.md) for complete error tables.

## Data Output

- `print()` + `json.dumps()` for small results (scene info, single object)
- `/tmp/*.json` for large extraction results (full hierarchy, animation data, material reports)
- Always include metadata: scene name, fps, frame range, Blender version
