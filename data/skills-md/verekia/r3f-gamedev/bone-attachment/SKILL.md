---
name: bone-attachment
description: Attach meshes to bones of a skinned mesh, such as attaching a sword to a character's hand.
---

# Bone Attachment

Attach meshes to bones of a skinned mesh, such as attaching a sword to a character's hand.

## Technique

Create a `BoneChild` component that uses `useEffect` to add a container group to a bone and remove it on cleanup. The bone reference is obtained from the GLTF nodes after loading the model.

## Key Concepts

- Access bones from GLTF nodes (e.g., `nodes.HandR`)
- Use `bone.add(container)` to parent objects to bones
- Clean up with `bone.remove(container)` in useEffect cleanup
- Apply position/rotation/scale offsets to adjust attachment placement

## Usage

```tsx
const { nodes } = useGLTF('/character.glb')

<BoneChild bone={nodes.HandR} position={[0, 0.3, 2]} rotation={[0, 0, 0]}>
  <mesh>
    <boxGeometry />
    <meshBasicMaterial color="red" />
  </mesh>
</BoneChild>
```

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
