---
name: flutter-flame-games
description: |
  Comprehensive guide for building 2D games with Flutter and Flame Engine. 
  Covers game architecture, sprites, animations, collision detection, 
  input handling (keyboard/joystick/gamepad), camera systems, Tiled maps, 
  audio, particles, and UI overlays. Use when creating or refactoring 
  Flutter games.
---

# Flame Game Development

Expert guidelines for building 2D games with Flutter and the Flame engine.

## Quick Start

When starting a new Flame game or reviewing code:

1. **Game Class**: Extend `FlameGame` with appropriate mixins (`HasCollisionDetection`, `HasKeyboardHandlerComponents`)
2. **Components**: Build entities with `SpriteComponent`, `PositionComponent`, or `SpriteAnimationComponent`
3. **Game Loop**: Implement `update(double dt)` for logic and `render(Canvas canvas)` for drawing
4. **Collision**: Add `CollisionCallbacks` mixin and define hitboxes (`CircleHitbox`, `RectangleHitbox`)
5. **Input**: Handle keyboard with `KeyboardHandler`, touch with `TapCallbacks`, joystick with `JoystickComponent`

## Project Setup

```bash
flutter create my_game
cd my_game
flutter pub add flame
```

For audio support:
```bash
flutter pub add flame_audio
```

For Tiled map support:
```bash
flutter pub add flame_tiled
```

### Assets Structure

```
assets/
├── images/
│   ├── player.png
│   ├── enemy_spritesheet.png
│   └── background.png
├── audio/
│   ├── bgm.mp3
│   └── sfx_jump.wav
└── tiles/
    └── map.tmx
```

Register in `pubspec.yaml`:
```yaml
flutter:
  assets:
    - assets/images/
    - assets/audio/
    - assets/tiles/
```

## Core Architecture

### Game Class Selection

**FlameGame** (Recommended for most games):
```dart
class MyGame extends FlameGame with HasCollisionDetection {
  @override
  Future<void> onLoad() async {
    await add(Player());
  }
}
```

**Low-level Game** (For custom implementations):
```dart
class MyGame extends Game {
  @override
  void render(Canvas canvas) { /* Custom rendering */ }
  
  @override
  void update(double dt) { /* Custom logic */ }
}
```

### Essential Mixins

| Mixin | Purpose |
|-------|---------|
| `HasCollisionDetection` | Enables collision system |
| `HasKeyboardHandlerComponents` | Allows keyboard input handling |
| `HasGameReference` | Provides access to game instance |

### Component Hierarchy

```
Component
├── PositionComponent
│   ├── SpriteComponent
│   ├── SpriteAnimationComponent
│   ├── TextComponent
│   └── ShapeComponent
├── ParticleSystemComponent
└── ParallaxComponent
```

### Component Lifecycle

```dart
class MyComponent extends PositionComponent {
  @override
  Future<void> onLoad() async {
    // Called once when added to game
    // Load assets, initialize state
  }
  
  @override
  void update(double dt) {
    // Called every frame
    // dt = delta time in seconds
  }
  
  @override
  void render(Canvas canvas) {
    // Called every frame for drawing
  }
  
  @override
  void onRemove() {
    // Cleanup before removal
  }
}
```

## Working with Sprites

### Static Sprite

```dart
class Player extends SpriteComponent {
  Player() : super(size: Vector2(64, 64), position: Vector2(100, 100));
  
  @override
  Future<void> onLoad() async {
    sprite = await Sprite.load('player.png');
  }
}
```

### Sprite from SpriteSheet

```dart
class Enemy extends SpriteComponent {
  @override
  Future<void> onLoad() async {
    final spriteSheet = await SpriteSheet.load(
      'enemies.png',
      srcSize: Vector2(32, 32),
    );
    sprite = spriteSheet.getSprite(0, 0); // row, column
  }
}
```

### PositionComponent (Custom Drawing)

```dart
class Circle extends PositionComponent {
  final Paint paint = Paint()..color = Colors.red;
  
  Circle() : super(size: Vector2.all(50));
  
  @override
  void render(Canvas canvas) {
    canvas.drawCircle(
      size.toOffset() / 2,
      size.x / 2,
      paint,
    );
  }
}
```

## Sprite Animation

### Basic Animation

