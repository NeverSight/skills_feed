---
name: floor-plan-generation
description: Generate floor plans and architectural layouts using each::sense AI. Create apartment designs, house layouts, office spaces, retail stores, restaurants, and 3D visualizations with furniture arrangements and measurements.
metadata:
  author: eachlabs
  version: "1.0"
---

# Floor Plan Generation

Generate professional floor plans and architectural layouts using each::sense. This skill creates 2D floor plans, 3D visualizations, and interior layouts for residential, commercial, and retail spaces.

## Features

- **Residential Floor Plans**: Houses, apartments, condos, and multi-story homes
- **Commercial Layouts**: Office spaces, co-working areas, meeting rooms
- **Retail Designs**: Store layouts, product placement, customer flow optimization
- **Restaurant Plans**: Kitchen layouts, dining areas, bar setups
- **3D Visualizations**: Rendered floor plans with depth and perspective
- **Furniture Arrangements**: Interior design with furniture placement
- **Measurements & Annotations**: Scaled plans with dimensions

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a floor plan for a modern 2-bedroom apartment, approximately 900 sq ft, with open kitchen and living area",
    "mode": "max"
  }'
```

## Floor Plan Types & Use Cases

| Type | Description | Common Applications |
|------|-------------|---------------------|
| 2D Floor Plan | Top-down schematic view | Architecture, real estate listings |
| 3D Floor Plan | Isometric or perspective view | Marketing, client presentations |
| Furnished Plan | Layout with furniture | Interior design, staging |
| Technical Plan | With measurements and annotations | Construction, permits |
| Conceptual Plan | Quick sketch style | Early design phases |

## Use Case Examples

### 1. Generate Floor Plan from Description

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a floor plan for a single-story family home with 3 bedrooms, 2 bathrooms, a large open-concept kitchen and living room, home office, and attached 2-car garage. Modern minimalist style.",
    "mode": "max"
  }'
```

### 2. Apartment Layout Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a studio apartment floor plan, 550 sq ft. Include a sleeping area, kitchenette, bathroom, and living space. Maximize natural light with large windows. Modern urban style with efficient use of space.",
    "mode": "max"
  }'
```

### 3. House Floor Plan

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a traditional 2-story house floor plan. Ground floor: entryway, living room, dining room, kitchen, half bath, mudroom. Second floor: master suite with walk-in closet and en-suite, 3 additional bedrooms, 2 full bathrooms, laundry room. Approximately 2,800 sq ft total.",
    "mode": "max"
  }'
```

### 4. Office Space Plan

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design an open office floor plan for a tech startup, 3,000 sq ft. Include: open workspace for 30 employees with standing desk options, 3 private offices, 2 meeting rooms (one for 8, one for 4), a phone booth area, kitchen/break room, reception area, and server room. Modern collaborative workspace aesthetic.",
    "mode": "max"
  }'
```

### 5. Restaurant Layout

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a floor plan for a 2,500 sq ft casual dining restaurant. Include: main dining area seating 60 guests, bar area with 12 bar stools, commercial kitchen with separate prep and cooking areas, walk-in cooler, restrooms, staff area, and outdoor patio seating for 20. Optimize customer flow and server paths.",
    "mode": "max"
  }'
```

### 6. Retail Store Layout

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a retail clothing store floor plan, 1,800 sq ft. Include: storefront display windows, main sales floor with clothing racks and display tables, fitting rooms (4 units), checkout counter area, stockroom, and small office. Create a customer journey that maximizes product exposure. Contemporary boutique style.",
    "mode": "max"
  }'
```

### 7. 3D Floor Plan Visualization

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D isometric floor plan visualization of a luxury penthouse apartment. Show the layout from an elevated angle with visible furniture, textures, and materials. Include living room, dining area, gourmet kitchen, master bedroom, two guest bedrooms, and wraparound terrace. High-end modern interior design with warm lighting.",
    "mode": "max"
  }'
```

