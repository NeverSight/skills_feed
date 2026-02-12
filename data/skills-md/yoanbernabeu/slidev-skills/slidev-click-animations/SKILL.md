---
name: slidev-click-animations
description: Master v-click and sequential animations in Slidev. Use this skill to reveal content progressively and create engaging presentations.
---

# Click Animations in Slidev

This skill covers all click-based animations in Slidev, including v-click, v-after, v-clicks, v-switch, and motion directives for creating dynamic, engaging presentations.

## When to Use This Skill

- Revealing content step by step
- Building up complex diagrams
- Creating suspense or emphasis
- Guiding audience attention
- Interactive presentation flow

## v-click Basics

### Component Syntax

```markdown
<v-click>

This appears on the first click

</v-click>
```

### Directive Syntax

```markdown
<div v-click>
  This also appears on click
</div>
```

### Multiple v-clicks

```markdown
<v-click>First</v-click>
<v-click>Second</v-click>
<v-click>Third</v-click>
```

Each appears on successive clicks.

## Click Positioning

### Explicit Position

```markdown
<div v-click="1">Appears first</div>
<div v-click="3">Appears third</div>
<div v-click="2">Appears second</div>
```

### Relative Position

```markdown
<div v-click>First (click 1)</div>
<div v-click="'+1'">Second (click 2)</div>
<div v-click="'+2'">Fourth (click 4)</div>
```

### Same Click (v-after)

```markdown
<v-click>Main content</v-click>
<v-after>Appears with main content</v-after>
```

Or using relative position:

```markdown
<v-click>Main content</v-click>
<v-click="'+0'">Also appears with main</v-click>
```

## v-clicks for Lists

### Basic List Animation

```markdown
<v-clicks>

- First item
- Second item
- Third item

</v-clicks>
```

### Nested Lists

```markdown
<v-clicks depth="2">

- Parent 1
  - Child 1.1
  - Child 1.2
- Parent 2
  - Child 2.1

</v-clicks>
```

### Every N Items

```markdown
<v-clicks every="2">

- Items 1-2 together
- (same click)
- Items 3-4 together
- (same click)

</v-clicks>
```

## Hide on Click

### v-click.hide

```markdown
<div v-click.hide>This disappears on click</div>
```

### v-click with hide

```markdown
<v-click hide>
  This content will be hidden after the click
</v-click>
```

### Range-based Hiding

```markdown
<div v-click.hide="[2, 4]">
  Visible until click 2, hidden on clicks 2-3, visible again at click 4
</div>
```

## v-switch

Switch between different content based on clicks:

```markdown
<v-switch>
  <template #1>Content at click 1</template>
  <template #2>Content at click 2</template>
  <template #3>Content at click 3</template>
  <template #4-6>Content at clicks 4, 5, and 6</template>
  <template #default>Default content (before click 1)</template>
</v-switch>
```

### Practical Example

```markdown
<v-switch>
  <template #0>
    <h2>Step 1: Initialize</h2>
    <p>Set up the project structure</p>
  </template>
  <template #1>
    <h2>Step 2: Configure</h2>
    <p>Add configuration files</p>
  </template>
  <template #2>
    <h2>Step 3: Build</h2>
    <p>Run the build command</p>
  </template>
</v-switch>
```

## Motion Animations

### Basic Motion

```markdown
<div
  v-motion
  :initial="{ opacity: 0, y: 100 }"
  :enter="{ opacity: 1, y: 0 }"
>
  Slides up and fades in
</div>
```

### Motion with Clicks

```markdown
<div
  v-motion
  :initial="{ x: -100, opacity: 0 }"
  :enter="{ x: 0, opacity: 1 }"
  :click-1="{ scale: 1.2 }"
  :click-2="{ x: 100 }"
  :leave="{ opacity: 0 }"
>
  Complex motion sequence
</div>
```

### Motion Variants

| Variant | When Applied |
|---------|--------------|
| `initial` | Initial state |
| `enter` | When slide is entered |
| `click-N` | At click N |
| `click-N-M` | During clicks N to M |
| `leave` | When leaving slide |

### Motion Properties

```markdown
<div
  v-motion
  :initial="{
    opacity: 0,
    scale: 0.5,
    x: -200,
    y: 100,
    rotate: -45
  }"
  :enter="{
    opacity: 1,
    scale: 1,
    x: 0,
    y: 0,
    rotate: 0,
    transition: {
      duration: 500,
      ease: 'easeOut'
    }
  }"
>
  Animated element
</div>
```

