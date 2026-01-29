---
name: lib-slint-expert
description: Comprehensive Slint GUI development expert based on official source code. Covers Rust integration, component design, layouts, styling, animations, cross-platform deployment, and performance optimization. Use when working with Slint UI toolkit, building native GUI applications, or when mentioning Slint, GUI development, or Rust user interfaces. Built with official documentation and examples.
category: gui-development
tags:
  - slint
  - rust
  - gui
  - ui-toolkit
  - cross-platform
  - native-ui
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Slint GUI Expert

A comprehensive guide for developing modern GUI applications using Slint with Rust. This skill is built directly from the official Slint repository and covers everything from basic component creation to advanced performance optimization and cross-platform deployment.

## 🎯 Getting Started with Official Tutorial

The best way to start is by following the official tutorial:

1. **Start Here**: `@source/docs/astro/src/content/docs/tutorial/quickstart.mdx`
2. **Basic Project**: Use `templates/basic-app/`
3. **Example Study**: Review `@source/examples/memory/`
4. **Reference**: Browse `@source/examples/gallery/`

### Quick Start with Template

```bash
# Use our pre-configured template
cp -r templates/basic-app/ my-first-slint-app/
cd my-first-slint-app/
cargo run
```

## Quick Start

### Basic Slint Application

```rust
// Cargo.toml
[dependencies]
slint = "1.13"

// main.rs
slint::slint! {
    export component AppWindow inherits Window {
        Text {
            text: "Hello, Slint!";
            color: #3498db;
            font-size: 24px;
            horizontal-alignment: center;
        }
    }
}

fn main() -> Result<(), slint::PlatformError> {
    let app = AppWindow::new()?;
    app.run()
}
```

### Project Structure

```
my-slint-app/
├── Cargo.toml
├── build.rs
└── src/
    ├── main.rs
    └── ui/
        └── main.slint
```

## Core Concepts

### 1. Component Architecture

**Component Definition**
```slint
// Define reusable components
export component Button inherits Rectangle {
    // Properties
    property <string> text: "Click me";
    property <color> background-color: #3498db;
    property <bool> enabled: true;

    // Callbacks
    callback clicked();

    // Layout and styling
    background: background-color;
    border-radius: 8px;

    // Content
    Text {
        text: root.text;
        color: enabled ? white : #cccccc;
        horizontal-alignment: center;
        vertical-alignment: center;
    }

    // Interactions
    TouchArea {
        enabled: root.enabled;
        clicked => { root.clicked(); }
    }
}

// Usage
export component MainWindow inherits Window {
    Button {
        text: "Submit";
        y: 100px;
        clicked => { /* handle click */ }
    }
}
```

**Rust Integration**
```rust
slint::include_modules!(); // Include .slint files

fn main() -> Result<(), slint::PlatformError> {
    let main_window = MainWindow::new()?;

    // Set up callbacks
    let window_weak = main_window.as_weak();
    main_window.on_submit_clicked(move || {
        let window = window_weak.unwrap();
        // Handle button click
        println!("Submit button clicked!");
    });

    main_window.run()
}
```

### 2. Layout Systems

**VerticalLayout**
```slint
export component LoginScreen inherits Window {
    VerticalLayout {
        spacing: 20px;
        padding: 40px;

        Text {
            text: "Login";
            font-size: 32px;
            font-weight: bold;
        }

        TextInput {
            placeholder-text: "Username";
            height: 40px;
        }

        TextInput {
            placeholder-text: "Password";
            height: 40px;
        }

        Button {
            text: "Login";
            height: 45px;
            clicked => { /* login logic */ }
        }
    }
}
```

**GridLayout**
```slint
export component Dashboard inherits Window {
    GridLayout {
        spacing: 10px;
        padding: 20px;

        Row[ 1, 2, 3 ] {
            Column[ 1 ] {
                Text { text: "Revenue"; }
                Text { text: "$10,234"; font-size: 24px; }
            }

            Column[ 2 ] {
                Text { text: "Users"; }
                Text { text: "1,024"; font-size: 24px; }
            }

            Column[ 3 ] {
                Text { text: "Orders"; }
                Text { text: "847"; font-size: 24px; }
            }
        }
    }
}
```

