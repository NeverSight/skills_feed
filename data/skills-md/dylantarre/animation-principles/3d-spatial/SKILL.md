---
name: 3d-spatial
description: Use when working in Blender, Unity 3D, Unreal Engine, Cinema 4D, VR/AR applications, or any three-dimensional animation work.
---

# 3D Spatial Animation

Apply Disney's 12 animation principles to 3D software, VR/AR, and spatial computing environments.

## Quick Reference

| Principle | 3D/Spatial Implementation |
|-----------|--------------------------|
| Squash & Stretch | Lattice deformers, blend shapes |
| Anticipation | IK/FK wind-ups, camera pre-motion |
| Staging | Camera angles, lighting, depth |
| Straight Ahead / Pose to Pose | Layered animation vs blocking |
| Follow Through / Overlapping | Bone chains, physics simulation |
| Slow In / Slow Out | F-curve editing, animation curves |
| Arc | IK handles, motion paths in 3D space |
| Secondary Action | Cloth sim, particle systems, environment |
| Timing | Frame timing, VR 90fps requirements |
| Exaggeration | Stylized deformation, pushed poses |
| Solid Drawing | Volume preservation, silhouettes |
| Appeal | Character design, satisfying motion |

## Principle Applications

**Squash & Stretch**: Use lattice or mesh deformers for organic squash. Blend shapes for facial deformation. Scale bones in hierarchies. Always preserve volume—if Y compresses, X/Z expand.

**Anticipation**: IK rig wind-ups for character animation. Camera pulls back before push-in. Objects coil before release. VR: telegraph actions clearly for user comfort.

**Staging**: Camera angle sells the action. Three-point lighting directs focus. Depth of field isolates subjects. In VR, use spatial audio and lighting to guide attention.

**Straight Ahead vs Pose to Pose**: Block key poses first (pose to pose), then refine (spline). Use layered animation—body first, then overlapping elements. Procedural secondary motion is straight ahead.

**Follow Through & Overlapping**: Bone chains for tails, hair, capes. Physics simulation for cloth and particles. Delay child bones from parents. Jiggle deformers for organic follow-through.

**Slow In / Slow Out**: F-curves (Blender), Animation Curves (Unity), Graph Editor (Maya). Tangent handles control easing. Flat tangents = slow, steep = fast. Never leave curves linear.

**Arc**: Motion paths visible in 3D space. IK handles naturally create arcs. Check arcs from multiple camera angles. FK rotation creates inherent arcs in hierarchies.

**Secondary Action**: Cloth simulation responds to primary motion. Particles emit on impacts. Environment objects react to character. Facial animation supports body action.

**Timing**: Film: 24fps with motion blur. Games: 60fps minimum. VR: 90fps required (72-120fps). Frame timing affects perceived weight—heavy = slower, light = faster.

**Exaggeration**: Push poses beyond anatomical limits for style. Smear frames for fast motion. Exaggerated anticipation and follow-through. VR: be careful—exaggeration can cause discomfort.

**Solid Drawing**: Check silhouettes from all angles. Maintain volume during deformation. Strong poses read in profile. Avoid interpenetration and broken geometry.

**Appeal**: Character design serves animation needs. Weight and balance feel believable. Movement has personality. In VR, presence and comfort are paramount.

## Software Techniques

### Blender
```python
# Add follow-through with driver
# On child bone, add driver to rotation
driver.expression = "var * 0.3"
driver.variables["var"].source = parent_bone.rotation

# Physics-based secondary
bpy.ops.object.modifier_add(type='CLOTH')
bpy.context.object.modifiers["Cloth"].settings.quality = 10
```

### Unity
```csharp
// Spring-based follow through
public class SpringFollow : MonoBehaviour {
    public Transform target;
    public float springStrength = 10f;
    public float damping = 0.5f;

    private Vector3 velocity;

    void Update() {
        Vector3 delta = target.position - transform.position;
        velocity += delta * springStrength * Time.deltaTime;
        velocity *= 1f - damping * Time.deltaTime;
        transform.position += velocity * Time.deltaTime;
    }
}
```

## VR/AR Considerations

| Aspect | Requirement |
|--------|-------------|
| Framerate | 90fps minimum, 120fps preferred |
| Motion | Avoid camera animation—user controls view |
| Comfort | Gradual acceleration, avoid sudden motion |
| Scale | Animations must work at world scale |
| Interaction | Clear feedback for hand/controller input |

## Performance Notes

- LOD (Level of Detail) for distant animations
- Bake complex simulations when possible
- GPU skinning for character meshes
- Culling animations outside view frustum
- VR: maintain framerate above all else