### 8. Furniture Arrangement Plan

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a furnished floor plan for a 400 sq ft living room. The room is rectangular (20ft x 20ft) with windows on the south wall and entry door on the north wall. Include furniture placement for: sectional sofa, coffee table, TV console, two accent chairs, bookshelf, and floor lamp. Focus on conversation-friendly arrangement with good TV viewing angles.",
    "mode": "max"
  }'
```

### 9. Multi-Story Floor Plan

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a 3-story townhouse floor plan. Basement: home gym, media room, full bathroom, utility room. Ground floor: open living/dining/kitchen, powder room, back patio access. Second floor: master suite with walk-in closet and spa bathroom, two bedrooms with shared bathroom, small home office nook. Show all three levels side by side.",
    "mode": "max"
  }'
```

### 10. Floor Plan with Measurements

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a technical floor plan with detailed measurements for a 1,200 sq ft 2-bedroom apartment. Show room dimensions, door widths, window placements with sizes, and wall thicknesses. Include: living room (15x18 ft), kitchen (10x12 ft), master bedroom (12x14 ft), second bedroom (10x12 ft), bathroom (8x6 ft), and hallway. Architectural blueprint style with dimension lines.",
    "mode": "max"
  }'
```

## Best Practices

### Floor Plan Specifications
- **Include square footage**: Helps AI understand scale and proportions
- **Specify room types**: Be explicit about which rooms you need
- **Mention style**: Modern, traditional, industrial, minimalist, etc.
- **Consider flow**: Describe how spaces should connect

### Detailed Descriptions
- **Functional requirements**: Number of occupants, specific use cases
- **Adjacencies**: Which rooms should be near each other
- **Special features**: Walk-in closets, islands, built-ins
- **Orientation**: Window placement, natural light preferences

### Visual Style
- **2D schematic**: Clean lines, architectural symbols
- **3D rendered**: Realistic textures and lighting
- **Sketch style**: Conceptual, hand-drawn look
- **Blueprint**: Technical with measurements

## Prompt Tips for Floor Plans

When requesting floor plans, include these details:

1. **Space Type**: Residential, commercial, retail, restaurant
2. **Total Area**: Square footage or meters
3. **Room List**: All rooms and spaces needed
4. **Style**: Architectural and interior design style
5. **View Type**: 2D top-down, 3D isometric, perspective
6. **Special Requirements**: Accessibility, specific features
7. **Level of Detail**: Conceptual, furnished, technical

### Example Prompt Structure

```
"Create a [view type] floor plan for a [space type], [total area].
Include [room list].
Style: [architectural/interior style].
[Additional requirements like measurements, furniture, etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final presentations, client deliverables, detailed plans | Slower | Highest |
| `eco` | Quick concepts, initial drafts, exploring options | Faster | Good |

## Multi-Turn Design Iteration

Use `session_id` to iterate on floor plan designs:

```bash
# Initial floor plan
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a floor plan for a 1,500 sq ft 3-bedroom ranch house with open concept living",
    "session_id": "floorplan-project-001"
  }'

# Request modification
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a sunroom off the living area and make the master closet larger",
    "session_id": "floorplan-project-001"
  }'

# Convert to 3D view
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now show this floor plan as a 3D visualization with modern furniture",
    "session_id": "floorplan-project-001"
  }'
```

## Batch Generation for Comparisons

Generate multiple layout options for comparison:

```bash
# Option A - Open concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2-bedroom apartment floor plan, 1,000 sq ft, with completely open concept living/dining/kitchen",
    "mode": "eco"
  }'

# Option B - Defined spaces
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2-bedroom apartment floor plan, 1,000 sq ft, with separate defined living room, dining room, and kitchen",
    "mode": "eco"
  }'

# Option C - Split bedroom layout
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2-bedroom apartment floor plan, 1,000 sq ft, with bedrooms on opposite sides of the unit for maximum privacy",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `interior-design-generation` - Room styling and decor
- `architectural-visualization` - Building exteriors and renders
- `real-estate-marketing` - Property marketing visuals