### 3. Data Binding and State Management

**Properties and Bindings**
```slint
export component Counter inherits Window {
    property <int> count: 0;
    property <string> status: count > 10 ? "High" : "Low";

    VerticalLayout {
        Text {
            text: "Count: " + count;
            font-size: 24px;
        }

        Text {
            text: "Status: " + status;
            color: count > 10 ? red : green;
        }

        HorizontalLayout {
            spacing: 10px;

            Button {
                text: "+";
                width: 50px;
                clicked => { count += 1; }
            }

            Button {
                text: "-";
                width: 50px;
                clicked => { count -= 1; }
            }
        }
    }
}
```

**Rust State Integration**
```rust
use slint::{SharedString, ModelRc, VecModel};

fn main() -> Result<(), slint::PlatformError> {
    let app = MainWindow::new()?;

    // Create data model
    let items = VecModel::from(vec![
        SharedString::from("Item 1"),
        SharedString::from("Item 2"),
        SharedString::from("Item 3"),
    ]);

    app.set_items(ModelRc::new(items));

    // Add new items from Rust
    let window_weak = app.as_weak();
    app.on_add_item(move || {
        let window = window_weak.unwrap();
        let current_items = window.get_items();

        if let Some(vec_model) = current_items.any_model().downcast::<VecModel<SharedString>>() {
            let new_item = format!("Item {}", vec_model.row_count() + 1);
            vec_model.push(SharedString::from(new_item));
        }
    });

    app.run()
}
```

### 4. Styling and Themes

**Custom Styling**
```slint
import { Button, StyleMetrics } from "std-widgets.slint";

export component ThemedApp inherits Window {
    // Define custom colors
    @theme.primary := #3498db;
    @theme.secondary := #2ecc71;
    @theme.background := #ecf0f1;
    @theme.text := #2c3e50;

    style := StyleMetrics.dark ? dark-style : light-style;

    global DarkStyle {
        @theme.primary := #2980b9;
        @theme.secondary := #27ae60;
        @theme.background := #34495e;
        @theme.text := #ecf0f1;
    }

    background: @theme.background;

    VerticalLayout {
        padding: 20px;

        Text {
            text: "Themed Application";
            color: @theme.text;
            font-size: 24px;
        }

        Button {
            text: "Primary Action";
            background: @theme.primary;
            clicked => { /* action */ }
        }
    }
}
```

**Style Switching in Rust**
```rust
fn main() -> Result<(), slint::PlatformError> {
    let app = ThemedApp::new()?;

    let window_weak = app.as_weak();
    app.on_toggle_theme(move || {
        let window = window_weak.unwrap();
        let current_style = window.get_style();

        // Toggle between light and dark themes
        if current_style == "light" {
            window.set_style("dark");
        } else {
            window.set_style("light");
        }
    });

    app.run()
}
```

### 5. Animations and Transitions

**Property Animations**
```slint
export component AnimatedButton inherits Rectangle {
    property <color> hover-color: #3498db;
    property <length> scale: 1.0;

    background: hover-color;
    border-radius: 8px;

    animate scale { duration: 200ms; easing: ease-out; }
    animate hover-color { duration: 300ms; }

    TouchArea {
        mouse-cursor: pointer;

        mouse-entered => {
            root.scale = 1.1;
            root.hover-color = #2980b9;
        }

        mouse-exited => {
            root.scale = 1.0;
            root.hover-color = #3498db;
        }
    }
}
```

**Complex Animations**
```slint
export component LoadingSpinner inherits Rectangle {
    property <float> rotation: 0deg;

    width: 40px;
    height: 40px;
    border-width: 3px;
    border-color: #3498db;
    border-radius: 20px;
    clip: true;

    Rectangle {
        x: 0px;
        y: 0px;
        width: 20px;
        height: 20px;
        background: #3498db;
        border-radius: 10px;

        animate rotation {
            duration: 1s;
            loop: true;
            easing: linear;
        }
    }

    init => {
        rotation-animation.start();
    }

    animation rotation-animation := Animation {
        duration: 1s;
        loop: true;
        to {
            rotation: 360deg;
        }
    }
}
```

