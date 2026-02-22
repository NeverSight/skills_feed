---
name: architecture-rendering
description: Generate photorealistic architectural renders and visualizations using each::sense AI. Create exterior views, interior renders, sketch-to-render conversions, and more for architects, designers, and real estate professionals.
metadata:
  author: eachlabs
  version: "1.0"
---

# Architecture Rendering

Generate stunning architectural visualizations using each::sense. This skill creates photorealistic renders from sketches, floor plans, and text descriptions for architects, interior designers, real estate developers, and visualization studios.

## Features

- **Exterior Renders**: Photorealistic building exteriors with landscaping and context
- **Interior Visualization**: Detailed interior spaces with furniture, lighting, and materials
- **Sketch to Render**: Transform hand-drawn sketches into photorealistic images
- **Aerial Views**: Bird's eye perspectives and drone-style shots
- **Night Scenes**: Dramatic nighttime renders with artificial lighting
- **Construction Visualization**: Progress renders and phased development views
- **Historical Restoration**: Visualize restored heritage buildings
- **Landscape Architecture**: Gardens, parks, and outdoor spaces

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photorealistic exterior render of a modern minimalist house with floor-to-ceiling glass windows, white concrete walls, flat roof, surrounded by a manicured garden with a pool",
    "mode": "max"
  }'
```

## Common Render Types & Specifications

| Render Type | Typical Aspect Ratio | Best For |
|-------------|---------------------|----------|
| Exterior Hero Shot | 16:9 | Marketing, presentations |
| Interior Room View | 4:3 or 16:9 | Interior design proposals |
| Aerial/Bird's Eye | 16:9 or 1:1 | Site plans, masterplans |
| Vertical Facade | 9:16 or 3:4 | Social media, tall buildings |
| Construction Progress | 16:9 | Client updates, documentation |

## Use Case Examples

### 1. Exterior Building Render

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photorealistic exterior render of a contemporary three-story residential building. Features: exposed concrete and timber cladding, large balconies with glass railings, green roof terrace, floor-to-ceiling windows. Environment: urban street setting, mature trees, late afternoon golden hour lighting, slight overcast for soft shadows. Professional architectural photography style.",
    "mode": "max"
  }'
```

### 2. Interior Architectural Render

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photorealistic interior render of a luxury open-plan living room. Features: double-height ceiling with exposed wooden beams, polished concrete floors, a large sectional sofa in cream fabric, floor-to-ceiling windows overlooking mountains, modern fireplace with black steel surround, pendant lighting fixtures. Style: Scandinavian minimalism meets industrial. Warm natural daylight flooding through windows.",
    "mode": "max"
  }'
```

### 3. Sketch to Render Conversion

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this architectural sketch into a photorealistic render. Interpret it as a modern office building with glass curtain wall facade, steel structural elements visible, rooftop garden. Add realistic context: urban setting, pedestrians, cars, trees. Professional architectural visualization quality, sunny day with blue sky and some clouds.",
    "mode": "max",
    "image_urls": ["https://example.com/architecture-sketch.jpg"]
  }'
```

### 4. Modern House Visualization

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a photorealistic render of a modern single-family home. Architecture: two-story with cantilevered upper floor, white stucco exterior, dark bronze window frames, integrated garage, flat roof with hidden parapets. Landscaping: drought-tolerant native plants, gravel pathways, specimen olive tree. Setting: hillside lot with city views in background. Time: dusk with interior lights glowing warmly, exterior accent lighting.",
    "mode": "max"
  }'
```

### 5. Commercial Building Render

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional architectural visualization of a 20-story commercial office tower. Design: curtain wall glass facade with vertical aluminum fins for solar shading, ground floor retail with double-height lobby, green terraces every 5 floors, rooftop helipad. Context: downtown business district, plaza with water feature at entrance, people walking. Lighting: midday sun, crisp shadows, reflections in glass.",
    "mode": "max"
  }'
```

### 6. Landscape Architecture Visualization

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Render a landscape architecture design for a public urban park. Features: meandering pedestrian paths with permeable pavers, native wildflower meadows, a central pond with wooden deck overlook, children playground with natural materials, seating areas with shade structures, mature deciduous and evergreen trees. Include families enjoying the space, joggers, people walking dogs. Spring season, sunny day, vibrant green foliage.",
    "mode": "max"
  }'
