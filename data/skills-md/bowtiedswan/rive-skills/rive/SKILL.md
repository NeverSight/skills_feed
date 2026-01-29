---
name: rive
description: |
  Comprehensive Rive animation platform skill covering scripting (Luau), runtime integration (React/Next.js), 
  state machines, data binding, and the complete API. Use this skill when users need to create interactive 
  animations with Rive, integrate Rive into React/Next.js applications, write Rive scripts (Node, Layout, 
  Converter, PathEffect protocols), control animations via state machines, implement scroll-based animations, 
  or work with Rive's drawing API (Path, Paint, Renderer). Triggers on: "rive", "rive animation", "rive script", 
  "luau", "@rive-app/react-canvas", "state machine animation", "interactive animation", "scroll animation with rive".
---

# Rive Animation Platform Skill

This skill provides comprehensive knowledge for working with Rive, an interactive animation platform that enables creating and running interactive graphics across web, mobile, and game platforms.

## Overview

Rive is a design and animation tool that produces lightweight, interactive graphics with a powerful runtime. Key capabilities:

- **Scripting**: Write Luau scripts directly in the Rive Editor to extend functionality
- **State Machines**: Create complex interactive animations with states and transitions
- **Data Binding**: Connect animations to dynamic data via View Models
- **Cross-Platform Runtimes**: Deploy to Web (React/Next.js), iOS, Android, Flutter, Unity, Unreal

## When to Use This Skill

Use this skill when:
- Creating Rive scripts (Node, Layout, Converter, PathEffect protocols)
- Integrating Rive animations into React or Next.js applications
- Implementing scroll-based or parallax animations with Rive
- Working with Rive state machines and inputs at runtime
- Using Rive's drawing API for custom rendering
- Building interactive animations with pointer events
- Implementing data binding with View Models

## Quick Start

### React/Next.js Integration

```tsx
import { useRive } from '@rive-app/react-canvas';

function MyAnimation() {
  const { rive, RiveComponent } = useRive({
    src: '/animation.riv',
    stateMachines: 'MainStateMachine',
    autoplay: true,
  });

  return <RiveComponent style={{ width: 400, height: 400 }} />;
}
```

### Controlling State Machine Inputs

```tsx
const { rive, RiveComponent } = useRive({
  src: '/animation.riv',
  stateMachines: 'State Machine 1',
});

// Get and set inputs
const scrollInput = rive?.stateMachineInputs('State Machine 1')
  ?.find(i => i.name === 'scrollProgress');
  
// Update on scroll (0-100 range example)
scrollInput?.value = scrollProgress * 100;
```

## Rive Scripting (Luau)

Rive scripts use Luau (a Lua variant) and follow specific protocols. For detailed API reference, see `@references/rive-scripting-api.md`.

### Script Protocols Overview

| Protocol | Purpose | Key Functions |
|----------|---------|---------------|
| **Node** | Custom drawing/rendering | `init()`, `advance(seconds)`, `draw(renderer)` |
| **Layout** | Custom layout behaviors | `measure()`, `resize(size)` + Node functions |
| **Converter** | Data transformation | `convert(input)`, `reverseConvert(input)` |
| **PathEffect** | Path modifications | `init()`, `update(pathData)`, `advance(seconds)` |
| **Test** | Testing harnesses | Unit testing scripts |

### Node Script Template

```lua
-- Define script data type with inputs
type MyNode = {
  color: Input<Color>,
  speed: Input<number>,
  path: Path,
  paint: Paint,
}

function init(self: MyNode): boolean
  self.path = Path.new()
  self.paint = Paint.new()
  self.paint.style = 'fill'
  return true
end

function advance(self: MyNode, seconds: number): boolean
  -- Animation logic here, called every frame
  return true -- Return true to keep receiving advance calls
end

function update(self: MyNode)
  -- Called when any input changes
end

function draw(self: MyNode, renderer: Renderer)
  renderer:drawPath(self.path, self.paint)
end

return function(): Node<MyNode>
  return {
    init = init,
    advance = advance,
    update = update,
    draw = draw,
    color = Color.rgba(255, 255, 255, 255),
    speed = 1.0,
    path = late(),
    paint = late(),
  }
end
```

### Layout Script Template

```lua
type MyLayout = {
  spacing: Input<number>,
}

function measure(self: MyLayout): Vec2D
  -- Return desired size (used when Fit type is Hug)
  return Vec2D.xy(200, 100)
end

function resize(self: MyLayout, size: Vec2D)
  -- Called when layout receives new size
  print("New size:", size.x, size.y)
end

-- Include Node functions (init, advance, draw) as needed

return function(): Layout<MyLayout>
  return {
    measure = measure,
    resize = resize,
    spacing = 10,
  }
end
```