```dart
class AnimatedPlayer extends SpriteAnimationComponent {
  AnimatedPlayer() : super(size: Vector2(64, 64));
  
  @override
  Future<void> onLoad() async {
    final spriteSheet = await SpriteSheet.load(
      'player_run.png',
      srcSize: Vector2(64, 64),
    );
    
    animation = spriteSheet.createAnimation(
      row: 0,
      stepTime: 0.1, // seconds per frame
      to: 8, // number of frames
    );
  }
}
```

### Multiple Animations

```dart
class Character extends SpriteAnimationComponent with HasGameReference {
  late final SpriteAnimation runAnimation;
  late final SpriteAnimation idleAnimation;
  late final SpriteAnimation jumpAnimation;
  
  @override
  Future<void> onLoad() async {
    final spritesheet = await game.images.load('character.png');
    
    runAnimation = _createAnimation(spritesheet, row: 0, frames: 8);
    idleAnimation = _createAnimation(spritesheet, row: 1, frames: 4);
    jumpAnimation = _createAnimation(spritesheet, row: 2, frames: 6);
    
    animation = idleAnimation;
  }
  
  SpriteAnimation _createAnimation(
    Image image, {
    required int row,
    required int frames,
  }) {
    return SpriteAnimation.fromFrameData(
      image,
      SpriteAnimationData.sequenced(
        amount: frames,
        amountPerRow: frames,
        textureSize: Vector2(64, 64),
        texturePosition: Vector2(0, row * 64),
        stepTime: 0.1,
      ),
    );
  }
  
  void run() => animation = runAnimation;
  void idle() => animation = idleAnimation;
  void jump() => animation = jumpAnimation;
}
```

## Collision Detection

### Basic Setup

```dart
// Game level
class MyGame extends FlameGame with HasCollisionDetection {
  @override
  Future<void> onLoad() async {
    add(Player());
    add(Enemy());
    add(ScreenHitbox()); // Boundary collision
  }
}

// Component level
class Player extends PositionComponent with CollisionCallbacks {
  @override
  Future<void> onLoad() async {
    add(CircleHitbox(radius: 20));
    // OR
    add(RectangleHitbox(size: Vector2(40, 40)));
    // OR
    add(PolygonHitbox([
      Vector2(0, 0),
      Vector2(20, 10),
      Vector2(0, 20),
    ]));
  }
  
  @override
  void onCollision(Set<Vector2> intersectionPoints, PositionComponent other) {
    if (other is Enemy) {
      takeDamage();
    }
  }
  
  @override
  void onCollisionStart(
    Set<Vector2> intersectionPoints,
    PositionComponent other,
  ) {
    // Called once when collision begins
  }
  
  @override
  void onCollisionEnd(PositionComponent other) {
    // Called once when collision ends
  }
}
```

### Collision Types

```dart
// Customize collision behavior
class MyHitbox extends CircleHitbox {
  MyHitbox() : super(radius: 20) {
    collisionType = CollisionType.passive; // Won't trigger collisions actively
    // Options: active, passive, inactive
  }
}
```

## Input Handling

### Keyboard Input

```dart
class Player extends SpriteComponent with KeyboardHandler {
  Vector2 velocity = Vector2.zero();
  double speed = 200;
  
  @override
  bool onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed) {
    velocity = Vector2.zero();
    
    if (keysPressed.contains(LogicalKeyboardKey.keyA)) {
      velocity.x = -1;
    }
    if (keysPressed.contains(LogicalKeyboardKey.keyD)) {
      velocity.x = 1;
    }
    if (keysPressed.contains(LogicalKeyboardKey.keyW)) {
      velocity.y = -1;
    }
    if (keysPressed.contains(LogicalKeyboardKey.keyS)) {
      velocity.y = 1;
    }
    
    return true;
  }
  
  @override
  void update(double dt) {
    position += velocity.normalized() * speed * dt;
  }
}
```

### Touch/Tap Input

```dart
class Button extends SpriteComponent with TapCallbacks {
  @override
  void onTapDown(TapDownEvent event) {
    scale = Vector2.all(0.9); // Visual feedback
  }
  
  @override
  void onTapUp(TapUpEvent event) {
    scale = Vector2.all(1.0);
    onPressed();
  }
  
  @override
  void onTapCancel(TapCancelEvent event) {
    scale = Vector2.all(1.0);
  }
  
  void onPressed() {
    // Handle button press
  }
}
```

