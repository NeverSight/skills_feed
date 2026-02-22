---
name: nodel-frontend
description: Build custom frontends and dashboards for Nodel nodes using index.xml, custom.css, custom.js, and XSL templates. Use when developing UI components for Nodel recipes.
---

# Nodel Frontend Development

## Frontend File Structure

A node's frontend is defined in its folder:

```
nodes/My Node/
├── script.py              # Node logic
├── nodeConfig.json        # Node config and bindings
└── content                # Web root
    ├── index.xml          # Frontend definition
    ├── css
    |   └── custom.css     # Custom styles (optional)
    └── js
        └── custom.js      # Custom JavaScript (optional)
```

## Basic Dashboard Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="v1/index.xsl"?>
<pages title='Dashboard Title' css='css/custom.css' js='js/custom.js'>
  <page title='Main'>
    <row>
      <column sm="6">
        <!-- Left column content -->
      </column>
      <column sm="6">
        <!-- Right column content -->
      </column>
    </row>
  </page>
  <page title='Settings'>
    <!-- Another page -->
  </page>
</pages>
```

### Root Attributes

| Attribute | Purpose |
|-----------|---------|
| `title` | Dashboard title in header |
| `theme` | Passed through to Bootstrap navbar classes and theme CSS selection |
| `logo` | Custom logo image path |
| `css` | Custom CSS file path |
| `js` | Custom JavaScript file path |
| `core` | Core/admin mode (skips custom `css` / `js` loading) |

## Layout System

### Grid System

Uses Bootstrap 3 grid (12 columns):

```xml
<row>
  <column sm="12">Full width on small+ screens</column>
</row>

<row>
  <column sm="6">Half width</column>
  <column sm="6">Half width</column>
</row>

<row>
  <column sm="3">Quarter</column>
  <column sm="3">Quarter</column>
  <column sm="3">Quarter</column>
  <column sm="3">Quarter</column>
</row>
```

Breakpoints:
- `xs` - Extra small (phones)
- `sm` - Small (tablets)
- `md` - Medium (desktops)
- `lg` - Large (large desktops)

### Groups

Visual grouping with background:

```xml
<group>
  <title>Power Control</title>
  <button action="Power" arg="On">Turn On</button>
  <button action="Power" arg="Off">Turn Off</button>
</group>
```

### Page Groups

Dropdown navigation for many pages:

```xml
<pagegroup title='Meeting Rooms'>
  <page title='Room A'>...</page>
  <page title='Room B'>...</page>
  <page title='Room C'>...</page>
</pagegroup>
```

## UI Components

See `references/components.md` for complete component reference.

Notes:
- Use `<image source='...'>` for images (`<img>` is not a supported component tag).
- `<input>` is header-only (place directly under `<header>`; checkbox is the built-in rendered type).
- `<footer>` should contain `<row>` children.

### Buttons

```xml
<!-- Simple action button -->
<button action='Power' arg='On' class='btn-success'>Turn On</button>

<!-- Confirmation before action -->
<button action='Reboot' confirm='true'>Reboot</button>

<!-- PIN confirmation -->
<button action='AdminMode' confirm='code' arg='true'>Unlock</button>

<!-- Momentary button (on while pressed) -->
<button type='momentary' action-on='VolumeUp' action-off='VolumeStop'>Vol +</button>

<!-- Multiple actions -->
<button action='["Action1","Action2","Action3"]'>Multiple</button>
```

### Button Groups

```xml
<buttongroup>
  <button action='Source' arg='HDMI1'>HDMI 1</button>
  <button action='Source' arg='HDMI2'>HDMI 2</button>
  <button action='Source' arg='DP1'>DisplayPort</button>
</buttongroup>
```

### Switches

```xml
<!-- On/Off toggle -->
<switch event='Power' action='Power' class='btn-primary'/>

<!-- Partial switch (shows current state) -->
<partialswitch event='Power' action='Power'/>

<!-- With confirmation -->
<partialswitch event='Power' action='Power' confirm='true'/>
```

### Pills (Radio Buttons)

```xml
<pills event='Source' action='Source'>
  <pill value='HDMI1'>HDMI 1</pill>
  <pill value='HDMI2'>HDMI 2</pill>
  <pill value='DP1'>DisplayPort</pill>
</pills>
```

### Select Dropdown

```xml
<select event='Source' action='Source' class='btn-default'>
  <item value='HDMI1'>HDMI 1</item>
  <item value='HDMI2'>HDMI 2</item>
  <item value='DP1'>DisplayPort</item>
</select>

<!-- Dynamic options from node -->
<dynamicselect data='SourceList' event='Source' action='Source'/>
```

### Range Slider

```xml
<!-- Basic slider -->
<range event='Volume' action='Volume' min='0' max='100'/>

<!-- With mute button -->
<range event='Volume' action='Volume' type='mute' min='0' max='100'/>