### Converter Script Template

```lua
type NumberToString = {}

function convert(self: NumberToString, input: DataInputs): DataOutput
  local dv: DataValueString = DataValue.string()
  if input:isNumber() then
    dv.value = tostring((input :: DataValueNumber).value)
  else
    dv.value = ""
  end
  return dv
end

function reverseConvert(self: NumberToString, input: DataOutput): DataInputs
  local dv: DataValueNumber = DataValue.number()
  if input:isString() then
    dv.value = tonumber((input :: DataValueString).value) or 0
  end
  return dv
end

return function(): Converter<NumberToString, DataValueNumber, DataValueString>
  return {
    convert = convert,
    reverseConvert = reverseConvert,
  }
end
```

### PathEffect Script Template

```lua
type WaveEffect = {
  amplitude: Input<number>,
  frequency: Input<number>,
  context: Context,
}

function init(self: WaveEffect, context: Context): boolean
  self.context = context
  return true
end

function update(self: WaveEffect, inPath: PathData): PathData
  local path = Path.new()
  -- Transform path geometry here
  for i = 1, #inPath do
    local cmd = inPath[i]
    -- Process each PathCommand
  end
  return path
end

function advance(self: WaveEffect, seconds: number): boolean
  -- Called each frame for animated effects
  return true
end

return function(): PathEffect<WaveEffect>
  return {
    init = init,
    update = update,
    advance = advance,
    amplitude = 10,
    frequency = 1,
    context = late(),
  }
end
```

## Script Inputs

Define inputs to expose configurable properties in the Rive Editor:

```lua
type MyNode = {
  -- Basic inputs
  myNumber: Input<number>,
  myColor: Input<Color>,
  myString: string,  -- Non-input, internal use only
  
  -- View Model inputs
  myViewModel: Input<Data.Character>,
  
  -- Artboard inputs (for dynamic instantiation)
  enemyTemplate: Input<Artboard<Data.Enemy>>,
}

-- Access input values
function init(self: MyNode): boolean
  print("Number:", self.myNumber)
  print("Color:", self.myColor)
  print("ViewModel property:", self.myViewModel.health.value)
  return true
end

-- Listen for changes
function init(self: MyNode): boolean
  self.myNumber:addListener(function()
    print("myNumber changed!")
  end)
  return true
end

-- Mark inputs assigned at runtime
return function(): Node<MyNode>
  return {
    init = init,
    myNumber = 0,
    myColor = Color.rgba(255, 255, 255, 255),
    myString = "default",
    myViewModel = late(),  -- Assigned via Editor
    enemyTemplate = late(),
  }
end
```

## Pointer Events

Handle touch/mouse interactions:

```lua
function pointerDown(self: MyNode, event: PointerEvent)
  print("Position:", event.position.x, event.position.y)
  print("Pointer ID:", event.id)  -- For multi-touch
  event:hit()  -- Mark as handled
end

function pointerMove(self: MyNode, event: PointerEvent)
  -- Handle drag
  event:hit()
end

function pointerUp(self: MyNode, event: PointerEvent)
  event:hit()
end

function pointerExit(self: MyNode, event: PointerEvent)
  event:hit()
end

return function(): Node<MyNode>
  return {
    pointerDown = pointerDown,
    pointerMove = pointerMove,
    pointerUp = pointerUp,
    pointerExit = pointerExit,
  }
end
```

## Dynamic Component Instantiation

Create artboard instances at runtime:

```lua
type Enemy = {
  artboard: Artboard<Data.Enemy>,
  position: Vec2D,
}

type GameScene = {
  enemyTemplate: Input<Artboard<Data.Enemy>>,
  enemies: { Enemy },
}

function createEnemy(self: GameScene, x: number, y: number)
  local enemy = self.enemyTemplate:instance()
  local entry: Enemy = {
    artboard = enemy,
    position = Vec2D.xy(x, y),
  }
  table.insert(self.enemies, entry)
end

function advance(self: GameScene, seconds: number): boolean
  for _, enemy in self.enemies do
    enemy.artboard:advance(seconds)
  end
  return true
end

function draw(self: GameScene, renderer: Renderer)
  for _, enemy in self.enemies do
    renderer:save()
    renderer:transform(Mat2D.fromTranslate(enemy.position.x, enemy.position.y))
    enemy.artboard:draw(renderer)
    renderer:restore()
  end
end
```

## Data Binding

Access View Model from scripts:

```lua
function init(self: MyNode, context: Context): boolean
  local vm = context:viewModel()
  
  -- Get properties
  local score = vm:getNumber('score')
  local name = vm:getString('playerName')
  
  -- Set values
  if score then
    score.value = 100
  end
  
  -- Listen for changes
  if score then
    score:addListener(function()
      print("Score changed to:", score.value)
    end)
  end
  
  -- Access nested view models
  local settings = vm:getViewModel('settings')
  local volume = settings:getNumber('volume')
  
  return true
end
```