### Drag Input

```dart
class DraggableObject extends PositionComponent with DragCallbacks {
  Vector2? dragStartPosition;
  Vector2? objectStartPosition;
  
  @override
  void onDragStart(DragStartEvent event) {
    dragStartPosition = event.localPosition;
    objectStartPosition = position.clone();
  }
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    if (dragStartPosition != null && objectStartPosition != null) {
      position = objectStartPosition! + event.localPosition - dragStartPosition!;
    }
  }
  
  @override
  void onDragEnd(DragEndEvent event) {
    dragStartPosition = null;
    objectStartPosition = null;
  }
}
```

## Camera System

### Camera Following Player

```dart
class MyGame extends FlameGame with HasCollisionDetection {
  late final Player player;
  
  @override
  Future<void> onLoad() async {
    final world = World();
    player = Player();
    
    await world.add(player);
    await add(world);
    
    camera = CameraComponent.withFixedResolution(
      world: world,
      width: 800,
      height: 600,
    );
    await add(camera);
    
    camera.follow(player);
  }
}
```

### Camera with Bounds

```dart
camera.follow(
  player,
  maxSpeed: 300,
  snap: false, // Smooth following
);

// Set world bounds
camera.setBounds(
  Rectangle.fromLTRB(0, 0, mapWidth, mapHeight),
);
```

### Zoom

```dart
// Zoom in
camera.viewfinder.zoom = 2.0;

// Animated zoom
await camera.viewfinder.zoomTo(2.0, speed: 2.0);
```

## Tiled Maps

### Loading Tiled Maps

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    final mapComponent = await TiledComponent.load(
      'map.tmx',
      Vector2(32, 32), // tile size
    );
    await add(mapComponent);
    
    // Access object layer
    final objectLayer = mapComponent.tileMap.getLayer<ObjectGroup>('objects');
    for (final object in objectLayer?.objects ?? []) {
      if (object.name == 'player_spawn') {
        add(Player(position: Vector2(object.x, object.y)));
      }
    }
  }
}
```

### Tile Collisions

```dart
// In Tiled editor, add custom property "collision" = true to tiles
// Then in code:

@override
Future<void> onLoad() async {
  final map = await TiledComponent.load('map.tmx', Vector2(32, 32));
  await add(map);
  
  // Generate collision blocks from tile layer
  final collisionLayer = map.tileMap.getLayer<TileLayer>('ground');
  final collisionBlocks = <PositionComponent>[];
  
  for (var y = 0; y < collisionLayer!.height; y++) {
    for (var x = 0; x < collisionLayer.width; x++) {
      final tile = collisionLayer.tileData![y][x];
      if (tile.tile > 0) {
        collisionBlocks.add(
          PositionComponent(
            position: Vector2(x * 32.0, y * 32.0),
            size: Vector2.all(32),
          )..add(RectangleHitbox()),
        );
      }
    }
  }
  
  addAll(collisionBlocks);
}
```

## Audio

### Background Music

```dart
import 'package:flame_audio/flame_audio.dart';

class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    await FlameAudio.audioCache.load('bgm.mp3');
    FlameAudio.bgm.initialize();
    FlameAudio.bgm.play('bgm.mp3', volume: 0.5);
  }
  
  @override
  void onRemove() {
    FlameAudio.bgm.dispose();
    super.onRemove();
  }
}
```

### Sound Effects

```dart
class Player extends PositionComponent {
  void jump() {
    FlameAudio.play('jump.wav', volume: 0.8);
    velocity.y = -300;
  }
  
  void collectCoin() {
    FlameAudio.play('coin.wav');
  }
}
```

## Particle Effects

### Basic Particle

```dart
import 'package:flame/particles.dart';