<!-- Vertical slider -->
<range event='Volume' action='Volume' type='vertical' height='250'/>

<!-- With nudge buttons -->
<range event='Volume' action='Volume' min='0' max='100' nudge='5'/>
```

Behavior details:
- `type='mute'` creates a mute toggle bound to `{baseName}Muting` (for `Volume`, bind `VolumeMuting`).
- `nudge` buttons only appear if `action` or `join` is present.

### Status Display

```xml
<!-- Status box with event binding -->
<status event='DeviceStatus'>Device Status</status>

<!-- With badge -->
<status event='Status1'>
  <badge event='OnlineStatus'/>
  Main Status
</status>

<!-- With link -->
<status event='Status'>
  <link url='http://device.local'>Open Device</link>
  Status text here
</status>
```

### Meters

```xml
<meter event='AudioLevel'/>
<meter event='CPUUsage'/>
<meter event='dBLevel' range='db'/>
```

### Text Display

```xml
<title>Section Title</title>
<subtitle>Section Subtitle</subtitle>
<text>Descriptive text here</text>
<field event='CurrentValue'/>
<panel height='100' event='LongText'/>
```

## Conditional Visibility

Show/hide elements based on event values:

```xml
<!-- Show only when Power is "On" -->
<button showevent='Power' showvalue='On' action='Settings'>Settings</button>

<!-- Show when Power is "On" OR "Standby" -->
<column showevent='Power' showvalue='["On","Standby"]'>
  ...
</column>

<!-- Column visibility -->
<column sm='6' event='AdminMode' value='true'>
  Admin-only controls
</column>
```

## Icons

Using Font Awesome icons:

```xml
<button action='Power' arg='On'>
  <icon lib='fa' type='power-off' style='fas'/>
</button>

<button action='VolumeUp'>
  <icon lib='fa' type='volume-up' size='2' style='fas'/>
</button>
```

Icon attributes:
- `lib` - Icon library (`fa` for Font Awesome)
- `type` - Icon name (e.g., `power-off`, `volume-up`)
- `style` - Icon style (`fas` solid, `far` regular)
- `size` - Size multiplier (1-5)

## Badges

Status indicators:

```xml
<button action='Source'>
  <badge event='SourceOnline'/>
  Select Source
</button>

<status event='MainStatus'>
  <badge event='SubStatus'/>
  <partialbadge event='PartialStatus'/>
  Status Text
</status>
```

## QR Codes

```xml
<qrcode text='https://example.com' height='128'/>
<qrcode event='DynamicURL' height='128' help='Scan to connect'/>
```

## Header Customization

```xml
<pages title='My Dashboard'>
  <header>
    <nodel type='nav'/>    <!-- Node navigation dropdown -->
    <nodel type='edit'/>   <!-- Edit functions dropdown -->
    <input type='checkbox' event='AdminMode' action='AdminMode'>Admin</input>
    <button action='Refresh'>Refresh</button>
  </header>
  ...
</pages>
```

## Custom Styling

### custom.css

```css
/* Override button colors */
.btn-power-on {
  background-color: #4CAF50;
}

/* Blur images until hover */
img {
  filter: blur(5px);
  transition: filter 0.3s ease;
}
img:hover {
  filter: blur(0);
}

/* Custom status colors */
.status-warning {
  background-color: #ff9800;
}
```

### custom.js

```javascript
// Add custom behavior
$(document).ready(function() {
  // Custom initialization
});

// Handle custom events
$(document).on('nodel-event', function(e, data) {
  console.log('Event:', data);
});
```

## Common Patterns

### Admin Lock

```xml
<button join='AdminEnabled' confirm='code' arg='true' showevent='AdminDisabled'>
  <icon lib='fa' type='lock' style='fas'/>
</button>
<button join='AdminEnabled' arg='false' showevent='AdminEnabled'>
  <icon lib='fa' type='lock-open' style='fas'/>
</button>
```

Supporting script.py code:
```python
local_event_AdminEnabled = LocalEvent({'schema': {'type': 'boolean'}})
local_event_AdminDisabled = LocalEvent({'schema': {'type': 'boolean'}})

@local_action({})
def AdminEnabled(arg):
    local_event_AdminEnabled.emit(arg)
    local_event_AdminDisabled.emit(not arg)
```

### Dynamic Button Group

```xml
<dynamicbuttongroup join='Source' data='sourceData' confirmtext='Switch source?'/>
```

### Multi-Page Dashboard

```xml
<pages title='AV Control'>
  <page title='Sources'>
    <!-- Source selection controls -->
  </page>
  <page title='Audio'>
    <!-- Audio controls -->
  </page>
  <page title='Lighting'>
    <!-- Lighting controls -->
  </page>
  <pagegroup title='Advanced'>
    <page title='Network'>...</page>
    <page title='Debug'>...</page>
  </pagegroup>
</pages>
```