## Drawing API

For complete API reference, see `@references/rive-scripting-api.md`.

### Path Operations

```lua
local path = Path.new()

-- Drawing commands
path:moveTo(Vec2D.xy(0, 0))
path:lineTo(Vec2D.xy(100, 0))
path:quadTo(Vec2D.xy(150, 50), Vec2D.xy(100, 100))
path:cubicTo(Vec2D.xy(75, 150), Vec2D.xy(25, 150), Vec2D.xy(0, 100))
path:close()

-- Reset path for reuse
path:reset()

-- Measure path
local length = path:measure()
local contours = path:contours()
```

### Paint Configuration

```lua
local paint = Paint.new()
paint.style = 'fill'  -- or 'stroke'
paint.color = Color.rgba(255, 128, 0, 255)
paint.thickness = 3  -- For strokes
paint.cap = 'round'  -- 'butt', 'round', 'square'
paint.join = 'round' -- 'miter', 'round', 'bevel'
paint.blendMode = 'srcOver'

-- Gradient fills
paint.gradient = Gradient.linear(
  Vec2D.xy(0, 0),
  Vec2D.xy(100, 100),
  { GradientStop.new(0, Color.hex('#FF0000')),
    GradientStop.new(1, Color.hex('#0000FF')) }
)
```

### Renderer Operations

```lua
function draw(self: MyNode, renderer: Renderer)
  renderer:save()
  
  -- Transform
  renderer:transform(Mat2D.fromScale(2, 2))
  renderer:transform(Mat2D.fromRotation(math.pi / 4))
  renderer:transform(Mat2D.fromTranslate(50, 50))
  
  -- Draw path
  renderer:drawPath(self.path, self.paint)
  
  -- Draw image
  renderer:drawImage(self.image, ImageSampler.linear, 'srcOver', 1.0)
  
  -- Clipping
  renderer:clipPath(self.clipPath)
  
  renderer:restore()
end
```

## React/Next.js Runtime Reference

For detailed runtime API, see `@references/rive-react-runtime.md`.

### Installation

```bash
# Recommended
npm install @rive-app/react-canvas

# Alternative options
npm install @rive-app/react-canvas-lite  # Smaller, no Rive Text
npm install @rive-app/react-webgl         # WebGL renderer
npm install @rive-app/react-webgl2        # Rive Renderer (WebGL2)
```

### useRive Hook

```tsx
import { useRive, useStateMachineInput } from '@rive-app/react-canvas';

function Animation() {
  const { rive, RiveComponent } = useRive({
    src: '/animation.riv',
    artboard: 'MainArtboard',
    stateMachines: 'StateMachine1',
    autoplay: true,
    layout: new Layout({
      fit: Fit.Contain,
      alignment: Alignment.Center,
    }),
  });

  // Playback control
  const play = () => rive?.play();
  const pause = () => rive?.pause();
  const stop = () => rive?.stop();

  return (
    <RiveComponent 
      style={{ width: '100%', height: '100vh' }}
      onMouseEnter={() => rive?.play()}
    />
  );
}
```

### State Machine Inputs

```tsx
function InteractiveAnimation() {
  const { rive, RiveComponent } = useRive({
    src: '/interactive.riv',
    stateMachines: 'Controls',
    autoplay: true,
  });

  useEffect(() => {
    if (!rive) return;
    
    const inputs = rive.stateMachineInputs('Controls');
    
    // Number input
    const progress = inputs?.find(i => i.name === 'progress');
    if (progress) progress.value = 50;
    
    // Boolean input
    const isActive = inputs?.find(i => i.name === 'isActive');
    if (isActive) isActive.value = true;
    
    // Trigger input
    const onClick = inputs?.find(i => i.name === 'onClick');
    onClick?.fire();
  }, [rive]);

  return <RiveComponent />;
}
```

### Scroll-Based Animation

```tsx
function ScrollAnimation() {
  const { rive, RiveComponent } = useRive({
    src: '/scroll-animation.riv',
    stateMachines: 'ScrollMachine',
    autoplay: true,
  });
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!rive) return;
    
    const progressInput = rive.stateMachineInputs('ScrollMachine')
      ?.find(i => i.name === 'scrollProgress');
    
    const handleScroll = () => {
      if (!containerRef.current || !progressInput) return;
      
      const rect = containerRef.current.getBoundingClientRect();
      const windowHeight = window.innerHeight;
      
      // Calculate scroll progress (0-100)
      const progress = Math.max(0, Math.min(100,
        ((windowHeight - rect.top) / (windowHeight + rect.height)) * 100
      ));
      
      progressInput.value = progress;
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [rive]);

  return (
    <div ref={containerRef} style={{ height: '200vh' }}>
      <div style={{ position: 'sticky', top: 0, height: '100vh' }}>
        <RiveComponent style={{ width: '100%', height: '100%' }} />
      </div>
    </div>
  );
}
```