```

### 7. Night Scene Render

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a dramatic nighttime architectural render of a luxury boutique hotel entrance. Building: Art Deco revival style with geometric patterns, brass detailing, black granite facade. Lighting: warm interior glow through large windows, facade uplighting highlighting architectural details, subtle landscape lighting, illuminated hotel sign. Scene: valet area with luxury car, doorman, guests arriving. Atmosphere: sophisticated, inviting, slight wet pavement reflections from recent rain.",
    "mode": "max"
  }'
```

### 8. Aerial/Bird's Eye View

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an aerial architectural render of a mixed-use development masterplan. Layout: central public plaza, surrounding mid-rise residential buildings (6-8 stories), ground floor retail, underground parking entrances, community center with distinctive curved roof. Include: rooftop gardens, tree-lined streets, pedestrian promenades, outdoor dining areas. View: 45-degree angle bird's eye perspective, showing the full development and neighborhood context. Clear day, afternoon light.",
    "mode": "max"
  }'
```

### 9. Construction Progress Visualization

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a construction progress visualization showing a residential tower at 60% completion. Show: concrete core structure complete, lower floors with installed curtain wall glazing, upper floors with exposed steel framing and temporary weather protection, tower crane active, construction workers on scaffolding (safe distances), ground level site office and material staging. Style: documentary realism, overcast day for even lighting, professional construction photography look.",
    "mode": "max"
  }'
```

### 10. Historical Building Restoration Render

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Visualize a restored Victorian-era mansion. Architecture: three-story red brick with ornate white trim, wraparound porch with turned columns, steep gabled roof with decorative shingles, restored original windows with period-appropriate shutters, chimney stacks. Grounds: formal English garden with boxwood hedges, gravel carriage drive, restored iron fence and gate. Show both the historical authenticity and modern updates like subtle landscape lighting. Golden hour lighting, autumn foliage.",
    "mode": "max"
  }'
```

## Best Practices

### Render Quality Tips

- **Lighting**: Specify time of day and weather conditions for appropriate shadows and mood
- **Materials**: Describe textures explicitly (polished concrete, brushed steel, matte wood)
- **Context**: Include surroundings (streets, vegetation, people) for realism
- **Scale Reference**: Add people, cars, or furniture to convey scale
- **Camera Angle**: Specify perspective (eye-level, low angle, bird's eye)

### Prompt Structure for Architecture

When creating architectural renders, include these elements:

1. **Building Type**: Residential, commercial, institutional, mixed-use
2. **Architectural Style**: Modern, contemporary, traditional, industrial
3. **Key Features**: Materials, facade elements, structural systems
4. **Environment**: Urban, suburban, rural, waterfront
5. **Time & Weather**: Golden hour, midday, dusk, night; sunny, overcast, dramatic
6. **View Angle**: Eye-level, aerial, worm's eye, three-quarter view
7. **Context Elements**: People, vehicles, landscaping, neighboring buildings

### Example Prompt Template

```
"Create a photorealistic [view type] render of a [building type].
Architecture: [style], [key features], [materials].
Environment: [setting], [landscaping].
Lighting: [time of day], [weather conditions].
Include: [context elements like people, cars, etc.]
Style: [professional architectural visualization / specific mood]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast drafts or final presentation quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final presentations, client deliverables, marketing materials | Slower | Highest |
| `eco` | Quick concept exploration, early design iterations, massing studies | Faster | Good |

## Multi-Turn Design Iteration

Use `session_id` to iterate on architectural renders:

```bash
# Initial concept render
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an exterior render of a modern beach house with large glass walls and a wooden deck",
    "session_id": "beach-house-project",
    "mode": "eco"
  }'

# Design revision
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a rooftop terrace with a pergola and outdoor kitchen. Make the facade more tropical with natural stone accents.",
    "session_id": "beach-house-project"
  }'

# Time of day variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a sunset version of this design with warm lighting and the interior lights starting to glow",
    "session_id": "beach-house-project",
    "mode": "max"
  }'
```

## Presentation Set Generation

Generate a complete set of renders for a project:

```bash
# Hero exterior shot
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the main exterior hero shot of our modern villa project - front facade, golden hour, dramatic angle",
    "session_id": "villa-presentation",
    "mode": "max"
  }'

# Interior living space
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create an interior render of the main living area - open plan, same modern style, afternoon light",
    "session_id": "villa-presentation",
    "mode": "max"
  }'

# Aerial site view
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an aerial view showing the villa in its landscape context - pool, garden, and property boundaries",
    "session_id": "villa-presentation",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Low quality output | Insufficient detail in prompt | Add more specific architectural details, materials, lighting |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product visualization
- `interior-design-generation` - Interior styling focus