class Explosion extends ParticleSystemComponent {
  Explosion({required Vector2 position})
      : super(
          position: position,
          particle: Particle.generate(
            count: 20,
            lifespan: 0.5,
            generator: (i) => AcceleratedParticle(
              acceleration: Vector2.random() * 100,
              speed: Vector2.random() * 200,
              child: CircleParticle(
                radius: 4,
                paint: Paint()..color = Colors.orange,
              ),
            ),
          ),
        );
}
```

### Computed Particle (Custom)

```dart
Particle.generate(
  count: 12,
  lifespan: 1.0,
  generator: (i) {
    final angle = (i / 12) * 2 * pi;
    return ComputedParticle(
      renderer: (canvas, particle) {
        final progress = particle.progress;
        final radius = 10 * (1 - progress);
        final alpha = (1 - progress) * 255;
        
        canvas.drawCircle(
          Offset(cos(angle) * 50 * progress, sin(angle) * 50 * progress),
          radius,
          Paint()..color = Colors.red.withAlpha(alpha.toInt()),
        );
      },
    );
  },
)
```

## UI Overlays

### Setup

```dart
void main() {
  runApp(
    GameWidget(
      game: MyGame(),
      overlayBuilderMap: {
        'PauseMenu': (context, game) => PauseMenuOverlay(),
        'HUD': (context, game) => HudOverlay(game: game as MyGame),
      },
      initialActiveOverlays: const ['HUD'],
    ),
  );
}
```

### Show/Hide Overlays

```dart
class MyGame extends FlameGame {
  void showPauseMenu() {
    overlays.add('PauseMenu');
    pauseEngine();
  }
  
  void resumeGame() {
    overlays.remove('PauseMenu');
    resumeEngine();
  }
}
```

### HUD Example

```dart
class HudOverlay extends StatelessWidget {
  final MyGame game;
  
  const HudOverlay({required this.game});
  
  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<int>(
      valueListenable: game.score,
      builder: (context, score, child) {
        return Positioned(
          top: 20,
          left: 20,
          child: Text(
            'Score: $score',
            style: TextStyle(fontSize: 24, color: Colors.white),
          ),
        );
      },
    );
  }
}
```

## Parallax Backgrounds

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    final parallax = await loadParallaxComponent(
      [
        ParallaxImageData('bg_layer1.png'),
        ParallaxImageData('bg_layer2.png'),
        ParallaxImageData('bg_layer3.png'),
      ],
      baseVelocity: Vector2(50, 0),
      velocityMultiplierDelta: Vector2(1.5, 0),
    );
    
    add(parallax);
  }
}
```

## Joystick Component

```dart
class MyGame extends FlameGame {
  late final JoystickComponent joystick;
  late final Player player;
  
  @override
  Future<void> onLoad() async {
    player = Player();
    await add(player);
    
    joystick = JoystickComponent(
      knob: CircleComponent(
        radius: 20,
        paint: Paint()..color = Colors.red.withAlpha(200),
      ),
      background: CircleComponent(
        radius: 50,
        paint: Paint()..color = Colors.black.withAlpha(100),
      ),
      margin: const EdgeInsets.only(left: 40, bottom: 40),
    );
    await add(joystick);
  }
  
  @override
  void update(double dt) {
    if (joystick.direction != JoystickDirection.idle) {
      player.velocity = joystick.delta * 5;
    }
    super.update(dt);
  }
}
```

## Performance Best Practices

### Delta Time Usage

Always multiply movement/animation by `dt` for frame-rate independence:

```dart
@override
void update(double dt) {
  // Good - frame-rate independent
  position.x += speed * dt;
  
  // Bad - frame-rate dependent
  position.x += speed;
}
```

### Object Pooling

Reuse frequently created/destroyed objects:

```dart
class BulletPool {
  final List<Bullet> _available = [];
  final List<Bullet> _inUse = [];
  
  Bullet acquire() {
    if (_available.isEmpty) {
      return Bullet();
    }
    final bullet = _available.removeLast();
    _inUse.add(bullet);
    return bullet;
  }
  
  void release(Bullet bullet) {
    _inUse.remove(bullet);
    _available.add(bullet);
  }
}
```

### Cleanup

Always dispose resources:

```dart
class Player extends PositionComponent {
  late final SpriteAnimationTicker ticker;
  
  @override
  void onRemove() {
    ticker.dispose();
    super.onRemove();
  }
}
```

## References

For detailed guides on specific topics:

- **Components Deep Dive**: See [references/components.md](references/components.md)
- **Collision System**: See [references/collision-system.md](references/collision-system.md)
- **Input Handling**: See [references/input-handling.md](references/input-handling.md)
- **Camera & Tiled Maps**: See [references/camera-tiled.md](references/camera-tiled.md)
- **Audio & Particles**: See [references/audio-particles.md](references/audio-particles.md)
