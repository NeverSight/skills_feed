---
name: karabiner
description: Configure Karabiner-Elements keyboard remapping using Goku EDN syntax. Use when creating keybindings, layers, simlayers, app-specific shortcuts, or modifying karabiner.edn.
---

# Karabiner (via Goku)

Configure macOS keyboard remapping with [GokuRakuJoudo](https://github.com/yqrashawn/GokuRakuJoudo) - an EDN-based DSL that compiles to Karabiner-Elements JSON.

## Why Goku?

Karabiner's native JSON is verbose (20,000+ lines). Goku's EDN format is 10-50x more concise:

```clojure
;; Goku: 1 line
[:caps_lock :escape]

;; Karabiner JSON: ~30 lines
```

## Prerequisites

```bash
# Install Goku
brew install yqrashawn/goku/goku

# Start as service (watches ~/.config/karabiner.edn)
brew services start goku

# Or run once manually
goku
```

Config location: `~/.config/karabiner.edn`

Logs: `~/Library/Logs/goku.log`

## EDN Syntax Quick Reference

### Basic Structure

```clojure
{:main [{:des "Rule description"
         :rules [[:from :to]
                 [:from2 :to2]]}]}
```

### Keycodes

All keys use keyword syntax: `:a`, `:1`, `:f19`, `:spacebar`, `:return_or_enter`

Find keycodes:
- Run Karabiner-EventViewer.app
- See [keys_info.clj](https://github.com/yqrashawn/GokuRakuJoudo/blob/master/src/karabiner_configurator/keys_info.clj)

### Modifier Syntax

| Symbol | Modifier | Example |
|--------|----------|---------|
| `!C` | Left Command | `:!Ca` = Cmd+A |
| `!T` | Left Control | `:!Ta` = Ctrl+A |
| `!O` | Left Option | `:!Oa` = Opt+A |
| `!S` | Left Shift | `:!Sa` = Shift+A |
| `!Q` | Right Command | `:!Qa` |
| `!W` | Right Control | `:!Wa` |
| `!E` | Right Option | `:!Ea` |
| `!R` | Right Shift | `:!Ra` |
| `!F` | Fn | `:!Fa` |
| `!P` | Caps Lock | `:!Pa` |
| `!!` | Hyper (Cmd+Ctrl+Opt+Shift) | `:!!a` |
| `##` | Optional any modifier | `:##a` |

Combine modifiers: `:!CTSa` = Cmd+Ctrl+Shift+A

### Rule Format

```clojure
[:from :to]                           ;; Basic
[:from :to :condition]                ;; With condition
[:from :to :condition {:alone :x}]    ;; With options
```

### Multiple Keys

```clojure
;; Press sequence
[:a [:1 :2 :3]]           ;; a -> types 1, 2, 3

;; Simultaneous press (from)
[[:j :k] :escape]         ;; j+k together -> escape
```

### Shell Commands

```clojure
[:!!1 "open -a Safari"]   ;; Hyper+1 runs shell command
```

---

## Conditions

### Application Conditions

```clojure
{:applications {:chrome ["^com\\.google\\.Chrome$"]
                :code   ["com.microsoft.VSCode"]}
 :main [{:des "Chrome only"
         :rules [[:a :b :chrome]]}]}
```

### Device Conditions

```clojure
{:devices {:hhkb [{:vendor_id 1278 :product_id 51966}]}
 :main [{:rules [[:a :b :hhkb]]}]}
```

### Input Source Conditions

```clojure
{:input-sources {:us {:input_source_id "com.apple.keylayout.US"}}
 :main [{:rules [[:a :b :us]]}]}
```

### Combining & Negating Conditions

```clojure
[:a :b [:chrome :hhkb]]    ;; Both conditions
[:a :b [:!chrome]]         ;; NOT in Chrome
```

---

## Layers

### Simlayers (Recommended)

Fast, simultaneous-key based layers - best for typing speed:

```clojure
{:simlayers {:w-mode {:key :w}}        ;; Hold W activates layer
 :main [{:des "w-mode shortcuts"
         :rules [:w-mode                ;; Apply to this layer
                 [:e "open -a Finder"]  ;; W+E opens Finder
                 [:r "open -a Safari"]  ;; W+R opens Safari
                 ]}]}
```

**Simlayer options:**
```clojure
{:simlayers {:w-mode {:key :w
                      :modi {:mandatory [:left_control]}}}}  ;; Ctrl+W activates
```

### Standard Layers (Tap/Hold)

Different behavior on tap vs hold:

```clojure
{:layers {:caps-mode {:key :caps_lock
                      :alone {:key :escape}}}}  ;; Tap=Esc, Hold=layer
```

### Manual Layer Variables

```clojure
;; Set variable on keydown, clear on keyup
[:w ["w-mode" 1] nil {:afterup ["w-mode" 0] :alone :w}]

;; Use the variable as condition
[:e :!Ce ["w-mode" 1]]  ;; W+E -> Cmd+E (only when w-mode=1)
```

---

## Templates

Reusable shell command patterns:

```clojure
{:templates {:open "open -a '%s'"
             :launch "/path/to/script.sh %s"
             :alfred "osascript -e 'tell application \"Alfred\" to run trigger \"%s\"'"}
 :main [{:rules [[:!!1 [:open "Safari"]]      ;; %s replaced with Safari
                 [:!!2 [:launch "arg1"]]]}]}
```

---

## Predefined Aliases

### :froms (Input Keys)

```clojure
{:froms {:delete {:key :delete_or_backspace}
         :return {:key :return_or_enter}
         :mouse1 {:pkey :button1}}}
```

### :tos (Output Actions)

```clojure
{:tos {:spotlight {:key :spacebar :modi :command}
       :paste {:key :v :modi :command}
       :shift-click {:pkey :button1 :modi :left_shift}}}
```

### Custom Modifier Sets

```clojure
{:modifiers {:hyper [:command :shift :control :option]
             :meh   [:shift :control :option]}}
```

---

## Advanced Options

Fourth position in rules:

```clojure
[:from :to :condition {
  :alone :key              ;; to_if_alone
  :held :key               ;; to_if_held_down
  :afterup :key            ;; to_after_key_up
  :delayed {:invoked :x :canceled :y}
  :params {:alone_timeout 200}
}]
```

---

## Profile Settings

```clojure
{:profiles {:Default {:default true
                      :sim 250        ;; Simultaneous threshold (ms)
                      :delay 500      ;; Delayed action time (ms)
                      :alone 1000     ;; to_if_alone timeout (ms)
                      :held 500}}}    ;; Held threshold (ms)
```

---

## Common Workflows

### Add a Simple Remap

```clojure
{:main [{:des "Caps to Escape"
         :rules [[:caps_lock :escape]]}]}
```

### Add App-Specific Shortcut

```clojure
{:applications {:chrome ["com.google.Chrome"]}
 :main [{:des "Chrome shortcuts"
         :rules [[:!Cl :!Ct :chrome]]}]}  ;; Cmd+L -> Cmd+T in Chrome
```

### Create a Layer

```clojure
{:simlayers {:nav {:key :spacebar}}
 :main [{:des "Navigation layer"
         :rules [:nav
                 [:h :left_arrow]
                 [:j :down_arrow]
                 [:k :up_arrow]
                 [:l :right_arrow]]}]}
```

### Hyper Key Setup

```clojure
{:main [{:des "Caps Lock to Hyper"
         :rules [[:caps_lock :!CTOSleft_shift nil {:alone :escape}]]}]}
```

---

## CLI Commands

```bash
goku           # Compile karabiner.edn once
gokuw          # Watch mode (compile on change)
goku -h        # Help

# Service management
brew services start goku    # Start watch service
brew services stop goku     # Stop service
brew services restart goku  # Restart after changes

# Check logs
tail -f ~/Library/Logs/goku.log
```

---

## Validation & Debugging

1. **Check syntax**: Goku reports EDN parse errors
2. **View output**: `~/.config/karabiner/karabiner.json`
3. **Use EventViewer**: Karabiner-EventViewer.app shows key events
4. **Check logs**: `tail ~/Library/Logs/goku.log`

---

## Best Practices

1. **Use simlayers** for frequently-accessed shortcuts (faster than hold-layers)
2. **Group rules by purpose** with descriptive `:des` tags
3. **Use templates** for repeated shell command patterns
4. **Define aliases** in `:froms`/`:tos` for complex key definitions
5. **Test incrementally** - add one rule, verify, repeat
6. **Back up your config** before major changes

---

## Resources

- [Tutorial](https://github.com/yqrashawn/GokuRakuJoudo/blob/master/tutorial.md)
- [Examples](https://github.com/yqrashawn/GokuRakuJoudo/blob/master/examples.org)
- [Configs in the wild](https://github.com/yqrashawn/GokuRakuJoudo/blob/master/in-the-wild.md)
- [Keycodes reference](https://github.com/yqrashawn/GokuRakuJoudo/blob/master/src/karabiner_configurator/keys_info.clj)