### Event Handling

```tsx
function AnimationWithEvents() {
  const { rive, RiveComponent } = useRive({
    src: '/events.riv',
    stateMachines: 'Main',
    autoplay: true,
  });

  useEffect(() => {
    if (!rive) return;
    
    // Listen for Rive events
    rive.on('statechange', (event) => {
      console.log('State changed:', event.data);
    });
    
    rive.on('riveevent', (event) => {
      console.log('Rive event:', event.data.name);
    });
  }, [rive]);

  return <RiveComponent />;
}
```

## Animation API Reference

### Animation Object

```lua
local anim = artboard:animation('AnimationName')

-- Control
anim:advance(0.016)  -- Advance by time in seconds
anim:setTime(1.5)    -- Set time in seconds
anim:setTimeFrames(30)  -- Set time in frames
anim:setTimePercentage(0.5)  -- Set time as 0-1

-- Properties
local duration = anim.duration
```

### Artboard Object

```lua
local artboard = self.myArtboard:instance()

-- Properties
artboard.width = 400
artboard.height = 300
artboard.frameOrigin = true

-- Control
artboard:advance(seconds)
artboard:draw(renderer)

-- Access nodes and bounds
local node = artboard:node('NodeName')
local minPt, maxPt = artboard:bounds()

-- Pointer events
artboard:pointerDown(event)
artboard:pointerUp(event)
artboard:pointerMove(event)
```

## Best Practices

### Performance

1. **Reuse paths and paints**: Create in `init()`, reuse in `draw()`
2. **Use fixed timestep**: For consistent physics across devices
3. **Minimize state machine inputs**: Batch updates when possible
4. **Lazy load .riv files**: Especially for multiple animations

### Code Organization

1. **Separate concerns**: Use different scripts for different behaviors
2. **Use View Models**: For complex state management
3. **Type your scripts**: Leverage Luau's type system

### Scroll Animations

1. **Use `scrollProgress` input**: Map scroll position to 0-100 range
2. **Debounce scroll handlers**: Prevent performance issues
3. **Use `sticky` positioning**: For scroll-triggered scenes
4. **Consider Intersection Observer**: For triggering animations on visibility

## Troubleshooting

### Common Issues

1. **Script not in list**: Check Assets Panel and Problems Panel
2. **Animation not playing**: Verify `autoplay` and state machine name
3. **Inputs not updating**: Ensure input names match exactly
4. **Performance issues**: Check for excessive path resets or redraws

### Debug Tools

```lua
-- In scripts
print("Debug:", value)

-- Check Problems Panel in Rive Editor
-- Use Debug Panel for runtime inspection
```

## Additional Resources

- Official Docs: https://rive.app/docs
- React Runtime: https://github.com/rive-app/rive-react
- Community: https://community.rive.app
- Discord: https://discord.com/invite/FGjmaTr

### Reference Documentation

For detailed API reference and guides, see:

**Scripting & Core**
- `@references/rive-scripting-api.md` - Complete Luau scripting API

**Editor Features**
- `@references/rive-editor-fundamentals.md` - Interface, artboards, shapes, components
- `@references/rive-animation-mode.md` - Timeline, keyframes, easing, animation mixing
- `@references/rive-state-machine.md` - States, inputs, transitions, listeners, layers
- `@references/rive-constraints.md` - IK, Distance, Transform, Follow Path constraints
- `@references/rive-layouts.md` - Flexbox-like layouts, N-Slicing, scrolling
- `@references/rive-manipulating-shapes.md` - Bones, meshes, clipping, joysticks
- `@references/rive-text.md` - Fonts, text runs, modifiers, styles
- `@references/rive-events.md` - Rive events, audio events, runtime listening
- `@references/rive-data-binding.md` - View Models, lists, runtime data binding

**Web Runtimes**
- `@references/rive-react-runtime.md` - React/Next.js integration
- `@references/rive-web-runtime.md` - Vanilla JS, Canvas, WebGL, WASM

**Mobile Runtimes**
- `@references/rive-flutter-runtime.md` - Flutter widgets and controllers
- `@references/rive-mobile-runtimes.md` - iOS (Swift), Android (Kotlin), React Native

**Game Engine Runtimes**
- `@references/rive-game-runtimes.md` - Unity, Unreal Engine, Defold