## Click Counter Configuration

### Setting Total Clicks

```yaml
---
clicks: 5
---
```

Forces the slide to have exactly 5 clicks.

### Auto Clicks

```yaml
---
clicks: auto
---
```

Automatically determines click count (default).

## Styling Click States

### CSS Classes

When an element has `v-click`:
- `.slidev-vclick-target` - Always applied
- `.slidev-vclick-hidden` - When hidden
- `.slidev-vclick-current` - Currently active click
- `.slidev-vclick-prior` - Already revealed

### Custom Transitions

```css
/* styles/index.css */
.slidev-vclick-target {
  transition: all 0.5s ease;
}

.slidev-vclick-hidden {
  opacity: 0;
  transform: translateY(20px);
}
```

### Scale Animation

```css
.slidev-vclick-target {
  transition: all 0.3s ease;
}

.slidev-vclick-hidden {
  transform: scale(0);
  opacity: 0;
}
```

### Blur Effect

```css
.slidev-vclick-hidden {
  filter: blur(10px);
  opacity: 0;
}
```

## Practical Patterns

### Building a List

```markdown
# Key Points

<v-clicks>

1. **Performance** - Optimized for speed
2. **Security** - Built-in protection
3. **Scalability** - Handles growth
4. **Maintainability** - Clean architecture

</v-clicks>
```

### Progressive Diagram

```markdown
# Architecture

<div class="grid grid-cols-3 gap-4">
  <div v-click="1" class="box">Frontend</div>
  <div v-click="2" class="box">API</div>
  <div v-click="3" class="box">Database</div>
</div>

<Arrow v-click="4" x1="100" y1="100" x2="200" y2="100" />
<Arrow v-click="5" x1="300" y1="100" x2="400" y2="100" />
```

### Before/After Reveal

```markdown
# The Solution

<div v-click.hide="2">
  <h2>Before</h2>
  <pre>Old code here</pre>
</div>

<div v-click="2">
  <h2>After</h2>
  <pre>New improved code</pre>
</div>
```

### Animated Highlight

```markdown
# Important Concept

<p v-click="1">
  This is a paragraph with
  <span
    v-motion
    :initial="{ background: 'transparent' }"
    :click-2="{ background: '#fef08a' }"
    class="px-1"
  >
    highlighted text
  </span>
  that appears.
</p>
```

### Step-by-Step Code

````markdown
```typescript {1|2|3|all}
const name = 'Slidev'
const version = '0.50'
console.log(`${name} v${version}`)
```
````

## Best Practices

### 1. Don't Overuse

❌ **Too many clicks**
```markdown
<v-click>Word</v-click>
<v-click>by</v-click>
<v-click>word</v-click>
<v-click>is</v-click>
<v-click>annoying</v-click>
```

✓ **Meaningful groups**
```markdown
<v-click>First complete thought</v-click>
<v-click>Second complete thought</v-click>
```

### 2. Group Related Content

```markdown
<v-click>
  <h3>Feature A</h3>
  <p>Description of feature A</p>
</v-click>

<v-click>
  <h3>Feature B</h3>
  <p>Description of feature B</p>
</v-click>
```

### 3. Consider Timing

```markdown
<!-- Good for demos - immediate -->
<div v-click>Quick reveal</div>

<!-- Good for emphasis - animated -->
<div
  v-motion
  :initial="{ opacity: 0 }"
  :enter="{ opacity: 1, transition: { duration: 800 } }"
>
  Dramatic reveal
</div>
```

### 4. Use for Navigation Cues

```markdown
<v-click at="1">
  👉 First, we'll look at setup
</v-click>

<v-click at="2">
  👉 Then, we'll implement features
</v-click>

<v-click at="3">
  👉 Finally, we'll deploy
</v-click>
```

## Debugging Tips

1. **Check click count**: Look at the click counter in presenter mode
2. **Verify positions**: Use explicit positions when order matters
3. **Test all clicks**: Click through every animation before presenting
4. **Check CSS conflicts**: Custom styles might interfere

## Output Format

When creating click animations:

```markdown
# [Slide Title]

[Static introductory content if any]

<v-clicks>

- [Point revealed at click 1]
- [Point revealed at click 2]
- [Point revealed at click 3]

</v-clicks>

<v-click at="4">

[Conclusion that appears last]

</v-click>

---
CLICK SEQUENCE:
1. [What appears/happens]
2. [What appears/happens]
3. [What appears/happens]
4. [What appears/happens]

TOTAL CLICKS: [N]
```