## Advanced Topics

### 1. Custom Components Library

**Component Library Structure**
```slint
// components/button.slint
export component PrimaryButton inherits Rectangle {
    property <string> text;
    property <bool> enabled: true;
    callback clicked;

    background: enabled ? #3498db : #bdc3c7;
    border-radius: 6px;

    Text {
        text: root.text;
        color: white;
        horizontal-alignment: center;
        vertical-alignment: center;
    }

    TouchArea {
        enabled: root.enabled;
        clicked => { root.clicked(); }
    }
}

// components/card.slint
export component Card inherits Rectangle {
    property <string> title;
    property <string> content;

    background: white;
    border-width: 1px;
    border-color: #ecf0f1;
    border-radius: 8px;
    elevation: 2dp;

    VerticalLayout {
        padding: 16px;
        spacing: 8px;

        Text {
            text: title;
            font-weight: bold;
            font-size: 18px;
        }

        Text {
            text: content;
            color: #7f8c8d;
            wrap: word-wrap;
        }
    }
}
```

### 2. Performance Optimization

**Efficient Rendering**
```slint
export component OptimizedList inherits Window {
    property <[ListItem]> items;

    ListView {
        for item in items : ListItem {
            height: 60px;

            Rectangle {
                background: even ? #f8f9fa : white;

                Text {
                    x: 16px;
                    text: item.title;
                    vertical-alignment: center;
                }
            }
        }
    }
}

// In Rust - implement efficient data models
use slint::{ModelRc, VecModel};

struct ListItem {
    title: String,
    // other fields
}

impl From<ListItem> for slint::ModelRc<slint::SharedString> {
    fn from(items: Vec<ListItem>) -> Self {
        let model = VecModel::from(
            items.into_iter()
                .map(|item| slint::SharedString::from(item.title))
                .collect()
        );
        ModelRc::new(model)
    }
}
```

**Memory Management**
```rust
// Use weak references to avoid circular references
let window_weak = app.as_weak();

// Clear models when no longer needed
app.on_cleanup(move || {
    if let Some(window) = window_weak.upgrade() {
        window.set_data_model(ModelRc::new(VecModel::default()));
    }
});

// Use resource pooling for frequently created components
struct ComponentPool {
    buttons: Vec<Rc<slint::ComponentHandle<ButtonComponent>>>,
}

impl ComponentPool {
    fn get_button(&mut self) -> Rc<slint::ComponentHandle<ButtonComponent>> {
        self.buttons.pop().unwrap_or_else(|| {
            Rc::new(ButtonComponent::new().unwrap())
        })
    }

    fn return_button(&mut self, button: Rc<slint::ComponentHandle<ButtonComponent>>) {
        self.buttons.push(button);
    }
}
```

### 3. Cross-Platform Development

**Platform-Specific Configuration**
```rust
// build.rs
fn main() {
    let mut config = slint_build::CompilerConfiguration::new();

    // Configure platform-specific features
    #[cfg(target_os = "windows")]
    {
        config = config.with_style("fluent");
    }

    #[cfg(target_os = "macos")]
    {
        config = config.with_style("native");
    }

    #[cfg(target_arch = "wasm32")]
    {
        config = config.with_style("material");
    }

    slint_build::compile_with_config("ui/main.slint", config).unwrap();
}
```

**WebAssembly Integration**
```rust
// main.rs
#[cfg(target_arch = "wasm32")]
use wasm_bindgen::prelude::*;

slint::include_modules!();

#[cfg_attr(target_arch = "wasm32", wasm_bindgen(start))]
pub fn main() {
    let main_window = MainWindow::new().unwrap();

    // WASM-specific setup
    #[cfg(target_arch = "wasm32")]
    {
        web_sys::window()
            .unwrap()
            .document()
            .unwrap()
            .body()
            .unwrap()
            .style()
            .set_property("margin", "0")
            .unwrap();
    }

    main_window.run().unwrap();
}
```

