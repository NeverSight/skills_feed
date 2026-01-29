---
name: moving-rainbow
description: Generate MicroPython programs for the Moving Rainbow LED strip educational project using Raspberry Pi Pico with NeoPixel strips and button controls.
---

# Moving Rainbow MicroPython Program Generator

This skill helps create MicroPython programs for the Moving Rainbow educational project. Use this skill when the user asks to create LED animations, NeoPixel programs, or Moving Rainbow examples for Raspberry Pi Pico.

## Hardware Configuration

The default hardware setup consists of:
- **Microcontroller**: Raspberry Pi Pico (RP2040)
- **LED Strip**: 30-pixel NeoPixel/WS2812B addressable LED strip connected to GPIO pin 0
- **Input Controls**: Two momentary push buttons
  - Button 1: GPIO pin 14
  - Button 2: GPIO pin 15
- **Built-in LED**: GPIO pin 25 (can be used for status indication)

Configuration values are stored in a `config.py` file that should be imported by programs. See the `references/config.py` file for the standard configuration template.

## Code Structure and Patterns

### Basic Program Template

All programs should follow this structure:

```python
from machine import Pin
from neopixel import NeoPixel
from utime import sleep
import config

# Initialize the LED strip
strip = NeoPixel(Pin(config.NEOPIXEL_PIN), config.NUMBER_PIXELS)

# Your code here

while True:
    # Animation loop
    pass
```

### Essential Components

1. **Imports**: Always import from `machine`, `neopixel`, `utime`, and the `config` module
2. **Strip Initialization**: Create the NeoPixel object using configuration values
3. **Main Loop**: Use a `while True:` loop for continuous animations
4. **Color Format**: Colors are RGB tuples like `(red, green, blue)` with values 0-255

### Common Functions and Patterns

#### Color Wheel Function
For smooth rainbow transitions, use the standard color wheel function:

```python
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
```

#### Strip Control Patterns

**Setting pixels**:
```python
strip[index] = (red_value, green_value, blue_value)
strip.write()  # Always call write() to display changes
```

**Erasing the strip**:
```python
def erase():
    for i in range(0, config.NUMBER_PIXELS):
        strip[i] = (0, 0, 0)
    strip.write()
```

**Using a counter with modulo for wrapping**:
```python
counter = 0
while True:
    # Use counter for position
    strip[counter] = color
    strip.write()
    sleep(delay)

    counter += 1
    counter = counter % config.NUMBER_PIXELS  # Wrap around
```

### Button Integration

For interactive programs with button controls:

```python
from machine import Pin
from utime import ticks_ms
import config

BUTTON_PIN_1 = config.BUTTON_PIN_1
BUTTON_PIN_2 = config.BUTTON_PIN_2

button1 = Pin(BUTTON_PIN_1, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(BUTTON_PIN_2, Pin.IN, Pin.PULL_DOWN)

last_time = 0

def button_pressed_handler(pin):
    global mode, last_time
    new_time = ticks_ms()
    # Debounce: require 200ms between button presses
    if (new_time - last_time) > 200:
        pin_num = int(str(pin)[4:6])
        if pin_num == BUTTON_PIN_1:
            # Button 1 action (e.g., increment mode)
            mode += 1
        else:
            # Button 2 action (e.g., decrement mode)
            mode -= 1
        last_time = new_time

# Register interrupt handlers
button1.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed_handler)
button2.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed_handler)
```

### Common Animation Patterns

#### Moving Dot
```python
def move_dot(counter, color, delay):
    strip[counter] = color
    strip.write()
    sleep(delay)
    strip[counter] = (0, 0, 0)
```

#### Color Wipe
```python
def color_wipe(color, delay):
    for i in range(config.NUMBER_PIXELS):
        strip[i] = color
        strip.write()
        sleep(delay)
```

#### Rainbow Cycle
```python
def rainbow_cycle(counter, delay):
    percent_color_wheel = round(255 / config.NUMBER_PIXELS)
    for i in range(0, config.NUMBER_PIXELS):
        color_index = round(i * percent_color_wheel)
        color = wheel(color_index)
        strip[(i + counter) % config.NUMBER_PIXELS] = color
        strip.write()
    sleep(delay)
```

#### Comet Tail Effect
```python
def comet_tail(counter, color, tail_length, delay):
    levels = [255, 128, 64, 32, 16, 8, 4, 2, 1]
    for i in range(0, tail_length):
        target = (counter - i) % config.NUMBER_PIXELS
        scale = levels[i] / 255
        strip[target] = (int(color[0]*scale), int(color[1]*scale), int(color[2]*scale))
    strip.write()
    sleep(delay)
```

#### Random Effects
```python
from urandom import randint

def random_color(delay):
    random_offset = randint(0, config.NUMBER_PIXELS - 1)
    random_color_value = randint(0, 255)
    strip[random_offset] = wheel(random_color_value)
    strip.write()
    sleep(delay)
```

### Multi-Mode Programs

For programs with multiple animation modes that can be switched with buttons:

```python
mode_list = ['moving rainbow', 'red dot', 'blue dot', 'candle flicker', 'random']
mode_count = len(mode_list)
mode = 0
last_mode = -1

while True:
    # Print mode changes
    if mode != last_mode:
        print('mode=', mode, 'running', mode_list[mode])
        last_mode = mode

    # Execute the current mode
    if mode == 0:
        moving_rainbow(counter, 0.05)
    elif mode == 1:
        move_dot(counter, red, 0.05)
    # ... more modes

    counter += 1
    counter = counter % config.NUMBER_PIXELS
```

## Standard Color Definitions

Use these common color constants:

```python
red = (255, 0, 0)
orange = (255, 60, 0)
yellow = (255, 150, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
indigo = (75, 0, 130)
violet = (138, 43, 226)
white = (128, 128, 128)
off = (0, 0, 0)
```

## Educational Principles

When generating programs, follow these educational guidelines:

1. **Progressive Complexity**: Start simple and add features incrementally
2. **Clear Comments**: Explain what each section does for learning purposes
3. **Consistent Naming**: Use descriptive variable names (e.g., `counter`, `delay`, `color`)
4. **Visible Feedback**: Use print statements to show what's happening
5. **Adjustable Parameters**: Use constants for delays and other values so students can experiment

## Best Practices

1. **Always call `strip.write()`** after modifying pixels to display changes
2. **Use modulo for wrapping**: `counter % config.NUMBER_PIXELS` to loop animations
3. **Debounce buttons**: Check that at least 200ms has passed between button presses
4. **Import config**: Always use `import config` and reference `config.NEOPIXEL_PIN`, etc.
5. **Add delays**: Include appropriate `sleep()` calls to control animation speed
6. **Clear pixels**: Turn off pixels when moving animations to prevent trails
7. **Test boundary conditions**: Ensure animations work correctly at pixel 0 and the last pixel

## When to Use This Skill

Use this skill when:
- Creating LED animation programs for Raspberry Pi Pico
- Working with NeoPixel/WS2812B addressable LED strips
- Building educational examples for the Moving Rainbow project
- Implementing button-controlled LED effects
- Generating MicroPython code for LED strip projects

## Output Format

Generated programs should:
- Be complete, runnable MicroPython code
- Include necessary imports
- Use the config module for hardware settings
- Include helpful comments
- Follow the established code patterns
- Be educational and easy to understand