**Embedded/MCU Support**
```rust
#![no_std]
#![cfg_attr(not(feature = "simulator"), no_main)]

slint::include_modules!();

#[cfg_attr(not(feature = "simulator"), no_main)]
fn main() -> ! {
    mcu_board_support::init();

    let window = slint::platform::software_renderer::MinimalSoftwareWindow::new(
        slint::platform::software_renderer::RepaintBufferType::ReusedBuffer
    );

    let ui = MainWindow::new().unwrap();

    // Embedded-specific event loop
    loop {
        ui.window().draw_if_needed(|renderer| {
            renderer.render_by_line(&mut display_wrapper);
        });

        // Handle other embedded tasks
        mcu_board_support::delay_ms(16); // ~60 FPS
    }
}
```

## Best Practices

### 1. Code Organization

**Project Structure**
```
my-app/
├── Cargo.toml
├── build.rs
├── src/
│   ├── main.rs
│   ├── models/
│   │   ├── mod.rs
│   │   └── data.rs
│   ├── components/
│   │   ├── mod.rs
│   │   ├── button.rs
│   │   └── card.rs
│   └── ui/
│       ├── main.slint
│       ├── components/
│       │   ├── button.slint
│       │   └── card.slint
│       └── styles/
│           └── theme.slint
└── assets/
    ├── icons/
    └── images/
```

**Component Design Principles**
- Keep components focused and reusable
- Use properties for configuration
- Prefer composition over inheritance
- Implement proper error handling
- Use TypeScript-like naming conventions

### 2. Performance Guidelines

**Rendering Optimization**
- Use `clip: true` for complex shapes
- Avoid unnecessary property animations
- Implement efficient data models
- Use `ListView` for large datasets
- Minimize layout recalculations

**Memory Management**
- Use weak references for callbacks
- Clear models when components are destroyed
- Implement resource pooling for reusable components
- Avoid circular references between Rust and Slint

### 3. Testing Strategies

**Unit Testing**
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use slint_testing::*;

    #[test]
    fn test_button_click() {
        let app = TestApp::new().unwrap();

        // Simulate button click
        app.get_test_button().clicked().emit();

        // Verify state changes
        assert_eq!(app.get_click_count(), 1);
    }

    #[test]
    fn test_data_binding() {
        let app = TestApp::new().unwrap();
        app.set_input_text("Hello");

        assert_eq!(app.get_display_text(), "Hello");
    }
}
```

## Common Patterns

### 1. Form Handling

```slint
export component LoginForm inherits Window {
    callback login(string, string);

    property <string> username: "";
    property <string> password: "";
    property <bool> loading: false;

    VerticalLayout {
        spacing: 16px;
        padding: 24px;

        Text {
            text: "Login";
            font-size: 24px;
            font-weight: bold;
        }

        TextInput {
            text: username;
            placeholder-text: "Username";
            edited => { username = self.text; }
        }

        TextInput {
            text: password;
            placeholder-text: "Password";
            input-type: password;
            edited => { password = self.text; }
        }

        Button {
            text: loading ? "Logging in..." : "Login";
            enabled: !loading && username != "" && password != "";
            clicked => {
                loading = true;
                root.login(username, password);
            }
        }
    }
}
```

### 2. Navigation Pattern

```slint
export component NavigationContainer inherits Window {
    property <int> current-screen: 0;

    @screens := [
        HomeScreen {},
        SettingsScreen {},
        ProfileScreen {}
    ];

    @screen-titles := ["Home", "Settings", "Profile"];

    Rectangle {
        height: 60px;
        background: #3498db;

        HorizontalLayout {
            padding: 16px;

            for i in 0..3 : int {
                Button {
                    text: @screen-titles[i];
                    background: current-screen == i ? #2980b9 : transparent;
                    clicked => { current-screen = i; }
                }
            }
        }
    }

    Rectangle {
        y: 60px;
        height: parent.height - 60px;

        // Show current screen
        @screens[current-screen];
    }
}
```

## Integration Examples

### 1. Async Operations

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() -> Result<(), slint::PlatformError> {
    let app = AppWindow::new()?;
    let app_weak = app.as_weak();

    app.on_load_data(move || {
        let app_clone = app_weak.clone();

        thread::spawn(move || {
            // Simulate async operation
            thread::sleep(std::time::Duration::from_secs(2));

            // Update UI on main thread
            slint::invoke_from_event_loop(move || {
                if let Some(app) = app_clone.upgrade() {
                    app.set_loading(false);
                    app.set_data("Loaded data".into());
                }
            }).unwrap();
        });

        // Set loading state immediately
        if let Some(app) = app_weak.upgrade() {
            app.set_loading(true);
        }
    });

    app.run()
}
```

### 2. File Operations

```rust
use std::fs;

fn main() -> Result<(), slint::PlatformError> {
    let app = AppWindow::new()?;
    let app_weak = app.as_weak();

    app.on_save_file(move |content| {
        let app_clone = app_weak.clone();

        thread::spawn(move || {
            match fs::write("output.txt", content.as_str()) {
                Ok(()) => {
                    slint::invoke_from_event_loop(move || {
                        if let Some(app) = app_clone.upgrade() {
                            app.set_status("File saved successfully!".into());
                        }
                    }).unwrap();
                }
                Err(e) => {
                    let error_msg = format!("Failed to save: {}", e);
                    slint::invoke_from_event_loop(move || {
                        if let Some(app) = app_clone.upgrade() {
                            app.set_status(error_msg.into());
                        }
                    }).unwrap();
                }
            }
        });
    });

    app.run()
}
```

## 📚 Official Resources and Learning Materials

### 🎯 Primary Learning Path (Recommended)
1. **Official Tutorial**: `@source/docs/astro/src/content/docs/tutorial/` - Complete memory game tutorial
2. **Working Examples**: `@source/examples/memory/` - Tutorial implementation
3. **Component Reference**: `@source/examples/gallery/` - All UI components
4. **Language Guide**: `@source/docs/astro/src/content/docs/guide/language/` - Complete syntax reference

### 📖 Official Documentation
This skill includes the complete official Slint repository as a git submodule in the `source/` directory:

- **🎓 Tutorial**: `@source/docs/astro/src/content/docs/tutorial/` - Step-by-step learning
- **📋 Language**: `@source/docs/astro/src/content/docs/guide/language/` - Complete language specification
- **🔧 API**: `@source/api/rs/slint/` - Rust API documentation
- **💎 Examples**: `@source/examples/` - Extensive working examples
- **🎨 UI Libraries**: `@source/ui-libraries/` - Material & Fluent components
- **📚 Integration**: `@source/docs/astro/src/content/docs/language-integrations/` - Multiple language bindings

### 🛠️ Skill-Specific Resources
- **[docs/](docs/README.md)** - Navigation guide for official documentation
- **[examples/](examples/README.md)** - Curated learning paths with official examples
- **[templates/](templates/README.md)** - Ready-to-use project templates
- **[SOURCE_STRUCTURE.md](SOURCE_STRUCTURE.md)** - Complete skill structure mapping

### 🚀 Quick Start Templates
Based on official examples, ready for immediate use:

1. **`templates/basic-app/`** - Simple starter with counter demo
2. **`templates/component-library/`** - Reusable component system (planned)
3. **`templates/cross-platform/`** - Multi-platform deployment (planned)
4. **`templates/game-development/`** - Game development pattern (planned)

### Getting Started with Official Source
```bash
# Initialize the submodule (if not already done)
git submodule update --init --recursive

# Update to latest version
git submodule update --remote source

# Browse official examples
ls source/examples/

# View official documentation
ls source/docs/
```

## Troubleshooting

**Common Issues:**
- Compilation errors: Check `.slint` syntax and Rust integration
- Performance issues: Optimize layout complexity and data models
- Memory leaks: Use weak references and proper cleanup
- Platform-specific bugs: Test on target platforms early

**Debug Techniques:**
- Use `slint::debug_log!()` for logging
- Enable debug mode in build configuration
- Test with different rendering backends
- Profile memory usage and rendering performance